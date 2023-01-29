import os
import pathlib

from freezegun import freeze_time

from clinvar_this import batches
from clinvar_this.io import tsv as io_tsv

# We must read this outside of the test as we use the fake file system.
with (pathlib.Path(__file__).parent / "data/batches/small_variant.tsv").open("rt") as inputf:
    #: Small variant TSV for testing batches module.  Likely pathogenic.
    SMALL_VARIANT_TSV = inputf.read()

with (pathlib.Path(__file__).parent / "data/batches/small_variant.payload.json").open(
    "rt"
) as inputf:
    #: The ``SMALL_VARIANT_TSV`` after import for testing batches module.
    SMALL_VARIANT_PAYLOAD_JSON = inputf.read()

with (pathlib.Path(__file__).parent / "data/batches/small_variant-update.tsv").open("rt") as inputf:
    #: Small variant TSV for testing batches module.  Updated to Pathonenic.
    SMALL_VARIANT_UPDATE_TSV = inputf.read()

with (pathlib.Path(__file__).parent / "data/batches/small_variant-update.payload.json").open(
    "rt"
) as inputf:
    #: The `SMALL_VARIANT_UPDATE_TSV` after import / merge.
    SMALL_VARIANT_UPDATE_PAYLOAD_JSON = inputf.read()


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
def test_import_small_variant_tsv_new(fs, app_config, monkeypatch):
    path_tsv = "/tmp/small_variant.tsv"
    fs.create_file(path_tsv, contents=SMALL_VARIANT_TSV)

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
    assert payload_json == SMALL_VARIANT_PAYLOAD_JSON


@freeze_time("2012-01-14")
def test_import_small_variant_tsv_update(fs, app_config):
    path_tsv = "/tmp/small_variant-update.tsv"
    fs.create_file(path_tsv, contents=SMALL_VARIANT_UPDATE_TSV)

    fs.create_file(
        os.path.expanduser(
            "~/.local/share/clinvar-this/default/the-batch/payload.20120113000000.json"
        ),
        contents=SMALL_VARIANT_PAYLOAD_JSON,
    )

    batch_name = "the-batch"
    batches.import_(config=app_config, name=batch_name, path=path_tsv, metadata=())

    print(os.listdir(os.path.expanduser("~/.local/share/clinvar-this/default/the-batch")))

    payload_path = os.path.expanduser(
        "~/.local/share/clinvar-this/default/the-batch/payload.20120114000000.json"
    )
    assert os.path.exists(payload_path)
    with open(payload_path, "rt") as inputf:
        payload_json = inputf.read()
    assert payload_json == SMALL_VARIANT_UPDATE_PAYLOAD_JSON


def test_import_deletion_tsv_new(fs):
    pass


def test_import_deletion_tsv_update(fs):
    pass


def test_import_structural_variant_tsv_new(fs):
    pass


def test_import_structural_variant_tsv_update(fs):
    pass


def test_export_small_variant_tsv(fs):
    pass


def test_export_structural_variant_tsv(fs):
    pass


def test_submit(fs):
    pass


def test_retrieve_state_submitted(fs):
    pass


def test_retrieve_state_processing(fs):
    pass


def test_retrieve_state_processed(fs):
    pass


def test_retrieve_state_error(fs):
    pass
