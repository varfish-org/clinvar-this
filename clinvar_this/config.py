"""Configuration management."""

import datetime
import pathlib
import sys

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

    #: The name of the profile.
    profile: str

    #: The authentication token to use in the API.
    auth_token: str = attrs.field(repr=_obfuscate_repr)

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
    all_config[profile] = {k: v for k, v in cattrs.unstructure(config).items() if k != "profile"}

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
