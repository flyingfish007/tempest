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

LOG = log.getLogger(__name__)


class AppnodessTestJSON(base.BaseVSMAdminTest):

    """

    Tests appnodes API using admin privileges.
    """

    @classmethod
    def setup_clients(cls):
        super(AppnodessTestJSON, cls).setup_clients()
        cls.appnodes_client = cls.os_adm.vsm_appnodes_client

    @classmethod
    def resource_setup(cls):
        super(AppnodessTestJSON, cls).resource_setup()

    @test.idempotent_id('6e475cbf-5852-4473-a73b-28b29e83d630')
    def test_list_appnodes(self):
        body = self.appnodes_client.list_appnodes()
        appnodes = body['appnodes']
        LOG.info("=============appnodes: " + str(appnodes))
        self.assertTrue(len(appnodes) != 0, str(appnodes))
