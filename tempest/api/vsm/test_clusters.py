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


class ClustersTestJSON(base.BaseVSMAdminTest):

    """

    Tests clusters API using admin privileges.
    """

    OK_STATUS = [200, 202]

    @classmethod
    def setup_clients(cls):
        super(ClustersTestJSON, cls).setup_clients()
        cls.clusters_client = cls.os_adm.vsm_clusters_client
        cls.servers_client = cls.os_adm.vsm_servers_client

    @test.idempotent_id('b69103ea-56a8-4410-9484-aa940e4bd276')
    def test_create_clusters(self):
        resp, body = self.clusters_client.create_cluster()
        status = resp['status']
        LOG.info("==========body: " + str(body))
        LOG.info("==========status: " + status)
        self.assertIn(int(status), self.OK_STATUS)
        servers_body = self.servers_client.list_servers()
        servers = servers_body['servers']
        LOG.info("=============servers: " + str(servers))


    @test.idempotent_id('087acd2f-ce75-48e4-9b0b-a82c9ae57578')
    def test_list_clusters(self):
        body = self.clusters_client.list_clusters()
        clusters = body['clusters']
        LOG.info("=============clusters: " + str(clusters))
        self.assertTrue(len(clusters) == 1, str(clusters))