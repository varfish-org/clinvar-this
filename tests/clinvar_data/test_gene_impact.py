from clinvar_data import gene_impact


def test_smoke_test_run(tmpdir, snapshot):
    path_input = "tests/clinvar_data/data/ten_records.jsonl"
    path_output = f"{tmpdir}/output.jsonl"
    gene_impact.run_report(path_input, path_output)

    with open(path_output, "rt") as outputf:
        snapshot.assert_match(outputf.read(), "output.jsonl")
