"""Determin ACMG class by frequency."""

import enum
import gzip
import json
import typing

import tqdm

from clinvar_data import models

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


@enum.unique
class Classes(enum.Enum):
    BENIGN = "benign"
    UNCERTAIN = "uncertain"
    PATHOGENIC = "pathogenic"


CLINSIG_TO_CLASS = {
    models.ClinicalSignificanceDescription.BENIGN: Classes.BENIGN,
    models.ClinicalSignificanceDescription.LIKELY_BENIGN: Classes.BENIGN,
    models.ClinicalSignificanceDescription.UNCERTAIN_SIGNIFICANCE: Classes.UNCERTAIN,
    models.ClinicalSignificanceDescription.LIKELY_PATHOGENIC: Classes.PATHOGENIC,
    models.ClinicalSignificanceDescription.PATHOGENIC: Classes.PATHOGENIC,
}


def zero_counts(count: int):
    return {klass: [0] * (count + 1) for klass in Classes}


def locate(thresholds: typing.List[float], value: typing.Optional[float]) -> int:
    if value is None:
        return 0
    for i, threshold in enumerate(thresholds):
        if value <= threshold:
            return i
    return len(thresholds)


def generate_counts(path_input: str, thresholds: typing.List[float]):
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

            if not clinvar_set.reference_clinvar_assertion.measures:
                continue
            freq = None
            for measure in clinvar_set.reference_clinvar_assertion.measures.measures:
                if measure.global_minor_allele_frequency:
                    freq = measure.global_minor_allele_frequency.value

            hgnc = None
            for measure in clinvar_set.reference_clinvar_assertion.measures.measures:
                for measure_relationship in measure.measure_relationship:
                    for xref in measure_relationship.xrefs:
                        if xref.db == "HGNC":
                            hgnc = xref.id
                            break

            if not hgnc or pathogenicity not in CLINSIG_TO_CLASS:
                continue

            if hgnc not in counts:
                counts[hgnc] = zero_counts(len(thresholds))

            idx = locate(thresholds, freq)
            counts[hgnc][CLINSIG_TO_CLASS[pathogenicity]][idx] += 1

    return counts


def write_report(counts: dict, path_output: str):
    if path_output.endswith(".gz"):
        outputf = gzip.open(path_output, "wt")
    else:
        outputf = open(path_output, "wt")

    with outputf:
        for hgnc, counts in sorted(counts.items(), key=lambda x: int(x[0][5:])):
            print(
                json.dumps({"hgnc": hgnc, "counts": counts}),  # type: ignore
                file=outputf,
            )


def run_report(path_input: str, path_output: str, thresholds: typing.List[float]):
    counts = generate_counts(path_input, thresholds)
    write_report(counts, path_output)
