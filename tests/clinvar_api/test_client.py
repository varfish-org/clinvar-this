import pytest

from clinvar_api import client, exceptions, models

FAKE_ID = "SUBxxx"
FAKE_TOKEN = "1234567890abcdefghijklmnopqrstuvwxyz"
FAKE_HEADERS = {
    "SP-API-KEY": FAKE_TOKEN,
}


def test_config_long_token():
    config = client.Config(auth_token="1234567890", use_testing=False, use_dryrun=False)
    assert str(config) == (
        "Config(auth_token='12345*****', use_testing=False, use_dryrun=False, presubmission_validation=True, verify_ssl=True)"
    )


def test_config_short_token():
    config = client.Config(auth_token="123", use_testing=False, use_dryrun=False)
    assert str(config) == (
        "Config(auth_token='***', use_testing=False, use_dryrun=False, presubmission_validation=True, verify_ssl=True)"
    )


def test_submit_data_success(requests_mock):
    requests_mock.register_uri(
        "POST",
        "https://submit.ncbi.nlm.nih.gov/api/v1/submissions/",
        request_headers=FAKE_HEADERS,
        status_code=200,
        reason="OK",
        json={"id": "SUB999999"},
    )
    result = client.submit_data(
        models.SubmissionContainer(),
        config=client.Config(auth_token=FAKE_TOKEN, presubmission_validation=False),
    )
    assert str(result) == "Created(id='SUB999999')"


def test_submit_data_failed(requests_mock):
    requests_mock.register_uri(
        "POST",
        "https://submit.ncbi.nlm.nih.gov/api/v1/submissions/",
        request_headers=FAKE_HEADERS,
        status_code=400,
        reason="Bad request",
        json={"message": "Submission is incorrect"},
    )
    with pytest.raises(exceptions.SubmissionFailed):
        client.submit_data(
            models.SubmissionContainer(),
            config=client.Config(auth_token=FAKE_TOKEN, presubmission_validation=False),
        )


def test_retrieve_status_result():
    status_result = client.RetrieveStatusResult(
        status=models.SubmissionStatus(actions=[]), summaries={}
    )
    assert (
        str(status_result)
        == "RetrieveStatusResult(status=SubmissionStatus(actions=[]), summaries={})"
    )


def test_retrieve_status_success_no_extra_file(requests_mock, data_submission_submitted):
    requests_mock.register_uri(
        "GET",
        f"https://submit.ncbi.nlm.nih.gov/api/v1/submissions/{FAKE_ID}/actions/",
        request_headers=FAKE_HEADERS,
        status_code=200,
        reason="OK",
        json=data_submission_submitted,
    )
    result = client.retrieve_status(
        FAKE_ID, config=client.Config(auth_token=FAKE_TOKEN, presubmission_validation=False)
    )
    assert str(result).replace("tzlocal", "tzutc") == (
        "RetrieveStatusResult(status=SubmissionStatus(actions=[SubmissionStatusActions("
        "id='SUB999999-1', responses=[], status='submitted', target_db='clinvar', "
        "updated=datetime.datetime(2021, 3, 19, 17, 24, 24, 384085, tzinfo=tzutc()))]), summaries={})"
    )


def test_retrieve_status_success_with_extra_files(
    requests_mock, data_submission_processed, data_summary_response_processed
):
    requests_mock.register_uri(
        "GET",
        f"https://submit.ncbi.nlm.nih.gov/api/v1/submissions/{FAKE_ID}/actions/",
        request_headers=FAKE_HEADERS,
        status_code=200,
        reason="OK",
        json=data_submission_processed,
    )
    requests_mock.register_uri(
        "GET",
        (
            "https://dsubmit.ncbi.nlm.nih.gov/api/2.0/files/xxxxxxxx"
            "/sub999999-summary-report.json/?format=attachment"
        ),
        status_code=200,
        reason="OK",
        json=data_summary_response_processed,
    )
    result = client.retrieve_status(
        FAKE_ID, config=client.Config(auth_token=FAKE_TOKEN, presubmission_validation=False)
    )
    assert str(result).replace("tzlocal", "tzutc") == (
        "RetrieveStatusResult(status=SubmissionStatus(actions=[SubmissionStatusActions(id='SUB999999-1', "
        "responses=[SubmissionStatusResponse(status='processed', files=[SubmissionStatusFile(url='"
        "https://dsubmit.ncbi.nlm.nih.gov/api/2.0/files/xxxxxxxx/sub999999-summary-report.json/"
        "?format=attachment')], message=SubmissionStatusResponseMessage(error_code=None, severity='info', "
        'text=\'Your ClinVar submission processing status is "Success". Please find the details in the file '
        "referenced by actions[0].responses[0].files[0].url.'), objects=[])], status='processed', "
        "target_db='clinvar', updated=datetime.datetime(2021, 3, 24, 4, 22, 4, 101297, tzinfo=tzutc()))]), "
        "summaries={'https://dsubmit.ncbi.nlm.nih.gov/api/2.0/files/xxxxxxxx/sub999999-summary-report.json/"
        "?format=attachment': SummaryResponse(batch_processing_status=<BatchProcessingStatus.SUCCESS: "
        "'Success'>, batch_release_status=<BatchReleaseStatus.NOT_RELEASED: 'Not released'>, "
        "submission_date='2021-03-25', submission_name='SUB673156', total_count=3, total_errors=0, "
        "total_public=0, total_success=3, deletions=None, submissions=[SummaryResponseSubmission("
        "identifiers=SummaryResponseSubmissionIdentifiers(clinvar_local_key='"
        "adefc5ed-7d59-4119-8b3d-07dcdc504c09_success1', clinvar_accession='SCV000839746', "
        "local_id='adefc5ed-7d59-4119-8b3d-07dcdc504c09_success1', "
        "local_key='adefc5ed-7d59-4119-8b3d-07dcdc504c09_success1'), processing_status='Success', "
        "clinvar_accession_version=None, errors=None, release_date=None, release_status=None), "
        "SummaryResponseSubmission(identifiers=SummaryResponseSubmissionIdentifiers("
        "clinvar_local_key='adefc5ed-7d59-4119-8b3d-07dcdc504c09_success2', "
        "clinvar_accession='SCV000839747', local_id='adefc5ed-7d59-4119-8b3d-07dcdc504c09_success2', "
        "local_key='adefc5ed-7d59-4119-8b3d-07dcdc504c09_success2'), processing_status='Success', "
        "clinvar_accession_version=None, errors=None, release_date=None, release_status=None), "
        "SummaryResponseSubmission(identifiers=SummaryResponseSubmissionIdentifiers("
        "clinvar_local_key='adefc5ed-7d59-4119-8b3d-07dcdc504c09_success3', "
        "clinvar_accession='SCV000839748', local_id='adefc5ed-7d59-4119-8b3d-07dcdc504c09_success3', "
        "local_key='adefc5ed-7d59-4119-8b3d-07dcdc504c09_success3'), processing_status='Success', "
        "clinvar_accession_version=None, errors=None, release_date=None, release_status=None)], "
        "total_delete_count=None, total_deleted=None, total_delete_errors=None, total_delete_success=None)})"
    )


def test_retrieve_status_failed_initial_request(requests_mock):
    requests_mock.register_uri(
        "GET",
        f"https://submit.ncbi.nlm.nih.gov/api/v1/submissions/{FAKE_ID}/actions/",
        request_headers=FAKE_HEADERS,
        status_code=401,
        reason="Unauthorized",
        json={"message": "No valid API key provided"},
    )

    with pytest.raises(exceptions.QueryFailed):
        client.retrieve_status(
            FAKE_ID, config=client.Config(auth_token=FAKE_TOKEN, presubmission_validation=False)
        )


def test_retrieve_status_failed_extra_request(requests_mock, data_submission_processed):
    requests_mock.register_uri(
        "GET",
        f"https://submit.ncbi.nlm.nih.gov/api/v1/submissions/{FAKE_ID}/actions/",
        request_headers=FAKE_HEADERS,
        status_code=200,
        reason="OK",
        json=data_submission_processed,
    )
    requests_mock.register_uri(
        "GET",
        (
            "https://dsubmit.ncbi.nlm.nih.gov/api/2.0/files/xxxxxxxx"
            "/sub999999-summary-report.json/?format=attachment"
        ),
        status_code=404,
        reason="Not Found",
    )

    with pytest.raises(exceptions.QueryFailed):
        client.retrieve_status(
            FAKE_ID, config=client.Config(auth_token=FAKE_TOKEN, presubmission_validation=False)
        )


def test_client_submit_success(requests_mock):
    requests_mock.register_uri(
        "POST",
        "https://submit.ncbi.nlm.nih.gov/api/v1/submissions/",
        request_headers=FAKE_HEADERS,
        status_code=200,
        reason="OK",
        json={"id": "SUB999999"},
    )
    client_obj = client.Client(
        config=client.Config(auth_token=FAKE_TOKEN, presubmission_validation=False)
    )
    result = client_obj.submit_data(models.SubmissionContainer())
    assert str(result) == "Created(id='SUB999999')"


def test_client_retrieve_status_success_no_extra_file(requests_mock, data_submission_submitted):
    requests_mock.register_uri(
        "GET",
        f"https://submit.ncbi.nlm.nih.gov/api/v1/submissions/{FAKE_ID}/actions/",
        request_headers=FAKE_HEADERS,
        status_code=200,
        reason="OK",
        json=data_submission_submitted,
    )
    client_obj = client.Client(
        config=client.Config(auth_token=FAKE_TOKEN, presubmission_validation=False)
    )
    result = client_obj.retrieve_status(FAKE_ID)
    assert str(result).replace("tzlocal", "tzutc") == (
        "RetrieveStatusResult(status=SubmissionStatus(actions=[SubmissionStatusActions("
        "id='SUB999999-1', responses=[], status='submitted', target_db='clinvar', "
        "updated=datetime.datetime(2021, 3, 19, 17, 24, 24, 384085, tzinfo=tzutc()))]), summaries={})"
    )
