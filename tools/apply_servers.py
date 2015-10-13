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

try:
    from novaclient.v1_1 import client as nc_client
except Exception:
    from novaclient.v2 import client as nc_client
try:
    from cinderclient.v1 import client as cc_client
except Exception:
    from cinderclient.v2 import client as cc_client


CONF = ConfigParser.ConfigParser()
if sys.argv[1]:
    CONF.read(sys.argv[1])
else:
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
        self.controller_floating_ip = CONF.get("vsm", "vsm_controller_ip")
        self.agents_floating_ip = CONF.get("vsm", "vsm_agents_ip")
        self.floating_ip_list = self.agents_floating_ip.split(",")
        self.floating_ip_list.append(self.controller_floating_ip)

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
        if volume_name in [volume.name for volume in volumes_list]:
            print("The volume is available")
        else:
            print("Not found the volume %s" % volume_name)
            print("Creating the volume %s" % volume_name)
            volume_status = self.create_volume(volume_name, self.volume_size)
            count = 1
            while volume_status != "available":
                if count < 6:
                    time.sleep(count)
                    count = count + 1
                    continue
                else:
                    print("The volume %s is still not available, "
                          "please check by yourself" % volume_name)
                    break

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
                return volume.status

    def create_server(self, server_name, image_name, flavor_id, net_id,
                      security_group="default", key_name="demo-key",
                      floating_ip=None):
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
        if server_name in [server.name for server in server_list]:
            self.novaclient.servers.delete(server_name)
            server_list = self.novaclient.servers.list()
            count = 1
            while count < 6:
                time.sleep(count)
                if server_name in [server.name for server in server_list]:
                    count = count + 1
                    continue
                else:
                    print("the old server has been deleted")
                    break
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
            time.sleep(count)
            server = self.novaclient.servers.get(server.id)
            if server.status == "ACTIVE":
                print("The server is active")
                print("Begin to associate floating ip to server")
                self.novaclient.servers.add_floating_ip(server.id, floating_ip)
                print("End to associate floating ip to server")
                count = 100
            else:
                count = count + 1
                continue

    def attach_volume_to_server(self, volume_id, server_id):
        return


if __name__ == "__main__":
    apply_servers = ApplyServers()
    apply_servers.image_available(apply_servers.image_name)
    apply_servers.flavor_available(apply_servers.flavor_id)
    apply_servers.net_available(apply_servers.net_id)

    if not apply_servers.volumes_name:
        error("No volumes name, please check your "
              "flavor id in tempest.conf or config.py file")
    volumes_name = apply_servers.volumes_name
    volumes_name_list = volumes_name.split(",")
    for volume_name in volumes_name_list:
        apply_servers.volume_available(volume_name.strip(" "))

    servers_name_list = apply_servers.servers_name.split(",")
    floating_ip_list = apply_servers.floating_ip_list
    if len(floating_ip_list) != len(servers_name_list):
        error("The number of floating ip does not equal "
              "servers, please check again!")
    count = 0
    for server_name in servers_name_list:
        server_name = server_name.strip()
        apply_servers.create_server(server_name,
                                    apply_servers.image_name,
                                    apply_servers.flavor_id,
                                    apply_servers.net_id,
                                    apply_servers.security_group,
                                    apply_servers.key_name,
                                    floating_ip_list[count])
        count = count + 1