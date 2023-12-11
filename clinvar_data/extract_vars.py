"""Extract variants from RCV records."""

import contextlib
import enum
import gzip
import os
import typing

from pydantic import BaseModel, ConfigDict
import tqdm

from clinvar_data import models
from clinvar_data.models import MeasureAttributeType


class OutputFilesHandler:
    def __init__(self, output_dir: str, gzip_output: bool):
        self.output_dir = output_dir
        self.gzip_output = gzip_output
        self.suffix = "jsonl.gz" if self.gzip_output else "jsonl"
        self.files: typing.Dict[typing.Tuple[str, str], typing.TextIO] = {}

    def get_file(self, stack: contextlib.ExitStack, assembly: str, variant_size: str):
        key = (assembly, variant_size)
        if key not in self.files:
            file_path = os.path.join(
                self.output_dir, f"clinvar-variants-{assembly}-{variant_size}.{self.suffix}"
            )
            if self.gzip_output:
                self.files[key] = gzip.open(file_path, "wt")
            else:
                self.files[key] = open(file_path, "wt")
            stack.push(self.files[key])
        return self.files[key]


@enum.unique
class VariantType(enum.Enum):
    INSERTION = "insertion"
    DELETION = "deletion"
    SNV = "single nucleotide variant"
    INDEL = "indel"
    DUPLICATION = "duplication"
    TANDEM_DUPLICATION = "tandem duplication"
    STRUCTURAL_VARIANT = "structural variant"
    COPY_NUMBER_GAIN = "copy number gain"
    COPY_NUMBER_LOSS = "copy number loss"
    PROTEIN_ONLY = "protein only"
    MICROSATELLITE = "microsatellite"
    INVERSION = "inversion"
    OTHER = "other"

    @classmethod
    def from_measure_type(cls, mt: typing.Optional[models.MeasureType]) -> "VariantType":
        mapping: typing.Dict[typing.Optional[models.MeasureType], VariantType] = {
            models.MeasureType.INSERTION: VariantType.INSERTION,
            models.MeasureType.DELETION: VariantType.DELETION,
            models.MeasureType.SNV: VariantType.SNV,
            models.MeasureType.INDEL: VariantType.INDEL,
            models.MeasureType.DUPLICATION: VariantType.DUPLICATION,
            models.MeasureType.TANDEM_DUPLICATION: VariantType.TANDEM_DUPLICATION,
            models.MeasureType.STRUCTURAL_VARIANT: VariantType.STRUCTURAL_VARIANT,
            models.MeasureType.COPY_NUMBER_GAIN: VariantType.COPY_NUMBER_GAIN,
            models.MeasureType.COPY_NUMBER_LOSS: VariantType.COPY_NUMBER_LOSS,
            models.MeasureType.INVERSION: VariantType.INVERSION,
        }
        return mapping.get(mt, VariantType.OTHER)


class VariantRecord(BaseModel):
    model_config = ConfigDict(frozen=True)

    rcv: str
    rcv_version: int
    vcv: str
    vcv_version: int
    title: str
    variant_type: VariantType
    clinical_significance: typing.Optional[models.ClinicalSignificanceDescription]
    review_status: typing.Optional[models.ReviewStatus]
    sequence_location: models.SequenceLocation
    hgnc_ids: typing.List[str]
    absolute_copy_number: typing.Union[None, str, int, float] = None
    reference_copy_number: typing.Union[None, str, int, float] = None
    copy_number_tuple: typing.Union[None, str, int, float] = None


def run(path_input: str, output_dir: str, gzip_output: bool):
    os.makedirs(output_dir, exist_ok=True)

    if path_input.endswith(".gz"):
        inputf = gzip.open(path_input, "rt")
    else:
        inputf = open(path_input, "rt")

    output_files = OutputFilesHandler(output_dir, gzip_output)

    with inputf, contextlib.ExitStack() as stack:
        for line in tqdm.tqdm(inputf, desc="processing", unit=" JSONL records"):
            clinvar_set = models.ClinVarSet.model_validate_json(line)
            rca = clinvar_set.reference_clinvar_assertion

            if rca.measures:
                for measure in rca.measures.measures or []:
                    if not measure.sequence_locations:
                        continue

                    hgnc_ids_set = set()
                    for measure_relationship in measure.measure_relationship or []:
                        for xref in measure_relationship.xrefs:
                            if xref.db == "HGNC":
                                hgnc_ids_set.add(xref.id)
                    hgnc_ids = list(sorted(hgnc_ids_set))

                    absolute_copy_number = None
                    reference_copy_number = None
                    copy_number_tuple = None
                    for attribute in measure.attributes or []:
                        value = attribute.value or attribute.integer_value
                        if attribute.type == MeasureAttributeType.ABSOLUTE_COPY_NUMBER:
                            absolute_copy_number = value
                        elif attribute.type == MeasureAttributeType.REFERENCE_COPY_NUMBER:
                            reference_copy_number = value
                        elif attribute.type == MeasureAttributeType.COPY_NUMBER_TUPLE:
                            copy_number_tuple = value

                    if rca.clinical_significance and rca.clinical_significance.description:
                        clinical_significance = rca.clinical_significance.description
                        review_status = rca.clinical_significance.review_status
                    else:
                        clinical_significance = None
                        review_status = None

                    # The structural variants that we saw had the sequence location directly on the measure.
                    for sequence_location in measure.sequence_locations:
                        record = VariantRecord(
                            rcv=rca.clinvar_accession.acc,
                            rcv_version=rca.clinvar_accession.version,
                            vcv=rca.measures.acc or "__MISSING__",
                            vcv_version=rca.measures.version or 0,
                            title=clinvar_set.title or "__MISSING__",
                            clinical_significance=clinical_significance,
                            review_status=review_status,
                            variant_type=VariantType.from_measure_type(measure.type),
                            sequence_location=sequence_location,
                            hgnc_ids=hgnc_ids,
                            absolute_copy_number=absolute_copy_number,
                            reference_copy_number=reference_copy_number,
                            copy_number_tuple=copy_number_tuple,
                        )
                        if record.variant_type == VariantType.OTHER:
                            continue

                        if (
                            sequence_location.reference_allele
                            or sequence_location.alternate_allele
                            or sequence_location.reference_allele_vcf
                            or sequence_location.alternate_allele_vcf
                        ):
                            variant_size = "seqvars"
                        else:
                            variant_size = "strucvars"
                        dest = output_files.get_file(
                            stack, sequence_location.assembly.lower(), variant_size
                        )
                        print(record.model_dump_json(), file=dest)
