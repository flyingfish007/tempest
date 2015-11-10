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

from tempest.api_schema.response.vsm.v2_0 import placement_groups as schema
from tempest.common import service_client
from tempest import config

LOG = log.getLogger(__name__)

CONF = config.CONF


class PlacementGroupsClient(service_client.ServiceClient):

    def list_placement_groups(self, detailed=False, search_opts=None,
                      paginate_opts=None):
        if paginate_opts == None:
            paginate_opts = {}
        if search_opts == None:
            search_opts = {}
        qparams = {}

        for k, v in paginate_opts.iteritems():
            if v:
                qparams[k] = v

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

        url = "placement_groups%s%s" % (detail, query_string)
        resp, body = self.get(url)
        body = json.loads(body)
        self.validate_response(schema.list_placement_groups, resp, body)
        # TODO return
        return resp, service_client.ResponseBody(resp, body)

    def summary_placement_group(self):
        url = "placement_groups/summary"
        resp, body = self.get(url)
        body = json.loads(body)
        self.validate_response(schema.summary_placement_group, resp, body)
        # TODO return
        return resp, service_client.ResponseBody(resp, body['placement_group-summary'])