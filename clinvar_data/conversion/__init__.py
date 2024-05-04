"""Code to convert ClinVar XML to JSONL"""

import datetime
import gzip
import json
import sys
import traceback
import typing

import click
import tqdm
import xmltodict

from clinvar_data import models


def remove_empties_from_containers(
    container: typing.Union[dict, list]
) -> typing.Union[dict, list, None]:
    if isinstance(container, list):
        new_list = []
        for v in container:
            if isinstance(v, (dict, list)):
                v = remove_empties_from_containers(v)
            if v is not None:
                new_list.append(v)
        return new_list or None
    elif isinstance(container, dict):
        new_dict = {}
        for k, v in container.items():
            if isinstance(v, (dict, list)):
                v = remove_empties_from_containers(v)
            if v is not None:
                new_dict[k] = v
        return new_dict or None
    else:  # pragma: no cover
        assert False, "must not happen"


# Define a custom function to serialize datetime objects
def json_default(obj):
    if isinstance(obj, datetime.datetime):
        return obj.strftime("%Y-%m-%d %H:%M:%S")
    elif isinstance(obj, datetime.date):
        return obj.strftime("%Y-%m-%d")
    else:
        raise TypeError("Type not serializable")


def convert_clinvarset(json_cv: dict) -> models.ClinVarSet:
    """Convert a ClinVarSet from JSON dict."""
    return models.ClinVarSet.from_json_data(json_cv)


def convert(
    input_file: str, output_file: str, max_records: int = 0, use_click: bool = False
) -> int:
    """Run conversion from ClinVar XML to JSONL"""
    if input_file.endswith((".gz", ".bgz")):
        inputf: typing.Union[typing.BinaryIO, gzip.GzipFile] = gzip.open(input_file, "rb")
    elif use_click:
        inputf = click.open_file(input_file, "rb")
    else:
        inputf = open(input_file, "rb")

    if output_file.endswith(".gz"):
        outputf = gzip.open(output_file, "wt")
    elif use_click:
        outputf = click.open_file(output_file, "wt")
    else:
        outputf = open(output_file, "wt")

    pb = tqdm.tqdm(desc="parsing", unit=" ClinVarSet records", smoothing=1.0)
    records_written = 0
    errors = 0

    def handle_clinvarset(_, json_cvs: dict):
        """Handle single ClinVarSet entry after parsing by ``xmltodict``."""
        try:
            data = convert_clinvarset(json_cvs)
        except Exception:  # pragma: no cover
            nonlocal errors
            errors += 1
            print("Problem with data: exception and data follow", file=sys.stderr)
            traceback.print_exc()
            print(json_cvs, file=sys.stderr)
            return True

        print(
            json.dumps(
                remove_empties_from_containers(data.model_dump(mode="json")), default=json_default
            ),
            file=outputf,
        )

        nonlocal records_written
        records_written += 1
        pb.update(1)

        return max_records == 0 or records_written < max_records

    try:
        xmltodict.parse(inputf, item_depth=2, item_callback=handle_clinvarset)
    except xmltodict.ParsingInterrupted:  # pragma: no cover
        print(f"stopping after parsing {records_written} records", file=sys.stderr)

    if errors == 0:
        return 0
    else:
        print(f"a total of {errors} errors occurred", file=sys.stderr)
        return 1
