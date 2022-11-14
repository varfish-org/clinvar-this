"""Test ``clinar_api.api_msg`` with real-world examples."""

from clinvar_api import api_msg, common


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


def test_data_summary_response_processed(data_summary_response_processed):
    assert common.CONVERTER.structure(data_summary_response_processed, api_msg.SummaryResponse)


def test_data_summary_response_error_partial(data_summary_response_error_partial):
    assert common.CONVERTER.structure(data_summary_response_error_partial, api_msg.SummaryResponse)


def test_data_summary_response_error_all(data_summary_response_error_all):
    assert common.CONVERTER.structure(data_summary_response_error_all, api_msg.SummaryResponse)


def test_data_submission_snv(data_submission_snv):
    assert common.CONVERTER.structure(data_submission_snv, api_msg.SubmissionContainer)
