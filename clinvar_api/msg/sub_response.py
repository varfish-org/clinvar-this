"""Data structures for parsing submission response."""

from enum import Enum
import typing

from pydantic import BaseModel
from pydantic.config import ConfigDict


class BatchProcessingStatus(Enum):
    IN_PROCESSING = "In processing"
    SUCCESS = "Success"
    ERROR = "Error"
    PARTIAL_SUCCESS = "Partial success"


class BatchReleaseStatus(Enum):
    RELEASED = "Released"
    PARTIAL_RELEASED = "Partial released"
    NOT_RELEASED = "Not released"


class Created(BaseModel):
    """Representation of successful creation."""

    model_config = ConfigDict(frozen=True)

    #: The submission ID.
    id: str


class Error(BaseModel):
    """Representation of server's response in case of failure."""

    model_config = ConfigDict(frozen=True)

    #: The error response's message.
    message: str


class SummaryResponseErrorInput(BaseModel):
    model_config = ConfigDict(frozen=True)

    value: typing.Optional[str] = None
    field: typing.Optional[str] = None


class SummaryResponseErrorOutputError(BaseModel):
    model_config = ConfigDict(frozen=True)

    userMessage: str


class SummaryResponseErrorOutput(BaseModel):
    model_config = ConfigDict(frozen=True)

    errors: typing.List[SummaryResponseErrorOutputError]


class SummaryResponseError(BaseModel):
    model_config = ConfigDict(frozen=True)

    # NB: docs and schema say required but examples do not show
    input: typing.List[SummaryResponseErrorInput]
    output: SummaryResponseErrorOutput


class SummaryResponseDeletionIdentifier(BaseModel):
    model_config = ConfigDict(frozen=True)

    clinvarAccession: str
    clinvarLocalKey: typing.Optional[str] = None


class SummaryResponseDeletion(BaseModel):
    model_config = ConfigDict(frozen=True)

    identifiers: SummaryResponseDeletionIdentifier
    processingStatus: str
    deleteDate: typing.Optional[str] = None
    deleteStatus: typing.Optional[str] = None
    errors: typing.Optional[typing.List[SummaryResponseError]] = None


class SummaryResponseSubmissionIdentifiers(BaseModel):
    model_config = ConfigDict(frozen=True)

    clinvarLocalKey: str
    clinvarAccession: typing.Optional[str] = None
    localID: typing.Optional[str] = None
    localKey: typing.Optional[str] = None


class SummaryResponseSubmission(BaseModel):
    model_config = ConfigDict(frozen=True)

    identifiers: SummaryResponseSubmissionIdentifiers
    processingStatus: str
    clinvarAccessionVersion: typing.Optional[str] = None
    errors: typing.Optional[typing.List[SummaryResponseError]] = None
    releaseDate: typing.Optional[str] = None
    releaseStatus: typing.Optional[str] = None


class SummaryResponse(BaseModel):
    """Represetation of server's response to a submission."""

    model_config = ConfigDict(frozen=True)

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
