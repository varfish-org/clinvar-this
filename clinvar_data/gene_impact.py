"""Generate a report for each gene with variant count per impact and pathogenicity"""

import gzip
import json
import sys
import typing

from google.protobuf.json_format import MessageToDict, ParseDict
import tqdm

from clinvar_data.pbs.clinvar_public_pb2 import VariationArchive
from clinvar_data.pbs.gene_impact import (
    ClinicalSignificance,
    GeneImpact,
    GeneImpactCounts,
)


class ConvertGeneImpact:
    """Static method helper for ``GeneImpact`` string to enum conversion."""

    #: Dict for conversion.
    CONVERT: dict[str, GeneImpact.ValueType] = {
        "3 prime utr variant": GeneImpact.GENE_IMPACT_THREE_PRIME_UTR_VARIANT,
        "5 prime utr variant": GeneImpact.GENE_IMPACT_FIVE_PRIME_UTR_VARIANT,
        "downstream transcript variant": GeneImpact.GENE_IMPACT_DOWNSTREAM_TRANSCRIPT_VARIANT,
        "frameshift variant": GeneImpact.GENE_IMPACT_FRAMESHIFT_VARIANT,
        "genic downstream transcript variant": GeneImpact.GENE_IMPACT_DOWNSTREAM_TRANSCRIPT_VARIANT,
        "genic upstream transcript variant": GeneImpact.GENE_IMPACT_UPSTREAM_TRANSCRIPT_VARIANT,
        "inframe deletion": GeneImpact.GENE_IMPACT_INFRAME_INDEL,
        "inframe indel": GeneImpact.GENE_IMPACT_INFRAME_INDEL,
        "inframe insertion": GeneImpact.GENE_IMPACT_INFRAME_INDEL,
        "initiatior codon variant": GeneImpact.GENE_IMPACT_START_LOST,
        "intron variant": GeneImpact.GENE_IMPACT_INTRON_VARIANT,
        "missense variant": GeneImpact.GENE_IMPACT_MISSENSE_VARIANT,
        "non coding transcript variant": GeneImpact.GENE_IMPACT_NON_CODING_TRANSCRIPT_VARIANT,
        "nonsense": GeneImpact.GENE_IMPACT_STOP_GAINED,
        "no sequence alteration": GeneImpact.GENE_IMPACT_NO_SEQUENCE_ALTERATION,
        "splice acceptor variant": GeneImpact.GENE_IMPACT_SPLICE_ACCEPTOR_VARIANT,
        "splice donor variant": GeneImpact.GENE_IMPACT_SPLICE_DONOR_VARIANT,
        "stop lost": GeneImpact.GENE_IMPACT_STOP_LOST,
        "synonymous variant": GeneImpact.GENE_IMPACT_SYNONYMOUS_VARIANT,
        "upstream transcript variant": GeneImpact.GENE_IMPACT_UPSTREAM_TRANSCRIPT_VARIANT,
    }

    @classmethod
    def from_str(cls, string_value: str) -> GeneImpact.ValueType:
        """Convert string to protobuf enum value."""
        return cls.CONVERT[string_value.lower()]


class ConvertClinicalSignificance:
    """Static method helper for ``ClinicalSignificance`` string to enum conversion."""

    #: Dict for conversion.
    CONVERT: dict[str, ClinicalSignificance.ValueType] = {
        "Pathogenic": ClinicalSignificance.CLINICAL_SIGNIFICANCE_PATHOGENIC,
        "Likely pathogenic": ClinicalSignificance.CLINICAL_SIGNIFICANCE_LIKELY_PATHOGENIC,
        "Uncertain significance": ClinicalSignificance.CLINICAL_SIGNIFICANCE_UNCERTAIN_SIGNIFICANCE,
        "Likely benign": ClinicalSignificance.CLINICAL_SIGNIFICANCE_LIKELY_BENIGN,
        "Benign": ClinicalSignificance.CLINICAL_SIGNIFICANCE_BENIGN,
    }

    @classmethod
    def from_str(cls, string_value: str) -> ClinicalSignificance.ValueType:
        """Convert string to protobuf enum value."""
        return cls.CONVERT.get(string_value, ClinicalSignificance.CLINICAL_SIGNIFICANCE_OTHER)


#: Canonical ACMG clinical significance values.
CANONICAL_CLINSIG = (
    ClinicalSignificance.CLINICAL_SIGNIFICANCE_BENIGN,
    ClinicalSignificance.CLINICAL_SIGNIFICANCE_LIKELY_BENIGN,
    ClinicalSignificance.CLINICAL_SIGNIFICANCE_UNCERTAIN_SIGNIFICANCE,
    ClinicalSignificance.CLINICAL_SIGNIFICANCE_LIKELY_PATHOGENIC,
    ClinicalSignificance.CLINICAL_SIGNIFICANCE_PATHOGENIC,
    ClinicalSignificance.CLINICAL_SIGNIFICANCE_OTHER,
)

#: Type variable for gene impact and significance.
KeyImpactSig = typing.Tuple[GeneImpact.ValueType, ClinicalSignificance.ValueType]
#: Counter dictionary.
PerGeneCounter = typing.Dict[KeyImpactSig, int]


def zero_counts() -> PerGeneCounter:
    """Returns counter from gene impact and clinical significance to zero count."""
    return {
        (v.number, clinsig): 0
        for v in GeneImpact.DESCRIPTOR.values
        for clinsig in CANONICAL_CLINSIG
    }


def write_report(
    counters: typing.Dict[str, PerGeneCounter],
    path_output: str,
):
    """Write report to output."""

    if path_output.endswith(".gz"):
        outputf = gzip.open(path_output, "wt")
    else:
        outputf = open(path_output, "wt")

    with outputf:
        for hgnc_id, counts in sorted(counters.items(), key=lambda x: int(x[0][5:])):
            record = GeneImpactCounts(hgnc_id=hgnc_id)
            for v in GeneImpact.DESCRIPTOR.values:
                if any([counts[(v.number, sig)] for sig in CANONICAL_CLINSIG]):
                    record.impact_counts.append(
                        GeneImpactCounts.ImpactCounts(
                            gene_impact=v.number,
                            count_benign=counts[
                                (v.number, ClinicalSignificance.CLINICAL_SIGNIFICANCE_BENIGN)
                            ],
                            count_likely_benign=counts[
                                (v.number, ClinicalSignificance.CLINICAL_SIGNIFICANCE_LIKELY_BENIGN)
                            ],
                            count_uncertain_significance=counts[
                                (
                                    v.number,
                                    ClinicalSignificance.CLINICAL_SIGNIFICANCE_UNCERTAIN_SIGNIFICANCE,
                                )
                            ],
                            count_likely_pathogenic=counts[
                                (
                                    v.number,
                                    ClinicalSignificance.CLINICAL_SIGNIFICANCE_LIKELY_PATHOGENIC,
                                )
                            ],
                            count_pathogenic=counts[
                                (v.number, ClinicalSignificance.CLINICAL_SIGNIFICANCE_PATHOGENIC)
                            ],
                        )
                    )
            print(json.dumps(MessageToDict(record)), file=outputf)


def generate_counts(path_input: str) -> dict:  # noqa: C901
    """Count occurrences of each impact for each gene."""
    counts: dict[str, dict[KeyImpactSig, int]] = {}

    if path_input.endswith(".gz"):
        inputf = gzip.open(path_input, "rt")
    else:
        inputf = open(path_input, "rt")

    with inputf:
        for line in tqdm.tqdm(inputf, desc="processing", unit=" JSONL records"):
            line_json = json.loads(line)
            va: VariationArchive = ParseDict(line_json, message=VariationArchive())

            # Obtain variant name, will start with submitted transcript.
            if not va.HasField("classified_record"):
                continue
            elif not va.classified_record.HasField("simple_allele"):
                continue
            variant_name: str = va.classified_record.simple_allele.name

            # Obtain germline classification description or skip record if has none.
            if not va.classified_record.HasField("classifications"):
                continue
            elif not va.classified_record.classifications.HasField("germline_classification"):
                continue
            elif not va.classified_record.classifications.germline_classification.HasField(
                "description"
            ):
                continue
            else:
                description: str = (
                    va.classified_record.classifications.germline_classification.description
                )
                pathogenicity: ClinicalSignificance.ValueType = (
                    ConvertClinicalSignificance.from_str(description)
                )

            # Obtain molecular consequence on transcript of variant name, skip if none.
            if not va.classified_record.simple_allele.hgvs_expressions:
                continue
            else:
                csq: str | None = None
                for expression in va.classified_record.simple_allele.hgvs_expressions:
                    if expression.HasField(
                        "nucleotide_expression"
                    ) and expression.nucleotide_expression.HasField("sequence_accession"):
                        sequence_accession: str = (
                            expression.nucleotide_expression.sequence_accession
                        )
                        if variant_name.startswith(sequence_accession):
                            for molecular_consequences in expression.molecular_consequences:
                                if molecular_consequences.type in ConvertGeneImpact.CONVERT:
                                    csq = molecular_consequences.type
                if not csq:
                    print(
                        f"Skipping variant {variant_name} due to no molecular consequence",
                        file=sys.stderr,
                    )
                    continue

            # Obtain gene HGNC ID
            hgnc_id: str | None = None
            for gene in va.classified_record.simple_allele.genes:
                if not gene.HasField("hgnc_id"):
                    continue
                else:
                    hgnc_id = gene.hgnc_id
                    break
            if not hgnc_id:
                print(
                    f"Skipping variant {variant_name} due to no HGNC ID",
                    file=sys.stderr,
                )
                continue

            if hgnc_id not in counts:
                counts[hgnc_id] = zero_counts()

            counts[hgnc_id][(ConvertGeneImpact.from_str(csq), pathogenicity)] += 1
    return counts


def run_report(path_input: str, path_output: str):
    """Generate the report from the given input to output path."""
    counts = generate_counts(path_input)
    write_report(counts, path_output)
