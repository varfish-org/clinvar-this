"""Console script for ClinVar This!"""

import typing

import click
from pydantic import SecretStr

from clinvar_data import (
    class_by_freq,
    conversion,
    extract_vars,
    gene_impact,
    phenotype_link,
)
from clinvar_this import _version, batches, exceptions
from clinvar_this.config import Config, dump_config, load_config, save_config


@click.group()
@click.version_option(_version.__version__)
@click.option("--verbose/--no-verbose", default=False)
@click.option("--profile", default="default", help="The profile to use")
@click.option(
    "--verify-ssl/--no-verify-ssl", default=True, help="Whether to enable SSL verification"
)
@click.pass_context
def cli(ctx: click.Context, verbose: bool, profile: str, verify_ssl: bool):
    """Main entry point for CLI via click."""
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose
    ctx.obj["profile"] = profile
    ctx.obj["verify_ssl"] = verify_ssl


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
        config_obj = Config(profile=profile, auth_token=SecretStr(""))  # swallow, will recreate
    allowed_names = ["auth_token"]
    if name not in allowed_names:
        raise click.ClickException(f"Invalid value {name}, must be one of {allowed_names}")
    # We need to ignore type checking in the following line because of a false positive:
    #
    # error: Argument 2 to "evolve" of "Config" has incompatible type "**dict[str, str]";
    # expected "bool"  [arg-type]
    if name == "auth_token":
        config_obj = config_obj.model_copy(update={name: SecretStr(value)})  # type: ignore
    else:
        config_obj = config_obj.model_copy(update={name: value})  # type: ignore
    save_config(config_obj, profile)


@config.command("get")
@click.option("--profile", default="default", help="The profile to get the value from")
@click.argument("name")
def config_get(profile: str, name: str):
    """Sub command ``varfish-this config get NAME``

    Show the configuration variable with the given ``NAME``.  This will interpret the current ``--profile`` setting.
    """
    config = load_config(profile)
    if name == "auth_token":
        print(getattr(config, name).get_secret_value())
    else:
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
@click.option(
    "--struc-var/--no-struc-var",
    required=False,
    default=False,
    help="Export structural variants rather than sequence variants",
)
@click.pass_context
def batch_export(
    ctx: click.Context,
    name: str,
    path: str,
    force: bool = False,
    struc_var: bool = False,
):
    """Export batch data to a given file"""
    config_obj = load_config(ctx.obj["profile"])
    batches.export(config_obj, name, path, force, struc_var)


@batch.command("update-metadata")
@click.argument("name")
@click.argument("metadata", nargs=-1)
@click.pass_context
def batch_update_metadata(
    ctx: click.Context, name: str, metadata: typing.Optional[typing.Tuple[str, ...]] = None
):
    """Update batch metadata without importing files"""
    if not metadata:
        metadata = ()
    print(metadata)
    config_obj = load_config(ctx.obj["profile"])
    batches.update_metadata(config_obj, name, metadata)


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
    config_obj = config_obj.model_copy(update={"verify_ssl": ctx.obj["verify_ssl"]})
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
    config_obj = config_obj.model_copy(update={"verify_ssl": ctx.obj["verify_ssl"]})
    batches.retrieve(config_obj, name, use_testing=use_testing)


@cli.group("data")
def data():
    """Sub command category "data"."""


@data.command("xml-to-jsonl")
@click.argument("input_file")
@click.argument("output_file")
@click.option(
    "--max-records", required=False, default=0, help="Maximum number of records to convert"
)
@click.pass_context
def xml_to_jsonl(ctx: click.Context, input_file: str, output_file: str, max_records: int):
    """Convert XML to JSONL"""
    retcode = conversion.convert(input_file, output_file, max_records=max_records, use_click=True)
    ctx.exit(retcode)


@data.command("gene-variant-report")
@click.argument("input_file")
@click.argument("output_file")
@click.pass_context
def gene_impact_report(ctx: click.Context, input_file: str, output_file: str):
    """Create a gene variant summary report."""
    _ = ctx
    gene_impact.run_report(input_file, output_file)


@data.command("gene-phenotype-links")
@click.argument("input_file")
@click.argument("output_file")
@click.option(
    "--needs-hpo-terms/--no-needs-hpo-terms",
    type=bool,
    default=True,
    help="Whether to filter to rows with HPO terms (default: true)",
)
@click.pass_context
def gene_phenotype_links(
    ctx: click.Context, input_file: str, output_file: str, needs_hpo_terms: bool
):
    """Create links between gene and phenotype."""
    _ = ctx
    phenotype_link.run_report(input_file, output_file, needs_hpo_terms=needs_hpo_terms)


@data.command("acmg-class-by-freq")
@click.argument("input_file")
@click.argument("output_file")
@click.option(
    "--thresholds",
    type=str,
    default=",".join(map(str, class_by_freq.DEFAULT_THRESHOLDS)),
    help="Whether to filter to rows with HPO terms (default: true)",
)
@click.pass_context
def acmg_class_by_freq(ctx: click.Context, input_file: str, output_file: str, thresholds: str):
    """Create links between gene and phenotype."""
    _ = ctx
    thresholds_float = list(map(float, thresholds.split(",")))
    class_by_freq.run_report(input_file, output_file, thresholds=thresholds_float)


@data.command("extract-vars")
@click.argument("path_input")
@click.argument("path_output_dir")
@click.option(
    "--gzip-output/--no-gzip-output", default=True, help="Whether to gzip output (default: true)"
)
@click.pass_context
def cli_extract_vars(ctx: click.Context, path_input: str, path_output_dir: str, gzip_output: bool):
    """Write out variants from RCV records."""
    _ = ctx
    extract_vars.run(path_input, path_output_dir, gzip_output)
