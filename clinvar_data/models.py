"""Support for representing ClinVar data from XSD file using pydantic"""

import datetime
import enum
import typing

from dateutil.parser import parse as parse_datetime
from pydantic import BaseModel, ConfigDict

T = typing.TypeVar("T")


def extract_text(element: typing.Any) -> typing.Optional[str]:
    """Extract text from a string or dict with ``#text`` key"""
    if element is None:
        return element
    elif isinstance(element, str):
        return element
    else:
        return element["#text"]


def force_list(value: typing.Union[T, typing.List[T]]) -> typing.List[T]:
    """Helper value that wraps atomic values in a list"""
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
    """Enumeration with ``ClinVarSet.record_status`"""

    CURRENT = "current"
    REPLACED = "replaced"
    REMOVED = "removed"


@enum.unique
class Status(enum.Enum):
    """Corresponds to ``typeStatus``"""

    CURRENT = "current"
    COMPLETED_AND_RETIRED = "completed and retired"
    DELETE = "delete"
    IN_DEVELOPMENT = "in development"
    RECLASSIFIED = "reclassified"
    REJECT = "reject"
    SECONDARY = "secondary"
    SUPPRESSED = "suppressed"
    UNDER_REVIEW = "under review"


class Xref(BaseModel):
    """This structure is used to represent how an object described in the submission relates to
    objects in other databases.
    """

    model_config = ConfigDict(frozen=True)

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
    def from_json_data(cls, json_data: dict) -> "Xref":
        return Xref(
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

    - 0 stars: a conflict or not classified by submitter
    - 1 star: classified by single submitter
    - 2 stars: classified by multiple submitters
    - 3 stars: reviewed by expert panel
    - 4 stars: reviewed by professional society

    In the case that a submission was flagged as duplicate, ``FLAGGED_SUBMISSION`` is used.
    When no unflagged submission is found, ``NO_UNFLAGGED_CLASSIFICATION`` is used.
    """

    NO_ASSERTION_PROVIDED = "no assertion provided"
    NO_ASSERTION_CRITERIA_PROVIDED = "no assertion criteria provided"
    CRITERIA_PROVIDED_SINGLE_SUBMITTER = "criteria provided, single submitter"
    CRITERIA_PROVIDED_MULTIPLE_SUBMITTERS = "criteria provided, multiple submitters, no conflicts"
    CRITERIA_PROVIDED_CONFLICTING_INTERPRETATIONS = "criteria provided, conflicting interpretations"
    REVIEWED_BY_EXPERT_PANEL = "reviewed by expert panel"
    PRACTICE_GUIDELINE = "practice guideline"
    FLAGGED_SUBMISSION = "flagged submission"
    NO_UNFLAGGED_CLASSIFICATION = "no classifications from unflagged records"


@enum.unique
class ClinicalSignificanceDescription(enum.Enum):
    """Allowed values for clinical significance description"""

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

    @property
    def is_canonical_acmg(self) -> bool:
        return self in (
            ClinicalSignificanceDescription.BENIGN,
            ClinicalSignificanceDescription.LIKELY_BENIGN,
            ClinicalSignificanceDescription.UNCERTAIN_SIGNIFICANCE,
            ClinicalSignificanceDescription.LIKELY_PATHOGENIC,
            ClinicalSignificanceDescription.PATHOGENIC,
        )

    @property
    def acmg_code(self) -> typing.Optional[int]:
        return {
            ClinicalSignificanceDescription.BENIGN: 1,
            ClinicalSignificanceDescription.LIKELY_BENIGN: 2,
            ClinicalSignificanceDescription.UNCERTAIN_SIGNIFICANCE: 3,
            ClinicalSignificanceDescription.LIKELY_PATHOGENIC: 4,
            ClinicalSignificanceDescription.PATHOGENIC: 5,
        }.get(self)

    @classmethod
    def from_the_wild(cls, str) -> "ClinicalSignificanceDescription":
        """Convert values "from the wild" where sometimes invalid values are used.

        These are converted to ``Other``.
        """
        try:
            return ClinicalSignificanceDescription(str)
        except ValueError:
            return ClinicalSignificanceDescription.OTHER


@enum.unique
class CommentType(enum.Enum):
    """Types of comments"""

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
    FLAGGED_COMMENT = "FlaggedComment"


class Comment(BaseModel):
    """A structure to support reporting unformatted content"""

    model_config = ConfigDict(frozen=True)

    #: The comment's content.
    text: str
    #: An optional type of the comment.
    type: typing.Optional[CommentType] = None
    #: An optional datasource name.
    datasource: typing.Optional[str] = None

    @classmethod
    def from_json_data(cls, json_data: dict) -> "Comment":
        if isinstance(json_data, str):
            return Comment(text=json_data)
        else:
            return Comment(
                type=CommentType(json_data["@Type"]) if json_data.get("@Type") else None,
                datasource=json_data.get("@DataSource"),
                text=json_data["#text"],
            )


class CitationIdentifier(BaseModel):
    """Type for a citation identifier"""

    model_config = ConfigDict(frozen=True)

    #: The identifier source.
    source: str
    #: The identifier value.
    value: str

    @classmethod
    def from_json_data(cls, json_data: dict) -> "CitationIdentifier":
        return CitationIdentifier(
            source=json_data["@Source"],
            value=json_data["#text"],
        )


class Citation(BaseModel):
    """Type for a citation"""

    model_config = ConfigDict(frozen=True)

    #: Citation identifiers.
    ids: typing.List[CitationIdentifier] = []
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
        return Citation(
            ids=[
                CitationIdentifier.from_json_data(raw_identifier)
                for raw_identifier in force_list(json_data.get("ID", []))
            ],
            type=json_data.get("@Type"),
            abbrev=json_data.get("@Abbrev"),
            url=json_data.get("URL"),
            citation_text=json_data.get("CitationText"),
        )


@enum.unique
class AssertionTypeSCV(enum.Enum):
    """The assertion types available for SCV records"""

    VARIATION_TO_DISEASE = "variation to disease"
    VARIATION_IN_MODIFIER_GENE_TO_DISEASE = "variation in modifier gene to disease"
    CONFERS_SENSITIVITY = "confers sensitivity"
    CONFERS_RESISTANCE = "confers resistance"
    VARIANT_TO_NAMED_PROTEIN_EFFECT = "variant to named protein"
    VARIATION_TO_INCLUDED_DISEASE = "variation to included disease"


class CustomAssertionScore(BaseModel):
    """A custom assertion score"""

    model_config = ConfigDict(frozen=True)

    #: Score value
    value: float
    #: Scoring scheme
    type: typing.Optional[str] = None

    @classmethod
    def from_json_data(cls, json_data: dict) -> "CustomAssertionScore":
        return CustomAssertionScore(
            value=float(json_data["#text"]),
            type=json_data.get("@type"),
        )


class ClinicalSignificanceTypeSCV(BaseModel):
    """The clinical significance from the SCV"""

    model_config = ConfigDict(frozen=True)

    #: The review status
    review_status: typing.Optional[ReviewStatus] = None
    #: We are not providing an enumeration for the values we report for clinical significance within the xsd.
    #: The values are maintained here: ftp://ftp.ncbi.nlm.nih.gov/pub/GTR/standard_terms/Clinical_significance.txt.
    descriptions: typing.List[ClinicalSignificanceDescription] = []
    #: Explanation is used only when the description is 'conflicting data from submitters'.
    #: The element summarizes the conflict.
    explanation: typing.Optional[Comment] = None
    #: Explanation for interpretation.
    explanation_of_interpretation: typing.Optional[str] = None
    #: Custom asertion scores.
    custom_assertion_score: typing.List[CustomAssertionScore] = []
    #: Cross-references.
    xrefs: typing.List[Xref] = []
    #: Citations
    citations: typing.List[Citation] = []
    #: Comments.
    comments: typing.List[Comment] = []
    #: Date of last evaluation.
    date_last_evaluated: typing.Optional[datetime.date] = None

    @classmethod
    def from_json_data(cls, json_data: dict) -> "ClinicalSignificanceTypeSCV":
        # Handle case of the following::
        #
        #     <ReviewStatus xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">\
        #     criteria provided, single submitter</ReviewStatus>
        #
        # In contrast to::
        #
        #     <ReviewStatus>criteria provided, single submitter</ReviewStatus>
        review_status = None
        if "ReviewStatus" in json_data:
            review_status = ReviewStatus(extract_text(json_data["ReviewStatus"]))

        # Same for the descriptions.
        descriptions = []
        for raw_description in force_list(json_data.get("Description", [])):
            value = extract_text(raw_description)
            if value:
                descriptions.append(ClinicalSignificanceDescription.from_the_wild(value.lower()))

        return ClinicalSignificanceTypeSCV(
            review_status=review_status,
            descriptions=descriptions,
            explanation=Comment.from_json_data(json_data["Explanation"])
            if json_data.get("Explanation")
            else None,
            explanation_of_interpretation=json_data.get("ExplanationOfInterpretation"),
            custom_assertion_score=[
                CustomAssertionScore(
                    value=float(raw_score["#text"]),
                    type=raw_score.get("@Type"),
                )
                for raw_score in force_list(json_data.get("CustomAssertionScore", []))
                if "#text" in raw_score
            ],
            xrefs=[
                Xref.from_json_data(raw_xref) for raw_xref in force_list(json_data.get("XRef", []))
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


class ClinicalSignificanceRCV(BaseModel):
    """The clinical significance from the RCV"""

    model_config = ConfigDict(frozen=True)

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
    xrefs: typing.List[Xref] = []
    #: Citations
    citations: typing.List[Citation] = []
    #: Comments.
    comments: typing.List[Comment] = []
    #: Date of last evaluation.
    date_last_evaluated: typing.Optional[datetime.date] = None

    @classmethod
    def from_json_data(cls, json_data: dict) -> "ClinicalSignificanceRCV":
        # Handle case of the following::
        #
        #     <ReviewStatus xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">\
        #     criteria provided, single submitter</ReviewStatus>
        #
        # In contrast to::
        #
        #     <ReviewStatus>criteria provided, single submitter</ReviewStatus>
        review_status = None
        if "ReviewStatus" in json_data:
            review_status = ReviewStatus(extract_text(json_data["ReviewStatus"]))

        # Same for the optional description.
        raw_description = extract_text(json_data.get("Description", None))
        description = None
        if raw_description:
            description = ClinicalSignificanceDescription.from_the_wild(raw_description.lower())

        return ClinicalSignificanceRCV(
            review_status=review_status,
            description=description,
            explanation=Comment.from_json_data(json_data["Explanation"])
            if "Explanation" in json_data
            else None,
            explanation_of_interpretation=json_data.get("ExplanationOfInterpretation"),
            xrefs=[
                Xref.from_json_data(raw_xref) for raw_xref in force_list(json_data.get("XRef", []))
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


class ReferenceClinVarAccession(BaseModel):
    """Accession for a reference ClinVar record"""

    model_config = ConfigDict(frozen=True)

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
    def from_json_data(cls, json_data: dict) -> "ReferenceClinVarAccession":
        return ReferenceClinVarAccession(
            acc=json_data["@Acc"],
            version=int(json_data["@Version"]),
            type=ClinVarAccessionType(json_data["@Type"]),
            date_updated=parse_datetime(json_data["@DateUpdated"]).date(),
            date_created=parse_datetime(json_data["@DateCreated"]).date(),
        )


@enum.unique
class ReferenceClinVarAssertionAttributeType(enum.Enum):
    """Type for an attribute in a ``ReferenceClinVarAssertion``"""

    MODE_OF_INHERITANCE = "ModeOfInheritance"
    PENETRANCE = "Penetrance"
    AGE_OF_ONSET = "AgeOfOnset"


class ReferenceClinVarAssertionAttribute(BaseModel):
    """Attribute for ``ReferenceClnVarAssertion``

    Corresponds to the ``<AttributeSet>`` elements.
    """

    model_config = ConfigDict(frozen=True)

    #: The attribute's value
    value: str
    #: The attribute's type
    type: ReferenceClinVarAssertionAttributeType
    #: The optional integer value provided in ClinVar public XML
    integer_value: typing.Optional[int] = None
    #: The optional date value provided in ClinVar public XML
    date_value: typing.Optional[datetime.date] = None
    #: Optional list of citations for this attribute
    citations: typing.List[Citation] = []
    #: Optional list of cross-references for this attribute
    xrefs: typing.List[Xref] = []
    #: Optional list of comments for this attribute
    comments: typing.List[Comment] = []

    @classmethod
    def from_json_data(cls, json_data: dict) -> "ReferenceClinVarAssertionAttribute":
        attribute = json_data["Attribute"]
        return ReferenceClinVarAssertionAttribute(
            # value of <Attribute> tag
            value=attribute["#text"],
            type=ReferenceClinVarAssertionAttributeType(attribute["@Type"]),
            integer_value=int(attribute["@integerValue"]) if "@integerValue" in attribute else None,
            date_value=parse_datetime(attribute["@dateValue"])
            if "@dateValue" in attribute
            else None,
            # other data in lists
            citations=[
                Citation.from_json_data(raw_citation)
                for raw_citation in force_list(json_data.get("Citation", []))
            ],
            xrefs=[
                Xref.from_json_data(raw_xref) for raw_xref in force_list(json_data.get("XRef", []))
            ],
            comments=[
                Comment.from_json_data(raw_comment)
                for raw_comment in force_list(json_data.get("Comment", []))
            ],
        )


@enum.unique
class Zygosity(enum.Enum):
    """Zygosity options"""

    HOMOZYGOTE = "Homozygote"
    SINGLE_HETEROZYGOTE = "SingleHeterozygote"
    COMPOUND_HETEROZYGOTE = "CompoundHeterozygote"
    HEMIZYGOTE = "Hemizygote"
    NOT_PROVIDED = "not provided"


@enum.unique
class RelativeOrientation(enum.Enum):
    """Relative orientation of two variants"""

    CIS = "cis"
    TRANS = "trans"
    UNKNOWN = "unknown"


class AlleleDescription(BaseModel):
    """Description of one allele for use in co-occurence description"""

    model_config = ConfigDict(frozen=True)

    #: Name of the allele
    name: str
    #: Relative orientation in variant co-occurence
    relative_orientation: typing.Optional[RelativeOrientation]
    #: Zygosity information
    zygosity: typing.Optional[Zygosity] = None
    #: Clinical significance description of variant
    clinical_significance: typing.Optional[ClinicalSignificanceRCV] = None

    @classmethod
    def from_json_data(cls, json_data: dict) -> "AlleleDescription":
        return AlleleDescription(
            name=json_data["Name"],
            relative_orientation=RelativeOrientation(json_data["RelativeOrientation"])
            if "RelativeOrientation" in json_data
            else None,
            zygosity=Zygosity(json_data["Zygosity"]) if "Zygosity" in json_data else None,
            clinical_significance=ClinicalSignificanceRCV.from_json_data(
                json_data["ClinicalSignificance"]
            )
            if "ClinicalSignificance" in json_data
            else None,
        )


class Cooccurrence(BaseModel):
    """Describes co-ocurrence of variants"""

    model_config = ConfigDict(frozen=True)

    #: The overall zygosity
    zygosity: typing.Optional[Zygosity] = None
    #: The description of the alleles
    allele_descriptions: typing.List[AlleleDescription] = []
    #: A count (undocumented in ClinVar XML)
    count: typing.Optional[int] = None

    @classmethod
    def from_json_data(cls, json_data: dict) -> "Cooccurrence":
        return Cooccurrence(
            zygosity=Zygosity(json_data["Zygosity"]) if "Zygosity" in json_data else None,
            allele_descriptions=[
                AlleleDescription.from_json_data(raw_allele_description)
                for raw_allele_description in force_list(json_data.get("AlleleDescSet", []))
            ],
            count=int(json_data["Count"]) if "Count" in json_data else None,
        )


@enum.unique
class ObservationMethod(enum.Enum):
    """Method for generating an observation"""

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
        """Convert values "from the wild" where sometimes invalid values are used.

        These are converted to ``Other``.
        """
        try:
            return ObservationMethod(str)
        except ValueError:
            return cls.OTHER


@enum.unique
class ObservedDataAttributeType(enum.Enum):
    """Type for an attribute in a ``ObservedData``"""

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


class ObservedDataAttribute(BaseModel):
    """Attribute for ``ObservedData``"""

    model_config = ConfigDict(frozen=True)

    #: The type of the attribute
    type: ObservedDataAttributeType
    #: The attribute's value
    value: typing.Optional[str] = None
    #: The optional integer value provided in ClinVar public XML
    integer_value: typing.Optional[int] = None
    #: The optional date value provided in ClinVar public XML
    date_value: typing.Optional[datetime.date] = None

    @classmethod
    def from_json_data(cls, json_data: dict) -> "ObservedDataAttribute":
        return ObservedDataAttribute(
            type=ObservedDataAttributeType(json_data["@Type"]),
            value=json_data.get("#text"),
            integer_value=int(json_data["@integerValue"]) if "@integerValue" in json_data else None,
            date_value=parse_datetime(json_data["@dateValue"])
            if "@dateValue" in json_data
            else None,
        )


@enum.unique
class Severity(enum.Enum):
    """Severity of a condition"""

    MILD = "mild"
    MODERATE = "moderate"
    SEVERE = "severe"


class ObservedData(BaseModel):
    """Store structured observed data"""

    model_config = ConfigDict(frozen=True)

    #: The core observation data
    attribute: ObservedDataAttribute
    #: Optional description of severity
    severity: typing.Optional[Severity] = None
    #: Optional list of citations
    citations: typing.List[Citation] = []
    #: Optional list of cross-references
    xrefs: typing.List[Xref] = []
    #: Optional list of comments
    comments: typing.List[Comment] = []

    @classmethod
    def from_json_data(cls, json_data: dict) -> "ObservedData":
        return ObservedData(
            attribute=ObservedDataAttribute.from_json_data(json_data["Attribute"]),
            severity=Severity(json_data["Severity"]) if "Severity" in json_data else None,
            citations=[
                Citation.from_json_data(raw_citation)
                for raw_citation in force_list(json_data.get("Citation", []))
            ],
            xrefs=[
                Xref.from_json_data(raw_xref) for raw_xref in force_list(json_data.get("XRef", []))
            ],
            comments=[
                Comment.from_json_data(raw_comment)
                for raw_comment in force_list(json_data.get("Comment", []))
            ],
        )


class SampleDescription(BaseModel):
    """Description of a sample with optional citation"""

    model_config = ConfigDict(frozen=True)

    #: The sample's description
    description: typing.Optional[Comment] = None
    #: A citation for the sample
    citation: typing.Optional[Citation] = None

    @classmethod
    def from_json_data(cls, json_data: dict) -> "SampleDescription":
        return SampleDescription(
            description=Comment.from_json_data(json_data["Description"])
            if "Description" in json_data
            else None,
            citation=Citation.from_json_data(json_data["Citation"])
            if "Citation" in json_data
            else None,
        )


class FamilyInfo(BaseModel):
    """Description of a family in an observation.

    If the details of the number of families and the de-identified pedigree id are not available,
    use FamilyHistory to describe what type of family data is available.  Can also be used to report
    'Yes' or 'No' if there are no more details.
    """

    model_config = ConfigDict(frozen=True)

    #: Family history description
    family_history: typing.Optional[str] = None
    #: Number of families with observations
    num_families: typing.Optional[int] = None
    #: Number of families with a varaint
    num_families_with_variant: typing.Optional[int] = None
    #: Number of families with observed segregation
    num_families_with_segregation_observed: typing.Optional[int] = None
    #: Pedigree identifier
    pedigree_id: typing.Optional[str] = None
    #: Whether segration was observeds
    segregation_observed: typing.Optional[bool] = None

    @classmethod
    def from_json_data(cls, json_data: dict) -> "FamilyInfo":
        return FamilyInfo(
            family_history=json_data.get("FamilyHistory"),
            num_families=int(json_data["@NumFamilies"]) if "@NumFamilies" in json_data else None,
            num_families_with_variant=int(json_data["@NumFamiliesWithVariant"])
            if "@NumFamiliesWithVariant" in json_data
            else None,
            num_families_with_segregation_observed=int(
                json_data["@NumFamiliesWithSegregationObserved"]
            )
            if "@NumFamiliesWithSegregationObserved" in json_data
            else None,
            pedigree_id=json_data.get("@PedigreeID"),
            segregation_observed=json_data["@SegregationObserved"] == "yes"
            if "@SegregationObserved" in json_data
            else None,
        )


@enum.unique
class SampleOrigin(enum.Enum):
    """Origin of a sample"""

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
    TESTED_INCONCLUSIVE = "tested inconclusive"
    NOT_APPLICABLE = "not applicable"
    EXPERIMENTALLY_GENERATED = "experimentally generated"

    @classmethod
    def from_the_wild(cls, s: str) -> "SampleOrigin":
        """Convert values "from the wild" where sometimes invalid values are used.

        These are converted to ``Other``.
        """
        try:
            return SampleOrigin(s.replace("-", " ").lower())
        except ValueError:
            return SampleOrigin.UNKNOWN


class Species(BaseModel):
    """Definition of the species of a sample"""

    model_config = ConfigDict(frozen=True)

    #: The species name
    value: str
    #: The taxonomy id
    taxonomy_id: typing.Optional[int] = None

    @classmethod
    def from_json_data(cls, json_data: typing.Union[dict, str]) -> "Species":
        if isinstance(json_data, str):
            return Species(
                value=json_data,
            )
        else:
            return Species(
                value=json_data["#text"],
                taxonomy_id=int(json_data["@TaxonomyId"]),
            )


@enum.unique
class AgeType(enum.Enum):
    """Type of an age or side of an age range"""

    MINIMUM = "minimum"
    MAXIMUM = "maximum"
    SINGLE = "single"


class Age(BaseModel):
    """Description of an age or a side of an age range"""

    model_config = ConfigDict(frozen=True)

    #: The unit of the age
    age_unit: str
    #: The age value
    value: int
    #: The type of the age (side of a range or single age)
    type: AgeType

    @classmethod
    def from_json_data(cls, json_data: dict) -> "Age":
        return Age(
            age_unit=json_data["@age_unit"],
            value=int(json_data["#text"]),
            type=AgeType(json_data["@Type"]),
        )


@enum.unique
class AffectedStatus(enum.Enum):
    """Affected status of a sample"""

    YES = "yes"
    NO = "no"
    NOT_PROVIDED = "not provided"
    UNKNOWN = "unknown"
    NOT_APPLICABLE = "not applicable"


@enum.unique
class Gender(enum.Enum):
    """Gender of a sample"""

    MALE = "male"
    FEMALE = "female"
    MIXED = "mixed"


@enum.unique
class SampleSource(enum.Enum):
    """Source of a sample"""

    SUBMITTER_GENERATED = "submitter generated"
    DATA_MINING = "data mining"


class TypedValue(BaseModel):
    """A typed value in a value set"""

    model_config = ConfigDict(frozen=True)

    #: The type description
    type: str
    #: The value
    value: typing.Optional[str] = None

    @classmethod
    def from_json_data(cls, json_data: dict) -> "TypedValue":
        return TypedValue(
            type=json_data["@Type"],
            value=json_data.get("#text"),
        )


class AnnotatedTypedValue(BaseModel):
    """A further annotated ``TypedValue``"""

    model_config = ConfigDict(frozen=True)

    #: The inner typed value
    value: TypedValue
    #: Optional list of citations
    citations: typing.List[Citation] = []
    #: Optional list of cross-references
    xrefs: typing.List[Xref] = []
    #: Optional list of comments
    comments: typing.List[Comment] = []

    @classmethod
    def from_json_data(cls, json_data: dict) -> "AnnotatedTypedValue":
        if "ElementValue" in json_data:
            value = TypedValue.from_json_data(json_data["ElementValue"])
        elif "Attribute" in json_data:
            value = TypedValue.from_json_data(json_data["Attribute"])
        else:
            raise TypeError(f"Expected ElementValue or Attribute in {json_data}")
        return AnnotatedTypedValue(
            value=value,
            citations=[
                Citation.from_json_data(raw_citation)
                for raw_citation in force_list(json_data.get("Citation", []))
            ],
            xrefs=[
                Xref.from_json_data(raw_xref) for raw_xref in force_list(json_data.get("XRef", []))
            ],
            comments=[
                Comment.from_json_data(raw_comment)
                for raw_comment in force_list(json_data.get("Comment", []))
            ],
        )


@enum.unique
class ClinicalFeaturesAffectedStatus(enum.Enum):
    """Affected status of a clinical feature"""

    PRESENT = "present"
    ABSENT = "absent"
    NOT_TESTED = "not tested"


@enum.unique
class SourceType(enum.Enum):
    """Type of a source"""

    LABORATORY = "laboratory"
    LSDB = "locus-specific database (LSDB)"
    CONSORTIUM = "consortium"
    RESOURCE = "resource"
    PATIENT_REGISTRY = "patient registry"
    OTHER = "other"


class Source(BaseModel):
    """Source information of some data"""

    model_config = ConfigDict(frozen=True)

    #: A standard term for the source of the information
    data_source: str
    #: The identifier used by the data source
    id: typing.Optional[str] = None
    #: Controlled terms to categorize the source of the information
    source_type: typing.Optional[SourceType] = None

    @classmethod
    def from_json_data(cls, json_data: dict) -> "Source":
        return Source(
            data_source=json_data["@DataSource"],
            id=json_data.get("@ID"),
            source_type=SourceType(json_data["@SourceType"])
            if json_data.get("@SourceType")
            else None,
        )


@enum.unique
class TraitRelationshipType(enum.Enum):
    """Type of a trait relationship"""

    PHENOCOPY = "phenocopy"
    SUBPHENOTYPE = "Subphenotype"
    DRUG_RESPONSE_AND_DIASEASE = "DrugResponseAndDisease"
    CO_OCCURRING_CONDITION = "co-occurring condition"
    FINDING_MEMBER = "Finding member"


class TraitRelationship(BaseModel):
    """Describe relations between two types"""

    model_config = ConfigDict(frozen=True)

    #: The type of the relationship
    type: TraitRelationshipType
    #: An optional identifier of the relationship
    id: typing.Optional[int] = None
    #: List of names
    names: typing.List[AnnotatedTypedValue] = []
    #: List of symbols
    symbols: typing.List[AnnotatedTypedValue] = []
    #: List of attributes
    attributes: typing.List[AnnotatedTypedValue] = []
    #: List of citations
    citations: typing.List[Citation] = []
    #: List of cross-references
    xrefs: typing.List[Xref] = []
    #: List of comments
    source: typing.List[Source] = []

    @classmethod
    def from_json_data(cls, json_data: dict) -> "TraitRelationship":
        return TraitRelationship(
            type=TraitRelationshipType(json_data["@Type"]),
            id=int(json_data["@ID"]) if "@ID" in json_data else None,
            names=[
                AnnotatedTypedValue.from_json_data(raw_name)
                for raw_name in force_list(json_data.get("Name", []))
            ],
            symbols=[
                AnnotatedTypedValue.from_json_data(raw_symbol)
                for raw_symbol in force_list(json_data.get("Symbol", []))
            ],
            attributes=[
                AnnotatedTypedValue.from_json_data(raw_attribute)
                for raw_attribute in force_list(json_data.get("AttributeSet", []))
            ],
            citations=[
                Citation.from_json_data(raw_citation)
                for raw_citation in force_list(json_data.get("Citation", []))
            ],
            xrefs=[
                Xref.from_json_data(raw_xref) for raw_xref in force_list(json_data.get("XRef", []))
            ],
            source=[
                Source.from_json_data(raw_source)
                for raw_source in force_list(json_data.get("Source", []))
            ],
        )


class ClinVarAssertionTraitRelationship(BaseModel):
    """Trait relationship for ``ClinVarAssertionTrait`` records"""

    model_config = ConfigDict(frozen=True)

    #: List of names
    names: typing.List[AnnotatedTypedValue] = []
    #: List of symbols
    symbols: typing.List[AnnotatedTypedValue] = []
    #: List of attributes
    attributes: typing.List[AnnotatedTypedValue] = []
    #: List of citations
    citations: typing.List[Citation] = []
    #: List of cross-references
    xrefs: typing.List[Xref] = []
    #: List of comments
    comments: typing.List[Comment] = []
    #: List of sources
    sources: typing.List[Source] = []

    @classmethod
    def from_json_data(cls, json_data: dict) -> "ClinVarAssertionTraitRelationship":
        return ClinVarAssertionTraitRelationship(
            names=[
                AnnotatedTypedValue.from_json_data(raw_name)
                for raw_name in force_list(json_data.get("Name", []))
            ],
            symbols=[
                AnnotatedTypedValue.from_json_data(raw_symbol)
                for raw_symbol in force_list(json_data.get("Symbol", []))
            ],
            attributes=[
                AnnotatedTypedValue.from_json_data(raw_attribute)
                for raw_attribute in force_list(json_data.get("AttributeSet", []))
            ],
            citations=[
                Citation.from_json_data(raw_citation)
                for raw_citation in force_list(json_data.get("Citation", []))
            ],
            xrefs=[
                Xref.from_json_data(raw_xref) for raw_xref in force_list(json_data.get("XRef", []))
            ],
            comments=[
                Comment.from_json_data(raw_comment)
                for raw_comment in force_list(json_data.get("Comment", []))
            ],
            sources=[
                Source.from_json_data(raw_source)
                for raw_source in force_list(json_data.get("Source", []))
            ],
        )


class ClinVarAssertionTrait(BaseModel):
    """Trait description for a ClinVar assertion"""

    model_config = ConfigDict(frozen=True)

    #: List of names
    names: typing.List[AnnotatedTypedValue] = []
    #: List of symbols
    symbols: typing.List[AnnotatedTypedValue] = []
    #: List of attributes
    attributes: typing.List[AnnotatedTypedValue] = []
    #: List of trait relationships
    trait_relationships: typing.List[TraitRelationship] = []
    #: List of citations
    citations: typing.List[Citation] = []
    #: List of cross-references
    xrefs: typing.List[Xref] = []
    #: List of comments
    comments: typing.List[Comment] = []
    #: List of sources
    sources: typing.List[Source] = []

    @classmethod
    def from_json_data(cls, json_data: dict) -> "ClinVarAssertionTrait":
        return ClinVarAssertionTrait(
            names=[
                AnnotatedTypedValue.from_json_data(raw_name)
                for raw_name in force_list(json_data.get("Name", []))
            ],
            symbols=[
                AnnotatedTypedValue.from_json_data(raw_symbol)
                for raw_symbol in force_list(json_data.get("Symbol", []))
            ],
            attributes=[
                AnnotatedTypedValue.from_json_data(raw_attribute)
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
                Xref.from_json_data(raw_xref) for raw_xref in force_list(json_data.get("XRef", []))
            ],
            comments=[
                Comment.from_json_data(raw_comment)
                for raw_comment in force_list(json_data.get("Comment", []))
            ],
            sources=[
                Source.from_json_data(raw_source)
                for raw_source in force_list(json_data.get("Source", []))
            ],
        )


@enum.unique
class TraitType(enum.Enum):
    """Type of a trait"""

    DISEASE = "Disease"
    DRUG_RESPONSE = "DrugResponse"
    BLOOD_GROUP = "BloodGroup"
    FINDING = "Finding"
    NAMED_PROTEIN_VARIANT = "NamedProteinVariant"
    PHENOTYPE_INSTRUCTION = "PhenotypeInstruction"


class Trait(BaseModel):
    """Trait description for trait sets"""

    model_config = ConfigDict(frozen=True)

    #: Type of the trait
    type: TraitType
    #: List of names
    names: typing.List[AnnotatedTypedValue] = []
    #: List of symbols
    symbols: typing.List[AnnotatedTypedValue] = []
    #: List of attributes
    attributes: typing.List[AnnotatedTypedValue] = []
    #: List of trait relationships
    trait_relationships: typing.List[TraitRelationship] = []
    #: List of citations
    citations: typing.List[Citation] = []
    #: List of cross-references
    xrefs: typing.List[Xref] = []
    #: List of comments
    comments: typing.List[Comment] = []
    #: List of sources
    sources: typing.List[Source] = []

    @classmethod
    def from_json_data(cls, json_data: dict) -> "Trait":
        return Trait(
            type=TraitType(json_data["@Type"]),
            names=[
                AnnotatedTypedValue.from_json_data(raw_name)
                for raw_name in force_list(json_data.get("Name", []))
            ],
            symbols=[
                AnnotatedTypedValue.from_json_data(raw_symbol)
                for raw_symbol in force_list(json_data.get("Symbol", []))
            ],
            attributes=[
                AnnotatedTypedValue.from_json_data(raw_attribute)
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
                Xref.from_json_data(raw_xref) for raw_xref in force_list(json_data.get("XRef", []))
            ],
            comments=[
                Comment.from_json_data(raw_comment)
                for raw_comment in force_list(json_data.get("Comment", []))
            ],
            sources=[
                Source.from_json_data(raw_source)
                for raw_source in force_list(json_data.get("Source", []))
            ],
        )


@enum.unique
class IndicationType(enum.Enum):
    """Type of an indication"""

    INDICATION = "Indication"


class Indication(BaseModel):
    """Connect trait to test"""

    model_config = ConfigDict(frozen=True)

    #: List of traits
    traits: typing.List[ClinVarAssertionTrait] = []
    #: List of names
    names: typing.List[AnnotatedTypedValue] = []
    #: List of symbols
    symbols: typing.List[AnnotatedTypedValue] = []
    #: List of attributes
    attributes: typing.List[AnnotatedTypedValue] = []
    #: List of citations
    citations: typing.List[Citation] = []
    #: List of cross-references
    xrefs: typing.List[Xref] = []
    #: List of comments
    comment: typing.Optional[Comment] = None
    #: The type of the indication
    type: typing.Optional[IndicationType] = None

    @classmethod
    def from_json_data(cls, json_data: dict) -> "Indication":
        return Indication(
            type=IndicationType(json_data["@Type"]),
            traits=[
                ClinVarAssertionTrait.from_json_data(raw_trait)
                for raw_trait in force_list(json_data.get("Trait", []))
            ],
            names=[
                AnnotatedTypedValue.from_json_data(raw_name)
                for raw_name in force_list(json_data.get("Name", []))
            ],
            symbols=[
                AnnotatedTypedValue.from_json_data(raw_symbol)
                for raw_symbol in force_list(json_data.get("Symbol", []))
            ],
            attributes=[
                AnnotatedTypedValue.from_json_data(raw_attribute)
                for raw_attribute in force_list(json_data.get("Attribute", []))
            ],
            citations=[
                Citation.from_json_data(raw_citation)
                for raw_citation in force_list(json_data.get("Citation", []))
            ],
            xrefs=[
                Xref.from_json_data(raw_xref) for raw_xref in force_list(json_data.get("XRef", []))
            ],
            comment=Comment.from_json_data(json_data["Comment"])
            if "Comment" in json_data
            else None,
        )


class Sample(BaseModel):
    """A sample from a ClinVar XML file"""

    model_config = ConfigDict(frozen=True)

    #: Sample description
    description: typing.Optional[SampleDescription] = None
    #: Sample origin
    origin: typing.Optional[SampleOrigin] = None
    #: Proband's ethnicity
    ethnicity: typing.Optional[str] = None
    #: Geographic origin
    geographic_origin: typing.Optional[str] = None
    #: Tissue
    tissue: typing.Optional[str] = None
    #: Cell line
    cell_line: typing.Optional[str] = None
    #: Species
    species: typing.Optional[Species] = None
    #: Age
    age: typing.List[Age] = []
    #: Strain
    strain: typing.Optional[str] = None
    #: Affected status
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
    #: Family data
    family_data: typing.Optional[FamilyInfo] = None
    #: Proband
    proband: typing.Optional[str] = None
    #: Indication
    indication: typing.Optional[Indication] = None
    #: List of citations
    citations: typing.List[Citation] = []
    #: List of cross-references
    xrefs: typing.List[Xref] = []
    #: List of comments
    comments: typing.List[Comment] = []
    #: Sample source
    source: typing.Optional[SampleSource] = None

    @classmethod
    def from_json_data(cls, json_data: dict) -> "Sample":
        origin = None
        if "Origin" in json_data:
            raw_origin = extract_text(json_data["Origin"])
            if raw_origin:
                origin = SampleOrigin.from_the_wild(raw_origin)
        return Sample(
            description=SampleDescription.from_json_data(json_data["SampleDescription"])
            if "SampleDescription" in json_data
            else None,
            origin=origin,
            ethnicity=json_data.get("Ethnicity"),
            geographic_origin=json_data.get("GeographicOrigin"),
            tissue=extract_text(json_data["Tissue"]) if "Tissue" in json_data else None,
            cell_line=json_data["CellLine"] if "CellLine" in json_data else None,
            species=Species.from_json_data(json_data["Species"])
            if ("Species" in json_data and json_data.get("Species"))
            else None,
            age=[Age.from_json_data(raw_age) for raw_age in force_list(json_data.get("Age", []))],
            strain=json_data.get("Strain"),
            affected_status=AffectedStatus(extract_text(json_data["AffectedStatus"]))
            if "AffectedStatus" in json_data
            else AffectedStatus.NOT_PROVIDED,
            number_tested=int(extract_text(json_data["NumberTested"]) or 0)
            if "NumberTested" in json_data
            else None,
            number_males=int(extract_text(json_data["NumberMales"]) or 0)
            if "NumberMales" in json_data
            else None,
            number_females=int(extract_text(json_data["NumberFemales"]) or 0)
            if "NumberFemales" in json_data
            else None,
            number_chr_tested=int(extract_text(json_data["NumberChrTested"]) or 0)
            if "NumberChrTested" in json_data
            else None,
            gender=Gender(extract_text(json_data["Gender"])) if "Gender" in json_data else None,
            family_data=FamilyInfo.from_json_data(json_data["FamilyData"])
            if "FamilyData" in json_data
            else None,
            proband=json_data.get("Proband"),
            indication=Indication.from_json_data(json_data["Indication"])
            if "Indication" in json_data
            else None,
            citations=[
                Citation.from_json_data(raw_citation)
                for raw_citation in force_list(json_data.get("Citation", []))
            ],
            xrefs=[
                Xref.from_json_data(raw_xref) for raw_xref in force_list(json_data.get("XRef", []))
            ],
            comments=[
                Comment.from_json_data(raw_comment)
                for raw_comment in force_list(json_data.get("Comment", []))
            ],
            source=SampleSource(json_data["SourceType"]) if "SourceType" in json_data else None,
        )


@enum.unique
class TraitSetType(enum.Enum):
    """Type of a trait set"""

    DISEASE = "Disease"
    DRUG_RESPONSE = "DrugResponse"
    FINDING = "Finding"
    PHENOTYPE_INSTRUCTION = "PhenotypeInstruction"
    TRAIT_CHOICE = "TraitChoice"


class TraitSet(BaseModel):
    """Description of a trait set"""

    model_config = ConfigDict(frozen=True)

    #: Type of the trait set
    type: TraitSetType
    #: List of traits
    traits: typing.List[Trait] = []
    #: Optional identifier
    id: typing.Optional[int] = None
    #: List of names
    names: typing.List[AnnotatedTypedValue] = []
    #: List of symbols
    symbols: typing.List[AnnotatedTypedValue] = []
    #: List of attributes
    attributes: typing.List[AnnotatedTypedValue] = []
    #: List of citations
    citations: typing.List[Citation] = []
    #: List of cross-references
    xrefs: typing.List[Xref] = []
    #: List of comments
    comments: typing.List[Comment] = []

    @classmethod
    def from_json_data(cls, json_data: dict) -> "TraitSet":
        return cls(
            type=TraitSetType(json_data["@Type"]),
            traits=[
                Trait.from_json_data(raw_trait)
                for raw_trait in force_list(json_data.get("Trait", []))
            ],
            id=int(json_data["@ID"]) if json_data.get("@ID") else None,
            names=[
                AnnotatedTypedValue.from_json_data(raw_name)
                for raw_name in force_list(json_data.get("Name", []))
            ],
            symbols=[
                AnnotatedTypedValue.from_json_data(raw_symbol)
                for raw_symbol in force_list(json_data.get("Symbol", []))
            ],
            attributes=[
                AnnotatedTypedValue.from_json_data(raw_attribute)
                for raw_attribute in force_list(json_data.get("AttributeSet", []))
            ],
            citations=[
                Citation.from_json_data(raw_citation)
                for raw_citation in force_list(json_data.get("Citation", []))
            ],
            xrefs=[
                Xref.from_json_data(raw_xref) for raw_xref in force_list(json_data.get("XRef", []))
            ],
            comments=[
                Comment.from_json_data(raw_comment)
                for raw_comment in force_list(json_data.get("Comment", []))
            ],
        )


class ObservationSet(BaseModel):
    """Documents in what populations or samples an allele or genotype has been observed
    relative to the described trait.

    Summary observations can be registered per submitted assertion, grouped by common
    citation, study type, origin, ethnicity, tissue, cell line, and species data. Not
    all options are valid per study type, but these will not be validated in the xsd.
    """

    model_config = ConfigDict(frozen=True)

    #: Sample in observation
    sample: Sample
    #: List of observation methods
    methods: typing.List[ObservationMethod] = []
    #: List of observed data
    observed_data: typing.List[ObservedData] = []
    #: Traits
    traits: typing.Optional[TraitSet] = None
    #: List of co-occurrences
    cooccurrences: typing.List[Cooccurrence] = []
    #: List of citations
    citations: typing.List[Citation] = []
    #: List of cross-references
    xrefs: typing.List[Xref] = []
    #: List of comments
    comments: typing.List[Comment] = []

    @classmethod
    def from_json_data(cls, json_data: dict) -> "ObservationSet":
        return ObservationSet(
            sample=Sample.from_json_data(json_data["Sample"]),
            methods=[
                ObservationMethod.from_the_wild(method["MethodType"])
                for method in force_list(json_data.get("Method", []))
            ],
            observed_data=[
                ObservedData.from_json_data(raw_observed_data)
                for raw_observed_data in force_list(json_data.get("ObservedData", []))
            ],
            traits=TraitSet.from_json_data(json_data["TraitSet"])
            if "TraitSet" in json_data
            else None,
            cooccurrences=[
                Cooccurrence.from_json_data(raw_cooccurrence)
                for raw_cooccurrence in force_list(json_data.get("Coocurrence", []))
            ],
            citations=[
                Citation.from_json_data(raw_citation)
                for raw_citation in force_list(json_data.get("Citation", []))
            ],
            xrefs=[
                Xref.from_json_data(raw_xref) for raw_xref in force_list(json_data.get("XRef", []))
            ],
            comments=[
                Comment.from_json_data(raw_comment)
                for raw_comment in force_list(json_data.get("Comment", []))
            ],
        )


@enum.unique
class AssertionType(enum.Enum):
    """The assertion types for RCV records"""

    VARIATION_TO_DISEASE = "variation to disease"
    VARIATION_IN_MODIFIER_GENE_TO_DISEASE = "variation in modifier gene to disease"
    CONFERS_SENSITIVITY = "confers sensitivity"
    CONFERS_RESISTANCE = "confers resistance"
    VARIANT_TO_NAMED_PROTEIN_EFFECT = "variant to named protein"


@enum.unique
class MeasureSetAttributeType(enum.Enum):
    """Type of an attribute in a measure set"""

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


class MeasureSetAttribute(BaseModel):
    """An attribute in a MeasureSet"""

    model_config = ConfigDict(frozen=True)

    #: Type of the attribute
    type: MeasureSetAttributeType
    #: Value of the attribute
    value: str
    #: Described change
    change: typing.Optional[str] = None
    #: Whether the attribute is MANE select
    mane_select: typing.Optional[bool] = None
    #: Whether the attribute is in MANE plus clinical
    mane_plus_clinical: typing.Optional[bool] = None
    #: List of citations
    citations: typing.List[Citation] = []
    #: List of cross-references
    xrefs: typing.List[Xref] = []
    #: List of comments
    comments: typing.List[Comment] = []

    @classmethod
    def from_json_data(cls, json_data: dict) -> "MeasureSetAttribute":
        attribute = json_data["Attribute"]
        return MeasureSetAttribute(
            type=MeasureSetAttributeType(attribute["@Type"]),
            value=attribute["#text"],
            change=attribute.get("@Change"),
            mane_select=attribute["@ManeSelect"] == "yes" if "@ManeSelect" in attribute else None,
            mane_plus_clinical=attribute["@ManePlusClinical"] == "yes"
            if "@ManePlusClinical" in attribute
            else None,
            citations=[
                Citation.from_json_data(raw_citation)
                for raw_citation in force_list(json_data.get("Citation", []))
            ],
            xrefs=[
                Xref.from_json_data(raw_xref) for raw_xref in force_list(json_data.get("XRef", []))
            ],
            comments=[
                Comment.from_json_data(raw_comment)
                for raw_comment in force_list(json_data.get("Comment", []))
            ],
        )


@enum.unique
class MeasureAttributeType(enum.Enum):
    """Type of an attribute in a measure type"""

    HGVS_GENOMIC_TOP_LEVEL = "HGVS, genomic, top level"
    HGVS_GENOMIC_TOP_LEVEL_PREVIOUS = "HGVS, genomic, top level, previous"
    HGVS_GENOMIC_TOP_LEVEL_OTHER = "HGVS, genomic, top level, other"
    HGVS_GENOMIC_REFSEQGENE = "HGVS, genomic, RefSeqGene"
    HGVS_GENOMIC_LRG = "HGVS, genomic, LRG"
    HGVS_GENOMIC = "HGVS, genomic"
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
    ABSOLUTE_COPY_NUMBER = "AbsoluteCopyNumber"
    REFERENCE_COPY_NUMBER = "ReferenceCopyNumber"
    COPY_NUMBER_TUPLE = "CopyNumberTuple"
    COSMIC = "COSMIC"
    SUBMITTER_VARIANT_ID = "SubmitterVariantId"
    ISCN_COORDINATES = "ISCNCoordinates"


class MeasureAttribute(BaseModel):
    """An attribute in a MeasureType"""

    model_config = ConfigDict(frozen=True)

    #: The type of the attribute
    type: MeasureAttributeType
    #: Value of the attribute
    value: typing.Optional[str] = None
    #: List of citations
    citations: typing.List[Citation] = []
    #: List of cross-references
    xrefs: typing.List[Xref] = []
    #: List of comments
    comments: typing.List[Comment] = []
    #: The optional integer value provided in ClinVar public XML
    integer_value: typing.Optional[int] = None
    #: The optional date value provided in ClinVar public XML
    date_value: typing.Optional[datetime.date] = None

    @classmethod
    def from_json_data(cls, json_data: dict) -> "MeasureAttribute":
        attribute = json_data["Attribute"]
        return MeasureAttribute(
            type=MeasureAttributeType(attribute["@Type"]),
            value=attribute.get("#text"),
            citations=[
                Citation.from_json_data(raw_citation)
                for raw_citation in force_list(json_data.get("Citation", []))
            ],
            xrefs=[
                Xref.from_json_data(raw_xref) for raw_xref in force_list(json_data.get("XRef", []))
            ],
            comments=[
                Comment.from_json_data(raw_comment)
                for raw_comment in force_list(json_data.get("Comment", []))
            ],
            integer_value=int(attribute["@integerValue"]) if "@integerValue" in attribute else None,
            date_value=parse_datetime(attribute["@dateValue"])
            if "@dateValue" in attribute
            else None,
        )


class AlleleFrequency(BaseModel):
    """Description of an allele frequency"""

    model_config = ConfigDict(frozen=True)

    #: AF value
    value: float
    #: AF source
    source: str
    #: URL
    url: typing.Optional[str] = None

    @classmethod
    def from_json_data(cls, json_data: dict) -> "AlleleFrequency":
        return AlleleFrequency(
            value=float(json_data["@Value"]),
            source=json_data["@Source"],
            url=json_data.get("@URL"),
        )


class GlobalMinorAlleleFrequency(BaseModel):
    """Description of a global minor allele frequency"""

    model_config = ConfigDict(frozen=True)

    #: MAF value
    value: float
    #: MAF source
    source: str
    #: Minor allele string
    minor_allele: typing.Optional[str] = None
    #: URL
    url: typing.Optional[str] = None

    @classmethod
    def from_json_data(cls, json_data: dict) -> "GlobalMinorAlleleFrequency":
        return GlobalMinorAlleleFrequency(
            value=float(json_data["@Value"]),
            source=json_data["@Source"],
            minor_allele=json_data.get("@MinorAllele"),
            url=json_data.get("@URL"),
        )


@enum.unique
class AssemblyStatus(enum.Enum):
    """Status of an assembly"""

    CURRENT = "current"
    PREVIOUS = "previous"


class SequenceLocation(BaseModel):
    """Description of a location on a sequence"""

    model_config = ConfigDict(frozen=True)

    #: Assembly of the location
    assembly: str
    #: Chromosome
    chr: str
    #: Accession
    accession: typing.Optional[str] = None
    #: Outer start position (1-based)
    outer_start: typing.Optional[int] = None
    #: Inner start position (1-based)
    inner_start: typing.Optional[int] = None
    #: Start position (1-based)
    start: typing.Optional[int] = None
    #: Stop position (1-based)
    stop: typing.Optional[int] = None
    #: Inner stop position (1-based)
    inner_stop: typing.Optional[int] = None
    #: Outer stop position (1-based)
    outer_stop: typing.Optional[int] = None
    #: Display start position (1-based)
    display_start: typing.Optional[int] = None
    #: Display stop position (1-based)
    display_stop: typing.Optional[int] = None
    #: Strand
    strand: typing.Optional[str] = None
    #: Variant length
    variant_length: typing.Optional[int] = None
    #: Reference allele
    reference_allele: typing.Optional[str] = None
    #: Alternate allele
    alternate_allele: typing.Optional[str] = None
    #: Assembly accession and version
    assembly_accession_version: typing.Optional[str] = None
    #: Assembly status
    assembly_status: typing.Optional[AssemblyStatus] = None
    #: Position in VCF
    position_vcf: typing.Optional[int] = None
    #: Reference allele in VCF
    reference_allele_vcf: typing.Optional[str] = None
    #: Alternate allele in VCF
    alternate_allele_vcf: typing.Optional[str] = None
    #: Whether the location is for display length
    for_display_length: typing.Optional[bool] = None

    @classmethod
    def from_json_data(cls, json_data: dict) -> "SequenceLocation":
        return SequenceLocation(
            assembly=json_data["@Assembly"],
            chr=json_data["@Chr"],
            accession=json_data.get("@Accession"),
            outer_start=int(json_data["@outerStart"]) if "@outerStart" in json_data else None,
            inner_start=int(json_data["@innerStart"]) if "@innerStart" in json_data else None,
            start=int(json_data["@start"]) if "@start" in json_data else None,
            stop=int(json_data["@stop"]) if "@stop" in json_data else None,
            inner_stop=int(json_data["@innerStop"]) if "@innerStop" in json_data else None,
            outer_stop=int(json_data["@outerStop"]) if "@outerStop" in json_data else None,
            display_start=int(json_data["@display_start"])
            if "@display_start" in json_data
            else None,
            display_stop=int(json_data["@display_stop"]) if "@display_stop" in json_data else None,
            strand=json_data.get("@Strand"),
            variant_length=int(json_data["@variantLength"])
            if "@variantLength" in json_data
            else None,
            reference_allele=json_data.get("@referenceAllele"),
            alternate_allele=json_data.get("@alternateAllele"),
            assembly_accession_version=json_data.get("@AssemblyAccessionVersion"),
            assembly_status=AssemblyStatus(json_data["@AssemblyStatus"])
            if "@AssemblyStatus" in json_data
            else None,
            position_vcf=int(json_data["@positionVCF"]) if "@positionVCF" in json_data else None,
            reference_allele_vcf=json_data.get("@referenceAlleleVCF"),
            alternate_allele_vcf=json_data.get("@alternateAlleleVCF"),
            for_display_length=json_data["@forDisplayLength"] == "true"
            if "@forDisplayLength" in json_data
            else None,
        )


@enum.unique
class MeasureRelationshipAttributeType(enum.Enum):
    """Type of an attribute in ``MeasureRelationship``"""

    HGVS = "HGVS"
    GENOTYPE = "genotype"
    HAPLOINSUFFICIENCY = "Haploinsufficiency"
    TRIPLOSENSITIVITY = "Triplosensitivity"
    GENE_RELATIONSHIPS = "gene relationships"


class MeasureRelationshipAttribute(BaseModel):
    """Attribute of a measure releationship"""

    model_config = ConfigDict(frozen=True)

    #: The attribute's value
    value: str
    #: The attribute's type
    type: MeasureRelationshipAttributeType
    #: The optional integer value provided in ClinVar public XML
    integer_value: typing.Optional[int] = None
    #: The optional date value provided in ClinVar public XML
    date_value: typing.Optional[datetime.date] = None
    #: List of citations
    citations: typing.List[Citation] = []
    #: List of cross-references
    xrefs: typing.List[Xref] = []
    #: List of comments
    comments: typing.List[Comment] = []

    @classmethod
    def from_json_data(cls, json_data: dict) -> "MeasureRelationshipAttribute":
        attribute = json_data["Attribute"]
        return MeasureRelationshipAttribute(
            # value of <Attribute> tag
            value=attribute["#text"],
            type=MeasureRelationshipAttributeType(attribute["@Type"]),
            integer_value=int(attribute["@integerValue"]) if "@integerValue" in attribute else None,
            date_value=parse_datetime(attribute["@dateValue"])
            if "@dateValue" in attribute
            else None,
            # other data in lists
            citations=[
                Citation.from_json_data(raw_citation)
                for raw_citation in force_list(json_data.get("Citation", []))
            ],
            xrefs=[
                Xref.from_json_data(raw_xref) for raw_xref in force_list(json_data.get("XRef", []))
            ],
            comments=[
                Comment.from_json_data(raw_comment)
                for raw_comment in force_list(json_data.get("Comment", []))
            ],
        )


@enum.unique
class MeasureRelationshipType(enum.Enum):
    VARIANT_IN_GENE = "variant in gene"
    COOCURRING_VARIANT = "co-occurring variant"
    WITHIN_SNIGLE_GENE = "within single gene"
    WITHIN_MULTIPLE_GENES_BY_OVERLAP = "within multiple genes by overlap"
    GENES_OVERLAPPED_BY_VARIANT = "genes overlapped by variant"
    NEAR_GENE_UPSTREAM = "near gene, upstream"
    NEAR_GENE_DOWNSTREAM = "near gene, downstream"
    ASSERTED_BUT_NOT_COMPUTED = "asserted, but not computed"


class MeasureRelationship(BaseModel):
    """Description of a measure relationship"""

    model_config = ConfigDict(frozen=True)

    #: Type of the measure relationship
    type: typing.Optional[MeasureRelationshipType] = None
    #: List of names
    names: typing.List[AnnotatedTypedValue] = []
    #: List of symbols
    symbols: typing.List[AnnotatedTypedValue] = []
    #: List of attributes
    attributes: typing.List[MeasureRelationshipAttribute] = []
    #: Sequence locations
    sequence_locations: typing.List[SequenceLocation] = []
    #: List of citations
    citations: typing.List[Citation] = []
    #: List of cross-references
    xrefs: typing.List[Xref] = []
    #: List of comments
    comments: typing.List[Comment] = []

    @classmethod
    def from_json_data(cls, json_data: dict) -> "MeasureRelationship":
        return MeasureRelationship(
            type=MeasureRelationshipType(json_data["@Type"]) if "@Type" in json_data else None,
            names=[
                AnnotatedTypedValue.from_json_data(raw_name)
                for raw_name in force_list(json_data.get("Name", []))
            ],
            symbols=[
                AnnotatedTypedValue.from_json_data(raw_symbol)
                for raw_symbol in force_list(json_data.get("Symbol", []))
            ],
            attributes=[
                MeasureRelationshipAttribute.from_json_data(raw_attribute)
                for raw_attribute in force_list(json_data.get("Attribute", []))
            ],
            sequence_locations=[
                SequenceLocation.from_json_data(raw_sequence_location)
                for raw_sequence_location in force_list(json_data.get("SequenceLocation", []))
            ],
            citations=[
                Citation.from_json_data(raw_citation)
                for raw_citation in force_list(json_data.get("Citation", []))
            ],
            xrefs=[
                Xref.from_json_data(raw_xref) for raw_xref in force_list(json_data.get("XRef", []))
            ],
            comments=[
                Comment.from_json_data(raw_comment)
                for raw_comment in force_list(json_data.get("Comment", []))
            ],
        )


@enum.unique
class MeasureType(enum.Enum):
    GENE = "gene"
    VARIATION = "variation"
    INSERTION = "insertion"
    DELETION = "deletion"
    SNV = "single nucleotide variant"
    INDEL = "indel"
    DUPLICATION = "duplication"
    TANDEM_DUPLICATION = "tandem duplication"
    STRUCTURAL_VARIANT = "structural variant"
    COPY_NUMBER_GAIN = "copy number gain"
    COPY_NUMBER_LOSS = "copy number loss"
    PROTEIN_ONLY = "protein only"
    MICROSATELLITE = "microsatellite"
    FUSION = "fusion"
    INVERSION = "inversion"
    TRANSLOCATION = "translocation"
    QTL = "qtl"
    COMPLEX = "complex"
    OTHER = "other"

    @classmethod
    def from_the_wild(cls, value: str) -> "MeasureType":
        """Convert values "from the wild" where sometimes invalid values are used.

        These are converted to ``Other``.
        """
        try:
            return MeasureType(value.lower().replace("-", " "))
        except ValueError:
            return MeasureType.OTHER


class Measure(BaseModel):
    """Description of a measures"""

    model_config = ConfigDict(frozen=True)

    #: Type of the measure
    type: typing.Optional[MeasureType] = None
    #: List of names
    names: typing.List[AnnotatedTypedValue] = []
    #: Canonical SPDI
    canonical_spdi: typing.Optional[str] = None
    #: List of symbols
    symbols: typing.List[AnnotatedTypedValue] = []
    #: List of attributes
    attributes: typing.List[MeasureAttribute] = []
    #: List of allele frequencies
    allele_frequencies: typing.List[AlleleFrequency] = []
    #: Global minor allele frequency
    global_minor_allele_frequency: typing.Optional[GlobalMinorAlleleFrequency] = None
    #: Cytogenic location
    cytogenic_locations: typing.List[str] = []
    #: Sequence location
    sequence_locations: typing.List[SequenceLocation] = []
    #: Measure relationship
    measure_relationship: typing.List[MeasureRelationship] = []
    #: List of citations
    citations: typing.List[Citation] = []
    #: List of cross-references
    xrefs: typing.List[Xref] = []
    #: List of comments
    comments: typing.List[Comment] = []
    #: List of sources
    source: typing.List[Source] = []
    #: Optional identifier
    id: typing.Optional[int] = None

    @classmethod
    def from_json_data(cls, json_data: dict) -> "Measure":
        return Measure(
            type=MeasureType.from_the_wild(json_data["@Type"]) if "@Type" in json_data else None,
            id=int(json_data["@ID"]) if "@ID" in json_data else None,
            names=[
                AnnotatedTypedValue.from_json_data(raw_name)
                for raw_name in force_list(json_data.get("Name", []))
            ],
            canonical_spdi=json_data.get("CanonicalSPDI"),
            symbols=[
                AnnotatedTypedValue.from_json_data(raw_symbol)
                for raw_symbol in force_list(json_data.get("Symbol", []))
            ],
            attributes=[
                MeasureAttribute.from_json_data(raw_attribute)
                for raw_attribute in force_list(json_data.get("AttributeSet", []))
            ],
            allele_frequencies=[
                AlleleFrequency.from_json_data(raw_allele_frequency)
                for raw_allele_frequency in force_list(json_data.get("AlleleFrequency", []))
            ],
            global_minor_allele_frequency=GlobalMinorAlleleFrequency.from_json_data(
                json_data["GlobalMinorAlleleFrequency"]
            )
            if "GlobalMinorAlleleFrequency" in json_data
            else None,
            cytogenic_locations=[
                raw_cytogenic_location
                for raw_cytogenic_location in force_list(json_data.get("CytogeneticLocation", []))
            ],
            sequence_locations=[
                SequenceLocation.from_json_data(raw_sequence_location)
                for raw_sequence_location in force_list(json_data.get("SequenceLocation", []))
            ],
            measure_relationship=[
                MeasureRelationship.from_json_data(raw_measure_relationship)
                for raw_measure_relationship in force_list(json_data.get("MeasureRelationship", []))
            ],
            citations=[
                Citation.from_json_data(raw_citation)
                for raw_citation in force_list(json_data.get("Citation", []))
            ],
            xrefs=[
                Xref.from_json_data(raw_xref) for raw_xref in force_list(json_data.get("XRef", []))
            ],
            comments=[
                Comment.from_json_data(raw_comment)
                for raw_comment in force_list(json_data.get("Comment", []))
            ],
            source=[
                Source.from_json_data(raw_source)
                for raw_source in force_list(json_data.get("Source", []))
            ],
        )


@enum.unique
class MeasureSetType(enum.Enum):
    """Type of a measure set"""

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


class MeasureSet(BaseModel):
    """A collection of ``Measure`` objects with further annotations"""

    model_config = ConfigDict(frozen=True)

    #: Type of the measure
    type: MeasureSetType
    #: Accession of the measure
    acc: typing.Optional[str] = None
    #: Version of the measure
    version: typing.Optional[int] = None
    #: List of measures
    measures: typing.List[Measure] = []
    #: List of names
    names: typing.List[AnnotatedTypedValue] = []
    #: List of symbols
    symbols: typing.List[AnnotatedTypedValue] = []
    #: List of attributes
    attributes: typing.List[MeasureSetAttribute] = []
    #: List of citations
    citations: typing.List[Citation] = []
    #: List of cross-references
    xrefs: typing.List[Xref] = []
    #: List of comments
    comments: typing.List[Comment] = []
    #: Number of chromosomes
    number_of_chromosomes: typing.Optional[int] = None
    #: Optional identifier
    id: typing.Optional[int] = None

    @classmethod
    def from_json_data(cls, json_data: dict) -> "MeasureSet":
        return MeasureSet(
            type=MeasureSetType(json_data["@Type"]),
            acc=json_data.get("@Acc"),
            version=int(json_data["@Version"]) if json_data.get("@Version") else None,
            measures=[
                Measure.from_json_data(raw_measure)
                for raw_measure in force_list(json_data.get("Measure", []))
            ],
            names=[
                AnnotatedTypedValue.from_json_data(raw_name)
                for raw_name in force_list(json_data.get("Name", []))
            ],
            symbols=[
                AnnotatedTypedValue.from_json_data(raw_symbol)
                for raw_symbol in force_list(json_data.get("Symbol", []))
            ],
            attributes=[
                MeasureSetAttribute.from_json_data(raw_attribute)
                for raw_attribute in force_list(json_data.get("AttributeSet", []))
            ],
            citations=[
                Citation.from_json_data(raw_citation)
                for raw_citation in force_list(json_data.get("Citation", []))
            ],
            xrefs=[
                Xref.from_json_data(raw_xref) for raw_xref in force_list(json_data.get("XRef", []))
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
    """Type for a genotype set"""

    COMPOUND_HETEROZYGOTE = "CompoundHeterozygote"
    DIPLOTYPE = "Diplotype"


class GenotypeSet(BaseModel):
    """Genotype set description (compound heterozygote or diplotype)"""

    model_config = ConfigDict(frozen=True)

    #: Type of the genotype set
    type: GenotypeSetType
    #: List of measures
    measures: typing.List[MeasureSet] = []
    #: List of names
    names: typing.List[AnnotatedTypedValue] = []
    #: List of symbols
    symbols: typing.List[AnnotatedTypedValue] = []
    #: List of attributes
    attributes: typing.List[MeasureSetAttribute] = []
    #: List of citations
    citations: typing.List[Citation] = []
    #: List of cross-references
    xrefs: typing.List[Xref] = []
    #: List of comments
    comments: typing.List[Comment] = []
    #: Optional identifier
    id: typing.Optional[int] = None
    #: Optional accession
    acc: typing.Optional[str] = None
    #: Optional version
    version: typing.Optional[str] = None

    @classmethod
    def from_json_data(cls, json_data: dict) -> "GenotypeSet":
        return GenotypeSet(
            type=GenotypeSetType(json_data["@Type"]),
            measures=[
                MeasureSet.from_json_data(raw_measure)
                for raw_measure in force_list(json_data.get("MeasureSet", []))
            ],
            names=[
                AnnotatedTypedValue.from_json_data(raw_name)
                for raw_name in force_list(json_data.get("Name", []))
            ],
            symbols=[
                AnnotatedTypedValue.from_json_data(raw_symbol)
                for raw_symbol in force_list(json_data.get("Symbol", []))
            ],
            attributes=[
                MeasureSetAttribute.from_json_data(raw_attribute)
                for raw_attribute in force_list(json_data.get("AttributeSet", []))
            ],
            citations=[
                Citation.from_json_data(raw_citation)
                for raw_citation in force_list(json_data.get("Citation", []))
            ],
            xrefs=[
                Xref.from_json_data(raw_xref) for raw_xref in force_list(json_data.get("XRef", []))
            ],
            comments=[
                Comment.from_json_data(raw_comment)
                for raw_comment in force_list(json_data.get("Comment", []))
            ],
            id=int(json_data["@ID"]) if json_data.get("@ID") else None,
            acc=json_data.get("@Acc"),
            version=json_data.get("@Version"),
        )


class ReferenceClinVarAssertion(BaseModel):
    """The reference ClinVar assertion"""

    model_config = ConfigDict(frozen=True)

    #: Accesion of the RCV record.
    clinvar_accession: ReferenceClinVarAccession
    #: Status of the record.
    record_status: RecordStatus
    #: Clinical significance summary of RCV record.
    clinical_significance: ClinicalSignificanceRCV
    #: The assertion RCV type.
    assertion: AssertionType
    #: Represents the public identifier a source may have for this record.
    external_ids: typing.List[Xref] = []
    #: Attributes of the RCV record
    attributes: typing.List[ReferenceClinVarAssertionAttribute] = []
    #: Observations.
    observed_in: typing.List[ObservationSet] = []
    #: Measurement information, mutually exlusive with ``genotypes``.
    measures: typing.Optional[MeasureSet] = None
    #: Genotyping information, mutually exlusive with ``measures``.
    genotypes: typing.Optional[GenotypeSet] = None
    #: List of traits
    traits: typing.Optional[TraitSet] = None
    #: List of citations
    citations: typing.List[Citation] = []
    #: List of comments
    comments: typing.List[Comment] = []
    #: Date created
    date_created: typing.Optional[datetime.date] = None
    #: Date last updated
    date_last_updated: typing.Optional[datetime.date] = None
    #: Submission date
    submission_date: typing.Optional[datetime.date] = None
    #: Optional identifier
    id: typing.Optional[int] = None

    @classmethod
    def from_json_data(cls, json_data: dict) -> "ReferenceClinVarAssertion":
        return ReferenceClinVarAssertion(
            clinvar_accession=ReferenceClinVarAccession.from_json_data(
                json_data["ClinVarAccession"]
            ),
            record_status=RecordStatus(json_data["RecordStatus"]),
            clinical_significance=ClinicalSignificanceRCV.from_json_data(
                json_data["ClinicalSignificance"]
            ),
            assertion=AssertionType(json_data["Assertion"]["@Type"]),
            external_ids=[
                Xref.from_json_data(raw_external_id)
                for raw_external_id in force_list(json_data.get("ExternalID", []))
            ],
            attributes=[
                ReferenceClinVarAssertionAttribute.from_json_data(raw_attribute)
                for raw_attribute in force_list(json_data.get("Attribute", []))
            ],
            observed_in=[
                ObservationSet.from_json_data(raw_observations)
                for raw_observations in force_list(json_data.get("ObservedIn", []))
            ],
            measures=MeasureSet.from_json_data(json_data["MeasureSet"])
            if json_data.get("MeasureSet")
            else None,
            genotypes=GenotypeSet.from_json_data(json_data["GenotypeSet"])
            if json_data.get("GenotypeSet")
            else None,
            traits=TraitSet.from_json_data(json_data["TraitSet"])
            if "TraitSet" in json_data
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


class ClinVarSubmissionId(BaseModel):
    """Corresponds to ``ClinVarSubmissionID`` in XML file"""

    model_config = ConfigDict(frozen=True)

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
    def from_json_data(cls, json_data: dict) -> "ClinVarSubmissionId":
        return ClinVarSubmissionId(
            local_key=json_data["@localKey"],
            submitter=json_data.get("@submitter"),
            title=json_data.get("@title"),
            submitted_assembly=json_data.get("@submittedAssembly"),
            submitter_date=parse_datetime(json_data["@submitterDate"] or "").date()
            if json_data.get("@submitterDate")
            else None,
            local_key_is_submitted=json_data.get("localKeyIsSubmitted") == "1"
            if json_data.get("localKeyIsSubmitted")
            else None,
        )


@enum.unique
class SubmitterType(enum.Enum):
    """Enumeration with ``Submitter.type``"""

    PRIMARY = "primary"
    SECONDARY = "secondary"
    BEHALF = "behalf"


class Submitter(BaseModel):
    """A structure to support reportng the name of a submitter, its org_id, and whether primary
    or secondary or behalf.

    Corresponds to ``SubmitterType`` in XML file.
    """

    model_config = ConfigDict(frozen=True)

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
            org_id=int(json_data["@OrgID"]) if "@OrgID" in json_data else None,
            category=json_data.get("@Category"),
        )


@enum.unique
class ClinVarAssertionAccessionType(enum.Enum):
    """ClinVar assertion accession type"""

    RCV = "RCV"
    SCV = "SCV"


class ClinVarAssertionAccession(BaseModel):
    """Accession number for a ClinVar record in a ``ClinVarAssertion``"""

    model_config = ConfigDict(frozen=True)

    #: The accession
    acc: str
    #: The version
    version: int
    #: The accession type
    type: ClinVarAssertionAccessionType
    #: The date that the latest update to the submitted record became public in ClinVar.
    date_updated: typing.Optional[datetime.date] = None
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
        return ClinVarAssertionAccession(
            acc=json_data["@Acc"],
            version=int(json_data["@Version"]),
            type=ClinVarAssertionAccessionType(json_data["@Type"]),
            date_updated=parse_datetime(json_data["@DateUpdated"] or "").date()
            if json_data.get("@DateUpdated")
            else None,
            date_created=parse_datetime(json_data["@DateCreated"] or "").date()
            if json_data.get("@DateCreated")
            else None,
            org_id=json_data.get("@OrgID"),
            org_abbreviation=json_data.get("@OrgAbbreviation"),
            org_type=json_data.get("@OrgType"),
            org_category=json_data.get("@OrganizationCategory"),
        )


class RecordHistory(BaseModel):
    """A structure to support reporting of an accession, its version, the date its status
    changed, and text describing that change.
    """

    model_config = ConfigDict(frozen=True)

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


@enum.unique
class ClinVarAssertionAttributeType(enum.Enum):
    MODE_OF_INHERITANCE = "ModeOfInheritance"
    PENETRANCE = "Penetrance"
    AGE_OF_ONSET = "AgeOfOnset"
    SEVERITY = "Severity"
    CLINICAL_SIGNIFICANCE_HISTORY = "ClinicalSignificanceHistory"
    SEVERITY_DESCRIPTION = "SeverityDescription"
    ASSERTION_METHOD = "AssertionMethod"


class ClinVarAssertionAttribute(BaseModel):
    model_config = ConfigDict(frozen=True)

    type: ClinVarAssertionAttributeType
    value: str

    @classmethod
    def from_json_data(cls, json_data: dict) -> "ClinVarAssertionAttribute":
        return cls(
            type=ClinVarAssertionAttributeType(json_data["@Type"]),
            value=json_data["#text"],
        )


class ClinVarAssertionAttributeSet(BaseModel):
    """AttributeSet is a package to represent a unit of information, the source(s) of that unit,
    identifiers representing that unit, and comments.
    """

    model_config = ConfigDict(frozen=True)

    #: Specification of the attribute set type.
    attribute: ClinVarAssertionAttribute
    #: List of citations
    citations: typing.List[Citation] = []
    #: List of Xrefs
    xrefs: typing.List[Xref] = []
    #: List of comments
    comments: typing.List[Comment] = []

    @classmethod
    def from_json_data(cls, json_data: dict) -> "ClinVarAssertionAttributeSet":
        return cls(
            attribute=ClinVarAssertionAttribute.from_json_data(json_data["Attribute"]),
            citations=[
                Citation.from_json_data(raw_citation)
                for raw_citation in force_list(json_data.get("Citation", []))
            ],
            xrefs=[
                Xref.from_json_data(raw_xref) for raw_xref in force_list(json_data.get("XRef", []))
            ],
            comments=[
                Comment.from_json_data(raw_comment)
                for raw_comment in force_list(json_data.get("Comment", []))
            ],
        )


class ClinAsserTraitSetTypeAttribute(BaseModel):
    model_config = ConfigDict(frozen=True)

    value: str
    type: str
    citations: typing.List[Citation] = []
    xrefs: typing.List[Xref] = []
    comments: typing.List[Comment] = []

    @classmethod
    def from_json_data(cls, json_data: dict) -> "ClinAsserTraitSetTypeAttribute":
        return cls(
            value=json_data["#text"],
            type=json_data["@Type"],
            citations=[
                Citation.from_json_data(raw_citation)
                for raw_citation in force_list(json_data.get("Citation", []))
            ],
            xrefs=[
                Xref.from_json_data(raw_xref) for raw_xref in force_list(json_data.get("XRef", []))
            ],
            comments=[
                Comment.from_json_data(raw_comment)
                for raw_comment in force_list(json_data.get("Comment", []))
            ],
        )


@enum.unique
class ClinVarAssertionTraitSetType(enum.Enum):
    DISEASE = "Disease"
    DRUG_RESPONSE = "DrugResponse"
    FINDING = "Finding"
    PHENOTYPE_INSTRUCITON = "PhenotypeInstruction"
    TRAIT_CHOICE = "TraitChoice"


class ClinVarAssertionTraitSet(BaseModel):
    model_config = ConfigDict(frozen=True)

    type: ClinVarAssertionTraitSetType
    date_last_evaluated: typing.Optional[datetime.date] = None
    traits: typing.List[ClinVarAssertionTrait] = []
    names: typing.List[AnnotatedTypedValue] = []
    symbols: typing.List[AnnotatedTypedValue] = []
    attributes: typing.List[ClinAsserTraitSetTypeAttribute] = []
    id: typing.Optional[int] = None
    multiple_condition_explanation: typing.Optional[str] = None

    @classmethod
    def from_json_data(cls, json_data: dict) -> "ClinVarAssertionTraitSet":
        return cls(
            type=ClinVarAssertionTraitSetType(json_data["@Type"]),
            date_last_evaluated=parse_datetime(json_data["@DateLastEvaluated"]).date()
            if json_data.get("@DateLastEvaluated")
            else None,
            traits=[
                ClinVarAssertionTrait.from_json_data(raw_trait)
                for raw_trait in force_list(json_data.get("Trait", []))
            ],
            names=[
                AnnotatedTypedValue.from_json_data(raw_name)
                for raw_name in force_list(json_data.get("Name", []))
            ],
            symbols=[
                AnnotatedTypedValue.from_json_data(raw_symbol)
                for raw_symbol in force_list(json_data.get("Symbol", []))
            ],
            attributes=[
                ClinAsserTraitSetTypeAttribute.from_json_data(raw_attribute)
                for raw_attribute in force_list(json_data.get("AttributeSet", []))
            ],
            id=int(json_data["@ID"]) if json_data.get("@ID") else None,
            multiple_condition_explanation=json_data.get("MultipleConditionExplanation"),
        )


class ClinVarAssertion(BaseModel):
    """The ClinVarAssertion is the package of data as received from the submitter. During
    integration with other submissions, the content may have been mapped to controlled values.

    Represents a ``ClinVarAssertion`` in the XML file.
    """

    model_config = ConfigDict(frozen=True)

    #: The submission's ID.
    id: int
    #: More detaield submission information.
    submission_id: ClinVarSubmissionId
    #: The ClinVar accession number.
    clinvar_accession: ClinVarAssertionAccession
    #: The assertion type.
    assertion_type: AssertionTypeSCV
    #: The record status
    record_status: RecordStatus = RecordStatus.CURRENT
    #: Optional element used only if there are multiple submitters. When there are multiple,
    #: each is listed in this element.
    additional_submitters: typing.List[Submitter] = []
    #: The list of SCV accessions this SCV record has replaced.
    replaced_list: typing.List[RecordHistory] = []
    #: The clinical significance assertion.
    clinical_significance: typing.List[ClinicalSignificanceTypeSCV] = []
    #: XrefType is used to identify data source(s) and their identifiers. Optional because
    #: not all sources have an ID specific to the assertion.
    external_ids: typing.List[Xref] = []
    #: Additional attribute sets.
    attributes: typing.List[ClinVarAssertionAttributeSet] = []
    #: Observation information.
    observed_in: typing.List[ObservationSet] = []
    #: Measurement information, mutually exlusive with ``genotype``.
    measures: typing.Optional[MeasureSet] = None
    #: Genotyping information, mutually exlusive with ``measure``.
    genotypes: typing.Optional[GenotypeSet] = None
    #: Traits associated with the disease.
    traits: typing.Optional[ClinVarAssertionTraitSet] = None
    #: Citations for the variant.
    citations: typing.List[Citation] = []
    #: An optional study name.
    study_name: typing.Optional[str] = None
    #: An optional study description.
    study_description: typing.Optional[str] = None
    #: Optional comments.
    comments: typing.List[Comment] = []

    @classmethod
    def from_json_data(cls, json_data: dict) -> "ClinVarAssertion":
        return ClinVarAssertion(
            id=int(json_data["@ID"]),
            submission_id=ClinVarSubmissionId.from_json_data(json_data["ClinVarSubmissionID"]),
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
                ClinicalSignificanceTypeSCV.from_json_data(raw_clinical_significance)
                for raw_clinical_significance in force_list(
                    json_data.get("ClinicalSignificance", [])
                )
            ],
            external_ids=[
                Xref.from_json_data(raw_xref)
                for raw_xref in force_list(json_data.get("ExternalID", []))
            ],
            attributes=[
                ClinVarAssertionAttributeSet.from_json_data(raw_attribute)
                for raw_attribute in force_list(json_data.get("AttributeSet", []))
            ],
            observed_in=[
                ObservationSet.from_json_data(raw_observations)
                for raw_observations in force_list(json_data.get("ObservedIn", []))
            ],
            measures=MeasureSet.from_json_data(json_data["MeasureSet"])
            if json_data.get("MeasureSet")
            else None,
            genotypes=GenotypeSet.from_json_data(json_data["GenotypeSet"])
            if json_data.get("GenotypeSet")
            else None,
            traits=ClinVarAssertionTraitSet.from_json_data(json_data["TraitSet"])
            if "TraitSet" in json_data
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


class ClinVarSet(BaseModel):
    """A ``<ClinVarSet>`` in the ClinVar public XML file"""

    model_config = ConfigDict(frozen=True)

    #: The reference clinvar assertion as used in RCV records
    reference_clinvar_assertion: ReferenceClinVarAssertion
    #: The set's record status
    record_status: RecordStatus = RecordStatus.CURRENT
    #: The identifiers that this record replaces
    replaces: typing.List[str] = []
    #: An optional title for the submission
    title: typing.Optional[str] = None
    #: The clinvar assertion
    clinvar_assertions: typing.List[ClinVarAssertion] = []

    @classmethod
    def from_json_data(cls, json_data: dict) -> "ClinVarSet":
        raw_clinvar_assertions = force_list(json_data["ClinVarAssertion"])

        result = ClinVarSet(
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
