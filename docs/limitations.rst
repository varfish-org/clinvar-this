.. _limitations:

===========
Limitations
===========


----------------
Design Decisions
----------------


``clinvar_api``
===============

The ``clinvar_api`` module provides a full implementation of the NCBI ClinVar API as documented.
In the case of changes to the upstream NCBI API, we aim to adjust the code appropriately.
Please let us know about any issues in the `GitHub issue tracker <https://github.com/bihealth/clinvar-tsv/issues>`__.
Note that the ClinVar API has some limitations when compared with uploading the spreadsheet templates via the ClinVar submission website.

At the time of writing (January 2023), the following were unsupported.

- age of onset
- observedIn

    - citations
    - tissue
    - variant allele count
    - zygosity

The ClinVar staff has been made aware of these limitations and intends to fill the gaps at some point.


clinvar-this
============

The clinvar-this software provides a **useful and not-so-minimal, yet limited, subset** for creating ClinVar submissions.
The aim is to allow for the easy automated submission of variants with associated diseases and phenotypes to ClinVar in environments with medium to high turnover of cases such as diagnostics labs.
Non-aims include providing a graphical interface and providing full, fine-grained access to all ClinVar submission API features.

The authors make the following assumptions:

- all variants have GRCh37 or GRCh38 coordinates
- users have experience in the Linux command line and bioinformatics data formats
- users have pathogenicity assessments and OMIM/HPO terms stored in machine-readable format already and do not need another database of their variants
- users are interested in getting their variant assessment information into ClinVar and then get on with their (work) life
- the ClinVar API is useful but not flawless; in the case of problems, users are willing to look into details (and report them back to the authors)
- if users want custom features, they will either implement them ``clinvar_api`` in their own software or work with the authors on improving clinvar-this

The clinvar-this package makes the following opinionated decisions:

- data is internally stored slightly augmented ClinVar API JSON data (full introspection) in internal repository
- all sent and received data is stored as in inernal repository for debugging introspection when necessary
- common formats such as Phenopackets can be imported, but only certain subsets are interpreted with focus on usability in clinvar-this


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
