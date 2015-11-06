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


class ClustersTestJSON(base.BaseVSMAdminTest):

    """

    Tests clusters API using admin privileges.
    Cluster Rest API function:
        create              post
        list                get
        summary             get
        refresh             post
        import_ceph_conf    post
        integrate           post
        stop_cluster        post
        start_cluster       post
    """

    OK_STATUS = [200, 202]

    @classmethod
    def setup_clients(cls):
        super(ClustersTestJSON, cls).setup_clients()
        cls.clusters_client = cls.os_adm.vsm_clusters_client
        cls.servers_client = cls.os_adm.vsm_servers_client

    @classmethod
    def resource_setup(cls):
        super(ClustersTestJSON, cls).resource_setup()

    @test.idempotent_id('b69103ea-56a8-4410-9484-aa940e4bd276')
    def test_create_clusters(self):
        result = self.check_vsm_cluster_exist()
        if result == "yes":
            self.assertEqual(True, True)
            return
        resp, body = self.clusters_client.create_cluster()
        status = resp['status']
        LOG.info("==========body: " + str(body))
        LOG.info("==========status: " + status)
        self.assertIn(int(status), self.OK_STATUS)
        servers_body = self.servers_client.list_servers()
        servers = servers_body['servers']
        LOG.info("=============servers: " + str(servers))
        active_servers_num = 0
        for server in servers:
            final_status = waiters.wait_for_vsm_server_status(
                self.servers_client, server['id'], "Active"
            )
            if final_status == "Active":
                active_servers_num = active_servers_num + 1
        self.assertEqual(active_servers_num >= 3, True)

    @test.idempotent_id('087acd2f-ce75-48e4-9b0b-a82c9ae57578')
    def test_list_clusters(self):
        # TODO the rest api of list cluster is hardcode
        resp, body = self.clusters_client.list_clusters()
        status = resp['status']
        self.assertIn(int(status), self.OK_STATUS)
        clusters = body['clusters']
        LOG.info("=============clusters: " + str(clusters))
        self.assertTrue(len(clusters) == 1, str(clusters))

    @test.idempotent_id('46be542c-8c44-4896-a362-fd5242620a0f')
    def test_cluster_summary(self):
        resp, body = self.clusters_client.summary_cluster()
        status = resp['status']
        # TODO wish better than this assert
        self.assertIn(int(status), self.OK_STATUS)

    @test.idempotent_id('4f075ad4-8d8b-4afc-a773-65891abc3251')
    def test_refresh_cluster(self):
        resp, body = self.clusters_client.refresh_cluster()
        status = resp['status']
        # TODO wish better than this assert
        self.assertIn(int(status), self.OK_STATUS)

    @test.idempotent_id('121ad650-5d4b-4669-b07f-3fbafecff371')
    def test_import_ceph_conf(self):
        # TODO not implemented
        self.assertEqual(True, True)

    @test.idempotent_id('b882e5ff-2820-4d8f-85cf-d79f80026816')
    def test_integrate_cluster(self):
        # TODO not implemented
        self.assertEqual(True, True)

    @test.idempotent_id('188d2113-29dc-41e9-b60e-87ec14a63c44')
    def test_stop_cluster(self):
        # TODO not implemented
        self.assertEqual(True, True)

    @test.idempotent_id('e2aa865b-ecd6-4acb-bd33-be69b928762f')
    def test_start_cluster(self):
        # TODO not implemented
        self.assertEqual(True, True)
