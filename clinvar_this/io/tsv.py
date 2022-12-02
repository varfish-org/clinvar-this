"""Support for I/O of the minimal TSV format to define submissions."""

import csv
import pathlib
import typing
import uuid

import attrs
import cattrs

from clinvar_api.models import (
    AffectedStatus,
    AlleleOrigin,
    Assembly,
    Chromosome,
    CitationDb,
    ClinicalSignificanceDescription,
    CollectionMethod,
    ConditionDb,
    ModeOfInheritance,
    RecordStatus,
    ReleaseStatus,
    SubmissionAssertionCriteria,
    SubmissionChromosomeCoordinates,
    SubmissionClinicalSignificance,
    SubmissionClinvarSubmission,
    SubmissionCondition,
    SubmissionConditionSet,
    SubmissionContainer,
    SubmissionObservedIn,
    SubmissionVariant,
    SubmissionVariantSet,
)
from clinvar_this import exceptions

#: The expected first header columns.
HEADER = (
    "ASSEMBLY",
    "CHROM",
    "POS",
    "REF",
    "ALT",
    "OMIM",
    "MOI",
    "CLIN_SIG",
    "KEY",
)

#: Corresponding keys in ``TsvRecord``.
KEYS = (
    "assembly",
    "chromosome",
    "pos",
    "ref",
    "alt",
    "omim",
    "inheritance",
    "clinical_significance_description",
    "local_key",
)


def _uuid4_if_falsy(value: typing.Optional[str] = None) -> typing.Union[str, uuid.UUID]:
    """Return a new UUID4 if ``value`` is falsy."""
    if value:
        return value
    else:
        return uuid.uuid4()


#: Type converters
CONV = (
    str,
    str,
    int,
    str,
    str,
    lambda x: x.split(","),
    lambda x: x or None,
    str,
    _uuid4_if_falsy,
)


@attrs.define(frozen=True)
class TsvRecord:
    """Record for reading."""

    #: Assembly
    assembly: Assembly
    #: Chromosome
    chromosome: Chromosome
    #: Position
    pos: int
    #: Reference allele bases
    ref: str
    #: Alternative allele bases
    alt: str
    #: OMIM ID
    omim: typing.List[str]
    #: Mode of inheritance
    inheritance: typing.Optional[ModeOfInheritance]
    #: Clinical significance
    clinical_significance_description: ClinicalSignificanceDescription
    #: Local identifier of variant-condition pair.
    local_key: str
    #: Additional columns
    extra_data: typing.Dict[str, str] = attrs.field(factory=dict)


def _read_tsv_file(inputf: typing.TextIO) -> typing.List[TsvRecord]:
    """Read TSV from the given file."""

    def row_empty(row: typing.List[str]) -> bool:
        return not row or not [val.strip() for val in row if val.strip()]

    reader = csv.reader(inputf, delimiter="\t")
    header = None

    result: typing.List[TsvRecord] = []
    for row in reader:
        if row_empty(row):
            continue  # skip empty lines
        if header:
            core = row[: len(HEADER)]
            extra = row[len(HEADER) :]
            extra_header = header[len(HEADER) :]
            raw_record = {key: conv(data) for key, conv, data in zip(KEYS, CONV, core)}
            record = cattrs.structure(raw_record, TsvRecord)
            result.append(attrs.evolve(record, extra_data=dict(zip(extra_header, extra))))
        else:
            header = row
            prefix = tuple(header[: len(HEADER)])
            if prefix != HEADER:
                raise exceptions.IOException(
                    f"Expected header to start with {HEADER} but was {prefix}"
                )
    return result


def read_tsv(
    *,
    file: typing.Optional[typing.TextIO] = None,
    path: typing.Union[None, str, pathlib.Path] = None,
) -> typing.List[TsvRecord]:
    """Read TSV from either file or path"""
    if file:
        return _read_tsv_file(file)
    elif path:
        with pathlib.Path(path).open("rt") as inputf:
            return _read_tsv_file(inputf)
    else:
        raise TypeError("You have to provide either file or path")


def _write_tsv_file(tsv_records: typing.Iterable[TsvRecord], outputf: typing.TextIO):
    """Write records as TSV to the given file."""
    extra_keys = []
    for record in tsv_records:
        if record.extra_data:
            for key in record.extra_data:
                if key not in extra_keys:
                    extra_keys.append(key)
    writer = csv.writer(outputf, delimiter="\t")
    writer.writerow(list(HEADER) + extra_keys)
    for record in tsv_records:
        row = list(
            map(
                str,
                [
                    record.assembly.value,
                    record.chromosome.value,
                    record.pos,
                    record.ref,
                    record.alt,
                    ",".join(record.omim),
                    "" if not record.inheritance else record.inheritance.value,
                    record.clinical_significance_description.value,
                    record.local_key,
                ],
            )
        ) + [record.extra_data.get(extra_key, "") for extra_key in extra_keys]
        writer.writerow(row)


def write_tsv(
    tsv_records: typing.Iterable[TsvRecord],
    *,
    file: typing.Optional[typing.TextIO] = None,
    path: typing.Union[None, str, pathlib.Path] = None,
):
    """Write TSV to either file or path"""
    if file:
        return _write_tsv_file(tsv_records, file)
    elif path:
        with pathlib.Path(path).open("wt") as outputf:
            return _write_tsv_file(tsv_records, outputf)
    else:
        raise TypeError("You have to provide either file or path")


@attrs.define(frozen=True)
class BatchMetadata:
    """Batch-wide settings for TSV import.

    The properties will be assigned to all variants/samples in the batch.
    """

    #: The collection method
    collection_method: typing.Optional[CollectionMethod] = None
    #: The allele origin
    allele_origin: typing.Optional[AlleleOrigin] = None
    #: The release status
    release_status: typing.Optional[ReleaseStatus] = None


#: Default values for ``BatchMetadata`` to use optional.
BATCH_METADATA_DEFAULTS: typing.Dict[str, typing.Any] = {
    "collection_method": CollectionMethod.NOT_PROVIDED,
    "allele_origin": AlleleOrigin.GERMLINE,
    "release_status": ReleaseStatus.PUBLIC,
}


def batch_metadata_from_mapping(
    keys_values: typing.Iterable[str], *, use_defaults: bool = False
) -> BatchMetadata:
    """Convert configuration from ``KEY=VALUE`` strings to ``BatchMetadata``

    Default values can be used (should be on import but not on update).
    """
    field_types = {f.name: f.type for f in attrs.fields(BatchMetadata)}
    kwargs = {}
    for key_value in keys_values:
        if "=" not in key_value:
            raise exceptions.ArgumentsError(f"Invalid key/value pair in {key_value}")
        key, value = key_value.split("=")
        if key in field_types:
            try:
                kwargs[key] = cattrs.structure(value, field_types[key])
            except ValueError:
                raise exceptions.ArgumentsError(f"Failed to parse {value} as for key {key}")
    if use_defaults:
        for key, value in BATCH_METADATA_DEFAULTS.items():
            kwargs.setdefault(key, value)
    return BatchMetadata(**kwargs)


def tsv_records_to_submission_container(
    tsv_records: typing.List[TsvRecord],
    batch_metadata: BatchMetadata,
) -> SubmissionContainer:
    """Convert TSV records to submission container data structure."""

    def record_condition(record: TsvRecord):
        if not record.omim:
            return SubmissionCondition(name="not provided")
        else:
            return SubmissionCondition(db=ConditionDb.OMIM, id=record.omim[0])

    allele_origin = batch_metadata.allele_origin or BATCH_METADATA_DEFAULTS["batch_metadata"]
    collection_method = (
        batch_metadata.collection_method or BATCH_METADATA_DEFAULTS["collection_method"]
    )
    release_status = batch_metadata.release_status or BATCH_METADATA_DEFAULTS["release_status"]

    return SubmissionContainer(
        assertion_criteria=SubmissionAssertionCriteria(
            # The following should come from the profile, cf.
            #
            # https://github.com/bihealth/clinvar-this/issues/36
            db=CitationDb.PUBMED,
            id="25741868",
        ),
        clinvar_submission_release_status=release_status,
        clinvar_submission=[
            SubmissionClinvarSubmission(
                local_id=str(_uuid4_if_falsy()),
                local_key=record.local_key,
                condition_set=SubmissionConditionSet(condition=[record_condition(record)]),
                observed_in=[
                    SubmissionObservedIn(
                        affected_status=AffectedStatus.YES,
                        allele_origin=allele_origin,
                        collection_method=collection_method,
                    )
                ],
                clinical_significance=SubmissionClinicalSignificance(
                    clinical_significance_description=record.clinical_significance_description,
                    mode_of_inheritance=record.inheritance,
                ),
                record_status=RecordStatus.NOVEL,
                variant_set=SubmissionVariantSet(
                    variant=[
                        SubmissionVariant(
                            chromosome_coordinates=SubmissionChromosomeCoordinates(
                                assembly=record.assembly,
                                chromosome=record.chromosome,
                                start=record.pos,
                                stop=record.pos + len(record.ref) - 1,
                                reference_allele=record.ref,
                                alternate_allele=record.alt,
                            ),
                        )
                    ]
                ),
                extra_data=record.extra_data or None,  # prefer ``None`` over ``{}``
            )
            for record in tsv_records
        ],
    )


def submission_container_to_tsv_records(
    submission_container: SubmissionContainer,
) -> typing.List[TsvRecord]:
    def _condition(submission: SubmissionClinvarSubmission) -> typing.List[str]:
        if not submission.condition_set.condition:
            raise exceptions.ClinvarThisException(
                "Problem with internal data structure - condition cannot be empty"
            )
        if submission.condition_set.condition[0].name:
            return []  # not provided
        else:
            if submission.condition_set.condition[0].id:
                return [submission.condition_set.condition[0].id]
            else:
                return []

    def _inheritance(submission: SubmissionClinvarSubmission) -> typing.Optional[ModeOfInheritance]:
        if submission.clinical_significance.mode_of_inheritance:
            return submission.clinical_significance.mode_of_inheritance
        else:
            return None

    def submission_to_tsv_record(submission: SubmissionClinvarSubmission) -> TsvRecord:
        if not submission.variant_set:
            raise exceptions.ClinvarThisException(
                "Problem with internal data structure - no variant set"
            )
        elif not submission.variant_set.variant:
            raise exceptions.ClinvarThisException(
                "Problem with internal data structure - no variant"
            )
        elif not submission.variant_set.variant[0].chromosome_coordinates:
            raise exceptions.ClinvarThisException(
                "Problem with internal data structure - no chromosome coordinates"
            )
        else:
            chromosome_coordinates: SubmissionChromosomeCoordinates = (
                submission.variant_set.variant[0].chromosome_coordinates
            )
        if not (
            chromosome_coordinates.assembly
            and chromosome_coordinates.chromosome
            and chromosome_coordinates.start
            and chromosome_coordinates.reference_allele
            and chromosome_coordinates.alternate_allele
        ):
            raise exceptions.ClinvarThisException(
                "Problem with internal data structure - incomplete coordinates"
            )

        extra_data = {}
        if submission.clinvar_accession:
            extra_data["clinvar_accession"] = submission.clinvar_accession  # XXX
        if submission.extra_data:
            extra_data.update(submission.extra_data)

        return TsvRecord(
            assembly=chromosome_coordinates.assembly,
            chromosome=chromosome_coordinates.chromosome,
            pos=chromosome_coordinates.start,
            ref=chromosome_coordinates.reference_allele,
            alt=chromosome_coordinates.alternate_allele,
            omim=_condition(submission),
            inheritance=_inheritance(submission),
            clinical_significance_description=submission.clinical_significance.clinical_significance_description,
            local_key=submission.local_key or "",
            extra_data=extra_data,
        )

    clinvar_submissions = submission_container.clinvar_submission or []

    return [submission_to_tsv_record(submission) for submission in clinvar_submissions]
