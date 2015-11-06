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


get_osd = {
    'status_code': [200],
    'response_body': {
        'type': 'object',
        'properties': {
            'osd': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer'},
                    'cluster_ip': {'type': 'string'},
                    'storage_group': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer'},
                            'status': {'type': 'string'},
                            'name': {'type': 'string'},
                            'deleted': {'type': 'boolean'},
                            'created_at': {'type': 'string'},
                            'friendly_name': {'type': 'string'},
                            'updated_at': {'type': 'string'},
                            'rule_id': {'type': 'integer'},
                            'drive_extended_threshold': {'type': 'integer'},
                            'storage_class': {'type': 'string'},
                            'deleted_at': {'type': 'string'}
                        }
                    },
                    'zone_id': {'type': 'integer'},
                    'weight': {'type': 'integer'},
                    'deleted': {'type': 'boolean'},
                    'storage_group_id': {'type': 'integer'},
                    'created_at': {'type': 'string'},
                    'osd_name': {'type': 'string'},
                    'updated_at': {'type': 'string'},
                    'public_ip': {'type': 'string'},
                    'state': {'type': 'string'},
                    'operation_status': {'type': 'string'},
                    'service_id': {'type': 'integer'},
                    'storage_group_id': {'type': 'integer'},
                    'storage_group_id': {'type': 'integer'},
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

list_osds = {
    'status_code': [200],
    'response_body': {
        'type': 'object',
        'properties': {
            'osds': {
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
        'required': ['osds']
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