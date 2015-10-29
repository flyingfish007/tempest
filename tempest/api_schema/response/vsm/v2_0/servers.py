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


list_servers = {
    'status_code': [200],
    'response_body': {
        'type': 'object',
        'properties': {
            'clusters': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'cluster_ip': {'type': 'string'},
                        'raw_ip': {'type': 'string'},
                        'secondary_public_ip': {'type': 'string'},
                        'primary_public_ip': {'type': 'string'},
                        'host': {'type': 'string'},
                        'ceph_ver': {'type': 'string'},
                        'zone_id': {'type': 'integer'},
                        'osds': {'type': 'string'},
                        'status': {'type': 'string'},
                        'service_id': {'type': 'integer'},
                        'type': {'type': 'string'}
                    },
                    'required': ['id', 'cluster_ip', 'raw_ip',
                                 'secondary_public_ip', 'primary_public_ip',
                                 'host', 'ceph_ver', 'zone_id', 'osds',
                                 'status', 'service_id', 'type']
                }
            }
        },
        'required': ['servers']
    }
}

get_server = {
    'status_code': [200],
    'response_body': {
        'type': 'object',
        'properties': {
            'clusters': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'cluster_ip': {'type': 'string'},
                        'raw_ip': {'type': 'string'},
                        'secondary_public_ip': {'type': 'string'},
                        'primary_public_ip': {'type': 'string'},
                        'host': {'type': 'string'},
                        'ceph_ver': {'type': 'string'},
                        'zone_id': {'type': 'integer'},
                        'osds': {'type': 'string'},
                        'status': {'type': 'string'},
                        'type': {'type': 'string'}
                    },
                    'required': ['id', 'cluster_ip', 'raw_ip',
                                 'secondary_public_ip', 'primary_public_ip',
                                 'host', 'ceph_ver', 'zone_id', 'osds',
                                 'status', 'type']
                }
            }
        },
        'required': ['server']
    }
}