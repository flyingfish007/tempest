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

from tempest.api_schema.response.vsm.v2_0 import osds as schema
from tempest.common import service_client
from tempest import config

LOG = log.getLogger(__name__)

CONF = config.CONF


class OsdsClient(service_client.ServiceClient):

    def get_osd(self, osd_id):
        url = "osds/%s" % osd_id
        resp, body = self.get(url)
        body = json.loads(body)
        self.validate_response(schema.get_osd, resp, body)
        # TODO return
        return resp, service_client.ResponseBody(resp, body)

    def list_osds(self, detailed=False, search_opts=None,
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

        url = "osds%s%s" % (detail, query_string)
        resp, body = self.get(url)
        body = json.loads(body)
        self.validate_response(schema.list_osds, resp, body)
        # TODO return
        return resp, service_client.ResponseBody(resp, body)

    def _action(self, id, action_name, response_key,
                schema=None, response_class=None,
                **kwargs):
        post_body = json.dumps({action_name: kwargs})
        url = "osds/%s/action" % id
        resp, body = self.post(url, post_body)
        if response_key is not None:
            body = json.loads(body)
            self.validate_response(schema, resp, body)
            body = body[response_key]
        else:
            self.validate_response(schema, resp, body)
        # TODO return
        return resp, response_class(resp, body)

    def restart_osd(self, osd_id):
        self._action(osd_id, "restart", None,
                     schema=schema.restart_osd,
                     response_class=service_client.ResponseBody)

    def remove_osd(self, osd_id):
        self._action(osd_id, "remove", None,
                     schema=schema.remove_osd,
                     response_class=service_client.ResponseBody)

    def add_new_disks_to_cluster(self, **kwargs):
        server_id = kwargs.get("server_id", None)
        storage_group_id = kwargs.get("storage_group_id", None)
        weight = kwargs.get("weight", None)
        journal = kwargs.get("journal", None)
        data = kwargs.get("data", None)

        post_body = json.dumps({
            "server_id": server_id,
            "osdinfo": [
                {
                    "storage_group_id": storage_group_id,
                    "weight": weight,
                    "journal": journal,
                    "data": data
                }
            ]
        })
        url = "osds/add_new_disks_to_cluster"
        resp, body = self.post(url, post_body)
        self.validate_response(schema.add_new_disks_to_cluster, resp, body)
        # TODO return
        return resp, service_client.ResponseBody(resp, body)

    def restore_osd(self, osd_id):
        self._action(osd_id, "restore", None,
                     schema=schema.restore_osd,
                     response_class=service_client.ResponseBody)

    def refresh_osd(self):
        url = "osds/refresh"
        resp, body = self.post(url, {})
        self.validate_response(schema.refresh_osd, resp, body)
        # TODO return
        return resp, service_client.ResponseBody(resp, body)

    def summary_osd(self):
        url = "osds/summary"
        resp, body = self.get(url)
        body = json.loads(body)
        self.validate_response(schema.summary_osd, resp, body)
        # TODO return
        return resp, service_client.ResponseBody(resp, body['osd-summary'])