"""Generate JSONL with gene to phenotype/disease links"""

import gzip
import json
import typing

from google.protobuf.json_format import MessageToDict, ParseDict
import tqdm

from clinvar_data import models
from clinvar_data.pbs.clinvar_public_pb2 import (
    Allele,
    Assertion,
    ClassifiedRecord,
    VariationArchive,
)
from clinvar_data.pbs.extracted_vars import VersionedAccession
from clinvar_data.pbs.phenotype_link import GenePhenotypeRecord


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
            line_json = json.loads(line)
            variation_archive: VariationArchive = ParseDict(
                js_dict=line_json, message=VariationArchive()
            )

            vcv = VersionedAccession(
                accession=variation_archive.accession,
                version=variation_archive.version,
            )

            if not variation_archive.HasField("classified_record"):
                continue
            classified_record: ClassifiedRecord = variation_archive.classified_record
            if not variation_archive.classified_record.HasField("simple_allele"):
                continue
            simple_allele: Allele = classified_record.simple_allele
            hgnc_ids = [gene.hgnc_id for gene in simple_allele.genes if gene.HasField('hgnc_id')]

            for clinical_assertion in classified_record.clinical_assertions:
                scv = (
                    VersionedAccession(
                        accession=clinical_assertion.clinvar_accession.accession,
                        version=clinical_assertion.clinvar_accession.version,
                    )
                )
                germline_classification: str | None = None
                for classification in clinical_assertion.classifications:
                    if (
                        classification.HasField("germline_classification")
                        and "pathogenic" in classification.germline_classification.lower()
                    ):
                        germline_classification = classification.germline_classification
                        break
                if not germline_classification:
                    continue

                if clinical_assertion.assertion != Assertion.ASSERTION_VARIATION_TO_DISEASE:
                    continue

                mondo_terms = []
                omim_terms = []
                hpo_terms = []
                for trait in clinical_assertion.trait_set.traits:
                    for xref in trait.xrefs:
                        if xref.db == "OMIM":
                            omim_terms.append(xref.id)
                        elif xref.db == "HP":
                            hpo_terms.append(xref.id)
                        elif xref.db == "MONDO":
                            mondo_terms.append(xref.id)

                for observed_in in clinical_assertion.observed_ins:
                    for trait in observed_in.trait_set.traits:
                        for xref in trait.xrefs:
                            if xref.db == "OMIM":
                                omim_terms.append(xref.id)
                            elif xref.db == "HP":
                                hpo_terms.append(xref.id)
                            elif xref.db == "MONDO":
                                mondo_terms.append(xref.id)

                mondo_terms = list(sorted(set(mondo_terms)))
                omim_terms = list(sorted(set(omim_terms)))
                hpo_terms = list(sorted(set(hpo_terms)))
                record = GenePhenotypeRecord(
                    vcv=vcv,
                    scv=scv,
                    germline_classification=germline_classification,
                    hgnc_ids=hgnc_ids,
                    mondo_terms=mondo_terms,
                    omim_terms=omim_terms,
                    hpo_terms=hpo_terms,
                )
                print(json.dumps(MessageToDict(record)))

                # germline_classification: str = classification.germline_classification
                # simple_allele: Allele = classification.simple_allele

            # vcv_accession: VersionedAccession = VersionedAccession(
            #     accession=variation_archive.accession,
            #     version=variation_archive.version,
            # )

            # for rcv_record in classified_record.rcv_list.rcv_accessions:
            #     rcv_accession: VersionedAccession = VersionedAccession(
            #         accession=rcv_record.accession,
            #         version=rcv_record.version,
            #     )
            #     rcv_record.class

            # clinvar_set = models.ClinVarSet.model_validate_json(line)
            # rca = clinvar_set.reference_clinvar_assertion
            # rcv = rca.clinvar_accession.acc
            # rcv_version = rca.clinvar_accession.version

            # hgnc_ids = set()
            # if rca.measures:
            #     for measure in rca.measures.measures or []:
            #         for measure_relationship in measure.measure_relationship:
            #             hgnc_ids |= {
            #                 xref.id for xref in measure_relationship.xrefs if xref.db == "HGNC"
            #             }

            # for ca in clinvar_set.clinvar_assertions or []:
            #     clinsig = None
            #     for clinical_significance in ca.clinical_significance:
            #         for description in clinical_significance.descriptions:
            #             if description in (
            #                 models.ClinicalSignificanceDescription.PATHOGENIC,
            #                 models.ClinicalSignificanceDescription.LIKELY_PATHOGENIC,
            #             ):
            #                 clinsig = description
            #                 break

            #     scv = ca.clinvar_accession.acc
            #     scv_version = ca.clinvar_accession.version

            #     terms = TermCollector()
            #     for observed_in in ca.observed_in or []:
            #         if observed_in.traits:
            #             for trait in observed_in.traits.traits or []:
            #                 for xref in trait.xrefs:
            #                     terms.add_xref(xref)

            #     if needs_hpo_terms and not terms.hpo_terms or not terms.has_link():
            #         continue

            #     record = GenePhenotypeRecord(
            #         rcv=rcv,
            #         rcv_version=rcv_version,
            #         scv=scv,
            #         scv_version=scv_version,
            #         clinsig=clinsig,
            #         submitter=ca.submission_id.submitter,
            #         hgnc_ids=list(sorted(hgnc_ids)),
            #         omim_terms=list(sorted(clean_omim(terms.omim_terms))),
            #         mondo_terms=list(sorted(terms.mondo_terms)),
            #         hpo_terms=list(sorted(terms.hpo_terms)),
            #     )

            #     print(json.dumps(record.model_dump(mode="json")), file=outputf)
