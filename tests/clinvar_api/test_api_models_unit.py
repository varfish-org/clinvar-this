"""Test ``clinvar_api.api_models`` with unit tests."""

import datetime

from clinvar_api import api_models, api_msg


def test_created_construction():
    api_models.Created(id="test-id")


def test_created_from_msg():
    api_models.Created.from_msg(api_msg.Created(id="test-id"))


def test_error_construction():
    api_models.Error(message="fake-message")


def test_error_from_msg():
    api_models.Error.from_msg(api_msg.Error(message="fake-message"))


def test_submission_status_file_construction():
    api_models.SubmissionStatusFile(url="http://example.com")


def test_submission_status_file_from_msg():
    api_models.SubmissionStatusFile.from_msg(api_msg.SubmissionStatusFile(url="http://example.com"))


def test_submission_status_object_content_construction():
    api_models.SubmissionStatusObjectContent(
        clinvar_processing_status="In processing",
        clinvar_release_status="Not released",
    )


def test_submission_status_object_content_from_msg():
    api_models.SubmissionStatusObjectContent.from_msg(
        api_msg.SubmissionStatusObjectContent(
            clinvarProcessingStatus="In processing",
            clinvarReleaseStatus="Not released",
        )
    )


def test_submission_status_object_construction():
    api_models.SubmissionStatusObject(
        accession="accession",
        content=api_models.SubmissionStatusObjectContent(
            clinvar_processing_status="In processing",
            clinvar_release_status="Not released",
        ),
        target_db="clinvar",
    )
    api_models.SubmissionStatusObject(
        accession=None,
        content=api_models.SubmissionStatusObjectContent(
            clinvar_processing_status="In processing",
            clinvar_release_status="Not released",
        ),
        target_db="clinvar",
    )


def test_submission_status_object_from_msg():
    api_models.SubmissionStatusObject.from_msg(
        api_msg.SubmissionStatusObject(
            accession="accession",
            content=api_msg.SubmissionStatusObjectContent(
                clinvarProcessingStatus="In processing",
                clinvarReleaseStatus="Not released",
            ),
            targetDb="clinvar",
        )
    )


def test_submission_status_response_message_construction():
    api_models.SubmissionStatusResponseMessage(
        error_code="error-code", severity="fake-severity", text="fake text"
    )
    api_models.SubmissionStatusResponseMessage(
        error_code=None, severity="fake-severity", text="fake text"
    )


def test_submission_status_response_message_from_msg():
    api_models.SubmissionStatusResponseMessage.from_msg(
        api_msg.SubmissionStatusResponseMessage(
            errorCode="error-code", severity="fake-severity", text="fake text"
        )
    )


def test_submission_status_response_construction():
    api_models.SubmissionStatusResponse(
        status=None,
        files=[api_models.SubmissionStatusFile(url="http://example.com")],
        message=api_models.SubmissionStatusResponseMessage(
            error_code="error-code", severity="fake-severity", text="fake text"
        ),
        objects=[
            api_models.SubmissionStatusObject(
                accession=None,
                content=api_models.SubmissionStatusObjectContent(
                    clinvar_processing_status="In processing",
                    clinvar_release_status="Not released",
                ),
                target_db="clinvar",
            )
        ],
    )
    api_models.SubmissionStatusResponse(
        status="fake-status",
        files=[api_models.SubmissionStatusFile(url="http://example.com")],
        message=api_models.SubmissionStatusResponseMessage(
            error_code="error-code", severity="fake-severity", text="fake text"
        ),
        objects=[
            api_models.SubmissionStatusObject(
                accession=None,
                content=api_models.SubmissionStatusObjectContent(
                    clinvar_processing_status="In processing",
                    clinvar_release_status="Not released",
                ),
                target_db="clinvar",
            )
        ],
    )


def test_submission_status_response_from_msg():
    api_models.SubmissionStatusResponse.from_msg(
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
    )


def test_submission_status_actions_construction():
    api_models.SubmissionStatusActions(
        id="fake-id",
        responses=[
            api_models.SubmissionStatusResponse(
                status=None,
                files=[api_models.SubmissionStatusFile(url="http://example.com")],
                message=api_models.SubmissionStatusResponseMessage(
                    error_code="error-code", severity="fake-severity", text="fake text"
                ),
                objects=[
                    api_models.SubmissionStatusObject(
                        accession=None,
                        content=api_models.SubmissionStatusObjectContent(
                            clinvar_processing_status="In processing",
                            clinvar_release_status="Not released",
                        ),
                        target_db="clinvar",
                    )
                ],
            )
        ],
        status="the-status",
        target_db="clinvar",
        updated=datetime.datetime.now(),
    )
    api_models.SubmissionStatusActions(
        id="fake-id",
        responses=[],
        status="the-status",
        target_db="clinvar",
        updated=datetime.datetime.now(),
    )


def test_submission_status_actions_from_msg():
    api_models.SubmissionStatusActions.from_msg(
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
    )


def test_submission_status_construction():
    api_models.SubmissionStatus(actions=[])
    api_models.SubmissionStatus(
        actions=[
            api_models.SubmissionStatusActions(
                id="fake-id",
                responses=[],
                status="the-status",
                target_db="clinvar",
                updated=datetime.datetime.now(),
            )
        ]
    )


def test_submission_status_from_msg():
    api_models.SubmissionStatus.from_msg(
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
    )


def test_summary_response_error_input_construction():
    api_models.SummaryResponseErrorInput(value="value", field="field")
    api_models.SummaryResponseErrorInput(value="value", field=None)


def test_summary_response_error_input_from_msg():
    api_models.SummaryResponseErrorInput.from_msg(
        api_msg.SummaryResponseErrorInput(value="value", field="field")
    )


def test_summary_response_error_output_error_construction():
    api_models.SummaryResponseErrorOutputError(user_message="the message")


def test_summary_response_error_output_error_from_msg():
    api_models.SummaryResponseErrorOutputError.from_msg(
        api_msg.SummaryResponseErrorOutputError(userMessage="the message")
    )


def test_summary_response_error_output_construction():
    api_models.SummaryResponseErrorOutput(
        errors=[api_models.SummaryResponseErrorOutputError(user_message="the message")]
    )
    api_models.SummaryResponseErrorOutput(errors=[])


def test_summary_response_error_output_from_msg():
    api_models.SummaryResponseErrorOutput.from_msg(
        api_msg.SummaryResponseErrorOutput(
            errors=[api_msg.SummaryResponseErrorOutputError(userMessage="the message")]
        )
    )


def test_summary_response_error_construction():
    api_models.SummaryResponseError(
        input=[api_models.SummaryResponseErrorInput(value="value", field="field")],
        output=api_models.SummaryResponseErrorOutput(errors=[]),
    )
    api_models.SummaryResponseError(
        input=[], output=api_models.SummaryResponseErrorOutput(errors=[])
    )


def test_summary_response_error_from_msg():
    api_models.SummaryResponseError.from_msg(
        api_msg.SummaryResponseError(
            input=[api_msg.SummaryResponseErrorInput(value="value", field="field")],
            output=api_msg.SummaryResponseErrorOutput(errors=[]),
        )
    )


def test_summary_response_deletion_identifier_construction():
    api_models.SummaryResponseDeletionIdentifier(
        clinvar_accession="the-accession",
        clinvar_local_key="the-local-key",
    )
    api_models.SummaryResponseDeletionIdentifier(
        clinvar_accession="the-accession",
        clinvar_local_key=None,
    )


def test_summary_response_deletion_identifier_from_msg():
    api_models.SummaryResponseDeletionIdentifier.from_msg(
        api_msg.SummaryResponseDeletionIdentifier(
            clinvarAccession="the-accession",
            clinvarLocalKey="the-local-key",
        )
    )


def test_summary_response_deletion_construction():
    api_models.SummaryResponseDeletion(
        identifiers=api_models.SummaryResponseDeletionIdentifier(
            clinvar_accession="the-accession",
        ),
        processing_status="processing-status",
        delete_date="2022-01-01",
        delete_status="delete-status",
        errors=[
            api_models.SummaryResponseError(
                input=[], output=api_models.SummaryResponseErrorOutput(errors=[])
            )
        ],
    )
    api_models.SummaryResponseDeletion(
        identifiers=api_models.SummaryResponseDeletionIdentifier(
            clinvar_accession="the-accession",
        ),
        processing_status="processing-status",
        delete_date=None,
        delete_status=None,
        errors=None,
    )


def test_summary_response_deletion_from_msg():
    api_models.SummaryResponseDeletion.from_msg(
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
    )


def test_summary_response_submission_identifier_construction():
    api_models.SummaryResponseSubmissionIdentifiers(
        clinvar_local_key="local-key",
        clinvar_accession="the-accession",
        local_id="local-id",
        local_key="local-key",
    )
    api_models.SummaryResponseSubmissionIdentifiers(
        clinvar_local_key="local-key",
        clinvar_accession=None,
        local_id=None,
        local_key=None,
    )


def test_summary_response_submission_identifier_from_msg():
    api_models.SummaryResponseSubmissionIdentifiers.from_msg(
        api_msg.SummaryResponseSubmissionIdentifiers(
            clinvarLocalKey="local-key",
            clinvarAccession="the-accession",
            localID="local-id",
            localKey="local-key",
        )
    )


def test_summary_response_submission_construction():
    api_models.SummaryResponseSubmission(
        identifiers=api_models.SummaryResponseSubmissionIdentifiers(clinvar_local_key="local-key"),
        processing_status="processing-status",
        clinvar_accession_version="accession-version",
        errors=[
            api_models.SummaryResponseError(
                input=[], output=api_models.SummaryResponseErrorOutput(errors=[])
            )
        ],
        release_date="2022-01-01",
        release_status="released",
    )
    api_models.SummaryResponseSubmission(
        identifiers=api_models.SummaryResponseSubmissionIdentifiers(clinvar_local_key="local-key"),
        processing_status="processing-status",
        clinvar_accession_version=None,
        errors=None,
        release_date=None,
        release_status=None,
    )


def test_summary_response_submission_from_msg():
    api_models.SummaryResponseSubmission.from_msg(
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
    )


def test_summary_response_construction():
    api_models.SummaryResponse(
        batch_processing_status="status",
        batch_release_status="released",
        submission_date="2022-01-01",
        submission_name="submission-name",
        total_count=10,
        total_errors=10,
        total_public=10,
        total_success=10,
        deletions=[
            api_models.SummaryResponseDeletion(
                identifiers=api_models.SummaryResponseDeletionIdentifier(
                    clinvar_accession="the-accession",
                ),
                processing_status="processing-status",
            )
        ],
        submissions=[
            api_models.SummaryResponseSubmission(
                identifiers=api_models.SummaryResponseSubmissionIdentifiers(
                    clinvar_local_key="local-key"
                ),
                processing_status="processing-status",
            )
        ],
        total_delete_count=10,
        total_deleted=10,
        total_delete_errors=10,
        total_delete_success=10,
    )
    api_models.SummaryResponse(
        batch_processing_status="status",
        batch_release_status="released",
        submission_date="2022-01-01",
        submission_name="submission-name",
        total_count=10,
        total_errors=10,
        total_public=10,
        total_success=10,
        deletions=None,
        submissions=None,
        total_delete_count=None,
        total_deleted=None,
        total_delete_errors=None,
        total_delete_success=None,
    )


def test_summary_response_from_msg():
    api_models.SummaryResponse.from_msg(
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
    )


def test_sumbmission_clinvar_deletetion_accession_set_construction():
    api_models.SubmissionClinvarDeletionAccessionSet(
        accession="accession",
        reason="whatever",
    )
    api_models.SubmissionClinvarDeletionAccessionSet(
        accession="accession",
        reason=None,
    )


def test_sumbmission_clinvar_deletetion_accession_set_from_msg():
    api_models.SubmissionClinvarDeletionAccessionSet.from_msg(
        api_msg.SubmissionClinvarDeletionAccessionSet(
            accession="accession",
            reason="whatever",
        )
    )


def test_submission_clinvar_deletion_construction():
    api_models.SubmissionClinvarDeletion(
        accession_set=[
            api_models.SubmissionClinvarDeletionAccessionSet(
                accession="accession",
                reason="whatever",
            )
        ]
    )
    api_models.SubmissionClinvarDeletion(accession_set=[])


def test_submission_clinvar_deletion_from_msg():
    api_models.SubmissionClinvarDeletion.from_msg(
        api_msg.SubmissionClinvarDeletion(
            accessionSet=[
                api_msg.SubmissionClinvarDeletionAccessionSet(
                    accession="accession",
                    reason="whatever",
                )
            ]
        )
    )


def test_submission_chromosome_coordinates_construction():
    api_models.SubmissionChromosomeCoordinates(
        accession="accession",
        alternate_allele="A",
        assembly=api_models.Assembly.GRCH37,
        chromosome=api_models.Chromosome.CHR12,
        inner_start=100,
        inner_stop=200,
        outer_start=90,
        outer_stop=210,
        reference_allele="C",
        start=100,
        stop=200,
        variant_length=10,
    )
    api_models.SubmissionChromosomeCoordinates(
        assembly=api_models.Assembly.GRCH37,
        chromosome=api_models.Chromosome.CHR12,
        start=100,
        stop=100,
        reference_allele="C",
        alternate_allele="A",
        variant_length=1,
    )


def test_submission_chromosome_coordinates_from_msg():
    api_models.SubmissionChromosomeCoordinates.from_msg(
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
    )


def test_submission_variant_gene_construction():
    api_models.SubmissionVariantGene(
        id="some-id",
        symbol="some-symbol",
    )
    api_models.SubmissionVariantGene()


def test_submission_variant_gene_from_msg():
    api_models.SubmissionVariantGene.from_msg(
        api_msg.SubmissionVariantGene(
            id="some-id",
            symbol="some-symbol",
        )
    )


def test_submission_variant_construction():
    api_models.SubmissionVariant(
        chromosome_coordinates=api_models.SubmissionChromosomeCoordinates(
            assembly=api_models.Assembly.GRCH37,
            chromosome=api_models.Chromosome.CHR12,
            start=100,
            stop=100,
            reference_allele="C",
            alternate_allele="A",
            variant_length=1,
        ),
        copy_number="2",
        gene=[api_models.SubmissionVariantGene()],
        hgvs="hgvs-string",
        reference_copy_number="2",
        variant_type=api_models.VariantType.DELETION,
    )
    api_models.SubmissionVariant()


def test_submission_variant_from_msg():
    api_models.SubmissionVariant.from_msg(
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
    )


def test_sumbmission_variant_set_construction():
    api_models.SubmissionVariantSet(variant=[api_msg.SubmissionVariant()])
    api_models.SubmissionVariantSet(variant=[])


def test_sumbmission_variant_set_from_msg():
    api_models.SubmissionVariantSet.from_msg(
        api_models.SubmissionVariantSet(variant=[api_msg.SubmissionVariant()])
    )


def test_submission_phase_unknown_set_construction():
    api_models.SubmissionPhaseUnknownSet(
        hgvs="hgvs-string",
        variants=[api_models.SubmissionVariant()],
    )
    api_models.SubmissionPhaseUnknownSet(
        hgvs="hgvs-string",
        variants=[],
    )


def test_submission_phase_unknown_set_from_msg():
    api_models.SubmissionPhaseUnknownSet.from_msg(
        api_msg.SubmissionPhaseUnknownSet(
            hgvs="hgvs-string",
            variants=[api_msg.SubmissionVariant()],
        )
    )


def test_submission_clinical_feature_construction():
    api_models.SubmissionClinicalFeature(
        clinical_features_affected_status="affected-status",
        db="HP",
        id="the-id",
        name="same-name",
    )


def test_submission_clinical_feature_from_msg():
    api_models.SubmissionClinicalFeature.from_msg(
        api_msg.SubmissionClinicalFeature(
            clinicalFeaturesAffectedStatus="affected-status",
            db="HP",
            id="the-id",
            name="same-name",
        )
    )


def test_submission_observed_in_construction():
    api_models.SubmissionObservedIn(
        affected_status="affected",
        allele_origin="germline",
        collection_method="clinical testing",
        clinical_features=[
            api_models.SubmissionClinicalFeature(
                clinical_features_affected_status="affected-status",
                db="HP",
                id="the-id",
                name="same-name",
            )
        ],
        clinical_features_comment="some comment",
        number_of_individuals=1,
        struct_var_method_type="some-type",
    )
    api_models.SubmissionObservedIn(
        affected_status="affected",
        allele_origin="germline",
        collection_method="clinical testing",
    )


def test_submission_observed_in_from_msg():
    api_models.SubmissionObservedIn.from_msg(
        api_msg.SubmissionObservedIn(
            affectedStatus="affected",
            alleleOrigin="germline",
            collectionMethod="clinical testing",
            clinicalFeaturesComment="some comment",
            numberOfIndividuals=1,
            structVarMethodType="some-type",
        )
    )


def test_submission_haplotype_set_construction():
    api_models.SubmissionHaplotypeSet(
        hgvs="the-hgvs",
        variants=[],
        star_allele_name="the-name",
    )
    api_models.SubmissionHaplotypeSet(
        hgvs="the-hgvs",
        variants=[api_msg.SubmissionVariant()],
        star_allele_name="the-name",
    )


def test_submission_haplotype_set_from_msg():
    api_models.SubmissionHaplotypeSet.from_msg(
        api_msg.SubmissionHaplotypeSet(
            hgvs="the-hgvs",
            variants=[],
            starAlleleName="the-name",
        )
    )


def test_submission_distinct_chromosome_set_construction():
    api_models.SubmissionDistinctChromosomesSet(
        hgvs="some-hgvs",
        variants=[
            api_models.SubmissionVariant(),
            api_models.SubmissionVariant(),
        ],
    )


def test_submission_distinct_chromosome_set_from_msg():
    api_models.SubmissionDistinctChromosomesSet.from_msg(
        api_msg.SubmissionDistinctChromosomesSet(
            hgvs="some-hgvs",
            variants=[
                api_msg.SubmissionVariant(),
                api_msg.SubmissionVariant(),
            ],
        )
    )


def test_submission_haplotype_sets_construction():
    api_models.SubmissionHaplotypeSets(
        haplotype_set=api_models.SubmissionHaplotypeSet(
            hgvs="the-hgvs",
            variants=[api_models.SubmissionVariant()],
            star_allele_name="the-name",
        ),
        haplotype_single_variant_set=api_models.SubmissionHaplotypeSet(
            hgvs="the-hgvs",
            variants=[api_models.SubmissionVariant()],
            star_allele_name="the-name",
        ),
    )
    api_models.SubmissionHaplotypeSets()


def test_submission_haplotype_sets_from_msg():
    api_models.SubmissionHaplotypeSets.from_msg(
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
    )


def test_submission_diplotype_set_construction():
    api_models.SubmissionDiplotypeSet(
        haplotype_sets=[api_models.SubmissionHaplotypeSets()],
        hgvs="the-hgvs",
        star_allele_name="star-allele-name",
    )
    api_models.SubmissionDiplotypeSet(
        haplotype_sets=[api_models.SubmissionHaplotypeSets()],
        hgvs="the-hgvs",
        star_allele_name=None,
    )


def test_submission_diplotype_set_from_msg():
    api_models.SubmissionDiplotypeSet.from_msg(
        api_msg.SubmissionDiplotypeSet(
            haplotypeSets=[api_msg.SubmissionHaplotypeSets()],
            hgvs="the-hgvs",
            starAlleleName="star-allele-name",
        )
    )


def test_submission_citation_construction():
    api_models.SubmissionCitation(
        db=api_models.CitationDb.PMC,
        id="PMC123",
        url="https://example.com",
    )
    api_models.SubmissionCitation(
        db=None,
        id=None,
        url=None,
    )


def test_submission_citation_from_msg():
    api_models.SubmissionCitation.from_msg(
        api_msg.SubmissionCitation(
            db=api_msg.CitationDb.PMC,
            id="PMC123",
            url="https://example.com",
        )
    )


def test_submission_assertion_criteria_construction():
    api_models.SubmissionAssertionCriteria(
        citation=api_models.SubmissionCitation(),
        method="some-method",
    )


def test_submission_assertion_criteria_from_msg():
    api_models.SubmissionAssertionCriteria.from_msg(
        api_msg.SubmissionAssertionCriteria(
            citation=api_msg.SubmissionCitation(),
            method="some-method",
        )
    )


def test_submission_condition_construction():
    api_models.SubmissionCondition(
        db=api_models.ConditionDb.HP,
        id="some-id",
        name="some-name",
    )
    api_models.SubmissionCondition(
        db=None,
        id=None,
        name=None,
    )


def test_submission_condition_from_msg():
    api_models.SubmissionCondition.from_msg(
        api_msg.SubmissionCondition(
            db=api_msg.ConditionDb.HP,
            id="some-id",
            name="some-name",
        )
    )


def test_submission_drug_response_construction():
    api_models.SubmissionDrugResponse(
        db=api_models.ConditionDb.HP,
        drug_name="some drug",
        id="some-id",
        condition=[api_models.SubmissionCondition()],
    )
    api_models.SubmissionDrugResponse(
        db=None,
        drug_name=None,
        id=None,
        condition=None,
    )


def test_submission_drug_response_from_msg():
    api_models.SubmissionDrugResponse.from_msg(
        api_msg.SubmissionDrugResponse(
            db=api_msg.ConditionDb.HP,
            drugName="some drug",
            id="some-id",
            condition=[api_msg.SubmissionCondition()],
        )
    )


def test_submission_condition_set_construction():
    api_models.SubmissionConditionSet(
        condition=[api_msg.SubmissionCondition()],
        drug_response=[api_msg.SubmissionDrugResponse()],
    )
    api_models.SubmissionConditionSet(
        condition=None,
        drug_response=None,
    )


def test_submission_condition_set_from_msg():
    api_models.SubmissionConditionSet.from_msg(
        api_msg.SubmissionConditionSet(
            condition=[api_msg.SubmissionCondition()],
            drugResponse=[api_msg.SubmissionDrugResponse()],
        )
    )


def test_submission_compound_heterozygote_set_variant_set_construction():
    api_models.SubmissionCompoundHeterozygoteSetVariantSet(
        variant_set=api_models.SubmissionVariantSet(variant=[]),
    )
    api_models.SubmissionCompoundHeterozygoteSetVariantSet(
        variant_set=None,
    )


def test_submission_compound_heterozygote_set_variant_set_from_msg():
    api_models.SubmissionCompoundHeterozygoteSetVariantSet(
        api_msg.SubmissionCompoundHeterozygoteSetVariantSet(
            variantSet=api_msg.SubmissionVariantSet(variant=[]),
        )
    )


def test_submission_compound_heterozygote_set_construction():
    api_models.SubmissionCompoundHeterozygoteSet(
        hgvs="hgvs",
        variant_sets=[
            api_models.SubmissionCompoundHeterozygoteSetVariantSet(),
            api_models.SubmissionCompoundHeterozygoteSetVariantSet(),
        ],
    )


def test_submission_compound_heterozygote_set_from_msg():
    api_models.SubmissionCompoundHeterozygoteSet.from_msg(
        api_msg.SubmissionCompoundHeterozygoteSet(
            hgvs="hgvs",
            variantSets=[
                api_msg.SubmissionCompoundHeterozygoteSetVariantSet(),
                api_msg.SubmissionCompoundHeterozygoteSetVariantSet(),
            ],
        )
    )


def test_submission_clinical_significance_construction():
    api_models.SubmissionClinicalSignificance(
        clinical_significance_description=api_models.ClinicalSignificanceDescription.PATHOGENIC,
        citation=[
            api_models.SubmissionCitation(
                db=api_models.CitationDb.PMC,
                id="PMC123",
                url="https://example.com",
            )
        ],
        comment="some comment",
        custom_assertion_score=42.0,
        date_last_evaluated="2022-01-01",
        explanation_of_drug_response="some explanation",
        explanation_of_other_clinical_significance="2022-01-01",
        mode_of_inheritance=api_models.ModeOfInheritance.AUTOSOMAL_DOMINANT_INHERITANCE,
    )
    api_models.SubmissionClinicalSignificance(
        clinical_significance_description=api_models.ClinicalSignificanceDescription.PATHOGENIC,
    )


def test_submission_clinical_significance_from_msg():
    api_models.SubmissionClinicalSignificance.from_msg(
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
    )


def test_submission_clinvar_submission_construction():
    api_models.SubmissionClinvarSubmission(
        clinical_significance=api_models.SubmissionClinicalSignificance(
            clinical_significance_description=api_models.ClinicalSignificanceDescription.PATHOGENIC,
        ),
        condition_set=api_models.SubmissionConditionSet(),
        observed_in=[
            api_models.SubmissionObservedIn(
                affected_status="affected",
                allele_origin="germline",
                collection_method="clinical testing",
            )
        ],
        record_status="record-status",
        release_status="release-status",
        assertion_criteria=api_models.SubmissionAssertionCriteria(
            citation=api_models.SubmissionCitation(),
            method="some-method",
        ),
        clinvar_accession="some-accession",
        compound_heterozygote_set=api_models.SubmissionCompoundHeterozygoteSet(
            hgvs="hgvs",
            variant_sets=[
                api_models.SubmissionCompoundHeterozygoteSetVariantSet(),
                api_models.SubmissionCompoundHeterozygoteSetVariantSet(),
            ],
        ),
        diplotype_set=api_models.SubmissionDiplotypeSet(
            haplotype_sets=[api_models.SubmissionHaplotypeSets()],
            hgvs="the-hgvs",
        ),
        distinct_chromosomes_set=api_models.SubmissionDistinctChromosomesSet(
            hgvs="some-hgvs",
            variants=[
                api_models.SubmissionVariant(),
                api_models.SubmissionVariant(),
            ],
        ),
        haplotype_set=api_models.SubmissionHaplotypeSet(
            hgvs="the-hgvs",
            variants=[],
            star_allele_name="the-name",
        ),
        haplotype_single_variant_set=api_models.SubmissionHaplotypeSet(
            hgvs="the-hgvs",
            variants=[api_models.SubmissionVariant()],
            star_allele_name="the-name",
        ),
        local_id="local-id",
        local_key="local-key",
        phase_unknown_set=api_models.SubmissionPhaseUnknownSet(
            hgvs="hgvs-string",
            variants=[],
        ),
        variant_set=api_models.SubmissionVariantSet(variant=[]),
    )
    api_models.SubmissionClinvarSubmission(
        clinical_significance=api_models.SubmissionClinicalSignificance(
            clinical_significance_description=api_models.ClinicalSignificanceDescription.PATHOGENIC,
        ),
        condition_set=api_models.SubmissionConditionSet(),
        observed_in=[
            api_models.SubmissionObservedIn(
                affected_status="affected",
                allele_origin="germline",
                collection_method="clinical testing",
            )
        ],
        record_status="record-status",
        release_status="release-status",
    )


def test_submission_clinvar_submission_from_msg():
    api_models.SubmissionClinvarSubmission.from_msg(
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
    )


def test_submission_container_construction():
    api_models.SubmissionContainer(
        behalf_org_id=123,
        clinvar_deletion=api_models.SubmissionClinvarDeletion(
            accession_set=[
                api_models.SubmissionClinvarDeletionAccessionSet(
                    accession="accession",
                    reason="whatever",
                )
            ]
        ),
        clinvar_submission=None,
        submission_name="some-name",
    )
    api_models.SubmissionContainer(
        behalf_org_id=123,
        clinvar_deletion=None,
        clinvar_submission=[
            api_models.SubmissionClinvarSubmission(
                clinical_significance=api_models.SubmissionClinicalSignificance(
                    clinical_significance_description=api_models.ClinicalSignificanceDescription.PATHOGENIC,
                ),
                condition_set=api_models.SubmissionConditionSet(),
                observed_in=[
                    api_models.SubmissionObservedIn(
                        affected_status="affected",
                        allele_origin="germline",
                        collection_method="clinical testing",
                    )
                ],
                record_status="record-status",
                release_status="release-status",
            )
        ],
        submission_name="some-name",
    )


def test_submission_container_from_msg():
    api_models.SubmissionContainer.from_msg(
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
    )
    api_models.SubmissionContainer.from_msg(
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
    )
