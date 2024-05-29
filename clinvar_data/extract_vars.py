"""Extract variants from RCV records."""

import contextlib
import gzip
import json
import os
import typing

from google.protobuf.json_format import MessageToJson, ParseDict
import tqdm

from clinvar_data.pbs.clinvar_public import Allele, ClassifiedRecord, VariationArchive
from clinvar_data.pbs.clinvar_public_pb2 import AggregateClassificationSet
from clinvar_data.pbs.extracted_vars import (
    ExtractedRcvRecord,
    ExtractedVcvRecord,
    VariationType,
    VersionedAccession,
)


class OutputFilesHandler:
    """Helper for creating output paths."""

    def __init__(self, output_dir: str, gzip_output: bool):
        #: Output directory.
        self.output_dir = output_dir
        #: Whether to gzip output.
        self.gzip_output = gzip_output
        #: File suffix.
        self.suffix = "jsonl.gz" if self.gzip_output else "jsonl"
        #: Mapping of assembly and variant size to file.
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


class ConvertVariationType:
    """Static method helper for ``VariationType`` string to enum conversion."""

    #: Dict for conversion.
    CONVERT: dict[str, VariationType.ValueType] = {
        "insertion": VariationType.VARIATION_TYPE_INSERTION,
        "deletion": VariationType.VARIATION_TYPE_DELETION,
        "single nucleotide variant": VariationType.VARIATION_TYPE_SNV,
        "indel": VariationType.VARIATION_TYPE_INDEL,
        "duplication": VariationType.VARIATION_TYPE_DUPLICATION,
        "tandem duplication": VariationType.VARIATION_TYPE_TANDEM_DUPLICATION,
        "structural variant": VariationType.VARIATION_TYPE_STRUCTURAL_VARIANT,
        "copy number gain": VariationType.VARIATION_TYPE_COPY_NUMBER_GAIN,
        "copy number loss": VariationType.VARIATION_TYPE_COPY_NUMBER_LOSS,
        "protein only": VariationType.VARIATION_TYPE_PROTEIN_ONLY,
        "microsatellite": VariationType.VARIATION_TYPE_MICROSATELLITE,
        "inversion": VariationType.VARIATION_TYPE_INVERSION,
        "other": VariationType.VARIATION_TYPE_OTHER,
    }

    @classmethod
    def from_string_value(cls, string_value: str) -> VariationType.ValueType:
        """Convert string to protobuf enum value."""
        return cls.CONVERT.get(string_value.lower(), VariationType.VARIATION_TYPE_OTHER)


def thin_out_aggregate_classification_set(
    classifications: AggregateClassificationSet | None,
) -> AggregateClassificationSet | None:
    """Thin out the aggregate classifications set for extracted variants."""
    if classifications is None:
        return None
    else:
        result = AggregateClassificationSet()
        result.CopyFrom(classifications)
        if result.HasField("germline_classification"):
            for key in ("xrefs", "citations", "history_records", "conditions"):
                result.germline_classification.ClearField(key)
        for somatic_clinical_impacts in result.somatic_clinical_impacts:
            for key in ("xrefs", "citations", "history_records", "conditions"):
                somatic_clinical_impacts.ClearField(key)
        if result.HasField("oncogenicity_classification"):
            for key in ("xrefs", "citations", "history_records", "conditions"):
                result.oncogenicity_classification.ClearField(key)
        return result


def run(path_input: str, output_dir: str, gzip_output: bool):
    """Execute the variant extraction."""
    os.makedirs(output_dir, exist_ok=True)

    if path_input.endswith(".gz"):
        inputf = gzip.open(path_input, "rt")
    else:
        inputf = open(path_input, "rt")

    output_files = OutputFilesHandler(output_dir, gzip_output)

    with inputf, contextlib.ExitStack() as stack:
        for line in tqdm.tqdm(inputf, desc="processing", unit=" JSONL records"):
            line_json = json.loads(line)
            variation_archive: VariationArchive = ParseDict(
                js_dict=line_json, message=VariationArchive()
            )

            if not variation_archive.HasField("classified_record"):
                continue
            classified_record: ClassifiedRecord = variation_archive.classified_record
            if not variation_archive.classified_record.HasField("simple_allele"):
                continue
            simple_allele: Allele = classified_record.simple_allele

            name: str = variation_archive.variation_name
            variation_type: VariationType.ValueType = ConvertVariationType.from_string_value(
                variation_archive.variation_type
            )
            accession: VersionedAccession = VersionedAccession(
                accession=variation_archive.accession,
                version=variation_archive.version,
            )
            rcvs: list[ExtractedRcvRecord] = [
                ExtractedRcvRecord(
                    accession=VersionedAccession(
                        accession=rcva.accession,
                        version=rcva.version,
                    ),
                    title=rcva.title,
                    classifications=rcva.rcv_classifications,
                )
                for rcva in classified_record.rcv_list.rcv_accessions
            ]
            hgnc_ids: list[str] = [
                gene.hgnc_id
                for gene in classified_record.simple_allele.genes
                if gene.HasField("hgnc_id")
            ]

            for location in simple_allele.locations or []:
                for sequence_location in location.sequence_locations or []:
                    record = ExtractedVcvRecord(
                        accession=accession,
                        rcvs=rcvs,
                        name=name,
                        variation_type=variation_type,
                        classifications=(
                            thin_out_aggregate_classification_set(classified_record.classifications)
                        ),
                        sequence_location=sequence_location,
                        hgnc_ids=hgnc_ids,
                    )

                    if record.variation_type == VariationType.VARIATION_TYPE_OTHER:
                        continue
                    if sequence_location.assembly.lower() == "ncbi36":
                        continue

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
                        variant_size = "seqvars"
                    else:
                        variant_size = "strucvars"

                    dest = output_files.get_file(
                        stack, sequence_location.assembly.lower(), variant_size
                    )
                    print(MessageToJson(record, indent=None), file=dest)
