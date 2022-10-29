import pytest

import clinvar_this  # noqa
from clinvar_this import cli


def test_call_main_help():
    with pytest.raises(SystemExit) as exc:
        cli.main(["--help"])

    assert exc.value.code == 0


def test_call_main_verbose():
    cli.main(["--verbose"])


def test_call_main():
    cli.main([])
