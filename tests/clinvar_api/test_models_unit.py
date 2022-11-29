"""Test ``clinvar_api.models`` with unit tests."""

import datetime

from clinvar_api import models, msg


def test_created_construction():
    models.Created(id="test-id")


def test_created_from_msg():
    models.Created.from_msg(msg.Created(id="test-id"))


def test_error_construction():
    models.Error(message="fake-message")


def test_error_from_msg():
    models.Error.from_msg(msg.Error(message="fake-message"))


def test_submission_status_file_construction():
    models.SubmissionStatusFile(url="http://example.com")


def test_submission_status_file_from_msg():
    models.SubmissionStatusFile.from_msg(msg.SubmissionStatusFile(url="http://example.com"))


def test_submission_status_object_content_construction():
    models.SubmissionStatusObjectContent(
        clinvar_processing_status="In processing",
        clinvar_release_status="Not released",
    )


def test_submission_status_object_content_from_msg():
    models.SubmissionStatusObjectContent.from_msg(
        msg.SubmissionStatusObjectContent(
            clinvarProcessingStatus="In processing",
            clinvarReleaseStatus="Not released",
        )
    )


def test_submission_status_object_construction():
    models.SubmissionStatusObject(
        accession="accession",
        content=models.SubmissionStatusObjectContent(
            clinvar_processing_status="In processing",
            clinvar_release_status="Not released",
        ),
        target_db="clinvar",
    )
    models.SubmissionStatusObject(
        accession=None,
        content=models.SubmissionStatusObjectContent(
            clinvar_processing_status="In processing",
            clinvar_release_status="Not released",
        ),
        target_db="clinvar",
    )


def test_submission_status_object_from_msg():
    models.SubmissionStatusObject.from_msg(
        msg.SubmissionStatusObject(
            accession="accession",
            content=msg.SubmissionStatusObjectContent(
                clinvarProcessingStatus="In processing",
                clinvarReleaseStatus="Not released",
            ),
            targetDb="clinvar",
        )
    )


def test_submission_status_response_message_construction():
    models.SubmissionStatusResponseMessage(
        error_code="error-code", severity="fake-severity", text="fake text"
    )
    models.SubmissionStatusResponseMessage(
        error_code=None, severity="fake-severity", text="fake text"
    )


def test_submission_status_response_message_from_msg():
    models.SubmissionStatusResponseMessage.from_msg(
        msg.SubmissionStatusResponseMessage(
            errorCode="error-code", severity="fake-severity", text="fake text"
        )
    )


def test_submission_status_response_construction():
    models.SubmissionStatusResponse(
        status=None,
        files=[models.SubmissionStatusFile(url="http://example.com")],
        message=models.SubmissionStatusResponseMessage(
            error_code="error-code", severity="fake-severity", text="fake text"
        ),
        objects=[
            models.SubmissionStatusObject(
                accession=None,
                content=models.SubmissionStatusObjectContent(
                    clinvar_processing_status="In processing",
                    clinvar_release_status="Not released",
                ),
                target_db="clinvar",
            )
        ],
    )
    models.SubmissionStatusResponse(
        status="fake-status",
        files=[models.SubmissionStatusFile(url="http://example.com")],
        message=models.SubmissionStatusResponseMessage(
            error_code="error-code", severity="fake-severity", text="fake text"
        ),
        objects=[
            models.SubmissionStatusObject(
                accession=None,
                content=models.SubmissionStatusObjectContent(
                    clinvar_processing_status="In processing",
                    clinvar_release_status="Not released",
                ),
                target_db="clinvar",
            )
        ],
    )


def test_submission_status_response_from_msg():
    models.SubmissionStatusResponse.from_msg(
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
    )


def test_submission_status_actions_construction():
    models.SubmissionStatusActions(
        id="fake-id",
        responses=[
            models.SubmissionStatusResponse(
                status=None,
                files=[models.SubmissionStatusFile(url="http://example.com")],
                message=models.SubmissionStatusResponseMessage(
                    error_code="error-code", severity="fake-severity", text="fake text"
                ),
                objects=[
                    models.SubmissionStatusObject(
                        accession=None,
                        content=models.SubmissionStatusObjectContent(
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
    models.SubmissionStatusActions(
        id="fake-id",
        responses=[],
        status="the-status",
        target_db="clinvar",
        updated=datetime.datetime.now(),
    )


def test_submission_status_actions_from_msg():
    models.SubmissionStatusActions.from_msg(
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
    )


def test_submission_status_construction():
    models.SubmissionStatus(actions=[])
    models.SubmissionStatus(
        actions=[
            models.SubmissionStatusActions(
                id="fake-id",
                responses=[],
                status="the-status",
                target_db="clinvar",
                updated=datetime.datetime.now(),
            )
        ]
    )


def test_submission_status_from_msg():
    models.SubmissionStatus.from_msg(
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
    )


def test_summary_response_error_input_construction():
    models.SummaryResponseErrorInput(value="value", field="field")
    models.SummaryResponseErrorInput(value="value", field=None)


def test_summary_response_error_input_from_msg():
    models.SummaryResponseErrorInput.from_msg(
        msg.SummaryResponseErrorInput(value="value", field="field")
    )


def test_summary_response_error_output_error_construction():
    models.SummaryResponseErrorOutputError(user_message="the message")


def test_summary_response_error_output_error_from_msg():
    models.SummaryResponseErrorOutputError.from_msg(
        msg.SummaryResponseErrorOutputError(userMessage="the message")
    )


def test_summary_response_error_output_construction():
    models.SummaryResponseErrorOutput(
        errors=[models.SummaryResponseErrorOutputError(user_message="the message")]
    )
    models.SummaryResponseErrorOutput(errors=[])


def test_summary_response_error_output_from_msg():
    models.SummaryResponseErrorOutput.from_msg(
        msg.SummaryResponseErrorOutput(
            errors=[msg.SummaryResponseErrorOutputError(userMessage="the message")]
        )
    )


def test_summary_response_error_construction():
    models.SummaryResponseError(
        input=[models.SummaryResponseErrorInput(value="value", field="field")],
        output=models.SummaryResponseErrorOutput(errors=[]),
    )
    models.SummaryResponseError(input=[], output=models.SummaryResponseErrorOutput(errors=[]))


def test_summary_response_error_from_msg():
    models.SummaryResponseError.from_msg(
        msg.SummaryResponseError(
            input=[msg.SummaryResponseErrorInput(value="value", field="field")],
            output=msg.SummaryResponseErrorOutput(errors=[]),
        )
    )


def test_summary_response_deletion_identifier_construction():
    models.SummaryResponseDeletionIdentifier(
        clinvar_accession="the-accession",
        clinvar_local_key="the-local-key",
    )
    models.SummaryResponseDeletionIdentifier(
        clinvar_accession="the-accession",
        clinvar_local_key=None,
    )


def test_summary_response_deletion_identifier_from_msg():
    models.SummaryResponseDeletionIdentifier.from_msg(
        msg.SummaryResponseDeletionIdentifier(
            clinvarAccession="the-accession",
            clinvarLocalKey="the-local-key",
        )
    )


def test_summary_response_deletion_construction():
    models.SummaryResponseDeletion(
        identifiers=models.SummaryResponseDeletionIdentifier(
            clinvar_accession="the-accession",
        ),
        processing_status="processing-status",
        delete_date="2022-01-01",
        delete_status="delete-status",
        errors=[
            models.SummaryResponseError(
                input=[], output=models.SummaryResponseErrorOutput(errors=[])
            )
        ],
    )
    models.SummaryResponseDeletion(
        identifiers=models.SummaryResponseDeletionIdentifier(
            clinvar_accession="the-accession",
        ),
        processing_status="processing-status",
        delete_date=None,
        delete_status=None,
        errors=None,
    )


def test_summary_response_deletion_from_msg():
    models.SummaryResponseDeletion.from_msg(
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
    )


def test_summary_response_submission_identifier_construction():
    models.SummaryResponseSubmissionIdentifiers(
        clinvar_local_key="local-key",
        clinvar_accession="the-accession",
        local_id="local-id",
        local_key="local-key",
    )
    models.SummaryResponseSubmissionIdentifiers(
        clinvar_local_key="local-key",
        clinvar_accession=None,
        local_id=None,
        local_key=None,
    )


def test_summary_response_submission_identifier_from_msg():
    models.SummaryResponseSubmissionIdentifiers.from_msg(
        msg.SummaryResponseSubmissionIdentifiers(
            clinvarLocalKey="local-key",
            clinvarAccession="the-accession",
            localID="local-id",
            localKey="local-key",
        )
    )


def test_summary_response_submission_construction():
    models.SummaryResponseSubmission(
        identifiers=models.SummaryResponseSubmissionIdentifiers(clinvar_local_key="local-key"),
        processing_status="processing-status",
        clinvar_accession_version="accession-version",
        errors=[
            models.SummaryResponseError(
                input=[], output=models.SummaryResponseErrorOutput(errors=[])
            )
        ],
        release_date="2022-01-01",
        release_status="released",
    )
    models.SummaryResponseSubmission(
        identifiers=models.SummaryResponseSubmissionIdentifiers(clinvar_local_key="local-key"),
        processing_status="processing-status",
        clinvar_accession_version=None,
        errors=None,
        release_date=None,
        release_status=None,
    )


def test_summary_response_submission_from_msg():
    models.SummaryResponseSubmission.from_msg(
        msg.SummaryResponseSubmission(
            identifiers=msg.SummaryResponseSubmissionIdentifiers(clinvarLocalKey="local-key"),
            processingStatus="processing-status",
            clinvarAccessionVersion="accession-version",
            errors=[
                msg.SummaryResponseError(input=[], output=msg.SummaryResponseErrorOutput(errors=[]))
            ],
            releaseDate="2022-01-01",
            releaseStatus="released",
        )
    )


def test_summary_response_construction():
    models.SummaryResponse(
        batch_processing_status="status",
        batch_release_status="released",
        submission_date="2022-01-01",
        submission_name="submission-name",
        total_count=10,
        total_errors=10,
        total_public=10,
        total_success=10,
        deletions=[
            models.SummaryResponseDeletion(
                identifiers=models.SummaryResponseDeletionIdentifier(
                    clinvar_accession="the-accession",
                ),
                processing_status="processing-status",
            )
        ],
        submissions=[
            models.SummaryResponseSubmission(
                identifiers=models.SummaryResponseSubmissionIdentifiers(
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
    models.SummaryResponse(
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
    models.SummaryResponse.from_msg(
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
                    identifiers=msg.SummaryResponseSubmissionIdentifiers(
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


def test_sumbmission_clinvar_deletion_accession_set_construction():
    models.SubmissionClinvarDeletionAccessionSet(
        accession="accession",
        reason="whatever",
    )
    models.SubmissionClinvarDeletionAccessionSet(
        accession="accession",
        reason=None,
    )


def test_sumbmission_clinvar_deletion_accession_set_to_msg():
    models.SubmissionClinvarDeletionAccessionSet(
        accession="accession",
        reason="whatever",
    ).to_msg()
    models.SubmissionClinvarDeletionAccessionSet(
        accession="accession",
        reason=None,
    ).to_msg()


def test_submission_clinvar_deletion_construction():
    models.SubmissionClinvarDeletion(
        accession_set=[
            models.SubmissionClinvarDeletionAccessionSet(
                accession="accession",
                reason="whatever",
            )
        ]
    )
    models.SubmissionClinvarDeletion(accession_set=[])


def test_submission_clinvar_deletion_to_msg():
    models.SubmissionClinvarDeletion(
        accession_set=[
            models.SubmissionClinvarDeletionAccessionSet(
                accession="accession",
                reason="whatever",
            )
        ]
    ).to_msg()
    models.SubmissionClinvarDeletion(accession_set=[]).to_msg()


def test_submission_chromosome_coordinates_construction():
    models.SubmissionChromosomeCoordinates(
        accession="accession",
        alternate_allele="A",
        assembly=models.Assembly.GRCH37,
        chromosome=models.Chromosome.CHR12,
        inner_start=100,
        inner_stop=200,
        outer_start=90,
        outer_stop=210,
        reference_allele="C",
        start=100,
        stop=200,
        variant_length=10,
    )
    models.SubmissionChromosomeCoordinates(
        assembly=models.Assembly.GRCH37,
        chromosome=models.Chromosome.CHR12,
        start=100,
        stop=100,
        reference_allele="C",
        alternate_allele="A",
        variant_length=1,
    )


def test_submission_chromosome_coordinates_to_msg():
    models.SubmissionChromosomeCoordinates(
        accession="accession",
        alternate_allele="A",
        assembly=models.Assembly.GRCH37,
        chromosome=models.Chromosome.CHR12,
        inner_start=100,
        inner_stop=200,
        outer_start=90,
        outer_stop=210,
        reference_allele="C",
        start=100,
        stop=200,
        variant_length=10,
    ).to_msg()
    models.SubmissionChromosomeCoordinates(
        assembly=models.Assembly.GRCH37,
        chromosome=models.Chromosome.CHR12,
        start=100,
        stop=100,
        reference_allele="C",
        alternate_allele="A",
        variant_length=1,
    ).to_msg()


def test_submission_variant_gene_construction():
    models.SubmissionVariantGene(
        id="some-id",
        symbol="some-symbol",
    )
    models.SubmissionVariantGene()


def test_submission_variant_gene_to_msg():
    models.SubmissionVariantGene(
        id="some-id",
        symbol="some-symbol",
    ).to_msg()
    models.SubmissionVariantGene().to_msg()


def test_submission_variant_construction():
    models.SubmissionVariant(
        chromosome_coordinates=models.SubmissionChromosomeCoordinates(
            assembly=models.Assembly.GRCH37,
            chromosome=models.Chromosome.CHR12,
            start=100,
            stop=100,
            reference_allele="C",
            alternate_allele="A",
            variant_length=1,
        ),
        copy_number="2",
        gene=[models.SubmissionVariantGene()],
        hgvs="hgvs-string",
        reference_copy_number="2",
        variant_type=models.VariantType.DELETION,
    )
    models.SubmissionVariant()


def test_submission_variant_to_msg():
    models.SubmissionVariant(
        chromosome_coordinates=models.SubmissionChromosomeCoordinates(
            assembly=models.Assembly.GRCH37,
            chromosome=models.Chromosome.CHR12,
            start=100,
            stop=100,
            reference_allele="C",
            alternate_allele="A",
            variant_length=1,
        ),
        copy_number="2",
        gene=[models.SubmissionVariantGene()],
        hgvs="hgvs-string",
        reference_copy_number="2",
        variant_type=models.VariantType.DELETION,
    ).to_msg()
    models.SubmissionVariant().to_msg()


def test_sumbmission_variant_set_construction():
    models.SubmissionVariantSet(variant=[models.SubmissionVariant()])
    models.SubmissionVariantSet(variant=[])


def test_sumbmission_variant_set_to_msg():
    models.SubmissionVariantSet(variant=[models.SubmissionVariant()]).to_msg()
    models.SubmissionVariantSet(variant=[]).to_msg()


def test_submission_phase_unknown_set_construction():
    models.SubmissionPhaseUnknownSet(
        hgvs="hgvs-string",
        variants=[models.SubmissionVariant()],
    )
    models.SubmissionPhaseUnknownSet(
        hgvs="hgvs-string",
        variants=[],
    )


def test_submission_phase_unknown_set_to_msg():
    models.SubmissionPhaseUnknownSet(
        hgvs="hgvs-string",
        variants=[models.SubmissionVariant()],
    ).to_msg()
    models.SubmissionPhaseUnknownSet(
        hgvs="hgvs-string",
        variants=[],
    ).to_msg()


def test_submission_clinical_feature_construction():
    models.SubmissionClinicalFeature(
        clinical_features_affected_status="affected-status",
        db="HP",
        id="the-id",
        name="same-name",
    )


def test_submission_clinical_feature_to_msg():
    models.SubmissionClinicalFeature(
        clinical_features_affected_status="affected-status",
        db="HP",
        id="the-id",
        name="same-name",
    ).to_msg()


def test_submission_observed_in_construction():
    models.SubmissionObservedIn(
        affected_status="affected",
        allele_origin="germline",
        collection_method="clinical testing",
        clinical_features=[
            models.SubmissionClinicalFeature(
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
    models.SubmissionObservedIn(
        affected_status="affected",
        allele_origin="germline",
        collection_method="clinical testing",
    )


def test_submission_observed_in_to_msg():
    models.SubmissionObservedIn(
        affected_status="affected",
        allele_origin="germline",
        collection_method="clinical testing",
        clinical_features=[
            models.SubmissionClinicalFeature(
                clinical_features_affected_status="affected-status",
                db="HP",
                id="the-id",
                name="same-name",
            )
        ],
        clinical_features_comment="some comment",
        number_of_individuals=1,
        struct_var_method_type="some-type",
    ).to_msg()
    models.SubmissionObservedIn(
        affected_status="affected",
        allele_origin="germline",
        collection_method="clinical testing",
    ).to_msg()


def test_submission_haplotype_set_construction():
    models.SubmissionHaplotypeSet(
        hgvs="the-hgvs",
        variants=[],
        star_allele_name="the-name",
    )
    models.SubmissionHaplotypeSet(
        hgvs="the-hgvs",
        variants=[models.SubmissionVariant()],
        star_allele_name="the-name",
    )


def test_submission_haplotype_set_to_msg():
    models.SubmissionHaplotypeSet(
        hgvs="the-hgvs",
        variants=[],
        star_allele_name="the-name",
    ).to_msg()
    models.SubmissionHaplotypeSet(
        hgvs="the-hgvs",
        variants=[models.SubmissionVariant()],
        star_allele_name="the-name",
    ).to_msg()


def test_submission_distinct_chromosome_set_construction():
    models.SubmissionDistinctChromosomesSet(
        hgvs="some-hgvs",
        variants=[
            models.SubmissionVariant(),
            models.SubmissionVariant(),
        ],
    )


def test_submission_distinct_chromosome_set_to_msg():
    models.SubmissionDistinctChromosomesSet(
        hgvs="some-hgvs",
        variants=[
            models.SubmissionVariant(),
            models.SubmissionVariant(),
        ],
    ).to_msg()


def test_submission_haplotype_sets_construction():
    models.SubmissionHaplotypeSets(
        haplotype_set=models.SubmissionHaplotypeSet(
            hgvs="the-hgvs",
            variants=[models.SubmissionVariant()],
            star_allele_name="the-name",
        ),
        haplotype_single_variant_set=models.SubmissionHaplotypeSet(
            hgvs="the-hgvs",
            variants=[models.SubmissionVariant()],
            star_allele_name="the-name",
        ),
    )
    models.SubmissionHaplotypeSets()


def test_submission_haplotype_sets_to_msg():
    models.SubmissionHaplotypeSets(
        haplotype_set=models.SubmissionHaplotypeSet(
            hgvs="the-hgvs",
            variants=[models.SubmissionVariant()],
            star_allele_name="the-name",
        ),
        haplotype_single_variant_set=models.SubmissionHaplotypeSet(
            hgvs="the-hgvs",
            variants=[models.SubmissionVariant()],
            star_allele_name="the-name",
        ),
    ).to_msg()
    models.SubmissionHaplotypeSets().to_msg()


def test_submission_diplotype_set_construction():
    models.SubmissionDiplotypeSet(
        haplotype_sets=[models.SubmissionHaplotypeSets()],
        hgvs="the-hgvs",
        star_allele_name="star-allele-name",
    )
    models.SubmissionDiplotypeSet(
        haplotype_sets=[models.SubmissionHaplotypeSets()],
        hgvs="the-hgvs",
        star_allele_name=None,
    )


def test_submission_diplotype_set_to_msg():
    models.SubmissionDiplotypeSet(
        haplotype_sets=[models.SubmissionHaplotypeSets()],
        hgvs="the-hgvs",
        star_allele_name="star-allele-name",
    ).to_msg()
    models.SubmissionDiplotypeSet(
        haplotype_sets=[models.SubmissionHaplotypeSets()],
        hgvs="the-hgvs",
        star_allele_name=None,
    ).to_msg()


def test_submission_citation_construction():
    models.SubmissionCitation(
        db=models.CitationDb.PMC,
        id="PMC123",
        url="https://example.com",
    )
    models.SubmissionCitation(
        db=None,
        id=None,
        url=None,
    )


def test_submission_citation_to_msg():
    models.SubmissionCitation(
        db=models.CitationDb.PMC,
        id="PMC123",
        url="https://example.com",
    ).to_msg()
    models.SubmissionCitation(
        db=None,
        id=None,
        url=None,
    ).to_msg()


def test_submission_assertion_criteria_construction():
    models.SubmissionAssertionCriteria(
        db=models.CitationDb.PMC,
        id="PMC123",
        url="https://example.com",
    ).to_msg()
    models.SubmissionAssertionCriteria(
        db=None,
        id=None,
        url=None,
    ).to_msg()


def test_submission_assertion_criteria_to_msg():
    models.SubmissionAssertionCriteria(
        db=models.CitationDb.PMC,
        id="PMC123",
        url="https://example.com",
    ).to_msg()


def test_submission_condition_construction():
    models.SubmissionCondition(
        db=models.ConditionDb.HP,
        id="some-id",
        name="some-name",
    )
    models.SubmissionCondition(
        db=None,
        id=None,
        name=None,
    )


def test_submission_condition_to_msg():
    models.SubmissionCondition(
        db=models.ConditionDb.HP,
        id="some-id",
        name="some-name",
    ).to_msg()
    models.SubmissionCondition(
        db=None,
        id=None,
        name=None,
    ).to_msg()


def test_submission_drug_response_construction():
    models.SubmissionDrugResponse(
        db=models.ConditionDb.HP,
        drug_name="some drug",
        id="some-id",
        condition=[models.SubmissionCondition()],
    )
    models.SubmissionDrugResponse(
        db=None,
        drug_name=None,
        id=None,
        condition=None,
    )


def test_submission_drug_response_to_msg():
    models.SubmissionDrugResponse(
        db=models.ConditionDb.HP,
        drug_name="some drug",
        id="some-id",
        condition=[models.SubmissionCondition()],
    ).to_msg()
    models.SubmissionDrugResponse(
        db=None,
        drug_name=None,
        id=None,
        condition=None,
    ).to_msg()


def test_submission_condition_set_construction():
    models.SubmissionConditionSet(
        condition=[models.SubmissionCondition()],
        drug_response=[models.SubmissionDrugResponse()],
    )
    models.SubmissionConditionSet(
        condition=None,
        drug_response=None,
    )


def test_submission_condition_set_to_msg():
    models.SubmissionConditionSet(
        condition=[models.SubmissionCondition()],
        drug_response=[models.SubmissionDrugResponse()],
    ).to_msg()
    models.SubmissionConditionSet(
        condition=None,
        drug_response=None,
    ).to_msg()


def test_submission_compound_heterozygote_set_variant_set_construction():
    models.SubmissionCompoundHeterozygoteSetVariantSet(
        variant_set=models.SubmissionVariantSet(variant=[]),
    )
    models.SubmissionCompoundHeterozygoteSetVariantSet(
        variant_set=None,
    )


def test_submission_compound_heterozygote_set_variant_set_to_msg():
    models.SubmissionCompoundHeterozygoteSetVariantSet(
        variant_set=models.SubmissionVariantSet(variant=[]),
    ).to_msg()
    models.SubmissionCompoundHeterozygoteSetVariantSet(
        variant_set=None,
    ).to_msg()


def test_submission_compound_heterozygote_set_construction():
    models.SubmissionCompoundHeterozygoteSet(
        hgvs="hgvs",
        variant_sets=[
            models.SubmissionCompoundHeterozygoteSetVariantSet(),
            models.SubmissionCompoundHeterozygoteSetVariantSet(),
        ],
    )


def test_submission_compound_heterozygote_set_to_msg():
    models.SubmissionCompoundHeterozygoteSet(
        hgvs="hgvs",
        variant_sets=[
            models.SubmissionCompoundHeterozygoteSetVariantSet(),
            models.SubmissionCompoundHeterozygoteSetVariantSet(),
        ],
    ).to_msg()


def test_submission_clinical_significance_construction():
    models.SubmissionClinicalSignificance(
        clinical_significance_description=models.ClinicalSignificanceDescription.PATHOGENIC,
        citation=[
            models.SubmissionCitation(
                db=models.CitationDb.PMC,
                id="PMC123",
                url="https://example.com",
            )
        ],
        comment="some comment",
        custom_assertion_score=42.0,
        date_last_evaluated="2022-01-01",
        explanation_of_drug_response="some explanation",
        explanation_of_other_clinical_significance="2022-01-01",
        mode_of_inheritance=models.ModeOfInheritance.AUTOSOMAL_DOMINANT_INHERITANCE,
    )
    models.SubmissionClinicalSignificance(
        clinical_significance_description=models.ClinicalSignificanceDescription.PATHOGENIC,
    )


def test_submission_clinical_significance_to_msg():
    models.SubmissionClinicalSignificance(
        clinical_significance_description=models.ClinicalSignificanceDescription.PATHOGENIC,
        citation=[
            models.SubmissionCitation(
                db=models.CitationDb.PMC,
                id="PMC123",
                url="https://example.com",
            )
        ],
        comment="some comment",
        custom_assertion_score=42.0,
        date_last_evaluated="2022-01-01",
        explanation_of_drug_response="some explanation",
        explanation_of_other_clinical_significance="2022-01-01",
        mode_of_inheritance=models.ModeOfInheritance.AUTOSOMAL_DOMINANT_INHERITANCE,
    ).to_msg()
    models.SubmissionClinicalSignificance(
        clinical_significance_description=models.ClinicalSignificanceDescription.PATHOGENIC,
    ).to_msg()


def test_submission_clinvar_submission_construction():
    models.SubmissionClinvarSubmission(
        clinical_significance=models.SubmissionClinicalSignificance(
            clinical_significance_description=models.ClinicalSignificanceDescription.PATHOGENIC,
        ),
        condition_set=models.SubmissionConditionSet(),
        observed_in=[
            models.SubmissionObservedIn(
                affected_status="affected",
                allele_origin="germline",
                collection_method="clinical testing",
            )
        ],
        record_status="record-status",
        clinvar_accession="some-accession",
        compound_heterozygote_set=models.SubmissionCompoundHeterozygoteSet(
            hgvs="hgvs",
            variant_sets=[
                models.SubmissionCompoundHeterozygoteSetVariantSet(),
                models.SubmissionCompoundHeterozygoteSetVariantSet(),
            ],
        ),
        diplotype_set=models.SubmissionDiplotypeSet(
            haplotype_sets=[models.SubmissionHaplotypeSets()],
            hgvs="the-hgvs",
        ),
        distinct_chromosomes_set=models.SubmissionDistinctChromosomesSet(
            hgvs="some-hgvs",
            variants=[
                models.SubmissionVariant(),
                models.SubmissionVariant(),
            ],
        ),
        haplotype_set=models.SubmissionHaplotypeSet(
            hgvs="the-hgvs",
            variants=[],
            star_allele_name="the-name",
        ),
        haplotype_single_variant_set=models.SubmissionHaplotypeSet(
            hgvs="the-hgvs",
            variants=[models.SubmissionVariant()],
            star_allele_name="the-name",
        ),
        local_id="local-id",
        local_key="local-key",
        phase_unknown_set=models.SubmissionPhaseUnknownSet(
            hgvs="hgvs-string",
            variants=[],
        ),
        variant_set=models.SubmissionVariantSet(variant=[]),
    )
    models.SubmissionClinvarSubmission(
        clinical_significance=models.SubmissionClinicalSignificance(
            clinical_significance_description=models.ClinicalSignificanceDescription.PATHOGENIC,
        ),
        condition_set=models.SubmissionConditionSet(),
        observed_in=[
            models.SubmissionObservedIn(
                affected_status="affected",
                allele_origin="germline",
                collection_method="clinical testing",
            )
        ],
        record_status="record-status",
    )


def test_submission_clinvar_submission_to_msg():
    models.SubmissionClinvarSubmission(
        clinical_significance=models.SubmissionClinicalSignificance(
            clinical_significance_description=models.ClinicalSignificanceDescription.PATHOGENIC,
        ),
        condition_set=models.SubmissionConditionSet(),
        observed_in=[
            models.SubmissionObservedIn(
                affected_status="affected",
                allele_origin="germline",
                collection_method="clinical testing",
            )
        ],
        record_status="record-status",
        clinvar_accession="some-accession",
        compound_heterozygote_set=models.SubmissionCompoundHeterozygoteSet(
            hgvs="hgvs",
            variant_sets=[
                models.SubmissionCompoundHeterozygoteSetVariantSet(),
                models.SubmissionCompoundHeterozygoteSetVariantSet(),
            ],
        ),
        diplotype_set=models.SubmissionDiplotypeSet(
            haplotype_sets=[models.SubmissionHaplotypeSets()],
            hgvs="the-hgvs",
        ),
        distinct_chromosomes_set=models.SubmissionDistinctChromosomesSet(
            hgvs="some-hgvs",
            variants=[
                models.SubmissionVariant(),
                models.SubmissionVariant(),
            ],
        ),
        haplotype_set=models.SubmissionHaplotypeSet(
            hgvs="the-hgvs",
            variants=[],
            star_allele_name="the-name",
        ),
        haplotype_single_variant_set=models.SubmissionHaplotypeSet(
            hgvs="the-hgvs",
            variants=[models.SubmissionVariant()],
            star_allele_name="the-name",
        ),
        local_id="local-id",
        local_key="local-key",
        phase_unknown_set=models.SubmissionPhaseUnknownSet(
            hgvs="hgvs-string",
            variants=[],
        ),
        variant_set=models.SubmissionVariantSet(variant=[]),
    ).to_msg()
    models.SubmissionClinvarSubmission(
        clinical_significance=models.SubmissionClinicalSignificance(
            clinical_significance_description=models.ClinicalSignificanceDescription.PATHOGENIC,
        ),
        condition_set=models.SubmissionConditionSet(),
        observed_in=[
            models.SubmissionObservedIn(
                affected_status="affected",
                allele_origin="germline",
                collection_method="clinical testing",
            )
        ],
        record_status="record-status",
    ).to_msg()


def test_submission_container_construction():
    models.SubmissionContainer(
        behalf_org_id=123,
        clinvar_deletion=models.SubmissionClinvarDeletion(
            accession_set=[
                models.SubmissionClinvarDeletionAccessionSet(
                    accession="accession",
                    reason="whatever",
                )
            ]
        ),
        clinvar_submission=None,
        clinvar_submission_release_status="release-status",
        submission_name="some-name",
    )
    models.SubmissionContainer(
        behalf_org_id=123,
        clinvar_deletion=None,
        clinvar_submission=[
            models.SubmissionClinvarSubmission(
                clinical_significance=models.SubmissionClinicalSignificance(
                    clinical_significance_description=models.ClinicalSignificanceDescription.PATHOGENIC,
                ),
                condition_set=models.SubmissionConditionSet(),
                observed_in=[
                    models.SubmissionObservedIn(
                        affected_status="affected",
                        allele_origin="germline",
                        collection_method="clinical testing",
                    )
                ],
                record_status="record-status",
            )
        ],
        clinvar_submission_release_status="release-status",
        submission_name="some-name",
    )


def test_submission_container_to_msg():
    models.SubmissionContainer(
        behalf_org_id=123,
        clinvar_deletion=models.SubmissionClinvarDeletion(
            accession_set=[
                models.SubmissionClinvarDeletionAccessionSet(
                    accession="accession",
                    reason="whatever",
                )
            ]
        ),
        clinvar_submission=None,
        clinvar_submission_release_status="release-status",
        submission_name="some-name",
    ).to_msg()
    models.SubmissionContainer(
        behalf_org_id=123,
        clinvar_deletion=None,
        clinvar_submission=[
            models.SubmissionClinvarSubmission(
                clinical_significance=models.SubmissionClinicalSignificance(
                    clinical_significance_description=models.ClinicalSignificanceDescription.PATHOGENIC,
                ),
                condition_set=models.SubmissionConditionSet(),
                observed_in=[
                    models.SubmissionObservedIn(
                        affected_status="affected",
                        allele_origin="germline",
                        collection_method="clinical testing",
                    )
                ],
                record_status="record-status",
            )
        ],
        clinvar_submission_release_status="release-status",
        submission_name="some-name",
    ).to_msg()
