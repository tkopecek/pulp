# -*- coding: utf-8 -*-
#
# Copyright © 2011 Red Hat, Inc.
#
# This software is licensed to you under the GNU General Public
# License as published by the Free Software Foundation; either version
# 2 of the License (GPLv2) or (at your option) any later version.
# There is NO WARRANTY for this software, express or implied,
# including the implied warranties of MERCHANTABILITY,
# NON-INFRINGEMENT, or FITNESS FOR A PARTICULAR PURPOSE. You should
# have received a copy of GPLv2 along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.

"""
Contains (proxy) classes that represent the pulp agent.
"""

from logging import getLogger

from gofer.proxy import Agent

from pulp.server.agent.direct.services import Services


log = getLogger(__name__)


# --- Agent ------------------------------------------------------------------

class PulpAgent(object):
    """
    Represents a remote pulp agent.
    """

    @property
    def consumer(self):
        """
        Access to *consumer* capability.
        :return: Consumer API.
        :rtype: Consumer
        """
        return Consumer

    @property
    def content(self):
        """
        Access to *content* capability.
        :return: Content API.
        :rtype: Content
        """
        return Content

    @property
    def profile(self):
        """
        Access to *profile* capability.
        :return: Profile API.
        :rtype: Profile
        """
        return Profile()

    @classmethod
    def status(cls, uuids):
        """
        Get the status of the agent.
        Relies on heartbeat.
        :param uuids: A list of uuids.
        :type uuids: list
        :return: {}
        """
        return Services.heartbeat_listener.status(uuids)

    def cancel(self, context, task_id):
        """
        Cancel an agent request by task ID.
        :param task_id: The ID of a task associated with an agent request.
        :type task_id: str
        """
        criteria = {'match': {'task_id': task_id}}
        agent = Agent(context.uuid, url=context.url, secret=context.secret, async=True)
        admin = agent.Admin()
        admin.cancel(criteria=criteria)


# --- Agent Capabilities -----------------------------------------------------


class Consumer(object):
    """
    The consumer management capability.
    """

    @staticmethod
    def unregistered(context):
        """
        Notification that the consumer has been unregistered.
        Registration artifacts are cleaned up.
        :param context: The call context.
        :type context: pulp.server.agent.direct.context.Context
        :return: The RMI request serial number.
        :rtype: str
        """
        agent = Agent(context.uuid, url=context.url, secret=context.secret, async=True)
        consumer = agent.Consumer()
        return consumer.unregistered()

    @staticmethod
    def bind(context, bindings, options):
        """
        Bind a consumer to the specified repository.
        :param context: The call context.
        :type context: pulp.server.agent.direct.context.Context
        :param bindings: A list of bindings to add/update.
          Each binding is: {type_id:<str>, repo_id:<str>, details:<dict>}
            The 'details' are at the discretion of the distributor.
        :type bindings: list
        :param options: Bind options.
        :type options: dict
        :return: The RMI request serial number.
        :rtype: str
        """
        agent = Agent(
            context.uuid,
            url=context.url,
            timeout=context.get_timeout('bind_timeout'),
            secret=context.secret,
            ctag=context.ctag,
            watchdog=context.watchdog,
            any=context.details)
        consumer = agent.Consumer()
        return consumer.bind(bindings, options)

    @staticmethod
    def unbind(context, bindings, options):
        """
        Unbind a consumer from the specified repository.
        :param context: The call context.
        :type context: pulp.server.agent.direct.context.Context
        :param bindings: A list of bindings to be removed.
          Each binding is: {type_id:<str>, repo_id:<str>}
        :type bindings: list
        :param options: Unbind options.
        :type options: dict
        :return: The RMI request serial number.
        :rtype: str
        """
        agent = Agent(
            context.uuid,
            url=context.url,
            timeout=context.get_timeout('unbind_timeout'),
            secret=context.secret,
            ctag=context.ctag,
            watchdog=context.watchdog,
            any=context.details)
        consumer = agent.Consumer()
        return consumer.unbind(bindings, options)


class Content(object):
    """
    The content management capability.
    """

    @staticmethod
    def install(context, units, options):
        """
        Install content on a consumer.
        :param context: The call context.
        :type context: pulp.server.agent.direct.context.Context
        :param units: A list of content units to be installed.
        :type units: list of:
            { type_id:<str>, unit_key:<dict> }
        :param options: Install options; based on unit type.
        :type options: dict
        :return: The RMI request serial number.
        :rtype: str
        """
        agent = Agent(
            context.uuid,
            url=context.url,
            timeout=context.get_timeout('install_timeout'),
            secret=context.secret,
            ctag=context.ctag,
            watchdog=context.watchdog,
            any=context.details)
        content = agent.Content()
        return content.install(units, options)

    @staticmethod
    def update(context, units, options):
        """
        Update content on a consumer.
        :param context: The call context.
        :type context: pulp.server.agent.direct.context.Context
        :param units: A list of content units to be updated.
        :type units: list of:
            { type_id:<str>, unit_key:<dict> }
        :param options: Update options; based on unit type.
        :type options: dict
        :return: The RMI request serial number.
        :rtype: str
        """
        agent = Agent(
            context.uuid,
            url=context.url,
            timeout=context.get_timeout('update_timeout'),
            secret=context.secret,
            ctag=context.ctag,
            watchdog=context.watchdog,
            any=context.details)
        content = agent.Content()
        return content.update(units, options)

    @staticmethod
    def uninstall(context, units, options):
        """
        Uninstall content on a consumer.
        :param context: The call context.
        :type context: pulp.server.agent.direct.context.Context
        :param units: A list of content units to be uninstalled.
        :type units: list of:
            { type_id:<str>, unit_key:<dict> }
        :param options: Uninstall options; based on unit type.
        :type options: dict
        :return: The RMI request serial number.
        :rtype: str
        """
        agent = Agent(
            context.uuid,
            url=context.url,
            timeout=context.get_timeout('uninstall_timeout'),
            secret=context.secret,
            ctag=context.ctag,
            watchdog=context.watchdog,
            any=context.details)
        content = agent.Content()
        return content.uninstall(units, options)


class Profile(object):
    """
    The profile management capability.
    """

    @staticmethod
    def send(context):
        """
        Request the agent to send the package profile.
        :param context: The call context.
        :type context: pulp.server.agent.direct.context.Context
        :return: The RMI request serial number.
        :rtype: str
        """
        agent = Agent(context.uuid, secret=context.secret)
        profile = agent.Profile()
        return profile.send()
