"""Configuration management."""

import datetime
import pathlib
import sys

from pydantic import BaseModel, SecretStr
from pydantic.config import ConfigDict
import toml

from clinvar_this import exceptions


class Config(BaseModel):
    """Configuration for the ``clinvar-this`` app."""

    model_config = ConfigDict(frozen=True)

    #: The name of the profile.
    profile: str

    #: The authentication token to use in the API.
    auth_token: SecretStr

    #: Whether to verify SSL or not
    verify_ssl: bool = True


def load_config(profile: str = "default") -> Config:
    """Load configuration for the given profile.

    :params profile: The profile to load configuration for.
    :returns: The ``Config`` with the configuration.
    :raises exceptions.ConfigException: In the case of problems with configuration.
    """

    config_path = pathlib.Path.home() / ".config" / "clinvar-this" / "config.toml"

    if not config_path.exists():
        raise exceptions.ConfigFileMissingException(
            f"Configuration file {config_path} does not exist. Try `clinvar-this config set auth_token XXX`."
        )

    with config_path.open("rt") as configf:
        try:
            config_dict = toml.load(configf)
        except toml.TomlDecodeError as e:
            raise exceptions.ConfigException(
                f"Problem decoding configuration file {config_path}"
            ) from e

    return Config(profile=profile, auth_token=config_dict.get(profile, {}).get("auth_token"))


def save_config(config: Config, profile: str = "default"):
    """Save configuration to the given profile."""

    config_path = pathlib.Path.home() / ".config" / "clinvar-this" / "config.toml"

    if not config_path.parent.exists():
        config_path.parent.mkdir(parents=True)

    all_config = {}
    if config_path.exists():
        with config_path.open("rt") as configf:
            all_config = toml.load(configf)
        # create backup
        suffix = datetime.datetime.now().strftime("%Y%m%d-%H%M%S.%f")
        backup_path = config_path.parent / (config_path.name + f"~{suffix}")
        config_path.rename(backup_path)

    all_config.setdefault("default", {})
    all_config[profile] = {
        k: v for k, v in config.model_dump(mode="json").items() if k != "profile"
    }
    all_config[profile]["auth_token"] = config.auth_token.get_secret_value()

    with config_path.open("wt") as configf:
        toml.dump(all_config, configf)


def dump_config(outf=None):
    """Dump configuraiton file to ``outf``."""
    if not outf:
        outf = sys.stdout

    config_path = pathlib.Path.home() / ".config" / "clinvar-this" / "config.toml"
    if config_path.exists():
        with config_path.open("rt") as configf:
            print(f"# path: {config_path}", file=outf)
            print(configf.read(), file=outf)
    else:
        print(f"# no file at path: {config_path}", file=outf)
