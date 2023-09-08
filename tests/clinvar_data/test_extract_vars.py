import os

import pytest

from clinvar_data import extract_vars


@pytest.mark.parametrize("inputf", ["ex_kynu.jsonl"])
def test_smoke_test_run(inputf, tmpdir, snapshot):
    path_input = f"tests/clinvar_data/data/{inputf}"
    path_output = str(tmpdir)
    extract_vars.run(path_input, path_output, gzip_output=False)

    for path_f in [
        "clinvar-variants-grch37-seqvars.jsonl",
        "clinvar-variants-grch38-seqvars.jsonl",
    ]:
        with open(os.path.join(tmpdir, path_f), "rt") as outputf:
            snapshot.assert_match(outputf.read(), path_f)
