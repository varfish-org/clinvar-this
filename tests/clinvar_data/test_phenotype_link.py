import pytest

from clinvar_data import phenotype_link


@pytest.mark.parametrize("inputf", ["records_with_hpo.jsonl", "record_with_submitter.jsonl"])
def test_smoke_test_run(inputf, tmpdir, snapshot):
    path_input = f"tests/clinvar_data/data/{inputf}"
    path_output = f"{tmpdir}/output.jsonl"
    phenotype_link.run_report(path_input, path_output)

    with open(path_output, "rt") as outputf:
        snapshot.assert_match(outputf.read(), "output.jsonl")
