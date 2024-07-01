"""Regression tests for issues occuring in weekly builds of clinvar-data-jsonl"""

import json

from google.protobuf.json_format import MessageToDict
import pytest

from clinvar_data.conversion.dict_to_pb import ConvertClassifiedRecord


@pytest.mark.parametrize(
    "path_json_input",
    [
        "tests/clinvar_data/data/regressions/2024-07-01/allele-id-1706807.json",
        "tests/clinvar_data/data/regressions/2024-07-01/allelle-id-1704898.json",
    ],
)
def test_convert_classified_record_xmldict_data_to_pb(path_json_input: str, snapshot):
    with open(path_json_input, "rt") as input:
        xmldict_value = json.load(input)
    result = ConvertClassifiedRecord.xmldict_data_to_pb(xmldict_value)
    result_json = MessageToDict(result)
    snapshot.assert_match(json.dumps(result_json, indent=2), "result")
