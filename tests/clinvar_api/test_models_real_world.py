from clinvar_api import common, models, msg


def test_from_msg_data_created(data_created):
    msg_record = common.CONVERTER.structure(data_created, msg.Created)
    assert models.Created.from_msg(msg_record)


def test_from_msg_data_message(data_message):
    msg_record = common.CONVERTER.structure(data_message, msg.Error)
    assert models.Error.from_msg(msg_record)


def test_from_msg_data_submission_submitted(data_submission_submitted):
    msg_record = common.CONVERTER.structure(data_submission_submitted, msg.SubmissionStatus)
    assert models.SubmissionStatus.from_msg(msg_record)


def test_from_msg_data_submission_processing(data_submission_processing):
    msg_record = common.CONVERTER.structure(data_submission_processing, msg.SubmissionStatus)
    assert models.SubmissionStatus.from_msg(msg_record)


def test_from_msg_data_submission_processed(data_submission_processed):
    msg_record = common.CONVERTER.structure(data_submission_processed, msg.SubmissionStatus)
    assert models.SubmissionStatus.from_msg(msg_record)


def test_from_msg_data_partially_successful_submission(data_partially_successful_submission):
    msg_record = common.CONVERTER.structure(
        data_partially_successful_submission, msg.SubmissionStatus
    )
    assert models.SubmissionStatus.from_msg(msg_record)
