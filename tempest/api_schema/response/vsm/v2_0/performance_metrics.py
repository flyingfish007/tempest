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


get_metrics = {
    'status_code': [200],
    'response_body': {
        'type': 'object',
        'properties': {
            'metrics': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'deleted': {'type': 'string'},
                        'timestamp': {'type': 'integer'},
                        'created_at': {'type': 'string'},
                        'hostname': {'type': 'string'},
                        'updated_at': {'type': 'string'},
                        'value': {'type': 'string'},
                        'instance': {'type': 'string'},
                        'deleted_at': {'type': 'string'},
                        'metric': {'type': 'string'}
                    },
                    'required': ['id', 'deleted', 'timestamp',
                                 'created_at', 'hostname',
                                 'updated_at', 'value',
                                 'instance', 'deleted_at', 'metric']
                }
            }
        },
        'required': ['metrics']
    }
}