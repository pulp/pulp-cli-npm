import click

from pulp_glue.common.i18n import get_translation
from pulp_glue.npm.context import (
    PulpNpmDistributionContext,
    PulpNpmRepositoryContext,
)

from pulp_cli.generic import (
    PulpCLIContext,
    common_distribution_create_options,
    content_guard_option,
    create_command,
    destroy_command,
    distribution_filter_options,
    distribution_lookup_option,
    href_option,
    label_command,
    list_command,
    name_option,
    pass_pulp_context,
    pulp_group,
    pulp_labels_option,
    resource_option,
    role_command,
    show_command,
    update_command,
)

translation = get_translation(__package__)
_ = translation.gettext


repository_option = resource_option(
    "--repository",
    default_plugin="npm",
    default_type="npm",
    context_table={"npm:npm": PulpNpmRepositoryContext},
    href_pattern=PulpNpmRepositoryContext.HREF_PATTERN,
    help=_(
        "Repository to be used for auto-distributing."
        " Specified as '[[<plugin>:]<type>:]<name>' or as href."
    ),
)


@pulp_group()
@click.option(
    "-t",
    "--type",
    "distribution_type",
    type=click.Choice(["npm"], case_sensitive=False),
    default="npm",
)
@pass_pulp_context
@click.pass_context
def distribution(
    ctx: click.Context, pulp_ctx: PulpCLIContext, /, distribution_type: str
) -> None:
    if distribution_type == "npm":
        ctx.obj = PulpNpmDistributionContext(pulp_ctx)
    else:
        raise NotImplementedError()


lookup_options = [href_option, name_option, distribution_lookup_option]
nested_lookup_options = [distribution_lookup_option]
update_options = [
    repository_option,
    content_guard_option,
    pulp_labels_option,
]
create_options = common_distribution_create_options + update_options

distribution.add_command(list_command(decorators=distribution_filter_options))
distribution.add_command(show_command(decorators=lookup_options))
distribution.add_command(create_command(decorators=create_options))
distribution.add_command(
    update_command(decorators=lookup_options + update_options + [click.option("--base-path")])
)
distribution.add_command(destroy_command(decorators=lookup_options))
distribution.add_command(label_command(decorators=nested_lookup_options))
distribution.add_command(role_command(decorators=lookup_options))
