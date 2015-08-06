# Copyright 2012 OpenStack Foundation
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import time

from oslo_log import log as logging
from oslo_utils import excutils
from tempest_lib.common.utils import data_utils

from tempest.common import fixed_network
from tempest import config
from tempest import exceptions
import tempest.test

CONF = config.CONF

LOG = logging.getLogger(__name__)


class BaseVSMTest(tempest.test.BaseTestCase):
    """Base test case class for all Compute API tests."""

    _api_version = 2

    credentials = ['primary']

    @classmethod
    def skip_checks(cls):
        super(BaseVSMTest, cls).skip_checks()
        if cls._api_version != 2:
            msg = ("Unexpected API version is specified (%s)" %
                   cls._api_version)
            raise exceptions.InvalidConfiguration(message=msg)

    @classmethod
    def setup_credentials(cls):
        cls.set_network_resources()
        super(BaseVSMTest, cls).setup_credentials()

    @classmethod
    def setup_clients(cls):
        super(BaseVSMTest, cls).setup_clients()
        cls.servers_client = cls.os.clusters_client

    @classmethod
    def resource_setup(cls):
        super(BaseVSMTest, cls).resource_setup()

    @classmethod
    def resource_cleanup(cls):
        super(BaseVSMTest, cls).resource_cleanup()

    @classmethod
    def create_test_server(cls, **kwargs):
        """Wrapper utility that returns a test server."""
        name = data_utils.rand_name(cls.__name__ + "-instance")
        if 'name' in kwargs:
            name = kwargs.pop('name')
        flavor = kwargs.get('flavor', cls.flavor_ref)
        image_id = kwargs.get('image_id', cls.image_ref)

        kwargs = fixed_network.set_networks_kwarg(
            cls.get_tenant_network(), kwargs) or {}
        body = cls.servers_client.create_server(
            name, image_id, flavor, **kwargs)

        # handle the case of multiple servers
        servers = [body]
        if 'min_count' in kwargs or 'max_count' in kwargs:
            # Get servers created which name match with name param.
            b = cls.servers_client.list_servers()
            servers = [s for s in b['servers'] if s['name'].startswith(name)]

        if 'wait_until' in kwargs:
            for server in servers:
                try:
                    cls.servers_client.wait_for_server_status(
                        server['id'], kwargs['wait_until'])
                except Exception:
                    with excutils.save_and_reraise_exception():
                        if ('preserve_server_on_error' not in kwargs
                            or kwargs['preserve_server_on_error'] is False):
                            for server in servers:
                                try:
                                    cls.servers_client.delete_server(
                                        server['id'])
                                except Exception:
                                    pass

        cls.servers.extend(servers)

        return body

    def wait_for(self, condition):
        """Repeatedly calls condition() until a timeout."""
        start_time = int(time.time())
        while True:
            try:
                condition()
            except Exception:
                pass
            else:
                return
            if int(time.time()) - start_time >= self.build_timeout:
                condition()
                return
            time.sleep(self.build_interval)


class BaseV2VSMTest(BaseVSMTest):
    _api_version = 2


class BaseVSMAdminTest(BaseVSMTest):
    """Base test case class for VSM Admin API tests."""

    credentials = ['primary', 'admin']

    @classmethod
    def setup_clients(cls):
        super(BaseVSMAdminTest, cls).setup_clients()


class BaseV2VSMAdminTest(BaseVSMAdminTest):
    """Base test case class for VSM Admin V2 API tests."""
    _api_version = 2
