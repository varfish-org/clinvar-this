import pytest


@pytest.fixture
def data_created():
    return {"id": "SUB999999"}


@pytest.fixture
def data_message():
    return {"message": "No valid API key provided"}


@pytest.fixture
def data_submission_submitted():
    """Example data 'Example with a status of "submitted"'."""
    return {
        "actions": [
            {
                "id": "SUB999999-1",
                "responses": [],
                "status": "submitted",
                "targetDb": "clinvar",
                "updated": "2021-03-19T17:24:24.384085Z",
            }
        ]
    }


@pytest.fixture
def data_submission_processing():
    """Example data 'Example with a status of "processing"'."""
    return {
        "actions": [
            {
                "id": "SUB999999-1",
                "responses": [
                    {
                        "files": [],
                        "message": None,
                        "objects": [
                            {
                                "accession": None,
                                "content": {
                                    "clinvarProcessingStatus": "In processing",
                                    "clinvarReleaseStatus": "Not released",
                                },
                                "targetDb": "clinvar",
                            }
                        ],
                        "status": "processing",
                    }
                ],
                "status": "processing",
                "targetDb": "clinvar",
                "updated": "2021-03-19T12:33:09.243072Z",
            }
        ]
    }


@pytest.fixture
def data_submission_processed():
    """Example data 'Example of a successful submission with a status of "processed"'."""
    return {
        "actions": [
            {
                "id": "SUB999999-1",
                "responses": [
                    {
                        "status": "processed",
                        "message": {
                            "errorCode": None,
                            "severity": "info",
                            "text": (
                                'Your ClinVar submission processing status is "Success". Please find the '
                                "details in the file referenced by actions[0].responses[0].files[0].url."
                            ),
                        },
                        "files": [
                            {
                                "url": (
                                    "https://dsubmit.ncbi.nlm.nih.gov/api/2.0/files/xxxxxxxx"
                                    "/sub999999-summary-report.json/?format=attachment"
                                )
                            }
                        ],
                        "objects": [],
                    }
                ],
                "status": "processed",
                "targetDb": "clinvar",
                "updated": "2021-03-24T04:22:04.101297Z",
            }
        ]
    }


@pytest.fixture
def data_partially_successful_submission():
    """Example data'Example of a partially successful submission and a status of "error"'."""
    return {
        "actions": [
            {
                "id": "SUB999999-1",
                "targetDb": "clinvar",
                "status": "error",
                "updated": "2021-03-25T16:05:03.319474Z",
                "responses": [
                    {
                        "status": "error",
                        "message": {
                            "severity": "error",
                            "errorCode": "1",
                            "text": (
                                'Your ClinVar submission processing status is "Partial success". '
                                "Please find the details in the file referenced by "
                                "actions[0].responses[0].files[0].url.",
                            ),
                        },
                        "files": [
                            {
                                "url": (
                                    "https://dsubmit.ncbi.nlm.nih.gov/api/2.0/files/xxxxxxxx/"
                                    "sub999999-summary-report.json/?format=attachment"
                                )
                            }
                        ],
                        "objects": [],
                    }
                ],
            }
        ]
    }


@pytest.fixture
def data_submission_error():
    """Example data 'Example of a submission with a status of "error" where all records failed:'."""
    return {
        "actions": [
            {
                "id": "SUB999999-1",
                "targetDb": "clinvar",
                "status": "error",
                "updated": "2021-03-25T15:31:04.411550Z",
                "responses": [
                    {
                        "status": "error",
                        "message": {
                            "severity": "error",
                            "errorCode": "2",
                            "text": (
                                'Your ClinVar submission processing status is "Error".  Please find the '
                                "details in the file referenced by actions[0].responses[0].files[0].url."
                            ),
                        },
                        "files": [
                            {
                                "url": (
                                    "https://dsubmit.ncbi.nlm.nih.gov/api/2.0/files/xxxxxxxx/"
                                    "sub999999-summary-report.json/?format=attachment"
                                )
                            }
                        ],
                        "objects": [],
                    }
                ],
            }
        ]
    }


@pytest.fixture
def data_summary_response_processed():
    """Example of a successful submission with a status of processed:

    This response contains a URL for a summary file with more details. Following is an example:
    """
    return {
        "submissionName": "SUB673156",
        "submissionDate": "2021-03-25",
        "batchProcessingStatus": "Success",
        "batchReleaseStatus": "Not released",
        "totalCount": 3,
        "totalErrors": 0,
        "totalSuccess": 3,
        "totalPublic": 0,
        "submissions": [
            {
                "identifiers": {
                    "localID": "adefc5ed-7d59-4119-8b3d-07dcdc504c09_success1",
                    "clinvarLocalKey": "adefc5ed-7d59-4119-8b3d-07dcdc504c09_success1",
                    "localKey": "adefc5ed-7d59-4119-8b3d-07dcdc504c09_success1",
                    "clinvarAccession": "SCV000839746",
                },
                "processingStatus": "Success",
            },
            {
                "identifiers": {
                    "localID": "adefc5ed-7d59-4119-8b3d-07dcdc504c09_success2",
                    "clinvarLocalKey": "adefc5ed-7d59-4119-8b3d-07dcdc504c09_success2",
                    "localKey": "adefc5ed-7d59-4119-8b3d-07dcdc504c09_success2",
                    "clinvarAccession": "SCV000839747",
                },
                "processingStatus": "Success",
            },
            {
                "identifiers": {
                    "localID": "adefc5ed-7d59-4119-8b3d-07dcdc504c09_success3",
                    "clinvarLocalKey": "adefc5ed-7d59-4119-8b3d-07dcdc504c09_success3",
                    "localKey": "adefc5ed-7d59-4119-8b3d-07dcdc504c09_success3",
                    "clinvarAccession": "SCV000839748",
                },
                "processingStatus": "Success",
            },
        ],
    }


@pytest.fixture
def data_summary_response_error_partial():
    """Example of a partially successful submission and a status of error:

    This response contains a URL for a summary file with more details. Following is an example:
    """
    return {
        "submissionName": "PAHVCEP_10_2020_API",
        "submissionDate": "2021-03-25",
        "batchProcessingStatus": "Partial success",
        "batchReleaseStatus": "Not released",
        "totalCount": 6,
        "totalErrors": 5,
        "totalSuccess": 1,
        "totalPublic": 0,
        "submissions": [
            {
                "identifiers": {
                    "localID": "adefc5ed-7d59-4119-8b3d-07dcdc504c09",
                    "localKey": "adefc5ed-7d59-4119-8b3d-07dcdc504c09",
                    "clinvarLocalKey": "adefc5ed-7d59-4119-8b3d-07dcdc504c09",
                },
                "processingStatus": "Error",
                "errors": [
                    {
                        "input": [
                            {"field": "ConditionID.type", "value": "MONDO"},
                            {"field": "ConditionID.value", "value": "MONDO:0009861"},
                        ],
                        "output": {
                            "errors": [
                                {
                                    "userMessage": "The identifier you provided (MONDO:MONDO:0009861) cannot be validated, either because it is invalid or because it is valid but not in our database yet. For the latter case, contact us at clinvar@ncbi.nlm.nih.gov."
                                }
                            ]
                        },
                    }
                ],
            },
            {
                "identifiers": {
                    "localID": "adefc5ed-7d59-4119-8b3d-07dcdc504c09",
                    "localKey": "adefc5ed-7d59-4119-8b3d-07dcdc504c09",
                    "clinvarLocalKey": "adefc5ed-7d59-4119-8b3d-07dcdc504c09",
                },
                "processingStatus": "Error",
                "errors": [
                    {
                        "input": [
                            {"field": "ConditionID.type", "value": "MONDO"},
                            {"field": "ConditionID.value", "value": "MONDO:000"},
                        ],
                        "output": {
                            "errors": [
                                {
                                    "userMessage": "The identifier you provided (MONDO:MONDO:000) cannot be validated, either because it is invalid or because it is valid but not in our database yet. For the latter case, contact us at clinvar@ncbi.nlm.nih.gov."
                                }
                            ]
                        },
                    },
                    {
                        "input": [],
                        "output": {
                            "errors": [
                                {
                                    "userMessage": "Records adefc5ed-7d59-4119-8b3d-07dcdc504c09, adefc5ed-7d59-4119-8b3d-07dcdc504c09 and adefc5ed-7d59-4119-8b3d-07dcdc504c09 report the same variant/condition pair. Please remove all but one of these records. If your intent is to provide data for more than one individuals with the variant, please report them as distinct observations (ObservedIn)."
                                }
                            ]
                        },
                    },
                ],
            },
            {
                "identifiers": {
                    "localID": "adefc5ed-7d59-4119-8b3d-07dcdc504c09",
                    "localKey": "adefc5ed-7d59-4119-8b3d-07dcdc504c09",
                    "clinvarLocalKey": "adefc5ed-7d59-4119-8b3d-07dcdc504c09",
                },
                "processingStatus": "Error",
                "errors": [
                    {
                        "input": [
                            {"field": "ConditionID.type", "value": "MONDO"},
                            {"field": "ConditionID.value", "value": "MONDO:000"},
                        ],
                        "output": {
                            "errors": [
                                {
                                    "userMessage": "The identifier you provided (MONDO:MONDO:000) cannot be validated, either because it is invalid or because it is valid but not in our database yet. For the latter case, contact us at clinvar@ncbi.nlm.nih.gov."
                                }
                            ]
                        },
                    },
                    {
                        "input": [],
                        "output": {
                            "errors": [
                                {
                                    "userMessage": "Records adefc5ed-7d59-4119-8b3d-07dcdc504c09, adefc5ed-7d59-4119-8b3d-07dcdc504c09 and adefc5ed-7d59-4119-8b3d-07dcdc504c09 report the same variant/condition pair. Please remove all but one of these records. If your intent is to provide data for more than one individuals with the variant, please report them as distinct observations (ObservedIn)."
                                }
                            ]
                        },
                    },
                ],
            },
            {
                "identifiers": {
                    "localID": "adefc5ed-7d59-4119-8b3d-07dcdc504c09",
                    "localKey": "adefc5ed-7d59-4119-8b3d-07dcdc504c09",
                    "clinvarLocalKey": "adefc5ed-7d59-4119-8b3d-07dcdc504c09",
                },
                "processingStatus": "Error",
                "errors": [
                    {
                        "input": [
                            {"field": "ConditionID.type", "value": "MONDO"},
                            {"field": "ConditionID.value", "value": "MONDO:000"},
                        ],
                        "output": {
                            "errors": [
                                {
                                    "userMessage": "The identifier you provided (MONDO:MONDO:000) cannot be validated, either because it is invalid or because it is valid but not in our database yet. For the latter case, contact us at clinvar@ncbi.nlm.nih.gov."
                                }
                            ]
                        },
                    },
                    {
                        "input": [],
                        "output": {
                            "errors": [
                                {
                                    "userMessage": "Records adefc5ed-7d59-4119-8b3d-07dcdc504c09, adefc5ed-7d59-4119-8b3d-07dcdc504c09 and adefc5ed-7d59-4119-8b3d-07dcdc504c09 report the same variant/condition pair. Please remove all but one of these records. If your intent is to provide data for more than one individuals with the variant, please report them as distinct observations (ObservedIn)."
                                }
                            ]
                        },
                    },
                ],
            },
            {
                "identifiers": {
                    "localID": "adefc5ed-7d59-4119-8b3d-07dcdc504c09_success1",
                    "clinvarLocalKey": "adefc5ed-7d59-4119-8b3d-07dcdc504c09_success1",
                    "localKey": "adefc5ed-7d59-4119-8b3d-07dcdc504c09_success1",
                    "clinvarAccession": "SCV000839746",
                },
                "processingStatus": "Success",
            },
            {
                "identifiers": {
                    "localID": "adefc5ed-7d59-4119-8b3d-07dcdc504c09_success2",
                    "clinvarLocalKey": "adefc5ed-7d59-4119-8b3d-07dcdc504c09_success2",
                    "localKey": "adefc5ed-7d59-4119-8b3d-07dcdc504c09_success2",
                },
                "processingStatus": "Error",
                "errors": [
                    {
                        "input": [{"value": "adefc5ed-7d59-4119-8b3d-07dcdc504c09_success2"}],
                        "output": {
                            "errors": [
                                {
                                    "userMessage": "You provided multiple rows on the Variant tab with the same LinkingID adefc5ed-7d59-4119-8b3d-07dcdc504c09_success2."
                                }
                            ]
                        },
                    }
                ],
            },
        ],
    }


@pytest.fixture
def data_summary_response_error_all():
    """Example of a submission with a status of error where all records failed:

    This response contains a URL for a summary file with more details. Following is an example:
    """
    return {
        "submissionName": "PAHVCEP_10_2020_API",
        "submissionDate": "2021-03-25",
        "batchProcessingStatus": "Error",
        "batchReleaseStatus": "Not released",
        "totalCount": 3,
        "totalErrors": 3,
        "totalSuccess": 0,
        "totalPublic": 0,
        "submissions": [
            {
                "identifiers": {
                    "localID": "adefc5ed-7d59-4119-8b3d-07dcdc504c09_success1",
                    "clinvarLocalKey": "adefc5ed-7d59-4119-8b3d-07dcdc504c09_success1|MedGen_C0149978",
                },
                "processingStatus": "Error",
                "errors": [
                    {
                        "input": [
                            {
                                "value": "adefc5ed-7d59-4119-8b3d-07dcdc504c09_success1|MedGen_C0149978"
                            }
                        ],
                        "output": {
                            "errors": [
                                {
                                    "userMessage": "This assertion duplicates another assertion with the RecordID adefc5ed-7d59-4119-8b3d-07dcdc504c09_success1, ClinVar accession SCV000839746, and Submitted variant NC_000012.12:g.102852945T>M."
                                }
                            ]
                        },
                    }
                ],
            },
            {
                "identifiers": {
                    "localID": "adefc5ed-7d59-4119-8b3d-07dcdc504c09_success2",
                    "clinvarLocalKey": "adefc5ed-7d59-4119-8b3d-07dcdc504c09_success2|MedGen_C0153436",
                },
                "processingStatus": "Error",
                "errors": [
                    {
                        "input": [
                            {
                                "value": "adefc5ed-7d59-4119-8b3d-07dcdc504c09_success2|MedGen_C0153436"
                            }
                        ],
                        "output": {
                            "errors": [
                                {
                                    "userMessage": "This assertion duplicates another assertion with the RecordID adefc5ed-7d59-4119-8b3d-07dcdc504c09_success2, ClinVar accession SCV000839747, and Submitted variant NC_000012.12:g.102852945T>M."
                                }
                            ]
                        },
                    }
                ],
            },
            {
                "identifiers": {
                    "localID": "adefc5ed-7d59-4119-8b3d-07dcdc504c09_success3",
                    "clinvarLocalKey": "adefc5ed-7d59-4119-8b3d-07dcdc504c09_success3|MedGen_C1134719",
                },
                "processingStatus": "Error",
                "errors": [
                    {
                        "input": [
                            {
                                "value": "adefc5ed-7d59-4119-8b3d-07dcdc504c09_success3|MedGen_C1134719"
                            }
                        ],
                        "output": {
                            "errors": [
                                {
                                    "userMessage": "This assertion duplicates another assertion with the RecordID adefc5ed-7d59-4119-8b3d-07dcdc504c09_success3, ClinVar accession SCV000839748, and Submitted variant NC_000012.12:g.102852945T>M."
                                }
                            ]
                        },
                    }
                ],
            },
        ],
    }


@pytest.fixture
def data_submission_snv():
    return {
        "clinvarSubmissionReleaseStatus": "hold until published",
        "clinvarSubmission": [
            {
                "assertionCriteria": {
                    "citation": {"db": "PubMed", "id": "25741868"},
                    "method": "ACMG",
                },
                "clinicalSignificance": {
                    "citation": [],
                    "clinicalSignificanceDescription": "Likely pathogenic",
                    "comment": "PM1_sup, PP3_mod, PM2_sup, PP4_mod",
                    "dateLastEvaluated": "2022-11-09",
                    "modeOfInheritance": "Autosomal recessive inheritance",
                },
                "conditionSet": {"condition": [{"name": "not provided"}]},
                "observedIn": [
                    {
                        "affectedStatus": "yes",
                        "alleleOrigin": "biparental",
                        "clinicalFeatures": [
                            {
                                "db": "HP",
                                "id": "HP:0003097",
                                "clinicalFeaturesAffectedStatus": "present",
                            },
                            {
                                "db": "HP",
                                "id": "HP:0011427",
                                "clinicalFeaturesAffectedStatus": "present",
                            },
                            {
                                "db": "HP",
                                "id": "HP:0002643",
                                "clinicalFeaturesAffectedStatus": "present",
                            },
                            {
                                "db": "HP",
                                "id": "HP:0002089",
                                "clinicalFeaturesAffectedStatus": "present",
                            },
                            {
                                "db": "HP",
                                "id": "HP:0005180",
                                "clinicalFeaturesAffectedStatus": "present",
                            },
                            {
                                "db": "HP",
                                "id": "HP:0001762",
                                "clinicalFeaturesAffectedStatus": "present",
                            },
                            {
                                "db": "HP",
                                "id": "HP:0001342",
                                "clinicalFeaturesAffectedStatus": "present",
                            },
                            {
                                "db": "HP",
                                "id": "HP:0001250",
                                "clinicalFeaturesAffectedStatus": "present",
                            },
                        ],
                        "numberOfIndividuals": 1,
                        "collectionMethod": "clinical testing",
                    }
                ],
                "recordStatus": "novel",
                "variantSet": {
                    "variant": [
                        {
                            "chromosomeCoordinates": {
                                "assembly": "GRCh37",
                                "chromosome": "9",
                                "start": 116021007,
                                "stop": 116021007,
                                "referenceAllele": "T",
                                "alternateAllele": "C",
                            }
                        }
                    ]
                },
            }
        ],
    }
