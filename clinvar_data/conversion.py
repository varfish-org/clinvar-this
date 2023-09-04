"""Code to convert ClinVar XML to JSONL"""

import datetime
import gzip
import io
import json
import multiprocessing
import typing

import cattrs
import click
import tqdm
import xmltodict

from clinvar_data import models


def chunker(inputf: typing.BinaryIO, records: int = 1_000) -> typing.Iterator[io.BytesIO]:
    head = []
    head_done = False
    chunk = io.BytesIO()
    chunk_size = 0
    for line in inputf:
        if b"<ClinVarSet" in line and not head_done:
            head_done = True
            for head_line in head:
                chunk.write(head_line)
        elif b"</ReleaseSet" in line:
            break  # all done

        if not head_done:
            head.append(line)
        else:
            chunk.write(line)

        if b"<ClinVarSet" in line:
            chunk_size += 1

        if b"</ClinVarSet" in line:
            if chunk_size >= records:
                # yield and start new chunk
                chunk.write(b"</ReleaseSet>")
                chunk.seek(0)
                yield chunk

                chunk = io.BytesIO()
                for line in head:
                    chunk.write(line)
                chunk_size = 0

    # yield final chunk if any
    if chunk_size > 0:
        chunk.write(b"</ReleaseSet>")
        chunk.seek(0)
        yield chunk


# Define a custom function to serialize datetime objects
def json_default(obj):
    if isinstance(obj, datetime.datetime):
        return obj.strftime("%Y-%m-%d %H:%M:%S")
    elif isinstance(obj, datetime.date):
        return obj.strftime("%Y-%m-%d")
    else:
        raise TypeError("Type not serializable")


def convert_clinvarset(json_cv: dict) -> models.PublicSetType:
    """Convert a ClinVarSet from JSON dict."""
    return models.PublicSetType.from_json(json_cv)


def run_thread(work: typing.Tuple[io.BytesIO, int, str]):
    xml_chunk, no, tmpdir = work

    with open(f"{tmpdir}/chunk-{no}.xml", "wb") as tmpf:
        tmpf.write(xml_chunk.read())
    xml_chunk.seek(0)

    path_out = f"{tmpdir}/out-{no}.jsonl"
    with open(path_out, "wt") as tmpf:

        def handle_local(_, json_cvs: dict):
            print(
                json.dumps(cattrs.unstructure(convert_clinvarset(json_cvs)), default=json_default),
                file=tmpf,
            )
            return True

        xmltodict.parse(xml_chunk, item_depth=2, item_callback=handle_local)

    return path_out


def convert(
    input_file: str, output_file: str, threads: int, chunk_size: int, use_click: bool = False
):
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

    def run_sequential():
        def handle_clinvarset(_, json_cvs: dict):
            """Handle single ClinVarSet entry after parsing by ``xmltodict``."""
            print(
                json.dumps(cattrs.unstructure(convert_clinvarset(json_cvs)), default=json_default),
                file=outputf,
            )
            return True

        xmltodict.parse(inputf, item_depth=2, item_callback=handle_clinvarset)

    if threads == 0:
        run_sequential()
    else:
        tmpdir = "/tmp/dummy"
        # with tempfile.TemporaryDirectory() as tmpdir, multiprocessing.Pool(threads) as pool:
        with multiprocessing.Pool(threads) as pool:
            click.echo("starting %d threads" % threads)
            chunks = ((c, i, str(tmpdir)) for (i, c) in enumerate(chunker(inputf)))
            tmpfiles = tqdm.tqdm(pool.imap(run_thread, chunks), unit="chunks")
            for fname in tmpfiles:
                with open(fname, "rt") as tmpf:
                    for line in tmpf:
                        outputf.write(line)
