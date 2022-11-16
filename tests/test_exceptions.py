import pytest

from clinvar_api import exceptions


def test_clinvar_api_exception():
    with pytest.raises(exceptions.ClinvarApiException):
        raise exceptions.ClinvarApiException()


def test_submission_failed():
    with pytest.raises(exceptions.SubmissionFailed):
        raise exceptions.SubmissionFailed()


def test_query_failed():
    with pytest.raises(exceptions.QueryFailed):
        raise exceptions.QueryFailed()
