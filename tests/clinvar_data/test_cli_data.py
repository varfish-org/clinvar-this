"""Smoke test for the CLI to ClinVar XML parsing."""

import gzip
import os.path

from click.testing import CliRunner
import pytest

from clinvar_this import cli


@pytest.mark.parametrize(
    "fname_in,fname_out",
    [("one_record.xml", "one_record.jsonl"), ("one_record.xml.gz", "one_record.jsonl.gz")],
)
def test_cli_xml_to_json(fname_in, fname_out, tmp_path):
    runner = CliRunner()
    in_path = os.path.dirname(__file__) + f"/data/{fname_in}"
    out_path = f"{tmp_path}/{fname_out}"
    result = runner.invoke(cli.cli, ["data", "xml-to-jsonl", in_path, out_path])
    assert result.exit_code == 0

    expected_path = os.path.dirname(__file__) + "/data/one_record.jsonl"
    with open(expected_path, "rt") as expected_f:
        if fname_out.endswith(".gz"):
            output_f = gzip.open(out_path, "rt")
        else:
            output_f = open(out_path, "rt")
        with output_f:
            assert expected_f.read() == output_f.read()


def test_cli_xml_to_json_stdin_stdout():
    in_path = os.path.dirname(__file__) + "/data/one_record.xml"
    with open(in_path, "rt") as inputf:
        stdin_txt = inputf.read()

    runner = CliRunner()
    result = runner.invoke(cli.cli, ["data", "xml-to-jsonl", "-", "-"], input=stdin_txt)

    expected_path = os.path.dirname(__file__) + "/data/one_record.jsonl"
    with open(expected_path, "rt") as expected_f:
        assert expected_f.read() == result.output
