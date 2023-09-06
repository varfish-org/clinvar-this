import datetime
import json

import cattrs
import pytest

from clinvar_data import conversion, models


def test_force_list_lst():
    assert models.force_list(1) == [1]
    assert models.force_list([1]) == [1]


@pytest.mark.parametrize(
    "input,expected",
    [
        (
            {"@DB": "MedGen", "@ID": "C1704981"},
            {"db": "MedGen", "id": "C1704981"},
        ),
        (
            {
                "@DB": "MedGen",
                "@ID": "C1704981",
                "@Type": "CUI",
                "@URL": "about:blank",
                "@Status": "current",
            },
            {
                "db": "MedGen",
                "id": "C1704981",
                "type": "CUI",
                "url": "about:blank",
                "status": "current",
            },
        ),
    ],
)
def test_xref_type_from_json_data(input, expected):
    obj = models.Xref.from_json_data(input)
    value = conversion.remove_empties_from_containers(cattrs.unstructure(obj))
    assert value == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        ("affects", models.ClinicalSignificanceDescription.AFFECTS),
        ("x", models.ClinicalSignificanceDescription.OTHER),
    ],
)
def test_clinical_significance_description_from_the_wild(value, expected):
    value = models.ClinicalSignificanceDescription.from_the_wild(value)
    assert value == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        ("comment text", {"text": "comment text"}),
        ({"#text": "comment text"}, {"text": "comment text"}),
        (
            {"@DataSource": "NCBI curation", "@Type": "public", "#text": "comment text"},
            {"text": "comment text", "type": "public", "datasource": "NCBI curation"},
        ),
    ],
)
def test_comment_from_json_data(value, expected):
    obj = models.Comment.from_json_data(value)
    value = conversion.remove_empties_from_containers(cattrs.unstructure(obj))
    assert value == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        ({"@Source": "PubMed", "#text": "9731074"}, {"source": "PubMed", "value": "9731074"}),
        ({"@Source": "PubMed", "#text": "123"}, {"source": "PubMed", "value": "123"}),
    ],
)
def test_citation_identifier_from_json_data(value, expected):
    obj = models.CitationIdentifier.from_json_data(value)
    value = conversion.remove_empties_from_containers(cattrs.unstructure(obj))
    assert value == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        (
            {"@Type": "general", "ID": {"@Source": "PubMed", "#text": "8547665"}},
            {"ids": [{"source": "PubMed", "value": "8547665"}], "type": "general"},
        ),
        ({"CitationText": "text here"}, {"citation_text": "text here"}),
        (
            {
                "@Type": "review",
                "@Abbrev": "GeneReviews",
                "ID": [
                    {"@Source": "PubMed", "#text": "29595935"},
                    {"@Source": "BookShelf", "#text": "NBK488189"},
                ],
            },
            {
                "abbrev": "GeneReviews",
                "ids": [
                    {"source": "PubMed", "value": "29595935"},
                    {"source": "BookShelf", "value": "NBK488189"},
                ],
                "type": "review",
            },
        ),
        (
            {"URL": "https://www.ncbi.nlm.nih.gov/projects/dbvar/ISCA/isca_gene.cgi?sym=NEFL"},
            {"url": "https://www.ncbi.nlm.nih.gov/projects/dbvar/ISCA/isca_gene.cgi?sym=NEFL"},
        ),
    ],
)
def test_citation_from_json_data(value, expected):
    obj = models.Citation.from_json_data(value)
    value = conversion.remove_empties_from_containers(cattrs.unstructure(obj))
    assert value == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        (
            {"@type": "ACMG/ClinGen CNV Guidelines, 2019", "#text": "3"},
            {"type": "ACMG/ClinGen CNV Guidelines, 2019", "value": 3.0},
        ),
        ({"@type": "Geneting testing", "#text": "5"}, {"type": "Geneting testing", "value": 5.0}),
        (
            {"@type": "ACMG/ClinGen CNV Guidelines, 2019", "#text": "0.95"},
            {"type": "ACMG/ClinGen CNV Guidelines, 2019", "value": 0.95},
        ),
    ],
)
def test_custom_assertion_score_from_json_data(value, expected):
    obj = models.CustomAssertionScore.from_json_data(value)
    value = conversion.remove_empties_from_containers(cattrs.unstructure(obj))
    assert value == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        (
            {
                "@DateLastEvaluated": "2010-09-09",
                "ReviewStatus": "no assertion criteria provided",
                "Description": "Pathogenic",
            },
            {
                "date_last_evaluated": datetime.date(2010, 9, 9),
                "descriptions": ["pathogenic"],
                "review_status": "no assertion criteria provided",
            },
        ),
        (
            {
                "@DateLastEvaluated": "2020-01-06",
                "ReviewStatus": "no assertion criteria provided",
                "Description": "Benign",
                "Comment": "comment text",
            },
            {
                "comments": [{"text": "comment text"}],
                "date_last_evaluated": datetime.date(2020, 1, 6),
                "descriptions": ["benign"],
                "review_status": "no assertion criteria provided",
            },
        ),
        (
            {
                "@DateLastEvaluated": "2020-04-16",
                "ReviewStatus": "no assertion criteria provided",
                "Description": "Pathogenic",
                "Citation": {"@Type": "general", "ID": {"@Source": "PubMed", "#text": "32576985"}},
            },
            {
                "citations": [
                    {"ids": [{"source": "PubMed", "value": "32576985"}], "type": "general"}
                ],
                "date_last_evaluated": datetime.date(2020, 4, 16),
                "descriptions": ["pathogenic"],
                "review_status": "no assertion criteria provided",
            },
        ),
        (
            {
                "@DateLastEvaluated": "2016-05-01",
                "ReviewStatus": "no assertion criteria provided",
                "Description": ["other", "other"],
                "ExplanationOfInterpretation": "explanation text",
            },
            {
                "date_last_evaluated": datetime.date(2016, 5, 1),
                "descriptions": ["other", "other"],
                "explanation_of_interpretation": "explanation text",
                "review_status": "no assertion criteria provided",
            },
        ),
        (
            {
                "@DateLastEvaluated": "2022-09-27",
                "ReviewStatus": {
                    "@xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
                    "#text": "criteria provided, single submitter",
                },
                "Description": [
                    {
                        "@xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
                        "#text": "Pathogenic",
                    },
                    {
                        "@xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
                        "#text": "Pathogenic",
                    },
                ],
            },
            {
                "date_last_evaluated": datetime.date(2022, 9, 27),
                "descriptions": ["pathogenic", "pathogenic"],
                "review_status": "criteria provided, single submitter",
            },
        ),
    ],
)
def test_clinical_significance_scv_from_json_data(value, expected):
    obj = models.ClinicalSignificanceTypeSCV.from_json_data(value)
    value = conversion.remove_empties_from_containers(cattrs.unstructure(obj))
    assert value == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        (
            {
                "@DateLastEvaluated": "2010-09-09",
                "ReviewStatus": "no assertion criteria provided",
                "Description": "Pathogenic",
            },
            {
                "date_last_evaluated": datetime.date(2010, 9, 9),
                "description": "pathogenic",
                "review_status": "no assertion criteria provided",
            },
        ),
        (
            {
                "@DateLastEvaluated": "2020-01-06",
                "ReviewStatus": "no assertion criteria provided",
                "Description": "Benign",
                "Comment": "comment text",
            },
            {
                "comments": [{"text": "comment text"}],
                "date_last_evaluated": datetime.date(2020, 1, 6),
                "description": "benign",
                "review_status": "no assertion criteria provided",
            },
        ),
        (
            {
                "@DateLastEvaluated": "2020-04-16",
                "ReviewStatus": "no assertion criteria provided",
                "Description": "Pathogenic",
                "Citation": {"@Type": "general", "ID": {"@Source": "PubMed", "#text": "32576985"}},
            },
            {
                "citations": [
                    {"ids": [{"source": "PubMed", "value": "32576985"}], "type": "general"}
                ],
                "date_last_evaluated": datetime.date(2020, 4, 16),
                "description": "pathogenic",
                "review_status": "no assertion criteria provided",
            },
        ),
        (
            {
                "@DateLastEvaluated": "2016-05-01",
                "ReviewStatus": "no assertion criteria provided",
                "Description": "other",
                "ExplanationOfInterpretation": "explanation text",
            },
            {
                "date_last_evaluated": datetime.date(2016, 5, 1),
                "description": "other",
                "explanation_of_interpretation": "explanation text",
                "review_status": "no assertion criteria provided",
            },
        ),
        (
            {
                "@DateLastEvaluated": "2022-09-27",
                "ReviewStatus": {
                    "@xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
                    "#text": "criteria provided, single submitter",
                },
                "Description": {
                    "@xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
                    "#text": "Pathogenic",
                },
            },
            {
                "date_last_evaluated": datetime.date(2022, 9, 27),
                "description": "pathogenic",
                "review_status": "criteria provided, single submitter",
            },
        ),
    ],
)
def test_clinical_significance_rcv_from_json_data(value, expected):
    obj = models.ClinicalSignificanceRCV.from_json_data(value)
    value = conversion.remove_empties_from_containers(cattrs.unstructure(obj))
    assert value == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        (
            {
                "@Acc": "RCV000000009",
                "@DateUpdated": "2022-04-23",
                "@DateCreated": "2013-04-04",
                "@Version": "4",
                "@Type": "RCV",
            },
            {
                "acc": "RCV000000009",
                "date_created": datetime.date(2013, 4, 4),
                "date_updated": datetime.date(2022, 4, 23),
                "type": "RCV",
                "version": 4,
            },
        ),
    ],
)
def test_reference_clinvar_accession_from_json_data(value, expected):
    obj = models.ReferenceClinVarAccession.from_json_data(value)
    value = conversion.remove_empties_from_containers(cattrs.unstructure(obj))
    assert value == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        (
            {
                "Attribute": {
                    "@Type": "ModeOfInheritance",
                    "@integerValue": "263",
                    "#text": "Autosomal recessive inheritance",
                }
            },
            {
                "integer_value": 263,
                "type": "ModeOfInheritance",
                "value": "Autosomal recessive inheritance",
            },
        ),
        (
            {
                "Attribute": {
                    "@Type": "ModeOfInheritance",
                    "@integerValue": "263",
                    "#text": "Autosomal recessive inheritance",
                },
                "XRef": {
                    "@ID": "FGDYS-ID3",
                    "@DB": "Laboratory of Molecular ...",
                },
            },
            {
                "integer_value": 263,
                "type": "ModeOfInheritance",
                "value": "Autosomal recessive inheritance",
                "xrefs": [{"db": "Laboratory of Molecular ...", "id": "FGDYS-ID3"}],
            },
        ),
    ],
)
def test_clinvar_accession_from_json_data(value, expected):
    obj = models.ReferenceClinVarAssertionAttribute.from_json_data(value)
    value = conversion.remove_empties_from_containers(cattrs.unstructure(obj))
    assert value == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        (
            {"Name": "ABCC8:c.2117-3C>T", "Zygosity": "SingleHeterozygote"},
            {"name": "ABCC8:c.2117-3C>T", "zygosity": "SingleHeterozygote"},
        ),
        (
            {
                "Name": "ABCC8:c.2117-3C>T",
                "Zygosity": "SingleHeterozygote",
                "RelativeOrientation": "cis",
            },
            {
                "name": "ABCC8:c.2117-3C>T",
                "relative_orientation": "cis",
                "zygosity": "SingleHeterozygote",
            },
        ),
    ],
)
def test_allele_description_from_json_data(value, expected):
    obj = models.AlleleDescription.from_json_data(value)
    value = conversion.remove_empties_from_containers(cattrs.unstructure(obj))
    assert value == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        (
            {
                "Zygosity": "SingleHeterozygote",
                "AlleleDescSet": [
                    {"Name": "ABCC8:c.2117-3C>T", "Zygosity": "SingleHeterozygote"},
                    {"Name": "KCNJ11:c.1009G>A", "Zygosity": "Homozygote"},
                ],
                "Count": "1",
            },
            {
                "allele_descriptions": [
                    {"name": "ABCC8:c.2117-3C>T", "zygosity": "SingleHeterozygote"},
                    {"name": "KCNJ11:c.1009G>A", "zygosity": "Homozygote"},
                ],
                "count": 1,
                "zygosity": "SingleHeterozygote",
            },
        ),
        (
            {
                "Zygosity": "SingleHeterozygote",
                "AlleleDescSet": [],
            },
            {"zygosity": "SingleHeterozygote"},
        ),
        (
            {},
            None,
        ),
    ],
)
def test_cooccurrence_from_json_data(value, expected):
    obj = models.Cooccurrence.from_json_data(value)
    value = conversion.remove_empties_from_containers(cattrs.unstructure(obj))
    assert value == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        ("curation", models.ObservationMethod.CURATION),
        ("x", models.ObservationMethod.OTHER),
    ],
)
def test_observation_method_from_the_wild(value, expected):
    value = models.ObservationMethod.from_the_wild(value)
    assert value == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        (
            {"@Type": "Description", "#text": "Tournamille et al. (1998) ..."},
            {"type": "Description", "value": "Tournamille et al. (1998) ..."},
        ),
    ],
)
def test_observed_data_attribute_from_json_data(value, expected):
    obj = models.ObservedDataAttribute.from_json_data(value)
    value = conversion.remove_empties_from_containers(cattrs.unstructure(obj))
    assert value == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        (
            {"Attribute": {"@Type": "Description", "#text": "not provided"}},
            {"attribute": {"type": "Description", "value": "not provided"}},
        ),
        (
            {
                "Attribute": {
                    "@Type": "Description",
                    "#text": "Tournamille et al. (1998) and Olsson et al. (1998)...",
                },
                "Citation": [
                    {"ID": {"@Source": "PubMed", "#text": "9731074"}},
                    {"ID": {"@Source": "PubMed", "#text": "9886340"}},
                ],
            },
            {
                "attribute": {
                    "type": "Description",
                    "value": "Tournamille et al. (1998) and Olsson et al. " "(1998)...",
                },
                "citations": [
                    {"ids": [{"source": "PubMed", "value": "9731074"}]},
                    {"ids": [{"source": "PubMed", "value": "9886340"}]},
                ],
            },
        ),
        (
            {
                "Attribute": {
                    "@Type": "Description",
                    "#text": "In a patient with chronic hemolytic...",
                },
                "Citation": {"ID": {"@Source": "PubMed", "#text": "6933565"}},
                "XRef": {"@DB": "OMIM", "@ID": "300653", "@Type": "MIM"},
            },
            {
                "attribute": {
                    "type": "Description",
                    "value": "In a patient with chronic hemolytic...",
                },
                "citations": [{"ids": [{"source": "PubMed", "value": "6933565"}]}],
                "xrefs": [{"db": "OMIM", "id": "300653", "type": "MIM"}],
            },
        ),
    ],
)
def test_observed_data_from_json_data(value, expected):
    obj = models.ObservedData.from_json_data(value)
    value = conversion.remove_empties_from_containers(cattrs.unstructure(obj))
    assert value == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        (
            {
                "Description": {
                    "@Type": "public",
                    "#text": "Phenotype: fine and gross motor delay...",
                }
            },
            {"description": {"text": "Phenotype: fine and gross motor delay...", "type": "public"}},
        ),
    ],
)
def test_sample_description_from_json_data(value, expected):
    obj = models.SampleDescription.from_json_data(value)
    value = conversion.remove_empties_from_containers(cattrs.unstructure(obj))
    assert value == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        (
            {
                "@NumFamiliesWithSegregationObserved": "1",
                "@NumFamiliesWithVariant": "1",
                "FamilyHistory": "yes",
            },
            {
                "family_history": "yes",
                "num_families_with_segregation_observed": 1,
                "num_families_with_variant": 1,
            },
        ),
        (
            {"@NumFamiliesWithVariant": "1", "FamilyHistory": "no"},
            {"family_history": "no", "num_families_with_variant": 1},
        ),
    ],
)
def test_family_info_from_json_data(value, expected):
    obj = models.FamilyInfo.from_json_data(value)
    value = conversion.remove_empties_from_containers(cattrs.unstructure(obj))
    assert value == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        (
            {"@TaxonomyId": "9606", "#text": "human"},
            {"taxonomy_id": 9606, "value": "human"},
        ),
        (
            "human",
            {"value": "human"},
        ),
    ],
)
def test_species_from_json_data(value, expected):
    obj = models.Species.from_json_data(value)
    value = conversion.remove_empties_from_containers(cattrs.unstructure(obj))
    assert value == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        (
            {"@Type": "minimum", "@age_unit": "years", "#text": "10"},
            {"age_unit": "years", "type": "minimum", "value": 10},
        ),
        (
            {"@Type": "maximum", "@age_unit": "years", "#text": "69"},
            {"age_unit": "years", "type": "maximum", "value": 69},
        ),
        (
            {"@Type": "single", "@age_unit": "years", "#text": "80"},
            {"age_unit": "years", "type": "single", "value": 80},
        ),
    ],
)
def test_age_from_json_data(value, expected):
    obj = models.Age.from_json_data(value)
    value = conversion.remove_empties_from_containers(cattrs.unstructure(obj))
    assert value == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        (
            {"@Type": "Preferred", "#text": "ACKR1"},
            {"type": "Preferred", "value": "ACKR1"},
        ),
        (
            {"@Type": "Preferred", "#text": "NM_002036.4(ACKR1):c.265C>T (p.Arg89Cys)"},
            {"type": "Preferred", "value": "NM_002036.4(ACKR1):c.265C>T (p.Arg89Cys)"},
        ),
        (
            {"@Type": "Alternate", "#text": "NM_001127505.2:c.155A>G(p.Tyr52Cys)"},
            {"type": "Alternate", "value": "NM_001127505.2:c.155A>G(p.Tyr52Cys)"},
        ),
    ],
)
def test_typed_value_from_json_data(value, expected):
    obj = models.TypedValue.from_json_data(value)
    value = conversion.remove_empties_from_containers(cattrs.unstructure(obj))
    assert value == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        (
            {
                "ElementValue": {
                    "@Type": "Preferred",
                    "#text": "NM_006642.5(SDCCAG8):c.1946_1949del (p.Cys649fs)",
                },
                "XRef": {"@ID": "CA113828", "@DB": "ClinGen"},
            },
            {
                "value": {
                    "type": "Preferred",
                    "value": "NM_006642.5(SDCCAG8):c.1946_1949del (p.Cys649fs)",
                },
                "xrefs": [{"db": "ClinGen", "id": "CA113828"}],
            },
        ),
    ],
)
def test_annotated_typed_value_from_json_data(value, expected):
    obj = models.AnnotatedTypedValue.from_json_data(value)
    value = conversion.remove_empties_from_containers(cattrs.unstructure(obj))
    assert value == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        (
            {"@DataSource": "MedGen", "@ID": "CN192494"},
            {"data_source": "MedGen", "id": "CN192494"},
        ),
        (
            {"@DataSource": "MedGen", "@ID": "CN192494", "@SourceType": "resource"},
            {"data_source": "MedGen", "id": "CN192494", "source_type": "resource"},
        ),
    ],
)
def test_source_from_json_data(value, expected):
    obj = models.Source.from_json_data(value)
    value = conversion.remove_empties_from_containers(cattrs.unstructure(obj))
    assert value == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        (
            {"@Type": "co-occurring condition", "@ID": "70"},
            {"id": 70, "type": "co-occurring condition"},
        ),
        (
            {
                "@Type": "DrugResponseAndDisease",
                "Name": {"ElementValue": {"@Type": "Preferred", "#text": "Breast Cancer"}},
            },
            {
                "names": [{"value": {"type": "Preferred", "value": "Breast Cancer"}}],
                "type": "DrugResponseAndDisease",
            },
        ),
        (
            {"@Type": "Finding member", "@ID": "890"},
            {"id": 890, "type": "Finding member"},
        ),
    ],
)
def test_trait_relationship_from_json_data(value, expected):
    obj = models.TraitRelationship.from_json_data(value)
    value = conversion.remove_empties_from_containers(cattrs.unstructure(obj))
    assert value == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        (
            {"Name": {"ElementValue": {"@Type": "Preferred", "#text": "BARDET-BIEDL SYNDROME 16"}}},
            {"names": [{"value": {"type": "Preferred", "value": "BARDET-BIEDL SYNDROME 16"}}]},
        ),
    ],
)
def test_clinvar_assertion_trait_relationship_from_json_data(value, expected):
    obj = models.ClinVarAssertionTraitRelationship.from_json_data(value)
    value = conversion.remove_empties_from_containers(cattrs.unstructure(obj))
    assert value == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        (
            {"Name": {"ElementValue": {"@Type": "Preferred", "#text": "BARDET-BIEDL SYNDROME 16"}}},
            {"names": [{"value": {"type": "Preferred", "value": "BARDET-BIEDL SYNDROME 16"}}]},
        ),
    ],
)
def test_clinvar_assertion_trait_from_json_data(value, expected):
    obj = models.ClinVarAssertionTrait.from_json_data(value)
    value = conversion.remove_empties_from_containers(cattrs.unstructure(obj))
    assert value == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        (
            {
                "@ID": "15693",
                "@Type": "BloodGroup",
                "Name": {
                    "ElementValue": {
                        "@Type": "Preferred",
                        "#text": "DUFFY BLOOD GROUP SYSTEM, FY(bwk) PHENOTYPE",
                    },
                    "XRef": {"@Type": "Allelic variant", "@ID": "613665.0003", "@DB": "OMIM"},
                },
            },
            {
                "names": [
                    {
                        "value": {
                            "type": "Preferred",
                            "value": "DUFFY BLOOD GROUP SYSTEM, FY(bwk) PHENOTYPE",
                        },
                        "xrefs": [{"db": "OMIM", "id": "613665.0003", "type": "Allelic variant"}],
                    }
                ],
                "type": "BloodGroup",
            },
        ),
    ],
)
def test_trait_from_json_data(value, expected):
    obj = models.Trait.from_json_data(value)
    value = conversion.remove_empties_from_containers(cattrs.unstructure(obj))
    assert value == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        (
            {
                "@Type": "Indication",
                "Trait": {
                    "@Type": "Finding",
                    "Name": {"ElementValue": {"@Type": "Preferred", "#text": "Diagnostic"}},
                },
            },
            {
                "traits": [{"names": [{"value": {"type": "Preferred", "value": "Diagnostic"}}]}],
                "type": "Indication",
            },
        ),
        (
            {
                "@Type": "Indication",
                "Trait": {
                    "@Type": "Finding",
                    "Name": {"ElementValue": {"@Type": "Preferred", "#text": "Vision phenotype"}},
                },
            },
            {
                "traits": [
                    {"names": [{"value": {"type": "Preferred", "value": "Vision phenotype"}}]}
                ],
                "type": "Indication",
            },
        ),
    ],
)
def test_indication_from_json_data(value, expected):
    obj = models.Indication.from_json_data(value)
    value = conversion.remove_empties_from_containers(cattrs.unstructure(obj))
    assert value == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        (
            {
                "Origin": "germline",
                "Species": {"@TaxonomyId": "9606", "#text": "human"},
                "AffectedStatus": "not provided",
            },
            {
                "affected_status": "not provided",
                "origin": "germline",
                "species": {"taxonomy_id": 9606, "value": "human"},
            },
        ),
        (
            {
                "Origin": "unknown",
                "Species": {"@TaxonomyId": "9606", "#text": "human"},
                "AffectedStatus": "not provided",
                "NumberTested": "3",
                "NumberMales": "1",
                "FamilyData": {"@NumFamilies": "1"},
            },
            {
                "affected_status": "not provided",
                "family_data": {"num_families": 1},
                "number_males": 1,
                "number_tested": 3,
                "origin": "unknown",
                "species": {"taxonomy_id": 9606, "value": "human"},
            },
        ),
    ],
)
def test_sample_from_json_data(value, expected):
    obj = models.Sample.from_json_data(value)
    value = conversion.remove_empties_from_containers(cattrs.unstructure(obj))
    assert value == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        (
            {
                "Sample": {
                    "Origin": "germline",
                    "Species": "human",
                    "AffectedStatus": "not provided",
                },
                "Method": {"MethodType": "literature only"},
                "ObservedData": [
                    {
                        "Attribute": {"@Type": "Description", "#text": "In a 27-week-old male ..."},
                        "Citation": {"ID": {"@Source": "PubMed", "#text": "19465910"}},
                        "XRef": {"@DB": "OMIM", "@ID": "610031", "@Type": "MIM"},
                    },
                    {
                        "Attribute": {
                            "@Type": "Description",
                            "#text": "Fallet-Bianco et al. (2014)...",
                        },
                        "Citation": {"ID": {"@Source": "PubMed", "#text": "25059107"}},
                    },
                ],
            },
            {
                "methods": ["literature only"],
                "observed_data": [
                    {
                        "attribute": {"type": "Description", "value": "In a 27-week-old male ..."},
                        "citations": [{"ids": [{"source": "PubMed", "value": "19465910"}]}],
                        "xrefs": [{"db": "OMIM", "id": "610031", "type": "MIM"}],
                    },
                    {
                        "attribute": {
                            "type": "Description",
                            "value": "Fallet-Bianco et al. (2014)...",
                        },
                        "citations": [{"ids": [{"source": "PubMed", "value": "25059107"}]}],
                    },
                ],
                "sample": {
                    "affected_status": "not provided",
                    "origin": "germline",
                    "species": {"value": "human"},
                },
            },
        ),
        (
            {
                "Sample": {
                    "Origin": "germline",
                    "Species": {"@TaxonomyId": "9606", "#text": "human"},
                    "AffectedStatus": "unknown",
                    "NumberTested": "1",
                },
                "Method": {"MethodType": "clinical testing"},
                "ObservedData": {
                    "@ID": "110387662",
                    "Attribute": {"@integerValue": "1", "@Type": "VariantAlleles"},
                },
            },
            {
                "methods": ["clinical testing"],
                "observed_data": [{"attribute": {"integer_value": 1, "type": "VariantAlleles"}}],
                "sample": {
                    "affected_status": "unknown",
                    "number_tested": 1,
                    "origin": "germline",
                    "species": {"taxonomy_id": 9606, "value": "human"},
                },
            },
        ),
    ],
)
def test_observation_set_from_json_data(value, expected):
    obj = models.ObservationSet.from_json_data(value)
    value = conversion.remove_empties_from_containers(cattrs.unstructure(obj))
    assert value == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        (
            {
                "Attribute": {
                    "@Accession": "NM_170784",
                    "@Version": "3",
                    "@Change": "c.281del",
                    "@Type": "HGVS, coding, RefSeq",
                    "@MANESelect": "true",
                    "#text": "NM_170784.3:c.281del",
                }
            },
            {"change": "c.281del", "type": "HGVS, coding, RefSeq", "value": "NM_170784.3:c.281del"},
        ),
        (
            {
                "Attribute": {
                    "@Accession": "NM_170784",
                    "@Version": "2",
                    "@Change": "c.281del",
                    "@Type": "HGVS, previous",
                    "#text": "NM_170784.2:c.281del",
                }
            },
            {"change": "c.281del", "type": "HGVS, previous", "value": "NM_170784.2:c.281del"},
        ),
        (
            {
                "Attribute": {"@Type": "MolecularConsequence", "#text": "frameshift variant"},
                "XRef": [
                    {"@ID": "SO:0001589", "@DB": "Sequence Ontology"},
                    {"@ID": "NM_018848.3:c.281del", "@DB": "RefSeq"},
                ],
            },
            {
                "type": "MolecularConsequence",
                "value": "frameshift variant",
                "xrefs": [
                    {"db": "Sequence Ontology", "id": "SO:0001589"},
                    {"db": "RefSeq", "id": "NM_018848.3:c.281del"},
                ],
            },
        ),
    ],
)
def test_measure_set_attribute_from_json_data(value, expected):
    obj = models.MeasureSetAttribute.from_json_data(value)
    value = conversion.remove_empties_from_containers(cattrs.unstructure(obj))
    assert value == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        (
            {
                "Attribute": {
                    "@Accession": "LRG_801t1",
                    "@Type": "HGVS, coding, LRG",
                    "#text": "LRG_801t1:c.265C>T",
                }
            },
            {"type": "HGVS, coding, LRG", "value": "LRG_801t1:c.265C>T"},
        ),
        (
            {
                "Attribute": {
                    "@Accession": "NM_002036",
                    "@Version": "4",
                    "@Change": "c.286_299del",
                    "@Type": "HGVS, coding, RefSeq",
                    "@MANESelect": "true",
                    "#text": "NM_002036.4:c.286_299del",
                }
            },
            {"type": "HGVS, coding, RefSeq", "value": "NM_002036.4:c.286_299del"},
        ),
    ],
)
def test_measure_type_attribute_from_json_data(value, expected):
    obj = models.MeasureAttribute.from_json_data(value)
    value = conversion.remove_empties_from_containers(cattrs.unstructure(obj))
    assert value == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        (
            {
                "@Value": "0.01099",
                "@Source": "NHLBI Exome Sequencing Project (ESP) Exome Variant Server",
            },
            {
                "source": "NHLBI Exome Sequencing Project (ESP) Exome Variant Server",
                "value": 0.01099,
            },
        ),
        (
            {"@Value": "0.00001", "@Source": "Exome Aggregation Consortium (ExAC)"},
            {"source": "Exome Aggregation Consortium (ExAC)", "value": 1e-05},
        ),
    ],
)
def test_allele_frequency_from_json_data(value, expected):
    obj = models.AlleleFrequency.from_json_data(value)
    value = conversion.remove_empties_from_containers(cattrs.unstructure(obj))
    assert value == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        (
            {"@Value": "0.00459", "@Source": "1000 Genomes Project", "@MinorAllele": "T"},
            {"minor_allele": "T", "source": "1000 Genomes Project", "value": 0.00459},
        ),
        (
            {"@Value": "0.00080", "@Source": "1000 Genomes Project", "@MinorAllele": "A"},
            {"minor_allele": "A", "source": "1000 Genomes Project", "value": 0.0008},
        ),
    ],
)
def test_global_minor_allele_frequency_from_json_data(value, expected):
    obj = models.GlobalMinorAlleleFrequency.from_json_data(value)
    value = conversion.remove_empties_from_containers(cattrs.unstructure(obj))
    assert value == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        (
            {
                "@Acc": "SCV000020152",
                "@DateCreated": "2013-04-04",
                "@DateUpdated": "2017-12-15",
                "@Version": "3",
                "@Type": "SCV",
                "@OrgID": "3",
                "@OrganizationCategory": "resource",
                "@OrgType": "primary",
            },
            {
                "acc": "SCV000020152",
                "date_created": datetime.date(2013, 4, 4),
                "date_updated": datetime.date(2017, 12, 15),
                "org_category": "resource",
                "org_id": "3",
                "org_type": "primary",
                "type": "SCV",
                "version": 3,
            },
        ),
    ],
)
def test_clinvar_assertion_accession_from_json_data(value, expected):
    obj = models.ClinVarAssertionAccession.from_json_data(value)
    value = conversion.remove_empties_from_containers(cattrs.unstructure(obj))
    assert value == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        (
            {
                "@Assembly": "GRCh38",
                "@AssemblyAccessionVersion": "GCF_000001405.38",
                "@AssemblyStatus": "current",
                "@Chr": "16",
                "@Accession": "NC_000016.10",
                "@start": "50742086",
                "@stop": "50801935",
                "@display_start": "50742086",
                "@display_stop": "50801935",
                "@Strand": "+",
            },
            {
                "accession": "NC_000016.10",
                "assembly": "GRCh38",
                "assembly_accesion_version": "GCF_000001405.38",
                "assembly_status": "current",
                "chr": "16",
                "display_start": 50742086,
                "display_stop": 50801935,
                "start": 50742086,
                "stop": 50801935,
                "strand": "+",
            },
        ),
        (
            {
                "@Assembly": "GRCh37",
                "@AssemblyAccessionVersion": "GCF_000001405.25",
                "@AssemblyStatus": "previous",
                "@Chr": "6",
                "@Accession": "NC_000006.11",
                "@start": "41129260",
                "@stop": "41129260",
                "@display_start": "41129260",
                "@display_stop": "41129260",
                "@variantLength": "1",
                "@positionVCF": "41129260",
                "@referenceAlleleVCF": "C",
                "@alternateAlleleVCF": "T",
            },
            {
                "accession": "NC_000006.11",
                "alternate_allele_vcf": "T",
                "assembly": "GRCh37",
                "assembly_accesion_version": "GCF_000001405.25",
                "assembly_status": "previous",
                "chr": "6",
                "display_start": 41129260,
                "display_stop": 41129260,
                "position_vcf": 41129260,
                "reference_allele_vcf": "C",
                "start": 41129260,
                "stop": 41129260,
                "variant_length": 1,
            },
        ),
    ],
)
def test_sequence_location_from_json_data(value, expected):
    obj = models.SequenceLocation.from_json_data(value)
    value = conversion.remove_empties_from_containers(cattrs.unstructure(obj))
    assert value == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        (
            {
                "Attribute": {
                    "@dateValue": "2020-05-27",
                    "@Type": "Haploinsufficiency",
                    "#text": "Little evidence for dosage pathogenicity",
                },
                "Citation": {
                    "URL": "https://www.ncbi.nlm.nih.gov/projects/dbvar/ISCA/isca_gene.cgi?sym=TAB2"
                },
            },
            {
                "citations": [
                    {
                        "url": "https://www.ncbi.nlm.nih.gov/projects/dbvar/ISCA/isca_gene.cgi?sym=TAB2"
                    }
                ],
                "date_value": datetime.datetime(2020, 5, 27, 0, 0),
                "type": "Haploinsufficiency",
                "value": "Little evidence for dosage pathogenicity",
            },
        ),
        (
            {
                "Attribute": {
                    "@dateValue": "2020-05-27",
                    "@Type": "Triplosensitivity",
                    "#text": "No evidence available",
                },
                "Citation": {
                    "URL": "https://www.ncbi.nlm.nih.gov/projects/dbvar/ISCA/isca_gene.cgi?sym=TAB2"
                },
            },
            {
                "citations": [
                    {
                        "url": "https://www.ncbi.nlm.nih.gov/projects/dbvar/ISCA/isca_gene.cgi?sym=TAB2"
                    }
                ],
                "date_value": datetime.datetime(2020, 5, 27, 0, 0),
                "type": "Triplosensitivity",
                "value": "No evidence available",
            },
        ),
    ],
)
def test_measure_relationship_attribute_from_json_data(value, expected):
    obj = models.MeasureRelationshipAttribute.from_json_data(value)
    value = conversion.remove_empties_from_containers(cattrs.unstructure(obj))
    assert value == expected


@pytest.mark.parametrize(
    "value",
    [
        {
            "@Type": "within single gene",
            "Name": {
                "ElementValue": {
                    "@Type": "Preferred",
                    "#text": "TGF-beta activated kinase 1 (MAP3K7) binding protein 2",
                }
            },
            "Symbol": {"ElementValue": {"@Type": "Preferred", "#text": "TAB2"}},
            "AttributeSet": [
                {
                    "Attribute": {
                        "@dateValue": "2020-05-27",
                        "@Type": "Haploinsufficiency",
                        "#text": "Little evidence for dosage pathogenicity",
                    },
                    "Citation": {
                        "URL": "https://www.ncbi.nlm.nih.gov/projects/dbvar/ISCA/isca_gene.cgi?sym=TAB2"
                    },
                },
                {
                    "Attribute": {
                        "@dateValue": "2020-05-27",
                        "@Type": "Triplosensitivity",
                        "#text": "No evidence available",
                    },
                    "Citation": {
                        "URL": "https://www.ncbi.nlm.nih.gov/projects/dbvar/ISCA/isca_gene.cgi?sym=TAB2"
                    },
                },
            ],
            "SequenceLocation": [
                {
                    "@Assembly": "GRCh38",
                    "@AssemblyAccessionVersion": "GCF_000001405.38",
                    "@AssemblyStatus": "current",
                    "@Chr": "6",
                    "@Accession": "NC_000006.12",
                    "@start": "149217926",
                    "@stop": "149411607",
                    "@display_start": "149217926",
                    "@display_stop": "149411607",
                    "@Strand": "+",
                },
            ],
            "XRef": [
                {"@ID": "23118", "@DB": "Gene"},
            ],
        },
    ],
)
def test_measure_relationship_from_json_data(value, snapshot):
    obj = models.MeasureRelationship.from_json_data(value)
    value = conversion.remove_empties_from_containers(cattrs.unstructure(obj))
    # NB: the input/expect output value pairs do not fit on one screen any more for
    # this test, so we use snapshot testing
    snapshot.assert_match(json.dumps(value, indent=2), "output")


@pytest.mark.parametrize(
    "value",
    [
        {
            "@Type": "Deletion",
            "@ID": "33436",
            "Name": [
                {
                    "ElementValue": {
                        "@Type": "Preferred",
                        "#text": "NM_002036.4(ACKR1):c.286_299del (p.Trp96fs)",
                    }
                },
                {
                    "ElementValue": {"@Type": "Alternate", "#text": "ACKR1, 14-BP DEL, NT286"},
                    "XRef": {"@Type": "Allelic variant", "@ID": "613665.0004", "@DB": "OMIM"},
                },
            ],
            "CanonicalSPDI": "NC_000001.11:159205718:CCTGGCTGGCCTGTCCTGGC:CCTGGC",
            "AttributeSet": [
                {
                    "Attribute": {
                        "@Accession": "LRG_801t1",
                        "@Type": "HGVS, coding, LRG",
                        "#text": "LRG_801t1:c.286_299del",
                    }
                },
            ],
            "CytogeneticLocation": "1q23.2",
            "SequenceLocation": [
                {
                    "@Assembly": "GRCh38",
                    "@AssemblyAccessionVersion": "GCF_000001405.38",
                    "@AssemblyStatus": "current",
                    "@Chr": "1",
                    "@Accession": "NC_000001.11",
                    "@start": "159205719",
                    "@stop": "159205732",
                    "@display_start": "159205719",
                    "@display_stop": "159205732",
                    "@variantLength": "14",
                    "@positionVCF": "159205718",
                    "@referenceAlleleVCF": "CCCTGGCTGGCCTGT",
                    "@alternateAlleleVCF": "C",
                },
            ],
            "MeasureRelationship": {
                "@Type": "within single gene",
                "Name": {
                    "ElementValue": {
                        "@Type": "Preferred",
                        "#text": "atypical chemokine receptor 1 (Duffy blood group)",
                    }
                },
                "Symbol": {"ElementValue": {"@Type": "Preferred", "#text": "ACKR1"}},
                "SequenceLocation": [
                    {
                        "@Assembly": "GRCh38",
                        "@AssemblyAccessionVersion": "GCF_000001405.38",
                        "@AssemblyStatus": "current",
                        "@Chr": "1",
                        "@Accession": "NC_000001.11",
                        "@start": "159204875",
                        "@stop": "159206500",
                        "@display_start": "159204875",
                        "@display_stop": "159206500",
                        "@Strand": "+",
                    },
                ],
                "XRef": [
                    {"@ID": "2532", "@DB": "Gene"},
                ],
            },
            "XRef": [
                {"@Type": "Allelic variant", "@ID": "613665.0004", "@DB": "OMIM"},
            ],
        }
    ],
)
def test_measure_from_json_data(value, snapshot):
    obj = models.Measure.from_json_data(value)
    value = conversion.remove_empties_from_containers(cattrs.unstructure(obj))
    # NB: the input/expect output value pairs do not fit on one screen any more for
    # this test, so we use snapshot testing
    snapshot.assert_match(json.dumps(value, indent=2), "output")


@pytest.mark.parametrize(
    "value",
    [
        {
            "@Type": "Variant",
            "@ID": "18397",
            "@Acc": "VCV000018397",
            "@Version": "1",
            "Measure": {
                "@Type": "Deletion",
                "@ID": "33436",
                "Name": [
                    {
                        "ElementValue": {
                            "@Type": "Preferred",
                            "#text": "NM_002036.4(ACKR1):c.286_299del (p.Trp96fs)",
                        }
                    },
                    {
                        "ElementValue": {"@Type": "Alternate", "#text": "ACKR1, 14-BP DEL, NT286"},
                        "XRef": {"@Type": "Allelic variant", "@ID": "613665.0004", "@DB": "OMIM"},
                    },
                ],
                "CanonicalSPDI": "NC_000001.11:159205718:CCTGGCTGGCCTGTCCTGGC:CCTGGC",
                "AttributeSet": [
                    {
                        "Attribute": {
                            "@Accession": "LRG_801t1",
                            "@Type": "HGVS, coding, LRG",
                            "#text": "LRG_801t1:c.286_299del",
                        }
                    },
                ],
                "CytogeneticLocation": "1q23.2",
                "SequenceLocation": [
                    {
                        "@Assembly": "GRCh38",
                        "@AssemblyAccessionVersion": "GCF_000001405.38",
                        "@AssemblyStatus": "current",
                        "@Chr": "1",
                        "@Accession": "NC_000001.11",
                        "@start": "159205719",
                        "@stop": "159205732",
                        "@display_start": "159205719",
                        "@display_stop": "159205732",
                        "@variantLength": "14",
                        "@positionVCF": "159205718",
                        "@referenceAlleleVCF": "CCCTGGCTGGCCTGT",
                        "@alternateAlleleVCF": "C",
                    },
                ],
                "MeasureRelationship": {
                    "@Type": "within single gene",
                    "Name": {
                        "ElementValue": {
                            "@Type": "Preferred",
                            "#text": "atypical chemokine receptor 1 (Duffy blood group)",
                        }
                    },
                    "Symbol": {"ElementValue": {"@Type": "Preferred", "#text": "ACKR1"}},
                    "SequenceLocation": [
                        {
                            "@Assembly": "GRCh38",
                            "@AssemblyAccessionVersion": "GCF_000001405.38",
                            "@AssemblyStatus": "current",
                            "@Chr": "1",
                            "@Accession": "NC_000001.11",
                            "@start": "159204875",
                            "@stop": "159206500",
                            "@display_start": "159204875",
                            "@display_stop": "159206500",
                            "@Strand": "+",
                        },
                    ],
                    "XRef": [
                        {"@ID": "2532", "@DB": "Gene"},
                    ],
                },
                "XRef": [
                    {"@Type": "Allelic variant", "@ID": "613665.0004", "@DB": "OMIM"},
                ],
            },
            "Name": {
                "ElementValue": {
                    "@Type": "Preferred",
                    "#text": "NM_002036.4(ACKR1):c.286_299del (p.Trp96fs)",
                }
            },
            "XRef": {"@ID": "CA113791", "@DB": "ClinGen"},
        },
    ],
)
def test_measure_set_from_json_data(value, snapshot):
    obj = models.MeasureSet.from_json_data(value)
    value = conversion.remove_empties_from_containers(cattrs.unstructure(obj))
    snapshot.assert_match(json.dumps(value, indent=2), "output")


@pytest.mark.parametrize(
    "value,expected",
    [
        (
            {
                "@Type": "CompoundHeterozygote",
                "MeasureSet": [
                    {
                        "@Type": "Variant",
                        "Measure": {
                            "@Type": "Variation",
                            "AttributeSet": {
                                "Attribute": {"@Type": "HGVS", "#text": "NM_000497.3:c.1024C>T"}
                            },
                            "MeasureRelationship": {
                                "@Type": "variant in gene",
                                "Symbol": {
                                    "ElementValue": {"@Type": "Preferred", "#text": "CYP11B1"}
                                },
                            },
                        },
                    },
                    {
                        "@Type": "Variant",
                        "Measure": {
                            "@Type": "Variation",
                            "AttributeSet": {
                                "Attribute": {"@Type": "HGVS", "#text": "NM_000497.3:c.1012dup"}
                            },
                            "MeasureRelationship": {
                                "@Type": "variant in gene",
                                "Symbol": {
                                    "ElementValue": {"@Type": "Preferred", "#text": "CYP11B1"}
                                },
                            },
                        },
                    },
                ],
                "Name": {
                    "ElementValue": {
                        "@Type": "Preferred",
                        "#text": "NM_000497.3:c.[1024C>T];[1012dup]",
                    }
                },
            },
            {
                "measures": [
                    {
                        "measures": [
                            {
                                "attributes": [{"type": "HGVS", "value": "NM_000497.3:c.1024C>T"}],
                                "measure_relationship": [
                                    {
                                        "symbols": [
                                            {"value": {"type": "Preferred", "value": "CYP11B1"}}
                                        ]
                                    }
                                ],
                            }
                        ],
                        "type": "Variant",
                    },
                    {
                        "measures": [
                            {
                                "attributes": [{"type": "HGVS", "value": "NM_000497.3:c.1012dup"}],
                                "measure_relationship": [
                                    {
                                        "symbols": [
                                            {"value": {"type": "Preferred", "value": "CYP11B1"}}
                                        ]
                                    }
                                ],
                            }
                        ],
                        "type": "Variant",
                    },
                ],
                "names": [
                    {"value": {"type": "Preferred", "value": "NM_000497.3:c.[1024C>T];[1012dup]"}}
                ],
                "type": "CompoundHeterozygote",
            },
        )
    ],
)
def test_genotype_set_from_json_data(value, expected):
    obj = models.GenotypeSet.from_json_data(value)
    value = conversion.remove_empties_from_containers(cattrs.unstructure(obj))
    assert value == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        (
            {
                "@Type": "Disease",
                "Trait": {
                    "@Type": "Disease",
                    "Name": {
                        "ElementValue": {
                            "@Type": "Preferred",
                            "#text": "BARDET-BIEDL SYNDROME 2/6, DIGENIC",
                        }
                    },
                },
            },
            {
                "traits": [
                    {
                        "names": [
                            {
                                "value": {
                                    "type": "Preferred",
                                    "value": "BARDET-BIEDL SYNDROME 2/6, " "DIGENIC",
                                }
                            }
                        ],
                        "type": "Disease",
                    }
                ],
                "type": "Disease",
            },
        )
    ],
)
def test_trait_set_from_json_data(value, expected):
    obj = models.TraitSet.from_json_data(value)
    value = conversion.remove_empties_from_containers(cattrs.unstructure(obj))
    assert value == expected


@pytest.mark.parametrize(
    "value",
    [
        {
            "@ID": "63146",
            "@DateLastUpdated": "2022-04-23",
            "@DateCreated": "2013-04-04",
            "ClinVarAccession": {
                "@Acc": "RCV000005643",
                "@DateUpdated": "2022-04-23",
                "@DateCreated": "2013-04-04",
                "@Version": "4",
                "@Type": "RCV",
            },
            "RecordStatus": "current",
            "ClinicalSignificance": {
                "@DateLastEvaluated": "2001-09-21",
                "ReviewStatus": "no assertion criteria provided",
                "Description": "Pathogenic",
            },
            "Assertion": {"@Type": "variation to disease"},
            "ObservedIn": {
                "Sample": {
                    "Origin": "germline",
                    "Species": {"@TaxonomyId": "9606", "#text": "human"},
                    "AffectedStatus": "not provided",
                },
                "Method": {"MethodType": "literature only"},
                "ObservedData": {
                    "@ID": "96578166",
                    "Attribute": {
                        "@Type": "Description",
                        "#text": "In a patient carrying 2 different termination codons in the BBS2 gene (606151.0003, 606151.0004), Katsanis et al. (2001) identified a nonsense mutation in the BBS6 gene, a glutamine-to-termination substitution at codon 147.",
                    },
                    "Citation": {
                        "@Type": "general",
                        "ID": {"@Source": "PubMed", "#text": "11567139"},
                    },
                },
            },
            "MeasureSet": {
                "@Type": "Variant",
                "@ID": "5318",
                "@Acc": "VCV000005318",
                "@Version": "1",
                "Measure": {
                    "@Type": "single nucleotide variant",
                    "@ID": "20357",
                    "Name": [
                        {
                            "ElementValue": {
                                "@Type": "Preferred",
                                "#text": "NM_170784.3(MKKS):c.442C>T (p.Gln148Ter)",
                            }
                        },
                        {
                            "ElementValue": {"@Type": "Alternate", "#text": "Q147*"},
                            "XRef": {
                                "@Type": "Allelic variant",
                                "@ID": "604896.0012",
                                "@DB": "OMIM",
                            },
                        },
                    ],
                    "CanonicalSPDI": "NC_000020.11:10413072:G:A",
                    "AttributeSet": [
                        {
                            "Attribute": {
                                "@Accession": "NM_018848",
                                "@Version": "3",
                                "@Change": "c.442C>T",
                                "@Type": "HGVS, coding, RefSeq",
                                "#text": "NM_018848.3:c.442C>T",
                            }
                        },
                        {
                            "Attribute": {
                                "@Accession": "NM_170784",
                                "@Version": "3",
                                "@Change": "c.442C>T",
                                "@Type": "HGVS, coding, RefSeq",
                                "@MANESelect": "true",
                                "#text": "NM_170784.3:c.442C>T",
                            }
                        },
                        {
                            "Attribute": {
                                "@Accession": "NG_009109",
                                "@Version": "2",
                                "@Change": "g.26146C>T",
                                "@Type": "HGVS, genomic, RefSeqGene",
                                "#text": "NG_009109.2:g.26146C>T",
                            }
                        },
                        {
                            "Attribute": {
                                "@Accession": "NC_000020",
                                "@Version": "11",
                                "@Change": "g.10413073G>A",
                                "@Type": "HGVS, genomic, top level",
                                "@integerValue": "38",
                                "#text": "NC_000020.11:g.10413073G>A",
                            }
                        },
                        {
                            "Attribute": {
                                "@Accession": "NC_000020",
                                "@Version": "10",
                                "@Change": "g.10393721G>A",
                                "@Type": "HGVS, genomic, top level, previous",
                                "@integerValue": "37",
                                "#text": "NC_000020.10:g.10393721G>A",
                            }
                        },
                        {
                            "Attribute": {
                                "@Accession": "NP_061336",
                                "@Version": "1",
                                "@Change": "p.Gln148Ter",
                                "@Type": "HGVS, protein, RefSeq",
                                "#text": "NP_061336.1:p.Gln148Ter",
                            }
                        },
                        {
                            "Attribute": {
                                "@Accession": "NP_740754",
                                "@Version": "1",
                                "@Change": "p.Gln148Ter",
                                "@Type": "HGVS, protein, RefSeq",
                                "#text": "NP_740754.1:p.Gln148Ter",
                            }
                        },
                        {
                            "Attribute": {"@Type": "MolecularConsequence", "#text": "nonsense"},
                            "XRef": [
                                {"@ID": "SO:0001587", "@DB": "Sequence Ontology"},
                                {"@ID": "NM_018848.3:c.442C>T", "@DB": "RefSeq"},
                            ],
                        },
                        {
                            "Attribute": {"@Type": "MolecularConsequence", "#text": "nonsense"},
                            "XRef": [
                                {"@ID": "SO:0001587", "@DB": "Sequence Ontology"},
                                {"@ID": "NM_170784.3:c.442C>T", "@DB": "RefSeq"},
                            ],
                        },
                        {"Attribute": {"@Type": "ProteinChange1LetterCode", "#text": "Q148*"}},
                        {"Attribute": {"@Type": "ProteinChange3LetterCode", "#text": "GLN147TER"}},
                    ],
                    "CytogeneticLocation": "20p12.2",
                    "SequenceLocation": [
                        {
                            "@Assembly": "GRCh38",
                            "@AssemblyAccessionVersion": "GCF_000001405.38",
                            "@AssemblyStatus": "current",
                            "@Chr": "20",
                            "@Accession": "NC_000020.11",
                            "@start": "10413073",
                            "@stop": "10413073",
                            "@display_start": "10413073",
                            "@display_stop": "10413073",
                            "@variantLength": "1",
                            "@positionVCF": "10413073",
                            "@referenceAlleleVCF": "G",
                            "@alternateAlleleVCF": "A",
                        },
                        {
                            "@Assembly": "GRCh37",
                            "@AssemblyAccessionVersion": "GCF_000001405.25",
                            "@AssemblyStatus": "previous",
                            "@Chr": "20",
                            "@Accession": "NC_000020.10",
                            "@start": "10393721",
                            "@stop": "10393721",
                            "@display_start": "10393721",
                            "@display_stop": "10393721",
                            "@variantLength": "1",
                            "@positionVCF": "10393721",
                            "@referenceAlleleVCF": "G",
                            "@alternateAlleleVCF": "A",
                        },
                    ],
                    "MeasureRelationship": {
                        "@Type": "within single gene",
                        "Name": {
                            "ElementValue": {
                                "@Type": "Preferred",
                                "#text": "MKKS centrosomal shuttling protein",
                            }
                        },
                        "Symbol": {"ElementValue": {"@Type": "Preferred", "#text": "MKKS"}},
                        "SequenceLocation": [
                            {
                                "@Assembly": "GRCh38",
                                "@AssemblyAccessionVersion": "GCF_000001405.38",
                                "@AssemblyStatus": "current",
                                "@Chr": "20",
                                "@Accession": "NC_000020.11",
                                "@start": "10401009",
                                "@stop": "10434222",
                                "@display_start": "10401009",
                                "@display_stop": "10434222",
                                "@Strand": "-",
                            },
                            {
                                "@Assembly": "GRCh37",
                                "@AssemblyAccessionVersion": "GCF_000001405.25",
                                "@AssemblyStatus": "previous",
                                "@Chr": "20",
                                "@Accession": "NC_000020.10",
                                "@start": "10385427",
                                "@stop": "10414886",
                                "@display_start": "10385427",
                                "@display_stop": "10414886",
                                "@variantLength": "29460",
                                "@Strand": "-",
                            },
                        ],
                        "XRef": [
                            {"@ID": "8195", "@DB": "Gene"},
                            {"@Type": "MIM", "@ID": "604896", "@DB": "OMIM"},
                            {"@ID": "HGNC:7108", "@DB": "HGNC"},
                        ],
                    },
                    "XRef": [
                        {"@Type": "Allelic variant", "@ID": "604896.0012", "@DB": "OMIM"},
                        {"@Type": "rs", "@ID": "137853154", "@DB": "dbSNP"},
                    ],
                },
                "Name": {
                    "ElementValue": {
                        "@Type": "Preferred",
                        "#text": "NM_170784.3(MKKS):c.442C>T (p.Gln148Ter)",
                    }
                },
                "XRef": {"@ID": "CA117400", "@DB": "ClinGen"},
            },
            "TraitSet": {
                "@Type": "Disease",
                "@ID": "19803",
                "Trait": {
                    "@ID": "32093",
                    "@Type": "Disease",
                    "Name": {
                        "ElementValue": {
                            "@Type": "Preferred",
                            "#text": "Bardet-biedl syndrome 2/6, digenic",
                        }
                    },
                    "XRef": {"@ID": "C4016908", "@DB": "MedGen"},
                },
            },
        }
    ],
)
def test_reference_clinvar_assertion_from_json_data(value, snapshot):
    obj = models.ReferenceClinVarAssertion.from_json_data(value)
    value = conversion.remove_empties_from_containers(cattrs.unstructure(obj))
    snapshot.assert_match(json.dumps(value, indent=2, default=conversion.json_default), "output")


@pytest.mark.parametrize(
    "value,expected",
    [
        (
            {
                "@localKey": "604896.0012_BARDET-BIEDL SYNDROME 2/6, DIGENIC",
                "@submitter": "OMIM",
                "@submitterDate": "2017-12-13",
                "@title": "MKKS, GLN147TER_BARDET-BIEDL SYNDROME 2/6, DIGENIC",
            },
            {
                "local_key": "604896.0012_BARDET-BIEDL SYNDROME 2/6, DIGENIC",
                "submitter": "OMIM",
                "submitter_date": datetime.date(2017, 12, 13),
                "title": "MKKS, GLN147TER_BARDET-BIEDL SYNDROME 2/6, DIGENIC",
            },
        ),
    ],
)
def test_clinvar_submission_id_from_json_data(value, expected):
    obj = models.ClinVarSubmissionId.from_json_data(value)
    value = conversion.remove_empties_from_containers(cattrs.unstructure(obj))
    assert value == expected
