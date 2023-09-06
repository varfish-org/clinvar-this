"""Tests for the conversion module."""

import os

import pytest

from clinvar_data import conversion


@pytest.mark.parametrize(
    "value,expected",
    [
        ({}, None),
        ({"a": 1, "b": 2}, {"a": 1, "b": 2}),
        ({"a": None}, None),
        ({"a": {"b": None}}, None),
    ],
)
def test_remove_empties_from_dict(value, expected):
    assert conversion.remove_empties_from_containers(value) == expected


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
