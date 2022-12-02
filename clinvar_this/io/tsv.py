"""Support for I/O of the minimal TSV format to define submissions."""

import csv
import datetime
import enum
import pathlib
import re
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
from clinvar_api.models.sub_payload import SubmissionClinicalFeature
from clinvar_api.msg.sub_payload import (
    ClinicalFeaturesAffectedStatus,
    ClinicalFeaturesDb,
)
from clinvar_this import exceptions


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
    #: Date of last evaluation of clinical significance
    clinical_significance_date_last_evaluated: typing.Optional[str] = None
    #: Additional comment of clinical significance
    clinical_significance_comment: typing.Optional[str] = None
    #: HPO terms for clinical features
    hpo_terms: typing.Optional[typing.List[str]] = None


@attrs.frozen
class HeaderColumn:
    #: Interpreted header names from TSV
    header_names: typing.Tuple[str]
    #: The corresponding key in in ``TsvRecord``
    key: str
    #: Whether the header is required
    required: bool
    #: Type converter on import
    converter: typing.Callable[[str], typing.Any]
    #: Extractor on export
    extractor: typing.Callable[[TsvRecord], str]

    @property
    def canonical_name(self):
        """The first entry in ``header_names`` is the canonical one."""
        return self.header_names[0]


def _str_list(val: str, pat: str = r"[;,]") -> typing.List[str]:
    """Split a string and return list of trimmed entries"""
    return [x.strip() for x in re.split(pat, val)]


def _uuid4_if_falsy(value: typing.Optional[str] = None) -> typing.Union[str, uuid.UUID]:
    """Return a new UUID4 if ``value`` is falsy."""
    if value:
        return value
    else:
        return uuid.uuid4()


def _today_if_falsy(value: typing.Optional[str] = None) -> str:
    """Return string with today's date if ``value`` is falsy."""
    if value:
        return value
    else:
        return datetime.datetime.now().strftime("%Y-%m-%d")


def _enum_value(e: enum.Enum) -> str:
    return str(e.value)


def _enum_value_or_empty(e: typing.Optional[enum.Enum]) -> str:
    if e:
        return str(e.value)
    else:
        return ""


def _join_list(xs: typing.List[typing.Any]) -> str:
    return ",".join([str(x).strip() for x in xs])


#: The header columns for TSV files.
HEADER_COLUMNS: typing.Tuple[HeaderColumn, ...] = (
    HeaderColumn(
        header_names=("ASSEMBLY",),
        key="assembly",
        required=True,
        converter=str,
        extractor=lambda r: _enum_value(r.assembly),
    ),
    HeaderColumn(
        header_names=("CHROM",),
        key="chromosome",
        required=True,
        converter=str,
        extractor=lambda r: _enum_value(r.chromosome),
    ),
    HeaderColumn(
        header_names=("POS",),
        key="pos",
        required=True,
        converter=int,
        extractor=lambda r: str(r.pos),
    ),
    HeaderColumn(
        header_names=("REF",),
        key="ref",
        required=True,
        converter=str,
        extractor=lambda r: str(r.ref),
    ),
    HeaderColumn(
        header_names=("ALT",),
        key="alt",
        required=True,
        converter=str,
        extractor=lambda r: str(r.alt),
    ),
    HeaderColumn(
        header_names=("OMIM",),
        key="omim",
        required=True,
        converter=_str_list,
        extractor=lambda r: _join_list(r.omim),
    ),
    HeaderColumn(
        header_names=("MOI",),
        key="inheritance",
        required=True,
        converter=lambda x: x or None,
        extractor=lambda r: _enum_value_or_empty(r.inheritance),
    ),
    HeaderColumn(
        header_names=("CLIN_SIG",),
        key="clinical_significance_description",
        required=True,
        converter=str,
        extractor=lambda r: str(r.clinical_significance_description),
    ),
    HeaderColumn(
        header_names=("CLIN_EVAL",),
        key="clinical_significance_date_last_evaluated",
        required=False,
        converter=_today_if_falsy,
        extractor=lambda r: str(r.clinical_significance_date_last_evaluated or ""),
    ),
    HeaderColumn(
        header_names=("CLIN_COMMENT",),
        key="clinical_significance_comment",
        required=False,
        converter=lambda x: x or None,
        extractor=lambda r: str(r.clinical_significance_comment or ""),
    ),
    HeaderColumn(
        header_names=("KEY",),
        key="local_key",
        required=False,
        converter=_uuid4_if_falsy,
        extractor=lambda r: str(r.local_key),
    ),
    HeaderColumn(
        header_names=("HPO",),
        key="hpo_terms",
        required=False,
        converter=_str_list,
        extractor=lambda r: _join_list(r.omim),
    ),
)


def _map_header(header: typing.List[str]) -> typing.List[typing.Optional[HeaderColumn]]:
    """Map header row from TSV file to header columns

    Map to ``None`` for extra data columns.  Raises if a required column is missing.
    """
    seen_required = {column.canonical_name: False for column in HEADER_COLUMNS if column.required}
    by_name = {name: column for column in HEADER_COLUMNS for name in column.header_names}
    result = []
    for entry in header:
        column = by_name.get(entry)
        if column:
            seen_required[column.canonical_name] = True
        result.append(column)

    missing_columns = [name for name, seen in seen_required.items() if not seen]
    if missing_columns:
        raise exceptions.InvalidFormat(f"Missing columns in TSV file: {missing_columns}")

    return result


def _read_tsv_file(inputf: typing.TextIO) -> typing.List[TsvRecord]:
    """Read TSV from the given file."""

    def row_empty(row: typing.List[str]) -> bool:
        return not row or not [val.strip() for val in row if val.strip()]

    reader = csv.reader(inputf, delimiter="\t")
    header_row = None
    headers = None

    result: typing.List[TsvRecord] = []
    for lineno, row in enumerate(reader):
        if row_empty(row):
            continue  # skip empty lines
        if header_row:
            raw_record = {}
            extra_data = {}
            if len(row) != len(header_row):
                raise exceptions.InvalidFormat(f"Wrong number of rows in line {lineno+1}")
            for value, header, header_name in zip(row, headers, header_row):
                if header:
                    raw_record[header.key] = header.converter(value)
                else:
                    extra_data[header_name] = value
            record = cattrs.structure(raw_record, TsvRecord)
            result.append(attrs.evolve(record, extra_data=extra_data))
        else:
            header_row = row
            headers = _map_header(row)
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
    writer.writerow([h.canonical_name for h in HEADER_COLUMNS] + extra_keys)
    for record in tsv_records:
        row = [hc.extractor(record) for hc in HEADER_COLUMNS] + [
            record.extra_data.get(extra_key, "") for extra_key in extra_keys
        ]
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

    def record_condition(record: TsvRecord) -> SubmissionCondition:
        """Construct ``SubmissionCondition`` from ``TsvRecord``."""
        if not record.omim or record.omim == ["not provided"]:
            return SubmissionCondition(name="not provided")
        else:
            return SubmissionCondition(db=ConditionDb.OMIM, id=record.omim[0])

    def record_clinical_features(
        record: TsvRecord,
    ) -> typing.Optional[typing.List[SubmissionClinicalFeature]]:
        """Construct ``typing.Optional[typing.List[SubmissionClinicalFeature]]`` from ``TsvRecord``."""
        if record.hpo_terms:
            return [
                SubmissionClinicalFeature(
                    clinical_features_affected_status=ClinicalFeaturesAffectedStatus.PRESENT,
                    db=ClinicalFeaturesDb.HP,
                    id=hpo_term,
                )
                for hpo_term in record.hpo_terms
            ]
        else:
            return None

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
                        clinical_features=record_clinical_features(record),
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
            clinical_significance_date_last_evaluated=submission.clinical_significance.date_last_evaluated
            or "",
            clinical_significance_comment=submission.clinical_significance.comment or "",
        )

    clinvar_submissions = submission_container.clinvar_submission or []

    return [submission_to_tsv_record(submission) for submission in clinvar_submissions]
