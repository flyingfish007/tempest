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


list_pool_usages = {
    'status_code': [200],
    'response_body': {
        'type': 'object',
        'properties': {
            'poolusages': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'attach_at': {'type': 'string'},
                        'attach_status': {'type': 'string'},
                        'vsmapp_id': {'type': 'integer'},
                        'pool_id': {'type': 'integer'}
                    },
                    'required': ['id', 'attach_at', 'attach_status',
                                 'vsmapp_id', 'pool_id']
                }
            }
        },
        'required': ['placement_groups']
    }
}

create_pool_usage = {
    'status_code': [202],
    'response_body': {
        'type': 'object',
        'properties': {
            'status': {'type': 'string'},
            'host': {'type': 'array'}
        },
        'required': ['status', 'host']
    }
}