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

from tempest.api.vsm import base
from tempest import test

import sys
import time

from tempest import config

try:
    from novaclient.v1_1 import client as nc_client
except Exception:
    from novaclient.v2 import client as nc_client
try:
    from cinderclient.v1 import client as cc_client
except Exception:
    from cinderclient.v2 import client as cc_client

CONF = config.CONF


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
        self.uri = CONF.identity.uri
        self.auth_version = CONF.identity.auth_version
        self.auth_url = self.uri + "/" + self.auth_version
        self.region = CONF.identity.region
        self.admin_username = CONF.identity.admin_username
        self.admin_tenant_name = CONF.identity.admin_tenant_name
        self.admin_password = CONF.identity.admin_password

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

        self.image_name = CONF.vsm.image_name
        self.flavor_id = CONF.vsm.flavor_id
        self.volumes_name = CONF.vsm.volumes_name
        self.volume_size = CONF.vsm.volume_size
        self.net_id = CONF.vsm.net_id
        self.servers_name = CONF.vsm.servers_name
        self.security_group = CONF.vsm.security_group
        self.key_name = CONF.vsm.key_name

    def image_available(self, image_name):
        """

        :param image_name:
        :return:
        """
        if not image_name:
            error("No image name, please check your image_name "
                  "in tempest.conf or config.py file")
            sys.exit(1)

        images_list = self.novaclient.images.list()
        if image_name in [image.name for image in images_list]:
            print("The image is available")
        else:
            error("Not found the image %s" % image_name)
            sys.exit(1)

    def flavor_available(self, flavor_id):
        """

        :param flavor_id:
        :return:
        """
        if not flavor_id:
            error("No flavor id, please check your flavor "
                  "id in tempest.conf or config.py file")
            sys.exit(1)

        flavor_list = self.novaclient.flavors.list()
        if flavor_id in [flavor.id for flavor in flavor_list]:
            print("The flavor is available")
        else:
            error("Not found the flavor id %s" % flavor_id)
            sys.exit(1)

    def net_available(self, net_id):
        """

        :param net_id:
        :return:
        """
        if not net_id:
            error("No network id, please check your flavor "
                  "id in tempest.conf or config.py file")
            sys.exit(1)

        net_list = self.novaclient.networks.list()
        if net_id in [net.id for net in net_list]:
            print("The net is available")
        else:
            error("Not found the net id %s" % net_id)
            sys.exit(1)

    def volume_available(self, volume_name):
        """

        :param volume_name:
        :return:
        """
        volumes_list = self.cinderclient.volumes.list()
        if volume_name in [volume.name for volume in volumes_list]:
            print("The volume is available")
        else:
            error("Not found the volume %s" % volume_name)
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
        volume_status = self.cinderclient.volumes.get(name)
        return volume_status

    def create_server(self, server_name, image_name, flavor_id, net_id,
                      security_group="default", key_name="demo-key"):
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
        self.novaclient.servers.create(server_name, image_name, flavor_id,
                                       security_groups=[security_group],
                                       key_name=key_name,
                                       nics=[{"net-id": net_id}])
        server_list = self.novaclient.servers.list()
        count = 1
        while count < 100:
            time.sleep(count)
            server = self.novaclient.servers.get(server_name)
            if server.status == "ACTIVE":
                print("The server is active")
                count = 100
            else:
                count = count + 1
                break

    def attach_volume_to_server(self, volume_id, server_id):
        return


class ApplyServersTestJSON(base.BaseVSMAdminTest):

    """
    Tests clusters API using admin privileges.
    """

    @classmethod
    def setup_clients(cls):
        super(ApplyServersTestJSON, cls).setup_clients()
        cls.client = cls.os_adm.clusters_client

    @test.idempotent_id('087acd2f-ce75-48e4-9b0b-a82c9ae57578')
    def test_apply_servers(self):
        apply_servers = ApplyServers()
        apply_servers.image_available(apply_servers.image_name)
        apply_servers.flavor_available(apply_servers.flavor_id)
        apply_servers.net_available(apply_servers.net_id)

        if not apply_servers.volumes_name:
            error("No volumes name, please check your "
                  "flavor id in tempest.conf or config.py file")
            sys.exit(1)
        volumes_name_list = apply_servers.volumes_name
        for volume_name in volumes_name_list:
            apply_servers.volume_available(volume_name)

        servers_name_list = apply_servers.servers_name.split(",")
        for server_name in servers_name_list:
            server_name = server_name.strip()
            apply_servers.create_server(server_name,
                                        apply_servers.image_name,
                                        apply_servers.flavor_id,
                                        apply_servers.net_id,
                                        apply_servers.security_group,
                                        apply_servers.key_name)
