"""Generate JSONL with gene to phenotype/disease links"""

import json
import typing

import attrs
import cattrs
import tqdm

from clinvar_data import models
from clinvar_data.cattrs_helpers import CONVERTER


@attrs.frozen(auto_attribs=True)
class GenePhenotypeRecord:
    #: RCV accession
    rcv: str
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
        elif xref.db == "Human Phenotype Ontology":
            self.hpo_terms.add(xref.id)
        elif xref.db == "MONDO":
            self.mondo_terms.add(xref.id)

    def has_link(self) -> bool:
        return self.hpo_terms or self.omim_terms or self.mondo_terms


def run_report(path_input: str, path_output: str, needs_hpo_terms: bool = True):
    """Read in file at path_input and generate link records to path_output."""

    with open(path_input, "rt") as inputf, open(path_output, "wt") as outputf:
        for line in tqdm.tqdm(inputf, desc="processing", unit=" JSONL records"):
            dict_value = json.loads(line)
            clinvar_set = CONVERTER.structure(dict_value, models.ClinVarSet)
            rca = clinvar_set.reference_clinvar_assertion

            if not rca.measure_set:  # pragma: no cover
                continue

            rcv = rca.clinvar_accession.acc

            hgnc_ids = set()
            for measure in rca.measure_set.measures:
                for measure_relationship in measure.measure_relationship:
                    hgnc_ids |= {
                        xref.id for xref in measure_relationship.xrefs if xref.db == "HGNC"
                    }

            terms = TermCollector()
            if rca.trait_set:
                for trait in rca.trait_set.traits or []:
                    for name in trait.names:
                        for xref in name.xrefs:
                            terms.add_xref(xref)
                    for symbol in trait.symbols:
                        for xref in symbol.xrefs:
                            terms.add_xref(xref)
                    for xref in trait.xrefs:
                        terms.add_xref(xref)

            if needs_hpo_terms and not terms.hpo_terms or not terms.has_link():
                continue

            record = GenePhenotypeRecord(
                rcv=rcv,
                hgnc_ids=list(sorted(hgnc_ids)),
                omim_terms=list(sorted(clean_omim(terms.omim_terms))),
                mondo_terms=list(sorted(terms.mondo_terms)),
                hpo_terms=list(sorted(terms.hpo_terms)),
            )

            print(json.dumps(cattrs.unstructure(record)), file=outputf)
