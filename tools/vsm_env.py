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


import ConfigParser
import sys
import os
import time
import re
import fileinput

import paramiko
import pexpect

try:
    from novaclient.v1_1 import client as nc_client
except Exception:
    from novaclient.v2 import client as nc_client
try:
    from cinderclient.v1 import client as cc_client
except Exception:
    from cinderclient.v2 import client as cc_client


CONF = ConfigParser.ConfigParser()
try:
    CONF.read(sys.argv[1])
except Exception:
    CONF.read("/opt/tempest/etc/tempest.conf")

def print_msg(level, action, msg):
    now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(now_time + " " + level + " " + action + " " + msg)
    if level == "ERROR":
        sys.exit(1)

def ingreen(str):
    return"%s[32;2m%s%s[0m"%(chr(27), str, chr(27))

def inred(str):
    return"%s[31;2m%s%s[0m"%(chr(27), str, chr(27))


class ApplyServers(object):
    """

    """

    def __init__(self, username, password, tenant_name,
                 auth_url, region_name):
        self.timeout = CONF.get("vsm", "timeout")
        self.controller_server_name = CONF.get("vsm", "controller_server_name")
        self.agent_servers_name = CONF.get("vsm", "agent_servers_name")
        self.servers_name = self.agent_servers_name + "," + self.controller_server_name
        self.ssh_username = CONF.get("vsm", "ssh_username")
        self.ssh_password = CONF.get("vsm", "ssh_password")
        self.os_type = CONF.get("vsm", "os_type")
        self.floating_ip = CONF.get("vsm", "floating_ip")
        self.fixed_ip_list = []
        self.vsm_openstack_server_name = \
            CONF.get("vsm", "vsm_openstack_server_name")
        self.vsm_openstack_ssh_username = \
            CONF.get("vsm", "vsm_openstack_ssh_username")
        self.vsm_openstack_ssh_password = \
            CONF.get("vsm", "vsm_openstack_ssh_password")

        self.novaclient = \
            nc_client.Client(
                username,
                password,
                tenant_name,
                auth_url,
                region_name=region_name
            )

        self.cinderclient = \
            cc_client.Client(
                username,
                password,
                tenant_name,
                auth_url,
                region_name=region_name
            )

    def image_available(self, image_name):
        """

        :param str image_name: Image Name
        :return object image: Image Object
        """

        print_msg("INFO", "[-] check image", "[-]")
        if not image_name:
            print_msg("ERROR", "[-] check image",
                      inred("[-] Image name is null, please check "
                            "your image_name in tempest.conf file"))

        images_list = self.novaclient.images.list()
        for image in images_list:
            if image_name == image.name and image.status == "ACTIVE":
                print_msg("INFO", "[-] check image",
                          ingreen("[-] The image " + image_name + " is available"))
                return image
        print_msg("ERROR", "[-] check image",
                  inred("[-] Not found the " + image_name + " image"))

    def flavor_available(self, flavor_id):
        """

        :param str flavor_id: Flavor ID
        :return object flavor: Flavor Object
        """

        print_msg("INFO", "[-] check flavor", "[-]")
        if not flavor_id:
            print_msg("ERROR", "[-] check flavor",
                      inred("[-] Flavor id is null, please check your "
                            "flavor id in tempest.conf file"))

        flavors_list = self.novaclient.flavors.list()
        for flavor in flavors_list:
            if flavor_id == flavor.id:
                flavor_name = flavor.name
                print_msg("INFO", "[-] check flavor",
                          ingreen("[-] The flavor " + flavor_name + " is available"))
                return flavor
        print_msg("ERROR", "[-] check flavor",
                  inred("[-] Not found the flavor id " + flavor_id))

    def net_available(self, net_id):
        """

        :param str net_id: Network ID
        :return object net: Network Objeck
        """

        print_msg("INFO", "[-] check net", "[-]")
        if not net_id:
            print_msg("ERROR", "[-] check net",
                      inred("[-] Network id is null, please check "
                            "your net id in tempest.conf file"))

        nets_list = self.novaclient.networks.list()
        for net in nets_list:
            if net_id == net.id:
                net_name = net.label
                print_msg("INFO", "[-] check net",
                          ingreen("[-] The net " + net_name +" is available"))
                return net
        print_msg("ERROR", "[-] check net", inred("[-] Not found the net id " + net_id))

    def volume_available(self, volume_name, volume_size):
        """

        :param str volume_name: Volume Name
        :param int volume_size: Volume Size
        :return object volume: Volume Object
        """

        print_msg("INFO", "[-] check volume", "[-]")
        volumes_list = self.cinderclient.volumes.list()
        for volume in volumes_list:
            if volume_name == volume.name:
                print_msg("INFO", "[-] check volume",
                          ingreen("[-] The volume " + volume_name + " is available"))
                return volume
        print_msg("WARNING", "[-] check volume",
                  "[-] Not found the volume " + inred(volume_name))
        volume = self.create_volume(volume_name, volume_size)
        return volume

    def create_volume(self, volume_name, volume_size):
        """

        :param str volume_name: Volume Name
        :param int volume_size: Volume Size
        :return object volume: Volume Object
        """

        print_msg("INFO", "[-] create volume", "[-] Creating the volume %s" % volume_name)
        self.cinderclient.volumes.create(volume_size, display_name=volume_name)
        time.sleep(2)
        wait_time = 1
        while wait_time < self.timeout:
            time.sleep(wait_time)
            volumes = self.cinderclient.volumes.list()
            for volume in volumes:
                if volume_name == volume.name and volume.status == "available":
                    return volume
            wait_time = wait_time + 1
            continue
        print_msg("ERROR", "[-] create volume",
                  inred("[-] The volume " + volume_name + " is still not available, please "
                                                      "check it by yourself"))

    def run_command_remote_server(self, ip, username, password, cmd):
        """

        :param str ip: Remote IP to connect
        :param str cmd: Execute command
        :return
        """
        hostname_or_ip = ip
        port = 22
        # username = self.ssh_username
        # password = self.ssh_password
        print_msg("INFO", "[-] run command", "[-] " + cmd + " on " + ip)

        s = paramiko.SSHClient()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.connect(hostname_or_ip, port=port, username=username,
                  password=password)
        stdin, stdout, stderr = s.exec_command(cmd)
        result = stdout.read()
        s.close()
        return result

    def create_server(self, server_name, image_name, flavor_id, net_id,
                      security_group="default", key_name="demo-key",
                      floating_ip=None, volume_size=None, volumes_list=None,
                      vsm_server_type="agent"):
        """

        :param str server_name: Server Name
        :param str image_name: Image Name
        :param str flavor_id: Flavor ID
        :param str net_id: Network ID
        :param str security_group: Security Group
        :param str key_name: Key Name
        :param str floating_ip: Floating IP
        :param int volume size: Volume Size
        :param list volume list: Volume List
        :return
        """
        if not server_name:
            print_msg("ERROR", "[-] create server", "[-] Server name is null")

        image = None
        if not image_name:
            print_msg("ERROR", "[-] create server", "[-] Image name is null")
        else:
            image = self.image_available(image_name)

        flavor = None
        if not flavor_id:
            print_msg("ERROR", "[-] create server", "[-] Flavor id is null")
        else:
            flavor = self.flavor_available(flavor_id)

        net = None
        if not net_id:
            print_msg("ERROR", "[-] create server", "[-] Network id is null")
        else:
            net = self.net_available(net_id)

        server_list = self.novaclient.servers.list()
        for server in server_list:
            if server.name == server_name:
                print_msg("INFO", "[-] create server", "[-] Begin to delete %s" % server_name)
                self.novaclient.servers.delete(server.id)
                wait_time = 1
                while wait_time < self.timeout:
                    time.sleep(wait_time)
                    print_msg("INFO", "[-] create server",
                              "[-] Waiting %s seconds to delete server %s" %
                              (wait_time, server_name))
                    server_list = self.novaclient.servers.list()
                    if server_name in [server.name for server in server_list]:
                        wait_time = wait_time + 1
                        continue
                    else:
                        break
                print_msg("INFO", "[-] create server",
                          ingreen("[-] Old server %s has been deleted" % server_name))

        image_id = image.id
        server = self.novaclient.servers.create(
            server_name,
            image_id,
            flavor.id,
            security_groups=[security_group],
            key_name=key_name,
            nics=[{"net-id": net.id}]
        )
        wait_time = 1
        while wait_time < 100:
            print_msg("INFO", "[-] create server",
                      "[-] Waiting %s seconds to create server %s" %
                      (wait_time, server_name))
            time.sleep(wait_time)
            server = self.novaclient.servers.get(server.id)
            if server.status == "ACTIVE":
                print_msg("INFO", "[-] create server",
                          ingreen("[-] The server " + server.name + " is active"))
                print_msg("INFO", "[-] create server",
                          "[-] Begin to associate floating ip to server")
                self.novaclient.servers.add_floating_ip(server.id, floating_ip)
                print_msg("INFO", "[-] create server",
                          "[-] End to associate floating ip to server")
                if vsm_server_type == "agent":
                    print_msg("INFO", "[-] create server", "[-] Begin to attach volume")
                    for volume_name in volumes_list:
                        volume = self.volume_available(volume_name, volume_size)
                        self.novaclient.volumes.create_server_volume(
                            server.id,
                            volume.id,
                            None
                        )
                    print_msg("INFO", "[-] create server", "[-] End to attach volume")

                print_msg("INFO", "[-] create server",
                          "[-] Set NOPASSWD for user %s" % self.ssh_username)
                while True:
                    try:
                        if self.os_type == "ubuntu":
                            ssh = pexpect.spawn(
                                'ssh -t %s@%s \'echo "%s ALL=(ALL) NOPASSWD: ALL" '
                                '| sudo tee /etc/sudoers.d/%s\'' %
                                (self.ssh_username, floating_ip,
                                 self.ssh_username, self.ssh_username))
                        else:
                            ssh = pexpect.spawn(
                                'ssh -t %s@%s \'echo "%s ALL=(ALL) NOPASSWD: ALL" '
                                '| tee /etc/sudoers.d/%s\'' %
                                (self.ssh_username, floating_ip,
                                 self.ssh_username, self.ssh_username))
                        index = ssh.expect(["continue connecting", "password"])
                        if index == 0:
                            time.sleep(1)
                            ssh.sendline("yes")
                            time.sleep(1)
                            ssh.expect("password")
                            time.sleep(1)
                            ssh.sendline(self.ssh_password)
                        else:
                            time.sleep(1)
                            ssh.sendline(self.ssh_password)
                        if self.ssh_username != "root":
                            ssh.expect("password")
                            ssh.sendline(self.ssh_password)
                        break
                    except Exception:
                        print_msg("INFO", "[-] create server",
                                  "[-] Waiting for 10 seconds that "
                                  "floating ip is not ready...")
                        time.sleep(10)

                if self.os_type == "ubuntu":
                    self.run_command_remote_server(
                        floating_ip, self.ssh_username, self.ssh_password,
                        "sudo chmod 0440 /etc/sudoers.d/%s" % self.ssh_username)
                else:
                    self.run_command_remote_server(
                        floating_ip, self.ssh_username, self.ssh_password,
                        "chmod 0440 /etc/sudoers.d/%s" % self.ssh_username)
                print_msg("INFO", "[-] create server",
                          "[-] Generate ssh-key for user %s" % self.ssh_username)
                while True:
                    try:
                        ssh = pexpect.spawn('ssh -t %s@%s \'ssh-keygen -t rsa\''
                                            % (self.ssh_username, floating_ip))
                        ssh.expect("password")
                        ssh.sendline(self.ssh_password)
                        ssh.expect("Enter file")
                        ssh.sendline("")
                        ssh.expect("Enter passphrase")
                        ssh.sendline("")
                        ssh.expect("Enter same passphrase")
                        ssh.sendline("")
                        break
                    except Exception:
                        print_msg("WARNING", "[-] create server",
                                  "[-] connecting to %s failed, wait for 5 seconds" % floating_ip)
                        time.sleep(5)

                if self.os_type.lower() == "ubuntu":
                    cmd1 = "ifconfig eth0|grep \"inet addr\"|awk -F \" \" " \
                           "'{print $2}'|awk -F \":\" '{print $2}'"

                    cmd2 = "sudo parted /dev/vdb -- mklabel gpt;" \
                       "sudo parted /dev/vdc -- mklabel gpt;" \
                       "sudo parted -a optimal /dev/vdb -- mkpart xfs 1MB 100%;" \
                       "sudo parted -a optimal /dev/vdc -- mkpart xfs 1MB 100%"

                    cmd3 = "echo \"deb http://192.168.1.34 vsm-dep-repo-ubuntu14/\" |" \
                           "sudo tee /etc/apt/sources.list.d/repo.list;" \
                           "echo \"APT::Get::AllowUnauthenticated 1 ;\" |" \
                           "sudo tee /etc/apt/apt.conf;" \
                           "echo \"nameserver 10.248.2.5\" |" \
                           "sudo tee /etc/resolvconf/resolv.conf.d/base;" \
                           "sudo mv /etc/apt/sources.list /etc/apt/sources.list.old;" \
                           "echo %s | sudo tee /etc/hostname;" \
                           "sudo reboot" % server_name

                else:
                    cmd1 = "ifconfig |grep broadcast| awk -F \" \" " \
                           "'{print $2}'"

                    cmd2 = "parted /dev/vdb -- mklabel gpt;" \
                           "parted /dev/vdc -- mklabel gpt;" \
                           "parted -a optimal /dev/vdb -- mkpart xfs 1MB 100%;" \
                           "parted -a optimal /dev/vdc -- mkpart xfs 1MB 100%"

                    cmd3 = "mv /etc/yum.repos.d/* /tmp;" \
                           "sed -i \"s/Defaults    requiretty/#Defaults    requiretty/g\" /etc/sudoers;" \
                           "echo \"[repo]\"|tee /etc/yum.repos.d/repo.repo;" \
                           "echo \"name=repo\"|tee /etc/yum.repos.d/repo.repo;" \
                           "echo \"baseurl=http://192.168.1.34/vsm-dep-repo-centos7\"|" \
                           "tee /etc/yum.repos.d/repo.repo;" \
                           "echo \"gpgcheck=0\"|tee /etc/yum.repos.d/repo.repo;" \
                           "echo \"enabled=1\"|tee /etc/yum.repos.d/repo.repo;" \
                           "echo \"proxy=_none_\"|tee /etc/yum.repos.d/repo.repo;" \
                           "echo %s |tee /etc/hostname;" \
                           "reboot" % server_name

                ip = self.run_command_remote_server(floating_ip, self.ssh_username,
                                                    self.ssh_password, cmd1)
                # print(ip.replace("\n", ""))
                self.fixed_ip_list.append(ip.replace("\n", ""))
                if vsm_server_type == "agent":
                    self.run_command_remote_server(floating_ip, self.ssh_username,
                                                   self.ssh_password, cmd2)

                if len(self.fixed_ip_list) == len(self.servers_name.split(",")):
                    ip_str = ",".join(self.fixed_ip_list)
                    CONF.set("vsm", ip_str)
                    i = 0
                    servers_name_list = self.servers_name.split(",")
                    while i < len(self.servers_name.split(",")):
                        if self.os_type == "ubuntu":
                            cmd = "echo \"%s  %s\" | sudo tee -a /etc/hosts" % (
                                self.fixed_ip_list[i], servers_name_list[i].strip(" ")
                            )
                        else:
                            cmd = "echo \"%s  %s\" | tee -a /etc/hosts" % (
                                self.fixed_ip_list[i], servers_name_list[i].strip(" ")
                            )
                        self.run_command_remote_server(floating_ip, self.ssh_username,
                                                       self.ssh_password, cmd)
                        i = i + 1
                    for ip in self.fixed_ip_list:
                        print_msg("INFO", "[-] create server",
                                  "[-] xtrust between controller and %s" % ip)
                        ssh = pexpect.spawn('ssh -t %s@%s \'ssh-copy-id %s\''
                                            % (self.ssh_username,
                                               floating_ip, ip))
                        ssh.expect("password")
                        ssh.sendline(self.ssh_password)
                        ssh.expect("yes/no")
                        ssh.sendline("yes")
                        ssh.expect("password")
                        ssh.sendline(self.ssh_password)
                        time.sleep(1)
                self.run_command_remote_server(floating_ip, self.ssh_username,
                                               self.ssh_password, cmd3)

                break
            else:
                wait_time = wait_time + 1
                continue
        if vsm_server_type == "agent":
            self.novaclient.servers.remove_floating_ip(server.id,floating_ip)

    def create_openstack_server(self, server_name, image_name, flavor_id, net_id_list,
                                security_group="default", key_name="demo-key",
                                floating_ip=None, vsm_ip_list=None, script_path=None):

        if not os.path.isfile(script_path):
            print_msg("ERROR", "[-] create openstack server", "[-] Script file does not exist")

        if not server_name:
            print_msg("ERROR", "[-] create openstack server", "[-] Server name is null")

        image = None
        if not image_name:
            print_msg("ERROR", "[-] create openstack server", "[-] Image name is null")
        else:
            image = self.image_available(image_name)

        flavor = None
        if not flavor_id:
            print_msg("ERROR", "[-] create openstack server", "[-] Flavor id is null")
        else:
            flavor = self.flavor_available(flavor_id)

        net = []
        if not net_id_list:
            print_msg("ERROR", "[-] create openstack server", "[-] Network id is null")
        else:
            for net_id in net_id_list:
                net.append(self.net_available(net_id))

        server_list = self.novaclient.servers.list()
        for server in server_list:
            if server.name == server_name:
                print_msg("INFO", "[-] create openstack server", "[-] Begin to delete %s" % server_name)
                self.novaclient.servers.delete(server.id)
                wait_time = 1
                while wait_time < self.timeout:
                    time.sleep(wait_time)
                    print_msg("INFO", "[-] create openstack server",
                              "[-] Waiting %s seconds to delete server %s" %
                              (wait_time, server_name))
                    server_list = self.novaclient.servers.list()
                    if server_name in [server.name for server in server_list]:
                        wait_time = wait_time + 1
                        continue
                    else:
                        break
                print_msg("INFO", "[-] create openstack server",
                          ingreen("[-] Old server %s has been deleted" % server_name))

        image_id = image.id

        nics = []
        for n in net:
            nics.append({"net-id": n.id})

        server = self.novaclient.servers.create(
            server_name,
            image_id,
            flavor.id,
            security_groups=[security_group],
            key_name=key_name,
            nics=nics
        )
        wait_time = 1
        while wait_time < 100:
            print_msg("INFO", "[-] create openstack server",
                      "[-] Waiting %s seconds to create server %s" %
                      (wait_time, server_name))
            time.sleep(wait_time)
            server = self.novaclient.servers.get(server.id)
            if server.status == "ACTIVE":
                print_msg("INFO", "[-] create openstack server",
                          ingreen("[-] The server " + server.name + " is active"))
                print_msg("INFO", "[-] create openstack server",
                          "[-] Begin to associate floating ip to server")
                while True:
                    try:
                        self.novaclient.servers.add_floating_ip(server.id, floating_ip)
                        ssh = pexpect.spawn('ssh -t %s@%s ls' %
                                            (self.vsm_openstack_ssh_username, floating_ip))
                        index = ssh.expect(["continue connecting", "password"])
                        if index == 0:
                            time.sleep(1)
                            ssh.sendline("yes")
                            time.sleep(1)
                            ssh.expect("password")
                            time.sleep(1)
                            ssh.sendline(self.vsm_openstack_ssh_password)
                        else:
                            time.sleep(1)
                            ssh.sendline(self.vsm_openstack_ssh_password)
                        break
                    except Exception:
                        time.sleep(5)
                        print_msg("INFO", "[-] create openstack server",
                                  "[-] Waiting 5 seconds to associate floating ip")
                        self.novaclient.servers.remove_floating_ip(server.id,floating_ip)
                print_msg("INFO", "[-] create openstack server",
                          "[-] End to associate floating ip to server")

                if self.vsm_openstack_ssh_username != self.ssh_username and \
                    self.vsm_openstack_ssh_username == "root":
                    cmd = "useradd intel -m -s /bin/bash"
                    time.sleep(5)
                    self.run_command_remote_server(floating_ip,
                                                   self.vsm_openstack_ssh_username,
                                                   self.vsm_openstack_ssh_password,
                                                   cmd)
                    ssh = pexpect.spawn('ssh -t %s@%s sudo passwd %s' %
                                        (self.vsm_openstack_ssh_username,
                                         floating_ip,
                                         self.ssh_username))
                    time.sleep(1)
                    ssh.expect("password")
                    time.sleep(1)
                    ssh.sendline(self.vsm_openstack_ssh_password)
                    time.sleep(1)
                    ssh.expect("password")
                    time.sleep(1)
                    ssh.sendline(self.ssh_password)
                    time.sleep(1)
                    ssh.expect("password")
                    time.sleep(1)
                    ssh.sendline(self.ssh_password)

                print_msg("INFO", "[-] create server",
                          "[-] Set NOPASSWD for user %s" % self.ssh_username)
                while True:
                    try:
                        if self.vsm_openstack_ssh_username != self.ssh_username and \
                                self.vsm_openstack_ssh_username == "root":
                            ssh = pexpect.spawn('ssh -t %s@%s \'echo "%s ALL=(ALL) NOPASSWD: ALL" '
                                                '| tee /etc/sudoers.d/%s\'' %
                                                (self.vsm_openstack_ssh_username,
                                                 floating_ip,
                                                 self.ssh_username,
                                                 self.ssh_username))
                        else:
                            ssh = pexpect.spawn(
                                'ssh -t %s@%s \'echo "%s ALL=(ALL) NOPASSWD: ALL" '
                                '| tee /etc/sudoers.d/%s\'' %
                                (self.vsm_openstack_ssh_username, floating_ip,
                                 self.vsm_openstack_ssh_username,
                                 self.vsm_openstack_ssh_username))
                        index = ssh.expect(["continue connecting", "password"])
                        if index == 0:
                            time.sleep(1)
                            ssh.sendline("yes")
                            time.sleep(1)
                            ssh.expect("password")
                            time.sleep(1)
                            ssh.sendline(self.vsm_openstack_ssh_password)
                        else:
                            time.sleep(1)
                            ssh.sendline(self.vsm_openstack_ssh_password)
                        if self.vsm_openstack_ssh_username != "root":
                            ssh.expect("password")
                            ssh.sendline(self.vsm_openstack_ssh_password)
                        break
                    except Exception:
                        print_msg("INFO", "[-] create openstack server",
                                  "[-] Waiting for 10 seconds that "
                                  "floating ip is not ready...")
                        time.sleep(10)

                if self.vsm_openstack_ssh_username != self.ssh_username and \
                    self.vsm_openstack_ssh_username == "root":
                    cmd = "chmod 0440 /etc/sudoers.d/%s" % self.ssh_username
                else:
                    cmd = "chmod 0440 /etc/sudoers.d/%s" % self.vsm_openstack_ssh_username

                self.run_command_remote_server(
                    floating_ip, self.vsm_openstack_ssh_username,
                    self.vsm_openstack_ssh_password, cmd)

                while True:
                    try:
                        if self.vsm_openstack_ssh_username != self.ssh_username and \
                            self.vsm_openstack_ssh_username == "root":
                            print_msg("INFO", "[-] create openstack server",
                                      "[-] Generate ssh-key for user %s" % self.ssh_username)
                            ssh = pexpect.spawn('ssh -t %s@%s \'ssh-keygen -t rsa\''
                                                % (self.ssh_username, floating_ip))
                            ssh.expect("password")
                            ssh.sendline(self.ssh_password)
                        else:
                            print_msg("INFO", "[-] create openstack server",
                                      "[-] Generate ssh-key for user %s" % self.vsm_openstack_ssh_username)
                            ssh = pexpect.spawn('ssh -t %s@%s \'ssh-keygen -t rsa\''
                                                % (self.vsm_openstack_ssh_username, floating_ip))
                            ssh.expect("password")
                            ssh.sendline(self.vsm_openstack_ssh_password)
                        ssh.expect("Enter file")
                        ssh.sendline("")
                        ssh.expect("Enter passphrase")
                        ssh.sendline("")
                        ssh.expect("Enter same passphrase")
                        ssh.sendline("")
                        break
                    except Exception:
                        print_msg("WARNING", "[-] create openstack server",
                                  "[-] connecting to %s failed, wait for 5 seconds" % floating_ip)
                        time.sleep(5)

                cmd1 = "ifconfig |grep broadcast| awk -F \" \" " \
                       "'{print $2}'"

                ip = self.run_command_remote_server(floating_ip, self.vsm_openstack_ssh_username,
                                                    self.vsm_openstack_ssh_password, cmd1)
                ip = ip.replace("\n", "")
                openstack_hostname = self.run_command_remote_server(
                    floating_ip, self.vsm_openstack_ssh_username,
                    self.vsm_openstack_ssh_password, "hostname").replace("\n", "")

                for vsm_ip in vsm_ip_list:
                    print_msg("INFO", "[-] create openstack server",
                              "[-] echo %s %s to %s /etc/hosts" % (ip, openstack_hostname, vsm_ip))
                    cmd = "ssh -t %s 'echo \"%s  %s\" | sudo tee -a /etc/hosts'" \
                          % (vsm_ip, ip, openstack_hostname)
                    self.run_command_remote_server(self.floating_ip,
                                                   self.ssh_username,
                                                   self.ssh_password,
                                                   cmd)

                    print_msg("INFO", "[-] create openstack server",
                              "[-] xtrust between %s and %s" % (vsm_ip, ip))
                    if self.vsm_openstack_ssh_username != self.ssh_username and \
                        self.vsm_openstack_ssh_username == "root":
                        ssh = pexpect.spawn('ssh -t %s@%s \'ssh -t %s ssh-copy-id %s\''
                                            % (self.ssh_username,
                                               self.floating_ip, vsm_ip, ip))
                    else:
                        ssh = pexpect.spawn('ssh -t %s@%s \'ssh -t %s ssh-copy-id %s@%s\''
                                            % (self.ssh_username,
                                               self.floating_ip, vsm_ip,
                                               self.vsm_openstack_ssh_username, ip))
                    ssh.expect("password")
                    ssh.sendline(self.ssh_password)
                    ssh.expect("yes/no")
                    ssh.sendline("yes")
                    ssh.expect("password")
                    ssh.sendline(self.vsm_openstack_ssh_password)
                    time.sleep(1)

                print_msg("INFO", "[-] create openstack server",
                          "[-] xtrust between %s and %s" % (self.floating_ip, openstack_hostname))
                ssh = pexpect.spawn('ssh -t %s@%s \'ssh-copy-id %s@%s\''
                                    % (self.ssh_username,
                                       self.floating_ip,
                                       self.vsm_openstack_ssh_username,
                                       openstack_hostname))
                ssh.expect("password")
                ssh.sendline(self.ssh_password)
                ssh.expect("yes/no")
                ssh.sendline("yes")
                ssh.expect("password")
                ssh.sendline(self.vsm_openstack_ssh_password)

                self.run_command_remote_server(floating_ip,
                                               self.vsm_openstack_ssh_username,
                                               self.vsm_openstack_ssh_password,
                                               "sed -i \"s/192.168.1.54 controller/%s controller/g\" /etc/hosts" % ip)

                if self.vsm_openstack_ssh_username != self.ssh_username and \
                    self.vsm_openstack_ssh_username == "root":
                    ssh = pexpect.spawn('ssh -t %s@%s \'ssh-copy-id %s@%s\''
                                        % (self.ssh_username,
                                           floating_ip,
                                           self.ssh_username,
                                           openstack_hostname))
                    ssh.expect("password")
                    ssh.sendline(self.ssh_password)
                    ssh.expect("yes/no")
                    ssh.sendline("yes")
                    ssh.expect("password")
                    ssh.sendline(self.ssh_password)
                else:
                    ssh = pexpect.spawn('ssh -t %s@%s \'ssh-copy-id %s@%s\''
                                        % (self.vsm_openstack_ssh_username,
                                           floating_ip,
                                           self.vsm_openstack_ssh_username,
                                           openstack_hostname))
                    ssh.expect("password")
                    ssh.sendline(self.vsm_openstack_ssh_password)
                    ssh.expect("yes/no")
                    ssh.sendline("yes")
                    ssh.expect("password")
                    ssh.sendline(self.vsm_openstack_ssh_password)

                if self.vsm_openstack_ssh_username != self.ssh_username and \
                    self.vsm_openstack_ssh_username == "root":
                    ssh = pexpect.spawn('ssh -t %s@%s \'ssh-copy-id %s@%s\''
                                        % (self.ssh_username,
                                           floating_ip,
                                           self.ssh_username,
                                           ip))
                    ssh.expect("password")
                    ssh.sendline(self.ssh_password)
                    # ssh.expect("yes/no")
                    # ssh.sendline("yes")
                else:
                    ssh = pexpect.spawn('ssh -t %s@%s \'ssh-copy-id %s@%s\''
                                        % (self.vsm_openstack_ssh_username,
                                           floating_ip,
                                           self.vsm_openstack_ssh_username,
                                           ip))
                    ssh.expect("password")
                    ssh.sendline(self.vsm_openstack_ssh_password)
                    # ssh.expect("yes/no")
                    # ssh.sendline("yes")
                print("+++++++++++++++++++++here")

                localpath = CONF.get("vsm", "vsm_openstack_script_path")
                localfile = localpath.split("/")[-1]
                remotepath = "/tmp/" + localfile
                while True:
                    try:
                        t = paramiko.Transport(floating_ip, 22)
                        t.connect(username=self.vsm_openstack_ssh_username,
                                  password=self.vsm_openstack_ssh_password)
                        sftp = paramiko.SFTPClient.from_transport(t)
                        sftp.put(localpath, remotepath)
                        print_msg("INFO", "[-] create openstack server",
                                  "[-] transport script to openstack node")
                        t.close()
                        break
                    except Exception:
                        time.sleep(5)
                        print_msg("INFO", "[-] create openstack server",
                                  "[-] waiting the openstack server is active!")

                self.run_command_remote_server(floating_ip,
                                               self.vsm_openstack_ssh_username,
                                               self.vsm_openstack_ssh_password,
                                               "chmod 755 /tmp/%s;cd /tmp;./%s" %
                                               (localfile, localfile))
                while True:
                    try:
                        ssh = pexpect.spawn('ssh -t %s@%s ls' %
                                            (self.vsm_openstack_ssh_username, floating_ip))
                        index = ssh.expect(["continue connecting", "password"])
                        if index == 0:
                            time.sleep(1)
                            ssh.sendline("yes")
                            time.sleep(1)
                            ssh.expect("password")
                            time.sleep(1)
                            ssh.sendline(self.vsm_openstack_ssh_password)
                        else:
                            time.sleep(1)
                            ssh.sendline(self.vsm_openstack_ssh_password)
                        print_msg("INFO", "[-] create openstack server",
                                  "[-] the openstack server is running")
                        break
                    except Exception:
                        time.sleep(5)
                        print_msg("INFO", "[-] create openstack server",
                                  "[-] Waiting 5 seconds to wait the openstack "
                                  "server is running")
                break
            else:
                wait_time = wait_time + 1
                continue


class DeployVSM(object):
    """

    """

    def __init__(self):
        self.vsm_pakcage_path = CONF.get("vsm", "vsm_release_package_path")
        self.floating_ip = CONF.get("vsm", "floating_ip")
        self.ssh_username = CONF.get("vsm", "ssh_username")
        self.ssh_password = CONF.get("vsm", "ssh_password")

    def deploy_vsm(self, fixed_ip_list):
        print_msg("WARNING", "[-] create server",
                  "[-] Be sure that you have vsm release "
                  "package under the folder tools")
        time.sleep(3)
        vsm_pakcage_path = self.vsm_pakcage_path
        os.system("tar -zxvf %s" % vsm_pakcage_path)
        vsm_package = vsm_pakcage_path.split("/")[-1]
        vsm_release_path = ".".join(vsm_package.split(".")[0:3])
        controller_ip = fixed_ip_list[-1]
        agent_ip_list = " ".join(fixed_ip_list[0:-1])
        os.system("echo '\nCONTROLLER_ADDRESS=\"%s\"'|tee -a %s" % (
            controller_ip, vsm_release_path + "/installrc"
        ))
        os.system("echo 'AGENT_ADDRESS_LIST=\"%s\"'|tee -a %s" % (
            agent_ip_list, vsm_release_path + "/installrc"
        ))
        os.system("sed -i \"/sleep 5/aexport https_proxy="
                  "http:\/\/proxy-shz.intel.com:911\" %s" %
                  vsm_release_path + "/install.sh")

        net = ".".join(fixed_ip_list[0].split(".")[0:3]) + ".0"
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
        for agent_ip in fixed_ip_list[0:-1]:
            server_manifest_path = vsm_release_path + "/manifest/" + agent_ip
            os.system("mkdir -p %s" % server_manifest_path)
            os.system("cp %s %s" % (server_manifest_example_path,
                                    server_manifest_path + "/server.manifest"))
        os.system("tar -czvf %s %s" % (vsm_package, vsm_release_path))

        print_msg("INFO", "[-] deploy vsm", "[-] waiting the controller server is active!")
        time.sleep(5)

        while True:
            try:
                t = paramiko.Transport(self.floating_ip, 22)
                t.connect(username=self.ssh_username,
                          password=self.ssh_password)
                sftp = paramiko.SFTPClient.from_transport(t)
                localpath = vsm_package
                remotepath = "/tmp/" + vsm_package
                sftp.put(localpath, remotepath)
                print_msg("INFO", "[-] deploy vsm", "[-] transport vsm package to controller")
                t.close()
                break
            except Exception:
                time.sleep(5)
                print_msg("INFO", "[-] deploy vsm", "[-] waiting the controller server is active!")

        s = paramiko.SSHClient()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.connect(self.floating_ip, port=22,
                  username=self.ssh_username,
                  password=self.ssh_password)
        print_msg("INFO", "[-] deploy vsm",
                  "[-] Begin to install vsm, please wait for a few minutes!")
        print_msg("INFO", "[-] deploy vsm",
                  "[-] Install controller %s ..." % controller_ip)
        stdin, stdout, stderr = s.exec_command("cd /tmp;tar -zxvf %s;cd %s;"
                                               "./install.sh -v 2.0 -u %s "
                                               "--prepare --controller %s"
                                               % (vsm_package, vsm_release_path,
                                                  self.ssh_username,
                                                  controller_ip))
        print_msg("INFO", "[-] deploy vsm", "[-] out: " + stdout.read())
        print_msg("INFO", "[-] deploy vsm", "[-] err: " + stderr.read())

        for ip in fixed_ip_list[0:-1]:
            print_msg("INFO", "[-] deploy vsm",
                      "[-] Install agent %s ..." % ip)
            stdin, stdout, stderr = s.exec_command("cd /tmp/%s;"
                                                   "./install.sh -v 2.0 -u %s "
                                                   "--agent %s"
                                                   % (vsm_release_path,
                                                      self.ssh_username,
                                                      ip))
            print_msg("INFO", "[-] create server", "[-] out: " + stdout.read())
            print_msg("INFO", "[-] create server", "[-] err: " + stderr.read())

        s.close()

    def config_tempest(self):
        t = paramiko.Transport((self.floating_ip, 22))
        t.connect(username=self.ssh_username, password=self.ssh_password)
        sftp = paramiko.SFTPClient.from_transport(t)
        if self.ssh_username == "root":
            remotepath = "/root/keyrc"
        else:
            remotepath = "/home/%s/keyrc" % self.ssh_username
        localpath = "/tmp/keyrc"
        sftp.get(remotepath, localpath)
        t.close()

        def _replaceInFile(file, oldstr, newstr):
            for line in fileinput.input(file, inplace=True):
                if re.search(oldstr, line):
                    line = line.replace(oldstr, newstr)
                print line,

        cwd = os.getcwd()
        tempest_conf = "%s/etc/tempest.conf" % cwd
        os.system(
            "sed -i \"s/^admin_tenant_name = *.*/#admin_tenant_name = "
            "<None>/g\" %s" % tempest_conf)
        os.system(
            "sed -i \"s/^admin_username = *.*/#admin_username = "
            "<None>/g\" %s" % tempest_conf)
        os.system(
            "sed -i \"s/^admin_password = *.*/#admin_password = "
            "<None>/g\" %s" % tempest_conf)
        os.system(
            "sed -i \"s/^uri = *.*/#uri = <None>/g\" %s" % tempest_conf)
        os.system(
            "sed -i \"s/api_v3 = false/#api_v3 = true/g\" %s" % tempest_conf)

        file = open("/tmp/keyrc")
        line = file.readline()
        if line:
            os_tenant_name = line.strip("\n").split(" ")[1].split("=")[1]
            _replaceInFile(tempest_conf,
                           "#admin_tenant_name = <None>",
                           "admin_tenant_name = %s" % os_tenant_name)
        line = file.readline()
        if line:
            os_username = line.strip("\n").split(" ")[1].split("=")[1]
            _replaceInFile(tempest_conf,
                           "#admin_username = <None>",
                           "admin_username = %s" % os_username)
        line = file.readline()
        if line:
            os_password = line.strip("\n").split(" ")[1].split("=")[1]
            _replaceInFile(tempest_conf,
                           "#admin_password = <None>",
                           "admin_password = %s" % os_password)
        line = file.readline()
        if line:
            os_auth_url = line.strip("\n").split(" ")[1].split("=")[1]
            _replaceInFile(tempest_conf,
                           "#uri = <None>",
                           "uri = %s" % os_auth_url)
        _replaceInFile(tempest_conf,
                       "#api_v3 = true",
                       "api_v3 = false")

    def clean_data(self):
        vsm_release = self.vsm_pakcage_path.split("/")[-1][:-7]
        s = paramiko.SSHClient()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.connect(self.floating_ip, port=22,
                  username=self.ssh_username, password=self.ssh_password)

        stdin, stdout, stderr = s.exec_command("sudo clean-data -f")
        stdout.read()
        stdin, stdout, stderr = s.exec_command("agent-token")
        token_id = stdout.read().strip("\n")

        cmd = "for ip in `source /tmp/%s/installrc;echo $AGENT_ADDRESS_LIST`; do " \
              "ssh -t $ip 'sudo replace-str %s; sudo clean-data -f;" \
              "sudo service vsm-agent restart;" \
              "sudo service vsm-physical restart'; done" % (vsm_release, token_id)
        stdin, stdout, stderr = s.exec_command(cmd)
        stdout.read()
        s.close()

        os.system("sudo rm -rf /tmp/keyrc")
        t = paramiko.Transport((self.floating_ip, 22))
        t.connect(username=self.ssh_username, password=self.ssh_password)
        sftp = paramiko.SFTPClient.from_transport(t)
        if self.ssh_username == "root":
            remotepath = "/root/keyrc"
        else:
            remotepath = "/home/%s/keyrc" % self.ssh_username
        localpath = "/tmp/keyrc"
        sftp.get(remotepath, localpath)
        t.close()

        def _replaceInFile(file, oldstr, newstr):
            for line in fileinput.input(file, inplace=True):
                if re.search(oldstr, line):
                    line = line.replace(oldstr, newstr)
                print line,

        cwd = os.getcwd()
        tempest_conf = "%s/etc/tempest.conf" % cwd
        os.system(
            "sed -i \"s/^admin_password = *.*/#admin_password = "
            "<None>/g\" %s" % tempest_conf)

        file = open("/tmp/keyrc")
        file.readline()
        file.readline()
        line = file.readline()
        if line:
            os_password = line.strip("\n").split(" ")[1].split("=")[1]
            _replaceInFile(tempest_conf,
                           "#admin_password = <None>",
                           "admin_password = %s" % os_password)


def main():
    try:
        new_server = CONF.get("vsm", "new_server")
    except Exception:
        print_msg("WARNING", "[-] vsm_env", "[-] Not found new_server in "
                                            "tempest.conf, Be sure that "
                                            "you have an exist cluster")
        time.sleep(3)
        new_server = ""
    if new_server == "True":
        # identity info
        username = CONF.get("vsm", "openstack_username")
        password = CONF.get("vsm", "openstack_password")
        tenant_name = CONF.get("vsm", "openstack_tenant_name")
        uri = CONF.get("vsm", "openstack_auth_uri")
        auth_version = CONF.get("vsm", "openstack_auth_version")
        auth_url = uri + "/" + auth_version
        region_name = CONF.get("vsm", "openstack_region")

        image_name = CONF.get("vsm", "image_name")
        flavor_id = CONF.get("vsm", "flavor_id")
        net_id = CONF.get("vsm", "net_id")
        volumes_name = CONF.get("vsm", "volumes_name")
        volume_size = CONF.get("vsm", "volume_size")
        osd_count = int(CONF.get("vsm", "osd_count"))
        agent_servers_name = CONF.get("vsm", "agent_servers_name")
        controller_server_name = CONF.get("vsm", "controller_server_name")
        security_group = CONF.get("vsm", "security_group")
        key_name = CONF.get("vsm", "key_name")
        floating_ip = CONF.get("vsm", "floating_ip")

        os_type = CONF.get("vsm", "os_type")
        ssh_username = CONF.get("vsm", "ssh_username")
        if os_type.lower() == "centos" and ssh_username != "root":
            print_msg("ERROR", "[-]", "[-] If your os is centos, please use root to login!")

        print("Apply new servers and deploy a vsm env")
        apply_servers = ApplyServers(username, password, tenant_name,
                                     auth_url, region_name)

        if not volumes_name:
            print_msg("ERROR", "[-]",
                      "[-] Volumes name is null, please check "
                      "your volumes name in tempest.conf file")
        volumes_name_list = volumes_name.split(",")
        if not agent_servers_name:
            print_msg("ERROR", "[-] create server",
                      "[-] Servers name is null, please check "
                      "your servers name in tempest.conf file")
        servers_name_list = agent_servers_name.split(",")
        if len(volumes_name_list) != len(servers_name_list) * 2:
            print_msg("ERROR", "[-] create server",
                      "[-] Please check the volumes name and "
                      "servers name in tempest.conf file")

        for server_name in servers_name_list:
            volumes_list = []
            osd_count_new = osd_count
            while osd_count_new > 0:
                volumes_list.append(volumes_name_list.pop(0))
                volumes_list.append(volumes_name_list.pop(0))
                osd_count_new = osd_count_new - 1
            server_name = server_name.strip(" ")
            apply_servers.create_server(
                server_name, image_name, flavor_id, net_id,
                security_group=security_group,
                key_name=key_name,
                floating_ip=floating_ip,
                volume_size=volume_size,
                volumes_list=volumes_list,
                vsm_server_type="agent"
            )
        # create vsm controller server
        apply_servers.create_server(
            controller_server_name, image_name, flavor_id, net_id,
            security_group=security_group,
            key_name=key_name,
            floating_ip=floating_ip,
            volume_size=None,
            volumes_list=None,
            vsm_server_type="controller"
        )

        # create openstack server
        vsm_openstack_server_name = CONF.get("vsm", "vsm_openstack_server_name")
        vsm_openstack_floating_ip = CONF.get("vsm", "vsm_openstack_floating_ip")
        vsm_openstack_image_name = CONF.get("vsm", "vsm_openstack_image_name")
        vsm_openstack_flavor_id = CONF.get("vsm", "vsm_openstack_flavor_id")
        vsm_openstack_net_id_list = CONF.get("vsm", "vsm_openstack_net_id_list")
        vsm_openstack_net_id_list = vsm_openstack_net_id_list.split(",")
        vsm_openstack_script_path = CONF.get("vsm", "vsm_openstack_script_path")
        apply_servers.create_openstack_server(vsm_openstack_server_name,
                                              vsm_openstack_image_name,
                                              vsm_openstack_flavor_id,
                                              vsm_openstack_net_id_list,
                                              security_group="default",
                                              key_name="demo-key",
                                              floating_ip=vsm_openstack_floating_ip,
                                              vsm_ip_list=apply_servers.fixed_ip_list,
                                              script_path=vsm_openstack_script_path)

        deploy_vsm = DeployVSM()
        deploy_vsm.deploy_vsm(apply_servers.fixed_ip_list)
        deploy_vsm.config_tempest()
    elif new_server == "False":
        print_msg("INFO", "[-] create server", "[-] clean the vsm env data")
        deploy_vsm = DeployVSM()
        deploy_vsm.clean_data()
    elif new_server == "" or new_server == None:
        print_msg("INFO", "[-]", "[-] Using an exist vsm cluster")
    else:
        print_msg("ERROR", "[-] vsm_env", inred("[-] Please set True or False or "
                                                "leave blank to new_server in tempest.conf"))

if __name__ == "__main__":
    main()