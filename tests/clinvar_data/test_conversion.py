"""Tests for the conversion module."""

import os

from clinvar_data import conversion


def test_cli_xml_to_json(tmp_path):
    in_path = os.path.dirname(__file__) + "/data/one_record.xml"
    out_path = f"{tmp_path}/one_record.jsonl"
    conversion.convert(
        in_path,
        out_path,
        use_click=False,
    )

    expected_path = os.path.dirname(__file__) + "/data/one_record.jsonl"
    with open(expected_path, "rt") as expected_f, open(out_path, "rt") as output_f:
        assert expected_f.read() == output_f.read()
