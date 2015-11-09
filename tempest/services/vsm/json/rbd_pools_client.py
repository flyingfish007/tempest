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

from tempest.api_schema.response.vsm.v2_0 import rbd_pools as schema
from tempest.common import service_client
from tempest import config

LOG = log.getLogger(__name__)

CONF = config.CONF


class RbdPoolsClient(service_client.ServiceClient):

    # TODO api is not ok
    def get_rbd_pool(self):
        return

    def list_rbd_pools(self, detailed=False, search_opts=None,
                      paginate_opts=None):
        if paginate_opts:
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

        url = "rbd_pools%s%s" % (detail, query_string)
        resp, body = self.get(url)
        body = json.loads(body)
        self.validate_response(schema.list_rbd_pools, resp, body)
        # TODO return
        return resp, service_client.ResponseBody(resp, body)

    def summary_rbd_pool(self):
        url = "rbd_pools/summary"
        resp, body = self.get(url)
        body = json.loads(body)
        self.validate_response(schema.summary_rbd_pool, resp, body)
        # TODO return
        return resp, service_client.ResponseBody(resp, body['rbd-summary'])