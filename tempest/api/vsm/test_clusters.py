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

from tempest.api.vsm import base
from tempest import test

class ClustersTestJSON(base.BaseV2VSMAdminTest):

    """
    Tests clusters API using admin privileges.
    """

    @classmethod
    def setup_clients(cls):
        super(ClustersTestJSON, cls).setup_clients()
        cls.client = cls.os_adm.clusters_client

    @test.idempotent_id('087acd2f-ce75-48e4-9b0b-a82c9ae57578')
    def test_list_clusters(self):
        clusters = self.client.list_clusters()
        self.assertTrue(len(clusters) == 1, str(clusters))