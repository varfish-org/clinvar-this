.. _known_issues:

============
Known Issues
============

-----------------------------------
Testing and Dry-run Inconsistencies
-----------------------------------

When enabling `--use-testing`, an alternative API endpoint provided by ClinVar will be used.
This is different than when using ``--dry-run`` which uses the main endpoint with a dry-run parameter.
This endpoint may use a different schema than the official endpoint (e.g., this has happened in November 2022).
ClinVar has previously notified their submitters via email without official news posts.

---------------------------------------------
Lack of Proper Versioning in NCBI ClinVar API
---------------------------------------------

The ClinVar API from NCBI is not properly versioned.
The same is true for their documentation and the JSON schemas that you may find on there.

-------------------------------------------
Inconsistent Schema use by NCBI ClinVar API
-------------------------------------------

You may see warnings abou the results from the ClinVar API not fulfilling their provided schemas.
This sometimes happens and you can ignore them.
Apparently, the NCBI ClinVar server has no tight coupling to the JSON schemas and these schemas are mostly for informative purposes.
