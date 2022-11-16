"""Module with the exception classes."""


class ClinvarApiException(Exception):
    """Base exception for ``clinvar_api``."""


class SubmissionFailed(ClinvarApiException):
    """Raised when there was a problem with submitting to ClinVar."""


class QueryFailed(ClinvarApiException):
    """Raised when the status query failed."""
