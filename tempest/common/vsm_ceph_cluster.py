# Copyright (c) 2015 Hewlett-Packard Development Company, L.P.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

from oslo_log import log as logging

from tempest import config
from tempest import exceptions
from tempest.common import waiters

import paramiko
import glob
import os

CONF = config.CONF

LOG = logging.getLogger(__name__)


def create_vsm_ceph_cluster(clients):
    file = glob.glob("/tmp/vsm_cluster.lock")
    if file:
        result = wait_server_active(clients)
        if result == "no":
            os.remove("/tmp/vsm_cluster.lock")
            raise exceptions.VSMClusterErrorException
        os.remove("/tmp/vsm_cluster.lock")
        return None
    file = open("/tmp/vsm_cluster.lock", 'w')
    file.close()
    LOG.info("++++++++++++++create_vsm_ceph_cluster++++++++++++++")
    resp, body = clients.vsm_clusters_client.create_cluster()
    status = resp['status']

    if status not in ['200', '202'] or int(status) not in [200, 202]:
        os.remove("/tmp/vsm_cluster.lock")
        raise exceptions.VSMClusterErrorException
    result = wait_server_active(clients)
    if result == "no":
        os.remove("/tmp/vsm_cluster.lock")
        raise exceptions.VSMClusterErrorException

    os.remove("/tmp/vsm_cluster.lock")
    return None

def wait_server_active(clients):
    LOG.info("++++++++++++++wait_server_active++++++++++++++")
    servers_body = clients.vsm_servers_client.list_servers()
    servers = servers_body['servers']
    active_servers_num = 0
    for server in servers:
        final_status = waiters.wait_for_vsm_server_status(
            clients.vsm_servers_client, server['id'], "Active"
        )
        if final_status == "Active":
            active_servers_num = active_servers_num + 1
    if active_servers_num >= 3:
        exist = "yes"
    else:
        exist = "no"
    return exist

def check_vsm_cluster_exist(clients):
    LOG.info("++++++++++++++check_vsm_cluster_exist++++++++++++++")
    servers_body = clients.vsm_servers_client.list_servers()
    servers = servers_body['servers']
    LOG.info("++++check_vsm_cluster_exist, servers++++++++++++++" + str(servers))
    for server in servers:
        if server['status'] == "Active":
            exist = "yes"
            return exist
    return "no"

def cleanup_vsm_cluster():
    LOG.info("++++++++++++++cleanup_vsm_cluster++++++++++++++")
    floating_ip = CONF.vsm.floating_ip
    username = CONF.vsm.ssh_username
    password = CONF.vsm.ssh_password
    vsm_release_package_path = CONF.vsm.vsm_release_package_path
    vsm_release = vsm_release_package_path.split("/")[-1][:-7]
    s = paramiko.SSHClient()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.connect(floating_ip, port=22, username=username, password=password)

    LOG.info("=============cleanup vsm controller")
    stdin, stdout, stderr = s.exec_command("clean-data -f")
    stdin, stdout, stderr = s.exec_command("agent-token")
    token_id = stdout.read().strip("\n")

    LOG.info("=============cleanup vsm agent")
    cmd = "for ip in `source /tmp/%s;echo $AGENT_ADDRESS_LIST`; do " \
          "ssh $ip 'sudo replace-str %s; clean-data -f;" \
          "sudo service vsm-agent restart;" \
          "sudo service vsm-physical restart'" % (vsm_release, token_id)
    stdin, stdout, stderr = s.exec_command(cmd)

    LOG.info("=============cleanup OVER success")
