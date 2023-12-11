import pytest

from clinvar_api import client, exceptions, models

FAKE_ID = "SUBxxx"
FAKE_TOKEN = "1234567890abcdefghijklmnopqrstuvwxyz"
FAKE_HEADERS = {
    "SP-API-KEY": FAKE_TOKEN,
}


def test_config_long_token():
    config = client.Config(auth_token="1234567890", use_testing=False, use_dryrun=False)
    assert repr(config) == (
        "Config(auth_token=SecretStr('**********'), use_testing=False, use_dryrun=False, presubmission_validation=True, verify_ssl=True)"
    )


def test_config_short_token():
    config = client.Config(auth_token="123", use_testing=False, use_dryrun=False)
    assert repr(config) == (
        "Config(auth_token=SecretStr('**********'), use_testing=False, use_dryrun=False, presubmission_validation=True, verify_ssl=True)"
    )


def test_submit_data_success(httpx_mock):
    httpx_mock.add_response(
        method="POST",
        url="https://submit.ncbi.nlm.nih.gov/api/v1/submissions/",
        match_headers=FAKE_HEADERS,
        status_code=200,
        json={"id": "SUB999999"},
    )
    result = client.submit_data(
        models.SubmissionContainer(),
        config=client.Config(auth_token=FAKE_TOKEN, presubmission_validation=False),
    )
    assert repr(result) == "Created(id='SUB999999')"


def test_submit_data_failed(httpx_mock):
    httpx_mock.add_response(
        method="POST",
        url="https://submit.ncbi.nlm.nih.gov/api/v1/submissions/",
        match_headers=FAKE_HEADERS,
        status_code=400,
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
        repr(status_result)
        == "RetrieveStatusResult(status=SubmissionStatus(actions=[]), summaries={})"
    )


def test_retrieve_status_success_no_extra_file(httpx_mock, data_submission_submitted):
    httpx_mock.add_response(
        method="GET",
        url=f"https://submit.ncbi.nlm.nih.gov/api/v1/submissions/{FAKE_ID}/actions/",
        match_headers=FAKE_HEADERS,
        status_code=200,
        json=data_submission_submitted,
    )
    result = client.retrieve_status(
        FAKE_ID, config=client.Config(auth_token=FAKE_TOKEN, presubmission_validation=False)
    )
    assert repr(result).replace("tzlocal", "tzutc") == (
        "RetrieveStatusResult(status=SubmissionStatus(actions=[SubmissionStatusActions("
        "id='SUB999999-1', responses=[], status='submitted', target_db='clinvar', "
        "updated=datetime.datetime(2021, 3, 19, 17, 24, 24, 384085, tzinfo=TzInfo(UTC)))]), summaries={})"
    )


def test_retrieve_status_success_with_extra_files(
    httpx_mock, data_submission_processed, data_summary_response_processed
):
    httpx_mock.add_response(
        method="GET",
        url=f"https://submit.ncbi.nlm.nih.gov/api/v1/submissions/{FAKE_ID}/actions/",
        match_headers=FAKE_HEADERS,
        status_code=200,
        json=data_submission_processed,
    )
    httpx_mock.add_response(
        method="GET",
        url=(
            "https://dsubmit.ncbi.nlm.nih.gov/api/2.0/files/xxxxxxxx"
            "/sub999999-summary-report.json/?format=attachment"
        ),
        status_code=200,
        json=data_summary_response_processed,
    )
    result = client.retrieve_status(
        FAKE_ID, config=client.Config(auth_token=FAKE_TOKEN, presubmission_validation=False)
    )
    assert repr(result) == (
        "RetrieveStatusResult(status=SubmissionStatus(actions=[SubmissionStatusActions(id='SUB999999-1', "
        "responses=[SubmissionStatusResponse(status='processed', files=[SubmissionStatusFile(url='"
        "https://dsubmit.ncbi.nlm.nih.gov/api/2.0/files/xxxxxxxx/sub999999-summary-report.json/"
        "?format=attachment')], message=SubmissionStatusResponseMessage(error_code=None, severity='info', "
        'text=\'Your ClinVar submission processing status is "Success". Please find the details in the file '
        "referenced by actions[0].responses[0].files[0].url.'), objects=[])], status='processed', "
        "target_db='clinvar', updated=datetime.datetime(2021, 3, 24, 4, 22, 4, 101297, tzinfo=TzInfo(UTC)))]), "
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


def test_retrieve_status_failed_initial_request(httpx_mock):
    httpx_mock.add_response(
        method="GET",
        url=f"https://submit.ncbi.nlm.nih.gov/api/v1/submissions/{FAKE_ID}/actions/",
        match_headers=FAKE_HEADERS,
        status_code=401,
        json={"message": "No valid API key provided"},
    )

    with pytest.raises(exceptions.QueryFailed):
        client.retrieve_status(
            FAKE_ID, config=client.Config(auth_token=FAKE_TOKEN, presubmission_validation=False)
        )


def test_retrieve_status_failed_extra_request(httpx_mock, data_submission_processed):
    httpx_mock.add_response(
        method="GET",
        url=f"https://submit.ncbi.nlm.nih.gov/api/v1/submissions/{FAKE_ID}/actions/",
        match_headers=FAKE_HEADERS,
        status_code=200,
        json=data_submission_processed,
    )
    httpx_mock.add_response(
        method="GET",
        url=(
            "https://dsubmit.ncbi.nlm.nih.gov/api/2.0/files/xxxxxxxx"
            "/sub999999-summary-report.json/?format=attachment"
        ),
        status_code=404,
    )

    with pytest.raises(exceptions.QueryFailed):
        client.retrieve_status(
            FAKE_ID, config=client.Config(auth_token=FAKE_TOKEN, presubmission_validation=False)
        )


def test_client_submit_success(httpx_mock):
    httpx_mock.add_response(
        method="POST",
        url="https://submit.ncbi.nlm.nih.gov/api/v1/submissions/",
        match_headers=FAKE_HEADERS,
        status_code=200,
        json={"id": "SUB999999"},
    )
    client_obj = client.Client(
        config=client.Config(auth_token=FAKE_TOKEN, presubmission_validation=False)
    )
    result = client_obj.submit_data(models.SubmissionContainer())
    assert repr(result) == "Created(id='SUB999999')"


def test_client_retrieve_status_success_no_extra_file(httpx_mock, data_submission_submitted):
    httpx_mock.add_response(
        method="GET",
        url=f"https://submit.ncbi.nlm.nih.gov/api/v1/submissions/{FAKE_ID}/actions/",
        match_headers=FAKE_HEADERS,
        status_code=200,
        json=data_submission_submitted,
    )
    client_obj = client.Client(
        config=client.Config(auth_token=FAKE_TOKEN, presubmission_validation=False)
    )
    result = client_obj.retrieve_status(FAKE_ID)
    assert repr(result) == (
        "RetrieveStatusResult(status=SubmissionStatus(actions=[SubmissionStatusActions("
        "id='SUB999999-1', responses=[], status='submitted', target_db='clinvar', "
        "updated=datetime.datetime(2021, 3, 19, 17, 24, 24, 384085, tzinfo=TzInfo(UTC)))]), summaries={})"
    )


@pytest.mark.asyncio
async def test_async_submit_data_success(httpx_mock):
    httpx_mock.add_response(
        method="POST",
        url="https://submit.ncbi.nlm.nih.gov/api/v1/submissions/",
        match_headers=FAKE_HEADERS,
        status_code=200,
        json={"id": "SUB999999"},
    )
    result = await client.async_submit_data(
        models.SubmissionContainer(),
        config=client.Config(auth_token=FAKE_TOKEN, presubmission_validation=False),
    )
    assert repr(result) == "Created(id='SUB999999')"


@pytest.mark.asyncio
async def test_async_submit_data_failed(httpx_mock):
    httpx_mock.add_response(
        method="POST",
        url="https://submit.ncbi.nlm.nih.gov/api/v1/submissions/",
        match_headers=FAKE_HEADERS,
        status_code=400,
        json={"message": "Submission is incorrect"},
    )
    with pytest.raises(exceptions.SubmissionFailed):
        await client.async_submit_data(
            models.SubmissionContainer(),
            config=client.Config(auth_token=FAKE_TOKEN, presubmission_validation=False),
        )


@pytest.mark.asyncio
async def test_async_retrieve_status_success_no_extra_file(httpx_mock, data_submission_submitted):
    httpx_mock.add_response(
        method="GET",
        url=f"https://submit.ncbi.nlm.nih.gov/api/v1/submissions/{FAKE_ID}/actions/",
        match_headers=FAKE_HEADERS,
        status_code=200,
        json=data_submission_submitted,
    )
    result = await client.async_retrieve_status(
        FAKE_ID, config=client.Config(auth_token=FAKE_TOKEN, presubmission_validation=False)
    )
    assert repr(result).replace("tzlocal", "tzutc") == (
        "RetrieveStatusResult(status=SubmissionStatus(actions=[SubmissionStatusActions("
        "id='SUB999999-1', responses=[], status='submitted', target_db='clinvar', "
        "updated=datetime.datetime(2021, 3, 19, 17, 24, 24, 384085, tzinfo=TzInfo(UTC)))]), summaries={})"
    )


@pytest.mark.asyncio
async def test_async_retrieve_status_success_with_extra_files(
    httpx_mock, data_submission_processed, data_summary_response_processed
):
    httpx_mock.add_response(
        method="GET",
        url=f"https://submit.ncbi.nlm.nih.gov/api/v1/submissions/{FAKE_ID}/actions/",
        match_headers=FAKE_HEADERS,
        status_code=200,
        json=data_submission_processed,
    )
    httpx_mock.add_response(
        method="GET",
        url=(
            "https://dsubmit.ncbi.nlm.nih.gov/api/2.0/files/xxxxxxxx"
            "/sub999999-summary-report.json/?format=attachment"
        ),
        status_code=200,
        json=data_summary_response_processed,
    )
    result = await client.async_retrieve_status(
        FAKE_ID, config=client.Config(auth_token=FAKE_TOKEN, presubmission_validation=False)
    )
    assert repr(result) == (
        "RetrieveStatusResult(status=SubmissionStatus(actions=[SubmissionStatusActions(id='SUB999999-1', "
        "responses=[SubmissionStatusResponse(status='processed', files=[SubmissionStatusFile(url='"
        "https://dsubmit.ncbi.nlm.nih.gov/api/2.0/files/xxxxxxxx/sub999999-summary-report.json/"
        "?format=attachment')], message=SubmissionStatusResponseMessage(error_code=None, severity='info', "
        'text=\'Your ClinVar submission processing status is "Success". Please find the details in the file '
        "referenced by actions[0].responses[0].files[0].url.'), objects=[])], status='processed', "
        "target_db='clinvar', updated=datetime.datetime(2021, 3, 24, 4, 22, 4, 101297, tzinfo=TzInfo(UTC)))]), "
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


@pytest.mark.asyncio
async def test_async_retrieve_status_failed_initial_request(httpx_mock):
    httpx_mock.add_response(
        method="GET",
        url=f"https://submit.ncbi.nlm.nih.gov/api/v1/submissions/{FAKE_ID}/actions/",
        match_headers=FAKE_HEADERS,
        status_code=401,
        json={"message": "No valid API key provided"},
    )

    with pytest.raises(exceptions.QueryFailed):
        await client.async_retrieve_status(
            FAKE_ID, config=client.Config(auth_token=FAKE_TOKEN, presubmission_validation=False)
        )


@pytest.mark.asyncio
async def test_async_retrieve_status_failed_extra_request(httpx_mock, data_submission_processed):
    httpx_mock.add_response(
        method="GET",
        url=f"https://submit.ncbi.nlm.nih.gov/api/v1/submissions/{FAKE_ID}/actions/",
        match_headers=FAKE_HEADERS,
        status_code=200,
        json=data_submission_processed,
    )
    httpx_mock.add_response(
        method="GET",
        url=(
            "https://dsubmit.ncbi.nlm.nih.gov/api/2.0/files/xxxxxxxx"
            "/sub999999-summary-report.json/?format=attachment"
        ),
        status_code=404,
    )

    with pytest.raises(exceptions.QueryFailed):
        await client.async_retrieve_status(
            FAKE_ID, config=client.Config(auth_token=FAKE_TOKEN, presubmission_validation=False)
        )


@pytest.mark.asyncio
async def test_async_client_submit_success(httpx_mock):
    httpx_mock.add_response(
        method="POST",
        url="https://submit.ncbi.nlm.nih.gov/api/v1/submissions/",
        match_headers=FAKE_HEADERS,
        status_code=200,
        json={"id": "SUB999999"},
    )
    client_obj = client.AsyncClient(
        config=client.Config(auth_token=FAKE_TOKEN, presubmission_validation=False)
    )
    result = await client_obj.submit_data(models.SubmissionContainer())
    assert repr(result) == "Created(id='SUB999999')"


@pytest.mark.asyncio
async def test_async_client_retrieve_status_success_no_extra_file(
    httpx_mock, data_submission_submitted
):
    httpx_mock.add_response(
        method="GET",
        url=f"https://submit.ncbi.nlm.nih.gov/api/v1/submissions/{FAKE_ID}/actions/",
        match_headers=FAKE_HEADERS,
        status_code=200,
        json=data_submission_submitted,
    )
    client_obj = client.AsyncClient(
        config=client.Config(auth_token=FAKE_TOKEN, presubmission_validation=False)
    )
    result = await client_obj.retrieve_status(FAKE_ID)
    assert repr(result) == (
        "RetrieveStatusResult(status=SubmissionStatus(actions=[SubmissionStatusActions("
        "id='SUB999999-1', responses=[], status='submitted', target_db='clinvar', "
        "updated=datetime.datetime(2021, 3, 19, 17, 24, 24, 384085, tzinfo=TzInfo(UTC)))]), summaries={})"
    )
