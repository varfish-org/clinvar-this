"""Data structures for internal representation of query response."""

import datetime
import typing

from pydantic import BaseModel
from pydantic.config import ConfigDict

from clinvar_api import msg
from clinvar_api.msg import ErrorCode


class SubmissionStatusFile(BaseModel):
    model_config = ConfigDict(frozen=True)

    url: str

    @classmethod
    def from_msg(cls, other: msg.SubmissionStatusFile):
        return SubmissionStatusFile(url=other.url)


class SubmissionStatusObjectContent(BaseModel):
    model_config = ConfigDict(frozen=True)

    #: Processing status
    clinvar_processing_status: str
    #: Release status
    clinvar_release_status: str

    @classmethod
    def from_msg(cls, other: msg.SubmissionStatusObjectContent):
        return SubmissionStatusObjectContent(
            clinvar_processing_status=other.clinvarProcessingStatus,
            clinvar_release_status=other.clinvarReleaseStatus,
        )


class SubmissionStatusObject(BaseModel):
    model_config = ConfigDict(frozen=True)

    #: Optional object accession.
    accession: typing.Optional[str]
    #: Object content.
    content: SubmissionStatusObjectContent
    #: Target database, usually "clinvar" per the docs.
    target_db: str

    @classmethod
    def from_msg(cls, other: msg.SubmissionStatusObject):
        return SubmissionStatusObject(
            accession=other.accession,
            content=SubmissionStatusObjectContent.from_msg(other.content),
            target_db=other.targetDb,
        )


class SubmissionStatusResponseMessage(BaseModel):
    model_config = ConfigDict(frozen=True)

    #: The error code.
    error_code: typing.Optional[ErrorCode]
    #: The message severity.
    severity: str
    #: The message text.
    text: str

    @classmethod
    def from_msg(cls, other: msg.SubmissionStatusResponseMessage):
        return SubmissionStatusResponseMessage(
            error_code=other.errorCode, severity=other.severity, text=other.text
        )


class SubmissionStatusResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    #: Status, one of "processing", "processed", "error",
    status: str
    #: Files in the response.
    files: typing.List[SubmissionStatusFile]
    #: Message
    message: typing.Optional[SubmissionStatusResponseMessage]
    #: Objects
    objects: typing.List[SubmissionStatusObject]

    @classmethod
    def from_msg(cls, other: msg.SubmissionStatusResponse):
        if other.message:
            message = SubmissionStatusResponseMessage.from_msg(other.message)
        else:
            message = None
        return SubmissionStatusResponse(
            status=other.status,
            files=[SubmissionStatusFile.from_msg(f) for f in other.files],
            message=message,
            objects=list(map(SubmissionStatusObject.from_msg, other.objects)),
        )


class SubmissionStatusActions(BaseModel):
    model_config = ConfigDict(frozen=True)

    #: Identifier of the submission
    id: str
    #: Entries in ``actions[*].responses``, only one entry per the docs.
    responses: typing.List[SubmissionStatusResponse]
    #: Status of the submission, one of "submitted", "processing", "processed", "error"
    status: str
    #: Target database, usually "clinvar"
    target_db: str
    #: Last updated time
    updated: datetime.datetime

    @classmethod
    def from_msg(cls, other: msg.SubmissionStatusActions):
        return SubmissionStatusActions(
            id=other.id,
            responses=[SubmissionStatusResponse.from_msg(response) for response in other.responses],
            status=other.status,
            target_db=other.targetDb,
            updated=other.updated,
        )


class SubmissionStatus(BaseModel):
    """Internal submission status."""

    model_config = ConfigDict(frozen=True)

    #: The list of actions (one element only by the docs).
    actions: typing.List[SubmissionStatusActions]

    @classmethod
    def from_msg(cls, other: msg.SubmissionStatus):
        return SubmissionStatus(
            actions=[SubmissionStatusActions.from_msg(action) for action in other.actions]
        )
