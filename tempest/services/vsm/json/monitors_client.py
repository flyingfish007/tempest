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

from tempest.api_schema.response.vsm.v2_0 import monitors as schema
from tempest.common import service_client
from tempest import config

LOG = log.getLogger(__name__)

CONF = config.CONF


class MonitorsClient(service_client.ServiceClient):

    def list_monitors(self, detailed=False, search_opts=None):
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

        url = "monitors%s%s" % (detail, query_string)
        resp, body = self.get(url)
        body = json.loads(body)
        self.validate_response(schema.list_monitors, resp, body)
        # TODO return
        return resp, service_client.ResponseBody(resp, body)

    def summary_monitor(self):
        url = "monitors/summary"
        resp, body = self.get(url)
        body = json.loads(body)
        self.validate_response(schema.summary_monitor, resp, body)
        # TODO return
        return resp, service_client.ResponseBody(resp, body['monitor-summary'])

    def _action(self, id, action_name, response_key,
                schema=None, response_class=None,
                **kwargs):
        post_body = json.dumps({action_name: kwargs})
        url = "monitors/%s/action" % id
        resp, body = self.post(url, post_body)
        if response_key is not None:
            body = json.loads(body)
            self.validate_response(schema, resp, body)
            body = body[response_key]
        else:
            self.validate_response(schema, resp, body)
        # TODO return
        return resp, response_class(resp, body)

    def restart_monitor(self, monitor_id):
        self._action(monitor_id, "restart", None,
                     schema=schema.restart_monitor,
                     response_class=service_client.ResponseBody)