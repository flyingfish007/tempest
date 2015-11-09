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

from tempest.api_schema.response.vsm.v2_0 import servers as schema
from tempest.common import service_client
from tempest import config

LOG = log.getLogger(__name__)

CONF = config.CONF


class ServersClient(service_client.ServiceClient):

    def list_servers(self, detailed=False, search_opts=None):
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

        url = "servers%s%s" % (detail, query_string)
        resp, body = self.get(url)
        body = json.loads(body)
        self.validate_response(schema.list_servers, resp, body)
        # TODO return
        return service_client.ResponseBody(resp, body)

    def get_server_by_server_id(self, server_id):
        url = "servers/%s" % server_id
        resp, body = self.get(url)
        body = json.loads(body)
        self.validate_response(schema.get_server, resp, body)
        # TODO return
        return service_client.ResponseBody(resp, body)

    def add_server(self, **kwargs):
        cluster_id = kwargs.get("cluster_id", None)
        id = kwargs.get("id", None)
        is_monitor = kwargs.get("is_monitor", None)
        is_storage = kwargs.get("is_storage", None)
        zone_id = kwargs.get("zone_id", None)

        post_body = json.dumps({
            "servers": [
                {
                    "cluster_id": cluster_id,
                    "id": id,
                    "is_monitor": is_monitor,
                    "is_storage": is_storage,
                    "zone_id": zone_id
                }
            ]
        })
        url = "servers/add"
        resp, body = self.post(url, post_body)
        self.validate_response(schema.add_server, resp, body)
        # TODO return
        return resp, service_client.ResponseBody(resp, body)

    def remove_server(self, **kwargs):
        cluster_id = kwargs.get("cluster_id", None)
        id = kwargs.get("id", None)
        remove_monitor = kwargs.get("is_monitor", None)
        remove_storage = kwargs.get("is_storage", None)

        post_body = json.dumps({
            "servers": [
                {
                    "cluster_id": cluster_id,
                    "id": id,
                    "remove_monitor": remove_monitor,
                    "remove_storage": remove_storage
                }
            ]
        })
        url = "servers/remove"
        resp, body = self.post(url, post_body)
        self.validate_response(schema.remove_server, resp, body)
        # TODO return
        return resp, service_client.ResponseBody(resp, body)

    def reset_server_status(self, server_id):
        post_body = json.dumps({
            "servers": server_id
        })
        url = "servers/reset_status"
        resp, body = self.post(url, post_body)
        body = json.loads(body)
        self.validate_response(schema.reset_server_status, resp, body)
        # TODO return
        return resp, service_client.ResponseBody(resp, body)

    def start_server(self, **kwargs):
        cluster_id = kwargs.get("cluster_id", None)
        server_id = kwargs.get("server_id", None)

        post_body = json.dumps({
            "servers": [
                {
                    "cluster_id": cluster_id,
                    "id": server_id
                }
            ]
        })
        url = "servers/start"
        resp, body = self.post(url, post_body)
        self.validate_response(schema.start_server, resp, body)
        # TODO return
        return resp, service_client.ResponseBody(resp, body)

    def stop_server(self, **kwargs):
        cluster_id = kwargs.get("cluster_id", None)
        server_id = kwargs.get("server_id", None)
        remove_monitor = kwargs.get("remove_monitor", None)
        remove_storage = kwargs.get("remove_storage", None)

        post_body = json.dumps({
            "servers": [
                {
                    "cluster_id": cluster_id,
                    "id": server_id,
                    "remove_monitor": remove_monitor,
                    "remove_storage": remove_storage
                }
            ]
        })
        url = "servers/stop"
        resp, body = self.post(url, post_body)
        self.validate_response(schema.stop_server, resp, body)
        # TODO return
        return resp, service_client.ResponseBody(resp, body)

    # TODO
    def upgrade_ceph(self, **kwargs):
        pkg_url = kwargs.get("pkg_url", None)
        key_url = kwargs.get("key_url", None)
        proxy = kwargs.get("proxy", None)
        ssh_user = kwargs.get("ssh_user", None)

        post_body = json.dumps({
            "pkg_url": pkg_url,
            "key_url": key_url,
            "proxy": proxy,
            "ssh_user": ssh_user
        })
        url = "servers/ceph_upgrade"
        resp, body = self.post(url, post_body)
        body = json.loads(body)
        self.validate_response(schema.upgrade_ceph, resp, body)
        # TODO return
        return resp, service_client.ResponseBody(resp, body)