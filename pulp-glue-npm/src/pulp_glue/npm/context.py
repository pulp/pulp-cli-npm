from pulp_glue.common.context import (
    PluginRequirement,
    PulpContentContext,
    PulpDistributionContext,
    PulpRemoteContext,
    PulpRepositoryContext,
    PulpRepositoryVersionContext,
)
from pulp_glue.common.i18n import get_translation

translation = get_translation(__package__)
_ = translation.gettext


class PulpNpmPackageContentContext(PulpContentContext):
    PLUGIN = "npm"
    RESOURCE_TYPE = "package"
    ENTITY = _("npm package")
    ENTITIES = _("npm packages")
    HREF = "npm_package_href"
    ID_PREFIX = "content_npm_packages"
    NEEDS_PLUGINS = [PluginRequirement("npm", specifier=">=0.1.0")]
    CAPABILITIES = {"upload": []}


class PulpNpmDistributionContext(PulpDistributionContext):
    PLUGIN = "npm"
    RESOURCE_TYPE = "npm"
    ENTITY = _("npm distribution")
    ENTITIES = _("npm distributions")
    HREF = "npm_npm_distribution_href"
    ID_PREFIX = "distributions_npm_npm"
    NEEDS_PLUGINS = [PluginRequirement("npm", specifier=">=0.1.0")]


class PulpNpmRemoteContext(PulpRemoteContext):
    PLUGIN = "npm"
    RESOURCE_TYPE = "npm"
    ENTITY = _("npm remote")
    ENTITIES = _("npm remotes")
    HREF = "npm_npm_remote_href"
    ID_PREFIX = "remotes_npm_npm"
    NEEDS_PLUGINS = [PluginRequirement("npm", specifier=">=0.1.0")]


class PulpNpmRepositoryVersionContext(PulpRepositoryVersionContext):
    HREF = "npm_npm_repository_version_href"
    ID_PREFIX = "repositories_npm_npm_versions"
    NEEDS_PLUGINS = [PluginRequirement("npm", specifier=">=0.1.0")]


class PulpNpmRepositoryContext(PulpRepositoryContext):
    PLUGIN = "npm"
    RESOURCE_TYPE = "npm"
    HREF = "npm_npm_repository_href"
    ENTITY = _("npm repository")
    ENTITIES = _("npm repositories")
    ID_PREFIX = "repositories_npm_npm"
    VERSION_CONTEXT = PulpNpmRepositoryVersionContext
    CAPABILITIES = {
        "sync": [PluginRequirement("npm")],
    }
    NULLABLES = PulpRepositoryContext.NULLABLES | {"remote"}
    NEEDS_PLUGINS = [PluginRequirement("npm", specifier=">=0.1.0")]
