"""Exceptions used in ``clinvar_this`` module."""


class ClinvarThisException(Exception):
    """Base exception class."""


class IOException(ClinvarThisException):
    """Raised on problems with I/O in ``clinvar-this``."""


class ConfigException(ClinvarThisException):
    """Raised on configuration problems with ``clinvar-this``."""


class ConfigFileMissingException(ClinvarThisException):
    """Raised if the configuration file is missing."""


class ArgumentsError(ClinvarThisException):
    """Raised on problems with program arguments."""


class InvalidFormat(ClinvarThisException):
    """Raised on problems file contents in ``clinvar-this``."""
