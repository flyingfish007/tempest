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

import sys

from tempest import config

try:
    from novaclient.v1_1 import client as nc_client
except:
    from novaclient.v2 import client as nc_client
try:
    from cinderclient.v1 import client as cc_client
except:
    from cinderclient.v2 import client as cc_client

CONF = config.CONF

def error(msg):
    print '---------------ERROR----------------'
    print '------------------------------------'
    if isinstance(msg, list):
        for n in msg:
            print n
    else:
        print msg
    print '------------------------------------'
    sys.exit(1)

class ApplyServers(object):
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
            region_name = self.region
        )

        self.cinderclient = cc_client.Client(
            self.admin_username,
            self.admin_password,
            self.admin_tenant_name,
            self.auth_url,
            region_name = self.region
        )


        self.image_name = CONF.vsm.image_name
        self._image_available(client=self.novaclient, image_name=self.image_name)

    def _image_available(client, image_name):
        if not image_name:
            error("No image_name, please check your image_name in tempest.conf "
                  "or config.py file")

        images_list = client.images.list()
        if image_name in [image.name for image in images_list]:
            print "The image is available"
        else:
            error("Not found the image %s" % image_name)
            sys.exit(1)

    def _flavor_available(flavor_id):
        return

    def _volume_available(cinder_id):
        return

    def create_volume(id, size):
        return

    def create_server(image_name, flavor_id, net_id, ):
        return

    def attach_volume_to_server(volume_id, server_id):
        return


if __name__ == "__main__":
    apply_servers = ApplyServers()


