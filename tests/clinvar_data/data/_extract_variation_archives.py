"""Helper to extract the ``<VariationArchive>`` elements from the ClinVar XML"""

import dataclasses
import gzip
import os
import subprocess
import sys

import tqdm

#: Number of lines in XML file on 2024-05-24 was 783496700.
NUM_LINES = 800_000_000


@dataclasses.dataclass
class Target:
    """Specify a collection target."""

    vcvs: list[str]
    name: str


#: The targets VCVs to collect.
TARGETS: list[Target] = [
    Target(
        vcvs=["VCV000000002"],
        name="first",
    ),
    Target(
        vcvs=["VCV000056992"],
        name="ex_additional_submitters",
    ),
    Target(
        vcvs=["VCV000011900"],
        name="ex_attribute_set",
    ),
    Target(
        vcvs=["VCV001810274"],
        name="ex_custom_score",
    ),
    Target(
        vcvs=["VCV000009474"],
        name="ex_flagged_submission",
    ),
    Target(
        vcvs=["VCV000226036"],
        name="ex_indication",
    ),
    Target(
        vcvs=["VCV000978270"],
        name="ex_kynu",
    ),
    Target(
        vcvs=["VCV000012205"],
        name="ex_missense",
    ),
    Target(
        vcvs=["VCV000127244"],
        name="ex_no_unflagged",
    ),
    Target(
        vcvs=["VCV000029674"],
        name="ex_replaces",
    ),
    Target(
        vcvs=["VCV001708487"],
        name="ex_review_status_ns",
    ),
    Target(
        vcvs=["VCV000034753"],
        name="ex_study_description",
    ),
    Target(
        vcvs=["VCV000065427"],
        name="ex_study_name",
    ),
    Target(
        vcvs=["VCV000000654"],
        name="ex_with_ethnicity",
    ),
    Target(
        vcvs=["VCV000007501"],
        name="ex_with_hpo",
    ),
    Target(
        vcvs=["VCV000018396"],
        name="one_record",
    ),
    Target(
        vcvs=["VCV000018396", "VCV000018397"],
        name="two_records",
    ),
    Target(
        vcvs=["VCV000253751"],
        name="record_with_submitter",
    ),
    Target(
        vcvs=[
            "VCV000000220",
            "VCV000000221",
            "VCV000000224",
            "VCV000000228",
            "VCV000000273",
            "VCV000000351",
            "VCV000000407",
            "VCV000000408",
            "VCV000000573",
            "VCV000000574",
            "VCV000000575",
            "VCV000000651",
            "VCV000000654",
            "VCV000000856",
            "VCV000000857",
            "VCV000000858",
            "VCV000000859",
            "VCV000000860",
            "VCV000000861",
            "VCV000000862",
            "VCV000000863",
            "VCV000000864",
            "VCV000001190",
            "VCV000001192",
            "VCV000001194",
            "VCV000001212",
            "VCV000001408",
            "VCV000001610",
            "VCV000001612",
            "VCV000002497",
            "VCV000002752",
            "VCV000002940",
            "VCV000003350",
            "VCV000004159",
            "VCV000005052",
            "VCV000005053",
            "VCV000005054",
            "VCV000005220",
            "VCV000005221",
        ],
        name="records_with_hpo",
    ),
    Target(
        vcvs=[
            "VCV000018396",
            "VCV000018397",
            "VCV000000002",
            "VCV000000003",
            "VCV000000006",
            "VCV000000025",
            "VCV000000026",
            "VCV000000032",
            "VCV000000040",
            "VCV000000042",
        ],
        name="ten_records",
    ),
]


def main() -> int:
    args = sys.argv
    if len(args) != 2:
        print("Usage: extract_variation_archives.py <input_xml>")
        return 1

    input_xml = args[1]
    out_dir = os.path.dirname(__file__)

    print(f"Extracting from {input_xml} to {out_dir}...", file=sys.stderr)

    if input_xml.endswith(".gz"):
        inputf = gzip.open(input_xml, "rt")
    else:
        inputf = open(input_xml, "rt")

    with inputf:
        leading: list[str] = []
        collecting: dict[str, bool] = {}
        collected: dict[str, list[str]] = {target.name: [] for target in TARGETS}
        trailing: list[str] = ["</ClinVarVariationRelease>"]
        for lineno, line in tqdm.tqdm(
            enumerate(inputf), unit="lines", unit_scale=True, unit_divisor=1000, total=NUM_LINES
        ):
            if lineno < 2:
                leading.append(line.rstrip())
            elif line.startswith("<VariationArchive"):
                for target in TARGETS:
                    if any(f'Accession="{vcv}"' in line for vcv in target.vcvs):
                        collecting[target.name] = True
                        collected[target.name].append(line.rstrip())
            elif line.startswith("</VariationArchive>"):
                for key, value in collecting.items():
                    if value:
                        collected[key].append(line.rstrip())
                        collecting[key] = False
            else:
                for key, value in collecting.items():
                    if value:
                        collected[key].append(line.rstrip())

    for target in TARGETS:
        with open(os.path.join(out_dir, f"{target.name}.xml"), "wt") as outputf:
            outputf.write("\n".join(leading + collected[target.name] + trailing) + "\n")

    subprocess.run(["gzip", "--keep", "--force", "tests/clinvar_data/data/one_record.xml.gz"])
    for name in ["ex_kynu", "record_with_submitter", "records_with_hpo", "ten_records"]:
        subprocess.run(
            [
                "clinvar-this",
                "data",
                "xml-to-jsonl",
                f"tests/clinvar_data/data/{name}.xml",
                f"tests/clinvar_data/data/{name}.jsonl",
            ]
        )
    subprocess.run(["gzip", "--keep", "--force", "tests/clinvar_data/data/one_record.xml"])

    return 0


if __name__ == "__main__":
    sys.exit(main())
