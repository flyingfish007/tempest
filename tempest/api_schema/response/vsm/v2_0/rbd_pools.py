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


# TODO API is not ok
get_rbd_pool = {

}

list_rbd_pools = {
    'status_code': [200],
    'response_body': {
        'type': 'object',
        'properties': {
            'rbd_pools': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'format': {'type': 'integer'},
                        'updated_at': {'type': 'string'},
                        'image_name': {'type': 'string'},
                        'objects': {'type': 'integer'},
                        'order': {'type': 'integer'},
                        'pool': {'type': 'string'},
                        'size': {'type': 'integer'}
                    },
                    'required': ['id', 'format', 'updated_at',
                                 'image_name', 'objects',
                                 'order', 'pool', 'size']
                }
            }
        },
        'required': ['rbd_pools']
    }
}

summary_rbd_pool = {
    'status_code': [200],
    'response_body': {
        'type': 'object',
        'properties': {
            'rbd-summary': {
                'type': 'object',
                'properties': {
                    'full': {'type': 'boolean'},
                    'num_up_rbd_pools': {'type': 'integer'},
                    'num_rbd_pools': {'type': 'integer'},
                    'nearfull': {'type': 'boolean'},
                    'epoch': {'type': 'integer'},
                    'num_in_rbd_pools': {'type': 'integer'}
                },
                'required': ['full', 'num_up_rbd_pools',
                             'num_rbd_pools', 'nearfull',
                             'epoch', 'num_in_rbd_pools']
            }
        },
        'required': ['rbd-summary']
    }
}