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

from tempest.api_schema.response.vsm.v2_0 import clusters as schema
from tempest.common import service_client


class ClustersClient(service_client.ServiceClient):

    def create_cluster(self, params=None):
        post_body = json.dumps(
            {"is_storage": 1, "is_monitor": 1, "id": "1"},
            {"is_storage": 1, "is_monitor": 1, "id": "2"},
            {"is_storage": 1, "is_monitor": 1, "id": "3"}
        )
        resp, body = self.post("clusters", post_body)
        print(resp, body)

    def list_clusters(self, params=None):
        url = "clusters"

        resp, body = self.get(url)
        body = json.loads(body)
        self.validate_response(schema.list_clusters, resp, body)
        return service_client.ResponseBodyList(resp, body['clusters'])