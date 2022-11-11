"""Types for the messages as returned by the API."""

import datetime
import typing

import attrs

ERROR_CODE_PARTIAL_SUCCESS = "1"
ERROR_CODE_ALL_FAILURE = "2"


@attrs.define
class Created:
    """Representation of successful creation."""

    #: The submission ID.
    id: str


@attrs.define
class Error:
    """Representation of server's response in case of failure."""

    #: The error response's message.
    message: str


@attrs.define
class SubmissionStatusFile:
    """Type for ``SubmissionStatus`` entry ``actions[*].response[*].files[*]``."""

    #: File URL
    url: str


@attrs.define
class SubmissionStatusObjectContent:
    """type for ``SubmissionStatusObjectContent`` entry in ``actions[*].response[*].objects[*].content``."""

    #: Processing status
    clinvarProcessingStatus: str
    #: Release status
    clinvarReleaseStatus: str


@attrs.define
class SubmissionStatusObject:
    """Type for ``SubmissionStatusObject`` entry in ``actions[*].response[*].objects[*]``."""

    #: Optional object accession.
    accession: typing.Optional[str]
    #: Object content.
    content: SubmissionStatusObjectContent
    #: Target database, usually "clinvar" per the docs.
    targetDb: str


@attrs.define
class SubmissionStatusResponseMessage:
    """Type for ``SubmissionStatusResponseMessage`` entry in ``actions[*].response[*].message``."""

    #: The error code.
    errorCode: typing.Optional[str]
    #: The message severity.
    severity: str
    #: The message text.
    text: str


@attrs.define
class SubmissionStatusResponse:
    """Type for ``SubmissionStatus`` entry ``actions[*].response[*]``."""

    #: Status, one of "processing", "processed", "error",
    status: str
    #: Files
    files: typing.List[SubmissionStatusFile]
    #: Message
    message: typing.Optional[SubmissionStatusResponseMessage]
    #: Objects
    objects: typing.List[SubmissionStatusObject]


@attrs.define
class SubmissionStatusActions:
    """Type for ``SubmissionStatus`` entry ``actions[*]``."""

    #: Identifier of the submission
    id: str
    #: Entries in ``actions[*].responses``, only one entry per the docs.
    responses: typing.List[SubmissionStatusResponse]
    #: Status of the submission, one of "submitted", "processing", "processed", "error"
    status: str
    #: Target database, usually "clinvar"
    targetDb: str
    #: Last updated time
    updated: datetime.datetime


@attrs.define
class SubmissionStatus:
    """Representation of server's response to a submission status query."""

    #: The list of actions (one element only by the docs).
    actions: typing.List[SubmissionStatusActions]


@attrs.define
class SummaryResponseErrorInput:
    value: str
    field: typing.Optional[str] = None


@attrs.define
class SummaryResponseErrorOutputError:
    userMessage: str


@attrs.define
class SummaryResponseErrorOutput:
    errors: typing.List[SummaryResponseErrorOutputError]


@attrs.define
class SummaryResponseError:
    # NB: docs and schema say required but examples do not show
    input: typing.List[SummaryResponseErrorInput]
    output: SummaryResponseErrorOutput


@attrs.define
class SummaryResponseDeletionIdentifier:
    clinvarAccession: str
    clinvarLocalKey: typing.Optional[str] = None


@attrs.define
class SummaryResponseDeletion:
    identifiers: SummaryResponseDeletionIdentifier
    processingStatus: str
    deleteDate: typing.Optional[str] = None
    deleteStatus: typing.Optional[str] = None
    errors: typing.Optional[typing.List[SummaryResponseError]] = None


@attrs.define
class SummaryResponseSubmissionIdentifiers:
    clinvarLocalKey: str
    clinvarAccession: typing.Optional[str] = None
    localID: typing.Optional[str] = None
    localKey: typing.Optional[str] = None


@attrs.define
class SummaryResponseSubmission:
    identifiers: SummaryResponseSubmissionIdentifiers
    processingStatus: str
    clinvarAccessionVersion: typing.Optional[str] = None
    errors: typing.Optional[typing.List[SummaryResponseError]] = None
    releaseDate: typing.Optional[str] = None
    releaseStatus: typing.Optional[str] = None


@attrs.define
class SummaryResponse:
    """Represetation of server's response to a submission."""

    batchProcessingStatus: str
    batchReleaseStatus: str
    submissionDate: str
    submissionName: str
    totalCount: int
    totalErrors: int
    totalPublic: int
    totalSuccess: int
    deletions: typing.Optional[typing.List[SummaryResponseDeletion]] = None
    submissions: typing.Optional[typing.List[SummaryResponseSubmission]] = None
    totalDeleteCount: typing.Optional[int] = None
    totalDeleted: typing.Optional[int] = None
    totalDeleteErrors: typing.Optional[int] = None
    totalDeleteSuccess: typing.Optional[int] = None
