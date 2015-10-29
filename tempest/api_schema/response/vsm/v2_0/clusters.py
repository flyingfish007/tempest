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


list_clusters = {
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
                        'name': {'type': 'string'},
                        'cluster_ip_netmask': {'type': 'string'},
                        'file_system': {'type': 'string'},
                        'size': {'type': 'string'},
                        'scecondary_public_ip_netmask': {'type': 'string'},
                        'primary_public_ip_netmask': {'type': 'string'},
                        'cluster_network': {'type': 'string'},
                        'journal_size': {'type': 'string'}
                    },
                    'required': ['id', 'name', 'cluster_ip_netmask',
                                 'file_system', 'size',
                                 'scecondary_public_ip_netmask',
                                 'primary_public_ip_netmask',
                                 'cluster_network', 'journal_size']
                }
            }
        },
        'required': ['clusters']
    }
}

create_cluster = {
    'status_code': [202]
}