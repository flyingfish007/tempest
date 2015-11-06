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
    Server Rest API function:
        get             get
        list            get
        add             post
        remove          post
        reset_status    post
        start           post
        stop            post
        ceph_upgrade    post
    """

    @classmethod
    def setup_clients(cls):
        super(ServersTestJSON, cls).setup_clients()
        cls.servers_client = cls.os_adm.vsm_servers_client

    @classmethod
    def resource_setup(cls):
        super(ServersTestJSON, cls).resource_setup()

    @test.idempotent_id('f8aeb7c1-b050-4f5c-86b2-14071153731e')
    def test_get_server(self):
        # TODO not implemented
        self.assertEqual(True, True)

    @test.idempotent_id('741909c5-9523-42c4-8f59-ba4096e4b9fc')
    def test_list_servers(self):
        body = self.servers_client.list_servers()
        servers = body['servers']
        LOG.info("=============servers: " + str(servers))
        servers_from_conf  = CONF.vsm.servers_name
        self.assertEqual(len(servers) == len(servers_from_conf) - 1, True)

    @test.idempotent_id('e6d4f819-c2e4-4308-b7a6-43e48c80c701')
    def test_add_server(self):
        # TODO not implemented
        self.assertEqual(True, True)

    @test.idempotent_id('89d81df0-18d5-4c5d-b27e-9fd13eb31b84')
    def test_remove_server(self):
        # TODO not implemented
        self.assertEqual(True, True)

    @test.idempotent_id('bc09fca7-df4b-4a7f-b15c-ac59222933c6')
    def test_reset_server_status(self):
        # TODO not implemented
        self.assertEqual(True, True)

    @test.idempotent_id('877a8b02-38d6-4746-976f-ef5c309df382')
    def test_start_server(self):
        # TODO not implemented
        self.assertEqual(True, True)

    @test.idempotent_id('48cdfc18-2216-4776-bc58-81f4f838b002')
    def test_stop_server(self):
        # TODO not implemented
        self.assertEqual(True, True)

    @test.idempotent_id('330a0d01-af53-4f64-9885-804dd0044137')
    def test_ceph_upgrade(self):
        # TODO not implemented
        self.assertEqual(True, True)