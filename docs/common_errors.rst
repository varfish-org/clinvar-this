.. _common_errors:

=============
Common Errors
=============

This section lists some errors that the ClinVar API commonly returns for data.

-------------------
Reference Mismatch
-------------------

Message
    The submitted reference allele (``<BASES>``) does not agree with the actual reference sequence (``<BASES>``)

Explanation
    There is a problem with the variant that you provided.

Resolution
    Fix the variant description to match the reference bases in the reference.

-------------------
Record is not Novel
-------------------

Message
    This record is submitted as novel but it should be submitted as an update, including the SCV accession, because your organization previously submitted ``<SCV>`` for the same variant and condition.

Explanation
    Your organisation has already submitted a record with this "name" and condition (OMIM code or ``"not provided"``).
    ClinVar generates a variant name from your genomic coordinates.
    Each organisation can only have one submission for the combination of the condition and variant.

Resolution
    You can either submit a revision of your interpretation, (or, e.g., extend the "observed in" information), or leave it as is.
    Revisions are coded by providing the ``ACCESSION`` header in the TSV file.

----------------------------------
Submission Names Cannot be Changed
----------------------------------

Message
    This update changes the description of the variant for ``<SCV>``, which is generally not allowed on a ClinVar record.
    Please check the description of the variant and correct if necessary.
    If you intend to change the description of the variant, please submit as a new record and delete this record.
    Contact clinvar@ncbi.nlm.nih.gov if you have questions.

Explanation
    Most likely, you try to update the coordinates of a variant with an existing SCV.
    ClinVar does not allow this.
    Rather, you should remove the old variant and create a new submission.

Resolution
    Remove the old variant and add a new variant instead.
    Note that ClinVar will store your "local variant ID".
    If you resubmit a new record, make sure that this is changed or cleared such that ClinVar does not link your new request to your old submission and thinks you want to change your variant coordinates.

-----------------------------------------------------------
Multiple Conditions have been submitted without explanation
-----------------------------------------------------------

Message
    You provided multiple diseases as the condition for the classification. If they
    represent related diseases along a spectrum, provide ``uncertain`` for
    multipleConditionExplanation. If they represent diseases that occur together in
    an individual with the variant (this case is rare), provide ``co-occurring`` for
    multipleConditionExplanation."

Explanation
    Multiple Condition IDs have been submitted for single variant. Check if this
    has been intentional. If multiple conditions are to be submitted, a reason
    needs to be included with the submission.

Resolution
    Explicitly add either ``Uncertain``, ``Co-occurring`` or ``Novel disease``
    to the list of ``CONDITIONS``.
