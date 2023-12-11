"""Generate JSONL with gene to phenotype/disease links"""

import gzip
import json
import typing

from pydantic import BaseModel, ConfigDict
import tqdm

from clinvar_data import models


class GenePhenotypeRecord(BaseModel):
    model_config = ConfigDict(frozen=True)

    #: RCV accession
    rcv: str
    #: RCV accession version
    rcv_version: int
    #: SCV accession
    scv: str
    #: SCV accession version
    scv_version: int
    #: Clinical significance
    clinsig: typing.Optional[models.ClinicalSignificanceDescription]
    #: Submitter
    submitter: typing.Optional[str]
    #: Gene HGNC ID
    hgnc_ids: typing.List[str]
    #: Linked OMIM terms
    omim_terms: typing.List[str]
    #: Linked MONDO terms
    mondo_terms: typing.List[str]
    #: Linked HPO terms
    hpo_terms: typing.List[str]


def clean_omim(terms: typing.Set[str]) -> typing.Set[str]:
    return {term.split(".")[0] for term in terms}


class TermCollector:
    def __init__(self):
        self.omim_terms = set()
        self.mondo_terms = set()
        self.hpo_terms = set()

    def add_xref(self, xref: models.Xref):
        if xref.db == "OMIM":
            self.omim_terms.add(xref.id)
        elif xref.db in ("Human Phenotype Ontology", "HP"):
            self.hpo_terms.add(xref.id)
        elif xref.db == "MONDO":
            self.mondo_terms.add(xref.id)

    def has_link(self) -> bool:
        return self.hpo_terms or self.omim_terms or self.mondo_terms


def run_report(path_input: str, path_output: str, needs_hpo_terms: bool = True):
    """Read in file at path_input and generate link records to path_output."""

    if path_input.endswith(".gz"):
        inputf = gzip.open(path_input, "rt")
    else:
        inputf = open(path_input, "rt")

    if path_output.endswith(".gz"):
        outputf = gzip.open(path_output, "wt")
    else:
        outputf = open(path_output, "wt")

    with inputf, outputf:
        for line in tqdm.tqdm(inputf, desc="processing", unit=" JSONL records"):
            clinvar_set = models.ClinVarSet.model_validate_json(line)
            rca = clinvar_set.reference_clinvar_assertion
            rcv = rca.clinvar_accession.acc
            rcv_version = rca.clinvar_accession.version

            hgnc_ids = set()
            if rca.measures:
                for measure in rca.measures.measures or []:
                    for measure_relationship in measure.measure_relationship:
                        hgnc_ids |= {
                            xref.id for xref in measure_relationship.xrefs if xref.db == "HGNC"
                        }

            for ca in clinvar_set.clinvar_assertions or []:
                clinsig = None
                for clinical_significance in ca.clinical_significance:
                    for description in clinical_significance.descriptions:
                        if description in (
                            models.ClinicalSignificanceDescription.PATHOGENIC,
                            models.ClinicalSignificanceDescription.LIKELY_PATHOGENIC,
                        ):
                            clinsig = description
                            break

                scv = ca.clinvar_accession.acc
                scv_version = ca.clinvar_accession.version

                terms = TermCollector()
                for observed_in in ca.observed_in or []:
                    if observed_in.traits:
                        for trait in observed_in.traits.traits or []:
                            for xref in trait.xrefs:
                                terms.add_xref(xref)

                if needs_hpo_terms and not terms.hpo_terms or not terms.has_link():
                    continue

                record = GenePhenotypeRecord(
                    rcv=rcv,
                    rcv_version=rcv_version,
                    scv=scv,
                    scv_version=scv_version,
                    clinsig=clinsig,
                    submitter=ca.submission_id.submitter,
                    hgnc_ids=list(sorted(hgnc_ids)),
                    omim_terms=list(sorted(clean_omim(terms.omim_terms))),
                    mondo_terms=list(sorted(terms.mondo_terms)),
                    hpo_terms=list(sorted(terms.hpo_terms)),
                )

                print(json.dumps(record.model_dump(mode="json")), file=outputf)
