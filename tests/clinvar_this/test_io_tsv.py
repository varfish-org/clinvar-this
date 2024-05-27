from io import StringIO
import pathlib

import pytest

from clinvar_api.models import SubmissionCondition, SubmissionConditionSet
from clinvar_api.msg import (
    Assembly,
    Chromosome,
    ClinicalSignificanceDescription,
    ConditionDb,
    ModeOfInheritance,
    MultipleConditionExplanation,
    VariantType,
)
from clinvar_this import exceptions
from clinvar_this.io.tsv import (
    BatchMetadata,
    SeqVarTsvRecord,
    StrucVarTsvRecord,
    TsvType,
    guess_tsv_type,
    read_seq_var_tsv,
    read_struc_var_tsv,
    seq_var_tsv_records_to_submission_container,
    struc_var_tsv_records_to_submission_container,
    submission_container_to_seq_var_tsv_records,
    submission_container_to_struc_var_tsv_records,
)

DATA_DIR = pathlib.Path(__file__).parent / "data/io_tsv"


def _create_struc_tsv_fake(overrides: dict) -> StringIO:
    entry = {
        "ASSEMBLY": "GRCh37",
        "CHROM": "10",
        "START": "123456",
        "STOP": "654321",
        "SV_TYPE": "Deletion",
        "CONDITION": "",
        "MOI": "Autosomal recessive inheritance",
        "CLIN_SIG": "not provided",
    }
    for k, v in overrides.items():
        entry[k] = v
    header = list(entry.keys())
    values = list(entry.values())
    tsv_string = "\n".join("\t".join(line) for line in [header, values])
    return StringIO(tsv_string)


def _create_seq_tsv_fake(overrides: dict) -> StringIO:
    entry = {
        "ASSEMBLY": "GRCh37",
        "CHROM": "10",
        "POS": "123456",
        "REF": "A",
        "ALT": "G",
        "CONDITION": "",
        "MOI": "Autosomal recessive inheritance",
        "CLIN_SIG": "not provided",
    }
    for k, v in overrides.items():
        entry[k] = v
    header = list(entry.keys())
    values = list(entry.values())
    tsv_string = "\n".join("\t".join(line) for line in [header, values])
    return StringIO(tsv_string)


def test_read_seq_var_tsv_path():
    actual = read_seq_var_tsv(path=DATA_DIR / "example.tsv")
    assert actual == [
        SeqVarTsvRecord(
            accession="SCV1",
            assembly=Assembly.GRCH37,
            chromosome=Chromosome.CHR10,
            pos=115614632,
            ref="A",
            alt="G",
            condition=["OMIM:618278"],
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
            accession="SCV1",
            assembly=Assembly.GRCH38,
            chromosome=Chromosome.CHR1,
            start=844347,
            stop=4398122,
            sv_type=VariantType.DELETION,
            condition=[],
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
            accession="SCV1",
            assembly=Assembly.GRCH37,
            chromosome=Chromosome.CHR10,
            pos=115614632,
            ref="A",
            alt="G",
            condition=["OMIM:618278"],
            inheritance=ModeOfInheritance.AUTOSOMAL_RECESSIVE_INHERITANCE,
            clinical_significance_description=ClinicalSignificanceDescription.NOT_PROVIDED,
            local_key="KEY",
            extra_data={"gene": "NHLRC2"},
        )
    ]


def test_read_seq_var_tsv_file_citation():
    with (DATA_DIR / "example_citation.tsv").open("rt") as inputf:
        actual = read_seq_var_tsv(file=inputf)
    assert actual == [
        SeqVarTsvRecord(
            assembly=Assembly.GRCH37,
            chromosome=Chromosome.CHR10,
            pos=115614632,
            ref="A",
            alt="G",
            condition=["OMIM:618278"],
            inheritance=ModeOfInheritance.AUTOSOMAL_RECESSIVE_INHERITANCE,
            clinical_significance_description=ClinicalSignificanceDescription.NOT_PROVIDED,
            local_key="KEY",
            pmids=["123456", "000001"],
            extra_data={"gene": "NHLRC2"},
        )
    ]


def test_read_struc_var_tsv_file():
    with (DATA_DIR / "example_sv.tsv").open("rt") as inputf:
        actual = read_struc_var_tsv(file=inputf)
    assert actual == [
        StrucVarTsvRecord(
            accession="SCV1",
            assembly=Assembly.GRCH38,
            chromosome=Chromosome.CHR1,
            start=844347,
            stop=4398122,
            sv_type=VariantType.DELETION,
            condition=[],
            inheritance=ModeOfInheritance.AUTOSOMAL_DOMINANT_INHERITANCE,
            clinical_significance_description=ClinicalSignificanceDescription.NOT_PROVIDED,
            hpo_terms=["HP:0001263"],
        )
    ]


class TestConditionDefinition:
    condition_strings = [
        {
            "raw": "OMIM:123",
            "expected": ["OMIM:123"],
            "parsed": SubmissionConditionSet(
                condition=[SubmissionCondition(db=ConditionDb.OMIM, id="123")]
            ),
        },
        {
            "raw": "MONDO:123;OMIM:123",
            "expected": ["MONDO:123", "OMIM:123"],
            "parsed": SubmissionConditionSet(
                condition=[
                    SubmissionCondition(db=ConditionDb.MONDO, id="MONDO:123"),
                    SubmissionCondition(db=ConditionDb.OMIM, id="123"),
                ]
            ),
        },
        {
            "raw": "MONDO:123 ;OMIM:123",
            "expected": ["MONDO:123", "OMIM:123"],
            "parsed": SubmissionConditionSet(
                condition=[
                    SubmissionCondition(db=ConditionDb.MONDO, id="MONDO:123"),
                    SubmissionCondition(db=ConditionDb.OMIM, id="123"),
                ]
            ),
        },
        {
            "raw": "MONDO:123;OMIM:123;ORPHA:123",
            "expected": ["MONDO:123", "OMIM:123", "ORPHA:123"],
            "parsed": SubmissionConditionSet(
                condition=[
                    SubmissionCondition(db=ConditionDb.MONDO, id="MONDO:123"),
                    SubmissionCondition(db=ConditionDb.OMIM, id="123"),
                    SubmissionCondition(db=ConditionDb.ORPHANET, id="ORPHA123"),
                ]
            ),
        },
        {
            "raw": "MONDO:123;OMIM:123;ORPHA:123;Uncertain",
            "expected": ["MONDO:123", "OMIM:123", "ORPHA:123", "Uncertain"],
            "parsed": SubmissionConditionSet(
                condition=[
                    SubmissionCondition(db=ConditionDb.MONDO, id="MONDO:123"),
                    SubmissionCondition(db=ConditionDb.OMIM, id="123"),
                    SubmissionCondition(db=ConditionDb.ORPHANET, id="ORPHA123"),
                ],
                multiple_condition_explanation=MultipleConditionExplanation.UNCERTAIN,
            ),
        },
        {
            "raw": "MONDO:123;OMIM:123;ORPHA:123;Co-occurring",
            "expected": ["MONDO:123", "OMIM:123", "ORPHA:123", "Co-occurring"],
            "parsed": SubmissionConditionSet(
                condition=[
                    SubmissionCondition(db=ConditionDb.MONDO, id="MONDO:123"),
                    SubmissionCondition(db=ConditionDb.OMIM, id="123"),
                    SubmissionCondition(db=ConditionDb.ORPHANET, id="ORPHA123"),
                ],
                multiple_condition_explanation=MultipleConditionExplanation.CO_OCCURING,
            ),
        },
        {
            "raw": "HP:123;HP:124;HP:125;Novel disease",
            "expected": ["HP:123", "HP:124", "HP:125", "Novel disease"],
            "parsed": SubmissionConditionSet(
                condition=[
                    SubmissionCondition(db=ConditionDb.HP, id="HP:123"),
                    SubmissionCondition(db=ConditionDb.HP, id="HP:124"),
                    SubmissionCondition(db=ConditionDb.HP, id="HP:125"),
                ],
                multiple_condition_explanation=MultipleConditionExplanation.NOVEL_DISEASE,
            ),
        },
    ]

    def _create_seq_record(self, **overrides):
        params = {
            "assembly": Assembly.GRCH37,
            "chromosome": Chromosome.CHR1,
            "pos": 123,
            "ref": "A",
            "alt": "G",
            "condition": ["not provided"],
            "inheritance": ModeOfInheritance.AUTOSOMAL_DOMINANT_INHERITANCE,
            "clinical_significance_description": ClinicalSignificanceDescription.NOT_PROVIDED,
            "hpo_terms": ["HP:0001263"],
        }
        for k, v in overrides.items():
            params[k] = v
        return SeqVarTsvRecord(**params)

    def _create_struc_record(self, **overrides):
        params = {
            "assembly": Assembly.GRCH37,
            "chromosome": Chromosome.CHR1,
            "start": 123,
            "stop": 543,
            "sv_type": VariantType.DELETION,
            "condition": ["not provided"],
            "inheritance": ModeOfInheritance.AUTOSOMAL_DOMINANT_INHERITANCE,
            "clinical_significance_description": ClinicalSignificanceDescription.NOT_PROVIDED,
            "hpo_terms": ["HP:0001263"],
        }
        for k, v in overrides.items():
            params[k] = v
        return StrucVarTsvRecord(**params)

    def test_seq_vars_read(self):
        for condition in self.condition_strings:
            result = read_seq_var_tsv(file=_create_seq_tsv_fake({"CONDITION": condition["raw"]}))
            assert len(result) == 1
            assert result[0].condition == condition["expected"]

    def test_struc_vars_read(self):
        for condition in self.condition_strings:
            result = read_struc_var_tsv(
                file=_create_struc_tsv_fake({"CONDITION": condition["raw"]})
            )
            assert len(result) == 1
            assert result[0].condition == condition["expected"]

    def test_seq_vars_parse(self):
        metadata = BatchMetadata()
        for condition in self.condition_strings:
            record = self._create_seq_record(condition=condition["expected"])
            container = seq_var_tsv_records_to_submission_container([record], metadata)
            assert container.clinvar_submission is not None
            assert container.clinvar_submission[0].condition_set == condition["parsed"]

    def test_struc_vars_parse(self):
        metadata = BatchMetadata()
        for condition in self.condition_strings:
            record = self._create_struc_record(condition=condition["expected"])
            container = struc_var_tsv_records_to_submission_container([record], metadata)
            assert container.clinvar_submission is not None
            assert container.clinvar_submission[0].condition_set == condition["parsed"]

    def test_seq_vars_dump(self):
        metadata = BatchMetadata()
        for condition in self.condition_strings:
            record = self._create_seq_record(condition=condition["expected"])
            container = seq_var_tsv_records_to_submission_container([record], metadata)
            reconverted = submission_container_to_seq_var_tsv_records(container)
            assert len(reconverted) == 1
            assert record.condition == reconverted[0].condition

    def test_struc_vars_dump(self):
        metadata = BatchMetadata()
        for condition in self.condition_strings:
            record = self._create_struc_record(condition=condition["expected"])
            container = struc_var_tsv_records_to_submission_container([record], metadata)
            reconverted = submission_container_to_struc_var_tsv_records(container)
            assert len(reconverted) == 1
            assert record.condition == reconverted[0].condition


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
    assert guess_tsv_type(path=str(DATA_DIR / "example.bad.tsv")) == None  # noqa: E711
    assert guess_tsv_type(path=str(DATA_DIR / "example.tsv")) == TsvType.SEQ_VAR
    assert guess_tsv_type(path=str(DATA_DIR / "example_sv.tsv")) == TsvType.STRUC_VAR
