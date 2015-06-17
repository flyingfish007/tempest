
import json

from tempest.api_schema.response.compute.v2_1 import clusters as schema
from tempest.common import service_client

class ClustersClientJSON(service_client.ServiceClient):

    def list_clusters(self, params=None):
        url = "clusters"

        resp, body = self.get(url)
        body = json.loads(body)
        self.validate_response(schema.list_clusters, resp, body)
        return service_client.ResponseBodyList(resp, body['clusters'])