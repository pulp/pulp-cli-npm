import typing as t

import click

from pulp_glue.common.context import (
    EntityFieldDefinition,
    PulpRemoteContext,
    PulpRepositoryContext,
)
from pulp_glue.common.i18n import get_translation
from pulp_glue.npm.context import (
    PulpNpmPackageContentContext,
    PulpNpmRemoteContext,
    PulpNpmRepositoryContext,
)

from pulp_cli.generic import (
    PulpCLIContext,
    create_command,
    destroy_command,
    href_option,
    label_command,
    label_select_option,
    list_command,
    name_option,
    pass_pulp_context,
    pass_repository_context,
    pulp_group,
    pulp_labels_option,
    repository_content_command,
    repository_href_option,
    repository_lookup_option,
    resource_option,
    retained_versions_option,
    role_command,
    show_command,
    update_command,
    version_command,
)

translation = get_translation(__package__)
_ = translation.gettext


remote_option = resource_option(
    "--remote",
    default_plugin="npm",
    default_type="npm",
    context_table={"npm:npm": PulpNpmRemoteContext},
    href_pattern=PulpRemoteContext.HREF_PATTERN,
    help=_("Remote used for syncing in the form '[[<plugin>:]<resource_type>:]<name>' or by href."),
)


@pulp_group()
@click.option(
    "-t",
    "--type",
    "repo_type",
    type=click.Choice(["npm"], case_sensitive=False),
    default="npm",
)
@pass_pulp_context
@click.pass_context
def repository(ctx: click.Context, pulp_ctx: PulpCLIContext, /, repo_type: str) -> None:
    if repo_type == "npm":
        ctx.obj = PulpNpmRepositoryContext(pulp_ctx)
    else:
        raise NotImplementedError()


lookup_options = [href_option, name_option, repository_lookup_option]
nested_lookup_options = [repository_href_option, repository_lookup_option]
update_options = [
    click.option("--description"),
    remote_option,
    retained_versions_option,
    pulp_labels_option,
]
create_options = update_options + [click.option("--name", required=True)]

repository.add_command(
    list_command(
        decorators=[label_select_option, click.option("--name-startswith", "name__startswith")]
    )
)
repository.add_command(show_command(decorators=lookup_options))
repository.add_command(create_command(decorators=create_options))
repository.add_command(update_command(decorators=lookup_options + update_options))
repository.add_command(destroy_command(decorators=lookup_options))
repository.add_command(version_command(decorators=nested_lookup_options))
repository.add_command(label_command(decorators=nested_lookup_options))
repository.add_command(
    repository_content_command(
        contexts={"npm.package": PulpNpmPackageContentContext},
    )
)
repository.add_command(role_command(decorators=lookup_options))


@repository.command()
@name_option
@href_option
@repository_lookup_option
@remote_option
@click.option(
    "--mirror/--no-mirror",
    default=None,
)
@pass_repository_context
def sync(
    repository_ctx: PulpRepositoryContext,
    /,
    remote: EntityFieldDefinition,
    mirror: bool | None,
) -> None:
    """Sync the repository from a remote source."""
    body: dict[str, t.Any] = {}
    repository = repository_ctx.entity
    if mirror is not None:
        body["mirror"] = mirror

    if remote:
        body["remote"] = remote
    elif repository["remote"] is None:
        raise click.ClickException(
            _(
                "Repository '{name}' does not have a default remote. "
                "Please specify with '--remote'."
            ).format(name=repository["name"])
        )

    repository_ctx.sync(body=body)
