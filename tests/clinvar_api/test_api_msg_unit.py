"""Test ``clinar_api.api_msg`` with unit tests."""

import datetime

from clinvar_api import api_msg


def test_created_construction():
    api_msg.Created(id="test-id")


def test_error_construction():
    api_msg.Error(message="fake-message")


def test_submission_status_file():
    api_msg.SubmissionStatusFile(url="http://example.com")


def test_submission_status_object_content():
    api_msg.SubmissionStatusObjectContent(
        clinvarProcessingStatus="In processing",
        clinvarReleaseStatus="Not released",
    )


def test_submission_status_object():
    api_msg.SubmissionStatusObject(
        accession="accession",
        content=api_msg.SubmissionStatusObjectContent(
            clinvarProcessingStatus="In processing",
            clinvarReleaseStatus="Not released",
        ),
        targetDb="clinvar",
    )
    api_msg.SubmissionStatusObject(
        accession=None,
        content=api_msg.SubmissionStatusObjectContent(
            clinvarProcessingStatus="In processing",
            clinvarReleaseStatus="Not released",
        ),
        targetDb="clinvar",
    )


def test_submission_status_response_message():
    api_msg.SubmissionStatusResponseMessage(
        errorCode="error-code", severity="fake-severity", text="fake text"
    )
    api_msg.SubmissionStatusResponseMessage(
        errorCode=None, severity="fake-severity", text="fake text"
    )


def test_submission_status_response():
    api_msg.SubmissionStatusResponse(
        status=None,
        files=[api_msg.SubmissionStatusFile(url="http://example.com")],
        message=api_msg.SubmissionStatusResponseMessage(
            errorCode="error-code", severity="fake-severity", text="fake text"
        ),
        objects=[
            api_msg.SubmissionStatusObject(
                accession=None,
                content=api_msg.SubmissionStatusObjectContent(
                    clinvarProcessingStatus="In processing",
                    clinvarReleaseStatus="Not released",
                ),
                targetDb="clinvar",
            )
        ],
    )
    api_msg.SubmissionStatusResponse(
        status="fake-status",
        files=[api_msg.SubmissionStatusFile(url="http://example.com")],
        message=api_msg.SubmissionStatusResponseMessage(
            errorCode="error-code", severity="fake-severity", text="fake text"
        ),
        objects=[
            api_msg.SubmissionStatusObject(
                accession=None,
                content=api_msg.SubmissionStatusObjectContent(
                    clinvarProcessingStatus="In processing",
                    clinvarReleaseStatus="Not released",
                ),
                targetDb="clinvar",
            )
        ],
    )


def test_submission_status_actions():
    api_msg.SubmissionStatusActions(
        id="fake-id",
        responses=[
            api_msg.SubmissionStatusResponse(
                status=None,
                files=[api_msg.SubmissionStatusFile(url="http://example.com")],
                message=api_msg.SubmissionStatusResponseMessage(
                    errorCode="error-code", severity="fake-severity", text="fake text"
                ),
                objects=[
                    api_msg.SubmissionStatusObject(
                        accession=None,
                        content=api_msg.SubmissionStatusObjectContent(
                            clinvarProcessingStatus="In processing",
                            clinvarReleaseStatus="Not released",
                        ),
                        targetDb="clinvar",
                    )
                ],
            )
        ],
        status="the-status",
        targetDb="clinvar",
        updated=datetime.datetime.now(),
    )
    api_msg.SubmissionStatusActions(
        id="fake-id",
        responses=[],
        status="the-status",
        targetDb="clinvar",
        updated=datetime.datetime.now(),
    )


def test_submission_status():
    api_msg.SubmissionStatus(actions=[])
    api_msg.SubmissionStatus(
        actions=[
            api_msg.SubmissionStatusActions(
                id="fake-id",
                responses=[],
                status="the-status",
                targetDb="clinvar",
                updated=datetime.datetime.now(),
            )
        ]
    )
