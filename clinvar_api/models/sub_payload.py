"""Data structures for internal representation of submission payload."""

import typing

from pydantic import BaseModel
from pydantic.config import ConfigDict

from clinvar_api import msg

# Import and re-use the enums. This makes coupling tighter than it would have to be but the
# trade-off of copy-pasting them with no influence on the interal record API makes that not
# worth it.
from clinvar_api.msg.sub_payload import (
    AffectedStatus,
    AlleleOrigin,
    Assembly,
    Chromosome,
    CitationDb,
    ClinicalFeaturesAffectedStatus,
    ClinicalFeaturesDb,
    ClinicalSignificanceDescription,
    CollectionMethod,
    ConditionDb,
    ModeOfInheritance,
    MultipleConditionExplanation,
    RecordStatus,
    ReleaseStatus,
    StructVarMethodType,
    VariantType,
)


class SubmissionClinvarDeletionAccessionSet(BaseModel):
    model_config = ConfigDict(frozen=True)

    accession: str
    reason: typing.Optional[str] = None

    def to_msg(self) -> msg.SubmissionClinvarDeletionAccessionSet:
        return msg.SubmissionClinvarDeletionAccessionSet(
            accession=self.accession,
            reason=self.reason,
        )


class SubmissionClinvarDeletion(BaseModel):
    model_config = ConfigDict(frozen=True)

    accession_set: typing.List[SubmissionClinvarDeletionAccessionSet]

    def to_msg(self) -> msg.SubmissionClinvarDeletion:
        return msg.SubmissionClinvarDeletion(
            accessionSet=[msg_accession_set.to_msg() for msg_accession_set in self.accession_set],
        )


class SubmissionChromosomeCoordinates(BaseModel):
    model_config = ConfigDict(frozen=True)

    accession: typing.Optional[str] = None
    alternate_allele: typing.Optional[str] = None
    assembly: typing.Optional[Assembly] = None
    chromosome: typing.Optional[Chromosome] = None
    inner_start: typing.Optional[int] = None
    inner_stop: typing.Optional[int] = None
    outer_start: typing.Optional[int] = None
    outer_stop: typing.Optional[int] = None
    reference_allele: typing.Optional[str] = None
    start: typing.Optional[int] = None
    stop: typing.Optional[int] = None
    variant_length: typing.Optional[int] = None

    def to_msg(self) -> msg.SubmissionChromosomeCoordinates:
        return msg.SubmissionChromosomeCoordinates(
            accession=self.accession,
            assembly=self.assembly,
            alternateAllele=self.alternate_allele,
            chromosome=self.chromosome,
            innerStart=self.inner_start,
            innerStop=self.inner_stop,
            outerStart=self.outer_start,
            outerStop=self.outer_stop,
            referenceAllele=self.reference_allele,
            start=self.start,
            stop=self.stop,
            variantLength=self.variant_length,
        )


class SubmissionVariantGene(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: typing.Optional[int] = None
    symbol: typing.Optional[str] = None

    def to_msg(self) -> msg.SubmissionVariantGene:
        return msg.SubmissionVariantGene(
            id=self.id,
            symbol=self.symbol,
        )


class SubmissionVariant(BaseModel):
    model_config = ConfigDict(frozen=True)

    chromosome_coordinates: typing.Optional[SubmissionChromosomeCoordinates] = None
    copy_number: typing.Optional[str] = None
    gene: typing.Optional[typing.List[SubmissionVariantGene]] = None
    hgvs: typing.Optional[str] = None
    reference_copy_number: typing.Optional[int] = None
    variant_type: typing.Optional[VariantType] = None

    def to_msg(self) -> msg.SubmissionVariant:
        chromosome_coordinates = None
        if self.chromosome_coordinates:
            chromosome_coordinates = self.chromosome_coordinates.to_msg()
        gene = None
        if self.gene:
            gene = [msg_gene.to_msg() for msg_gene in self.gene]
        return msg.SubmissionVariant(
            chromosomeCoordinates=chromosome_coordinates,
            copyNumber=self.copy_number,
            gene=gene,
            hgvs=self.hgvs,
            referenceCopyNumber=self.reference_copy_number,
            variantType=self.variant_type,
        )


class SubmissionVariantSet(BaseModel):
    model_config = ConfigDict(frozen=True)

    variant: typing.List[SubmissionVariant]

    def to_msg(self) -> msg.SubmissionVariantSet:
        return msg.SubmissionVariantSet(
            variant=[msg_variant.to_msg() for msg_variant in self.variant]
        )


class SubmissionPhaseUnknownSet(BaseModel):
    model_config = ConfigDict(frozen=True)

    hgvs: str
    variants: typing.List[SubmissionVariant]

    def to_msg(self) -> msg.SubmissionPhaseUnknownSet:
        return msg.SubmissionPhaseUnknownSet(
            hgvs=self.hgvs,
            variants=[msg_variant.to_msg() for msg_variant in self.variants],
        )


class SubmissionClinicalFeature(BaseModel):
    model_config = ConfigDict(frozen=True)

    clinical_features_affected_status: ClinicalFeaturesAffectedStatus
    db: typing.Optional[ClinicalFeaturesDb] = None
    id: typing.Optional[str] = None
    name: typing.Optional[str] = None

    def to_msg(self) -> msg.SubmissionClinicalFeature:
        return msg.SubmissionClinicalFeature(
            clinicalFeaturesAffectedStatus=self.clinical_features_affected_status,
            db=self.db,
            id=self.id,
            name=self.name,
        )


class SubmissionObservedIn(BaseModel):
    model_config = ConfigDict(frozen=True)

    affected_status: AffectedStatus
    allele_origin: AlleleOrigin
    collection_method: CollectionMethod
    clinical_features: typing.Optional[typing.List[SubmissionClinicalFeature]] = None
    clinical_features_comment: typing.Optional[str] = None
    number_of_individuals: typing.Optional[int] = None
    struct_var_method_type: typing.Optional[StructVarMethodType] = None

    def to_msg(self) -> msg.SubmissionObservedIn:
        clinical_features = None
        if self.clinical_features:
            clinical_features = [
                SubmissionClinicalFeature.to_msg(msg_feature)
                for msg_feature in self.clinical_features
            ]
        return msg.SubmissionObservedIn(
            affectedStatus=self.affected_status,
            alleleOrigin=self.allele_origin,
            collectionMethod=self.collection_method,
            clinicalFeatures=clinical_features,
            clinicalFeaturesComment=self.clinical_features_comment,
            numberOfIndividuals=self.number_of_individuals,
            structVarMethodType=self.struct_var_method_type,
        )


class SubmissionHaplotypeSet(BaseModel):
    model_config = ConfigDict(frozen=True)

    hgvs: str
    variants: typing.List[SubmissionVariant]
    star_allele_name: typing.Optional[str] = None

    def to_msg(self) -> msg.SubmissionHaplotypeSet:
        return msg.SubmissionHaplotypeSet(
            hgvs=self.hgvs,
            variants=[msg_variant.to_msg() for msg_variant in self.variants],
            starAlleleName=self.star_allele_name,
        )


class SubmissionDistinctChromosomesSet(BaseModel):
    model_config = ConfigDict(frozen=True)

    hgvs: str
    #: Hast at least two elements
    variants: typing.List[SubmissionVariant]

    def to_msg(self) -> msg.SubmissionDistinctChromosomesSet:
        return msg.SubmissionDistinctChromosomesSet(
            hgvs=self.hgvs,
            variants=[msg_variant.to_msg() for msg_variant in self.variants],
        )


class SubmissionHaplotypeSets(BaseModel):
    model_config = ConfigDict(frozen=True)

    haplotype_set: typing.Optional[SubmissionHaplotypeSet] = None
    haplotype_single_variant_set: typing.Optional[SubmissionHaplotypeSet] = None

    def to_msg(self) -> msg.SubmissionHaplotypeSets:
        haplotype_set = None
        if self.haplotype_set:
            haplotype_set = self.haplotype_set.to_msg()
        haplotype_single_variant_set = None
        if self.haplotype_single_variant_set:
            haplotype_single_variant_set = self.haplotype_single_variant_set.to_msg()
        return msg.SubmissionHaplotypeSets(
            haplotypeSet=haplotype_set,
            haplotypeSingleVariantSet=haplotype_single_variant_set,
        )


class SubmissionDiplotypeSet(BaseModel):
    model_config = ConfigDict(frozen=True)

    haplotype_sets: typing.List[SubmissionHaplotypeSets]
    hgvs: str
    star_allele_name: typing.Optional[str] = None

    def to_msg(self) -> msg.SubmissionDiplotypeSet:
        return msg.SubmissionDiplotypeSet(
            haplotypeSets=[msg_sets.to_msg() for msg_sets in self.haplotype_sets],
            hgvs=self.hgvs,
            starAlleleName=self.star_allele_name,
        )


class SubmissionCitation(BaseModel):
    model_config = ConfigDict(frozen=True)

    db: typing.Optional[CitationDb] = None
    id: typing.Optional[str] = None
    url: typing.Optional[str] = None

    def to_msg(self) -> msg.SubmissionCitation:
        return msg.SubmissionCitation(
            db=self.db,
            id=self.id,
            url=self.url,
        )


class SubmissionAssertionCriteria(BaseModel):
    model_config = ConfigDict(frozen=True)

    db: typing.Optional[CitationDb] = None
    id: typing.Optional[str] = None
    url: typing.Optional[str] = None

    def to_msg(self) -> msg.SubmissionAssertionCriteria:
        return msg.SubmissionAssertionCriteria(
            db=self.db,
            id=self.id,
            url=self.url,
        )


class SubmissionCondition(BaseModel):
    model_config = ConfigDict(frozen=True)

    db: typing.Optional[ConditionDb] = None
    id: typing.Optional[str] = None
    name: typing.Optional[str] = None

    def to_msg(self) -> msg.SubmissionCondition:
        return msg.SubmissionCondition(
            db=self.db,
            id=self.id,
            name=self.name,
        )


class SubmissionDrugResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    db: typing.Optional[ConditionDb] = None
    drug_name: typing.Optional[str] = None
    id: typing.Optional[str] = None
    condition: typing.Optional[typing.List[SubmissionCondition]] = None

    def to_msg(self) -> msg.SubmissionDrugResponse:
        condition = None
        if self.condition:
            condition = [msg_condition.to_msg() for msg_condition in self.condition]
        return msg.SubmissionDrugResponse(
            db=self.db,
            drugName=self.drug_name,
            id=self.id,
            condition=condition,
        )


class SubmissionConditionSet(BaseModel):
    model_config = ConfigDict(frozen=True)

    condition: typing.Optional[typing.List[SubmissionCondition]] = None
    drug_response: typing.Optional[typing.List[SubmissionDrugResponse]] = None
    multiple_condition_explanation: typing.Optional[MultipleConditionExplanation] = None

    def to_msg(self) -> msg.SubmissionConditionSet:
        condition = None
        if self.condition:
            condition = [msg_condition.to_msg() for msg_condition in self.condition]
        drug_response = None
        if self.drug_response:
            drug_response = [msg_response.to_msg() for msg_response in self.drug_response]
        return msg.SubmissionConditionSet(
            condition=condition,
            drugResponse=drug_response,
            multipleConditionExplanation=self.multiple_condition_explanation,
        )


class SubmissionCompoundHeterozygoteSetVariantSet(BaseModel):
    model_config = ConfigDict(frozen=True)

    variant_set: typing.Optional[SubmissionVariantSet] = None

    def to_msg(self) -> msg.SubmissionCompoundHeterozygoteSetVariantSet:
        variant_set = None
        if self.variant_set:
            variant_set = self.variant_set.to_msg()
        return msg.SubmissionCompoundHeterozygoteSetVariantSet(variantSet=variant_set)


class SubmissionCompoundHeterozygoteSet(BaseModel):
    model_config = ConfigDict(frozen=True)

    hgvs: str
    # Must have two entries
    variant_sets: typing.List[SubmissionCompoundHeterozygoteSetVariantSet]

    def to_msg(self) -> msg.SubmissionCompoundHeterozygoteSet:
        return msg.SubmissionCompoundHeterozygoteSet(
            hgvs=self.hgvs,
            variantSets=[msg_set.to_msg() for msg_set in self.variant_sets],
        )


class SubmissionClinicalSignificance(BaseModel):
    model_config = ConfigDict(frozen=True)

    clinical_significance_description: ClinicalSignificanceDescription
    #: Must have at least one entry.
    citation: typing.Optional[typing.List[SubmissionCitation]] = None
    comment: typing.Optional[str] = None
    custom_assertion_score: typing.Optional[float] = None
    date_last_evaluated: typing.Optional[str] = None
    explanation_of_drug_response: typing.Optional[str] = None
    explanation_of_other_clinical_significance: typing.Optional[str] = None
    mode_of_inheritance: typing.Optional[ModeOfInheritance] = None

    def to_msg(self) -> msg.SubmissionClinicalSignificance:
        citation = None
        if self.citation:
            citation = [msg_citation.to_msg() for msg_citation in self.citation]
        return msg.SubmissionClinicalSignificance(
            clinicalSignificanceDescription=self.clinical_significance_description,
            citation=citation,
            comment=self.comment,
            customAssertionScore=self.custom_assertion_score,
            dateLastEvaluated=self.date_last_evaluated,
            explanationOfDrugResponse=self.explanation_of_drug_response,
            explanationOfOtherClinicalSignificance=self.explanation_of_other_clinical_significance,
            modeOfInheritance=self.mode_of_inheritance,
        )


class SubmissionClinvarSubmission(BaseModel):
    model_config = ConfigDict(frozen=True)

    clinical_significance: SubmissionClinicalSignificance
    condition_set: SubmissionConditionSet
    observed_in: typing.List[SubmissionObservedIn]
    record_status: RecordStatus
    clinvar_accession: typing.Optional[str] = None
    compound_heterozygote_set: typing.Optional[SubmissionCompoundHeterozygoteSet] = None
    diplotype_set: typing.Optional[SubmissionDiplotypeSet] = None
    distinct_chromosomes_set: typing.Optional[SubmissionDistinctChromosomesSet] = None
    #: Has at least two elements in `variants`
    haplotype_set: typing.Optional[SubmissionHaplotypeSet] = None
    #: Has exactly one elements in `variants`
    haplotype_single_variant_set: typing.Optional[SubmissionHaplotypeSet] = None
    local_id: typing.Optional[str] = None
    local_key: typing.Optional[str] = None
    phase_unknown_set: typing.Optional[SubmissionPhaseUnknownSet] = None
    variant_set: typing.Optional[SubmissionVariantSet] = None
    #: Additional information from import.  Will not be used for conversion to message but can be converted back to
    #: external formats.
    extra_data: typing.Optional[typing.Dict[str, typing.Any]] = None

    def to_msg(self) -> msg.SubmissionClinvarSubmission:
        compound_heterozygote_set = None
        if self.compound_heterozygote_set:
            compound_heterozygote_set = self.compound_heterozygote_set.to_msg()
        diplotype_set = None
        if self.diplotype_set:
            diplotype_set = self.diplotype_set.to_msg()
        distinct_chromosomes_set = None
        if self.distinct_chromosomes_set:
            distinct_chromosomes_set = self.distinct_chromosomes_set.to_msg()
        haplotype_set = None
        if self.haplotype_set:
            haplotype_set = self.haplotype_set.to_msg()
        haplotype_single_variant_set = None
        if self.haplotype_single_variant_set:
            haplotype_single_variant_set = self.haplotype_single_variant_set.to_msg()
        phase_unknown_set = None
        if self.phase_unknown_set:
            phase_unknown_set = self.phase_unknown_set.to_msg()
        variant_set = None
        if self.variant_set:
            variant_set = self.variant_set.to_msg()
        return msg.SubmissionClinvarSubmission(
            clinicalSignificance=self.clinical_significance.to_msg(),
            conditionSet=self.condition_set.to_msg(),
            observedIn=[msg_observed_in.to_msg() for msg_observed_in in self.observed_in],
            recordStatus=self.record_status,
            clinvarAccession=self.clinvar_accession,
            compoundHeterozygoteSet=compound_heterozygote_set,
            diplotypeSet=diplotype_set,
            distinctChromosomesSet=distinct_chromosomes_set,
            haplotypeSet=haplotype_set,
            haplotypeSingleVariantSet=haplotype_single_variant_set,
            localID=self.local_id,
            localKey=self.local_key,
            phaseUnknownSet=phase_unknown_set,
            variantSet=variant_set,
        )


class SubmissionContainer(BaseModel):
    model_config = ConfigDict(frozen=True)

    assertion_criteria: typing.Optional[SubmissionAssertionCriteria] = None
    behalf_org_id: typing.Optional[int] = None
    clinvar_deletion: typing.Optional[SubmissionClinvarDeletion] = None
    clinvar_submission: typing.Optional[typing.List[SubmissionClinvarSubmission]] = None
    clinvar_submission_release_status: typing.Optional[ReleaseStatus] = None
    submission_name: typing.Optional[str] = None

    def to_msg(self) -> msg.SubmissionContainer:
        assertion_criteria = None
        if self.assertion_criteria:
            assertion_criteria = self.assertion_criteria.to_msg()
        clinvar_deletion = None
        if self.clinvar_deletion:
            clinvar_deletion = self.clinvar_deletion.to_msg()
        clinvar_submission = None
        if self.clinvar_submission:
            clinvar_submission = [
                msg_submission.to_msg() for msg_submission in self.clinvar_submission
            ]
        return msg.SubmissionContainer(
            assertionCriteria=assertion_criteria,
            behalfOrgID=self.behalf_org_id,
            clinvarDeletion=clinvar_deletion,
            clinvarSubmission=clinvar_submission,
            clinvarSubmissionReleaseStatus=self.clinvar_submission_release_status,
            submissionName=self.submission_name,
        )
