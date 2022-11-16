"""Models to be used by the API user."""

import datetime
import typing

import attrs

from clinvar_api import api_msg

Assembly = api_msg.Assembly

Chromosome = api_msg.Chromosome

VariantType = api_msg.VariantType

CitationDb = api_msg.CitationDb

ConditionDb = api_msg.ConditionDb

ClinicalSignificanceDescription = api_msg.ClinicalSignificanceDescription

ModeOfInheritance = api_msg.ModeOfInheritance

AffectedStatus = api_msg.AffectedStatus

AlleleOrigin = api_msg.AlleleOrigin

ClinicalFeaturesAffectedStatus = api_msg.ClinicalFeaturesAffectedStatus

ClinicalFeaturesDb = api_msg.ClinicalFeaturesDb

CollectionMethod = api_msg.CollectionMethod

StructVarMethodType = api_msg.StructVarMethodType

BatchProcessingStatus = api_msg.BatchProcessingStatus

ProcessingStatus = api_msg.ProcessingStatus

RecordStatus = api_msg.RecordStatus

ReleaseStatus = api_msg.ReleaseStatus

BatchReleaseStatus = api_msg.BatchReleaseStatus


@attrs.define
class Created:
    #: The submission ID.
    id: str

    @classmethod
    def from_msg(cls, other: api_msg.Created):
        return Created(id=other.id)


@attrs.define
class Error:
    #: The error response's message.
    message: str

    @classmethod
    def from_msg(cls, other: api_msg.Error):
        return Error(message=other.message)


#: Re-use the type directly.
SubmissionStatusFile = api_msg.SubmissionStatusFile


@attrs.define
class SubmissionStatusObjectContent:
    #: Processing status
    clinvar_processing_status: str
    #: Release status
    clinvar_release_status: str

    @classmethod
    def from_msg(cls, other: api_msg.SubmissionStatusObjectContent):
        return SubmissionStatusObjectContent(
            clinvar_processing_status=other.clinvarProcessingStatus,
            clinvar_release_status=other.clinvarReleaseStatus,
        )


@attrs.define
class SubmissionStatusObject:
    #: Optional object accession.
    accession: typing.Optional[str]
    #: Object content.
    content: SubmissionStatusObjectContent
    #: Target database, usually "clinvar" per the docs.
    target_db: str

    @classmethod
    def from_msg(cls, other: api_msg.SubmissionStatusObject):
        return SubmissionStatusObject(
            accession=other.accession,
            content=SubmissionStatusObjectContent.from_msg(other.content),
            target_db=other.targetDb,
        )


@attrs.define
class SubmissionStatusResponseMessage:
    #: The error code.
    error_code: typing.Optional[str]
    #: The message severity.
    severity: str
    #: The message text.
    text: str

    @classmethod
    def from_msg(cls, other: api_msg.SubmissionStatusResponseMessage):
        return SubmissionStatusResponseMessage(
            error_code=other.errorCode, severity=other.severity, text=other.text
        )


@attrs.define
class SubmissionStatusResponse:

    #: Status, one of "processing", "processed", "error",
    status: str
    #: Files in the response.
    files: typing.List[SubmissionStatusFile]
    #: Message
    message: typing.Optional[SubmissionStatusResponseMessage]
    #: Objects
    objects: typing.List[SubmissionStatusObject]

    @classmethod
    def from_msg(cls, other: api_msg.SubmissionStatusResponse):
        if other.message:
            message = SubmissionStatusResponseMessage.from_msg(other.message)
        else:
            message = None
        return SubmissionStatusResponse(
            status=other.status,
            files=other.files,
            message=message,
            objects=list(map(SubmissionStatusObject.from_msg, other.objects)),
        )


@attrs.define
class SubmissionStatus:
    """Internal submission status."""

    #: Identifier of the submission
    id: str
    #: Entries in ``actions[*].responses``, only one entry per the docs.
    response: typing.Optional[SubmissionStatusResponse]
    #: Status of the submission, one of "submitted", "processing", "processed", "error"
    status: str
    #: Target database, usually "clinvar"
    target_db: str
    #: Last updated time
    updated: datetime.datetime

    @classmethod
    def from_msg(cls, other: api_msg.SubmissionStatus):
        if other.actions[0].responses:
            response = SubmissionStatusResponse.from_msg(other.actions[0].responses[0])
        else:
            response = None
        return SubmissionStatus(
            id=other.actions[0].id,
            response=response,
            status=other.actions[0].status,
            target_db=other.actions[0].targetDb,
            updated=other.actions[0].updated,
        )


@attrs.define
class SummaryResponseErrorInput:
    value: str
    field: typing.Optional[str] = None

    @classmethod
    def from_msg(cls, other: api_msg.SummaryResponseErrorInput):
        return SummaryResponseErrorInput(
            value=other.value,
            field=other.field,
        )


@attrs.define
class SummaryResponseErrorOutputError:
    user_message: str

    @classmethod
    def from_msg(cls, other: api_msg.SummaryResponseErrorOutputError):
        return SummaryResponseErrorOutputError(
            user_message=other.userMessage,
        )


@attrs.define
class SummaryResponseErrorOutput:
    errors: typing.List[SummaryResponseErrorOutputError]

    @classmethod
    def from_msg(cls, other: api_msg.SummaryResponseErrorOutput):
        return SummaryResponseErrorOutput(
            errors=[
                SummaryResponseErrorOutputError.from_msg(msg_error) for msg_error in other.errors
            ]
        )


@attrs.define
class SummaryResponseError:
    input: typing.List[SummaryResponseErrorInput]
    output: SummaryResponseErrorOutput

    @classmethod
    def from_msg(cls, other: api_msg.SummaryResponseError):
        return SummaryResponseError(
            input=[SummaryResponseErrorInput.from_msg(msg_input) for msg_input in other.input],
            output=SummaryResponseErrorOutput.from_msg(other.output),
        )


@attrs.define
class SummaryResponseDeletionIdentifier:
    clinvar_accession: str
    clinvar_local_key: typing.Optional[str] = None

    @classmethod
    def from_msg(cls, other: api_msg.SummaryResponseDeletionIdentifier):
        return SummaryResponseDeletionIdentifier(
            clinvar_accession=other.clinvarAccession,
            clinvar_local_key=other.clinvarLocalKey,
        )


@attrs.define
class SummaryResponseDeletion:
    identifiers: SummaryResponseDeletionIdentifier
    processing_status: str
    delete_date: typing.Optional[str] = None
    delete_status: typing.Optional[str] = None
    errors: typing.Optional[typing.List[SummaryResponseError]] = None

    @classmethod
    def from_msg(cls, other: api_msg.SummaryResponseDeletion):
        errors = None
        if other.errors:
            errors = [SummaryResponseError.from_msg(msg_error) for msg_error in other.errors]
        return SummaryResponseDeletion(
            identifiers=SummaryResponseDeletionIdentifier.from_msg(other.identifiers),
            processing_status=other.processingStatus,
            delete_date=other.deleteDate,
            delete_status=other.deleteStatus,
            errors=errors,
        )


@attrs.define
class SummaryResponseSubmissionIdentifiers:
    clinvar_local_key: str
    clinvar_accession: typing.Optional[str] = None
    local_id: typing.Optional[str] = None
    local_key: typing.Optional[str] = None

    @classmethod
    def from_msg(cls, other: api_msg.SummaryResponseSubmissionIdentifiers):
        return SummaryResponseSubmissionIdentifiers(
            clinvar_local_key=other.clinvarLocalKey,
            clinvar_accession=other.clinvarAccession,
            local_id=other.localID,
            local_key=other.localKey,
        )


@attrs.define
class SummaryResponseSubmission:
    identifiers: SummaryResponseSubmissionIdentifiers
    processing_status: str
    clinvar_accession_version: typing.Optional[str] = None
    errors: typing.Optional[typing.List[SummaryResponseError]] = None
    release_date: typing.Optional[str] = None
    release_status: typing.Optional[str] = None

    @classmethod
    def from_msg(cls, other: api_msg.SummaryResponseSubmission):
        errors = None
        if other.errors:
            errors = [SummaryResponseError.from_msg(msg_error) for msg_error in other.errors]
        return SummaryResponseSubmission(
            identifiers=SummaryResponseSubmissionIdentifiers.from_msg(
                other.identifiers,
            ),
            processing_status=other.processingStatus,
            clinvar_accession_version=other.clinvarAccessionVersion,
            errors=errors,
            release_date=other.releaseDate,
            release_status=other.releaseStatus,
        )


@attrs.define
class SummaryResponse:
    """Represetation of server's response to a submission."""

    batch_processing_status: BatchProcessingStatus
    batch_release_status: BatchReleaseStatus
    submission_date: str
    submission_name: str
    total_count: int
    total_errors: int
    total_public: int
    total_success: int
    deletions: typing.Optional[typing.List[SummaryResponseDeletion]] = None
    submissions: typing.Optional[typing.List[SummaryResponseSubmission]] = None
    total_delete_count: typing.Optional[int] = None
    total_deleted: typing.Optional[int] = None
    total_delete_errors: typing.Optional[int] = None
    total_delete_success: typing.Optional[int] = None

    @classmethod
    def from_msg(cls, other: api_msg.SummaryResponse):
        deletions = None
        if other.deletions:
            deletions = [
                SummaryResponseDeletion.from_msg(msg_deletion) for msg_deletion in other.deletions
            ]
        submissions = None
        if other.submissions:
            submissions = [
                SummaryResponseSubmission.from_msg(msg_deletion)
                for msg_deletion in other.submissions
            ]
        return SummaryResponse(
            batch_processing_status=other.batchProcessingStatus,
            batch_release_status=other.batchReleaseStatus,
            submission_date=other.submissionDate,
            submission_name=other.submissionName,
            total_count=other.totalCount,
            total_errors=other.totalErrors,
            total_public=other.totalPublic,
            total_success=other.totalSuccess,
            deletions=deletions,
            submissions=submissions,
            total_delete_count=other.totalDeleteCount,
            total_deleted=other.totalDeleted,
            total_delete_errors=other.totalDeleteErrors,
            total_delete_success=other.totalDeleteSuccess,
        )


@attrs.define
class SubmissionClinvarDeletionAccessionSet:
    accession: str
    reason: typing.Optional[str] = None

    @classmethod
    def from_msg(cls, other: api_msg.SubmissionClinvarDeletionAccessionSet):
        return SubmissionClinvarDeletionAccessionSet(
            accession=other.accession,
            reason=other.reason,
        )


@attrs.define
class SubmissionClinvarDeletion:
    accession_set: typing.List[SubmissionClinvarDeletionAccessionSet]

    @classmethod
    def from_msg(cls, other: api_msg.SubmissionClinvarDeletion):
        return SubmissionClinvarDeletion(
            accession_set=[
                SubmissionClinvarDeletionAccessionSet.from_msg(msg_accession_set)
                for msg_accession_set in other.accessionSet
            ],
        )


@attrs.define
class SubmissionChromosomeCoordinates:
    accession: typing.Optional[str] = None
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

    @classmethod
    def from_msg(cls, other: api_msg.SubmissionChromosomeCoordinates):
        return SubmissionChromosomeCoordinates(
            accession=other.accession,
            assembly=other.assembly,
            chromosome=other.chromosome,
            inner_start=other.innerStart,
            inner_stop=other.innerStop,
            outer_start=other.outerStart,
            outer_stop=other.outerStop,
            reference_allele=other.referenceAllele,
            start=other.start,
            stop=other.stop,
            variant_length=other.variantLength,
        )


@attrs.define
class SubmissionVariantGene:
    id: typing.Optional[int] = None
    symbol: typing.Optional[str] = None

    @classmethod
    def from_msg(cls, other: api_msg.SubmissionVariantGene):
        return SubmissionVariantGene(
            id=other.id,
            symbol=other.symbol,
        )


@attrs.define
class SubmissionVariant:
    chromosome_coordinates: typing.Optional[SubmissionChromosomeCoordinates] = None
    copy_number: typing.Optional[str] = None
    gene: typing.Optional[typing.List[SubmissionVariantGene]] = None
    hgvs: typing.Optional[str] = None
    reference_copy_number: typing.Optional[int] = None
    variant_type: typing.Optional[VariantType] = None

    @classmethod
    def from_msg(cls, other: api_msg.SubmissionVariant):
        chromosome_coordinates = None
        if other.chromosomeCoordinates:
            chromosome_coordinates = SubmissionChromosomeCoordinates.from_msg(
                other.chromosomeCoordinates
            )
        gene = None
        if other.gene:
            gene = [SubmissionVariantGene.from_msg(msg_gene) for msg_gene in other.gene]
        return SubmissionVariant(
            chromosome_coordinates=chromosome_coordinates,
            copy_number=other.copyNumber,
            gene=gene,
            hgvs=other.hgvs,
            reference_copy_number=other.referenceCopyNumber,
            variant_type=other.variantType,
        )


@attrs.define
class SubmissionVariantSet:
    variant: typing.List[SubmissionVariant]

    @classmethod
    def from_msg(cls, other: api_msg.SubmissionVariantSet):
        return SubmissionVariantSet(
            variant=[SubmissionVariant.from_msg(msg_variant) for msg_variant in other.variant]
        )


@attrs.define
class SubmissionPhaseUnknownSet:
    hgvs: str
    variants: typing.List[SubmissionVariant]

    @classmethod
    def from_msg(cls, other: api_msg.SubmissionPhaseUnknownSet):
        return SubmissionPhaseUnknownSet(
            hgvs=other.hgvs,
            variants=[SubmissionVariant.from_msg(msg_variant) for msg_variant in other.variants],
        )


@attrs.define
class SubmissionClinicalFeature:
    clinical_features_affected_status: ClinicalFeaturesAffectedStatus
    db: typing.Optional[ClinicalFeaturesDb] = None
    id: typing.Optional[str] = None
    name: typing.Optional[str] = None

    @classmethod
    def from_msg(cls, other: api_msg.SubmissionClinicalFeature):
        return SubmissionClinicalFeature(
            clinical_features_affected_status=other.clinicalFeaturesAffectedStatus,
            db=other.db,
            id=other.id,
            name=other.name,
        )


@attrs.define
class SubmissionObservedIn:
    affected_status: AffectedStatus
    allele_origin: AlleleOrigin
    collection_method: CollectionMethod
    clinical_features: typing.Optional[typing.List[SubmissionClinicalFeature]] = None
    clinical_features_comment: typing.Optional[str] = None
    number_of_individuals: typing.Optional[int] = None
    struct_var_method_type: typing.Optional[StructVarMethodType] = None

    @classmethod
    def from_msg(cls, other: api_msg.SubmissionObservedIn):
        clinical_features = None
        if other.clinicalFeatures:
            clinical_features = [
                SubmissionClinicalFeature.from_msg(msg_feature)
                for msg_feature in other.clinicalFeatures
            ]
        return SubmissionObservedIn(
            affected_status=other.affectedStatus,
            allele_origin=other.alleleOrigin,
            collection_method=other.collectionMethod,
            clinical_features=clinical_features,
            clinical_features_comment=other.clinicalFeaturesComment,
            number_of_individuals=other.numberOfIndividuals,
            struct_var_method_type=other.structVarMethodType,
        )


@attrs.define
class SubmissionHaplotypeSet:
    hgvs: str
    variants: typing.List[SubmissionVariant]
    star_allele_name: typing.Optional[str] = None

    @classmethod
    def from_msg(cls, other: api_msg.SubmissionHaplotypeSet):
        return SubmissionHaplotypeSet(
            hgvs=other.hgvs,
            variants=[SubmissionVariant.from_msg(msg_variant) for msg_variant in other.variants],
            star_allele_name=other.starAlleleName,
        )


@attrs.define
class SubmissionDistinctChromosomesSet:
    hgvs: str
    #: Hast at least two elements
    variants: typing.List[SubmissionVariant]

    @classmethod
    def from_msg(cls, other: api_msg.SubmissionDistinctChromosomesSet):
        return SubmissionDistinctChromosomesSet(
            hgvs=other.hgvs,
            variants=[SubmissionVariant.from_msg(msg_variant) for msg_variant in other.variants],
        )


@attrs.define
class SubmissionHaplotypeSets:
    haplotype_set: typing.Optional[SubmissionHaplotypeSet] = None
    haplotype_single_variant_set: typing.Optional[SubmissionHaplotypeSet] = None

    @classmethod
    def from_msg(cls, other: api_msg.SubmissionHaplotypeSets):
        haplotype_set = None
        if other.haplotypeSet:
            haplotype_set = SubmissionHaplotypeSet.from_msg(other.haplotypeSet)
        haplotype_single_variant_set = None
        if other.haplotypeSingleVariantSet:
            haplotype_single_variant_set = SubmissionHaplotypeSet.from_msg(
                other.haplotypeSingleVariantSet
            )
        return SubmissionHaplotypeSets(
            haplotype_set=haplotype_set,
            haplotype_single_variant_set=haplotype_single_variant_set,
        )


@attrs.define
class SubmissionDisplotypeSet:
    haplotype_sets: typing.List[SubmissionHaplotypeSets]
    hgvs: str
    star_allele_name: typing.Optional[str] = None

    @classmethod
    def from_msg(cls, other: api_msg.SubmissionDiplotypeSet):
        return SubmissionDisplotypeSet(
            haplotype_sets=[
                SubmissionHaplotypeSets.from_msg(msg_sets) for msg_sets in other.haplotypeSets
            ],
            hgvs=other.hgvs,
            star_allele_name=other.starAlleleName,
        )


@attrs.define
class SubmissionCitation:
    db: typing.Optional[CitationDb] = None
    id: typing.Optional[str] = None
    url: typing.Optional[str] = None

    @classmethod
    def from_msg(cls, other: api_msg.SubmissionCitation):
        return SubmissionCitation(
            db=other.db,
            id=other.id,
            url=other.url,
        )


@attrs.define
class SubmissionAssertionCriteria:
    citation: SubmissionCitation
    method: str

    @classmethod
    def from_msg(cls, other: api_msg.SubmissionAssertionCriteria):
        return SubmissionAssertionCriteria(
            citation=SubmissionCitation.from_msg(other.citation), method=other.method
        )


@attrs.define
class SubmissionCondition:
    db: typing.Optional[ConditionDb] = None
    id: typing.Optional[str] = None
    name: typing.Optional[str] = None

    @classmethod
    def from_msg(cls, other: api_msg.SubmissionCondition):
        return SubmissionCondition(
            db=other.db,
            id=other.id,
            name=other.name,
        )


@attrs.define
class SubmissionDrugResponse:
    db: typing.Optional[ConditionDb] = None
    drug_name: typing.Optional[str] = None
    id: typing.Optional[str] = None
    condition: typing.Optional[typing.List[SubmissionCondition]] = None

    @classmethod
    def from_msg(cls, other: api_msg.SubmissionDrugResponse):
        condition = None
        if other.condition:
            condition = [
                SubmissionCondition.from_msg(msg_condition) for msg_condition in other.condition
            ]
        return SubmissionDrugResponse(
            db=other.db,
            drug_name=other.drugName,
            id=other.id,
            condition=condition,
        )


@attrs.define
class SubmissionConditionSet:
    condition: typing.Optional[typing.List[SubmissionCondition]] = None
    drug_response: typing.Optional[typing.List[SubmissionDrugResponse]] = None

    @classmethod
    def from_msg(cls, other: api_msg.SubmissionConditionSet):
        condition = None
        if other.condition:
            condition = [
                SubmissionCondition.from_msg(msg_condition) for msg_condition in other.condition
            ]
        drug_response = None
        if other.drugResponse:
            drug_response = [
                SubmissionDrugResponse.from_msg(msg_response) for msg_response in other.drugResponse
            ]
        return SubmissionConditionSet(
            condition=condition,
            drug_response=drug_response,
        )


@attrs.define
class SubmissionCompoundHeterozygoteSetVariantSet:
    variant_set: typing.Optional[SubmissionVariantSet] = None

    @classmethod
    def from_msg(cls, other: api_msg.SubmissionCompoundHeterozygoteSetVariantSet):
        variant_set = None
        if other.variantSet:
            variant_set = SubmissionVariantSet.from_msg(other.variantSet)
        return SubmissionCompoundHeterozygoteSetVariantSet(variant_set=variant_set)


@attrs.define
class SubmissionCompoundHeterozygoteSet:
    hgvs: str
    # Must have two entries
    variant_sets: typing.List[SubmissionCompoundHeterozygoteSetVariantSet]

    @classmethod
    def from_msg(cls, other: api_msg.SubmissionCompoundHeterozygoteSet):
        return SubmissionCompoundHeterozygoteSet(
            hgvs=other.hgvs,
            variant_sets=[
                SubmissionCompoundHeterozygoteSetVariantSet.from_msg(msg_set)
                for msg_set in other.variantSets
            ],
        )


@attrs.define
class SubmissionClinicalSignificance:
    clinical_significance_description: ClinicalSignificanceDescription
    citation: typing.Optional[typing.List[SubmissionCitation]] = None
    comment: typing.Optional[str] = None
    custom_assertion_score: typing.Optional[float] = None
    date_last_evaluated: typing.Optional[str] = None
    explanation_of_drug_response: typing.Optional[str] = None
    explanation_of_other_clinical_significance: typing.Optional[str] = None
    mode_of_inheritance: typing.Optional[ModeOfInheritance] = None

    @classmethod
    def from_msg(cls, other: api_msg.SubmissionClinicalSignificance):
        citation = None
        if other.citation:
            citation = [
                SubmissionCitation.from_msg(msg_citation) for msg_citation in other.citation
            ]
        return SubmissionClinicalSignificance(
            clinical_significance_description=other.clinicalSignificanceDescription,
            citation=citation,
            comment=other.comment,
            custom_assertion_score=other.customAssertionScore,
            date_last_evaluated=other.dateLastEvaluated,
            explanation_of_drug_response=other.explanationOfDrugResponse,
            explanation_of_other_clinical_significance=other.explanationOfOtherClinicalSignificance,
            mode_of_inheritance=other.modeOfInheritance,
        )


@attrs.define
class SubmissionClinvarSubmission:
    clinical_significance: SubmissionClinicalSignificance
    condition_set: SubmissionConditionSet
    observed_in: typing.List[SubmissionObservedIn]
    record_status: RecordStatus
    release_status: ReleaseStatus
    assertion_criteria: typing.Optional[SubmissionAssertionCriteria] = None
    clinvar_accession: typing.Optional[str] = None
    compound_heterozygote_set: typing.Optional[SubmissionCompoundHeterozygoteSet] = None
    diplotype_set: typing.Optional[SubmissionDisplotypeSet] = None
    distinct_chromosomes_set: typing.Optional[SubmissionDistinctChromosomesSet] = None
    #: Has at least two elements in `variants`
    haplotype_set: typing.Optional[SubmissionHaplotypeSet] = None
    #: Has exactly one elements in `variants`
    haplotype_single_variant_set: typing.Optional[SubmissionHaplotypeSet] = None
    local_id: typing.Optional[str] = None
    local_key: typing.Optional[str] = None
    phase_unknown_set: typing.Optional[SubmissionPhaseUnknownSet] = None
    variant_set: typing.Optional[SubmissionVariantSet] = None

    @classmethod
    def from_msg(cls, other: api_msg.SubmissionClinvarSubmission):
        assertion_criteria = None
        if other.assertionCriteria:
            assertion_criteria = SubmissionAssertionCriteria.from_msg(other.assertionCriteria)
        compound_heterozygote_set = None
        if other.compoundHeterozygoteSet:
            compound_heterozygote_set = SubmissionCompoundHeterozygoteSet.from_msg(
                other.compoundHeterozygoteSet
            )
        diplotype_set = None
        if other.diplotypeSet:
            diplotype_set = SubmissionDisplotypeSet.from_msg(other.diplotypeSet)
        distinct_chromosomes_set = None
        if other.distinctChromosomesSet:
            distinct_chromosomes_set = SubmissionDistinctChromosomesSet.from_msg(
                other.distinctChromosomesSet,
            )
        haplotype_set = None
        if other.haplotypeSet:
            haplotype_set = SubmissionHaplotypeSet.from_msg(other.haplotypeSet)
        haplotype_single_variant_set = None
        if other.haplotypeSingleVariantSet:
            haplotype_single_variant_set = SubmissionHaplotypeSet.from_msg(
                other.haplotypeSingleVariantSet,
            )
        phase_unknown_set = None
        if other.phaseUnknownSet:
            phase_unknown_set = SubmissionPhaseUnknownSet.from_msg(other.phaseUnknownSet)
        variant_set = None
        if other.variantSet:
            variant_set = SubmissionVariantSet.from_msg(other.variantSet)
        return SubmissionClinvarSubmission(
            clinical_significance=SubmissionClinicalSignificance.from_msg(
                other.clinicalSignificance
            ),
            condition_set=SubmissionConditionSet.from_msg(other.conditionSet),
            observed_in=[
                SubmissionObservedIn.from_msg(msg_observed_in)
                for msg_observed_in in other.observedIn
            ],
            record_status=other.recordStatus,
            release_status=other.releaseStatus,
            assertion_criteria=assertion_criteria,
            clinvar_accession=other.clinvarAccession,
            compound_heterozygote_set=compound_heterozygote_set,
            diplotype_set=diplotype_set,
            distinct_chromosomes_set=distinct_chromosomes_set,
            haplotype_set=haplotype_set,
            haplotype_single_variant_set=haplotype_single_variant_set,
            local_id=other.localID,
            local_key=other.localKey,
            phase_unknown_set=phase_unknown_set,
            variant_set=variant_set,
        )


@attrs.define
class SubmissionContainer:
    behalf_org_id: typing.Optional[int] = None
    clinvar_deletion: typing.Optional[SubmissionClinvarDeletion] = None
    clinvar_submission: typing.Optional[typing.List[SubmissionClinvarSubmission]] = None
    submission_name: typing.Optional[str] = None

    @classmethod
    def from_msg(cls, other: api_msg.SubmissionContainer):
        clinvar_deletion = None
        if other.clinvarDeletion:
            clinvar_deletion = SubmissionClinvarDeletion.from_msg(other.clinvarDeletion)
        clinvar_submission = None
        if other.clinvarSubmission:
            clinvar_submission = [
                SubmissionClinvarSubmission.from_msg(msg_submission)
                for msg_submission in other.clinvarSubmission
            ]
        return SubmissionContainer(
            behalf_org_id=other.behalfOrgID,
            clinvar_deletion=clinvar_deletion,
            clinvar_submission=clinvar_submission,
            submission_name=other.submissionName,
        )
