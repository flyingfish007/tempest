
from tempest.api.compute import base
from tempest import test

class ClustersTestJSON(base.BaseV2ComputeAdminTest):

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