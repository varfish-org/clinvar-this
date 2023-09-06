from clinvar_data import phenotype_link


def test_smoke_test_run(tmpdir, snapshot):
    path_input = "tests/clinvar_data/data/records_with_hpo.jsonl"
    path_output = f"{tmpdir}/output.jsonl"
    phenotype_link.run_report(path_input, path_output)

    with open(path_output, "rt") as outputf:
        snapshot.assert_match(outputf.read(), "output.jsonl")
