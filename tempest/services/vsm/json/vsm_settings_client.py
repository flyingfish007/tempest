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

from tempest.api_schema.response.vsm.v2_0 import vsm_settings as schema
from tempest.common import service_client
from tempest import config

LOG = log.getLogger(__name__)

CONF = config.CONF


class VsmSettingsClient(service_client.ServiceClient):

    def get_vsm_setting(self, vsm_setting_name):
        qparams = {}
        if vsm_setting_name:
            qparams["name"] = vsm_setting_name

        if qparams:
            query_string = "?%s" % urllib.urlencode(qparams)
        else:
            query_string = ""

        url = "vsm_settings/get_by_name%s" % query_string
        resp, body = self.get(url)
        body = json.loads(body)
        self.validate_response(schema.get_vsm_setting, resp, body)
        # TODO return
        return resp, service_client.ResponseBody(resp, body)

    def list_vsm_settings(self, detailed=False, search_opts=None):
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

        url = "vsm_settings%s%s" % (detail, query_string)
        resp, body = self.get(url)
        body = json.loads(body)
        self.validate_response(schema.list_vsm_settings, resp, body)
        # TODO return
        return resp, service_client.ResponseBody(resp, body)

    def create_vsm_setting(self, vsm_setting_name, vsm_setting_value):
        post_body = json.dumps({
            "setting": {
                "name": vsm_setting_name,
                "value": vsm_setting_value
            }
        })
        url = "vsm_settings"
        resp, body = self.post(url, post_body)
        body = json.loads(body)
        self.validate_response(schema.create_vsm_setting, resp, body)
        # TODO return
        return resp, service_client.ResponseBody(resp, body)