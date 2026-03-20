import typing as t

import click
from pulp_cli.generic import pulp_group

from pulp_glue.common.i18n import get_translation

from pulpcore.cli.npm.content import content
from pulpcore.cli.npm.distribution import distribution
from pulpcore.cli.npm.remote import remote
from pulpcore.cli.npm.repository import repository

translation = get_translation(__package__)
_ = translation.gettext

__version__ = "0.0.1"


@pulp_group(name="npm")
def npm_group() -> None:
    pass


def mount(main: click.Group, **kwargs: t.Any) -> None:
    npm_group.add_command(content)
    npm_group.add_command(distribution)
    npm_group.add_command(remote)
    npm_group.add_command(repository)
    main.add_command(npm_group)
