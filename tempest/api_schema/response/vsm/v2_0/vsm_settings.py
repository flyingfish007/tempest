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


get_vsm_setting = {
    'status_code': [200],
    'response_body': {
        'type': 'object',
        'properties': {
            'setting': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer'},
                    'value': {'type': 'string'},
                    'name': {'type': 'string'}
                },
                'required': ['id', 'value', 'name']
            }
        },
        'required': ['setting']
    }
}

list_vsm_settings = {
    'status_code': [200],
    'response_body': {
        'type': 'object',
        'properties': {
            'settings': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'value': {'type': 'string'},
                        'name': {'type': 'string'}
                    },
                    'required': ['id', 'value', 'name']
                }
            }
        },
        'required': ['settings']
    }
}

create_vsm_setting = {
    'status_code': [202],
    'response_body': {
        'type': 'object',
        'properties': {
            'setting': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer'},
                    'value': {'type': 'string'},
                    'name': {'type': 'string'}
                },
                'required': ['id', 'value', 'name']
            }
        },
        'required': ['setting']
    }
}