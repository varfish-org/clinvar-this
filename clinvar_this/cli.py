"""Console script for ClinVar This!"""

import attrs
import click

from clinvar_this import exceptions
from clinvar_this.config import Config, load_config, save_config


@click.group()
@click.option("--verbose/--no-verbose", default=False)
@click.option("--profile", default="default", help="The profile to use")
@click.pass_context
def cli(ctx: click.Context, verbose: bool, profile: str):
    """Main entry point for CLI via click."""
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose
    ctx.obj["profile"] = profile


@cli.group()
@click.pass_context
def config(ctx: click.Context):
    """Sub command category ``varfish-this config ...``"""
    _ = ctx


@config.command("set")
@click.argument("name")
@click.argument("value")
@click.pass_context
def config_set(ctx: click.Context, name: str, value: str):
    """Sub command ``varfish-this config set NAME VALUE``.

    Set the configuration variable with the given ``NAME`` to the given ``VALUE``.  This will interpret the
    current ``--profile`` setting.
    """
    profile: str = ctx.obj["profile"]
    try:
        config_obj = load_config(profile)
    except exceptions.ConfigFileMissingException:
        config_obj = Config(auth_token="")  # swallow, will recreate
    allowed_names = ["auth_token"]
    if name not in allowed_names:
        raise click.ClickException(f"Invalid value {name}, must be one of {allowed_names}")
    config_obj = attrs.evolve(config_obj, **{name: value})
    save_config(config_obj, profile)


@config.command("get")
@click.option("--profile", default="default", help="The profile to get the value from")
@click.argument("name")
def config_get(profile: str, name: str):
    """Sub command ``varfish-this config get NAME``.

    Show the configuration variable with the given ``NAME``.  This will interpret the current ``--profile`` setting.
    """
    config = load_config(profile)
    print(getattr(config, name, "<undefined>"))
