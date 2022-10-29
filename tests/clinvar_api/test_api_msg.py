import pytest

from clinvar_api import api_msg, common


@pytest.fixture
def data_created():
    return {"id": "SUB999999"}


@pytest.fixture
def data_message():
    return {"message": "No valid API key provided"}


@pytest.fixture
def data_submission_submitted():
    """Example data 'Example with a status of "submitted"'."""
    return {
        "actions": [
            {
                "id": "SUB999999-1",
                "responses": [],
                "status": "submitted",
                "targetDb": "clinvar",
                "updated": "2021-03-19T17:24:24.384085Z",
            }
        ]
    }


@pytest.fixture
def data_submission_processing():
    """Example data 'Example with a status of "processing"'."""
    return {
        "actions": [
            {
                "id": "SUB999999-1",
                "responses": [
                    {
                        "files": [],
                        "message": None,
                        "objects": [
                            {
                                "accession": None,
                                "content": {
                                    "clinvarProcessingStatus": "In processing",
                                    "clinvarReleaseStatus": "Not released",
                                },
                                "targetDb": "clinvar",
                            }
                        ],
                        "status": "processing",
                    }
                ],
                "status": "processing",
                "targetDb": "clinvar",
                "updated": "2021-03-19T12:33:09.243072Z",
            }
        ]
    }


@pytest.fixture
def data_submission_processed():
    """Example data 'Example of a successful submission with a status of "processed"'."""
    return {
        "actions": [
            {
                "id": "SUB999999-1",
                "responses": [
                    {
                        "status": "processed",
                        "message": {
                            "errorCode": None,
                            "severity": "info",
                            "text": (
                                'Your ClinVar submission processing status is "Success". Please find the '
                                "details in the file referenced by actions[0].responses[0].files[0].url."
                            ),
                        },
                        "files": [
                            {
                                "url": (
                                    "https://dsubmit.ncbi.nlm.nih.gov/api/2.0/files/xxxxxxxx"
                                    "/sub999999-summary-report.json/?format=attachment"
                                ),
                            }
                        ],
                        "objects": [],
                    }
                ],
                "status": "processed",
                "targetDb": "clinvar",
                "updated": "2021-03-24T04:22:04.101297Z",
            }
        ]
    }


@pytest.fixture
def data_partially_successful_submission():
    """Example data'Example of a partially successful submission and a status of "error"'."""
    return {
        "actions": [
            {
                "id": "SUB999999-1",
                "targetDb": "clinvar",
                "status": "error",
                "updated": "2021-03-25T16:05:03.319474Z",
                "responses": [
                    {
                        "status": "error",
                        "message": {
                            "severity": "error",
                            "errorCode": "1",
                            "text": (
                                'Your ClinVar submission processing status is "Partial success". '
                                "Please find the details in the file referenced by "
                                "actions[0].responses[0].files[0].url.",
                            ),
                        },
                        "files": [
                            {
                                "url": (
                                    "https://dsubmit.ncbi.nlm.nih.gov/api/2.0/files/xxxxxxxx/"
                                    "sub999999-summary-report.json/?format=attachment"
                                )
                            }
                        ],
                        "objects": [],
                    }
                ],
            }
        ]
    }


@pytest.fixture
def data_submission_error():
    """Example data 'Example of a submission with a status of "error" where all records failed:'."""
    return {
        "actions": [
            {
                "id": "SUB999999-1",
                "targetDb": "clinvar",
                "status": "error",
                "updated": "2021-03-25T15:31:04.411550Z",
                "responses": [
                    {
                        "status": "error",
                        "message": {
                            "severity": "error",
                            "errorCode": "2",
                            "text": (
                                'Your ClinVar submission processing status is "Error".  Please find the '
                                "details in the file referenced by actions[0].responses[0].files[0].url."
                            ),
                        },
                        "files": [
                            {
                                "url": (
                                    "https://dsubmit.ncbi.nlm.nih.gov/api/2.0/files/xxxxxxxx/"
                                    "sub999999-summary-report.json/?format=attachment"
                                )
                            }
                        ],
                        "objects": [],
                    }
                ],
            }
        ]
    }


def test_structure_data_created(data_created):
    assert common.CONVERTER.structure(data_created, api_msg.Created)


def test_structure_data_message(data_message):
    assert common.CONVERTER.structure(data_message, api_msg.Error)


def test_data_submission_submitted(data_submission_submitted):
    assert common.CONVERTER.structure(data_submission_submitted, api_msg.SubmissionStatus)


def test_data_submission_processing(data_submission_processing):
    assert common.CONVERTER.structure(data_submission_processing, api_msg.SubmissionStatus)


def test_data_submission_processed(data_submission_processed):
    assert common.CONVERTER.structure(data_submission_processed, api_msg.SubmissionStatus)


def test_data_partially_successful_submission(data_partially_successful_submission):
    assert common.CONVERTER.structure(
        data_partially_successful_submission, api_msg.SubmissionStatus
    )
