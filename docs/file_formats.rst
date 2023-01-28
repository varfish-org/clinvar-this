.. _file_formats:

============
File Formats
============

This section documents the supported file formats that can be imported by ``batch import``.
In the case of the non-native TSV format, this section documents how the file format maps to the information handled and stored by clinvar-this.

--------------------------
Small Variant TSV (Native)
--------------------------

The following headers are required.
Clinvar-this will recognize the TSV file format based on these headers.

- ``ASSEMBLY`` - the assembly used, e.g., ``GRCh37``, ``hg19``, ``GRCh38``, ``hg38``
- ``CHROM`` - the chromosomal position without ``chr`` prefix, e.g., ``1``
- ``POS`` - the 1-based position of the first base in ``REF`` column
- ``REF`` - the reference allele of your variant
- ``ALT`` - the alternative allele of your variant
- ``OMIM`` - the OMIM id of the carrier's condition (not the OMIM gene ID), e.g., ``619325``.
  Leave empty or use ``not provided`` if you have no OMIM ID.
- ``MOI`` - mode of inheritance, e.g., ``Autosomal dominant inheritance`` or ``Autosomal recessive inheritance``
- ``CLIN_SIG`` - clinical significance, e.g. ``Pathogenic``, or ``Likely benign``

The following headers are optional:

- ``clinvar_accession`` - ClinVar SCV accession if any exists yet.
  When this is set then this variant will be updated in the batch rather than added as a novel variant.
- ``CLIN_EVAL`` - date of late clinical evaluation, e.g. ``2022-12-02``, leave empty to fill with the date of today
- ``CLIN_COMMENT`` - a comment on the clinical significance, e.g., ``ACMG Class IV; PS3, PM2_sup, PP4``
- ``KEY`` - a local key to identify the variant/condition pair.
  Filled automatically with a UUID if missing, recommeded to leave empty.
- ``HPO`` - List of HPO terms separated by comma or semicolon, any space will be stripped.
  E.g., ``HP:0004322; HP:0001263``.

Any further header will be imported into the local repository into an ``extra_data`` field.
Note that the error returned by ClinVar for your variant will be writen to a ``error_msg`` field.
