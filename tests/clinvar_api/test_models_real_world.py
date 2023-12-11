from clinvar_api import models, msg


def test_from_msg_data_created(data_created):
    msg_record = msg.Created.model_validate(data_created)
    assert models.Created.from_msg(msg_record)


def test_from_msg_data_message(data_message):
    msg_record = msg.Error.model_validate(data_message)
    assert models.Error.from_msg(msg_record)


def test_from_msg_data_submission_submitted(data_submission_submitted):
    msg_record = msg.SubmissionStatus.model_validate(data_submission_submitted)
    assert models.SubmissionStatus.from_msg(msg_record)


def test_from_msg_data_submission_processing(data_submission_processing):
    msg_record = msg.SubmissionStatus.model_validate(data_submission_processing)
    assert models.SubmissionStatus.from_msg(msg_record)


def test_from_msg_data_submission_processed(data_submission_processed):
    msg_record = msg.SubmissionStatus.model_validate(data_submission_processed)
    assert models.SubmissionStatus.from_msg(msg_record)


def test_from_msg_data_partially_successful_submission(data_partially_successful_submission):
    msg_record = msg.SubmissionStatus.model_validate(data_partially_successful_submission)
    assert models.SubmissionStatus.from_msg(msg_record)
