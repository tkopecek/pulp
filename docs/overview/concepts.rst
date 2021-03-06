Concepts and Terminology
========================

This introduction presents a high level overview of Pulp terminology and concepts. It is designed
to be understandable to anyone who is familiar with software management even without prior
knowledge of Pulp. This document favors clarity and accuracy over ease of reading.

From a user’s perspective Pulp is a tool to manage their content. In this context, “Pulp” refers to
“pulpcore and one or more plugins”. Because of its dependent relationship with plugins, pulpcore
can be described as a framework for plugin development.

:term:`pulpcore` is a generalized backend with a REST API and a plugin API. Users will need at
least one :term:`plugin` to manage :term:`content`.  Each :term:`type` of content unit (like rpm or
deb) is defined by a plugin.  Files that belong to a content unit are called
:term:`artifacts<artifact>`. Each content unit can have 0 or many artifacts and artifacts can be
shared by multiple content units.

Content units in Pulp are organized by their membership in :term:`repositories<repository>` over
time. Plugin users can add or remove content units to a repository. Each time the content set of a
repository is changed, a new :term:`repository version<RepositoryVersion>` is created.

Users can inform Pulp about external sources of content units, called :term:`remotes<remote>`.
Plugins can define actions to interact with those sources. For example, most or all plugins define
:term:`sync` to fetch content units from a remote and add them to a repository.

All content that is managed by Pulp can be hosted by the :term:`content app`. Users create
type-specific :term:`publishers<publisher>` that provide the settings necessary to generate
a :term:`publication` for a content set in a repository version. A publication consists of the
metadata of the content set and the artifacts of each content unit in the content set. To host a
publication, it must be assigned to a :term:`distribution`, which determines how and where a
publication is served.
