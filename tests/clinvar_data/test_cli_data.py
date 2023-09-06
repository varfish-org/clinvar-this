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
def test_cli_xml_to_json(fname_in, fname_out, tmp_path, snapshot):
    runner = CliRunner()
    in_path = os.path.dirname(__file__) + f"/data/{fname_in}"
    out_path = f"{tmp_path}/{fname_out}"
    result = runner.invoke(cli.cli, ["data", "xml-to-jsonl", in_path, out_path])
    assert result.exit_code == 0

    if fname_out.endswith(".gz"):
        output_f = gzip.open(out_path, "rt")
    else:
        output_f = open(out_path, "rt")
    with output_f:
        snapshot.assert_match(output_f.read(), "one_record.jsonl")


def test_cli_xml_to_json_stdin_stdout(snapshot):
    in_path = os.path.dirname(__file__) + "/data/one_record.xml"
    with open(in_path, "rt") as inputf:
        stdin_txt = inputf.read()

    runner = CliRunner(mix_stderr=False)
    result = runner.invoke(cli.cli, ["data", "xml-to-jsonl", "-", "-"], input=stdin_txt)
    assert result.exit_code == 0

    snapshot.assert_match(result.output, "one_record.jsonl")


@pytest.mark.parametrize(
    "fname_in",
    [
        "ex_additional_submitters.xml",
        "ex_attribute_set.xml",
        "ex_custom_score.xml",
        "ex_indication.xml",
        "ex_missense.xml",
        "ex_replaces.xml",
        "ex_review_status_ns.xml",
        "ex_study_description.xml",
        "ex_with_ethnicity.xml",
        "ex_with_hpo.xml",
    ],
)
def test_convert_snapshot_to_jsonl(fname_in, tmp_path, snapshot):
    runner = CliRunner()
    in_path = os.path.dirname(__file__) + f"/data/{fname_in}"
    out_path = f"{tmp_path}/out.jsonl"
    result = runner.invoke(cli.cli, ["data", "xml-to-jsonl", in_path, out_path])
    assert result.exit_code == 0

    with open(out_path, "rt") as output_f:
        snapshot.assert_match(output_f.read(), "out.jsonl")
