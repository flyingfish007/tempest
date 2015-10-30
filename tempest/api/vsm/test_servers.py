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

from oslo_log import log

from tempest.api.vsm import base
from tempest import test
from tempest import config

LOG = log.getLogger(__name__)

CONF = config.CONF


class ServersTestJSON(base.BaseVSMAdminTest):

    """

    Test servers API using admin privileges.
    """

    @classmethod
    def setup_clients(cls):
        super(ServersTestJSON, cls).setup_clients()
        cls.servers_client = cls.os_adm.vsm_servers_client

    @test.idempotent_id('741909c5-9523-42c4-8f59-ba4096e4b9fc')
    def test_list_servers(self):
        body = self.servers_client.list_servers()
        servers = body['servers']
        LOG.info("=============servers: " + str(servers))
        servers_from_conf  = CONF.vsm.servers_name
        self.assertEqual(len(servers) == len(servers_from_conf) - 1, True)