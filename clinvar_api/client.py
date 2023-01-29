"""REST API client code for communicating with server endpoints."""

import json
import typing

import attrs
import cattrs
from jsonschema import ValidationError
from logzero import logger
import requests

from clinvar_api import common, exceptions, models, msg, schemas

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

    #: Whether to validate submission payload before posting.
    presubmission_validation: bool = True

    #: Whether or not to verify SSL on submission.
    verify_ssl: bool = True


def submit_data(submission_container: models.SubmissionContainer, config: Config) -> models.Created:
    """Submit new data to ClinVar API.

    :param payload: The submission data.
    :param config: The connfiguration to use.
    :return: The information about the created submission.
    :raises exceptions.SubmissionFailed: on problems with the submission.
    """
    logger.info("Submitting with config %s", config)

    url_prefix = ENDPOINT_URL_TEST if config.use_testing else ENDPOINT_URL_PROD
    url_suffix = SUFFIX_DRYRUN if config.use_dryrun else ""
    url = f"{url_prefix}{url_suffix}"
    logger.debug("Will submit to URL %s", url)
    headers = {
        "SP-API-KEY": config.auth_token,
    }

    payload = cattrs.unstructure(submission_container.to_msg())
    logger.debug("Payload data is %s", json.dumps(payload, indent=2))
    cleaned_payload = common.clean_for_json(payload)
    logger.debug("Cleaned payload data is %s", json.dumps(cleaned_payload, indent=2))
    if config.presubmission_validation:
        logger.info("Validating payload...")
        schemas.validate_submission_payload(cleaned_payload)
        logger.info("... done validating payload")
    else:
        logger.info("Configured to NOT validate payload before submission")

    post_data = {
        "actions": [
            {"type": "AddData", "targetDb": "clinvar", "data": {"content": cleaned_payload}}
        ]
    }
    logger.debug("Overall POST payload is %s", post_data)

    response = requests.post(url, headers=headers, json=post_data, verify=config.verify_ssl)

    if response.ok:
        logger.info("API returned OK - %s:  %s", response.status_code, response.reason)
        if response.status_code == 204:  # no content, on dry-run
            logger.info("Server returned '204: No Content', constructing fake created message.")
            return models.Created(id="--NONE--dry-run-result--")
        else:
            created_msg = common.CONVERTER.structure(response.json(), msg.Created)
            return models.Created.from_msg(created_msg)
    else:
        logger.warning("API returned an error - %s: %s", response.status_code, response.reason)
        error_msg = common.CONVERTER.structure(response.json(), msg.Error)
        error_obj = models.Error.from_msg(error_msg)
        logger.debug("Full server response is %s", response.json())
        if hasattr(error_obj, "errors"):
            raise exceptions.SubmissionFailed(
                f"ClinVar submission failed: {error_obj.message}, errors: {error_obj.errors}"
            )
        else:
            raise exceptions.SubmissionFailed(f"ClinVar submission failed: {error_obj.message}")


@attrs.define(frozen=True)
class RetrieveStatusResult:
    """Result type for ``retrieve_status`` function."""

    #: The submission status.
    status: models.SubmissionStatus
    #: A dict mapping file URLs to the parsed ``Sum``.
    summaries: typing.Dict[str, models.SummaryResponse]


def _retrieve_status_summary(
    url: str, validate_response_json: bool = True
) -> models.SummaryResponse:
    """Retrieve status summary from the given URL."""
    response = requests.get(url)
    if response.ok:
        response_json = response.json()
        if validate_response_json:
            logger.debug("Validating status summary response ...")
            try:
                schemas.validate_status_summary(response_json)
            except ValidationError as e:
                logger.warning("Response summary validation JSON is invalid: %s", e)
            logger.debug("... done validating status summary response")
        sr_msg = cattrs.structure(response.json(), msg.SummaryResponse)
        return models.SummaryResponse.from_msg(sr_msg)
    else:
        raise exceptions.QueryFailed(
            f"Could not perform query: {response.status_code} {response.reason}"
        )


def retrieve_status(
    submission_id: str,
    config: Config,
) -> RetrieveStatusResult:
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
        "SP-API-KEY": config.auth_token,
    }
    logger.debug("Will query URL %s", url)
    response = requests.get(url, headers=headers)
    if response.ok:
        logger.info("API returned OK - %s: %s", response.status_code, response.reason)
        logger.debug("Structuring response ...")
        status_msg = common.CONVERTER.structure(response.json(), msg.SubmissionStatus)
        logger.debug(
            "structured response is %s",
            json.dumps(common.CONVERTER.unstructure(status_msg), indent=2),
        )
        logger.debug("... done structuring response")
        status_obj = models.SubmissionStatus.from_msg(status_msg)
        logger.info(
            "Attempting to fetch %d status summary files...",
            len(
                [
                    None
                    for action in status_obj.actions
                    for action_response in action.responses
                    for _ in action_response.files
                ]
            ),
        )
        summaries = {}
        for action in status_obj.actions:
            for action_response in action.responses:
                for file_ in action_response.files:
                    logger.info(" - fetching %s", file_.url)
                    summaries[file_.url] = _retrieve_status_summary(file_.url)
        logger.info("... done fetching status summary files")
        return RetrieveStatusResult(status=status_obj, summaries=summaries)
    else:
        logger.info("API returned an error %s: %s", response.status_code, response.reason)
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
