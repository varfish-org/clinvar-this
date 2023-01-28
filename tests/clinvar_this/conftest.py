import os

import pytest


@pytest.fixture
def fs_config(fs):
    """Fake file system with fake config"""
    fs.create_file(
        os.path.expanduser("~/.config/clinvar-this/config.toml"),
        contents='[default]\nauth_token = "fake"',
    )
    yield fs
