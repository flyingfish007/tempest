# Copyright 2013 NEC Corporation.
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

from oslo_serialization import jsonutils as json

from tempest.api_schema.response.compute.v2_1 import availability_zone \
    as schema
from tempest.common import service_client


class AvailabilityZoneClient(service_client.ServiceClient):

    def list_availability_zones(self, detail=False):
        url = 'os-availability-zone'
        schema_list = schema.list_availability_zone_list
        if detail:
            url += '/detail'
            schema_list = schema.list_availability_zone_list_detail

        resp, body = self.get(url)
        body = json.loads(body)
        self.validate_response(schema_list, resp, body)
        return service_client.ResponseBody(resp, body)
