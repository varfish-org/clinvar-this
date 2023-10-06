.. _file_formats:

============
File Formats
============

This section documents the supported file formats that can be imported by ``batch import``.
In the case of the non-native TSV format, this section documents how the file format maps to the information handled and stored by clinvar-this.

Overall, the aim of clinvar-this is to support you in submitting data easily with restrictions (see :ref:`limitations`).
If you need the full functionality of the NCBI ClinVar API then please consider using the ``clinvar_api`` Python module.

-----------------------------
Sequence Variant TSV (Native)
-----------------------------

The following headers are required.
Clinvar-this will recognize the TSV file format based on these headers.

- ``ASSEMBLY`` - the assembly used, e.g., ``GRCh37``, ``hg19``, ``GRCh38``, ``hg38``
- ``CHROM`` - the chromosomal position without ``chr`` prefix, e.g., ``1``
- ``POS`` - the 1-based position of the first base in ``REF`` column
- ``REF`` - the reference allele of your variant
- ``ALT`` - the alternative allele of your variant
- ``CONDITION`` - the OMIM id of the carrier's condition (not the OMIM gene ID), e.g., ``619325``, alternatively also MONDO, ORPHA and HPO-Terms are supported, if multiple conditions are given, a multiple condition qualifier (``Co-occurring``, ``Uncertain``, ``Novel disease``) should also be given as an additional term.
  Leave empty or use ``not provided`` if you have no OMIM ID.
- ``MOI`` - mode of inheritance, e.g., ``Autosomal dominant inheritance`` or ``Autosomal recessive inheritance``
- ``CLIN_SIG`` - clinical significance, e.g. ``Pathogenic``, or ``Likely benign``

The following headers are optional:

- ``clinvar_accession`` - ClinVar SCV accession if any exists yet.
  When this is set then this variant will be updated in the batch rather than added as a novel variant.
- ``CLIN_EVAL`` - date of last clinical evaluation, e.g. ``2022-12-02``, leave empty to fill with the date of today
- ``CLIN_COMMENT`` - a comment on the clinical significance, e.g., ``ACMG Class IV; PS3, PM2_sup, PP4``
- ``KEY`` - a local key to identify the variant/condition pair.
  Filled automatically with a UUID if missing, recommeded to leave empty.
- ``HPO`` - List of HPO terms separated by comma or semicolon, any space will be stripped.
  E.g., ``HP:0004322; HP:0001263``.
- ``PMID`` - List of Pubmed IDs separated by a comma or semicolon, any space
  will be stripped.
  E.g., ``31859447‚29474920``.
- ``ACCESSION`` - Existing clinvar SCV for this variant. This should only be set
  if the submitters organization has already uploaded the variant for the same
  condition before.
- ``$remove_from_batch`` - you can use this for removing a previously added variant from the given batch; one of ``true`` and ``false``, defaults to ``false``.

Any further header will be imported into the local repository into an ``extra_data`` field.
Note that the error returned by ClinVar for your variant will be writen to a ``error_msg`` field.

The following shows an example.

.. code-block:: text

    ASSEMBLY	CHROM	POS	REF	ALT	CONDITION	MOI	CLIN_SIG	HPO
    GRCh37	19	48183936	C	CA	OMIM:619325	Autosomal	dominant	inheritance	Likely	pathogenic	HP:0004322;HP:0001263

Note that you cannot submission TSV imports with batches that contain removals already.

-------------------------------
Structural Variant TSV (Native)
-------------------------------

The following headers are required.
Clinvar-this will recognize the TSV file format based on these headers.

- ``ASSEMBLY`` - the assembly used, e.g., ``GRCh37``, ``hg19``, ``GRCh38``, ``hg38``
- ``CHROM`` - the chromosomal position without ``chr`` prefix, e.g., ``1``
- ``START`` - the 1-based position
- ``STOP`` - the 1-based end position
- ``SV_TYPE`` - the type of the structural variant; one of ``Insertion``, ``Deletion``, ``Duplication``, ``Tandem duplication``, ``copy number loss``, ``copy number gain``, ``Inversion``, ``Translocation``, ``Complex``.
  Note that ClinVar does not allow you to specify the second end of a non-linear event (e.g., a fusion with another chromosome).
  We suggest that you submit a second SV entry with the coordinate and link the two events in ``CLIN_COMMENT``.
- ``CONDITION`` - the OMIM id of the carrier's condition (not the OMIM gene ID), e.g., ``OMIM:619325``, alternatively also MONDO, ORPHA and HPO-Terms are supported, if multiple conditions are given, a multiple condition qualifier (``Co-occurring``, ``Uncertain``, ``Novel disease``) should also be given as an additional term.
- ``MOI`` - mode of inheritance, e.g., ``Autosomal dominant inheritance`` or ``Autosomal recessive inheritance``
- ``CLIN_SIG`` - clinical significance, e.g. ``Pathogenic``, or ``Likely benign``

Note that instead of ``START`` and ``STOP`` you can also provide the following headers.
You have to provide all of them and cannot provide them together with ``START`` and ``STOP``

- ``START:OUTER`` - imprecise start location, outer boundary
- ``START:INNER`` - imprecise start location, inner boundary
- ``STOP:INNER`` - imprecise start location, inner boundary
- ``STOP:OUTER`` - imprecise stop location, outer boundary

The following headers are optional:

- ``ACCESSION`` - ClinVar SCV accession if any exists yet.
  When this is set then this variant will be updated in the batch rather than added as a novel variant.
- ``CLIN_EVAL`` - date of late clinical evaluation, e.g. ``2022-12-02``, leave empty to fill with the date of today
- ``CLIN_COMMENT`` - a comment on the clinical significance, e.g., ``ACMG Class IV; PS3, PM2_sup, PP4``
- ``KEY`` - a local key to identify the variant/condition pair.
  Filled automatically with a UUID if missing, recommeded to leave empty.
- ``HPO`` - List of HPO terms separated by comma or semicolon, any space will be stripped.
  E.g., ``HP:0004322; HP:0001263``.
- ``PMID`` - List of Pubmed IDs separated by a comma or semicolon, any space
  will be stripped.
  E.g., ``31859447‚29474920``.
- ``$remove_from_batch`` - you can use this for removing a previously added variant from the given batch; one of ``true`` and ``false``, defaults to ``false``.

Any further header will be imported into the local repository into an ``extra_data`` field.
Note that the error returned by ClinVar for your variant will be writen to a ``error_msg`` field.

The following shows an example.

.. code-block:: text

    ASSEMBLY	CHROM	START	STOP	SV_TYPE	CONDITION	MOI	CLIN_SIG	HPO
    GRCh38	chr1	844347	4398122	Deletion	not provided	Autosomal dominant inheritance	HP:0001263

Note that you cannot submission TSV imports with batches that contain removals already.

-----------
Removal TSV
-----------

The following headers are required.
Clinvar-this will recognize the TSV file format based on these headers.

- ``SCV`` - the ClinVar accession to be deleted
- ``REASON`` - a free text comment to give to ClinVar as a reason

You can optionally provide the following header:

- ``$remove_from_batch`` - you can use this for removing a previously added variant from the given deletion batch; one of ``true`` and ``false``, defaults to ``false``.

The following shows an example:

.. code-block:: text

    SCV	REASON
    SCV00042	Uploaded with hg38 coordinates but annotated as hg19; replaced by SCV00043.

Note that you cannot submission TSV imports with batches that contain removals already.

------------
Phenopackets
------------

Notes:

- This has not been implemented yet.

Note that only Phenopackets version 2 is supported.
Phenopackets are interpreted as follows:

- When ``Family`` or ``Cohort`` are used then all contained ``Phenopacket`` records will be interpreted.
- Variants will be read from ``Phenopacket.diagnosis.genomic_interpretations`` and below.
- Each ``Diagnosis`` must be labeled with the corresponding ``disease`` (corresponds to ``OMIM`` in TSV).
  The following IDs are allowed for ClinVar: ``OMIM``, ``MedGen``, ``Orphanet``, ``MeSH``, ``HP``, ``MONDO``.
  When no disease is given, ``not provided`` will be used.
- ``Diagnosis.genomic_interpretations`` will be scanned for variants.
  When ``interpretation_status`` is ``UNKNOWN_STATUS`` or ``REJECTED`` then this ``GenomicInterpretation`` will be ignored.
  ``GenomicInterpretation`` records providing no ``variant_interpretation`` are ignored.
- ``VariantInterpretation.acmg_pathogenicity_classification`` will be mapped to the clinical significance (``CLIN_SIG`` in TSV).
- ``VariantInterpretation.variation_descriptor`` will be used to describe the variant.
- See the section :ref:`vcf_files` on the interpretation of ``VariantDescription.vcf_record`` (as it relates to the variant).
  As ClinVar API does not support allelic state yet, decode ``allelic_state`` to the mode of inheritance.

The following decoding ``allelic_state`` to mode of inheritance (``MOI`` in TSV) is performed.

- GENO:0000603 (heteroplasmic), GENO:0000602 (homoplasmic) are mapped to ``Mitochondrial inheritance``.
- GENO:0000136 (homozygous), GENO:0000402 (compound heterozygous) are mapped to ``Autosomal recessive inheritance`` unless the variant is on the X chromosome in which case ``X-linked recessive inheritance`` is used.
- GENO:0000458 (simple heterozygous) is mapped to ``Autosomal dominant inheritance`` unless the variant is on the X chromosome in which case ``X-linked dominant inheritance`` is used.
- GENO:0000604 (hemizygous X-linked) is mapped to ``X-linked recessive inheritance``.
- GENO:0000605 (hemizygous Y-linked) is mapped to ``Y-linked inheritance``.
- In all other cases, ``not provided`` will be used.
- Note that you will need to use compound heterozygous even if you are matching the second hit to express recessive inheritance.

You currently cannot use phenopackets to update batches.
You will need to export to TSV and re-import from there.

.. _vcf_files:

------------------------
Variant Call Files (VCF)
------------------------

Notes:

- This has not been implemented yet.

- The VCF file must contain headers for the chromosomes and the genome release is derived from the chromosome lengths.
- VCF files may only contain the one sample that is to be submitted.
- Small variants will be decoded directly from ``CHROM``, ``POS``, ``REF``, ``ALT``.
- Structural variants will be decoded as follows.

    - ``REF`` will be ignored
    - ``ALT`` should show one of the VCF alternative allele descriptions.
      We interpret the following ``<DEL>``, ``<DUP>``, ``<DUP:TANDEM>``, ``<INV>``, ``<INS>`` and VCF encoded break-ends.
      If the ``ALT`` value matches a prefix in the list above (e.g., ``<INS>`` is a prefix for ``<INS:ME>``) then this prefix will be used.
      All invalid variant specifications will be ignored.
    - ``INFO/END`` must be the end position of the variant, for break-ends the target chromosome/pos is parsed from ``ALT``.
    - We will map break-ends and ``<INS>`` to ``Complex`` and the other types to the corresponding equivalents in ClinVar terminology.

- You provide the following ``INFO`` fields (use URL encoding) for the mandatory information that you are used to from VCF.
    - ``OMIM`` - the OMIM ID of the carrier, can be empty or "not provided"
    - ``HPO`` - corresponds to ``HPO`` in TSV
    - ``KEY`` - corresponds to ``KEY`` in TSV
    - ``CLIN_EVAL`` - corresponds to ``CLIN_EVAL`` in TSV
    - ``CLIN_COPMMENT`` - corresponds to ``CLIN_COMMENT`` in TSV
    - ``clinvar_accession`` - corresponds to ``clinvar_accession`` in TSV

See the examples directory for example VCF files that also show you working VCF header sections for the INFO values used above.

You currently cannot use VCF to update batches (of course you can provide clinvar accessions to trigger ClinVar record updates).
You will need to export to TSV and re-import from there.

-----------------------
ClinVar Excel Templates
-----------------------

Notes:

- This has not been implemented yet.

You already have a process for filling out these ClinVar Excel tables?
You have one filled out already and not submitted before discovering clinvar-this?
This is for you.

Only the "Variant" tab is used.

You have to use ``SubmissionTemplate.xlsx``. The following columns are interpreted by clinvar-this.

- ``Local ID`` / ``A`` maps to ``KEY`` from the TSV format.
- For small variants, you can specify the coordinates based on transcripts or genomic description, so either will translate to (``CHROM``, ``POS``, ``REF``, and ``ALT``; you will have to specify the release on the command line on import):

    - ``Reference sequence`` / ``D`` and ``HGVS`` / ``E`` are translated into chromosomal coordinates using the `VariantValidator <https://variantvalidator.org/>`__ API, OR:
    - ``Chromosome``, ``Start``, ``Stop``, ``Reference allele``, ``Alternate allele`` in ``F-J``.

- For structural variants, you have to provide:

    - ``Chromosome``, ``Start``, ``Stop``, in ``F-H``.
    - Alternatively to ``Start``/``Stop``, you can provide ``Outer start`` ... ``Outer stop`` (``L-O``).
    - Provide the variant type in ``Variant Type`` / ``K``.

- ``Condition ID type`` / ``AB`` and ``Condition ID value`` / ``AC`` map to ``OMIM`` in TSV.
- ``Clinical significance`` / ``AH`` maps to ``CLIN_SIG`` in TSV.
- ``Date last evaluated`` / ``AJ`` maps to ``CLIN_EVAL`` in TSV.
- ``ClinVarAccession`` / ``CK`` maps to ``clinvar_accession`` in TSV.
- ``Mode of inheritance`` / ``AK`` maps to ``MOI`` in TSV.

You currently cannot use ClinVar Excel to update batches (of course you can provide clinvar accessions to trigger ClinVar record updates).
You will need to export to TSV and re-import from there.
