"""Code to convert ClinVar XML to JSONL"""

import gzip
import json
import sys
import traceback
import typing

import click
from google.protobuf.json_format import MessageToDict
import tqdm
import xmltodict

from clinvar_data.conversion import dict_to_pb
from clinvar_data.pbs import clinvar_public

#: Total number of VariantArchive records in ClinVar on 2024-05-24: 2966486.
TOTAL_RECORDS: int = 3_000_000


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


def convert_variation_archive(json_va: dict) -> clinvar_public.VariationArchive:
    """Convert a ClinVarSet from JSON dict."""
    return dict_to_pb.ConvertVariationArchive.xmldict_data_to_pb(json_va)


def convert(
    input_file: str,
    output_file: str,
    max_records: int = 0,
    use_click: bool = False,
    show_progress: bool = True,
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

    pb: tqdm.tqdm | None = None
    if show_progress:
        pb = tqdm.tqdm(
            desc="parsing", unit=" VariationArchive records", smoothing=1.0, total=TOTAL_RECORDS
        )
    records_written = 0
    errors = 0

    def handle_variationarchive(ctx: list[dict], json_cvs: dict):
        """Handle single VariationArchive entry after parsing by ``xmltodict``."""
        try:
            key, val = ctx[-1]
            assert key == "VariationArchive"
            json_va = {key: {f"@{k}": v for k, v in val.items()}}
            json_va[key].update(json_cvs)
            data = convert_variation_archive(json_va)
        except Exception:  # pragma: no cover
            nonlocal errors
            errors += 1
            print("Problem with data: exception and data follow", file=sys.stderr)
            traceback.print_exc()
            print(json_cvs, file=sys.stderr)
            return True

        print(
            json.dumps(MessageToDict(data)),
            file=outputf,
        )

        nonlocal records_written
        records_written += 1
        if pb:
            pb.update(1)

        return max_records == 0 or records_written < max_records

    try:
        xmltodict.parse(inputf, item_depth=2, item_callback=handle_variationarchive)
    except xmltodict.ParsingInterrupted:  # pragma: no cover
        print(f"stopping after parsing {records_written} records", file=sys.stderr)

    if errors == 0:
        return 0
    else:
        print(f"a total of {errors} errors occurred", file=sys.stderr)
        return 1
