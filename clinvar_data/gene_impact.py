"""Generate a report for each gene with variant count per impact and pathogenicity"""

import json

import tqdm

from clinvar_data import models
from clinvar_data.cattrs_helpers import CONVERTER


def run_report(path_input: str, path_output: str):
    with open(path_input, "rt") as inputf, open(path_output, "wt") as outputf:
        print("\t".join(["hgnc", "csq", "pathogenicity", "canonical_spdi"]), file=outputf)

        for line in tqdm.tqdm(inputf, unit="lines"):
            dict_value = json.loads(line)
            clinvar_set = CONVERTER.structure(dict_value, models.ClinVarSet)

            pathogenicity = (
                clinvar_set.reference_clinvar_assertion.clinical_significance.description
            )
            if not pathogenicity or not pathogenicity.is_canonical_acmg:
                continue  # skip not ACMG 1-5

            acc = clinvar_set.reference_clinvar_assertion.clinvar_accession.acc

            if not clinvar_set.reference_clinvar_assertion.measure_set:
                continue

            canonical_spdis_candidate = [
                measure.canonical_spdi
                for measure in clinvar_set.reference_clinvar_assertion.measure_set.measures
                if measure.canonical_spdi
            ][:1]
            canonical_spdi = canonical_spdis_candidate[0] if canonical_spdis_candidate else None

            csq = None
            for measure in clinvar_set.reference_clinvar_assertion.measure_set.measures:
                for attribute in measure.attributes:
                    if attribute.type == models.MeasureAttributeType.MOLECULAR_CONSEQUENCE:
                        csq = attribute.value
                        break
            if not csq:
                continue  # skip, no molecular consequence

            hgnc = None
            for measure in clinvar_set.reference_clinvar_assertion.measure_set.measures:
                for measure_relationship in measure.measure_relationship:
                    for xref in measure_relationship.xrefs:
                        if xref.db == "HGNC":
                            hgnc = xref.id
                            break
            if not hgnc:
                continue  # skip, no HGNC ID

            print(
                "\t".join(map(str, [hgnc, csq, pathogenicity.value, canonical_spdi, acc])),
                file=outputf,
            )
