"""Code for converting dicts from ``xmltodict`` to Protocol Buffers"""

from dataclasses import dataclass
import time
from typing import Any, Dict

import dateutil.parser
import google.protobuf.timestamp_pb2

from clinvar_data.pbs.clinvar_public import (
    AggregateClassificationSet,
    AggregatedGermlineClassification,
    AggregatedOncogenicityClassification,
    AggregatedSomaticClinicalImpact,
    AggregateGermlineReviewStatus,
    AggregateOncogenicityReviewStatus,
    AggregateSomaticClinicalImpactReviewStatus,
    Allele,
    AlleleDescription,
    AlleleScv,
    Assertion,
    AttributeSetElement,
    BaseAttribute,
    Chromosome,
    Citation,
    ClassificationScv,
    ClassifiedCondition,
    ClinicalAssertion,
    ClinicalAssertionRecordHistory,
    ClinicalFeaturesAffectedStatusType,
    ClinicalSignificance,
    Comment,
    CommentType,
    Cooccurrence,
    DeletedScv,
    DescriptionHistory,
    DosageSensitivity,
    EvidenceType,
    FamilyData,
    FunctionalConsequence,
    GeneralCitations,
    GenericSetElement,
    GeneVariantRelationship,
    GenotypeScv,
    HaplotypeScv,
    HaploVariationType,
    HgvsExpression,
    HgvsNucleotideExpression,
    HgvsProteinExpression,
    HgvsType,
    Indication,
    Location,
    Method,
    MethodListType,
    NucleotideSequence,
    ObservedIn,
    Origin,
    OtherName,
    PhenotypeSetType,
    ProteinSequence,
    RecordHistory,
    Sample,
    Scv,
    Severity,
    Software,
    Species,
    Status,
    Submitter,
    SubmitterIdentifiers,
    SubmitterReviewStatus,
    Trait,
    TraitSet,
    VariationType,
    Xref,
    Zygosity,
)
from clinvar_data.pbs.clinvar_public_pb2 import (
    ClassifiedRecord,
    ClinvarVariationRelease,
    Genotype,
    Haplotype,
    IncludedRecord,
    RcvAccession,
    VariationArchive,
)


def ensure_str(value: str | dict[str, str]) -> str:
    """Ensure the value is a string and not a dict with an xlnsi."""
    if isinstance(value, dict):
        assert (
            "@xmlns:xsi" in value
            and value["@xmlns:xsi"] == "http://www.w3.org/2001/XMLSchema-instance"
        )
        return value["#text"]
    else:
        return value


class ConvertGeneVariantRelationship:
    """Static method helper for converting XML data to to ``GeneVariantRelationship``."""

    #: Conversion from XML value to Protocol Buffers.
    CONVERT: Dict[str, GeneVariantRelationship.ValueType] = {
        "variant within gene": GeneVariantRelationship.GENE_VARIANT_RELATIONSHIP_VARIANT_WITHIN_GENE,
        "gene overlapped by variant": GeneVariantRelationship.GENE_VARIANT_RELATIONSHIP_GENE_OVERLAPPED_BY_VARIANT,
        "genes overlapped by variant": GeneVariantRelationship.GENE_VARIANT_RELATIONSHIP_GENE_OVERLAPPED_BY_VARIANT,
        "variant near gene, upstream": GeneVariantRelationship.GENE_VARIANT_RELATIONSHIP_NEAR_GENE_UPSTREAM,
        "near gene, upstream": GeneVariantRelationship.GENE_VARIANT_RELATIONSHIP_NEAR_GENE_UPSTREAM,
        "variant near gene, downstream": GeneVariantRelationship.GENE_VARIANT_RELATIONSHIP_NEAR_GENE_DOWNSTREAM,
        "near gene, downstream": GeneVariantRelationship.GENE_VARIANT_RELATIONSHIP_NEAR_GENE_DOWNSTREAM,
        "asserted, but not computed": GeneVariantRelationship.GENE_VARIANT_RELATIONSHIP_ASSERTED_BUT_NOT_COMPUTED,
        "within multiple genes by overlap": GeneVariantRelationship.GENE_VARIANT_RELATIONSHIP_WITHIN_MULTIPLE_GENES_BY_OVERLAP,
        "within single gene": GeneVariantRelationship.GENE_VARIANT_RELATIONSHIP_WITHIN_SINGLE_GENE,
    }

    @classmethod
    def xmldict_data_to_pb(cls, value: str) -> GeneVariantRelationship.ValueType:
        """Converts a dict from ``xmltodict`` to a ``GeneVariantRelationship.ValueType`` protobuf.

        Args:
            value: The string from ``xmltodict``.

        Returns:
            The ``GeneVariantRelationship.ValueType`` protobuf.

        Raises:
            ValueError: If the value is not known.
        """
        result = cls.CONVERT.get(value)
        if not result:
            raise ValueError(f"Unknown value {value}")
        else:
            return result


class ConvertSeverity:
    """Static method helper for converting XML data to to ``Severity``."""

    #: Conversion from XML value to Protocol Buffers.
    CONVERT: Dict[str, Severity.ValueType] = {
        "mild": Severity.SEVERITY_MILD,
        "moderate": Severity.SEVERITY_MODERATE,
        "severe": Severity.SEVERITY_SEVERE,
    }

    @classmethod
    def xmldict_data_to_pb(cls, value: str) -> Severity.ValueType:
        """Converts a dict from ``xmltodict`` to a ``Severity.ValueType`` protobuf.

        Args:
            value: The string from ``xmltodict``.

        Returns:
            The ``Severity.ValueType`` protobuf.

        Raises:
            ValueError: If the value is not known.
        """
        result = cls.CONVERT.get(value)
        if not result:
            raise ValueError(f"Unknown value {value}")
        else:
            return result


class ConvertStatus:
    """Static method helper for converting XML data to to ``Status``."""

    CONVERT: Dict[str, Status.ValueType] = {
        "current": Status.STATUS_CURRENT,
        "completed and retired": Status.STATUS_COMPLETED_AND_RETIRED,
        "delete": Status.STATUS_DELETE,
        "in development": Status.STATUS_IN_DEVELOPMENT,
        "reclassified": Status.STATUS_RECLASSIFIED,
        "reject": Status.STATUS_REJECT,
        "secondary": Status.STATUS_SECONDARY,
        "suppressed": Status.STATUS_SUPPRESSED,
        "under review": Status.STATUS_UNDER_REVIEW,
    }

    @classmethod
    def xmldict_data_to_pb(cls, value: str) -> Status.ValueType:
        """Converts a dict from ``xmltodict`` to a ``Status.ValueType`` protobuf.

        Args:
            value: The string from ``xmltodict``.

        Returns:
            The ``Status.ValueType`` protobuf.

        Raises:
            ValueError: If the value is not known.
        """
        result = cls.CONVERT.get(value)
        if not result:
            raise ValueError(f"Unknown value {value}")
        else:
            return result


class ConvertSubmitterReviewStatus:
    """Static method helper for converting XML data to `SubmitterReviewStatus`."""

    CONVERT: Dict[str, SubmitterReviewStatus.ValueType] = {
        "no classification provided": SubmitterReviewStatus.SUBMITTER_REVIEW_STATUS_NO_CLASSIFICATION_PROVIDED,
        "no assertion criteria provided": SubmitterReviewStatus.SUBMITTER_REVIEW_STATUS_NO_ASSERTION_CRITERIA_PROVIDED,
        "criteria provided, single submitter": SubmitterReviewStatus.SUBMITTER_REVIEW_STATUS_CRITERIA_PROVIDED_SINGLE_SUBMITTER,
        "reviewed by expert panel": SubmitterReviewStatus.SUBMITTER_REVIEW_STATUS_REVIEWED_BY_EXPERT_PANEL,
        "practice guideline": SubmitterReviewStatus.SUBMITTER_REVIEW_STATUS_PRACTICE_GUIDELINE,
        "flagged submission": SubmitterReviewStatus.SUBMITTER_REVIEW_STATUS_FLAGGED_SUBMISSION,
        "criteria provided, multiple submitters, no conflicts": SubmitterReviewStatus.SUBMITTER_REVIEW_STATUS_CRITERIA_PROVIDED_MULTIPLE_SUBMITTERS_NO_CONFLICTS,
        "criteria provided, conflicting classifications": SubmitterReviewStatus.SUBMITTER_REVIEW_STATUS_CRITERIA_PROVIDED_CONFLICTING_CLASSIFICATIONS,
        "classified by single submitter": SubmitterReviewStatus.SUBMITTER_REVIEW_STATUS_CLASSIFIED_BY_SINGLE_SUBMITTER,
        "reviewed by professional society": SubmitterReviewStatus.SUBMITTER_REVIEW_STATUS_REVIEWED_BY_PROFESSIONAL_SOCIETY,
        "not classified by submitter": SubmitterReviewStatus.SUBMITTER_REVIEW_STATUS_NOT_CLASSIFIED_BY_SUBMITTER,
        "classified by multiple submitters": SubmitterReviewStatus.SUBMITTER_REVIEW_STATUS_CLASSIFIED_BY_MULTIPLE_SUBMITTERS,
    }

    @classmethod
    def xmldict_data_to_pb(cls, value: str) -> SubmitterReviewStatus.ValueType:
        """Converts a dict from `xmltodict` to a `SubmitterReviewStatus.ValueType` protobuf.

        Args:
            value: The string from `xmltodict`.

        Returns:
            The `SubmitterReviewStatus.ValueType` protobuf.

        Raises:
            ValueError: If the value is not known.
        """
        result = cls.CONVERT.get(value)
        if result is None:
            raise ValueError(f"Unknown value {value}")
        else:
            return result


class ConvertZygosity:
    """Static method helper for converting XML data to `Zygosity`."""

    CONVERT: Dict[str, Zygosity.ValueType] = {
        "Homozygote": Zygosity.ZYGOSITY_HOMOZYGOTE,
        "SingleHeterozygote": Zygosity.ZYGOSITY_SINGLE_HETEROZYGOTE,
        "CompoundHeterozygote": Zygosity.ZYGOSITY_COMPOUND_HETEROZYGOTE,
        "Hemizygote": Zygosity.ZYGOSITY_HEMIZYGOTE,
        "not provided": Zygosity.ZYGOSITY_NOT_PROVIDED,
    }

    @classmethod
    def xmldict_data_to_pb(cls, value: str) -> Zygosity.ValueType:
        """Converts a dict from `xmltodict` to a `Zygosity.ValueType` protobuf.

        Args:
            value: The string from `xmltodict`.

        Returns:
            The `Zygosity.ValueType` protobuf.

        Raises:
            ValueError: If the value is not known.
        """
        result = cls.CONVERT.get(value)
        if result is None:
            raise ValueError(f"Unknown value {value}")
        else:
            return result


class ConvertAssertion:
    """Static method helper for converting XML data to `Assertion`."""

    CONVERT: Dict[str, Assertion.ValueType] = {
        "variation to disease": Assertion.ASSERTION_VARIATION_TO_DISEASE,
        "variation to included disease": Assertion.ASSERTION_VARIATION_TO_INCLUDED_DISEASE,
        "variation in modifier gene to disease": Assertion.ASSERTION_VARIATION_IN_MODIFIER_GENE_TO_DISEASE,
        "confers sensitivity": Assertion.ASSERTION_CONFERS_SENSITIVITY,
        "confers resistance": Assertion.ASSERTION_CONFERS_RESISTANCE,
        "variant to named protein": Assertion.ASSERTION_VARIANT_TO_NAMED_PROTEIN,
    }

    @classmethod
    def xmldict_data_to_pb(cls, value: str) -> Assertion.ValueType:
        """Converts a dict from `xmltodict` to a `Assertion.ValueType` protobuf.

        Args:
            value: The string from `xmltodict`.

        Returns:
            The `Assertion.ValueType` protobuf.

        Raises:
            ValueError: If the value is not known.
        """
        result = cls.CONVERT.get(value)
        if result is None:
            raise ValueError(f"Unknown value {value}")
        else:
            return result


class ConvertAggregateGermlineReviewStatus:
    """Static method helper for converting XML data to `AggregateGermlineReviewStatus`."""

    CONVERT: Dict[str, AggregateGermlineReviewStatus.ValueType] = {
        "no classification provided": AggregateGermlineReviewStatus.AGGREGATE_GERMLINE_REVIEW_STATUS_NO_CLASSIFICATION_PROVIDED,
        "no assertion criteria provided": AggregateGermlineReviewStatus.AGGREGATE_GERMLINE_REVIEW_STATUS_NO_ASSERTION_CRITERIA_PROVIDED,
        "criteria provided, single submitter": AggregateGermlineReviewStatus.AGGREGATE_GERMLINE_REVIEW_STATUS_CRITERIA_PROVIDED_SINGLE_SUBMITTER,
        "criteria provided, multiple submitters, no conflicts": AggregateGermlineReviewStatus.AGGREGATE_GERMLINE_REVIEW_STATUS_CRITERIA_PROVIDED_MULTIPLE_SUBMITTERS_NO_CONFLICTS,
        "criteria provided, conflicting classifications": AggregateGermlineReviewStatus.AGGREGATE_GERMLINE_REVIEW_STATUS_CRITERIA_PROVIDED_CONFLICTING_CLASSIFICATIONS,
        "reviewed by expert panel": AggregateGermlineReviewStatus.AGGREGATE_GERMLINE_REVIEW_STATUS_REVIEWED_BY_EXPERT_PANEL,
        "practice guideline": AggregateGermlineReviewStatus.AGGREGATE_GERMLINE_REVIEW_STATUS_PRACTICE_GUIDELINE,
        "no classifications from unflagged records": AggregateGermlineReviewStatus.AGGREGATE_GERMLINE_REVIEW_STATUS_NO_CLASSIFICATIONS_FROM_UNFLAGGED_RECORDS,
        "no classification for the single variant": AggregateGermlineReviewStatus.AGGREGATE_GERMLINE_REVIEW_STATUS_NO_CLASSIFICATION_FOR_THE_SINGLE_VARIANT,
    }

    @classmethod
    def xmldict_data_to_pb(cls, value: str) -> AggregateGermlineReviewStatus.ValueType:
        """Converts a dict from `xmltodict` to a `AggregateGermlineReviewStatus.ValueType` protobuf.

        Args:
            value: The string from `xmltodict`.

        Returns:
            The `AggregateGermlineReviewStatus.ValueType` protobuf.

        Raises:
            ValueError: If the value is not known.
        """
        result = cls.CONVERT.get(value)
        if result is None:
            raise ValueError(f"Unknown value {value}")
        else:
            return result


class ConvertAggregateSomaticClinicalImpactReviewStatus:
    """Static method helper for converting XML data to `AggregateSomaticClinicalImpactReviewStatus`."""

    CONVERT: Dict[str, AggregateSomaticClinicalImpactReviewStatus.ValueType] = {
        "no classification provided": AggregateSomaticClinicalImpactReviewStatus.AGGREGATE_SOMATIC_CLINICAL_IMPACT_REVIEW_STATUS_NO_CLASSIFICATION_PROVIDED,
        "no assertion criteria provided": AggregateSomaticClinicalImpactReviewStatus.AGGREGATE_SOMATIC_CLINICAL_IMPACT_REVIEW_STATUS_NO_ASSERTION_CRITERIA_PROVIDED,
        "criteria provided, single submitter": AggregateSomaticClinicalImpactReviewStatus.AGGREGATE_SOMATIC_CLINICAL_IMPACT_REVIEW_STATUS_CRITERIA_PROVIDED_SINGLE_SUBMITTER,
        "criteria provided, multiple submitters": AggregateSomaticClinicalImpactReviewStatus.AGGREGATE_SOMATIC_CLINICAL_IMPACT_REVIEW_STATUS_CRITERIA_PROVIDED_MULTIPLE_SUBMITTERS,
        "reviewed by expert panel": AggregateSomaticClinicalImpactReviewStatus.AGGREGATE_SOMATIC_CLINICAL_IMPACT_REVIEW_STATUS_REVIEWED_BY_EXPERT_PANEL,
        "practice guideline": AggregateSomaticClinicalImpactReviewStatus.AGGREGATE_SOMATIC_CLINICAL_IMPACT_REVIEW_STATUS_PRACTICE_GUIDELINE,
        "no classifications from unflagged records": AggregateSomaticClinicalImpactReviewStatus.AGGREGATE_SOMATIC_CLINICAL_IMPACT_REVIEW_STATUS_NO_CLASSIFICATIONS_FROM_UNFLAGGED_RECORDS,
        "no classification for the single variant": AggregateSomaticClinicalImpactReviewStatus.AGGREGATE_SOMATIC_CLINICAL_IMPACT_REVIEW_STATUS_NO_CLASSIFICATION_FOR_THE_SINGLE_VARIANT,
    }

    @classmethod
    def xmldict_data_to_pb(cls, value: str) -> AggregateSomaticClinicalImpactReviewStatus.ValueType:
        """Converts a dict from `xmltodict` to a `AggregateSomaticClinicalImpactReviewStatus.ValueType` protobuf.

        Args:
            value: The string from `xmltodict`.

        Returns:
            The `AggregateSomaticClinicalImpactReviewStatus.ValueType` protobuf.

        Raises:
            ValueError: If the value is not known.
        """
        result = cls.CONVERT.get(value)
        if result is None:
            raise ValueError(f"Unknown value {value}")
        else:
            return result


class ConvertAggregateOncogenicityReviewStatus:
    """Static method helper for converting XML data to to ``AggregateOncogenicityReviewStatus``."""

    CONVERT: Dict[str, AggregateOncogenicityReviewStatus.ValueType] = {
        "no classification provided": AggregateOncogenicityReviewStatus.AGGREGATE_ONCOGENICITY_REVIEW_STATUS_NO_CLASSIFICATION_PROVIDED,
        "no assertion criteria provided": AggregateOncogenicityReviewStatus.AGGREGATE_ONCOGENICITY_REVIEW_STATUS_NO_ASSERTION_CRITERIA_PROVIDED,
        "criteria provided, single submitter": AggregateOncogenicityReviewStatus.AGGREGATE_ONCOGENICITY_REVIEW_STATUS_CRITERIA_PROVIDED_SINGLE_SUBMITTER,
        "criteria provided, multiple submitters, no conflicts": AggregateOncogenicityReviewStatus.AGGREGATE_ONCOGENICITY_REVIEW_STATUS_CRITERIA_PROVIDED_MULTIPLE_SUBMITTERS_NO_CONFLICTS,
        "criteria provided, conflicting classifications": AggregateOncogenicityReviewStatus.AGGREGATE_ONCOGENICITY_REVIEW_STATUS_CRITERIA_PROVIDED_CONFLICTING_CLASSIFICATIONS,
        "reviewed by expert panel": AggregateOncogenicityReviewStatus.AGGREGATE_ONCOGENICITY_REVIEW_STATUS_REVIEWED_BY_EXPERT_PANEL,
        "practice guideline": AggregateOncogenicityReviewStatus.AGGREGATE_ONCOGENICITY_REVIEW_STATUS_PRACTICE_GUIDELINE,
        "no classifications from unflagged records": AggregateOncogenicityReviewStatus.AGGREGATE_ONCOGENICITY_REVIEW_STATUS_NO_CLASSIFICATIONS_FROM_UNFLAGGED_RECORDS,
        "no classification for the single variant": AggregateOncogenicityReviewStatus.AGGREGATE_ONCOGENICITY_REVIEW_STATUS_NO_CLASSIFICATION_FOR_THE_SINGLE_VARIANT,
    }

    @classmethod
    def xmldict_data_to_pb(cls, value: str) -> AggregateOncogenicityReviewStatus.ValueType:
        """Converts a dict from ``xmltodict`` to a ``AggregateOncogenicityReviewStatus.ValueType`` protobuf.

        Args:
            value: The string from ``xmltodict``.

        Returns:
            The ``AggregateOncogenicityReviewStatus.ValueType`` protobuf.

        Raises:
            ValueError: If the value is not known.
        """
        result = cls.CONVERT.get(value)
        if not result:
            raise ValueError(f"Unknown value {value}")
        else:
            return result


class ConvertOrigin:
    """Static method helper for converting XML data to to ``Origin``."""

    CONVERT: Dict[str, Origin.ValueType] = {
        "germline": Origin.ORIGIN_GERMLINE,
        "somatic": Origin.ORIGIN_SOMATIC,
        "de novo": Origin.ORIGIN_DE_NOVO,
        "not provided": Origin.ORIGIN_NOT_PROVIDED,
        "inherited": Origin.ORIGIN_INHERITED,
        "maternal": Origin.ORIGIN_MATERNAL,
        "paternal": Origin.ORIGIN_PATERNAL,
        "uniparental": Origin.ORIGIN_UNIPARENTAL,
        "biparental": Origin.ORIGIN_BIPARENTAL,
        "not-reported": Origin.ORIGIN_NOT_REPORTED,
        "tested-inconclusive": Origin.ORIGIN_TESTED_INCONCLUSIVE,
        "unknown": Origin.ORIGIN_UNKNOWN,
        "not applicable": Origin.ORIGIN_NOT_APPLICABLE,
        "experimentally generated": Origin.ORIGIN_EXPERIMENTALLY_GENERATED,
    }

    @classmethod
    def xmldict_data_to_pb(cls, value: str) -> Origin.ValueType:
        """Converts a dict from ``xmltodict`` to a ``Origin.ValueType`` protobuf.

        Args:
            value: The string from ``xmltodict``.

        Returns:
            The ``Origin.ValueType`` protobuf.

        Raises:
            ValueError: If the value is not known.
        """
        result = cls.CONVERT.get(value)
        if not result:
            raise ValueError(f"Unknown value {value}")
        else:
            return result


class ConvertNucleotideSequence:
    """Static method helper for converting XML data to `NucleotideSequence`."""

    CONVERT: Dict[str, NucleotideSequence.ValueType] = {
        "genomic, top-level": NucleotideSequence.NUCLEOTIDE_SEQUENCE_GENOMIC_TOP_LEVEL,
        "genomic, RefSeqGene": NucleotideSequence.NUCLEOTIDE_SEQUENCE_GENOMIC_REF_SEQ_GENE,
        "genomic": NucleotideSequence.NUCLEOTIDE_SEQUENCE_GENOMIC,
        "coding": NucleotideSequence.NUCLEOTIDE_SEQUENCE_CODING,
        "non-coding": NucleotideSequence.NUCLEOTIDE_SEQUENCE_NON_CODING,
        "protein": NucleotideSequence.NUCLEOTIDE_SEQUENCE_PROTEIN,
    }

    @classmethod
    def xmldict_data_to_pb(cls, value: str) -> NucleotideSequence.ValueType:
        """Converts a dict from `xmltodict` to a `NucleotideSequence.ValueType` protobuf.

        Args:
            value: The string from `xmltodict`.

        Returns:
            The `NucleotideSequence.ValueType` protobuf.

        Raises:
            ValueError: If the value is not known.
        """
        result = cls.CONVERT.get(value)
        if result is None:
            raise ValueError(f"Unknown value {value}")
        else:
            return result


class ConvertProteinSequence:
    """Static method helper for converting XML data to `ProteinSequence`."""

    CONVERT: Dict[str, ProteinSequence.ValueType] = {
        "protein": ProteinSequence.PROTEIN_SEQUENCE_PROTEIN,
    }

    @classmethod
    def xmldict_data_to_pb(cls, value: str) -> ProteinSequence.ValueType:
        """Converts a dict from `xmltodict` to a `ProteinSequence.ValueType` protobuf.

        Args:
            value: The string from `xmltodict`.

        Returns:
            The `ProteinSequence.ValueType` protobuf.

        Raises:
            ValueError: If the value is not known.
        """
        result = cls.CONVERT.get(value)
        if result is None:
            raise ValueError(f"Unknown value {value}")
        else:
            return result


class ConvertPhenotypeSetType:
    """Static method helper for converting XML data to `PhenotypeSetType`."""

    CONVERT: Dict[str, PhenotypeSetType.ValueType] = {
        "Disease": PhenotypeSetType.PHENOTYPE_SET_TYPE_DISEASE,
        "DrugResponse": PhenotypeSetType.PHENOTYPE_SET_TYPE_DRUG_RESPONSE,
        "Finding": PhenotypeSetType.PHENOTYPE_SET_TYPE_FINDING,
        "PhenotypeInstruction": PhenotypeSetType.PHENOTYPE_SET_TYPE_PHENOTYPE_INSTRUCTION,
        "TraitChoice": PhenotypeSetType.PHENOTYPE_SET_TYPE_TRAIT_CHOICE,
    }

    @classmethod
    def xmldict_data_to_pb(cls, value: str) -> PhenotypeSetType.ValueType:
        """Converts a dict from `xmltodict` to a `PhenotypeSetType.ValueType` protobuf.

        Args:
            value: The string from `xmltodict`.

        Returns:
            The `PhenotypeSetType.ValueType` protobuf.

        Raises:
            ValueError: If the value is not known.
        """
        result = cls.CONVERT.get(value)
        if result is None:
            raise ValueError(f"Unknown value {value}")
        else:
            return result


class ConvertChromosome:
    """Static method helper for converting XML data to to ``Chromosome``."""

    CONVERT: Dict[str, Chromosome.ValueType] = {
        str(i): getattr(Chromosome, f"CHROMOSOME_{i}") for i in range(1, 23)
    }
    CONVERT.update(
        {
            "X": Chromosome.CHROMOSOME_X,
            "Y": Chromosome.CHROMOSOME_Y,
            "MT": Chromosome.CHROMOSOME_MT,
            "PAR": Chromosome.CHROMOSOME_PAR,
            "Un": Chromosome.CHROMOSOME_UN,
        }
    )

    @classmethod
    def xmldict_data_to_pb(cls, value: str) -> Chromosome.ValueType:
        """Converts a dict from ``xmltodict`` to a ``Chromosome.ValueType`` protobuf.

        Args:
            value: The string from ``xmltodict``.

        Returns:
            The ``Chromosome.ValueType`` protobuf.

        Raises:
            ValueError: If the value is not known.
        """
        result = cls.CONVERT.get(value)
        if not result:
            raise ValueError(f"Unknown value {value}")
        else:
            return result


class ConvertCommentType:
    """Static method helper for converting XML data to to ``CommentType``."""

    CONVERT: Dict[str, CommentType.ValueType] = {
        "public": CommentType.COMMENT_TYPE_PUBLIC,
        "ConvertedByNCBI": CommentType.COMMENT_TYPE_CONVERTED_BY_NCB,
        "MissingFromAssembly": CommentType.COMMENT_TYPE_MISSING_FROM_ASSEMBLY,
        "GenomicLocationNotEstablished": CommentType.COMMENT_TYPE_GENOMIC_LOCATION_NOT_ESTABLISHED,
        "LocationOnGenomeAndProductNotAligned": CommentType.COMMENT_TYPE_LOCATION_ON_GENOME_AND_PRODUCT_NOT_ALIGNED,
        "DeletionComment": CommentType.COMMENT_TYPE_DELETION_COMMENT,
        "MergeComment": CommentType.COMMENT_TYPE_MERGE_COMMENT,
        "AssemblySpecificAlleleDefinition": CommentType.COMMENT_TYPE_ASSEMBLY_SPECIFIC_ALLELE_DEFINITION,
        "AlignmentGapMakesAppearInconsistent": CommentType.COMMENT_TYPE_ALIGNMENT_GAP_MAKES_APPEAR_INCONSISTENT,
        "ExplanationOfClassification": CommentType.COMMENT_TYPE_EXPLANATION_OF_CLASSIFICATION,
        "FlaggedComment": CommentType.COMMENT_TYPE_FLAGGED_COMMENT,
    }

    @classmethod
    def xmldict_data_to_pb(cls, value: str) -> CommentType.ValueType:
        """Converts a dict from ``xmltodict`` to a ``CommentType.ValueType`` protobuf.

        Args:
            value: The string from ``xmltodict``.

        Returns:
            The ``CommentType.ValueType`` protobuf.

        Raises:
            ValueError: If the value is not known.
        """
        result = cls.CONVERT.get(value)
        if not result:
            raise ValueError(f"Unknown value {value}")
        else:
            return result


class ConvertVariationType:
    """Static method helper for converting XML data to `VariationType`."""

    CONVERT: Dict[str, VariationType.ValueType] = {
        "Diplotype": VariationType.VARIATION_TYPE_DIPLOTYPE,
        "CompoundHeterozygote": VariationType.VARIATION_TYPE_COMPOUND_HETEROZYGOTE,
        "Distinct chromosomes": VariationType.VARIATION_TYPE_DISTINCT_CHROMOSOMES,
    }

    @classmethod
    def xmldict_data_to_pb(cls, value: str) -> VariationType.ValueType:
        """Converts a dict from `xmltodict` to a `VariationType.ValueType` protobuf.

        Args:
            value: The string from `xmltodict`.

        Returns:
            The `VariationType.ValueType` protobuf.

        Raises:
            ValueError: If the value is not known.
        """
        result = cls.CONVERT.get(value)
        if result is None:
            raise ValueError(f"Unknown value {value}")
        else:
            return result


class ConvertEvidenceType:
    """Static method helper for converting XML data to `EvidenceType`."""

    CONVERT: Dict[str, EvidenceType.ValueType] = {
        "Genetic": EvidenceType.EVIDENCE_TYPE_GENETIC,
        "Experimental": EvidenceType.EVIDENCE_TYPE_EXPERIMENTAL,
        "Population": EvidenceType.EVIDENCE_TYPE_POPULATION,
        "Computational": EvidenceType.EVIDENCE_TYPE_COMPUTATIONAL,
    }

    @classmethod
    def xmldict_data_to_pb(cls, value: str) -> EvidenceType.ValueType:
        """Converts a dict from `xmltodict` to a `EvidenceType.ValueType` protobuf.

        Args:
            value: The string from `xmltodict`.

        Returns:
            The `EvidenceType.ValueType` protobuf.

        Raises:
            ValueError: If the value is not known.
        """
        result = cls.CONVERT.get(value)
        if result is None:
            raise ValueError(f"Unknown value {value}")
        else:
            return result


class ConvertMethodListType:
    """Static method helper for converting XML data to `MethodListType`."""

    CONVERT: Dict[str, MethodListType.ValueType] = {
        "literature only": MethodListType.METHOD_LIST_TYPE_LITERATURE_ONLY,
        "reference population": MethodListType.METHOD_LIST_TYPE_REFERENCE_POPULATION,
        "case-control": MethodListType.METHOD_LIST_TYPE_CASE_CONTROL,
        "clinical testing": MethodListType.METHOD_LIST_TYPE_CLINICAL_TESTING,
        "in vitro": MethodListType.METHOD_LIST_TYPE_IN_VITRO,
        "in vivo": MethodListType.METHOD_LIST_TYPE_IN_VIVO,
        "research": MethodListType.METHOD_LIST_TYPE_RESEARCH,
        "curation": MethodListType.METHOD_LIST_TYPE_CURATION,
        "not provided": MethodListType.METHOD_LIST_TYPE_NOT_PROVIDED,
        "provider interpretation": MethodListType.METHOD_LIST_TYPE_PROVIDER_INTERPRETATION,
        "phenotyping only": MethodListType.METHOD_LIST_TYPE_PHENOTYPING_ONLY,
    }

    @classmethod
    def xmldict_data_to_pb(cls, value: str) -> MethodListType.ValueType:
        """Converts a dict from `xmltodict` to a `MethodListType.ValueType` protobuf.

        Args:
            value: The string from `xmltodict`.

        Returns:
            The `MethodListType.ValueType` protobuf.

        Raises:
            ValueError: If the value is not known.
        """
        result = cls.CONVERT.get(value)
        if result is None:
            raise ValueError(f"Unknown value {value}")
        else:
            return result


class ConvertHgvsType:
    """Static method helper for converting XML data to to ``HgvsType``."""

    CONVERT: Dict[str, HgvsType.ValueType] = {
        "coding": HgvsType.HGVS_TYPE_CODING,
        "genomic": HgvsType.HGVS_TYPE_GENOMIC,
        "genomic, top-level": HgvsType.HGVS_TYPE_GENOMIC_TOP_LEVEL,
        "non-coding": HgvsType.HGVS_TYPE_NON_CODING,
        "protein": HgvsType.HGVS_TYPE_PROTEIN,
    }

    @classmethod
    def xmldict_data_to_pb(cls, value: str) -> HgvsType.ValueType:
        """Converts a dict from ``xmltodict`` to a ``HgvsType.ValueType`` protobuf.

        Args:
            value: The string from ``xmltodict``.

        Returns:
            The ``HgvsType.ValueType`` protobuf.

        Raises:
            ValueError: If the value is not known.
        """
        result = cls.CONVERT.get(value)
        if not result:
            raise ValueError(f"Unknown value {value}")
        else:
            return result


class ConvertClinicalFeaturesAffectedStatusType:
    """Static method helper for converting XML data to to ``ClinicalFeaturesAffectedStatusType``."""

    CONVERT: Dict[str, ClinicalFeaturesAffectedStatusType.ValueType] = {
        "present": ClinicalFeaturesAffectedStatusType.CLINICAL_FEATURES_AFFECTED_STATUS_TYPE_PRESENT,
        "absent": ClinicalFeaturesAffectedStatusType.CLINICAL_FEATURES_AFFECTED_STATUS_TYPE_ABSENT,
        "not tested": ClinicalFeaturesAffectedStatusType.CLINICAL_FEATURES_AFFECTED_STATUS_TYPE_NOT_TESTED,
    }

    @classmethod
    def xmldict_data_to_pb(cls, value: str) -> ClinicalFeaturesAffectedStatusType.ValueType:
        """Converts a dict from ``xmltodict`` to a ``ClinicalFeaturesAffectedStatusType.ValueType`` protobuf.

        Args:
            value: The string from ``xmltodict``.

        Returns:
            The ``ClinicalFeaturesAffectedStatusType.ValueType`` protobuf.

        Raises:
            ValueError: If the value is not known.
        """
        result = cls.CONVERT.get(value)
        if not result:
            raise ValueError(f"Unknown value {value}")
        else:
            return result


class ConvertHaploVariationType:
    """Static method helper for converting XML data to to ``HaploVariationType``."""

    CONVERT: Dict[str, HaploVariationType.ValueType] = {
        "Haplotype": HaploVariationType.HAPLO_VARIATION_TYPE_HAPLOTYPE,
        "Haplotype, single variant": HaploVariationType.HAPLO_VARIATION_TYPE_HAPLOTYPE_SINGLE_VARIANT,
        "Variation": HaploVariationType.HAPLO_VARIATION_TYPE_VARIATION,
        "Phase unknown": HaploVariationType.HAPLO_VARIATION_TYPE_PHASE_UNKNOWN,
        "Haplotype defined by a single variant": HaploVariationType.HAPLO_VARIATION_TYPE_HAPLOTYPE_DEFINED_BY_SINGLE_VARIANT,
    }

    @classmethod
    def xmldict_data_to_pb(cls, value: str) -> HaploVariationType.ValueType:
        """Converts a dict from ``xmltodict`` to a ``HaploVariationType.ValueType`` protobuf.

        Args:
            value: The string from ``xmltodict``.

        Returns:
            The ``HaploVariationType.ValueType`` protobuf.

        Raises:
            ValueError: If the value is not known.
        """
        result = cls.CONVERT.get(value)
        if not result:
            raise ValueError(f"Unknown value {value}")
        else:
            return result


@dataclass(kw_only=True)
class CitationsXrefsComments:
    """Bundle of citations, xrefs, and comments."""

    #: Optional list of citations.
    citations: list[Citation] | None
    #: Optional list of xrefs.
    xrefs: list[Xref] | None
    #: Optional list of comments.
    comments: list[Comment] | None


class ConverterBase:
    """Base class for static helper class."""

    @staticmethod
    def ensure_list(value: Any) -> list[Any]:
        """Ensures that the given value is a list.

        Args:
            value: The value to check.

        Returns:
            The list.

        Raises:
            ValueError: If the value is not a list.
        """
        if isinstance(value, list):
            return value
        else:
            return [value]

    @classmethod
    def parse_citations_xrefs_comments(cls, value: dict[str, Any]) -> CitationsXrefsComments:
        """Parse out common Citation, XRef, Comment lists from tag."""

        # parse out citations
        citations: list[Citation] | None = None
        if "Citation" not in value:
            pass
        elif isinstance(value["Citation"], list):
            citations = [
                ConvertCitation.xmldict_data_to_pb({"Citation": entry})
                for entry in value["Citation"]
            ]
        elif isinstance(value["Citation"], dict):
            citations = [ConvertCitation.xmldict_data_to_pb({"Citation": value["Citation"]})]
        else:
            assert False, f"Invalid type for Citation {value['Citation']}"
        # parse out xrefs
        xrefs: list[Xref] | None = None
        if "XRef" not in value:
            pass
        elif isinstance(value["XRef"], list):
            xrefs = [ConvertXref.xmldict_data_to_pb({"XRef": entry}) for entry in value["XRef"]]
        elif isinstance(value["XRef"], dict):
            xrefs = [ConvertXref.xmldict_data_to_pb({"XRef": value["XRef"]})]
        else:
            assert False, f"Invalid type for XRef {value['XRef']}"
        # parse out comments
        comments: list[Comment] | None = None
        if "Comment" not in value:
            pass
        elif isinstance(value["Comment"], list):
            comments = [
                ConvertComment.xmldict_data_to_pb({"Comment": entry}) for entry in value["Comment"]
            ]
        elif isinstance(value["Comment"], (str, dict)):
            comments = [ConvertComment.xmldict_data_to_pb({"Comment": value["Comment"]})]
        else:
            assert False, f"Invalid type for comment {value['Comment']}"

        return CitationsXrefsComments(citations=citations, xrefs=xrefs, comments=comments)

    @classmethod
    def assert_keys(cls, value: dict[str, Any], keys: list[str]) -> None:
        """Asserts that the given keys are in the dict.

        Args:
            value: The dict to check.
            keys: The keys to check.

        Raises:
            ValueError: If an attribute is missing.
        """
        for key in keys:
            if key not in value:
                raise ValueError(f"Missing key {key} in {value}")

    @classmethod
    def assert_not_keys(cls, value: dict[str, Any], keys: list[str]) -> None:
        """Asserts that the given keys are not in the dict.

        Args:
            value: The dict to check.
            keys: The keys to check.

        Raises:
            ValueError: If an attribute is missing.
        """
        for key in keys:
            if key in value:
                raise ValueError(f"Forbidden key {key} in {value}")


class ConvertComment(ConverterBase):
    """Static method helper for converting XML data to to ``Comment``."""

    @classmethod
    def xmldict_data_to_pb(cls, value: dict[str, Any]) -> Comment:
        """Converts a dict from ``xmltodict`` to a ``Comment`` protobuf.

        Args:
            value: The dict from ``xmltodict``.

        Returns:
            The ``Comment`` protobuf.
        """
        assert "Comment" in value
        if isinstance(value["Comment"], str):
            return Comment(value=value["Comment"])
        else:
            tag_comment: dict[str, str] = value["Comment"]
            cls.assert_keys(tag_comment, ["#text"])
            return Comment(
                value=tag_comment["#text"],
                data_source=tag_comment.get("@DataSource"),
                type=ConvertCommentType.xmldict_data_to_pb(tag_comment["@Type"]),
            )


class ConvertXref(ConverterBase):
    """Static method helper for conerting XML data to ``Xref``."""

    @classmethod
    def xmldict_data_to_pb(cls, value: dict[str, Any]) -> Xref:
        """Converts a dict from ``xmltodict`` to a ``Xref`` protobuf.

        Args:
            value: The dict from ``xmltodict``.

        Returns:
            The ``Xref`` protobuf.
        """
        assert "XRef" in value
        assert isinstance(value["XRef"], dict)
        tag_xref: dict[str, str] = value["XRef"]
        cls.assert_keys(tag_xref, ["@ID", "@DB"])
        if "@Status" in tag_xref:
            status = ConvertStatus.xmldict_data_to_pb(tag_xref["@Status"])
        else:
            status = None
        return Xref(
            db=tag_xref["@DB"],
            id=tag_xref["@ID"],
            type=tag_xref.get("@Type"),
            url=tag_xref.get("@URL"),
            status=status,
        )


class ConvertCitation(ConverterBase):
    """Static method helper for converting XML data to to ``Citation``."""

    @classmethod
    def xmldict_data_to_pb(cls, value: dict[str, Any]) -> Citation:
        """Converts a dict from ``xmltodict`` to a ``Citation`` protobuf.

        Args:
            value: The dict from ``xmltodict``.

        Returns:
            The ``Citation`` protobuf.
        """
        assert "Citation" in value
        tag_citation: dict[str, Any] = value["Citation"]

        # obtain IDs (many, one, none)
        ids: list[Citation.IdType] | None = None
        if "ID" not in tag_citation:
            pass
        elif isinstance(tag_citation["ID"], list):
            tags_id_type: list[dict[str, str]] = tag_citation["ID"]
            ids = [
                Citation.IdType(value=tag_id_type["#text"], source=tag_id_type["@Source"])
                for tag_id_type in tags_id_type
            ]
        elif isinstance(tag_citation["ID"], dict):
            tag_id_type: dict[str, str] = tag_citation["ID"]
            ids = [Citation.IdType(value=tag_id_type["#text"], source=tag_id_type["@Source"])]
        # obtain URL
        if "URL" in tag_citation:
            assert isinstance(tag_citation["URL"], str)
            url = tag_citation["URL"]
        else:
            url = None
        # obtain citation text
        if "CitationText" in tag_citation:
            assert isinstance(tag_citation["CitationText"], str)
            citation_text = tag_citation["CitationText"]
        else:
            citation_text = None

        return Citation(
            ids=ids,
            url=url,
            citation_text=citation_text,
            type=tag_citation.get("@Type"),
            abbrev=tag_citation.get("@Abbrev"),
        )


class ConvertBaseAttribute(ConverterBase):
    """Static method helper for converting XML data to ``BaseAttribute``.

    All uses cases of the ``typeAttribute`` from XSD extend the attribute.
    """

    @staticmethod
    def xmldict_data_to_pb(value: dict[str, Any]) -> BaseAttribute:
        """Converts a dict from ``xmltodict`` to a ``AttributeBase`` protobuf.

        Args:
            value: The dict from ``xmltodict``.

        Returns:
            The ``BaseAttribute`` protobuf.
        """
        assert "Attribute" in value, value
        tag_attribute: dict[str, Any] = value["Attribute"]

        # obtain text value
        text_value: str | None = None
        if "#text" in tag_attribute:
            text_value = tag_attribute["#text"]
        # obtain integer value
        integer_value: int | None = None
        if "@integerValue" in tag_attribute:
            integer_value = int(tag_attribute["@integerValue"])
        # obtain date value
        date_value: google.protobuf.timestamp_pb2.Timestamp | None = None
        if "@dateValue" in tag_attribute:
            dt = dateutil.parser.parse(tag_attribute["@dateValue"])
            seconds = int(time.mktime(dt.timetuple()))
            date_value = google.protobuf.timestamp_pb2.Timestamp(seconds=seconds)

        return BaseAttribute(
            value=text_value,
            integer_value=integer_value,
            date_value=date_value,
        )


class ConvertHgvsNucleotideExpression(ConverterBase):
    """Static method helper for converting XML data to ``HgvsNucleotideExpression``."""

    @classmethod
    def xmldict_data_to_pb(cls, value: dict[str, Any]) -> HgvsNucleotideExpression:
        """Converts a dict from ``xmltodict`` to a ``HgvsNucleotideExpression`` protobuf.

        Args:
            value: The dict from ``xmltodict``.

        Returns:
            The ``HgvsNucleotideExpression`` protobuf.
        """
        assert "NucleotideExpression" in value
        tag_nucleotide_expression: dict[str, Any] = value["NucleotideExpression"]
        cls.assert_keys(tag_nucleotide_expression, ["Expression"])

        expression = tag_nucleotide_expression["Expression"]
        sequence_type: NucleotideSequence.ValueType | None = None
        if "@sequenceType" in tag_nucleotide_expression:
            sequence_type = ConvertNucleotideSequence.xmldict_data_to_pb(
                tag_nucleotide_expression["@Type"]
            )
        sequence_accession_version: str | None = None
        if "@sequenceAccessionVersion" in tag_nucleotide_expression:
            sequence_accession_version = tag_nucleotide_expression["@sequenceAccessionVersion"]
        sequence_accession: str | None = None
        if "@sequenceAccession" in tag_nucleotide_expression:
            sequence_accession = tag_nucleotide_expression["@sequenceAccession"]
        sequence_version: int | None = None
        if "@sequenceVersion" in tag_nucleotide_expression:
            sequence_version = int(tag_nucleotide_expression["@sequenceVersion"])
        change: str | None = None
        if "@change" in tag_nucleotide_expression:
            change = tag_nucleotide_expression["@change"]
        assembly: str | None = None
        if "@assembly" in tag_nucleotide_expression:
            assembly = tag_nucleotide_expression["@assembly"]
        submitted: str | None = None
        if "@submitted" in tag_nucleotide_expression:
            submitted = tag_nucleotide_expression["@submitted"]
        mane_select: bool | None = None
        if "@MANESelect" in tag_nucleotide_expression:
            mane_select = tag_nucleotide_expression["@MANESelect"] == "true"
        mane_plus_clinical: bool | None = None
        if "@MANEPlusClinical" in tag_nucleotide_expression:
            mane_plus_clinical = tag_nucleotide_expression["@MANEPlusClinical"] == "true"

        return HgvsNucleotideExpression(
            expression=expression,
            sequence_type=sequence_type,
            sequence_accession_version=sequence_accession_version,
            sequence_accession=sequence_accession,
            sequence_version=sequence_version,
            change=change,
            assembly=assembly,
            submitted=submitted,
            mane_select=mane_select,
            mane_plus_clinical=mane_plus_clinical,
        )


class ConvertHgvsProteinExpression(ConverterBase):
    """Static method helper for converting XML data to to ``HgvsProteinExpression``."""

    @classmethod
    def xmldict_data_to_pb(cls, value: dict[str, Any]) -> HgvsProteinExpression:
        """Converts a dict from ``xmltodict`` to a `HgvsProteinExpression`` protobuf.

        Args:
            value: The dict from ``xmltodict``.

        Returns:
            The `HgvsProteinExpression`` protobuf.
        """
        assert "ProteinExpression" in value
        tag_pse: dict[str, Any] = value["ProteinExpression"]

        cls.assert_keys(tag_pse, ["Expression"])
        assert isinstance(tag_pse["Expression"], str)

        sequence_accession_version: str | None = None
        if "@sequenceAccessionVersion" in tag_pse:
            sequence_accession_version = tag_pse["@sequenceAccessionVersion"]
        sequence_accession: str | None = None
        if "@sequenceAccession" in tag_pse:
            sequence_accession = tag_pse["@sequenceAccession"]
        sequence_version: int | None = None
        if "@sequenceVersion" in tag_pse:
            sequence_version = int(tag_pse["@sequenceVersion"])
        change: str | None = None
        if "@change" in tag_pse:
            change = tag_pse["@change"]

        return HgvsProteinExpression(
            expression=tag_pse["Expression"],
            sequence_accession_version=sequence_accession_version,
            sequence_accession=sequence_accession,
            sequence_version=sequence_version,
            change=change,
        )


class ConvertHgvsExpression(ConverterBase):
    """Static method helper for converting XML data to to ``HgvsExpression``."""

    @classmethod
    def xmldict_data_to_pb(cls, value: dict[str, Any]) -> HgvsExpression:
        """Converts a dict from ``xmltodict`` to a `HgvsExpression`` protobuf.

        Args:
            value: The dict from ``xmltodict``.

        Returns:
            The `HgvsExpression`` protobuf.
        """
        assert "HGVS" in value
        tag_hgvs: dict[str, Any] = value["HGVS"]

        cls.assert_keys(tag_hgvs, ["@Type"])

        nucleotide_expression: HgvsNucleotideExpression | None = None
        if "NucleotideExpression" in tag_hgvs:
            nucleotide_expression = ConvertHgvsNucleotideExpression.xmldict_data_to_pb(
                {"NucleotideExpression": tag_hgvs["NucleotideExpression"]}
            )
        protein_expression: HgvsProteinExpression | None = None
        if "ProteinExpression" in tag_hgvs:
            protein_expression = ConvertHgvsProteinExpression.xmldict_data_to_pb(
                {"ProteinExpression": tag_hgvs["ProteinExpression"]}
            )
        molecular_consequences: list[Xref] | None = None
        if "MolecularConsequence" in tag_hgvs:
            molecular_consequences = [
                ConvertXref.xmldict_data_to_pb({"XRef": entry})
                for entry in cls.ensure_list(tag_hgvs["MolecularConsequence"])
            ]
        type_: HgvsType.ValueType = ConvertHgvsType.xmldict_data_to_pb(tag_hgvs["@Type"])
        assembly: str | None = tag_hgvs.get("@Assembly")

        return HgvsExpression(
            nucleotide_expression=nucleotide_expression,
            protein_expression=protein_expression,
            molecular_consequences=molecular_consequences,
            type=type_,
            assembly=assembly,
        )


class ConvertSoftware(ConverterBase):
    """Static method helper for converting XML data to to ``Software``."""

    @classmethod
    def xmldict_data_to_pb(cls, value: dict[str, Any]) -> Software:
        """Converts a dict from ``xmltodict`` to a ``Software`` protobuf.

        Args:
            value: The dict from ``xmltodict``.

        Returns:
            The ``Software`` protobuf.
        """
        assert "Software" in value
        tag_software: dict[str, str] = value["Software"]
        cls.assert_keys(tag_software, ["@name"])

        return Software(
            name=tag_software["@name"],
            version=tag_software.get("@version"),
            purpose=tag_software.get("@purpose"),
        )


class ConvertDescriptionHistory(ConverterBase):
    """Static method helper for converting XML data to to ``DescriptionHistory``."""

    @classmethod
    def xmldict_data_to_pb(cls, value: dict[str, Any]) -> DescriptionHistory:
        """Converts a dict from ``xmltodict`` to a ``DescriptionHistory`` protobuf.

        Args:
            value: The dict from ``xmltodict``.

        Returns:
            The ``DescriptionHistory`` protobuf.
        """
        assert "DescriptionHistory" in value
        tag_history_record: dict[str, Any] = value["DescriptionHistory"]
        cls.assert_keys(tag_history_record, ["Description"])
        assert isinstance(tag_history_record["Description"], str)

        dated: google.protobuf.timestamp_pb2.Timestamp | None = None
        if "@Dated" in tag_history_record:
            parsed = dateutil.parser.parse(tag_history_record["@Dated"])
            seconds = int(time.mktime(parsed.timetuple()))
            dated = google.protobuf.timestamp_pb2.Timestamp(seconds=seconds)

        return DescriptionHistory(
            description=tag_history_record["Description"],
            dated=dated,
        )


class ConvertGenericSetElement(ConverterBase):
    """Static method helper for converting XML data to to ``GenericSetElement``."""

    @classmethod
    def xmldict_data_to_pb(cls, value: dict[str, Any], tag_name: str) -> GenericSetElement:
        """Converts a dict from ``xmltodict`` to a ``GenericElementSet`` protobuf.

        Args:
            value: The dict from ``xmltodict``.
            tag_name: The tag name, e.g., ``"Name"``.

        Returns:
            The ``GenericSetElement`` protobuf.
        """
        assert tag_name in value
        tag_generic_set_element: dict[str, Any] = value[tag_name]
        cls.assert_keys(tag_generic_set_element, ["ElementValue"])

        tag_element_value: dict[str, str] = tag_generic_set_element["ElementValue"]
        cls.assert_keys(tag_element_value, ["#text", "@Type"])
        text_value = tag_element_value["#text"]
        type_ = tag_element_value["@Type"]

        # Parse out Citation, XRef, Comment tags.
        cxcs = cls.parse_citations_xrefs_comments(tag_generic_set_element)

        return GenericSetElement(
            value=text_value,
            type=type_,
            citations=cxcs.citations,
            xrefs=cxcs.xrefs,
            comments=cxcs.comments,
        )


class ConvertAttributeSetElement(ConverterBase):
    """Static method helper for converting XML data to to ``AttributeSetElement``."""

    @classmethod
    def xmldict_data_to_pb(cls, value: dict[str, Any]) -> AttributeSetElement:
        """Converts a dict from ``xmltodict`` to a ``AttributeSetElement`` protobuf.

        Args:
            value: The dict from ``xmltodict``.

        Returns:
            The ``AttributeSetElement`` protobuf.
        """
        assert "AttributeSet" in value
        tag_attribute_set_element: dict[str, Any] = value["AttributeSet"]
        cls.assert_keys(tag_attribute_set_element, ["Attribute"])

        # Parse out the augmented BaseAttribute.
        cls.assert_keys(tag_attribute_set_element["Attribute"], ["@Type"])
        attribute = AttributeSetElement.Attribute(
            base=ConvertBaseAttribute.xmldict_data_to_pb(
                {"Attribute": tag_attribute_set_element["Attribute"]}
            ),
            type=tag_attribute_set_element["Attribute"]["@Type"],
        )
        # Parse out Citation, XRef, Comment tags.
        cxcs = cls.parse_citations_xrefs_comments(tag_attribute_set_element)

        return AttributeSetElement(
            attribute=attribute, citations=cxcs.citations, xrefs=cxcs.xrefs, comments=cxcs.comments
        )


class ConvertTrait(ConverterBase):
    """Static method helper for converting XML data to to ``Trait``."""

    #: Map for converting from XML value to protobuf enum.
    CONVERT_TYPE: Dict[str, Trait.TraitRelationship.Type.ValueType] = {
        "phenotype": Trait.TraitRelationship.Type.TYPE_PHENOTYPE,
        "Subphenotype": Trait.TraitRelationship.Type.TYPE_SUBPHENOTYPE,
        "DrugResponseAndDisease": Trait.TraitRelationship.Type.TYPE_DRUG_RESPONSE_AND_DISEASE,
        "co-occuring condition": Trait.TraitRelationship.Type.TYPE_CO_OCCURING_CONDITION,
        "Finding member": Trait.TraitRelationship.Type.TYPE_FINDING_MEMBER,
    }

    @classmethod
    def convert_trait_relationship_type(cls, value: str) -> Trait.TraitRelationship.Type.ValueType:
        """Converts a string to a ``TraitRelationship.Type``.

        Args:
            value: The string.

        Returns:
            The ``TraitRelationship.Type``.
        """
        result = cls.CONVERT_TYPE.get(value)
        if not result:
            raise ValueError(f"Unknown value {value}")
        else:
            return result

    @classmethod
    def convert_trait_relationship(cls, value: dict[str, Any]) -> Trait.TraitRelationship:
        """Converts a dict from ``xmltodict`` to a ``TraitRelationship`` protobuf.

        Args:
            value: The dict from ``xmltodict``.

        Returns:
            The ``TraitRelationship`` protobuf.
        """
        assert "TraitRelationship" in value
        tag_trait_relationship: dict[str, Any] = value["TraitRelationship"]
        cls.assert_keys(tag_trait_relationship, ["@Type"])
        cls.assert_not_keys(  # In XSD but never seen in XML
            tag_trait_relationship,
            [
                "Symbol",
                "AttributeSet",
            ],
        )

        type_ = cls.convert_trait_relationship_type(tag_trait_relationship["@Type"])
        names: list[GenericSetElement] | None = None
        if "Name" in tag_trait_relationship:
            assert isinstance(
                tag_trait_relationship["Name"], dict
            ), "never seen more than once in XML"
            names = [ConvertGenericSetElement.xmldict_data_to_pb(tag_trait_relationship, "Name")]
        # Parse out Citation, XRef, Comment tags.
        cxcs = cls.parse_citations_xrefs_comments(tag_trait_relationship)

        return Trait.TraitRelationship(
            type=type_,
            names=names,
            citations=cxcs.citations,
            xrefs=cxcs.xrefs,
            comments=cxcs.comments,
        )

    @classmethod
    def xmldict_data_to_pb(cls, value: dict[str, Any]) -> Trait:
        """Converts a dict from ``xmltodict`` to a ``Trait`` protobuf.

        Args:
            value: The dict from ``xmltodict``.

        Returns:
            The ``Trait`` protobuf.
        """
        assert "Trait" in value
        tag_trait: dict[str, Any] = value["Trait"]

        # obtain names
        names: list[GenericSetElement] | None = None
        if "Name" in tag_trait:
            names = [
                ConvertGenericSetElement.xmldict_data_to_pb({"Name": element}, "Name")
                for element in cls.ensure_list(tag_trait["Name"])
            ]
        # obtain symbols
        symbols: list[GenericSetElement] | None = None
        if "Symbol" in tag_trait:
            symbols = [
                ConvertGenericSetElement.xmldict_data_to_pb({"Symbol": element}, "Symbol")
                for element in cls.ensure_list(tag_trait["Symbol"])
            ]
        # obtain attributes
        attributes: list[AttributeSetElement] | None = None
        if "AttributeSet" in tag_trait:
            attributes = [
                ConvertAttributeSetElement.xmldict_data_to_pb({"AttributeSet": element})
                for element in cls.ensure_list(tag_trait["AttributeSet"])
            ]
        # obtain trait relationships
        trait_relationships: list[Trait.TraitRelationship] | None = None
        if "TraitRelationship" in tag_trait:
            trait_relationships = [
                cls.convert_trait_relationship({"TraitRelationship": element})
                for element in cls.ensure_list(tag_trait["TraitRelationship"])
            ]
        # obtain sources
        sources: list[str] | None = None
        if "Source" in tag_trait:
            if isinstance(tag_trait["Source"], list):
                sources = tag_trait["Source"]
            else:
                assert isinstance(tag_trait["Source"], str)
                sources = [tag_trait["Source"]]

        # Parse out Citation, XRef, Comment tags.
        cxcs = cls.parse_citations_xrefs_comments(tag_trait)

        return Trait(
            names=names,
            symbols=symbols,
            attributes=attributes,
            trait_relationships=trait_relationships,
            citations=cxcs.citations,
            xrefs=cxcs.xrefs,
            comments=cxcs.comments,
            sources=sources,
        )


class ConvertIndication(ConverterBase):
    """Static method helper for converting XML data to to ``Indication``."""

    #: Map for converting from XML value to protobuf enum.
    CONVERT_TYPE: Dict[str, Indication.Type.ValueType] = {
        "Indication": Indication.Type.TYPE_INDICATION,
    }

    @classmethod
    def convert_indication_type(cls, value: str) -> Indication.Type.ValueType:
        """Converts a string to a ``Indication.Type``.

        Args:
            value: The string.

        Returns:
            The ``Indication.Type``.
        """
        result = cls.CONVERT_TYPE.get(value)
        if not result:
            raise ValueError(f"Unknown value {value}")
        else:
            return result

    @classmethod
    def xmldict_data_to_pb(cls, value: dict[str, Any]) -> Indication:
        """Converts a dict from ``xmltodict`` to a ``Indication`` protobuf.

        Args:
            value: The dict from ``xmltodict``.

        Returns:
            The ``Indication`` protobuf.
        """
        assert "Indication" in value
        tag_indication: dict[str, Any] = value["Indication"]

        # obtain traits
        traits: list[Trait] | None = None
        if "Trait" in tag_indication:
            traits = [
                ConvertTrait.xmldict_data_to_pb({"Trait": element})
                for element in cls.ensure_list(tag_indication["Trait"])
            ]
        # obtain names
        names: list[GenericSetElement] | None = None
        if "Name" in tag_indication:
            names = [
                ConvertGenericSetElement.xmldict_data_to_pb({"Name": element}, "Name")
                for element in cls.ensure_list(tag_indication["Name"])
            ]
        # obtain attributes
        attributes: list[AttributeSetElement] | None = None
        if "AttributeSet" in tag_indication:
            attributes = [
                ConvertAttributeSetElement.xmldict_data_to_pb({"AttributeSet": element})
                for element in cls.ensure_list(tag_indication["AttributeSet"])
            ]

        # Parse out Citation, XRef, Comment tags.
        cxcs = cls.parse_citations_xrefs_comments(tag_indication)

        # Obtaint ype.
        type_ = cls.convert_indication_type(tag_indication["@Type"])

        return Indication(
            traits=traits,
            names=names,
            attributes=attributes,
            citations=cxcs.citations,
            xrefs=cxcs.xrefs,
            comments=cxcs.comments,
            type=type_,
        )


class ConvertTraitSet(ConverterBase):
    """Static method helper for converting XML data to to ``TraitSet``."""

    #: Map for converting from XML value to protobuf enum.
    CONVERT_TYPE: Dict[str, TraitSet.Type.ValueType] = {
        "Disease": TraitSet.Type.TYPE_DISEASE,
        "DrugResponse": TraitSet.Type.TYPE_DRUG_RESPONSE,
        "Finding": TraitSet.Type.TYPE_FINDING,
        "PhenotypeInstruction": TraitSet.Type.TYPE_PHENOTYPE_INSTRUCTION,
        "TraitChoice": TraitSet.Type.TYPE_TRAIT_CHOICE,
    }

    @classmethod
    def convert_type(cls, value: str) -> TraitSet.Type.ValueType:
        """Converts a string to a ``TraitSet.Type``.

        Args:
            value: The string.

        Returns:
            The ``TraitSet.Type``.
        """
        result = cls.CONVERT_TYPE.get(value)
        if not result:
            raise ValueError(f"Unknown value {value}")
        else:
            return result

    @classmethod
    def xmldict_data_to_pb(cls, value: dict[str, Any]) -> TraitSet:
        """Converts a dict from ``xmltodict`` to a ``TraitSet`` protobuf.

        Args:
            value: The dict from ``xmltodict``.

        Returns:
            The ``TraitSet`` protobuf.
        """
        assert "TraitSet" in value
        tag_trait_set: dict[str, Any] = value["TraitSet"]

        # obtain traits
        traits: list[Trait] | None = None
        if "Trait" in tag_trait_set:
            traits = [
                ConvertTrait.xmldict_data_to_pb({"Trait": element})
                for element in cls.ensure_list(tag_trait_set["Trait"])
            ]
        # obtain names
        names: list[GenericSetElement] | None = None
        if "Name" in tag_trait_set:
            names = [
                ConvertGenericSetElement.xmldict_data_to_pb({"Name": element}, "Name")
                for element in cls.ensure_list(tag_trait_set["Name"])
            ]
        # obtain symbols
        symbols: list[GenericSetElement] | None = None
        if "Symbol" in tag_trait_set:
            symbols = [
                ConvertGenericSetElement.xmldict_data_to_pb({"Symbol": element}, "Symbol")
                for element in cls.ensure_list(tag_trait_set["Symbol"])
            ]
        # obtain attributes
        attributes: list[AttributeSetElement] | None = None
        if "AttributeSet" in tag_trait_set:
            attributes = [
                ConvertAttributeSetElement.xmldict_data_to_pb({"AttributeSet": element})
                for element in cls.ensure_list(tag_trait_set["AttributeSet"])
            ]

        # Parse out Citation, XRef, Comment tags.
        cxcs = cls.parse_citations_xrefs_comments(tag_trait_set)

        # Obtain type.
        type_ = cls.convert_type(tag_trait_set["@Type"])
        # Obtain date_last_evaluated
        date_last_evaluated: google.protobuf.timestamp_pb2.Timestamp | None = None
        if "@DateLastEvaluated" in tag_trait_set:
            parsed = dateutil.parser.parse(tag_trait_set["@DateLastEvaluated"])
            seconds = int(time.mktime(parsed.timetuple()))
            date_last_evaluated = google.protobuf.timestamp_pb2.Timestamp(seconds=seconds)
        # Obtain id
        id_: int | None = None
        if "@ID" in tag_trait_set:
            id_ = int(tag_trait_set["@ID"])
        # Obtain ContributesToAggregateClassification
        contributes_to_aggregate_classification: bool | None = None
        if "@ContributesToAggregateClassification" in tag_trait_set:
            contributes_to_aggregate_classification = (
                tag_trait_set["@ContributesToAggregateClassification"] == "true"
            )
        # Obtain lower_level_of_evidence.
        lower_level_of_evidence: bool | None = None
        if "@LowerLevelOfEvidence" in tag_trait_set:
            lower_level_of_evidence = tag_trait_set["@LowerLevelOfEvidence"] == "true"
        # Obtain multipleConditionExplanation
        multiple_condition_explanation: str | None = tag_trait_set.get(
            "@multipleConditionExplanation"
        )

        return TraitSet(
            traits=traits,
            names=names,
            symbols=symbols,
            attributes=attributes,
            citations=cxcs.citations,
            xrefs=cxcs.xrefs,
            comments=cxcs.comments,
            type=type_,
            date_last_evaluated=date_last_evaluated,
            id=id_,
            contributes_to_aggregate_classification=contributes_to_aggregate_classification,
            lower_level_of_evidence=lower_level_of_evidence,
            multiple_condition_explanation=multiple_condition_explanation,
        )


class ConvertAggregatedGermlineClassification(ConverterBase):
    """Static method helper for converting XML data to to ``AggregatedGermlineClassification``."""

    @classmethod
    def xmldict_data_to_pb(cls, value: dict[str, Any]) -> AggregatedGermlineClassification:
        """Converts a dict from ``xmltodict`` to a ``GermlineClassification`` protobuf.

        Args:
            value: The dict from ``xmltodict``.

        Returns:
            The ``GermlineClassification`` protobuf.
        """
        assert "GermlineClassification" in value
        tag_germline_classification: dict[str, Any] = value["GermlineClassification"]

        review_status: AggregateGermlineReviewStatus.ValueType = (
            ConvertAggregateGermlineReviewStatus.xmldict_data_to_pb(
                tag_germline_classification["ReviewStatus"]
            )
        )
        description: str | None = tag_germline_classification.get("Description")
        explanation: Comment | None = None
        if "Explanation" in tag_germline_classification:
            explanation = ConvertComment.xmldict_data_to_pb(
                {"Comment": tag_germline_classification["Explanation"]}
            )

        # Parse out Citation, XRef, Comment tags.
        cxcs = cls.parse_citations_xrefs_comments(tag_germline_classification)

        history_records: list[DescriptionHistory] | None = None
        if "History" in tag_germline_classification:
            history_records = [
                ConvertDescriptionHistory.xmldict_data_to_pb({"DescriptionHistory": element})
                for element in cls.ensure_list(tag_germline_classification["History"])
            ]

        conditions: list[TraitSet] | None = None
        if (
            "ConditionList" in tag_germline_classification
            and "TraitSet" in tag_germline_classification["ConditionList"]
        ):
            conditions = [
                ConvertTraitSet.xmldict_data_to_pb({"TraitSet": element})
                for element in cls.ensure_list(
                    tag_germline_classification["ConditionList"]["TraitSet"]
                )
            ]

        # Obtain date_last_evaluated
        date_last_evaluated: google.protobuf.timestamp_pb2.Timestamp | None = None
        if "@DateLastEvaluated" in tag_germline_classification:
            parsed = dateutil.parser.parse(tag_germline_classification["@DateLastEvaluated"])
            seconds = int(time.mktime(parsed.timetuple()))
            date_last_evaluated = google.protobuf.timestamp_pb2.Timestamp(seconds=seconds)
        # Obtain date_created
        date_created: google.protobuf.timestamp_pb2.Timestamp | None = None
        if "@DateCreated" in tag_germline_classification:
            parsed = dateutil.parser.parse(tag_germline_classification["@DateCreated"])
            seconds = int(time.mktime(parsed.timetuple()))
            date_created = google.protobuf.timestamp_pb2.Timestamp(seconds=seconds)
        # Obtain most_recent_submission
        most_recent_submission: google.protobuf.timestamp_pb2.Timestamp | None = None
        if "@MostRecentSubmission" in tag_germline_classification:
            parsed = dateutil.parser.parse(tag_germline_classification["@MostRecentSubmission"])
            seconds = int(time.mktime(parsed.timetuple()))
            most_recent_submission = google.protobuf.timestamp_pb2.Timestamp(seconds=seconds)

        # Obtain number_of_submissions
        number_of_submissions: int | None = None
        if "@NumberOfSubmissions" in tag_germline_classification:
            number_of_submissions = int(tag_germline_classification["@NumberOfSubmissions"])
        # Obtain number_of_submitters
        number_of_submitters: int | None = None
        if "@NumberOfSubmitters" in tag_germline_classification:
            number_of_submitters = int(tag_germline_classification["@NumberOfSubmitters"])

        return AggregatedGermlineClassification(
            review_status=review_status,
            description=description,
            explanation=explanation,
            citations=cxcs.citations,
            xrefs=cxcs.xrefs,
            comments=cxcs.comments,
            history_records=history_records,
            conditions=conditions,
            date_last_evaluated=date_last_evaluated,
            date_created=date_created,
            most_recent_submission=most_recent_submission,
            number_of_submissions=number_of_submissions,
            number_of_submitters=number_of_submitters,
        )


class ConvertAggregatedSomaticClinicalImpact(ConverterBase):
    """Static method helper for converting XML data to to ``ConvertAggregatedSomaticClinicalImpact``."""

    @classmethod
    def xmldict_data_to_pb(cls, value: dict[str, Any]) -> AggregatedSomaticClinicalImpact:
        """Converts a dict from ``xmltodict`` to a `AggregatedSomaticClinicalImpact`` protobuf.

        Args:
            value: The dict from ``xmltodict``.

        Returns:
            The `OncogenicityClassification`` protobuf.
        """
        assert "SomaticClinicalImpact" in value
        tag_somatic_clinical_impact: dict[str, Any] = value["SomaticClinicalImpact"]

        review_status: AggregateSomaticClinicalImpactReviewStatus.ValueType = (
            ConvertAggregateSomaticClinicalImpactReviewStatus.xmldict_data_to_pb(
                tag_somatic_clinical_impact["ReviewStatus"]
            )
        )
        description: str | None = tag_somatic_clinical_impact.get("Description")

        # Parse out Citation, XRef, Comment tags.
        cxcs = cls.parse_citations_xrefs_comments(tag_somatic_clinical_impact)

        history_records: list[DescriptionHistory] | None = None
        if "History" in tag_somatic_clinical_impact:
            history_records = [
                ConvertDescriptionHistory.xmldict_data_to_pb({"DescriptionHistory": element})
                for element in cls.ensure_list(tag_somatic_clinical_impact["History"])
            ]

        conditions: list[TraitSet] | None = None
        if "Condition" in tag_somatic_clinical_impact:
            conditions = [
                ConvertTraitSet.xmldict_data_to_pb({"TraitSet": element})
                for element in cls.ensure_list(tag_somatic_clinical_impact["Condition"])
            ]

        # Obtain date_last_evaluated
        date_last_evaluated: google.protobuf.timestamp_pb2.Timestamp | None = None
        if "@DateLastEvaluated" in tag_somatic_clinical_impact:
            parsed = dateutil.parser.parse(tag_somatic_clinical_impact["@DateLastEvaluated"])
            seconds = int(time.mktime(parsed.timetuple()))
            date_last_evaluated = google.protobuf.timestamp_pb2.Timestamp(seconds=seconds)
        # Obtain date_created
        date_created: google.protobuf.timestamp_pb2.Timestamp | None = None
        if "@DateCreated" in tag_somatic_clinical_impact:
            parsed = dateutil.parser.parse(tag_somatic_clinical_impact["@DateCreated"])
            seconds = int(time.mktime(parsed.timetuple()))
            date_created = google.protobuf.timestamp_pb2.Timestamp(seconds=seconds)
        # Obtain most_recent_submission
        most_recent_submission: google.protobuf.timestamp_pb2.Timestamp | None = None
        if "@MostRecentSubmission" in tag_somatic_clinical_impact:
            parsed = dateutil.parser.parse(tag_somatic_clinical_impact["@MostRecentSubmission"])
            seconds = int(time.mktime(parsed.timetuple()))
            most_recent_submission = google.protobuf.timestamp_pb2.Timestamp(seconds=seconds)

        # Obtain number_of_submissions
        number_of_submissions: int | None = None
        if "@NumberOfSubmissions" in tag_somatic_clinical_impact:
            number_of_submissions = int(tag_somatic_clinical_impact["@NumberOfSubmissions"])
        # Obtain number_of_submitters
        number_of_submitters: int | None = None
        if "@NumberOfSubmitters" in tag_somatic_clinical_impact:
            number_of_submitters = int(tag_somatic_clinical_impact["@NumberOfSubmitters"])

        return AggregatedSomaticClinicalImpact(
            review_status=review_status,
            description=description,
            citations=cxcs.citations,
            xrefs=cxcs.xrefs,
            comments=cxcs.comments,
            history_records=history_records,
            conditions=conditions,
            date_last_evaluated=date_last_evaluated,
            date_created=date_created,
            most_recent_submission=most_recent_submission,
            number_of_submissions=number_of_submissions,
            number_of_submitters=number_of_submitters,
        )


class ConvertAggregatedOncogenicityClassification(ConverterBase):
    """Static method helper for converting XML data to to ``AggregatedOncogenicityClassification``."""

    @classmethod
    def xmldict_data_to_pb(cls, value: dict[str, Any]) -> AggregatedOncogenicityClassification:
        """Converts a dict from ``xmltodict`` to a `AggregatedOncogenicityClassification`` protobuf.

        Args:
            value: The dict from ``xmltodict``.

        Returns:
            The ``OncogenicityClassification`` protobuf.
        """
        assert "OncogenicityClassification" in value
        tag_oncogenicity_classification: dict[str, Any] = value["OncogenicityClassification"]

        review_status: AggregateOncogenicityReviewStatus.ValueType = (
            ConvertAggregateOncogenicityReviewStatus.xmldict_data_to_pb(
                tag_oncogenicity_classification["ReviewStatus"]
            )
        )
        description: str | None = tag_oncogenicity_classification.get("Description")

        # Parse out Citation, XRef, Comment tags.
        cxcs = cls.parse_citations_xrefs_comments(tag_oncogenicity_classification)

        history_records: list[DescriptionHistory] | None = None
        if "History" in tag_oncogenicity_classification:
            history_records = [
                ConvertDescriptionHistory.xmldict_data_to_pb({"DescriptionHistory": element})
                for element in cls.ensure_list(tag_oncogenicity_classification["History"])
            ]

        conditions: list[TraitSet] | None = None
        if "Condition" in tag_oncogenicity_classification:
            conditions = [
                ConvertTraitSet.xmldict_data_to_pb({"TraitSet": element})
                for element in cls.ensure_list(tag_oncogenicity_classification["Condition"])
            ]

        # Obtain date_last_evaluated
        date_last_evaluated: google.protobuf.timestamp_pb2.Timestamp | None = None
        if "@DateLastEvaluated" in tag_oncogenicity_classification:
            parsed = dateutil.parser.parse(tag_oncogenicity_classification["@DateLastEvaluated"])
            seconds = int(time.mktime(parsed.timetuple()))
            date_last_evaluated = google.protobuf.timestamp_pb2.Timestamp(seconds=seconds)
        # Obtain date_created
        date_created: google.protobuf.timestamp_pb2.Timestamp | None = None
        if "@DateCreated" in tag_oncogenicity_classification:
            parsed = dateutil.parser.parse(tag_oncogenicity_classification["@DateCreated"])
            seconds = int(time.mktime(parsed.timetuple()))
            date_created = google.protobuf.timestamp_pb2.Timestamp(seconds=seconds)
        # Obtain most_recent_submission
        most_recent_submission: google.protobuf.timestamp_pb2.Timestamp | None = None
        if "@MostRecentSubmission" in tag_oncogenicity_classification:
            parsed = dateutil.parser.parse(tag_oncogenicity_classification["@MostRecentSubmission"])
            seconds = int(time.mktime(parsed.timetuple()))
            most_recent_submission = google.protobuf.timestamp_pb2.Timestamp(seconds=seconds)

        # Obtain number_of_submissions
        number_of_submissions: int | None = None
        if "@NumberOfSubmissions" in tag_oncogenicity_classification:
            number_of_submissions = int(tag_oncogenicity_classification["@NumberOfSubmissions"])
        # Obtain number_of_submitters
        number_of_submitters: int | None = None
        if "@NumberOfSubmitters" in tag_oncogenicity_classification:
            number_of_submitters = int(tag_oncogenicity_classification["@NumberOfSubmitters"])

        return AggregatedOncogenicityClassification(
            review_status=review_status,
            description=description,
            citations=cxcs.citations,
            xrefs=cxcs.xrefs,
            comments=cxcs.comments,
            history_records=history_records,
            conditions=conditions,
            date_last_evaluated=date_last_evaluated,
            date_created=date_created,
            most_recent_submission=most_recent_submission,
            number_of_submissions=number_of_submissions,
            number_of_submitters=number_of_submitters,
        )


class ConvertAggregateClassificationSet(ConverterBase):
    """Static method helper for converting XML data to to ``AggregateClassificationSet``."""

    @classmethod
    def xmldict_data_to_pb(cls, value: dict[str, Any]) -> AggregateClassificationSet:
        """Converts a dict from ``xmltodict`` to a `AggregateClassificationSet`` protobuf.

        Args:
            value: The dict from ``xmltodict``.

        Returns:
            The `AggregateClassificationSet`` protobuf.
        """
        assert "Classifications" in value
        tag_classifications: dict[str, Any] = value["Classifications"]

        germline_classification: AggregatedGermlineClassification | None = None
        if "GermlineClassification" in tag_classifications:
            germline_classification = ConvertAggregatedGermlineClassification.xmldict_data_to_pb(
                {"GermlineClassification": tag_classifications["GermlineClassification"]}
            )
        somatic_clinical_impacts: list[AggregatedSomaticClinicalImpact] | None = None
        if "SomaticClinicalImpact" in tag_classifications:
            somatic_clinical_impacts = [
                ConvertAggregatedSomaticClinicalImpact.xmldict_data_to_pb(
                    {"SomaticClinicalImpact": element}
                )
                for element in cls.ensure_list(tag_classifications["SomaticClinicalImpact"])
            ]
        oncogenicity_classification: AggregatedOncogenicityClassification | None = None
        if "OncogenicityClassification" in tag_classifications:
            oncogenicity_classification = (
                ConvertAggregatedOncogenicityClassification.xmldict_data_to_pb(
                    {
                        "OncogenicityClassification": tag_classifications[
                            "OncogenicityClassification"
                        ]
                    }
                )
            )

        return AggregateClassificationSet(
            germline_classification=germline_classification,
            somatic_clinical_impacts=somatic_clinical_impacts,
            oncogenicity_classification=oncogenicity_classification,
        )


class ConvertClinicalSignificance(ConverterBase):
    """Static method helper for converting XML data to to ``ClinicalSignificance``."""

    @classmethod
    def xmldict_data_to_pb(cls, value: dict[str, Any]) -> ClinicalSignificance:
        """Converts a dict from ``xmltodict`` to a `ClinicalSignificance`` protobuf.

        Args:
            value: The dict from ``xmltodict``.

        Returns:
            The `ClinicalSignificance`` protobuf.
        """
        assert "ClinicalSignificance" in value
        tag_clinical_significance: dict[str, Any] = value["ClinicalSignificance"]

        review_status: SubmitterReviewStatus.ValueType | None = None
        if "ReviewStatus" in tag_clinical_significance:
            review_status = ConvertSubmitterReviewStatus.xmldict_data_to_pb(
                tag_clinical_significance["ReviewStatus"]
            )
        description: str | None = tag_clinical_significance.get("Description")
        explanation: Comment | None = None
        if "Explanation" in tag_clinical_significance:
            explanation = ConvertComment.xmldict_data_to_pb(
                {"Comment": tag_clinical_significance["Explanation"]}
            )
        cxcs: CitationsXrefsComments = cls.parse_citations_xrefs_comments(tag_clinical_significance)
        date_last_evaluated: google.protobuf.timestamp_pb2.Timestamp | None = None
        if "@DateLastEvaluated" in tag_clinical_significance:
            parsed = dateutil.parser.parse(tag_clinical_significance["@DateLastEvaluated"])
            seconds = int(time.mktime(parsed.timetuple()))
            date_last_evaluated = google.protobuf.timestamp_pb2.Timestamp(seconds=seconds)

        return ClinicalSignificance(
            review_status=review_status,
            description=description,
            explanation=explanation,
            xrefs=cxcs.xrefs,
            citations=cxcs.citations,
            comments=cxcs.comments,
            date_last_evaluated=date_last_evaluated,
        )


class ConvertAlleleDescription(ConverterBase):
    """Static method helper for converting XML data to to ``AlleleDescription``."""

    #: Map for converting from XML value to protobuf enum.
    CONVERT_RELATIVE_ORIENTATION: Dict[str, AlleleDescription.RelativeOrientation.ValueType] = {
        "cis": AlleleDescription.RelativeOrientation.RELATIVE_ORIENTATION_CIS,
        "trans": AlleleDescription.RelativeOrientation.RELATIVE_ORIENTATION_TRANS,
        "unknown": AlleleDescription.RelativeOrientation.RELATIVE_ORIENTATION_UNKNOWN,
    }

    @classmethod
    def convert_relative_orientation(
        cls, value: str
    ) -> AlleleDescription.RelativeOrientation.ValueType:
        """Converts a string to a ``AlleleDescription.RelativeOrientation``.

        Args:
            value: The string.

        Returns:
            The ``TraitRelationship.Type``.
        """
        result = cls.CONVERT_RELATIVE_ORIENTATION.get(value)
        if not result:
            raise ValueError(f"Unknown value {value}")
        else:
            return result

    @classmethod
    def xmldict_data_to_pb(cls, value: dict[str, Any]) -> AlleleDescription:
        """Converts a dict from ``xmltodict`` to a `AlleleDescription`` protobuf.

        Args:
            value: The dict from ``xmltodict``.

        Returns:
            The `AlleleDescription`` protobuf.
        """
        assert "AlleleDescSet" in value
        tag_allele_desc_set: dict[str, Any] = value["AlleleDescSet"]
        cls.assert_keys(tag_allele_desc_set, ["Name"])

        name: str = tag_allele_desc_set["Name"]
        relative_orientation: AlleleDescription.RelativeOrientation.ValueType | None = None
        if "RelativeOrientation" in tag_allele_desc_set:
            relative_orientation = cls.convert_relative_orientation(
                tag_allele_desc_set["RelativeOrientation"]
            )
        zygosity: Zygosity.ValueType | None = None
        if "Zygosity" in tag_allele_desc_set:
            zygosity = ConvertZygosity.xmldict_data_to_pb(tag_allele_desc_set["Zygosity"])
        clinical_significance: ClinicalSignificance | None = None
        if "ClinicalSignificance" in tag_allele_desc_set:
            clinical_significance = ConvertClinicalSignificance.xmldict_data_to_pb(
                {"ClinicalSignificance": tag_allele_desc_set["ClinicalSignificance"]}
            )

        return AlleleDescription(
            name=name,
            relative_orientation=relative_orientation,
            zygosity=zygosity,
            clinical_significance=clinical_significance,
        )


class ConvertRecordHistory(ConverterBase):
    """Static method helper for converting XML data to to ``RecordHistory``."""

    @classmethod
    def xmldict_data_to_pb(cls, value: dict[str, Any]) -> RecordHistory:
        """Converts a dict from ``xmltodict`` to a `RecordHistory`` protobuf.

        Args:
            value: The dict from ``xmltodict``.

        Returns:
            The `RecordHistory`` protobuf.
        """
        assert "Replaced" in value
        tag_record_history: dict[str, Any] = value["Replaced"]

        comment: Comment | None = None
        if "Comment" in tag_record_history:
            comment = ConvertComment.xmldict_data_to_pb({"Comment": tag_record_history["Comment"]})
        accession: str = tag_record_history["@Accession"]
        version: int = int(tag_record_history["@Version"])
        date_changed_parsed = dateutil.parser.parse(tag_record_history["@DateChanged"])
        date_changed_seconds = int(time.mktime(date_changed_parsed.timetuple()))
        date_changed = google.protobuf.timestamp_pb2.Timestamp(seconds=date_changed_seconds)
        variation_id: int | None = None
        if "@VariationID" in tag_record_history:
            variation_id = int(tag_record_history["@VariationID"])

        return RecordHistory(
            comment=comment,
            accession=accession,
            version=version,
            date_changed=date_changed,
            variation_id=variation_id,
        )


class ConvertClassificationScv(ConverterBase):
    """Static method helper for converting XML data to to ``ClassificationScv``."""

    @classmethod
    def convert_somatic_clinical_impact(
        cls, value: dict[str, Any]
    ) -> ClassificationScv.SomaticClinicalImpact:
        """Converts a dict from ``xmltodict`` to a ``SomaticClinicalImpact`` protobuf.

        Args:
            value: The dict from ``xmltodict``.

        Returns:
            The ``SomaticClinicalImpact`` protobuf.
        """
        assert "SomaticClinicalImpact" in value
        tag_somatic_clinical_impact: str | dict[str, Any] = value["SomaticClinicalImpact"]
        if isinstance(tag_somatic_clinical_impact, str):
            return ClassificationScv.SomaticClinicalImpact(value=tag_somatic_clinical_impact)
        else:
            cls.assert_keys(tag_somatic_clinical_impact, ["#text"])

            clinical_impact_assertion_type: str | None = tag_somatic_clinical_impact.get(
                "@ClinicalImpactAssertionType"
            )
            clinical_impact_clinical_significance: str | None = tag_somatic_clinical_impact.get(
                "@ClinicalImpactClinicalSignificance"
            )
            drug_for_therapeutic_assertion: str | None = tag_somatic_clinical_impact.get(
                "@DrugForTherapeuticAssertion"
            )

            return ClassificationScv.SomaticClinicalImpact(
                value=tag_somatic_clinical_impact["#text"],
                clinical_impact_assertion_type=clinical_impact_assertion_type,
                clinical_impact_clinical_significance=clinical_impact_clinical_significance,
                drug_for_therapeutic_assertion=drug_for_therapeutic_assertion,
            )

    @classmethod
    def convert_classification_score(
        cls, value: dict[str, Any]
    ) -> ClassificationScv.ClassificationScore:
        """Converts a dict from ``xmltodict`` to a ``ClassificationScore`` protobuf.

        Args:
            value: The dict from ``xmltodict``.

        Returns:
            The ``ClassificationScore`` protobuf.
        """
        assert "ClassificationScore" in value
        tag_classification_score: str | dict[str, Any] = value["ClassificationScore"]

        if isinstance(tag_classification_score, str):
            return ClassificationScv.ClassificationScore(
                value=float(tag_classification_score),
            )
        else:
            cls.assert_keys(tag_classification_score, ["#text"])
            type_: str | None = tag_classification_score.get("@type")
            return ClassificationScv.ClassificationScore(
                value=float(tag_classification_score["#text"]),
                type=type_,
            )

    @classmethod
    def xmldict_data_to_pb(cls, value: dict[str, Any]) -> ClassificationScv:
        """Converts a dict from ``xmltodict`` to a ``ClassificationScv`` protobuf.

        Args:
            value: The dict from ``xmltodict``.

        Returns:
            The ``ClassificationScv`` protobuf.
        """
        assert "Classification" in value
        tag_classification: dict[str, Any] = value["Classification"]

        review_status: SubmitterReviewStatus.ValueType = (
            ConvertSubmitterReviewStatus.xmldict_data_to_pb(
                ensure_str(tag_classification["ReviewStatus"])
            )
        )
        germline_classification: str | None = tag_classification.get("GermlineClassification")
        somatic_clinical_impacts: ClassificationScv.SomaticClinicalImpact | None = None
        if "SomaticClinicalImpact" in tag_classification:
            somatic_clinical_impacts = cls.convert_somatic_clinical_impact(
                {"SomaticClinicalImpact": tag_classification["SomaticClinicalImpact"]}
            )
        oncogenicity_classification: str | None = tag_classification.get(
            "OncogenicityClassification"
        )
        explanation_of_classification: str | None = tag_classification.get(
            "ExplanationOfClassification"
        )
        classification_scores: list[ClassificationScv.ClassificationScore] | None = None
        if "ClassificationScore" in tag_classification:
            classification_scores = [
                cls.convert_classification_score({"ClassificationScore": element})
                for element in cls.ensure_list(tag_classification["ClassificationScore"])
            ]

        # Parse out Citation, XRef, Comment tags.
        cxcs = cls.parse_citations_xrefs_comments(tag_classification)

        date_last_evaluated: google.protobuf.timestamp_pb2.Timestamp | None = None
        if "@DateLastEvaluated" in tag_classification:
            parsed = dateutil.parser.parse(tag_classification["@DateLastEvaluated"])
            seconds = int(time.mktime(parsed.timetuple()))
            date_last_evaluated = google.protobuf.timestamp_pb2.Timestamp(seconds=seconds)

        return ClassificationScv(
            review_status=review_status,
            germline_classification=germline_classification,
            somatic_clinical_impacts=somatic_clinical_impacts,
            oncogenicity_classification=oncogenicity_classification,
            explanation_of_classification=explanation_of_classification,
            classification_scores=classification_scores,
            xrefs=cxcs.xrefs,
            citations=cxcs.citations,
            comments=cxcs.comments,
            date_last_evaluated=date_last_evaluated,
        )


class ConvertSubmitterIdentifiers(ConverterBase):
    """Static method helper for converting XML data to to ``SubmitterIdentifiers``."""

    @classmethod
    def xmldict_data_to_pb(cls, tag: dict[str, Any], tag_name: str) -> SubmitterIdentifiers:
        """Converts a dict from ``xmltodict`` to a `SubmitterIdentifiers`` protobuf.

        Args:
            tag: The dict from ``xmltodict``.

        Returns:
            The `SubmitterIdentifiers`` protobuf.
        """
        inner_tag = tag[tag_name]

        return SubmitterIdentifiers(
            submitter_name=inner_tag["@SubmitterName"],
            org_id=int(inner_tag["@OrgID"]),
            org_category=inner_tag["@OrganizationCategory"],
            org_abbreviation=inner_tag.get("@OrgAbbreviation"),
        )


class ConvertSpecies(ConverterBase):
    """Static method helper for converting XML data to to ``Species``."""

    @classmethod
    def xmldict_data_to_pb(cls, value: dict[str, Any]) -> Species:
        """Converts a dict from ``xmltodict`` to a `Species`` protobuf.

        Args:
            tag: The dict from ``xmltodict``.

        Returns:
            The `Species`` protobuf.
        """
        assert "Species" in value
        tag_species = value["Species"]
        if isinstance(tag_species, str):
            return Species(name=tag_species)
        else:
            assert isinstance(tag_species, dict)
            name: str = tag_species["#text"]
            taxonomy_id: int | None = None
            if "@TaxonomyId" in tag_species:
                taxonomy_id = int(tag_species["@TaxonomyId"])

            return Species(
                name=name,
                taxonomy_id=taxonomy_id,
            )


class ConvertClassifiedCondition(ConverterBase):
    """Static method helper for converting XML data to to ``ClassifiedCondition``."""

    @classmethod
    def xmldict_data_to_pb(cls, tag: dict[str, Any]) -> ClassifiedCondition:
        """Converts a dict from ``xmltodict`` to a `ClassifiedCondition`` protobuf.

        Args:
            tag: The dict from ``xmltodict``.

        Returns:
            The `ClassifiedCondition`` protobuf.
        """
        assert "ClassifiedCondition" in tag
        tag_classified_condition: dict[str, Any] = tag["ClassifiedCondition"]

        if isinstance(tag_classified_condition, str):
            return ClassifiedCondition(value=tag_classified_condition)
        else:
            assert isinstance(tag_classified_condition, dict)
            value: str = tag_classified_condition["#text"]
            db: str | None = None
            if "@DB" in tag_classified_condition:
                db = tag_classified_condition["@DB"]
            id_: str | None = None
            if "@ID" in tag_classified_condition:
                id_ = tag_classified_condition["@ID"]
            return ClassifiedCondition(
                value=value,
                db=db,
                id=id_,
            )


class ConvertClinicalAssertionRecordHistory(ConverterBase):
    """Static method helper for converting XML data to to ``ClinicalAssertionRecordHistory``."""

    @classmethod
    def xmldict_data_to_pb(cls, tag: dict[str, Any]) -> ClinicalAssertionRecordHistory:
        """Converts a dict from ``xmltodict`` to a `ClinicalAssertionRecordHistory`` protobuf.

        Args:
            tag: The dict from ``xmltodict``.

        Returns:
            The `ClinicalAssertionRecordHistory`` protobuf.
        """
        assert "Replaced" in tag
        tag_record_history: dict[str, Any] = tag["Replaced"]

        comment: Comment | None = None
        if "Comment" in tag_record_history:
            comment = ConvertComment.xmldict_data_to_pb({"Comment": tag_record_history["Comment"]})
        accession: str = tag_record_history["@Accession"]
        version: int = int(tag_record_history["@Version"])
        date_changed_parsed = dateutil.parser.parse(tag_record_history["@DateChanged"])
        date_changed_seconds = int(time.mktime(date_changed_parsed.timetuple()))
        date_changed = google.protobuf.timestamp_pb2.Timestamp(seconds=date_changed_seconds)

        return ClinicalAssertionRecordHistory(
            comment=comment,
            accession=accession,
            version=version,
            date_changed=date_changed,
        )


class ConvertFunctionalConsequence(ConverterBase):
    """Static method helper for converting XML data to to ``FunctionalConsequence``."""

    @classmethod
    def xmldict_data_to_pb(cls, tag: dict[str, Any]) -> FunctionalConsequence:
        """Converts a dict from ``xmltodict`` to a `FunctionalConsequence`` protobuf.

        Args:
            tag: The dict from ``xmltodict``.

        Returns:
            The `FunctionalConsequence`` protobuf.
        """
        assert "FunctionalConsequence" in tag
        tag_function_consequence: dict[str, Any] = tag["FunctionalConsequence"]

        value = tag_function_consequence["@Value"]
        # Parse out Citation, XRef, Comment tags.
        cxcs = cls.parse_citations_xrefs_comments(tag_function_consequence)

        return FunctionalConsequence(
            xrefs=cxcs.xrefs, citations=cxcs.citations, comments=cxcs.comments, value=value
        )


class ConvertGeneralCitations(ConverterBase):
    """Static method helper for converting XML data to to ``GeneralCitationss``."""

    @classmethod
    def xmldict_data_to_pb(cls, tag: dict[str, Any]) -> GeneralCitations:
        """Converts a dict from ``xmltodict`` to a `GeneralCitations`` protobuf.

        Args:
            tag: The dict from ``xmltodict``.

        Returns:
            The `GeneralCitations`` protobuf.
        """
        assert "GeneralCitations" in tag
        tag_function_consequence: dict[str, Any] = tag["GeneralCitations"]

        citations: list[Citation] | None = None
        if "Citation" in tag_function_consequence:
            citations = [
                ConvertCitation.xmldict_data_to_pb({"Citation": entry})
                for entry in cls.ensure_list(tag_function_consequence["Citation"])
            ]

        xrefs: list[Xref] | None = None
        if "XRef" in tag_function_consequence:
            xrefs = [
                ConvertXref.xmldict_data_to_pb({"XRef": entry})
                for entry in cls.ensure_list(tag_function_consequence["XRef"])
            ]

        return GeneralCitations(
            citations=citations,
            xrefs=xrefs,
        )


class ConvertCooccurrence(ConverterBase):
    """Static method helper for converting XML data to to ``Cooccurrence``."""

    @classmethod
    def xmldict_data_to_pb(cls, tag: dict[str, Any]) -> Cooccurrence:
        """Converts a dict from ``xmltodict`` to a `Cooccurrence`` protobuf.

        Args:
            tag: The dict from ``xmltodict``.

        Returns:
            The `Cooccurrence`` protobuf.
        """
        assert "Co-occurrenceSet" in tag
        tag_cooccurrence: dict[str, Any] = tag["Co-occurrenceSet"]

        zygosity: Zygosity.ValueType | None = None
        if "Zygosity" in tag_cooccurrence:
            zygosity = ConvertZygosity.xmldict_data_to_pb(tag_cooccurrence["Zygosity"])
        allele_descriptions: list[AlleleDescription] | None = None
        if "AlleleDescSet" in tag_cooccurrence:
            allele_descriptions = [
                ConvertAlleleDescription.xmldict_data_to_pb({"AlleleDescSet": element})
                for element in cls.ensure_list(tag_cooccurrence["AlleleDescSet"])
            ]
        count: int | None = None
        if "Count" in tag_cooccurrence:
            count = int(tag_cooccurrence["Count"])

        return Cooccurrence(
            zygosity=zygosity,
            allele_descriptions=allele_descriptions,
            count=count,
        )


class ConvertSubmitter(ConverterBase):
    """Static method helper for converting XML data to to ``Submitter``."""

    #: Map for converting from XML value to protobuf enum.
    CONVERT_YPE: Dict[str, Submitter.Type.ValueType] = {
        "primary": Submitter.Type.TYPE_PRIMARY,
        "secondary": Submitter.Type.TYPE_SECONDARY,
        "behalf": Submitter.Type.TYPE_BEHALF,
    }

    @classmethod
    def convert_type(cls, value: str) -> Submitter.Type.ValueType:
        """Converts a string to a ``Submitter.Type.ValueType``.

        Args:
            value: The string.

        Returns:
            The ``Submitter.Type``.
        """
        result = cls.CONVERT_YPE.get(value)
        if not result:
            raise ValueError(f"Unknown value {value}")
        else:
            return result

    @classmethod
    def xmldict_data_to_pb(cls, tag: dict[str, Any]) -> Submitter:
        """Converts a dict from ``xmltodict`` to a `Submitter`` protobuf.

        Args:
            tag: The dict from ``xmltodict``.

        Returns:
            The `Submitter`` protobuf.
        """
        assert "SubmitterDescription" in tag
        tag_sd = tag["SubmitterDescription"]

        return Submitter(
            submitter_identifiers=ConvertSubmitterIdentifiers.xmldict_data_to_pb(
                tag, "SubmitterDescription"
            ),
            type=cls.convert_type(tag_sd["@Type"]),
        )


class ConvertDosageSensitivity(ConverterBase):
    """Static method helper for converting XML data to to ``DosageSensitivity``."""

    @classmethod
    def xmldict_data_to_pb(cls, tag: dict[str, Any], tag_name: str) -> DosageSensitivity:
        """Converts a dict from ``xmltodict`` to a `DosageSensitivity`` protobuf.

        Args:
            tag: The dict from ``xmltodict``.
            tag_name: The name of the tag.

        Returns:
            The `DosageSensitivity`` protobuf.
        """
        assert tag_name in tag
        tag_inner: dict[str, Any] = tag[tag_name]

        value: str = tag_inner.get("#text", "")
        last_evaluated: google.protobuf.timestamp_pb2.Timestamp | None = None
        if "@last_evaluated" in tag_inner:
            parsed = dateutil.parser.parse(tag_inner["@last_evaluated"])
            seconds = int(time.mktime(parsed.timetuple()))
            last_evaluated = google.protobuf.timestamp_pb2.Timestamp(seconds=seconds)
        clingen: str | None = None
        if "@ClinGen" in tag_inner:
            clingen = tag_inner["@ClinGen"]

        return DosageSensitivity(
            value=value,
            last_evaluated=last_evaluated,
            clingen=clingen,
        )


class ConvertOtherName(ConverterBase):
    """Static method helper for converting XML data to to ``OtherName``."""

    @classmethod
    def xmldict_data_to_pb(cls, tag: dict[str, Any]) -> OtherName:
        """Converts a dict from ``xmltodict`` to a `OtherName`` protobuf.

        Args:
            tag: The dict from ``xmltodict``.

        Returns:
            The `OtherName`` protobuf.
        """
        assert "Name" in tag
        tag_inner: dict[str, Any] = tag["Name"]

        if isinstance(tag_inner, str):
            return OtherName(value=tag_inner)
        else:
            assert isinstance(tag_inner, dict)
            value: str = tag_inner.get("#text", "")
            type_: str | None = tag_inner.get("@Type")
            return OtherName(value=value, type=type_)


class ConvertDeletedScv(ConverterBase):
    """Static method helper for converting XML data to to ``DeletedScv``."""

    @classmethod
    def xmldict_data_to_pb(cls, tag: dict[str, Any]) -> DeletedScv:
        """Converts a dict from ``xmltodict`` to a `DeletedScv`` protobuf.

        Args:
            tag: The dict from ``xmltodict``.

        Returns:
            The `DeletedScv`` protobuf.
        """
        assert "Accession" in tag
        tag_scv: dict[str, Any] = tag["Accession"]

        accession: str = tag_scv["#text"]
        version: int = int(tag_scv["@Version"])
        date_deleted_parsed = dateutil.parser.parse(tag_scv["@DateDeleted"])
        date_deleted_seconds = int(time.mktime(date_deleted_parsed.timetuple()))
        date_deleted = google.protobuf.timestamp_pb2.Timestamp(seconds=date_deleted_seconds)

        return DeletedScv(
            accession=accession,
            version=version,
            date_deleted=date_deleted,
        )


class ConvertLocation(ConverterBase):
    """Static method helper for converting XML data to to ``Location``."""

    #: Map for converting from XML value to protobuf enum.
    CONVERT_ASSEMBLY_STATUS: Dict[str, Location.SequenceLocation.AssemblyStatus.ValueType] = {
        "current": Location.SequenceLocation.AssemblyStatus.ASSEMBLY_STATUS_CURRENT,
        "previous": Location.SequenceLocation.AssemblyStatus.ASSEMBLY_STATUS_PREVIOUS,
    }

    @classmethod
    def convert_assembly_status(
        cls, value: str
    ) -> Location.SequenceLocation.AssemblyStatus.ValueType:
        """Converts a string to a ``Location.SequenceLocation.AssemblyStatus.ValueType``.

        Args:
            value: The string.

        Returns:
            The ``Location.SequenceLocation.AssemblyStatus``.
        """
        result = cls.CONVERT_ASSEMBLY_STATUS.get(value)
        if not result:
            raise ValueError(f"Unknown value {value}")
        else:
            return result

    @classmethod
    def convert_sequence_location(cls, tag: dict[str, Any]) -> Location.SequenceLocation:
        """Converts a dict from ``xmltodict`` to a ``Location.SequenceLocation`` protobuf.

        Args:
            tag: The dict from ``xmltodict``.

        Returns:
            The ``Location.SequenceLocation`` protobuf.
        """
        assert "SequenceLocation" in tag
        tag_sl: dict[str, Any] = tag["SequenceLocation"]

        for_display: bool | None = None
        if "@forDisplay" in tag_sl:
            for_display = tag_sl["@forDisplay"] == "true"
        assembly: str = tag_sl["@Assembly"]
        chr_: Chromosome.ValueType = ConvertChromosome.xmldict_data_to_pb(tag_sl["@Chr"])
        accession: str | None = tag_sl.get("@Accession")
        outer_start: int | None = None
        if "@outerStart" in tag_sl:
            outer_start = int(tag_sl["@outerStart"])
        inner_start: int | None = None
        if "@innerStart" in tag_sl:
            inner_start = int(tag_sl["@innerStart"])
        start: int | None = None
        if "@start" in tag_sl:
            start = int(tag_sl["@start"])
        stop: int | None = None
        if "@stop" in tag_sl:
            stop = int(tag_sl["@stop"])
        inner_stop: int | None = None
        if "@innerStop" in tag_sl:
            inner_stop = int(tag_sl["@innerStop"])
        outer_stop: int | None = None
        if "@outerStop" in tag_sl:
            outer_stop = int(tag_sl["@outerStop"])
        display_start: int | None = None
        if "@display_start" in tag_sl:
            display_start = int(tag_sl["@display_start"])
        display_stop: int | None = None
        if "@display_stop" in tag_sl:
            display_stop = int(tag_sl["@display_stop"])
        strand: str | None = None
        if "@Strand" in tag_sl:
            strand = tag_sl["@Strand"]
        variant_length: int | None = None
        if "@variantLength" in tag_sl:
            variant_length = int(tag_sl["@variantLength"])
        reference_allele: str | None = tag_sl.get("@referenceAllele")
        alternate_allele: str | None = tag_sl.get("@alternateAllele")
        assembly_accession_version: str | None = tag_sl.get("@assemblyAccessionVersion")
        assembly_status: Location.SequenceLocation.AssemblyStatus.ValueType | None = None
        if "@assemblyStatus" in tag_sl:
            assembly_status = cls.convert_assembly_status(tag_sl["@assemblyStatus"])
        position_vcf: int | None = None
        if "@positionVCF" in tag_sl:
            position_vcf = int(tag_sl["@positionVCF"])
        reference_allele_vcf: str | None = tag_sl.get("@referenceAlleleVCF")
        alternate_allele_vcf: str | None = tag_sl.get("@alternateAlleleVCF")
        for_display_length: int | None = None
        if "@forDisplayLength" in tag_sl:
            for_display_length = int(tag_sl["@forDisplayLength"])

        return Location.SequenceLocation(
            for_display=for_display,
            assembly=assembly,
            chr=chr_,
            accession=accession,
            outer_start=outer_start,
            inner_start=inner_start,
            start=start,
            stop=stop,
            inner_stop=inner_stop,
            outer_stop=outer_stop,
            display_start=display_start,
            display_stop=display_stop,
            strand=strand,
            variant_length=variant_length,
            reference_allele=reference_allele,
            alternate_allele=alternate_allele,
            assembly_accession_version=assembly_accession_version,
            assembly_status=assembly_status,
            position_vcf=position_vcf,
            reference_allele_vcf=reference_allele_vcf,
            alternate_allele_vcf=alternate_allele_vcf,
            for_display_length=for_display_length,
        )

    @classmethod
    def xmldict_data_to_pb(cls, value: dict[str, Any]) -> Location:
        """Converts a dict from ``xmltodict`` to a ``Location`` protobuf.

        Args:
            value: The dict from ``xmltodict``.

        Returns:
            The ``Location`` protobuf.
        """
        assert "Location" in value
        tag_location: dict[str, Any] = value["Location"]

        cytogenic_locations: list[str] | None = None
        if "CytogeneticLocation" in tag_location:
            cytogenic_locations = [
                entry for entry in cls.ensure_list(tag_location["CytogeneticLocation"])
            ]

        sequence_locations: list[Location.SequenceLocation] | None = None
        if "SequenceLocation" in tag_location:
            sequence_locations = [
                cls.convert_sequence_location({"SequenceLocation": entry})
                for entry in cls.ensure_list(tag_location["SequenceLocation"])
            ]

        gene_locations: list[str] | None = None
        if "GeneLocation" in tag_location:
            gene_locations = [entry for entry in cls.ensure_list(tag_location["GeneLocation"])]

        xrefs: list[Xref] | None = None
        if "XRef" in tag_location:
            xrefs = [
                ConvertXref.xmldict_data_to_pb({"XRef": entry})
                for entry in cls.ensure_list(tag_location["XRef"])
            ]

        return Location(
            cytogenetic_locations=cytogenic_locations,
            sequence_locations=sequence_locations,
            gene_locations=gene_locations,
            xrefs=xrefs,
        )


class ConvertScv(ConverterBase):
    """Static method helper for converting XML data to to ``Scv``."""

    @classmethod
    def xmldict_data_to_pb(cls, tag: dict[str, Any]) -> Scv:
        """Converts a dict from ``xmltodict`` to a `Scv`` protobuf.

        Args:
            tag: The dict from ``xmltodict``.

        Returns:
            The `Scv`` protobuf.
        """
        assert "SCV" in tag
        tag_scv: dict[str, Any] = tag["SCV"]

        title: str | None = tag_scv.get("@Title")
        accession: str = tag_scv["@Accession"]
        version: int = int(tag_scv["@Version"])

        return Scv(
            title=title,
            accession=accession,
            version=version,
        )


class ConvertFamilyData(ConverterBase):
    """Static method helper for converting XML data to to ``FamilyData``."""

    @classmethod
    def xmldict_data_to_pb(cls, tag: dict[str, Any]) -> FamilyData:
        """Converts a dict from ``xmltodict`` to a `FamilyData`` protobuf.

        Args:
            tag: The dict from ``xmltodict``.

        Returns:
            The `FamilyData`` protobuf.
        """
        assert "FamilyData" in tag
        tag_inner: dict[str, Any] = tag["FamilyData"]

        family_history: str | None = tag_inner.get("FamilyHistory")
        num_families: int | None = None
        if "@NumFamilies" in tag_inner:
            num_families = int(tag_inner["@NumFamilies"])
        num_families_with_variant: int | None = None
        if "@NumFamiliesWithVariant" in tag_inner:
            num_families_with_variant = int(tag_inner["@NumFamiliesWithVariant"])
        num_families_with_segregation_observed: int | None = None
        if "@NumFamiliesWithSegregationObserved" in tag_inner:
            num_families_with_segregation_observed = int(
                tag_inner["@NumFamiliesWithSegregationObserved"]
            )
        pedigree_id: str | None = tag_inner.get("@PedigreeID")
        segregation_observed: str | None = tag_inner.get("@SegregationObserved")

        return FamilyData(
            family_history=family_history,
            num_families=num_families,
            num_families_with_variant=num_families_with_variant,
            num_families_with_segregation_observed=num_families_with_segregation_observed,
            pedigree_id=pedigree_id,
            segregation_observed=segregation_observed,
        )


class ConvertSample(ConverterBase):
    """Static method helper for converting XML data to to ``Sample``."""

    @classmethod
    def convert_sample_description(cls, tag: dict[str, Any]) -> Sample.SampleDescription:
        """Converts a dict from ``xmltodict`` to a ``Sample.SampleDescription`` protobuf.

        Args:
            tag: The dict from ``xmltodict``.

        Returns:
            The ``Sample.SampleDescription`` protobuf.
        """
        assert "SampleDescription" in tag
        tag_sd: dict[str, Any] = tag["SampleDescription"]

        description: Comment | None = None
        if "Description" in tag_sd:
            description = ConvertComment.xmldict_data_to_pb({"Comment": tag_sd["Description"]})
        citation: Citation | None = None
        if "Citation" in tag_sd:
            citation = ConvertCitation.xmldict_data_to_pb({"Citation": tag_sd["Citation"]})

        return Sample.SampleDescription(
            description=description,
            citation=citation,
        )

    #: Map for converting from XML value to protobuf enum.
    CONVERT_SOMATIC_VARIANT_IN_NORMAL_TISSUE: Dict[
        str, Sample.SomaticVariantInNormalTissue.ValueType
    ] = {
        "present": Sample.SomaticVariantInNormalTissue.SOMATIC_VARIANT_IN_NORMAL_TISSUE_PRESENT,
        "absent": Sample.SomaticVariantInNormalTissue.SOMATIC_VARIANT_IN_NORMAL_TISSUE_ABSENT,
        "not tested": Sample.SomaticVariantInNormalTissue.SOMATIC_VARIANT_IN_NORMAL_TISSUE_NOT_TESTED,
    }

    @classmethod
    def convert_somatic_variant_in_normal_tissue(
        cls, value: str
    ) -> Sample.SomaticVariantInNormalTissue.ValueType:
        """Converts a string to a ``Sample.SomaticVariantInNormalTissue.ValueType``.

        Args:
            value: The string.

        Returns:
            The ``Sample.SomaticVariantInNormalTissue.ValueType``.
        """
        result = cls.CONVERT_SOMATIC_VARIANT_IN_NORMAL_TISSUE.get(value)
        if not result:
            raise ValueError(f"Unknown value {value}")
        else:
            return result

    #: Map for converting from XML value to protobuf enum.
    CONVERT_AGE_UNIT: Dict[str, Sample.AgeUnit.ValueType] = {
        "days": Sample.AgeUnit.AGE_UNIT_DAYS,
        "weeks": Sample.AgeUnit.AGE_UNIT_WEEKS,
        "months": Sample.AgeUnit.AGE_UNIT_MONTHS,
        "years": Sample.AgeUnit.AGE_UNIT_YEARS,
        "weeks gestation": Sample.AgeUnit.AGE_UNIT_WEEKS_GESTATION,
        "months gestation": Sample.AgeUnit.AGE_UNIT_MONTHS_GESTATION,
    }

    @classmethod
    def convert_age_unit(cls, value: str) -> Sample.AgeUnit.ValueType:
        """Converts a string to a ``Sample.AgeUnit.ValueType``.

        Args:
            value: The string.

        Returns:
            The ``Sample.AgeUnit.ValueType``.
        """
        result = cls.CONVERT_AGE_UNIT.get(value)
        if not result:
            raise ValueError(f"Unknown value {value}")
        else:
            return result

    #: Map for converting from XML value to protobuf enum.
    CONVERT_AGE_TYPE: Dict[str, Sample.AgeType.ValueType] = {
        "minimum": Sample.AgeType.AGE_TYPE_MINIMUM,
        "maximum": Sample.AgeType.AGE_TYPE_MAXIMUM,
        "single": Sample.AgeType.AGE_TYPE_SINGLE,
    }

    @classmethod
    def convert_age_type(cls, value: str) -> Sample.AgeType.ValueType:
        """Converts a string to a ``Sample.AgeType.ValueType``.

        Args:
            value: The string.

        Returns:
            The ``Sample.AgeType.ValueType``.
        """
        result = cls.CONVERT_AGE_TYPE.get(value)
        if not result:
            raise ValueError(f"Unknown value {value}")
        else:
            return result

    #: Map for converting from XML value to protobuf enum.
    CONVERT_AFFECTED_STATUS: Dict[str, Sample.AffectedStatus.ValueType] = {
        "yes": Sample.AffectedStatus.AFFECTED_STATUS_YES,
        "no": Sample.AffectedStatus.AFFECTED_STATUS_NO,
        "not provided": Sample.AffectedStatus.AFFECTED_STATUS_NOT_PROVIDED,
        "unknown": Sample.AffectedStatus.AFFECTED_STATUS_UNKNOWN,
        "not applicable": Sample.AffectedStatus.AFFECTED_STATUS_NOT_APPLICABLE,
    }

    @classmethod
    def convert_affected_status(cls, value: str) -> Sample.AffectedStatus.ValueType:
        """Converts a string to a ``Sample.AffectedStatus.ValueType``.

        Args:
            value: The string.

        Returns:
            The ``Sample.AffectedStatus.ValueType``.
        """
        result = cls.CONVERT_AFFECTED_STATUS.get(value)
        if not result:
            raise ValueError(f"Unknown value {value}")
        else:
            return result

    @classmethod
    def convert_age(cls, tag: dict[str, Any]) -> Sample.Age:
        assert "Age" in tag
        tag_age: dict[str, Any] = tag["Age"]

        return Sample.Age(
            value=int(tag_age["#text"]),
            unit=cls.convert_age_unit(tag_age["@age_unit"]),
            type=cls.convert_age_type(tag_age["@Type"]),
        )

    #: Map for converting from XML value to protobuf enum.
    CONVERT_GENDER: Dict[str, Sample.Gender.ValueType] = {
        "male": Sample.Gender.GENDER_MALE,
        "female": Sample.Gender.GENDER_FEMALE,
        "mixed": Sample.Gender.GENDER_MIXED,
    }

    @classmethod
    def convert_gender(cls, value: str) -> Sample.Gender.ValueType:
        """Converts a string to a ``Sample.Gender.ValueType``.

        Args:
            value: The string.

        Returns:
            The ``Sample.Gender.ValueType``.
        """
        result = cls.CONVERT_GENDER.get(value)
        if not result:
            raise ValueError(f"Unknown value {value}")
        else:
            return result

    #: Map for converting from XML value to protobuf enum.
    CONVERT_SOURCE_TYPE: Dict[str, Sample.SourceType.ValueType] = {
        "submitter-generated": Sample.SourceType.SOURCE_TYPE_SUBMITTER_GENERATED,
        "data mining": Sample.SourceType.SOURCE_TYPE_DATA_MINING,
    }

    @classmethod
    def convert_source_type(cls, value: str) -> Sample.SourceType.ValueType:
        """Converts a string to a ``Sample.SourceType.ValueType``.

        Args:
            value: The string.

        Returns:
            The ``Sample.SourceType.ValueType``.
        """
        result = cls.CONVERT_SOURCE_TYPE.get(value)
        if not result:
            raise ValueError(f"Unknown value {value}")
        else:
            return result

    @classmethod
    def xmldict_data_to_pb(cls, value: dict[str, Any]) -> Sample:
        """Converts a dict from ``xmltodict`` to a ``Sample`` protobuf.

        Args:
            value: The dict from ``xmltodict``.

        Returns:
            The ``Sample`` protobuf.
        """
        assert "Sample" in value
        tag_sample: dict[str, Any] = value["Sample"]

        sample_description: Sample.SampleDescription | None = None
        if "SampleDescription" in tag_sample:
            sample_description = cls.convert_sample_description(tag_sample)

        origin: Origin.ValueType | None = None
        if "Origin" in tag_sample:
            origin = ConvertOrigin.xmldict_data_to_pb(ensure_str(tag_sample["Origin"]))

        ethnicity: str | None = tag_sample.get("Ethnicity")
        geographic_origin: str | None = tag_sample.get("GeographicOrigin")
        val_tissue: str | dict[str, str] | None = tag_sample.get("Tissue")
        if val_tissue:
            tissue = ensure_str(val_tissue)
        else:
            tissue = None
        somatic_variant_in_normal_tissue: Sample.SomaticVariantInNormalTissue.ValueType | None = (
            None
        )
        if "SomaticVariantInNormalTissue" in tag_sample:
            somatic_variant_in_normal_tissue = cls.convert_somatic_variant_in_normal_tissue(
                tag_sample["SomaticVariantInNormalTissue"]
            )
        somatic_variant_allele_fraction: str | None = None
        if "SomaticVariantAlleleFraction" in tag_sample:
            somatic_variant_allele_fraction = tag_sample["SomaticVariantAlleleFraction"]
        cell_line: str | None = tag_sample.get("CellLine")
        species: Species | None = None
        if "Species" in tag_sample:
            species = ConvertSpecies.xmldict_data_to_pb(tag_sample)
        ages: list[Sample.Age] | None = None
        if "Age" in tag_sample:
            ages = [cls.convert_age({"Age": entry}) for entry in cls.ensure_list(tag_sample["Age"])]
        strain: str | None = tag_sample.get("Strain")
        affected_status: Sample.AffectedStatus.ValueType | None = None
        if "AffectedStatus" in tag_sample:
            affected_status = cls.convert_affected_status(ensure_str(tag_sample["AffectedStatus"]))
        number_tested: int | None = None
        if "NumberTested" in tag_sample:
            number_tested = int(ensure_str(tag_sample["NumberTested"]))
        number_males: int | None = None
        if "NumberMales" in tag_sample:
            number_males = int(ensure_str(tag_sample["NumberMales"]))
        number_females: int | None = None
        if "NumberFemales" in tag_sample:
            number_females = int(ensure_str(tag_sample["NumberFemales"]))
        number_chr_tested: int | None = None
        if "NumberChrTested" in tag_sample:
            number_chr_tested = int(ensure_str(tag_sample["NumberChrTested"]))
        gender: Sample.Gender.ValueType | None = None
        if "Gender" in tag_sample:
            gender = cls.convert_gender(ensure_str(tag_sample["Gender"]))
        family_data: FamilyData | None = None
        if "FamilyData" in tag_sample:
            family_data = ConvertFamilyData.xmldict_data_to_pb(
                {"FamilyData": tag_sample["FamilyData"]}
            )
        proband: str | None = None
        if "Proband" in tag_sample:
            proband = tag_sample["Proband"]
        indication: Indication | None = None
        if "Indication" in tag_sample:
            indication = ConvertIndication.xmldict_data_to_pb(
                {"Indication": tag_sample["Indication"]}
            )
        cxcs = cls.parse_citations_xrefs_comments(tag_sample)
        source_type: Sample.SourceType.ValueType | None = None
        if "SourceType" in tag_sample:
            source_type = cls.convert_source_type(tag_sample["SourceType"])

        return Sample(
            sample_description=sample_description,
            origin=origin,
            ethnicity=ethnicity,
            geographic_origin=geographic_origin,
            tissue=tissue,
            somatic_variant_in_normal_tissue=somatic_variant_in_normal_tissue,
            somatic_variant_allele_fraction=somatic_variant_allele_fraction,
            cell_line=cell_line,
            species=species,
            ages=ages,
            strain=strain,
            affected_status=affected_status,
            numer_tested=number_tested,
            number_males=number_males,
            number_females=number_females,
            number_chr_tested=number_chr_tested,
            gender=gender,
            family_data=family_data,
            proband=proband,
            indication=indication,
            citations=cxcs.citations,
            xrefs=cxcs.xrefs,
            comments=cxcs.comments,
            source_type=source_type,
        )


class ConvertMethodType(ConverterBase):
    """Static method helper for converting XML data to to ``MethodType``."""

    #: Map for converting from XML value to protobuf enum.
    CONVERT_RESULT_TYPE: Dict[str, Method.ResultType.ValueType] = {
        "number of occurences": Method.ResultType.RESULT_TYPE_NUMBER_OF_OCCURRENCES,
        "p value": Method.ResultType.RESULT_TYPE_P_VALUE,
        "odds ratio": Method.ResultType.RESULT_TYPE_ODDS_RATIO,
        "variant call": Method.ResultType.RESULT_TYPE_VARIANT_CALL,
    }

    @classmethod
    def convert_result_type(cls, value: str) -> Method.ResultType.ValueType:
        """Converts a string to a ``Method.ResultType.ValueType``.

        Args:
            value: The string.

        Returns:
            The ``Method.ResultType.ValueType``.
        """
        result = cls.CONVERT_RESULT_TYPE.get(value)
        if not result:
            raise ValueError(f"Unknown value {value}")
        else:
            return result

    #: Map for converting from XML value to protobuf enum.
    CONVERT_SOURCE_TYPE: Dict[str, Method.SourceType.ValueType] = {
        "submitter-generated": Method.SourceType.SOURCE_TYPE_SUBMITTER_GENERATED,
        "data mining": Method.SourceType.SOURCE_TYPE_DATA_MINING,
        "data review": Method.SourceType.SOURCE_TYPE_DATA_REVIEW,
    }

    @classmethod
    def convert_source_type(cls, value: str) -> Method.SourceType.ValueType:
        """Converts a string to a ``Method.SourceType.ValueType``.

        Args:
            value: The string.

        Returns:
            The ``Method.SourceType.ValueType``.
        """
        result = cls.CONVERT_SOURCE_TYPE.get(value)
        if not result:
            raise ValueError(f"Unknown value {value}")
        else:
            return result

    #: Map for converting from XML value to protobuf enum.
    CONVERT_METHOD_ATTRIBUTE_TYPE: Dict[str, Method.MethodAttribute.AttributeType.ValueType] = {
        "Location": Method.MethodAttribute.AttributeType.ATTRIBUTE_TYPE_LOCATION,
        "ControlsAppropriate": Method.MethodAttribute.AttributeType.ATTRIBUTE_TYPE_CONTROLS_APPROPRIATE,
        "MethodAppropriate": Method.MethodAttribute.AttributeType.ATTRIBUTE_TYPE_METHOD_APPROPRIATE,
        "TestName": Method.MethodAttribute.AttributeType.ATTRIBUTE_TYPE_TEST_NAME,
        "StructVarMethodType": Method.MethodAttribute.AttributeType.ATTRIBUTE_TYPE_STRUCT_VAR_METHOD_TYPE,
        "ProbeAccession": Method.MethodAttribute.AttributeType.ATTRIBUTE_TYPE_PROBE_ACCESSION,
    }

    @classmethod
    def convert_method_attribute_type(
        cls, value: str
    ) -> Method.MethodAttribute.AttributeType.ValueType:
        """Converts a string to a ``Method.MethodAttribute.AttributeType.ValueType``.

        Args:
            value: The string.

        Returns:
            The ``Method.MethodAttribute.AttributeType.ValueType``.
        """
        result = cls.CONVERT_METHOD_ATTRIBUTE_TYPE.get(value)
        if not result:
            raise ValueError(f"Unknown value {value}")
        else:
            return result

    @classmethod
    def convert_method_attribute(cls, tag: dict[str, Any]) -> Method.MethodAttribute:
        """Converts a dict from ``xmltodict`` to a ``Method.MethodAttribute`` protobuf.

        Args:
            tag: The dict from ``xmltodict``.

        Returns:
            The ``Method.MethodAttribute`` protobuf.
        """
        assert "MethodAttribute" in tag
        tag_ma: dict[str, Any] = tag["MethodAttribute"]
        tag_attribute: dict[str, Any] = tag_ma["Attribute"]

        base: BaseAttribute = ConvertBaseAttribute.xmldict_data_to_pb(tag_ma)
        type_: Method.MethodAttribute.AttributeType.ValueType = cls.convert_method_attribute_type(
            tag_attribute["@Type"]
        )

        return Method.MethodAttribute(
            base=base,
            type=type_,
        )

    #: Map for converting from XML value to protobuf enum.
    CONVERT_OBS_METHOD_ATTRIBUTE_TYPE: Dict[
        str, Method.ObsMethodAttribute.AttributeType.ValueType
    ] = {
        "MethodResult": Method.ObsMethodAttribute.AttributeType.ATTRIBUTE_TYPE_METHOD_RESULT,
        "TestingLaboratory": Method.ObsMethodAttribute.AttributeType.ATTRIBUTE_TYPE_TESTING_LABORATORY,
    }

    @classmethod
    def convert_obs_method_attribute_type(
        cls, value: str
    ) -> Method.ObsMethodAttribute.AttributeType.ValueType:
        """Converts a string to a ``Method.ObsMethodAttribute.AttributeType.ValueType``.

        Args:
            value: The string.

        Returns:
            The ``Method.ObsMethodAttribute.AttributeType.ValueType``.
        """
        result = cls.CONVERT_OBS_METHOD_ATTRIBUTE_TYPE.get(value)
        if not result:
            raise ValueError(f"Unknown value {value}")
        else:
            return result

    @classmethod
    def convert_obs_method_attribute(cls, tag: dict[str, Any]) -> Method.ObsMethodAttribute:
        """Converts a dict from ``xmltodict`` to a ``Method.ObsMethodAttribute`` protobuf.

        Args:
            tag: The dict from ``xmltodict``.

        Returns:
            The ``Method.ObsMethodAttribute`` protobuf.
        """
        assert "ObsMethodAttribute" in tag
        tag_ma: dict[str, Any] = tag["ObsMethodAttribute"]
        tag_attribute: dict[str, Any] = tag_ma["Attribute"]

        base: BaseAttribute = ConvertBaseAttribute.xmldict_data_to_pb(tag_ma)
        type_: Method.ObsMethodAttribute.AttributeType.ValueType = (
            cls.convert_obs_method_attribute_type(tag_attribute["@Type"])
        )
        comments: list[Comment] | None = None
        if "Comment" in tag_ma:
            comments = [
                ConvertComment.xmldict_data_to_pb({"Comment": entry})
                for entry in cls.ensure_list(tag_ma["Comment"])
            ]

        return Method.ObsMethodAttribute(
            base=base,
            type=type_,
            comments=comments,
        )

    @classmethod
    def xmldict_data_to_pb(cls, tag: dict[str, Any]) -> Method:
        """Converts a dict from ``xmltodict`` to a ``MethodType`` protobuf.

        Args:
            tag: The dict from ``xmltodict``.

        Returns:
            The ``MethodType`` protobuf.
        """
        assert "Method" in tag
        tag_method: dict[str, Any] = tag["Method"]

        name_platform: str | None = None
        if "NamePlatform" in tag_method:
            name_platform = tag_method["NamePlatform"]
        type_platform: str | None = None
        if "TypePlatform" in tag_method:
            type_platform = tag_method["TypePlatform"]
        purpose: str | None = None
        if "Purpose" in tag_method:
            purpose = tag_method["Purpose"]
        result_type: Method.ResultType.ValueType | None = None
        if "ResultType" in tag_method:
            result_type = cls.convert_result_type(tag_method["ResultType"])
        min_reported: str | None = None
        if "MinReported" in tag_method:
            min_reported = tag_method["MinReported"]
        max_reported: str | None = None
        if "MaxReported" in tag_method:
            max_reported = tag_method["MaxReported"]
        reference_standard: str | None = None
        if "ReferenceStandard" in tag_method:
            reference_standard = tag_method["ReferenceStandard"]
        citations: list[Citation] | None = None
        if "Citation" in tag_method:
            citations = [
                ConvertCitation.xmldict_data_to_pb({"Citation": entry})
                for entry in cls.ensure_list(tag_method["Citation"])
            ]
        xrefs: list[Xref] | None = None
        if "XRef" in tag_method:
            xrefs = [
                ConvertXref.xmldict_data_to_pb({"XRef": entry})
                for entry in cls.ensure_list(tag_method["XRef"])
            ]
        description: str | None = None
        if "Description" in tag_method:
            description = tag_method["Description"]
        software: list[Software] | None = None
        if "Software" in tag_method:
            software = [
                ConvertSoftware.xmldict_data_to_pb({"Software": element})
                for element in cls.ensure_list(tag_method["Software"])
            ]
        source_type: Method.SourceType.ValueType | None = None
        if "SourceType" in tag_method:
            source_type = cls.convert_source_type(tag_method["SourceType"])
        method_type: MethodListType.ValueType = ConvertMethodListType.xmldict_data_to_pb(
            tag_method["MethodType"]
        )
        method_attributes: list[Method.MethodAttribute] | None = None
        if "MethodAttribute" in tag_method:
            method_attributes = [
                cls.convert_method_attribute({"MethodAttribute": entry})
                for entry in cls.ensure_list(tag_method["MethodAttribute"])
            ]
        obs_method_attributes: list[Method.ObsMethodAttribute] | None = None
        if "ObsMethodAttribute" in tag_method:
            obs_method_attributes = [
                cls.convert_obs_method_attribute({"ObsMethodAttribute": entry})
                for entry in cls.ensure_list(tag_method["ObsMethodAttribute"])
            ]

        return Method(
            name_platform=name_platform,
            type_platform=type_platform,
            purpose=purpose,
            result_type=result_type,
            min_reported=min_reported,
            max_reported=max_reported,
            reference_standard=reference_standard,
            citations=citations,
            xrefs=xrefs,
            description=description,
            software=software,
            source_type=source_type,
            method_type=method_type,
            method_attributes=method_attributes,
            obs_method_attributes=obs_method_attributes,
        )


class ConvertAlleleScv(ConverterBase):
    """Static method helper for converting XML data to to ``AlleleScv``."""

    @classmethod
    def convert_gene(cls, tag: dict[str, Any]) -> AlleleScv.Gene:
        """Converts a dict from ``xmltodict`` to a ``AlleleScv.Gene`` protobuf.

        Args:
            tag: The dict from ``xmltodict``.

        Returns:
            The ``AlleleScv.Gene`` protobuf.
        """
        assert "Gene" in tag
        tag_gene: dict[str, Any] = tag["Gene"]

        name: str | None = None
        if "Name" in tag_gene:
            assert isinstance(tag_gene["Name"], str)
            name = tag_gene["Name"]
        properties: list[str] | None = None
        if "Property" in tag_gene:
            properties = [entry for entry in cls.ensure_list(tag_gene["Property"])]
        xrefs: list[Xref] | None = None
        if "XRef" in tag_gene:
            xrefs = [
                ConvertXref.xmldict_data_to_pb({"XRef": entry})
                for entry in cls.ensure_list(tag_gene["XRef"])
            ]
        symbol: str | None = None
        if "@Symbol" in tag_gene:
            symbol = tag_gene["@Symbol"]
        relationship_type: GeneVariantRelationship.ValueType | None = None
        if "@RelationshipType" in tag_gene:
            relationship_type = ConvertGeneVariantRelationship.xmldict_data_to_pb(
                tag_gene["@RelationshipType"]
            )

        return AlleleScv.Gene(
            name=name,
            properties=properties,
            xrefs=xrefs,
            symbol=symbol,
            relationship_type=relationship_type,
        )

    @classmethod
    def convert_molecular_consequence(cls, tag: dict[str, Any]) -> AlleleScv.MolecularConsequence:
        """Converts a dict from ``xmltodict`` to a ``AlleleScv.MolecularConsequence`` protobuf.

        Args:
            tag: The dict from ``xmltodict``.

        Returns:
            The ``AlleleScv.MolecularConsequence`` protobuf.
        """
        assert "MolecularConsequence" in tag
        tag_mc: dict[str, Any] = tag["MolecularConsequence"]

        cxcs: CitationsXrefsComments = cls.parse_citations_xrefs_comments(tag_mc)

        rs: int | None = None
        if "@RS" in tag_mc:
            rs = int(tag_mc["@RS"])
        hgvs: str | None = None
        if "@HGVS" in tag_mc:
            hgvs = tag_mc["@HGVS"]
        so_id: str | None = None
        if "@SOid" in tag_mc:
            so_id = tag_mc["@SOid"]
        function: str = tag_mc["@Function"]

        return AlleleScv.MolecularConsequence(
            rs=rs,
            hgvs=hgvs,
            so_id=so_id,
            function=function,
            citations=cxcs.citations,
            xrefs=cxcs.xrefs,
            comments=cxcs.comments,
        )

    @classmethod
    def xmldict_data_to_pb(cls, value: dict[str, Any]) -> AlleleScv:  # noqa: C901
        """Converts a dict from ``xmltodict`` to a ``AlleleScv`` protobuf.

        Args:
            value: The dict from ``xmltodict``.

        Returns:
            The ``AlleleScv`` protobuf.
        """
        assert "SimpleAllele" in value
        tag_sa: dict[str, Any] = value["SimpleAllele"]

        genes: list[AlleleScv.Gene] | None = None
        if "GeneList" in tag_sa and "Gene" in tag_sa["GeneList"]:
            genes = [
                cls.convert_gene({"Gene": entry})
                for entry in cls.ensure_list(tag_sa["GeneList"]["Gene"])
            ]
        names: list[OtherName] | None = None
        if "Name" in tag_sa:
            names = [
                ConvertOtherName.xmldict_data_to_pb({"Name": entry})
                for entry in cls.ensure_list(tag_sa["Name"])
            ]
        variant_type: str | None = tag_sa.get("VariantType")
        location: Location | None = None
        if "Location" in tag_sa:
            location = ConvertLocation.xmldict_data_to_pb({"Location": tag_sa["Location"]})
        other_names: list[OtherName] | None = None
        if "OtherNameList" in tag_sa and "Name" in tag_sa["OtherNameList"]:
            other_names = [
                ConvertOtherName.xmldict_data_to_pb({"Name": entry})
                for entry in cls.ensure_list(tag_sa["OtherNameList"]["Name"])
            ]
        protein_changes: list[str] | None = None
        if "ProteinChange" in tag_sa:
            protein_changes = [entry for entry in cls.ensure_list(tag_sa["ProteinChange"])]

        # parse out citations
        citations: list[Citation] | None = None
        if "CitationList" not in tag_sa or "Citation" not in tag_sa["CitationList"]:
            pass
        elif isinstance(tag_sa["CitationList"]["Citation"], list):
            citations = [
                ConvertCitation.xmldict_data_to_pb({"Citation": entry})
                for entry in tag_sa["CitationList"]["Citation"]
            ]
        elif isinstance(tag_sa["CitationList"]["Citation"], dict):
            citations = [
                ConvertCitation.xmldict_data_to_pb({"Citation": tag_sa["CitationList"]["Citation"]})
            ]
        else:
            assert False, f"Invalid type for Citation {tag_sa['Citation']}"
        # parse out xrefs
        xrefs: list[Xref] | None = None
        if "XRefList" not in tag_sa or "XRef" not in tag_sa["XRefList"]:
            pass
        elif isinstance(tag_sa["XRefList"]["XRef"], list):
            xrefs = [
                ConvertXref.xmldict_data_to_pb({"XRef": entry})
                for entry in tag_sa["XRefList"]["XRef"]
            ]
        elif isinstance(tag_sa["XRefList"]["XRef"], dict):
            xrefs = [ConvertXref.xmldict_data_to_pb({"XRef": tag_sa["XRefList"]["XRef"]})]
        else:
            assert False, f"Invalid type for XRef {tag_sa['XRef']}"
        # parse out comments
        comments: list[Comment] | None = None
        if "Comment" not in tag_sa:
            pass
        elif isinstance(tag_sa["Comment"], list):
            comments = [
                ConvertComment.xmldict_data_to_pb({"Comment": entry}) for entry in tag_sa["Comment"]
            ]
        elif isinstance(tag_sa["Comment"], (str, dict)):
            comments = [ConvertComment.xmldict_data_to_pb({"Comment": tag_sa["Comment"]})]
        else:
            assert False, f"Invalid type for comment {tag_sa['Comment']}"

        molecular_consequences: list[AlleleScv.MolecularConsequence] | None = None
        if (
            "MolecularConsequenceList" in tag_sa
            and "MolecularConsequence" in tag_sa["MolecularConsequenceList"]
        ):
            molecular_consequences = [
                cls.convert_molecular_consequence(entry)
                for entry in cls.ensure_list(tag_sa["MolecularConsequenceList"])
            ]
        functional_consequences: list[FunctionalConsequence] | None = None
        if "FunctionalConsequence" in tag_sa:
            functional_consequences = [
                ConvertFunctionalConsequence.xmldict_data_to_pb({"FunctionalConsequence": entry})
                for entry in cls.ensure_list(tag_sa["FunctionalConsequence"])
            ]
        attributes: list[AttributeSetElement] | None = None
        if "AttributeSet" in tag_sa:
            attributes = [
                ConvertAttributeSetElement.xmldict_data_to_pb({"AttributeSet": entry})
                for entry in cls.ensure_list(tag_sa["AttributeSet"])
            ]
        allele_id: int | None = None
        if "@AlleleID" in tag_sa:
            allele_id = int(tag_sa["@AlleleID"])

        return AlleleScv(
            genes=genes,
            names=names,
            variant_type=variant_type,
            location=location,
            other_names=other_names,
            protein_changes=protein_changes,
            xrefs=xrefs,
            citations=citations,
            comments=comments,
            molecular_consequences=molecular_consequences,
            functional_consequences=functional_consequences,
            attributes=attributes,
            allele_id=allele_id,
        )


class ConvertHaplotypeScv(ConverterBase):
    """Static method helper for converting XML data to to ``HaplotypeScv``."""

    @classmethod
    def xmldict_data_to_pb(cls, tag: dict[str, Any]) -> HaplotypeScv:
        """Converts a dict from ``xmltodict`` to a `HaplotypeScv`` protobuf.

        Args:
            tag: The dict from ``xmltodict``.

        Returns:
            The `HaplotypeScv`` protobuf.
        """
        assert "Haplotype" in tag
        tag_genotype: dict[str, Any] = tag["Haplotype"]

        simple_alleles: list[AlleleScv] | None = None
        if "SimpleAllele" in tag_genotype:
            simple_alleles = [
                ConvertAlleleScv.xmldict_data_to_pb({"SimpleAllele": entry})
                for entry in cls.ensure_list(tag_genotype["SimpleAllele"])
            ]
        name: str | None = tag_genotype.get("Name")
        other_names: list[OtherName] | None = None
        if "OtherNameList" in tag_genotype:
            other_names = [
                ConvertOtherName.xmldict_data_to_pb({"Name": entry})
                for entry in cls.ensure_list(tag_genotype["OtherNameList"]["Name"])
            ]
        classification: AggregateClassificationSet | None = None
        if "Classification" in tag_genotype:
            classification = ConvertAggregateClassificationSet.xmldict_data_to_pb(
                tag_genotype["Classification"]
            )
        functional_consequences: list[FunctionalConsequence] | None = None
        if "FunctionalConsequence" in tag_genotype:
            functional_consequences = [
                ConvertFunctionalConsequence.xmldict_data_to_pb({"FunctionalConsequence": entry})
                for entry in cls.ensure_list(tag_genotype["FunctionalConsequence"])
            ]
        attributes: list[AttributeSetElement] | None = None
        if "AttributeSet" in tag_genotype:
            attributes = [
                ConvertAttributeSetElement.xmldict_data_to_pb({"AttributeSet": entry})
                for entry in cls.ensure_list(tag_genotype["AttributeSet"])
            ]
        citations: list[Citation] | None = None
        if "CitationList" in tag_genotype and "Citation" in tag_genotype["CitationList"]:
            citations = [
                ConvertCitation.xmldict_data_to_pb({"Citation": entry})
                for entry in cls.ensure_list(tag_genotype["CitationList"]["Citation"])
            ]
        xrefs: list[Xref] | None = None
        if "XRefList" in tag_genotype and "XRef" in tag_genotype["XRefList"]:
            xrefs = [
                ConvertXref.xmldict_data_to_pb({"XRef": entry})
                for entry in cls.ensure_list(tag_genotype["XRefList"]["XRef"])
            ]
        comments: list[Comment] | None = None
        if "Comment" in tag_genotype:
            comments = [
                ConvertComment.xmldict_data_to_pb({"Comment": entry})
                for entry in cls.ensure_list(tag_genotype["Comment"])
            ]
        variation_id: int | None = None
        if "@VariationID" in tag_genotype:
            variation_id = int(tag_genotype["@VariationID"])
        number_of_copies: int | None = None
        if "@NumberOfCopies" in tag_genotype:
            number_of_copies = int(tag_genotype["@NumberOfCopies"])
        number_of_chromosomes: int | None = None
        if "@NumberOfChromosomes" in tag_genotype:
            number_of_chromosomes = int(tag_genotype["@NumberOfChromosomes"])

        return HaplotypeScv(
            simple_alleles=simple_alleles,
            name=name,
            other_names=other_names,
            classification=classification,
            functional_consequences=functional_consequences,
            attributes=attributes,
            citations=citations,
            xrefs=xrefs,
            comments=comments,
            variation_id=variation_id,
            number_of_copies=number_of_copies,
            number_of_chromosomes=number_of_chromosomes,
        )


class ConvertGenotypeScv(ConverterBase):
    """Static method helper for converting XML data to to ``GenotypeScv``."""

    @classmethod
    def xmldict_data_to_pb(cls, tag: dict[str, Any]) -> GenotypeScv:
        """Converts a dict from ``xmltodict`` to a `GenotypeScv`` protobuf.

        Args:
            tag: The dict from ``xmltodict``.

        Returns:
            The `GenotypeScv`` protobuf.
        """
        assert "Genotype" in tag
        tag_genotype: dict[str, Any] = tag["Genotype"]

        simple_alleles: list[AlleleScv] | None = None
        if "SimpleAllele" in tag_genotype:
            simple_alleles = [
                ConvertAlleleScv.xmldict_data_to_pb({"SimpleAllele": entry})
                for entry in cls.ensure_list(tag_genotype["SimpleAllele"])
            ]
        haplotypes: list[HaplotypeScv] | None = None
        if "Haplotype" in tag_genotype:
            haplotypes = [
                ConvertHaplotypeScv.xmldict_data_to_pb({"Haplotype": entry})
                for entry in cls.ensure_list(tag_genotype["Haplotype"])
            ]
        name: str | None = tag_genotype.get("Name")
        other_names: list[OtherName] | None = None
        if "OtherNameList" in tag_genotype:
            other_names = [
                ConvertOtherName.xmldict_data_to_pb({"Name": entry})
                for entry in cls.ensure_list(tag_genotype["OtherNameList"]["Name"])
            ]
        variation_type: VariationType.ValueType = ConvertVariationType.xmldict_data_to_pb(
            tag_genotype["VariationType"]
        )
        functional_consequences: list[FunctionalConsequence] | None = None
        if "FunctionalConsequence" in tag_genotype:
            functional_consequences = [
                ConvertFunctionalConsequence.xmldict_data_to_pb({"FunctionalConsequence": entry})
                for entry in cls.ensure_list(tag_genotype["FunctionalConsequence"])
            ]
        attributes: list[AttributeSetElement] | None = None
        if "AttributeSet" in tag_genotype:
            attributes = [
                ConvertAttributeSetElement.xmldict_data_to_pb({"AttributeSet": entry})
                for entry in cls.ensure_list(tag_genotype["AttributeSet"])
            ]
        citations: list[Citation] | None = None
        if "CitationList" in tag_genotype and "Citation" in tag_genotype["CitationList"]:
            citations = [
                ConvertCitation.xmldict_data_to_pb({"Citation": entry})
                for entry in cls.ensure_list(tag_genotype["CitationList"]["Citation"])
            ]
        xrefs: list[Xref] | None = None
        if "XRefList" in tag_genotype and "XRef" in tag_genotype["XRefList"]:
            xrefs = [
                ConvertXref.xmldict_data_to_pb({"XRef": entry})
                for entry in cls.ensure_list(tag_genotype["XRefList"]["XRef"])
            ]
        comments: list[Comment] | None = None
        if "Comment" in tag_genotype:
            comments = [
                ConvertComment.xmldict_data_to_pb({"Comment": entry})
                for entry in cls.ensure_list(tag_genotype["Comment"])
            ]
        variation_id: int | None = None

        return GenotypeScv(
            simple_alleles=simple_alleles,
            haplotypes=haplotypes,
            name=name,
            other_names=other_names,
            variation_type=variation_type,
            functional_consequences=functional_consequences,
            attributes=attributes,
            citations=citations,
            xrefs=xrefs,
            comments=comments,
            variation_id=variation_id,
        )


class ConvertObservedIn(ConverterBase):
    """Static method helper for converting XML data to to ``ObservedIn``."""

    #: Map for converting from XML value to protobuf enum.
    CONVERT_METHOD_TYPE: Dict[str, ObservedIn.MethodType.ValueType] = {
        "literature only": ObservedIn.MethodType.METHOD_TYPE_LITERATURE_ONLY,
        "reference population": ObservedIn.MethodType.METHOD_TYPE_REFERENCE_POPULATION,
        "case-control": ObservedIn.MethodType.METHOD_TYPE_CASE_CONTROL,
        "clinical testing": ObservedIn.MethodType.METHOD_TYPE_CLINICAL_TESTING,
        "in vitro": ObservedIn.MethodType.METHOD_TYPE_IN_VITRO,
        "in vivo": ObservedIn.MethodType.METHOD_TYPE_IN_VIVO,
        "inferred from source": ObservedIn.MethodType.METHOD_TYPE_INFERRED_FROM_SOURCE,
        "research": ObservedIn.MethodType.METHOD_TYPE_RESEARCH,
    }

    @classmethod
    def convert_method_type(cls, value: str) -> ObservedIn.MethodType.ValueType:
        """Converts a string to a ``ObservedIn.MethodType.ValueType``.

        Args:
            value: The string.

        Returns:
            The ``ObservedIn.MethodType.ValueType``.
        """
        result = cls.CONVERT_METHOD_TYPE.get(value)
        if not result:
            raise ValueError(f"Unknown value {value}")
        else:
            return result

    #: Map for converting from XML value to protobuf enum.
    CONVERT_OBSERVED_DATA_ATTRIBUTE_TYPE: Dict[
        str, ObservedIn.ObservedDataAttribute.Type.ValueType
    ] = {
        "Description": ObservedIn.ObservedDataAttribute.Type.TYPE_DESCRIPTION,
        "VariantAlleles": ObservedIn.ObservedDataAttribute.Type.TYPE_VARIANT_ALLELES,
        "SubjectsWithVariant": ObservedIn.ObservedDataAttribute.Type.TYPE_SUBJECTS_WITH_VARIANT,
        "SubjectsWithDifferentCausativeVariant": ObservedIn.ObservedDataAttribute.Type.TYPE_SUBJECTS_WITH_DIFFERENT_CAUSATIVE_VARIANT,
        "VariantChromosomes": ObservedIn.ObservedDataAttribute.Type.TYPE_VARIANT_CHROMOSOMES,
        "IndependentObservations": ObservedIn.ObservedDataAttribute.Type.TYPE_INDEPENDENT_OBSERVATIONS,
        "SingleHeterozygote": ObservedIn.ObservedDataAttribute.Type.TYPE_SINGLE_HETEROZYGOUS,
        "CompoundHeterozygote": ObservedIn.ObservedDataAttribute.Type.TYPE_COMPOUND_HETEROZYGOUS,
        "Homozygote": ObservedIn.ObservedDataAttribute.Type.TYPE_HOMOZYGOUS,
        "Hemizygote": ObservedIn.ObservedDataAttribute.Type.TYPE_HEMIZYGOUS,
        "NumberMosaic": ObservedIn.ObservedDataAttribute.Type.TYPE_NUMBER_MOSAIC,
        "ObservedUnspecified": ObservedIn.ObservedDataAttribute.Type.TYPE_OBSERVED_UNSPECIFIED,
        "AlleleFrequency": ObservedIn.ObservedDataAttribute.Type.TYPE_ALLELE_FREQUENCY,
        "SecondaryFinding": ObservedIn.ObservedDataAttribute.Type.TYPE_SECONDARY_FINDING,
        "GenotypeAndMOIConsistent": ObservedIn.ObservedDataAttribute.Type.TYPE_GENOTYPE_AND_MOI_CONSISTENT,
        "UnaffectedFamilyMemberWithCausativeVariant": ObservedIn.ObservedDataAttribute.Type.TYPE_UNAFFECTED_FAMILY_MEMBER_WITH_CAUSATIVE_VARIANT,
        "HetParentTransmitNormalAllele": ObservedIn.ObservedDataAttribute.Type.TYPE_HET_PARENT_TRANSMIT_NORMAL_ALLELE,
        "CosegregatingFamilies": ObservedIn.ObservedDataAttribute.Type.TYPE_COSEGREGATING_FAMILIES,
        "InformativeMeioses": ObservedIn.ObservedDataAttribute.Type.TYPE_INFORMATIVE_MEIOSES,
        "SampleLocalID": ObservedIn.ObservedDataAttribute.Type.TYPE_SAMPLE_LOCAL_ID,
        "SampleVariantID": ObservedIn.ObservedDataAttribute.Type.TYPE_SAMPLE_VARIANT_ID,
        "FamilyHistory": ObservedIn.ObservedDataAttribute.Type.TYPE_FAMILY_HISTORY,
        "NumFamiliesWithVariant": ObservedIn.ObservedDataAttribute.Type.TYPE_NUM_FAMILIES_WITH_VARIANT,
        "NumFamiliesWithSegregationObserved": ObservedIn.ObservedDataAttribute.Type.TYPE_NUM_FAMILIES_WITH_SEGREGATION_OBSERVED,
        "SegregationObserved": ObservedIn.ObservedDataAttribute.Type.TYPE_SEGREGATION_OBSERVED,
    }

    @classmethod
    def convert_observed_data_attribute_type(
        cls, value: str
    ) -> ObservedIn.ObservedDataAttribute.Type.ValueType:
        """Converts a string to a ``ObservedIn.ObservedDataAttribute.Type``.

        Args:
            value: The string.

        Returns:
            The ``ObservedIn.ObservedDataAttribute.Type``.
        """
        result = cls.CONVERT_OBSERVED_DATA_ATTRIBUTE_TYPE.get(value)
        if not result:
            raise ValueError(f"Unknown value {value}")
        else:
            return result

    @classmethod
    def convert_observed_data_attribute(
        cls, tag: dict[str, Any]
    ) -> ObservedIn.ObservedDataAttribute:
        """Converts a dict from ``xmltodict`` to a ``ObservedIn.ObservedDataAttribute`` protobuf.

        Args:
            tag: The dict from ``xmltodict``.

        Returns:
            The ``ObservedIn.ObservedDataAttribute`` protobuf.
        """
        assert "Attribute" in tag
        tag_attribute: dict[str, Any] = tag["Attribute"]

        base: BaseAttribute = ConvertBaseAttribute.xmldict_data_to_pb(tag)
        type: ObservedIn.ObservedDataAttribute.Type.ValueType = (
            cls.convert_observed_data_attribute_type(tag_attribute["@Type"])
        )

        return ObservedIn.ObservedDataAttribute(
            base=base,
            type=type,
        )

    @classmethod
    def convert_observed_data(cls, tag: dict[str, Any]) -> ObservedIn.ObservedData:
        """Converts a dict from ``xmltodict`` to a ``ObservedIn.ObservedData`` protobuf.

        Args:
            tag: The dict from ``xmltodict``.

        Returns:
            The ``ObservedIn.ObservedData`` protobuf.
        """
        assert "ObservedData" in tag
        tag_od: dict[str, Any] = tag["ObservedData"]

        attributes: list[ObservedIn.ObservedDataAttribute] | None = None
        if "Attribute" in tag_od:
            attributes = [
                cls.convert_observed_data_attribute({"Attribute": entry})
                for entry in cls.ensure_list(tag_od["Attribute"])
            ]
        severity: Severity.ValueType | None = None
        if "Severity" in tag_od:
            severity = ConvertSeverity.xmldict_data_to_pb(tag_od["Severity"])
        cxcs: CitationsXrefsComments = cls.parse_citations_xrefs_comments(tag_od)

        return ObservedIn.ObservedData(
            attributes=attributes,
            severity=severity,
            citations=cxcs.citations,
            xrefs=cxcs.xrefs,
            comments=cxcs.comments,
        )

    @classmethod
    def xmldict_data_to_pb(cls, tag: dict[str, Any]) -> ObservedIn:
        """Converts a dict from ``xmltodict`` to a `ObservedIn`` protobuf.

        Args:
            tag: The dict from ``xmltodict``.

        Returns:
            The `ObservedIn`` protobuf.
        """
        assert "ObservedIn" in tag
        tag_observed_in: dict[str, Any] = tag["ObservedIn"]

        cxcs: CitationsXrefsComments = cls.parse_citations_xrefs_comments(tag_observed_in)

        sample: Sample = ConvertSample.xmldict_data_to_pb(tag_observed_in)
        observed_data: list[ObservedIn.ObservedData] | None = None
        if "ObservedData" in tag_observed_in:
            observed_data = [
                cls.convert_observed_data({"ObservedData": entry})
                for entry in cls.ensure_list(tag_observed_in["ObservedData"])
            ]
        trait_set: TraitSet | None = None
        if "TraitSet" in tag_observed_in:
            trait_set = ConvertTraitSet.xmldict_data_to_pb(
                {"TraitSet": tag_observed_in["TraitSet"]}
            )

        return ObservedIn(
            sample=sample,
            observed_data=observed_data,
            trait_set=trait_set,
            citations=cxcs.citations,
            xrefs=cxcs.xrefs,
            comments=cxcs.comments,
        )


class ConvertClinicalAssertion(ConverterBase):
    """Static method helper for converting XML data to to ``ClinicalAssertion``."""

    @classmethod
    def convert_clinvar_submission_id(
        cls, tag: dict[str, Any]
    ) -> ClinicalAssertion.ClinvarSubmissionId:
        """Converts a dict from ``xmltodict`` to a ``ClinicalAssertion.ClinvarSubmissionId`` protobuf.

        Args:
            tag: The dict from ``xmltodict``.

        Returns:
            The ``ClinicalAssertion.ClinvarSubmissionId`` protobuf.
        """
        assert "ClinVarSubmissionID" in tag

        local_key: str = tag["ClinVarSubmissionID"]["@localKey"]
        title: str | None = tag["ClinVarSubmissionID"].get("@title")
        local_key_is_submitted: bool | None = None
        if "@localKeyIsSubmitted" in tag["ClinVarSubmissionID"]:
            local_key_is_submitted = (
                tag["ClinVarSubmissionID"].get("@localKeyIsSubmitted") == "true"
            )
        submitted_assembly: str | None = tag["ClinVarSubmissionID"].get("@submittedAssembly")

        return ClinicalAssertion.ClinvarSubmissionId(
            local_key=local_key,
            title=title,
            local_key_is_submitted=local_key_is_submitted,
            submitted_assembly=submitted_assembly,
        )

    #: Map for converting from XML value to protobuf enum.
    CONVERT_ATTRIBUTE_SET_TYPE: Dict[str, ClinicalAssertion.AttributeSetElement.Type.ValueType] = {
        "ModeOfInheritance": ClinicalAssertion.AttributeSetElement.Type.TYPE_MODE_OF_INHERITANCE,
        "Penetrance": ClinicalAssertion.AttributeSetElement.Type.TYPE_PENETRANCE,
        "AgeOfOnset": ClinicalAssertion.AttributeSetElement.Type.TYPE_AGE_OF_ONSET,
        "Severity": ClinicalAssertion.AttributeSetElement.Type.TYPE_SEVERITY,
        "ClassificationHistory": ClinicalAssertion.AttributeSetElement.Type.TYPE_CLASSIFICATION_HISTORY,
        "SeverityDescription": ClinicalAssertion.AttributeSetElement.Type.TYPE_SEVERITY_DESCRIPTION,
        "AssertionMethod": ClinicalAssertion.AttributeSetElement.Type.TYPE_ASSERTION_METHOD,
    }

    @classmethod
    def convert_attribute_set_type(
        cls, value: str
    ) -> ClinicalAssertion.AttributeSetElement.Type.ValueType:
        """Converts a string to a ``ClinicalAssertion.AttributeSetElement.Type.ValueType``.

        Args:
            value: The string.

        Returns:
            The ``ClinicalAssertion.AttributeSetElement.Type.ValueType``.
        """
        result = cls.CONVERT_ATTRIBUTE_SET_TYPE.get(value)
        if not result:
            raise ValueError(f"Unknown value {value}")
        else:
            return result

    @classmethod
    def convert_attribute_set(cls, tag: dict[str, Any]) -> ClinicalAssertion.AttributeSetElement:
        """Converts a dict from ``xmltodict`` to a ``ClinicalAssertion.AttributeSetElement`` protobuf.

        Args:
            tag: The dict from ``xmltodict``.

        Returns:
            The ``ClinicalAssertion.AttributeSetElement`` protobuf.
        """
        assert "AttributeSet" in tag
        tag_as = tag["AttributeSet"]
        tag_attribute = tag_as["Attribute"]

        # Parse out the augmented BaseAttribute.
        cls.assert_keys(tag_attribute, ["@Type"])
        attribute = ConvertBaseAttribute.xmldict_data_to_pb({"Attribute": tag_attribute})
        type_: ClinicalAssertion.AttributeSetElement.Type.ValueType = (
            cls.convert_attribute_set_type(tag_attribute["@Type"])
        )
        # Parse out Citation, XRef, Comment tags.
        cxcs = cls.parse_citations_xrefs_comments(tag_as)

        return ClinicalAssertion.AttributeSetElement(
            attribute=attribute,
            type=type_,
            citations=cxcs.citations,
            xrefs=cxcs.xrefs,
            comments=cxcs.comments,
        )

    @classmethod
    def convert_clinvar_accession(cls, tag: dict[str, Any]) -> ClinicalAssertion.ClinvarAccession:
        """Converts a dict from ``xmltodict`` to a ``ClinicalAssertion.ClinvarAccession`` protobuf.

        Args:
            tag: The dict from ``xmltodict``.

        Returns:
            The ``ClinicalAssertion.ClinvarAccession`` protobuf.
        """
        assert "ClinVarAccession" in tag
        tag_cva = tag["ClinVarAccession"]

        accession: str = tag_cva["@Accession"]
        version: int = int(tag_cva["@Version"])
        submitter_identifiers: SubmitterIdentifiers = (
            ConvertSubmitterIdentifiers.xmldict_data_to_pb(tag, "ClinVarAccession")
        )
        date_updated: google.protobuf.timestamp_pb2.Timestamp | None = None
        if "@DateUpdated" in tag_cva:
            dt_date_updated = dateutil.parser.parse(tag_cva["@DateUpdated"])
            seconds_date_updated = int(time.mktime(dt_date_updated.timetuple()))
            date_updated = google.protobuf.timestamp_pb2.Timestamp(seconds=seconds_date_updated)
        date_created: google.protobuf.timestamp_pb2.Timestamp | None = None
        if "@DateCreated" in tag_cva:
            dt_date_created = dateutil.parser.parse(tag_cva["@DateCreated"])
            seconds_date_created = int(time.mktime(dt_date_created.timetuple()))
            date_created = google.protobuf.timestamp_pb2.Timestamp(seconds=seconds_date_created)

        return ClinicalAssertion.ClinvarAccession(
            accession=accession,
            version=version,
            submitter_identifiers=submitter_identifiers,
            date_updated=date_updated,
            date_created=date_created,
        )

    #: Map for converting from XML value to protobuf enum.
    CONVERT_RECORD_STATUS: Dict[str, ClinicalAssertion.RecordStatus.ValueType] = {
        "current": ClinicalAssertion.RecordStatus.RECORD_STATUS_CURRENT,
        "replaced": ClinicalAssertion.RecordStatus.RECORD_STATUS_REPLACED,
        "removed": ClinicalAssertion.RecordStatus.RECORD_STATUS_REMOVED,
    }

    @classmethod
    def convert_record_status(cls, value: str) -> ClinicalAssertion.RecordStatus.ValueType:
        """Converts a string to a ``ClinicalAssertion.RecordStatus.ValueType``.

        Args:
            value: The string.

        Returns:
            The ``ClinicalAssertion.RecordStatus.ValueType``.
        """
        result = cls.CONVERT_RECORD_STATUS.get(value)
        if not result:
            raise ValueError(f"Unknown value {value}")
        else:
            return result

    @classmethod
    def xmldict_data_to_pb(cls, tag: dict[str, Any]) -> ClinicalAssertion:  # noqa: C901
        """Converts a dict from ``xmltodict`` to a `ClinicalAssertion`` protobuf.

        Args:
            tag: The dict from ``xmltodict``.

        Returns:
            The `ClinicalAssertion`` protobuf.
        """
        assert "ClinicalAssertion" in tag
        tag_ca: dict[str, Any] = tag["ClinicalAssertion"]

        clinvar_submission_id: ClinicalAssertion.ClinvarSubmissionId = (
            cls.convert_clinvar_submission_id(tag_ca)
        )
        clinvar_accession: ClinicalAssertion.ClinvarAccession = cls.convert_clinvar_accession(
            tag_ca
        )
        if "ClinVarAccession" in tag_ca:
            clinvar_accession = cls.convert_clinvar_accession(tag_ca)
        additional_submitters: list[Submitter] | None = None
        if (
            "AdditionalSubmitters" in tag_ca
            and "SubmitterDescription" in tag_ca["AdditionalSubmitters"]
        ):
            additional_submitters = [
                ConvertSubmitter.xmldict_data_to_pb({"SubmitterDescription": entry})
                for entry in cls.ensure_list(tag_ca["AdditionalSubmitters"]["SubmitterDescription"])
            ]
        record_status: ClinicalAssertion.RecordStatus.ValueType = cls.convert_record_status(
            tag_ca["RecordStatus"]
        )
        replaces: list[str] | None = None
        if "Replaces" in tag_ca:
            replaces = [entry for entry in cls.ensure_list(tag_ca["Replaces"])]
        replaceds: list[ClinicalAssertionRecordHistory] | None = None
        if "ReplacedList" in tag_ca and "Replaced" in tag_ca["ReplacedList"]:
            replaceds = [
                ConvertClinicalAssertionRecordHistory.xmldict_data_to_pb({"Replaced": entry})
                for entry in cls.ensure_list(tag_ca["ReplacedList"]["Replaced"])
            ]
        classifications: list[ClassificationScv] | None = None
        if "Classification" in tag_ca:
            classifications = [
                ConvertClassificationScv.xmldict_data_to_pb({"Classification": entry})
                for entry in cls.ensure_list(tag_ca["Classification"])
            ]
        assertion: Assertion.ValueType = ConvertAssertion.xmldict_data_to_pb(tag_ca["Assertion"])
        attributes: list[ClinicalAssertion.AttributeSetElement] | None = None
        if "AttributeSet" in tag_ca:
            attributes = [
                cls.convert_attribute_set({"AttributeSet": entry})
                for entry in cls.ensure_list(tag_ca["AttributeSet"])
            ]
        observed_ins: list[ObservedIn] | None = None
        if "ObservedInList" in tag_ca and "ObservedIn" in tag_ca["ObservedInList"]:
            observed_ins = [
                ConvertObservedIn.xmldict_data_to_pb({"ObservedIn": entry})
                for entry in cls.ensure_list(tag_ca["ObservedInList"]["ObservedIn"])
            ]
        simple_allele: AlleleScv | None = None
        if "SimpleAllele" in tag_ca:
            simple_allele = ConvertAlleleScv.xmldict_data_to_pb(
                {"SimpleAllele": tag_ca["SimpleAllele"]}
            )
        haplotype: HaplotypeScv | None = None
        if "Haplotype" in tag_ca:
            haplotype = ConvertHaplotypeScv.xmldict_data_to_pb({"Haplotype": tag_ca["Haplotype"]})
        genotype: GenotypeScv | None = None
        if "Genotype" in tag_ca:
            genotype = ConvertGenotypeScv.xmldict_data_to_pb({"Genotype": tag_ca["Genotype"]})
        trait_set: TraitSet = ConvertTraitSet.xmldict_data_to_pb({"TraitSet": tag_ca["TraitSet"]})
        citations: list[Citation] | None = None
        if "CitationList" in tag_ca and "Citation" in tag_ca["CitationList"]:
            citations = [
                ConvertCitation.xmldict_data_to_pb({"Citation": entry})
                for entry in cls.ensure_list(tag_ca["CitationList"]["Citation"])
            ]
        study_name: str | None = tag_ca.get("StudyName")
        study_description: str | None = tag_ca.get("StudyDescription")
        comments: list[Comment] | None = None
        if "Comment" in tag_ca:
            comments = [
                ConvertComment.xmldict_data_to_pb({"Comment": entry})
                for entry in cls.ensure_list(tag_ca["Comment"])
            ]
        submission_names: list[str] | None = None
        if "SubmissionNameList" in tag_ca and "SubmissionName" in tag_ca["SubmissionNameList"]:
            submission_names = [
                entry for entry in cls.ensure_list(tag_ca["SubmissionNameList"]["SubmissionName"])
            ]
        date_created: google.protobuf.timestamp_pb2.Timestamp | None = None
        if "DateCreated" in tag_ca:
            dt_date_created = dateutil.parser.parse(tag_ca["DateCreated"])
            seconds_date_created = int(time.mktime(dt_date_created.timetuple()))
            date_created = google.protobuf.timestamp_pb2.Timestamp(seconds=seconds_date_created)
        date_last_updated: google.protobuf.timestamp_pb2.Timestamp | None = None
        if "DateLastUpdated" in tag_ca:
            dt_date_last_updated = dateutil.parser.parse(tag_ca["DateLastUpdated"])
            seconds_date_last_updated = int(time.mktime(dt_date_last_updated.timetuple()))
            date_last_updated = google.protobuf.timestamp_pb2.Timestamp(
                seconds=seconds_date_last_updated
            )
        submission_date: google.protobuf.timestamp_pb2.Timestamp | None = None
        if "SubmissionDate" in tag_ca:
            dt_submission_date = dateutil.parser.parse(tag_ca["SubmissionDate"])
            seconds_submission_date = int(time.mktime(dt_submission_date.timetuple()))
            submission_date = google.protobuf.timestamp_pb2.Timestamp(
                seconds=seconds_submission_date
            )
        id_: int | None = None
        if "@ID" in tag_ca:
            id_ = int(tag_ca["@ID"])
        fda_recognized_database: bool | None = None
        if "@FDARecognizedDatabase" in tag_ca:
            fda_recognized_database = tag_ca["@FDARecognizedDatabase"] == "true"

        return ClinicalAssertion(
            clinvar_submission_id=clinvar_submission_id,
            clinvar_accession=clinvar_accession,
            additional_submitters=additional_submitters,
            record_status=record_status,
            replaces=replaces,
            replaceds=replaceds,
            classifications=classifications,
            assertion=assertion,
            attributes=attributes,
            observed_ins=observed_ins,
            simple_allele=simple_allele,
            haplotype=haplotype,
            genotype=genotype,
            trait_set=trait_set,
            citations=citations,
            study_name=study_name,
            study_description=study_description,
            comments=comments,
            submission_names=submission_names,
            date_created=date_created,
            date_last_updated=date_last_updated,
            submission_date=submission_date,
            id=id_,
            fda_recognized_database=fda_recognized_database,
        )


class ConvertAllele(ConverterBase):
    """Static method helper for converting XML data to to ``Allele``."""

    @classmethod
    def convert_gene(cls, tag: dict[str, Any]) -> Allele.Gene:
        """Converts a dict from ``xmltodict`` to a ``Allele.Gene`` protobuf.

        Args:
            tag: The dict from ``xmltodict``.

        Returns:
            The ``Allele.Gene`` protobuf.
        """
        assert "Gene" in tag
        tag_gene: dict[str, Any] = tag["Gene"]

        locations: list[Location] | None = None
        if "Location" in tag_gene:
            locations = [
                ConvertLocation.xmldict_data_to_pb({"Location": entry})
                for entry in cls.ensure_list(tag_gene["Location"])
                if entry
            ]
        omims: list[int] | None = None
        if "OMIM" in tag_gene:
            omims = [int(omim_value) for omim_value in cls.ensure_list(tag_gene["OMIM"])]
        haploinsufficiency: DosageSensitivity | None = None
        if "Haploinsufficiency" in tag_gene:
            haploinsufficiency = ConvertDosageSensitivity.xmldict_data_to_pb(
                {"Haploinsufficiency": tag_gene["Haploinsufficiency"]}, "Haploinsufficiency"
            )
        triplosensitivity: DosageSensitivity | None = None
        if "Triplosensitivity" in tag_gene:
            triplosensitivity = ConvertDosageSensitivity.xmldict_data_to_pb(
                {"Triplosensitivity": tag_gene["Triplosensitivity"]}, "Triplosensitivity"
            )
        properties: list[str] | None = None
        if "Property" in tag_gene:
            properties = [entry for entry in cls.ensure_list(tag_gene["Property"])]
        symbol: str | None = tag_gene.get("Symbol")
        full_name: str = tag_gene["@FullName"]
        gene_id: int = int(tag_gene["@GeneID"])
        hgnc_id: str | None = None
        if "@HGNC_ID" in tag_gene:
            hgnc_id = tag_gene["@HGNC_ID"]
        source: str = tag_gene["@Source"]
        relationship_type: GeneVariantRelationship.ValueType | None = None
        if "@RelationshipType" in tag_gene:
            relationship_type = ConvertGeneVariantRelationship.xmldict_data_to_pb(
                tag_gene["@RelationshipType"]
            )

        return Allele.Gene(
            locations=locations,
            omims=omims,
            haploinsufficiency=haploinsufficiency,
            triplosensitivity=triplosensitivity,
            properties=properties,
            symbol=symbol,
            full_name=full_name,
            gene_id=gene_id,
            hgnc_id=hgnc_id,
            source=source,
            relationship_type=relationship_type,
        )

    @classmethod
    def convert_allele_frequency(cls, tag: dict[str, Any]) -> Allele.AlleleFrequency:
        """Converts a dict from ``xmltodict`` to a ``Allele.AlleleFrequency`` protobuf.

        Args:
            tag: The dict from ``xmltodict``.

        Returns:
            The ``Allele.AlleleFrequency`` protobuf.
        """
        assert "AlleleFrequency" in tag

        value: float = float(tag["AlleleFrequency"]["@Value"])
        source: str = tag["AlleleFrequency"]["@Source"]
        url: str | None = None
        if "@URL" in tag["AlleleFrequency"]:
            url = tag["AlleleFrequency"]["@URL"]

        return Allele.AlleleFrequency(
            value=value,
            source=source,
            url=url,
        )

    @classmethod
    def convert_global_minor_allele_frequency(
        cls, tag: dict[str, Any]
    ) -> Allele.GlobalMinorAlleleFrequency:
        """Converts a dict from ``xmltodict`` to a ``Allele.GlobalMinorAlleleFrequency`` protobuf.

        Args:
            tag: The dict from ``xmltodict``.

        Returns:
            The ``Allele.GlobalMinorAlleleFrequency`` protobuf.
        """
        assert "GlobalMinorAlleleFrequency" in tag

        value: float = float(tag["GlobalMinorAlleleFrequency"]["@Value"])
        source: str = tag["GlobalMinorAlleleFrequency"]["@Source"]
        url: str | None = None
        if "@URL" in tag["GlobalMinorAlleleFrequency"]:
            url = tag["GlobalMinorAlleleFrequency"]["@URL"]
        minor_allele: str | None = None
        if "@MinorAllele" in tag["GlobalMinorAlleleFrequency"]:
            minor_allele = tag["GlobalMinorAlleleFrequency"]["@MinorAllele"]

        return Allele.GlobalMinorAlleleFrequency(
            value=value,
            source=source,
            minor_allele=minor_allele,
            url=url,
        )

    @classmethod
    def xmldict_data_to_pb(cls, tag: dict[str, Any]) -> Allele:
        """Converts a dict from ``xmltodict`` to a `Allele`` protobuf.

        Args:
            tag: The dict from ``xmltodict``.

        Returns:
            The `Allele`` protobuf.
        """
        assert "SimpleAllele" in tag
        tag_allele: dict[str, Any] = tag["SimpleAllele"]

        genes: list[Allele.Gene] | None = None
        if "GeneList" in tag_allele and "Gene" in tag_allele["GeneList"]:
            genes = [
                cls.convert_gene({"Gene": entry})
                for entry in cls.ensure_list(tag_allele["GeneList"]["Gene"])
            ]
        name: str = tag_allele["Name"]
        canonical_spdi: str | None = tag_allele.get("CanonicalSPDI")
        variant_types: list[str] | None = None
        if "VariantType" in tag_allele:
            variant_types = [entry for entry in cls.ensure_list(tag_allele["VariantType"])]
        locations: list[Location] | None = None
        if "Location" in tag_allele:
            locations = [
                ConvertLocation.xmldict_data_to_pb({"Location": entry})
                for entry in cls.ensure_list(tag_allele["Location"])
            ]
        other_names: list[OtherName] | None = None
        if "OtherNameList" in tag_allele:
            other_names = [
                ConvertOtherName.xmldict_data_to_pb({"Name": entry})
                for entry in cls.ensure_list(tag_allele["OtherNameList"]["Name"])
            ]
        protein_changes: list[str] | None = None
        if "ProteinChange" in tag_allele:
            protein_changes = [entry for entry in cls.ensure_list(tag_allele["ProteinChange"])]
        hgvs_expressions: list[HgvsExpression] | None = None
        if "HGVSlist" in tag_allele and "HGVS" in tag_allele["HGVSlist"]:
            hgvs_expressions = [
                ConvertHgvsExpression.xmldict_data_to_pb({"HGVS": entry})
                for entry in cls.ensure_list(tag_allele["HGVSlist"]["HGVS"])
            ]
        classifications: AggregateClassificationSet | None = None
        if "Classifications" in tag_allele:
            classifications = ConvertAggregateClassificationSet.xmldict_data_to_pb(
                {"Classifications": tag_allele["Classifications"]}
            )
        xrefs: list[Xref] | None = None
        if "XRefList" in tag_allele and "XRef" in tag_allele["XRefList"]:
            xrefs = [
                ConvertXref.xmldict_data_to_pb({"XRef": entry})
                for entry in cls.ensure_list(tag_allele["XRefList"]["XRef"])
            ]
        comments: list[Comment] | None = None
        if "Comment" in tag_allele:
            comments = [
                ConvertComment.xmldict_data_to_pb({"Comment": entry})
                for entry in cls.ensure_list(tag_allele["Comment"])
            ]
        functional_consequences: list[FunctionalConsequence] | None = None
        if "FunctionalConsequence" in tag_allele:
            functional_consequences = [
                ConvertFunctionalConsequence.xmldict_data_to_pb({"FunctionalConsequence": entry})
                for entry in cls.ensure_list(tag_allele["FunctionalConsequence"])
            ]
        allele_frequencies: list[Allele.AlleleFrequency] | None = None
        if "AlleleFrequency" in tag_allele:
            allele_frequencies = [
                cls.convert_allele_frequency({"AlleleFrequency": entry})
                for entry in cls.ensure_list(tag_allele["AlleleFrequency"])
            ]
        global_minor_allele_frequency: Allele.GlobalMinorAlleleFrequency | None = None
        if "GlobalMinorAlleleFrequency" in tag_allele:
            global_minor_allele_frequency = cls.convert_global_minor_allele_frequency(
                {"GlobalMinorAlleleFrequency": tag_allele["GlobalMinorAlleleFrequency"]}
            )
        allele_id: int = int(tag_allele["@AlleleID"])
        variation_id: int = int(tag_allele["@VariationID"])

        return Allele(
            genes=genes,
            name=name,
            canonical_spdi=canonical_spdi,
            variant_types=variant_types,
            locations=locations,
            other_names=other_names,
            protein_changes=protein_changes,
            hgvs_expressions=hgvs_expressions,
            classifications=classifications,
            xrefs=xrefs,
            comments=comments,
            functional_consequences=functional_consequences,
            allele_frequencies=allele_frequencies,
            global_minor_allele_frequency=global_minor_allele_frequency,
            allele_id=allele_id,
            variation_id=variation_id,
        )


class ConvertHaplotype(ConverterBase):
    """Static method helper for converting XML data to to ``Haplotype``."""

    @classmethod
    def xmldict_data_to_pb(cls, tag: dict[str, Any]) -> Haplotype:
        """Converts a dict from ``xmltodict`` to a `Haplotype`` protobuf.

        Args:
            tag: The dict from ``xmltodict``.

        Returns:
            The `Haplotype`` protobuf.
        """
        assert "Haplotype" in tag
        tag_haplotype: dict[str, Any] = tag["Haplotype"]

        simple_alleles: list[Allele] | None = None
        if "SimpleAllele" in tag_haplotype:
            simple_alleles = [
                ConvertAllele.xmldict_data_to_pb({"SimpleAllele": entry})
                for entry in cls.ensure_list(tag_haplotype["SimpleAllele"])
            ]
        name: str = tag_haplotype["Name"]
        variation_type: HaploVariationType.ValueType = ConvertHaploVariationType.xmldict_data_to_pb(
            tag_haplotype["VariationType"]
        )
        other_names: list[OtherName] | None = None
        if "OtherNameList" in tag_haplotype and "Name" in tag_haplotype["OtherNameList"]:
            other_names = [
                ConvertOtherName.xmldict_data_to_pb({"Name": entry})
                for entry in cls.ensure_list(tag_haplotype["OtherNameList"]["Name"])
            ]
        hgvs_expressions: list[HgvsExpression] | None = None
        if "HGVSlist" in tag_haplotype and "HGVS" in tag_haplotype["HGVSlist"]:
            hgvs_expressions = [
                ConvertHgvsExpression.xmldict_data_to_pb({"HGVS": entry})
                for entry in cls.ensure_list(tag_haplotype["HGVSlist"]["HGVS"])
            ]
        classifications: AggregateClassificationSet | None = None
        if "Classifications" in tag_haplotype:
            classifications = ConvertAggregateClassificationSet.xmldict_data_to_pb(
                {"Classifications": tag_haplotype["Classifications"]}
            )
        functional_consequences: list[FunctionalConsequence] | None = None
        if "FunctionalConsequence" in tag_haplotype:
            functional_consequences = [
                ConvertFunctionalConsequence.xmldict_data_to_pb({"FunctionalConsequence": entry})
                for entry in cls.ensure_list(tag_haplotype["FunctionalConsequence"])
            ]
        xrefs: list[Xref] | None = None
        if "XRefList" in tag_haplotype and "XRef" in tag_haplotype["XRefList"]:
            xrefs = [
                ConvertXref.xmldict_data_to_pb({"XRef": entry})
                for entry in cls.ensure_list(tag_haplotype["XRefList"]["XRef"])
            ]
        comments: list[Comment] | None = None
        if "Comment" in tag_haplotype:
            comments = [
                ConvertComment.xmldict_data_to_pb({"Comment": entry})
                for entry in cls.ensure_list(tag_haplotype["Comment"])
            ]
        variation_id: int = int(tag_haplotype["@VariationID"])
        number_of_copies: int | None = None
        if "@NumberOfCopies" in tag_haplotype:
            number_of_copies = int(tag_haplotype["@NumberOfCopies"])
        number_of_chromosomes: int | None = None
        if "@NumberOfChromosomes" in tag_haplotype:
            number_of_chromosomes = int(tag_haplotype["@NumberOfChromosomes"])

        return Haplotype(
            simple_alleles=simple_alleles,
            name=name,
            variation_type=variation_type,
            other_names=other_names,
            hgvs_expressions=hgvs_expressions,
            classifications=classifications,
            functional_consequences=functional_consequences,
            xrefs=xrefs,
            comments=comments,
            variation_id=variation_id,
            number_of_copies=number_of_copies,
            number_of_chromosomes=number_of_chromosomes,
        )


class ConvertIncludedRecord(ConverterBase):
    """Static method helper for converting XML data to to ``IncludedRecord``."""

    @classmethod
    def convert_classified_variation(
        cls, tag: dict[str, Any]
    ) -> IncludedRecord.ClassifiedVariation:
        """Converts a dict from ``xmltodict`` to a ``IncludedRecord.ClassifiedVariation`` protobuf.

        Args:
            tag: The dict from ``xmltodict``.

        Returns:
            The ``IncludedRecord.ClassifiedVariation`` protobuf.
        """
        assert "ClassifiedVariation" in tag
        tag_cv: dict[str, Any] = tag["ClassifiedVariation"]

        variation_id: int = int(tag_cv["@VariationID"])
        accession: str | None = tag_cv.get("@Accession")
        version: int = int(tag_cv["@Version"])

        return IncludedRecord.ClassifiedVariation(
            variation_id=variation_id,
            accession=accession,
            version=version,
        )

    @classmethod
    def xmldict_data_to_pb(cls, tag: dict[str, Any]) -> IncludedRecord:  # noqa: C901
        """Converts a dict from ``xmltodict`` to a `IncludedRecord`` protobuf.

        Args:
            tag: The dict from ``xmltodict``.

        Returns:
            The `IncludedRecord`` protobuf.
        """
        assert "IncludedRecord" in tag
        tag_record: dict[str, Any] = tag["IncludedRecord"]

        simple_allele: Allele | None = None
        if "SimpleAllele" in tag_record:
            simple_allele = ConvertAllele.xmldict_data_to_pb(
                {"SimpleAllele": tag_record["SimpleAllele"]}
            )
        haplotype: Haplotype | None = None
        if "Haplotype" in tag_record:
            haplotype = ConvertHaplotype.xmldict_data_to_pb({"Haplotype": tag_record["Haplotype"]})
        classifications: AggregateClassificationSet | None = None
        if "Classifications" in tag_record:
            classifications = ConvertAggregateClassificationSet.xmldict_data_to_pb(
                {"Classifications": tag_record["Classifications"]}
            )
        submitted_classifications: list[Scv] | None = None
        if (
            "SubmittedClassifications" in tag_record
            and "SCV" in tag_record["SubmittedClassifications"]
        ):
            submitted_classifications = [
                ConvertScv.xmldict_data_to_pb({"SCV": entry})
                for entry in cls.ensure_list(tag_record["SubmittedClassifications"]["SCV"])
            ]
        classified_variations: list[IncludedRecord.ClassifiedVariation] | None = None
        if (
            "ClassifiedVariationList" in tag_record
            and "ClassifiedVariation" in tag_record["ClassifiedVariationList"]
        ):
            pass
        general_citations: list[GeneralCitations] | None = None

        return IncludedRecord(
            simple_allele=simple_allele,
            haplotype=haplotype,
            classifications=classifications,
            submitted_classifications=submitted_classifications,
            classified_variations=classified_variations,
            general_citations=general_citations,
        )


class ConvertGenotype(ConverterBase):
    """Static method helper for converting XML data to to ``Genotype``."""

    @classmethod
    def xmldict_data_to_pb(cls, tag: dict[str, Any]) -> Genotype:  # noqa: C901
        """Converts a dict from ``xmltodict`` to a `Genotype`` protobuf.

        Args:
            tag: The dict from ``xmltodict``.

        Returns:
            The `Genotype`` protobuf.
        """
        assert "Genotype" in tag
        tag_record: dict[str, Any] = tag["Genotype"]

        simple_alleles: list[Allele] | None = None
        if "SimpleAllele" in tag_record:
            simple_alleles = [
                ConvertAllele.xmldict_data_to_pb({"SimpleAllele": entry})
                for entry in cls.ensure_list(tag_record["SimpleAllele"])
            ]
        haplotypes: list[Haplotype] | None = None
        if "Haplotype" in tag_record:
            haplotypes = [
                ConvertHaplotype.xmldict_data_to_pb({"Haplotype": entry})
                for entry in cls.ensure_list(tag_record["Haplotype"])
            ]
        name: str = tag_record["Name"]
        variation_type: VariationType.ValueType = ConvertVariationType.xmldict_data_to_pb(
            tag_record["VariationType"]
        )
        other_names: list[OtherName] | None = None
        if "OtherNameList" in tag_record and "Name" in tag_record["OtherNameList"]:
            other_names = [
                ConvertOtherName.xmldict_data_to_pb({"Name": entry})
                for entry in cls.ensure_list(tag_record["OtherNameList"]["Name"])
            ]
        hgvs_expressions: list[HgvsExpression] | None = None
        if "HGVSlist" in tag_record and "HGVS" in tag_record["HGVSlist"]:
            hgvs_expressions = [
                ConvertHgvsExpression.xmldict_data_to_pb({"HGVS": entry})
                for entry in cls.ensure_list(tag_record["HGVSlist"]["HGVS"])
            ]
        functional_consequences: list[FunctionalConsequence] | None = None
        if "FunctionalConsequence" in tag_record:
            functional_consequences = [
                ConvertFunctionalConsequence.xmldict_data_to_pb({"FunctionalConsequence": entry})
                for entry in cls.ensure_list(tag_record["FunctionalConsequence"])
            ]
        classifications: AggregateClassificationSet | None = None
        if "Classifications" in tag_record:
            classifications = ConvertAggregateClassificationSet.xmldict_data_to_pb(
                {"Classifications": tag_record["Classifications"]}
            )
        xrefs: list[Xref] | None = None
        if "XRefList" in tag_record and "XRef" in tag_record["XRefList"]:
            xrefs = [
                ConvertXref.xmldict_data_to_pb({"XRef": entry})
                for entry in cls.ensure_list(tag_record["XRefList"]["XRef"])
            ]
        citations: list[Citation] | None = None
        if "CitationList" in tag_record and "Citation" in tag_record["CitationList"]:
            citations = [
                ConvertCitation.xmldict_data_to_pb({"Citation": entry})
                for entry in cls.ensure_list(tag_record["CitationList"]["Citation"])
            ]
        comments: list[Comment] | None = None
        if "Comment" in tag_record:
            comments = [
                ConvertComment.xmldict_data_to_pb({"Comment": entry})
                for entry in cls.ensure_list(tag_record["Comment"])
            ]
        attributes: list[AttributeSetElement] | None = None
        if "AttributeSet" in tag_record:
            attributes = [
                ConvertAttributeSetElement.xmldict_data_to_pb({"AttributeSet": element})
                for element in cls.ensure_list(tag_record["AttributeSet"])
            ]
        variation_id: int = int(tag_record["@VariationID"])

        return Genotype(
            simple_alleles=simple_alleles,
            haplotypes=haplotypes,
            name=name,
            variation_type=variation_type,
            other_names=other_names,
            hgvs_expressions=hgvs_expressions,
            functional_consequences=functional_consequences,
            classifications=classifications,
            xrefs=xrefs,
            citations=citations,
            comments=comments,
            attributes=attributes,
            variation_id=variation_id,
        )


class ConvertRcvAccession(ConverterBase):
    """Static method helper for converting XML data to to ``RcvAccession``."""

    @classmethod
    def convert_classified_condition_list(
        cls, tag: dict[str, Any]
    ) -> RcvAccession.ClassifiedConditionList:
        """Converts a dict from ``xmltodict`` to a ``RcvAccession.ClassifiedConditionList`` protobuf.

        Args:
            tag: The dict from ``xmltodict``.

        Returns:
            The ``RcvAccession.ClassifiedConditionList`` protobuf.
        """
        assert "ClassifiedConditionList" in tag
        tag_ccl: dict[str, Any] = tag["ClassifiedConditionList"]

        classified_conditions: list[ClassifiedCondition] | None = None
        if "ClassifiedCondition" in tag_ccl:
            classified_conditions = [
                ConvertClassifiedCondition.xmldict_data_to_pb({"ClassifiedCondition": entry})
                for entry in cls.ensure_list(tag_ccl["ClassifiedCondition"])
            ]
        trait_set_id: int = int(tag_ccl["@TraitSetID"])

        return RcvAccession.ClassifiedConditionList(
            classified_conditions=classified_conditions,
            trait_set_id=trait_set_id,
        )

    @classmethod
    def convert_germline_classification_description(
        cls, tag: dict[str, Any]
    ) -> RcvAccession.GermlineClassification.Description:
        """Converts a dict from ``xmltodict`` to a ``RcvAccession.GermlineClassification.Description`` protobuf.

        Args:
            tag: The dict from ``xmltodict``.

        Returns:
            The ``RcvAccession.GermlineClassification.Description`` protobuf.
        """
        assert "Description" in tag
        tag_description: str | dict[str, Any] = tag["Description"]

        if isinstance(tag_description, str):
            return RcvAccession.GermlineClassification.Description(value=tag_description)
        else:
            value: str = tag_description["#text"]
            date_last_evaluated: google.protobuf.timestamp_pb2.Timestamp | None = None
            if "@DateLastEvaluated" in tag_description:
                dt = dateutil.parser.parse(tag_description["@DateLastEvaluated"])
                seconds = int(time.mktime(dt.timetuple()))
                date_last_evaluated = google.protobuf.timestamp_pb2.Timestamp(seconds=seconds)
            submission_count: int | None = None
            if "@SubmissionCount" in tag_description:
                submission_count = int(tag_description["@SubmissionCount"])

            return RcvAccession.GermlineClassification.Description(
                value=value,
                date_last_evaluated=date_last_evaluated,
                submission_count=submission_count,
            )

    @classmethod
    def convert_germline_classification(
        cls, tag: dict[str, Any]
    ) -> RcvAccession.GermlineClassification:
        """Converts a dict from ``xmltodict`` to a ``RcvAccession.GermlineClassification`` protobuf.

        Args:
            tag: The dict from ``xmltodict``.

        Returns:
            The ``RcvAccession.GermlineClassification`` protobuf.
        """
        assert "GermlineClassification" in tag
        tag_gc: dict[str, Any] = tag["GermlineClassification"]

        review_status: AggregateGermlineReviewStatus.ValueType = (
            ConvertAggregateGermlineReviewStatus.xmldict_data_to_pb(tag_gc["ReviewStatus"])
        )
        description: RcvAccession.GermlineClassification.Description = (
            cls.convert_germline_classification_description({"Description": tag_gc["Description"]})
        )

        return RcvAccession.GermlineClassification(
            review_status=review_status,
            description=description,
        )

    @classmethod
    def convert_somatic_clinical_impact_description(
        cls, tag: dict[str, Any]
    ) -> RcvAccession.SomaticClinicalImpact.Description:
        """Converts a dict from ``xmltodict`` to a ``RcvAccession.SomaticClinicalImpact.Description`` protobuf.

        Args:
            tag: The dict from ``xmltodict``.

        Returns:
            The ``RcvAccession.SomaticClinicalImpact.Description`` protobuf.
        """
        assert "Description" in tag
        tag_description: str | dict[str, Any] = tag["Description"]

        if isinstance(tag_description, str):
            return RcvAccession.SomaticClinicalImpact.Description(value=tag_description)
        else:
            value: str = tag_description["#text"]
            clinical_impact_assertion_type: str | None = tag_description.get(
                "@ClinicalImpactAssertionType"
            )
            clinical_impact_clinical_significance: str | None = tag_description.get(
                "@ClinicalImpactClinicalSignificance"
            )
            date_last_evaluated: google.protobuf.timestamp_pb2.Timestamp | None = None
            if "@DateLastEvaluated" in tag_description:
                dt = dateutil.parser.parse(tag_description["@DateLastEvaluated"])
                seconds = int(time.mktime(dt.timetuple()))
                date_last_evaluated = google.protobuf.timestamp_pb2.Timestamp(seconds=seconds)
            submission_count: int | None = None
            if "@SubmissionCount" in tag_description:
                submission_count = int(tag_description["@SubmissionCount"])

            return RcvAccession.SomaticClinicalImpact.Description(
                value=value,
                clinical_impact_assertion_type=clinical_impact_assertion_type,
                clinical_impact_clinical_significance=clinical_impact_clinical_significance,
                date_last_evaluated=date_last_evaluated,
                submission_count=submission_count,
            )

    @classmethod
    def convert_somatic_clinical_impact(
        cls, tag: dict[str, Any]
    ) -> RcvAccession.SomaticClinicalImpact:
        """Converts a dict from ``xmltodict`` to a ``RcvAccession.SomaticClinicalImpact`` protobuf.

        Args:
            tag: The dict from ``xmltodict``.

        Returns:
            The ``RcvAccession.SomaticClinicalImpact`` protobuf.
        """
        assert "SomaticClinicalImpact" in tag
        tag_sci: dict[str, Any] = tag["SomaticClinicalImpact"]

        review_status: AggregateSomaticClinicalImpactReviewStatus.ValueType = (
            ConvertAggregateSomaticClinicalImpactReviewStatus.xmldict_data_to_pb(
                tag_sci["ReviewStatus"]
            )
        )
        descriptions: list[RcvAccession.SomaticClinicalImpact.Description] = [
            cls.convert_somatic_clinical_impact_description({"Description": description})
            for description in cls.ensure_list(tag_sci["Description"])
        ]

        return RcvAccession.SomaticClinicalImpact(
            review_status=review_status,
            descriptions=descriptions,
        )

    @classmethod
    def convert_oncogenicity_classification_description(
        cls, tag: dict[str, Any]
    ) -> RcvAccession.OncogenicityClassification.Description:
        """Converts a dict from ``xmltodict`` to a ``RcvAccession.OncogenicityClassification.Description`` protobuf.

        Args:
            tag: The dict from ``xmltodict``.

        Returns:
            The ``RcvAccession.OncogenicityClassification.Description`` protobuf.
        """
        assert "Description" in tag
        tag_description: str | dict[str, Any] = tag["Description"]

        if isinstance(tag_description, str):
            return RcvAccession.OncogenicityClassification.Description(value=tag_description)
        else:
            value: str = tag_description["#text"]
            date_last_evaluated: google.protobuf.timestamp_pb2.Timestamp | None = None
            if "@DateLastEvaluated" in tag_description:
                dt = dateutil.parser.parse(tag_description["@DateLastEvaluated"])
                seconds = int(time.mktime(dt.timetuple()))
                date_last_evaluated = google.protobuf.timestamp_pb2.Timestamp(seconds=seconds)
            submission_count: int | None = None
            if "@SubmissionCount" in tag_description:
                submission_count = int(tag_description["@SubmissionCount"])

            return RcvAccession.OncogenicityClassification.Description(
                value=value,
                date_last_evaluated=date_last_evaluated,
                submission_count=submission_count,
            )

    @classmethod
    def convert_oncogenicity_classification(
        cls, tag: dict[str, Any]
    ) -> RcvAccession.OncogenicityClassification:
        """Converts a dict from ``xmltodict`` to a ``RcvAccession.OncogenicityClassification`` protobuf.

        Args:
            tag: The dict from ``xmltodict``.

        Returns:
            The ``RcvAccession.OncogenicityClassification`` protobuf.
        """
        assert "OncogenicityClassification" in tag
        tag_oc: dict[str, Any] = tag["OncogenicityClassification"]

        review_status: AggregateOncogenicityReviewStatus.ValueType = (
            ConvertAggregateOncogenicityReviewStatus.xmldict_data_to_pb(tag_oc["ReviewStatus"])
        )
        description: RcvAccession.OncogenicityClassification.Description = (
            cls.convert_oncogenicity_classification_description(
                {"Description": tag_oc["Description"]}
            )
        )

        return RcvAccession.OncogenicityClassification(
            review_status=review_status,
            description=description,
        )

    @classmethod
    def convert_rcv_classifications(cls, tag: dict[str, Any]) -> RcvAccession.RcvClassifications:
        """Converts a dict from ``xmltodict`` to a ``RcvAccession.RcvClassifications`` protobuf.

        Args:
            tag: The dict from ``xmltodict``.

        Returns:
            The ``RcvAccession.RcvClassifications`` protobuf.
        """
        assert "RCVClassifications" in tag
        tag_rc: dict[str, Any] = tag["RCVClassifications"]

        germline_classification: RcvAccession.GermlineClassification | None = None
        if "GermlineClassification" in tag_rc:
            germline_classification = cls.convert_germline_classification(
                {"GermlineClassification": tag_rc["GermlineClassification"]}
            )
        somatic_clinical_impact: RcvAccession.SomaticClinicalImpact | None = None
        if "SomaticClinicalImpact" in tag_rc:
            somatic_clinical_impact = cls.convert_somatic_clinical_impact(
                {"SomaticClinicalImpact": tag_rc["SomaticClinicalImpact"]}
            )
        oncogenicity_classification: RcvAccession.OncogenicityClassification | None = None
        if "OncogenicityClassification" in tag_rc:
            oncogenicity_classification = cls.convert_oncogenicity_classification(
                {"OncogenicityClassification": tag_rc["OncogenicityClassification"]}
            )

        return RcvAccession.RcvClassifications(
            germline_classification=germline_classification,
            somatic_clinical_impact=somatic_clinical_impact,
            oncogenicity_classification=oncogenicity_classification,
        )

    @classmethod
    def xmldict_data_to_pb(cls, tag: dict[str, Any]) -> RcvAccession:
        """Converts a dict from ``xmltodict`` to a ``RcvAccession`` protobuf.

        Args:
            tag: The dict from ``xmltodict``.

        Returns:
            The ``RcvAccession`` protobuf.
        """
        assert "RCVAccession" in tag
        tag_ra: dict[str, Any] = tag["RCVAccession"]

        classified_condition_list: RcvAccession.ClassifiedConditionList | None = None
        if "ClassifiedConditionList" in tag_ra:
            classified_condition_list = cls.convert_classified_condition_list(
                {"ClassifiedConditionList": tag_ra["ClassifiedConditionList"]}
            )
        rcv_classifications: RcvAccession.RcvClassifications | None = None
        if "RCVClassifications" in tag_ra:
            rcv_classifications = cls.convert_rcv_classifications(
                {"RCVClassifications": tag_ra["RCVClassifications"]}
            )
        replaceds: list[RecordHistory] | None = None
        if "ReplacedList" in tag_ra and "Replaced" in tag_ra["ReplacedList"]:
            replaceds = [
                ConvertRecordHistory.xmldict_data_to_pb({"Replaced": entry})
                for entry in cls.ensure_list(tag_ra["ReplacedList"]["Replaced"])
            ]

        title: str | None = tag_ra.get("@Title")
        accession: str = tag_ra["@Accession"]
        version: int = int(tag_ra["@Version"])

        return RcvAccession(
            classified_condition_list=classified_condition_list,
            rcv_classifications=rcv_classifications,
            replaceds=replaceds,
            title=title,
            accession=accession,
            version=version,
        )


class ConvertClassifiedRecord(ConverterBase):
    """Static method helper for converting XML data to to ``ClassifiedRecord``."""

    @classmethod
    def convert_rcv_list(cls, value: dict[str, Any]) -> ClassifiedRecord.RcvList:
        """Converts a dict from ``xmltodict`` to a ``RCVList`` protobuf.

        Args:
            value: The dict from ``xmltodict``.

        Returns:
            The ``ClassifiedRecord.RcvList`` protobuf.
        """
        assert "RCVList" in value
        tag_rl: dict[str, Any] = value["RCVList"]

        rcv_accessions: list[RcvAccession] | None = None
        if "RCVAccession" in tag_rl:
            rcv_accessions = [
                ConvertRcvAccession.xmldict_data_to_pb({"RCVAccession": entry})
                for entry in cls.ensure_list(tag_rl["RCVAccession"])
            ]
        submission_count: int | None = None
        if "@SubmissionCount" in tag_rl:
            submission_count = int(tag_rl["@SubmissionCount"])
        independent_observations: int | None = None
        if "@IndependentObservations" in tag_rl:
            independent_observations = int(tag_rl["@IndependentObservations"])

        return ClassifiedRecord.RcvList(
            rcv_accessions=rcv_accessions,
            submission_count=submission_count,
            independent_observations=independent_observations,
        )

    #: Map for converting from XML value to protobuf enum.
    CONVERT_MAPPING_TYPE: Dict[str, ClassifiedRecord.MappingType.ValueType] = {
        "Name": ClassifiedRecord.MappingType.MAPPING_TYPE_NAME,
        "XRef": ClassifiedRecord.MappingType.MAPPING_TYPE_XREF,
    }

    @classmethod
    def convert_mapping_type(cls, value: str) -> ClassifiedRecord.MappingType.ValueType:
        """Converts a string to a ``ClassifiedRecord.MappingType``.

        Args:
            value: The string.

        Returns:
            The ``ClassifiedRecord.MappingType``.
        """
        result = cls.CONVERT_MAPPING_TYPE.get(value)
        if not result:
            raise ValueError(f"Unknown value {value}")
        else:
            return result

    @classmethod
    def convert_trait_mapping_medgen(
        cls, value: dict[str, Any]
    ) -> ClassifiedRecord.TraitMapping.Medgen:
        """Converts a dict from ``xmltodict`` to a ``ClassifiedRecord.TraitMapping.Medgen`` protobuf.

        Args:
            value: The dict from ``xmltodict``.

        Returns:
            The ``ClassifiedRecord.RcvList`` protobuf.
        """
        assert "MedGen" in value
        tag_medgen: dict[str, Any] = value["MedGen"]

        return ClassifiedRecord.TraitMapping.Medgen(
            name=tag_medgen["@Name"],
            cui=tag_medgen["@CUI"],
        )

    @classmethod
    def convert_trait_mapping(cls, value: dict[str, Any]) -> ClassifiedRecord.TraitMapping:
        """Converts a dict from ``xmltodict`` to a ``ClassifiedRecord.TraitMapping`` protobuf.

        Args:
            value: The dict from ``xmltodict``.

        Returns:
            The ``ClassifiedRecord.TraitMapping`` protobuf.
        """
        assert "TraitMapping" in value
        tag_tm: dict[str, Any] = value["TraitMapping"]

        medgens: list[ClassifiedRecord.TraitMapping.Medgen] | None = None
        if "MedGen" in tag_tm:
            medgens = [
                cls.convert_trait_mapping_medgen({"MedGen": entry})
                for entry in cls.ensure_list(tag_tm["MedGen"])
            ]
        clinical_assertion_id: int = int(tag_tm["@ClinicalAssertionID"])
        trait_type: str = tag_tm["@TraitType"]
        mapping_type: ClassifiedRecord.MappingType.ValueType = cls.convert_mapping_type(
            tag_tm["@MappingType"]
        )
        mapping_value: str = tag_tm["@MappingValue"]
        mapping_ref: str = tag_tm["@MappingRef"]

        return ClassifiedRecord.TraitMapping(
            medgens=medgens,
            clinical_assertion_id=clinical_assertion_id,
            trait_type=trait_type,
            mapping_type=mapping_type,
            mapping_value=mapping_value,
            mapping_ref=mapping_ref,
        )

    @classmethod
    def xmldict_data_to_pb(cls, value: dict[str, Any]) -> ClassifiedRecord:
        """Converts a dict from ``xmltodict`` to a ``ClassifiedRecord`` protobuf.

        Args:
            value: The dict from ``xmltodict``.

        Returns:
            The ``ClassifiedRecord`` protobuf.
        """
        assert "ClassifiedRecord" in value
        tag_cr: dict[str, Any] = value["ClassifiedRecord"]

        simple_allele: Allele | None = None
        if "SimpleAllele" in tag_cr:
            simple_allele = ConvertAllele.xmldict_data_to_pb(
                {"SimpleAllele": tag_cr["SimpleAllele"]}
            )
        haplotype: Haplotype | None = None
        if "Haplotype" in tag_cr:
            haplotype = ConvertHaplotype.xmldict_data_to_pb({"Haplotype": tag_cr["Haplotype"]})
        genotype: Genotype | None = None
        if "Genotype" in tag_cr:
            genotype = ConvertGenotype.xmldict_data_to_pb({"Genotype": tag_cr["Genotype"]})
        rcv_list: ClassifiedRecord.RcvList = cls.convert_rcv_list({"RCVList": tag_cr["RCVList"]})
        classifications: AggregateClassificationSet = (
            ConvertAggregateClassificationSet.xmldict_data_to_pb(
                {"Classifications": tag_cr["Classifications"]}
            )
        )
        clinical_assertions: list[ClinicalAssertion] | None = None
        if (
            "ClinicalAssertionList" in tag_cr
            and "ClinicalAssertion" in tag_cr["ClinicalAssertionList"]
        ):
            clinical_assertions = [
                ConvertClinicalAssertion.xmldict_data_to_pb({"ClinicalAssertion": entry})
                for entry in cls.ensure_list(tag_cr["ClinicalAssertionList"]["ClinicalAssertion"])
            ]
        trait_mappings: list[ClassifiedRecord.TraitMapping] | None = None
        if "TraitMappingList" in tag_cr and "TraitMapping" in tag_cr["TraitMappingList"]:
            trait_mappings = [
                cls.convert_trait_mapping({"TraitMapping": entry})
                for entry in cls.ensure_list(tag_cr["TraitMappingList"]["TraitMapping"])
            ]
        deleted_scvs: list[DeletedScv] | None = None
        if "DeletedSCVList" in tag_cr and "DeletedSCV" in tag_cr["DeletedSCVList"]:
            deleted_scvs = [
                ConvertDeletedScv.xmldict_data_to_pb({"DeletedSCV": entry})
                for entry in cls.ensure_list(tag_cr["DeletedSCVList"]["DeletedSCV"])
            ]
        general_citations: list[GeneralCitations] | None = None
        if "GeneralCitations" in tag_cr:
            general_citations = [
                ConvertGeneralCitations.xmldict_data_to_pb({"GeneralCitations": entry})
                for entry in cls.ensure_list(tag_cr["GeneralCitations"])
            ]

        return ClassifiedRecord(
            simple_allele=simple_allele,
            haplotype=haplotype,
            genotype=genotype,
            rcv_list=rcv_list,
            classifications=classifications,
            clinical_assertions=clinical_assertions,
            trait_mappings=trait_mappings,
            deleted_scvs=deleted_scvs,
            general_citations=general_citations,
        )


class ConvertVariationArchive(ConverterBase):
    """Static method helper for converting XML data to to ``VariationArchive``."""

    #: Map for converting from XML value to protobuf enum.
    CONVERT_RECORD_TYPE: Dict[str, VariationArchive.RecordType.ValueType] = {
        "included": VariationArchive.RecordType.RECORD_TYPE_INCLUDED,
        "classified": VariationArchive.RecordType.RECORD_TYPE_CLASSIFIED,
    }

    @classmethod
    def convert_record_type(cls, value: str) -> VariationArchive.RecordType.ValueType:
        """Converts a string to a ``VariationArchive.RecordType``.

        Args:
            value: The string.

        Returns:
            The ``VariationArchive.RecordType``.
        """
        result = cls.CONVERT_RECORD_TYPE.get(value)
        if not result:
            raise ValueError(f"Unknown value {value}")
        else:
            return result

    #: Map for converting from XML value to protobuf enum.
    CONVERT_RECORD_STATUS: Dict[str, VariationArchive.RecordStatus.ValueType] = {
        "current": VariationArchive.RecordStatus.RECORD_STATUS_CURRENT,
        "previous": VariationArchive.RecordStatus.RECORD_STATUS_PREVIOUS,
        "replaced": VariationArchive.RecordStatus.RECORD_STATUS_REPLACED,
        "deleted": VariationArchive.RecordStatus.RECORD_STATUS_DELETED,
    }

    @classmethod
    def convert_record_status(cls, value: str) -> VariationArchive.RecordStatus.ValueType:
        """Converts a string to a ``VariationArchive.RecordStatus``.

        Args:
            value: The string.

        Returns:
            The ``VariationArchive.RecordStatus``.
        """
        result = cls.CONVERT_RECORD_STATUS.get(value)
        if not result:
            raise ValueError(f"Unknown value {value}")
        else:
            return result

    @classmethod
    def xmldict_data_to_pb(cls, value: dict[str, Any]) -> VariationArchive:
        """Converts a dict from ``xmltodict`` to a ``VariationArchive`` protobuf.

        Args:
            value: The dict from ``xmltodict``.

        Returns:
            The ``VariationArchive`` protobuf.
        """
        assert "VariationArchive" in value
        tag_va: dict[str, Any] = value["VariationArchive"]

        variation_id: int = int(tag_va["@VariationID"])
        variation_name: str = tag_va["@VariationName"]
        variation_type: str = tag_va["@VariationType"]
        date_created: google.protobuf.timestamp_pb2.Timestamp | None = None
        if "@DateCreated" in tag_va:
            date_created_dt = dateutil.parser.parse(tag_va["@DateCreated"])
            date_created_seconds = int(time.mktime(date_created_dt.timetuple()))
            date_created = google.protobuf.timestamp_pb2.Timestamp(seconds=date_created_seconds)
        date_last_updated: google.protobuf.timestamp_pb2.Timestamp | None = None
        if "@DateLastUpdated" in tag_va:
            date_last_updated_dt = dateutil.parser.parse(tag_va["@DateLastUpdated"])
            date_last_updated_seconds = int(time.mktime(date_last_updated_dt.timetuple()))
            date_last_updated = google.protobuf.timestamp_pb2.Timestamp(
                seconds=date_last_updated_seconds
            )
        most_recent_submission: google.protobuf.timestamp_pb2.Timestamp | None = None
        if "@MostRecentSubmission" in tag_va:
            most_recent_submission_dt = dateutil.parser.parse(tag_va["@MostRecentSubmission"])
            most_recent_submission_seconds = int(time.mktime(most_recent_submission_dt.timetuple()))
            most_recent_submission = google.protobuf.timestamp_pb2.Timestamp(
                seconds=most_recent_submission_seconds
            )
        accession: str = tag_va["@Accession"]
        version: int = int(tag_va["@Version"])
        number_of_submitters: int = int(tag_va["@NumberOfSubmitters"])
        number_of_submissions: int = int(tag_va["@NumberOfSubmissions"])
        record_type: VariationArchive.RecordType.ValueType = cls.convert_record_type(
            tag_va["@RecordType"]
        )

        record_status: VariationArchive.RecordStatus.ValueType = cls.convert_record_status(
            tag_va["RecordStatus"]
        )
        replaced_by: RecordHistory | None = None
        if "ReplacedBy" in tag_va:
            replaced_by = ConvertRecordHistory.xmldict_data_to_pb(
                {"ReplacedBy": tag_va["ReplacedBy"]}
            )
        replaceds: list[RecordHistory] | None = None
        if "ReplacedList" in tag_va and "Replaced" in tag_va["ReplacedList"]:
            replaceds = [
                ConvertRecordHistory.xmldict_data_to_pb({"Replaced": entry})
                for entry in cls.ensure_list(tag_va["ReplacedList"]["Replaced"])
            ]
        comment: Comment | None = None
        if "Comment" in tag_va:
            comment = ConvertComment.xmldict_data_to_pb({"Comment": tag_va["Comment"]})
        species: Species | None = None
        if "Species" in tag_va:
            species = ConvertSpecies.xmldict_data_to_pb({"Species": tag_va["Species"]})
        classified_record: ClassifiedRecord | None = None
        if "ClassifiedRecord" in tag_va:
            classified_record = ConvertClassifiedRecord.xmldict_data_to_pb(
                {"ClassifiedRecord": tag_va["ClassifiedRecord"]}
            )
        included_record: IncludedRecord | None = None
        if "IncludedRecord" in tag_va:
            included_record = ConvertIncludedRecord.xmldict_data_to_pb(
                {"IncludedRecord": tag_va["IncludedRecord"]}
            )

        return VariationArchive(
            variation_id=variation_id,
            variation_name=variation_name,
            variation_type=variation_type,
            date_created=date_created,
            date_last_updated=date_last_updated,
            most_recent_submission=most_recent_submission,
            accession=accession,
            version=version,
            number_of_submitters=number_of_submitters,
            number_of_submissions=number_of_submissions,
            record_type=record_type,
            record_status=record_status,
            replaced_by=replaced_by,
            replaceds=replaceds,
            comment=comment,
            species=species,
            classified_record=classified_record,
            included_record=included_record,
        )


class ConvertClinvarVariationRelease(ConverterBase):
    """Static method helper for converting XML data to to ``ClinvarVariationRelease``."""

    @classmethod
    def xmldict_data_to_pb(cls, value: dict[str, Any]) -> ClinvarVariationRelease:
        """Converts a dict from ``xmltodict`` to a ``ClinvarVariationRelease`` protobuf.

        Args:
            value: The dict from ``xmltodict``.

        Returns:
            The ``ClinvarVariationRelease`` protobuf.
        """
        assert "ClinVarVariationRelease" in value
        tag_release: dict[str, Any] = value["ClinVarVariationRelease"]

        release_date: google.protobuf.timestamp_pb2.Timestamp | None = None
        if "@ReleaseDate" in tag_release:
            release_date_dt = dateutil.parser.parse(tag_release["@ReleaseDate"])
            release_date_seconds = int(time.mktime(release_date_dt.timetuple()))
            release_date = google.protobuf.timestamp_pb2.Timestamp(seconds=release_date_seconds)
        variation_archives: list[VariationArchive] | None = None
        if "VariationArchive" in tag_release:
            variation_archives = [
                ConvertVariationArchive.xmldict_data_to_pb({"VariationArchive": entry})
                for entry in cls.ensure_list(tag_release["VariationArchive"])
            ]

        return ClinvarVariationRelease(
            release_date=release_date,
            variation_archives=variation_archives,
        )
