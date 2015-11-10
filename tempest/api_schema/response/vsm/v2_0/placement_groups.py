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


list_placement_groups = {
    'status_code': [200],
    'response_body': {
        'type': 'object',
        'properties': {
            'placement_groups': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'acting': {'type': 'string'},
                        'state': {'type': 'string'},
                        'pg_id': {'type': 'integer'},
                        'up': {'type': 'string'}
                    },
                    'required': ['id', 'acting', 'state',
                                 'pg_id', 'up']
                }
            }
        },
        'required': ['placement_groups']
    }
}

summary_placement_group = {
    'status_code': [200],
    'response_body': {
        'type': 'object',
        'properties': {
            'placement_group-summary': {
                'type': 'object',
                'items': {
                    'type': 'object',
                    'properties': {
                        'bytes_total': {'type': 'integer'},
                        'degraded_objects': {'type': 'integer'},
                        'num_pgs': {'type': 'integer'},
                        'data_bytes': {'type': 'integer'},
                        'degraded_total': {'type': 'integer'},
                        'bytes_used': {'type': 'integer'},
                        'unfound_ratio': {'type': 'integer'},
                        'op_per_sec': {'type': 'integer'},
                        'write_bytes_sec': {'type': 'integer'},
                        'updated_at': {'type': 'string'},
                        'unfound_objects': {'type': 'integer'},
                        'version': {'type': 'integer'},
                        'pgs_by_state': {
                            'type': 'array',
                            'items': {
                                'type': 'object',
                                'properties': {
                                    'count': {'type': 'integer'},
                                    'state_name': {'type': 'string'}
                                },
                                'required': ['count', 'state_name']
                            }
                        },
                        'read_bytes_sec': {'type': 'integer'},
                        'degraded_ratio': {'type': 'integer'},
                        'bytes_avail': {'type': 'integer'},
                        'unfound_total': {'type': 'integer'}
                    },
                    'required': ['bytes_total', 'degraded_objects',
                                 'num_pgs', 'data_bytes', 'degraded_total',
                                 'bytes_used', 'unfound_ratio', 'op_per_sec',
                                 'write_bytes_sec', 'updated_at',
                                 'unfound_objects', 'version', 'pgs_by_state',
                                 'read_bytes_sec', 'degraded_ratio',
                                 'bytes_avail', 'unfound_total']
                }
            }
        },
        'required': ['placement_group-summary']
    }
}