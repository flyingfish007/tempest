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

from tempest.api_schema.response.vsm.v2_0 import storage_groups as schema
from tempest.common import service_client
from tempest import config

LOG = log.getLogger(__name__)

CONF = config.CONF


class StorageGroupsClient(service_client.ServiceClient):

    def create_storage_group(self, **kwargs):
        name = kwargs.get("name", None)
        friendly_name = kwargs.get("friendly_name", None)
        storage_class = kwargs.get("storage_class", None)
        cluster_id = kwargs.get("cluster_id", None)

        post_body = json.dumps({
            "storage_group": {
                "name": name,
                "friendly_name": friendly_name,
                "storage_class": storage_class,
                "cluster_id": cluster_id
            }
        })
        url = "storage_groups"
        resp, body = self.post(url, post_body)
        self.validate_response(schema.create_storage_group, resp, body)
        # TODO return
        return resp, service_client.ResponseBody(resp, body)

    # TODO api is not ok
    def get_storage_group(self):
        return

    def list_storage_groups(self, detailed=False, search_opts=None):
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

        url = "storage_groups%s%s" % (detail, query_string)
        resp, body = self.get(url)
        body = json.loads(body)
        self.validate_response(schema.list_storage_groups, resp, body)
        # TODO return
        return resp, service_client.ResponseBody(resp, body)

    def summary_storage_group(self):
        url = "storage_groups/summary"
        resp, body = self.get(url)
        body = json.loads(body)
        self.validate_response(schema.summary_storage_group, resp, body)
        # TODO return
        return resp, service_client.ResponseBody(resp, body['storage_group-summary'])