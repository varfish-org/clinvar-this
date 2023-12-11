"""Management of batches."""

import datetime
import pathlib
import typing

from logzero import logger
from tabulate import tabulate

from clinvar_api import client, models
from clinvar_this import config, exceptions
from clinvar_this.io import tsv


def get_share_dir():
    """Shared files directory"""
    return pathlib.Path.home() / ".local" / "share" / "clinvar-this"


#: Format string
FORMAT_STR = "%Y%m%d%H%M%S"


def _list_get_batches(share_dir: pathlib.Path):
    if not share_dir.exists():
        return []
    else:
        return [share_dir / path for path in share_dir.glob("*") if path.is_dir()]


def list_(config: config.Config):
    """List batches to stdout."""
    share_dir = get_share_dir()
    print(f"Listing batches at {share_dir}/{config.profile}")
    _ = config
    paths = _list_get_batches(share_dir / config.profile)
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
        if not (get_share_dir() / config.profile / dirname).exists():
            return dirname
    else:  # pragma: no cover
        raise exceptions.IOException("Could not generate batch name")


def _write_payload(submission_container: models.SubmissionContainer, profile: str, name: str):
    """Write out payload to a new JSON file."""
    # Create directory for batch.
    batch_dir = get_share_dir() / profile / name
    batch_dir.mkdir(exist_ok=True, parents=True)
    # Write out payload.
    timestamp = datetime.datetime.now().strftime(FORMAT_STR)
    payload_path = batch_dir / f"payload.{timestamp}.json"
    payload_json = submission_container.model_dump_json(indent=2)
    with payload_path.open("wt") as outputf:
        outputf.write(payload_json)
        outputf.write("\n")


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
        clinvar_accession = base.clinvar_accession or patch.clinvar_accession
        return base.model_copy(
            update={
                "clinvar_accession": clinvar_accession,
                "condition_set": patch.condition_set,
                "clinical_significance": patch.clinical_significance,
                "observed_in": patch.observed_in,
            }
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
    result = base.model_copy(update={"clinvar_submission": clinvar_submissions})
    logger.info("... done merging submission information")
    return result


def import_(config: config.Config, name: str, path: str, metadata: typing.Tuple[str, ...]):
    """Import the data file at ``path`` into the batch of name ``name``."""
    existing_payloads = list((get_share_dir() / config.profile / name).glob("payload.*.json"))
    if existing_payloads:
        logger.info("Loading existing payload for later merging with new one")
        previous_submission_container = _load_latest_payload(config.profile, name)
    else:
        logger.info("Creating new payload only")
        previous_submission_container = None
    if path.endswith(".tsv") or path.endswith(".txt"):
        tsv_type = tsv.guess_tsv_type(path)
        if tsv_type in (tsv.TsvType.SEQ_VAR, tsv.TsvType.STRUC_VAR):
            batch_metadata = tsv.batch_metadata_from_mapping(metadata, use_defaults=True)
            if tsv_type == tsv.TsvType.SEQ_VAR:
                new_submission_container = tsv.seq_var_tsv_records_to_submission_container(
                    tsv.read_seq_var_tsv(path=path), batch_metadata
                )
            else:  # tsv_type == tsv.TsvType.STRUC_VAR
                new_submission_container = tsv.struc_var_tsv_records_to_submission_container(
                    tsv.read_struc_var_tsv(path=path), batch_metadata
                )
            if previous_submission_container:
                submission_container = _merge_submission_container(
                    base=previous_submission_container,
                    patch=new_submission_container,
                )
            else:
                submission_container = new_submission_container
        else:
            raise exceptions.IOException(f"Could not guess TSV file type from header for {path}")
        _write_payload(submission_container, config.profile, name)
    else:  # pragma: no cover
        raise exceptions.IOException(f"File extension of {path} cannot be handled.")


def _load_latest_payload(profile: str, name: str):
    submission_path = get_share_dir() / profile / name
    payload_paths = list(sorted(submission_path.glob("payload.*.json")))
    if not payload_paths:  # pragma: no cover
        raise exceptions.ClinvarThisException(f"Found no payload JSON file at {submission_path}")

    payload_path = submission_path / payload_paths[-1]
    with payload_path.open("rt") as inputf:
        payload_json = inputf.read()
    return models.SubmissionContainer.model_validate_json(payload_json)


def export(
    config: config.Config, name: str, path: str, force: bool = False, struc_var: bool = False
):
    """Export the batch with the given ``name`` to the file at ``path``."""
    if pathlib.Path(path).exists() and not force:
        raise exceptions.IOException(
            f"File at output path {path} already exists. Use --force to overwrite."
        )
    if path.endswith(".tsv") or path.endswith(".txt"):
        payload = _load_latest_payload(config.profile, name)
        if struc_var:
            tsv.write_struc_var_tsv(
                tsv_records=tsv.submission_container_to_struc_var_tsv_records(payload), path=path
            )
        else:
            tsv.write_seq_var_tsv(
                tsv_records=tsv.submission_container_to_seq_var_tsv_records(payload), path=path
            )
    else:  # pragma: no cover
        raise exceptions.IOException(f"File extension of {path} cannot be handled.")


def update_metadata(config: config.Config, name: str, metadata: typing.Tuple[str, ...]):
    """Update the batch' meta data."""
    batch_metadata = tsv.batch_metadata_from_mapping(metadata, use_defaults=False)
    _ = batch_metadata


def submit(config: config.Config, name: str, *, use_testing: bool = False, dry_run: bool = False):
    """Submit the batch to ClinVar."""
    if not config.auth_token:  # pragma: no cover
        raise exceptions.ConfigException("auth_token not configured")

    client_obj = client.Client(
        client.Config(
            auth_token=config.auth_token,
            use_testing=use_testing,
            use_dryrun=dry_run,
            verify_ssl=config.verify_ssl,
        )
    )

    payload = _load_latest_payload(config.profile, name)

    logger.info("Initiating submission to ClinVar API")
    client_res = client_obj.submit_data(payload)

    # Terminate earlyier in dry-run mode.
    if dry_run:
        logger.info("In dry-run mode, not writing out response.")
        return

    timestamp = datetime.datetime.now().strftime(FORMAT_STR)
    response_path = (
        get_share_dir() / config.profile / name / f"submission-response.{timestamp}.json"
    )

    logger.info("Writing out server response to %s", response_path)
    with response_path.open("wt") as outputf:
        print(client_res.model_dump_json(), file=outputf)
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
                submission.identifiers.local_key or submission.identifiers.clinvar_local_key
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
        submission.model_copy(
            update={
                "clinvar_accession": local_key_to_accession.get(
                    submission.local_key, submission.clinvar_accession
                ),
                "record_status": models.RecordStatus.UPDATE
                if submission.local_key in local_key_to_accession
                else models.RecordStatus.NOVEL,
                "extra_data": {
                    **(submission.extra_data or {}),
                    "error_msg": local_id_to_error.get(submission.local_id, ""),
                },
            }
        )
        for submission in payload.clinvar_submission
    ]
    updated_payload = payload.model_copy(update={"clinvar_submission": clinvar_submission})
    logger.debug("Write out updated payload")
    _write_payload(updated_payload, config.profile, name)
    logger.debug("... done updating local payload from retrieve status response")


def retrieve(config: config.Config, name: str, *, use_testing: bool = False):
    """Retrieve current processing status from ClinVar."""
    client_obj = client.Client(client.Config(auth_token=config.auth_token, use_testing=use_testing))

    submission_path = get_share_dir() / config.profile / name
    submission_response_paths = list(sorted(submission_path.glob("submission-response.*.json")))

    if not submission_path.exists():  # pragma: no cover
        raise exceptions.ClinvarThisException(f"Submission does not exist at {submission_path}")
    elif not submission_response_paths:  # pragma: no cover
        raise exceptions.ClinvarThisException(
            f"Submission not submitted? No submission response at {submission_path}"
        )

    submission_response_path = submission_path / submission_response_paths[-1]
    logger.info("Loading response from %s", submission_response_path)
    with submission_response_path.open("rb") as inputf:
        created = models.Created.model_validate_json(inputf.read())
    logger.info("Submission ID is %s", created.id)

    logger.info("Initiating fetching of status from ClinVar API")
    status_result = client_obj.retrieve_status(created.id)
    timestamp = datetime.datetime.now().strftime(FORMAT_STR)
    retrieve_response_path = submission_path / f"retrieve-response.{timestamp}.json"
    logger.debug("Writing out response to %s", retrieve_response_path)
    with retrieve_response_path.open("wt") as outputf:
        print(status_result.model_dump_json(indent=2), file=outputf)

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
    else:  # pragma: no cover
        logger.error("Status is %s and clinvar-this does not know how to handle this yet!")
        raise exceptions.ClinvarThisException(f"Unknown status {status_str}")
