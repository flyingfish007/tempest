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

from tempest.api.vsm import base
from tempest import test
from tempest import config

LOG = log.getLogger(__name__)

CONF = config.CONF


class PerformanceMetricsTestJSON(base.BaseVSMAdminTest):

    """

    Tests performance_metrics API using admin privileges.
    Performance_metric Rest API function:
        get_metrics         get
    """

    OK_STATUS = [200, 202]

    @classmethod
    def setup_clients(cls):
        super(PerformanceMetricsTestJSON, cls).setup_clients()
        cls.performance_metrics_client = \
            cls.os_adm.vsm_performance_metrics_client

    @classmethod
    def resource_setup(cls):
        super(PerformanceMetricsTestJSON, cls).resource_setup()

    @test.idempotent_id('75547727-a1ed-4394-a01e-dae36ab447c3')
    def test_get_metrics(self):
        resp, body = self.performance_metrics_client.get_metrics()
        status = resp['status']
        # TODO wish better than this assert
        self.assertIn(int(status), self.OK_STATUS)