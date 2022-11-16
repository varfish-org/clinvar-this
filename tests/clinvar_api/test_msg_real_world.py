"""Test ``clinar_api.msg`` with real-world examples."""

from clinvar_api import common, msg


def test_structure_data_created(data_created):
    assert common.CONVERTER.structure(data_created, msg.Created)


def test_structure_data_message(data_message):
    assert common.CONVERTER.structure(data_message, msg.Error)


def test_data_submission_submitted(data_submission_submitted):
    assert common.CONVERTER.structure(data_submission_submitted, msg.SubmissionStatus)


def test_data_submission_processing(data_submission_processing):
    assert common.CONVERTER.structure(data_submission_processing, msg.SubmissionStatus)


def test_data_submission_processed(data_submission_processed):
    assert common.CONVERTER.structure(data_submission_processed, msg.SubmissionStatus)


def test_data_partially_successful_submission(data_partially_successful_submission):
    assert common.CONVERTER.structure(data_partially_successful_submission, msg.SubmissionStatus)


def test_data_summary_response_processed(data_summary_response_processed):
    assert common.CONVERTER.structure(data_summary_response_processed, msg.SummaryResponse)


def test_data_summary_response_error_partial(data_summary_response_error_partial):
    assert common.CONVERTER.structure(data_summary_response_error_partial, msg.SummaryResponse)


def test_data_summary_response_error_all(data_summary_response_error_all):
    assert common.CONVERTER.structure(data_summary_response_error_all, msg.SummaryResponse)


def test_data_submission_snv(data_submission_snv):
    assert common.CONVERTER.structure(data_submission_snv, msg.SubmissionContainer)
