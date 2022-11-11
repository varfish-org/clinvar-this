import pathlib

import pytest

from clinvar_this import exceptions
from clinvar_this.tsv import TsvRecord, read_tsv

DATA_DIR = pathlib.Path(__file__).parent / "data"


def test_read_tsv_path():
    actual = read_tsv(path=DATA_DIR / "example.tsv")
    assert actual == [
        TsvRecord(
            assembly="GRCh37",
            chromosome="10",
            pos="115614632",
            ref="A",
            alt="G",
            omim="OMIM:618278",
            inheritance="Autosomal recessive inheritance",
            extra_data={"gene": "NHLRC2"},
        )
    ]


def test_read_tsv_file():
    with (DATA_DIR / "example.tsv").open("rt") as inputf:
        actual = read_tsv(file=inputf)
    assert actual == [
        TsvRecord(
            assembly="GRCh37",
            chromosome="10",
            pos="115614632",
            ref="A",
            alt="G",
            omim="OMIM:618278",
            inheritance="Autosomal recessive inheritance",
            extra_data={"gene": "NHLRC2"},
        )
    ]


def test_read_tsv_path_bad():
    with pytest.raises(exceptions.IOException):
        read_tsv(path=DATA_DIR / "example.bad.tsv")


def test_read_tsv_error():
    with pytest.raises(TypeError):
        read_tsv()
