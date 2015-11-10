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
import random

from tempest.api.vsm import base
from tempest import test

LOG = log.getLogger(__name__)


class DevicesTestJSON(base.BaseVSMAdminTest):
    """

    Tests devices API using admin privileges.
    Device Rest API function:
        list                    get
        get_available_disks     get
        get_smart_info          get
    """

    OK_STATUS = [200, 202]

    @classmethod
    def setup_clients(cls):
        super(DevicesTestJSON, cls).setup_clients()
        cls.devices_client = cls.os_adm.vsm_devices_client
        cls.servers_client = cls.os_adm.vsm_servers_client

    @classmethod
    def resource_setup(cls):
        super(DevicesTestJSON, cls).resource_setup()

    @test.idempotent_id('e795ce77-c3d1-41d5-8b24-e67d8518ff1d')
    def test_list_devices(self):
        resp, body = self.devices_client.list_devices()
        status = resp['status']
        # TODO wish better than this assert
        self.assertIn(int(status), self.OK_STATUS)
        devices = body['devices']
        # TODO wish better than this assert
        self.assertEqual(len(devices) >= 3, True)

    @test.idempotent_id('f6497572-7c49-433e-a443-63ac4bc8923c')
    def test_get_available_disks(self):
        servers_body = self.servers_client.list_servers()
        servers = servers_body['servers']
        random_num = random.randint(0, len(servers) - 1)
        server = servers[random_num]
        server_id = server['id']
        resp, body = self.devices_client.get_available_disks(
            {
                # "result_mode": "get_disks",
                "server_id": server_id
            }
        )
        status = resp['status']
        # TODO wish better than this assert
        self.assertIn(int(status), self.OK_STATUS)
        # availables_disks = body['available_disks']
        # TODO wish better than this assert
        # self.assertEqual(len(availables_disks) > 1, True)

    # TODO test get smart info
    @test.idempotent_id('6f97d20b-ff65-4fd2-aa0a-bc72506e6a2b')
    def test_get_smart_info(self):
        self.assertEqual(True, True)