# Copyright 2012 OpenStack Foundation
# All Rights Reserved.
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

from oslo_log import log
import random

from tempest.api.vsm import base
from tempest import test
from tempest import config

LOG = log.getLogger(__name__)

CONF = config.CONF


class OsdsTestJSON(base.BaseVSMAdminTest):

    """

    Tests osds API using admin privileges.
    Osd Rest API function:
        get                         get
        list                        get
        restart                     post
        remove                      post
        add_new_disks_to_cluster    post
        restore                     post
        refresh                     post
        summary                     get
    """

    OK_STATUS = [200, 202]

    @classmethod
    def setup_clients(cls):
        super(OsdsTestJSON, cls).setup_clients()
        cls.osds_client = cls.os_adm.vsm_osds_client

    @classmethod
    def resource_setup(cls):
        super(OsdsTestJSON, cls).resource_setup()

    @test.idempotent_id('d08c54fd-dedc-4ad1-b3cf-b3197bf2aa6b')
    def test_get_osd(self):
        _, body = self.osds_client.list_osds()
        osds = body['osds']
        random_num = random.randint(0, len(osds) - 1)
        osd = osds[random_num]
        osd_id = osd['id']
        resp, body = self.osds_client.get_osd(osd_id)
        status = resp['status']
        # TODO wish better than this assert
        self.assertIn(int(status), self.OK_STATUS)

    @test.idempotent_id('5a66bd70-34ea-456b-86c8-dae78ed18679')
    def test_list_osds(self):
        resp, body = self.osds_client.list_osds()
        status = resp['status']
        # TODO wish better than this assert
        self.assertIn(int(status), self.OK_STATUS)

    @test.idempotent_id('fad4dcb1-f07d-4b5a-a3c6-b250d000ba92')
    def test_restart_osd(self):
        _, body = self.osds_client.list_osds()
        osds = body['osds']
        random_num = random.randint(0, len(osds) - 1)
        osd = osds[random_num]
        osd_id = osd['id']
        resp, body = self.osds_client.restart_osd(osd_id)
        status = resp['status']
        # TODO wish better than this assert
        self.assertIn(int(status), self.OK_STATUS)

    @test.idempotent_id('38d71762-197d-4b9c-96fb-f6f518a4909d')
    def test_remove_ods(self):
        # TODO not implemented
        self.assertEqual(True, True)

    @test.idempotent_id('c6d82ddc-0ee4-4536-ab17-d27b4f31a089')
    def test_add_new_disks_to_cluster(self):
        # TODO not implemented
        self.assertEqual(True, True)

    @test.idempotent_id('6c243285-9e50-48c7-a523-7b6addb173cb')
    def test_restore_osd(self):
        # TODO not implemented
        self.assertEqual(True, True)

    @test.idempotent_id('66ad0f74-bc12-46a3-aadb-94e87e362636')
    def test_refresh_osd(self):
        resp, body = self.osds_client.refresh_osd()
        status = resp['status']
        # TODO wish better than this assert
        self.assertIn(int(status), self.OK_STATUS)

    @test.idempotent_id('928f0bd3-46f5-4039-a555-70943ec0e151')
    def test_summary_osd(self):
        resp, body = self.osds_client.summary_osd()
        status = resp['status']
        # TODO wish better than this assert
        self.assertIn(int(status), self.OK_STATUS)