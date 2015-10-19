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


import os
import time

import paramiko

from apply_servers import ApplyServers
from apply_servers import error


apply_servers = ApplyServers()


def prepare_servers():
    apply_servers.image_available(apply_servers.image_name)
    apply_servers.flavor_available(apply_servers.flavor_id)
    apply_servers.net_available(apply_servers.net_id)

    if not apply_servers.volumes_name:
        error("No volumes name, please check your "
              "flavor id in tempest.conf or config.py file")
    volumes_name = apply_servers.volumes_name
    volumes_name_list = volumes_name.split(",")

    servers_name_list = apply_servers.servers_name.split(",")
    if len(volumes_name_list) != len(servers_name_list) * 2:
        error("Please check the volume config "
              "each agent has two volumes!")
    count = 0
    floating_ip = apply_servers.floating_ip
    for server_name in servers_name_list:
        server_name = server_name.strip()
        apply_servers.create_server(server_name,
                                    apply_servers.image_name,
                                    apply_servers.flavor_id,
                                    apply_servers.net_id,
                                    apply_servers.security_group,
                                    apply_servers.key_name,
                                    floating_ip,
                                    volumes_name_list[count:count + 2])
        count = count + 2
    print(apply_servers.ip_list)


def deploy_vsm():
    print("Be sure that you have vsm release package "
          "under the folder tools")
    vsm_release_package_path = apply_servers.vsm_release_package_path
    os.system("tar -zxvf %s" % vsm_release_package_path)
    vsm_package = vsm_release_package_path.split("/")[-1]
    vsm_release_path = ".".join(vsm_package.split(".")[0:3])
    controller_ip = apply_servers.ip_list[-1]
    agent_ip_list = " ".join(apply_servers.ip_list[0:-1])
    os.system("echo '\nCONTROLLER_ADDRESS=\"%s\"'|tee -a %s" % (
        controller_ip, vsm_release_path + "/installrc"
    ))
    os.system("echo 'AGENT_ADDRESS_LIST=\"%s\"'|tee -a %s" % (
        agent_ip_list, vsm_release_path + "/installrc"
    ))
    os.system("sed -i \"/sleep 5/aexport https_proxy="
              "http:\/\/proxy-shz.intel.com:911\" %s" %
              vsm_release_path + "/install.sh")

    net = ".".join(apply_servers.ip_list[0].split(".")[0:3]) + ".0"
    cluster_manifest_example_path = vsm_release_path + "/manifest/cluster." \
                                                       "manifest.sample"
    server_manifest_example_path = vsm_release_path + "/manifest/server." \
                                                      "manifest.sample"
    os.system("sed -i \"s/192.168.123.0/%s/g\" %s" %
              (net, cluster_manifest_example_path))
    os.system("sed -i \"s/192.168.124.0/%s/g\" %s" %
              (net, cluster_manifest_example_path))
    os.system("sed -i \"s/192.168.125.0/%s/g\" %s" %
              (net, cluster_manifest_example_path))
    os.system("echo \"[vsm_controller_ip]\"| tee %s" %
              server_manifest_example_path)
    os.system("echo \"%s\"| tee -a %s" %
              (controller_ip, server_manifest_example_path))
    os.system("echo \"\"| tee -a %s" % server_manifest_example_path)
    os.system("echo \"[role]\"| tee -a %s" % server_manifest_example_path)
    os.system("echo \"storage\"| tee -a %s" % server_manifest_example_path)
    os.system("echo \"monitor\"| tee -a %s" % server_manifest_example_path)
    os.system("echo \"\"| tee -a %s" % server_manifest_example_path)
    os.system("echo \"[auth_key]\"| tee -a %s" % server_manifest_example_path)
    os.system("echo \"token-tenant\"| tee -a %s" %
              server_manifest_example_path)
    os.system("echo \"\"| tee -a %s" % server_manifest_example_path)
    os.system("echo \"[ssd]\"| tee -a %s" % server_manifest_example_path)
    os.system("echo \"#format [ssd_device]  [journal_device]\"| tee -a %s" %
              server_manifest_example_path)
    os.system("echo \"\"| tee -a %s" % server_manifest_example_path)
    os.system("echo \"[7200_rpm_sata]\"| tee -a %s" %
              server_manifest_example_path)
    os.system("echo \"#format [sata_device]  [journal_device]\"| tee -a %s" %
              server_manifest_example_path)
    os.system("echo \"\"| tee -a %s" % server_manifest_example_path)
    os.system("echo \"[10krpm_sas]\"| tee -a %s" %
              server_manifest_example_path)
    os.system("echo \"#format [sas_device]  [journal_device]\"| tee -a %s" %
              server_manifest_example_path)
    os.system("echo \"/dev/vdb1  /dev/vdc1\"| tee -a %s" %
              server_manifest_example_path)

    cluster_manifest_path = vsm_release_path + "/manifest/" + controller_ip
    os.system("mkdir -p %s" % cluster_manifest_path)
    os.system("cp %s %s" % (cluster_manifest_example_path,
                            cluster_manifest_path + "/cluster.manifest"))
    for agent_ip in apply_servers.ip_list[0:-1]:
        server_manifest_path = vsm_release_path + "/manifest/" + agent_ip
        os.system("mkdir -p %s" % server_manifest_path)
        os.system("cp %s %s" % (server_manifest_example_path,
                                server_manifest_path + "/server.manifest"))
    os.system("tar -czvf %s %s" % (vsm_package, vsm_release_path))
    time.sleep(5)
    print("waiting the controller server is active!")

    while True:
        try:
            print("===============")
            t = paramiko.Transport(apply_servers.floating_ip, 22)
            t.connect(username=apply_servers.ssh_username,
                      password=apply_servers.ssh_password)
            sftp = paramiko.SFTPClient.from_transport(t)
            localpath = vsm_package
            remotepath = "/tmp/" + vsm_package
            sftp.put(localpath, remotepath)
            t.close()
            break
        except Exception:
            continue

    s = paramiko.SSHClient()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.connect(apply_servers.floating_ip, port=22,
              username=apply_servers.ssh_username,
              password=apply_servers.ssh_password)
    print("Begin to install vsm, please wait for a few minutes!")
    print("Install controller %s ..." % controller_ip)
    stdin, stdout, stderr = s.exec_command("cd /tmp;tar -zxvf %s;cd %s;"
                                           "./install.sh -v 2.0 -u %s "
                                           "--prepare --controller %s"
                                           % (vsm_package, vsm_release_path,
                                              apply_servers.ssh_username,
                                              controller_ip))
    print("out: " + stdout.read())
    print("err: " + stderr.read())

    for ip in apply_servers.ip_list[0:-1]:
        print("Install agent %s ..." % ip)
        stdin, stdout, stderr = s.exec_command("cd /tmp/%s;"
                                               "./install.sh -v 2.0 -u %s "
                                               "--agent %s"
                                               % (apply_servers.ssh_username,
                                                  vsm_release_path, ip))
        print("out: " + stdout.read())
        print("err: " + stderr.read())

    s.close()


if __name__ == "__main__":
    prepare_servers()
    deploy_vsm()