import datetime
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
