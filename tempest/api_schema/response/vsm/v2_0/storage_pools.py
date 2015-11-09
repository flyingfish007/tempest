# Copyright 2014 NEC Corporation.  All rights reserved.
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


list_storage_pools = {
    'status_code': [200],
    'response_body': {
        'type': 'object',
        'properties': {
            'pool': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'status': {'type': 'string'},
                        'num_write_kb': {'type': 'integer'},
                        'write_bytes_sec': {'type': 'string'},
                        'op_per_sec': {'type': 'string'},
                        'updated_at': {'type': 'string'},
                        'num_objects_degraded': {'type': 'integer'},
                        'createdDate': {'type': 'string'},
                        'clusterId': {'type': 'integer'},
                        'quota': {'type': 'string'},
                        'replica_storage_group': {'type': 'string'},
                        'tag': {'type': 'string'},
                        'num_read': {'type': 'integer'},
                        'createdBy': {'type': 'string'},
                        'crashRelayInterval': {'type': 'integer'},
                        'pgpNum': {'type': 'integer'},
                        'size': {'type': 'integer'},
                        'num_objects_unfound': {'type': 'integer'},
                        'crushRuleset': {'type': 'integer'},
                        'name': {'type': 'string'},
                        'num_object_clones': {'type': 'integer'},
                        'cache_tier_status': {'type': 'string'},
                        'recipeId': {'type': 'string'},
                        'num_objects': {'type': 'integer'},
                        'pool_id': {'type': 'integer'},
                        'num_read_kb': {'type': 'integer'},
                        'minSize': {'type': 'integer'},
                        'erasure_code_status': {'type': 'string'},
                        'storageGroup': {'type': 'string'},
                        'ruleset': {'type': 'string'},
                        'poolId': {'type': 'integer'},
                        'read_bytes_sec': {'type': 'string'},
                        'pgNum': {'type': 'integer'},
                        'num_write': {'type': 'integer'},
                        'num_bytes': {'type': 'integer'},
                    },
                    'required': ['id', 'status', 'num_write_kb',
                                 'write_bytes_sec', 'op_per_sec',
                                 'updated_at', 'num_objects_degraded',
                                 'createdDate', 'clusterId',
                                 'quota', 'replica_storage_group',
                                 'tag', 'num_read', 'createdBy',
                                 'crashRelayInterval', 'pgpNum',
                                 'size', 'num_objects_unfound',
                                 'crushRuleset', 'name',
                                 'num_object_clones', 'cache_tier_status',
                                 'recipeId', 'num_objects',
                                 'pool_id', 'num_read_kb',
                                 'minSize', 'erasure_code_status',
                                 'storageGroup', 'ruleset',
                                 'poolId', 'read_bytes_sec',
                                 'pgNum', 'num_write', 'num_bytes']
                }
            }
        },
        'required': ['pool']
    }
}

add_cache_tier = {
    'status_code': [200]
}

remove_cache_tier = {
    'status_code': [200]
}

list_ec_profiles = {
    'status_code': [200],
    'response_body': {
        'type': 'object',
        'properties': {
            'ec_profiles': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'name': {'type': 'string'}
                    },
                    'required': ['id', 'name']
                }
            }
        },
        'required': ['ec_profiles']
    }
}

create_ec_pool = {
    'status_code': [200],
    'response_body': {
        'type': 'object',
        'properties': {
            'message': {'type': 'string'}
        },
        'required': ['message']
    }
}

create_replicated_pool = {
    'status_code': [200]
}