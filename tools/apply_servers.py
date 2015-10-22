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
import time

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


def error(msg):
    print('---------------ERROR----------------')
    print('------------------------------------')
    if isinstance(msg, list):
        for n in msg:
            print(n)
    else:
        print(msg)
    print('------------------------------------')
    sys.exit(1)


class ApplyServers(object):
    """

    """
    def __init__(self):
        self.uri = CONF.get("vsm", "openstack_auth_uri")
        self.auth_version = CONF.get("vsm", "openstack_auth_version")
        self.auth_url = self.uri + "/" + self.auth_version
        self.region = CONF.get("vsm", "openstack_region")
        self.admin_username = CONF.get("vsm", "openstack_username")
        self.admin_tenant_name = CONF.get("vsm", "openstack_tenant_name")
        self.admin_password = CONF.get("vsm", "openstack_password")
        self.vsm_release_package_path = CONF.get("vsm",
                                                 "vsm_release_package_path")

        self.novaclient = nc_client.Client(
            self.admin_username,
            self.admin_password,
            self.admin_tenant_name,
            self.auth_url,
            region_name=self.region
        )

        self.cinderclient = cc_client.Client(
            self.admin_username,
            self.admin_password,
            self.admin_tenant_name,
            self.auth_url,
            region_name=self.region
        )

        self.image_name = CONF.get("vsm", "image_name")
        self.flavor_id = CONF.get("vsm", "flavor_id")
        self.volumes_name = CONF.get("vsm", "volumes_name")
        self.volume_size = CONF.get("vsm", "volume_size")
        self.net_id = CONF.get("vsm", "net_id")
        self.servers_name = CONF.get("vsm", "servers_name")
        self.security_group = CONF.get("vsm", "security_group")
        self.key_name = CONF.get("vsm", "key_name")
        self.floating_ip = CONF.get("vsm", "floating_ip")

        self.ssh_username = CONF.get("vsm", "ssh_username")
        self.ssh_password = CONF.get("vsm", "ssh_password")
        self.ip_list = []

    def image_available(self, image_name):
        """

        :param image_name:
        :return:
        """
        if not image_name:
            error("No image name, please check your image_name "
                  "in tempest.conf or config.py file")

        images_list = self.novaclient.images.list()
        if image_name in [image.name for image in images_list]:
            print("The image is available")
        else:
            error("Not found the image %s" % image_name)

    def flavor_available(self, flavor_id):
        """

        :param flavor_id:
        :return:
        """
        if not flavor_id:
            error("No flavor id, please check your flavor "
                  "id in tempest.conf or config.py file")

        flavor_list = self.novaclient.flavors.list()
        if flavor_id in [flavor.id for flavor in flavor_list]:
            print("The flavor is available")
        else:
            error("Not found the flavor id %s" % flavor_id)

    def net_available(self, net_id):
        """

        :param net_id:
        :return:
        """
        if not net_id:
            error("No network id, please check your flavor "
                  "id in tempest.conf or config.py file")

        net_list = self.novaclient.networks.list()
        if net_id in [net.id for net in net_list]:
            print("The net is available")
        else:
            error("Not found the net id %s" % net_id)

    def volume_available(self, volume_name):
        """

        :param volume_name:
        :return:
        """
        volumes_list = self.cinderclient.volumes.list()
        for volume in volumes_list:
            if volume_name == volume.name:
                print("The volume is available")
                return volume
        print("Not found the volume %s" % volume_name)
        print("Creating the volume %s" % volume_name)
        volume = self.create_volume(volume_name, self.volume_size)
        count = 1
        while volume.status != "available":
            if count < 6:
                time.sleep(count)
                count = count + 1
                continue
            else:
                print("The volume %s is still not available, "
                      "please check by yourself" % volume_name)
                break
        return volume

    def create_volume(self, name, size):
        """

        :param name:
        :param size:
        :return:
        """
        self.cinderclient.volumes.create(size, display_name=name)
        time.sleep(2)
        volumes = self.cinderclient.volumes.list()
        for volume in volumes:
            if name == volume.name:
                return volume

    def create_server(self, server_name, image_name, flavor_id, net_id,
                      security_group="default", key_name="demo-key",
                      floating_ip=None, volume_list=None):
        """

        :param server_name:
        :param image_name:
        :param flavor_id:
        :param net_id:
        :param security_group:
        :param key_name:
        :return:
        """
        if not server_name:
            print("server name is null")
            sys.exit(1)
        if not image_name:
            print("image name is null")
            sys.exit(1)
        if not flavor_id:
            print("flavor id is null")
            sys.exit(1)
        if not net_id:
            print("network id is null")
            sys.exit(1)
        server_list = self.novaclient.servers.list()
        for server in server_list:
            if server.name == server_name:
                print("Begin to delete %s" % server_name)
                self.novaclient.servers.delete(server.id)
                count = 1
                while count < 100:
                    time.sleep(count)
                    print("waiting %s seconds to delete server %s" %
                          (count, server_name))
                    server_list = self.novaclient.servers.list()
                    if server_name in [server.name for server in server_list]:
                        count = count + 1
                        continue
                    else:
                        print("the old server has been deleted")
                        break
                print("End to delete")
        images_list = self.novaclient.images.list()
        image_id = None
        for image in images_list:
            if image_name == image.name:
                image_id = image.id
        server = self.novaclient.servers.create(
            server_name,
            image_id,
            flavor_id,
            security_groups=[security_group],
            key_name=key_name,
            nics=[{"net-id": net_id}]
        )
        count = 1
        while count < 100:
            print("waiting %s seconds to create server %s" %
                  (count, server_name))
            time.sleep(count)
            server = self.novaclient.servers.get(server.id)
            if server.status == "ACTIVE":
                print("The server is active")
                print("Begin to associate floating ip to server")
                self.novaclient.servers.add_floating_ip(server.id, floating_ip)
                print("End to associate floating ip to server")
                print("Begin to attach volume")
                for volume_name in volume_list:
                    volume = self.volume_available(volume_name)
                    self.novaclient.volumes.create_server_volume(
                        server.id,
                        volume.id,
                        None
                    )
                print("End to attach volume")

                print("Set NOPASSWD for user %s" % self.ssh_username)
                # self.config_server(self.floating_ip,
                #                    "echo \"%s ALL=(ALL) NOPASSWD: ALL\" | "
                #                    "sudo tee /etc/sudoers.d/%s"
                #                    % (self.ssh_username, self.ssh_username),
                #                    self.ssh_password)
                flag = True
                while flag:
                    try:
                        ssh = pexpect.spawn(
                            'ssh -t %s@%s \'echo "%s ALL=(ALL) NOPASSWD: ALL" '
                            '| sudo tee /etc/sudoers.d/%s\'' %
                            (self.ssh_username, self.floating_ip,
                             self.ssh_username, self.ssh_username))
                        ssh.expect("password")
                        ssh.sendline(self.ssh_password)
                        ssh.expect("password")
                        ssh.sendline(self.ssh_password)
                        flag = False
                    except Exception:
                        print("Waiting for 10 seconds that "
                              "floating ip is not ready...")
                        time.sleep(10)

                self.config_server(self.floating_ip,
                                   "sudo chmod 0440 /etc/sudoers.d/%s"
                                   % self.ssh_username)
                print("Generate ssh-key for user %s" % self.ssh_username)
                ssh = pexpect.spawn('ssh -t %s@%s \'ssh-keygen -t rsa\''
                                    % (self.ssh_username, self.floating_ip))
                ssh.expect("password")
                ssh.sendline(self.ssh_password)
                print(1)
                ssh.expect("Enter file")
                ssh.sendline("")
                print(2)
                ssh.expect("Enter passphrase")
                ssh.sendline("")
                print(3)
                ssh.expect("Enter same passphrase")
                ssh.sendline("")

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
                ip = self.config_server(floating_ip, cmd1)
                print(ip.replace("\n", ""))
                self.ip_list.append(ip.replace("\n", ""))
                self.config_server(floating_ip, cmd2)

                if len(self.ip_list) == len(self.servers_name.split(",")):
                    ip_str = ",".join(self.ip_list)
                    CONF.set("vsm", ip_str)
                    i = 0
                    servers_name_list = self.servers_name.split(",")
                    while i < len(self.servers_name.split(",")):
                        cmd = "echo \"%s  %s\" | sudo tee -a /etc/hosts" % (
                            self.ip_list[i], servers_name_list[i].strip(" ")
                        )
                        self.config_server(floating_ip, cmd)
                        i = i + 1
                    for ip in self.ip_list:
                        print("xtrust between controller and %s" % ip)
                        ssh = pexpect.spawn('ssh -t %s@%s \'ssh-copy-id %s\''
                                            % (self.ssh_username,
                                               self.floating_ip, ip))
                        ssh.expect("password")
                        ssh.sendline(self.ssh_password)
                        ssh.expect("yes/no")
                        ssh.sendline("yes")
                        ssh.expect("password")
                        ssh.sendline(self.ssh_password)
                        time.sleep(1)
                self.config_server(floating_ip, cmd3)

                break
            else:
                count = count + 1
                continue

    def attach_volume_to_server(self, volume_id, server_id):
        return

    def config_server(self, ip, cmd):
        hostname_or_ip = ip
        port = 22
        username = self.ssh_username
        password = self.ssh_password
        print(hostname_or_ip, port, username, password)

        s = paramiko.SSHClient()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.connect(hostname_or_ip, port=port, username=username,
                  password=password)
        stdin, stdout, stderr = s.exec_command(cmd)
        result = stdout.read()
        s.close()
        return result


if __name__ == "__main__":
    apply_servers = ApplyServers()
    apply_servers.image_available(apply_servers.image_name)
    apply_servers.flavor_available(apply_servers.flavor_id)
    apply_servers.net_available(apply_servers.net_id)

    if not apply_servers.volumes_name:
        error("No volumes name, please check your "
              "flavor id in tempest.conf or config.py file")
    volumes_name = apply_servers.volumes_name
    volumes = volumes_name.split(",")

    servers_name_list = apply_servers.servers_name.split(",")
    if len(volumes) != len(servers_name_list) * 2:
        error("Please check the volume config "
              "each agent has two volumes!")
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
                                    [volumes.pop(0), volumes.pop(0)])
    print(apply_servers.ip_list)