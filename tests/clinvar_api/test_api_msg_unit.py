"""Test ``clinvar_api.api_msg`` with unit tests."""

import datetime

from clinvar_api import api_msg


def test_created_construction():
    api_msg.Created(id="test-id")


def test_error_construction():
    api_msg.Error(message="fake-message")


def test_submission_status_file_construction():
    api_msg.SubmissionStatusFile(url="http://example.com")


def test_submission_status_object_content_construction():
    api_msg.SubmissionStatusObjectContent(
        clinvarProcessingStatus="In processing",
        clinvarReleaseStatus="Not released",
    )


def test_submission_status_object_construction():
    api_msg.SubmissionStatusObject(
        accession="accession",
        content=api_msg.SubmissionStatusObjectContent(
            clinvarProcessingStatus="In processing",
            clinvarReleaseStatus="Not released",
        ),
        targetDb="clinvar",
    )
    api_msg.SubmissionStatusObject(
        accession=None,
        content=api_msg.SubmissionStatusObjectContent(
            clinvarProcessingStatus="In processing",
            clinvarReleaseStatus="Not released",
        ),
        targetDb="clinvar",
    )


def test_submission_status_response_message_construction():
    api_msg.SubmissionStatusResponseMessage(
        errorCode="error-code", severity="fake-severity", text="fake text"
    )
    api_msg.SubmissionStatusResponseMessage(
        errorCode=None, severity="fake-severity", text="fake text"
    )


def test_submission_status_response_construction():
    api_msg.SubmissionStatusResponse(
        status=None,
        files=[api_msg.SubmissionStatusFile(url="http://example.com")],
        message=api_msg.SubmissionStatusResponseMessage(
            errorCode="error-code", severity="fake-severity", text="fake text"
        ),
        objects=[
            api_msg.SubmissionStatusObject(
                accession=None,
                content=api_msg.SubmissionStatusObjectContent(
                    clinvarProcessingStatus="In processing",
                    clinvarReleaseStatus="Not released",
                ),
                targetDb="clinvar",
            )
        ],
    )
    api_msg.SubmissionStatusResponse(
        status="fake-status",
        files=[api_msg.SubmissionStatusFile(url="http://example.com")],
        message=api_msg.SubmissionStatusResponseMessage(
            errorCode="error-code", severity="fake-severity", text="fake text"
        ),
        objects=[
            api_msg.SubmissionStatusObject(
                accession=None,
                content=api_msg.SubmissionStatusObjectContent(
                    clinvarProcessingStatus="In processing",
                    clinvarReleaseStatus="Not released",
                ),
                targetDb="clinvar",
            )
        ],
    )


def test_submission_status_actions_construction():
    api_msg.SubmissionStatusActions(
        id="fake-id",
        responses=[
            api_msg.SubmissionStatusResponse(
                status=None,
                files=[api_msg.SubmissionStatusFile(url="http://example.com")],
                message=api_msg.SubmissionStatusResponseMessage(
                    errorCode="error-code", severity="fake-severity", text="fake text"
                ),
                objects=[
                    api_msg.SubmissionStatusObject(
                        accession=None,
                        content=api_msg.SubmissionStatusObjectContent(
                            clinvarProcessingStatus="In processing",
                            clinvarReleaseStatus="Not released",
                        ),
                        targetDb="clinvar",
                    )
                ],
            )
        ],
        status="the-status",
        targetDb="clinvar",
        updated=datetime.datetime.now(),
    )
    api_msg.SubmissionStatusActions(
        id="fake-id",
        responses=[],
        status="the-status",
        targetDb="clinvar",
        updated=datetime.datetime.now(),
    )


def test_submission_status_construction():
    api_msg.SubmissionStatus(actions=[])
    api_msg.SubmissionStatus(
        actions=[
            api_msg.SubmissionStatusActions(
                id="fake-id",
                responses=[],
                status="the-status",
                targetDb="clinvar",
                updated=datetime.datetime.now(),
            )
        ]
    )


def test_summary_response_error_input_construction():
    api_msg.SummaryResponseErrorInput(value="value", field="field")
    api_msg.SummaryResponseErrorInput(value="value", field=None)


def test_summary_response_error_output_error_construction():
    api_msg.SummaryResponseErrorOutputError(userMessage="the message")


def test_summary_response_error_output_construction():
    api_msg.SummaryResponseErrorOutput(
        errors=[api_msg.SummaryResponseErrorOutputError(userMessage="the message")]
    )
    api_msg.SummaryResponseErrorOutput(errors=[])


def test_summary_response_error_construction():
    api_msg.SummaryResponseError(
        input=[api_msg.SummaryResponseErrorInput(value="value", field="field")],
        output=api_msg.SummaryResponseErrorOutput(errors=[]),
    )
    api_msg.SummaryResponseError(input=[], output=api_msg.SummaryResponseErrorOutput(errors=[]))


def test_summary_response_deletion_identifier_construction():
    api_msg.SummaryResponseDeletionIdentifier(
        clinvarAccession="the-accession",
        clinvarLocalKey="the-local-key",
    )
    api_msg.SummaryResponseDeletionIdentifier(
        clinvarAccession="the-accession",
        clinvarLocalKey=None,
    )


def test_summary_response_deletion_construction():
    api_msg.SummaryResponseDeletion(
        identifiers=api_msg.SummaryResponseDeletionIdentifier(
            clinvarAccession="the-accession",
        ),
        processingStatus="processing-status",
        deleteDate="2022-01-01",
        deleteStatus="delete-status",
        errors=[
            api_msg.SummaryResponseError(
                input=[], output=api_msg.SummaryResponseErrorOutput(errors=[])
            )
        ],
    )
    api_msg.SummaryResponseDeletion(
        identifiers=api_msg.SummaryResponseDeletionIdentifier(
            clinvarAccession="the-accession",
        ),
        processingStatus="processing-status",
        deleteDate=None,
        deleteStatus=None,
        errors=None,
    )


def test_summary_response_submission_identifier_construction():
    api_msg.SummaryResponseSubmissionIdentifiers(
        clinvarLocalKey="local-key",
        clinvarAccession="the-accession",
        localID="local-id",
        localKey="local-key",
    )
    api_msg.SummaryResponseSubmissionIdentifiers(
        clinvarLocalKey="local-key",
        clinvarAccession=None,
        localID=None,
        localKey=None,
    )


def test_summary_response_submission_construction():
    api_msg.SummaryResponseSubmission(
        identifiers=api_msg.SummaryResponseSubmissionIdentifiers(clinvarLocalKey="local-key"),
        processingStatus="processing-status",
        clinvarAccessionVersion="accession-version",
        errors=[
            api_msg.SummaryResponseError(
                input=[], output=api_msg.SummaryResponseErrorOutput(errors=[])
            )
        ],
        releaseDate="2022-01-01",
        releaseStatus="released",
    )
    api_msg.SummaryResponseSubmission(
        identifiers=api_msg.SummaryResponseSubmissionIdentifiers(clinvarLocalKey="local-key"),
        processingStatus="processing-status",
        clinvarAccessionVersion=None,
        errors=None,
        releaseDate=None,
        releaseStatus=None,
    )


def test_summary_response_construction():
    api_msg.SummaryResponse(
        batchProcessingStatus="status",
        batchReleaseStatus="released",
        submissionDate="2022-01-01",
        submissionName="submission-name",
        totalCount=10,
        totalErrors=10,
        totalPublic=10,
        totalSuccess=10,
        deletions=[
            api_msg.SummaryResponseDeletion(
                identifiers=api_msg.SummaryResponseDeletionIdentifier(
                    clinvarAccession="the-accession",
                ),
                processingStatus="processing-status",
            )
        ],
        submissions=[
            api_msg.SummaryResponseSubmission(
                identifiers=api_msg.SummaryResponseSubmissionIdentifiers(
                    clinvarLocalKey="local-key"
                ),
                processingStatus="processing-status",
            )
        ],
        totalDeleteCount=10,
        totalDeleted=10,
        totalDeleteErrors=10,
        totalDeleteSuccess=10,
    )
    api_msg.SummaryResponse(
        batchProcessingStatus="status",
        batchReleaseStatus="released",
        submissionDate="2022-01-01",
        submissionName="submission-name",
        totalCount=10,
        totalErrors=10,
        totalPublic=10,
        totalSuccess=10,
        deletions=None,
        submissions=None,
        totalDeleteCount=None,
        totalDeleted=None,
        totalDeleteErrors=None,
        totalDeleteSuccess=None,
    )


def test_sumbmission_clinvar_deletetion_accession_set_construction():
    api_msg.SubmissionClinvarDeletionAccessionSet(
        accession="accession",
        reason="whatever",
    )
    api_msg.SubmissionClinvarDeletionAccessionSet(
        accession="accession",
        reason=None,
    )


def test_submission_clinvar_deletion_construction():
    api_msg.SubmissionClinvarDeletion(
        accessionSet=[
            api_msg.SubmissionClinvarDeletionAccessionSet(
                accession="accession",
                reason="whatever",
            )
        ]
    )
    api_msg.SubmissionClinvarDeletion(accessionSet=[])


def test_submission_chromosome_coordinates_construction():
    api_msg.SubmissionChromosomeCoordinates(
        accession="accession",
        alternateAllele="A",
        assembly=api_msg.Assembly.GRCH37,
        chromosome=api_msg.Chromosome.CHR12,
        innerStart=100,
        innerStop=200,
        outerStart=90,
        outerStop=210,
        referenceAllele="C",
        start=100,
        stop=200,
        variantLength=10,
    )
    api_msg.SubmissionChromosomeCoordinates(
        assembly=api_msg.Assembly.GRCH37,
        chromosome=api_msg.Chromosome.CHR12,
        start=100,
        stop=100,
        referenceAllele="C",
        alternateAllele="A",
        variantLength=1,
    )


def test_submission_variant_gene_construction():
    api_msg.SubmissionVariantGene(
        id="some-id",
        symbol="some-symbol",
    )
    api_msg.SubmissionVariantGene()


def test_submission_variant_construction():
    api_msg.SubmissionVariant(
        chromosomeCoordinates=api_msg.SubmissionChromosomeCoordinates(
            assembly=api_msg.Assembly.GRCH37,
            chromosome=api_msg.Chromosome.CHR12,
            start=100,
            stop=100,
            referenceAllele="C",
            alternateAllele="A",
            variantLength=1,
        ),
        copyNumber="2",
        gene=[api_msg.SubmissionVariantGene()],
        hgvs="hgvs-string",
        referenceCopyNumber="2",
        variantType=api_msg.VariantType.DELETION,
    )
    api_msg.SubmissionVariant()


def test_sumbmission_variant_set_construction():
    api_msg.SubmissionVariantSet(variant=[api_msg.SubmissionVariant()])
    api_msg.SubmissionVariantSet(variant=[])


def test_submission_phase_unknown_set_construction():
    api_msg.SubmissionPhaseUnknownSet(
        hgvs="hgvs-string",
        variants=[api_msg.SubmissionVariant()],
    )
    api_msg.SubmissionPhaseUnknownSet(
        hgvs="hgvs-string",
        variants=[],
    )


def test_submission_clinical_feature_construction():
    api_msg.SubmissionClinicalFeature(
        clinicalFeaturesAffectedStatus="affected-status",
        db="HP",
        id="the-id",
        name="same-name",
    )


def test_submission_observed_in_construction():
    api_msg.SubmissionObservedIn(
        affectedStatus="affected",
        alleleOrigin="germline",
        collectionMethod="clinical testing",
        clinicalFeatures=[
            api_msg.SubmissionClinicalFeature(
                clinicalFeaturesAffectedStatus="affected-status",
                db="HP",
                id="the-id",
                name="same-name",
            )
        ],
        clinicalFeaturesComment="some comment",
        numberOfIndividuals=1,
        structVarMethodType="some-type",
    )
    api_msg.SubmissionObservedIn(
        affectedStatus="affected",
        alleleOrigin="germline",
        collectionMethod="clinical testing",
    )


def test_submission_haplotype_set_construction():
    api_msg.SubmissionHaplotypeSet(
        hgvs="the-hgvs",
        variants=[],
        starAlleleName="the-name",
    )
    api_msg.SubmissionHaplotypeSet(
        hgvs="the-hgvs",
        variants=[api_msg.SubmissionVariant()],
        starAlleleName="the-name",
    )


def test_submission_distinct_chromosome_set_construction():
    api_msg.SubmissionDistinctChromosomesSet(
        hgvs="some-hgvs",
        variants=[
            api_msg.SubmissionVariant(),
            api_msg.SubmissionVariant(),
        ],
    )


def test_submission_haplotype_sets_construction():
    api_msg.SubmissionHaplotypeSets(
        haplotypeSet=api_msg.SubmissionHaplotypeSet(
            hgvs="the-hgvs",
            variants=[api_msg.SubmissionVariant()],
            starAlleleName="the-name",
        ),
        haplotypeSingleVariantSet=api_msg.SubmissionHaplotypeSet(
            hgvs="the-hgvs",
            variants=[api_msg.SubmissionVariant()],
            starAlleleName="the-name",
        ),
    )
    api_msg.SubmissionHaplotypeSets()


def test_submission_diplotype_set_construction():
    api_msg.SubmissionDiplotypeSet(
        haplotypeSets=[api_msg.SubmissionHaplotypeSets()],
        hgvs="the-hgvs",
        starAlleleName="star-allele-name",
    )
    api_msg.SubmissionDiplotypeSet(
        haplotypeSets=[api_msg.SubmissionHaplotypeSets()],
        hgvs="the-hgvs",
        starAlleleName=None,
    )


def test_submission_citation_construction():
    api_msg.SubmissionCitation(
        db=api_msg.CitationDb.PMC,
        id="PMC123",
        url="https://example.com",
    )
    api_msg.SubmissionCitation(
        db=None,
        id=None,
        url=None,
    )


def test_submission_assertion_criteria_construction():
    api_msg.SubmissionAssertionCriteria(
        citation=api_msg.SubmissionCitation(),
        method="some-method",
    )


def test_submission_condition_construction():
    api_msg.SubmissionCondition(
        db=api_msg.ConditionDb.HP,
        id="some-id",
        name="some-name",
    )
    api_msg.SubmissionCondition(
        db=None,
        id=None,
        name=None,
    )


def test_submission_drug_response_construction():
    api_msg.SubmissionDrugResponse(
        db=api_msg.ConditionDb.HP,
        drugName="some drug",
        id="some-id",
        condition=[api_msg.SubmissionCondition()],
    )
    api_msg.SubmissionDrugResponse(
        db=None,
        drugName=None,
        id=None,
        condition=None,
    )


def test_submission_condition_set_construction():
    api_msg.SubmissionConditionSet(
        condition=[api_msg.SubmissionCondition()],
        drugResponse=[api_msg.SubmissionDrugResponse()],
    )
    api_msg.SubmissionConditionSet(
        condition=None,
        drugResponse=None,
    )


def test_submission_compound_heterozygote_set_variant_set_construction():
    api_msg.SubmissionCompoundHeterozygoteSetVariantSet(
        variantSet=api_msg.SubmissionVariantSet(variant=[]),
    )
    api_msg.SubmissionCompoundHeterozygoteSetVariantSet(
        variantSet=None,
    )


def test_submission_compound_heterozygote_set_construction():
    api_msg.SubmissionCompoundHeterozygoteSet(
        hgvs="hgvs",
        variantSets=[
            api_msg.SubmissionCompoundHeterozygoteSetVariantSet(),
            api_msg.SubmissionCompoundHeterozygoteSetVariantSet(),
        ],
    )


def test_submission_clinical_significance_construction():
    api_msg.SubmissionClinicalSignificance(
        clinicalSignificanceDescription=api_msg.ClinicalSignificanceDescription.PATHOGENIC,
        citation=[
            api_msg.SubmissionCitation(
                db=api_msg.CitationDb.PMC,
                id="PMC123",
                url="https://example.com",
            )
        ],
        comment="some comment",
        customAssertionScore=42.0,
        dateLastEvaluated="2022-01-01",
        explanationOfDrugResponse="some explanation",
        explanationOfOtherClinicalSignificance="2022-01-01",
        modeOfInheritance=api_msg.ModeOfInheritance.AUTOSOMAL_DOMINANT_INHERITANCE,
    )
    api_msg.SubmissionClinicalSignificance(
        clinicalSignificanceDescription=api_msg.ClinicalSignificanceDescription.PATHOGENIC,
    )


def test_submission_clinvar_submission_construction():
    api_msg.SubmissionClinvarSubmission(
        clinicalSignificance=api_msg.SubmissionClinicalSignificance(
            clinicalSignificanceDescription=api_msg.ClinicalSignificanceDescription.PATHOGENIC,
        ),
        conditionSet=api_msg.SubmissionConditionSet(),
        observedIn=[
            api_msg.SubmissionObservedIn(
                affectedStatus="affected",
                alleleOrigin="germline",
                collectionMethod="clinical testing",
            )
        ],
        recordStatus="record-status",
        releaseStatus="release-status",
        assertionCriteria=api_msg.SubmissionAssertionCriteria(
            citation=api_msg.SubmissionCitation(),
            method="some-method",
        ),
        clinvarAccession="some-accession",
        compoundHeterozygoteSet=api_msg.SubmissionCompoundHeterozygoteSet(
            hgvs="hgvs",
            variantSets=[
                api_msg.SubmissionCompoundHeterozygoteSetVariantSet(),
                api_msg.SubmissionCompoundHeterozygoteSetVariantSet(),
            ],
        ),
        diplotypeSet=api_msg.SubmissionDiplotypeSet(
            haplotypeSets=[api_msg.SubmissionHaplotypeSets()],
            hgvs="the-hgvs",
        ),
        distinctChromosomesSet=api_msg.SubmissionDistinctChromosomesSet(
            hgvs="some-hgvs",
            variants=[
                api_msg.SubmissionVariant(),
                api_msg.SubmissionVariant(),
            ],
        ),
        haplotypeSet=api_msg.SubmissionHaplotypeSet(
            hgvs="the-hgvs",
            variants=[],
            starAlleleName="the-name",
        ),
        haplotypeSingleVariantSet=api_msg.SubmissionHaplotypeSet(
            hgvs="the-hgvs",
            variants=[api_msg.SubmissionVariant()],
            starAlleleName="the-name",
        ),
        localID="local-id",
        localKey="local-key",
        phaseUnknownSet=api_msg.SubmissionPhaseUnknownSet(
            hgvs="hgvs-string",
            variants=[],
        ),
        variantSet=api_msg.SubmissionVariantSet(variant=[]),
    )
    api_msg.SubmissionClinvarSubmission(
        clinicalSignificance=api_msg.SubmissionClinicalSignificance(
            clinicalSignificanceDescription=api_msg.ClinicalSignificanceDescription.PATHOGENIC,
        ),
        conditionSet=api_msg.SubmissionConditionSet(),
        observedIn=[
            api_msg.SubmissionObservedIn(
                affectedStatus="affected",
                alleleOrigin="germline",
                collectionMethod="clinical testing",
            )
        ],
        recordStatus="record-status",
        releaseStatus="release-status",
    )


def test_submission_container_construction():
    api_msg.SubmissionContainer(
        behalfOrgID=123,
        clinvarDeletion=api_msg.SubmissionClinvarDeletion(
            accessionSet=[
                api_msg.SubmissionClinvarDeletionAccessionSet(
                    accession="accession",
                    reason="whatever",
                )
            ]
        ),
        clinvarSubmission=None,
        submissionName="some-name",
    )
    api_msg.SubmissionContainer(
        behalfOrgID=123,
        clinvarDeletion=None,
        clinvarSubmission=[
            api_msg.SubmissionClinvarSubmission(
                clinicalSignificance=api_msg.SubmissionClinicalSignificance(
                    clinicalSignificanceDescription=api_msg.ClinicalSignificanceDescription.PATHOGENIC,
                ),
                conditionSet=api_msg.SubmissionConditionSet(),
                observedIn=[
                    api_msg.SubmissionObservedIn(
                        affectedStatus="affected",
                        alleleOrigin="germline",
                        collectionMethod="clinical testing",
                    )
                ],
                recordStatus="record-status",
                releaseStatus="release-status",
            )
        ],
        submissionName="some-name",
    )
