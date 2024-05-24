"""Tests for converting XML data to Protocol Buffers."""

import json
from typing import Any

from google.protobuf.json_format import MessageToDict
import pytest
import xmltodict

from clinvar_data.conversion.dict_to_pb import (
    ConvertAggregateClassificationSet,
    ConvertAggregatedGermlineClassification,
    ConvertAggregatedOncogenicityClassification,
    ConvertAggregatedSomaticClinicalImpact,
    ConvertAggregateGermlineReviewStatus,
    ConvertAggregateOncogenicityReviewStatus,
    ConvertAggregateSomaticClinicalImpactReviewStatus,
    ConvertAllele,
    ConvertAlleleDescription,
    ConvertAlleleScv,
    ConvertAssertion,
    ConvertAttributeSetElement,
    ConvertBaseAttribute,
    ConvertChromosome,
    ConvertCitation,
    ConvertClassificationScv,
    ConvertClassifiedCondition,
    ConvertClassifiedRecord,
    ConvertClinicalAssertion,
    ConvertClinicalAssertionRecordHistory,
    ConvertClinicalFeaturesAffectedStatusType,
    ConvertClinicalSignificance,
    ConvertClinvarVariationRelease,
    ConvertComment,
    ConvertCommentType,
    ConvertCooccurrence,
    ConvertDeletedScv,
    ConvertDescriptionHistory,
    ConvertDosageSensitivity,
    ConvertEvidenceType,
    ConvertFamilyData,
    ConvertFunctionalConsequence,
    ConvertGenericSetElement,
    ConvertGeneVariantRelationship,
    ConvertGenotype,
    ConvertGenotypeScv,
    ConvertHaplotype,
    ConvertHaplotypeScv,
    ConvertHaploVariationType,
    ConvertHgvsExpression,
    ConvertHgvsNucleotideExpression,
    ConvertHgvsProteinExpression,
    ConvertHgvsType,
    ConvertIncludedRecord,
    ConvertIndication,
    ConvertLocation,
    ConvertMethodListType,
    ConvertMethodType,
    ConvertNucleotideSequence,
    ConvertObservedIn,
    ConvertOrigin,
    ConvertOtherName,
    ConvertPhenotypeSetType,
    ConvertProteinSequence,
    ConvertRcvAccession,
    ConvertRecordHistory,
    ConvertSample,
    ConvertScv,
    ConvertSeverity,
    ConvertSoftware,
    ConvertSpecies,
    ConvertStatus,
    ConvertSubmitter,
    ConvertSubmitterIdentifiers,
    ConvertSubmitterReviewStatus,
    ConvertTrait,
    ConvertTraitSet,
    ConvertVariationArchive,
    ConvertVariationType,
    ConvertXref,
    ConvertZygosity,
)
from clinvar_data.pbs.clinvar_this.clinvar_public import (
    AggregateGermlineReviewStatus,
    AggregateOncogenicityReviewStatus,
    AggregateSomaticClinicalImpactReviewStatus,
    Assertion,
    Chromosome,
    ClinicalAssertion,
    ClinicalFeaturesAffectedStatusType,
    CommentType,
    EvidenceType,
    GeneVariantRelationship,
    HaploVariationType,
    HgvsType,
    Indication,
    Location,
    Method,
    MethodListType,
    NucleotideSequence,
    ObservedIn,
    Origin,
    PhenotypeSetType,
    ProteinSequence,
    Sample,
    Severity,
    Status,
    Submitter,
    SubmitterReviewStatus,
    Trait,
    TraitSet,
    VariationType,
    Zygosity,
)
from clinvar_data.pbs.clinvar_this.clinvar_public_pb2 import (
    ClassifiedRecord,
    VariationArchive,
)


@pytest.mark.parametrize(
    "xmldict_value,expected",
    [
        (
            "variant within gene",
            GeneVariantRelationship.GENE_VARIANT_RELATIONSHIP_VARIANT_WITHIN_GENE,
        ),
        (
            "gene overlapped by variant",
            GeneVariantRelationship.GENE_VARIANT_RELATIONSHIP_GENE_OVERLAPPED_BY_VARIANT,
        ),
        (
            "genes overlapped by variant",
            GeneVariantRelationship.GENE_VARIANT_RELATIONSHIP_GENE_OVERLAPPED_BY_VARIANT,
        ),
        (
            "variant near gene, upstream",
            GeneVariantRelationship.GENE_VARIANT_RELATIONSHIP_NEAR_GENE_UPSTREAM,
        ),
        (
            "near gene, upstream",
            GeneVariantRelationship.GENE_VARIANT_RELATIONSHIP_NEAR_GENE_UPSTREAM,
        ),
        (
            "variant near gene, downstream",
            GeneVariantRelationship.GENE_VARIANT_RELATIONSHIP_NEAR_GENE_DOWNSTREAM,
        ),
        (
            "near gene, downstream",
            GeneVariantRelationship.GENE_VARIANT_RELATIONSHIP_NEAR_GENE_DOWNSTREAM,
        ),
        (
            "asserted, but not computed",
            GeneVariantRelationship.GENE_VARIANT_RELATIONSHIP_ASSERTED_BUT_NOT_COMPUTED,
        ),
        (
            "within multiple genes by overlap",
            GeneVariantRelationship.GENE_VARIANT_RELATIONSHIP_WITHIN_MULTIPLE_GENES_BY_OVERLAP,
        ),
        (
            "within single gene",
            GeneVariantRelationship.GENE_VARIANT_RELATIONSHIP_WITHIN_SINGLE_GENE,
        ),
    ],
)
def test_convert_gene_variant_relationship(xmldict_value: str, expected: GeneVariantRelationship):
    result = ConvertGeneVariantRelationship.xmldict_data_to_pb(xmldict_value)
    assert result == expected


@pytest.mark.parametrize(
    "xmldict_value,expected",
    [
        ("mild", Severity.SEVERITY_MILD),
        ("moderate", Severity.SEVERITY_MODERATE),
        ("severe", Severity.SEVERITY_SEVERE),
    ],
)
def test_convert_severity(xmldict_value: str, expected: Severity.ValueType):
    result = ConvertSeverity.xmldict_data_to_pb(xmldict_value)
    assert result == expected


@pytest.mark.parametrize(
    "xmldict_value,expected",
    [
        ("current", Status.STATUS_CURRENT),
        ("completed and retired", Status.STATUS_COMPLETED_AND_RETIRED),
        ("delete", Status.STATUS_DELETE),
        ("in development", Status.STATUS_IN_DEVELOPMENT),
        ("reclassified", Status.STATUS_RECLASSIFIED),
        ("reject", Status.STATUS_REJECT),
        ("secondary", Status.STATUS_SECONDARY),
        ("suppressed", Status.STATUS_SUPPRESSED),
        ("under review", Status.STATUS_UNDER_REVIEW),
    ],
)
def test_convert_status(xmldict_value: str, expected: Status.ValueType):
    result = ConvertStatus.xmldict_data_to_pb(xmldict_value)
    assert result == expected


@pytest.mark.parametrize(
    "xmldict_value,expected",
    [
        (
            "no classification provided",
            SubmitterReviewStatus.SUBMITTER_REVIEW_STATUS_NO_CLASSIFICATION_PROVIDED,
        ),
        (
            "no assertion criteria provided",
            SubmitterReviewStatus.SUBMITTER_REVIEW_STATUS_NO_ASSERTION_CRITERIA_PROVIDED,
        ),
        (
            "criteria provided, single submitter",
            SubmitterReviewStatus.SUBMITTER_REVIEW_STATUS_CRITERIA_PROVIDED_SINGLE_SUBMITTER,
        ),
        (
            "reviewed by expert panel",
            SubmitterReviewStatus.SUBMITTER_REVIEW_STATUS_REVIEWED_BY_EXPERT_PANEL,
        ),
        (
            "practice guideline",
            SubmitterReviewStatus.SUBMITTER_REVIEW_STATUS_PRACTICE_GUIDELINE,
        ),
        (
            "flagged submission",
            SubmitterReviewStatus.SUBMITTER_REVIEW_STATUS_FLAGGED_SUBMISSION,
        ),
        (
            "criteria provided, multiple submitters, no conflicts",
            SubmitterReviewStatus.SUBMITTER_REVIEW_STATUS_CRITERIA_PROVIDED_MULTIPLE_SUBMITTERS_NO_CONFLICTS,
        ),
        (
            "criteria provided, conflicting classifications",
            SubmitterReviewStatus.SUBMITTER_REVIEW_STATUS_CRITERIA_PROVIDED_CONFLICTING_CLASSIFICATIONS,
        ),
        (
            "classified by single submitter",
            SubmitterReviewStatus.SUBMITTER_REVIEW_STATUS_CLASSIFIED_BY_SINGLE_SUBMITTER,
        ),
        (
            "reviewed by professional society",
            SubmitterReviewStatus.SUBMITTER_REVIEW_STATUS_REVIEWED_BY_PROFESSIONAL_SOCIETY,
        ),
        (
            "not classified by submitter",
            SubmitterReviewStatus.SUBMITTER_REVIEW_STATUS_NOT_CLASSIFIED_BY_SUBMITTER,
        ),
        (
            "classified by multiple submitters",
            SubmitterReviewStatus.SUBMITTER_REVIEW_STATUS_CLASSIFIED_BY_MULTIPLE_SUBMITTERS,
        ),
    ],
)
def test_convert_submitter_review_status(
    xmldict_value: str, expected: SubmitterReviewStatus.ValueType
):
    result = ConvertSubmitterReviewStatus.xmldict_data_to_pb(xmldict_value)
    assert result == expected


@pytest.mark.parametrize(
    "xmldict_value,expected",
    [
        ("Homozygote", Zygosity.ZYGOSITY_HOMOZYGOTE),
        ("SingleHeterozygote", Zygosity.ZYGOSITY_SINGLE_HETEROZYGOTE),
        ("CompoundHeterozygote", Zygosity.ZYGOSITY_COMPOUND_HETEROZYGOTE),
        ("Hemizygote", Zygosity.ZYGOSITY_HEMIZYGOTE),
        ("not provided", Zygosity.ZYGOSITY_NOT_PROVIDED),
    ],
)
def test_convert_zygosity(xmldict_value: str, expected: Zygosity.ValueType):
    result = ConvertZygosity.xmldict_data_to_pb(xmldict_value)
    assert result == expected


@pytest.mark.parametrize(
    "xmldict_value,expected",
    [
        ("variation to disease", Assertion.ASSERTION_VARIATION_TO_DISEASE),
        ("variation to included disease", Assertion.ASSERTION_VARIATION_TO_INCLUDED_DISEASE),
        (
            "variation in modifier gene to disease",
            Assertion.ASSERTION_VARIATION_IN_MODIFIER_GENE_TO_DISEASE,
        ),
        ("confers sensitivity", Assertion.ASSERTION_CONFERS_SENSITIVITY),
        ("confers resistance", Assertion.ASSERTION_CONFERS_RESISTANCE),
        ("variant to named protein", Assertion.ASSERTION_VARIANT_TO_NAMED_PROTEIN),
    ],
)
def test_convert_assertion(xmldict_value: str, expected: Assertion.ValueType):
    result = ConvertAssertion.xmldict_data_to_pb(xmldict_value)
    assert result == expected


@pytest.mark.parametrize(
    "xmldict_value,expected",
    [
        (
            "no classification provided",
            AggregateGermlineReviewStatus.AGGREGATE_GERMLINE_REVIEW_STATUS_NO_CLASSIFICATION_PROVIDED,
        ),
        (
            "no assertion criteria provided",
            AggregateGermlineReviewStatus.AGGREGATE_GERMLINE_REVIEW_STATUS_NO_ASSERTION_CRITERIA_PROVIDED,
        ),
        (
            "criteria provided, single submitter",
            AggregateGermlineReviewStatus.AGGREGATE_GERMLINE_REVIEW_STATUS_CRITERIA_PROVIDED_SINGLE_SUBMITTER,
        ),
        (
            "criteria provided, multiple submitters, no conflicts",
            AggregateGermlineReviewStatus.AGGREGATE_GERMLINE_REVIEW_STATUS_CRITERIA_PROVIDED_MULTIPLE_SUBMITTERS_NO_CONFLICTS,
        ),
        (
            "criteria provided, conflicting classifications",
            AggregateGermlineReviewStatus.AGGREGATE_GERMLINE_REVIEW_STATUS_CRITERIA_PROVIDED_CONFLICTING_CLASSIFICATIONS,
        ),
        (
            "reviewed by expert panel",
            AggregateGermlineReviewStatus.AGGREGATE_GERMLINE_REVIEW_STATUS_REVIEWED_BY_EXPERT_PANEL,
        ),
        (
            "practice guideline",
            AggregateGermlineReviewStatus.AGGREGATE_GERMLINE_REVIEW_STATUS_PRACTICE_GUIDELINE,
        ),
        (
            "no classifications from unflagged records",
            AggregateGermlineReviewStatus.AGGREGATE_GERMLINE_REVIEW_STATUS_NO_CLASSIFICATIONS_FROM_UNFLAGGED_RECORDS,
        ),
        (
            "no classification for the single variant",
            AggregateGermlineReviewStatus.AGGREGATE_GERMLINE_REVIEW_STATUS_NO_CLASSIFICATION_FOR_THE_SINGLE_VARIANT,
        ),
    ],
)
def test_convert_aggregate_germline_review_status(
    xmldict_value: str, expected: AggregateGermlineReviewStatus.ValueType
):
    result = ConvertAggregateGermlineReviewStatus.xmldict_data_to_pb(xmldict_value)
    assert result == expected


@pytest.mark.parametrize(
    "xmldict_value,expected",
    [
        (
            "no classification provided",
            AggregateSomaticClinicalImpactReviewStatus.AGGREGATE_SOMATIC_CLINICAL_IMPACT_REVIEW_STATUS_NO_CLASSIFICATION_PROVIDED,
        ),
        (
            "no assertion criteria provided",
            AggregateSomaticClinicalImpactReviewStatus.AGGREGATE_SOMATIC_CLINICAL_IMPACT_REVIEW_STATUS_NO_ASSERTION_CRITERIA_PROVIDED,
        ),
        (
            "criteria provided, single submitter",
            AggregateSomaticClinicalImpactReviewStatus.AGGREGATE_SOMATIC_CLINICAL_IMPACT_REVIEW_STATUS_CRITERIA_PROVIDED_SINGLE_SUBMITTER,
        ),
        (
            "criteria provided, multiple submitters",
            AggregateSomaticClinicalImpactReviewStatus.AGGREGATE_SOMATIC_CLINICAL_IMPACT_REVIEW_STATUS_CRITERIA_PROVIDED_MULTIPLE_SUBMITTERS,
        ),
        (
            "reviewed by expert panel",
            AggregateSomaticClinicalImpactReviewStatus.AGGREGATE_SOMATIC_CLINICAL_IMPACT_REVIEW_STATUS_REVIEWED_BY_EXPERT_PANEL,
        ),
        (
            "practice guideline",
            AggregateSomaticClinicalImpactReviewStatus.AGGREGATE_SOMATIC_CLINICAL_IMPACT_REVIEW_STATUS_PRACTICE_GUIDELINE,
        ),
        (
            "no classifications from unflagged records",
            AggregateSomaticClinicalImpactReviewStatus.AGGREGATE_SOMATIC_CLINICAL_IMPACT_REVIEW_STATUS_NO_CLASSIFICATIONS_FROM_UNFLAGGED_RECORDS,
        ),
        (
            "no classification for the single variant",
            AggregateSomaticClinicalImpactReviewStatus.AGGREGATE_SOMATIC_CLINICAL_IMPACT_REVIEW_STATUS_NO_CLASSIFICATION_FOR_THE_SINGLE_VARIANT,
        ),
    ],
)
def test_convert_aggregate_somatic_clinical_impact_review_status(
    xmldict_value: str, expected: AggregateSomaticClinicalImpactReviewStatus.ValueType
):
    result = ConvertAggregateSomaticClinicalImpactReviewStatus.xmldict_data_to_pb(xmldict_value)
    assert result == expected


@pytest.mark.parametrize(
    "xmldict_value,expected",
    [
        (
            "no classification provided",
            AggregateOncogenicityReviewStatus.AGGREGATE_ONCOGENICITY_REVIEW_STATUS_NO_CLASSIFICATION_PROVIDED,
        ),
        (
            "no assertion criteria provided",
            AggregateOncogenicityReviewStatus.AGGREGATE_ONCOGENICITY_REVIEW_STATUS_NO_ASSERTION_CRITERIA_PROVIDED,
        ),
        (
            "criteria provided, single submitter",
            AggregateOncogenicityReviewStatus.AGGREGATE_ONCOGENICITY_REVIEW_STATUS_CRITERIA_PROVIDED_SINGLE_SUBMITTER,
        ),
        (
            "criteria provided, multiple submitters, no conflicts",
            AggregateOncogenicityReviewStatus.AGGREGATE_ONCOGENICITY_REVIEW_STATUS_CRITERIA_PROVIDED_MULTIPLE_SUBMITTERS_NO_CONFLICTS,
        ),
        (
            "criteria provided, conflicting classifications",
            AggregateOncogenicityReviewStatus.AGGREGATE_ONCOGENICITY_REVIEW_STATUS_CRITERIA_PROVIDED_CONFLICTING_CLASSIFICATIONS,
        ),
        (
            "reviewed by expert panel",
            AggregateOncogenicityReviewStatus.AGGREGATE_ONCOGENICITY_REVIEW_STATUS_REVIEWED_BY_EXPERT_PANEL,
        ),
        (
            "practice guideline",
            AggregateOncogenicityReviewStatus.AGGREGATE_ONCOGENICITY_REVIEW_STATUS_PRACTICE_GUIDELINE,
        ),
        (
            "no classifications from unflagged records",
            AggregateOncogenicityReviewStatus.AGGREGATE_ONCOGENICITY_REVIEW_STATUS_NO_CLASSIFICATIONS_FROM_UNFLAGGED_RECORDS,
        ),
        (
            "no classification for the single variant",
            AggregateOncogenicityReviewStatus.AGGREGATE_ONCOGENICITY_REVIEW_STATUS_NO_CLASSIFICATION_FOR_THE_SINGLE_VARIANT,
        ),
    ],
)
def test_convert_aggregate_oncogenicity_review_status(
    xmldict_value: str, expected: AggregateOncogenicityReviewStatus.ValueType
):
    result = ConvertAggregateOncogenicityReviewStatus.xmldict_data_to_pb(xmldict_value)
    assert result == expected


@pytest.mark.parametrize(
    "xmldict_value,expected",
    [
        ("germline", Origin.ORIGIN_GERMLINE),
        ("somatic", Origin.ORIGIN_SOMATIC),
        ("de novo", Origin.ORIGIN_DE_NOVO),
        ("not provided", Origin.ORIGIN_NOT_PROVIDED),
        ("inherited", Origin.ORIGIN_INHERITED),
        ("maternal", Origin.ORIGIN_MATERNAL),
        ("paternal", Origin.ORIGIN_PATERNAL),
        ("uniparental", Origin.ORIGIN_UNIPARENTAL),
        ("biparental", Origin.ORIGIN_BIPARENTAL),
        ("not-reported", Origin.ORIGIN_NOT_REPORTED),
        ("tested-inconclusive", Origin.ORIGIN_TESTED_INCONCLUSIVE),
        ("not applicable", Origin.ORIGIN_NOT_APPLICABLE),
        ("experimentally generated", Origin.ORIGIN_EXPERIMENTALLY_GENERATED),
    ],
)
def test_convert_origin(xmldict_value: str, expected: Origin.ValueType):
    result = ConvertOrigin.xmldict_data_to_pb(xmldict_value)
    assert result == expected


@pytest.mark.parametrize(
    "xmldict_value,expected",
    [
        ("genomic, top-level", NucleotideSequence.NUCLEOTIDE_SEQUENCE_GENOMIC_TOP_LEVEL),
        ("genomic, RefSeqGene", NucleotideSequence.NUCLEOTIDE_SEQUENCE_GENOMIC_REF_SEQ_GENE),
        ("genomic", NucleotideSequence.NUCLEOTIDE_SEQUENCE_GENOMIC),
        ("coding", NucleotideSequence.NUCLEOTIDE_SEQUENCE_CODING),
        ("non-coding", NucleotideSequence.NUCLEOTIDE_SEQUENCE_NON_CODING),
        ("protein", NucleotideSequence.NUCLEOTIDE_SEQUENCE_PROTEIN),
    ],
)
def test_convert_nucleotide_sequence(xmldict_value: str, expected: NucleotideSequence.ValueType):
    result = ConvertNucleotideSequence.xmldict_data_to_pb(xmldict_value)
    assert result == expected


@pytest.mark.parametrize(
    "xmldict_value,expected",
    [
        ("protein", ProteinSequence.PROTEIN_SEQUENCE_PROTEIN),
    ],
)
def test_convert_protein_sequence(xmldict_value: str, expected: ProteinSequence.ValueType):
    result = ConvertProteinSequence.xmldict_data_to_pb(xmldict_value)
    assert result == expected


@pytest.mark.parametrize(
    "xmldict_value,expected",
    [
        ("Disease", PhenotypeSetType.PHENOTYPE_SET_TYPE_DISEASE),
        ("DrugResponse", PhenotypeSetType.PHENOTYPE_SET_TYPE_DRUG_RESPONSE),
        ("Finding", PhenotypeSetType.PHENOTYPE_SET_TYPE_FINDING),
        ("PhenotypeInstruction", PhenotypeSetType.PHENOTYPE_SET_TYPE_PHENOTYPE_INSTRUCTION),
        ("TraitChoice", PhenotypeSetType.PHENOTYPE_SET_TYPE_TRAIT_CHOICE),
    ],
)
def test_convert_phenotype_set_type(xmldict_value: str, expected: PhenotypeSetType.ValueType):
    result = ConvertPhenotypeSetType.xmldict_data_to_pb(xmldict_value)
    assert result == expected


@pytest.mark.parametrize(
    "xmldict_value,expected",
    [
        ("1", Chromosome.CHROMOSOME_1),
        ("2", Chromosome.CHROMOSOME_2),
        ("3", Chromosome.CHROMOSOME_3),
        ("4", Chromosome.CHROMOSOME_4),
        ("5", Chromosome.CHROMOSOME_5),
        ("6", Chromosome.CHROMOSOME_6),
        ("7", Chromosome.CHROMOSOME_7),
        ("8", Chromosome.CHROMOSOME_8),
        ("9", Chromosome.CHROMOSOME_9),
        ("10", Chromosome.CHROMOSOME_10),
        ("11", Chromosome.CHROMOSOME_11),
        ("12", Chromosome.CHROMOSOME_12),
        ("13", Chromosome.CHROMOSOME_13),
        ("14", Chromosome.CHROMOSOME_14),
        ("15", Chromosome.CHROMOSOME_15),
        ("16", Chromosome.CHROMOSOME_16),
        ("17", Chromosome.CHROMOSOME_17),
        ("18", Chromosome.CHROMOSOME_18),
        ("19", Chromosome.CHROMOSOME_19),
        ("20", Chromosome.CHROMOSOME_20),
        ("21", Chromosome.CHROMOSOME_21),
        ("22", Chromosome.CHROMOSOME_22),
        ("X", Chromosome.CHROMOSOME_X),
        ("Y", Chromosome.CHROMOSOME_Y),
        ("MT", Chromosome.CHROMOSOME_MT),
        ("PAR", Chromosome.CHROMOSOME_PAR),
        ("Un", Chromosome.CHROMOSOME_UN),
    ],
)
def test_convert_chromosome(xmldict_value: str, expected: Chromosome.ValueType):
    result = ConvertChromosome.xmldict_data_to_pb(xmldict_value)
    assert result == expected


@pytest.mark.parametrize(
    "xmldict_value,expected",
    [
        ("public", CommentType.COMMENT_TYPE_PUBLIC),
        ("ConvertedByNCBI", CommentType.COMMENT_TYPE_CONVERTED_BY_NCB),
        ("MissingFromAssembly", CommentType.COMMENT_TYPE_MISSING_FROM_ASSEMBLY),
        (
            "GenomicLocationNotEstablished",
            CommentType.COMMENT_TYPE_GENOMIC_LOCATION_NOT_ESTABLISHED,
        ),
        (
            "LocationOnGenomeAndProductNotAligned",
            CommentType.COMMENT_TYPE_LOCATION_ON_GENOME_AND_PRODUCT_NOT_ALIGNED,
        ),
        ("DeletionComment", CommentType.COMMENT_TYPE_DELETION_COMMENT),
        ("MergeComment", CommentType.COMMENT_TYPE_MERGE_COMMENT),
        (
            "AssemblySpecificAlleleDefinition",
            CommentType.COMMENT_TYPE_ASSEMBLY_SPECIFIC_ALLELE_DEFINITION,
        ),
        (
            "AlignmentGapMakesAppearInconsistent",
            CommentType.COMMENT_TYPE_ALIGNMENT_GAP_MAKES_APPEAR_INCONSISTENT,
        ),
        ("ExplanationOfClassification", CommentType.COMMENT_TYPE_EXPLANATION_OF_CLASSIFICATION),
        ("FlaggedComment", CommentType.COMMENT_TYPE_FLAGGED_COMMENT),
    ],
)
def test_convert_comment_type(xmldict_value: str, expected: CommentType.ValueType):
    result = ConvertCommentType.xmldict_data_to_pb(xmldict_value)
    assert result == expected


@pytest.mark.parametrize(
    "xmldict_value,expected",
    [
        ("Diplotype", VariationType.VARIATION_TYPE_DIPLOTYPE),
        ("CompoundHeterozygote", VariationType.VARIATION_TYPE_COMPOUND_HETEROZYGOTE),
        ("Distinct chromosomes", VariationType.VARIATION_TYPE_DISTINCT_CHROMOSOMES),
    ],
)
def test_convert_variation_type(xmldict_value: str, expected: VariationType.ValueType):
    result = ConvertVariationType.xmldict_data_to_pb(xmldict_value)
    assert result == expected


@pytest.mark.parametrize(
    "xmldict_value,expected",
    [
        ("Genetic", EvidenceType.EVIDENCE_TYPE_GENETIC),
        ("Experimental", EvidenceType.EVIDENCE_TYPE_EXPERIMENTAL),
        ("Population", EvidenceType.EVIDENCE_TYPE_POPULATION),
        ("Computational", EvidenceType.EVIDENCE_TYPE_COMPUTATIONAL),
    ],
)
def test_convert_evidence_type(xmldict_value: str, expected: EvidenceType.ValueType):
    result = ConvertEvidenceType.xmldict_data_to_pb(xmldict_value)
    assert result == expected


@pytest.mark.parametrize(
    "xmldict_value,expected",
    [
        ("literature only", MethodListType.METHOD_LIST_TYPE_LITERATURE_ONLY),
        ("reference population", MethodListType.METHOD_LIST_TYPE_REFERENCE_POPULATION),
        ("case-control", MethodListType.METHOD_LIST_TYPE_CASE_CONTROL),
        ("clinical testing", MethodListType.METHOD_LIST_TYPE_CLINICAL_TESTING),
        ("in vitro", MethodListType.METHOD_LIST_TYPE_IN_VITRO),
        ("in vivo", MethodListType.METHOD_LIST_TYPE_IN_VIVO),
        ("research", MethodListType.METHOD_LIST_TYPE_RESEARCH),
        ("curation", MethodListType.METHOD_LIST_TYPE_CURATION),
        ("not provided", MethodListType.METHOD_LIST_TYPE_NOT_PROVIDED),
        ("provider interpretation", MethodListType.METHOD_LIST_TYPE_PROVIDER_INTERPRETATION),
        ("phenotyping only", MethodListType.METHOD_LIST_TYPE_PHENOTYPING_ONLY),
    ],
)
def test_convert_method_list_type(xmldict_value: str, expected: MethodListType.ValueType):
    result = ConvertMethodListType.xmldict_data_to_pb(xmldict_value)
    assert result == expected


@pytest.mark.parametrize(
    "xmldict_value,expected",
    [
        ("coding", HgvsType.HGVS_TYPE_CODING),
        ("genomic", HgvsType.HGVS_TYPE_GENOMIC),
        ("genomic, top-level", HgvsType.HGVS_TYPE_GENOMIC_TOP_LEVEL),
        ("non-coding", HgvsType.HGVS_TYPE_NON_CODING),
        ("protein", HgvsType.HGVS_TYPE_PROTEIN),
    ],
)
def test_convert_hgvs_type(xmldict_value: str, expected: HgvsType.ValueType):
    result = ConvertHgvsType.xmldict_data_to_pb(xmldict_value)
    assert result == expected


@pytest.mark.parametrize(
    "xmldict_value,expected",
    [
        (
            "present",
            ClinicalFeaturesAffectedStatusType.CLINICAL_FEATURES_AFFECTED_STATUS_TYPE_PRESENT,
        ),
        (
            "absent",
            ClinicalFeaturesAffectedStatusType.CLINICAL_FEATURES_AFFECTED_STATUS_TYPE_ABSENT,
        ),
        (
            "not tested",
            ClinicalFeaturesAffectedStatusType.CLINICAL_FEATURES_AFFECTED_STATUS_TYPE_NOT_TESTED,
        ),
    ],
)
def test_convert_clinical_features_affected_status_type(
    xmldict_value: str, expected: ClinicalFeaturesAffectedStatusType.ValueType
):
    result = ConvertClinicalFeaturesAffectedStatusType.xmldict_data_to_pb(xmldict_value)
    assert result == expected


@pytest.mark.parametrize(
    "xmldict_value,expected",
    [
        ("Haplotype", HaploVariationType.HAPLO_VARIATION_TYPE_HAPLOTYPE),
        (
            "Haplotype, single variant",
            HaploVariationType.HAPLO_VARIATION_TYPE_HAPLOTYPE_SINGLE_VARIANT,
        ),
        ("Variation", HaploVariationType.HAPLO_VARIATION_TYPE_VARIATION),
        ("Phase unknown", HaploVariationType.HAPLO_VARIATION_TYPE_PHASE_UNKNOWN),
        (
            "Haplotype defined by a single variant",
            HaploVariationType.HAPLO_VARIATION_TYPE_HAPLOTYPE_DEFINED_BY_SINGLE_VARIANT,
        ),
    ],
)
def test_convert_haplo_variation_type(xmldict_value: str, expected: HaploVariationType.ValueType):
    result = ConvertHaploVariationType.xmldict_data_to_pb(xmldict_value)
    assert result == expected


@pytest.mark.parametrize(
    "xml_str,expected_json",
    [
        (
            """
            <Comment DataSource="ClinGen" Type="public">ClinGen staff contributed the HGVS expression for this variant.</Comment>
            """,
            {
                "dataSource": "ClinGen",
                "type": "COMMENT_TYPE_PUBLIC",
                "value": "ClinGen staff contributed the HGVS expression for this variant.",
            },
        ),
        (
            """
            <Comment>ClinGen staff contributed the HGVS expression for this variant.</Comment>
            """,
            {
                "value": "ClinGen staff contributed the HGVS expression for this variant.",
            },
        ),
    ],
)
def test_convert_comment(xml_str: str, expected_json: Any):
    xmldict_value = xmltodict.parse(xml_str)
    result = ConvertComment.xmldict_data_to_pb(xmldict_value)
    result_json = MessageToDict(result)
    assert result_json == expected_json


@pytest.mark.parametrize(
    "xml_str,expected_json",
    [
        (
            """
            <XRef ID="CA215070" DB="ClinGen"/>
            """,
            {
                "id": "CA215070",
                "db": "ClinGen",
            },
        ),
        (
            """
            <XRef ID="MONDO:0008963" DB="MONDO" Status="current"/>
            """,
            {
                "id": "MONDO:0008963",
                "db": "MONDO",
                "status": "STATUS_CURRENT",
            },
        ),
        (
            """
            <XRef DB="GTR" ID="GTR000553916.1" URL="http://www.ncbi.nlm.nih.gov/gtr/tests/553916/"/>
            """,
            {
                "db": "GTR",
                "id": "GTR000553916.1",
                "url": "http://www.ncbi.nlm.nih.gov/gtr/tests/553916/",
            },
        ),
    ],
)
def test_convert_xref(xml_str: str, expected_json: Any):
    xmldict_value = xmltodict.parse(xml_str)
    result = ConvertXref.xmldict_data_to_pb(xmldict_value)
    result_json = MessageToDict(result)
    assert result_json == expected_json


@pytest.mark.parametrize(
    "xml_str,expected_json",
    [
        (
            """
            <Citation>
                <ID Source="PubMed">20613862</ID>
            </Citation>
            """,
            {
                "ids": [
                    {
                        "source": "PubMed",
                        "value": "20613862",
                    },
                ],
            },
        ),
        (
            """
            <Citation Type="practice guideline" Abbrev="DailyMed Drug Label, 2020">
                <URL>https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=0ab0c9f8-3eee-4e0f-9f3f-c1e16aaffe25</URL>
                <CitationText>DailyMed Drug Label, KALYDECO, 2020</CitationText>
            </Citation>
            """,
            {
                "abbrev": "DailyMed Drug Label, 2020",
                "citationText": "DailyMed Drug Label, KALYDECO, 2020",
                "type": "practice guideline",
                "url": "https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=0ab0c9f8-3eee-4e0f-9f3f-c1e16aaffe25",
            },
        ),
        (
            """
            <Citation Type="review" Abbrev="GeneReviews">
                <ID Source="PubMed">20301339</ID>
                <ID Source="BookShelf">NBK1160</ID>
            </Citation>
            """,
            {
                "abbrev": "GeneReviews",
                "ids": [
                    {
                        "source": "PubMed",
                        "value": "20301339",
                    },
                    {
                        "source": "BookShelf",
                        "value": "NBK1160",
                    },
                ],
                "type": "review",
            },
        ),
    ],
)
def test_convert_citation(xml_str: str, expected_json: Any):
    xmldict_value = xmltodict.parse(xml_str)

    result = ConvertCitation.xmldict_data_to_pb(xmldict_value)
    result_json = MessageToDict(result)
    assert result_json == expected_json


@pytest.mark.parametrize(
    "xml_str,expected_json",
    [
        (
            """
            <Attribute Type="VariantAlleles" integerValue="2"/>
            """,
            {
                "integerValue": "2",
            },
        ),
        (
            """
            <Attribute Type="public definition">In WDR62 primary microcephaly ...</Attribute>
            """,
            {"value": "In WDR62 primary microcephaly ..."},
        ),
        (
            """
            <Attribute Type="TestingLaboratory" dateValue="2020-03-18" integerValue="26957">GeneDx</Attribute>
            """,
            {
                "dateValue": "2020-03-18T00:00:00Z",
                "integerValue": "26957",
                "value": "GeneDx",
            },
        ),
    ],
)
def test_convert_base_attribute(xml_str: str, expected_json: Any):
    xmldict_value = xmltodict.parse(xml_str)
    result = ConvertBaseAttribute.xmldict_data_to_pb(xmldict_value)
    result_json = MessageToDict(result)
    assert result_json == expected_json


@pytest.mark.parametrize(
    "xml_str,expected_json",
    [
        (
            """
            <NucleotideExpression sequenceAccessionVersion="NM_001166688.2" sequenceAccession="NM_001166688" sequenceVersion="2" change="c.2137A&gt;G">
                <Expression>NM_001166688.2:c.2137A&gt;G</Expression>
            </NucleotideExpression>
            """,
            {
                "change": "c.2137A>G",
                "expression": "NM_001166688.2:c.2137A>G",
                "sequenceAccession": "NM_001166688",
                "sequenceAccessionVersion": "NM_001166688.2",
                "sequenceVersion": 2,
            },
        ),
        (
            """
            <NucleotideExpression sequenceAccessionVersion="NM_005572.4" sequenceAccession="NM_005572" sequenceVersion="4" change="c.165G&gt;A" MANEPlusClinical="true">
                <Expression>NM_005572.4:c.165G&gt;A</Expression>
            </NucleotideExpression>
            """,
            {
                "change": "c.165G>A",
                "expression": "NM_005572.4:c.165G>A",
                "manePlusClinical": True,
                "sequenceAccession": "NM_005572",
                "sequenceAccessionVersion": "NM_005572.4",
                "sequenceVersion": 4,
            },
        ),
        (
            """
            <NucleotideExpression sequenceAccessionVersion="NM_000519.4" sequenceAccession="NM_000519" sequenceVersion="4" change="c.8A&gt;G" MANESelect="true">
                <Expression>NM_000519.4:c.8A&gt;G</Expression>
            </NucleotideExpression>
            """,
            {
                "change": "c.8A>G",
                "expression": "NM_000519.4:c.8A>G",
                "maneSelect": True,
                "sequenceAccession": "NM_000519",
                "sequenceAccessionVersion": "NM_000519.4",
                "sequenceVersion": 4,
            },
        ),
    ],
)
def test_convert_hgvs_nucleotide_expression(xml_str: str, expected_json: Any):
    xmldict_value = xmltodict.parse(xml_str)
    result = ConvertHgvsNucleotideExpression.xmldict_data_to_pb(xmldict_value)
    result_json = MessageToDict(result)
    assert result_json == expected_json


@pytest.mark.parametrize(
    "xml_str,expected_json",
    [
        (
            """
            <ProteinExpression sequenceAccessionVersion="LRG_1247p1" sequenceAccession="LRG_1247p1" change="p.Arg27_Ile28delinsLeuLeuTer">
                <Expression>LRG_1247p1:p.Arg27_Ile28delinsLeuLeuTer</Expression>
            </ProteinExpression>
            """,
            {
                "change": "p.Arg27_Ile28delinsLeuLeuTer",
                "expression": "LRG_1247p1:p.Arg27_Ile28delinsLeuLeuTer",
                "sequenceAccession": "LRG_1247p1",
                "sequenceAccessionVersion": "LRG_1247p1",
            },
        ),
        (
            """
            <ProteinExpression sequenceAccessionVersion="NP_001077430.1" sequenceAccession="NP_001077430" sequenceVersion="1" change="p.Gln470Ter">
                <Expression>NP_001077430.1:p.Gln470Ter</Expression>
            </ProteinExpression>
            """,
            {
                "change": "p.Gln470Ter",
                "expression": "NP_001077430.1:p.Gln470Ter",
                "sequenceAccession": "NP_001077430",
                "sequenceAccessionVersion": "NP_001077430.1",
                "sequenceVersion": 1,
            },
        ),
    ],
)
def test_convert_hgvs_protein_expression_xmldict_data_to_pb(xml_str: str, expected_json: Any):
    xmldict_value = xmltodict.parse(xml_str)
    result = ConvertHgvsProteinExpression.xmldict_data_to_pb(xmldict_value)
    result_json = MessageToDict(result)
    assert result_json == expected_json


@pytest.mark.parametrize(
    "xml_str,expected_json",
    [
        (
            """
            <HGVS Type="coding">
                <NucleotideExpression sequenceAccessionVersion="NM_001364858.1" sequenceAccession="NM_001364858" sequenceVersion="1" change="c.-202_-199delinsTGCTGTAAACTGTAACTGTAAA">
                    <Expression>NM_001364858.1:c.-202_-199delinsTGCTGTAAACTGTAACTGTAAA</Expression>
                </NucleotideExpression>
                <MolecularConsequence ID="SO:0001623" Type="5 prime UTR variant" DB="SO"/>
            </HGVS>
            """,
            {
                "molecularConsequences": [
                    {
                        "db": "SO",
                        "id": "SO:0001623",
                        "type": "5 prime UTR variant",
                    },
                ],
                "nucleotideExpression": {
                    "change": "c.-202_-199delinsTGCTGTAAACTGTAACTGTAAA",
                    "expression": "NM_001364858.1:c.-202_-199delinsTGCTGTAAACTGTAACTGTAAA",
                    "sequenceAccession": "NM_001364858",
                    "sequenceAccessionVersion": "NM_001364858.1",
                    "sequenceVersion": 1,
                },
                "type": "HGVS_TYPE_CODING",
            },
        ),
        (
            """
            <HGVS Assembly="GRCh38" Type="genomic, top-level">
                <NucleotideExpression sequenceAccessionVersion="NC_000008.11" sequenceAccession="NC_000008" sequenceVersion="11" change="g.18062383G&gt;C" Assembly="GRCh38">
                    <Expression>NC_000008.11:g.18062383G&gt;C</Expression>
                </NucleotideExpression>
            </HGVS>
            """,
            {
                "assembly": "GRCh38",
                "nucleotideExpression": {
                    "change": "g.18062383G>C",
                    "expression": "NC_000008.11:g.18062383G>C",
                    "sequenceAccession": "NC_000008",
                    "sequenceAccessionVersion": "NC_000008.11",
                    "sequenceVersion": 11,
                },
                "type": "HGVS_TYPE_GENOMIC_TOP_LEVEL",
            },
        ),
        (
            """
            <HGVS Type="coding">
                <NucleotideExpression sequenceAccessionVersion="LRG_1247t1" sequenceAccession="LRG_1247t1" change="c.80_83delinsTGCTGTAAACTGTAACTGTAAA">
                    <Expression>LRG_1247t1:c.80_83delinsTGCTGTAAACTGTAACTGTAAA</Expression>
                </NucleotideExpression>
                <ProteinExpression sequenceAccessionVersion="LRG_1247p1" sequenceAccession="LRG_1247p1" change="p.Arg27_Ile28delinsLeuLeuTer">
                    <Expression>LRG_1247p1:p.Arg27_Ile28delinsLeuLeuTer</Expression>
                </ProteinExpression>
            </HGVS>
            """,
            {
                "nucleotideExpression": {
                    "change": "c.80_83delinsTGCTGTAAACTGTAACTGTAAA",
                    "expression": "LRG_1247t1:c.80_83delinsTGCTGTAAACTGTAACTGTAAA",
                    "sequenceAccession": "LRG_1247t1",
                    "sequenceAccessionVersion": "LRG_1247t1",
                },
                "proteinExpression": {
                    "change": "p.Arg27_Ile28delinsLeuLeuTer",
                    "expression": "LRG_1247p1:p.Arg27_Ile28delinsLeuLeuTer",
                    "sequenceAccession": "LRG_1247p1",
                    "sequenceAccessionVersion": "LRG_1247p1",
                },
                "type": "HGVS_TYPE_CODING",
            },
        ),
    ],
)
def test_convert_hgvs_expression_xmldict_data_to_pb(xml_str: str, expected_json: Any):
    xmldict_value = xmltodict.parse(xml_str)
    result = ConvertHgvsExpression.xmldict_data_to_pb(xmldict_value)
    result_json = MessageToDict(result)
    assert result_json == expected_json


@pytest.mark.parametrize(
    "xml_str,expected_json",
    [
        (
            """
            <Software name="Most Probable Genotype" purpose="variant calls"/>
            """,
            {
                "name": "Most Probable Genotype",
                "purpose": "variant calls",
            },
        ),
        (
            """
            <Software name="SIFT" purpose="to predict variant function" version="Polyphen-2"/>
            """,
            {
                "name": "SIFT",
                "purpose": "to predict variant function",
                "version": "Polyphen-2",
            },
        ),
    ],
)
def test_convert_software(xml_str: str, expected_json: Any):
    xmldict_value = xmltodict.parse(xml_str)
    result = ConvertSoftware.xmldict_data_to_pb(xmldict_value)
    result_json = MessageToDict(result)
    assert result_json == expected_json


@pytest.mark.parametrize(
    "xml_str,expected_json",
    [
        (
            """
            <DescriptionHistory Dated="2018-07-20">
                <Description>Pathogenic</Description>
            </DescriptionHistory>
            """,
            {
                "dated": "2018-07-20T00:00:00Z",
                "description": "Pathogenic",
            },
        ),
        (
            """
            <DescriptionHistory>
                <Description>Pathogenic</Description>
            </DescriptionHistory>
            """,
            {
                "description": "Pathogenic",
            },
        ),
    ],
)
def test_convert_description_history(xml_str: str, expected_json: Any):
    xmldict_value = xmltodict.parse(xml_str)
    result = ConvertDescriptionHistory.xmldict_data_to_pb(xmldict_value)
    result_json = MessageToDict(result)
    assert result_json == expected_json


@pytest.mark.parametrize(
    "xml_str,tag_name,expected_json",
    [
        (
            """
            <Name>
                <ElementValue Type="Alternate">Spastic paraplegia 48</ElementValue>
            </Name>
            """,
            "Name",
            {
                "type": "Alternate",
                "value": "Spastic paraplegia 48",
            },
        ),
        (
            """
            <Symbol>
                <ElementValue Type="Alternate">SPG48</ElementValue>
                <XRef Type="MIM" ID="613647" DB="OMIM"/>
            </Symbol>
            """,
            "Symbol",
            {
                "type": "Alternate",
                "value": "SPG48",
                "xrefs": [
                    {
                        "db": "OMIM",
                        "id": "613647",
                        "type": "MIM",
                    },
                ],
            },
        ),
        (
            """
            <Name>
                <ElementValue Type="Alternate">MITOCHONDRIAL COMPLEX I DEFICIENCY, NUCLEAR TYPE 19</ElementValue>
                <XRef Type="MIM" ID="618241" DB="OMIM"/>
                <XRef Type="Allelic variant" ID="613622.0001" DB="OMIM"/>
                <XRef Type="Allelic variant" ID="613622.0002" DB="OMIM"/>
                <XRef Type="Allelic variant" ID="613622.0003" DB="OMIM"/>
            </Name>
            """,
            "Name",
            {
                "type": "Alternate",
                "value": "MITOCHONDRIAL COMPLEX I DEFICIENCY, NUCLEAR TYPE 19",
                "xrefs": [
                    {
                        "db": "OMIM",
                        "id": "618241",
                        "type": "MIM",
                    },
                    {
                        "db": "OMIM",
                        "id": "613622.0001",
                        "type": "Allelic variant",
                    },
                    {
                        "db": "OMIM",
                        "id": "613622.0002",
                        "type": "Allelic variant",
                    },
                    {
                        "db": "OMIM",
                        "id": "613622.0003",
                        "type": "Allelic variant",
                    },
                ],
            },
        ),
    ],
)
def test_convert_generic_set_element(xml_str: str, tag_name: str, expected_json: Any):
    xmldict_value = xmltodict.parse(xml_str)
    result = ConvertGenericSetElement.xmldict_data_to_pb(xmldict_value, tag_name)
    result_json = MessageToDict(result)
    assert result_json == expected_json


@pytest.mark.parametrize(
    "xml_str,expected_json",
    [
        (
            """
            <AttributeSet>
                <Attribute Type="AssertionMethod">ACMG Guidelines, 2015</Attribute>
                <Citation>
                    <ID Source="PubMed">25741868</ID>
                </Citation>
            </AttributeSet>
            """,
            {
                "attribute": {
                    "base": {
                        "value": "ACMG Guidelines, 2015",
                    },
                    "type": "AssertionMethod",
                },
                "citations": [
                    {
                        "ids": [
                            {
                                "source": "PubMed",
                                "value": "25741868",
                            },
                        ],
                    },
                ],
            },
        ),
        (
            """
            <AttributeSet>
                <Attribute Type="HGVS">NM_014855.3:c.80_83delinsTGCTGTAAACTGTAACTGTAAA</Attribute>
            </AttributeSet>
            """,
            {
                "attribute": {
                    "base": {
                        "value": "NM_014855.3:c.80_83delinsTGCTGTAAACTGTAACTGTAAA",
                    },
                    "type": "HGVS",
                },
            },
        ),
        (
            """
            <AttributeSet>
                <Attribute Type="public definition">In WDR62 primary microcephaly...</Attribute>
                <XRef ID="NBK578067" DB="GeneReviews"/>
            </AttributeSet>
            """,
            {
                "attribute": {
                    "base": {
                        "value": "In WDR62 primary microcephaly...",
                    },
                    "type": "public definition",
                },
                "xrefs": [
                    {
                        "db": "GeneReviews",
                        "id": "NBK578067",
                    },
                ],
            },
        ),
    ],
)
def test_convert_attribute_set_element(xml_str: str, expected_json: Any):
    xmldict_value = xmltodict.parse(xml_str)
    result = ConvertAttributeSetElement.xmldict_data_to_pb(xmldict_value)
    result_json = MessageToDict(result)
    assert result_json == expected_json


@pytest.mark.parametrize(
    "xml_str,expected",
    [
        ("phenotype", Trait.TraitRelationship.Type.TYPE_PHENOTYPE),
        ("Subphenotype", Trait.TraitRelationship.Type.TYPE_SUBPHENOTYPE),
        (
            "DrugResponseAndDisease",
            Trait.TraitRelationship.Type.TYPE_DRUG_RESPONSE_AND_DISEASE,
        ),
        (
            "co-occuring condition",
            Trait.TraitRelationship.Type.TYPE_CO_OCCURING_CONDITION,
        ),
        ("Finding member", Trait.TraitRelationship.Type.TYPE_FINDING_MEMBER),
    ],
)
def test_convert_trait_trait_relationship_type(
    xml_str: str, expected: Trait.TraitRelationship.Type.ValueType
):
    result = ConvertTrait.convert_trait_relationship_type(xml_str)
    result == expected


@pytest.mark.parametrize(
    "xml_str,expected_json",
    [
        (
            """
            <TraitRelationship Type="DrugResponseAndDisease">
                <Name>
                    <ElementValue Type="Preferred">malignant granular cell tumor</ElementValue>
                </Name>
            </TraitRelationship>
            """,
            {
                "names": [{"type": "Preferred", "value": "malignant granular cell tumor"}],
                "type": "TYPE_DRUG_RESPONSE_AND_DISEASE",
            },
        ),
        (
            """
            <TraitRelationship Type="DrugResponseAndDisease">
                <XRef DB="Orphanet" ID="ORPHA139402"/>
            </TraitRelationship>
            """,
            {
                "type": "TYPE_DRUG_RESPONSE_AND_DISEASE",
                "xrefs": [{"db": "Orphanet", "id": "ORPHA139402"}],
            },
        ),
    ],
)
def test_convert_trait_trait_relationship(xml_str: str, expected_json: Any):
    xmldict_value = xmltodict.parse(xml_str)
    result = ConvertTrait.convert_trait_relationship(xmldict_value)
    result_json = MessageToDict(result)
    assert result_json == expected_json


@pytest.mark.parametrize(
    "xml_str",
    [
        """
        <Trait ID="9580" Type="Disease">
            <Name>
                <ElementValue Type="Preferred">Hereditary spastic paraplegia 48</ElementValue>
                <XRef ID="MONDO:0013342" DB="MONDO"/>
            </Name>
            <Name>
                <ElementValue Type="Alternate">Spastic paraplegia 48</ElementValue>
            </Name>
            <Name>
                <ElementValue Type="Alternate">Spastic paraplegia 48, autosomal recessive</ElementValue>
                <XRef ID="Spastic+paraplegia+48%2C+autosomal+recessive/9323" DB="Genetic Alliance"/>
            </Name>
            <Symbol>
                <ElementValue Type="Alternate">SPG48</ElementValue>
                <XRef Type="MIM" ID="613647" DB="OMIM"/>
            </Symbol>
            <XRef ID="306511" DB="Orphanet"/>
            <XRef ID="C3150901" DB="MedGen"/>
        </Trait>
        """,
        """
        <Trait ID="5522" Type="Disease">
            <Name>
                <ElementValue Type="Alternate">MICROCEPHALY 2, PRIMARY, AUTOSOMAL RECESSIVE, WITH CORTICAL MALFORMATIONS</ElementValue>
                <XRef Type="Allelic variant" ID="613583.0005" DB="OMIM"/>
                <XRef Type="Allelic variant" ID="613583.0003" DB="OMIM"/>
            </Name>
            <Name>
                <ElementValue Type="Alternate">Primary autosomal recessive microcephaly 2</ElementValue>
                <XRef ID="Primary+autosomal+recessive+microcephaly+2/9156" DB="Genetic Alliance"/>
            </Name>
            <Name>
                <ElementValue Type="Preferred">Microcephaly 2, primary, autosomal recessive, with or without cortical malformations</ElementValue>
                <XRef ID="MONDO:0011435" DB="MONDO"/>
            </Name>
            <Symbol>
                <ElementValue Type="Alternate">MCPH2</ElementValue>
                <XRef Type="MIM" ID="604317" DB="OMIM"/>
            </Symbol>
            <AttributeSet>
            <Attribute Type="public definition">In WDR62 primary microcephaly...</Attribute>
                <XRef ID="NBK578067" DB="GeneReviews"/>
            </AttributeSet>
            <Citation Type="review" Abbrev="GeneReviews">
                <ID Source="PubMed">35188728</ID>
                <ID Source="BookShelf">NBK578067</ID>
            </Citation>
            <XRef ID="2512" DB="Orphanet"/>
            <XRef ID="C1858535" DB="MedGen"/>
        </Trait>
        """,
    ],
    ids=[
        "trait-9580",
        "trait-5522",
    ],
)
def test_convert_trait_xmldict_data_to_pb(xml_str: str, snapshot):
    xmldict_value = xmltodict.parse(xml_str)
    result = ConvertTrait.xmldict_data_to_pb(xmldict_value)
    result_json = MessageToDict(result)
    snapshot.assert_match(json.dumps(result_json, indent=2), "result")


@pytest.mark.parametrize(
    "xml_str,expected",
    [
        (
            "Indication",
            Indication.Type.TYPE_INDICATION,
        ),
    ],
)
def test_convert_indication_type(xml_str: str, expected: Indication.Type.ValueType):
    result = ConvertIndication.convert_indication_type(xml_str)
    assert result == expected


@pytest.mark.parametrize(
    "xml_str,expected",
    [
        (
            "Disease",
            TraitSet.Type.TYPE_DISEASE,
        ),
        (
            "DrugResponse",
            TraitSet.Type.TYPE_DRUG_RESPONSE,
        ),
        (
            "Finding",
            TraitSet.Type.TYPE_FINDING,
        ),
        (
            "PhenotypeInstruction",
            TraitSet.Type.TYPE_PHENOTYPE_INSTRUCTION,
        ),
        (
            "TraitChoice",
            TraitSet.Type.TYPE_TRAIT_CHOICE,
        ),
    ],
)
def test_convert_trait_set_convert_type(xml_str: str, expected: TraitSet.Type.ValueType):
    result = ConvertTraitSet.convert_type(xml_str)
    assert result == expected


@pytest.mark.parametrize(
    "xml_str",
    [
        """
        <TraitSet ID="2" Type="Disease" ContributesToAggregateClassification="true">
            <Trait ID="9580" Type="Disease">
                <Name>
                    <ElementValue Type="Preferred">Hereditary spastic paraplegia 48</ElementValue>
                    <XRef ID="MONDO:0013342" DB="MONDO"/>
                </Name>
                <Name>
                    <ElementValue Type="Alternate">Spastic paraplegia 48</ElementValue>
                </Name>
                <Name>
                    <ElementValue Type="Alternate">Spastic paraplegia 48, autosomal recessive</ElementValue>
                    <XRef ID="Spastic+paraplegia+48%2C+autosomal+recessive/9323" DB="Genetic Alliance"/>
                </Name>
                <Symbol>
                    <ElementValue Type="Alternate">SPG48</ElementValue>
                    <XRef Type="MIM" ID="613647" DB="OMIM"/>
                </Symbol>
                <XRef ID="306511" DB="Orphanet"/>
                <XRef ID="C3150901" DB="MedGen"/>
                <XRef ID="MONDO:0013342" DB="MONDO"/>
                <XRef Type="MIM" ID="613647" DB="OMIM"/>
            </Trait>
        </TraitSet>
        """,
        """
        <TraitSet ID="6288" Type="Disease" ContributesToAggregateClassification="false" LowerLevelOfEvidence="true">
            <Trait ID="15736" Type="Disease">
                <Name>
                    <ElementValue Type="Alternate">Acute myeloid leukemia, adult</ElementValue>
                </Name>
                <Name>
                    <ElementValue Type="Alternate">AML adult</ElementValue>
                </Name>
                <Name>
                    <ElementValue Type="Alternate">Acute myelogenous leukemia</ElementValue>
                    <XRef ID="Acute+Myeloid+Leukemia%2C+Adult/204" DB="Genetic Alliance" />
                    <XRef ID="HP:0004808" DB="Human Phenotype Ontology" />
                </Name>
                <Name>
                    <ElementValue Type="Alternate">Acute non-lymphocytic leukemia</ElementValue>
                </Name>
                <Name>
                    <ElementValue Type="Alternate">Acute granulocytic leukemia</ElementValue>
                </Name>
                <Name>
                    <ElementValue Type="Alternate">Leukemia, acute myelogenous, somatic</ElementValue>
                </Name>
                <Name>
                    <ElementValue Type="Alternate">Leukemia, acute myeloid, somatic</ElementValue>
                </Name>
                <Name>
                    <ElementValue Type="Preferred">Acute myeloid leukemia</ElementValue>
                    <XRef ID="HP:0004808" DB="Human Phenotype Ontology" />
                    <XRef ID="MONDO:0018874" DB="MONDO" />
                    <XRef ID="519" DB="Orphanet" />
                    <XRef ID="17788007" DB="SNOMED CT" />
                </Name>
                <Symbol>
                    <ElementValue Type="Preferred">AML</ElementValue>
                    <XRef ID="GTR000500636" DB="Genetic Testing Registry (GTR)" />
                    <XRef Type="MIM" ID="601626" DB="OMIM" />
                </Symbol>
                <AttributeSet>
                    <Attribute Type="disease mechanism">Constitutively activated FLT3</Attribute>
                    <XRef ID="GTR000552464" DB="Genetic Testing Registry (GTR)" />
                </AttributeSet>
                <AttributeSet>
                    <Attribute Type="public definition">A clonal expansion of myeloid...</Attribute>
                </AttributeSet>
                <AttributeSet>
                    <Attribute Type="GARD id" integerValue="12757" />
                    <XRef ID="12757" DB="Office of Rare Diseases" />
                </AttributeSet>
                <Citation Type="review" Abbrev="GeneReviews">
                    <ID Source="PubMed">20963938</ID>
                    <ID Source="BookShelf">NBK47457</ID>
                </Citation>
                <Citation Type="Translational/Evidence-based" Abbrev="NCCN, 2011">
                    <ID Source="PubMed">22138009</ID>
                </Citation>
                <Citation Type="general" Abbrev="ESMO, 2013">
                    <ID Source="PubMed">23970018</ID>
                </Citation>
                <Citation Type="review" Abbrev="GeneReviews">
                    <ID Source="PubMed">33226740</ID>
                    <ID Source="BookShelf">NBK564234</ID>
                </Citation>
                <Citation Type="review" Abbrev="GeneReviews">
                    <ID Source="PubMed">33661592</ID>
                    <ID Source="BookShelf">NBK568319</ID>
                </Citation>
                <Citation Type="review" Abbrev="GeneReviews">
                    <ID Source="PubMed">34723452</ID>
                    <ID Source="BookShelf">NBK574843</ID>
                </Citation>
                <Citation Type="general" Abbrev="ESMO, 2020">
                    <ID Source="PubMed">32171751</ID>
                </Citation>
                <Citation Type="practice guideline" Abbrev="NCCN, 2023">
                    <URL>https://www.nccn.org/professionals/physician_gls/pdf/all.pdf</URL>
                    <CitationText>NCCN Clinical Practice Guidelines in Oncology (NCCN Guidelines®) Acute Lymphoblastic Leukemia, 2023</CitationText>
                </Citation>
                <Citation Type="practice guideline" Abbrev="NCCN, 2023">
                    <URL>https://www.nccn.org/professionals/physician_gls/pdf/aml.pdf</URL>
                    <CitationText>NCCN Clinical Practice Guidelines in Oncology (NCCN Guidelines®) Acute Myeloid Leukemia, 2023</CitationText>
                </Citation>
                <XRef ID="519" DB="Orphanet" />
                <XRef ID="C0023467" DB="MedGen" />
                <XRef ID="D015470" DB="MeSH" />
                <XRef ID="MONDO:0018874" DB="MONDO" />
                <XRef Type="MIM" ID="601626" DB="OMIM" />
                <XRef Type="primary" ID="HP:0004808" DB="Human Phenotype Ontology" />
                <XRef Type="secondary" ID="HP:0001914" DB="Human Phenotype Ontology" />
                <XRef Type="secondary" ID="HP:0004843" DB="Human Phenotype Ontology" />
                <XRef Type="secondary" ID="HP:0005516" DB="Human Phenotype Ontology" />
                <XRef Type="secondary" ID="HP:0006724" DB="Human Phenotype Ontology" />
                <XRef Type="secondary" ID="HP:0006728" DB="Human Phenotype Ontology" />
            </Trait>
        </TraitSet>
        """,
    ],
    ids=["trait-set-2", "trait-set-6288"],
)
def test_convert_trait_set_xmldict_data_to_pb(xml_str: str, snapshot):
    xmldict_value = xmltodict.parse(xml_str)
    result = ConvertTraitSet.xmldict_data_to_pb(xmldict_value)
    result_json = MessageToDict(result)
    snapshot.assert_match(json.dumps(result_json, indent=2), "result")


@pytest.mark.parametrize(
    "xml_str",
    [
        """
        <GermlineClassification DateLastEvaluated="2010-10-01" NumberOfSubmissions="1" NumberOfSubmitters="1" DateCreated="2016-10-23" MostRecentSubmission="2016-10-23">
            <ReviewStatus>no assertion criteria provided</ReviewStatus>
            <Description>Pathogenic</Description>
            <Citation Type="general">
                <ID Source="PubMed">20835237</ID>
            </Citation>
            <ConditionList>
                <TraitSet ID="29" Type="Disease" ContributesToAggregateClassification="true">
                    <Trait ID="9600" Type="Disease">
                        <Name>
                            <ElementValue Type="Preferred">Senior-Loken syndrome 7</ElementValue>
                            <XRef ID="Senior-Loken+syndrome+7/9283" DB="Genetic Alliance" />
                            <XRef ID="MONDO:0013326" DB="MONDO" />
                        </Name>
                        <Symbol>
                            <ElementValue Type="Preferred">SLSN7</ElementValue>
                            <XRef Type="MIM" ID="613615" DB="OMIM" />
                        </Symbol>
                        <XRef ID="3156" DB="Orphanet" />
                        <XRef ID="C3150877" DB="MedGen" />
                        <XRef ID="MONDO:0013326" DB="MONDO" />
                        <XRef Type="MIM" ID="613615" DB="OMIM" />
                    </Trait>
                </TraitSet>
            </ConditionList>
        </GermlineClassification>
        """,
        """
        <GermlineClassification NumberOfSubmissions="2" NumberOfSubmitters="2" DateCreated="2017-01-30" MostRecentSubmission="2021-05-16">
            <ReviewStatus>criteria provided, single submitter</ReviewStatus>
            <Description>Pathogenic</Description>
            <Citation Type="general">
                <ID Source="PubMed">20613862</ID>
            </Citation>
            <ConditionList>
                <TraitSet ID="2" Type="Disease" ContributesToAggregateClassification="true">
                    <Trait ID="9580" Type="Disease">
                        <Name>
                            <ElementValue Type="Preferred">Hereditary spastic paraplegia 48</ElementValue>
                            <XRef ID="MONDO:0013342" DB="MONDO" />
                        </Name>
                        <Name>
                            <ElementValue Type="Alternate">Spastic paraplegia 48</ElementValue>
                        </Name>
                        <Name>
                            <ElementValue Type="Alternate">Spastic paraplegia 48, autosomal recessive</ElementValue>
                            <XRef ID="Spastic+paraplegia+48%2C+autosomal+recessive/9323" DB="Genetic Alliance" />
                        </Name>
                        <Symbol>
                            <ElementValue Type="Alternate">SPG48</ElementValue>
                            <XRef Type="MIM" ID="613647" DB="OMIM" />
                        </Symbol>
                        <XRef ID="306511" DB="Orphanet" />
                        <XRef ID="C3150901" DB="MedGen" />
                        <XRef ID="MONDO:0013342" DB="MONDO" />
                        <XRef Type="MIM" ID="613647" DB="OMIM" />
                    </Trait>
                </TraitSet>
            </ConditionList>
        </GermlineClassification>
        """,
        """
        <GermlineClassification DateLastEvaluated="2021-02-01" NumberOfSubmissions="2" NumberOfSubmitters="2" DateCreated="2018-06-02" MostRecentSubmission="2021-10-30">
            <ReviewStatus>criteria provided, single submitter</ReviewStatus>
            <Description>Uncertain significance</Description>
            <Citation Type="general">
                <CitationText>Tomatsu, S., Fukuda, S., ...</CitationText>
            </Citation>
            <Citation Type="general">
                <ID Source="PubMed">34387910</ID>
            </Citation>
            <Citation Type="general">
                <ID Source="PubMed">7795586</ID>
            </Citation>
            <DescriptionHistory Dated="2021-08-24">
                <Description>Pathogenic</Description>
            </DescriptionHistory>
            <ConditionList>
                <TraitSet ID="175" Type="Disease" ContributesToAggregateClassification="true">
                    <Trait ID="3036" Type="Disease">
                        <Name>
                            <ElementValue Type="Alternate">Mucopolysaccharidosis Type IVA</ElementValue>
                            <XRef ID="NBK148668" DB="GeneReviews" />
                        </Name>
                        <Name>
                            <ElementValue Type="Alternate">Morquio syndrome A</ElementValue>
                        </Name>
                        <Name>
                            <ElementValue Type="Alternate">MPS 4A</ElementValue>
                        </Name>
                        <Name>
                            <ElementValue Type="Alternate">Morquio A disease</ElementValue>
                        </Name>
                        <Name>
                            <ElementValue Type="Alternate">Galactosamine-6-sulfatase deficiency</ElementValue>
                        </Name>
                        <Name>
                            <ElementValue Type="Alternate">Mucopolysaccharidosis type IV A</ElementValue>
                        </Name>
                        <Name>
                            <ElementValue Type="Alternate">MPS IVA</ElementValue>
                            <XRef Type="MIM" ID="253000" DB="OMIM" />
                        </Name>
                        <Name>
                            <ElementValue Type="Alternate">Morquio syndrome A, mild</ElementValue>
                        </Name>
                        <Name>
                            <ElementValue Type="Preferred">Mucopolysaccharidosis, MPS-IV-A</ElementValue>
                            <XRef ID="Morquio+syndrome+A/4876" DB="Genetic Alliance" />
                            <XRef ID="7259005" DB="SNOMED CT" />
                        </Name>
                        <Symbol>
                            <ElementValue Type="Preferred">MPS4A</ElementValue>
                            <XRef Type="MIM" ID="253000" DB="OMIM" />
                        </Symbol>
                        <AttributeSet>
                            <Attribute Type="public definition">The phenotypic spectrum of ...</Attribute>
                            <XRef ID="NBK148668" DB="GeneReviews" />
                        </AttributeSet>
                        <AttributeSet>
                            <Attribute Type="GARD id" integerValue="3785" />
                            <XRef ID="3785" DB="Office of Rare Diseases" />
                        </AttributeSet>
                        <Citation Type="review" Abbrev="GeneReviews">
                            <ID Source="PubMed">23844448</ID>
                            <ID Source="BookShelf">NBK148668</ID>
                        </Citation>
                        <XRef ID="309297" DB="Orphanet" />
                        <XRef ID="582" DB="Orphanet" />
                        <XRef ID="C0086651" DB="MedGen" />
                        <XRef ID="MONDO:0009659" DB="MONDO" />
                        <XRef Type="MIM" ID="253000" DB="OMIM" />
                    </Trait>
                </TraitSet>
            </ConditionList>
        </GermlineClassification>
        """,
    ],
    ids=["trait-set-29", "trait-set-6288", "trait-set-175"],
)
def test_convert_aggregated_germline_classification_xmldict_data_to_pb(xml_str: str, snapshot):
    xmldict_value = xmltodict.parse(xml_str)
    result = ConvertAggregatedGermlineClassification.xmldict_data_to_pb(xmldict_value)
    result_json = MessageToDict(result)
    snapshot.assert_match(json.dumps(result_json, indent=2), "result")


@pytest.mark.parametrize(
    "xml_str",
    [
        """
        <SomaticClinicalImpact DateLastEvaluated="2018-10-16" NumberOfSubmissions="1" NumberOfSubmitters="1" DateCreated="2024-02-20" MostRecentSubmission="2024-02-20">
            <ReviewStatus>criteria provided, single submitter</ReviewStatus>
            <Description>Tier II - Potential</Description>
            <Citation Type="general">
                <ID Source="PubMed">24705250</ID>
            </Citation>
            <Citation Type="general">
                <ID Source="PubMed">24705254</ID>
            </Citation>
            <Citation Type="general">
                <URL>https://civicdb.org/links/evidence/4846</URL>
            </Citation>
            <Citation Type="general">
                <URL>https://civicdb.org/links/evidence/6955</URL>
            </Citation>
            <Citation Type="general">
                <URL>https://identifiers.org/civic.mpid:1594</URL>
            </Citation>
            <ConditionList>
                <TraitSet ID="93559" Type="Disease" ContributesToAggregateClassification="true">
                    <Trait ID="73010" Type="Disease">
                        <Name>
                            <ElementValue Type="Preferred">Diffuse midline glioma, H3 K27M-mutant</ElementValue>
                            <XRef ID="MONDO:0957196" DB="MONDO" />
                        </Name>
                        <XRef ID="CN377633" DB="MedGen" />
                        <XRef ID="MONDO:0957196" DB="MONDO" />
                    </Trait>
                </TraitSet>
            </ConditionList>
        </SomaticClinicalImpact>
        """,
        """
        <SomaticClinicalImpact DateLastEvaluated="2018-02-23" NumberOfSubmissions="2" NumberOfSubmitters="1" DateCreated="2024-02-20" MostRecentSubmission="2024-02-20">
            <ReviewStatus>criteria provided, single submitter</ReviewStatus>
            <Description>Tier I - Strong</Description>
            <Citation Type="general" Abbrev="FDA, 2014">
                <ID Source="PubMed">24868098</ID>
            </Citation>
            <Citation Type="general">
                <ID Source="PubMed">17877814</ID>
            </Citation>
            <Citation Type="general">
                <ID Source="PubMed">18408761</ID>
            </Citation>
            <Citation Type="general">
                <ID Source="PubMed">19147750</ID>
            </Citation>
            <Citation Type="general">
                <URL>https://civicdb.org/links/evidence/229</URL>
            </Citation>
            <Citation Type="general">
                <URL>https://civicdb.org/links/evidence/2629</URL>
            </Citation>
            <Citation Type="general">
                <URL>https://civicdb.org/links/evidence/2994</URL>
            </Citation>
            <ConditionList>
                <TraitSet ID="4069" Type="Disease" ContributesToAggregateClassification="true">
                    <Trait ID="7728" Type="Disease">
                        <Name>
                            <ElementValue Type="Alternate">Non-small cell lung cancer</ElementValue>
                            <XRef ID="Non-small+cell+lung+cancer/5250" DB="Genetic Alliance" />
                            <XRef ID="HP:0030358" DB="Human Phenotype Ontology" />
                            <XRef ID="254637007" DB="SNOMED CT" />
                        </Name>
                        <Name>
                            <ElementValue Type="Preferred">Non-small cell lung carcinoma</ElementValue>
                            <XRef ID="HP:0030358" DB="Human Phenotype Ontology" />
                            <XRef ID="MONDO:0005233" DB="MONDO" />
                        </Name>
                        <Symbol>
                            <ElementValue Type="Preferred">NSCLC</ElementValue>
                        </Symbol>
                        <AttributeSet>
                            <Attribute Type="disease mechanism" integerValue="283">Other</Attribute>
                            <XRef ID="GTR000592350" DB="Genetic Testing Registry (GTR)" />
                            <XRef ID="GTR000596970" DB="Genetic Testing Registry (GTR)" />

                        </AttributeSet>
                        <Citation Type="practice guideline" Abbrev="AHRQ, 2013">
                            <URL>https://www.cms.gov/Medicare/Coverage/DeterminationProcess/downloads/id90TA.pdf</URL>
                            <CitationText>Technology Assessment on Genetic Testing or Molecular Pathology Testing of Cancers with Unknown Primary Site to Determine Origin (ARCHIVED)</CitationText>
                        </Citation>
                        <Citation Type="general" Abbrev="FDA, 2014">
                            <ID Source="PubMed">24868098</ID>
                        </Citation>
                        <Citation Type="practice guideline" Abbrev="NICE, 2023">
                            <URL>https://www.nice.org.uk/guidance/ng122</URL>
                            <CitationText>UK NICE guideline NG122, Lung cancer: diagnosis and management, 2023</CitationText>
                        </Citation>
                        <XRef ID="C0007131" DB="MedGen" />
                        <XRef ID="D002289" DB="MeSH" />
                        <XRef ID="MONDO:0005233" DB="MONDO" />
                        <XRef Type="primary" ID="HP:0030358" DB="Human Phenotype Ontology" />
                    </Trait>
                </TraitSet>
            </ConditionList>
        </SomaticClinicalImpact>
        """,
    ],
    ids=["trait-set-93559", "trait-set-4069"],
)
def test_convert_aggregated_somatic_clinical_impact_xmldict_data_to_pb(xml_str: str, snapshot):
    xmldict_value = xmltodict.parse(xml_str)
    result = ConvertAggregatedSomaticClinicalImpact.xmldict_data_to_pb(xmldict_value)
    result_json = MessageToDict(result)
    snapshot.assert_match(json.dumps(result_json, indent=2), "result")


@pytest.mark.parametrize(
    "xml_str",
    [
        """
        <OncogenicityClassification DateLastEvaluated="2024-01-24" NumberOfSubmissions="1" NumberOfSubmitters="1" DateCreated="2024-03-05" MostRecentSubmission="2024-03-05">
            <ReviewStatus>no assertion criteria provided</ReviewStatus>
            <Description>Oncogenic</Description>
            <Citation Type="general">
                <ID Source="PubMed">17698969</ID>
            </Citation>
            <Citation Type="general">
                <ID Source="PubMed">23435422</ID>
            </Citation>
            <Citation Type="general">
                <ID Source="PubMed">24030976</ID>
            </Citation>
            <Citation Type="general">
                <ID Source="PubMed">30655867</ID>
            </Citation>
            <Citation Type="general">
                <ID Source="PubMed">32895364</ID>
            </Citation>
            <ConditionList>
                <TraitSet ID="6288" Type="Disease" ContributesToAggregateClassification="true">
                    <Trait ID="15736" Type="Disease">
                        <Name>
                            <ElementValue Type="Alternate">Acute myeloid leukemia, adult</ElementValue>
                        </Name>
                        <Name>
                            <ElementValue Type="Alternate">AML adult</ElementValue>
                        </Name>
                        <Name>
                            <ElementValue Type="Alternate">Acute myelogenous leukemia</ElementValue>
                            <XRef ID="Acute+Myeloid+Leukemia%2C+Adult/204" DB="Genetic Alliance" />
                            <XRef ID="HP:0004808" DB="Human Phenotype Ontology" />
                        </Name>
                        <Name>
                            <ElementValue Type="Alternate">Acute non-lymphocytic leukemia</ElementValue>
                        </Name>
                        <Name>
                            <ElementValue Type="Alternate">Acute granulocytic leukemia</ElementValue>
                        </Name>
                        <Name>
                            <ElementValue Type="Alternate">Leukemia, acute myeloid, somatic</ElementValue>
                        </Name>
                        <Name>
                            <ElementValue Type="Alternate">Leukemia, acute myelogenous, somatic</ElementValue>
                        </Name>
                        <Name>
                            <ElementValue Type="Preferred">Acute myeloid leukemia</ElementValue>
                            <XRef ID="HP:0004808" DB="Human Phenotype Ontology" />
                            <XRef ID="MONDO:0018874" DB="MONDO" />
                            <XRef ID="519" DB="Orphanet" />
                            <XRef ID="17788007" DB="SNOMED CT" />
                        </Name>
                        <Symbol>
                            <ElementValue Type="Preferred">AML</ElementValue>
                            <XRef ID="GTR000500636" DB="Genetic Testing Registry (GTR)" />
                            <XRef Type="MIM" ID="601626" DB="OMIM" />
                        </Symbol>
                        <AttributeSet>
                            <Attribute Type="disease mechanism">Constitutively activated FLT3</Attribute>
                            <XRef ID="GTR000552464" DB="Genetic Testing Registry (GTR)" />
                        </AttributeSet>
                        <AttributeSet>
                            <Attribute Type="GARD id" integerValue="12757" />
                            <XRef ID="12757" DB="Office of Rare Diseases" />
                        </AttributeSet>
                        <AttributeSet>
                            <Attribute Type="public definition">A clonal expansion of myeloid blasts in the bone marrow,</Attribute>
                        </AttributeSet>
                        <Citation Type="review" Abbrev="GeneReviews">
                            <ID Source="PubMed">20963938</ID>
                            <ID Source="BookShelf">NBK47457</ID>
                        </Citation>
                        <Citation Type="Translational/Evidence-based" Abbrev="NCCN, 2011">
                            <ID Source="PubMed">22138009</ID>
                        </Citation>
                        <Citation Type="general" Abbrev="ESMO, 2013">
                            <ID Source="PubMed">23970018</ID>
                        </Citation>
                        <Citation Type="review" Abbrev="GeneReviews">
                            <ID Source="PubMed">33226740</ID>
                            <ID Source="BookShelf">NBK564234</ID>
                        </Citation>
                        <Citation Type="review" Abbrev="GeneReviews">
                            <ID Source="PubMed">33661592</ID>
                            <ID Source="BookShelf">NBK568319</ID>
                        </Citation>
                        <Citation Type="review" Abbrev="GeneReviews">
                            <ID Source="PubMed">34723452</ID>
                            <ID Source="BookShelf">NBK574843</ID>
                        </Citation>
                        <Citation Type="general" Abbrev="ESMO, 2020">
                            <ID Source="PubMed">32171751</ID>
                        </Citation>
                        <Citation Type="practice guideline" Abbrev="NCCN, 2023">
                            <URL>https://www.nccn.org/professionals/physician_gls/pdf/all.pdf</URL>
                            <CitationText>NCCN Clinical Practice Guidelines in Oncology (NCCN Guidelines®) Acute Lymphoblastic Leukemia, 2023</CitationText>
                        </Citation>
                        <Citation Type="practice guideline" Abbrev="NCCN, 2023">
                            <URL>https://www.nccn.org/professionals/physician_gls/pdf/aml.pdf</URL>
                            <CitationText>NCCN Clinical Practice Guidelines in Oncology (NCCN Guidelines®) Acute Myeloid Leukemia, 2023</CitationText>
                        </Citation>
                        <XRef ID="519" DB="Orphanet" />
                        <XRef ID="C0023467" DB="MedGen" />
                        <XRef ID="D015470" DB="MeSH" />
                        <XRef ID="MONDO:0018874" DB="MONDO" />
                        <XRef Type="MIM" ID="601626" DB="OMIM" />
                        <XRef Type="primary" ID="HP:0004808" DB="Human Phenotype Ontology" />
                        <XRef Type="secondary" ID="HP:0001914" DB="Human Phenotype Ontology" />
                        <XRef Type="secondary" ID="HP:0004843" DB="Human Phenotype Ontology" />
                        <XRef Type="secondary" ID="HP:0005516" DB="Human Phenotype Ontology" />
                        <XRef Type="secondary" ID="HP:0006724" DB="Human Phenotype Ontology" />
                        <XRef Type="secondary" ID="HP:0006728" DB="Human Phenotype Ontology" />
                    </Trait>
                </TraitSet>
            </ConditionList>
        </OncogenicityClassification>
        """,
    ],
    ids=["trait-set-6288"],
)
def test_convert_aggregated_oncogenicity_classification_xmldict_data_to_pb(xml_str: str, snapshot):
    xmldict_value = xmltodict.parse(xml_str)
    result = ConvertAggregatedOncogenicityClassification.xmldict_data_to_pb(xmldict_value)
    result_json = MessageToDict(result)
    snapshot.assert_match(json.dumps(result_json, indent=2), "result")


@pytest.mark.parametrize(
    "xml_str",
    [
        """
        <Classifications>
            <GermlineClassification DateLastEvaluated="2010-10-01" NumberOfSubmissions="1" NumberOfSubmitters="1" DateCreated="2019-02-04" MostRecentSubmission="2019-02-04">
                <ReviewStatus>no assertion criteria provided</ReviewStatus>
                <Description>Pathogenic</Description>
            </GermlineClassification>
        </Classifications>
        """,
        """
        <Classifications>
            <SomaticClinicalImpact DateLastEvaluated="2024-01-24" NumberOfSubmissions="1" NumberOfSubmitters="1" DateCreated="2024-03-05" MostRecentSubmission="2024-03-05">
                <ReviewStatus>no assertion criteria provided</ReviewStatus>
                <Description>Tier I - Strong</Description>
            </SomaticClinicalImpact>
        </Classifications>
        """,
        """
        <Classifications>
            <OncogenicityClassification DateLastEvaluated="2024-01-24" NumberOfSubmissions="1" NumberOfSubmitters="1" DateCreated="2024-03-05" MostRecentSubmission="2024-03-05">
                <ReviewStatus>no assertion criteria provided</ReviewStatus>
                <Description>Uncertain significance</Description>
            </OncogenicityClassification>
        </Classifications>
        """,
        """
        <!-- rs1555760738 -->
        <Classifications>
            <GermlineClassification DateLastEvaluated="2022-02-10" NumberOfSubmissions="3" NumberOfSubmitters="2" DateCreated="2014-05-05" MostRecentSubmission="2022-12-31">
                <ReviewStatus>criteria provided, single submitter</ReviewStatus>
                <Description>Pathogenic</Description>
            </GermlineClassification>
            <SomaticClinicalImpact DateLastEvaluated="2024-01-24" NumberOfSubmissions="3" NumberOfSubmitters="1" DateCreated="2024-03-05" MostRecentSubmission="2024-03-05">
                <ReviewStatus>no assertion criteria provided</ReviewStatus>
                <Description>Tier I - Strong</Description>
            </SomaticClinicalImpact>
            <OncogenicityClassification DateLastEvaluated="2024-01-24" NumberOfSubmissions="1" NumberOfSubmitters="1" DateCreated="2024-03-05" MostRecentSubmission="2024-03-05">
                <ReviewStatus>no assertion criteria provided</ReviewStatus>
                <Description>Uncertain significance</Description>
            </OncogenicityClassification>
        </Classifications>
        """,
    ],
    ids=["germline", "somatic", "onco", "all"],
)
def test_convert_aggregate_classification_set_xmldict_data_to_pb(xml_str: str, snapshot):
    xmldict_value = xmltodict.parse(xml_str)
    result = ConvertAggregateClassificationSet.xmldict_data_to_pb(xmldict_value)
    result_json = MessageToDict(result)
    snapshot.assert_match(json.dumps(result_json, indent=2), "result")


@pytest.mark.parametrize(
    "xml_str,expected_json",
    [
        (
            """
            <ClinicalSignificance>
                <ReviewStatus>no assertion criteria provided</ReviewStatus>
                <Description>Uncertain significance</Description>
            </ClinicalSignificance>
            """,
            {
                "description": "Uncertain significance",
                "reviewStatus": "SUBMITTER_REVIEW_STATUS_NO_ASSERTION_CRITERIA_PROVIDED",
            },
        ),
    ],
)
def test_convert_clinical_significance_xmldict_data_to_pb(xml_str: str, expected_json: Any):
    xmldict_value = xmltodict.parse(xml_str)
    result = ConvertClinicalSignificance.xmldict_data_to_pb(xmldict_value)
    result_json = MessageToDict(result)
    assert result_json == expected_json


@pytest.mark.parametrize(
    "xml_str,expected_json",
    [
        (
            """
            <AlleleDescSet>
                <Name>AVPR2:c.26-6T&gt;G</Name>
                <Zygosity>Homozygote</Zygosity>
            </AlleleDescSet>
            """,
            {
                "name": "AVPR2:c.26-6T>G",
                "zygosity": "ZYGOSITY_HOMOZYGOTE",
            },
        ),
        (
            """
            <AlleleDescSet>
                <Name>BRCA2:IVS18+1G&gt;A</Name>
                <Zygosity>SingleHeterozygote</Zygosity>
                <ClinicalSignificance>
                    <ReviewStatus>no assertion criteria provided</ReviewStatus>
                    <Description>Pathogenic</Description>
                </ClinicalSignificance>
            </AlleleDescSet>
            """,
            {
                "clinicalSignificance": {
                    "description": "Pathogenic",
                    "reviewStatus": "SUBMITTER_REVIEW_STATUS_NO_ASSERTION_CRITERIA_PROVIDED",
                },
                "name": "BRCA2:IVS18+1G>A",
                "zygosity": "ZYGOSITY_SINGLE_HETEROZYGOTE",
            },
        ),
    ],
)
def test_convert_allele_description_xmldict_data_to_pb(xml_str: str, expected_json: Any):
    xmldict_value = xmltodict.parse(xml_str)
    result = ConvertAlleleDescription.xmldict_data_to_pb(xmldict_value)
    result_json = MessageToDict(result)
    assert result_json == expected_json


@pytest.mark.parametrize(
    "xml_str,expected_json",
    [
        (
            """
            <Replaced Accession="SCV000057029" DateChanged="2014-08-31" Version="1" VariationID="42" />
            """,
            {
                "accession": "SCV000057029",
                "dateChanged": "2014-08-31T00:00:00Z",
                "version": 1,
                "variationId": "42",
            },
        ),
    ],
)
def test_convert_record_history_xmldict_data_to_pb(xml_str: str, expected_json: Any):
    xmldict_value = xmltodict.parse(xml_str)
    result = ConvertRecordHistory.xmldict_data_to_pb(xmldict_value)
    result_json = MessageToDict(result)
    assert result_json == expected_json


@pytest.mark.parametrize(
    "xml_str,expected_json",
    [
        (
            """
            <SomaticClinicalImpact ClinicalImpactAssertionType="prognostic" ClinicalImpactClinicalSignificance="poor outcome">Tier II - Potential</SomaticClinicalImpact>
            """,
            {
                "clinicalImpactAssertionType": "prognostic",
                "clinicalImpactClinicalSignificance": "poor outcome",
                "value": "Tier II - Potential",
            },
        ),
    ],
)
def test_convert_classification_scv_convert_somatic_clinical_impact(
    xml_str: str, expected_json: Any
):
    xmldict_value = xmltodict.parse(xml_str)
    result = ConvertClassificationScv.convert_somatic_clinical_impact(xmldict_value)
    result_json = MessageToDict(result)
    assert result_json == expected_json


@pytest.mark.parametrize(
    "xml_str,expected_json",
    [
        (
            """
            <ClassificationScore type="ACMG/ClinGen CNV Guidelines, 2019">0.9</ClassificationScore>
            """,
            {
                "type": "ACMG/ClinGen CNV Guidelines, 2019",
                "value": 0.9,
            },
        ),
        (
            """
            <ClassificationScore type="ACMG Guidelines, 2015">7</ClassificationScore>
            """,
            {
                "type": "ACMG Guidelines, 2015",
                "value": 7.0,
            },
        ),
    ],
)
def test_convert_classification_scv_convert_classification_score(xml_str: str, expected_json: Any):
    xmldict_value = xmltodict.parse(xml_str)
    result = ConvertClassificationScv.convert_classification_score(xmldict_value)
    result_json = MessageToDict(result)
    assert result_json == expected_json


@pytest.mark.parametrize(
    "xml_str,expected_json",
    [
        (
            """
            <Classification DateLastEvaluated="2010-10-01">
                <ReviewStatus>no assertion criteria provided</ReviewStatus>
                <GermlineClassification>Pathogenic</GermlineClassification>
            </Classification>
            """,
            {
                "dateLastEvaluated": "2010-10-01T00:00:00Z",
                "germlineClassification": "Pathogenic",
                "reviewStatus": "SUBMITTER_REVIEW_STATUS_NO_ASSERTION_CRITERIA_PROVIDED",
            },
        ),
        (
            """
           <Classification DateLastEvaluated="2024-01-24">
               <ReviewStatus>no assertion criteria provided</ReviewStatus>
               <SomaticClinicalImpact ClinicalImpactAssertionType="diagnostic" ClinicalImpactClinicalSignificance="supports diagnosis">Tier I - Strong</SomaticClinicalImpact>
               <Citation>
                   <ID Source="PubMed">32730663</ID>
                </Citation>
                <Citation>
                    <ID Source="PubMed">28933735</ID>
                </Citation>
                <Comment>This variant was detected in a...</Comment>
            </Classification>
            """,
            {
                "citations": [
                    {
                        "ids": [
                            {
                                "source": "PubMed",
                                "value": "32730663",
                            },
                        ],
                    },
                    {
                        "ids": [
                            {
                                "source": "PubMed",
                                "value": "28933735",
                            },
                        ],
                    },
                ],
                "comments": [
                    {
                        "value": "This variant was detected in a...",
                    },
                ],
                "dateLastEvaluated": "2024-01-24T00:00:00Z",
                "reviewStatus": "SUBMITTER_REVIEW_STATUS_NO_ASSERTION_CRITERIA_PROVIDED",
                "somaticClinicalImpacts": {
                    "clinicalImpactAssertionType": "diagnostic",
                    "clinicalImpactClinicalSignificance": "supports diagnosis",
                    "value": "Tier I - Strong",
                },
            },
        ),
    ],
)
def test_convert_classification_scv_xmldict_data_to_pb(xml_str: str, expected_json: Any):
    xmldict_value = xmltodict.parse(xml_str)
    result = ConvertClassificationScv.xmldict_data_to_pb(xmldict_value)
    result_json = MessageToDict(result)
    assert result_json == expected_json


@pytest.mark.parametrize(
    "xml_str,expected_json",
    [
        (
            """
            <ClinVarAccession Accession="SCV000020155" DateUpdated="2017-01-30" DateCreated="2013-04-04" Type="SCV" Version="3" SubmitterName="OMIM" OrgID="3" OrganizationCategory="resource"/>
            """,
            {
                "orgCategory": "resource",
                "orgId": "3",
                "submitterName": "OMIM",
            },
        ),
        (
            """
            <ClinVarAccession Accession="SCV001451119" DateUpdated="2021-05-16" DateCreated="2021-05-16" Type="SCV" Version="1" SubmitterName="Paris Brain Institute, Inserm - ICM" OrgID="507826" OrganizationCategory="laboratory"/>
            """,
            {
                "orgCategory": "laboratory",
                "orgId": "507826",
                "submitterName": "Paris Brain Institute, Inserm - ICM",
            },
        ),
    ],
)
def test_convert_submitter_identifiers_xml_data_to_pb(xml_str: str, expected_json: Any):
    xmldict_value = xmltodict.parse(xml_str)
    result = ConvertSubmitterIdentifiers.xmldict_data_to_pb(xmldict_value, "ClinVarAccession")
    result_json = MessageToDict(result)
    assert result_json == expected_json


@pytest.mark.parametrize(
    "xml_str,expected_json",
    [
        (
            """
            <Species>Homo sapiens</Species>
            """,
            {
                "name": "Homo sapiens",
            },
        ),
        (
            """
            <Species TaxonomyId="9606">human</Species>
            """,
            {"name": "human", "taxonomyId": 9606},
        ),
    ],
)
def test_convert_species_xml_data_to_pb(xml_str: str, expected_json: Any):
    xmldict_value = xmltodict.parse(xml_str)
    result = ConvertSpecies.xmldict_data_to_pb(xmldict_value)
    result_json = MessageToDict(result)
    assert result_json == expected_json


@pytest.mark.parametrize(
    "xml_str,expected_json",
    [
        (
            """
            <ClassifiedCondition>See cases</ClassifiedCondition>
            """,
            {
                "value": "See cases",
            },
        ),
        (
            """
            <ClassifiedCondition DB="MedGen" ID="C2749757">Bronchiectasis with or without elevated sweat chloride 1</ClassifiedCondition>
            """,
            {
                "db": "MedGen",
                "id": "C2749757",
                "value": "Bronchiectasis with or without elevated sweat chloride 1",
            },
        ),
    ],
)
def test_convert_classified_condition_xml_data_to_pb(xml_str: str, expected_json: Any):
    xmldict_value = xmltodict.parse(xml_str)
    result = ConvertClassifiedCondition.xmldict_data_to_pb(xmldict_value)
    result_json = MessageToDict(result)
    assert result_json == expected_json


@pytest.mark.parametrize(
    "xml_str,expected_json",
    [
        (
            """
            <Replaced Accession="SCV000057029" DateChanged="2014-08-31" Version="1"/>
            """,
            {
                "accession": "SCV000057029",
                "dateChanged": "2014-08-31T00:00:00Z",
                "version": 1,
            },
        ),
    ],
)
def test_convert_clinical_assertion_record_history_xmldict_data_to_pb(
    xml_str: str, expected_json: Any
):
    xmldict_value = xmltodict.parse(xml_str)
    result = ConvertClinicalAssertionRecordHistory.xmldict_data_to_pb(xmldict_value)
    result_json = MessageToDict(result)
    assert result_json == expected_json


@pytest.mark.parametrize(
    "xml_str,expected_json",
    [
        (
            """
            <FunctionalConsequence Value="exon loss">
                <XRef ID="0381" DB="Variation Ontology"/>
            </FunctionalConsequence>
            """,
            {
                "value": "exon loss",
                "xrefs": [
                    {
                        "db": "Variation Ontology",
                        "id": "0381",
                    },
                ],
            },
        ),
        (
            """
            <FunctionalConsequence Value="unknown functional consequence"/>
            """,
            {
                "value": "unknown functional consequence",
            },
        ),
        (
            """
            <FunctionalConsequence Value="effect on RNA splicing">
                <XRef ID="0362" DB="Variation Ontology"/>
                <Comment DataSource="NCBI curation" Type="public">Loss of exon 8 in gene PDHX caused by unknown genomic change.</Comment>
            </FunctionalConsequence>
            """,
            {
                "comments": [
                    {
                        "dataSource": "NCBI curation",
                        "type": "COMMENT_TYPE_PUBLIC",
                        "value": "Loss of exon 8 in gene PDHX caused by unknown genomic change.",
                    },
                ],
                "value": "effect on RNA splicing",
                "xrefs": [
                    {
                        "db": "Variation Ontology",
                        "id": "0362",
                    },
                ],
            },
        ),
    ],
)
def test_convert_functional_consequence_xmldict_data_to_pb(xml_str: str, expected_json: Any):
    xmldict_value = xmltodict.parse(xml_str)
    result = ConvertFunctionalConsequence.xmldict_data_to_pb(xmldict_value)
    result_json = MessageToDict(result)
    assert result_json == expected_json


@pytest.mark.parametrize(
    "xml_str,tag_name,expected_json",
    [
        (
            """
            <Haploinsufficiency last_evaluated="2020-06-24" ClinGen="https://www.ncbi.nlm.nih.gov/projects/dbvar/ISCA/isca_gene.cgi?sym=SHH">Sufficient evidence for dosage pathogenicity</Haploinsufficiency>
            """,
            "Haploinsufficiency",
            {
                "clingen": "https://www.ncbi.nlm.nih.gov/projects/dbvar/ISCA/isca_gene.cgi?sym=SHH",
                "lastEvaluated": "2020-06-24T00:00:00Z",
                "value": "Sufficient evidence for dosage pathogenicity",
            },
        ),
        (
            """
            <Triplosensitivity last_evaluated="2020-06-24" ClinGen="https://www.ncbi.nlm.nih.gov/projects/dbvar/ISCA/isca_gene.cgi?sym=SHH">No evidence available</Triplosensitivity>
            """,
            "Triplosensitivity",
            {
                "clingen": "https://www.ncbi.nlm.nih.gov/projects/dbvar/ISCA/isca_gene.cgi?sym=SHH",
                "lastEvaluated": "2020-06-24T00:00:00Z",
                "value": "No evidence available",
            },
        ),
    ],
)
def test_convert_general_citation_xmldict_data_to_pb(
    xml_str: str, tag_name: str, expected_json: Any
):
    xmldict_value = xmltodict.parse(xml_str)
    result = ConvertDosageSensitivity.xmldict_data_to_pb(xmldict_value, tag_name)
    result_json = MessageToDict(result)
    assert result_json == expected_json


@pytest.mark.parametrize(
    "xml_str,tag_name,expected_json",
    [
        (
            """
            <Haploinsufficiency last_evaluated="2020-06-24" ClinGen="https://www.ncbi.nlm.nih.gov/projects/dbvar/ISCA/isca_gene.cgi?sym=SHH">Sufficient evidence for dosage pathogenicity</Haploinsufficiency>
            """,
            "Haploinsufficiency",
            {
                "clingen": "https://www.ncbi.nlm.nih.gov/projects/dbvar/ISCA/isca_gene.cgi?sym=SHH",
                "lastEvaluated": "2020-06-24T00:00:00Z",
                "value": "Sufficient evidence for dosage pathogenicity",
            },
        ),
        (
            """
            <Triplosensitivity last_evaluated="2020-06-24" ClinGen="https://www.ncbi.nlm.nih.gov/projects/dbvar/ISCA/isca_gene.cgi?sym=SHH">No evidence available</Triplosensitivity>
            """,
            "Triplosensitivity",
            {
                "clingen": "https://www.ncbi.nlm.nih.gov/projects/dbvar/ISCA/isca_gene.cgi?sym=SHH",
                "lastEvaluated": "2020-06-24T00:00:00Z",
                "value": "No evidence available",
            },
        ),
    ],
)
def test_convert_dosage_sensitivity_xmldict_data_to_pb(
    xml_str: str, tag_name: str, expected_json: Any
):
    xmldict_value = xmltodict.parse(xml_str)
    result = ConvertDosageSensitivity.xmldict_data_to_pb(xmldict_value, tag_name)
    result_json = MessageToDict(result)
    assert result_json == expected_json


@pytest.mark.parametrize(
    "xml_str,expected_json",
    [
        (
            """
            <Co-occurrenceSet>
                <Zygosity>SingleHeterozygote</Zygosity>
                <AlleleDescSet>
                    <Name>GCK:c.1253+8C&gt;T</Name>
                    <Zygosity>Homozygote</Zygosity>
                </AlleleDescSet>
                <AlleleDescSet>
                    <Name>HNF4A:c.459T&gt;C</Name>
                    <Zygosity>SingleHeterozygote</Zygosity>
                </AlleleDescSet>
                <AlleleDescSet>
                    <Name>TCF1:c.51C&gt;G</Name>
                    <Zygosity>SingleHeterozygote</Zygosity>
                </AlleleDescSet>
                <AlleleDescSet>
                    <Name>TCF1:c.1720A&gt;G</Name>
                    <Zygosity>Homozygote</Zygosity>
                </AlleleDescSet>
                <Count>1</Count>
            </Co-occurrenceSet>
            """,
            {
                "alleleDescriptions": [
                    {
                        "name": "GCK:c.1253+8C>T",
                        "zygosity": "ZYGOSITY_HOMOZYGOTE",
                    },
                    {
                        "name": "HNF4A:c.459T>C",
                        "zygosity": "ZYGOSITY_SINGLE_HETEROZYGOTE",
                    },
                    {
                        "name": "TCF1:c.51C>G",
                        "zygosity": "ZYGOSITY_SINGLE_HETEROZYGOTE",
                    },
                    {
                        "name": "TCF1:c.1720A>G",
                        "zygosity": "ZYGOSITY_HOMOZYGOTE",
                    },
                ],
                "count": 1,
                "zygosity": "ZYGOSITY_SINGLE_HETEROZYGOTE",
            },
        ),
        (
            """
            <Co-occurrenceSet>
                <Zygosity>SingleHeterozygote</Zygosity>
                <AlleleDescSet>
                    <Name>LAMP2:c.156A&gt;T</Name>
                    <Zygosity>Homozygote</Zygosity>
                </AlleleDescSet>
                <Count>1</Count>
            </Co-occurrenceSet>
            """,
            {
                "alleleDescriptions": [
                    {
                        "name": "LAMP2:c.156A>T",
                        "zygosity": "ZYGOSITY_HOMOZYGOTE",
                    },
                ],
                "count": 1,
                "zygosity": "ZYGOSITY_SINGLE_HETEROZYGOTE",
            },
        ),
    ],
)
def test_convert_cooccurrence_xmldict_data_to_pb(xml_str: str, expected_json: Any):
    xmldict_value = xmltodict.parse(xml_str)
    result = ConvertCooccurrence.xmldict_data_to_pb(xmldict_value)
    result_json = MessageToDict(result)
    assert result_json == expected_json


@pytest.mark.parametrize(
    "xmldict_value,expected",
    [
        ("primary", Submitter.Type.TYPE_PRIMARY),
        ("secondary", Submitter.Type.TYPE_SECONDARY),
        ("behalf", Submitter.Type.TYPE_BEHALF),
    ],
)
def test_convert_submitter_convert_type(
    xmldict_value: str, expected: ObservedIn.ObservedDataAttribute.Type.ValueType
):
    result = ConvertSubmitter.convert_type(xmldict_value)
    assert result == expected


@pytest.mark.parametrize(
    "xml_str,expected_json",
    [
        (
            """
            <SubmitterDescription OrgID="505516" SubmitterName="University of Washington Center for Mendelian Genomics, University of Washington" Type="secondary" OrganizationCategory="laboratory"/>
            """,
            {
                "submitterIdentifiers": {
                    "orgCategory": "laboratory",
                    "orgId": "505516",
                    "submitterName": "University of Washington Center for Mendelian Genomics, University of Washington",
                },
                "type": "TYPE_SECONDARY",
            },
        ),
        (
            """
            <SubmitterDescription OrgID="506382" SubmitterName="Diagnostic Laboratory, Department of Genetics, University Medical Center Groningen" Type="behalf" OrganizationCategory="laboratory"/>
            """,
            {
                "submitterIdentifiers": {
                    "orgCategory": "laboratory",
                    "orgId": "506382",
                    "submitterName": "Diagnostic Laboratory, Department of Genetics, University Medical Center Groningen",
                },
                "type": "TYPE_BEHALF",
            },
        ),
    ],
)
def test_convert_submitter_xmldict_data_to_pb(xml_str: str, expected_json: Any):
    xmldict_value = xmltodict.parse(xml_str)
    result = ConvertSubmitter.xmldict_data_to_pb(xmldict_value)
    result_json = MessageToDict(result)
    assert result_json == expected_json


@pytest.mark.parametrize(
    "xml_str,expected_json",
    [
        (
            """
            <Name>AP5Z1, 4-BP DEL/22-BP INS, NT80</Name>
            """,
            {
                "value": "AP5Z1, 4-BP DEL/22-BP INS, NT80",
            },
        ),
        (
            """
            <Name Type="NonHGVS">4-BP DEL/22-BP INS, NT80</Name>
            """,
            {
                "type": "NonHGVS",
                "value": "4-BP DEL/22-BP INS, NT80",
            },
        ),
    ],
)
def test_convert_other_name_list_xmldict_data_to_pb(xml_str: str, expected_json: Any):
    xmldict_value = xmltodict.parse(xml_str)
    result = ConvertOtherName.xmldict_data_to_pb(xmldict_value)
    result_json = MessageToDict(result)
    assert result_json == expected_json


@pytest.mark.parametrize(
    "xml_str,expected_json",
    [
        (
            """
            <Accession Version="1" DateDeleted="2021-07-14">SCV000087037</Accession>
            """,
            {
                "accession": "SCV000087037",
                "dateDeleted": "2021-07-14T00:00:00Z",
                "version": 1,
            },
        ),
    ],
)
def test_convert_deleted_scv_xmldict_data_to_pb(xml_str: str, expected_json: Any):
    xmldict_value = xmltodict.parse(xml_str)
    result = ConvertDeletedScv.xmldict_data_to_pb(xmldict_value)
    result_json = MessageToDict(result)
    assert result_json == expected_json


@pytest.mark.parametrize(
    "xmldict_value,expected",
    [
        ("current", Location.SequenceLocation.AssemblyStatus.ASSEMBLY_STATUS_CURRENT),
        ("previous", Location.SequenceLocation.AssemblyStatus.ASSEMBLY_STATUS_PREVIOUS),
    ],
)
def test_convert_location_convert_assembly_status(
    xmldict_value: str, expected: Location.SequenceLocation.AssemblyStatus.ValueType
):
    result = ConvertLocation.convert_assembly_status(xmldict_value)
    assert result == expected


@pytest.mark.parametrize(
    "xml_str,expected_json",
    [
        (
            """
            <SequenceLocation Assembly="GRCh38" AssemblyAccessionVersion="GCF_000001405.38" forDisplay="true" AssemblyStatus="current" Chr="7" Accession="NC_000007.14" start="4781213" stop="4781216" display_start="4781213" display_stop="4781216" variantLength="22" positionVCF="4781213" referenceAlleleVCF="GGAT" alternateAlleleVCF="TGCTGTAAACTGTAACTGTAAA"/>
            """,
            {
                "accession": "NC_000007.14",
                "alternateAlleleVcf": "TGCTGTAAACTGTAACTGTAAA",
                "assembly": "GRCh38",
                "chr": "CHROMOSOME_7",
                "displayStart": 4781213,
                "displayStop": 4781216,
                "forDisplay": True,
                "positionVcf": 4781213,
                "referenceAlleleVcf": "GGAT",
                "start": 4781213,
                "stop": 4781216,
                "variantLength": 22,
            },
        ),
        (
            """
            <SequenceLocation Assembly="GRCh38" AssemblyAccessionVersion="GCF_000001405.38" forDisplay="true" AssemblyStatus="current" Chr="5" Accession="NC_000005.10" innerStart="181356054" innerStop="181448620" display_start="181356054" display_stop="181448620" variantLength="92567"/>
            """,
            {
                "accession": "NC_000005.10",
                "assembly": "GRCh38",
                "chr": "CHROMOSOME_5",
                "displayStart": 181356054,
                "displayStop": 181448620,
                "forDisplay": True,
                "innerStart": 181356054,
                "innerStop": 181448620,
                "variantLength": 92567,
            },
        ),
    ],
)
def test_convert_location_convert_sequence_location(xml_str: str, expected_json: Any):
    xmldict_value = xmltodict.parse(xml_str)
    result = ConvertLocation.convert_sequence_location(xmldict_value)
    result_json = MessageToDict(result)
    assert result_json == expected_json


@pytest.mark.parametrize(
    "xml_str,expected_json",
    [
        (
            """
            <Location>
                <GeneLocation>NM_003126.2: exon 2</GeneLocation>
            </Location>
            """,
            {
                "geneLocations": [
                    "NM_003126.2: exon 2",
                ],
            },
        ),
        (
            """
            <Location>
                <CytogeneticLocation>14q31.1</CytogeneticLocation>
                <SequenceLocation Assembly="GRCh38" AssemblyAccessionVersion="GCF_000001405.38" AssemblyStatus="current" Chr="14" Accession="NC_000014.9" start="80955621" stop="81146306" display_start="80955621" display_stop="81146306" Strand="+"/>
                <SequenceLocation Assembly="GRCh37" AssemblyAccessionVersion="GCF_000001405.25" AssemblyStatus="previous" Chr="14" Accession="NC_000014.8" start="81421868" stop="81612645" display_start="81421868" display_stop="81612645" Strand="+"/>
            </Location>
            """,
            {
                "cytogeneticLocations": [
                    "14q31.1",
                ],
                "sequenceLocations": [
                    {
                        "accession": "NC_000014.9",
                        "assembly": "GRCh38",
                        "chr": "CHROMOSOME_14",
                        "displayStart": 80955621,
                        "displayStop": 81146306,
                        "start": 80955621,
                        "stop": 81146306,
                        "strand": "+",
                    },
                    {
                        "accession": "NC_000014.8",
                        "assembly": "GRCh37",
                        "chr": "CHROMOSOME_14",
                        "displayStart": 81421868,
                        "displayStop": 81612645,
                        "start": 81421868,
                        "stop": 81612645,
                        "strand": "+",
                    },
                ],
            },
        ),
    ],
)
def test_convert_location_xmldict_data_to_pb(xml_str: str, expected_json: Any):
    xmldict_value = xmltodict.parse(xml_str)
    result = ConvertLocation.xmldict_data_to_pb(xmldict_value)
    result_json = MessageToDict(result)
    assert result_json == expected_json


@pytest.mark.parametrize(
    "xml_str,expected_json",
    [
        (
            """
            <SCV Title="SUB12197219" Accession="SCV002586263" Version="1"/>
            """,
            {
                "accession": "SCV002586263",
                "title": "SUB12197219",
                "version": 1,
            },
        ),
        (
            """
            <SCV Accession="SCV003843202" Version="1"/>
            """,
            {
                "accession": "SCV003843202",
                "version": 1,
            },
        ),
    ],
)
def test_convert_scv_xmldict_data_to_pb(xml_str: str, expected_json: Any):
    xmldict_value = xmltodict.parse(xml_str)
    result = ConvertScv.xmldict_data_to_pb(xmldict_value)
    result_json = MessageToDict(result)
    assert result_json == expected_json


@pytest.mark.parametrize(
    "xml_str,expected_json",
    [
        (
            """
            <SampleDescription>
                <Description Type="public">A limited chromosome study confirmed that...</Description>
                <Citation Type="general">
                    <ID Source="PubMed">20613862</ID>
                </Citation>
            </SampleDescription>
            """,
            {
                "citation": {
                    "ids": [
                        {
                            "source": "PubMed",
                            "value": "20613862",
                        },
                    ],
                    "type": "general",
                },
                "description": {
                    "type": "COMMENT_TYPE_PUBLIC",
                    "value": "A limited chromosome study confirmed that...",
                },
            },
        ),
        (
            """
            <SampleDescription>
                <Description Type="public">A limited chromosome study confirmed that...</Description>
            </SampleDescription>
            """,
            {
                "description": {
                    "type": "COMMENT_TYPE_PUBLIC",
                    "value": "A limited chromosome study confirmed that...",
                },
            },
        ),
    ],
)
def test_convert_sample_convert_sample_description(xml_str: str, expected_json: Any):
    xmldict_value = xmltodict.parse(xml_str)
    result = ConvertSample.convert_sample_description(xmldict_value)
    result_json = MessageToDict(result)
    assert result_json == expected_json


@pytest.mark.parametrize(
    "xmldict_value,expected",
    [
        ("present", Sample.SomaticVariantInNormalTissue.SOMATIC_VARIANT_IN_NORMAL_TISSUE_PRESENT),
        ("absent", Sample.SomaticVariantInNormalTissue.SOMATIC_VARIANT_IN_NORMAL_TISSUE_ABSENT),
        (
            "not tested",
            Sample.SomaticVariantInNormalTissue.SOMATIC_VARIANT_IN_NORMAL_TISSUE_NOT_TESTED,
        ),
    ],
)
def test_convert_sample_convert_somatic_variant_in_normal_tissue(
    xmldict_value: str, expected: Sample.SomaticVariantInNormalTissue.ValueType
):
    result = ConvertSample.convert_somatic_variant_in_normal_tissue(xmldict_value)
    assert result == expected


@pytest.mark.parametrize(
    "xmldict_value,expected",
    [
        ("days", Sample.AgeUnit.AGE_UNIT_DAYS),
        ("weeks", Sample.AgeUnit.AGE_UNIT_WEEKS),
        ("months", Sample.AgeUnit.AGE_UNIT_MONTHS),
        ("years", Sample.AgeUnit.AGE_UNIT_YEARS),
        ("weeks gestation", Sample.AgeUnit.AGE_UNIT_WEEKS_GESTATION),
        ("months gestation", Sample.AgeUnit.AGE_UNIT_MONTHS_GESTATION),
    ],
)
def test_convert_sample_convert_age_unit(xmldict_value: str, expected: Sample.AgeUnit.ValueType):
    result = ConvertSample.convert_age_unit(xmldict_value)
    assert result == expected


@pytest.mark.parametrize(
    "xmldict_value,expected",
    [
        ("minimum", Sample.AgeType.AGE_TYPE_MINIMUM),
        ("maximum", Sample.AgeType.AGE_TYPE_MAXIMUM),
        ("single", Sample.AgeType.AGE_TYPE_SINGLE),
    ],
)
def test_convert_sample_convert_age_type(xmldict_value: str, expected: Sample.AgeType.ValueType):
    result = ConvertSample.convert_age_type(xmldict_value)
    assert result == expected


@pytest.mark.parametrize(
    "xmldict_value,expected",
    [
        ("yes", Sample.AffectedStatus.AFFECTED_STATUS_YES),
        ("no", Sample.AffectedStatus.AFFECTED_STATUS_NO),
        ("not provided", Sample.AffectedStatus.AFFECTED_STATUS_NOT_PROVIDED),
        ("unknown", Sample.AffectedStatus.AFFECTED_STATUS_UNKNOWN),
        ("not applicable", Sample.AffectedStatus.AFFECTED_STATUS_NOT_APPLICABLE),
    ],
)
def test_convert_sample_convert_affected_status(
    xmldict_value: str, expected: Sample.AffectedStatus.ValueType
):
    result = ConvertSample.convert_affected_status(xmldict_value)
    assert result == expected


@pytest.mark.parametrize(
    "xml_str,expected_json",
    [
        (
            """
            <Age Type="minimum" age_unit="years">10</Age>
            """,
            {
                "type": "AGE_TYPE_MINIMUM",
                "unit": "AGE_UNIT_YEARS",
                "value": 10,
            },
        ),
        (
            """
            <Age Type="single" age_unit="years">10</Age>
            """,
            {
                "type": "AGE_TYPE_SINGLE",
                "unit": "AGE_UNIT_YEARS",
                "value": 10,
            },
        ),
    ],
)
def test_convert_sample_convert_age(xml_str: str, expected_json: Any):
    xmldict_value = xmltodict.parse(xml_str)
    result = ConvertSample.convert_age(xmldict_value)
    result_json = MessageToDict(result)
    assert result_json == expected_json


@pytest.mark.parametrize(
    "xmldict_value,expected",
    [
        ("male", Sample.Gender.GENDER_MALE),
        ("female", Sample.Gender.GENDER_FEMALE),
        ("mixed", Sample.Gender.GENDER_MIXED),
    ],
)
def test_convert_sample_convert_gender(xmldict_value: str, expected: Sample.Gender.ValueType):
    result = ConvertSample.convert_gender(xmldict_value)
    assert result == expected


@pytest.mark.parametrize(
    "xmldict_value,expected",
    [
        ("submitter-generated", Sample.SourceType.SOURCE_TYPE_SUBMITTER_GENERATED),
        ("data mining", Sample.SourceType.SOURCE_TYPE_DATA_MINING),
    ],
)
def test_convert_sample_convert_source_type(
    xmldict_value: str, expected: Sample.SourceType.ValueType
):
    result = ConvertSample.convert_source_type(xmldict_value)
    assert result == expected


@pytest.mark.parametrize(
    "xml_str,expected_json",
    [
        (
            """
            <FamilyData NumFamilies="1"/>
            """,
            {
                "numFamilies": 1,
            },
        ),
        (
            """
            <FamilyData>
                <FamilyHistory>yes</FamilyHistory>
            </FamilyData>
            """,
            {
                "familyHistory": "yes",
            },
        ),
        (
            """
            <FamilyData NumFamiliesWithVariant="3"/>
            """,
            {
                "numFamiliesWithVariant": 3,
            },
        ),
        (
            """
            <FamilyData NumFamilies="1" NumFamiliesWithSegregationObserved="1" NumFamiliesWithVariant="1" />
            """,
            {
                "numFamilies": 1,
                "numFamiliesWithSegregationObserved": 1,
                "numFamiliesWithVariant": 1,
            },
        ),
        (
            """
            <FamilyData PedigreeID="a921726"/>
            """,
            {"pedigreeId": "a921726"},
        ),
    ],
)
def test_convert_family_data_xmldict_data_to_pb(xml_str: str, expected_json: Any):
    xmldict_value = xmltodict.parse(xml_str)
    result = ConvertFamilyData.xmldict_data_to_pb(xmldict_value)
    result_json = MessageToDict(result)
    assert result_json == expected_json


@pytest.mark.parametrize(
    "xml_str,expected_json",
    [
        (
            """
            <Sample>
                <Origin>germline</Origin>
                <Species>human</Species>
                <AffectedStatus>not provided</AffectedStatus>
            </Sample>
            """,
            {
                "affectedStatus": "AFFECTED_STATUS_NOT_PROVIDED",
                "origin": "ORIGIN_GERMLINE",
                "species": {
                    "name": "human",
                },
            },
        ),
        (
            """
            <Sample>
                <Origin>germline</Origin>
                <Ethnicity>European</Ethnicity>
                <Species TaxonomyId="9606">human</Species>
                <AffectedStatus>unknown</AffectedStatus>
                <NumberTested>331</NumberTested>
            </Sample>
            """,
            {
                "affectedStatus": "AFFECTED_STATUS_UNKNOWN",
                "ethnicity": "European",
                "numerTested": 331,
                "origin": "ORIGIN_GERMLINE",
                "species": {
                    "name": "human",
                    "taxonomyId": 9606,
                },
            },
        ),
        (
            """
            <Sample>
                <Origin>paternal</Origin>
                <Species TaxonomyId="9606">human</Species>
                <AffectedStatus>yes</AffectedStatus>
            </Sample>
            """,
            {
                "affectedStatus": "AFFECTED_STATUS_YES",
                "origin": "ORIGIN_PATERNAL",
                "species": {
                    "name": "human",
                    "taxonomyId": 9606,
                },
            },
        ),
        (
            """
            <Sample>
                <Origin>paternal</Origin>
                <Ethnicity>Caucasian</Ethnicity>
                <GeographicOrigin>Greece</GeographicOrigin>
                <Species TaxonomyId="9606">human</Species>
                <Age Type="minimum" age_unit="years">10</Age>
                <Age Type="maximum" age_unit="years">19</Age>
                <AffectedStatus>yes</AffectedStatus>
                <Gender>male</Gender>
            </Sample>
            """,
            {
                "affectedStatus": "AFFECTED_STATUS_YES",
                "ages": [
                    {
                        "type": "AGE_TYPE_MINIMUM",
                        "unit": "AGE_UNIT_YEARS",
                        "value": 10,
                    },
                    {
                        "type": "AGE_TYPE_MAXIMUM",
                        "unit": "AGE_UNIT_YEARS",
                        "value": 19,
                    },
                ],
                "ethnicity": "Caucasian",
                "gender": "GENDER_MALE",
                "geographicOrigin": "Greece",
                "origin": "ORIGIN_PATERNAL",
                "species": {
                    "name": "human",
                    "taxonomyId": 9606,
                },
            },
        ),
    ],
)
def test_convert_sample_xml_data_to_pb(xml_str: str, expected_json: Any):
    xmldict_value = xmltodict.parse(xml_str)
    result = ConvertSample.xmldict_data_to_pb(xmldict_value)
    result_json = MessageToDict(result)
    assert result_json == expected_json


@pytest.mark.parametrize(
    "xmldict_value,expected",
    [
        ("number of occurences", Method.ResultType.RESULT_TYPE_NUMBER_OF_OCCURRENCES),
        ("p value", Method.ResultType.RESULT_TYPE_P_VALUE),
        ("odds ratio", Method.ResultType.RESULT_TYPE_ODDS_RATIO),
        ("variant call", Method.ResultType.RESULT_TYPE_VARIANT_CALL),
    ],
)
def test_convert_method_type_convert_result_type(
    xmldict_value: str, expected: Method.ResultType.ValueType
):
    result = ConvertMethodType.convert_result_type(xmldict_value)
    assert result == expected


@pytest.mark.parametrize(
    "xmldict_value,expected",
    [
        ("submitter-generated", Method.SourceType.SOURCE_TYPE_SUBMITTER_GENERATED),
        ("data mining", Method.SourceType.SOURCE_TYPE_DATA_MINING),
        ("data review", Method.SourceType.SOURCE_TYPE_DATA_REVIEW),
    ],
)
def test_convert_method_type_convert_source_type(
    xmldict_value: str, expected: Method.SourceType.ValueType
):
    result = ConvertMethodType.convert_source_type(xmldict_value)
    assert result == expected


@pytest.mark.parametrize(
    "xmldict_value,expected",
    [
        ("Location", Method.MethodAttribute.AttributeType.ATTRIBUTE_TYPE_LOCATION),
        (
            "ControlsAppropriate",
            Method.MethodAttribute.AttributeType.ATTRIBUTE_TYPE_CONTROLS_APPROPRIATE,
        ),
        (
            "MethodAppropriate",
            Method.MethodAttribute.AttributeType.ATTRIBUTE_TYPE_METHOD_APPROPRIATE,
        ),
        ("TestName", Method.MethodAttribute.AttributeType.ATTRIBUTE_TYPE_TEST_NAME),
        (
            "StructVarMethodType",
            Method.MethodAttribute.AttributeType.ATTRIBUTE_TYPE_STRUCT_VAR_METHOD_TYPE,
        ),
        ("ProbeAccession", Method.MethodAttribute.AttributeType.ATTRIBUTE_TYPE_PROBE_ACCESSION),
    ],
)
def test_convert_method_type_convert_method_attribute_type(
    xmldict_value: str, expected: Method.MethodAttribute.AttributeType.ValueType
):
    result = ConvertMethodType.convert_method_attribute_type(xmldict_value)
    assert result == expected


@pytest.mark.parametrize(
    "xml_str,expected_json",
    [
        (
            """
            <MethodAttribute>
                <Attribute Type="StructVarMethodType">Sequence alignment</Attribute>
            </MethodAttribute>
            """,
            {
                "base": {
                    "value": "Sequence alignment",
                },
                "type": "ATTRIBUTE_TYPE_STRUCT_VAR_METHOD_TYPE",
            },
        ),
        (
            """
            <MethodAttribute>
                <Attribute Type="TestName">Targeted Exome Sequencing</Attribute>
            </MethodAttribute>
            """,
            {
                "base": {
                    "value": "Targeted Exome Sequencing",
                },
                "type": "ATTRIBUTE_TYPE_TEST_NAME",
            },
        ),
    ],
)
def test_convert_method_type_convert_method_attribute(xml_str: str, expected_json: Any):
    xmldict_value = xmltodict.parse(xml_str)
    result = ConvertMethodType.convert_method_attribute(xmldict_value)
    result_json = MessageToDict(result)
    assert result_json == expected_json


@pytest.mark.parametrize(
    "xmldict_value,expected",
    [
        ("MethodResult", Method.ObsMethodAttribute.AttributeType.ATTRIBUTE_TYPE_METHOD_RESULT),
        (
            "TestingLaboratory",
            Method.ObsMethodAttribute.AttributeType.ATTRIBUTE_TYPE_TESTING_LABORATORY,
        ),
    ],
)
def test_convert_method_type_convert_obs_method_attribute_type(
    xmldict_value: str, expected: Method.ObsMethodAttribute.AttributeType.ValueType
):
    result = ConvertMethodType.convert_obs_method_attribute_type(xmldict_value)
    assert result == expected


@pytest.mark.parametrize(
    "xml_str,expected_json",
    [
        (
            """
            <ObsMethodAttribute>
                <Attribute Type="TestingLaboratory" dateValue="2017-01-17" integerValue="26957">GeneDx</Attribute>
            </ObsMethodAttribute>
            """,
            {
                "base": {
                    "dateValue": "2017-01-17T00:00:00Z",
                    "integerValue": "26957",
                    "value": "GeneDx",
                },
                "type": "ATTRIBUTE_TYPE_TESTING_LABORATORY",
            },
        ),
        (
            """
            <ObsMethodAttribute>
                <Attribute Type="TestingLaboratory" dateValue="2015-02-27" integerValue="500040">Lineagen, Inc</Attribute>
                <Comment>Uncertain significance</Comment>
            </ObsMethodAttribute>
            """,
            {
                "base": {
                    "dateValue": "2015-02-27T00:00:00Z",
                    "integerValue": "500040",
                    "value": "Lineagen, Inc",
                },
                "comments": [
                    {
                        "value": "Uncertain significance",
                    },
                ],
                "type": "ATTRIBUTE_TYPE_TESTING_LABORATORY",
            },
        ),
    ],
)
def test_convert_method_type_convert_obs_method_attribute(xml_str: str, expected_json: Any):
    xmldict_value = xmltodict.parse(xml_str)
    result = ConvertMethodType.convert_obs_method_attribute(xmldict_value)
    result_json = MessageToDict(result)
    assert result_json == expected_json


@pytest.mark.parametrize(
    "xml_str,expected_json",
    [
        (
            """
            <Method>
                <NamePlatform>NovaSeq</NamePlatform>
                <TypePlatform>whole exome sequencing</TypePlatform>
                <MethodType>clinical testing</MethodType>
            </Method>
            """,
            {
                "methodType": "METHOD_LIST_TYPE_CLINICAL_TESTING",
                "namePlatform": "NovaSeq",
                "typePlatform": "whole exome sequencing",
            },
        ),
        (
            """
            <Method>
                <NamePlatform>Complete Genomics</NamePlatform>
                <TypePlatform>next-gen sequencing</TypePlatform>
                <Purpose>discovery</Purpose>
                <MethodType>reference population</MethodType>
            </Method>
            """,
            {
                "methodType": "METHOD_LIST_TYPE_REFERENCE_POPULATION",
                "namePlatform": "Complete Genomics",
                "purpose": "discovery",
                "typePlatform": "next-gen sequencing",
            },
        ),
        (
            """
            <Method>
                <TypePlatform>Oligo aCGH</TypePlatform>
                <Purpose>Discovery</Purpose>
                <Description>Microarray</Description>
                <SourceType>submitter-generated</SourceType>
                <MethodType>clinical testing</MethodType>
            </Method>
            """,
            {
                "description": "Microarray",
                "methodType": "METHOD_LIST_TYPE_CLINICAL_TESTING",
                "purpose": "Discovery",
                "sourceType": "SOURCE_TYPE_SUBMITTER_GENERATED",
                "typePlatform": "Oligo aCGH",
            },
        ),
    ],
)
def test_convert_method_type_xmldict_data_to_pb(xml_str: str, expected_json: Any):
    xmldict_value = xmltodict.parse(xml_str)
    result = ConvertMethodType.xmldict_data_to_pb(xmldict_value)
    result_json = MessageToDict(result)
    assert result_json == expected_json


@pytest.mark.parametrize(
    "xml_str,expected_json",
    [
        (
            """
            <MolecularConsequence Function="frameshift mutation">
                <XRef DB="Sequence Ontology" ID="SO:0000865"/>
            </MolecularConsequence>
            """,
            {
                "function": "frameshift mutation",
                "xrefs": [
                    {
                        "db": "Sequence Ontology",
                        "id": "SO:0000865",
                    },
                ],
            },
        ),
    ],
)
def test_convert_allele_scv_convert_molecular_consequence(xml_str: str, expected_json: Any):
    xmldict_value = xmltodict.parse(xml_str)
    result = ConvertAlleleScv.convert_molecular_consequence(xmldict_value)
    result_json = MessageToDict(result)
    assert result_json == expected_json


@pytest.mark.parametrize(
    "xml_str,expected_json",
    [
        (
            """
            <SimpleAllele>
                <GeneList>
                    <Gene Symbol="AVPR2" />
                </GeneList>
                <VariantType>single nucleotide variant</VariantType>
                <MolecularConsequenceList>
                    <MolecularConsequence Function="frameshift mutation">
                        <XRef DB="Sequence Ontology" ID="SO:0000865" />
                    </MolecularConsequence>
                </MolecularConsequenceList>
                <AttributeSet>
                    <Attribute Type="HGVS">NM_000054.4:c.424delT</Attribute>
                </AttributeSet>
                <AttributeSet>
                    <Attribute Type="HGVS">p.Cys142AlafsX20</Attribute>
                </AttributeSet>
            </SimpleAllele>
            """,
            {
                "attributes": [
                    {
                        "attribute": {
                            "base": {
                                "value": "NM_000054.4:c.424delT",
                            },
                            "type": "HGVS",
                        },
                    },
                    {
                        "attribute": {
                            "base": {
                                "value": "p.Cys142AlafsX20",
                            },
                            "type": "HGVS",
                        },
                    },
                ],
                "genes": [
                    {
                        "symbol": "AVPR2",
                    },
                ],
                "molecularConsequences": [
                    {
                        "function": "frameshift mutation",
                        "xrefs": [
                            {
                                "db": "Sequence Ontology",
                                "id": "SO:0000865",
                            },
                        ],
                    },
                ],
                "variantType": "single nucleotide variant",
            },
        ),
        (
            """
            <SimpleAllele>
                <GeneList>
                    <Gene Symbol="THAP1" />
                </GeneList>
                <Name>THAP1, LYS24GLU</Name>
                <VariantType>Variation</VariantType>
                <OtherNameList>
                    <Name Type="NonHGVS">LYS24GLU</Name>
                </OtherNameList>
                <XRefList>
                    <XRef DB="OMIM" ID="609520.0008" Type="Allelic variant" />
                </XRefList>
            </SimpleAllele>
            """,
            {
                "genes": [
                    {
                        "symbol": "THAP1",
                    },
                ],
                "names": [
                    {
                        "value": "THAP1, LYS24GLU",
                    },
                ],
                "otherNames": [
                    {
                        "type": "NonHGVS",
                        "value": "LYS24GLU",
                    },
                ],
                "variantType": "Variation",
                "xrefs": [
                    {
                        "db": "OMIM",
                        "id": "609520.0008",
                        "type": "Allelic variant",
                    },
                ],
            },
        ),
    ],
)
def test_convert_allele_scv_xmldict_data_to_pb(xml_str: str, expected_json: Any):
    xmldict_value = xmltodict.parse(xml_str)
    result = ConvertAlleleScv.xmldict_data_to_pb(xmldict_value)
    result_json = MessageToDict(result)
    assert result_json == expected_json


@pytest.mark.parametrize(
    "xml_str",
    [
        """
        <Haplotype>
            <SimpleAllele>
                <GeneList>
                    <Gene Symbol="PIGN" />
                </GeneList>
                <VariantType>Variation</VariantType>
                <AttributeSet>
                    <Attribute Type="HGVS">NM_176787.5:c.2399G&gt;A</Attribute>
                </AttributeSet>
            </SimpleAllele>
            <SimpleAllele>
                <GeneList>
                    <Gene Symbol="PIGN" />
                </GeneList>
                <VariantType>Variation</VariantType>
                <AttributeSet>
                    <Attribute Type="HGVS">NM_176787.5:c.1251+1G&gt;T</Attribute>
                </AttributeSet>
            </SimpleAllele>
        </Haplotype>
        """,
        """
        <Haplotype>
            <SimpleAllele>
                <GeneList>
                    <Gene Symbol="INVS" />
                </GeneList>
                <VariantType>Variation</VariantType>
                <AttributeSet>
                    <Attribute Type="HGVS">NM_014425.5:c.796+5G&gt;A</Attribute>
                </AttributeSet>
            </SimpleAllele>
            <SimpleAllele>
                <GeneList>
                    <Gene Symbol="INVS" />
                </GeneList>
                <VariantType>Variation</VariantType>
                <AttributeSet>
                    <Attribute Type="HGVS">NM_014425.5:c.805_806del</Attribute>
                </AttributeSet>
            </SimpleAllele>
        </Haplotype>
        """,
    ],
    ids=["pign", "invs"],
)
def test_convert_haplootype_scv_xmldict_data_to_pb(xml_str: str, snapshot):
    xmldict_value = xmltodict.parse(xml_str)
    result = ConvertHaplotypeScv.xmldict_data_to_pb(xmldict_value)
    result_json = MessageToDict(result)
    snapshot.assert_match(json.dumps(result_json, indent=2), "result")


@pytest.mark.parametrize(
    "xml_str",
    [
        """
        <Genotype>
            <SimpleAllele>
                <GeneList>
                    <Gene Symbol="DYNC2H1">
                        <Name>dynein cytoplasmic 2 heavy chain 1</Name>
                    </Gene>
                </GeneList>
                <VariantType>Variation</VariantType>
                <Location>
                    <GeneLocation>NM_001080463.1:exon 48</GeneLocation>
                </Location>
                <OtherNameList>
                    <Name Type="SubmitterVariantId">D-2653</Name>
                    <Name>p.H2595R</Name>
                </OtherNameList>
                <AttributeSet>
                    <Attribute Type="HGVS">NM_001080463.1:c.7784A&gt;G</Attribute>
                </AttributeSet>
            </SimpleAllele>
            <SimpleAllele>
                <GeneList>
                    <Gene Symbol="DYNC2H1">
                        <Name>dynein cytoplasmic 2 heavy chain 1</Name>
                    </Gene>
                </GeneList>
                <VariantType>Variation</VariantType>
                <Location>
                    <GeneLocation>NM_001080463.1:Exon 33</GeneLocation>
                </Location>
                <OtherNameList>
                    <Name Type="SubmitterVariantId">D-2653</Name>
                    <Name>p.G1685R</Name>
                </OtherNameList>
                <AttributeSet>
                    <Attribute Type="HGVS">NM_001080463.1:c.5053G&gt;A</Attribute>
                </AttributeSet>
            </SimpleAllele>
            <VariationType>CompoundHeterozygote</VariationType>
        </Genotype>
        """,
        """
        <Genotype>
            <SimpleAllele>
                <GeneList>
                    <Gene Symbol="SRD5A2">
                        <Name>steroid 5 alpha-reductase 2</Name>
                    </Gene>
                </GeneList>
                <VariantType>Variation</VariantType>
                <Location>
                    <GeneLocation>NM_000348.3:intron 3</GeneLocation>
                </Location>
                <AttributeSet>
                    <Attribute Type="HGVS">NC_000002.11:g.31754536A&gt;C</Attribute>
                </AttributeSet>
            </SimpleAllele>
            <SimpleAllele>
                <GeneList>
                    <Gene Symbol="SRD5A2">
                        <Name>steroid 5 alpha-reductase 2</Name>
                    </Gene>
                </GeneList>
                <VariantType>Variation</VariantType>
                <Location>
                    <GeneLocation>NM_000348.3:exon 4</GeneLocation>
                </Location>
                <XRefList>
                    <XRef DB="dbSNP" ID="rs9332964" />
                </XRefList>
                <AttributeSet>
                    <Attribute Type="HGVS">NC_000002.11:g.31754395C&gt;T</Attribute>
                </AttributeSet>
            </SimpleAllele>
            <VariationType>CompoundHeterozygote</VariationType>
        </Genotype>
        """,
    ],
    ids=["dync2h1", "srd5a2"],
)
def test_convert_genotype_scv_xmldict_data_to_pb(xml_str: str, snapshot):
    xmldict_value = xmltodict.parse(xml_str)
    result = ConvertGenotypeScv.xmldict_data_to_pb(xmldict_value)
    result_json = MessageToDict(result)
    snapshot.assert_match(json.dumps(result_json, indent=2), "result")


@pytest.mark.parametrize(
    "xmldict_value,expected",
    [
        ("literature only", ObservedIn.MethodType.METHOD_TYPE_LITERATURE_ONLY),
        ("reference population", ObservedIn.MethodType.METHOD_TYPE_REFERENCE_POPULATION),
        ("case-control", ObservedIn.MethodType.METHOD_TYPE_CASE_CONTROL),
        ("clinical testing", ObservedIn.MethodType.METHOD_TYPE_CLINICAL_TESTING),
        ("in vitro", ObservedIn.MethodType.METHOD_TYPE_IN_VITRO),
        ("in vivo", ObservedIn.MethodType.METHOD_TYPE_IN_VIVO),
        ("inferred from source", ObservedIn.MethodType.METHOD_TYPE_INFERRED_FROM_SOURCE),
        ("research", ObservedIn.MethodType.METHOD_TYPE_RESEARCH),
    ],
)
def test_convert_observed_in_convert_method_type(
    xmldict_value: str, expected: ObservedIn.MethodType.ValueType
):
    result = ConvertObservedIn.convert_method_type(xmldict_value)
    assert result == expected


@pytest.mark.parametrize(
    "xmldict_value,expected",
    [
        ("Description", ObservedIn.ObservedDataAttribute.Type.TYPE_DESCRIPTION),
        ("VariantAlleles", ObservedIn.ObservedDataAttribute.Type.TYPE_VARIANT_ALLELES),
        ("SubjectsWithVariant", ObservedIn.ObservedDataAttribute.Type.TYPE_SUBJECTS_WITH_VARIANT),
        (
            "SubjectsWithDifferentCausativeVariant",
            ObservedIn.ObservedDataAttribute.Type.TYPE_SUBJECTS_WITH_DIFFERENT_CAUSATIVE_VARIANT,
        ),
        ("VariantChromosomes", ObservedIn.ObservedDataAttribute.Type.TYPE_VARIANT_CHROMOSOMES),
        (
            "IndependentObservations",
            ObservedIn.ObservedDataAttribute.Type.TYPE_INDEPENDENT_OBSERVATIONS,
        ),
        ("SingleHeterozygote", ObservedIn.ObservedDataAttribute.Type.TYPE_SINGLE_HETEROZYGOUS),
        ("CompoundHeterozygote", ObservedIn.ObservedDataAttribute.Type.TYPE_COMPOUND_HETEROZYGOUS),
        ("Homozygote", ObservedIn.ObservedDataAttribute.Type.TYPE_HOMOZYGOUS),
        ("Hemizygote", ObservedIn.ObservedDataAttribute.Type.TYPE_HEMIZYGOUS),
        ("NumberMosaic", ObservedIn.ObservedDataAttribute.Type.TYPE_NUMBER_MOSAIC),
        ("ObservedUnspecified", ObservedIn.ObservedDataAttribute.Type.TYPE_OBSERVED_UNSPECIFIED),
        ("AlleleFrequency", ObservedIn.ObservedDataAttribute.Type.TYPE_ALLELE_FREQUENCY),
        ("SecondaryFinding", ObservedIn.ObservedDataAttribute.Type.TYPE_SECONDARY_FINDING),
        (
            "GenotypeAndMOIConsistent",
            ObservedIn.ObservedDataAttribute.Type.TYPE_GENOTYPE_AND_MOI_CONSISTENT,
        ),
        (
            "UnaffectedFamilyMemberWithCausativeVariant",
            ObservedIn.ObservedDataAttribute.Type.TYPE_UNAFFECTED_FAMILY_MEMBER_WITH_CAUSATIVE_VARIANT,
        ),
        (
            "HetParentTransmitNormalAllele",
            ObservedIn.ObservedDataAttribute.Type.TYPE_HET_PARENT_TRANSMIT_NORMAL_ALLELE,
        ),
        (
            "CosegregatingFamilies",
            ObservedIn.ObservedDataAttribute.Type.TYPE_COSEGREGATING_FAMILIES,
        ),
        ("InformativeMeioses", ObservedIn.ObservedDataAttribute.Type.TYPE_INFORMATIVE_MEIOSES),
        ("SampleLocalID", ObservedIn.ObservedDataAttribute.Type.TYPE_SAMPLE_LOCAL_ID),
        ("SampleVariantID", ObservedIn.ObservedDataAttribute.Type.TYPE_SAMPLE_VARIANT_ID),
        ("FamilyHistory", ObservedIn.ObservedDataAttribute.Type.TYPE_FAMILY_HISTORY),
        (
            "NumFamiliesWithVariant",
            ObservedIn.ObservedDataAttribute.Type.TYPE_NUM_FAMILIES_WITH_VARIANT,
        ),
        (
            "NumFamiliesWithSegregationObserved",
            ObservedIn.ObservedDataAttribute.Type.TYPE_NUM_FAMILIES_WITH_SEGREGATION_OBSERVED,
        ),
        ("SegregationObserved", ObservedIn.ObservedDataAttribute.Type.TYPE_SEGREGATION_OBSERVED),
    ],
)
def test_convert_observed_in_convert_observed_data_attribute_type(
    xmldict_value: str, expected: ObservedIn.ObservedDataAttribute.Type.ValueType
):
    result = ConvertObservedIn.convert_observed_data_attribute_type(xmldict_value)
    assert result == expected


@pytest.mark.parametrize(
    "xml_str,expected_json",
    [
        (
            """
            <Attribute Type="Description">In 2 French sibs...</Attribute>
            """,
            {
                "base": {
                    "value": "In 2 French sibs...",
                },
                "type": "TYPE_DESCRIPTION",
            },
        ),
        (
            """
            <Attribute Type="VariantAlleles" integerValue="2"/>
            """,
            {
                "base": {
                    "integerValue": "2",
                },
                "type": "TYPE_VARIANT_ALLELES",
            },
        ),
    ],
)
def test_convert_observed_in_convert_observed_data_attribute(xml_str: str, expected_json: Any):
    xmldict_value = xmltodict.parse(xml_str)
    result = ConvertObservedIn.convert_observed_data_attribute(xmldict_value)
    result_json = MessageToDict(result)
    assert result_json == expected_json


@pytest.mark.parametrize(
    "xml_str,expected_json",
    [
        (
            """
            <ObservedData>
                <Attribute Type="VariantAlleles" integerValue="2"/>
            </ObservedData>
            """,
            {
                "attributes": [
                    {
                        "base": {
                            "integerValue": "2",
                        },
                        "type": "TYPE_VARIANT_ALLELES",
                    },
                ],
            },
        ),
        (
            """
            <ObservedData>
                <Attribute Type="Description">In 2 French sibs with...</Attribute>
                <Citation>
                    <ID Source="PubMed">20613862</ID>
                </Citation>
                <XRef DB="OMIM" ID="613647" Type="MIM"/>
            </ObservedData>

            """,
            {
                "attributes": [
                    {
                        "base": {
                            "value": "In 2 French sibs with...",
                        },
                        "type": "TYPE_DESCRIPTION",
                    },
                ],
                "citations": [
                    {
                        "ids": [
                            {
                                "source": "PubMed",
                                "value": "20613862",
                            },
                        ],
                    },
                ],
                "xrefs": [
                    {
                        "db": "OMIM",
                        "id": "613647",
                        "type": "MIM",
                    },
                ],
            },
        ),
    ],
)
def test_convert_observed_in_convert_observed_data(xml_str: str, expected_json: Any):
    xmldict_value = xmltodict.parse(xml_str)
    result = ConvertObservedIn.convert_observed_data(xmldict_value)
    result_json = MessageToDict(result)
    assert result_json == expected_json


@pytest.mark.parametrize(
    "xml_str",
    [
        """
        <ObservedIn>
            <Sample>
                <Origin>germline</Origin>
                <Species>human</Species>
                <AffectedStatus>not provided</AffectedStatus>
            </Sample>
            <Method>
                <MethodType>literature only</MethodType>
            </Method>
            <ObservedData>
                <Attribute Type="Description">In 2 French sibs...</Attribute>
                <Citation>
                    <ID Source="PubMed">20613862</ID>
                </Citation>
                <XRef DB="OMIM" ID="613647" Type="MIM" />
            </ObservedData>
        </ObservedIn>
        """,
        """
        <ObservedIn>
            <Sample>
                <Origin>germline</Origin>
                <Species>human</Species>
                <AffectedStatus>not provided</AffectedStatus>
            </Sample>
            <Method>
                <MethodType>literature only</MethodType>
            </Method>
            <ObservedData>
                <Attribute Type="Description">Goodeve (2010) noted that...</Attribute>
                <Citation>
                    <ID Source="PubMed">20409624</ID>
                </Citation>
            </ObservedData>
            <ObservedData>
                <Attribute Type="Description">Randi et al. (1991) suggested...</Attribute>
                <Citation>
                    <ID Source="PubMed">2010538</ID>
                </Citation>
                <Citation>
                    <ID Source="PubMed">20409624</ID>
                </Citation>
            </ObservedData>
        </ObservedIn>
        """,
    ],
    ids=["omim-613647", "pubmed-20409624"],
)
def test_convert_observed_data_xmldict_data_to_pb(xml_str: str, snapshot):
    xmldict_value = xmltodict.parse(xml_str)
    result = ConvertObservedIn.xmldict_data_to_pb(xmldict_value)
    result_json = MessageToDict(result)
    snapshot.assert_match(json.dumps(result_json, indent=2), "result")


@pytest.mark.parametrize(
    "xml_str,expected_json",
    [
        (
            """
            <ClinVarSubmissionID localKey="613653.0001_SPASTIC PARAPLEGIA 48, AUTOSOMAL RECESSIVE" title="AP5Z1, 4-BP DEL/22-BP INS, NT80_SPASTIC PARAPLEGIA 48, AUTOSOMAL RECESSIVE"/>
            """,
            {
                "localKey": "613653.0001_SPASTIC PARAPLEGIA 48, AUTOSOMAL RECESSIVE",
                "title": "AP5Z1, 4-BP DEL/22-BP INS, NT80_SPASTIC PARAPLEGIA 48, AUTOSOMAL RECESSIVE",
            },
        ),
        (
            """
            <ClinVarSubmissionID localKey="GDX:2626455|Not Provided" submittedAssembly="GRCh37"/>
            """,
            {
                "localKey": "GDX:2626455|Not Provided",
                "submittedAssembly": "GRCh37",
            },
        ),
    ],
)
def test_convert_clinical_assertion_convert_clinvar_submission_id(xml_str: str, expected_json: Any):
    xmldict_value = xmltodict.parse(xml_str)
    result = ConvertClinicalAssertion.convert_clinvar_submission_id(xmldict_value)
    result_json = MessageToDict(result)
    assert result_json == expected_json


@pytest.mark.parametrize(
    "xmldict_value,expected",
    [
        ("ModeOfInheritance", ClinicalAssertion.AttributeSetElement.Type.TYPE_MODE_OF_INHERITANCE),
        ("Penetrance", ClinicalAssertion.AttributeSetElement.Type.TYPE_PENETRANCE),
        ("AgeOfOnset", ClinicalAssertion.AttributeSetElement.Type.TYPE_AGE_OF_ONSET),
        ("Severity", ClinicalAssertion.AttributeSetElement.Type.TYPE_SEVERITY),
        (
            "ClassificationHistory",
            ClinicalAssertion.AttributeSetElement.Type.TYPE_CLASSIFICATION_HISTORY,
        ),
        (
            "SeverityDescription",
            ClinicalAssertion.AttributeSetElement.Type.TYPE_SEVERITY_DESCRIPTION,
        ),
        ("AssertionMethod", ClinicalAssertion.AttributeSetElement.Type.TYPE_ASSERTION_METHOD),
    ],
)
def test_convert_observed_in_convert_attribute_set_type(
    xmldict_value: str, expected: ObservedIn.ObservedDataAttribute.Type.ValueType
):
    result = ConvertClinicalAssertion.convert_attribute_set_type(xmldict_value)
    assert result == expected


@pytest.mark.parametrize(
    "xml_str,expected_json",
    [
        (
            """
            <AttributeSet>
                <Attribute Type="ModeOfInheritance">Autosomal dominant inheritance</Attribute>
            </AttributeSet>
            """,
            {
                "attribute": {
                    "value": "Autosomal dominant inheritance",
                },
                "type": "TYPE_MODE_OF_INHERITANCE",
            },
        ),
        (
            """
            <AttributeSet>
                <Attribute Type="AssertionMethod">ACMG Guidelines, 2015</Attribute>
                <Citation>
                    <ID Source="PubMed">25741868</ID>
                </Citation>
            </AttributeSet>
            """,
            {
                "attribute": {
                    "value": "ACMG Guidelines, 2015",
                },
                "citations": [
                    {
                        "ids": [
                            {
                                "source": "PubMed",
                                "value": "25741868",
                            },
                        ],
                    },
                ],
                "type": "TYPE_ASSERTION_METHOD",
            },
        ),
    ],
)
def test_convert_clinical_assertion_convert_attribute_set(xml_str: str, expected_json: Any):
    xmldict_value = xmltodict.parse(xml_str)
    result = ConvertClinicalAssertion.convert_attribute_set(xmldict_value)
    result_json = MessageToDict(result)
    assert result_json == expected_json


@pytest.mark.parametrize(
    "xml_str,expected_json",
    [
        (
            """
            <ClinVarAccession Accession="SCV000020896" DateUpdated="2018-06-02" DateCreated="2013-04-04" Type="SCV" Version="3" SubmitterName="OMIM" OrgID="3" OrganizationCategory="resource"/>
            """,
            {
                "accession": "SCV000020896",
                "dateCreated": "2018-06-02T00:00:00Z",
                "dateUpdated": "2018-06-02T00:00:00Z",
                "submitterIdentifiers": {
                    "orgCategory": "resource",
                    "orgId": "3",
                    "submitterName": "OMIM",
                },
                "version": 3,
            },
        ),
        (
            """
            <ClinVarAccession Accession="SCV000815549" DateUpdated="2018-10-10" DateCreated="2018-10-10" Type="SCV" Version="1" SubmitterName="Invitae" OrgID="500031" OrganizationCategory="laboratory"/>
            """,
            {
                "accession": "SCV000815549",
                "dateCreated": "2018-10-10T00:00:00Z",
                "dateUpdated": "2018-10-10T00:00:00Z",
                "submitterIdentifiers": {
                    "orgCategory": "laboratory",
                    "orgId": "500031",
                    "submitterName": "Invitae",
                },
                "version": 1,
            },
        ),
    ],
)
def test_convert_clinical_assertion_convert_clinvar_accession(xml_str: str, expected_json: Any):
    xmldict_value = xmltodict.parse(xml_str)
    result = ConvertClinicalAssertion.convert_clinvar_accession(xmldict_value)
    result_json = MessageToDict(result)
    assert result_json == expected_json


@pytest.mark.parametrize(
    "xmldict_value,expected",
    [
        ("current", ClinicalAssertion.RecordStatus.RECORD_STATUS_CURRENT),
        ("removed", ClinicalAssertion.RecordStatus.RECORD_STATUS_REMOVED),
        ("replaced", ClinicalAssertion.RecordStatus.RECORD_STATUS_REPLACED),
    ],
)
def test_convert_observed_in_convert_record_status(
    xmldict_value: str, expected: ObservedIn.ObservedDataAttribute.Type.ValueType
):
    result = ConvertClinicalAssertion.convert_record_status(xmldict_value)
    assert result == expected


@pytest.mark.parametrize(
    "xml_str",
    [
        """
        <ClinicalAssertion ID="20155" SubmissionDate="2017-01-26" DateLastUpdated="2017-01-30" DateCreated="2013-04-04">
            <ClinVarSubmissionID localKey="613653.0001_SPASTIC PARAPLEGIA 48, AUTOSOMAL RECESSIVE" title="AP5Z1, 4-BP DEL/22-BP INS, NT80_SPASTIC PARAPLEGIA 48, AUTOSOMAL RECESSIVE" />
            <ClinVarAccession Accession="SCV000020155" DateUpdated="2017-01-30" DateCreated="2013-04-04" Type="SCV" Version="3" SubmitterName="OMIM" OrgID="3" OrganizationCategory="resource" />
            <RecordStatus>current</RecordStatus>
            <Classification DateLastEvaluated="2010-06-29">
                <ReviewStatus>no assertion criteria provided</ReviewStatus>
                <GermlineClassification>Pathogenic</GermlineClassification>
            </Classification>
            <Assertion>variation to disease</Assertion>
            <ObservedInList>
                <ObservedIn>
                    <Sample>
                        <Origin>germline</Origin>
                        <Species>human</Species>
                        <AffectedStatus>not provided</AffectedStatus>
                    </Sample>
                    <Method>
                        <MethodType>literature only</MethodType>
                    </Method>
                    <ObservedData>
                        <Attribute Type="Description">In 2 French</Attribute>
                        <Citation>
                            <ID Source="PubMed">20613862</ID>
                        </Citation>
                        <XRef DB="OMIM" ID="613647" Type="MIM" />
                    </ObservedData>
                </ObservedIn>
            </ObservedInList>
            <SimpleAllele>
                <GeneList>
                    <Gene Symbol="AP5Z1" />
                </GeneList>
                <Name>AP5Z1, 4-BP DEL/22-BP INS, NT80</Name>
                <VariantType>Variation</VariantType>
                <OtherNameList>
                    <Name Type="NonHGVS">4-BP DEL/22-BP INS, NT80</Name>
                </OtherNameList>
                <XRefList>
                    <XRef DB="OMIM" ID="613653.0001" Type="Allelic variant" />
                </XRefList>
            </SimpleAllele>
            <TraitSet Type="Disease">
                <Trait Type="Disease">
                    <Name>
                        <ElementValue Type="Preferred">SPASTIC PARAPLEGIA 48, AUTOSOMAL RECESSIVE</ElementValue>
                    </Name>
                </Trait>
            </TraitSet>
        </ClinicalAssertion>
        """,
        """
        <ClinicalAssertion ID="2719824" SubmissionDate="2020-02-06" DateLastUpdated="2020-07-16" DateCreated="2020-07-16">
            <ClinVarSubmissionID localKey="4926460|MedGen:C0270850;C4310756" submittedAssembly="GRCh37" />
            <ClinVarAccession Accession="SCV001385009" DateUpdated="2020-07-16" DateCreated="2020-07-16" Type="SCV" Version="1" SubmitterName="Invitae" OrgID="500031" OrganizationCategory="laboratory" />
            <RecordStatus>current</RecordStatus>
            <Classification DateLastEvaluated="2019-08-08">
                <ReviewStatus>criteria provided, single submitter</ReviewStatus>
                <GermlineClassification>Uncertain significance</GermlineClassification>
                <Citation>
                    <ID Source="PubMed">15888660</ID>
                </Citation>
                <Citation>
                    <ID Source="PubMed">14729682</ID>
                </Citation>
                <Citation>
                    <ID Source="PubMed">12891677</ID>
                </Citation>
                <Comment>This sequence change replaces...</Comment>
            </Classification>
            <Assertion>variation to disease</Assertion>
            <AttributeSet>
                <Attribute Type="AssertionMethod">Invitae Variant Classification Sherloc (09022015)</Attribute>
                <Citation>
                    <ID Source="PubMed">28492532</ID>
                </Citation>
            </AttributeSet>
            <ObservedInList>
                <ObservedIn>
                    <Sample>
                        <Origin>germline</Origin>
                        <Species TaxonomyId="9606">human</Species>
                        <AffectedStatus>unknown</AffectedStatus>
                    </Sample>
                    <Method>
                        <MethodType>clinical testing</MethodType>
                    </Method>
                    <ObservedData>
                        <Attribute Type="Description">not provided</Attribute>
                    </ObservedData>
                </ObservedIn>
            </ObservedInList>
            <SimpleAllele>
                <GeneList>
                    <Gene Symbol="CACNA1H" />
                </GeneList>
                <VariantType>Variation</VariantType>
                <AttributeSet>
                    <Attribute Type="HGVS">NM_021098.2:c.844G&gt;A</Attribute>
                </AttributeSet>
            </SimpleAllele>
            <TraitSet Type="Disease">
                <Trait Type="Disease">
                    <Name>
                        <ElementValue Type="Preferred">Idiopathic generalized epilepsy</ElementValue>
                    </Name>
                    <XRef DB="MedGen" ID="C0270850" Type="CUI" />
                </Trait>
                <Trait Type="Disease">
                    <Name>
                        <ElementValue Type="Preferred">Hyperaldosteronism, familial, type IV</ElementValue>
                    </Name>
                    <XRef DB="MedGen" ID="C4310756" Type="CUI" />
                </Trait>
            </TraitSet>
            <SubmissionNameList>
                <SubmissionName>SUB6933842</SubmissionName>
            </SubmissionNameList>
        </ClinicalAssertion>
        """,
        """
        <ClinicalAssertion ID="3860220" SubmissionDate="2021-09-21" DateLastUpdated="2021-10-08" DateCreated="2021-10-08">
            <ClinVarSubmissionID localKey=":Chr.X_38178162_38178162_A_C|not provided" submittedAssembly="GRCh37" />
            <ClinVarAccession Accession="SCV001970600" DateUpdated="2021-10-08" DateCreated="2021-10-08" Type="SCV" Version="1" SubmitterName="Clinical Genetics DNA and cytogenetics Diagnostics Lab, Erasmus MC, Erasmus Medical Center" OrgID="506497" OrganizationCategory="laboratory" OrgAbbreviation="CGDx-EMC" />
            <AdditionalSubmitters>
                <SubmitterDescription OrgID="506382" SubmitterName="Diagnostic Laboratory, Department of Genetics, University Medical Center Groningen" Type="behalf" OrganizationCategory="laboratory" />
            </AdditionalSubmitters>
            <RecordStatus>current</RecordStatus>
            <Classification>
                <ReviewStatus>no assertion criteria provided</ReviewStatus>
                <GermlineClassification>Pathogenic</GermlineClassification>
            </Classification>
            <Assertion>variation to disease</Assertion>
            <ObservedInList>
                <ObservedIn>
                    <Sample>
                        <Origin>germline</Origin>
                        <Species TaxonomyId="9606">human</Species>
                        <AffectedStatus>yes</AffectedStatus>
                    </Sample>
                    <Method>
                        <MethodType>clinical testing</MethodType>
                    </Method>
                    <ObservedData>
                        <Attribute Type="Description">not provided</Attribute>
                    </ObservedData>
                </ObservedIn>
            </ObservedInList>
            <SimpleAllele>
                <GeneList>
                    <Gene Symbol="RPGR" />
                </GeneList>
                <VariantType>Variation</VariantType>
                <Location>
                    <SequenceLocation Assembly="GRCh37" Chr="X" alternateAllele="C" referenceAllele="A" start="38178162" stop="38178162" variantLength="1" />
                </Location>
            </SimpleAllele>
            <TraitSet Type="Disease">
                <Trait Type="Disease">
                    <Name>
                        <ElementValue Type="Preferred">not provided</ElementValue>
                    </Name>
                </Trait>
            </TraitSet>
            <StudyName>VKGL Data-share Consensus</StudyName>
            <SubmissionNameList>
                <SubmissionName>SUB10405229</SubmissionName>
            </SubmissionNameList>
        </ClinicalAssertion>
        """,
        """
        <ClinicalAssertion ID="21727" SubmissionDate="2012-08-17" DateLastUpdated="2013-04-04" DateCreated="2013-04-04">
            <ClinVarSubmissionID localKey="609712.0004_PYRUVATE KINASE DEFICIENCY" title="PKLR, THR384MET_PYRUVATE KINASE DEFICIENCY" />
            <ClinVarAccession Accession="SCV000021727" DateUpdated="2013-04-04" DateCreated="2013-04-04" Type="SCV" Version="1" SubmitterName="OMIM" OrgID="3" OrganizationCategory="resource" />
            <RecordStatus>current</RecordStatus>
            <ReplacedList>
                <Replaced Accession="SCV000057029" DateChanged="2014-08-31" Version="1" />
            </ReplacedList>
            <Classification DateLastEvaluated="1991-09-15">
                <ReviewStatus>no assertion criteria provided</ReviewStatus>
                <GermlineClassification>Pathogenic</GermlineClassification>
            </Classification>
            <Assertion>variation to disease</Assertion>
            <ObservedInList>
                <ObservedIn>
                    <Sample>
                        <Origin>germline</Origin>
                        <Species>human</Species>
                        <AffectedStatus>not provided</AffectedStatus>
                    </Sample>
                    <Method>
                        <MethodType>literature only</MethodType>
                    </Method>
                    <ObservedData>
                        <Attribute Type="Description">In 2 Japanese patients, born of consanguineous parents, with hereditary hemolytic anemia due to PK Tokyo (266200), Kanno et al. (1991) identified a homozygous 1151C-T transition in the PKLR gene, resulting in a thr384-to-met (T384M) substitution in a highly conserved residue at the end of the seventh alpha-helix of the A domain. Functional expression studies showed that the mutant enzyme had decreased stability. Each parent was heterozygous for the mutation.</Attribute>
                        <Citation>
                            <ID Source="PubMed">1896471</ID>
                        </Citation>
                        <XRef DB="OMIM" ID="266200" Type="MIM" />
                    </ObservedData>
                </ObservedIn>
            </ObservedInList>
            <SimpleAllele>
                <GeneList>
                    <Gene Symbol="PKLR" />
                </GeneList>
                <Name>PKLR, THR384MET</Name>
                <VariantType>Variation</VariantType>
                <OtherNameList>
                    <Name Type="NonHGVS">THR384MET</Name>
                </OtherNameList>
                <XRefList>
                    <XRef DB="OMIM" ID="609712.0004" Type="Allelic variant" />
                </XRefList>
            </SimpleAllele>
            <TraitSet Type="Disease">
                <Trait Type="Disease">
                    <Name>
                        <ElementValue Type="Preferred">PYRUVATE KINASE DEFICIENCY</ElementValue>
                    </Name>
                </Trait>
            </TraitSet>
        </ClinicalAssertion>
        """,
    ],
    ids=[
        "id-20155",
        "id-2719824",
        "id-3860220",
        "id-21727",
    ],
)
def test_convert_clinical_assertion_xmldict_data_to_pb(xml_str: str, snapshot):
    xmldict_value = xmltodict.parse(xml_str)
    result = ConvertClinicalAssertion.xmldict_data_to_pb(xmldict_value)
    result_json = MessageToDict(result)
    snapshot.assert_match(json.dumps(result_json, indent=2), "result")


@pytest.mark.parametrize(
    "xml_str,expected_json",
    [
        (
            """
            <Gene Symbol="AP5Z1" FullName="adaptor related protein complex 5 subunit zeta 1" GeneID="9907" HGNC_ID="HGNC:22197" Source="submitted" RelationshipType="within single gene">
                <Location>
                    <CytogeneticLocation>7p22.1</CytogeneticLocation>
                    <SequenceLocation Assembly="GRCh38" AssemblyAccessionVersion="GCF_000001405.38" AssemblyStatus="current" Chr="7" Accession="NC_000007.14" start="4775623" stop="4794397" display_start="4775623" display_stop="4794397" Strand="+"/>
                    <SequenceLocation Assembly="GRCh37" AssemblyAccessionVersion="GCF_000001405.25" AssemblyStatus="previous" Chr="7" Accession="NC_000007.13" start="4815261" stop="4834025" display_start="4815261" display_stop="4834025" Strand="+"/>
                </Location>
                <OMIM>613653</OMIM>
            </Gene>
            """,
            {
                "fullName": "adaptor related protein complex 5 subunit zeta 1",
                "geneId": "9907",
                "hgncId": "HGNC:22197",
                "locations": [
                    {
                        "cytogeneticLocations": [
                            "7p22.1",
                        ],
                        "sequenceLocations": [
                            {
                                "accession": "NC_000007.14",
                                "assembly": "GRCh38",
                                "chr": "CHROMOSOME_7",
                                "displayStart": 4775623,
                                "displayStop": 4794397,
                                "start": 4775623,
                                "stop": 4794397,
                                "strand": "+",
                            },
                            {
                                "accession": "NC_000007.13",
                                "assembly": "GRCh37",
                                "chr": "CHROMOSOME_7",
                                "displayStart": 4815261,
                                "displayStop": 4834025,
                                "start": 4815261,
                                "stop": 4834025,
                                "strand": "+",
                            },
                        ],
                    },
                ],
                "omim": "613653",
                "relationshipType": "GENE_VARIANT_RELATIONSHIP_WITHIN_SINGLE_GENE",
                "source": "submitted",
            },
        ),
        (
            """
            <Gene Symbol="WDR62" FullName="WD repeat domain 62" GeneID="284403" HGNC_ID="HGNC:24502" Source="submitted" RelationshipType="within single gene">
            <Location>
                <CytogeneticLocation>19q13.12</CytogeneticLocation>
                <SequenceLocation Assembly="GRCh38" AssemblyAccessionVersion="GCF_000001405.38" AssemblyStatus="current" Chr="19" Accession="NC_000019.10" start="36054897" stop="36111145" display_start="36054897" display_stop="36111145" Strand="+"/>
                <SequenceLocation Assembly="GRCh37" AssemblyAccessionVersion="GCF_000001405.25" AssemblyStatus="previous" Chr="19" Accession="NC_000019.9" start="36545782" stop="36596011" display_start="36545782" display_stop="36596011" Strand="+"/>
            </Location>
            <OMIM>613583</OMIM>
            </Gene>
            """,
            {
                "fullName": "WD repeat domain 62",
                "geneId": "284403",
                "hgncId": "HGNC:24502",
                "locations": [
                    {
                        "cytogeneticLocations": [
                            "19q13.12",
                        ],
                        "sequenceLocations": [
                            {
                                "accession": "NC_000019.10",
                                "assembly": "GRCh38",
                                "chr": "CHROMOSOME_19",
                                "displayStart": 36054897,
                                "displayStop": 36111145,
                                "start": 36054897,
                                "stop": 36111145,
                                "strand": "+",
                            },
                            {
                                "accession": "NC_000019.9",
                                "assembly": "GRCh37",
                                "chr": "CHROMOSOME_19",
                                "displayStart": 36545782,
                                "displayStop": 36596011,
                                "start": 36545782,
                                "stop": 36596011,
                                "strand": "+",
                            },
                        ],
                    },
                ],
                "omim": "613583",
                "relationshipType": "GENE_VARIANT_RELATIONSHIP_WITHIN_SINGLE_GENE",
                "source": "submitted",
            },
        ),
    ],
)
def test_convert_allele_convert_gene(xml_str: str, expected_json: Any):
    xmldict_value = xmltodict.parse(xml_str)
    result = ConvertAllele.convert_gene(xmldict_value)
    result_json = MessageToDict(result)
    assert result_json == expected_json


@pytest.mark.parametrize(
    "xml_str,expected_json",
    [
        (
            """
            <AlleleFrequency Value="0.00001" Source="Exome Aggregation Consortium (ExAC)"/>
            """,
            {
                "source": "Exome Aggregation Consortium (ExAC)",
                "value": 1e-05,
            },
        ),
        (
            """
            <AlleleFrequency Value="0.00001" Source="Trans-Omics for Precision Medicine (TOPMed)"/>
            """,
            {
                "source": "Trans-Omics for Precision Medicine (TOPMed)",
                "value": 1e-05,
            },
        ),
    ],
)
def test_convert_allele_convert_allele_frequency(xml_str: str, expected_json: Any):
    xmldict_value = xmltodict.parse(xml_str)
    result = ConvertAllele.convert_allele_frequency(xmldict_value)
    result_json = MessageToDict(result)
    assert result_json == expected_json


@pytest.mark.parametrize(
    "xml_str,expected_json",
    [
        (
            """
             <GlobalMinorAlleleFrequency Value="0.00579" Source="1000 Genomes Project" MinorAllele="T"/>
            """,
            {
                "minorAllele": "T",
                "source": "1000 Genomes Project",
                "value": 0.00579,
            },
        ),
        (
            """
            <GlobalMinorAlleleFrequency Value="0.00160" Source="1000 Genomes Project" MinorAllele="GAGAGAG"/>
            """,
            {
                "minorAllele": "GAGAGAG",
                "source": "1000 Genomes Project",
                "value": 0.0016,
            },
        ),
    ],
)
def test_convert_allele_convert_name(xml_str: str, expected_json: Any):
    xmldict_value = xmltodict.parse(xml_str)
    result = ConvertAllele.convert_global_minor_allele_frequency(xmldict_value)
    result_json = MessageToDict(result)
    assert result_json == expected_json


@pytest.mark.parametrize(
    "xml_str,expected_json",
    [
        (
            """
             <GlobalMinorAlleleFrequency Value="0.00579" Source="1000 Genomes Project" MinorAllele="T"/>
            """,
            {
                "minorAllele": "T",
                "source": "1000 Genomes Project",
                "value": 0.00579,
            },
        ),
        (
            """
            <GlobalMinorAlleleFrequency Value="0.00160" Source="1000 Genomes Project" MinorAllele="GAGAGAG"/>
            """,
            {
                "minorAllele": "GAGAGAG",
                "source": "1000 Genomes Project",
                "value": 0.0016,
            },
        ),
    ],
)
def test_convert_allele_convert_global_minor_allele_frequency(xml_str: str, expected_json: Any):
    xmldict_value = xmltodict.parse(xml_str)
    result = ConvertAllele.convert_global_minor_allele_frequency(xmldict_value)
    result_json = MessageToDict(result)
    assert result_json == expected_json


@pytest.mark.parametrize(
    "xml_str",
    [
        """
        <SimpleAllele AlleleID="29330" VariationID="14291">
            <GeneList>
                <Gene Symbol="LAMA2" FullName="laminin subunit alpha 2" GeneID="3908" HGNC_ID="HGNC:6482" Source="submitted" RelationshipType="within single gene">
                    <Location>
                        <CytogeneticLocation>6q22.33</CytogeneticLocation>
                        <SequenceLocation Assembly="GRCh38" AssemblyAccessionVersion="GCF_000001405.38" AssemblyStatus="current" Chr="6" Accession="NC_000006.12" start="128883138" stop="129516566" display_start="128883138" display_stop="129516566" Strand="+" />
                        <SequenceLocation Assembly="GRCh37" AssemblyAccessionVersion="GCF_000001405.25" AssemblyStatus="previous" Chr="6" Accession="NC_000006.11" start="129204285" stop="129837710" display_start="129204285" display_stop="129837710" Strand="+" />
                    </Location>
                    <OMIM>156225</OMIM>
                </Gene>
            </GeneList>
            <Name>NM_000426.4(LAMA2):c.9253C&gt;T (p.Arg3085Ter)</Name>
            <CanonicalSPDI>NC_000006.12:129516230:C:T</CanonicalSPDI>
            <VariantType>single nucleotide variant</VariantType>
            <Location>
                <CytogeneticLocation>6q22.33</CytogeneticLocation>
                <SequenceLocation Assembly="GRCh38" AssemblyAccessionVersion="GCF_000001405.38" forDisplay="true" AssemblyStatus="current" Chr="6" Accession="NC_000006.12" start="129516231" stop="129516231" display_start="129516231" display_stop="129516231" variantLength="1" positionVCF="129516231" referenceAlleleVCF="C" alternateAlleleVCF="T" />
                <SequenceLocation Assembly="GRCh37" AssemblyAccessionVersion="GCF_000001405.25" AssemblyStatus="previous" Chr="6" Accession="NC_000006.11" start="129837376" stop="129837376" display_start="129837376" display_stop="129837376" variantLength="1" positionVCF="129837376" referenceAlleleVCF="C" alternateAlleleVCF="T" />
            </Location>
            <ProteinChange>R3085*</ProteinChange>
            <ProteinChange>R3081*</ProteinChange>
            <HGVSlist>
                <HGVS Type="genomic">
                    <NucleotideExpression sequenceAccessionVersion="LRG_409" sequenceAccession="LRG_409">
                        <Expression>LRG_409:g.638091C&gt;T</Expression>
                    </NucleotideExpression>
                </HGVS>
                <HGVS Type="coding">
                    <NucleotideExpression sequenceAccessionVersion="LRG_409t1" sequenceAccession="LRG_409t1">
                        <Expression>LRG_409t1:c.9253C&gt;T</Expression>
                    </NucleotideExpression>
                    <ProteinExpression sequenceAccessionVersion="LRG_409p1" sequenceAccession="LRG_409p1" change="p.Arg3085Ter">
                        <Expression>LRG_409p1:p.Arg3085Ter</Expression>
                    </ProteinExpression>
                </HGVS>
                <HGVS Assembly="GRCh37" Type="genomic, top-level">
                    <NucleotideExpression sequenceAccessionVersion="NC_000006.11" sequenceAccession="NC_000006" sequenceVersion="11" change="g.129837376C&gt;T" Assembly="GRCh37">
                        <Expression>NC_000006.11:g.129837376C&gt;T</Expression>
                    </NucleotideExpression>
                </HGVS>
                <HGVS Assembly="GRCh38" Type="genomic, top-level">
                    <NucleotideExpression sequenceAccessionVersion="NC_000006.12" sequenceAccession="NC_000006" sequenceVersion="12" change="g.129516231C&gt;T" Assembly="GRCh38">
                        <Expression>NC_000006.12:g.129516231C&gt;T</Expression>
                    </NucleotideExpression>
                </HGVS>
                <HGVS Type="genomic">
                    <NucleotideExpression sequenceAccessionVersion="NG_008678.1" sequenceAccession="NG_008678" sequenceVersion="1" change="g.638091C&gt;T">
                        <Expression>NG_008678.1:g.638091C&gt;T</Expression>
                    </NucleotideExpression>
                </HGVS>
                <HGVS Type="coding">
                    <NucleotideExpression sequenceAccessionVersion="NM_000426.4" sequenceAccession="NM_000426" sequenceVersion="4" change="c.9253C&gt;T" MANESelect="true">
                        <Expression>NM_000426.4:c.9253C&gt;T</Expression>
                    </NucleotideExpression>
                    <ProteinExpression sequenceAccessionVersion="NP_000417.3" sequenceAccession="NP_000417" sequenceVersion="3" change="p.Arg3085Ter">
                        <Expression>NP_000417.3:p.Arg3085Ter</Expression>
                    </ProteinExpression>
                    <MolecularConsequence ID="SO:0001587" Type="nonsense" DB="SO" />
                </HGVS>
                <HGVS Type="coding">
                    <NucleotideExpression sequenceAccessionVersion="NM_001079823.2" sequenceAccession="NM_001079823" sequenceVersion="2" change="c.9241C&gt;T">
                        <Expression>NM_001079823.2:c.9241C&gt;T</Expression>
                    </NucleotideExpression>
                    <ProteinExpression sequenceAccessionVersion="NP_001073291.2" sequenceAccession="NP_001073291" sequenceVersion="2" change="p.Arg3081Ter">
                        <Expression>NP_001073291.2:p.Arg3081Ter</Expression>
                    </ProteinExpression>
                    <MolecularConsequence ID="SO:0001587" Type="nonsense" DB="SO" />
                </HGVS>
            </HGVSlist>
            <Classifications>
                <GermlineClassification DateLastEvaluated="2023-12-18" DateCreated="2011-01-25" MostRecentSubmission="2024-02-11" NumberOfSubmissions="5" NumberOfSubmitters="5">
                    <ReviewStatus>criteria provided, multiple submitters, no conflicts</ReviewStatus>
                    <Description>Pathogenic/Likely pathogenic</Description>
                    <Citation Type="general">
                        <ID Source="PubMed">10022829</ID>
                    </Citation>
                    <Citation Type="general">
                        <ID Source="PubMed">10619025</ID>
                    </Citation>
                    <Citation Type="general">
                        <ID Source="PubMed">11591858</ID>
                    </Citation>
                    <Citation Type="general">
                        <ID Source="PubMed">27159402</ID>
                    </Citation>
                    <Citation Type="general">
                        <ID Source="PubMed">34777456</ID>
                    </Citation>
                    <DescriptionHistory Dated="2024-02-11">
                        <Description>Likely pathogenic</Description>
                    </DescriptionHistory>
                    <DescriptionHistory Dated="2023-01-15">
                        <Description>Uncertain significance</Description>
                    </DescriptionHistory>
                    <DescriptionHistory Dated="2018-05-29">
                        <Description>Conflicting classifications of pathogenicity</Description>
                    </DescriptionHistory>
                    <DescriptionHistory Dated="2017-12-19">
                        <Description>Pathogenic</Description>
                    </DescriptionHistory>
                    <ConditionList>
                        <TraitSet ID="9460" Type="Disease" ContributesToAggregateClassification="true">
                            <Trait ID="17556" Type="Disease">
                                <Name>
                                    <ElementValue Type="Alternate">none provided</ElementValue>
                                </Name>
                                <Name>
                                    <ElementValue Type="Preferred">not provided</ElementValue>
                                    <XRef ID="13DG0619" DB="Department Of Translational Genomics (developmental Genetics Section), King Faisal Specialist Hospital &amp; Research Centre" />
                                </Name>
                                <AttributeSet>
                                    <Attribute Type="public definition">The term 'not provided' is registered in MedGen to support identification of submissions to ClinVar for which no condition was named when assessing the variant. 'not provided' differs from 'not specified', which is used when a variant is asserted to be benign, likely benign, or of uncertain significance for conditions that have not been specified.</Attribute>
                                </AttributeSet>
                                <XRef ID="C3661900" DB="MedGen" />
                            </Trait>
                        </TraitSet>
                        <TraitSet ID="9616" Type="Disease" ContributesToAggregateClassification="true">
                            <Trait ID="16601" Type="Disease">
                                <Name>
                                    <ElementValue Type="Alternate">Laminin alpha 2-related dystrophy</ElementValue>
                                </Name>
                                <Name>
                                    <ElementValue Type="Preferred">LAMA2-related muscular dystrophy</ElementValue>
                                    <XRef ID="MONDO:0100228" DB="MONDO" />
                                </Name>
                                <Symbol>
                                    <ElementValue Type="Preferred">LAMA2-RD</ElementValue>
                                </Symbol>
                                <AttributeSet>
                                    <Attribute Type="public definition">The clinical manifestations of LAMA2 muscular dystrophy (LAMA2-MD) comprise a continuous spectrum ranging from severe congenital muscular dystrophy type 1A (MDC1A) to milder late-onset LAMA2-MD. MDC1A is typically characterized by neonatal profound hypotonia, poor spontaneous movements, and respiratory failure. Failure to thrive, gastroesophageal reflux, aspiration, and recurrent chest infections necessitating frequent hospitalizations are common. As disease progresses, facial muscle weakness, temporomandibular joint contractures, and macroglossia may further impair feeding and can affect speech. In late-onset LAMA2-MD onset of manifestations range from early childhood to adulthood. Affected individuals may show muscle hypertrophy and develop a rigid spine syndrome with joint contractures, usually most prominent in the elbows. Progressive respiratory insufficiency, scoliosis, and cardiomyopathy can occur.</Attribute>
                                    <XRef ID="NBK97333" DB="GeneReviews" />
                                </AttributeSet>
                                <Citation Type="review" Abbrev="GeneReviews">
                                    <ID Source="PubMed">22675738</ID>
                                    <ID Source="BookShelf">NBK97333</ID>
                                </Citation>
                                <XRef ID="C5679788" DB="MedGen" />
                                <XRef ID="MONDO:0100228" DB="MONDO" />
                            </Trait>
                        </TraitSet>
                        <TraitSet ID="3941" Type="Disease" ContributesToAggregateClassification="true">
                            <Trait ID="3057" Type="Disease">
                                <Name>
                                    <ElementValue Type="Alternate">Muscular dystrophy congenital, merosin negative</ElementValue>
                                </Name>
                                <Name>
                                    <ElementValue Type="Alternate">Congenital merosin-deficient muscular dystrophy 1A</ElementValue>
                                    <XRef ID="MONDO:0011925" DB="MONDO" />
                                </Name>
                                <Name>
                                    <ElementValue Type="Preferred">Merosin deficient congenital muscular dystrophy</ElementValue>
                                    <XRef ID="Muscular+dystrophy+congenital%2C+merosin+negative/4985" DB="Genetic Alliance" />
                                    <XRef ID="111503008" DB="SNOMED CT" />
                                </Name>
                                <Symbol>
                                    <ElementValue Type="Preferred">MDC1A</ElementValue>
                                    <XRef Type="MIM" ID="607855" DB="OMIM" />
                                </Symbol>
                                <AttributeSet>
                                    <Attribute Type="GARD id" integerValue="3843" />
                                    <XRef ID="3843" DB="Office of Rare Diseases" />
                                </AttributeSet>
                                <Citation Type="general" Abbrev="ISCCCMD, 2010">
                                    <ID Source="PubMed">21078917</ID>
                                </Citation>
                                <Citation Type="review" Abbrev="GeneReviews">
                                    <ID Source="PubMed">22420014</ID>
                                    <ID Source="BookShelf">NBK84550</ID>
                                </Citation>
                                <Citation Type="review" Abbrev="GeneReviews">
                                    <ID Source="PubMed">22675738</ID>
                                    <ID Source="BookShelf">NBK97333</ID>
                                </Citation>
                                <XRef ID="258" DB="Orphanet" />
                                <XRef ID="C1263858" DB="MedGen" />
                                <XRef ID="MONDO:0011925" DB="MONDO" />
                                <XRef Type="MIM" ID="607855" DB="OMIM" />
                            </Trait>
                        </TraitSet>
                    </ConditionList>
                </GermlineClassification>
            </Classifications>
            <XRefList>
                <XRef ID="CA257204" DB="ClinGen" />
                <XRef Type="Allelic variant" ID="156225.0005" DB="OMIM" />
                <XRef Type="rs" ID="121913571" DB="dbSNP" />
                <XRef Type="Interpreted" ID="424826" DB="ClinVar" />
            </XRefList>
            <AlleleFrequencyList>
                <AlleleFrequency Value="0.00000" Source="The Genome Aggregation Database (gnomAD), exomes" />
                <AlleleFrequency Value="0.00001" Source="Trans-Omics for Precision Medicine (TOPMed)" />
            </AlleleFrequencyList>
        </SimpleAllele>
        """,
    ],
    ids=[
        "id-29330",
    ],
)
def test_convert_allele_xmldict_data_to_pb(xml_str: str, snapshot):
    xmldict_value = xmltodict.parse(xml_str)
    result = ConvertAllele.xmldict_data_to_pb(xmldict_value)
    result_json = MessageToDict(result)
    snapshot.assert_match(json.dumps(result_json, indent=2), "result")


@pytest.mark.parametrize(
    "xml_str",
    [
        """
        <Haplotype VariationID="431012" NumberOfChromosomes="1">
            <SimpleAllele AlleleID="370322" VariationID="383650">
                <GeneList>
                    <Gene Symbol="COQ4" FullName="coenzyme Q4" GeneID="51117" HGNC_ID="HGNC:19693" Source="submitted" RelationshipType="within single gene">
                        <Location>
                            <CytogeneticLocation>9q34.11</CytogeneticLocation>
                            <SequenceLocation Assembly="GRCh38" AssemblyAccessionVersion="GCF_000001405.38" AssemblyStatus="current" Chr="9" Accession="NC_000009.12" start="128322839" stop="128334072" display_start="128322839" display_stop="128334072" Strand="+" />
                            <SequenceLocation Assembly="GRCh37" AssemblyAccessionVersion="GCF_000001405.25" AssemblyStatus="previous" Chr="9" Accession="NC_000009.11" start="131084790" stop="131096350" display_start="131084790" display_stop="131096350" Strand="+" />
                        </Location>
                        <OMIM>612898</OMIM>
                    </Gene>
                </GeneList>
                <Name>NM_016035.5(COQ4):c.356C&gt;T (p.Pro119Leu)</Name>
                <CanonicalSPDI>NC_000009.12:128325834:C:T</CanonicalSPDI>
                <VariantType>single nucleotide variant</VariantType>
                <Location>
                    <CytogeneticLocation>9q34.11</CytogeneticLocation>
                    <SequenceLocation Assembly="GRCh38" AssemblyAccessionVersion="GCF_000001405.38" forDisplay="true" AssemblyStatus="current" Chr="9" Accession="NC_000009.12" start="128325835" stop="128325835" display_start="128325835" display_stop="128325835" variantLength="1" positionVCF="128325835" referenceAlleleVCF="C" alternateAlleleVCF="T" />
                    <SequenceLocation Assembly="GRCh37" AssemblyAccessionVersion="GCF_000001405.25" AssemblyStatus="previous" Chr="9" Accession="NC_000009.11" start="131088114" stop="131088114" display_start="131088114" display_stop="131088114" variantLength="1" positionVCF="131088114" referenceAlleleVCF="C" alternateAlleleVCF="T" />
                </Location>
                <ProteinChange>P119L</ProteinChange>
                <ProteinChange>R87W</ProteinChange>
                <HGVSlist>
                    <HGVS Assembly="GRCh37" Type="genomic, top-level">
                        <NucleotideExpression sequenceAccessionVersion="NC_000009.11" sequenceAccession="NC_000009" sequenceVersion="11" change="g.131088114C&gt;T" Assembly="GRCh37">
                            <Expression>NC_000009.11:g.131088114C&gt;T</Expression>
                        </NucleotideExpression>
                    </HGVS>
                    <HGVS Assembly="GRCh38" Type="genomic, top-level">
                        <NucleotideExpression sequenceAccessionVersion="NC_000009.12" sequenceAccession="NC_000009" sequenceVersion="12" change="g.128325835C&gt;T" Assembly="GRCh38">
                            <Expression>NC_000009.12:g.128325835C&gt;T</Expression>
                        </NucleotideExpression>
                    </HGVS>
                    <HGVS Type="genomic">
                        <NucleotideExpression sequenceAccessionVersion="NG_042101.1" sequenceAccession="NG_042101" sequenceVersion="1" change="g.8328C&gt;T">
                            <Expression>NG_042101.1:g.8328C&gt;T</Expression>
                        </NucleotideExpression>
                    </HGVS>
                    <HGVS Type="coding">
                        <NucleotideExpression sequenceAccessionVersion="NM_001305942.2" sequenceAccession="NM_001305942" sequenceVersion="2" change="c.259C&gt;T">
                            <Expression>NM_001305942.2:c.259C&gt;T</Expression>
                        </NucleotideExpression>
                        <ProteinExpression sequenceAccessionVersion="NP_001292871.2" sequenceAccession="NP_001292871" sequenceVersion="2" change="p.Arg87Trp">
                            <Expression>NP_001292871.2:p.Arg87Trp</Expression>
                        </ProteinExpression>
                        <MolecularConsequence ID="SO:0001583" Type="missense variant" DB="SO" />
                    </HGVS>
                    <HGVS Type="coding">
                        <NucleotideExpression sequenceAccessionVersion="NM_016035.5" sequenceAccession="NM_016035" sequenceVersion="5" change="c.356C&gt;T" MANESelect="true">
                            <Expression>NM_016035.5:c.356C&gt;T</Expression>
                        </NucleotideExpression>
                        <ProteinExpression sequenceAccessionVersion="NP_057119.3" sequenceAccession="NP_057119" sequenceVersion="3" change="p.Pro119Leu">
                            <Expression>NP_057119.3:p.Pro119Leu</Expression>
                        </ProteinExpression>
                        <MolecularConsequence ID="SO:0001583" Type="missense variant" DB="SO" />
                    </HGVS>
                </HGVSlist>
                <Classifications>
                    <GermlineClassification DateLastEvaluated="2023-08-17" DateCreated="2017-03-03" MostRecentSubmission="2024-02-11" NumberOfSubmissions="2" NumberOfSubmitters="2">
                        <ReviewStatus>criteria provided, conflicting classifications</ReviewStatus>
                        <Description>Conflicting classifications of pathogenicity</Description>
                        <Explanation DataSource="ClinVar" Type="public">Likely pathogenic(1); Uncertain significance(1)</Explanation>
                        <Citation Type="general">
                            <ID Source="PubMed">28540186</ID>
                        </Citation>
                        <Comment DataSource="ClinVar" Type="public">Likely pathogenic(1); Uncertain significance(1)</Comment>
                        <DescriptionHistory Dated="2022-08-22">
                            <Description>Likely pathogenic</Description>
                        </DescriptionHistory>
                        <DescriptionHistory Dated="2022-08-07">
                            <Description>Conflicting classifications of pathogenicity</Description>
                        </DescriptionHistory>
                        <DescriptionHistory Dated="2018-10-10">
                            <Description>Likely pathogenic</Description>
                        </DescriptionHistory>
                        <ConditionList>
                            <TraitSet ID="21037" Type="Disease" ContributesToAggregateClassification="true">
                                <Trait ID="33057" Type="Disease">
                                    <Name>
                                        <ElementValue Type="Preferred">Neonatal encephalomyopathy-cardiomyopathy-respiratory distress syndrome</ElementValue>
                                        <XRef ID="MONDO:0014562" DB="MONDO" />
                                    </Name>
                                    <Name>
                                        <ElementValue Type="Alternate">Coenzyme Q10 deficiency, primary, 7</ElementValue>
                                    </Name>
                                    <Symbol>
                                        <ElementValue Type="Alternate">COQ10D7</ElementValue>
                                        <XRef Type="MIM" ID="616276" DB="OMIM" />
                                    </Symbol>
                                    <AttributeSet>
                                        <Attribute Type="GARD id" integerValue="17796" />
                                        <XRef ID="17796" DB="Office of Rare Diseases" />
                                    </AttributeSet>
                                    <AttributeSet>
                                        <Attribute Type="public definition">Primary coenzyme Q10 (CoQ10) deficiency is usually associated with multisystem involvement, including neurologic manifestations such as fatal neonatal encephalopathy with hypotonia; a late-onset slowly progressive multiple-system atrophy-like phenotype (neurodegeneration with autonomic failure and various combinations of parkinsonism and cerebellar ataxia, and pyramidal dysfunction); and dystonia, spasticity, seizures, and intellectual disability. Steroid-resistant nephrotic syndrome (SRNS), the hallmark renal manifestation, is often the initial manifestation either as isolated renal involvement that progresses to end-stage renal disease (ESRD), or associated with encephalopathy (seizures, stroke-like episodes, severe neurologic impairment) resulting in early death. Hypertrophic cardiomyopathy (HCM), retinopathy or optic atrophy, and sensorineural hearing loss can also be seen.</Attribute>
                                        <XRef ID="NBK410087" DB="GeneReviews" />
                                    </AttributeSet>
                                    <Citation Type="review" Abbrev="GeneReviews">
                                        <ID Source="PubMed">28125198</ID>
                                        <ID Source="BookShelf">NBK410087</ID>
                                    </Citation>
                                    <XRef ID="457185" DB="Orphanet" />
                                    <XRef ID="C5568562" DB="MedGen" />
                                    <XRef ID="MONDO:0014562" DB="MONDO" />
                                    <XRef Type="MIM" ID="616276" DB="OMIM" />
                                </Trait>
                            </TraitSet>
                            <TraitSet ID="9460" Type="Disease" ContributesToAggregateClassification="true">
                                <Trait ID="17556" Type="Disease">
                                    <Name>
                                        <ElementValue Type="Alternate">none provided</ElementValue>
                                    </Name>
                                    <Name>
                                        <ElementValue Type="Preferred">not provided</ElementValue>
                                        <XRef ID="13DG0619" DB="Department Of Translational Genomics (developmental Genetics Section), King Faisal Specialist Hospital &amp; Research Centre" />
                                    </Name>
                                    <AttributeSet>
                                        <Attribute Type="public definition">The term 'not provided' is registered in MedGen to support identification of submissions to ClinVar for which no condition was named when assessing the variant. 'not provided' differs from 'not specified', which is used when a variant is asserted to be benign, likely benign, or of uncertain significance for conditions that have not been specified.</Attribute>
                                    </AttributeSet>
                                    <XRef ID="C3661900" DB="MedGen" />
                                </Trait>
                            </TraitSet>
                        </ConditionList>
                    </GermlineClassification>
                </Classifications>
                <XRefList>
                    <XRef Type="Included" ID="431012" DB="ClinVar" />
                    <XRef Type="Interpreted" ID="431013" DB="ClinVar" />
                    <XRef ID="CA5260526" DB="ClinGen" />
                    <XRef Type="rs" ID="773943371" DB="dbSNP" />
                </XRefList>
                <FunctionalConsequence Value="variation affecting protein">
                    <XRef ID="0002" DB="Variation Ontology" />
                </FunctionalConsequence>
                <AlleleFrequencyList>
                    <AlleleFrequency Value="0.00001" Source="Exome Aggregation Consortium (ExAC)" />
                    <AlleleFrequency Value="0.00001" Source="The Genome Aggregation Database (gnomAD)" />
                    <AlleleFrequency Value="0.00001" Source="The Genome Aggregation Database (gnomAD), exomes" />
                    <AlleleFrequency Value="0.00004" Source="Trans-Omics for Precision Medicine (TOPMed)" />
                </AlleleFrequencyList>
            </SimpleAllele>
            <SimpleAllele AlleleID="404620" VariationID="417816">
                <GeneList>
                    <Gene Symbol="COQ4" FullName="coenzyme Q4" GeneID="51117" HGNC_ID="HGNC:19693" Source="submitted" RelationshipType="within single gene">
                        <Location>
                            <CytogeneticLocation>9q34.11</CytogeneticLocation>
                            <SequenceLocation Assembly="GRCh38" AssemblyAccessionVersion="GCF_000001405.38" AssemblyStatus="current" Chr="9" Accession="NC_000009.12" start="128322839" stop="128334072" display_start="128322839" display_stop="128334072" Strand="+" />
                            <SequenceLocation Assembly="GRCh37" AssemblyAccessionVersion="GCF_000001405.25" AssemblyStatus="previous" Chr="9" Accession="NC_000009.11" start="131084790" stop="131096350" display_start="131084790" display_stop="131096350" Strand="+" />
                        </Location>
                        <OMIM>612898</OMIM>
                    </Gene>
                </GeneList>
                <Name>NM_016035.5(COQ4):c.331G&gt;T (p.Asp111Tyr)</Name>
                <CanonicalSPDI>NC_000009.12:128325809:G:T</CanonicalSPDI>
                <VariantType>single nucleotide variant</VariantType>
                <Location>
                    <CytogeneticLocation>9q34.11</CytogeneticLocation>
                    <SequenceLocation Assembly="GRCh37" AssemblyAccessionVersion="GCF_000001405.25" AssemblyStatus="previous" Chr="9" Accession="NC_000009.11" start="131088089" stop="131088089" display_start="131088089" display_stop="131088089" variantLength="1" positionVCF="131088089" referenceAlleleVCF="G" alternateAlleleVCF="T" />
                    <SequenceLocation Assembly="GRCh38" AssemblyAccessionVersion="GCF_000001405.38" forDisplay="true" AssemblyStatus="current" Chr="9" Accession="NC_000009.12" start="128325810" stop="128325810" display_start="128325810" display_stop="128325810" variantLength="1" positionVCF="128325810" referenceAlleleVCF="G" alternateAlleleVCF="T" />
                </Location>
                <ProteinChange>D111Y</ProteinChange>
                <HGVSlist>
                    <HGVS Assembly="GRCh37" Type="genomic, top-level">
                        <NucleotideExpression sequenceAccessionVersion="NC_000009.11" sequenceAccession="NC_000009" sequenceVersion="11" change="g.131088089G&gt;T" Assembly="GRCh37">
                            <Expression>NC_000009.11:g.131088089G&gt;T</Expression>
                        </NucleotideExpression>
                    </HGVS>
                    <HGVS Assembly="GRCh38" Type="genomic, top-level">
                        <NucleotideExpression sequenceAccessionVersion="NC_000009.12" sequenceAccession="NC_000009" sequenceVersion="12" change="g.128325810G&gt;T" Assembly="GRCh38">
                            <Expression>NC_000009.12:g.128325810G&gt;T</Expression>
                        </NucleotideExpression>
                    </HGVS>
                    <HGVS Type="genomic">
                        <NucleotideExpression sequenceAccessionVersion="NG_042101.1" sequenceAccession="NG_042101" sequenceVersion="1" change="g.8303G&gt;T">
                            <Expression>NG_042101.1:g.8303G&gt;T</Expression>
                        </NucleotideExpression>
                    </HGVS>
                    <HGVS Type="coding">
                        <NucleotideExpression sequenceAccessionVersion="NM_001305942.2" sequenceAccession="NM_001305942" sequenceVersion="2" change="c.234G&gt;T">
                            <Expression>NM_001305942.2:c.234G&gt;T</Expression>
                        </NucleotideExpression>
                        <ProteinExpression sequenceAccessionVersion="NP_001292871.2" sequenceAccession="NP_001292871" sequenceVersion="2" change="p.Ser78=">
                            <Expression>NP_001292871.2:p.Ser78=</Expression>
                        </ProteinExpression>
                        <MolecularConsequence ID="SO:0001819" Type="synonymous variant" DB="SO" />
                    </HGVS>
                    <HGVS Type="coding">
                        <NucleotideExpression sequenceAccessionVersion="NM_016035.5" sequenceAccession="NM_016035" sequenceVersion="5" change="c.331G&gt;T" MANESelect="true">
                            <Expression>NM_016035.5:c.331G&gt;T</Expression>
                        </NucleotideExpression>
                        <ProteinExpression sequenceAccessionVersion="NP_057119.3" sequenceAccession="NP_057119" sequenceVersion="3" change="p.Asp111Tyr">
                            <Expression>NP_057119.3:p.Asp111Tyr</Expression>
                        </ProteinExpression>
                        <MolecularConsequence ID="SO:0001583" Type="missense variant" DB="SO" />
                    </HGVS>
                </HGVSlist>
                <Classifications>
                    <GermlineClassification NumberOfSubmissions="0" NumberOfSubmitters="0">
                        <ReviewStatus>no classification for the single variant</ReviewStatus>
                        <Description>no classification for the single variant</Description>
                    </GermlineClassification>
                    <SomaticClinicalImpact NumberOfSubmissions="0" NumberOfSubmitters="0">
                        <ReviewStatus>no classification for the single variant</ReviewStatus>
                        <Description>no classification for the single variant</Description>
                    </SomaticClinicalImpact>
                    <OncogenicityClassification NumberOfSubmissions="0" NumberOfSubmitters="0">
                        <ReviewStatus>no classification for the single variant</ReviewStatus>
                        <Description>no classification for the single variant</Description>
                    </OncogenicityClassification>
                </Classifications>
                <XRefList>
                    <XRef Type="rs" ID="530213004" DB="dbSNP" />
                    <XRef Type="Included" ID="431012" DB="ClinVar" />
                    <XRef Type="Interpreted" ID="431013" DB="ClinVar" />
                </XRefList>
                <FunctionalConsequence Value="variation affecting protein">
                    <XRef ID="0002" DB="Variation Ontology" />
                </FunctionalConsequence>
                <GlobalMinorAlleleFrequency Value="0.00020" Source="1000 Genomes Project" MinorAllele="A" />
            </SimpleAllele>
            <Name>NM_016035.4(COQ4):c.[331G&gt;T;356C&gt;T]</Name>
            <VariationType>Haplotype</VariationType>
            <HGVSlist>
                <HGVS Type="coding">
                    <NucleotideExpression>
                        <Expression>NM_016035.4(COQ4):c.[331G&gt;T;356C&gt;T]</Expression>
                    </NucleotideExpression>
                </HGVS>
            </HGVSlist>
            <Classifications>
                <GermlineClassification NumberOfSubmissions="0" NumberOfSubmitters="0">
                    <ReviewStatus>no classification for the single variant</ReviewStatus>
                    <Description>no classification for the single variant</Description>
                </GermlineClassification>
                <SomaticClinicalImpact NumberOfSubmissions="0" NumberOfSubmitters="0">
                    <ReviewStatus>no classification for the single variant</ReviewStatus>
                    <Description>no classification for the single variant</Description>
                </SomaticClinicalImpact>
                <OncogenicityClassification NumberOfSubmissions="0" NumberOfSubmitters="0">
                    <ReviewStatus>no classification for the single variant</ReviewStatus>
                    <Description>no classification for the single variant</Description>
                </OncogenicityClassification>
            </Classifications>
            <FunctionalConsequence Value="effect on catalytic protein function" />
            <XRefList>
                <XRef ID="CA645372872" DB="ClinGen" />
                <XRef Type="Interpreted" ID="431013" DB="ClinVar" />
            </XRefList>
        </Haplotype>
        """,
    ],
    ids=[
        "id-431012",
    ],
)
def test_convert_haplotype_xmldict_data_to_pb(xml_str: str, snapshot):
    xmldict_value = xmltodict.parse(xml_str)
    result = ConvertHaplotype.xmldict_data_to_pb(xmldict_value)
    result_json = MessageToDict(result)
    snapshot.assert_match(json.dumps(result_json, indent=2), "result")


@pytest.mark.parametrize(
    "xml_str,expected_json",
    [
        (
            """
            <ClassifiedVariation VariationID="998020" Accession="VCV000998020" Version="1"/>
            """,
            {
                "accession": "VCV000998020",
                "variationId": "998020",
                "version": 1,
            },
        ),
    ],
)
def test_convert_included_record_convert_global_minor_allele_frequency(
    xml_str: str, expected_json: Any
):
    xmldict_value = xmltodict.parse(xml_str)
    result = ConvertIncludedRecord.convert_classified_variation(xmldict_value)
    result_json = MessageToDict(result)
    assert result_json == expected_json


@pytest.mark.parametrize(
    "xml_str",
    [
        """
        <IncludedRecord>
            <SimpleAllele AlleleID="1054167" VariationID="1076996">
                <GeneList>
                    <Gene Symbol="TUBB" FullName="tubulin beta class I" GeneID="203068" HGNC_ID="HGNC:20778" Source="submitted" RelationshipType="within single gene">
                        <Location>
                            <CytogeneticLocation>6p21.33</CytogeneticLocation>
                            <SequenceLocation Assembly="GRCh38" AssemblyAccessionVersion="GCF_000001405.38" AssemblyStatus="current" Chr="6" Accession="NC_000006.12" start="30720352" stop="30725422" display_start="30720352" display_stop="30725422" Strand="+" />
                            <SequenceLocation Assembly="GRCh38" AssemblyAccessionVersion="GCF_000001405.38" AssemblyStatus="current" Chr="6" Accession="NT_113891.3" start="2200091" stop="2205161" display_start="2200091" display_stop="2205161" Strand="+" />
                            <SequenceLocation Assembly="GRCh38" AssemblyAccessionVersion="GCF_000001405.38" AssemblyStatus="current" Chr="6" Accession="NT_167244.2" start="2049855" stop="2054925" display_start="2049855" display_stop="2054925" Strand="+" />
                            <SequenceLocation Assembly="GRCh38" AssemblyAccessionVersion="GCF_000001405.38" AssemblyStatus="current" Chr="6" Accession="NT_167245.2" start="1976202" stop="1981272" display_start="1976202" display_stop="1981272" Strand="+" />
                            <SequenceLocation Assembly="GRCh38" AssemblyAccessionVersion="GCF_000001405.38" AssemblyStatus="current" Chr="6" Accession="NT_167246.2" start="2030603" stop="2035673" display_start="2030603" display_stop="2035673" Strand="+" />
                            <SequenceLocation Assembly="GRCh38" AssemblyAccessionVersion="GCF_000001405.38" AssemblyStatus="current" Chr="6" Accession="NT_167247.2" start="2064427" stop="2069497" display_start="2064427" display_stop="2069497" Strand="+" />
                            <SequenceLocation Assembly="GRCh38" AssemblyAccessionVersion="GCF_000001405.38" AssemblyStatus="current" Chr="6" Accession="NT_167248.2" start="1975464" stop="1980535" display_start="1975464" display_stop="1980535" Strand="+" />
                            <SequenceLocation Assembly="GRCh38" AssemblyAccessionVersion="GCF_000001405.38" AssemblyStatus="current" Chr="6" Accession="NT_167249.2" start="2021138" stop="2026208" display_start="2021138" display_stop="2026208" Strand="+" />
                            <SequenceLocation Assembly="GRCh37" AssemblyAccessionVersion="GCF_000001405.25" AssemblyStatus="previous" Chr="6" Accession="NC_000006.11" start="30688156" stop="30693198" display_start="30688156" display_stop="30693198" Strand="+" />
                        </Location>
                        <OMIM>191130</OMIM>
                    </Gene>
                </GeneList>
                <Name>NM_178014.4(TUBB):c.58-593_58-575del</Name>
                <CanonicalSPDI>NC_000006.12:30721941:CCTGGGCAACAAAGCGAGACC:CC</CanonicalSPDI>
                <VariantType>Deletion</VariantType>
                <Location>
                    <CytogeneticLocation>6p21.33</CytogeneticLocation>
                    <SequenceLocation Assembly="GRCh38" AssemblyAccessionVersion="GCF_000001405.38" forDisplay="true" AssemblyStatus="current" Chr="6" Accession="NC_000006.12" start="30721942" stop="30721960" display_start="30721942" display_stop="30721960" variantLength="19" positionVCF="30721941" referenceAlleleVCF="TCCTGGGCAACAAAGCGAGA" alternateAlleleVCF="T" />
                    <SequenceLocation Assembly="GRCh37" AssemblyAccessionVersion="GCF_000001405.25" AssemblyStatus="previous" Chr="6" Accession="NC_000006.11" start="30689719" stop="30689737" display_start="30689719" display_stop="30689737" variantLength="19" positionVCF="30689718" referenceAlleleVCF="TCCTGGGCAACAAAGCGAGA" alternateAlleleVCF="T" />
                </Location>
                <ProteinChange>G23fs</ProteinChange>
                <HGVSlist>
                    <HGVS Type="coding">
                        <NucleotideExpression sequenceAccessionVersion="NM_001293212.2" sequenceAccession="NM_001293212" sequenceVersion="2" change="c.66_84delTGGGCAACAAAGCGAGACC">
                            <Expression>NM_001293212.2:c.66_84delTGGGCAACAAAGCGAGACC</Expression>
                        </NucleotideExpression>
                    </HGVS>
                    <HGVS Assembly="GRCh37" Type="genomic, top-level">
                        <NucleotideExpression sequenceAccessionVersion="NC_000006.11" sequenceAccession="NC_000006" sequenceVersion="11" change="g.30689721_30689739del" Assembly="GRCh37">
                            <Expression>NC_000006.11:g.30689721_30689739del</Expression>
                        </NucleotideExpression>
                    </HGVS>
                    <HGVS Assembly="GRCh38" Type="genomic, top-level">
                        <NucleotideExpression sequenceAccessionVersion="NC_000006.12" sequenceAccession="NC_000006" sequenceVersion="12" change="g.30721944_30721962del" Assembly="GRCh38">
                            <Expression>NC_000006.12:g.30721944_30721962del</Expression>
                        </NucleotideExpression>
                    </HGVS>
                    <HGVS Type="genomic">
                        <NucleotideExpression sequenceAccessionVersion="NG_034142.1" sequenceAccession="NG_034142" sequenceVersion="1" change="g.6744_6762del">
                            <Expression>NG_034142.1:g.6744_6762del</Expression>
                        </NucleotideExpression>
                    </HGVS>
                    <HGVS Type="coding">
                        <NucleotideExpression sequenceAccessionVersion="NM_001293212.2" sequenceAccession="NM_001293212" sequenceVersion="2" change="c.66_84del">
                            <Expression>NM_001293212.2:c.66_84del</Expression>
                        </NucleotideExpression>
                        <ProteinExpression sequenceAccessionVersion="NP_001280141.1" sequenceAccession="NP_001280141" sequenceVersion="1" change="p.Gly23fs">
                            <Expression>NP_001280141.1:p.Gly23fs</Expression>
                        </ProteinExpression>
                        <MolecularConsequence ID="SO:0001589" Type="frameshift variant" DB="SO" />
                    </HGVS>
                    <HGVS Type="coding">
                        <NucleotideExpression sequenceAccessionVersion="NM_178014.4" sequenceAccession="NM_178014" sequenceVersion="4" change="c.58-593_58-575del" MANESelect="true">
                            <Expression>NM_178014.4:c.58-593_58-575del</Expression>
                        </NucleotideExpression>
                        <MolecularConsequence ID="SO:0001627" Type="intron variant" DB="SO" />
                    </HGVS>
                    <HGVS Type="coding">
                        <NucleotideExpression sequenceAccessionVersion="NM_001293213.2" sequenceAccession="NM_001293213" sequenceVersion="2" change="c.58-593_58-575del">
                            <Expression>NM_001293213.2:c.58-593_58-575del</Expression>
                        </NucleotideExpression>
                        <MolecularConsequence ID="SO:0001627" Type="intron variant" DB="SO" />
                    </HGVS>
                    <HGVS Type="coding">
                        <NucleotideExpression sequenceAccessionVersion="NM_001293214.2" sequenceAccession="NM_001293214" sequenceVersion="2" change="c.35-974_35-956del">
                            <Expression>NM_001293214.2:c.35-974_35-956del</Expression>
                        </NucleotideExpression>
                        <MolecularConsequence ID="SO:0001627" Type="intron variant" DB="SO" />
                    </HGVS>
                    <HGVS Type="coding">
                        <NucleotideExpression sequenceAccessionVersion="NM_001293215.2" sequenceAccession="NM_001293215" sequenceVersion="2" change="c.-160+46_-160+64del">
                            <Expression>NM_001293215.2:c.-160+46_-160+64del</Expression>
                        </NucleotideExpression>
                        <MolecularConsequence ID="SO:0001627" Type="intron variant" DB="SO" />
                    </HGVS>
                    <HGVS Type="coding">
                        <NucleotideExpression sequenceAccessionVersion="NM_001293216.2" sequenceAccession="NM_001293216" sequenceVersion="2" change="c.-160+147_-160+165del">
                            <Expression>NM_001293216.2:c.-160+147_-160+165del</Expression>
                        </NucleotideExpression>
                        <MolecularConsequence ID="SO:0001627" Type="intron variant" DB="SO" />
                    </HGVS>
                </HGVSlist>
                <XRefList>
                    <XRef Type="Interpreted" ID="1065830" DB="ClinVar" />
                    <XRef Type="rs" ID="2127746598" DB="dbSNP" />
                </XRefList>
            </SimpleAllele>
            <Classifications>
                <GermlineClassification NumberOfSubmissions="0" NumberOfSubmitters="0">
                    <ReviewStatus>no classification for the single variant</ReviewStatus>
                    <Description>no classification for the single variant</Description>
                </GermlineClassification>
                <SomaticClinicalImpact NumberOfSubmissions="0" NumberOfSubmitters="0">
                    <ReviewStatus>no classification for the single variant</ReviewStatus>
                    <Description>no classification for the single variant</Description>
                </SomaticClinicalImpact>
                <OncogenicityClassification NumberOfSubmissions="0" NumberOfSubmitters="0">
                    <ReviewStatus>no classification for the single variant</ReviewStatus>
                    <Description>no classification for the single variant</Description>
                </OncogenicityClassification>
            </Classifications>
            <SubmittedClassificationList>
                <SCV Accession="SCV001573784" Version="2" />
            </SubmittedClassificationList>
            <ClassifiedVariationList>
                <ClassifiedVariation VariationID="1065830" Accession="VCV001065830" Version="2" />
            </ClassifiedVariationList>
        </IncludedRecord>
        """,
    ],
    ids=[
        "id-1054167",
    ],
)
def test_convert_included_record_xmldict_data_to_pb(xml_str: str, snapshot):
    xmldict_value = xmltodict.parse(xml_str)
    result = ConvertIncludedRecord.xmldict_data_to_pb(xmldict_value)
    result_json = MessageToDict(result)
    snapshot.assert_match(json.dumps(result_json, indent=2), "result")


@pytest.mark.parametrize(
    "xml_str",
    [
        """
        <Genotype VariationID="444003">
            <SimpleAllele AlleleID="437664" VariationID="444001">
                <GeneList>
                    <Gene Symbol="TUBGCP6" FullName="tubulin gamma complex component 6" GeneID="85378" HGNC_ID="HGNC:18127" Source="submitted" RelationshipType="within single gene">
                        <Location>
                            <CytogeneticLocation>22q13.33</CytogeneticLocation>
                            <SequenceLocation Assembly="GRCh38" AssemblyAccessionVersion="GCF_000001405.38" AssemblyStatus="current" Chr="22" Accession="NC_000022.11" start="50217694" stop="50245023" display_start="50217694" display_stop="50245023" Strand="-" />
                            <SequenceLocation Assembly="GRCh37" AssemblyAccessionVersion="GCF_000001405.25" AssemblyStatus="previous" Chr="22" Accession="NC_000022.10" start="50656117" stop="50683399" display_start="50656117" display_stop="50683399" Strand="-" />
                        </Location>
                        <OMIM>610053</OMIM>
                    </Gene>
                </GeneList>
                <Name>NM_020461.4(TUBGCP6):c.3139C&gt;T (p.Arg1047Trp)</Name>
                <CanonicalSPDI>NC_000022.11:50221219:G:A</CanonicalSPDI>
                <VariantType>single nucleotide variant</VariantType>
                <Location>
                    <CytogeneticLocation>22q13.33</CytogeneticLocation>
                    <SequenceLocation Assembly="GRCh38" AssemblyAccessionVersion="GCF_000001405.38" forDisplay="true" AssemblyStatus="current" Chr="22" Accession="NC_000022.11" start="50221220" stop="50221220" display_start="50221220" display_stop="50221220" variantLength="1" positionVCF="50221220" referenceAlleleVCF="G" alternateAlleleVCF="A" />
                    <SequenceLocation Assembly="GRCh37" AssemblyAccessionVersion="GCF_000001405.25" AssemblyStatus="previous" Chr="22" Accession="NC_000022.10" start="50659649" stop="50659649" display_start="50659649" display_stop="50659649" variantLength="1" positionVCF="50659649" referenceAlleleVCF="G" alternateAlleleVCF="A" />
                </Location>
                <ProteinChange>R1047W</ProteinChange>
                <HGVSlist>
                    <HGVS Assembly="GRCh37" Type="genomic, top-level">
                        <NucleotideExpression sequenceAccessionVersion="NC_000022.10" sequenceAccession="NC_000022" sequenceVersion="10" change="g.50659649G&gt;A" Assembly="GRCh37">
                            <Expression>NC_000022.10:g.50659649G&gt;A</Expression>
                        </NucleotideExpression>
                    </HGVS>
                    <HGVS Assembly="GRCh38" Type="genomic, top-level">
                        <NucleotideExpression sequenceAccessionVersion="NC_000022.11" sequenceAccession="NC_000022" sequenceVersion="11" change="g.50221220G&gt;A" Assembly="GRCh38">
                            <Expression>NC_000022.11:g.50221220G&gt;A</Expression>
                        </NucleotideExpression>
                    </HGVS>
                    <HGVS Type="genomic">
                        <NucleotideExpression sequenceAccessionVersion="NG_032160.1" sequenceAccession="NG_032160" sequenceVersion="1" change="g.28752C&gt;T">
                            <Expression>NG_032160.1:g.28752C&gt;T</Expression>
                        </NucleotideExpression>
                    </HGVS>
                    <HGVS Type="coding">
                        <NucleotideExpression sequenceAccessionVersion="NM_020461.4" sequenceAccession="NM_020461" sequenceVersion="4" change="c.3139C&gt;T" MANESelect="true">
                            <Expression>NM_020461.4:c.3139C&gt;T</Expression>
                        </NucleotideExpression>
                        <ProteinExpression sequenceAccessionVersion="NP_065194.3" sequenceAccession="NP_065194" sequenceVersion="3" change="p.Arg1047Trp">
                            <Expression>NP_065194.3:p.Arg1047Trp</Expression>
                        </ProteinExpression>
                        <MolecularConsequence ID="SO:0001583" Type="missense variant" DB="SO" />
                    </HGVS>
                </HGVSlist>
                <Classifications>
                    <GermlineClassification DateLastEvaluated="2023-08-04" DateCreated="2020-07-13" MostRecentSubmission="2024-02-11" NumberOfSubmissions="1" NumberOfSubmitters="1">
                        <ReviewStatus>criteria provided, single submitter</ReviewStatus>
                        <Description>Uncertain significance</Description>
                        <Citation Type="general">
                            <ID Source="PubMed">31069529</ID>
                        </Citation>
                        <DescriptionHistory Dated="2020-07-15">
                            <Description>no classification for the single variant</Description>
                        </DescriptionHistory>
                        <ConditionList>
                            <TraitSet ID="9460" Type="Disease" ContributesToAggregateClassification="true">
                                <Trait ID="17556" Type="Disease">
                                    <Name>
                                        <ElementValue Type="Alternate">none provided</ElementValue>
                                    </Name>
                                    <Name>
                                        <ElementValue Type="Preferred">not provided</ElementValue>
                                        <XRef ID="13DG0619" DB="Department Of Translational Genomics (developmental Genetics Section), King Faisal Specialist Hospital &amp; Research Centre" />
                                    </Name>
                                    <AttributeSet>
                                        <Attribute Type="public definition">The term 'not provided' is registered in MedGen to support identification of submissions to ClinVar for which no condition was named when assessing the variant. 'not provided' differs from 'not specified', which is used when a variant is asserted to be benign, likely benign, or of uncertain significance for conditions that have not been specified.</Attribute>
                                    </AttributeSet>
                                    <XRef ID="C3661900" DB="MedGen" />
                                </Trait>
                            </TraitSet>
                        </ConditionList>
                    </GermlineClassification>
                </Classifications>
                <XRefList>
                    <XRef ID="CA10308045" DB="ClinGen" />
                    <XRef Type="rs" ID="538652140" DB="dbSNP" />
                    <XRef Type="Interpreted" ID="444003" DB="ClinVar" />
                </XRefList>
                <AlleleFrequencyList>
                    <AlleleFrequency Value="0.00003" Source="The Genome Aggregation Database (gnomAD)" />
                    <AlleleFrequency Value="0.00012" Source="The Genome Aggregation Database (gnomAD), exomes" />
                    <AlleleFrequency Value="0.00016" Source="1000 Genomes Project 30x" />
                    <AlleleFrequency Value="0.00020" Source="1000 Genomes Project" />
                </AlleleFrequencyList>
                <GlobalMinorAlleleFrequency Value="0.00020" Source="1000 Genomes Project" MinorAllele="A" />
            </SimpleAllele>
            <SimpleAllele AlleleID="437663" VariationID="444002">
                <GeneList>
                    <Gene Symbol="TUBGCP6" FullName="tubulin gamma complex component 6" GeneID="85378" HGNC_ID="HGNC:18127" Source="submitted" RelationshipType="within single gene">
                        <Location>
                            <CytogeneticLocation>22q13.33</CytogeneticLocation>
                            <SequenceLocation Assembly="GRCh38" AssemblyAccessionVersion="GCF_000001405.38" AssemblyStatus="current" Chr="22" Accession="NC_000022.11" start="50217694" stop="50245023" display_start="50217694" display_stop="50245023" Strand="-" />
                            <SequenceLocation Assembly="GRCh37" AssemblyAccessionVersion="GCF_000001405.25" AssemblyStatus="previous" Chr="22" Accession="NC_000022.10" start="50656117" stop="50683399" display_start="50656117" display_stop="50683399" Strand="-" />
                        </Location>
                        <OMIM>610053</OMIM>
                    </Gene>
                </GeneList>
                <Name>NM_020461.4(TUBGCP6):c.5140G&gt;A (p.Ala1714Thr)</Name>
                <CanonicalSPDI>NC_000022.11:50218216:C:T</CanonicalSPDI>
                <VariantType>single nucleotide variant</VariantType>
                <Location>
                    <CytogeneticLocation>22q13.33</CytogeneticLocation>
                    <SequenceLocation Assembly="GRCh38" AssemblyAccessionVersion="GCF_000001405.38" forDisplay="true" AssemblyStatus="current" Chr="22" Accession="NC_000022.11" start="50218217" stop="50218217" display_start="50218217" display_stop="50218217" variantLength="1" positionVCF="50218217" referenceAlleleVCF="C" alternateAlleleVCF="T" />
                    <SequenceLocation Assembly="GRCh37" AssemblyAccessionVersion="GCF_000001405.25" AssemblyStatus="previous" Chr="22" Accession="NC_000022.10" start="50656646" stop="50656646" display_start="50656646" display_stop="50656646" variantLength="1" positionVCF="50656646" referenceAlleleVCF="C" alternateAlleleVCF="T" />
                </Location>
                <ProteinChange>A1714T</ProteinChange>
                <HGVSlist>
                    <HGVS Assembly="GRCh37" Type="genomic, top-level">
                        <NucleotideExpression sequenceAccessionVersion="NC_000022.10" sequenceAccession="NC_000022" sequenceVersion="10" change="g.50656646C&gt;T" Assembly="GRCh37">
                            <Expression>NC_000022.10:g.50656646C&gt;T</Expression>
                        </NucleotideExpression>
                    </HGVS>
                    <HGVS Assembly="GRCh38" Type="genomic, top-level">
                        <NucleotideExpression sequenceAccessionVersion="NC_000022.11" sequenceAccession="NC_000022" sequenceVersion="11" change="g.50218217C&gt;T" Assembly="GRCh38">
                            <Expression>NC_000022.11:g.50218217C&gt;T</Expression>
                        </NucleotideExpression>
                    </HGVS>
                    <HGVS Type="genomic">
                        <NucleotideExpression sequenceAccessionVersion="NG_032160.1" sequenceAccession="NG_032160" sequenceVersion="1" change="g.31755G&gt;A">
                            <Expression>NG_032160.1:g.31755G&gt;A</Expression>
                        </NucleotideExpression>
                    </HGVS>
                    <HGVS Type="coding">
                        <NucleotideExpression sequenceAccessionVersion="NM_020461.4" sequenceAccession="NM_020461" sequenceVersion="4" change="c.5140G&gt;A" MANESelect="true">
                            <Expression>NM_020461.4:c.5140G&gt;A</Expression>
                        </NucleotideExpression>
                        <ProteinExpression sequenceAccessionVersion="NP_065194.3" sequenceAccession="NP_065194" sequenceVersion="3" change="p.Ala1714Thr">
                            <Expression>NP_065194.3:p.Ala1714Thr</Expression>
                        </ProteinExpression>
                        <MolecularConsequence ID="SO:0001583" Type="missense variant" DB="SO" />
                    </HGVS>
                </HGVSlist>
                <Classifications>
                    <GermlineClassification DateLastEvaluated="2023-09-21" DateCreated="2022-03-24" MostRecentSubmission="2024-02-25" NumberOfSubmissions="1" NumberOfSubmitters="1">
                        <ReviewStatus>criteria provided, single submitter</ReviewStatus>
                        <Description>Uncertain significance</Description>
                        <Citation Type="general">
                            <ID Source="PubMed">31069529</ID>
                        </Citation>
                        <DescriptionHistory Dated="2022-03-25">
                            <Description>no classification for the single variant</Description>
                        </DescriptionHistory>
                        <ConditionList>
                            <TraitSet ID="9460" Type="Disease" ContributesToAggregateClassification="true">
                                <Trait ID="17556" Type="Disease">
                                    <Name>
                                        <ElementValue Type="Alternate">none provided</ElementValue>
                                    </Name>
                                    <Name>
                                        <ElementValue Type="Preferred">not provided</ElementValue>
                                        <XRef ID="13DG0619" DB="Department Of Translational Genomics (developmental Genetics Section), King Faisal Specialist Hospital &amp; Research Centre" />
                                    </Name>
                                    <AttributeSet>
                                        <Attribute Type="public definition">The term 'not provided' is registered in MedGen to support identification of submissions to ClinVar for which no condition was named when assessing the variant. 'not provided' differs from 'not specified', which is used when a variant is asserted to be benign, likely benign, or of uncertain significance for conditions that have not been specified.</Attribute>
                                    </AttributeSet>
                                    <XRef ID="C3661900" DB="MedGen" />
                                </Trait>
                            </TraitSet>
                        </ConditionList>
                    </GermlineClassification>
                </Classifications>
                <XRefList>
                    <XRef ID="CA10307162" DB="ClinGen" />
                    <XRef Type="rs" ID="748135189" DB="dbSNP" />
                    <XRef Type="Interpreted" ID="444003" DB="ClinVar" />
                </XRefList>
                <AlleleFrequencyList>
                    <AlleleFrequency Value="0.00001" Source="Trans-Omics for Precision Medicine (TOPMed)" />
                    <AlleleFrequency Value="0.00003" Source="The Genome Aggregation Database (gnomAD)" />
                    <AlleleFrequency Value="0.00006" Source="The Genome Aggregation Database (gnomAD), exomes" />
                    <AlleleFrequency Value="0.00008" Source="Exome Aggregation Consortium (ExAC)" />
                </AlleleFrequencyList>
            </SimpleAllele>
            <Name>NM_020461.3(TUBGCP6):c.[3139C&gt;T];[5140G&gt;A]</Name>
            <VariationType>CompoundHeterozygote</VariationType>
            <HGVSlist>
                <HGVS Type="coding">
                    <NucleotideExpression>
                        <Expression>NM_020461.3:c.[3139C&gt;T];[5140G&gt;A]</Expression>
                    </NucleotideExpression>
                </HGVS>
            </HGVSlist>
        </Genotype>
        """,
    ],
    ids=[
        "id-444003",
    ],
)
def test_convert_genotype_xmldict_data_to_pb(xml_str: str, snapshot):
    xmldict_value = xmltodict.parse(xml_str)
    result = ConvertGenotype.xmldict_data_to_pb(xmldict_value)
    result_json = MessageToDict(result)
    snapshot.assert_match(json.dumps(result_json, indent=2), "result")


@pytest.mark.parametrize(
    "xml_str,expected_json",
    [
        (
            """
            <ClassifiedConditionList TraitSetID="2">
                <ClassifiedCondition DB="MedGen" ID="C3150901">Hereditary spastic paraplegia 48</ClassifiedCondition>
            </ClassifiedConditionList>
            """,
            {
                "classifiedConditions": [
                    {
                        "db": "MedGen",
                        "id": "C3150901",
                        "value": "Hereditary spastic paraplegia 48",
                    },
                ],
                "traitSetId": "2",
            },
        ),
    ],
)
def test_convert_cv_accession_convert_classified_condition_list(xml_str: str, expected_json: Any):
    xmldict_value = xmltodict.parse(xml_str)
    result = ConvertRcvAccession.convert_classified_condition_list(xmldict_value)
    result_json = MessageToDict(result)
    assert result_json == expected_json


@pytest.mark.parametrize(
    "xml_str,expected_json",
    [
        (
            """
            <Description SubmissionCount="2">Pathogenic</Description>
            """,
            {
                "submissionCount": 2,
                "value": "Pathogenic",
            },
        ),
        (
            """
            <Description DateLastEvaluated="2010-10-01" SubmissionCount="1">Pathogenic</Description>
            """,
            {
                "dateLastEvaluated": "2010-10-01T00:00:00Z",
                "submissionCount": 1,
                "value": "Pathogenic",
            },
        ),
    ],
)
def test_convert_cv_accession_convert_germline_classification_description(
    xml_str: str, expected_json: Any
):
    xmldict_value = xmltodict.parse(xml_str)
    result = ConvertRcvAccession.convert_germline_classification_description(xmldict_value)
    result_json = MessageToDict(result)
    assert result_json == expected_json


@pytest.mark.parametrize(
    "xml_str,expected_json",
    [
        (
            """
            <GermlineClassification>
                <ReviewStatus>no assertion criteria provided</ReviewStatus>
                <Description DateLastEvaluated="2010-10-01" SubmissionCount="1">Pathogenic</Description>
            </GermlineClassification>
            """,
            {
                "description": {
                    "dateLastEvaluated": "2010-10-01T00:00:00Z",
                    "submissionCount": 1,
                    "value": "Pathogenic",
                },
                "reviewStatus": "AGGREGATE_GERMLINE_REVIEW_STATUS_NO_ASSERTION_CRITERIA_PROVIDED",
            },
        ),
    ],
)
def test_convert_cv_accession_convert_germline_classification(xml_str: str, expected_json: Any):
    xmldict_value = xmltodict.parse(xml_str)
    result = ConvertRcvAccession.convert_germline_classification(xmldict_value)
    result_json = MessageToDict(result)
    assert result_json == expected_json


@pytest.mark.parametrize(
    "xml_str,expected_json",
    [
        (
            """
            <Description ClinicalImpactAssertionType="prognostic" ClinicalImpactClinicalSignificance="poor outcome" DateLastEvaluated="2024-01-24" SubmissionCount="1">Tier I - Strong</Description>
            """,
            {
                "clinicalImpactAssertionType": "prognostic",
                "clinicalImpactClinicalSignificance": "poor outcome",
                "dateLastEvaluated": "2024-01-24T00:00:00Z",
                "submissionCount": 1,
                "value": "Tier I - Strong",
            },
        ),
        (
            """
            <Description>no classification for the single variant</Description>
            """,
            {
                "value": "no classification for the single variant",
            },
        ),
    ],
)
def test_convert_cv_accession_convert_somatic_clinical_impact_description(
    xml_str: str, expected_json: Any
):
    xmldict_value = xmltodict.parse(xml_str)
    result = ConvertRcvAccession.convert_somatic_clinical_impact_description(xmldict_value)
    result_json = MessageToDict(result)
    assert result_json == expected_json


@pytest.mark.parametrize(
    "xml_str,expected_json",
    [
        (
            """
            <SomaticClinicalImpact>
                <ReviewStatus>no assertion criteria provided</ReviewStatus>
                <Description ClinicalImpactAssertionType="prognostic" ClinicalImpactClinicalSignificance="poor outcome" DateLastEvaluated="2024-01-24" SubmissionCount="1">Tier I - Strong</Description>
            </SomaticClinicalImpact>
            """,
            {
                "description": {
                    "clinicalImpactAssertionType": "prognostic",
                    "clinicalImpactClinicalSignificance": "poor outcome",
                    "dateLastEvaluated": "2024-01-24T00:00:00Z",
                    "submissionCount": 1,
                    "value": "Tier I - Strong",
                },
                "reviewStatus": "AGGREGATE_SOMATIC_CLINICAL_IMPACT_REVIEW_STATUS_NO_ASSERTION_CRITERIA_PROVIDED",
            },
        ),
        (
            """
            <SomaticClinicalImpact>
                <ReviewStatus>no classification for the single variant</ReviewStatus>
                <Description>no classification for the single variant</Description>
            </SomaticClinicalImpact>
            """,
            {
                "description": {
                    "value": "no classification for the single variant",
                },
                "reviewStatus": "AGGREGATE_SOMATIC_CLINICAL_IMPACT_REVIEW_STATUS_NO_CLASSIFICATION_FOR_THE_SINGLE_VARIANT",
            },
        ),
    ],
)
def test_convert_cv_accession_convert_somatic_clinical_impact(xml_str: str, expected_json: Any):
    xmldict_value = xmltodict.parse(xml_str)
    result = ConvertRcvAccession.convert_somatic_clinical_impact(xmldict_value)
    result_json = MessageToDict(result)
    assert result_json == expected_json


@pytest.mark.parametrize(
    "xml_str,expected_json",
    [
        (
            """
            <Description DateLastEvaluated="2024-01-24" SubmissionCount="1">Uncertain significance</Description>
            """,
            {
                "dateLastEvaluated": "2024-01-24T00:00:00Z",
                "submissionCount": 1,
                "value": "Uncertain significance",
            },
        ),
        (
            """
            <Description>no classification for the single variant</Description>
            """,
            {
                "value": "no classification for the single variant",
            },
        ),
    ],
)
def test_convert_cv_accession_convert_oncogenicity_classification_description(
    xml_str: str, expected_json: Any
):
    xmldict_value = xmltodict.parse(xml_str)
    result = ConvertRcvAccession.convert_oncogenicity_classification_description(xmldict_value)
    result_json = MessageToDict(result)
    assert result_json == expected_json


@pytest.mark.parametrize(
    "xml_str,expected_json",
    [
        (
            """
            <OncogenicityClassification>
                <ReviewStatus>no classification for the single variant</ReviewStatus>
                <Description DateLastEvaluated="2024-01-24" SubmissionCount="1">Uncertain significance</Description>
            </OncogenicityClassification>
            """,
            {
                "description": {
                    "dateLastEvaluated": "2024-01-24T00:00:00Z",
                    "submissionCount": 1,
                    "value": "Uncertain significance",
                },
                "reviewStatus": "AGGREGATE_ONCOGENICITY_REVIEW_STATUS_NO_CLASSIFICATION_FOR_THE_SINGLE_VARIANT",
            },
        ),
        (
            """
            <OncogenicityClassification>
                <ReviewStatus>no classification for the single variant</ReviewStatus>
                <Description>no classification for the single variant</Description>
            </OncogenicityClassification>
            """,
            {
                "description": {
                    "value": "no classification for the single variant",
                },
                "reviewStatus": "AGGREGATE_ONCOGENICITY_REVIEW_STATUS_NO_CLASSIFICATION_FOR_THE_SINGLE_VARIANT",
            },
        ),
    ],
)
def test_convert_cv_accession_convert_oncogenicity_classification(xml_str: str, expected_json: Any):
    xmldict_value = xmltodict.parse(xml_str)
    result = ConvertRcvAccession.convert_oncogenicity_classification(xmldict_value)
    result_json = MessageToDict(result)
    assert result_json == expected_json


@pytest.mark.parametrize(
    "xml_str,expected_json",
    [
        (
            """
            <RCVClassifications>
                <GermlineClassification>
                    <ReviewStatus>no assertion criteria provided</ReviewStatus>
                    <Description DateLastEvaluated="1997-02-24" SubmissionCount="1">Pathogenic</Description>
                </GermlineClassification>
            </RCVClassifications>
            """,
            {
                "germlineClassification": {
                    "description": {
                        "dateLastEvaluated": "1997-02-24T00:00:00Z",
                        "submissionCount": 1,
                        "value": "Pathogenic",
                    },
                    "reviewStatus": "AGGREGATE_GERMLINE_REVIEW_STATUS_NO_ASSERTION_CRITERIA_PROVIDED",
                },
            },
        ),
        (
            """
            <RCVClassifications>
                <SomaticClinicalImpact>
                    <ReviewStatus>no assertion criteria provided</ReviewStatus>
                    <Description ClinicalImpactAssertionType="prognostic" ClinicalImpactClinicalSignificance="poor outcome" DateLastEvaluated="2024-01-24" SubmissionCount="1">Tier I - Strong</Description>
                </SomaticClinicalImpact>
            </RCVClassifications>
            """,
            {
                "somaticClinicalImpact": {
                    "description": {
                        "clinicalImpactAssertionType": "prognostic",
                        "clinicalImpactClinicalSignificance": "poor outcome",
                        "dateLastEvaluated": "2024-01-24T00:00:00Z",
                        "submissionCount": 1,
                        "value": "Tier I - Strong",
                    },
                    "reviewStatus": "AGGREGATE_SOMATIC_CLINICAL_IMPACT_REVIEW_STATUS_NO_ASSERTION_CRITERIA_PROVIDED",
                },
            },
        ),
    ],
)
def test_convert_cv_accession_convert_rcv_classifications(xml_str: str, expected_json: Any):
    xmldict_value = xmltodict.parse(xml_str)
    result = ConvertRcvAccession.convert_rcv_classifications(xmldict_value)
    result_json = MessageToDict(result)
    assert result_json == expected_json


@pytest.mark.parametrize(
    "xml_str,expected_json",
    [
        (
            """
            <RCVAccession Title="NM_014855.3(AP5Z1):c.80_83delinsTGCTGTAAACTGTAACTGTAAA (p.Arg27_Ile28delinsLeuLeuTer) AND Hereditary spastic paraplegia 48" Accession="RCV000000012" Version="5">
                <ClassifiedConditionList TraitSetID="2">
                    <ClassifiedCondition DB="MedGen" ID="C3150901">Hereditary spastic paraplegia 48</ClassifiedCondition>
                </ClassifiedConditionList>
                <RCVClassifications>
                    <GermlineClassification>
                        <ReviewStatus>criteria provided, single submitter</ReviewStatus>
                        <Description SubmissionCount="2">Pathogenic</Description>
                    </GermlineClassification>
                </RCVClassifications>
            </RCVAccession>
            """,
            {
                "accession": "RCV000000012",
                "classifiedConditionList": {
                    "classifiedConditions": [
                        {
                            "db": "MedGen",
                            "id": "C3150901",
                            "value": "Hereditary spastic paraplegia 48",
                        },
                    ],
                    "traitSetId": "2",
                },
                "rcvClassifications": {
                    "germlineClassification": {
                        "description": {
                            "submissionCount": 2,
                            "value": "Pathogenic",
                        },
                        "reviewStatus": "AGGREGATE_GERMLINE_REVIEW_STATUS_CRITERIA_PROVIDED_SINGLE_SUBMITTER",
                    },
                },
                "title": "NM_014855.3(AP5Z1):c.80_83delinsTGCTGTAAACTGTAACTGTAAA "
                "(p.Arg27_Ile28delinsLeuLeuTer) AND Hereditary spastic paraplegia 48",
                "version": 5,
            },
        ),
        (
            """
            <RCVAccession Title="NM_000353.3(TAT):c.[1085G&gt;T;912+2T&gt;G] AND Tyrosinemia type II" Accession="RCV000000432" Version="4">
                <ClassifiedConditionList TraitSetID="110">
                    <ClassifiedCondition DB="MedGen" ID="C0268487">Tyrosinemia type II</ClassifiedCondition>
                </ClassifiedConditionList>
                <RCVClassifications>
                    <GermlineClassification>
                        <ReviewStatus>no assertion criteria provided</ReviewStatus>
                        <Description DateLastEvaluated="1992-10-01" SubmissionCount="1">Pathogenic</Description>
                    </GermlineClassification>
                </RCVClassifications>
            </RCVAccession>
            """,
            {
                "accession": "RCV000000432",
                "classifiedConditionList": {
                    "classifiedConditions": [
                        {
                            "db": "MedGen",
                            "id": "C0268487",
                            "value": "Tyrosinemia type II",
                        },
                    ],
                    "traitSetId": "110",
                },
                "rcvClassifications": {
                    "germlineClassification": {
                        "description": {
                            "dateLastEvaluated": "1992-10-01T00:00:00Z",
                            "submissionCount": 1,
                            "value": "Pathogenic",
                        },
                        "reviewStatus": "AGGREGATE_GERMLINE_REVIEW_STATUS_NO_ASSERTION_CRITERIA_PROVIDED",
                    },
                },
                "title": "NM_000353.3(TAT):c.[1085G>T;912+2T>G] AND Tyrosinemia type II",
                "version": 4,
            },
        ),
    ],
)
def test_convert_cv_accession_xmldict_data_to_pb(xml_str: str, expected_json: Any):
    xmldict_value = xmltodict.parse(xml_str)
    result = ConvertRcvAccession.xmldict_data_to_pb(xmldict_value)
    result_json = MessageToDict(result)
    assert result_json == expected_json


@pytest.mark.parametrize(
    "xml_str,expected_json",
    [
        (
            """
            <RCVList>
                <RCVAccession Title="NM_014855.3(AP5Z1):c.80_83delinsTGCTGTAAACTGTAACTGTAAA (p.Arg27_Ile28delinsLeuLeuTer) AND Hereditary spastic paraplegia 48" Accession="RCV000000012" Version="5">
                    <ClassifiedConditionList TraitSetID="2">
                        <ClassifiedCondition DB="MedGen" ID="C3150901">Hereditary spastic paraplegia 48</ClassifiedCondition>
                    </ClassifiedConditionList>
                    <RCVClassifications>
                        <GermlineClassification>
                            <ReviewStatus>criteria provided, single submitter</ReviewStatus>
                            <Description SubmissionCount="2">Pathogenic</Description>
                        </GermlineClassification>
                    </RCVClassifications>
                </RCVAccession>
            </RCVList>
            """,
            {
                "rcvAccessions": [
                    {
                        "accession": "RCV000000012",
                        "classifiedConditionList": {
                            "classifiedConditions": [
                                {
                                    "db": "MedGen",
                                    "id": "C3150901",
                                    "value": "Hereditary spastic paraplegia 48",
                                },
                            ],
                            "traitSetId": "2",
                        },
                        "rcvClassifications": {
                            "germlineClassification": {
                                "description": {
                                    "submissionCount": 2,
                                    "value": "Pathogenic",
                                },
                                "reviewStatus": "AGGREGATE_GERMLINE_REVIEW_STATUS_CRITERIA_PROVIDED_SINGLE_SUBMITTER",
                            },
                        },
                        "title": "NM_014855.3(AP5Z1):c.80_83delinsTGCTGTAAACTGTAACTGTAAA "
                        "(p.Arg27_Ile28delinsLeuLeuTer) AND Hereditary spastic paraplegia "
                        "48",
                        "version": 5,
                    },
                ],
            },
        ),
    ],
)
def test_convert_classified_record_convert_rcv_list(xml_str: str, expected_json: Any):
    xmldict_value = xmltodict.parse(xml_str)
    result = ConvertClassifiedRecord.convert_rcv_list(xmldict_value)
    result_json = MessageToDict(result)
    assert result_json == expected_json


@pytest.mark.parametrize(
    "xmldict_value,expected",
    [
        (
            "Name",
            ClassifiedRecord.MappingType.MAPPING_TYPE_NAME,
        ),
        (
            "XRef",
            ClassifiedRecord.MappingType.MAPPING_TYPE_XREF,
        ),
    ],
)
def test_convert_classified_record_convert_mapping_type(
    xmldict_value: str, expected: ClassifiedRecord.MappingType.ValueType
):
    result = ConvertClassifiedRecord.convert_mapping_type(xmldict_value)
    assert result == expected


@pytest.mark.parametrize(
    "xml_str,expected_json",
    [
        (
            """
            <MedGen CUI="C3150901" Name="Hereditary spastic paraplegia 48"/>
            """,
            {
                "cui": "C3150901",
                "name": "Hereditary spastic paraplegia 48",
            },
        ),
    ],
)
def test_convert_classified_record_convert_trait_mapping_medgen(xml_str: str, expected_json: Any):
    xmldict_value = xmltodict.parse(xml_str)
    result = ConvertClassifiedRecord.convert_trait_mapping_medgen(xmldict_value)
    result_json = MessageToDict(result)
    assert result_json == expected_json


@pytest.mark.parametrize(
    "xml_str,expected_json",
    [
        (
            """
            <TraitMapping ClinicalAssertionID="20155" TraitType="Disease" MappingType="Name" MappingValue="SPASTIC PARAPLEGIA 48, AUTOSOMAL RECESSIVE" MappingRef="Preferred">
                <MedGen CUI="C3150901" Name="Hereditary spastic paraplegia 48"/>
            </TraitMapping>
            """,
            {
                "clinicalAssertionId": "20155",
                "mappingRef": "Preferred",
                "mappingType": "MAPPING_TYPE_NAME",
                "mappingValue": "SPASTIC PARAPLEGIA 48, AUTOSOMAL RECESSIVE",
                "medgens": [
                    {
                        "cui": "C3150901",
                        "name": "Hereditary spastic paraplegia 48",
                    },
                ],
                "traitType": "Disease",
            },
        ),
        (
            """
            <TraitMapping ClinicalAssertionID="2865972" TraitType="Disease" MappingType="XRef" MappingValue="613647" MappingRef="OMIM">
                <MedGen CUI="C3150901" Name="Hereditary spastic paraplegia 48"/>
            </TraitMapping>
            """,
            {
                "clinicalAssertionId": "2865972",
                "mappingRef": "OMIM",
                "mappingType": "MAPPING_TYPE_XREF",
                "mappingValue": "613647",
                "medgens": [
                    {
                        "cui": "C3150901",
                        "name": "Hereditary spastic paraplegia 48",
                    },
                ],
                "traitType": "Disease",
            },
        ),
    ],
)
def test_convert_classified_record_convert_trait_mapping(xml_str: str, expected_json: Any):
    xmldict_value = xmltodict.parse(xml_str)
    result = ConvertClassifiedRecord.convert_trait_mapping(xmldict_value)
    result_json = MessageToDict(result)
    assert result_json == expected_json


@pytest.mark.parametrize(
    "xml_str",
    [
        """
        <ClassifiedRecord>
            <SimpleAllele AlleleID="15065" VariationID="26">
                <GeneList>
                    <Gene Symbol="ABHD12" FullName="abhydrolase domain containing 12, lysophospholipase" GeneID="26090" HGNC_ID="HGNC:15868" Source="submitted" RelationshipType="within single gene">
                        <Location>
                            <CytogeneticLocation>20p11.21</CytogeneticLocation>
                            <SequenceLocation Assembly="GRCh38" AssemblyAccessionVersion="GCF_000001405.38" AssemblyStatus="current" Chr="20" Accession="NC_000020.11" start="25294743" stop="25390835" display_start="25294743" display_stop="25390835" Strand="-" />
                            <SequenceLocation Assembly="GRCh37" AssemblyAccessionVersion="GCF_000001405.25" AssemblyStatus="previous" Chr="20" Accession="NC_000020.10" start="25275378" stop="25371617" display_start="25275378" display_stop="25371617" Strand="-" />
                        </Location>
                        <OMIM>613599</OMIM>
                    </Gene>
                </GeneList>
                <Name>NM_001042472.3(ABHD12):c.846_852dup (p.His285Ter)</Name>
                <CanonicalSPDI>NC_000020.11:25307980:GCTCTTAGCT:GCTCTTAGCTCTTAGCT</CanonicalSPDI>
                <VariantType>Duplication</VariantType>
                <Location>
                    <CytogeneticLocation>20p11.21</CytogeneticLocation>
                    <SequenceLocation Assembly="GRCh38" AssemblyAccessionVersion="GCF_000001405.38" forDisplay="true" AssemblyStatus="current" Chr="20" Accession="NC_000020.11" start="25307980" stop="25307981" display_start="25307980" display_stop="25307981" variantLength="7" positionVCF="25307980" referenceAlleleVCF="G" alternateAlleleVCF="GGCTCTTA" />
                    <SequenceLocation Assembly="GRCh37" AssemblyAccessionVersion="GCF_000001405.25" AssemblyStatus="previous" Chr="20" Accession="NC_000020.10" start="25288616" stop="25288617" display_start="25288616" display_stop="25288617" variantLength="7" positionVCF="25288616" referenceAlleleVCF="G" alternateAlleleVCF="GGCTCTTA" />
                </Location>
                <ProteinChange>H285*</ProteinChange>
                <HGVSlist>
                    <HGVS Assembly="GRCh37" Type="genomic, top-level">
                        <NucleotideExpression sequenceAccessionVersion="NC_000020.10" sequenceAccession="NC_000020" sequenceVersion="10" change="g.25288620_25288626dup" Assembly="GRCh37">
                            <Expression>NC_000020.10:g.25288620_25288626dup</Expression>
                        </NucleotideExpression>
                    </HGVS>
                    <HGVS Assembly="GRCh38" Type="genomic, top-level">
                        <NucleotideExpression sequenceAccessionVersion="NC_000020.11" sequenceAccession="NC_000020" sequenceVersion="11" change="g.25307984_25307990dup" Assembly="GRCh38">
                            <Expression>NC_000020.11:g.25307984_25307990dup</Expression>
                        </NucleotideExpression>
                    </HGVS>
                    <HGVS Type="genomic">
                        <NucleotideExpression sequenceAccessionVersion="NG_028119.1" sequenceAccession="NG_028119" sequenceVersion="1" change="g.87996_88002dup">
                            <Expression>NG_028119.1:g.87996_88002dup</Expression>
                        </NucleotideExpression>
                    </HGVS>
                    <HGVS Type="coding">
                        <NucleotideExpression sequenceAccessionVersion="NM_001042472.3" sequenceAccession="NM_001042472" sequenceVersion="3" change="c.846_852dup" MANESelect="true">
                            <Expression>NM_001042472.3:c.846_852dup</Expression>
                        </NucleotideExpression>
                        <ProteinExpression sequenceAccessionVersion="NP_001035937.1" sequenceAccession="NP_001035937" sequenceVersion="1" change="p.His285Ter">
                            <Expression>NP_001035937.1:p.His285Ter</Expression>
                        </ProteinExpression>
                        <MolecularConsequence ID="SO:0001587" Type="nonsense" DB="SO" />
                    </HGVS>
                    <HGVS Type="coding">
                        <NucleotideExpression sequenceAccessionVersion="NM_015600.5" sequenceAccession="NM_015600" sequenceVersion="5" change="c.846_852dup">
                            <Expression>NM_015600.5:c.846_852dup</Expression>
                        </NucleotideExpression>
                        <ProteinExpression sequenceAccessionVersion="NP_056415.1" sequenceAccession="NP_056415" sequenceVersion="1" change="p.His285Ter">
                            <Expression>NP_056415.1:p.His285Ter</Expression>
                        </ProteinExpression>
                        <MolecularConsequence ID="SO:0001587" Type="nonsense" DB="SO" />
                    </HGVS>
                </HGVSlist>
                <XRefList>
                    <XRef ID="CA113810" DB="ClinGen" />
                    <XRef Type="Allelic variant" ID="613599.0003" DB="OMIM" />
                    <XRef Type="rs" ID="397704714" DB="dbSNP" />
                </XRefList>
            </SimpleAllele>
            <RCVList>
                <RCVAccession Title="NM_001042472.3(ABHD12):c.846_852dup (p.His285Ter) AND PHARC syndrome" Accession="RCV000000043" Version="3">
                    <ClassifiedConditionList TraitSetID="17">
                        <ClassifiedCondition DB="MedGen" ID="C2675204">PHARC syndrome</ClassifiedCondition>
                    </ClassifiedConditionList>
                    <RCVClassifications>
                        <GermlineClassification>
                            <ReviewStatus>no assertion criteria provided</ReviewStatus>
                            <Description DateLastEvaluated="2010-09-10" SubmissionCount="1">Pathogenic</Description>
                        </GermlineClassification>
                    </RCVClassifications>
                </RCVAccession>
            </RCVList>
            <Classifications>
                <GermlineClassification DateLastEvaluated="2010-09-10" NumberOfSubmissions="1" NumberOfSubmitters="1" DateCreated="2015-05-18" MostRecentSubmission="2015-05-18">
                    <ReviewStatus>no assertion criteria provided</ReviewStatus>
                    <Description>Pathogenic</Description>
                    <Citation Type="general">
                        <ID Source="PubMed">20797687</ID>
                    </Citation>
                    <ConditionList>
                        <TraitSet ID="17" Type="Disease" ContributesToAggregateClassification="true">
                            <Trait ID="5781" Type="Disease">
                                <Name>
                                    <ElementValue Type="Preferred">PHARC syndrome</ElementValue>
                                    <XRef ID="MONDO:0012984" DB="MONDO" />
                                </Name>
                                <Name>
                                    <ElementValue Type="Alternate">Polyneuropathy-hearing loss-ataxia-retinitis pigmentosa-cataract syndrome</ElementValue>
                                    <XRef ID="171848" DB="Orphanet" />
                                </Name>
                                <Name>
                                    <ElementValue Type="Alternate">Polyneuropathy, hearing loss, ataxia, retinitis pigmentosa, and cataract</ElementValue>
                                    <XRef ID="Polyneuropathy%2C+hearing+loss%2C+ataxia%2C+retinitis+pigmentosa%2C+and+cataract/9132" DB="Genetic Alliance" />
                                </Name>
                                <Symbol>
                                    <ElementValue Type="Alternate">PHARC</ElementValue>
                                    <XRef Type="MIM" ID="612674" DB="OMIM" />
                                </Symbol>
                                <XRef ID="171848" DB="Orphanet" />
                                <XRef ID="C2675204" DB="MedGen" />
                                <XRef ID="MONDO:0012984" DB="MONDO" />
                                <XRef Type="MIM" ID="612674" DB="OMIM" />
                            </Trait>
                        </TraitSet>
                    </ConditionList>
                </GermlineClassification>
            </Classifications>
            <ClinicalAssertionList>
                <ClinicalAssertion ID="20186" SubmissionDate="2015-05-12" DateLastUpdated="2015-05-18" DateCreated="2013-04-04">
                    <ClinVarSubmissionID localKey="613599.0003_POLYNEUROPATHY, HEARING LOSS, ATAXIA, RETINITIS PIGMENTOSA, AND CATARACT" title="ABHD12, 7-BP DUP, NT846_POLYNEUROPATHY, HEARING LOSS, ATAXIA, RETINITIS PIGMENTOSA, AND CATARACT" />
                    <ClinVarAccession Accession="SCV000020186" DateUpdated="2015-05-18" DateCreated="2013-04-04" Type="SCV" Version="2" SubmitterName="OMIM" OrgID="3" OrganizationCategory="resource" />
                    <RecordStatus>current</RecordStatus>
                    <Classification DateLastEvaluated="2010-09-10">
                        <ReviewStatus>no assertion criteria provided</ReviewStatus>
                        <GermlineClassification>Pathogenic</GermlineClassification>
                    </Classification>
                    <Assertion>variation to disease</Assertion>
                    <ObservedInList>
                        <ObservedIn>
                            <Sample>
                                <Origin>germline</Origin>
                                <Species>human</Species>
                                <AffectedStatus>not provided</AffectedStatus>
                            </Sample>
                            <Method>
                                <MethodType>literature only</MethodType>
                            </Method>
                            <ObservedData>
                                <Attribute Type="Description">In 7 patients from 4 Algerian families with polyneuropathy, hearing loss, ataxia, retinitis pigmentosa, and cataract (PHARC; 612674), Fiskerstrand et al. (2010) identified a homozygous 7-bp duplication in exon 9 of the ABHD12 gene (846_852dupTAAGAGC), resulting in a premature stop codon at residue 285. The patients ranged in age from 10 to 44 years. The older individuals were more severely affected. All patients had some evidence of a polyneuropathy, with hyporeflexia, pes cavus, and/or sensory loss, and most had gait ataxia with onset in the childhood. Four of the older patients had hearing loss, but only 1 had retinitis pigmentosa and cataract. Other common features included extensor plantar responses and cerebellar atrophy.</Attribute>
                                <Citation>
                                    <ID Source="PubMed">20797687</ID>
                                </Citation>
                                <XRef DB="OMIM" ID="612674" Type="MIM" />
                            </ObservedData>
                        </ObservedIn>
                    </ObservedInList>
                    <SimpleAllele>
                        <GeneList>
                            <Gene Symbol="ABHD12" />
                        </GeneList>
                        <Name>ABHD12, 7-BP DUP, NT846</Name>
                        <VariantType>Variation</VariantType>
                        <OtherNameList>
                            <Name Type="NonHGVS">7-BP DUP, NT846</Name>
                        </OtherNameList>
                        <XRefList>
                            <XRef DB="OMIM" ID="613599.0003" Type="Allelic variant" />
                        </XRefList>
                    </SimpleAllele>
                    <TraitSet Type="Disease">
                        <Trait Type="Disease">
                            <Name>
                                <ElementValue Type="Preferred">POLYNEUROPATHY, HEARING LOSS, ATAXIA, RETINITIS PIGMENTOSA, AND CATARACT</ElementValue>
                            </Name>
                        </Trait>
                    </TraitSet>
                </ClinicalAssertion>
            </ClinicalAssertionList>
            <TraitMappingList>
                <TraitMapping ClinicalAssertionID="20186" TraitType="Disease" MappingType="Name" MappingValue="POLYNEUROPATHY, HEARING LOSS, ATAXIA, RETINITIS PIGMENTOSA, AND CATARACT" MappingRef="Preferred">
                    <MedGen CUI="C2675204" Name="PHARC syndrome" />
                </TraitMapping>
            </TraitMappingList>
        </ClassifiedRecord>
        """,
    ],
    ids=[
        "id-15065",
    ],
)
def test_convert_classified_record_xmldict_data_to_pb(xml_str: str, snapshot):
    xmldict_value = xmltodict.parse(xml_str)
    result = ConvertClassifiedRecord.xmldict_data_to_pb(xmldict_value)
    result_json = MessageToDict(result)
    snapshot.assert_match(json.dumps(result_json, indent=2), "result")


@pytest.mark.parametrize(
    "xmldict_value,expected",
    [
        (
            "included",
            VariationArchive.RecordType.RECORD_TYPE_INCLUDED,
        ),
        (
            "classified",
            VariationArchive.RecordType.RECORD_TYPE_CLASSIFIED,
        ),
    ],
)
def test_convert_variation_archive_convert_record_type(
    xmldict_value: str, expected: VariationArchive.RecordType.ValueType
):
    result = ConvertVariationArchive.convert_record_type(xmldict_value)
    assert result == expected


@pytest.mark.parametrize(
    "xmldict_value,expected",
    [
        (
            "current",
            VariationArchive.RecordStatus.RECORD_STATUS_CURRENT,
        ),
        (
            "previous",
            VariationArchive.RecordStatus.RECORD_STATUS_PREVIOUS,
        ),
        (
            "replaced",
            VariationArchive.RecordStatus.RECORD_STATUS_REPLACED,
        ),
        (
            "deleted",
            VariationArchive.RecordStatus.RECORD_STATUS_DELETED,
        ),
    ],
)
def test_convert_variation_archive_convert_record_status(
    xmldict_value: str, expected: VariationArchive.RecordType.ValueType
):
    result = ConvertVariationArchive.convert_record_status(xmldict_value)
    assert result == expected


@pytest.mark.parametrize(
    "xml_str",
    [
        """
        <VariationArchive RecordType="classified" VariationID="2" VariationName="NM_014855.3(AP5Z1):c.80_83delinsTGCTGTAAACTGTAACTGTAAA (p.Arg27_Ile28delinsLeuLeuTer)" VariationType="Indel" Accession="VCV000000002" Version="3" NumberOfSubmissions="2" NumberOfSubmitters="2" DateLastUpdated="2022-04-25" DateCreated="2017-01-30" MostRecentSubmission="2021-05-16">
            <RecordStatus>current</RecordStatus>
            <Species>Homo sapiens</Species>
            <ClassifiedRecord>
                <SimpleAllele AlleleID="15041" VariationID="2">
                    <GeneList>
                        <Gene Symbol="AP5Z1" FullName="adaptor related protein complex 5 subunit zeta 1" GeneID="9907" HGNC_ID="HGNC:22197" Source="submitted" RelationshipType="within single gene">
                            <Location>
                                <CytogeneticLocation>7p22.1</CytogeneticLocation>
                                <SequenceLocation Assembly="GRCh38" AssemblyAccessionVersion="GCF_000001405.38" AssemblyStatus="current" Chr="7" Accession="NC_000007.14" start="4775623" stop="4794397" display_start="4775623" display_stop="4794397" Strand="+" />
                                <SequenceLocation Assembly="GRCh37" AssemblyAccessionVersion="GCF_000001405.25" AssemblyStatus="previous" Chr="7" Accession="NC_000007.13" start="4815261" stop="4834025" display_start="4815261" display_stop="4834025" Strand="+" />
                            </Location>
                            <OMIM>613653</OMIM>
                        </Gene>
                    </GeneList>
                    <Name>NM_014855.3(AP5Z1):c.80_83delinsTGCTGTAAACTGTAACTGTAAA (p.Arg27_Ile28delinsLeuLeuTer)</Name>
                    <CanonicalSPDI>NC_000007.14:4781212:GGAT:TGCTGTAAACTGTAACTGTAAA</CanonicalSPDI>
                    <VariantType>Indel</VariantType>
                    <Location>
                        <CytogeneticLocation>7p22.1</CytogeneticLocation>
                        <SequenceLocation Assembly="GRCh38" AssemblyAccessionVersion="GCF_000001405.38" forDisplay="true" AssemblyStatus="current" Chr="7" Accession="NC_000007.14" start="4781213" stop="4781216" display_start="4781213" display_stop="4781216" variantLength="22" positionVCF="4781213" referenceAlleleVCF="GGAT" alternateAlleleVCF="TGCTGTAAACTGTAACTGTAAA" />
                        <SequenceLocation Assembly="GRCh37" AssemblyAccessionVersion="GCF_000001405.25" AssemblyStatus="previous" Chr="7" Accession="NC_000007.13" start="4820844" stop="4820847" display_start="4820844" display_stop="4820847" variantLength="22" positionVCF="4820844" referenceAlleleVCF="GGAT" alternateAlleleVCF="TGCTGTAAACTGTAACTGTAAA" />
                    </Location>
                    <OtherNameList>
                        <Name>AP5Z1, 4-BP DEL/22-BP INS, NT80</Name>
                    </OtherNameList>
                    <HGVSlist>
                        <HGVS Assembly="GRCh37" Type="genomic, top-level">
                            <NucleotideExpression sequenceAccessionVersion="NC_000007.13" sequenceAccession="NC_000007" sequenceVersion="13" change="g.4820844_4820847delinsTGCTGTAAACTGTAACTGTAAA" Assembly="GRCh37">
                                <Expression>NC_000007.13:g.4820844_4820847delinsTGCTGTAAACTGTAACTGTAAA</Expression>
                            </NucleotideExpression>
                        </HGVS>
                        <HGVS Type="coding">
                            <NucleotideExpression sequenceAccessionVersion="NM_001364858.1" sequenceAccession="NM_001364858" sequenceVersion="1" change="c.-202_-199delinsTGCTGTAAACTGTAACTGTAAA">
                                <Expression>NM_001364858.1:c.-202_-199delinsTGCTGTAAACTGTAACTGTAAA</Expression>
                            </NucleotideExpression>
                            <MolecularConsequence ID="SO:0001623" Type="5 prime UTR variant" DB="SO" />
                        </HGVS>
                        <HGVS Type="coding">
                            <NucleotideExpression sequenceAccessionVersion="LRG_1247t1" sequenceAccession="LRG_1247t1" change="c.80_83delinsTGCTGTAAACTGTAACTGTAAA">
                                <Expression>LRG_1247t1:c.80_83delinsTGCTGTAAACTGTAACTGTAAA</Expression>
                            </NucleotideExpression>
                            <ProteinExpression sequenceAccessionVersion="LRG_1247p1" sequenceAccession="LRG_1247p1" change="p.Arg27_Ile28delinsLeuLeuTer">
                                <Expression>LRG_1247p1:p.Arg27_Ile28delinsLeuLeuTer</Expression>
                            </ProteinExpression>
                        </HGVS>
                        <HGVS Type="genomic">
                            <NucleotideExpression sequenceAccessionVersion="LRG_1247" sequenceAccession="LRG_1247" change="g.10583_10586delinsTGCTGTAAACTGTAACTGTAAA">
                                <Expression>LRG_1247:g.10583_10586delinsTGCTGTAAACTGTAACTGTAAA</Expression>
                            </NucleotideExpression>
                        </HGVS>
                        <HGVS Type="coding">
                            <NucleotideExpression sequenceAccessionVersion="NM_014855.3" sequenceAccession="NM_014855" sequenceVersion="3" change="c.80_83delinsTGCTGTAAACTGTAACTGTAAA" MANESelect="true">
                                <Expression>NM_014855.3:c.80_83delinsTGCTGTAAACTGTAACTGTAAA</Expression>
                            </NucleotideExpression>
                            <ProteinExpression sequenceAccessionVersion="NP_055670.1" sequenceAccession="NP_055670" sequenceVersion="1" change="p.Arg27_Ile28delinsLeuLeuTer">
                                <Expression>NP_055670.1:p.Arg27_Ile28delinsLeuLeuTer</Expression>
                            </ProteinExpression>
                            <MolecularConsequence ID="SO:0001587" Type="nonsense" DB="SO" />
                        </HGVS>
                        <HGVS Assembly="GRCh38" Type="genomic, top-level">
                            <NucleotideExpression sequenceAccessionVersion="NC_000007.14" sequenceAccession="NC_000007" sequenceVersion="14" change="g.4781213_4781216delinsTGCTGTAAACTGTAACTGTAAA" Assembly="GRCh38">
                                <Expression>NC_000007.14:g.4781213_4781216delinsTGCTGTAAACTGTAACTGTAAA</Expression>
                            </NucleotideExpression>
                        </HGVS>
                        <HGVS Type="genomic">
                            <NucleotideExpression sequenceAccessionVersion="NG_028111.1" sequenceAccession="NG_028111" sequenceVersion="1" change="g.10583_10586delinsTGCTGTAAACTGTAACTGTAAA">
                                <Expression>NG_028111.1:g.10583_10586delinsTGCTGTAAACTGTAACTGTAAA</Expression>
                            </NucleotideExpression>
                        </HGVS>
                        <HGVS Type="non-coding">
                            <NucleotideExpression sequenceAccessionVersion="NR_157345.1" sequenceAccession="NR_157345" sequenceVersion="1" change="n.173_176delinsTGCTGTAAACTGTAACTGTAAA">
                                <Expression>NR_157345.1:n.173_176delinsTGCTGTAAACTGTAACTGTAAA</Expression>
                            </NucleotideExpression>
                            <MolecularConsequence ID="SO:0001619" Type="non-coding transcript variant" DB="SO" />
                        </HGVS>
                    </HGVSlist>
                    <XRefList>
                        <XRef ID="CA215070" DB="ClinGen" />
                        <XRef Type="Allelic variant" ID="613653.0001" DB="OMIM" />
                        <XRef Type="rs" ID="397704705" DB="dbSNP" />
                    </XRefList>
                </SimpleAllele>
                <RCVList>
                    <RCVAccession Title="NM_014855.3(AP5Z1):c.80_83delinsTGCTGTAAACTGTAACTGTAAA (p.Arg27_Ile28delinsLeuLeuTer) AND Hereditary spastic paraplegia 48" Accession="RCV000000012" Version="5">
                        <ClassifiedConditionList TraitSetID="2">
                            <ClassifiedCondition DB="MedGen" ID="C3150901">Hereditary spastic paraplegia 48</ClassifiedCondition>
                        </ClassifiedConditionList>
                        <RCVClassifications>
                            <GermlineClassification>
                                <ReviewStatus>criteria provided, single submitter</ReviewStatus>
                                <Description SubmissionCount="2">Pathogenic</Description>
                            </GermlineClassification>
                        </RCVClassifications>
                    </RCVAccession>
                </RCVList>
                <Classifications>
                    <GermlineClassification NumberOfSubmissions="2" NumberOfSubmitters="2" DateCreated="2017-01-30" MostRecentSubmission="2021-05-16">
                        <ReviewStatus>criteria provided, single submitter</ReviewStatus>
                        <Description>Pathogenic</Description>
                        <Citation Type="general">
                            <ID Source="PubMed">20613862</ID>
                        </Citation>
                        <ConditionList>
                            <TraitSet ID="2" Type="Disease" ContributesToAggregateClassification="true">
                                <Trait ID="9580" Type="Disease">
                                    <Name>
                                        <ElementValue Type="Preferred">Hereditary spastic paraplegia 48</ElementValue>
                                        <XRef ID="MONDO:0013342" DB="MONDO" />
                                    </Name>
                                    <Name>
                                        <ElementValue Type="Alternate">Spastic paraplegia 48</ElementValue>
                                    </Name>
                                    <Name>
                                        <ElementValue Type="Alternate">Spastic paraplegia 48, autosomal recessive</ElementValue>
                                        <XRef ID="Spastic+paraplegia+48%2C+autosomal+recessive/9323" DB="Genetic Alliance" />
                                    </Name>
                                    <Symbol>
                                        <ElementValue Type="Alternate">SPG48</ElementValue>
                                        <XRef Type="MIM" ID="613647" DB="OMIM" />
                                    </Symbol>
                                    <XRef ID="306511" DB="Orphanet" />
                                    <XRef ID="C3150901" DB="MedGen" />
                                    <XRef ID="MONDO:0013342" DB="MONDO" />
                                    <XRef Type="MIM" ID="613647" DB="OMIM" />
                                </Trait>
                            </TraitSet>
                        </ConditionList>
                    </GermlineClassification>
                </Classifications>
                <ClinicalAssertionList>
                    <ClinicalAssertion ID="20155" SubmissionDate="2017-01-26" DateLastUpdated="2017-01-30" DateCreated="2013-04-04">
                        <ClinVarSubmissionID localKey="613653.0001_SPASTIC PARAPLEGIA 48, AUTOSOMAL RECESSIVE" title="AP5Z1, 4-BP DEL/22-BP INS, NT80_SPASTIC PARAPLEGIA 48, AUTOSOMAL RECESSIVE" />
                        <ClinVarAccession Accession="SCV000020155" DateUpdated="2017-01-30" DateCreated="2013-04-04" Type="SCV" Version="3" SubmitterName="OMIM" OrgID="3" OrganizationCategory="resource" />
                        <RecordStatus>current</RecordStatus>
                        <Classification DateLastEvaluated="2010-06-29">
                            <ReviewStatus>no assertion criteria provided</ReviewStatus>
                            <GermlineClassification>Pathogenic</GermlineClassification>
                        </Classification>
                        <Assertion>variation to disease</Assertion>
                        <ObservedInList>
                            <ObservedIn>
                                <Sample>
                                    <Origin>germline</Origin>
                                    <Species>human</Species>
                                    <AffectedStatus>not provided</AffectedStatus>
                                </Sample>
                                <Method>
                                    <MethodType>literature only</MethodType>
                                </Method>
                                <ObservedData>
                                    <Attribute Type="Description">In 2 French sibs with autosomal recessive spastic paraplegia-48 (SPG48; 613647), Slabicki et al. (2010) identified a homozygous complex insertion/deletion mutation in exon 2 of the KIAA0415 gene. The mutation comprised a 4-bp deletion (80del4) and a 22-bp insertion (84ins22), resulting in a frameshift and premature stop codon following residue 29. The insertion was found to be an imperfect quadruplication of a sequence, suggesting DNA polymerase slippage during DNA synthesis as the pathogenetic mechanism. The patients presented with progressive spastic paraplegia associated with urinary incontinence from ages 50 and 49 years, respectively. One had a normal cerebral MRI, whereas the other had spinal hyperintensities in the cervical spine. The unaffected parents were not known to be consanguineous, but they originated from 2 neighboring villages. The mutation was not found in 156 Caucasian or 242 North African control chromosomes. Studies of lymphoblastoid cells derived from 1 patient showed increased sensitivity to DNA-damaging drugs. The findings suggested a link between this form of spastic paraplegia, which could be considered a neurodegenerative disease, and defects in DNA repair.</Attribute>
                                    <Citation>
                                        <ID Source="PubMed">20613862</ID>
                                    </Citation>
                                    <XRef DB="OMIM" ID="613647" Type="MIM" />
                                </ObservedData>
                            </ObservedIn>
                        </ObservedInList>
                        <SimpleAllele>
                            <GeneList>
                                <Gene Symbol="AP5Z1" />
                            </GeneList>
                            <Name>AP5Z1, 4-BP DEL/22-BP INS, NT80</Name>
                            <VariantType>Variation</VariantType>
                            <OtherNameList>
                                <Name Type="NonHGVS">4-BP DEL/22-BP INS, NT80</Name>
                            </OtherNameList>
                            <XRefList>
                                <XRef DB="OMIM" ID="613653.0001" Type="Allelic variant" />
                            </XRefList>
                        </SimpleAllele>
                        <TraitSet Type="Disease">
                            <Trait Type="Disease">
                                <Name>
                                    <ElementValue Type="Preferred">SPASTIC PARAPLEGIA 48, AUTOSOMAL RECESSIVE</ElementValue>
                                </Name>
                            </Trait>
                        </TraitSet>
                    </ClinicalAssertion>
                    <ClinicalAssertion ID="2865972" SubmissionDate="2020-11-14" DateLastUpdated="2021-05-16" DateCreated="2021-05-16">
                        <ClinVarSubmissionID localKey="NM_014855.3:c.80_83delinsTGCTGTAAACTGTAACTGTAAA|OMIM:613647" submittedAssembly="GRCh37" />
                        <ClinVarAccession Accession="SCV001451119" DateUpdated="2021-05-16" DateCreated="2021-05-16" Type="SCV" Version="1" SubmitterName="Paris Brain Institute, Inserm - ICM" OrgID="507826" OrganizationCategory="laboratory" />
                        <RecordStatus>current</RecordStatus>
                        <Classification>
                            <ReviewStatus>criteria provided, single submitter</ReviewStatus>
                            <GermlineClassification>Pathogenic</GermlineClassification>
                        </Classification>
                        <Assertion>variation to disease</Assertion>
                        <AttributeSet>
                            <Attribute Type="AssertionMethod">ACMG Guidelines, 2015</Attribute>
                            <Citation>
                                <ID Source="PubMed">25741868</ID>
                            </Citation>
                        </AttributeSet>
                        <ObservedInList>
                            <ObservedIn>
                                <Sample>
                                    <Origin>unknown</Origin>
                                    <Species TaxonomyId="9606">human</Species>
                                    <AffectedStatus>yes</AffectedStatus>
                                </Sample>
                                <Method>
                                    <MethodType>clinical testing</MethodType>
                                </Method>
                                <ObservedData>
                                    <Attribute Type="VariantAlleles" integerValue="2" />
                                </ObservedData>
                            </ObservedIn>
                        </ObservedInList>
                        <SimpleAllele>
                            <VariantType>Variation</VariantType>
                            <AttributeSet>
                                <Attribute Type="HGVS">NM_014855.3:c.80_83delinsTGCTGTAAACTGTAACTGTAAA</Attribute>
                            </AttributeSet>
                        </SimpleAllele>
                        <TraitSet Type="Disease">
                            <Trait Type="Disease">
                                <XRef DB="OMIM" ID="613647" Type="MIM" />
                            </Trait>
                        </TraitSet>
                        <SubmissionNameList>
                            <SubmissionName>SUB8526155</SubmissionName>
                        </SubmissionNameList>
                    </ClinicalAssertion>
                </ClinicalAssertionList>
                <TraitMappingList>
                    <TraitMapping ClinicalAssertionID="20155" TraitType="Disease" MappingType="Name" MappingValue="SPASTIC PARAPLEGIA 48, AUTOSOMAL RECESSIVE" MappingRef="Preferred">
                        <MedGen CUI="C3150901" Name="Hereditary spastic paraplegia 48" />
                    </TraitMapping>
                    <TraitMapping ClinicalAssertionID="2865972" TraitType="Disease" MappingType="XRef" MappingValue="613647" MappingRef="OMIM">
                        <MedGen CUI="C3150901" Name="Hereditary spastic paraplegia 48" />
                    </TraitMapping>
                </TraitMappingList>
            </ClassifiedRecord>
        </VariationArchive>
        """,
    ],
    ids=[
        "VCV000000002",
    ],
)
def test_convert_variation_archive_xmldict_data_to_pb(xml_str: str, snapshot):
    xmldict_value = xmltodict.parse(xml_str)
    result = ConvertVariationArchive.xmldict_data_to_pb(xmldict_value)
    result_json = MessageToDict(result)
    snapshot.assert_match(json.dumps(result_json, indent=2), "result")


@pytest.mark.parametrize(
    "xml_str",
    [
        """
        <ClinVarVariationRelease xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://ftp.ncbi.nlm.nih.gov/pub/clinvar/xsd_public/ClinVar_VCV_2.0.xsd" ReleaseDate="2024-05-02">
            <VariationArchive RecordType="classified" VariationID="2" VariationName="NM_014855.3(AP5Z1):c.80_83delinsTGCTGTAAACTGTAACTGTAAA (p.Arg27_Ile28delinsLeuLeuTer)" VariationType="Indel" Accession="VCV000000002" Version="3" NumberOfSubmissions="2" NumberOfSubmitters="2" DateLastUpdated="2022-04-25" DateCreated="2017-01-30" MostRecentSubmission="2021-05-16">
                <RecordStatus>current</RecordStatus>
                <Species>Homo sapiens</Species>
                <ClassifiedRecord>
                    <SimpleAllele AlleleID="15041" VariationID="2">
                        <GeneList>
                            <Gene Symbol="AP5Z1" FullName="adaptor related protein complex 5 subunit zeta 1" GeneID="9907" HGNC_ID="HGNC:22197" Source="submitted" RelationshipType="within single gene">
                                <Location>
                                    <CytogeneticLocation>7p22.1</CytogeneticLocation>
                                    <SequenceLocation Assembly="GRCh38" AssemblyAccessionVersion="GCF_000001405.38" AssemblyStatus="current" Chr="7" Accession="NC_000007.14" start="4775623" stop="4794397" display_start="4775623" display_stop="4794397" Strand="+" />
                                    <SequenceLocation Assembly="GRCh37" AssemblyAccessionVersion="GCF_000001405.25" AssemblyStatus="previous" Chr="7" Accession="NC_000007.13" start="4815261" stop="4834025" display_start="4815261" display_stop="4834025" Strand="+" />
                                </Location>
                                <OMIM>613653</OMIM>
                            </Gene>
                        </GeneList>
                        <Name>NM_014855.3(AP5Z1):c.80_83delinsTGCTGTAAACTGTAACTGTAAA (p.Arg27_Ile28delinsLeuLeuTer)</Name>
                        <CanonicalSPDI>NC_000007.14:4781212:GGAT:TGCTGTAAACTGTAACTGTAAA</CanonicalSPDI>
                        <VariantType>Indel</VariantType>
                        <Location>
                            <CytogeneticLocation>7p22.1</CytogeneticLocation>
                            <SequenceLocation Assembly="GRCh38" AssemblyAccessionVersion="GCF_000001405.38" forDisplay="true" AssemblyStatus="current" Chr="7" Accession="NC_000007.14" start="4781213" stop="4781216" display_start="4781213" display_stop="4781216" variantLength="22" positionVCF="4781213" referenceAlleleVCF="GGAT" alternateAlleleVCF="TGCTGTAAACTGTAACTGTAAA" />
                            <SequenceLocation Assembly="GRCh37" AssemblyAccessionVersion="GCF_000001405.25" AssemblyStatus="previous" Chr="7" Accession="NC_000007.13" start="4820844" stop="4820847" display_start="4820844" display_stop="4820847" variantLength="22" positionVCF="4820844" referenceAlleleVCF="GGAT" alternateAlleleVCF="TGCTGTAAACTGTAACTGTAAA" />
                        </Location>
                        <OtherNameList>
                            <Name>AP5Z1, 4-BP DEL/22-BP INS, NT80</Name>
                        </OtherNameList>
                        <HGVSlist>
                            <HGVS Assembly="GRCh37" Type="genomic, top-level">
                                <NucleotideExpression sequenceAccessionVersion="NC_000007.13" sequenceAccession="NC_000007" sequenceVersion="13" change="g.4820844_4820847delinsTGCTGTAAACTGTAACTGTAAA" Assembly="GRCh37">
                                    <Expression>NC_000007.13:g.4820844_4820847delinsTGCTGTAAACTGTAACTGTAAA</Expression>
                                </NucleotideExpression>
                            </HGVS>
                            <HGVS Type="coding">
                                <NucleotideExpression sequenceAccessionVersion="NM_001364858.1" sequenceAccession="NM_001364858" sequenceVersion="1" change="c.-202_-199delinsTGCTGTAAACTGTAACTGTAAA">
                                    <Expression>NM_001364858.1:c.-202_-199delinsTGCTGTAAACTGTAACTGTAAA</Expression>
                                </NucleotideExpression>
                                <MolecularConsequence ID="SO:0001623" Type="5 prime UTR variant" DB="SO" />
                            </HGVS>
                            <HGVS Type="coding">
                                <NucleotideExpression sequenceAccessionVersion="LRG_1247t1" sequenceAccession="LRG_1247t1" change="c.80_83delinsTGCTGTAAACTGTAACTGTAAA">
                                    <Expression>LRG_1247t1:c.80_83delinsTGCTGTAAACTGTAACTGTAAA</Expression>
                                </NucleotideExpression>
                                <ProteinExpression sequenceAccessionVersion="LRG_1247p1" sequenceAccession="LRG_1247p1" change="p.Arg27_Ile28delinsLeuLeuTer">
                                    <Expression>LRG_1247p1:p.Arg27_Ile28delinsLeuLeuTer</Expression>
                                </ProteinExpression>
                            </HGVS>
                            <HGVS Type="genomic">
                                <NucleotideExpression sequenceAccessionVersion="LRG_1247" sequenceAccession="LRG_1247" change="g.10583_10586delinsTGCTGTAAACTGTAACTGTAAA">
                                    <Expression>LRG_1247:g.10583_10586delinsTGCTGTAAACTGTAACTGTAAA</Expression>
                                </NucleotideExpression>
                            </HGVS>
                            <HGVS Type="coding">
                                <NucleotideExpression sequenceAccessionVersion="NM_014855.3" sequenceAccession="NM_014855" sequenceVersion="3" change="c.80_83delinsTGCTGTAAACTGTAACTGTAAA" MANESelect="true">
                                    <Expression>NM_014855.3:c.80_83delinsTGCTGTAAACTGTAACTGTAAA</Expression>
                                </NucleotideExpression>
                                <ProteinExpression sequenceAccessionVersion="NP_055670.1" sequenceAccession="NP_055670" sequenceVersion="1" change="p.Arg27_Ile28delinsLeuLeuTer">
                                    <Expression>NP_055670.1:p.Arg27_Ile28delinsLeuLeuTer</Expression>
                                </ProteinExpression>
                                <MolecularConsequence ID="SO:0001587" Type="nonsense" DB="SO" />
                            </HGVS>
                            <HGVS Assembly="GRCh38" Type="genomic, top-level">
                                <NucleotideExpression sequenceAccessionVersion="NC_000007.14" sequenceAccession="NC_000007" sequenceVersion="14" change="g.4781213_4781216delinsTGCTGTAAACTGTAACTGTAAA" Assembly="GRCh38">
                                    <Expression>NC_000007.14:g.4781213_4781216delinsTGCTGTAAACTGTAACTGTAAA</Expression>
                                </NucleotideExpression>
                            </HGVS>
                            <HGVS Type="genomic">
                                <NucleotideExpression sequenceAccessionVersion="NG_028111.1" sequenceAccession="NG_028111" sequenceVersion="1" change="g.10583_10586delinsTGCTGTAAACTGTAACTGTAAA">
                                    <Expression>NG_028111.1:g.10583_10586delinsTGCTGTAAACTGTAACTGTAAA</Expression>
                                </NucleotideExpression>
                            </HGVS>
                            <HGVS Type="non-coding">
                                <NucleotideExpression sequenceAccessionVersion="NR_157345.1" sequenceAccession="NR_157345" sequenceVersion="1" change="n.173_176delinsTGCTGTAAACTGTAACTGTAAA">
                                    <Expression>NR_157345.1:n.173_176delinsTGCTGTAAACTGTAACTGTAAA</Expression>
                                </NucleotideExpression>
                                <MolecularConsequence ID="SO:0001619" Type="non-coding transcript variant" DB="SO" />
                            </HGVS>
                        </HGVSlist>
                        <XRefList>
                            <XRef ID="CA215070" DB="ClinGen" />
                            <XRef Type="Allelic variant" ID="613653.0001" DB="OMIM" />
                            <XRef Type="rs" ID="397704705" DB="dbSNP" />
                        </XRefList>
                    </SimpleAllele>
                    <RCVList>
                        <RCVAccession Title="NM_014855.3(AP5Z1):c.80_83delinsTGCTGTAAACTGTAACTGTAAA (p.Arg27_Ile28delinsLeuLeuTer) AND Hereditary spastic paraplegia 48" Accession="RCV000000012" Version="5">
                            <ClassifiedConditionList TraitSetID="2">
                                <ClassifiedCondition DB="MedGen" ID="C3150901">Hereditary spastic paraplegia 48</ClassifiedCondition>
                            </ClassifiedConditionList>
                            <RCVClassifications>
                                <GermlineClassification>
                                    <ReviewStatus>criteria provided, single submitter</ReviewStatus>
                                    <Description SubmissionCount="2">Pathogenic</Description>
                                </GermlineClassification>
                            </RCVClassifications>
                        </RCVAccession>
                    </RCVList>
                    <Classifications>
                        <GermlineClassification NumberOfSubmissions="2" NumberOfSubmitters="2" DateCreated="2017-01-30" MostRecentSubmission="2021-05-16">
                            <ReviewStatus>criteria provided, single submitter</ReviewStatus>
                            <Description>Pathogenic</Description>
                            <Citation Type="general">
                                <ID Source="PubMed">20613862</ID>
                            </Citation>
                            <ConditionList>
                                <TraitSet ID="2" Type="Disease" ContributesToAggregateClassification="true">
                                    <Trait ID="9580" Type="Disease">
                                        <Name>
                                            <ElementValue Type="Preferred">Hereditary spastic paraplegia 48</ElementValue>
                                            <XRef ID="MONDO:0013342" DB="MONDO" />
                                        </Name>
                                        <Name>
                                            <ElementValue Type="Alternate">Spastic paraplegia 48</ElementValue>
                                        </Name>
                                        <Name>
                                            <ElementValue Type="Alternate">Spastic paraplegia 48, autosomal recessive</ElementValue>
                                            <XRef ID="Spastic+paraplegia+48%2C+autosomal+recessive/9323" DB="Genetic Alliance" />
                                        </Name>
                                        <Symbol>
                                            <ElementValue Type="Alternate">SPG48</ElementValue>
                                            <XRef Type="MIM" ID="613647" DB="OMIM" />
                                        </Symbol>
                                        <XRef ID="306511" DB="Orphanet" />
                                        <XRef ID="C3150901" DB="MedGen" />
                                        <XRef ID="MONDO:0013342" DB="MONDO" />
                                        <XRef Type="MIM" ID="613647" DB="OMIM" />
                                    </Trait>
                                </TraitSet>
                            </ConditionList>
                        </GermlineClassification>
                    </Classifications>
                    <ClinicalAssertionList>
                        <ClinicalAssertion ID="20155" SubmissionDate="2017-01-26" DateLastUpdated="2017-01-30" DateCreated="2013-04-04">
                            <ClinVarSubmissionID localKey="613653.0001_SPASTIC PARAPLEGIA 48, AUTOSOMAL RECESSIVE" title="AP5Z1, 4-BP DEL/22-BP INS, NT80_SPASTIC PARAPLEGIA 48, AUTOSOMAL RECESSIVE" />
                            <ClinVarAccession Accession="SCV000020155" DateUpdated="2017-01-30" DateCreated="2013-04-04" Type="SCV" Version="3" SubmitterName="OMIM" OrgID="3" OrganizationCategory="resource" />
                            <RecordStatus>current</RecordStatus>
                            <Classification DateLastEvaluated="2010-06-29">
                                <ReviewStatus>no assertion criteria provided</ReviewStatus>
                                <GermlineClassification>Pathogenic</GermlineClassification>
                            </Classification>
                            <Assertion>variation to disease</Assertion>
                            <ObservedInList>
                                <ObservedIn>
                                    <Sample>
                                        <Origin>germline</Origin>
                                        <Species>human</Species>
                                        <AffectedStatus>not provided</AffectedStatus>
                                    </Sample>
                                    <Method>
                                        <MethodType>literature only</MethodType>
                                    </Method>
                                    <ObservedData>
                                        <Attribute Type="Description">In 2 French sibs with autosomal recessive spastic paraplegia-48 (SPG48; 613647), Slabicki et al. (2010) identified a homozygous complex insertion/deletion mutation in exon 2 of the KIAA0415 gene. The mutation comprised a 4-bp deletion (80del4) and a 22-bp insertion (84ins22), resulting in a frameshift and premature stop codon following residue 29. The insertion was found to be an imperfect quadruplication of a sequence, suggesting DNA polymerase slippage during DNA synthesis as the pathogenetic mechanism. The patients presented with progressive spastic paraplegia associated with urinary incontinence from ages 50 and 49 years, respectively. One had a normal cerebral MRI, whereas the other had spinal hyperintensities in the cervical spine. The unaffected parents were not known to be consanguineous, but they originated from 2 neighboring villages. The mutation was not found in 156 Caucasian or 242 North African control chromosomes. Studies of lymphoblastoid cells derived from 1 patient showed increased sensitivity to DNA-damaging drugs. The findings suggested a link between this form of spastic paraplegia, which could be considered a neurodegenerative disease, and defects in DNA repair.</Attribute>
                                        <Citation>
                                            <ID Source="PubMed">20613862</ID>
                                        </Citation>
                                        <XRef DB="OMIM" ID="613647" Type="MIM" />
                                    </ObservedData>
                                </ObservedIn>
                            </ObservedInList>
                            <SimpleAllele>
                                <GeneList>
                                    <Gene Symbol="AP5Z1" />
                                </GeneList>
                                <Name>AP5Z1, 4-BP DEL/22-BP INS, NT80</Name>
                                <VariantType>Variation</VariantType>
                                <OtherNameList>
                                    <Name Type="NonHGVS">4-BP DEL/22-BP INS, NT80</Name>
                                </OtherNameList>
                                <XRefList>
                                    <XRef DB="OMIM" ID="613653.0001" Type="Allelic variant" />
                                </XRefList>
                            </SimpleAllele>
                            <TraitSet Type="Disease">
                                <Trait Type="Disease">
                                    <Name>
                                        <ElementValue Type="Preferred">SPASTIC PARAPLEGIA 48, AUTOSOMAL RECESSIVE</ElementValue>
                                    </Name>
                                </Trait>
                            </TraitSet>
                        </ClinicalAssertion>
                        <ClinicalAssertion ID="2865972" SubmissionDate="2020-11-14" DateLastUpdated="2021-05-16" DateCreated="2021-05-16">
                            <ClinVarSubmissionID localKey="NM_014855.3:c.80_83delinsTGCTGTAAACTGTAACTGTAAA|OMIM:613647" submittedAssembly="GRCh37" />
                            <ClinVarAccession Accession="SCV001451119" DateUpdated="2021-05-16" DateCreated="2021-05-16" Type="SCV" Version="1" SubmitterName="Paris Brain Institute, Inserm - ICM" OrgID="507826" OrganizationCategory="laboratory" />
                            <RecordStatus>current</RecordStatus>
                            <Classification>
                                <ReviewStatus>criteria provided, single submitter</ReviewStatus>
                                <GermlineClassification>Pathogenic</GermlineClassification>
                            </Classification>
                            <Assertion>variation to disease</Assertion>
                            <AttributeSet>
                                <Attribute Type="AssertionMethod">ACMG Guidelines, 2015</Attribute>
                                <Citation>
                                    <ID Source="PubMed">25741868</ID>
                                </Citation>
                            </AttributeSet>
                            <ObservedInList>
                                <ObservedIn>
                                    <Sample>
                                        <Origin>unknown</Origin>
                                        <Species TaxonomyId="9606">human</Species>
                                        <AffectedStatus>yes</AffectedStatus>
                                    </Sample>
                                    <Method>
                                        <MethodType>clinical testing</MethodType>
                                    </Method>
                                    <ObservedData>
                                        <Attribute Type="VariantAlleles" integerValue="2" />
                                    </ObservedData>
                                </ObservedIn>
                            </ObservedInList>
                            <SimpleAllele>
                                <VariantType>Variation</VariantType>
                                <AttributeSet>
                                    <Attribute Type="HGVS">NM_014855.3:c.80_83delinsTGCTGTAAACTGTAACTGTAAA</Attribute>
                                </AttributeSet>
                            </SimpleAllele>
                            <TraitSet Type="Disease">
                                <Trait Type="Disease">
                                    <XRef DB="OMIM" ID="613647" Type="MIM" />
                                </Trait>
                            </TraitSet>
                            <SubmissionNameList>
                                <SubmissionName>SUB8526155</SubmissionName>
                            </SubmissionNameList>
                        </ClinicalAssertion>
                    </ClinicalAssertionList>
                    <TraitMappingList>
                        <TraitMapping ClinicalAssertionID="20155" TraitType="Disease" MappingType="Name" MappingValue="SPASTIC PARAPLEGIA 48, AUTOSOMAL RECESSIVE" MappingRef="Preferred">
                            <MedGen CUI="C3150901" Name="Hereditary spastic paraplegia 48" />
                        </TraitMapping>
                        <TraitMapping ClinicalAssertionID="2865972" TraitType="Disease" MappingType="XRef" MappingValue="613647" MappingRef="OMIM">
                            <MedGen CUI="C3150901" Name="Hereditary spastic paraplegia 48" />
                        </TraitMapping>
                    </TraitMappingList>
                </ClassifiedRecord>
            </VariationArchive>
        </ClinVarVariationRelease>
        """,
    ],
    ids=[
        "VCV000000002",
    ],
)
def test_convert_clinvar_variation_release_xmldict_data_to_pb(xml_str: str, snapshot):
    xmldict_value = xmltodict.parse(xml_str)
    result = ConvertClinvarVariationRelease.xmldict_data_to_pb(xmldict_value)
    result_json = MessageToDict(result)
    snapshot.assert_match(json.dumps(result_json, indent=2), "result")
