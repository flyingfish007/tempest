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

LOG = log.getLogger(__name__)


class ClustersClient(service_client.ServiceClient):

    def create_cluster(self, params=None):
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
                    "servers": [
                        {"is_storage": True, "is_monitor": True, "id": "1"},
                        {"is_storage": True, "is_monitor": True, "id": "2"},
                        {"is_storage": True, "is_monitor": True, "id": "3"}
                    ]
                }
            }
        )
        resp, body = self.post("clusters", post_body)
        LOG.info("++++++++++++" + str(resp))
        LOG.info("++++++++++++" + str(body))
        self.validate_response(schema.create_cluster, resp, body)
        return service_client.ResponseBody(resp, body)

    def list_clusters(self, params=None):
        url = "clusters"

        resp, body = self.get(url)
        LOG.info("++++++++++++" + str(resp))
        LOG.info("++++++++++++" + str(body))
        body = json.loads(body)
        self.validate_response(schema.list_clusters, resp, body)
        return service_client.ResponseBodyList(resp, body['clusters'])