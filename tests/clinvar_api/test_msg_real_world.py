"""Test ``clinar_api.msg`` with real-world examples."""

from clinvar_api import msg


def test_structure_data_created(data_created):
    assert msg.Created.model_validate(data_created)


def test_structure_data_message(data_message):
    assert msg.Error.model_validate(data_message)


def test_data_submission_submitted(data_submission_submitted):
    assert msg.SubmissionStatus.model_validate(data_submission_submitted)


def test_data_submission_processing(data_submission_processing):
    assert msg.SubmissionStatus.model_validate(data_submission_processing)


def test_data_submission_processed(data_submission_processed):
    assert msg.SubmissionStatus.model_validate(data_submission_processed)


def test_data_partially_successful_submission(data_partially_successful_submission):
    assert msg.SubmissionStatus.model_validate(data_partially_successful_submission)


def test_data_summary_response_processed(data_summary_response_processed):
    assert msg.SummaryResponse.model_validate(data_summary_response_processed)


def test_data_summary_response_error_partial(data_summary_response_error_partial):
    assert msg.SummaryResponse.model_validate(data_summary_response_error_partial)


def test_data_summary_response_error_all(data_summary_response_error_all):
    assert msg.SummaryResponse.model_validate(data_summary_response_error_all)


def test_data_submission_snv(data_submission_snv):
    assert msg.SubmissionContainer.model_validate(data_submission_snv)
