import json
import os
import pathlib
from unittest.mock import MagicMock

from freezegun import freeze_time
import pytest

import clinvar_api
from clinvar_api import models
from clinvar_api.client import RetrieveStatusResult
from clinvar_api.common import CONVERTER
from clinvar_this import batches, exceptions
from clinvar_this.io import tsv as io_tsv

# We must read this outside of the test as we use the fake file system.
with (pathlib.Path(__file__).parent / "data/batches/seq_variant.tsv").open("rt") as inputf:
    #: Small variant TSV for testing batches module.  Likely pathogenic.
    SEQ_VARIANT_TSV = inputf.read()

with (pathlib.Path(__file__).parent / "data/batches/struc_variant.tsv").open("rt") as inputf:
    #: Structural variant TSV for testing batches module.  Likely pathogenic.
    STRUC_VARIANT_TSV = inputf.read()

with (pathlib.Path(__file__).parent / "data/batches/seq_variant.payload.json").open("rt") as inputf:
    #: The ``SEQ_VARIANT_TSV`` after import for testing batches module.
    SEQ_VARIANT_PAYLOAD_JSON = inputf.read()

with (pathlib.Path(__file__).parent / "data/batches/struc_variant.payload.json").open(
    "rt"
) as inputf:
    #: The ``STRUC_VARIANT_TSV`` after import for testing batches module.
    STRUC_VARIANT_PAYLOAD_JSON = inputf.read()

with (pathlib.Path(__file__).parent / "data/batches/seq_variant-update.tsv").open("rt") as inputf:
    #: Sequence variant TSV for testing batches module.  Updated to Pathonenic.
    SEQ_VARIANT_UPDATE_TSV = inputf.read()

with (pathlib.Path(__file__).parent / "data/batches/struc_variant-update.tsv").open("rt") as inputf:
    #: Structural variant TSV for testing batches module.  Updated to Pathonenic.
    STRUC_VARIANT_UPDATE_TSV = inputf.read()

with (pathlib.Path(__file__).parent / "data/batches/seq_variant-update.payload.json").open(
    "rt"
) as inputf:
    #: The `SEQ_VARIANT_UPDATE_TSV` after import / merge.
    SEQ_VARIANT_UPDATE_PAYLOAD_JSON = inputf.read()

with (pathlib.Path(__file__).parent / "data/batches/struc_variant-update.payload.json").open(
    "rt"
) as inputf:
    #: The `STRUC_VARIANT_UPDATE_TSV` after import / merge.
    STRUC_VARIANT_UPDATE_PAYLOAD_JSON = inputf.read()

with (
    pathlib.Path(__file__).parent / "data/batches/seq_variant.retrieve-response-processing.json"
).open("rt") as inputf:
    #: A static response on retrieving with "processing" status.
    SEQ_VARIANT_RETRIEVE_RESPONSE_PROCESSING_JSON = inputf.read()

with (
    pathlib.Path(__file__).parent / "data/batches/seq_variant.retrieve-response-submitted.json"
).open("rt") as inputf:
    #: A static response on retrieving with "submitted" status.
    SEQ_VARIANT_RETRIEVE_RESPONSE_SUBMITTED_JSON = inputf.read()

with (
    pathlib.Path(__file__).parent / "data/batches/seq_variant.retrieve-response-success.json"
).open("rt") as inputf:
    #: A static response on retrieving with "success" status.
    SEQ_VARIANT_RETRIEVE_RESPONSE_SUCCESS_JSON = inputf.read()

with (pathlib.Path(__file__).parent / "data/batches/seq_variant.retrieve-response-error.json").open(
    "rt"
) as inputf:
    #: A static response on retrieving with "error" status.
    SEQ_VARIANT_RETRIEVE_RESPONSE_ERROR_JSON = inputf.read()

SUBMISSION_SCHEMA_JSON_PATH = (
    pathlib.Path(clinvar_api.__file__).parent / "schemas/submission_schema.json"
)
with SUBMISSION_SCHEMA_JSON_PATH.open("rt") as inputf:
    SUBMISSION_SCHEMA_JSON = inputf.read()


def test_list_no_batches_no_dir(fs, app_config, capsys):
    batches.list_(app_config)

    captured = capsys.readouterr()
    assert "-- NO BATCHES YET --" in captured.out


def test_list_no_batches_empty_repository(fs, app_config, capsys):
    fs.create_dir(
        os.path.expanduser("~/.local/share/clinvar-this/default"),
    )

    batches.list_(app_config)

    captured = capsys.readouterr()
    assert "-- NO BATCHES YET --" in captured.out


def test_list_with_batches(fs, app_config, capsys):
    fs.create_dir(
        os.path.expanduser("~/.local/share/clinvar-this/default/one"),
    )
    fs.create_dir(
        os.path.expanduser("~/.local/share/clinvar-this/default/two"),
    )

    batches.list_(app_config)

    captured = capsys.readouterr()
    assert "one" in captured.out
    assert "two" in captured.out


@freeze_time("2012-01-14")
def test_gen_name(fs, app_config):
    name = batches.gen_name(app_config)
    assert name == "2012-01-14-000"
    fs.create_dir(
        os.path.expanduser("~/.local/share/clinvar-this/default/2012-01-14-000"),
    )
    name = batches.gen_name(app_config)
    assert name == "2012-01-14-001"


def test_merge_submission_container():
    pass  # TODO:  more comprehensive tests


@freeze_time("2012-01-14")
def test_import_seq_variant_tsv_new(fs, app_config, monkeypatch):
    path_tsv = "/tmp/seq_variant.tsv"
    fs.create_file(path_tsv, contents=SEQ_VARIANT_TSV)

    def mock_uuid4():
        return "mock-uuid4"

    monkeypatch.setattr(io_tsv.uuid, "uuid4", mock_uuid4)

    batch_name = "the-batch"
    batches.import_(config=app_config, name=batch_name, path=path_tsv, metadata=())

    payload_path = os.path.expanduser(
        "~/.local/share/clinvar-this/default/the-batch/payload.20120114000000.json"
    )
    assert os.path.exists(payload_path)
    with open(payload_path, "rt") as inputf:
        payload_json = inputf.read()
    assert payload_json == SEQ_VARIANT_PAYLOAD_JSON


@freeze_time("2012-01-14")
def test_import_seq_variant_tsv_update(fs, app_config):
    path_tsv = "/tmp/seq_variant-update.tsv"
    fs.create_file(path_tsv, contents=SEQ_VARIANT_UPDATE_TSV)

    payload_path = os.path.expanduser(
        "~/.local/share/clinvar-this/default/the-batch/payload.20120114000000.json"
    )
    fs.create_file(
        os.path.expanduser(payload_path),
        contents=SEQ_VARIANT_PAYLOAD_JSON,
    )

    batch_name = "the-batch"
    batches.import_(config=app_config, name=batch_name, path=path_tsv, metadata=())

    filename = os.listdir(os.path.expanduser("~/.local/share/clinvar-this/default/the-batch"))[-1]

    payload_path = os.path.expanduser(f"~/.local/share/clinvar-this/default/the-batch/{filename}")
    assert os.path.exists(payload_path)
    with open(payload_path, "rt") as inputf:
        payload_json = inputf.read()
    assert payload_json == SEQ_VARIANT_UPDATE_PAYLOAD_JSON


@freeze_time("2012-01-14")
def test_import_deletion_tsv_new(fs):
    pass  # TODO


@freeze_time("2012-01-14")
def test_import_deletion_tsv_update(fs):
    pass  # TODO


@freeze_time("2012-01-14")
def test_import_structural_variant_tsv_new(fs, app_config, monkeypatch):
    path_tsv = "/tmp/seq_variant.tsv"
    fs.create_file(path_tsv, contents=STRUC_VARIANT_TSV)

    def mock_uuid4():
        return "mock-uuid4"

    monkeypatch.setattr(io_tsv.uuid, "uuid4", mock_uuid4)

    batch_name = "the-batch"
    batches.import_(config=app_config, name=batch_name, path=path_tsv, metadata=())

    payload_path = os.path.expanduser(
        "~/.local/share/clinvar-this/default/the-batch/payload.20120114000000.json"
    )
    assert os.path.exists(payload_path)
    with open(payload_path, "rt") as inputf:
        payload_json = inputf.read()
    assert payload_json == STRUC_VARIANT_PAYLOAD_JSON


def test_import_structural_variant_tsv_update(fs, app_config):
    path_tsv = "/tmp/struc_variant-update.tsv"
    fs.create_file(path_tsv, contents=STRUC_VARIANT_UPDATE_TSV)

    payload_path = os.path.expanduser(
        "~/.local/share/clinvar-this/default/the-batch/payload.20120113000000.json"
    )
    fs.create_file(
        os.path.expanduser(payload_path),
        contents=STRUC_VARIANT_PAYLOAD_JSON,
    )
    assert os.path.exists(payload_path)

    batch_name = "the-batch"
    batches.import_(config=app_config, name=batch_name, path=path_tsv, metadata=())

    fname = os.listdir(os.path.expanduser("~/.local/share/clinvar-this/default/the-batch"))[-1]

    payload_path = os.path.expanduser(f"~/.local/share/clinvar-this/default/the-batch/{fname}")
    assert os.path.exists(payload_path)
    with open(payload_path, "rt") as inputf:
        payload_json = inputf.read()
    assert payload_json == STRUC_VARIANT_UPDATE_PAYLOAD_JSON


@pytest.mark.parametrize(
    "exists,force",
    [
        (False, False),
        (True, False),
        (True, True),
    ],
)
def test_export_seq_variant_tsv(fs, app_config, exists, force):
    fs.create_file(
        os.path.expanduser(
            "~/.local/share/clinvar-this/default/the-batch/payload.20120113000000.json"
        ),
        contents=SEQ_VARIANT_PAYLOAD_JSON,
    )

    if exists:
        fs.create_file("/tmp/output.tsv", contents="foo")

    batch_name = "the-batch"

    if exists and not force:
        with pytest.raises(exceptions.IOException):
            batches.export(config=app_config, name=batch_name, path="/tmp/output.tsv")
    else:
        batches.export(config=app_config, name=batch_name, path="/tmp/output.tsv", force=force)

    with open("/tmp/output.tsv", "rt") as inputf:
        fcontents = inputf.read()

    if not exists or force:
        expected = "\n".join(
            [
                "ASSEMBLY\tCHROM\tPOS\tREF\tALT\tOMIM\tMOI\tCLIN_SIG\tCLIN_EVAL\tCLIN_COMMENT\tKEY\tHPO",
                (
                    "GRCh37\t19\t48183936\tC\tCA\t619325\tAutosomal dominant inheritance\t"
                    "Likely pathogenic\t\t\t\tHP:0004322,HP:0001263\n"
                ),
            ]
        )
    else:
        expected = "foo"
    assert fcontents == expected


@pytest.mark.parametrize(
    "exists,force",
    [
        (False, False),
        (True, False),
        (True, True),
    ],
)
def test_export_structural_variant_tsv(fs, app_config, exists, force):
    fs.create_file(
        os.path.expanduser(
            "~/.local/share/clinvar-this/default/the-batch/payload.20120113000000.json"
        ),
        contents=STRUC_VARIANT_PAYLOAD_JSON,
    )

    if exists:
        fs.create_file("/tmp/output.tsv", contents="foo")

    batch_name = "the-batch"

    if exists and not force:
        with pytest.raises(exceptions.IOException):
            batches.export(
                config=app_config, name=batch_name, path="/tmp/output.tsv", struc_var=True
            )
    else:
        batches.export(
            config=app_config, name=batch_name, path="/tmp/output.tsv", force=force, struc_var=True
        )

    with open("/tmp/output.tsv", "rt") as inputf:
        fcontents = inputf.read()

    if not exists or force:
        expected = "\n".join(
            [
                (
                    "ASSEMBLY\tCHROM\tSTART\tSTOP\tSV_TYPE\tOMIM\tMOI\tCLIN_SIG\tCLIN_EVAL\t"
                    "CLIN_COMMENT\tKEY\tHPO"
                ),
                (
                    "GRCh38\t1\t844347\t4398122\tDeletion\t\tAutosomal dominant inheritance\t"
                    "not provided\t\t\t\t\n"
                ),
            ]
        )
    else:
        expected = "foo"
    assert fcontents == expected


@pytest.mark.parametrize(
    "use_testing,dry_run",
    [(False, False), (False, True)],
)
@freeze_time("2012-01-14")
def test_submit(fs, app_config, use_testing, dry_run, monkeypatch):
    fs.create_file(
        os.path.expanduser(
            "~/.local/share/clinvar-this/default/the-batch/payload.20120113000000.json"
        ),
        contents=SEQ_VARIANT_PAYLOAD_JSON,
    )

    fs.create_file(SUBMISSION_SCHEMA_JSON_PATH, contents=SUBMISSION_SCHEMA_JSON)

    def mock_submit_data(_self, _payload):
        return {"id": "SUB000fake"}

    monkeypatch.setattr(batches.client.Client, "submit_data", mock_submit_data)

    batches.submit(config=app_config, name="the-batch", use_testing=use_testing, dry_run=dry_run)

    response_path = os.path.expanduser(
        "~/.local/share/clinvar-this/default/the-batch/submission-response.20120114000000.json"
    )
    if not dry_run:
        assert os.path.exists(response_path)
        with open(response_path, "rt") as inputf:
            assert inputf.read() == '{"id": "SUB000fake"}'
    else:
        assert not os.path.exists(response_path)


def test_retrieve_state_submitted(fs, app_config, monkeypatch):
    fs.create_file(
        os.path.expanduser(
            "~/.local/share/clinvar-this/default/the-batch/payload.20120113000000.json"
        ),
        contents=SEQ_VARIANT_PAYLOAD_JSON,
    )
    fs.create_file(
        os.path.expanduser(
            "~/.local/share/clinvar-this/default/the-batch/submission-response.20120114000000.json"
        ),
        contents='{"id": "SUB000fake"}',
    )

    response = json.loads(SEQ_VARIANT_RETRIEVE_RESPONSE_SUBMITTED_JSON)

    mock_retrieve_status = MagicMock()
    mock_retrieve_status.return_value = RetrieveStatusResult(
        status=CONVERTER.structure(response["status"], models.SubmissionStatus), summaries={}
    )

    monkeypatch.setattr(batches.client.Client, "retrieve_status", mock_retrieve_status)

    batches.retrieve(config=app_config, name="the-batch", use_testing=False)

    mock_retrieve_status.assert_called_once()
    assert len(mock_retrieve_status.call_args.args) == 1
    assert len(mock_retrieve_status.call_args.kwargs) == 0
    assert mock_retrieve_status.call_args.args[0] == "SUB000fake"


def test_retrieve_state_processing(fs, app_config, monkeypatch):
    fs.create_file(
        os.path.expanduser(
            "~/.local/share/clinvar-this/default/the-batch/payload.20120113000000.json"
        ),
        contents=SEQ_VARIANT_PAYLOAD_JSON,
    )
    fs.create_file(
        os.path.expanduser(
            "~/.local/share/clinvar-this/default/the-batch/submission-response.20120114000000.json"
        ),
        contents='{"id": "SUB000fake"}',
    )

    response = json.loads(SEQ_VARIANT_RETRIEVE_RESPONSE_PROCESSING_JSON)

    mock_retrieve_status = MagicMock()
    mock_retrieve_status.return_value = RetrieveStatusResult(
        status=CONVERTER.structure(response["status"], models.SubmissionStatus), summaries={}
    )

    monkeypatch.setattr(batches.client.Client, "retrieve_status", mock_retrieve_status)

    batches.retrieve(config=app_config, name="the-batch", use_testing=False)

    mock_retrieve_status.assert_called_once()
    assert len(mock_retrieve_status.call_args.args) == 1
    assert len(mock_retrieve_status.call_args.kwargs) == 0
    assert mock_retrieve_status.call_args.args[0] == "SUB000fake"


def test_retrieve_state_processed(fs, app_config, monkeypatch):
    fs.create_file(
        os.path.expanduser(
            "~/.local/share/clinvar-this/default/the-batch/payload.20120113000000.json"
        ),
        contents=SEQ_VARIANT_PAYLOAD_JSON,
    )
    fs.create_file(
        os.path.expanduser(
            "~/.local/share/clinvar-this/default/the-batch/submission-response.20120114000000.json"
        ),
        contents='{"id": "SUB000fake"}',
    )

    response = json.loads(SEQ_VARIANT_RETRIEVE_RESPONSE_SUCCESS_JSON)

    mock_retrieve_status = MagicMock()
    mock_retrieve_status.return_value = RetrieveStatusResult(
        status=CONVERTER.structure(response["status"], models.SubmissionStatus),
        summaries={
            key: CONVERTER.structure(value, models.SummaryResponse)
            for key, value in response["summaries"].items()
        },
    )

    monkeypatch.setattr(batches.client.Client, "retrieve_status", mock_retrieve_status)

    batches.retrieve(config=app_config, name="the-batch", use_testing=False)

    mock_retrieve_status.assert_called_once()
    assert len(mock_retrieve_status.call_args.args) == 1
    assert len(mock_retrieve_status.call_args.kwargs) == 0
    assert mock_retrieve_status.call_args.args[0] == "SUB000fake"


def test_retrieve_state_error(fs, app_config, monkeypatch):
    fs.create_file(
        os.path.expanduser(
            "~/.local/share/clinvar-this/default/the-batch/payload.20120113000000.json"
        ),
        contents=SEQ_VARIANT_PAYLOAD_JSON,
    )
    fs.create_file(
        os.path.expanduser(
            "~/.local/share/clinvar-this/default/the-batch/submission-response.20120114000000.json"
        ),
        contents='{"id": "SUB000fake"}',
    )

    response = json.loads(SEQ_VARIANT_RETRIEVE_RESPONSE_ERROR_JSON)

    mock_retrieve_status = MagicMock()
    mock_retrieve_status.return_value = RetrieveStatusResult(
        status=CONVERTER.structure(response["status"], models.SubmissionStatus), summaries={}
    )

    monkeypatch.setattr(batches.client.Client, "retrieve_status", mock_retrieve_status)

    batches.retrieve(config=app_config, name="the-batch", use_testing=False)

    mock_retrieve_status.assert_called_once()
    assert len(mock_retrieve_status.call_args.args) == 1
    assert len(mock_retrieve_status.call_args.kwargs) == 0
    assert mock_retrieve_status.call_args.args[0] == "SUB000fake"
