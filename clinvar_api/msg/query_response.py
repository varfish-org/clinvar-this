"""Data structures for the status update query communication."""

import datetime
from enum import Enum
import typing

from pydantic import BaseModel
from pydantic.config import ConfigDict


class ErrorCode(Enum):
    SUCCESS = "0"
    PARTIAL_SUCCESS = "1"
    ALL_FAILURE = "2"


class ProcessingStatus(Enum):
    ERROR = "Error"
    SUCCESS = "Success"


class SubmissionStatusFile(BaseModel):
    """Type for ``SubmissionStatus`` entry ``actions[*].response[*].files[*]``."""

    model_config = ConfigDict(frozen=True)

    #: File URL
    url: str


class SubmissionStatusObjectContent(BaseModel):
    """type for ``SubmissionStatusObjectContent`` entry in ``actions[*].response[*].objects[*].content``."""

    model_config = ConfigDict(frozen=True)

    #: Processing status
    clinvarProcessingStatus: str
    #: Release status
    clinvarReleaseStatus: str


class SubmissionStatusObject(BaseModel):
    """Type for ``SubmissionStatusObject`` entry in ``actions[*].response[*].objects[*]``."""

    model_config = ConfigDict(frozen=True)

    #: Optional object accession.
    accession: typing.Optional[str]
    #: Object content.
    content: SubmissionStatusObjectContent
    #: Target database, usually "clinvar" per the docs.
    targetDb: str


class SubmissionStatusResponseMessage(BaseModel):
    """Type for ``SubmissionStatusResponseMessage`` entry in ``actions[*].response[*].message``."""

    model_config = ConfigDict(frozen=True)

    #: The error code.
    errorCode: typing.Optional[ErrorCode]
    #: The message severity.
    severity: str
    #: The message text.
    text: str


class SubmissionStatusResponse(BaseModel):
    """Type for ``SubmissionStatus`` entry ``actions[*].response[*]``."""

    model_config = ConfigDict(frozen=True)

    #: Status, one of "processing", "processed", "error",
    status: str
    #: Files
    files: typing.List[SubmissionStatusFile]
    #: Message
    message: typing.Optional[SubmissionStatusResponseMessage]
    #: Objects
    objects: typing.List[SubmissionStatusObject]


class SubmissionStatusActions(BaseModel):
    """Type for ``SubmissionStatus`` entry ``actions[*]``."""

    model_config = ConfigDict(frozen=True)

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


class SubmissionStatus(BaseModel):
    """Representation of server's response to a submission status query."""

    model_config = ConfigDict(frozen=True)

    #: The list of actions (one element only by the docs).
    actions: typing.List[SubmissionStatusActions]
