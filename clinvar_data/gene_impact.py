"""Generate a report for each gene with variant count per impact and pathogenicity"""

import enum
import gzip
import json
import sys
import typing

import tqdm

from clinvar_data import models


@enum.unique
class Impact(enum.Enum):
    """SO terms for gene impact"""

    THREE_PRIME_UTR_VARIANT = "3_prime_UTR_variant"
    FIVE_PRIME_UTR_VARIANT = "5_prime_UTR_variant"
    DOWNSTREAM_TRANSCRIPT_VARIANT = "downstream_gene_variant"
    FRAMESHIFT_VARIANT = "frameshift_variant"
    INFRAME_INDEL = "inframe_indel"
    START_LOST = "start_lost"
    INTRON_VARIANT = "intron_variant"
    MISSENSE_VARIANT = "missense_variant"
    NON_CODING_TRANSCRIPT_VARIANT = "non_coding_transcript_variant"
    STOP_GAINED = "stop_gained"
    NO_SEQUENCE_ALTERATION = "no_sequence_alteration"
    SPLICE_ACCEPTOR_VARIANT = "splice_acceptor_variant"
    SPLICE_DONOR_VARIANT = "splice_donor_variant"
    STOP_LOST = "stop_lost"
    SYNONYMOUS_VARIANT = "synonymous_variant"
    UPSTREAM_TRANSCRIPT_VARIANT = "upstream_gene_variant"


#: Mapping from strings used in ClinVar XML to ``IMPACT``.
GENE_IMPACT_MAP = {
    "3 prime utr variant": Impact.THREE_PRIME_UTR_VARIANT,
    "5 prime utr variant": Impact.FIVE_PRIME_UTR_VARIANT,
    "downstream transcript variant": Impact.DOWNSTREAM_TRANSCRIPT_VARIANT,
    "frameshift variant": Impact.FRAMESHIFT_VARIANT,
    "genic downstream transcript variant": Impact.DOWNSTREAM_TRANSCRIPT_VARIANT,
    "genic upstream transcript variant": Impact.UPSTREAM_TRANSCRIPT_VARIANT,
    "inframe deletion": Impact.INFRAME_INDEL,
    "inframe indel": Impact.INFRAME_INDEL,
    "inframe insertion": Impact.INFRAME_INDEL,
    "initiatior codon variant": Impact.START_LOST,
    "intron variant": Impact.INTRON_VARIANT,
    "missense variant": Impact.MISSENSE_VARIANT,
    "non coding transcript variant": Impact.NON_CODING_TRANSCRIPT_VARIANT,
    "nonsense": Impact.STOP_GAINED,
    "no sequence alteration": Impact.NO_SEQUENCE_ALTERATION,
    "splice acceptor variant": Impact.SPLICE_ACCEPTOR_VARIANT,
    "splice donor variant": Impact.SPLICE_DONOR_VARIANT,
    "stop lost": Impact.STOP_LOST,
    "synonymous variant": Impact.SYNONYMOUS_VARIANT,
    "upstream transcript variant": Impact.UPSTREAM_TRANSCRIPT_VARIANT,
}

#: ACMG clinical significance values
ACMG_CLINSIGS = (
    models.ClinicalSignificanceDescription.BENIGN,
    models.ClinicalSignificanceDescription.LIKELY_BENIGN,
    models.ClinicalSignificanceDescription.UNCERTAIN_SIGNIFICANCE,
    models.ClinicalSignificanceDescription.LIKELY_PATHOGENIC,
    models.ClinicalSignificanceDescription.PATHOGENIC,
)


def zero_counts() -> typing.Dict[typing.Tuple[Impact, models.ClinicalSignificanceDescription], int]:
    return {(impact, pathogenicity): 0 for impact in Impact for pathogenicity in ACMG_CLINSIGS}


def write_report(counts: dict, path_output: str):
    """Write report to output."""

    if path_output.endswith(".gz"):
        outputf = gzip.open(path_output, "wt")
    else:
        outputf = open(path_output, "wt")

    with outputf:
        for hgnc, counts in sorted(counts.items(), key=lambda x: int(x[0][5:])):
            counts_out = {}
            for impact in Impact:
                arr = []
                for patho in ACMG_CLINSIGS:
                    arr.append(counts[(impact, patho)])
                if sum(arr) > 0:
                    counts_out[impact.value] = arr
            print(
                json.dumps({"hgnc": hgnc, "counts": counts_out}),
                file=outputf,
            )


def generate_counts(path_input: str) -> dict:
    """Count occurrences of each impact for each gene."""
    counts = {}

    if path_input.endswith(".gz"):
        inputf = gzip.open(path_input, "rt")
    else:
        inputf = open(path_input, "rt")

    with inputf:
        for line in tqdm.tqdm(inputf, desc="processing", unit=" JSONL records"):
            clinvar_set = models.ClinVarSet.model_validate_json(line)

            pathogenicity = (
                clinvar_set.reference_clinvar_assertion.clinical_significance.description
            )
            if not pathogenicity or not pathogenicity.is_canonical_acmg:
                continue  # skip not ACMG 1-5

            if not clinvar_set.reference_clinvar_assertion.measures:
                continue

            csq = None
            for measure in clinvar_set.reference_clinvar_assertion.measures.measures:
                for attribute in measure.attributes:
                    if attribute.type == models.MeasureAttributeType.MOLECULAR_CONSEQUENCE:
                        csq = attribute.value
                        break
            if not csq:
                continue  # skip, no molecular consequence
            else:
                csq = csq.lower().replace("_", " ").replace("-", " ")
                if csq not in GENE_IMPACT_MAP:
                    print(f"WARNING: unknown molecular consequence {csq}", file=sys.stderr)
                    continue

            hgnc = None
            for measure in clinvar_set.reference_clinvar_assertion.measures.measures:
                for measure_relationship in measure.measure_relationship:
                    for xref in measure_relationship.xrefs:
                        if xref.db == "HGNC":
                            hgnc = xref.id
                            break
            if not hgnc:
                continue  # skip, no HGNC ID

            if hgnc not in counts:
                counts[hgnc] = zero_counts()
            counts[hgnc][(GENE_IMPACT_MAP[csq], pathogenicity)] += 1
    return counts


def run_report(path_input: str, path_output: str):
    """Generate the report from the given input to output path."""
    counts = generate_counts(path_input)
    write_report(counts, path_output)
