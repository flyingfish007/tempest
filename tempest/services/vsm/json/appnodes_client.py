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

from tempest.api_schema.response.vsm.v2_0 import appnodes as schema
from tempest.common import service_client
from tempest import config

LOG = log.getLogger(__name__)

CONF = config.CONF


class AppnodesClient(service_client.ServiceClient):

    def list_appnodes(self, detailed=False, search_opts=None):
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

        url = "appnodes%s%s" % (detail, query_string)
        resp, body = self.get(url)
        body = json.loads(body)
        self.validate_response(schema.list_appnodes, resp, body)
        # TODO return
        return resp, service_client.ResponseBody(resp, body)

    def create_appnode(self, **kwargs):
        os_tenant_name = kwargs.get('os_tenant_name', None)
        os_username = kwargs.get('os_username', None)
        os_password = kwargs.get('os_password', None)
        os_auth_url = kwargs.get('os_auth_url', None)
        os_region_name = kwargs.get('os_region_name', None)
        ssh_user = kwargs.get('ssh_user', None)

        post_body = json.dumps({
            'appnodes': {
                'os_tenant_name': os_tenant_name,
                'os_username': os_username,
                'os_password': os_password,
                'os_auth_url': os_auth_url,
                'os_region_name': os_region_name,
                'ssh_user': ssh_user
            }
        })
        url = "appnodes"
        resp, body = self.post(url, post_body)
        try:
            body = json.loads(body)
        except Exception:
            body = body
        self.validate_response(schema.create_appnode, resp, body)
        # TODO return
        return resp, service_client.ResponseBody(resp, body)

    def delete_appnode(self, appnode_id):
        url = "appnodes/%s" % appnode_id
        resp, body = self.delete(url)
        self.validate_response(schema.delete_appnode, resp, body)
        # TODO return
        return resp, service_client.ResponseBody(resp, body)

    def update_appnode(self, appnode_id, **kwargs):
        os_tenant_name = kwargs.get('os_tenant_name', None)
        os_username = kwargs.get('os_username', None)
        os_password = kwargs.get('os_password', None)
        os_auth_url = kwargs.get('os_auth_url', None)
        os_region_name = kwargs.get('os_region_name', None)
        ssh_user = kwargs.get('ssh_user', None)
        ssh_status = ""
        log_info = ""

        post_body = json.dumps({
            'appnode': {
                'os_tenant_name': os_tenant_name,
                'os_username': os_username,
                'os_password': os_password,
                'os_auth_url': os_auth_url,
                'os_region_name': os_region_name,
                'ssh_user': ssh_user,
                'ssh_status': ssh_status,
                'log_info': log_info
            }
        })
        url = "appnodes/%s" % appnode_id
        resp, body = self.post(url, post_body)
        body = json.loads(body)
        self.validate_response(schema.update_appnode, resp, body)
        # TODO return
        return resp, service_client.ResponseBody(resp, body)
