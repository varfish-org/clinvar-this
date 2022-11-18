[![codecov](https://codecov.io/gh/bihealth/clinvar-this/branch/main/graph/badge.svg?token=059T45KAQM)](https://codecov.io/gh/bihealth/clinvar-this)
[![Documentation Status](https://readthedocs.org/projects/clinvar-this/badge/?version=latest)](https://clinvar-this.readthedocs.io/en/latest/?badge=latest)

# ClinVar This!

ClinVar Submission via API Made Easy

- Free software: MIT license
- Documentation: https://clinvar-this.readthedocs.io/en/latest/


## Caveats

- **The `--use-testing` and `--dry-run` mode.**
  When enabling `--use-testing`, an alternative API endpoint provided by ClinVar will be used.
  This endpoint may use a different schema than the official endpoint (e.g., this has happened in November 2022).
  ClinVar has previously notified their submitters via email without official news posts.
