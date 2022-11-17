"""Helpers for schema validation."""

import json
import pathlib
import typing

from jsonschema import validate


def validate_submission_payload(payload: typing.Any):
    schema_path = pathlib.Path(__file__).parent / "submission_schema.json"
    with schema_path.open("rt") as inputf:
        schema = json.load(inputf)

    validate(instance=payload, schema=schema)


def validate_status_summary(payload: typing.Any):
    schema_path = pathlib.Path(__file__).parent / "summary_response_schema.json"
    with schema_path.open("rt") as inputf:
        schema = json.load(inputf)

    validate(instance=payload, schema=schema)
