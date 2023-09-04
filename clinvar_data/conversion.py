"""Code to convert ClinVar XML to JSONL"""

import datetime
import gzip
import json

import cattrs
import click
import xmltodict

from clinvar_data import models


# Define a custom function to serialize datetime objects
def json_default(obj):
    if isinstance(obj, datetime.datetime):
        return obj.strftime("%Y-%m-%d %H:%M:%S")
    elif isinstance(obj, datetime.date):
        return obj.strftime("%Y-%m-%d")
    else:
        raise TypeError("Type not serializable")


def convert_clinvarset(json_cvs: dict) -> models.PublicSetType:
    """Convert a ClinVarSet from JSON dict."""
    return [
        models.PublicSetType.from_json(clinvar_set)
        for clinvar_set in models.force_list(json_cvs["ClinVarSet"])
    ]


def convert(input_file: str, output_file: str, use_click: bool = False):
    """Run conversion from ClinVar XML to JSONL"""
    if input_file.endswith((".gz", ".bgz")):
        inputf = gzip.open(input_file, "rb")
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

    def handle_clinvarset(_, json_cvs: dict):
        """Handle single ClinVarSet entry after parsing by ``xmltodict``."""
        print(
            json.dumps(cattrs.unstructure(convert_clinvarset(json_cvs)), default=json_default),
            file=outputf,
        )
        return True

    xmltodict.parse(inputf, item_depth=1, item_callback=handle_clinvarset)
