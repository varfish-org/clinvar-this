import logging
import typing

DEFAULT_FORMAT: str
DEFAULT_DATE_FORMAT: str
DEFAULT_COLORS: typing.Dict[int, int]

class LogFormatter(logging.Formatter):
    def __init__(
        self,
        color: bool = True,
        fmt: str = DEFAULT_FORMAT,
        datefmt: str = DEFAULT_DATE_FORMAT,
        colors: typing.Dict[int, int] = DEFAULT_COLORS,
    ): ...
    def format(self, record): ...

logger: logging.Logger
