"""Determin ACMG class by frequency."""

import gzip
import json
import typing

from google.protobuf.json_format import MessageToDict, Parse
import tqdm

from clinvar_data.pbs.class_by_freq import CoarseClinicalSignificance
from clinvar_data.pbs.class_by_freq_pb2 import GeneCoarseClinsigFrequencyCounts
from clinvar_data.pbs.clinvar_public_pb2 import VariationArchive

#: Default thresholds for frequency.
DEFAULT_THRESHOLDS = [
    0.0,
    1e-05,
    2.5e-05,
    5e-05,
    0.0001,
    0.00025,
    0.0005,
    0.001,
    0.0025,
    0.005,
    0.01,
    0.025,
    0.05,
    0.1,
    0.25,
    0.5,
    1.0,
]


class ConvertCoarseClinicalSignificance:
    """Static method helper for germline clinical significance summary string to coarse enum conversion."""

    #: Dict for conversion.
    CONVERT: dict[str, CoarseClinicalSignificance.ValueType] = {
        "Pathogenic": CoarseClinicalSignificance.COARSE_CLINICAL_SIGNIFICANCE_PATHOGENIC,
        "Pathogenic/Likely pathogenic": CoarseClinicalSignificance.COARSE_CLINICAL_SIGNIFICANCE_PATHOGENIC,
        "Likely pathogenic": CoarseClinicalSignificance.COARSE_CLINICAL_SIGNIFICANCE_PATHOGENIC,
        "Uncertain significance": CoarseClinicalSignificance.COARSE_CLINICAL_SIGNIFICANCE_UNCERTAIN,
        "Likely benign": CoarseClinicalSignificance.COARSE_CLINICAL_SIGNIFICANCE_BENIGN,
        "Benign": CoarseClinicalSignificance.COARSE_CLINICAL_SIGNIFICANCE_BENIGN,
        "Benign/Likely benign": CoarseClinicalSignificance.COARSE_CLINICAL_SIGNIFICANCE_BENIGN,
    }

    @classmethod
    def from_str(cls, string_value: str) -> CoarseClinicalSignificance.ValueType:
        """Convert string to protobuf enum value."""
        return cls.CONVERT.get(
            string_value, CoarseClinicalSignificance.COARSE_CLINICAL_SIGNIFICANCE_UNSPECIFIED
        )


def zero_counts(count: int):
    return {
        klass.number: [0] * (count + 1)
        for klass in CoarseClinicalSignificance.DESCRIPTOR.values
        if klass.number != CoarseClinicalSignificance.COARSE_CLINICAL_SIGNIFICANCE_UNSPECIFIED
    }


def locate(thresholds: typing.List[float], value: typing.Optional[float]) -> int:
    """Locate the index of the threshold that the value falls into."""
    if value is None:
        return 0
    for i, threshold in enumerate(thresholds):
        if value <= threshold:
            return i
    return len(thresholds)


def generate_counts(path_input: str, thresholds: typing.List[float]):
    """Generate counts from variant JSONL file."""
    counts = {}

    if path_input.endswith(".gz"):
        inputf = gzip.open(path_input, "rt")
    else:
        inputf = open(path_input, "rt")

    with inputf:
        for line in tqdm.tqdm(inputf, desc="processing", unit=" JSONL records"):
            va: VariationArchive = Parse(line, message=VariationArchive())

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
                pathogenicity: CoarseClinicalSignificance.ValueType = (
                    ConvertCoarseClinicalSignificance.from_str(description)
                )
            if pathogenicity == CoarseClinicalSignificance.COARSE_CLINICAL_SIGNIFICANCE_UNSPECIFIED:
                continue

            # Obtain minor allele frequency.
            gmaf: float | None = None
            if not va.HasField("classified_record"):
                continue
            elif not va.classified_record.HasField("simple_allele"):
                continue
            elif va.classified_record.simple_allele.HasField("global_minor_allele_frequency"):
                gmaf = va.classified_record.simple_allele.global_minor_allele_frequency.value

            # Try to get VCF location and skip unless is sequence variant.
            is_seqvar = False
            simple_allele = va.classified_record.simple_allele
            for location in simple_allele.locations or []:
                for sequence_location in location.sequence_locations or []:
                    if (
                        sequence_location.HasField("reference_allele")
                        and len(sequence_location.reference_allele) < 50
                        and sequence_location.HasField("alternate_allele")
                        and len(sequence_location.alternate_allele) < 50
                    ) or (
                        sequence_location.HasField("reference_allele_vcf")
                        and len(sequence_location.reference_allele_vcf) < 50
                        and sequence_location.HasField("alternate_allele_vcf")
                        and len(sequence_location.alternate_allele_vcf) < 50
                    ):
                        is_seqvar = True
                        break
            if not is_seqvar:
                continue

            # Obtain gene HGNC ID.
            hgnc_id: str | None = None
            for gene in va.classified_record.simple_allele.genes:
                if not gene.HasField("hgnc_id"):
                    continue
                else:
                    hgnc_id = gene.hgnc_id
                    break
            if not hgnc_id:
                continue

            if hgnc_id not in counts:
                counts[hgnc_id] = zero_counts(len(thresholds))

            idx = locate(thresholds, gmaf)
            counts[hgnc_id][pathogenicity][idx] += 1

    return counts


def write_report(counts: dict, path_output: str):
    """Write counts report to output."""
    if path_output.endswith(".gz"):
        outputf = gzip.open(path_output, "wt")
    else:
        outputf = open(path_output, "wt")

    with outputf:
        for hgnc_id, counts in sorted(counts.items(), key=lambda x: int(x[0][5:])):
            record: GeneCoarseClinsigFrequencyCounts = GeneCoarseClinsigFrequencyCounts(
                hgnc_id=hgnc_id,
                pathogenic_counts=counts[
                    CoarseClinicalSignificance.COARSE_CLINICAL_SIGNIFICANCE_PATHOGENIC
                ],
                uncertain_counts=counts[
                    CoarseClinicalSignificance.COARSE_CLINICAL_SIGNIFICANCE_UNCERTAIN
                ],
                benign_counts=counts[
                    CoarseClinicalSignificance.COARSE_CLINICAL_SIGNIFICANCE_BENIGN
                ],
            )
            print(
                json.dumps(MessageToDict(record)),
                file=outputf,
            )


def run_report(path_input: str, path_output: str, thresholds: typing.List[float]):
    counts = generate_counts(path_input, thresholds)
    write_report(counts, path_output)
