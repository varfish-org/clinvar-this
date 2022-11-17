"""Data structures for the status update query communication."""

import datetime
from enum import Enum
import typing

import attrs


class ErrorCode(Enum):
    SUCCESS = "0"
    PARTIAL_SUCCESS = "1"
    ALL_FAILURE = "2"


class ProcessingStatus(Enum):
    ERROR = "Error"
    SUCCESS = "Success"


@attrs.define(frozen=True)
class SubmissionStatusFile:
    """Type for ``SubmissionStatus`` entry ``actions[*].response[*].files[*]``."""

    #: File URL
    url: str


@attrs.define(frozen=True)
class SubmissionStatusObjectContent:
    """type for ``SubmissionStatusObjectContent`` entry in ``actions[*].response[*].objects[*].content``."""

    #: Processing status
    clinvarProcessingStatus: str
    #: Release status
    clinvarReleaseStatus: str


@attrs.define(frozen=True)
class SubmissionStatusObject:
    """Type for ``SubmissionStatusObject`` entry in ``actions[*].response[*].objects[*]``."""

    #: Optional object accession.
    accession: typing.Optional[str]
    #: Object content.
    content: SubmissionStatusObjectContent
    #: Target database, usually "clinvar" per the docs.
    targetDb: str


@attrs.define(frozen=True)
class SubmissionStatusResponseMessage:
    """Type for ``SubmissionStatusResponseMessage`` entry in ``actions[*].response[*].message``."""

    #: The error code.
    errorCode: typing.Optional[ErrorCode]
    #: The message severity.
    severity: str
    #: The message text.
    text: str


@attrs.define(frozen=True)
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


@attrs.define(frozen=True)
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


@attrs.define(frozen=True)
class SubmissionStatus:
    """Representation of server's response to a submission status query."""

    #: The list of actions (one element only by the docs).
    actions: typing.List[SubmissionStatusActions]
