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


class PlacementGroupsTestJSON(base.BaseVSMAdminTest):

    """

    Tests placement_groups API using admin privileges.
    Placement_group Rest API function:
        list            get
        summary         get
    """

    OK_STATUS = [200, 202]

    @classmethod
    def setup_clients(cls):
        super(PlacementGroupsTestJSON, cls).setup_clients()
        cls.placement_groups_client = \
            cls.os_adm.vsm_placement_groups_client

    @classmethod
    def resource_setup(cls):
        super(PlacementGroupsTestJSON, cls).resource_setup()

    @test.idempotent_id('ba9e89bb-8ec2-40a5-a538-5117f5bed2d5')
    def test_list_placement_groups(self):
        resp, body = self.placement_groups_client.list_placement_groups()
        status = resp['status']
        # TODO wish better than this assert
        self.assertIn(int(status), self.OK_STATUS)

    @test.idempotent_id('0834e65d-2f52-4ec9-b6a1-d32a8307f8f9')
    def test_summary_placement_group(self):
        resp, body = self.placement_groups_client.summary_placement_group()
        status = resp['status']
        # TODO wish better than this assert
        self.assertIn(int(status), self.OK_STATUS)