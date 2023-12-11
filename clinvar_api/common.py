import typing


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
