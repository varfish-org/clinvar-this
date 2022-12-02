"""Console script for ClinVar This!"""

import typing

import attrs
import click

from clinvar_this import batches, exceptions
from clinvar_this.config import Config, dump_config, load_config, save_config


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
def config():
    """Sub command category ``varfish-this config ...``"""


@config.command("set")
@click.argument("name")
@click.argument("value")
@click.pass_context
def config_set(ctx: click.Context, name: str, value: str):
    """Sub command ``varfish-this config set NAME VALUE``

    Set the configuration variable with the given ``NAME`` to the given ``VALUE``.  This will interpret the
    current ``--profile`` setting.
    """
    profile: str = ctx.obj["profile"]
    try:
        config_obj = load_config(profile)
    except exceptions.ConfigFileMissingException:
        config_obj = Config(profile=profile, auth_token="")  # swallow, will recreate
    allowed_names = ["auth_token"]
    if name not in allowed_names:
        raise click.ClickException(f"Invalid value {name}, must be one of {allowed_names}")
    config_obj = attrs.evolve(config_obj, **{name: value})
    save_config(config_obj, profile)


@config.command("get")
@click.option("--profile", default="default", help="The profile to get the value from")
@click.argument("name")
def config_get(profile: str, name: str):
    """Sub command ``varfish-this config get NAME``

    Show the configuration variable with the given ``NAME``.  This will interpret the current ``--profile`` setting.
    """
    config = load_config(profile)
    print(getattr(config, name, "<undefined>"))


@config.command("dump")
def config_dump():
    """Sub command ``varfish-this config dump``

    Print the configuration file to stdout.
    """
    dump_config()


@cli.group("batch")
def batch():
    """Sub comment category ``batch ...``"""


@batch.command("list")
@click.pass_context
def batch_list(ctx: click.Context):
    """List existing batches"""
    config_obj = load_config(ctx.obj["profile"])
    batches.list_(config_obj)


@batch.command("import")
@click.argument("path")
@click.option(
    "--metadata",
    "-m",
    required=False,
    multiple=True,
    help="Provide meta data settings as KEY=VALUE settings",
)
@click.option("--name", required=False, default=None, help="Name of the batch to create or add to")
@click.pass_context
def batch_import(
    ctx: click.Context,
    path: str,
    name: typing.Optional[str] = None,
    metadata: typing.Optional[typing.Tuple[str, ...]] = None,
):
    """Import data for a new or existing batch"""
    config_obj = load_config(ctx.obj["profile"])
    if not name:
        name = batches.gen_name(config_obj)
        print(f"Using name = {name}")
    if not metadata:
        metadata = ()
    print(f"metadata = {metadata}")
    config_obj = load_config(ctx.obj["profile"])
    batches.import_(config_obj, name, path, metadata)


@batch.command("export")
@click.argument("name")
@click.argument("path")
@click.option("--force/--no-force", required=False, default=False, help="Overwrite existing files")
@click.pass_context
def batch_export(
    ctx: click.Context,
    name: str,
    path: str,
    force: bool = False,
):
    """Export batch data to a given file"""
    config_obj = load_config(ctx.obj["profile"])
    batches.export_(config_obj, name, path, force)


@batch.command("update")
@click.argument("name")
@click.argument("metadata", nargs=-1)
@click.pass_context
def batch_update(
    ctx: click.Context, name: str, metadata: typing.Optional[typing.Tuple[str, ...]] = None
):
    """Update batch data without importing files"""
    if not metadata:
        metadata = ()
    print(metadata)
    config_obj = load_config(ctx.obj["profile"])
    batches.update(config_obj, name, metadata)


@batch.command("submit")
@click.option(
    "--use-testing/--no-testing",
    required=False,
    default=False,
    help="Whether to use the testing API",
)
@click.option(
    "--dry-run/--no-dry-run",
    required=False,
    default=False,
    help="Whether to use the ClinVar dry-run",
)
@click.argument("name")
@click.pass_context
def batch_submit(ctx: click.Context, use_testing: bool, dry_run: bool, name: str):
    """Submit the given batch to ClinVar"""
    config_obj = load_config(ctx.obj["profile"])
    batches.submit(config_obj, name, use_testing=use_testing, dry_run=dry_run)


@batch.command("retrieve")
@click.option(
    "--use-testing/--no-testing",
    required=False,
    default=False,
    help="Whether to use the testing API",
)
@click.argument("name")
@click.pass_context
def batch_retrieve(ctx: click.Context, use_testing: bool, name: str):
    """Submit the given batch to ClinVar"""
    config_obj = load_config(ctx.obj["profile"])
    batches.retrieve(config_obj, name, use_testing=use_testing)
