# Copyright 2014 NEC Corporation.
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

import json
from oslo_log import log

from tempest.api_schema.response.vsm.v2_0 import clusters as schema
from tempest.common import service_client
from tempest import config

LOG = log.getLogger(__name__)

CONF = config.CONF


class ClustersClient(service_client.ServiceClient):

    def create_cluster(self, params=None):
        servers = CONF.vsm.servers_name
        servers_list = []
        while len(servers)  > 1:
            servers_list.append(
                {
                    "is_storage": True,
                    "is_monitor": True,
                    "id": len(servers) - 1
                }
            )
            servers.pop()

        post_body = json.dumps(
            {
                "cluster": {
                    "name": "default",
                    "file_system": "xfs",
                    "journal_size": None,
                    "size": None,
                    "management_network": None,
                    "ceph_public_network": None,
                    "cluster_network": None,
                    "primary_public_netmask": None,
                    "secondary_public_netmask": None,
                    "cluster_netmask": None,
                    "servers": servers_list
                }
            }
        )
        # LOG.info("post_body create_cluster============" + str(post_body))
        resp, body = self.post("clusters", post_body)
        self.validate_response(schema.create_cluster, resp, body)
        # TODO return
        return resp, service_client.ResponseBody(resp, body)

    # TODO the return is hardcode
    def list_clusters(self, params=None):
        url = "clusters"
        resp, body = self.get(url)
        body = json.loads(body)
        self.validate_response(schema.list_clusters, resp, body)
        # TODO return
        return resp, service_client.ResponseBody(resp, body)

    def summary_cluster(self):
        url = "clusters/summary"
        resp, body = self.get(url)
        body = json.loads(body)
        self.validate_response(schema.summary_cluster, resp, body)
        # TODO return
        return resp, service_client.ResponseBody(resp, body['cluster-summary'])

    def refresh_cluster(self):
        url = "clusters/refresh"
        resp, body = self.post(url, {})
        self.validate_response(schema.refresh_cluster, resp, body)
        # TODO return
        return resp, service_client.ResponseBody(resp, body)

    def import_ceph_conf(self, **kwargs):
        cluster_name = kwargs.get('cluster_name', None)
        ceph_conf_path = kwargs.get('ceph_conf_path', None)
        post_body = json.dumps({
            'cluster': {
                'cluster_name': cluster_name,
                'ceph_conf_path': ceph_conf_path
            }
        })

        url = "clusters/import_ceph_conf"
        resp, body = self.post(url, post_body)
        body = json.loads(body)
        self.validate_response(schema.import_ceph_conf, resp, body)
        # TODO return
        return service_client.ResponseBody(resp, body)

    def integrate_cluster(self):
        # TODO integrate cluster function
        return

    def stop_cluster(self, cluster_id):
        post_body = json.dumps({
            'cluster': {
                'id': cluster_id
            }
        })
        url = "clusters/stop_cluster"
        resp, body = self.post(url, post_body)
        body = json.loads(body)
        self.validate_response(schema.stop_cluster, resp, body)
        # TODO retrun
        return service_client.ResponseBody(resp, body)

    def start_cluster(self, cluster_id):
        post_body = json.dumps({
            'cluster': {
                'id': cluster_id
            }
        })
        url = "clusters/start_cluster"
        resp, body = self.post(url, post_body)
        body = json.loads(body)
        self.validate_response(schema.start_cluster, resp, body)
        # TODO return
        return service_client.ResponseBody(resp, body)