"""Tests for the conversion CLI module."""

import os

from clinvar_data import conversion


def test_cli_xml_to_json(tmp_path, snapshot):
    in_path = os.path.dirname(__file__) + "/data/one_record.xml"
    out_path = f"{tmp_path}/one_record.jsonl"
    conversion.convert(
        in_path,
        out_path,
        use_click=False,
    )

    with open(out_path, "rt") as output_f:
        snapshot.assert_match(output_f.read(), "one_record.jsonl")
