# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: clinvar_data/pbs/extracted_vars.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from clinvar_data.pbs import (
    clinvar_public_pb2 as clinvar__data_dot_pbs_dot_clinvar__public__pb2,
)

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n%clinvar_data/pbs/extracted_vars.proto\x12\x1f\x63linvar_data.pbs.extracted_vars\x1a%clinvar_data/pbs/clinvar_public.proto"8\n\x12VersionedAccession\x12\x11\n\taccession\x18\x01 \x01(\t\x12\x0f\n\x07version\x18\x02 \x01(\x05"\xc6\x01\n\x12\x45xtractedRcvRecord\x12\x46\n\taccession\x18\x01 \x01(\x0b\x32\x33.clinvar_data.pbs.extracted_vars.VersionedAccession\x12\r\n\x05title\x18\x02 \x01(\t\x12Y\n\x0f\x63lassifications\x18\x03 \x01(\x0b\x32@.clinvar_data.pbs.clinvar_public.RcvAccession.RcvClassifications"\xb4\x03\n\x12\x45xtractedVcvRecord\x12\x46\n\taccession\x18\x01 \x01(\x0b\x32\x33.clinvar_data.pbs.extracted_vars.VersionedAccession\x12\x41\n\x04rcvs\x18\x02 \x03(\x0b\x32\x33.clinvar_data.pbs.extracted_vars.ExtractedRcvRecord\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\x46\n\x0evariation_type\x18\x04 \x01(\x0e\x32..clinvar_data.pbs.extracted_vars.VariationType\x12T\n\x0f\x63lassifications\x18\x05 \x01(\x0b\x32;.clinvar_data.pbs.clinvar_public.AggregateClassificationSet\x12U\n\x11sequence_location\x18\x06 \x01(\x0b\x32:.clinvar_data.pbs.clinvar_public.Location.SequenceLocation\x12\x10\n\x08hgnc_ids\x18\x07 \x03(\t*\xd0\x03\n\rVariationType\x12\x1e\n\x1aVARIATION_TYPE_UNSPECIFIED\x10\x00\x12\x1c\n\x18VARIATION_TYPE_INSERTION\x10\x01\x12\x1b\n\x17VARIATION_TYPE_DELETION\x10\x02\x12\x16\n\x12VARIATION_TYPE_SNV\x10\x03\x12\x18\n\x14VARIATION_TYPE_INDEL\x10\x04\x12\x1e\n\x1aVARIATION_TYPE_DUPLICATION\x10\x05\x12%\n!VARIATION_TYPE_TANDEM_DUPLICATION\x10\x06\x12%\n!VARIATION_TYPE_STRUCTURAL_VARIANT\x10\x07\x12#\n\x1fVARIATION_TYPE_COPY_NUMBER_GAIN\x10\x08\x12#\n\x1fVARIATION_TYPE_COPY_NUMBER_LOSS\x10\t\x12\x1f\n\x1bVARIATION_TYPE_PROTEIN_ONLY\x10\n\x12!\n\x1dVARIATION_TYPE_MICROSATELLITE\x10\x0b\x12\x1c\n\x18VARIATION_TYPE_INVERSION\x10\x0c\x12\x18\n\x14VARIATION_TYPE_OTHER\x10\rb\x06proto3'
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "clinvar_data.pbs.extracted_vars_pb2", _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _globals["_VARIATIONTYPE"]._serialized_start = 812
    _globals["_VARIATIONTYPE"]._serialized_end = 1276
    _globals["_VERSIONEDACCESSION"]._serialized_start = 113
    _globals["_VERSIONEDACCESSION"]._serialized_end = 169
    _globals["_EXTRACTEDRCVRECORD"]._serialized_start = 172
    _globals["_EXTRACTEDRCVRECORD"]._serialized_end = 370
    _globals["_EXTRACTEDVCVRECORD"]._serialized_start = 373
    _globals["_EXTRACTEDVCVRECORD"]._serialized_end = 809
# @@protoc_insertion_point(module_scope)
