"""Models to be used by the API user."""

import datetime
import typing

import attrs

from clinvar_api import api_msg

_Created = typing.TypeVar("Created")


@attrs.define
class Created:
    #: The submission ID.
    id: str

    @classmethod
    def from_msg(cls, other: api_msg.Created) -> _Created:
        return Created(id=other.id)


_Error = typing.TypeVar("Error")


@attrs.define
class Error:
    #: The error response's message.
    message: str

    @classmethod
    def from_msg(cls, other: api_msg.Error) -> _Error:
        return Error(message=other.message)


#: Re-use the type directly.
SubmissionStatusFile = api_msg.SubmissionStatusFile


#: Type variable as ``Self`` does not exist yet.
_SubmissionStatusObjectContent = typing.TypeVar("SubmissionStatusObjectContent")


@attrs.define
class SubmissionStatusObjectContent:
    #: Processing status
    clinvar_processing_status: str
    #: Release status
    clinvar_release_status: str

    @classmethod
    def from_msg(
        cls, other: api_msg.SubmissionStatusObjectContent
    ) -> _SubmissionStatusObjectContent:
        return SubmissionStatusObjectContent(
            clinvar_processing_status=other.clinvarProcessingStatus,
            clinvar_release_status=other.clinvarReleaseStatus,
        )


#: Type variable as ``Self`` does not exist yet.
_SubmissionStatusObject = typing.TypeVar("SubmissionStatusObject")


@attrs.define
class SubmissionStatusObject:
    #: Optional object accession.
    accession: typing.Optional[str]
    #: Object content.
    content: SubmissionStatusObjectContent
    #: Target database, usually "clinvar" per the docs.
    target_db: str

    @classmethod
    def from_msg(cls, other: api_msg.SubmissionStatusObject) -> _SubmissionStatusObject:
        return SubmissionStatusObject(
            accession=other.accession,
            content=SubmissionStatusObjectContent.from_msg(other.content),
            target_db=other.targetDb,
        )


#: Type variable as ``Self`` does not exist yet.
_SubmissionStatusResponseMessage = typing.TypeVar("SubmissionStatusResponseMessage")


@attrs.define
class SubmissionStatusResponseMessage:
    #: The error code.
    error_code: typing.Optional[str]
    #: The message severity.
    severity: str
    #: The message text.
    text: str

    @classmethod
    def from_msg(
        cls,
        other: api_msg.SubmissionStatusResponseMessage,
    ) -> _SubmissionStatusResponseMessage:
        return SubmissionStatusResponseMessage(
            error_code=other.errorCode,
            severity=other.severity,
            text=other.text,
        )


#: Type variable as ``Self`` does not exist yet.
_SubmissionStatusResponse = typing.TypeVar("SubmissionStatusResponse")


@attrs.define
class SubmissionStatusResponse:
    """Internal submission status response"""

    #: Status, one of "processing", "processed", "error",
    status: str
    #: Files in the response.
    files: typing.List[SubmissionStatusFile]
    #: Message
    message: typing.Optional[SubmissionStatusResponseMessage]
    #: Objects
    objects: typing.List[SubmissionStatusObject]

    @classmethod
    def from_msg(cls, other: api_msg.SubmissionStatusResponse) -> _SubmissionStatusResponse:
        if other.message:
            message = SubmissionStatusResponseMessage.from_msg(other.message)
        else:
            message = None
        return SubmissionStatusResponse(
            status=other.status,
            files=other.files,
            message=message,
            objects=list(map(SubmissionStatusObject.from_msg, other.objects)),
        )


#: Type variable as ``Self`` does not exist yet.
_SubmissionStatus = typing.TypeVar("SubmissionStatus")


@attrs.define
class SubmissionStatus:
    """Internal submission status."""

    #: Identifier of the submission
    id: str
    #: Entries in ``actions[*].responses``, only one entry per the docs.
    response: typing.Optional[SubmissionStatusResponse]
    #: Status of the submission, one of "submitted", "processing", "processed", "error"
    status: str
    #: Target database, usually "clinvar"
    target_db: str
    #: Last updated time
    updated: datetime.datetime

    @classmethod
    def from_msg(cls, other: api_msg.SubmissionStatus) -> _SubmissionStatus:
        if other.actions[0].responses:
            response = SubmissionStatusResponse.from_msg(other.actions[0].responses[0])
        else:
            response = None
        return SubmissionStatus(
            id=other.actions[0].id,
            response=response,
            status=other.actions[0].status,
            target_db=other.actions[0].targetDb,
            updated=other.actions[0].updated,
        )
