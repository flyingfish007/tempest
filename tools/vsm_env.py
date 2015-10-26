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


def error(msg):
    print('---------------ERROR----------------')
    print('------------------------------------')
    if isinstance(msg, list):
        for n in msg:
            print(inred(n))
    else:
        print(inred(msg))
    print('------------------------------------')
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
        self.servers_name = CONF.get("vsm", "servers_name")
        self.ssh_username = CONF.get("vsm", "ssh_username")
        self.ssh_password = CONF.get("vsm", "ssh_password")
        self.novaclient = nc_client.Client(
            username, password, tenant_name, auth_url,
            region_name=region_name)
        self.cinderclient = cc_client.Client(
            username, password, tenant_name, auth_url,
            region_name=region_name)
        self.fixed_ip_list = []

    def image_available(self, image_name):
        """

        :param image_name
        :type: string
        :return: image
        :rtype: object
        """
        if not image_name:
            error("Image name is null, please check your image_name "
                  "in tempest.conf file")

        print("Check image %s is available or not" % image_name)
        images_list = self.novaclient.images.list()
        for image in images_list:
            if image_name == image.name and image.status == "ACTIVE":
                print("The image " + ingreen(image_name) + " is available")
                return image
        error("Not found the image name " + inred(image_name))

    def flavor_available(self, flavor_id):
        """

        :param flavor_id
        :type: string
        :return: flavor
        :rtype: object
        """
        if not flavor_id:
            error("Flavor id is null, please check your flavor id "
                  "in tempest.conf file")

        print("Check flavor id %s is available or not" % flavor_id)
        flavors_list = self.novaclient.flavors.list()
        for flavor in flavors_list:
            if flavor_id == flavor.id:
                flavor_name = flavor.name
                print("The flavor " + ingreen(flavor_name) + " is available")
                return flavor
        error("Not found the flavor id " + inred(flavor_id))

    def net_available(self, net_id):
        """

        :param net_id
        :type: string
        :return: net
        :rtype: object
        """
        if not net_id:
            error("Network id is null, please check your net id "
                  "in tempest.conf file")

        print("Check net id %s is available or not" % net_id)
        nets_list = self.novaclient.networks.list()
        for net in nets_list:
            if net_id == net.id:
                net_name = net.label
                print("The net " + ingreen(net_name) +" is available")
                return net
        error("Not found the net id " + inred(net_id))

    def volume_available(self, volume_name, volume_size):
        """

        :param volume_name
        :type: string
        :return: volume
        :rtype: object
        """
        volumes_list = self.cinderclient.volumes.list()
        for volume in volumes_list:
            if volume_name == volume.name:
                print("The volume " + ingreen(volume_name) + " is available")
                return volume
        print("Not found the volume " + inred(volume_name))
        print("Creating the volume %s" % volume_name)
        volume = self.create_volume(volume_name, volume_size)
        return volume

    def create_volume(self, volume_name, volume_size):
        """

        :param volume_name
        :type: string
        :param volume_size
        :type: int
        :return volume
        :rtype: object
        """
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
        error("The volume " + inred(volume_name) + " is still not available, "
              "please check volume by yourself")

    def run_command_remote_server(self, ip, cmd):
        """

        :param ip
        :type: string
        :param cmd
        :type: string
        :return
        :rtype: string
        """
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

    def create_server(self, server_name, image_name, flavor_id, net_id,
                      security_group="default", key_name="demo-key",
                      floating_ip=None, volume_size=None, volumes_list=None):
        """

        :param str server_name: Server Name
        :param str image_name: Image Name
        :param str flavor_id: Flavor ID
        :param str net_id: Network ID
        :param str security_group: Security Group
        :param key name
        :type: string
        :param floating ip
        :type: string
        :param volume size
        :type: int
        :param volume list
        :type: list
        :return
        :rtype
        """
        if not server_name:
            error("Server name is null")

        image = None
        if not image_name:
            error("Image name is null")
        else:
            image = self.image_available(image_name)

        flavor = None
        if not flavor_id:
            error("Flavor id is null")
        else:
            flavor = self.flavor_available(flavor_id)

        net = None
        if not net_id:
            error("Network id is null")
        else:
            net = self.net_available(net_id)

        server_list = self.novaclient.servers.list()
        for server in server_list:
            if server.name == server_name:
                print("Begin to delete %s" % server_name)
                self.novaclient.servers.delete(server.id)
                wait_time = 1
                while wait_time < self.timeout:
                    time.sleep(wait_time)
                    print("Waiting %s seconds to delete server %s" %
                          (wait_time, server_name))
                    server_list = self.novaclient.servers.list()
                    if server_name in [server.name for server in server_list]:
                        wait_time = wait_time + 1
                        continue
                    else:
                        break
                print("Old server %s has been deleted" % server_name)

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
            print("Waiting %s seconds to create server %s" %
                  (wait_time, server_name))
            time.sleep(wait_time)
            server = self.novaclient.servers.get(server.id)
            if server.status == "ACTIVE":
                print("The server " + ingreen(server.name) + " is active")
                print("Begin to associate floating ip to server")
                self.novaclient.servers.add_floating_ip(server.id, floating_ip)
                print("End to associate floating ip to server")
                print("Begin to attach volume")
                for volume_name in volumes_list:
                    volume = self.volume_available(volume_name, volume_size)
                    self.novaclient.volumes.create_server_volume(
                        server.id,
                        volume.id,
                        None
                    )
                print("End to attach volume")

                print("Set NOPASSWD for user %s" % self.ssh_username)
                while True:
                    try:
                        ssh = pexpect.spawn(
                            'ssh -t %s@%s \'echo "%s ALL=(ALL) NOPASSWD: ALL" '
                            '| sudo tee /etc/sudoers.d/%s\'' %
                            (self.ssh_username, floating_ip,
                             self.ssh_username, self.ssh_username))
                        ssh.expect("password")
                        ssh.sendline(self.ssh_password)
                        ssh.expect("password")
                        ssh.sendline(self.ssh_password)
                        break
                    except Exception:
                        print("Waiting for 10 seconds that "
                              "floating ip is not ready...")
                        time.sleep(10)

                self.run_command_remote_server(
                    floating_ip,
                    "sudo chmod 0440 /etc/sudoers.d/%s" % self.ssh_username)
                print("Generate ssh-key for user %s" % self.ssh_username)
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
                ip = self.run_command_remote_server(floating_ip, cmd1)
                print(ip.replace("\n", ""))
                self.fixed_ip_list.append(ip.replace("\n", ""))
                self.run_command_remote_server(floating_ip, cmd2)

                if len(self.fixed_ip_list) == len(self.servers_name.split(",")):
                    ip_str = ",".join(self.fixed_ip_list)
                    CONF.set("vsm", ip_str)
                    i = 0
                    servers_name_list = self.servers_name.split(",")
                    while i < len(self.servers_name.split(",")):
                        cmd = "echo \"%s  %s\" | sudo tee -a /etc/hosts" % (
                            self.fixed_ip_list[i], servers_name_list[i].strip(" ")
                        )
                        self.run_command_remote_server(floating_ip, cmd)
                        i = i + 1
                    for ip in self.fixed_ip_list:
                        print("xtrust between controller and %s" % ip)
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
                self.run_command_remote_server(floating_ip, cmd3)

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
        print("Be sure that you have vsm release package "
              "under the folder tools")
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
        time.sleep(5)
        print("waiting the controller server is active!")

        while True:
            try:
                t = paramiko.Transport(self.floating_ip, 22)
                t.connect(username=self.ssh_username,
                          password=self.ssh_password)
                sftp = paramiko.SFTPClient.from_transport(t)
                localpath = vsm_package
                remotepath = "/tmp/" + vsm_package
                sftp.put(localpath, remotepath)
                t.close()
                break
            except Exception:
                time.sleep(5)
                continue

        s = paramiko.SSHClient()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.connect(self.floating_ip, port=22,
                  username=self.ssh_username,
                  password=self.ssh_password)
        print("Begin to install vsm, please wait for a few minutes!")
        print("Install controller %s ..." % controller_ip)
        stdin, stdout, stderr = s.exec_command("cd /tmp;tar -zxvf %s;cd %s;"
                                               "./install.sh -v 2.0 -u %s "
                                               "--prepare --controller %s"
                                               % (vsm_package, vsm_release_path,
                                                  self.ssh_username,
                                                  controller_ip))
        print("out: " + stdout.read())
        print("err: " + stderr.read())

        for ip in fixed_ip_list[0:-1]:
            print("Install agent %s ..." % ip)
            stdin, stdout, stderr = s.exec_command("cd /tmp/%s;"
                                                   "./install.sh -v 2.0 -u %s "
                                                   "--agent %s"
                                                   % (vsm_release_path,
                                                      self.ssh_username,
                                                      ip))
            print("out: " + stdout.read())
            print("err: " + stderr.read())

        s.close()

    def config_tempest(self, ip):
        t = paramiko.Transport((ip, 22))
        t.connect(username=self.ssh_username, password=self.ssh_password)
        sftp = paramiko.SFTPClient.from_transport(t)
        remotepath = "~/keyrc"
        localpath = "./keyrc"
        sftp.put(localpath, remotepath)
        t.close()

        def _replaceInFile(file, oldstr, newstr):
            for line in fileinput.input(file, inplace=True):
                if re.search(oldstr, line):
                    line = line.replace(oldstr, newstr)
                print line,

        tempest_conf = "./etc/tempest.conf"
        file = open("./keyrc")
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


def main():
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
    servers_name = CONF.get("vsm", "servers_name")
    security_group = CONF.get("vsm", "security_group")
    key_name = CONF.get("vsm", "key_name")
    floating_ip = CONF.get("vsm", "floating_ip")

    apply_servers = ApplyServers(username, password, tenant_name,
                                 auth_url, region_name)

    if not volumes_name:
        error("Volumes name is null, please check your volumes name "
              "in tempest.conf file")
    volumes_name_list = volumes_name.split(",")
    if not servers_name:
        error("Servers name is null, please check your servers name "
              "in tempest.conf file")
    servers_name_list = servers_name.split(",")
    if len(volumes_name_list) != len(servers_name_list) * 2:
        error("Please check the volumes name and servers name "
              "in tempest.conf file")
    for server_name in servers_name_list:
        server_name = server_name.strip(" ")
        apply_servers.create_server(
            server_name, image_name, flavor_id, net_id,
            security_group=security_group,
            key_name=key_name,
            floating_ip=floating_ip,
            volume_size=volume_size,
            volumes_list=[volumes_name_list.pop(0).strip(" "),
                          volumes_name_list.pop(0).strip(" ")]
        )

    deploy_vsm = DeployVSM()
    deploy_vsm.deploy_vsm(apply_servers.fixed_ip_list)


if __name__ == "__main__":
    main()