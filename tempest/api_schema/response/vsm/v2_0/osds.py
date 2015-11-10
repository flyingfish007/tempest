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
                            'deleted_at': {'type': 'null'}
                        },
                        'required': ['id', 'status', 'name',
                                     'deleted', 'created_at',
                                     'friendly_name', 'updated_at',
                                     'rule_id', 'drive_extended_threshold',
                                     'storage_class', 'deleted_at']
                    },
                    'zone_id': {'type': 'integer'},
                    'weight': {'type': 'number'},
                    'deleted': {'type': 'boolean'},
                    'storage_group_id': {'type': 'integer'},
                    'created_at': {'type': 'string'},
                    'osd_name': {'type': 'string'},
                    'updated_at': {'type': 'string'},
                    'public_ip': {'type': 'string'},
                    'state': {'type': 'string'},
                    'operation_status': {'type': 'string'},
                    'service_id': {'type': 'integer'},
                    'device': {
                        'type': 'object',
                        'properties': {
                            'mount_point': {'type': 'string'},
                            'name': {'type': 'string'},
                            'used_capacity_kb': {'type': 'integer'},
                            'deleted': {'type': 'boolean'},
                            'created_at': {'type': 'string'},
                            'updated_at': {'type': 'string'},
                            'interface_type': {'type': 'null'},
                            'id': {'type': 'integer'},
                            'journal_state': {'type': 'string'},
                            'state': {'type': 'string'},
                            'fs_type': {'type': 'string'},
                            'device_type': {'type': 'string'},
                            'service_id': {'type': 'integer'},
                            'journal': {'type': 'string'},
                            'path': {'type': 'string'},
                            'deleted_at': {'type': 'null'},
                            'total_capacity_kb': {'type': 'integer'},
                            'avail_capacity_kb': {'type': 'integer'}
                        },
                        'required': ['mount_point', 'name',
                                     'used_capacity_kb', 'deleted',
                                     'created_at', 'updated_at',
                                     'interface_type', 'id',
                                     'journal_state', 'state',
                                     'fs_type', 'device_type',
                                     'service_id', 'journal', 'path',
                                     'deleted_at', 'total_capacity_kb',
                                     'avail_capacity_kb']
                    },
                    'cluster_id': {'type': 'integer'},
                    'deleted_at': {'type': 'null'},
                    'device_id': {'type': 'integer'}
                },
                'required': ['id', 'cluster_ip', 'storage_group', 'zone_id',
                             'weight', 'deleted', 'storage_group_id',
                             'created_at', 'osd_name', 'updated_at', 'public_ip',
                             'state', 'operation_status', 'service_id', 'device',
                             'cluster_id', 'deleted_at', 'device_id']
            }
        },
        'required': ['osd']
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
                        'state': {'type': 'string'},
                        'operation_status': {'type': 'string'},
                        'weight': {'type': 'number'},
                        'updated_at': {'type': 'string'},
                        'service_id': {'type': 'integer'},
                        'osd_name': {'type': 'string'},
                        'device_id': {'type': 'integer'}
                    },
                    'required': ['id', 'state', 'operation_status',
                                 'weight', 'updated_at', 'service_id',
                                 'osd_name', 'device_id']
                }
            }
        },
        'required': ['osds']
    }
}

restart_osd = {
    'status_code': [202]
}

remove_osd = {
    'status_code': [202]
}

add_new_disks_to_cluster = {
    'status_code': [202]
}

restore_osd = {
    'status_code': [202]
}

refresh_osd = {
    'status_code': [200]
}

summary_osd = {
    'status_code': [200],
    'response_body': {
        'type': 'object',
        'properties': {
            'osd-summary': {
                'type': 'object',
                'properties': {
                    'full': {'type': 'boolean'},
                    'nearfull': {'type': 'boolean'},
                    'num_osds': {'type': 'integer'},
                    'updated_at': {'type': 'string'},
                    'num_up_osds': {'type': 'integer'},
                    'epoch': {'type': 'integer'},
                    'num_in_osds': {'type': 'integer'}
                },
                'required': ['full', 'nearfull',
                             'num_osds', 'updated_at',
                             'num_up_osds', 'epoch',
                             'num_in_osds']
            }
        },
        'required': ['osd-summary']
    }
}
