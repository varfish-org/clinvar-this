"""Code to convert ClinVar XML to JSONL"""

import gzip
import json

import click
import xmltodict


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

    def handle_clinvarset(_, clinvarset: dict):
        """Handle single ClinVarSet entry after parsing by ``xmltodict``."""
        print(json.dumps(clinvarset), file=outputf)
        return True

    xmltodict.parse(inputf, item_depth=2, item_callback=handle_clinvarset)
