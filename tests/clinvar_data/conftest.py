import os

import pytest


@pytest.fixture(autouse=True)
def use_utc_time():
    """Use UTC time zone for all tests in ``clinvar_data``."""
    curr_time = os.environ.get("TZ")
    os.environ["TZ"] = "UTC"
    yield
    if curr_time:
        os.environ["TZ"] = curr_time
