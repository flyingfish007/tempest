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


list_monitors = {
    'status_code': [200],
    'response_body': {
        'type': 'object',
        'properties': {
            'monitors': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'name': {'type': 'string'},
                        'details': {'type': 'string'},
                        'health': {'type': 'string'},
                        'address': {'type': 'string'}
                    },
                    'required': ['id', 'name', 'updated_at',
                                 'state', 'gid', 'address']
                }
            }
        },
        'required': ['monitors']
    }
}

summary_monitor = {
    'status_code': [200],
    'response_body': {
        'type': 'object',
        'properties': {
            'monitor-summary': {
                'type': 'object',
                'properties': {
                    'election_epoch': {'type': 'integer'},
                    'quorum': {'type': 'string'},
                    'monmap_epoch': {'type': 'integer'},
                    'updated_at': {'type': 'string'},
                    'overall_status': {'type': 'string'},
                    'quorum_leader_name': {'type': 'string'},
                    'monitors': {'type': 'integer'}
                },
                'required': ['election_epoch', 'quorum',
                             'monmap_epoch', 'updated_at',
                             'overall_status', 'quorum_leader_name',
                             'monitors']
            }
        },
        'required': ['monitor-summary']
    }
}

restart_monitor = {
    'status_code': [202]
}