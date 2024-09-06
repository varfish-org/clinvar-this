#!/usr/bin/env python

"""
This script is a python implementation of the algorithm for variant
normalization described by Tan et al 2015:

Tan A, Abecasis GR, Kang HM. Unified representation of genetic variants.
Bioinformatics. 2015 Jul 1;31(13):2202-4. doi: 10.1093/bioinformatics/btv112.
Epub 2015 Feb 19. PubMed PMID: 25701572.

The authors have made a C++ implementation available in vt as vt normalize
And the source code is viewable here: https://github.com/atks/vt

For our purposes, we wanted a Python implementation so that we could
build end-to-end scripts in Python.

If you use this, please cite Tan et al 2015.

A note about when this is useful. In VCFs generated with GATK (or probably
other tools) from short read sequencing data, variants are already left-aligned
but may be non-minimal to the extent that indels overlap with other variants.
For those cases, minimal_representation.py is sufficient to convert variants
to minimal representation. However, genomic coordinates converted from HGVS
(we have encountered this when parsing the ClinVar XML dump) may be not only
non-minimal but also right-aligned rather than left-aligned, and may contain
hyphens. For those situations, use this script (or just run vt normalize).

Usage: normalize.py -R $b37ref < bad_file.txt > good_file.txt
"""


import typing

import pysam


class RefEqualsAltError(Exception):
    """
    An Error class for rare cases where REF == ALT (seen in ClinVar XML)
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class InvalidNucleotideSequenceError(Exception):
    """
    An Error class for REF or ALT values that are not valid nucleotide sequences
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class WrongRefError(Exception):
    """
    An Error class for variants where the REF does not match the reference genome
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


def normalize(
    pysam_fasta: pysam.FastaFile, chrom: str, pos: int, ref: str, alt: str
) -> typing.Tuple[str, int, str, str]:
    """
    Accepts a pysam FastaFile object pointing to the reference genome, and
    chrom, pos, ref, alt genomic coordinates, and normalizes them.
    """
    pos = int(pos)  # make sure position is an integer
    ref = ref.upper()
    alt = alt.upper()
    # Remove variants that contain invalid nucleotides
    if any(letter not in ["A", "C", "G", "T", "N", "-"] for letter in ref + alt):
        raise InvalidNucleotideSequenceError(
            "Invalid nucleotide sequence: %s %s %s %s" % (chrom, pos, ref, alt)
        )
    # use blanks instead of hyphens
    if ref == "-":
        ref = ""
    if alt == "-":
        alt = ""
    # check whether the REF is correct
    true_ref = pysam_fasta.fetch(chrom, pos - 1, pos - 1 + len(ref)).upper()
    if ref != true_ref:
        raise WrongRefError(
            "Incorrect REF value: %s %s %s %s (actual REF should be %s)"
            % (chrom, pos, ref, alt, true_ref)
        )
    # Prevent infinite loops in cases where REF == ALT.
    # We have encountered this error in genomic coordinates from the ClinVar XML file
    if ref == alt:
        raise RefEqualsAltError(
            "The REF and ALT allele are the same: %s %s %s %s" % (chrom, pos, ref, alt)
        )
    # Time-saving shortcut for SNPs that are already minimally represented
    if (
        len(ref) == 1
        and len(alt) == 1
        and ref in ["A", "C", "G", "T"]
        and alt in ["A", "C", "G", "T"]
    ):
        return chrom, pos, ref, alt
    # This first loop left-aligns and removes excess nucleotides on the right.
    # This is Algorithm 1 lines 1-6 from Tan et al 2015
    keep_working = True
    while keep_working:
        keep_working = False
        if len(ref) > 0 and len(alt) > 0 and ref[-1] == alt[-1]:
            ref = ref[:-1]
            alt = alt[:-1]
            keep_working = True
        if len(ref) == 0 or len(alt) == 0:
            preceding_base = pysam_fasta.fetch(chrom, pos - 2, pos - 1)
            ref = preceding_base + ref
            alt = preceding_base + alt
            pos = pos - 1
            keep_working = True
    # This second loop removes excess nucleotides on the left. This is Algorithm 1 lines 7-8.
    while len(ref) > 1 and len(alt) > 1 and ref[0] == alt[0]:
        ref = ref[1:]
        alt = alt[1:]
        pos = pos + 1
    return chrom, pos, ref, alt
