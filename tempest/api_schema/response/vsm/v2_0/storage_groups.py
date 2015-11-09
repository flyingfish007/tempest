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


create_storage_group = {
    'status_code': [202]
}

list_storage_groups = {
    'status_code': [200],
    'response_body': {
        'type': 'object',
        'properties': {
            'storage_groups': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'status': {'type': 'string'},
                        'capacity_used': {'type': 'integer'},
                        'attached_pools': {'type': 'integer'},
                        'updated_at': {'type': 'string'},
                        'capacity_avail': {'type': 'integer'},
                        'capacity_total': {'type': 'integer'},
                        'name': {'type': 'string'},
                        'friendly_name': {'type': 'string'},
                        'largest_node_capacity_used': {'type': 'integer'},
                        'storage_class': {'type': 'string'},
                        'attached_osds': {'type': 'integer'}
                    },
                    'required': ['id', 'status', 'capacity_used',
                                 'attached_pools', 'updated_at',
                                 'capacity_avail', 'capacity_total',
                                 'name', 'friendly_name',
                                 'largest_node_capacity_used',
                                 'storage_class', 'attached_osds']
                }
            }
        },
        'required': ['storage_groups']
    }
}

summary_storage_group = {
    'status_code': [200],
    'response_body': {
        'type': 'object',
        'properties': {
            'storage_group-summary': {
                'type': 'object',
                'properties': {
                    'full': {'type': 'boolean'},
                    'num_up_storage_groups': {'type': 'integer'},
                    'num_storage_groups': {'type': 'integer'},
                    'nearfull': {'type': 'boolean'},
                    'epoch': {'type': 'integer'},
                    'num_in_storage_groups': {'type': 'integer'}
                },
                'required': ['full', 'num_up_storage_groups',
                             'num_storage_groups', 'nearfull',
                             'epoch', 'num_in_storage_groups']
            }
        },
        'required': ['storage_group-summary']
    }
}