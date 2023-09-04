"""Support for representing ClinVar data from XSD file using attrs."""

import datetime
import enum
import typing

import attrs
from dateutil.parser import parse as parse_datetime

T = typing.TypeVar("T")


def force_list(value: typing.Union[T, typing.List[T]]) -> typing.List[T]:
    """Helper value that wraps atomic values in a list."""
    if isinstance(value, list):
        return value
    else:
        return [value]


@enum.unique
class ClinVarAccessionType(enum.Enum):
    """ClinVar accession type"""

    RCV = "RCV"


@enum.unique
class RecordStatus(enum.Enum):
    """Enumeration with ``ClinVarSet.record_status`."""

    CURRENT = "current"
    REPLACED = "replaced"
    REMOVED = "removed"


@enum.unique
class Status(enum.Enum):
    """Corresponds to ``typeStatus``."""

    CURRENT = "current"
    COMPLETED_AND_RETIRED = "completed and retired"
    DELETE = "delete"
    IN_DEVELOPMENT = "in development"
    RECLASSIFIED = "reclassified"
    REJECT = "reject"
    SECONDARY = "secondary"
    SUPPRESSED = "suppressed"
    UNDER_REVIEW = "under review"


@attrs.frozen(auto_attribs=True)
class XrefType:
    """This structure is used to represent how an object described in the submission relates to
    objects in other databases.
    """

    #: The database name
    db: str
    #: The ID of the xref
    id: str
    #: Optional type of the xref
    type: typing.Optional[str] = None
    #: Optional URL of the xref
    url: typing.Optional[str] = None
    #: Optional status of the xref
    status: typing.Optional[Status] = None

    @classmethod
    def from_json_data(cls, json_data: dict) -> "XrefType":
        return cls(
            db=json_data["@DB"],
            id=json_data["@ID"],
            type=json_data.get("@Type"),
            url=json_data.get("@URL"),
            status=Status(json_data["@Status"]) if json_data.get("@Status") else None,
        )


@enum.unique
class ReviewStatus(enum.Enum):
    """The values of review status are used to build the 'star ratings' displayed on the
    ClinVar public site.

    - 0 stars:  a conflict or not classified by submitter
    - 1 star: classified by single submitter
    - 2 stars: classified by multiple submitters
    - 3 stars: reviewed by expert panel
    - 4 stars: reviewed by professional society
    """

    NO_ASSERTION_PROVIDED = "no assertion provided"
    NO_ASSERTION_CRITERIA_PROVIDED = "no assertion criteria provided"
    CRITERIA_PROVIDED_SINGLE_SUBMITTER = "criteria provided, single submitter"
    CRITERIA_PROVIDED_MULTIPLE_SUBMITTERS = "criteria provided, multiple submitters, no conflicts"
    CRITERIA_PROVIDED_CONFLICTING_INTERPRETATIONS = "criteria provided, conflicting interpretations"
    REVIEWED_BY_EXPERT_PANEL = "reviewed by expert panel"
    PRACTICE_GUIDELINE = "practice guideline"


@enum.unique
class ClinicalSignificanceDescription(enum.Enum):
    """Allowed values for clinical significance description."""

    AFFECTS = "affects"
    BENIGN = "benign"
    ESTABLISHED_RISK_ALLELE = "established risk allele"
    LIKELY_BENIGN = "likely benign"
    LIKELY_PATHOGENIC = "likely pathogenic"
    LIKELY_PATHOGENIC_LOW_PENETRANCE = "likely pathogenic, low penetrance"
    LIKELY_RISK_ALLELE = "likely risk allele"
    PATHOGENIC = "pathogenic"
    PATHOGENIC_LOW_PENETRANCE = "pathogenic, low penetrance"
    UNCERTAIN_RISK_ALLELE = "uncertain risk allele"
    UNCERTAIN_SIGNIFICANCE = "uncertain significance"
    ASSOCIATION = "association"
    ASSOCIATION_NOT_FOUND = "association not found"
    CONFERS_SENSITIVITY = "confers sensitivity"
    CONFLICTING_DATA_FROM_SUBMITTERS = "conflicting data from submitters"
    DRUG_RESPONSE = "drug response"
    NOT_PROVIDED = "not provided"
    OTHER = "other"
    PROTECTIVE = "protective"
    RISK_FACTOR = "risk factor"

    @classmethod
    def from_the_wild(cls, str) -> "ClinicalSignificanceDescription":
        try:
            return cls(str)
        except ValueError:
            return cls.OTHER


@enum.unique
class CommentType(enum.Enum):
    """Types of comments."""

    PUBLIC = "public"
    CONVERTED_BY_NCBI = "ConvertedByNCBI"
    MISSING_FROM_ASSEMBLY = "MissingFromAssembly"
    GENOMIC_LOCATION_NOT_ESTABLISHED = "GenomicLocationNotEstablished"
    LOCATION_ON_GENOME_AND_PRODUCT_NOT_ALIGNED = "LocationOnGenomeAndProductNotAligned"
    DELETION_COMMENT = "DeletionComment"
    MERGE_COMMENT = "MergeComment"
    ASSEMBLY_SPECIFIC_ALLELE_DEFINITON = "AssemblySpecificAlleleDefinition"
    ALIGNMENT_GAP_MAKES_APPEAR_INCONSISTENT = "AlignmentGapMakesAppearInconsistent"
    EXPLANATION_OF_INTERPRETATION = "ExplanationOfInterpretation"


@attrs.frozen(auto_attribs=True)
class Comment:
    """A structure to support reporting unformatted content."""

    #: The comment's content.
    text: str
    #: An optional type of the comment.
    type: typing.Optional[CommentType] = None
    #: An optional datasource name.
    datasource: typing.Optional[str] = None

    @classmethod
    def from_json_data(cls, json_data: typing.Union[str, dict]) -> "Comment":
        if isinstance(json_data, str):
            return cls(text=json_data)
        else:
            return cls(
                type=CommentType(json_data["@Type"]) if json_data.get("@Type") else None,
                datasource=json_data.get("@Datasource"),
                text=json_data["#text"],
            )


@attrs.frozen(auto_attribs=True)
class CitationIdentifier:
    #: The identifier source.
    source: str
    #: The identifier value.
    value: str

    @classmethod
    def from_json_data(cls, json_data: dict) -> "CitationIdentifier":
        return cls(
            source=json_data["@Source"],
            value=json_data["#text"],
        )


@attrs.frozen(auto_attribs=True)
class Citation:
    """Type for a citation"""

    #: Citation identifiers.
    identifiers: typing.List[CitationIdentifier] = attrs.field(factory=list)
    #: Citation type.
    type: typing.Optional[str] = None
    #: Corresponds to the abbreviation reported by GTR
    abbrev: typing.Optional[str] = None
    #: Optional citation URL
    url: typing.Optional[str] = None
    #: Optional citation text.
    citation_text: typing.Optional[str] = None

    @classmethod
    def from_json_data(cls, json_data: dict) -> "Citation":
        return cls(
            identifiers=[
                CitationIdentifier.from_json_data(raw_identifier)
                for raw_identifier in force_list(json_data.get("ID", []))
            ],
            type=json_data.get("@Type"),
            abbrev=json_data.get("@Abbrev"),
            url=json_data.get("@URL"),
            citation_text=json_data.get("CitationText"),
        )


@enum.unique
class AssertionTypeSCV(enum.Enum):
    """The assertion types available for SCV records."""

    VARIATION_TO_DISEASE = "variation to disease"
    VARIATION_IN_MODIFIER_GENE_TO_DISEASE = "variation in modifier gene to disease"
    CONFERS_SENSITIVITY = "confers sensitivity"
    CONFERS_RESISTANCE = "confers resistance"
    VARIANT_TO_NAMED_PROTEIN_EFFECT = "variant to named protein"
    VARIATION_TO_INCLUDED_DISEASE = "variation to included disease"


@attrs.frozen(auto_attribs=True)
class CustomAssertionScore:
    value: float
    type: typing.Optional[str] = None

    @classmethod
    def from_json_data(cls, json_data: dict) -> "CustomAssertionScore":
        return cls(
            value=float(json_data["@Value"]),
            type=json_data.get("@Type"),
        )


@attrs.frozen(auto_attribs=True)
class ClinicalSignificanceSCV:
    """The clinical significance from the SCV."""

    #: The review status
    review_status: typing.Optional[ReviewStatus] = None
    #: We are not providing an enumeration for the values we report for clinical significance within the xsd.
    #: The values are maintained here: ftp://ftp.ncbi.nlm.nih.gov/pub/GTR/standard_terms/Clinical_significance.txt.
    descriptions: typing.List[ClinicalSignificanceDescription] = attrs.field(factory=list)
    #: Explanation is used only when the description is 'conflicting data from submitters'.
    #: The element summarizes the conflict.
    explanation: typing.Optional[Comment] = None
    #: Explanation for interpretation.
    explanation_of_interpretation: typing.Optional[str] = None
    #: Custom asertion scores.
    custom_assertion_score: typing.List[CustomAssertionScore] = attrs.field(factory=list)
    #: Cross-references.
    xrefs: typing.List[XrefType] = attrs.field(factory=list)
    #: Citations
    citations: typing.List[Citation] = attrs.field(factory=list)
    #: Comments.
    comments: typing.List[Comment] = attrs.field(factory=list)
    #: Date of last evaluation.
    date_last_evaluated: typing.Optional[datetime.date] = None

    @classmethod
    def from_json_data(cls, json_data: dict) -> "ClinicalSignificanceSCV":
        # Handle case of the following::
        #
        #     <ReviewStatus xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">\
        #     criteria provided, single submitter</ReviewStatus>
        #
        # In contrast to::
        #
        #     <ReviewStatus>criteria provided, single submitter</ReviewStatus>
        if "ReviewStatus" in json_data:
            if isinstance(json_data["ReviewStatus"], str):
                review_status = json_data["ReviewStatus"]
            else:
                review_status = json_data["ReviewStatus"]["#text"]
        elif "@ReviewStatus" in json_data:
            review_status = json_data["@ReviewStatus"]
        else:
            review_status = None

        descriptions = []
        for raw_description in force_list(json_data.get("Description", [])):
            if isinstance(raw_description, str):
                value = raw_description
            else:
                value = raw_description.get("#text")
            if value:
                descriptions.append(ClinicalSignificanceDescription(raw_description.lower()))
                break
        else:  # did not break out of for loop above
            if "@Description" in json_data:
                descriptions.append(ClinicalSignificanceDescription(json_data.get["@Description"]))

        return cls(
            review_status=review_status,
            descriptions=descriptions,
            explanation=Comment.from_json_data(json_data.get("Explanation"))
            if json_data.get("Explanation")
            else None,
            explanation_of_interpretation=json_data.get("ExplanationOfInterpretation"),
            custom_assertion_score=[
                CustomAssertionScore(
                    value=float(raw_score["#text"]),
                    type=raw_score.get("@Type"),
                )
                for raw_score in force_list(json_data.get("CustomAssertionScore", []))
            ],
            xrefs=[
                XrefType.from_json_data(raw_xref)
                for raw_xref in force_list(json_data.get("XRef", []))
            ],
            citations=[
                Citation.from_json_data(raw_citation)
                for raw_citation in force_list(json_data.get("Citation", []))
            ],
            comments=[
                Comment.from_json_data(raw_comment)
                for raw_comment in force_list(json_data.get("Comment", []))
            ],
            date_last_evaluated=parse_datetime(
                json_data["@DateLastEvaluated"],
            ).date()
            if json_data.get("@DateLastEvaluated")
            else None,
        )


@attrs.frozen(auto_attribs=True)
class ClinicalSignificance:
    """The clinical significance from the RCV."""

    #: The review status
    review_status: typing.Optional[ReviewStatus] = None
    #: We are not providing an enumeration for the values we report for clinical significance within the xsd.
    #: The values are maintained here: ftp://ftp.ncbi.nlm.nih.gov/pub/GTR/standard_terms/Clinical_significance.txt.
    description: typing.Optional[ClinicalSignificanceDescription] = None
    #: Explanation is used only when the description is 'conflicting data from submitters'.
    #: The element summarizes the conflict.
    explanation: typing.Optional[Comment] = None
    #: Explanation for interpretation.
    explanation_of_interpretation: typing.Optional[str] = None
    #: Cross-references.
    xrefs: typing.List[XrefType] = attrs.field(factory=list)
    #: Citations
    citations: typing.List[Citation] = attrs.field(factory=list)
    #: Comments.
    comments: typing.List[Comment] = attrs.field(factory=list)
    #: Date of last evaluation.
    date_last_evaluated: typing.Optional[datetime.date] = None

    @classmethod
    def from_json_data(cls, json_data: dict) -> "ClinicalSignificanceSCV":
        # Handle case of the following::
        #
        #     <ReviewStatus xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">\
        #     criteria provided, single submitter</ReviewStatus>
        #
        # In contrast to::
        #
        #     <ReviewStatus>criteria provided, single submitter</ReviewStatus>
        if "ReviewStatus" in json_data:
            if isinstance(json_data["ReviewStatus"], str):
                review_status = json_data["ReviewStatus"]
            else:
                review_status = json_data["ReviewStatus"]["#text"]
        elif "@ReviewStatus" in json_data:
            review_status = json_data["@ReviewStatus"]
        else:
            review_status = None

        return cls(
            review_status=review_status,
            description=json_data.get("Description"),
            explanation=Comment.from_json_data(json_data.get("Explanation"))
            if json_data.get("Explanation")
            else None,
            explanation_of_interpretation=json_data.get("ExplanationOfInterpretation"),
            xrefs=[
                XrefType.from_json_data(raw_xref)
                for raw_xref in force_list(json_data.get("XRef", []))
            ],
            citations=[
                Citation.from_json_data(raw_citation)
                for raw_citation in force_list(json_data.get("Citation", []))
            ],
            comments=[
                Comment.from_json_data(raw_comment)
                for raw_comment in force_list(json_data.get("Comment", []))
            ],
            date_last_evaluated=parse_datetime(
                json_data["@DateLastEvaluated"],
            ).date()
            if json_data.get("@DateLastEvaluated")
            else None,
        )


@attrs.frozen(auto_attribs=True)
class ClinVarAccession:
    #: The accession assigned by ClinVar
    acc: str
    #: A new version of an SCV accession is assigned with an update from the submitter.
    #: A new version of an RCV accession is assigned when the set of ClinVarAssertions is
    #: changed, either by a change in version or by addition of a new submission.
    version: int
    #: The accession type
    type: ClinVarAccessionType
    #: Date of previous update
    date_updated: datetime.date
    #: Date of record creation.
    date_created: datetime.date

    @classmethod
    def from_json_data(cls, json_data: dict) -> "ClinVarAccession":
        return cls(
            acc=json_data["@Acc"],
            version=int(json_data["@Version"]),
            type=ClinVarAccessionType(json_data["@Type"]),
            date_updated=parse_datetime(json_data["@DateUpdated"]).date(),
            date_created=parse_datetime(json_data["@DateCreated"]).date(),
        )


@enum.unique
class ReferenceClinVarAssertionAttribute(enum.Enum):
    MODE_OF_INHERITANCE = "ModeOfInheritance"
    PENETRANCE = "Penetrance"
    AGE_OF_ONSET = "AgeOfOnset"


@attrs.frozen(auto_attribs=True)
class ReferenceClinVarAssertionAttribute:
    """Many concepts in the database are represented by what ClinVar terms an AttributeSet,
    which is an open-ended structure providing the equivalent of a type of information,
    the value(s) for that data type, submitter(s), free text comment(s) describing that attribute,
    identifier(s) for that attribute, and citation(s) related to that attribute.
    """

    type: ReferenceClinVarAssertionAttribute
    integer_value: typing.Optional[int] = None
    date_value: typing.Optional[datetime.date] = None
    citations: typing.List[Citation] = attrs.field(factory=list)
    xrefs: typing.List[XrefType] = attrs.field(factory=list)
    comments: typing.List[Comment] = attrs.field(factory=list)

    @classmethod
    def from_json_data(cls, json_data: dict) -> "ReferenceClinVarAssertionAttribute":
        return cls(
            type=ReferenceClinVarAssertionAttribute(json_data["@Type"]),
            integer_value=int(json_data["@integerValue"])
            if json_data.get("@integerValue")
            else None,
            date_value=parse_datetime(json_data["@dateValue"]).date()
            if json_data.get("@dateValue")
            else None,
            citations=[
                Citation.from_json_data(raw_citation)
                for raw_citation in force_list(json_data.get("Citation", []))
            ],
            xrefs=[
                XrefType.from_json_data(raw_xref)
                for raw_xref in force_list(json_data.get("XRef", []))
            ],
            comments=[
                Comment.from_json_data(raw_comment)
                for raw_comment in force_list(json_data.get("Comment", []))
            ],
        )


@enum.unique
class Zygosity(enum.Enum):
    HOMOZYGOTE = "Homozygote"
    SINGLE_HETEROZYGOTE = "SingleHeterozygote"
    COMPOUND_HETEROZYGOTE = "CompoundHeterozygote"
    HEMIZYGOTE = "Hemizygote"
    NOT_PROVIDED = "not provided"


@enum.unique
class RelativeOrientation(enum.Enum):
    CIS = "cis"
    TRANS = "trans"
    UNKNOWN = "unknown"


@attrs.frozen(auto_attribs=True)
class AlleleDescription:
    """This is to be used within co-occurrence set"""

    name: str
    relative_orientation: typing.Optional[RelativeOrientation]
    zygosity: typing.Optional[Zygosity] = None
    clinical_significance: typing.Optional[ClinicalSignificanceSCV] = None

    @classmethod
    def from_json_data(cls, json_data: dict) -> "AlleleDescription":
        return cls(
            name=json_data["@Name"],
            relative_orientation=RelativeOrientation(json_data["@RelativeOrientation"])
            if json_data.get("@RelativeOrientation")
            else None,
            zygosity=Zygosity(json_data["@Zygosity"]) if json_data.get("@Zygosity") else None,
            clinical_significance=ClinicalSignificanceSCV.from_json_data(
                json_data.get("ClinicalSignificance")
            )
            if json_data.get("ClinicalSignificance")
            else None,
        )


@attrs.frozen(auto_attribs=True)
class Coocurrence:
    """This refers to the zygosity of the variant being asserted."""

    zygosity: typing.Optional[Zygosity] = None
    allele_descriptions: typing.List[AlleleDescription] = attrs.field(factory=list)
    count: typing.Optional[int] = None

    @classmethod
    def from_json_data(cls, json_data: dict) -> "Coocurrence":
        return cls(
            zygosity=Zygosity(json_data["@Zygosity"]) if json_data.get("@Zygosity") else None,
            allele_descriptions=[
                AlleleDescription.from_json_data(raw_allele_description)
                for raw_allele_description in force_list(json_data.get("AlleleDescription", []))
            ],
            count=int(json_data["@Count"]) if json_data.get("@Count") else None,
        )


@enum.unique
class ObservationMethod(enum.Enum):
    CURATION = "curation"
    LITERATURE_ONLY = "literature only"
    REFERENCE_POPULATION = "reference population"
    RE_INTERPRETATION = "re-interpretation"
    CASE_CONTROL = "case-control"
    CLINICAL_TESTING = "clinical testing"
    IN_VITRO = "in vitro"
    IN_VIVO = "in vivo"
    INFERRED_FROM_SOURCE = "inferred from source"
    RESEARCH = "research"
    NOT_PROVIDED = "not provided"
    OTHER = "other"

    @classmethod
    def from_the_wild(cls, str) -> "ObservationMethod":
        try:
            return cls(str)
        except ValueError:
            return cls.OTHER


@enum.unique
class ObservedDataAttributeType(enum.Enum):
    DESCRIPTION = "Description"
    VARIANT_ALLELES = "VariantAlleles"
    SUBJECTS_WITH_VARIANT = "SubjectsWithVariant"
    SUBJECTS_WITH_DIFFERENT_CAUSATIVE_VARIANT = "SubjectsWithDifferentCausativeVariant"
    VARIANT_CHROMOSOMES = "VariantChromosomes"
    INDEPENDENT_OBSERVATIONS = "IndependentObservations"
    SINGLE_HETEROZYGOTE = "SingleHeterozygote"
    COMPOUND_HETEROZYGOTE = "CompoundHeterozygote"
    HOMOZYGOTE = "Homozygote"
    HEMIZYGOTE = "Hemizygote"
    NUMBER_MOSAIC = "NumberMosaic"
    OBSERVED_UNSPECIFIED = "ObservedUnspecified"
    ALLELE_FREQUENCY = "AlleleFrequency"
    SECONDARY_FINDING = "SecondaryFinding"
    GENOTYPE_AND_MOI_CONSISTENT = "GenotypeAndMOIConsistent"
    UNAFFECTED_FAMILY_MEMBER_WITH_CAUSATIVE_VARIANT = "UnaffectedFamilyMemberWithCausativeVariant"
    HET_PARENT_TRANSMIT_NORMAL_ALLELE = "HetParentTransmitNormalAllele"
    COSEGREGATING_FAMILY = "CosegregatingFamilies"
    INFORMATIVE_MEIOSES = "InformativeMeioses"
    SAMPLE_LOCAL_ID = "SampleLocalID"
    SAMPLE_VARIANT_ID = "SampleVariantID"
    FAMILY_HISTORY = "FamilyHistory"
    NUM_FAMILIES_WITH_VARIANT = "NumFamiliesWithVariant"
    NUM_FAMILIES_WITH_SEGREGATION_OBSERVED = "NumFamiliesWithSegregationObserved"
    SEGREGATION_OBSERVED = "SegregationObserved"


@attrs.frozen(auto_attribs=True)
class ObservedDataAttribute:
    type: ObservedDataAttributeType
    value: typing.Optional[str] = None
    integer_value: typing.Optional[int] = None
    date_value: typing.Optional[datetime.date] = None

    @classmethod
    def from_json_data(cls, json_data: dict) -> "ObservedDataAttribute":
        return cls(
            type=ObservedDataAttributeType(json_data["@Type"]),
            value=json_data.get("#text"),
            integer_value=int(json_data["@integerValue"])
            if json_data.get("@integerValue")
            else None,
            date_value=parse_datetime(json_data["@dateValue"]).date()
            if json_data.get("@dateValue")
            else None,
        )


@enum.unique
class Severity(enum.Enum):
    MILD = "mild"
    MODERATE = "moderate"
    SEVERE = "severe"


@attrs.frozen(auto_attribs=True)
class ObservedData:
    attribute: ObservedDataAttribute
    severity: typing.Optional[Severity] = None
    citations: typing.List[Citation] = attrs.field(factory=list)
    xrefs: typing.List[XrefType] = attrs.field(factory=list)
    comments: typing.List[Comment] = attrs.field(factory=list)

    @classmethod
    def from_json_data(cls, json_data: dict) -> "ObservedData":
        return cls(
            attribute=ObservedDataAttribute.from_json_data(json_data["Attribute"]),
            severity=Severity(json_data["@Severity"]) if json_data.get("@Severity") else None,
            citations=[
                Citation.from_json_data(raw_citation)
                for raw_citation in force_list(json_data.get("Citation", []))
            ],
            xrefs=[
                XrefType.from_json_data(raw_xref)
                for raw_xref in force_list(json_data.get("XRef", []))
            ],
            comments=[
                Comment.from_json_data(raw_comment)
                for raw_comment in force_list(json_data.get("Comment", []))
            ],
        )


@attrs.frozen(auto_attribs=True)
class SampleDescription:
    description: typing.Optional[Comment] = None
    citation: typing.Optional[Citation] = None

    @classmethod
    def from_json_data(cls, json_data: dict) -> "SampleDescription":
        return cls(
            description=Comment.from_json_data(json_data.get("Description"))
            if json_data.get("Description")
            else None,
            citation=Citation.from_json_data(json_data.get("Citation"))
            if json_data.get("Citation")
            else None,
        )


@attrs.frozen(auto_attribs=True)
class FamilyInfo:
    """Structure to describe attributes of any family data in an observation.

    If the details of the number of families and the de-identified pedigree id are not available,
    use FamilyHistory to describe what type of family data is available.  Can also be used to report
    'Yes' or 'No' if there are no more details.
    """

    family_history: typing.Optional[str] = None
    num_families: typing.Optional[int] = None
    num_families_with_variant: typing.Optional[int] = None
    num_families_with_segregation_observed: typing.Optional[int] = None
    pedigree_id: typing.Optional[str] = None
    segregation_observed: typing.Optional[bool] = None

    @classmethod
    def from_json_data(cls, json_data: dict) -> "FamilyInfo":
        return cls(
            family_history=json_data.get("FamilyHistory"),
            num_families=int(json_data["@NumFamilies"]) if json_data.get("@NumFamilies") else None,
            num_families_with_variant=int(json_data["@NumFamiliesWithVariant"])
            if json_data.get("@NumFamiliesWithVariant")
            else None,
            num_families_with_segregation_observed=int(
                json_data["@NumFamiliesWithSegregationObserved"]
            )
            if json_data.get("@NumFamiliesWithSegregationObserved")
            else None,
            pedigree_id=json_data.get("@PedigreeID"),
            segregation_observed=json_data["@SegregationObserved"] == "yes"
            if json_data.get("@SegregationObserved")
            else None,
        )


@enum.unique
class SampleOrigin(enum.Enum):
    GERMLINE = "germline"
    SOMATIC = "somatic"
    DE_NOVO = "de novo"
    UNKNOWN = "unknown"
    NOT_PROVIDED = "not provided"
    INHERITED = "inherited"
    MATERNAL = "maternal"
    PATERNAL = "paternal"
    BIPARENTAL = "biparental"
    NOT_REPORTED = "not reported"
    TESTED_INCONCLUSIVE = "tested-inconclusive"
    NOT_APPLICABLE = "not applicable"
    EXPERIMENTALLY_GENERATED = "experimentally generated"


@attrs.frozen(auto_attribs=True)
class Species:
    value: str
    taxonomy_id: typing.Optional[int] = None

    @classmethod
    def from_json_data(cls, json_data: typing.Union[dict, str]) -> "Species":
        if isinstance(json_data, str):
            return cls(
                value=json_data,
            )
        else:
            return cls(
                value=json_data["#text"],
                taxonomy_id=int(json_data["@TaxonomyId"]),
            )


@enum.unique
class AgeType(enum.Enum):
    MINIMUM = "minimum"
    MAXIMUM = "maximum"
    SINGLE = "single"


@attrs.frozen(auto_attribs=True)
class Age:
    age_unit: str
    value: int
    type: AgeType

    @classmethod
    def from_json_data(cls, json_data: dict) -> "Age":
        return cls(
            age_unit=json_data["@age_unit"],
            value=int(json_data["#text"]),
            type=AgeType(json_data["@Type"]),
        )


@enum.unique
class AffectedStatus(enum.Enum):
    YES = "yes"
    NO = "no"
    NOT_PROVIDED = "not provided"
    UNKNOWN = "unknown"
    NOT_APPLICABLE = "not applicable"


@enum.unique
class Gender(enum.Enum):
    MALE = "male"
    FEMALE = "female"
    MIXED = "mixed"


@enum.unique
class SampleSource(enum.Enum):
    SUBMITTER_GENERATED = "submitter generated"
    DATA_MINING = "data mining"


@enum.unique
class IndicationType(enum.Enum):
    INDICATION = "Indication"


@attrs.frozen(auto_attribs=True)
class ElementValue:
    type: str
    value: str

    @classmethod
    def from_json_data(cls, json_data: dict) -> "ElementValue":
        return cls(
            type=json_data["@Type"],
            value=json_data["#text"],
        )


@attrs.frozen(auto_attribs=True)
class SetElementSetType:
    element_value: ElementValue
    citations: typing.List[Citation] = attrs.field(factory=list)
    xrefs: typing.List[XrefType] = attrs.field(factory=list)
    comments: typing.List[Comment] = attrs.field(factory=list)

    @classmethod
    def from_json_data(cls, json_data: dict) -> "SetElementSetType":
        return cls(
            element_value=ElementValue.from_json_data(json_data["ElementValue"]),
            citations=[
                Citation.from_json_data(raw_citation)
                for raw_citation in force_list(json_data.get("Citation", []))
            ],
            xrefs=[
                XrefType.from_json_data(raw_xref)
                for raw_xref in force_list(json_data.get("XRef", []))
            ],
            comments=[
                Comment.from_json_data(raw_comment)
                for raw_comment in force_list(json_data.get("Comment", []))
            ],
        )


@attrs.frozen(auto_attribs=True)
class AttributeType:
    """The attribute is a general element to represent a defined set of data
        qualified by an enumerated set of types.

    For each attribute element, the value will
    be a character string and is optional. Source shall be used to store identifiers for
    supplied data from source other than the submitter (e.g. SequenceOntology). The data
    submitted where Type="variation" shall be validated against sequence_alternation in
    Sequence Ontology http://www.sequenceontology.org/. This is to be a generic version
    of AttributeType and should be used with extension when it is used to specify Type
    and its enumerations.
    """

    value: str
    integer_value: typing.Optional[int] = None
    date_value: typing.Optional[datetime.date] = None

    @classmethod
    def from_json_data(cls, json_data: dict) -> "AttributeType":
        return cls(
            integerValue=int(json_data["@integerValue"])
            if json_data.get("@integerValue")
            else None,
            dateValue=parse_datetime(json_data["@dateValue"]).date()
            if json_data.get("@dateValue")
            else None,
            value=json_data["#text"],
        )


@enum.unique
class ClinAsserTraitTypeType(enum.Enum):
    DISEASE = "Disease"
    DRUG_RESPONSE = "DrugResponse"
    BLOOD_GROUP = "BloodGroup"
    FINDING = "Finding"
    NAMED_PROTEIN_VARIANT = "NamedProteinVariant"
    PHENOTYPE_INSTRUCTION = "PhenotypeInstruction"


@enum.unique
class ClinicalFeaturesAffectedStatus(enum.Enum):
    PRESENT = "present"
    ABSENT = "absent"
    NOT_TESTED = "not tested"


@enum.unique
class DataSourceTypeType(enum.Enum):
    LABORATORY = "laboratory"
    LSDB = "locus-specific database (LSDB)"
    CONSORTIUM = "consortium"
    RESOURCE = "resource"
    PATIENT_REGISTRY = "patient registry"
    OTHER = "other"


@enum.unique
class TraitRelationshipType(enum.Enum):
    PHENOCOPY = "phenocopy"
    SUBPHENOTYPE = "Subphenotype"
    DRUG_RESPONSE_AND_DIASEASE = "DrugResponseAndDisease"
    CO_OCCURRING_CONDITION = "co-occurring condition"
    FINDING_MEMBER = "finding member"


@attrs.frozen(auto_attribs=True)
class DataSourceType:
    #: A standard term for the source of the information
    data_source: str
    #: The identifier used by the data source
    id: typing.Optional[str] = None
    #: Controlled terms to categorize the source of the information
    source_type: typing.Optional[DataSourceTypeType] = None

    @classmethod
    def from_json_data(cls, json_data: dict) -> "DataSourceType":
        return cls(
            data_source=json_data["@DataSource"],
            id=json_data.get("@ID"),
            source_type=DataSourceTypeType(json_data["@SourceType"])
            if json_data.get("@SourceType")
            else None,
        )


@enum.unique
class ClinVarAssertionAttributeType(enum.Enum):
    MODE_OF_INHERITANCE = "ModeOfInheritance"
    PENETRANCE = "Penetrance"
    AGE_OF_ONSET = "AgeOfOnset"
    SEVERITY = "Severity"
    CLINICAL_SIGNIFICANCE_HISTORY = "ClinicalSignificanceHistory"
    SEVERITY_DESCRIPTION = "SeverityDescription"
    ASSERTION_METHOD = "AssertionMethod"


@attrs.frozen(auto_attribs=True)
class ClinAsserTraitTypeAttribute:
    type: ClinVarAssertionAttributeType
    value: str

    @classmethod
    def from_json_data(cls, json_data: dict) -> "ClinAsserTraitTypeAttribute":
        return cls(
            type=ClinVarAssertionAttributeType(json_data["@Type"]),
            value=json_data["#text"],
        )


@attrs.frozen(auto_attribs=True)
class ClinAsserTraitTypeAttributeSet:
    attribute: ClinAsserTraitTypeAttribute
    citations: typing.List[Citation] = attrs.field(factory=list)
    xrefs: typing.List[XrefType] = attrs.field(factory=list)
    comments: typing.List[Comment] = attrs.field(factory=list)

    @classmethod
    def from_json_data(cls, json_data: dict) -> "ClinAsserTraitTypeAttributeSet":
        return cls(
            attribute=ClinAsserTraitTypeAttribute.from_json_data(json_data["Attribute"]),
            citations=[
                Citation.from_json_data(raw_citation)
                for raw_citation in force_list(json_data.get("Citation", []))
            ],
            xrefs=[
                XrefType.from_json_data(raw_xref)
                for raw_xref in force_list(json_data.get("XRef", []))
            ],
            comments=[
                Comment.from_json_data(raw_comment)
                for raw_comment in force_list(json_data.get("Comment", []))
            ],
        )


@attrs.frozen(auto_attribs=True)
class TraitRelationship:
    type: TraitRelationshipType
    id: typing.Optional[int] = None
    names: typing.List[SetElementSetType] = attrs.field(factory=list)
    symbols: typing.List[SetElementSetType] = attrs.field(factory=list)
    attributes: typing.List[ClinAsserTraitTypeAttributeSet] = attrs.field(factory=list)
    citations: typing.List[Citation] = attrs.field(factory=list)
    xrefs: typing.List[XrefType] = attrs.field(factory=list)
    source: typing.List[DataSourceType] = attrs.field(factory=list)

    @classmethod
    def from_json_data(cls, json_data: dict) -> "TraitRelationship":
        return cls(
            type=TraitRelationshipType(json_data["@Type"]),
            id=int(json_data["@ID"]) if json_data.get("@ID") else None,
            names=[
                SetElementSetType.from_json_data(raw_name)
                for raw_name in force_list(json_data.get("Name", []))
            ],
            symbols=[
                SetElementSetType.from_json_data(raw_symbol)
                for raw_symbol in force_list(json_data.get("Symbol", []))
            ],
            attributes=[
                ClinAsserTraitTypeAttributeSet.from_json_data(raw_attribute)
                for raw_attribute in force_list(json_data.get("AttributeSet", []))
            ],
            citations=[
                Citation.from_json_data(raw_citation)
                for raw_citation in force_list(json_data.get("Citation", []))
            ],
            xrefs=[
                XrefType.from_json_data(raw_xref)
                for raw_xref in force_list(json_data.get("XRef", []))
            ],
            source=[
                DataSourceType.from_json_data(raw_source)
                for raw_source in force_list(json_data.get("Source", []))
            ],
        )


@attrs.frozen(auto_attribs=True)
class ClinAsserTraitType:
    type: ClinAsserTraitTypeType
    names: typing.List[SetElementSetType] = attrs.field(factory=list)
    symbols: typing.List[SetElementSetType] = attrs.field(factory=list)
    attributes: typing.List[ClinAsserTraitTypeAttributeSet] = attrs.field(factory=list)
    trait_relationships: typing.List[TraitRelationship] = attrs.field(factory=list)
    citations: typing.List[Citation] = attrs.field(factory=list)
    xrefs: typing.List[XrefType] = attrs.field(factory=list)
    comments: typing.List[Comment] = attrs.field(factory=list)
    source: typing.List[DataSourceType] = attrs.field(factory=list)
    affected_status: typing.Optional[ClinicalFeaturesAffectedStatus] = None

    @classmethod
    def from_json_data(cls, json_data: dict) -> "ClinAsserTraitType":
        return cls(
            type=ClinAsserTraitTypeType(json_data["@Type"]),
            names=[
                SetElementSetType.from_json_data(raw_name)
                for raw_name in force_list(json_data.get("Name", []))
            ],
            symbols=[
                SetElementSetType.from_json_data(raw_symbol)
                for raw_symbol in force_list(json_data.get("Symbol", []))
            ],
            attributes=[
                ClinAsserTraitTypeAttributeSet.from_json_data(raw_attribute)
                for raw_attribute in force_list(json_data.get("AttributeSet", []))
            ],
            trait_relationships=[
                TraitRelationship.from_json_data(raw_trait_relationship)
                for raw_trait_relationship in force_list(json_data.get("TraitRelationship", []))
            ],
            citations=[
                Citation.from_json_data(raw_citation)
                for raw_citation in force_list(json_data.get("Citation", []))
            ],
            xrefs=[
                XrefType.from_json_data(raw_xref)
                for raw_xref in force_list(json_data.get("XRef", []))
            ],
            comments=[
                Comment.from_json_data(raw_comment)
                for raw_comment in force_list(json_data.get("Comment", []))
            ],
            source=[
                DataSourceType.from_json_data(raw_source)
                for raw_source in force_list(json_data.get("Source", []))
            ],
            affected_status=ClinicalFeaturesAffectedStatus(json_data["@AffectedStatus"])
            if json_data.get("@AffectedStatus")
            else None,
        )


@attrs.frozen(auto_attribs=True)
class Indication:
    traits: typing.List[ClinAsserTraitType] = attrs.field(factory=list)
    names: typing.List[SetElementSetType] = attrs.field(factory=list)
    symbols: typing.List[SetElementSetType] = attrs.field(factory=list)
    attributes: typing.List[AttributeType] = attrs.field(factory=list)
    citations: typing.List[Citation] = attrs.field(factory=list)
    xrefs: typing.List[XrefType] = attrs.field(factory=list)
    comment: typing.Optional[Comment] = None
    type: typing.Optional[IndicationType] = None

    @classmethod
    def from_json_data(cls, json_data: dict) -> "Indication":
        return cls(
            traits=[
                ClinAsserTraitType.from_json_data(raw_trait)
                for raw_trait in force_list(json_data.get("Trait", []))
            ],
            names=[
                SetElementSetType.from_json_data(raw_name)
                for raw_name in force_list(json_data.get("Name", []))
            ],
            symbols=[
                SetElementSetType.from_json_data(raw_symbol)
                for raw_symbol in force_list(json_data.get("Symbol", []))
            ],
            attributes=[
                AttributeType.from_json_data(raw_attribute)
                for raw_attribute in force_list(json_data.get("Attribute", []))
            ],
            citations=[
                Citation.from_json_data(raw_citation)
                for raw_citation in force_list(json_data.get("Citation", []))
            ],
            xrefs=[
                XrefType.from_json_data(raw_xref)
                for raw_xref in force_list(json_data.get("XRef", []))
            ],
            comment=Comment.from_json_data(json_data.get("Comment"))
            if json_data.get("Comment")
            else None,
            type=IndicationType(json_data["@Type"]),
        )


@attrs.frozen(auto_attribs=True)
class SampleType:
    sample_description: typing.Optional[SampleDescription] = None
    origin: typing.Optional[SampleOrigin] = None
    ethnicity: typing.Optional[str] = None
    geographic_origin: typing.Optional[str] = None
    tissue: typing.Optional[str] = None
    cell_line: typing.Optional[str] = None
    species: typing.Optional[Species] = None
    age: typing.List[Age] = attrs.field(factory=list)
    strain: typing.Optional[str] = None
    affected_status: AffectedStatus = AffectedStatus.NOT_PROVIDED
    #: Denominator, total individuals included in this observation set.
    number_tested: typing.Optional[int] = None
    #: Denominator, total males included in this observation set.
    number_males: typing.Optional[int] = None
    #: Denominator, total females included in this observation set.
    number_females: typing.Optional[int] = None
    #: Denominator, total number chromosomes tested. Number affected and
    #: unaffected are captured in the element NumberObserved.
    number_chr_tested: typing.Optional[int] = None
    #: Gender should be used ONLY if explicit values are not available for number
    #: of males or females, and there is a need to indicate that the genders in
    #: the sample are known.
    gender: typing.Optional[Gender] = None
    family_data: typing.Optional[FamilyInfo] = None
    proband: typing.Optional[str] = None
    indication: typing.Optional[Indication] = None
    citations: typing.List[Citation] = attrs.field(factory=list)
    xrefs: typing.List[XrefType] = attrs.field(factory=list)
    comments: typing.List[Comment] = attrs.field(factory=list)
    source: typing.Optional[SampleSource] = None

    @classmethod
    def from_json_data(cls, json_data: dict) -> "SampleType":
        return cls(
            sample_description=SampleDescription.from_json_data(json_data["SampleDescription"])
            if json_data.get("SampleDescription")
            else None,
            origin=SampleOrigin(json_data["Origin"]) if json_data.get("Origin") else None,
            ethnicity=json_data.get("Ethnicity"),
            geographic_origin=json_data.get("GeographicOrigin"),
            tissue=json_data.get("Tissue"),
            cell_line=json_data.get("CellLine"),
            species=Species.from_json_data(json_data.get("Species")),
            age=[Age.from_json_data(raw_age) for raw_age in force_list(json_data.get("Age", []))],
            strain=json_data.get("Strain"),
            affected_status=AffectedStatus(json_data["AffectedStatus"])
            if json_data.get("AffectedStatus")
            else AffectedStatus.NOT_PROVIDED,
            number_tested=int(json_data["NumberTested"]) if json_data.get("NumberTested") else None,
            number_males=int(json_data["NumberMales"]) if json_data.get("NumberMales") else None,
            number_females=int(json_data["NumberFemales"])
            if json_data.get("NumberFemales")
            else None,
            number_chr_tested=int(json_data["NumberChrTested"])
            if json_data.get("NumberChrTested")
            else None,
            gender=Gender(json_data["Gender"]) if json_data.get("Gender") else None,
            family_data=FamilyInfo.from_json_data(json_data.get("FamilyData"))
            if json_data.get("FamilyData")
            else None,
            proband=json_data.get("Proband"),
            indication=Indication.from_json_data(json_data.get("Indication"))
            if json_data.get("Indication")
            else None,
            citations=[
                Citation.from_json_data(raw_citation)
                for raw_citation in force_list(json_data.get("Citation", []))
            ],
            xrefs=[
                XrefType.from_json_data(raw_xref)
                for raw_xref in force_list(json_data.get("XRef", []))
            ],
            comments=[
                Comment.from_json_data(raw_comment)
                for raw_comment in force_list(json_data.get("Comment", []))
            ],
            source=SampleSource(json_data["SourceType"]) if json_data.get("SourceType") else None,
        )


@attrs.frozen(auto_attribs=True)
class ObservationSet:
    """Documents in what populations or samples an allele or genotype has been observed
    relative to the described trait.

    Summary observations can be registered per submitted assertion, grouped by common
    citation, study type, origin, ethnicity, tissue, cell line, and species data. Not
    all options are valid per study type, but these will not be validated in the xsd.
    """

    sample: SampleType
    method: typing.List[ObservationMethod] = attrs.field(factory=list)
    observed_data: typing.List[ObservedData] = attrs.field(factory=list)
    cooccurrences: typing.List[Coocurrence] = attrs.field(factory=list)
    citations: typing.List[Citation] = attrs.field(factory=list)
    xrefs: typing.List[XrefType] = attrs.field(factory=list)
    comments: typing.List[Comment] = attrs.field(factory=list)

    @classmethod
    def from_json_data(cls, json_data: dict) -> "ObservationSet":
        return cls(
            sample=SampleType.from_json_data(json_data["Sample"]),
            method=[
                ObservationMethod.from_the_wild(method["MethodType"])
                for method in force_list(json_data.get("Method", []))
            ],
            observed_data=[
                ObservedData.from_json_data(raw_observed_data)
                for raw_observed_data in force_list(json_data.get("ObservedData", []))
            ],
            cooccurrences=[
                Coocurrence.from_json_data(raw_cooccurrence)
                for raw_cooccurrence in force_list(json_data.get("Coocurrence", []))
            ],
            citations=[
                Citation.from_json_data(raw_citation)
                for raw_citation in force_list(json_data.get("Citation", []))
            ],
            xrefs=[
                XrefType.from_json_data(raw_xref)
                for raw_xref in force_list(json_data.get("XRef", []))
            ],
            comments=[
                Comment.from_json_data(raw_comment)
                for raw_comment in force_list(json_data.get("Comment", []))
            ],
        )


@enum.unique
class AssertionTypeAttr(enum.Enum):
    """The assertion types for RCV records."""

    VARIATION_TO_DISEASE = "variation to disease"
    VARIATION_IN_MODIFIER_GENE_TO_DISEASE = "variation in modifier gene to disease"
    CONFERS_SENSITIVITY = "confers sensitivity"
    CONFERS_RESISTANCE = "confers resistance"
    VARIANT_TO_NAMED_PROTEIN_EFFECT = "variant to named protein"


@attrs.frozen(auto_attribs=True)
class AssertionTypeRCV:
    """Assertion is used to represent the type of relationship between the trait set and the
    measure set.
    """

    type: AssertionTypeAttr

    @classmethod
    def from_json_data(cls, json_data: dict) -> "AssertionTypeRCV":
        return cls(
            type=AssertionTypeAttr(json_data["@Type"]),
        )


@enum.unique
class MeasureSetAttributeType(enum.Enum):
    DESCRIPTION = "Description"
    MOLECULAR_CONSEQUENCE = "MolecularConsequence"
    HGVS = "HGVS"
    HGVS_GENOMIC_TOP_LEVEL = "HGVS, genomic, top level"
    HGVS_GENOMIC_TOP_LEVEL_PREVIOUS = "HGVS, genomic, top level, previous"
    HGVS_GENOMIC_TOP_LEVEL_OTHER = "HGVS, genomic, top level, other"
    HGVS_GENOMIC_REFSEQGENE = "HGVS, genomic, RefSeqGene"
    HGVS_GENOMIC_LRG = "HGVS, genomic, LRG"
    HGVS_CODING_REFSEQGENE = "HGVS, coding, RefSeq"
    HGVS_CODING_LRG = "HGVS, coding, LRG"
    HGVS_CODING = "HGVS, coding"
    HGVS_RNA = "HGVS, RNA"
    HGVS_PREVIOUS = "HGVS, previous"
    HGVS_PROTEIN = "HGVS, protein"
    HGVS_PROTEIN_REFSEQ = "HGVS, protein, RefSeq"
    HGVS_NUCLEOTIDE = "HGVS, nucleotide"
    HGVS_NON_VALIDATED = "HGVS, non-validated"
    HGVS_LEGACY = "HGVS, legacy"
    HGVS_UNCERTAIN = "HGVS, uncertain"
    FUNCTIONAL_CONSEQUENCE = "FunctionalConsequence"
    ISCN_COORDINATES = "ISCNCoordinates"
    SUBMITTER_VARIANT_ID = "SubmitterVariantId"


@attrs.frozen(auto_attribs=True)
class MeasureSetAttribute:
    type: MeasureSetAttributeType
    value: str
    change: typing.Optional[str] = None
    mane_select: typing.Optional[bool] = None
    mane_plus_clinical: typing.Optional[bool] = None

    @classmethod
    def from_json_data(cls, json_data: dict) -> "MeasureSetAttribute":
        return cls(
            type=MeasureSetAttributeType(json_data["@Type"]),
            value=json_data["#text"],
            change=json_data.get("@Change"),
            mane_select=json_data["@ManeSelect"] == "yes" if json_data.get("@ManeSelect") else None,
            mane_plus_clinical=json_data["@ManePlusClinical"] == "yes"
            if json_data.get("@ManePlusClinical")
            else None,
        )


@attrs.frozen(auto_attribs=True)
class MeasureSetAttributeSet:
    attribute: MeasureSetAttribute
    citations: typing.List[Citation] = attrs.field(factory=list)
    xrefs: typing.List[XrefType] = attrs.field(factory=list)
    comments: typing.List[Comment] = attrs.field(factory=list)

    @classmethod
    def from_json_data(cls, json_data: dict) -> "MeasureSetAttributeSet":
        return cls(
            attribute=MeasureSetAttribute.from_json_data(json_data["Attribute"]),
            citations=[
                Citation.from_json_data(raw_citation)
                for raw_citation in force_list(json_data.get("Citation", []))
            ],
            xrefs=[
                XrefType.from_json_data(raw_xref)
                for raw_xref in force_list(json_data.get("XRef", []))
            ],
            comments=[
                Comment.from_json_data(raw_comment)
                for raw_comment in force_list(json_data.get("Comment", []))
            ],
        )


@enum.unique
class MeasureTypeAttributeType(enum.Enum):
    HGVS_GENOMIC_TOP_LEVEL = "HGVS, genomic, top level"
    HGVS_GENOMIC_TOP_LEVEL_PREVIOUS = "HGVS, genomic, top level, previous"
    HGVS_GENOMIC_TOP_LEVEL_OTHER = "HGVS, genomic, top level, other"
    HGVS_GENOMIC_REFSEQGENE = "HGVS, genomic, RefSeqGene"
    HGVS_GENOMIC_LRG = "HGVS, genomic, LRG"
    HGVS_CODING_REFSEQGENE = "HGVS, coding, RefSeq"
    HGVS_CODING_LRG = "HGVS, coding, LRG"
    HGVS_CODING = "HGVS, coding"
    HGVS_INCOMPLETE = "HGVS, incomplete"
    HGVS_PREVIOUS = "HGVS, previous"
    HGVS_PROTEIN = "HGVS, protein"
    HGVS_PROTEIN_REFSEQ = "HGVS, protein, RefSeq"
    HGVS_NON_CODING = "HGVS, non-coding"
    HGVS_NON_VALIDATED = "HGVS, non-validated"
    HGVS_RNA = "HGVS, RNA"
    HGVS_LEGACY = "HGVS, legacy"
    HGVS_UNCERTAIN = "HGVS, uncertain"
    HGVS = "HGVS"
    NON_HGVS = "NonHGVS"
    LOCATION = "Location"
    MISCELLANEOUS_DESCRIPTION = "MiscellaneousDescription"
    DESCRIPTION = "Description"
    FUNCTIONAL_CONCESEQUENCE = "FunctionalConsequence"
    MOLECULAR_CONSEQUENCE = "MolecularConsequence"
    PROTEIN_CHANGE_1_LETTER_CODE = "ProteinChange1LetterCode"
    PROTEIN_CHANGE_3_LETTER_CODE = "ProteinChange3LetterCode"
    ACTIVITY_LEVEL = "ActivityLevel"
    SUSPECT = "Suspect"
    ALLELIC_VARIANT_PREVIOUS = "Allelic Variant, previous"
    ACCEPTOR_SPLICE_SITE = "acceptor splice site"
    DONOR_SPLICE_SITE = "donor splice site"
    NUCLEOTIDE_CHANGE = "nucleotide change"
    PROTEIN_CHANGE_HISTORICAL = "protein change, historical"
    TRANSCRIPT_VARIANT = "transcript variant"
    ABSOLUTE_COPY_NUMBER = "absolute copy number"
    REFERENCE_COPY_NUMBER = "reference copy number"
    COPY_NUMBER_TUPLE = "copy number tuple"
    COSMIC = "COSMIC"
    SUBMITTER_VARIANT_ID = "SubmitterVariantId"
    ISCN_COORDINATES = "ISCNCoordinates"


@attrs.frozen(auto_attribs=True)
class MeasureTypeAttribute:
    type: MeasureTypeAttributeType
    change: typing.Optional[str] = None
    accession: typing.Optional[str] = None
    version: typing.Optional[int] = None
    mane_select: typing.Optional[bool] = None
    mane_plus_clinical: typing.Optional[bool] = None

    @classmethod
    def from_json_data(cls, json_data: dict) -> "MeasureTypeAttribute":
        return cls(
            type=MeasureTypeAttributeType(json_data["@Type"]),
            change=json_data.get("@Change"),
            accession=json_data.get("@Accession"),
            version=int(json_data["@Version"]) if json_data.get("@Version") else None,
            mane_select=json_data["@ManeSelect"] == "true"
            if json_data.get("@ManeSelect")
            else None,
            mane_plus_clinical=json_data["@ManePlusClinical"] == "true"
            if json_data.get("@ManePlusClinical")
            else None,
        )


@attrs.frozen(auto_attribs=True)
class AlleleFrequency:
    value: float
    source: str
    url: typing.Optional[str] = None

    @classmethod
    def from_json_data(cls, json_data: dict) -> "AlleleFrequency":
        return cls(
            value=float(json_data["@Value"]),
            source=json_data["@Source"],
            url=json_data.get("@URL"),
        )


@attrs.frozen(auto_attribs=True)
class GlobalMinorAlleleFrequency:
    value: float
    source: str
    minor_allele: typing.Optional[str] = None
    url: typing.Optional[str] = None

    @classmethod
    def from_json_data(cls, json_data: dict) -> "GlobalMinorAlleleFrequency":
        return cls(
            value=float(json_data["@Value"]),
            source=json_data["@Source"],
            minor_allele=json_data.get("@MinorAllele"),
            url=json_data.get("@URL"),
        )


@attrs.frozen(auto_attribs=True)
class MeasureType:
    names: typing.List[SetElementSetType] = attrs.field(factory=list)
    canonical_spdi: typing.Optional[str] = None
    symbols: typing.List[SetElementSetType] = attrs.field(factory=list)
    attributes: typing.List[MeasureTypeAttribute] = attrs.field(factory=list)
    allele_frequencies: typing.List[AlleleFrequency] = attrs.field(factory=list)
    global_minor_allele_frequency: typing.Optional[GlobalMinorAlleleFrequency] = None

    @classmethod
    def from_json_data(cls, json_data: dict) -> "MeasureType":
        return cls(
            names=[
                SetElementSetType.from_json_data(raw_name)
                for raw_name in force_list(json_data.get("Name", []))
            ],
            canonical_spdi=json_data.get("CanonicalSPDI"),
            symbols=[
                SetElementSetType.from_json_data(raw_symbol)
                for raw_symbol in force_list(json_data.get("Symbol", []))
            ],
            attributes=[
                MeasureTypeAttribute.from_json_data(raw_attribute)
                for raw_attribute in force_list(json_data.get("Attribute", []))
            ],
            allele_frequencies=[
                AlleleFrequency.from_json_data(raw_allele_frequency)
                for raw_allele_frequency in force_list(json_data.get("AlleleFrequency", []))
            ],
            global_minor_allele_frequency=GlobalMinorAlleleFrequency.from_json_data(
                json_data.get("GlobalMinorAlleleFrequency")
            )
            if json_data.get("GlobalMinorAlleleFrequency")
            else None,
        )


@enum.unique
class MeasureSetType(enum.Enum):
    GENE = "Gene"
    VARIANT = "Variant"
    GENE_VARIANT = "gene-variant"
    OMIM_RECORD = "OMIM record"
    HAPLOTYPE = "Haplotype"
    HAPLOTYPE_SINGLE_VARIANT = "Haplotype, single variant"
    PHASE_UNKNOWN = "Phase unknown"
    DISTINCT_CHROMOSOMES = "Distinct chromosomes"
    COMPOUND_HETEROZYGOUS = "Compound heterozygous"
    DIPLOTYPE = "Diplotype"


@attrs.frozen(auto_attribs=True)
class MeasureSet:
    type: MeasureSetType
    acc: str
    version: typing.Optional[int] = None
    measures: typing.List[MeasureType] = attrs.field(factory=list)
    names: typing.List[SetElementSetType] = attrs.field(factory=list)
    symbols: typing.List[SetElementSetType] = attrs.field(factory=list)
    attributes: typing.List[MeasureSetAttributeSet] = attrs.field(factory=list)
    citations: typing.List[Citation] = attrs.field(factory=list)
    xrefs: typing.List[XrefType] = attrs.field(factory=list)
    comments: typing.List[Comment] = attrs.field(factory=list)
    number_of_chromosomes: typing.Optional[int] = None
    id: typing.Optional[int] = None

    @classmethod
    def from_json_data(cls, json_data: dict) -> "MeasureSet":
        return cls(
            type=MeasureSetType(json_data["@Type"]),
            acc=json_data.get("@Acc"),
            version=int(json_data["@Version"]) if json_data.get("@Version") else None,
            measures=[
                MeasureType.from_json_data(raw_measure)
                for raw_measure in force_list(json_data.get("Measure", []))
            ],
            names=[
                SetElementSetType.from_json_data(raw_name)
                for raw_name in force_list(json_data.get("Name", []))
            ],
            symbols=[
                SetElementSetType.from_json_data(raw_symbol)
                for raw_symbol in force_list(json_data.get("Symbol", []))
            ],
            attributes=[
                MeasureSetAttributeSet.from_json_data(raw_attribute)
                for raw_attribute in force_list(json_data.get("AttributeSet", []))
            ],
            citations=[
                Citation.from_json_data(raw_citation)
                for raw_citation in force_list(json_data.get("Citation", []))
            ],
            xrefs=[
                XrefType.from_json_data(raw_xref)
                for raw_xref in force_list(json_data.get("XRef", []))
            ],
            comments=[
                Comment.from_json_data(raw_comment)
                for raw_comment in force_list(json_data.get("Comment", []))
            ],
            number_of_chromosomes=int(json_data["@NumberOfChromosomes"])
            if json_data.get("@NumberOfChromosomes")
            else None,
            id=int(json_data["@ID"]) if json_data.get("@ID") else None,
        )


@enum.unique
class GenotypeSetType(enum.Enum):
    COMPOUND_HETEROZYGOTE = "CompoundHeterozygote"
    DIPLOTYPE = "Diplotype"


@attrs.frozen(auto_attribs=True)
class GenotypeSet:
    type: GenotypeSetType
    measures: typing.List[MeasureSet] = attrs.field(factory=list)
    names: typing.List[SetElementSetType] = attrs.field(factory=list)
    symbols: typing.List[SetElementSetType] = attrs.field(factory=list)
    attributes: typing.List[MeasureSetAttributeSet] = attrs.field(factory=list)
    citations: typing.List[Citation] = attrs.field(factory=list)
    xrefs: typing.List[XrefType] = attrs.field(factory=list)
    comments: typing.List[Comment] = attrs.field(factory=list)
    id: typing.Optional[int] = None
    acc: typing.Optional[str] = None
    version: typing.Optional[str] = None

    @classmethod
    def from_json_data(cls, json_data: dict) -> "GenotypeSet":
        return cls(
            type=GenotypeSetType(json_data["@Type"]),
            measures=[
                MeasureSet.from_json_data(raw_measure) for raw_measure in force_list(json_data)
            ],
            names=[
                SetElementSetType.from_json_data(raw_name)
                for raw_name in force_list(json_data.get("Name", []))
            ],
            symbols=[
                SetElementSetType.from_json_data(raw_symbol)
                for raw_symbol in force_list(json_data.get("Symbol", []))
            ],
            attributes=[
                MeasureSetAttributeSet.from_json_data(raw_attribute)
                for raw_attribute in force_list(json_data.get("AttributeSet", []))
            ],
            citations=[
                Citation.from_json_data(raw_citation)
                for raw_citation in force_list(json_data.get("Citation", []))
            ],
            xrefs=[
                XrefType.from_json_data(raw_xref)
                for raw_xref in force_list(json_data.get("XRef", []))
            ],
            comments=[
                Comment.from_json_data(raw_comment)
                for raw_comment in force_list(json_data.get("Comment", []))
            ],
            id=int(json_data["@ID"]) if json_data.get("@ID") else None,
            acc=json_data.get("@Acc"),
            version=json_data.get("@Version"),
        )


@attrs.frozen(auto_attribs=True)
class TraitSetTypeAttribute:
    type: str
    value: str

    @classmethod
    def from_json_data(cls, json_data: dict) -> "TraitSetTypeAttribute":
        return cls(
            type=json_data["@Type"],
            value=json_data["#text"],
        )


@attrs.frozen(auto_attribs=True)
class TraitSetTypeAttributeSet:
    attribute: TraitSetTypeAttribute
    citations: typing.List[Citation] = attrs.field(factory=list)
    xrefs: typing.List[XrefType] = attrs.field(factory=list)
    comments: typing.List[Comment] = attrs.field(factory=list)

    @classmethod
    def from_json_data(cls, json_data: dict) -> "TraitSetTypeAttributeSet":
        return cls(
            attribute=TraitSetTypeAttribute.from_json_data(json_data["Attribute"]),
            citations=[
                Citation.from_json_data(raw_citation)
                for raw_citation in force_list(json_data.get("Citation", []))
            ],
            xrefs=[
                XrefType.from_json_data(raw_xref)
                for raw_xref in force_list(json_data.get("XRef", []))
            ],
            comments=[
                Comment.from_json_data(raw_comment)
                for raw_comment in force_list(json_data.get("Comment", []))
            ],
        )


@enum.unique
class TraitSetTypeType(enum.Enum):
    DISEASE = "Disease"
    DRUG_RESPONSE = "DrugResponse"
    FINDING = "Finding"
    PHENOTYPE_INSTRUCTION = "PhenotypeInstruction"
    TRAIT_CHOICE = "TraitChoice"


@attrs.frozen(auto_attribs=True)
class TraitSetType:
    type: TraitSetTypeType
    traits: typing.List[SetElementSetType] = attrs.field(factory=list)
    id: typing.Optional[int] = None
    names: typing.List[SetElementSetType] = attrs.field(factory=list)
    symbols: typing.List[SetElementSetType] = attrs.field(factory=list)
    attributes: typing.List[TraitSetTypeAttributeSet] = attrs.field(factory=list)
    citations: typing.List[Citation] = attrs.field(factory=list)
    xrefs: typing.List[XrefType] = attrs.field(factory=list)
    comments: typing.List[Comment] = attrs.field(factory=list)

    @classmethod
    def from_json_data(cls, json_data: dict) -> "TraitSetType":
        return cls(
            type=TraitSetTypeType(json_data["@Type"]),
            traits=[
                SetElementSetType.from_json_data(raw_trait)
                for raw_trait in force_list(json_data.get("Trait", []))
            ],
            id=int(json_data["@ID"]) if json_data.get("@ID") else None,
            names=[
                SetElementSetType.from_json_data(raw_name)
                for raw_name in force_list(json_data.get("Name", []))
            ],
            symbols=[
                SetElementSetType.from_json_data(raw_symbol)
                for raw_symbol in force_list(json_data.get("Symbol", []))
            ],
            attributes=[
                TraitSetTypeAttributeSet.from_json_data(raw_attribute)
                for raw_attribute in force_list(json_data.get("AttributeSet", []))
            ],
            citations=[
                Citation.from_json_data(raw_citation)
                for raw_citation in force_list(json_data.get("Citation", []))
            ],
            xrefs=[
                XrefType.from_json_data(raw_xref)
                for raw_xref in force_list(json_data.get("XRef", []))
            ],
            comments=[
                Comment.from_json_data(raw_comment)
                for raw_comment in force_list(json_data.get("Comment", []))
            ],
        )


@attrs.frozen(auto_attribs=True)
class ReferenceClinVarAssertion:
    #: Accesion of the RCV record.
    clinvar_accession: ClinVarAccession
    #: Status of the record.
    record_status: RecordStatus
    #: Clinical significance summary of RCV record.
    clinical_significance: ClinicalSignificance
    #: The assertion RCV type.
    assertion: AssertionTypeRCV
    #: Represents the public identifier a source may have for this record.
    external_ids: typing.List[XrefType] = attrs.field(factory=list)
    #: Attributes of the RCV record
    attributes: typing.List[ReferenceClinVarAssertionAttribute] = attrs.field(factory=list)
    #: Observations.
    observed_in: typing.List[ObservationSet] = attrs.field(factory=list)
    #: Measurement information, mutually exlusive with ``genotype_set``.
    measure_set: typing.Optional[MeasureSet] = None
    #: Genotyping information, mutually exlusive with ``measure_set``.
    genotype_set: typing.Optional[GenotypeSet] = None
    trait_set: typing.Optional[TraitSetType] = None
    citations: typing.List[Citation] = attrs.field(factory=list)
    comments: typing.List[Comment] = attrs.field(factory=list)
    date_created: typing.Optional[datetime.date] = None
    date_last_updated: typing.Optional[datetime.date] = None
    submission_date: typing.Optional[datetime.date] = None
    id: typing.Optional[int] = None

    @classmethod
    def from_json_data(cls, json_data: dict) -> "ReferenceClinVarAssertion":
        return cls(
            clinvar_accession=ClinVarAccession.from_json_data(json_data["ClinVarAccession"]),
            record_status=RecordStatus(json_data["RecordStatus"]),
            clinical_significance=ClinicalSignificance.from_json_data(
                json_data["ClinicalSignificance"]
            ),
            assertion=AssertionTypeRCV.from_json_data(json_data["Assertion"]),
            external_ids=[
                XrefType.from_json_data(raw_external_id)
                for raw_external_id in force_list(json_data.get("ExternalID", []))
            ],
            attributes=[
                ReferenceClinVarAssertionAttribute.from_json_data(raw_attribute)
                for raw_attribute in force_list(json_data.get("Attribute", []))
            ],
            observed_in=[
                ObservationSet.from_json_data(raw_observation_set)
                for raw_observation_set in force_list(json_data.get("ObservedIn", []))
            ],
            measure_set=MeasureSet.from_json_data(json_data["MeasureSet"])
            if json_data.get("MeasureSet")
            else None,
            genotype_set=GenotypeSet.from_json_data(json_data["GenotypeSet"])
            if json_data.get("GenotypeSet")
            else None,
            citations=[
                Citation.from_json_data(raw_citation)
                for raw_citation in force_list(json_data.get("Citation", []))
            ],
            comments=[
                Comment.from_json_data(raw_comment)
                for raw_comment in force_list(json_data.get("Comment", []))
            ],
            date_created=parse_datetime(json_data["@DateCreated"]).date()
            if json_data.get("@DateCreated")
            else None,
            date_last_updated=parse_datetime(json_data["@DateLastUpdated"]).date()
            if json_data.get("@DateLastUpdated")
            else None,
            submission_date=parse_datetime(json_data["@SubmissionDate"]).date()
            if json_data.get("@SubmissionDate")
            else None,
            id=int(json_data["@ID"]) if json_data.get("@ID") else None,
        )


@attrs.frozen(auto_attribs=True)
class ClinVarSubmissionID:
    """Corresponds to ``ClinVarSubmissionID`` in XML file."""

    #: Of primary use to submitters, to facilitate identification of records corresponding to
    #: their submissions.  If not provided by a submitter, NCBI generates. If provided by
    #: submitter, that is represented in localKeyIsSubmitted.
    local_key: str
    #: Name of the submitter
    submitter: typing.Optional[str] = None
    #: Title of the submission
    title: typing.Optional[str] = None
    #: Assembly used in submission
    submitted_assembly: typing.Optional[str] = None
    #: Submission date
    submitter_date: typing.Optional[datetime.date] = None
    #: Whether the local key was submitted (True) or has ben set by NCBI (False)
    local_key_is_submitted: typing.Optional[bool] = None

    @classmethod
    def from_json_data(cls, json_data: dict) -> "ClinVarSubmissionID":
        return cls(
            local_key=json_data["@localKey"],
            submitter=json_data.get("@submitter"),
            title=json_data.get("@title"),
            submitted_assembly=json_data.get("@submittedAssembly"),
            submitter_date=parse_datetime(json_data.get("@submitterDate")).date()
            if json_data.get("@submitterDate")
            else None,
            local_key_is_submitted=json_data.get("localKeyIsSubmitted") == "1"
            if json_data.get("localKeyIsSubmitted")
            else None,
        )


@enum.unique
class SubmitterType(enum.Enum):
    """Enumeration with ``Submitter.type``."""

    PRIMARY = "primary"
    SECONDARY = "secondary"
    BEHALF = "behalf"


@attrs.frozen(auto_attribs=True)
class Submitter:
    """A structure to support reportng the name of a submitter, its org_id, and whether primary
    or secondary or behalf.

    Corresponds to ``SubmitterType`` in XML file.
    """

    #: The type of the submitter
    type: SubmitterType
    #: The name of the submitter
    submitter_name: typing.Optional[str] = None
    #: The ID of the submitting organisation
    org_id: typing.Optional[int] = None
    #: The submitter category
    category: typing.Optional[str] = None

    @classmethod
    def from_json_data(cls, json_data: dict) -> "Submitter":
        return cls(
            type=SubmitterType(json_data["@Type"]),
            submitter_name=json_data.get("@SubmitterName"),
            org_id=int(json_data.get("@OrgID")),
            category=json_data.get("@Category"),
        )


@enum.unique
class ClinVarAssertionAccessionType(enum.Enum):
    """ClinVar assertion accession type"""

    RCV = "RCV"
    SCV = "SCV"


@attrs.frozen(auto_attribs=True)
class ClinVarAssertionAccession:
    """Accession number for a ClinVar record in a ``ClinVarAssertion``."""

    #: The accession
    acc: str
    #: The version
    version: int
    #: The accession type
    type: ClinVarAssertionAccessionType
    #: The date that the latest update to the submitted record became public in ClinVar.
    date_updated: datetime.date
    #: DateCreated is the date when the record first became public in ClinVar.
    date_created: typing.Optional[datetime.date] = None
    #: The ID of the submitting organisation
    org_id: typing.Optional[str] = None
    #: The abbreviation of the submitting organisation
    org_abbreviation: typing.Optional[str] = None
    #: The type of the organisation
    org_type: typing.Optional[str] = None
    #: The category of the organisation.
    org_category: typing.Optional[str] = None

    @classmethod
    def from_json_data(cls, json_data: dict) -> "ClinVarAssertionAccession":
        return cls(
            acc=json_data["@Acc"],
            version=int(json_data["@Version"]),
            type=ClinVarAssertionAccessionType(json_data["@Type"]),
            date_updated=parse_datetime(json_data["@DateUpdated"]).date()
            if json_data.get("@DateUpdated")
            else None,
            date_created=parse_datetime(json_data["@DateCreated"]).date()
            if json_data.get("@DateCreated")
            else None,
            org_id=json_data.get("@OrgID"),
            org_abbreviation=json_data.get("@OrgAbbreviation"),
            org_type=json_data.get("@OrgType"),
            org_category=json_data.get("@OrganizationCategory"),
        )


@attrs.frozen(auto_attribs=True)
class RecordHistory:
    """A structure to support reporting of an accession, its version, the date its status
    changed, and text describing that change.
    """

    #: The accession
    accession: str
    #: The version
    version: int
    #: The date the status changed
    date_changed: datetime.date
    #: Comment text
    comment: typing.Optional[str] = None
    #: Attribute @VaritionID is only populated for VCV, where @Accession is like VCV000000009
    variation_id: typing.Optional[int] = None

    @classmethod
    def from_json_data(cls, json_data: dict) -> "RecordHistory":
        return cls(
            accession=json_data["@Accession"],
            version=int(json_data["@Version"]),
            date_changed=parse_datetime(json_data["@DateChanged"]).date(),
            comment=json_data.get("@Comment"),
            variation_id=int(json_data["@VariationID"]) if json_data.get("@VariationID") else None,
        )


@attrs.frozen(auto_attribs=True)
class ClinVarAssertionAttribute:
    type: ClinVarAssertionAttributeType
    value: str

    @classmethod
    def from_json_data(cls, json_data: dict) -> "ClinVarAssertionAttribute":
        return cls(
            type=ClinVarAssertionAttributeType(json_data["@Type"]),
            value=json_data["#text"],
        )


@attrs.frozen(auto_attribs=True)
class ClinVarAssertionAttributeSet:
    """AttributeSet is a package to represent a unit of information, the source(s) of that unit,
    identifiers representing that unit, and comments.
    """

    #: Specification of the attribute set type.
    attribute: ClinVarAssertionAttribute
    #: List of citations
    citations: typing.List[Citation] = attrs.field(factory=list)
    #: List of Xrefs
    xrefs: typing.List[XrefType] = attrs.field(factory=list)
    #: List of comments
    comments: typing.List[Comment] = attrs.field(factory=list)

    @classmethod
    def from_json_data(cls, json_data: dict) -> "ClinVarAssertionAttributeSet":
        return cls(
            attribute=ClinVarAssertionAttribute.from_json_data(json_data["Attribute"]),
            citations=[
                Citation.from_json_data(raw_citation)
                for raw_citation in force_list(json_data.get("Citation", []))
            ],
            xrefs=[
                XrefType.from_json_data(raw_xref)
                for raw_xref in force_list(json_data.get("XRef", []))
            ],
            comments=[
                Comment.from_json_data(raw_comment)
                for raw_comment in force_list(json_data.get("Comment", []))
            ],
        )


@attrs.frozen(auto_attribs=True)
class ClinAsserTraitSetTypeAttribute:
    value: str
    type: str
    citations: typing.List[Citation] = attrs.field(factory=list)
    xrefs: typing.List[XrefType] = attrs.field(factory=list)
    comments: typing.List[Comment] = attrs.field(factory=list)


@enum.unique
class ClinAsserTraitSetTypeType(enum.Enum):
    DISEASE = "Disease"
    DRUG_RESPONSE = "DrugResponse"
    FINDING = "Finding"
    PHENOTYPE_INSTRUCITON = "PhenotypeInstruction"
    TRAIT_CHOICE = "TraitChoice"


@attrs.frozen(auto_attribs=True)
class ClinAsserTraitSetType:
    type: ClinAsserTraitSetTypeType
    date_last_evaluated: datetime.date
    traits: typing.List[ClinAsserTraitType] = attrs.field(factory=list)
    names: typing.List[SetElementSetType] = attrs.field(factory=list)
    symbols: typing.List[SetElementSetType] = attrs.field(factory=list)
    attributes: typing.List[ClinAsserTraitSetTypeAttribute] = attrs.field(factory=list)
    id: typing.Optional[int] = None
    multiple_condition_explanation: typing.Optional[str] = None


@attrs.frozen(auto_attribs=True)
class ClinVarAssertion:
    """The ClinVarAssertion is the package of data as received from the submitter. During
    integration with other submissions, the content may have been mapped to controlled values.

    Represents a ``ClinVarAssertion`` in the XML file.
    """

    #: The submission's ID.
    id: int
    #: More detaield submission information.
    clinvar_submission_id: ClinVarSubmissionID
    #: The ClinVar accession number.
    clinvar_accession: ClinVarAssertionAccession
    #: The assertion type.
    assertion_type: AssertionTypeSCV
    #: The record status
    record_status: RecordStatus = RecordStatus.CURRENT
    #: Optional element used only if there are multiple submitters. When there are multiple,
    #: each is listed in this element.
    additional_submitters: typing.List[Submitter] = attrs.field(factory=list)
    #: The list of SCV accessions this SCV record has replaced.
    replaced_list: typing.List[RecordHistory] = attrs.field(factory=list)
    #: The clinical significance assertion.
    clinical_significance: typing.List[ClinicalSignificanceSCV] = attrs.field(factory=list)
    #: XrefType is used to identify data source(s) and their identifiers. Optional because
    #: not all sources have an ID specific to the assertion.
    external_ids: typing.List[XrefType] = attrs.field(factory=list)
    #: Additional attribute sets.
    attributes: typing.List[ClinVarAssertionAttributeSet] = attrs.field(factory=list)
    #: Observation information.
    observed_in: typing.List[ObservationSet] = attrs.field(factory=list)
    #: Measurement information, mutually exlusive with ``genotype_set``.
    measure_set: typing.Optional[MeasureSet] = None
    #: Genotyping information, mutually exlusive with ``measure_set``.
    genotype_set: typing.Optional[GenotypeSet] = None
    #: Traits associated with the disease.
    trait_set: typing.List[ClinAsserTraitSetType] = attrs.field(factory=list)
    #: Citations for the variant.
    citations: typing.List[Citation] = attrs.field(factory=list)
    #: An optional study name.
    study_name: typing.Optional[str] = None
    #: An optional study description.
    study_description: typing.Optional[str] = None
    #: Optional comments.
    comments: typing.List[Comment] = attrs.field(factory=list)

    @classmethod
    def from_json_data(cls, json_data: dict) -> "ClinVarAssertion":
        return ClinVarAssertion(
            id=int(json_data["@ID"]),
            clinvar_submission_id=ClinVarSubmissionID.from_json_data(
                json_data["ClinVarSubmissionID"]
            ),
            clinvar_accession=ClinVarAssertionAccession.from_json_data(
                json_data["ClinVarAccession"]
            ),
            assertion_type=AssertionTypeSCV(json_data["Assertion"]["@Type"]),
            additional_submitters=[
                Submitter.from_json_data(raw_submitter)
                for raw_submitter in force_list(
                    json_data.get("AdditionalSubmitters", {}).get("SubmitterDescription", [])
                )
            ],
            replaced_list=[
                RecordHistory.from_json_data(raw_replaced)
                for raw_replaced in force_list(
                    json_data.get("ReplacedList", {}).get("Replaced", [])
                )
            ],
            clinical_significance=[
                ClinicalSignificanceSCV.from_json_data(raw_clinical_significance)
                for raw_clinical_significance in force_list(
                    json_data.get("ClinicalSignificance", [])
                )
            ],
            external_ids=[
                XrefType.from_json_data(raw_xref)
                for raw_xref in force_list(json_data.get("ExternalID", []))
            ],
            attributes=[
                ClinVarAssertionAttributeSet.from_json_data(raw_attribute)
                for raw_attribute in force_list(json_data.get("AttributeSet", []))
            ],
            observed_in=[
                ObservationSet.from_json_data(raw_observation_set)
                for raw_observation_set in force_list(json_data.get("ObservedIn", []))
            ],
            measure_set=MeasureSet.from_json_data(json_data.get("MeasureSet"))
            if json_data.get("MeasureSet")
            else None,
            genotype_set=GenotypeSet.from_json_data(json_data.get("GenotypeSet"))
            if json_data.get("GenotypeSet")
            else None,
            citations=[
                Citation.from_json_data(raw_citation)
                for raw_citation in force_list(json_data.get("Citation", []))
            ],
            study_name=json_data.get("StudyName"),
            study_description=json_data.get("StudyDescription"),
            comments=[
                Comment.from_json_data(raw_comment)
                for raw_comment in force_list(json_data.get("Comment", []))
            ],
        )


@attrs.frozen(auto_attribs=True)
class PublicSetType:
    """Used both for SCV and RCV accessions.

    Represents a ``ClinVarSet`` in the XML file.
    """

    #: The reference clinvar assertion as used in RCV records
    reference_clinvar_assertion: ReferenceClinVarAssertion
    #: The set's record status
    record_status: RecordStatus = RecordStatus.CURRENT
    #: The identifiers that this record replaces
    replaces: typing.List[str] = attrs.field(factory=list)
    #: An optional title for the submission
    title: typing.Optional[str] = None
    #: The clinvar assertion
    clinvar_assertions: typing.List[ClinVarAssertion] = attrs.field(factory=list)

    @classmethod
    def from_json(cls, json_data: dict) -> "PublicSetType":
        raw_clinvar_assertions = force_list(json_data["ClinVarAssertion"])

        result = PublicSetType(
            record_status=RecordStatus(json_data["RecordStatus"]),
            title=json_data.get("Title"),
            replaces=force_list(json_data.get("Replaces", [])),
            reference_clinvar_assertion=ReferenceClinVarAssertion.from_json_data(
                json_data["ReferenceClinVarAssertion"]
            ),
            clinvar_assertions=[
                ClinVarAssertion.from_json_data(raw_cva) for raw_cva in raw_clinvar_assertions
            ],
        )
        return result
