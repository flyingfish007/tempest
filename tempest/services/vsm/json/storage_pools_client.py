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

from tempest.api_schema.response.vsm.v2_0 import storage_pools as schema
from tempest.common import service_client
from tempest import config

LOG = log.getLogger(__name__)

CONF = config.CONF


class StoragePoolsClient(service_client.ServiceClient):

    def list_storage_pools(self, detailed=False, search_opts=None):
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

        url = "storage_pools%s%s" % (detail, query_string)
        resp, body = self.get(url)
        body = json.loads(body)
        self.validate_response(schema.list_storage_pools, resp, body)
        # TODO return
        return resp, service_client.ResponseBody(resp, body)

    def add_cache_tier(self, storage_pool_id, cache_pool_id,
                       cache_mode, force_nonempty, **kwargs):
        hit_set_type = kwargs.get("hit_set_type", None)
        hit_set_count = kwargs.get("hit_set_count", None)
        hit_set_period_s = kwargs.get("hit_set_period_s", None)
        target_max_mem_mb = kwargs.get("target_max_mem_mb", None)
        target_dirty_ratio = kwargs.get("target_dirty_ratio", None)
        target_full_ratio = kwargs.get("target_full_ratio", None)
        target_max_objects = kwargs.get("target_max_objects", None)
        target_min_flush_age_m = kwargs.get("target_min_flush_age_m", None)
        target_min_evict_age_m = kwargs.get("target_min_evict_age_m", None)

        post_body = json.dumps({
            "cache_tier": {
                "storage_pool_id": storage_pool_id,
                "cache_pool_id": cache_pool_id,
                "cache_mode": cache_mode,
                "force_nonempty": force_nonempty,
                "options": {
                    "hit_set_type": hit_set_type,
                    "hit_set_count": hit_set_count,
                    "hit_set_period_s": hit_set_period_s,
                    "target_max_mem_mb": target_max_mem_mb,
                    "target_dirty_ratio": target_dirty_ratio,
                    "target_full_ratio": target_full_ratio,
                    "target_max_objects": target_max_objects,
                    "target_min_flush_age_m": target_min_flush_age_m,
                    "target_min_evict_age_m": target_min_evict_age_m
                }
            }
        })
        url = "storage_pools/add_cache_tier"
        resp, body = self.post(url, post_body)
        self.validate_response(schema.add_cache_tier, resp, body)
        # TODO return
        return resp, service_client.ResponseBody(resp, body)

    def remove_cache_tier(self, cache_pool_id):
        post_body = json.dumps({
            "cache_tier": {
                "cache_pool_id": cache_pool_id
            }
        })
        url = "storage_pools/remove_cache_tier"
        resp, body = self.post(url, post_body)
        self.validate_response(schema.remove_cache_tier, resp, body)
        # TODO return
        return resp, service_client.ResponseBody(resp, body)

    # TODO api is not ok
    def delete_storage_pool(self):
        return

    def list_ec_profiles(self):
        url = "storage_pools/get_ec_profile_list"
        resp, body = self.get(url)
        body = json.loads(body)
        self.validate_response(schema.list_ec_profiles, resp, body)
        # TODO return
        return resp, service_client.ResponseBody(resp, body)

    def create_replicated_pool(self, **kwargs):
        name = kwargs.get("name", None)
        storage_group_id = kwargs.get("storage_group_id", None)
        replicated_storage_group_id = \
            kwargs.get("replicated_storage_group_id", None)
        replicated_factor = kwargs.get("replicated_factor", None)
        max_pg_num_per_osd = kwargs.get("max_pg_num_per_osd", None)
        tag = kwargs.get("tag", None)
        cluster_id = kwargs.get("cluster_id", None)
        create_by = kwargs.get("create_by", None)
        enable_pool_quota = kwargs.get("enable_pool_quota", None)
        pool_quota = kwargs.get("pool_quota", None)

        post_body = json.dumps({
            "pool": {
                "name": name,
                "storage_group_id": storage_group_id,
                "replicated_storage_group_id":
                    replicated_storage_group_id,
                "replicated_factor": replicated_factor,
                "max_pg_num_per_osd": max_pg_num_per_osd,
                "tag": tag,
                "cluster_id": cluster_id,
                "create_by": create_by,
                "enable_pool_quota": enable_pool_quota,
                "pool_quota": pool_quota
            }
        })
        url = "storage_pool/create"
        resp, body = self.post(url, post_body)
        self.validate_response(schema.create_replicated_pool, resp, body)
        # TODO return
        return resp, service_client.ResponseBody(resp, body)

    def create_ec_pool(self, **kwargs):
        name = kwargs.get("name", None)
        storage_group_id = kwargs.get("storage_group_id", None)
        tag = kwargs.get("tag", None)
        cluster_id = kwargs.get("cluster_id", None)
        create_by = kwargs.get("create_by", None)
        ec_profile_id = kwargs.get("ec_profile_id", None)
        ec_failure_domain = kwargs.get("ec_failure_domain", None)
        enable_pool_quota = kwargs.get("enable_pool_quota", None)
        pool_quota = kwargs.get("pool_quota", None)

        post_body = json.dumps({
            "pool": {
                "name": name,
                "storage_group_id": storage_group_id,
                "tag": tag,
                "cluster_id": cluster_id,
                "create_by": create_by,
                "ec_profile_id": ec_profile_id,
                "ec_failure_domain": ec_failure_domain,
                "enable_pool_quota": enable_pool_quota,
                "pool_quota": pool_quota
            }
        })
        url = "storage_pool/create"
        resp, body = self.post(url, post_body)
        body = json.loads(body)
        self.validate_response(schema.create_ec_pool, resp, body)
        # TODO return
        return resp, service_client.ResponseBody(resp, body)