"""Types for the messages as returned by the API."""

import datetime
import typing

import attrs

ERROR_CODE_PARTIAL_SUCCESS = "1"
ERROR_CODE_ALL_FAILURE = "2"


@attrs.define
class Created:
    """Representation of successful creation."""

    #: The submission ID.
    id: str


@attrs.define
class Error:
    """Representation of server's response in case of failure."""

    #: The error response's message.
    message: str


@attrs.define
class SubmissionStatusFile:
    """Type for ``SubmissionStatus`` entry ``actions[*].response[*].files[*]``."""

    #: File URL
    url: str


@attrs.define
class SubmissionStatusObjectContent:
    """type for ``SubmissionStatusObjectContent`` entry in ``actions[*].response[*].objects[*].content``."""

    #: Processing status
    clinvarProcessingStatus: str
    #: Release status
    clinvarReleaseStatus: str


@attrs.define
class SubmissionStatusObject:
    """Type for ``SubmissionStatusObject`` entry in ``actions[*].response[*].objects[*]``."""

    #: Optional object accession.
    accession: typing.Optional[str]
    #: Object content.
    content: SubmissionStatusObjectContent
    #: Target database, usually "clinvar" per the docs.
    targetDb: str


@attrs.define
class SubmissionStatusResponseMessage:
    """Type for ``SubmissionStatusResponseMessage`` entry in ``actions[*].response[*].message``."""

    #: The error code.
    errorCode: typing.Optional[str]
    #: The message severity.
    severity: str
    #: The message text.
    text: str


@attrs.define
class SubmissionStatusResponse:
    """Type for ``SubmissionStatus`` entry ``actions[*].response[*]``."""

    #: Status, one of "processing", "processed", "error",
    status: str
    #: Files
    files: typing.List[SubmissionStatusFile]
    #: Message
    message: typing.Optional[SubmissionStatusResponseMessage]
    #: Objects
    objects: typing.List[SubmissionStatusObject]


@attrs.define
class SubmissionStatusActions:
    """Type for ``SubmissionStatus`` entry ``actions[*]``."""

    #: Identifier of the submission
    id: str
    #: Entries in ``actions[*].responses``, only one entry per the docs.
    responses: typing.List[SubmissionStatusResponse]
    #: Status of the submission, one of "submitted", "processing", "processed", "error"
    status: str
    #: Target database, usually "clinvar"
    targetDb: str
    #: Last updated time
    updated: datetime.datetime


@attrs.define
class SubmissionStatus:
    """Representation of server's response to a submission status query."""

    #: The list of actions (one element only by the docs).
    actions: typing.List[SubmissionStatusActions]


@attrs.define
class SummaryResponseErrorInput:
    value: str
    field: typing.Optional[str] = None


@attrs.define
class SummaryResponseErrorOutputError:
    userMessage: str


@attrs.define
class SummaryResponseErrorOutput:
    errors: typing.List[SummaryResponseErrorOutputError]


@attrs.define
class SummaryResponseError:
    # NB: docs and schema say required but examples do not show
    input: typing.List[SummaryResponseErrorInput]
    output: SummaryResponseErrorOutput


@attrs.define
class SummaryResponseDeletionIdentifier:
    clinvarAccession: str
    clinvarLocalKey: typing.Optional[str] = None


@attrs.define
class SummaryResponseDeletion:
    identifiers: SummaryResponseDeletionIdentifier
    processingStatus: str
    deleteDate: typing.Optional[str] = None
    deleteStatus: typing.Optional[str] = None
    errors: typing.Optional[typing.List[SummaryResponseError]] = None


@attrs.define
class SummaryResponseSubmissionIdentifiers:
    clinvarLocalKey: str
    clinvarAccession: typing.Optional[str] = None
    localID: typing.Optional[str] = None
    localKey: typing.Optional[str] = None


@attrs.define
class SummaryResponseSubmission:
    identifiers: SummaryResponseSubmissionIdentifiers
    processingStatus: str
    clinvarAccessionVersion: typing.Optional[str] = None
    errors: typing.Optional[typing.List[SummaryResponseError]] = None
    releaseDate: typing.Optional[str] = None
    releaseStatus: typing.Optional[str] = None


@attrs.define
class SummaryResponse:
    """Represetation of server's response to a submission."""

    batchProcessingStatus: str
    batchReleaseStatus: str
    submissionDate: str
    submissionName: str
    totalCount: int
    totalErrors: int
    totalPublic: int
    totalSuccess: int
    deletions: typing.Optional[typing.List[SummaryResponseDeletion]] = None
    submissions: typing.Optional[typing.List[SummaryResponseSubmission]] = None
    totalDeleteCount: typing.Optional[int] = None
    totalDeleted: typing.Optional[int] = None
    totalDeleteErrors: typing.Optional[int] = None
    totalDeleteSuccess: typing.Optional[int] = None


@attrs.define
class SubmissionClinvarDeletionAccessionSet:
    accession: str
    reason: typing.Optional[str] = None


@attrs.define
class SubmissionClinvarDeletion:
    accessionSet: typing.List[SubmissionClinvarDeletionAccessionSet]


@attrs.define
class SubmissionChromosomeCoordinates:
    accession: typing.Optional[str] = None
    assembly: typing.Optional[str] = None
    chromosome: typing.Optional[str] = None
    innerStart: typing.Optional[int] = None
    innerStop: typing.Optional[int] = None
    outerStart: typing.Optional[int] = None
    outerStop: typing.Optional[int] = None
    referenceAllele: typing.Optional[str] = None
    start: typing.Optional[int] = None
    stop: typing.Optional[int] = None
    variantLength: typing.Optional[int] = None


@attrs.define
class SubmissionVariantGene:
    id: typing.Optional[int] = None
    symbol: typing.Optional[str] = None


@attrs.define
class SubmissionVariant:
    chromosomeCoordinates: typing.Optional[SubmissionChromosomeCoordinates] = None
    copyNumber: typing.Optional[str] = None
    gene: typing.Optional[typing.List[SubmissionVariantGene]] = None
    hgvs: typing.Optional[str] = None
    referenceCopyNumber: typing.Optional[int] = None
    variantType: typing.Optional[str] = None


@attrs.define
class SubmissionVariantSet:
    variant: typing.List[SubmissionVariant]


@attrs.define
class SubmissionPhaseUnknownSet:
    hgvs: str
    variants: typing.List[SubmissionVariant]


@attrs.define
class SubmissionClinicalFeature:
    clinicalFeaturesAffectedStatus: str
    db: typing.Optional[str] = None
    id: typing.Optional[str] = None
    name: typing.Optional[str] = None


@attrs.define
class SubmissionObservedIn:
    affectedStatus: str
    alleleOrigin: str
    collectionMethod: str
    clinicalFeatures: typing.Optional[typing.List[SubmissionClinicalFeature]] = None
    clinicalFeaturesComment: typing.Optional[str] = None
    numberOfIndividuals: typing.Optional[int] = None
    structVarMethodType: typing.Optional[str] = None


@attrs.define
class SubmissionHaplotypeSet:
    hgvs: str
    variants: typing.List[SubmissionVariant]
    starAlleleName: typing.Optional[str] = None


@attrs.define
class SubmissionDistinctChromosomesSet:
    hgvs: str
    #: Hast at least two elements
    variants: typing.List[SubmissionVariant]


@attrs.define
class SubmissionHaplotypeSets:
    haplotypeSet: typing.Optional[SubmissionHaplotypeSet] = None
    haplotypeSingleVariantSet: typing.Optional[SubmissionHaplotypeSet] = None


@attrs.define
class SubmissionDisplotypeSet:
    haplotypeSets: typing.List[SubmissionHaplotypeSets]
    hgvs: str
    starAlleleName: typing.Optional[str] = None


@attrs.define
class SubmissionCitation:
    db: typing.Optional[str] = None
    id: typing.Optional[str] = None
    url: typing.Optional[str] = None


@attrs.define
class SubmissionAssertionCriteria:
    citation: SubmissionCitation
    method: str


@attrs.define
class SubmissionCondition:
    db: typing.Optional[str] = None
    id: typing.Optional[str] = None
    name: typing.Optional[str] = None


@attrs.define
class SubmissionDrugResponse:
    db: typing.Optional[str] = None
    drugName: typing.Optional[str] = None
    id: typing.Optional[str] = None
    condition: typing.Optional[typing.List[SubmissionCondition]] = None


@attrs.define
class SubmissionConditionSet:
    condition: typing.Optional[typing.List[SubmissionCondition]] = None
    drugResponse: typing.Optional[typing.List[SubmissionDrugResponse]] = None


@attrs.define
class SubmissionCompoundHeterozygoteSetVariantSet:
    variantSet: typing.Optional[SubmissionVariantSet] = None


@attrs.define
class SubmissionCompoundHeterozygoteSet:
    hvs: str
    # Must have two entries
    variantSets: typing.List[SubmissionCompoundHeterozygoteSetVariantSet]


@attrs.define
class SubmissionClinicalSignificance:
    clinicalSignificanceDescription: str
    citation: typing.Optional[typing.List[SubmissionCitation]] = None
    comment: typing.Optional[str] = None
    customAssertionScore: typing.Optional[float] = None
    dateLastEvaluated: typing.Optional[str] = None
    explanationOfDrugResponse: typing.Optional[str] = None
    explanationOfOtherClinicalSignificance: typing.Optional[str] = None
    modeOfInheritance: typing.Optional[str] = None


@attrs.define
class SubmissionClinvarSubmission:
    clinicalSignificance: SubmissionClinicalSignificance
    conditionSet: SubmissionConditionSet
    observedIn: typing.List[SubmissionObservedIn]
    recordStatus: str
    releaseStatus: str
    assertionCriteria: typing.Optional[SubmissionAssertionCriteria] = None
    clinvarAccession: typing.Optional[str] = None
    compoundHeterozygoteSet: typing.Optional[SubmissionCompoundHeterozygoteSet] = None
    diplotypeSet: typing.Optional[SubmissionDisplotypeSet] = None
    distinctChromosomesSet: typing.Optional[SubmissionDistinctChromosomesSet] = None
    #: Has at least two elements in `variants`
    haplotypeSet: typing.Optional[SubmissionHaplotypeSet] = None
    #: Has exactly one elements in `variants`
    haplotypeSingleVariantSet: typing.Optional[SubmissionHaplotypeSet] = None
    localID: typing.Optional[str] = None
    localKey: typing.Optional[str] = None
    phaseUnknownSet: typing.Optional[SubmissionPhaseUnknownSet] = None
    variantSet: typing.Optional[SubmissionVariantSet] = None


@attrs.define
class SubmissionContainer:
    """Representation of the container for a submission."""

    behalfOrgID: typing.Optional[int] = None
    clinvarDeletion: typing.Optional[SubmissionClinvarDeletion] = None
    clinvarSubmission: typing.Optional[typing.List[SubmissionClinvarSubmission]] = None
    submissionName: typing.Optional[str] = None
