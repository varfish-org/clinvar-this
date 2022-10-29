from clinvar_api import api_models, api_msg, common


def test_from_msg_data_created(data_created):
    msg = common.CONVERTER.structure(data_created, api_msg.Created)
    assert api_models.Created.from_msg(msg)


def test_from_msg_data_message(data_message):
    msg = common.CONVERTER.structure(data_message, api_msg.Error)
    assert api_models.Error.from_msg(msg)


def test_from_msg_data_submission_submitted(data_submission_submitted):
    msg = common.CONVERTER.structure(data_submission_submitted, api_msg.SubmissionStatus)
    assert api_models.SubmissionStatus.from_msg(msg)


def test_from_msg_data_submission_processing(data_submission_processing):
    msg = common.CONVERTER.structure(data_submission_processing, api_msg.SubmissionStatus)
    assert api_models.SubmissionStatus.from_msg(msg)


def test_from_msg_data_submission_processed(data_submission_processed):
    msg = common.CONVERTER.structure(data_submission_processed, api_msg.SubmissionStatus)
    assert api_models.SubmissionStatus.from_msg(msg)


def test_from_msg_data_partially_successful_submission(data_partially_successful_submission):
    msg = common.CONVERTER.structure(data_partially_successful_submission, api_msg.SubmissionStatus)
    assert api_models.SubmissionStatus.from_msg(msg)
