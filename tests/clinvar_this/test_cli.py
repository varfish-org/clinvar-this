from unittest.mock import MagicMock, patch

from click.testing import CliRunner
import pytest

from clinvar_this import batches, cli, config, exceptions


def test_call_main_help():
    runner = CliRunner()
    result = runner.invoke(cli.cli, ["--help"])
    assert result.exit_code == 0


def test_call_main_verbose():
    runner = CliRunner()
    result = runner.invoke(cli.cli, ["--verbose"])
    assert result.exit_code != 0


def test_call_config():
    runner = CliRunner()
    result = runner.invoke(cli.cli, ["config"])
    assert result.exit_code == 0


def test_call_config_get():
    with patch(
        "clinvar_this.cli.load_config",
        MagicMock(return_value=config.Config(profile="default", auth_token="fake")),
    ):
        runner = CliRunner()
        result = runner.invoke(cli.cli, ["config", "get", "auth_token"])
    assert b"fake" in result.stdout_bytes
    assert result.exit_code == 0


def test_call_config_dump(fs_config):
    runner = CliRunner()
    result = runner.invoke(cli.cli, ["config", "dump"])
    assert b"fake" in result.stdout_bytes
    assert result.exit_code == 0


def test_call_config_set_success():
    mock_save_config = MagicMock()
    with patch(
        "clinvar_this.cli.load_config",
        MagicMock(return_value=config.Config(profile="default", auth_token="fake")),
    ), patch("clinvar_this.cli.save_config", mock_save_config):
        runner = CliRunner()
        result = runner.invoke(cli.cli, ["config", "set", "auth_token", "xxx"])
    mock_save_config.assert_called_once_with(
        config.Config(profile="default", auth_token="xxx"), "default"
    )
    assert result.exit_code == 0


def test_call_config_set_success_though_missing_config():
    mock_save_config = MagicMock()
    with patch(
        "clinvar_this.cli.load_config", MagicMock(side_effect=exceptions.ConfigFileMissingException)
    ), patch("clinvar_this.cli.save_config", mock_save_config):
        runner = CliRunner()
        result = runner.invoke(cli.cli, ["config", "set", "auth_token", "xxx"])
    mock_save_config.assert_called_once_with(
        config.Config(profile="default", auth_token="xxx"), "default"
    )
    assert result.exit_code == 0


def test_call_config_set_fail_invalid_name():
    mock_save_config = MagicMock()
    with patch("clinvar_this.cli.save_config", mock_save_config):
        runner = CliRunner()
        result = runner.invoke(cli.cli, ["config", "set", "xxx", "xxx"])
    # assert b"Invalid value" in result.stderr_bytes
    assert result.exit_code != 0


@pytest.mark.parametrize(
    "force,struc_var",
    [
        (True, False),
        (False, False),
        (True, True),
        (False, True),
    ],
)
def test_call_batch_export(fs_config, monkeypatch, force, struc_var):
    """Unit test of ``batch export`` with both sequence and structural variant.

    The test stubs out call of ``batches.list`` and checks results.
    """
    mock_export = MagicMock()
    monkeypatch.setattr(batches, "export", mock_export)

    args = ["batch", "export", "batch-name", "out-tsv"]
    if force:
        args.append("--force")
    if struc_var:
        args.append("--struc-var")

    runner = CliRunner()
    result = runner.invoke(cli.cli, args)

    mock_export.assert_called_once()
    assert len(mock_export.call_args.args) == 5
    assert len(mock_export.call_args.kwargs) == 0
    assert (
        str(mock_export.call_args.args[0])
        == "Config(profile='default', auth_token='****', verify_ssl=True)"
    )
    assert mock_export.call_args.args[1] == "batch-name"
    assert mock_export.call_args.args[2] == "out-tsv"
    assert mock_export.call_args.args[3] == force
    assert mock_export.call_args.args[4] == struc_var
    assert result.exit_code == 0


@pytest.mark.parametrize(
    "name,metadata",
    [
        (None, None),
        ("foo", None),
        (None, ("A=a", "B=b")),
    ],
)
def test_call_batch_import(fs_config, monkeypatch, name, metadata):
    """Unit test of ``batch import``.

    The test stubs out call of ``batches.import_`` and checks results.
    """
    mock_import = MagicMock()
    monkeypatch.setattr(batches, "import_", mock_import)

    mock_gen_name = MagicMock()
    mock_gen_name.return_value = "generated"
    monkeypatch.setattr(batches, "gen_name", mock_gen_name)

    args = ["batch", "import", "input-tsv"]
    if name:
        args += ["--name", name]
    for m in metadata or ():
        args += ["--metadata", m]

    runner = CliRunner()
    result = runner.invoke(cli.cli, args)

    mock_import.assert_called_once()
    assert len(mock_import.call_args.args) == 4
    assert len(mock_import.call_args.kwargs) == 0
    assert (
        str(mock_import.call_args.args[0])
        == "Config(profile='default', auth_token='****', verify_ssl=True)"
    )
    assert mock_import.call_args.args[1] == (name if name else "generated")
    assert mock_import.call_args.args[2] == "input-tsv"
    assert mock_import.call_args.args[3] == (metadata if metadata else ())
    assert result.exit_code == 0


@pytest.mark.parametrize(
    "name,metadata",
    [
        ("other", None),
        ("foo", ("A=a", "B=b")),
    ],
)
def test_call_batch_update_metadata(fs_config, monkeypatch, name, metadata):
    """Unit test of ``batch update-metadata``, stubs out call of ``batches.update_metadata`` and checks results."""
    mock_update_metadata = MagicMock()
    monkeypatch.setattr(batches, "update_metadata", mock_update_metadata)

    args = ["batch", "update-metadata", name]
    if metadata:
        args += metadata

    runner = CliRunner()
    result = runner.invoke(cli.cli, args)

    mock_update_metadata.assert_called_once()
    assert len(mock_update_metadata.call_args.args) == 3
    assert len(mock_update_metadata.call_args.kwargs) == 0
    assert (
        str(mock_update_metadata.call_args.args[0])
        == "Config(profile='default', auth_token='****', verify_ssl=True)"
    )
    assert mock_update_metadata.call_args.args[1] == name
    assert mock_update_metadata.call_args.args[2] == (metadata if metadata else ())
    assert result.exit_code == 0


@pytest.mark.parametrize(
    "dry_run,use_testing",
    [
        (False, False),
        (False, True),
        (True, False),
    ],
)
def test_call_batch_submit(fs_config, monkeypatch, dry_run, use_testing):
    """Unit test of ``batch submit``, stubs out call of ``batches.submit`` and checks results."""
    mock_submit = MagicMock()
    monkeypatch.setattr(batches, "submit", mock_submit)

    args = ["batch", "submit", "name"]
    if dry_run:
        args.append("--dry-run")
    if use_testing:
        args.append("--use-testing")

    runner = CliRunner()
    result = runner.invoke(cli.cli, args)

    mock_submit.assert_called_once()
    assert len(mock_submit.call_args.args) == 2
    assert len(mock_submit.call_args.kwargs) == 2
    assert (
        str(mock_submit.call_args.args[0])
        == "Config(profile='default', auth_token='****', verify_ssl=True)"
    )
    assert mock_submit.call_args.args[1] == "name"
    assert mock_submit.call_args.kwargs == {"dry_run": dry_run, "use_testing": use_testing}
    assert result.exit_code == 0


@pytest.mark.parametrize(
    "use_testing",
    [True, False],
)
def test_call_batch_retrieve(fs_config, monkeypatch, use_testing):
    """Unit test of ``batch retrieve``, stubs out call of ``batches.retrieve`` and checks results."""
    mock_retrieve = MagicMock()
    monkeypatch.setattr(batches, "retrieve", mock_retrieve)

    args = ["batch", "retrieve", "name"]
    if use_testing:
        args.append("--use-testing")

    runner = CliRunner()
    result = runner.invoke(cli.cli, args)

    mock_retrieve.assert_called_once()
    assert len(mock_retrieve.call_args.args) == 2
    assert len(mock_retrieve.call_args.kwargs) == 1
    assert (
        str(mock_retrieve.call_args.args[0])
        == "Config(profile='default', auth_token='****', verify_ssl=True)"
    )
    assert mock_retrieve.call_args.args[1] == "name"
    assert mock_retrieve.call_args.kwargs == {"use_testing": use_testing}
    assert result.exit_code == 0
