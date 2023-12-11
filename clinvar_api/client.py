"""REST API client code for communicating with server endpoints."""

import asyncio
import contextlib
import json
import typing

import httpx
from jsonschema import ValidationError
from logzero import logger
from pydantic import BaseModel, SecretStr
from pydantic.config import ConfigDict

from clinvar_api import common, exceptions, models, msg, schemas

#: URL of the server endpoint (non-test/production).
ENDPOINT_URL_PROD = "https://submit.ncbi.nlm.nih.gov/api/v1/submissions/"

#: URL of the test endpoint.
ENDPOINT_URL_TEST = "https://submit.ncbi.nlm.nih.gov/apitest/v1/submissions/"

#: URL suffix for enabling dry-run.
SUFFIX_DRYRUN = "?dry-run=true"


class Config(BaseModel):
    """Configuration for the ``Client`` class."""

    model_config = ConfigDict(frozen=True)

    #: Token to use for authentication.
    auth_token: SecretStr

    #: Whether to use the test endpoint.
    use_testing: bool = False

    #: Whether to use dry running.
    use_dryrun: bool = False

    #: Whether to validate submission payload before posting.
    presubmission_validation: bool = True

    #: Whether or not to verify SSL on submission.
    verify_ssl: bool = True


class _SubmitData:
    """Helper class to reduce redundancy betwee sync/async `sumbit_data`."""

    def __init__(self, submission_container: models.SubmissionContainer, config: Config):
        self.submission_container = submission_container
        self.config = config

        self.url: str = ""
        self.headers: typing.Dict[str, str] = {}
        self.post_data: typing.Dict[str, typing.Any] = {}

    def before_post(self) -> typing.Tuple[str, typing.Dict[str, str], typing.Dict[str, typing.Any]]:
        logger.info("Submitting with config %s", self.config)

        url_prefix = ENDPOINT_URL_TEST if self.config.use_testing else ENDPOINT_URL_PROD
        url_suffix = SUFFIX_DRYRUN if self.config.use_dryrun else ""
        url = f"{url_prefix}{url_suffix}"
        logger.debug("Will submit to URL %s", url)
        headers = {
            "SP-API-KEY": self.config.auth_token.get_secret_value(),
        }

        payload = self.submission_container.to_msg().model_dump(mode="json")
        logger.debug("Payload data is %s", json.dumps(payload, indent=2))
        cleaned_payload = common.clean_for_json(payload)
        logger.debug("Cleaned payload data is %s", json.dumps(cleaned_payload, indent=2))
        if self.config.presubmission_validation:
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
        return url, headers, post_data

    def after_post(self, response: httpx.Response):
        if httpx.codes.is_success(response.status_code):
            logger.info("API returned OK - %s", response.status_code)
            if response.status_code == 204:  # no content, on dry-run
                logger.info("Server returned '204: No Content', constructing fake created message.")
                return models.Created(id="--NONE--dry-run-result--")
            else:
                created_msg = msg.Created.model_validate_json(response.content)
                return models.Created.from_msg(created_msg)
        else:
            logger.warning("API returned an error - %s", response.status_code)
            error_msg = msg.Error.model_validate_json(response.content)
            error_obj = models.Error.from_msg(error_msg)
            logger.debug("Full server response is %s", response.json())
            if hasattr(error_obj, "errors"):
                raise exceptions.SubmissionFailed(
                    f"ClinVar submission failed: {error_obj.message}, errors: {error_obj.errors}"
                )
            else:
                raise exceptions.SubmissionFailed(f"ClinVar submission failed: {error_obj.message}")


def submit_data(submission_container: models.SubmissionContainer, config: Config) -> models.Created:
    """Submit new data to ClinVar API (sync).

    :param submission_container: The submission data.
    :param config: The connfiguration to use.
    :return: The information about the created submission.
    :raises exceptions.SubmissionFailed: on problems with the submission.
    """
    helper = _SubmitData(submission_container, config)
    url, headers, post_data = helper.before_post()
    response = httpx.post(url, headers=headers, json=post_data, verify=config.verify_ssl)
    return helper.after_post(response)


async def async_submit_data(
    submission_container: models.SubmissionContainer, config: Config
) -> models.Created:
    """Submit new data to ClinVar API via async API (async).

    :param submission_container: The submission data.
    :param config: The connfiguration to use.
    :return: The information about the created submission.
    :raises exceptions.SubmissionFailed: on problems with the submission.
    """
    helper = _SubmitData(submission_container, config)
    url, headers, post_data = helper.before_post()
    async with httpx.AsyncClient(verify=config.verify_ssl) as client:
        response = await client.post(url, headers=headers, json=post_data)
    return helper.after_post(response)


class RetrieveStatusResult(BaseModel):
    """Result type for ``retrieve_status`` function."""

    model_config = ConfigDict(frozen=True)

    #: The submission status.
    status: models.SubmissionStatus
    #: A dict mapping file URLs to the parsed ``Sum``.
    summaries: typing.Dict[str, models.SummaryResponse]


def _handle_retrieved_status_summaries(
    response: httpx.Response, validate_response_json: bool = True
) -> models.SummaryResponse:
    """Handle retrieved status summary from the given URL."""
    if httpx.codes.is_success(response.status_code):
        response_json = response.json()
        if validate_response_json:
            logger.debug("Validating status summary response ...")
            try:
                schemas.validate_status_summary(response_json)
            except ValidationError as e:
                logger.warning("Response summary validation JSON is invalid: %s", e)
            logger.debug("... done validating status summary response")
        sr_msg = msg.SummaryResponse.model_validate_json(response.content)
        return models.SummaryResponse.from_msg(sr_msg)
    else:
        raise exceptions.QueryFailed(f"Could not perform query: {response.status_code}")


class _RetrieveStatus:
    """Helper class to reduce redundancy betwee sync/async `retrieve_status`."""

    def __init__(self, submission_id: str, config: Config):
        self.submission_id = submission_id
        self.config = config

    def before_first_get(self) -> typing.Tuple[str, typing.Dict[str, str]]:
        url_prefix = ENDPOINT_URL_TEST if self.config.use_testing else ENDPOINT_URL_PROD
        url_suffix = SUFFIX_DRYRUN if self.config.use_dryrun else ""
        url = f"{url_prefix}{self.submission_id}/actions/{url_suffix}"
        headers = {
            "SP-API-KEY": self.config.auth_token.get_secret_value(),
        }
        logger.debug("Will query URL %s", url)
        return url, headers

    def after_first_get_failure(self, response: httpx.Response):
        logger.info("API returned an error %s", response.status_code, response)
        response_json = response.json()
        raise exceptions.QueryFailed(f"ClinVar query failed: {response_json}")

    def after_first_get_success(
        self, response: httpx.Response
    ) -> typing.Tuple[typing.List[str], models.SubmissionStatus]:
        logger.info("API returned OK - %s", response.status_code)
        logger.debug("Structuring response ...")
        status_msg = msg.SubmissionStatus.model_validate_json(response.content)
        logger.debug(
            "structured response is %s",
            status_msg.model_dump_json(indent=2),
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
        more_urls: typing.List[str] = []
        for action in status_obj.actions:
            for action_response in action.responses:
                for file_ in action_response.files:
                    more_urls.append(file_.url)
        return more_urls, status_obj

    def after_get_more_urls(
        self, status_obj: models.SubmissionStatus, more_results: typing.Dict[str, httpx.Response]
    ) -> RetrieveStatusResult:
        summaries = {}
        for url, response in more_results.items():
            summaries[url] = _handle_retrieved_status_summaries(response)
        logger.info("... done fetching status summary files")
        return RetrieveStatusResult(status=status_obj, summaries=summaries)


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
    helper = _RetrieveStatus(submission_id, config)
    url, headers = helper.before_first_get()
    response = httpx.get(url, headers=headers)
    if httpx.codes.is_success(response.status_code):
        more_urls, status_obj = helper.after_first_get_success(response)

        more_results = {}
        for url in more_urls:
            logger.info(" - fetching %s", url)
            more_results[url] = httpx.get(url)

        return helper.after_get_more_urls(status_obj, more_results)
    else:
        return helper.after_first_get_failure(response)


async def async_retrieve_status(
    submission_id: str,
    config: Config,
) -> RetrieveStatusResult:
    """Retrieve submission status from API.

    :param submission_id: The identifier of the submission as returned earlier from API.
    :param config: The connfiguration to use.
    :return: The information about the created submission.
    :raises exceptions.QueryFailed: on problems with the communication to the server.
    """
    helper = _RetrieveStatus(submission_id, config)
    url, headers = helper.before_first_get()
    async with httpx.AsyncClient(verify=config.verify_ssl) as client:
        response = await client.get(url, headers=headers)
    if httpx.codes.is_success(response.status_code):
        more_urls, status_obj = helper.after_first_get_success(response)

        async with contextlib.AsyncExitStack() as stack:
            tasks: typing.Dict[str, typing.Awaitable[httpx.Response]] = {}
            for url in more_urls:
                logger.info(" - fetching %s", url)
                client = await stack.enter_async_context(
                    httpx.AsyncClient(verify=config.verify_ssl)
                )
                tasks[url] = client.get(url)

            more_results: typing.Dict[str, httpx.Response] = dict(
                zip(tasks.keys(), await asyncio.gather(*tasks.values()))
            )

        return helper.after_get_more_urls(status_obj, more_results)
    else:
        return helper.after_first_get_failure(response)


class Client:
    """NCBI ClinVar REST API client (sync)."""

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


class AsyncClient:
    """NCBI ClinVar REST API client (async)."""

    def __init__(self, config: Config):
        self.config = config

    async def submit_data(self, payload: models.SubmissionContainer) -> models.Created:
        """Submit new data to ClinVar API.

        :param payload: The submission data.
        :return: The information about the created submission.
        :raises exceptions.SubmissionFailed: on problems with the submission.
        """
        return await async_submit_data(payload, self.config)

    async def retrieve_status(self, submission_id: str) -> RetrieveStatusResult:
        """Retrieve submission status from API.

        :param submission_id: The identifier of the submission as returned earlier from API.
        :return: The information about the created submission.
        :raises exceptions.QueryFailed: on problems with the communication to the server.
        """
        return await async_retrieve_status(submission_id, self.config)
