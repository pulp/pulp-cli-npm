import typing as t

import click
from pulp_cli.generic import (
    PulpCLIContext,
    chunk_size_option,
    href_option,
    list_command,
    pass_entity_context,
    pass_pulp_context,
    pulp_group,
    resource_option,
    show_command,
)

from pulp_glue.common.context import PulpEntityContext, PulpRepositoryContext
from pulp_glue.common.i18n import get_translation
from pulp_glue.npm.context import PulpNpmPackageContentContext, PulpNpmRepositoryContext

translation = get_translation(__package__)
_ = translation.gettext


repository_option = resource_option(
    "--repository",
    default_plugin="npm",
    default_type="npm",
    context_table={
        "npm:npm": PulpNpmRepositoryContext,
    },
    href_pattern=PulpRepositoryContext.HREF_PATTERN,
    help=_(
        "Repository to add the content to in the form '[[<plugin>:]<resource_type>:]<name>' or by "
        "href."
    ),
)


@pulp_group()
@click.option(
    "-t",
    "--type",
    "content_type",
    type=click.Choice(["package"], case_sensitive=False),
    default="package",
)
@pass_pulp_context
@click.pass_context
def content(ctx: click.Context, pulp_ctx: PulpCLIContext, /, content_type: str) -> None:
    if content_type == "package":
        ctx.obj = PulpNpmPackageContentContext(pulp_ctx)
    else:
        raise NotImplementedError()


lookup_options = [href_option]

content.add_command(
    list_command(
        decorators=[
            click.option("--name"),
            click.option("--version"),
        ]
    )
)
content.add_command(show_command(decorators=lookup_options))


@content.command()
@click.option("--file", type=click.File("rb"), required=True)
@chunk_size_option
@repository_option
@pass_entity_context
@pass_pulp_context
def upload(
    pulp_ctx: PulpCLIContext,
    entity_ctx: PulpEntityContext,
    /,
    file: t.IO[bytes],
    chunk_size: int,
    repository: PulpRepositoryContext | None,
) -> None:
    """Upload an npm package."""
    assert isinstance(entity_ctx, PulpNpmPackageContentContext)

    result = entity_ctx.upload(file=file, chunk_size=chunk_size, repository=repository)
    pulp_ctx.output_result(result)
