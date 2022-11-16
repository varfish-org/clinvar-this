"""Support for I/O of the minimal TSV format to define submissions."""

import csv
import pathlib
import typing

import attrs

from clinvar_api.msg import Assembly, Chromosome, ModeOfInheritance
from clinvar_this import exceptions

#: The expected first header columns.
HEADER = (
    "ASSEMBLY",
    "CHROM",
    "POS",
    "REF",
    "ALT",
    "OMIM",
    "MOI",
)


@attrs.define(frozen=True)
class TsvRecord:
    """Record for reading."""

    #: Assembly
    assembly: Assembly
    #: Chromosome
    chromosome: Chromosome
    #: Position
    pos: int
    #: Reference allele bases
    ref: str
    #: Alternative allele bases
    alt: str
    #: OMIM ID
    omim: typing.List[str]
    #: Mode of inheritance
    inheritance: ModeOfInheritance
    #: Additional columns
    extra_data: typing.Dict[str, str] = attrs.field(factory=dict)


def _read_tsv_file(inputf: typing.TextIO) -> typing.List[TsvRecord]:
    """Read TSV from the given file."""
    reader = csv.reader(inputf, delimiter="\t")
    header = None

    result: typing.List[TsvRecord] = []
    for row in reader:
        if header:
            core = row[: len(HEADER)]
            extra = row[len(HEADER) :]
            extra_header = header[len(HEADER) :]
            result.append(TsvRecord(*core, dict(zip(extra_header, extra))))
        else:
            header = row
            prefix = tuple(header[: len(HEADER)])
            if prefix != HEADER:
                raise exceptions.IOException(
                    f"Expected header to start with {HEADER} but was {prefix}"
                )
    return result


def read_tsv(
    *,
    file: typing.Optional[typing.TextIO] = None,
    path: typing.Union[None, str, pathlib.Path] = None,
) -> typing.List[TsvRecord]:
    """Read TSV from either file or path"""
    if file:
        return _read_tsv_file(file)
    elif path:
        with pathlib.Path(path).open("rt") as inputf:
            return _read_tsv_file(inputf)
    else:
        raise TypeError("You have to provide either file or path")
