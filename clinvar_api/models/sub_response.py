"""Data structures for submission response."""

import typing

from pydantic import BaseModel
from pydantic.config import ConfigDict

from clinvar_api import msg

# Import and re-use the enums. This makes coupling tighter than it would have to be but the
# trade-off of copy-pasting them with no influence on the interal record API makes that not
# worth it.
from clinvar_api.msg.sub_response import BatchProcessingStatus, BatchReleaseStatus


class Created(BaseModel):
    model_config = ConfigDict(frozen=True)

    #: The submission ID.
    id: str

    @classmethod
    def from_msg(cls, other: msg.Created):
        return Created(id=other.id)


class Error(BaseModel):
    model_config = ConfigDict(frozen=True)

    #: The error response's message.
    message: str

    @classmethod
    def from_msg(cls, other: msg.Error):
        return Error(message=other.message)


class SummaryResponseErrorInput(BaseModel):
    model_config = ConfigDict(frozen=True)

    value: typing.Optional[str] = None
    field: typing.Optional[str] = None

    @classmethod
    def from_msg(cls, other: msg.SummaryResponseErrorInput):
        return SummaryResponseErrorInput(
            value=other.value,
            field=other.field,
        )


class SummaryResponseErrorOutputError(BaseModel):
    model_config = ConfigDict(frozen=True)

    user_message: str

    @classmethod
    def from_msg(cls, other: msg.SummaryResponseErrorOutputError):
        return SummaryResponseErrorOutputError(
            user_message=other.userMessage,
        )


class SummaryResponseErrorOutput(BaseModel):
    model_config = ConfigDict(frozen=True)

    errors: typing.List[SummaryResponseErrorOutputError]

    @classmethod
    def from_msg(cls, other: msg.SummaryResponseErrorOutput):
        return SummaryResponseErrorOutput(
            errors=[
                SummaryResponseErrorOutputError.from_msg(msg_error) for msg_error in other.errors
            ]
        )


class SummaryResponseError(BaseModel):
    model_config = ConfigDict(frozen=True)

    input: typing.List[SummaryResponseErrorInput]
    output: SummaryResponseErrorOutput

    @classmethod
    def from_msg(cls, other: msg.SummaryResponseError):
        return SummaryResponseError(
            input=[SummaryResponseErrorInput.from_msg(msg_input) for msg_input in other.input],
            output=SummaryResponseErrorOutput.from_msg(other.output),
        )


class SummaryResponseDeletionIdentifier(BaseModel):
    model_config = ConfigDict(frozen=True)

    clinvar_accession: str
    clinvar_local_key: typing.Optional[str] = None

    @classmethod
    def from_msg(cls, other: msg.SummaryResponseDeletionIdentifier):
        return SummaryResponseDeletionIdentifier(
            clinvar_accession=other.clinvarAccession,
            clinvar_local_key=other.clinvarLocalKey,
        )


class SummaryResponseDeletion(BaseModel):
    model_config = ConfigDict(frozen=True)

    identifiers: SummaryResponseDeletionIdentifier
    processing_status: str
    delete_date: typing.Optional[str] = None
    delete_status: typing.Optional[str] = None
    errors: typing.Optional[typing.List[SummaryResponseError]] = None

    @classmethod
    def from_msg(cls, other: msg.SummaryResponseDeletion):
        errors = None
        if other.errors:
            errors = [SummaryResponseError.from_msg(msg_error) for msg_error in other.errors]
        return SummaryResponseDeletion(
            identifiers=SummaryResponseDeletionIdentifier.from_msg(other.identifiers),
            processing_status=other.processingStatus,
            delete_date=other.deleteDate,
            delete_status=other.deleteStatus,
            errors=errors,
        )


class SummaryResponseSubmissionIdentifiers(BaseModel):
    model_config = ConfigDict(frozen=True)

    clinvar_local_key: str
    clinvar_accession: typing.Optional[str] = None
    local_id: typing.Optional[str] = None
    local_key: typing.Optional[str] = None

    @classmethod
    def from_msg(cls, other: msg.SummaryResponseSubmissionIdentifiers):
        return SummaryResponseSubmissionIdentifiers(
            clinvar_local_key=other.clinvarLocalKey,
            clinvar_accession=other.clinvarAccession,
            local_id=other.localID,
            local_key=other.localKey,
        )


class SummaryResponseSubmission(BaseModel):
    model_config = ConfigDict(frozen=True)

    identifiers: SummaryResponseSubmissionIdentifiers
    processing_status: str
    clinvar_accession_version: typing.Optional[str] = None
    errors: typing.Optional[typing.List[SummaryResponseError]] = None
    release_date: typing.Optional[str] = None
    release_status: typing.Optional[str] = None

    @classmethod
    def from_msg(cls, other: msg.SummaryResponseSubmission):
        errors = None
        if other.errors:
            errors = [SummaryResponseError.from_msg(msg_error) for msg_error in other.errors]
        return SummaryResponseSubmission(
            identifiers=SummaryResponseSubmissionIdentifiers.from_msg(
                other.identifiers,
            ),
            processing_status=other.processingStatus,
            clinvar_accession_version=other.clinvarAccessionVersion,
            errors=errors,
            release_date=other.releaseDate,
            release_status=other.releaseStatus,
        )


class SummaryResponse(BaseModel):
    """Represetation of server's response to a submission."""

    model_config = ConfigDict(frozen=True)

    batch_processing_status: BatchProcessingStatus
    batch_release_status: BatchReleaseStatus
    submission_date: str
    submission_name: str
    total_count: int
    total_errors: int
    total_public: int
    total_success: int
    deletions: typing.Optional[typing.List[SummaryResponseDeletion]] = None
    submissions: typing.Optional[typing.List[SummaryResponseSubmission]] = None
    total_delete_count: typing.Optional[int] = None
    total_deleted: typing.Optional[int] = None
    total_delete_errors: typing.Optional[int] = None
    total_delete_success: typing.Optional[int] = None

    @classmethod
    def from_msg(cls, other: msg.SummaryResponse):
        deletions = None
        if other.deletions:
            deletions = [
                SummaryResponseDeletion.from_msg(msg_deletion) for msg_deletion in other.deletions
            ]
        submissions = None
        if other.submissions:
            submissions = [
                SummaryResponseSubmission.from_msg(msg_deletion)
                for msg_deletion in other.submissions
            ]
        return SummaryResponse(
            batch_processing_status=other.batchProcessingStatus,
            batch_release_status=other.batchReleaseStatus,
            submission_date=other.submissionDate,
            submission_name=other.submissionName,
            total_count=other.totalCount,
            total_errors=other.totalErrors,
            total_public=other.totalPublic,
            total_success=other.totalSuccess,
            deletions=deletions,
            submissions=submissions,
            total_delete_count=other.totalDeleteCount,
            total_deleted=other.totalDeleted,
            total_delete_errors=other.totalDeleteErrors,
            total_delete_success=other.totalDeleteSuccess,
        )
