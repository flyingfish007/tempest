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

from tempest.api_schema.response.vsm.v2_0 import devices as schema
from tempest.common import service_client
from tempest import config

LOG = log.getLogger(__name__)

CONF = config.CONF


class DevicesClient(service_client.ServiceClient):

    def list_devices(self, detailed=False, search_opts=None):
        if search_opts == None:
            search_opts = {}
        qparams = {}

        for opt, val in search_opts.iteritems():
            if val:
                qparams[opt] = val

        if qparams:
            query_string = "?%s" % urllib.urlencode(qparams)
        else:
            query_string = ""

        detail = ""
        if detailed:
            detail = "/detail"

        url = "devices%s%s" % (detail, query_string)
        resp, body = self.get(url)
        body = json.loads(body)
        self.validate_response(schema.list_devices, resp, body)
        # TODO return
        return resp, service_client.ResponseBody(resp, body)

    def get_available_disks(self, search_opts=None):
        if search_opts == None:
            search_opts = {}
        qparams = {}

        for opt, val in search_opts.iteritems():
            if val:
                qparams[opt] = val

        if qparams:
            query_string = "?%s" % urllib.urlencode(qparams)
        else:
            query_string = ""

        url = "devices%s" % query_string
        resp, body = self.get(url)
        body = json.loads(body)
        self.validate_response(schema.get_available_disks, resp, body)
        # TODO return
        return service_client.ResponseBody(resp, body)

    #TODO get smart info
    def get_smart_info(self):
        return
