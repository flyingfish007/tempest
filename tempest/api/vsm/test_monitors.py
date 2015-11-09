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
from tempest import config

LOG = log.getLogger(__name__)

CONF = config.CONF


class MonitorsTestJSON(base.BaseVSMAdminTest):

    """

    Tests monitors API using admin privileges.
    Monitor Rest API function:
        list                get
        summary             get
        restart             post
    """

    OK_STATUS = [200, 202]

    @classmethod
    def setup_clients(cls):
        super(MonitorsTestJSON, cls).setup_clients()
        cls.monitors_client = cls.os_adm.vsm_monitors_client

    @classmethod
    def resource_setup(cls):
        super(MonitorsTestJSON, cls).resource_setup()

    @test.idempotent_id('6cc59839-8852-4dfa-ab23-d9fda089eec0')
    def test_list_monitors(self):
        resp, body = self.monitors_client.list_monitors()
        status = resp['status']
        # TODO wish better than this assert
        self.assertIn(int(status), self.OK_STATUS)
        monitors = body['monitors']
        # TODO wish better than this assert
        self.assertEqual(len(monitors) > 1, True)

    @test.idempotent_id('608a96dc-5a90-4dd6-8ee3-6b8d9dc24eca')
    def test_summary_monitor(self):
        resp, body = self.monitors_client.summary_monitor()
        status = resp['status']
        # TODO wish better than this assert
        self.assertIn(int(status), self.OK_STATUS)

    @test.idempotent_id('bdee5e19-4a4e-45b8-9343-9ac1748eeaf4')
    def test_restart_monitor(self):
        resp, body = self.monitors_client.list_monitors()
        monitors = body['monitors']
        random_num = random.randint(0, len(monitors) - 1)
        monitor = monitors[random_num]
        monitor_id = monitor['id']
        resp, body = self.monitors_client.restart_monitor(monitor_id)
        status = resp['status']
        # TODO wish better than this assert
        self.assertIn(int(status), self.OK_STATUS)