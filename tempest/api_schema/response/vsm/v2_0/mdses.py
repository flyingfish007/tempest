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


list_mdses = {
    'status_code': [200],
    'response_body': {
        'type': 'object',
        'properties': {
            'mdses': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'name': {'type': 'string'},
                        'updated_at': {'type': 'string'},
                        'state': {'type': 'string'},
                        'gid': {'type': 'string'},
                        'address': {'type': 'string'}
                    },
                    'required': ['id', 'name', 'updated_at',
                                 'state', 'gid', 'address']
                }
            }
        },
        'required': ['mdses']
    }
}

summary_mds = {
    'status_code': [200],
    'response_body': {
        'type': 'object',
        'properties': {
            'mds-summary': {
                'type': 'object',
                'properties': {
                    'num_stopped_mdses': {'type': 'integer'},
                    'num_max_mdses': {'type': 'integer'},
                    'epoch': {'type': 'integer'},
                    'metadata_pool': {'type': 'integer'},
                    'updated_at': {'type': 'string'},
                    'data_pools': {'type': 'array'},
                    'num_failed_mdses': {'type': 'integer'},
                    'num_in_mdses': {'type': 'integer'},
                    'num_up_mdses': {'type': 'integer'},

                },
                'required': ['num_stopped_mdses', 'num_max_mdses',
                             'epoch', 'metadata_pool', 'updated_at',
                             'data_pools', 'num_failed_mdses',
                             'num_in_mdses', 'num_up_mdses']
            }
        },
        'required': ['mds-summary']
    }
}