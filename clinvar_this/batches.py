"""Management of batches."""

import datetime
import json
import pathlib
import typing

from attrs import evolve
from logzero import logger
from tabulate import tabulate

from clinvar_api import client, common, models
from clinvar_this import config, exceptions
from clinvar_this.io import tsv

#: Shared files directory
SHARE_DIR = pathlib.Path.home() / ".local" / "share" / "clinvar-this"

#: Format string
FORMAT_STR = "%Y%m%d%H%M%S"


def _list_get_batches(share_dir: pathlib.Path):
    if not share_dir.exists():
        return []
    else:
        return [share_dir / path for path in share_dir.glob("*") if path.is_dir()]


def list_(config: config.Config):
    """List batches to stdout."""
    print(f"Listing batches at {SHARE_DIR}/{config.profile}")
    _ = config
    paths = _list_get_batches(SHARE_DIR / config.profile)
    if not paths:
        table = [["-- NO BATCHES YET --"]]
        print(tabulate(table))
    else:
        table = [[path.name] for path in sorted(paths)]
        print(tabulate(table, headers=["path"], tablefmt="grid"))


def gen_name(config: config.Config) -> str:
    """Generate batch name that does not exist yet."""
    base = datetime.date.today().strftime("%Y-%m-%d")
    for i in range(1000):
        dirname = "%s-%03d" % (base, i)
        if not (SHARE_DIR / config.profile / dirname).exists():
            return dirname
    else:  # pragma: no cover
        raise exceptions.IOException("Could not generate batch name")


def _write_payload(submission_container: models.SubmissionContainer, profile: str, name: str):
    """Write out payload to a new JSON file."""
    # Create directory for batch.
    batch_dir = SHARE_DIR / profile / name
    batch_dir.mkdir(exist_ok=True, parents=True)
    # Write out payload.
    timestamp = datetime.datetime.now().strftime(FORMAT_STR)
    payload_path = batch_dir / f"payload.{timestamp}.json"
    payload_json = json.dumps(common.CONVERTER.unstructure(submission_container), indent=2)
    with payload_path.open("wt") as outputf:
        outputf.write(payload_json)


def _merge_submission_container(
    base: models.SubmissionContainer,
    patch: models.SubmissionContainer,
) -> models.SubmissionContainer:
    """Update base submission container with new one.

    The following attributes will be copied from ``patch`` to ``base``:

    - mode of inheritance
    - clinical significance
        - clinical significance description (ACMG grading)
        - condition
    """
    logger.info("Merging submission information...")

    def merge_submission(
        base: models.SubmissionClinvarSubmission,
        patch: models.SubmissionClinvarSubmission,
    ) -> models.SubmissionClinvarSubmission:
        return evolve(
            base,
            condition_set=patch.condition_set,
            clinical_significance=patch.clinical_significance,
            observed_in=patch.observed_in,
        )

    patch_clinvar_submission = {
        clinvar_submission.local_key: clinvar_submission
        for clinvar_submission in (patch.clinvar_submission or [])
    }
    clinvar_submissions = []
    for submission in base.clinvar_submission or []:
        if submission.local_key in patch_clinvar_submission:
            clinvar_submissions.append(
                merge_submission(submission, patch_clinvar_submission[submission.local_key])
            )
        else:
            clinvar_submissions.append(submission)
    result = evolve(base, clinvar_submission=clinvar_submissions)
    logger.info("... done merging submission information")
    return result


def import_(config: config.Config, name: str, path: str, metadata: typing.Tuple[str, ...]):
    """Import the data file at ``path`` into the batch of name ``name``."""
    existing_payloads = list((SHARE_DIR / config.profile / name).glob("payload.*.json"))
    if existing_payloads:
        logger.info("Loading existing payload for later merging with new one")
        previous_submission_container = _load_latest_payload(config.profile, name)
    else:
        previous_submission_container = None
    if path.endswith(".tsv") or path.endswith(".txt"):
        tsv_records = tsv.read_tsv(path=path)
        batch_metadata = tsv.batch_metadata_from_mapping(metadata, use_defaults=True)
        new_submission_container = tsv.tsv_records_to_submission_container(
            tsv_records, batch_metadata
        )
        if previous_submission_container:
            submission_container = _merge_submission_container(
                base=previous_submission_container,
                patch=new_submission_container,
            )
        else:
            submission_container = new_submission_container
        _write_payload(submission_container, config.profile, name)
    else:
        raise exceptions.IOException(f"File extension of {path} cannot be handled.")


def _load_latest_payload(profile: str, name: str):
    submission_path = SHARE_DIR / profile / name
    payload_paths = list(sorted(submission_path.glob("payload.*.json")))
    if not payload_paths:
        raise exceptions.ClinvarThisException(f"Found no payload JSON file at {submission_path}")

    payload_path = submission_path / payload_paths[-1]
    with payload_path.open("rt") as inputf:
        payload_json = inputf.read()
    payload_unstructured = json.loads(payload_json)
    return common.CONVERTER.structure(payload_unstructured, models.SubmissionContainer)


def export_(config: config.Config, name: str, path: str, force: bool = False):
    """Export the batch with the given ``name`` to the file at ``path``."""
    if pathlib.Path(path).exists() and not force:
        raise exceptions.IOException(
            f"File at output path {path} already exists. Use --force to overwrite."
        )
    if path.endswith(".tsv") or path.endswith(".txt"):
        payload = _load_latest_payload(config.profile, name)
        tsv_records = tsv.submission_container_to_tsv_records(payload)
        tsv.write_tsv(tsv_records, path=path)
    else:
        raise exceptions.IOException(f"File extension of {path} cannot be handled.")


def update(config: config.Config, name: str, metadata: typing.Tuple[str, ...]):
    """Update the batch' meta data."""
    batch_metadata = tsv.batch_metadata_from_mapping(metadata, use_defaults=False)
    _ = batch_metadata


def submit(config: config.Config, name: str, *, use_testing: bool = False, dry_run: bool = False):
    """Submit the batch to ClinVar."""
    if not config.auth_token:
        raise exceptions.ConfigException("auth_token not configured")

    client_obj = client.Client(
        client.Config(auth_token=config.auth_token, use_testing=use_testing, use_dryrun=dry_run)
    )

    payload = _load_latest_payload(config.profile, name)

    logger.info("Initiating submission to ClinVar API")
    client_res = client_obj.submit_data(payload)

    # Terminate earlyier in dry-run mode.
    if dry_run:
        logger.info("In dry-run mode, not writing out response.")
        return

    timestamp = datetime.datetime.now().strftime(FORMAT_STR)
    response_path = SHARE_DIR / config.profile / name / f"submission-response.{timestamp}.json"
    response_data = common.CONVERTER.unstructure(client_res)
    logger.info("Writing out server response to %s", response_path)
    with response_path.open("wt") as outputf:
        json.dump(response_data, outputf)
    logger.info(
        "The ClinVar API has accepted your submission and will perform additional checks in the background."
    )
    logger.info(
        (
            "The next step is to run ``clinvar-this batch retrieve %s`` and wait until you get a "
            "final success or error response"
        ),
        name,
    )
    logger.info("All done. Have a nice day!")


def _retrieve_store_response(
    config: config.Config, name: str, status_result: client.RetrieveStatusResult
):
    """Store information from the retrieve status result into a new payload JSON file.

    Currently, this is the clinvar accession only.
    """
    logger.debug("Updating local payload from retrieve status response ...")
    logger.debug("Obtaining local key to accession map")
    local_key_to_accession = {}
    local_id_to_error = {}
    for summary_response in status_result.summaries.values():
        submissions = summary_response.submissions or []
        for submission in submissions:
            local_key_to_accession[
                submission.identifiers.local_key
            ] = submission.identifiers.clinvar_accession
            errors = [
                error_inner.user_message
                for error_outer in (submission.errors or [])
                for error_inner in (error_outer.output.errors or [])
            ]
            local_id_to_error[submission.identifiers.local_id] = "; ".join(errors)
    logger.debug("Update map is %s", local_key_to_accession)
    logger.debug("Loading latest payload")
    payload = _load_latest_payload(config.profile, name)
    logger.debug("Updating local payload")
    clinvar_submission = [
        evolve(
            submission,
            clinvar_accession=local_key_to_accession.get(
                submission.local_key, submission.clinvar_accession
            ),
            record_status=models.RecordStatus.UPDATE
            if submission.local_key in local_key_to_accession
            else models.RecordStatus.NOVEL,
            extra_data={
                **(submission.extra_data or {}),
                "error_msg": local_id_to_error.get(submission.local_id, ""),
            },
        )
        for submission in payload.clinvar_submission
    ]
    updated_payload = evolve(payload, clinvar_submission=clinvar_submission)
    logger.debug("Write out updated payload")
    _write_payload(updated_payload, config.profile, name)
    logger.debug("... done updating local payload from retrieve status response")


def retrieve(config: config.Config, name: str, *, use_testing: bool = False):
    """Retrieve current processing status from ClinVar."""
    client_obj = client.Client(client.Config(auth_token=config.auth_token, use_testing=use_testing))

    submission_path = SHARE_DIR / config.profile / name
    submission_response_paths = list(sorted(submission_path.glob("submission-response.*.json")))

    if not submission_path.exists():
        raise exceptions.ClinvarThisException(f"Submission does not exist at {submission_path}")
    elif not submission_response_paths:
        raise exceptions.ClinvarThisException(
            f"Submission not submitted? No submission response at {submission_path}"
        )

    submission_response_path = submission_path / submission_response_paths[-1]
    logger.info("Loading response from %s", submission_response_path)
    with submission_response_path.open("rt") as inputf:
        created = common.CONVERTER.structure(json.load(inputf), models.Created)
    logger.info("Submission ID is %s", created.id)

    logger.info("Initiating fetching of status from ClinVar API")
    status_result = client_obj.retrieve_status(created.id)
    timestamp = datetime.datetime.now().strftime(FORMAT_STR)
    retrieve_response_path = submission_path / f"retrieve-response.{timestamp}.json"
    logger.debug("Writing out response to %s", retrieve_response_path)
    with retrieve_response_path.open("wt") as outputf:
        json.dump(common.CONVERTER.unstructure(status_result), outputf, indent=2)

    status_str = status_result.status.actions[0].status
    if status_str in ["submitted", "processing"]:
        logger.info(f"Status is {status_str}, be patient and check back in a while...")
        logger.info(
            "Submissions with errors tend to fail quickly while successful submissions tend to take a while."
        )
    elif status_str == "processed":
        logger.info("Submission has been processed successfully")
        logger.info("Will now update local information from response...")
        _retrieve_store_response(config, name, status_result)
        logger.info("... done updating local information from response")
    elif status_str == "error":
        logger.error("There were errors in your submission")
        logger.info("Check the file %s for details", retrieve_response_path)
        logger.info("Will now update local information from response...")
        _retrieve_store_response(config, name, status_result)
        logger.info("... done updating local information from response")
    else:
        logger.error("Status is %s and clinvar-this does not know how to handle this yet!")
        raise exceptions.ClinvarThisException(f"Unknown status {status_str}")
