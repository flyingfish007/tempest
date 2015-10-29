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


list_appnodes = {
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
                        'os_username': {'type': 'string'},
                        'xtrust_user': {'type': 'string'},
                        'os_tenant_name': {'type': 'string'},
                        'os_auth_url': {'type': 'string'},
                        'os_region_name': {'type': 'string'},
                        'os_password': {'type': 'string'},
                        'vsmapp_id': {'type': 'string'},
                        'uuid': {'type': 'string'},
                        'ssh_status': {'type': 'string'},
                        'log_info': {'type': 'string'}
                    },
                    'required': ['id', 'os_username', 'xtrust_user',
                                 'os_tenant_name', 'os_auth_url',
                                 'os_region_name', 'os_password',
                                 'vsmapp_id', 'uuid', 'ssh_status',
                                 'log_info']
                }
            }
        },
        'required': ['appnodes']
    }
}