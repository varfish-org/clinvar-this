import pathlib

import pytest

from clinvar_api.msg import (
    Assembly,
    Chromosome,
    ClinicalSignificanceDescription,
    ModeOfInheritance,
    VariantType,
)
from clinvar_this import exceptions
from clinvar_this.io.tsv import (
    SeqVarTsvRecord,
    StrucVarTsvRecord,
    TsvType,
    guess_tsv_type,
    read_seq_var_tsv,
    read_struc_var_tsv,
)

DATA_DIR = pathlib.Path(__file__).parent / "data/io_tsv"


def test_read_seq_var_tsv_path():
    actual = read_seq_var_tsv(path=DATA_DIR / "example.tsv")
    assert actual == [
        SeqVarTsvRecord(
            assembly=Assembly.GRCH37,
            chromosome=Chromosome.CHR10,
            pos=115614632,
            ref="A",
            alt="G",
            omim=["OMIM:618278"],
            inheritance=ModeOfInheritance.AUTOSOMAL_RECESSIVE_INHERITANCE,
            clinical_significance_description=ClinicalSignificanceDescription.NOT_PROVIDED,
            local_key="KEY",
            extra_data={"gene": "NHLRC2"},
        )
    ]


def test_read_struc_var_tsv_path():
    actual = read_struc_var_tsv(path=DATA_DIR / "example_sv.tsv")
    assert actual == [
        StrucVarTsvRecord(
            assembly=Assembly.GRCH38,
            chromosome=Chromosome.CHR1,
            start=844347,
            stop=4398122,
            sv_type=VariantType.DELETION,
            omim=[],
            inheritance=ModeOfInheritance.AUTOSOMAL_DOMINANT_INHERITANCE,
            clinical_significance_description=ClinicalSignificanceDescription.NOT_PROVIDED,
            hpo_terms=["HP:0001263"],
        )
    ]


def test_read_seq_var_tsv_file():
    with (DATA_DIR / "example.tsv").open("rt") as inputf:
        actual = read_seq_var_tsv(file=inputf)
    assert actual == [
        SeqVarTsvRecord(
            assembly=Assembly.GRCH37,
            chromosome=Chromosome.CHR10,
            pos=115614632,
            ref="A",
            alt="G",
            omim=["OMIM:618278"],
            inheritance=ModeOfInheritance.AUTOSOMAL_RECESSIVE_INHERITANCE,
            clinical_significance_description=ClinicalSignificanceDescription.NOT_PROVIDED,
            local_key="KEY",
            extra_data={"gene": "NHLRC2"},
        )
    ]


def test_read_struc_var_tsv_file():
    with (DATA_DIR / "example_sv.tsv").open("rt") as inputf:
        actual = read_struc_var_tsv(file=inputf)
    assert actual == [
        StrucVarTsvRecord(
            assembly=Assembly.GRCH38,
            chromosome=Chromosome.CHR1,
            start=844347,
            stop=4398122,
            sv_type=VariantType.DELETION,
            omim=[],
            inheritance=ModeOfInheritance.AUTOSOMAL_DOMINANT_INHERITANCE,
            clinical_significance_description=ClinicalSignificanceDescription.NOT_PROVIDED,
            hpo_terms=["HP:0001263"],
        )
    ]


def test_read_seq_var_tsv_path_bad():
    with pytest.raises(exceptions.InvalidFormat):
        read_seq_var_tsv(path=DATA_DIR / "example.bad.tsv")


def test_read_struc_var_tsv_path_bad():
    with pytest.raises(exceptions.InvalidFormat):
        read_struc_var_tsv(path=DATA_DIR / "example_sv.bad.tsv")


def test_read_seq_var_tsv_error():
    with pytest.raises(TypeError):
        read_seq_var_tsv()


def test_read_struc_var_tsv_error():
    with pytest.raises(TypeError):
        read_struc_var_tsv()


def test_guess_file_type():
    assert guess_tsv_type(path=DATA_DIR / "example.bad.tsv") == None  # noqa: E711
    assert guess_tsv_type(path=DATA_DIR / "example.tsv") == TsvType.SEQ_VAR
    assert guess_tsv_type(path=DATA_DIR / "example_sv.tsv") == TsvType.STRUC_VAR
