"""Data structures for encoding the submission payload."""

from enum import Enum
import typing

from pydantic import BaseModel
from pydantic.config import ConfigDict


class Assembly(Enum):
    GRCH38 = "GRCh38"
    HG38 = "hg38"
    GRCH37 = "GRCh37"
    HG19 = "hg19"
    NCBI36 = "NCBI36"
    HG18 = "hg18"


class Chromosome(Enum):
    CHR1 = "1"
    CHR2 = "2"
    CHR3 = "3"
    CHR4 = "4"
    CHR5 = "5"
    CHR6 = "6"
    CHR7 = "7"
    CHR8 = "8"
    CHR9 = "9"
    CHR10 = "10"
    CHR11 = "11"
    CHR12 = "12"
    CHR13 = "13"
    CHR14 = "14"
    CHR15 = "15"
    CHR16 = "16"
    CHR17 = "17"
    CHR18 = "18"
    CHR19 = "19"
    CHR20 = "20"
    CHR21 = "21"
    CHR22 = "22"
    CHRX = "X"
    CHRY = "Y"
    CHRMT = "MT"


class VariantType(Enum):
    INSERTION = "Insertion"
    DELETION = "Deletion"
    DUPLICATION = "Duplication"
    TANDEM_DUPLICATIOn = "Tandem duplication"
    COPY_NUMBER_LOSS = "copy number loss"
    COPY_NUMBER_GAIN = "copy number gain"
    INVERSION = "Inversion"
    TRANSLOCATION = "Translocation"
    COMPLEX = "Complex"


class CitationDb(Enum):
    """Allowed values for a citation's `db` field.

    The values of the enumeration map to the values used by the ClinVar submission API.
    """

    PUBMED = "PubMed"
    BOOKSHELF = "BookShelf"
    DOI = "DOI"
    PMC = "pmc"


class ConditionDb(Enum):
    OMIM = "OMIM"
    MEDGEN = "MedGen"
    ORPHANET = "Orphanet"
    MESH = "MeSH"
    HP = "HP"
    MONDO = "MONDO"


class MultipleConditionExplanation(Enum):
    NOVEL_DISEASE = "Novel disease"
    UNCERTAIN = "Uncertain"
    CO_OCCURING = "Co-occurring"


class AffectedStatus(Enum):
    YES = "yes"
    NO = "no"
    UNKNOWN = "unknown"
    NOT_PROVIDED = "not provided"
    NOT_APPLICABLE = "not applicable"


class AlleleOrigin(Enum):
    GERMLINE = "germline"
    SOMATIC = "somatic"
    DE_NOVO = "de novo"
    UNKNOWN = "unknown"
    INHERITED = "inherited"
    MATERNAL = "maternal"
    PATERNAL = "paternal"
    BIPARENTL = "biparental"
    NOT_APPLICABLE = "not applicable"


class ClinicalFeaturesAffectedStatus(Enum):
    PRESENT = "present"
    ABSENT = "absent"
    NOT_TESTED = "not tested"


class ClinicalFeaturesDb(Enum):
    HP = "HP"


class CollectionMethod(Enum):
    CURATION = "curation"
    LITERATURE_ONLY = "literature only"
    REFERENCE_POPULATION = "reference population"
    PROVIDER_INTERPRETATION = "provider interpretation"
    PHENOTYPING_ONLY = "phenotyping only"
    CASE_CONTROL = "case-control"
    CLINICAL_TESTING = "clinical testing"
    IN_VITRO = "in vitro"
    IN_VIVO = "in vivo"
    RESEARCH = "research"
    NOT_PROVIDED = "not provided"


class StructVarMethodType(Enum):
    SNP_ARRAY = "SNP array"
    OLIGO_ARRAY = "Oligo array"
    READ_DEPTH = "Read depth"
    PAIRED_END_MAPPING = "Paired-end mapping"
    ONE_END_ANCHORED_ASSEMBLY = "One end anchored assembly"
    SEQUENCE_ALIGNMENT = "Sequence alignment"
    OPTICAL_MAPPING = "Optical mapping"
    CURATED_PCR = "Curated,PCR"


class ClinicalSignificanceDescription(Enum):
    """Allowed values for the ``clinicalSignificanceDescription`` and
    ``germlineClassificationDescription``.

    The values of the enumeration map to the values used by the ClinVar submission API.
    """

    PATHOGENIC = "Pathogenic"
    LIKELY_PATHOGENIC = "Likely pathogenic"
    UNCERTAIN_SIGNIFICANCE = "Uncertain significance"
    LIKELY_BENIGN = "Likely benign"
    BENIGN = "Benign"
    PATHOGENIC_LOW_PENETRANCE = "Pathogenic, low penetrance"
    UNCERTAIN_RISK_ALLELE = "Uncertain risk allele"
    LIKELY_PATHOGENIC_LOW_PENETRANCE = "Likely pathogenic, low penetrance"
    ESTABLISHED_RISK_ALLELE = "Established risk allele"
    LIKELY_RISK_ALLELE = "Likely risk allele"
    AFFECTED = "affects"
    ASSOCIATION = "association"
    DRUG_RESPONSE = "drug response"
    CONFERS_SENSITIVITY = "confers sensitivity"
    PROTECTIVE = "protective"
    OTHER = "other"
    NOT_PROVIDED = "not provided"


class ModeOfInheritance(Enum):
    AUTOSOMAL_DOMINANT_INHERITANCE = "Autosomal dominant inheritance"
    AUTOSOMAL_RECESSIVE_INHERITANCE = "Autosomal recessive inheritance"
    MITOCHONDRIAL_INHERITANCE = "Mitochondrial inheritance"
    GENETIC_ANTICIPATION = "Genetic anticipation"
    SPORADIC = "Sporadic"
    SEX_LIMITED_AUTOSOMAL_DOMINANT = "Sex-limited autosomal dominant"
    SOMATIC_MUTATION = "Somatic mutation"
    X_LINKED_RECESSIVE_INHERITANCE = "X-linked recessive inheritance"
    X_LINKED_DOMINANT_INHERITANCE = "X-linked dominant inheritance"
    Y_LINKED_INHERITANCE = "Y-linked inheritance"
    OTHER = "Other"
    X_LINKED_INHERITANCE = "X-linked inheritance"
    CODOMINANT = "Codominant"
    DEMIDOMINANT_INHERITANCE = "Semidominant inheritance"
    AUTOSOMAL_UNKNOWN = "Autosomal unknown"
    AUTOSOMAL_DOMINANT_INHERITANCE_WITH_MATERNAL_IMPRINTING = (
        "Autosomal dominant inheritance with maternal imprinting"
    )
    AUTOSOMAL_DOMINANT_INHERITANCE_WITH_PATERNAL_IMPRINTING = (
        "Autosomal dominant inheritance with paternal imprinting"
    )
    MULTIFACTORIAL_INHERITANCE = "Multifactorial inheritance"
    UNKNOWN_MECHANISM = "Unknown mechanism"
    OLIGOGENIC_INHERITANCE = "Oligogenic inheritance"


class OncogenicityClassificationDescription(Enum):
    ONCOGENIC = "Oncogenic"
    LIKELY_ONCOGENIC = "Likely Oncogenic"
    UNCERTAIN_SIGNIFICANCE = ("Uncertain significance",)
    LIKELY_BENIGN = ("Likely benign",)
    BENIGN = "Benign"


class SomaticClinicalImpactClassificationDescription(Enum):
    STRONG = "Tier I - Strong"
    POTENTIAL = "Tier II - Potential"
    UNKNOWN = "Tier III - Unknown"
    BENIGN_LIKELY_BENIGN = "Tier IV - Benign/Likely benign"


class PresenceOfSomaticVariantInNormalTissue(Enum):
    PRESENT = "present"
    ABSENT = "absent"
    NOT_TESTED = "not tested"


class SomaticClinicalImpactAssertionType(Enum):
    THERAPEUTIC_SENSITIVITY_RESPONSE = "therapeutic: sensitivity/response"
    THERAPEUTIC_RESISTANCE = "therapeutic: resistance"
    THERAPEUTIC_REDUCED_SENSITIVITY = "therapeutic: reduced sensitivity"
    DIAGNOSTIC_SUPPORTS_DIAGNOSIS = "diagnostic: supports diagnosis"
    DIAGNOSTIC_EXCLUDES_DIAGNOSIS = "diagnostic: excludes diagnosis"
    PROGNOSTIC_BETTER_OUTCOME = "prognostic: better outcome"
    PROGNOSTIC_POOR_OUTCOME = "prognostic: poor outcome"


class RecordStatus(Enum):
    NOVEL = "novel"
    UPDATE = "update"


class ReleaseStatus(Enum):
    PUBLIC = "public"
    HOLD_UNTIL_PUBLISHED = "hold until published"


class SubmissionClinvarDeletionAccessionSet(BaseModel):
    model_config = ConfigDict(frozen=True)

    accession: str
    reason: typing.Optional[str] = None


class SubmissionClinvarDeletion(BaseModel):
    model_config = ConfigDict(frozen=True)

    accessionSet: typing.List[SubmissionClinvarDeletionAccessionSet]


class SubmissionChromosomeCoordinates(BaseModel):
    model_config = ConfigDict(frozen=True)

    alternateAllele: typing.Optional[str] = None
    accession: typing.Optional[str] = None
    assembly: typing.Optional[Assembly] = None
    chromosome: typing.Optional[Chromosome] = None
    innerStart: typing.Optional[int] = None
    innerStop: typing.Optional[int] = None
    outerStart: typing.Optional[int] = None
    outerStop: typing.Optional[int] = None
    referenceAllele: typing.Optional[str] = None
    start: typing.Optional[int] = None
    stop: typing.Optional[int] = None
    variantLength: typing.Optional[int] = None


class SubmissionVariantGene(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: typing.Optional[int] = None
    symbol: typing.Optional[str] = None


class SubmissionVariant(BaseModel):
    model_config = ConfigDict(frozen=True)

    chromosomeCoordinates: typing.Optional[SubmissionChromosomeCoordinates] = None
    copyNumber: typing.Optional[str] = None
    gene: typing.Optional[typing.List[SubmissionVariantGene]] = None
    hgvs: typing.Optional[str] = None
    referenceCopyNumber: typing.Optional[int] = None
    variantType: typing.Optional[VariantType] = None


class SubmissionVariantSet(BaseModel):
    model_config = ConfigDict(frozen=True)

    variant: typing.List[SubmissionVariant]


class SubmissionPhaseUnknownSet(BaseModel):
    model_config = ConfigDict(frozen=True)

    hgvs: str
    variants: typing.List[SubmissionVariant]


class SubmissionClinicalFeature(BaseModel):
    model_config = ConfigDict(frozen=True)

    clinicalFeaturesAffectedStatus: ClinicalFeaturesAffectedStatus
    db: typing.Optional[ClinicalFeaturesDb] = None
    id: typing.Optional[str] = None
    name: typing.Optional[str] = None


class _SubmissionObservedInBase(BaseModel):
    """Base observation type."""

    model_config = ConfigDict(frozen=True)

    affectedStatus: AffectedStatus
    alleleOrigin: AlleleOrigin
    collectionMethod: CollectionMethod
    clinicalFeatures: typing.Optional[typing.List[SubmissionClinicalFeature]] = None
    clinicalFeaturesComment: typing.Optional[str] = None
    numberOfIndividuals: typing.Optional[int] = None
    structVarMethodType: typing.Optional[StructVarMethodType] = None


class SubmissionObservedInGermline(_SubmissionObservedInBase):
    model_config = ConfigDict(frozen=True)


class SubmissionObservedInSomatic(_SubmissionObservedInBase):
    model_config = ConfigDict(frozen=True)

    presenceOfSomaticVariantInNormalTissue: typing.Optional[
        PresenceOfSomaticVariantInNormalTissue
    ] = None
    somaticVariantAlleleFraction: typing.Optional[float] = None


class SubmissionHaplotypeSet(BaseModel):
    model_config = ConfigDict(frozen=True)

    hgvs: str
    variants: typing.List[SubmissionVariant]
    starAlleleName: typing.Optional[str] = None


class SubmissionDistinctChromosomesSet(BaseModel):
    model_config = ConfigDict(frozen=True)

    hgvs: str
    #: Hast at least two elements
    variants: typing.List[SubmissionVariant]


class SubmissionHaplotypeSets(BaseModel):
    model_config = ConfigDict(frozen=True)

    haplotypeSet: typing.Optional[SubmissionHaplotypeSet] = None
    haplotypeSingleVariantSet: typing.Optional[SubmissionHaplotypeSet] = None


class SubmissionDiplotypeSet(BaseModel):
    model_config = ConfigDict(frozen=True)

    haplotypeSets: typing.List[SubmissionHaplotypeSets]
    hgvs: str
    starAlleleName: typing.Optional[str] = None


class SubmissionCitation(BaseModel):
    model_config = ConfigDict(frozen=True)

    db: typing.Optional[CitationDb] = None
    id: typing.Optional[str] = None
    url: typing.Optional[str] = None


class SubmissionAssertionCriteria(BaseModel):
    model_config = ConfigDict(frozen=True)

    db: typing.Optional[CitationDb] = None
    id: typing.Optional[str] = None
    url: typing.Optional[str] = None


class SubmissionCondition(BaseModel):
    model_config = ConfigDict(frozen=True)

    db: typing.Optional[ConditionDb] = None
    id: typing.Optional[str] = None
    name: typing.Optional[str] = None


class SubmissionDrugResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    db: typing.Optional[ConditionDb] = None
    drugName: typing.Optional[str] = None
    id: typing.Optional[str] = None
    condition: typing.Optional[typing.List[SubmissionCondition]] = None


class SubmissionConditionSetGermline(BaseModel):
    model_config = ConfigDict(frozen=True)

    condition: typing.Optional[typing.List[SubmissionCondition]] = None
    drugResponse: typing.Optional[typing.List[SubmissionDrugResponse]] = None
    multipleConditionExplanation: typing.Optional[MultipleConditionExplanation] = None


class SubmissionConditionSetSomatic(BaseModel):
    model_config = ConfigDict(frozen=True)

    condition: typing.List[SubmissionCondition]
    drugResponse: typing.Optional[typing.List[SubmissionDrugResponse]] = None
    multipleConditionExplanation: typing.Optional[MultipleConditionExplanation] = None


class SubmissionCompoundHeterozygoteSetVariantSet(BaseModel):
    model_config = ConfigDict(frozen=True)

    variantSet: typing.Optional[SubmissionVariantSet] = None


class SubmissionCompoundHeterozygoteSet(BaseModel):
    model_config = ConfigDict(frozen=True)

    hgvs: str
    # Must have two entries
    variantSets: typing.List[SubmissionCompoundHeterozygoteSetVariantSet]


class _SubmissionClinicalSignificanceBase(BaseModel):
    """Base class for clinical significance evaluation."""

    model_config = ConfigDict(frozen=True)

    citation: typing.Optional[typing.List[SubmissionCitation]] = None
    comment: typing.Optional[str] = None
    dateLastEvaluated: typing.Optional[str] = None


class SubmissionClinicalSignificance(_SubmissionClinicalSignificanceBase):
    model_config = ConfigDict(frozen=True)

    clinicalSignificanceDescription: ClinicalSignificanceDescription
    customAssertionScore: typing.Optional[float] = None
    explanationOfDrugResponse: typing.Optional[str] = None
    explanationOfOtherClinicalSignificance: typing.Optional[str] = None
    modeOfInheritance: typing.Optional[ModeOfInheritance] = None


class _SubmissionClinvarSubmissionBase(BaseModel):
    """Base class for ClinVar submissions."""

    model_config = ConfigDict(frozen=True)

    recordStatus: RecordStatus

    clinvarAccession: typing.Optional[str] = None
    compoundHeterozygoteSet: typing.Optional[SubmissionCompoundHeterozygoteSet] = None
    diplotypeSet: typing.Optional[SubmissionDiplotypeSet] = None
    distinctChromosomesSet: typing.Optional[SubmissionDistinctChromosomesSet] = None
    #: Has at least two elements in `variants`
    haplotypeSet: typing.Optional[SubmissionHaplotypeSet] = None
    #: Has exactly one elements in `variants`
    haplotypeSingleVariantSet: typing.Optional[SubmissionHaplotypeSet] = None
    localID: typing.Optional[str] = None
    localKey: typing.Optional[str] = None
    variantSet: typing.Optional[SubmissionVariantSet] = None
    phaseUnknownSet: typing.Optional[SubmissionPhaseUnknownSet] = None


class SubmissionClinvarSubmission(_SubmissionClinvarSubmissionBase):
    """Old format of ClinVar submission.

    The 2024 ClinVar has split germline, somatic clinical impact, and somatic
    oncogenicity submission.
    """

    model_config = ConfigDict(frozen=True)

    clinicalSignificance: SubmissionClinicalSignificance
    conditionSet: SubmissionConditionSetGermline
    observedIn: typing.List[SubmissionObservedInGermline]


class SomaticClinicalImpactClassification(_SubmissionClinicalSignificanceBase):
    """Details of somatic clinical impact classification."""

    clinicalImpactClassificationDescription: SomaticClinicalImpactClassificationDescription
    assertionTypeForClinicalImpact: typing.Optional[SomaticClinicalImpactAssertionType] = None
    drugForTherapeuticAssertion: typing.Optional[str] = None


class SubmissionClinicalImpactSubmission(_SubmissionClinvarSubmissionBase):
    """Submission relating to somatic clinical impact."""

    clinicalImpactClassification: SomaticClinicalImpactClassification
    conditionSet: SubmissionConditionSetSomatic
    observedIn: typing.List[SubmissionObservedInSomatic]


class SomaticOncogenicityClassification(_SubmissionClinicalSignificanceBase):
    """Details of somatic oncogenicity classification."""

    oncogenicityClassificationDescription: OncogenicityClassificationDescription


class SubmissionOncogenicitySubmission(_SubmissionClinvarSubmissionBase):
    """Submission relating to somatic clinical impact."""

    oncogenicityClassification: SomaticOncogenicityClassification
    conditionSet: SubmissionConditionSetSomatic
    observedIn: typing.List[SubmissionObservedInSomatic]


class GermlineClassification(_SubmissionClinicalSignificanceBase):
    model_config = ConfigDict(frozen=True)

    germlineClassificationDescription: ClinicalSignificanceDescription
    modeOfInheritance: ModeOfInheritance
    customClassificationScore: typing.Optional[float] = None
    explanationOfDrugResponse: typing.Optional[str] = None
    explanationOfOtherClassification: typing.Optional[str] = None


class SubmissionGermlineSubmission(_SubmissionClinvarSubmissionBase):
    """Submission relating to somatic clinical impact."""

    germlineClassification: GermlineClassification
    conditionSet: SubmissionConditionSetGermline
    observedIn: typing.List[SubmissionObservedInGermline]


class SubmissionContainer(BaseModel):
    """Representation of the container for a submission."""

    model_config = ConfigDict(frozen=True)

    assertionCriteria: typing.Optional[SubmissionAssertionCriteria] = None
    behalfOrgID: typing.Optional[int] = None
    clinvarDeletion: typing.Optional[SubmissionClinvarDeletion] = None
    #: The "old format" ClinVar submission, mutually exclusive with
    #: "clinicalImpactSubmission", "oncogenicitySubmission", and "germlineSubmission".
    clinvarSubmission: typing.Optional[typing.List[SubmissionClinvarSubmission]] = None
    #: ClinVar Submission Set for germline variants
    germlineSubmission: typing.Optional[typing.List[SubmissionGermlineSubmission]] = None
    #: ClinVar Submission Set for somatic variants with oncogenicityClassification.
    oncogenicitySubmission: typing.Optional[typing.List[SubmissionOncogenicitySubmission]] = None
    #: ClinVar Submission Set for somatic variants with clinicalImpactClassification.
    clinicalImpactSubmission: typing.Optional[typing.List[SubmissionClinicalImpactSubmission]] = (
        None
    )
    clinvarSubmissionReleaseStatus: typing.Optional[ReleaseStatus] = None
    submissionName: typing.Optional[str] = None
