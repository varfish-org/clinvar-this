"""Helper code for normalizing variants.

Note: one core assumption is that the contig names in the FASTA file
are prefixed with "chr", and the PAR on "chrY" is not N-masked, and
"chrMT" is the RCRS and present in the FASTA.

You will have to manually append a "chrMT" to "hg19.fa" and "hg38.fa".
"""

import typing

from logzero import logger
import pydantic
import pysam

from clinvar_data.conversion import normalize
from clinvar_data.pbs import clinvar_public
from clinvar_data.pbs.clinvar_public_pb2 import (
    Allele,
    ClassifiedRecord,
    VariationArchive,
)

#: Mapping from ambiguous IUPAC nucleotide codes to the possible nucleotides
IUPAC_AMBIGUOUS = {
    "R": "AG",
    "Y": "CT",
    "S": "GC",
    "W": "AT",
    "K": "GT",
    "M": "AC",
    "B": "CGT",
    "D": "AGT",
    "H": "ACT",
    "V": "ACG",
}


def is_ambiguous(seq: str) -> bool:
    """Check if a sequence contains ambiguous IUPAC nucleotide codes."""
    return any(key in seq for key in IUPAC_AMBIGUOUS.keys())


def expand_ambiguous(seq: str) -> typing.Iterator[str]:
    """Expand ambiguous IUPAC nucleotide codes in a sequence."""
    any_found = False
    for code, nts in IUPAC_AMBIGUOUS.items():
        try:
            pos = seq.index(code)
            any_found = True
            for nt in nts:
                yield from expand_ambiguous("".join((seq[:pos], nt, seq[pos + 1 :])))
        except ValueError:
            pass  # swallow
    if not any_found:
        yield seq


#: Chromosomes for which we have sequence.
CHROMS_WITH_SEQ = list(map(str, range(1, 23))) + ["X", "Y", "MT"]


class VcfVariant(pydantic.BaseModel):
    """VCF variant."""

    #: Chromosome.
    chrom: str
    #: Position.
    pos: int
    #: Reference allele.
    ref: str
    #: Alternate allele.
    alt: str

    model_config = pydantic.ConfigDict(frozen=True)


class DnaNormalizer:
    """Normalize a variant based on chrom/pos/ref/alt for DNA characters."""

    def __init__(self, fasta_ref: str):
        #: FASTA reference file.
        self.fasta_ref = pysam.FastaFile(fasta_ref)

    def normalize(self, variant: VcfVariant) -> VcfVariant:
        try:
            chrom, pos, ref, alt = normalize.normalize(
                self.fasta_ref, variant.chrom, variant.pos, variant.ref, variant.alt
            )
            if ref != variant.ref or alt != variant.alt:
                logger.info(
                    "normalized %s %s %s %s to %s %s %s %s",
                    variant.chrom,
                    variant.pos,
                    variant.ref,
                    variant.alt,
                    chrom,
                    pos,
                    ref,
                    alt,
                )
            return VcfVariant(chrom=chrom, pos=pos, ref=ref, alt=alt)
        except (normalize.RefEqualsAltError, normalize.WrongRefError) as e:
            logger.info("Skipping normalization because of error (will write out though): %s", e)
            return variant


class AmbiguousDnaNormalizer:
    """Normalize a variant, expanding ambiguous IUPAC codes in alternate allele.

    This implies normalizing to a list of variants.
    """

    def __init__(self, fasta_ref: str):
        #: Internal normalizer.
        self.normalizer = DnaNormalizer(fasta_ref)

    def normalize(self, variant: VcfVariant) -> typing.List[VcfVariant]:
        if is_ambiguous(variant.alt):
            return [
                self.normalizer.normalize(variant.model_copy(update={"alt": alt}))
                for alt in expand_ambiguous(variant.alt)
            ]
        else:
            return [self.normalizer.normalize(variant)]


def vcf_variant_from_variant_archive(
    va: VariationArchive, assembly: typing.Literal["GRCh37", "GRCh38"]
) -> typing.Optional[VcfVariant]:
    """Extract ``VcfVariant`` from a ``VariationArchive`mak` (via sequence location)."""
    if not va.HasField("classified_record"):
        return None
    classified_record: ClassifiedRecord = va.classified_record
    if not classified_record.HasField("simple_allele"):
        return None
    simple_allele: Allele = classified_record.simple_allele
    for location in simple_allele.locations or []:
        for sequence_location in location.sequence_locations or []:
            if (
                sequence_location.assembly == assembly
                and sequence_location.HasField("reference_allele_vcf")
                and sequence_location.HasField("alternate_allele_vcf")
            ):
                chrom = clinvar_public.Chromosome.Name(sequence_location.chr)[len("CHROMOSOME_") :]
                if chrom in CHROMS_WITH_SEQ:
                    return VcfVariant(
                        chrom=f"chr{chrom}",
                        pos=sequence_location.position_vcf,
                        ref=sequence_location.reference_allele_vcf,
                        alt=sequence_location.alternate_allele_vcf,
                    )
    return None


def write_vcf_variant_to_va(
    va: VariationArchive, vcf_variant: VcfVariant, assembly: typing.Literal["GRCh37", "GRCh38"]
):
    """Write VCF variant coordinates to a ``VariationArchive``."""
    if not va.HasField("classified_record"):
        return None
    classified_record: ClassifiedRecord = va.classified_record
    if not classified_record.HasField("simple_allele"):
        return None
    simple_allele: Allele = classified_record.simple_allele
    for location in simple_allele.locations or []:
        for sequence_location in location.sequence_locations or []:
            if (
                sequence_location.assembly == assembly
                and sequence_location.HasField("reference_allele_vcf")
                and sequence_location.HasField("alternate_allele_vcf")
            ):
                sequence_location.position_vcf = vcf_variant.pos
                sequence_location.reference_allele_vcf = vcf_variant.ref
                sequence_location.alternate_allele_vcf = vcf_variant.alt


class MatchedVcfVariants(pydantic.BaseModel):
    """Stores pair of matched hg19/hg38 variants."""

    #: HG19 variant.
    hg19: typing.Optional[VcfVariant] = None
    #: HG38 variant.
    hg38: typing.Optional[VcfVariant] = None


class VariationArchiveNormalizer:
    """Normalize the VCF variant description within a ``VariationArchive``.

    This will normalize the variant for both the GRCh37 and GRCh38 assemblies.
    Note that this will also expand ambiguous IUPAC codes in the alternate allele,
    leading to duplicate records in terms of VCV but still unique in terms
    of VCF positions.
    """

    def __init__(
        self,
        fasta_ref_hg19: typing.Optional[str] = None,
        fasta_ref_hg38: typing.Optional[str] = None,
    ):
        #: Normalizer to use for GRCh37.
        self.normalizer_hg19 = AmbiguousDnaNormalizer(fasta_ref_hg19) if fasta_ref_hg19 else None
        #: Normalizer to use for GRCh38.
        self.normalizer_hg38 = AmbiguousDnaNormalizer(fasta_ref_hg38) if fasta_ref_hg38 else None

    def normalize(self, va: VariationArchive) -> typing.List[VariationArchive]:
        """Normalize the VCF variant in ``va``.

        The algorithm is as follows:

        1. extract VCF-style coordinates on both GRCh37 and GRCh38 from ``va``
        2. normalize them, expanding ambiguous IUPAC codes in the alternate allele
        3. match the resulting variants based on expanded non-IUPAC alt alleles
        4. for each matched pair, create a copy of the original ``va``, write
           the normalized VCF variant back to the copy
        """
        # extract
        vcf_hg19 = vcf_variant_from_variant_archive(va, "GRCh37")
        vcf_hg38 = vcf_variant_from_variant_archive(va, "GRCh38")
        if vcf_hg19 is None and vcf_hg38 is None:
            return [va]
        # normalize
        vcfs_hg19 = (
            self.normalizer_hg19.normalize(vcf_hg19)
            if self.normalizer_hg19 and vcf_hg19
            else ([vcf_hg19] if vcf_hg19 is not None else [])
        )
        vcfs_hg38 = (
            self.normalizer_hg38.normalize(vcf_hg38)
            if self.normalizer_hg38 and vcf_hg38
            else ([vcf_hg38] if vcf_hg38 is not None else [])
        )
        # short-circuit if nothing to normalize
        if vcfs_hg19 == [vcf_hg19] and vcfs_hg38 == [vcf_hg38]:
            return [va]
        # match
        matched_vcfs: dict[str, MatchedVcfVariants] = {}
        for vcf_variant in vcfs_hg19:
            matched_vcfs[vcf_variant.alt] = MatchedVcfVariants(hg19=vcf_variant)
        for vcf_variant in vcfs_hg38:
            if vcf_variant.alt in matched_vcfs:
                matched_vcfs[vcf_variant.alt].hg38 = vcf_variant
            else:
                matched_vcfs[vcf_variant.alt] = MatchedVcfVariants(hg38=vcf_variant)
        return [
            self._create_copy_with_variant(va, matched_vcf) for matched_vcf in matched_vcfs.values()
        ]

    def _create_copy_with_variant(
        self, va: VariationArchive, matched_vcf: MatchedVcfVariants
    ) -> VariationArchive:
        result = VariationArchive()
        result.MergeFrom(va)
        if matched_vcf.hg19:
            write_vcf_variant_to_va(result, matched_vcf.hg19, "GRCh37")
        if matched_vcf.hg38:
            write_vcf_variant_to_va(result, matched_vcf.hg38, "GRCh38")
        return result
