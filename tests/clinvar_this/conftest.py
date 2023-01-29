import os

import pytest

from clinvar_this import config


@pytest.fixture
def fs_config(fs):
    """Fake file system with fake config"""
    fs.create_file(
        os.path.expanduser("~/.config/clinvar-this/config.toml"),
        contents='[default]\nauth_token = "fake"',
    )
    yield fs


@pytest.fixture
def app_config():
    yield config.Config(
        profile="default",
        auth_token="fake_auth_token",
        verify_ssl=False,
    )
