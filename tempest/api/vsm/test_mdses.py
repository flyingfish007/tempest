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
from tempest.common import waiters

LOG = log.getLogger(__name__)

CONF = config.CONF


class MdsesTestJSON(base.BaseVSMAdminTest):

    """

    Tests mdses API using admin privileges.
    Mds Rest API function:
        list                get
        summary             get
    """

    OK_STATUS = [200, 202]

    @classmethod
    def setup_clients(cls):
        super(MdsesTestJSON, cls).setup_clients()
        cls.mdses_client = cls.os_adm.vsm_mdses_client

    @classmethod
    def resource_setup(cls):
        super(MdsesTestJSON, cls).resource_setup()

    @test.idempotent_id('511f819d-c09e-42a3-ac67-75ca5cd14847')
    def test_list_mdses(self):
        resp, body = self.mdses_client.list_mdses()
        status = resp['status']
        self.assertIn(int(status), self.OK_STATUS)
        mdses = body['mdses']
        # TODO wish better than this assert
        self.assertEqual(len(mdses) >= 0, True)

    @test.idempotent_id('9456a658-499e-418e-bef0-60350997b6b6')
    def test_summary_mds(self):
        resp, body = self.mdses_client.summary_mds()
        status = resp['status']
        # TODO wish better than this assert
        self.assertIn(int(status), self.OK_STATUS)