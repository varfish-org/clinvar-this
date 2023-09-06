from clinvar_data import class_by_freq


def test_smoke_test_run(tmpdir, snapshot):
    path_input = "tests/clinvar_data/data/records_with_gmaf.jsonl"
    path_output = f"{tmpdir}/output.jsonl"
    class_by_freq.run_report(path_input, path_output, thresholds=class_by_freq.DEFAULT_THRESHOLDS)

    with open(path_output, "rt") as outputf:
        snapshot.assert_match(outputf.read(), "output.jsonl")
