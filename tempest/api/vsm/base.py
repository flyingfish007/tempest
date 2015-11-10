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

import time

from oslo_log import log as logging

from tempest import config
from tempest import exceptions
from tempest.common import vsm_ceph_cluster
import tempest.test

CONF = config.CONF

LOG = logging.getLogger(__name__)


class BaseVSMTest(tempest.test.BaseTestCase):
    """Base test case class for all VSM API tests."""

    _api_version = 2

    credentials = ['primary']

    @classmethod
    def skip_checks(cls):
        super(BaseVSMTest, cls).skip_checks()
        if cls._api_version != 2:
            msg = ("Unexpected API version is specified (%s)" %
                   cls._api_version)
            raise exceptions.InvalidConfiguration(message=msg)

    @classmethod
    def setup_credentials(cls):
        cls.set_network_resources()
        super(BaseVSMTest, cls).setup_credentials()

    @classmethod
    def setup_clients(cls):
        super(BaseVSMTest, cls).setup_clients()
        cls.clusters_client = cls.os.vsm_clusters_client
        cls.servers_client = cls.os.vsm_servers_client
        cls.appnodes_client = cls.os.vsm_appnodes_client
        cls.devices_client = cls.os.vsm_devices_client
        cls.mdses_client = cls.os.vsm_mdses_client
        cls.monitors_client = cls.os.vsm_monitors_client
        cls.osds_client = cls.os.vsm_osds_client
        cls.performance_metrics_client = \
            cls.os.vsm_performance_metrics_client
        cls.placement_groups_client = \
            cls.os.vsm_placement_groups_client

    @classmethod
    def resource_setup(cls):
        super(BaseVSMTest, cls).resource_setup()
        cls.build_interval = CONF.vsm.build_interval
        cls.build_timeout = CONF.vsm.build_timeout

    @classmethod
    def resource_cleanup(cls):
        super(BaseVSMTest, cls).resource_cleanup()

    @classmethod
    def create_vsm_ceph_cluster(cls):
        vsm_ceph_cluster.create_vsm_ceph_cluster(cls.os)

    @classmethod
    def check_vsm_cluster_exist(cls):
        result = vsm_ceph_cluster.check_vsm_cluster_exist(cls.os)
        return result

    @classmethod
    def cleanup_vsm_cluster(cls):
        vsm_ceph_cluster.cleanup_vsm_cluster(cls.os)

    def wait_for(self, condition):
        """Repeatedly calls condition() until a timeout."""
        start_time = int(time.time())
        while True:
            try:
                condition()
            except Exception:
                pass
            else:
                return
            if int(time.time()) - start_time >= self.build_timeout:
                condition()
                return
            time.sleep(self.build_interval)


class BaseVSMAdminTest(BaseVSMTest):
    """Base test case class for VSM Admin API tests."""

    credentials = ['primary', 'admin']

    @classmethod
    def setup_clients(cls):
        super(BaseVSMAdminTest, cls).setup_clients()
