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

list_devices = {
    'status_code': [200],
    'response_body': {
        'type': 'object',
        'properties': {
            'devices': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'journal_state': {'type': 'string'},
                        'state': {'type': 'string'},
                        'name': {'type': 'string'},
                        'device_type': {'type': 'string'},
                        'used_capacity_kb': {'type': 'integer'},
                        'path': {'type': 'string'},
                        'journal': {'type': 'string'},
                        'total_capacity_kb': {'type': 'integer'},
                        'avail_capacity_kb': {'type': 'integer'}
                    },
                    'required': ['id', 'journal_state', 'state',
                                 'name', 'device_type',
                                 'used_capacity_kb', 'path',
                                 'journal', 'total_capacity_kb',
                                 'avail_capacity_kb']
                }
            }
        },
        'required': ['devices']
    }
}

get_available_disks = {
    'status_code': [200],
    'response_body': {
        'type': 'object',
        'properties': {
            'available_disks': {'type': 'array'}
        },
        'required': ['available_disks']
    }
}

# TODO get smart info response
get_smart_info = {
    'status_code': [200]
}