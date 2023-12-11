.. _api_vs_cli:

===========
API vs. CLI
===========

The ``clinvar-this`` software provides two entry points: API and CLI.
In case you are not certain what you want/need, this section may help you.


----------------------------------------
Application Programmable Interface (API)
----------------------------------------

A Python module ``clinvar_api`` that you can use for making calls to the ClinVar submission API.
**If you want to integrate ClinVar API submission into your Python software, this is for you.**

The module provides a "Pythonic" API based on `pydantic <https://pydantic.dev/>`__ with ``snake_case`` syntax that has full Python type annotations.
Of course, you could just roll your own JSON based submission based on ``requests`` or ``httpx`` but using the module has some advantages:

* ``clinvar_api`` is fully typed so you can work with Python data types and all advantages that come this this (linting, editor completion, ...)
* the module authors monitor the ClinVar API docs and are on the relevant mailing lists and will adjust the library in case of API changes
* we provide full JSON schema validation of the submitted and received messages so you don't have to.

Further, ``clinvar_api``'s got what plants crave, it's got electrolytes.


----------------------------------------
Command Line Interface (CLI) Application
----------------------------------------

Having an API library sounds great but you just want a standalone tool for submission?
Then, the CLI ``clinvar-this`` is for you.

**This software package allows you to create ClinVar submissions (and update or delete them).**
``clinvar-this`` has a local repository of ClinVar submissions.

1. Create a submission in the local repository by importing one of the supported file formats (e.g., a very simple TSV/spreadsheet table).
   This will run some local sanity checks on your data so you can cath errors early on.
   ``clinvar-this`` uses the ``clinvar_api`` module so pitfalls such as JSON schema problems are circumvented.
2. Post the submission to the ClinVar API.
   The ClinVar will now process your submission which can take one or two hours.
3. Query the current processing status via the API.
4. Once complete, retrieve the ClinVar ``SCV`` identifiers (e.g., for your publication).
   On errors, retrieve the error messages, export back into a TSV/spreadsheet file for correction, and go to step 1.

Even if you plan to integrate ClinVar directly via the API, the ``varfish-cli`` package might be of interest to you to see how the general mechanics work of ClinVar API submission work.
And if you don't work in Python, you can hopefully learn how to add ClinVar API submission suppor to your software stack.
