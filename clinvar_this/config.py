"""Configuration management."""

import pathlib

import attrs
import cattrs
import toml

from clinvar_this import exceptions


def _obfuscate_repr(s):
    """Helper function for obfustating passwords"""
    if len(s) < 5:
        return repr("*" * len(s))
    else:
        return repr(s[:5] + "*" * (len(s) - 5))


@attrs.define(frozen=True)
class Config:
    """Configuration for the ``clinvar-this`` app."""

    #: The authentication token to use in the API.
    auth_token: str = attrs.field(repr=_obfuscate_repr)


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

    if profile not in config_dict:
        raise exceptions.ConfigException(
            f"Could not find profile {profile} in configuration file {config_path}."
        )

    return Config(auth_token=config_dict[profile].get("auth_token"))


def save_config(config: Config, profile: str = "default"):
    """Save configuration to the given profile."""

    config_path = pathlib.Path.home() / ".config" / "clinvar-this" / "config.toml"

    if not config_path.parent.exists():
        config_path.parent.mkdir(parents=True)

    all_config = {}
    if config_path.exists():
        with config_path.open("rt") as configf:
            all_config = toml.load(configf)
    all_config.setdefault("default", {})
    all_config[profile] = cattrs.unstructure(config)

    with config_path.open("wt") as configf:
        toml.dump(all_config, configf)
