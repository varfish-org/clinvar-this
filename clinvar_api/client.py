"""REST API client code for communicating with server endpoints."""

import typing

import attrs
import cattrs
import requests

from clinvar_api import common, exceptions, models, msg

#: URL of the server endpoint (non-test/production).
ENDPOINT_URL_PROD = "https://submit.ncbi.nlm.nih.gov/api/v1/submissions/"

#: URL of the test endpoint.
ENDPOINT_URL_TEST = "https://submit.ncbi.nlm.nih.gov/apitest/v1/submissions/"

#: URL suffix for enabling dry-run.
SUFFIX_DRYRUN = "?dry-run=true"


def _obfuscate_repr(s):
    """Helper function for obfustating passwords"""
    if len(s) < 5:
        return repr("*" * len(s))
    else:
        return repr(s[:5] + "*" * (len(s) - 5))


@attrs.define(frozen=True)
class Config:
    """Configuration for the ``Client`` class."""

    #: Token to use for authentication.
    auth_token: str = attrs.field(repr=_obfuscate_repr)

    #: Whether to use the test endpoint.
    use_testing: bool = False

    #: Whether to use dry running.
    use_dryrun: bool = False


def submit_data(payload: models.SubmissionContainer, config: Config) -> models.Created:
    """Submit new data to ClinVar API.

    :param payload: The submission data.
    :param config: The connfiguration to use.
    :return: The information about the created submission.
    :raises exceptions.SubmissionFailed: on problems with the submission.
    """
    url_prefix = ENDPOINT_URL_TEST if config.use_testing else ENDPOINT_URL_PROD
    url_suffix = SUFFIX_DRYRUN if config.use_dryrun else ""
    url = f"{url_prefix}{url_suffix}"
    headers = {
        "Content-type": "application/json",
        "SP-API-KEY": config.auth_token,
    }
    response = requests.post(url, headers=headers, data=cattrs.unstructure(payload.to_msg()))
    if response.ok:
        created_msg = common.CONVERTER.structure(response.json(), msg.Created)
        return models.Created.from_msg(created_msg)
    else:
        error_msg = common.CONVERTER.structure(response.json(), msg.Error)
        error_obj = models.Error.from_msg(error_msg)
        raise exceptions.SubmissionFailed(f"ClinVar submission failed: {error_obj.message}")


@attrs.define(frozen=True)
class RetrieveStatusResult:
    """Result type for ``retrieve_status`` function."""

    #: The submission status.
    status: models.SubmissionStatus
    #: A dict mapping file URLs to the parsed ``Sum``.
    summaries: typing.Dict[str, models.SummaryResponse]


def _retrieve_status_summary(url: str) -> models.SummaryResponse:
    """Retrieve status summary from the given URL."""
    response = requests.get(url)
    if response.ok:
        sr_msg = cattrs.structure(response.json(), msg.SummaryResponse)
        return models.SummaryResponse.from_msg(sr_msg)
    else:
        raise exceptions.QueryFailed(
            f"Could not perform query: {response.status_code} {response.reason}"
        )


def retrieve_status(
    submission_id: str,
    config: Config,
):
    """Retrieve submission status from API.

    :param submission_id: The identifier of the submission as returned earlier from API.
    :param config: The connfiguration to use.
    :return: The information about the created submission.
    :raises exceptions.QueryFailed: on problems with the communication to the server.
    """
    url_prefix = ENDPOINT_URL_TEST if config.use_testing else ENDPOINT_URL_PROD
    url_suffix = SUFFIX_DRYRUN if config.use_dryrun else ""
    url = f"{url_prefix}{submission_id}/actions/{url_suffix}"
    headers = {
        "Content-type": "application/json",
        "SP-API-KEY": config.auth_token,
    }
    response = requests.get(url, headers=headers)
    if response.ok:
        status_msg = common.CONVERTER.structure(response.json(), msg.SubmissionStatus)
        status_obj = models.SubmissionStatus.from_msg(status_msg)
        summaries = {}
        for action in status_obj.actions:
            for action_response in action.responses:
                for file_ in action_response.files:
                    summaries[file_.url] = _retrieve_status_summary(file_.url)
        return RetrieveStatusResult(status=status_obj, summaries=summaries)
    else:
        response_json = response.json()
        raise exceptions.QueryFailed(f"ClinVar query failed: {response_json}")


class Client:
    """NCBI ClinVar REST API client."""

    def __init__(self, config: Config):
        self.config = config

    def submit_data(self, payload: models.SubmissionContainer) -> models.Created:
        """Submit new data to ClinVar API.

        :param payload: The submission data.
        :return: The information about the created submission.
        :raises exceptions.SubmissionFailed: on problems with the submission.
        """
        return submit_data(payload, self.config)

    def retrieve_status(self, submission_id: str) -> RetrieveStatusResult:
        """Retrieve submission status from API.

        :param submission_id: The identifier of the submission as returned earlier from API.
        :return: The information about the created submission.
        :raises exceptions.QueryFailed: on problems with the communication to the server.
        """
        return retrieve_status(submission_id, self.config)
