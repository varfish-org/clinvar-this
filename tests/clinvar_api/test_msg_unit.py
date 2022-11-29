"""Test ``clinvar_api.msg`` with unit tests."""

import datetime

from clinvar_api import msg


def test_created_construction():
    msg.Created(id="test-id")


def test_error_construction():
    msg.Error(message="fake-message")


def test_submission_status_file_construction():
    msg.SubmissionStatusFile(url="http://example.com")


def test_submission_status_object_content_construction():
    msg.SubmissionStatusObjectContent(
        clinvarProcessingStatus="In processing",
        clinvarReleaseStatus="Not released",
    )


def test_submission_status_object_construction():
    msg.SubmissionStatusObject(
        accession="accession",
        content=msg.SubmissionStatusObjectContent(
            clinvarProcessingStatus="In processing",
            clinvarReleaseStatus="Not released",
        ),
        targetDb="clinvar",
    )
    msg.SubmissionStatusObject(
        accession=None,
        content=msg.SubmissionStatusObjectContent(
            clinvarProcessingStatus="In processing",
            clinvarReleaseStatus="Not released",
        ),
        targetDb="clinvar",
    )


def test_submission_status_response_message_construction():
    msg.SubmissionStatusResponseMessage(
        errorCode="error-code", severity="fake-severity", text="fake text"
    )
    msg.SubmissionStatusResponseMessage(errorCode=None, severity="fake-severity", text="fake text")


def test_submission_status_response_construction():
    msg.SubmissionStatusResponse(
        status=None,
        files=[msg.SubmissionStatusFile(url="http://example.com")],
        message=msg.SubmissionStatusResponseMessage(
            errorCode="error-code", severity="fake-severity", text="fake text"
        ),
        objects=[
            msg.SubmissionStatusObject(
                accession=None,
                content=msg.SubmissionStatusObjectContent(
                    clinvarProcessingStatus="In processing",
                    clinvarReleaseStatus="Not released",
                ),
                targetDb="clinvar",
            )
        ],
    )
    msg.SubmissionStatusResponse(
        status="fake-status",
        files=[msg.SubmissionStatusFile(url="http://example.com")],
        message=msg.SubmissionStatusResponseMessage(
            errorCode="error-code", severity="fake-severity", text="fake text"
        ),
        objects=[
            msg.SubmissionStatusObject(
                accession=None,
                content=msg.SubmissionStatusObjectContent(
                    clinvarProcessingStatus="In processing",
                    clinvarReleaseStatus="Not released",
                ),
                targetDb="clinvar",
            )
        ],
    )


def test_submission_status_actions_construction():
    msg.SubmissionStatusActions(
        id="fake-id",
        responses=[
            msg.SubmissionStatusResponse(
                status=None,
                files=[msg.SubmissionStatusFile(url="http://example.com")],
                message=msg.SubmissionStatusResponseMessage(
                    errorCode="error-code", severity="fake-severity", text="fake text"
                ),
                objects=[
                    msg.SubmissionStatusObject(
                        accession=None,
                        content=msg.SubmissionStatusObjectContent(
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
    msg.SubmissionStatusActions(
        id="fake-id",
        responses=[],
        status="the-status",
        targetDb="clinvar",
        updated=datetime.datetime.now(),
    )


def test_submission_status_construction():
    msg.SubmissionStatus(actions=[])
    msg.SubmissionStatus(
        actions=[
            msg.SubmissionStatusActions(
                id="fake-id",
                responses=[],
                status="the-status",
                targetDb="clinvar",
                updated=datetime.datetime.now(),
            )
        ]
    )


def test_summary_response_error_input_construction():
    msg.SummaryResponseErrorInput(value="value", field="field")
    msg.SummaryResponseErrorInput(value="value", field=None)


def test_summary_response_error_output_error_construction():
    msg.SummaryResponseErrorOutputError(userMessage="the message")


def test_summary_response_error_output_construction():
    msg.SummaryResponseErrorOutput(
        errors=[msg.SummaryResponseErrorOutputError(userMessage="the message")]
    )
    msg.SummaryResponseErrorOutput(errors=[])


def test_summary_response_error_construction():
    msg.SummaryResponseError(
        input=[msg.SummaryResponseErrorInput(value="value", field="field")],
        output=msg.SummaryResponseErrorOutput(errors=[]),
    )
    msg.SummaryResponseError(input=[], output=msg.SummaryResponseErrorOutput(errors=[]))


def test_summary_response_deletion_identifier_construction():
    msg.SummaryResponseDeletionIdentifier(
        clinvarAccession="the-accession",
        clinvarLocalKey="the-local-key",
    )
    msg.SummaryResponseDeletionIdentifier(
        clinvarAccession="the-accession",
        clinvarLocalKey=None,
    )


def test_summary_response_deletion_construction():
    msg.SummaryResponseDeletion(
        identifiers=msg.SummaryResponseDeletionIdentifier(
            clinvarAccession="the-accession",
        ),
        processingStatus="processing-status",
        deleteDate="2022-01-01",
        deleteStatus="delete-status",
        errors=[
            msg.SummaryResponseError(input=[], output=msg.SummaryResponseErrorOutput(errors=[]))
        ],
    )
    msg.SummaryResponseDeletion(
        identifiers=msg.SummaryResponseDeletionIdentifier(
            clinvarAccession="the-accession",
        ),
        processingStatus="processing-status",
        deleteDate=None,
        deleteStatus=None,
        errors=None,
    )


def test_summary_response_submission_identifier_construction():
    msg.SummaryResponseSubmissionIdentifiers(
        clinvarLocalKey="local-key",
        clinvarAccession="the-accession",
        localID="local-id",
        localKey="local-key",
    )
    msg.SummaryResponseSubmissionIdentifiers(
        clinvarLocalKey="local-key",
        clinvarAccession=None,
        localID=None,
        localKey=None,
    )


def test_summary_response_submission_construction():
    msg.SummaryResponseSubmission(
        identifiers=msg.SummaryResponseSubmissionIdentifiers(clinvarLocalKey="local-key"),
        processingStatus="processing-status",
        clinvarAccessionVersion="accession-version",
        errors=[
            msg.SummaryResponseError(input=[], output=msg.SummaryResponseErrorOutput(errors=[]))
        ],
        releaseDate="2022-01-01",
    )
    msg.SummaryResponseSubmission(
        identifiers=msg.SummaryResponseSubmissionIdentifiers(clinvarLocalKey="local-key"),
        processingStatus="processing-status",
        clinvarAccessionVersion=None,
        errors=None,
        releaseDate=None,
    )


def test_summary_response_construction():
    msg.SummaryResponse(
        batchProcessingStatus="status",
        batchReleaseStatus="released",
        submissionDate="2022-01-01",
        submissionName="submission-name",
        totalCount=10,
        totalErrors=10,
        totalPublic=10,
        totalSuccess=10,
        deletions=[
            msg.SummaryResponseDeletion(
                identifiers=msg.SummaryResponseDeletionIdentifier(
                    clinvarAccession="the-accession",
                ),
                processingStatus="processing-status",
            )
        ],
        submissions=[
            msg.SummaryResponseSubmission(
                identifiers=msg.SummaryResponseSubmissionIdentifiers(clinvarLocalKey="local-key"),
                processingStatus="processing-status",
            )
        ],
        totalDeleteCount=10,
        totalDeleted=10,
        totalDeleteErrors=10,
        totalDeleteSuccess=10,
    )
    msg.SummaryResponse(
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
    msg.SubmissionClinvarDeletionAccessionSet(
        accession="accession",
        reason="whatever",
    )
    msg.SubmissionClinvarDeletionAccessionSet(
        accession="accession",
        reason=None,
    )


def test_submission_clinvar_deletion_construction():
    msg.SubmissionClinvarDeletion(
        accessionSet=[
            msg.SubmissionClinvarDeletionAccessionSet(
                accession="accession",
                reason="whatever",
            )
        ]
    )
    msg.SubmissionClinvarDeletion(accessionSet=[])


def test_submission_chromosome_coordinates_construction():
    msg.SubmissionChromosomeCoordinates(
        accession="accession",
        alternateAllele="A",
        assembly=msg.Assembly.GRCH37,
        chromosome=msg.Chromosome.CHR12,
        innerStart=100,
        innerStop=200,
        outerStart=90,
        outerStop=210,
        referenceAllele="C",
        start=100,
        stop=200,
        variantLength=10,
    )
    msg.SubmissionChromosomeCoordinates(
        assembly=msg.Assembly.GRCH37,
        chromosome=msg.Chromosome.CHR12,
        start=100,
        stop=100,
        referenceAllele="C",
        alternateAllele="A",
        variantLength=1,
    )


def test_submission_variant_gene_construction():
    msg.SubmissionVariantGene(
        id="some-id",
        symbol="some-symbol",
    )
    msg.SubmissionVariantGene()


def test_submission_variant_construction():
    msg.SubmissionVariant(
        chromosomeCoordinates=msg.SubmissionChromosomeCoordinates(
            assembly=msg.Assembly.GRCH37,
            chromosome=msg.Chromosome.CHR12,
            start=100,
            stop=100,
            referenceAllele="C",
            alternateAllele="A",
            variantLength=1,
        ),
        copyNumber="2",
        gene=[msg.SubmissionVariantGene()],
        hgvs="hgvs-string",
        referenceCopyNumber="2",
        variantType=msg.VariantType.DELETION,
    )
    msg.SubmissionVariant()


def test_sumbmission_variant_set_construction():
    msg.SubmissionVariantSet(variant=[msg.SubmissionVariant()])
    msg.SubmissionVariantSet(variant=[])


def test_submission_phase_unknown_set_construction():
    msg.SubmissionPhaseUnknownSet(
        hgvs="hgvs-string",
        variants=[msg.SubmissionVariant()],
    )
    msg.SubmissionPhaseUnknownSet(
        hgvs="hgvs-string",
        variants=[],
    )


def test_submission_clinical_feature_construction():
    msg.SubmissionClinicalFeature(
        clinicalFeaturesAffectedStatus="affected-status",
        db="HP",
        id="the-id",
        name="same-name",
    )


def test_submission_observed_in_construction():
    msg.SubmissionObservedIn(
        affectedStatus="affected",
        alleleOrigin="germline",
        collectionMethod="clinical testing",
        clinicalFeatures=[
            msg.SubmissionClinicalFeature(
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
    msg.SubmissionObservedIn(
        affectedStatus="affected",
        alleleOrigin="germline",
        collectionMethod="clinical testing",
    )


def test_submission_haplotype_set_construction():
    msg.SubmissionHaplotypeSet(
        hgvs="the-hgvs",
        variants=[],
        starAlleleName="the-name",
    )
    msg.SubmissionHaplotypeSet(
        hgvs="the-hgvs",
        variants=[msg.SubmissionVariant()],
        starAlleleName="the-name",
    )


def test_submission_distinct_chromosome_set_construction():
    msg.SubmissionDistinctChromosomesSet(
        hgvs="some-hgvs",
        variants=[
            msg.SubmissionVariant(),
            msg.SubmissionVariant(),
        ],
    )


def test_submission_haplotype_sets_construction():
    msg.SubmissionHaplotypeSets(
        haplotypeSet=msg.SubmissionHaplotypeSet(
            hgvs="the-hgvs",
            variants=[msg.SubmissionVariant()],
            starAlleleName="the-name",
        ),
        haplotypeSingleVariantSet=msg.SubmissionHaplotypeSet(
            hgvs="the-hgvs",
            variants=[msg.SubmissionVariant()],
            starAlleleName="the-name",
        ),
    )
    msg.SubmissionHaplotypeSets()


def test_submission_diplotype_set_construction():
    msg.SubmissionDiplotypeSet(
        haplotypeSets=[msg.SubmissionHaplotypeSets()],
        hgvs="the-hgvs",
        starAlleleName="star-allele-name",
    )
    msg.SubmissionDiplotypeSet(
        haplotypeSets=[msg.SubmissionHaplotypeSets()],
        hgvs="the-hgvs",
        starAlleleName=None,
    )


def test_submission_citation_construction():
    msg.SubmissionCitation(
        db=msg.CitationDb.PMC,
        id="PMC123",
        url="https://example.com",
    )
    msg.SubmissionCitation(
        db=None,
        id=None,
        url=None,
    )


def test_submission_assertion_criteria_construction():
    msg.SubmissionAssertionCriteria(
        db=msg.CitationDb.PMC,
        id="PMC123",
        url="https://example.com",
    )


def test_submission_condition_construction():
    msg.SubmissionCondition(
        db=msg.ConditionDb.HP,
        id="some-id",
        name="some-name",
    )
    msg.SubmissionCondition(
        db=None,
        id=None,
        name=None,
    )


def test_submission_drug_response_construction():
    msg.SubmissionDrugResponse(
        db=msg.ConditionDb.HP,
        drugName="some drug",
        id="some-id",
        condition=[msg.SubmissionCondition()],
    )
    msg.SubmissionDrugResponse(
        db=None,
        drugName=None,
        id=None,
        condition=None,
    )


def test_submission_condition_set_construction():
    msg.SubmissionConditionSet(
        condition=[msg.SubmissionCondition()],
        drugResponse=[msg.SubmissionDrugResponse()],
    )
    msg.SubmissionConditionSet(
        condition=None,
        drugResponse=None,
    )


def test_submission_compound_heterozygote_set_variant_set_construction():
    msg.SubmissionCompoundHeterozygoteSetVariantSet(
        variantSet=msg.SubmissionVariantSet(variant=[]),
    )
    msg.SubmissionCompoundHeterozygoteSetVariantSet(
        variantSet=None,
    )


def test_submission_compound_heterozygote_set_construction():
    msg.SubmissionCompoundHeterozygoteSet(
        hgvs="hgvs",
        variantSets=[
            msg.SubmissionCompoundHeterozygoteSetVariantSet(),
            msg.SubmissionCompoundHeterozygoteSetVariantSet(),
        ],
    )


def test_submission_clinical_significance_construction():
    msg.SubmissionClinicalSignificance(
        clinicalSignificanceDescription=msg.ClinicalSignificanceDescription.PATHOGENIC,
        citation=[
            msg.SubmissionCitation(
                db=msg.CitationDb.PMC,
                id="PMC123",
                url="https://example.com",
            )
        ],
        comment="some comment",
        customAssertionScore=42.0,
        dateLastEvaluated="2022-01-01",
        explanationOfDrugResponse="some explanation",
        explanationOfOtherClinicalSignificance="2022-01-01",
        modeOfInheritance=msg.ModeOfInheritance.AUTOSOMAL_DOMINANT_INHERITANCE,
    )
    msg.SubmissionClinicalSignificance(
        clinicalSignificanceDescription=msg.ClinicalSignificanceDescription.PATHOGENIC,
    )


def test_submission_clinvar_submission_construction():
    msg.SubmissionClinvarSubmission(
        clinicalSignificance=msg.SubmissionClinicalSignificance(
            clinicalSignificanceDescription=msg.ClinicalSignificanceDescription.PATHOGENIC,
        ),
        conditionSet=msg.SubmissionConditionSet(),
        observedIn=[
            msg.SubmissionObservedIn(
                affectedStatus="affected",
                alleleOrigin="germline",
                collectionMethod="clinical testing",
            )
        ],
        recordStatus="record-status",
        clinvarAccession="some-accession",
        compoundHeterozygoteSet=msg.SubmissionCompoundHeterozygoteSet(
            hgvs="hgvs",
            variantSets=[
                msg.SubmissionCompoundHeterozygoteSetVariantSet(),
                msg.SubmissionCompoundHeterozygoteSetVariantSet(),
            ],
        ),
        diplotypeSet=msg.SubmissionDiplotypeSet(
            haplotypeSets=[msg.SubmissionHaplotypeSets()],
            hgvs="the-hgvs",
        ),
        distinctChromosomesSet=msg.SubmissionDistinctChromosomesSet(
            hgvs="some-hgvs",
            variants=[
                msg.SubmissionVariant(),
                msg.SubmissionVariant(),
            ],
        ),
        haplotypeSet=msg.SubmissionHaplotypeSet(
            hgvs="the-hgvs",
            variants=[],
            starAlleleName="the-name",
        ),
        haplotypeSingleVariantSet=msg.SubmissionHaplotypeSet(
            hgvs="the-hgvs",
            variants=[msg.SubmissionVariant()],
            starAlleleName="the-name",
        ),
        localID="local-id",
        localKey="local-key",
        phaseUnknownSet=msg.SubmissionPhaseUnknownSet(
            hgvs="hgvs-string",
            variants=[],
        ),
        variantSet=msg.SubmissionVariantSet(variant=[]),
    )
    msg.SubmissionClinvarSubmission(
        clinicalSignificance=msg.SubmissionClinicalSignificance(
            clinicalSignificanceDescription=msg.ClinicalSignificanceDescription.PATHOGENIC,
        ),
        conditionSet=msg.SubmissionConditionSet(),
        observedIn=[
            msg.SubmissionObservedIn(
                affectedStatus="affected",
                alleleOrigin="germline",
                collectionMethod="clinical testing",
            )
        ],
        recordStatus="record-status",
    )


def test_submission_container_construction():
    msg.SubmissionContainer(
        behalfOrgID=123,
        clinvarDeletion=msg.SubmissionClinvarDeletion(
            accessionSet=[
                msg.SubmissionClinvarDeletionAccessionSet(
                    accession="accession",
                    reason="whatever",
                )
            ]
        ),
        clinvarSubmissionReleaseStatus=None,
        submissionName="some-name",
    )
    msg.SubmissionContainer(
        assertionCriteria=msg.SubmissionAssertionCriteria(
            db=msg.CitationDb.PMC,
            id="PMC123",
            url="https://example.com",
        ),
        behalfOrgID=123,
        clinvarDeletion=None,
        clinvarSubmissionReleaseStatus="release-status",
        clinvarSubmission=[
            msg.SubmissionClinvarSubmission(
                clinicalSignificance=msg.SubmissionClinicalSignificance(
                    clinicalSignificanceDescription=msg.ClinicalSignificanceDescription.PATHOGENIC,
                ),
                conditionSet=msg.SubmissionConditionSet(),
                observedIn=[
                    msg.SubmissionObservedIn(
                        affectedStatus="affected",
                        alleleOrigin="germline",
                        collectionMethod="clinical testing",
                    )
                ],
                recordStatus="record-status",
            )
        ],
        submissionName="some-name",
    )
