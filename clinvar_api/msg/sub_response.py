"""Data structures for parsing submission response."""

from enum import Enum
import typing

import attrs


class BatchProcessingStatus(Enum):
    IN_PROCESSING = "In processing"
    SUCCESS = "Success"
    ERROR = "Error"
    PARTIAL_SUCCESS = "Partial success"


class BatchReleaseStatus(Enum):
    RELEASED = "Released"
    PARTIAL_RELEASED = "Partial released"
    NOT_RELEASED = "Not released"


@attrs.define(frozen=True)
class Created:
    """Representation of successful creation."""

    #: The submission ID.
    id: str


@attrs.define(frozen=True)
class Error:
    """Representation of server's response in case of failure."""

    #: The error response's message.
    message: str


@attrs.define(frozen=True)
class SummaryResponseErrorInput:
    value: typing.Optional[str] = None
    field: typing.Optional[str] = None


@attrs.define(frozen=True)
class SummaryResponseErrorOutputError:
    userMessage: str


@attrs.define(frozen=True)
class SummaryResponseErrorOutput:
    errors: typing.List[SummaryResponseErrorOutputError]


@attrs.define(frozen=True)
class SummaryResponseError:
    # NB: docs and schema say required but examples do not show
    input: typing.List[SummaryResponseErrorInput]
    output: SummaryResponseErrorOutput


@attrs.define(frozen=True)
class SummaryResponseDeletionIdentifier:
    clinvarAccession: str
    clinvarLocalKey: typing.Optional[str] = None


@attrs.define(frozen=True)
class SummaryResponseDeletion:
    identifiers: SummaryResponseDeletionIdentifier
    processingStatus: str
    deleteDate: typing.Optional[str] = None
    deleteStatus: typing.Optional[str] = None
    errors: typing.Optional[typing.List[SummaryResponseError]] = None


@attrs.define(frozen=True)
class SummaryResponseSubmissionIdentifiers:
    clinvarLocalKey: str
    clinvarAccession: typing.Optional[str] = None
    localID: typing.Optional[str] = None
    localKey: typing.Optional[str] = None


@attrs.define(frozen=True)
class SummaryResponseSubmission:
    identifiers: SummaryResponseSubmissionIdentifiers
    processingStatus: str
    clinvarAccessionVersion: typing.Optional[str] = None
    errors: typing.Optional[typing.List[SummaryResponseError]] = None
    releaseDate: typing.Optional[str] = None
    releaseStatus: typing.Optional[str] = None


@attrs.define(frozen=True)
class SummaryResponse:
    """Represetation of server's response to a submission."""

    batchProcessingStatus: BatchProcessingStatus
    batchReleaseStatus: BatchReleaseStatus
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
