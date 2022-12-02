from unittest.mock import MagicMock, patch

from click.testing import CliRunner

import clinvar_this  # noqa
from clinvar_this import cli, config, exceptions


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
