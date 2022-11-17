import datetime
import typing
import uuid

import cattr
import dateutil.parser


def _setup_converter() -> cattr.Converter:
    """Setup ``cattr`` converter for UUID and datetime."""
    result = cattr.Converter()
    result.register_structure_hook(uuid.UUID, lambda d, _: uuid.UUID(d))
    result.register_unstructure_hook(uuid.UUID, str)
    result.register_structure_hook(datetime.datetime, lambda d, _: dateutil.parser.parse(d))
    result.register_unstructure_hook(
        datetime.datetime,
        lambda obj: obj.replace(tzinfo=datetime.timezone.utc)
        .astimezone()
        .replace(microsecond=0)
        .isoformat(),
    )
    return result


#: cattr Converter to use
CONVERTER = _setup_converter()


def clean_for_json(
    value: typing.Union[
        bool, int, float, typing.List[typing.Any], None, typing.Dict[str, typing.Any]
    ]
) -> typing.Union[bool, int, float, typing.List[typing.Any], None, typing.Dict[str, typing.Any]]:
    """Clean the given value for JSON submission."""
    if isinstance(value, dict):
        return {k: clean_for_json(v) for k, v in value.items() if v is not None}
    elif isinstance(value, list):
        return [clean_for_json(elem) for elem in value]
    else:
        return value
