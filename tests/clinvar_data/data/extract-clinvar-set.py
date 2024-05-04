#!/usr/bin/env python3
"""Helper to extract ``<ClinVarSet>`` from ClinVar VCV XML file."""

import gzip
import typing

import click
import xmltodict


class DataHandler:
    verbose: bool
    query: str
    result: typing.Dict = {}

    def __init__(self, verbose: bool, query: str):
        self.verbose = verbose
        self.query = query

    def handle_variation_archive(self, path: typing.List[typing.Any], elem: typing.Dict):
        if "VariationArchive" in elem:
            value = elem["VariationArchive"]
            if value["@VariationID"] == self.query or value["@Accession"] == self.query:
                self.result = {path[0][0]: {**path[0][1], "VariationArchive": elem}}
                import json

                print(json.dumps(self.result, indent=2))
                return False
        else:
            return True


@click.command()
@click.option("--verbose/--no-verbose", default=False)
@click.option(
    "--path",
    "path_in",
    help="Path to ClinVar XML file to use",
    required=True,
    type=click.Path(exists=True),
)
@click.option(
    "--path-out",
    "file_out",
    help="Path to output file, - for stdout",
    type=click.File(mode="wb"),
    default="-",
)
@click.option("--query", help="VariationID or Accession to query", required=True, type=str)
def cli(verbose: bool, path_in: str, file_out: typing.BinaryIO, query: str):
    """Main entry point for CLI via click."""
    handler = DataHandler(verbose, query)

    if path_in.endswith(".gz"):
        file_in = gzip.open(path_in, "rb")
    else:
        file_in = open(path_in, "rb")  # type: ignore

    output: typing.Dict = {}
    with file_in:
        try:
            import json

            print(
                json.dumps(
                    xmltodict.parse(
                        file_in,
                        item_depth=1,
                        item_callback=handler.handle_variation_archive,
                        process_namespaces=True,
                    ),
                    indent=2,
                )
            )
            xmltodict.parse(
                file_in,
                item_depth=1,
                item_callback=handler.handle_variation_archive,
                process_namespaces=True,
            )
        except xmltodict.ParsingInterrupted:
            pass
        except Exception as e:
            raise e
    print(xmltodict.unparse(output, pretty=True, indent="  "))


if __name__ == "__main__":
    cli()
