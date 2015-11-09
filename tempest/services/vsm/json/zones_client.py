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
import urllib
from oslo_log import log

from tempest.api_schema.response.vsm.v2_0 import zones as schema
from tempest.common import service_client
from tempest import config

LOG = log.getLogger(__name__)

CONF = config.CONF


class ZonesClient(service_client.ServiceClient):

    def create_zone(self, zone_name, cluster_id):
        post_body = json.dumps({
            "zone": {
                "name": zone_name,
                "cluster_id": cluster_id
            }
        })
        url = "zones"
        resp, body = self.post(url, post_body)
        self.validate_response(schema.create_zone, resp, body)
        # TODO return
        return resp, service_client.ResponseBody(resp, body)

    def list_zones(self, detailed=False, search_opts=None):
        if search_opts == None:
            search_opts = {}
        qparams = {}

        for k, v in search_opts.iteritems():
            if v:
                qparams[k] = v

        if qparams:
            query_string = "?%s" % urllib.urlencode(qparams)
        else:
            query_string = ""

        detail = ""
        if detailed:
            detail = "/detail"

        url = "zones%s%s" % (detail, query_string)
        resp, body = self.get(url)
        body = json.loads(body)
        self.validate_response(schema.list_zones, resp, body)
        # TODO return
        return resp, service_client.ResponseBody(resp, body)