"""Helper code for cattrs."""
import datetime

import cattrs
from dateutil.parser import parse as parse_datetime

CONVERTER = cattrs.Converter()
CONVERTER.register_unstructure_hook(datetime.date, lambda d: d.strftime("%Y-%m-%d"))
CONVERTER.register_unstructure_hook(datetime.datetime, lambda d: d.strftime("%Y-%m-%d %H:%M:%S"))
CONVERTER.register_structure_hook(datetime.date, lambda s, _: parse_datetime(s).date())
CONVERTER.register_structure_hook(datetime.datetime, lambda s, _: parse_datetime(s))
