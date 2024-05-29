"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
Protocol buffers to store the extracted variants from ClinVar."""

import builtins
import clinvar_data.pbs.clinvar_public_pb2
import collections.abc
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import sys
import typing

if sys.version_info >= (3, 10):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class _VariationType:
    ValueType = typing.NewType("ValueType", builtins.int)
    V: typing_extensions.TypeAlias = ValueType

class _VariationTypeEnumTypeWrapper(
    google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_VariationType.ValueType],
    builtins.type,
):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    VARIATION_TYPE_UNSPECIFIED: _VariationType.ValueType  # 0
    """unspecified variation type"""
    VARIATION_TYPE_INSERTION: _VariationType.ValueType  # 1
    """Corresponds to "insertion"."""
    VARIATION_TYPE_DELETION: _VariationType.ValueType  # 2
    """Corresponds to "deletion"."""
    VARIATION_TYPE_SNV: _VariationType.ValueType  # 3
    """Corresponds to "single nucleotide variant"."""
    VARIATION_TYPE_INDEL: _VariationType.ValueType  # 4
    """Corresponds to "indel"."""
    VARIATION_TYPE_DUPLICATION: _VariationType.ValueType  # 5
    """Corresponds to "duplication"."""
    VARIATION_TYPE_TANDEM_DUPLICATION: _VariationType.ValueType  # 6
    """Corresponds to "tandem duplication"."""
    VARIATION_TYPE_STRUCTURAL_VARIANT: _VariationType.ValueType  # 7
    """Corresponds to "structural variant"."""
    VARIATION_TYPE_COPY_NUMBER_GAIN: _VariationType.ValueType  # 8
    """Corresponds to "copy number gain"."""
    VARIATION_TYPE_COPY_NUMBER_LOSS: _VariationType.ValueType  # 9
    """Corresponds to "copy number loss"."""
    VARIATION_TYPE_PROTEIN_ONLY: _VariationType.ValueType  # 10
    """Corresponds to "protein only"."""
    VARIATION_TYPE_MICROSATELLITE: _VariationType.ValueType  # 11
    """Corresponds to "microsatellite"."""
    VARIATION_TYPE_INVERSION: _VariationType.ValueType  # 12
    """Corresponds to "inversion"."""
    VARIATION_TYPE_OTHER: _VariationType.ValueType  # 13
    """Corresponds to "other"."""

class VariationType(_VariationType, metaclass=_VariationTypeEnumTypeWrapper):
    """Enumeration for the type of the variant."""

VARIATION_TYPE_UNSPECIFIED: VariationType.ValueType  # 0
"""unspecified variation type"""
VARIATION_TYPE_INSERTION: VariationType.ValueType  # 1
"""Corresponds to "insertion"."""
VARIATION_TYPE_DELETION: VariationType.ValueType  # 2
"""Corresponds to "deletion"."""
VARIATION_TYPE_SNV: VariationType.ValueType  # 3
"""Corresponds to "single nucleotide variant"."""
VARIATION_TYPE_INDEL: VariationType.ValueType  # 4
"""Corresponds to "indel"."""
VARIATION_TYPE_DUPLICATION: VariationType.ValueType  # 5
"""Corresponds to "duplication"."""
VARIATION_TYPE_TANDEM_DUPLICATION: VariationType.ValueType  # 6
"""Corresponds to "tandem duplication"."""
VARIATION_TYPE_STRUCTURAL_VARIANT: VariationType.ValueType  # 7
"""Corresponds to "structural variant"."""
VARIATION_TYPE_COPY_NUMBER_GAIN: VariationType.ValueType  # 8
"""Corresponds to "copy number gain"."""
VARIATION_TYPE_COPY_NUMBER_LOSS: VariationType.ValueType  # 9
"""Corresponds to "copy number loss"."""
VARIATION_TYPE_PROTEIN_ONLY: VariationType.ValueType  # 10
"""Corresponds to "protein only"."""
VARIATION_TYPE_MICROSATELLITE: VariationType.ValueType  # 11
"""Corresponds to "microsatellite"."""
VARIATION_TYPE_INVERSION: VariationType.ValueType  # 12
"""Corresponds to "inversion"."""
VARIATION_TYPE_OTHER: VariationType.ValueType  # 13
"""Corresponds to "other"."""
global___VariationType = VariationType

@typing.final
class VersionedAccession(google.protobuf.message.Message):
    """Accession with version."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ACCESSION_FIELD_NUMBER: builtins.int
    VERSION_FIELD_NUMBER: builtins.int
    accession: builtins.str
    """The accession."""
    version: builtins.int
    """The version."""
    def __init__(
        self,
        *,
        accession: builtins.str = ...,
        version: builtins.int = ...,
    ) -> None: ...
    def ClearField(
        self, field_name: typing.Literal["accession", b"accession", "version", b"version"]
    ) -> None: ...

global___VersionedAccession = VersionedAccession

@typing.final
class ExtractedRcvRecord(google.protobuf.message.Message):
    """Protocol buffer for storing essential information of one RCV."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ACCESSION_FIELD_NUMBER: builtins.int
    TITLE_FIELD_NUMBER: builtins.int
    CLASSIFICATIONS_FIELD_NUMBER: builtins.int
    title: builtins.str
    """Title of RCV."""
    @property
    def accession(self) -> global___VersionedAccession:
        """The accession."""

    @property
    def classifications(
        self,
    ) -> clinvar_data.pbs.clinvar_public_pb2.RcvAccession.RcvClassifications:
        """Classifications (thinned out)."""

    def __init__(
        self,
        *,
        accession: global___VersionedAccession | None = ...,
        title: builtins.str = ...,
        classifications: (
            clinvar_data.pbs.clinvar_public_pb2.RcvAccession.RcvClassifications | None
        ) = ...,
    ) -> None: ...
    def HasField(
        self,
        field_name: typing.Literal[
            "accession", b"accession", "classifications", b"classifications"
        ],
    ) -> builtins.bool: ...
    def ClearField(
        self,
        field_name: typing.Literal[
            "accession", b"accession", "classifications", b"classifications", "title", b"title"
        ],
    ) -> None: ...

global___ExtractedRcvRecord = ExtractedRcvRecord

@typing.final
class ExtractedVcvRecord(google.protobuf.message.Message):
    """Protocol buffer for storing essential information of one VCV."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ACCESSION_FIELD_NUMBER: builtins.int
    RCVS_FIELD_NUMBER: builtins.int
    NAME_FIELD_NUMBER: builtins.int
    VARIATION_TYPE_FIELD_NUMBER: builtins.int
    CLASSIFICATIONS_FIELD_NUMBER: builtins.int
    SEQUENCE_LOCATION_FIELD_NUMBER: builtins.int
    HGNC_IDS_FIELD_NUMBER: builtins.int
    name: builtins.str
    """Name of VCV."""
    variation_type: global___VariationType.ValueType
    """The type of the variant."""
    @property
    def accession(self) -> global___VersionedAccession:
        """The accession."""

    @property
    def rcvs(
        self,
    ) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[
        global___ExtractedRcvRecord
    ]:
        """List of aggregated RCVs."""

    @property
    def classifications(self) -> clinvar_data.pbs.clinvar_public_pb2.AggregateClassificationSet:
        """Classifications (thinned out)."""

    @property
    def sequence_location(self) -> clinvar_data.pbs.clinvar_public_pb2.Location.SequenceLocation:
        """The sequence location on one reference."""

    @property
    def hgnc_ids(
        self,
    ) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]:
        """List of HGNC IDs."""

    def __init__(
        self,
        *,
        accession: global___VersionedAccession | None = ...,
        rcvs: collections.abc.Iterable[global___ExtractedRcvRecord] | None = ...,
        name: builtins.str = ...,
        variation_type: global___VariationType.ValueType = ...,
        classifications: (
            clinvar_data.pbs.clinvar_public_pb2.AggregateClassificationSet | None
        ) = ...,
        sequence_location: (
            clinvar_data.pbs.clinvar_public_pb2.Location.SequenceLocation | None
        ) = ...,
        hgnc_ids: collections.abc.Iterable[builtins.str] | None = ...,
    ) -> None: ...
    def HasField(
        self,
        field_name: typing.Literal[
            "accession",
            b"accession",
            "classifications",
            b"classifications",
            "sequence_location",
            b"sequence_location",
        ],
    ) -> builtins.bool: ...
    def ClearField(
        self,
        field_name: typing.Literal[
            "accession",
            b"accession",
            "classifications",
            b"classifications",
            "hgnc_ids",
            b"hgnc_ids",
            "name",
            b"name",
            "rcvs",
            b"rcvs",
            "sequence_location",
            b"sequence_location",
            "variation_type",
            b"variation_type",
        ],
    ) -> None: ...

global___ExtractedVcvRecord = ExtractedVcvRecord
