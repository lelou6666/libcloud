# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Driver for IBM SmartCloud Enterprise

Formerly known as:
- IBM Developer Cloud
- IBM Smart Business Development and Test on the IBM Cloud
- IBM SmartBusiness Cloud
"""

import base64
import time

from libcloud.utils.py3 import urlencode
from libcloud.utils.py3 import httplib
from libcloud.utils.py3 import b

from libcloud.common.base import XmlResponse, ConnectionUserAndKey
from libcloud.common.types import InvalidCredsError, LibcloudError
from libcloud.compute.types import NodeState, Provider
from libcloud.compute.base import NodeDriver, Node, NodeImage, \
    NodeSize, NodeLocation, NodeAuthSSHKey, StorageVolume

HOST = 'www-147.ibm.com'
REST_BASE = '/computecloud/enterprise/api/rest/20100331'


class IBMResponse(XmlResponse):
    def success(self):
        return int(self.status) == 200

    def parse_error(self):
        if int(self.status) == 401:
            if not self.body:
                raise InvalidCredsError(str(self.status) + ': ' + self.error)
            else:
                raise InvalidCredsError(self.body)
        return self.body


class IBMConnection(ConnectionUserAndKey):
    """
    Connection class for the IBM SmartCloud Enterprise driver
    """

    host = HOST
    responseCls = IBMResponse

    def add_default_headers(self, headers):
        headers['Accept'] = 'text/xml'
        headers['Authorization'] = ('Basic %s' % (base64.b64encode(
            b('%s:%s' % (self.user_id, self.key))).decode('utf-8')))
        if not 'Content-Type' in headers:
            headers['Content-Type'] = 'text/xml'
        return headers

    def encode_data(self, data):
        return urlencode(data)


class IBMNodeLocation(NodeLocation):
    """
    Extends the base LibCloud NodeLocation to contain additional attributes
    """
    def __init__(self, id, name, country, driver, extra=None):
        self.id = str(id)
        self.name = name
        self.country = country
        self.driver = driver
        self.extra = extra or {}

    def __repr__(self):
        return ('<IBMNodeLocation: id=%s, name=%s, country=%s, '
<<<<<<< HEAD
                'driver=%s, extra=%s>' % self.id, self.name, self.country,
                self.driver.name, self.extra)
=======
                'driver=%s, extra=%s>' %
                (self.id, self.name, self.country, self.driver.name,
                 self.extra))
>>>>>>> refs/remotes/nimbusproject/trunk


class VolumeState(object):
    """
    The SCE specific states for a storage volume
    """
    NEW = '0'
    CREATING = '1'
    DELETING = '2'
    DELETED = '3'
    DETACHED = '4'
    ATTACHED = '5'
    FAILED = '6'
    DELETE_PENDING = '7'
    BEING_CLONED = '8'
    CLONING = '9'
    ATTACHING = '10'
    DETACHING = '11'
    ATTACHIED = '12'
    IMPORTING = '13'
    TRANSFER_RETRYING = '14'


class VolumeOffering(object):
    """
    An SCE specific storage volume offering class.
    The volume offering ID is needed to create a volume.
    Volume offering IDs are different for each data center.
    """
    def __init__(self, id, name, location, extra=None):
        self.id = id
        self.location = location
        self.name = name
        self.extra = extra or {}

    def __repr__(self):
        return ('<VolumeOffering: id=%s, location=%s, name=%s, extra=%s>' %
<<<<<<< HEAD
                 self.id, self.location, self.name, self.extra)
=======
                (self.id, self.location, self.name, self.extra))
>>>>>>> refs/remotes/nimbusproject/trunk


class Address(object):
    """
    A reserved IP address that can be attached to an instance.
<<<<<<< HEAD
    Properties: id, ip, state, options(location, type, created_time, state, hostname, instance_ids, vlan, owner,
=======
    Properties: id, ip, state, options(location, type, created_time, state,
     hostname, instance_ids, vlan, owner,
>>>>>>> refs/remotes/nimbusproject/trunk
    mode, offering_id)
    """
    def __init__(self, id, ip, state, options):
        self.id = id
        self.ip = ip
        self.state = state
        self.options = options

    def __repr__(self):
        return ('<Address: id=%s, ip=%s, state=%s, options=%s>' %
<<<<<<< HEAD
                 self.id, self.ip, self.state, self.options)
=======
                (self.id, self.ip, self.state, self.options))

>>>>>>> refs/remotes/nimbusproject/trunk

class IBMNodeDriver(NodeDriver):
    """
    Node driver for IBM SmartCloud Enterprise
    """
    connectionCls = IBMConnection
    type = Provider.IBM
    name = "IBM SmartCloud Enterprise"
    website = 'http://ibm.com/services/us/en/cloud-enterprise/'

    NODE_STATE_MAP = {
        0: NodeState.PENDING,      # New
        1: NodeState.PENDING,      # Provisioning
        2: NodeState.TERMINATED,   # Failed
        3: NodeState.TERMINATED,   # Removed
        4: NodeState.TERMINATED,   # Rejected
        5: NodeState.RUNNING,      # Active
        6: NodeState.UNKNOWN,      # Unknown
        7: NodeState.PENDING,      # Deprovisioning
        8: NodeState.REBOOTING,    # Restarting
        9: NodeState.PENDING,      # Starting
        10: NodeState.PENDING,     # Stopping
        11: NodeState.TERMINATED,  # Stopped
        12: NodeState.PENDING,     # Deprovision Pending
        13: NodeState.PENDING,     # Restart Pending
        14: NodeState.PENDING,     # Attaching
        15: NodeState.PENDING,     # Detaching
    }

    def create_node(self, **kwargs):
        """
        Creates a node in the IBM SmartCloud Enterprise.
<<<<<<< HEAD

        See L{NodeDriver.create_node} for more keyword args.
=======
>>>>>>> refs/remotes/nimbusproject/trunk

        See :class:`NodeDriver.create_node` for more keyword args.

        @inherits: :class:`NodeDriver.create_node`

        :keyword    auth: Name of the pubkey to use. When constructing
            :class:`NodeAuthSSHKey` instance, 'pubkey' argument must be the
            name of the public key to use. You chose this name when creating
            a new public key on the IBM server.
        :type       auth: :class:`NodeAuthSSHKey`

        :keyword    ex_configurationData: Image-specific configuration
            parameters. Configuration parameters are defined in the parameters
            .xml file.  The URL to this file is defined in the NodeImage at
            extra[parametersURL].
            Note: This argument must be specified when launching a Windows
            instance. It must contain 'UserName' and 'Password' keys.
        :type       ex_configurationData: ``dict``
        """

        # Compose headers for message body
        data = {}
        data.update({'name': kwargs['name']})
        data.update({'imageID': kwargs['image'].id})
        data.update({'instanceType': kwargs['size'].id})
        if 'location' in kwargs:
            data.update({'location': kwargs['location'].id})
        else:
            data.update({'location': '1'})
        if 'auth' in kwargs and isinstance(kwargs['auth'], NodeAuthSSHKey):
            data.update({'publicKey': kwargs['auth'].pubkey})
        if 'ex_configurationData' in kwargs:
            configurationData = kwargs['ex_configurationData']
            if configurationData:
                for key in configurationData.keys():
                    data.update({key: configurationData.get(key)})

        # Send request!
        resp = self.connection.request(
            action=REST_BASE + '/instances',
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            method='POST',
            data=data).object
        return self._to_nodes(resp)[0]

    def create_volume(self, size, name, location, **kwargs):
        """
        Create a new block storage volume (virtual disk)

<<<<<<< HEAD
        @param      size: Size of volume in gigabytes (required).
                          Find out the possible sizes from the
                          offerings/storage REST interface
        @type       size: C{int}

        @keyword    name: Name of the volume to be created (required)
        @type       name: C{str}

        @keyword    location: Which data center to create a volume in. If
                              empty, it will fail for IBM SmartCloud Enterprise
                              (required)
        @type       location: L{NodeLocation}

        @keyword    snapshot:  Not supported for IBM SmartCloud Enterprise
        @type       snapshot:  C{str}

        @keyword    kwargs.format:  Either RAW or EXT3 for IBM SmartCloud
                                    Enterprise (optional)
        @type       kwargs.format:  C{str}

        @keyword    kwargs.offering_id:  The storage offering ID for IBM
                                         SmartCloud Enterprise
                                         Find this from the REST interface
                                         storage/offerings. (optional)
        @type       kwargs.offering_id:  C{str}

        @keyword    kwargs.source_disk_id:  If cloning a volume, the storage
                                            disk to make a copy from (optional)
        @type       kwargs.source_disk_id:  C{str}

        @keyword    kwargs.storage_area_id:  The id of the storage availability
                                             area to create the volume in
                                             (optional)
        @type       kwargs.storage_area_id:  C{str}

        @keyword    kwargs.target_location_id:  If cloning a volume, the
                                                storage disk to make a copy
                                                from (optional)
        @type       kwargs.target_location_id:  C{str}

        @return: The newly created L{StorageVolume}.
=======
        :param      size: Size of volume in gigabytes (required).
                          Find out the possible sizes from the
                          offerings/storage REST interface
        :type       size: ``int``

        :keyword    name: Name of the volume to be created (required)
        :type       name: ``str``

        :keyword    location: Which data center to create a volume in. If
                              empty, it will fail for IBM SmartCloud Enterprise
                              (required)
        :type       location: :class:`NodeLocation`

        :keyword    snapshot:  Not supported for IBM SmartCloud Enterprise
        :type       snapshot:  ``str``

        :keyword    kwargs.format:  Either RAW or EXT3 for IBM SmartCloud
                                    Enterprise (optional)
        :type       kwargs.format:  ``str``

        :keyword    kwargs.offering_id:  The storage offering ID for IBM
                                         SmartCloud Enterprise
                                         Find this from the REST interface
                                         storage/offerings. (optional)
        :type       kwargs.offering_id:  ``str``

        :keyword    kwargs.source_disk_id:  If cloning a volume, the storage
                                            disk to make a copy from (optional)
        :type       kwargs.source_disk_id:  ``str``

        :keyword    kwargs.storage_area_id:  The id of the storage availability
                                             area to create the volume in
                                             (optional)
        :type       kwargs.storage_area_id:  ``str``

        :keyword    kwargs.target_location_id:  If cloning a volume, the
                                                storage disk to make a copy
                                                from (optional)
        :type       kwargs.target_location_id:  ``str``

        :return: The newly created :class:`StorageVolume`.
        :rtype: :class:`StorageVolume`
>>>>>>> refs/remotes/nimbusproject/trunk
        """
        data = {}
        data.update({'name': name})
        data.update({'size': size})
        data.update({'location': location})
        if (('format' in kwargs) and (kwargs['format'] is not None)):
            data.update({'format': kwargs['format']})
        if (('offering_id' in kwargs) and (kwargs['offering_id'] is not None)):
            data.update({'offeringID': kwargs['offering_id']})
<<<<<<< HEAD
        if (('storage_area_id' in kwargs) and (kwargs['storage_area_id'] is not None)):
=======
        if (('storage_area_id' in kwargs) and
                (kwargs['storage_area_id'] is not None)):
>>>>>>> refs/remotes/nimbusproject/trunk
            data.update({'storageAreaID': kwargs['storage_area_id']})
        if 'source_disk_id' in kwargs:
            data.update({'sourceDiskID': kwargs['source_disk_id']})
            data.update({'type': 'clone'})
        if 'target_location_id' in kwargs:
            data.update({'targetLocationID': kwargs['target_location_id']})
<<<<<<< HEAD
        resp = self.connection.request(action=REST_BASE + '/storage',
=======
        resp = self.connection.request(
            action=REST_BASE + '/storage',
>>>>>>> refs/remotes/nimbusproject/trunk
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            method='POST',
            data=data).object
        return self._to_volumes(resp)[0]

    def create_image(self, name, description=None, **kwargs):
        """
        Create a new node image from an existing volume or image.

<<<<<<< HEAD
        @param      name: Name of the image to be created (required)
        @type       name: C{str}

        @param      description: Description of the image to be created (optional)
        @type       description: L{str}

        @keyword    kwarge.image_id:  The ID of the source image if cloning the image
        @type       kwargs.image_id:  C{str}

        @keyword    kwargs.volume_id:  The ID of the storage volume if importing the image
        @type       kwargs.volume_id:  C{str}

        @return: The newly created L{NodeImage}.
=======
        :param      name: Name of the image to be created (required)
        :type       name: ``str``

        :param      description: Description of the image to be created
        :type       description: ``str``

        :keyword    image_id:  The ID of the source image if cloning the image
        :type       image_id:  ``str``

        :keyword    volume_id:  The ID of the storage volume if
                                importing the image
        :type       volume_id:  ``str``

        :return: The newly created :class:`NodeImage`.
        :rtype: :class:`NodeImage`
>>>>>>> refs/remotes/nimbusproject/trunk
        """
        data = {}
        data.update({'name': name})
        if description is not None:
            data.update({'description': description})
        if (('image_id' in kwargs) and (kwargs['image_id'] is not None)):
            data.update({'imageId': kwargs['image_id']})
        if (('volume_id' in kwargs) and (kwargs['volume_id'] is not None)):
            data.update({'volumeId': kwargs['volume_id']})
<<<<<<< HEAD
        resp = self.connection.request(action=REST_BASE + '/offerings/image',
=======
        resp = self.connection.request(
            action=REST_BASE + '/offerings/image',
>>>>>>> refs/remotes/nimbusproject/trunk
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            method='POST',
            data=data).object
        return self._to_images(resp)[0]

    def destroy_node(self, node):
        url = REST_BASE + '/instances/%s' % (node.id)
        status = int(self.connection.request(action=url,
                                             method='DELETE').status)
        return status == httplib.OK

    def destroy_volume(self, volume):
        """
        Destroys a storage volume.

        :param      volume: Volume to be destroyed
        :type       volume: :class:`StorageVolume`

        :rtype: ``bool``
        """
        url = REST_BASE + '/storage/%s' % (volume.id)
        status = int(self.connection.request(action=url,
                                             method='DELETE').status)
        return status == httplib.OK

    def ex_destroy_image(self, image):
        """
        Destroys an image.

        :param      image: Image to be destroyed
        :type       image: :class:`NodeImage`

        :return: ``bool``
        """

        url = REST_BASE + '/offerings/image/%s' % (image.id)
        status = int(self.connection.request(action=url,
                                             method='DELETE').status)
        return status == 200

<<<<<<< HEAD
    def destroy_volume(self, volume):
        """
        Destroys a storage volume.

        @param      volume: Volume to be destroyed
        @type       volume: L{StorageVolume}

        @return: C{bool}
        """
        url = REST_BASE + '/storage/%s' % (volume.id)
        status = int(self.connection.request(action=url,
                                             method='DELETE').status)
        return status == 200

=======
>>>>>>> refs/remotes/nimbusproject/trunk
    def attach_volume(self, node, volume):
        """
        Attaches volume to node.

<<<<<<< HEAD
        @param      node: Node to attach volume to
        @type       node: L{Node}

        @param      volume: Volume to attach
        @type       volume: L{StorageVolume}

        @return: C{bool}
=======
        :param      node: Node to attach volume to
        :type       node: :class:`Node`

        :param      volume: Volume to attach
        :type       volume: :class:`StorageVolume`

        :rtype: ``bool``
>>>>>>> refs/remotes/nimbusproject/trunk
        """
        url = REST_BASE + '/instances/%s' % (node.id)
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {'storageID': volume.id, 'type': 'attach'}
        resp = self.connection.request(action=url,
                                       method='PUT',
                                       headers=headers,
                                       data=data)
        return int(resp.status) == 200

    def detach_volume(self, node, volume):
        """
        Detaches a volume from a node.

<<<<<<< HEAD
        @param      volume: Volume to be detached
        @type       volume: L{StorageVolume}

        @returns C{bool}
=======
        :param      node: Node which should be used
        :type       node: :class:`Node`

        :param      volume: Volume to be detached
        :type       volume: :class:`StorageVolume`

        :rtype: ``bool``
>>>>>>> refs/remotes/nimbusproject/trunk
        """
        url = REST_BASE + '/instances/%s' % (node.id)
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {'storageID': volume.id, 'type': 'detach'}
        resp = self.connection.request(action=url,
                                       method='PUT',
                                       headers=headers,
                                       data=data)
        return int(resp.status) == 200

    def reboot_node(self, node):
        url = REST_BASE + '/instances/%s' % (node.id)
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {'state': 'restart'}

        resp = self.connection.request(action=url,
                                       method='PUT',
                                       headers=headers,
                                       data=data)
        return int(resp.status) == 200

    def list_nodes(self):
        return self._to_nodes(
            self.connection.request(REST_BASE + '/instances').object)

    def list_images(self, location=None):
        return self._to_images(
            self.connection.request(REST_BASE + '/offerings/image').object)

    def list_volumes(self):
        """
        List storage volumes.

<<<<<<< HEAD
        @return: C{list} of L{StorageVolume} objects
=======
        :rtype: ``list`` of :class:`StorageVolume`
>>>>>>> refs/remotes/nimbusproject/trunk
        """
        return self._to_volumes(
            self.connection.request(REST_BASE + '/storage').object)

    def list_sizes(self, location=None):
        """
<<<<<<< HEAD
        Returns a generic list of sizes.  See list_images() for a list of supported
        sizes for specific images.  In particular, you need to have a size that
        matches the architecture (32-bit vs 64-bit) of the virtual machine image
        operating system.
=======
        Returns a generic list of sizes.  See list_images() for a list of
        supported sizes for specific images.  In particular, you need to have
        a size that matches the architecture (32-bit vs 64-bit) of the virtual
        machine image operating system.
>>>>>>> refs/remotes/nimbusproject/trunk

        @inherits: :class:`NodeDriver.list_sizes`
        """
        return [
            NodeSize('BRZ32.1/2048/60*175', 'Bronze 32 bit', None, None, None,
                     None, self.connection.driver),
            NodeSize('BRZ64.2/4096/60*500*350', 'Bronze 64 bit', None, None,
                     None, None, self.connection.driver),
            NodeSize('COP32.1/2048/60', 'Copper 32 bit', None, None, None,
                     None, self.connection.driver),
            NodeSize('COP64.2/4096/60', 'Copper 64 bit', None, None, None,
                     None, self.connection.driver),
            NodeSize('SLV32.2/4096/60*350', 'Silver 32 bit', None, None, None,
                     None, self.connection.driver),
            NodeSize('SLV64.4/8192/60*500*500', 'Silver 64 bit', None, None,
                     None, None, self.connection.driver),
            NodeSize('GLD32.4/4096/60*350', 'Gold 32 bit', None, None, None,
                     None, self.connection.driver),
            NodeSize('GLD64.8/16384/60*500*500', 'Gold 64 bit', None, None,
                     None, None, self.connection.driver),
            NodeSize('PLT64.16/16384/60*500*500*500*500', 'Platinum 64 bit',
                     None, None, None, None, self.connection.driver)]

    def list_locations(self):
        """
        List the data center locations
        """
        return self._to_locations(
            self.connection.request(REST_BASE + '/locations').object)

    def ex_list_storage_offerings(self):
        """
        List the storage center offerings
<<<<<<< HEAD
=======

        :rtype: ``list`` of :class:`VolumeOffering`
>>>>>>> refs/remotes/nimbusproject/trunk
        """
        return self._to_volume_offerings(
            self.connection.request(REST_BASE + '/offerings/storage').object)

    def ex_allocate_address(self, location_id, offering_id, vlan_id=None):
        """
        Allocate a new reserved IP address

<<<<<<< HEAD
        @param      location_id: Target data center
        @type       location_id: L{str}
        @param      offering_id: Offering ID for address to create
        @type       offering_id: L{str}
        @param      vlan_id: ID of target VLAN
        @type       vlan_id: L{str}
        @return:    L{Address} object
=======
        :param      location_id: Target data center
        :type       location_id: ``str``

        :param      offering_id: Offering ID for address to create
        :type       offering_id: ``str``

        :param      vlan_id: ID of target VLAN
        :type       vlan_id: ``str``

        :return: :class:`Address` object
        :rtype: :class:`Address`
>>>>>>> refs/remotes/nimbusproject/trunk
        """
        url = REST_BASE + '/addresses'
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {'location': location_id, 'offeringID': offering_id}
        if vlan_id is not None:
            data.update({'vlanID': vlan_id})
        resp = self.connection.request(action=url,
                                       method='POST',
                                       headers=headers,
                                       data=data).object
        return self._to_addresses(resp)[0]

    def ex_list_addresses(self, resource_id=None):
        """
        List the reserved IP addresses

<<<<<<< HEAD
        @param      resource_id: If this is supplied only a single address will be returned (optional)
        @type       resource_id: L{str}
=======
        :param      resource_id: If this is supplied only a single address will
         be returned (optional)
        :type       resource_id: ``str``

        :rtype: ``list`` of :class:`Address`
>>>>>>> refs/remotes/nimbusproject/trunk
        """
        url = REST_BASE + '/addresses'
        if resource_id:
            url += '/' + resource_id
        return self._to_addresses(self.connection.request(url).object)

    def ex_copy_to(self, image, volume):
        """
        Copies a node image to a storage volume

<<<<<<< HEAD
        @param      image: source image to copy
        @type       image: L{NodeImage}

        @param      volume: Target storage volume to copy to
        @type       volume: L{StorageVolume}

        @return: C{bool} The success of the operation
=======
        :param      image: source image to copy
        :type       image: :class:`NodeImage`

        :param      volume: Target storage volume to copy to
        :type       volume: :class:`StorageVolume`

        :return: ``bool`` The success of the operation
        :rtype: ``bool``
>>>>>>> refs/remotes/nimbusproject/trunk
        """
        url = REST_BASE + '/storage/%s' % (volume.id)
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {'imageId': image.id}
        resp = self.connection.request(action=url,
                                       method='PUT',
                                       headers=headers,
                                       data=data)
        return int(resp.status) == 200

    def ex_delete_address(self, resource_id):
        """
        Delete a reserved IP address

<<<<<<< HEAD
        @param      resource_id: The address to delete (required)
        @type       resource_id: L{str}
=======
        :param      resource_id: The address to delete (required)
        :type       resource_id: ``str``

        :rtype: ``bool``
>>>>>>> refs/remotes/nimbusproject/trunk
        """
        url = REST_BASE + '/addresses/' + resource_id
        status = int(self.connection.request(action=url,
                                             method='DELETE').status)
        return status == 200

    def ex_wait_storage_state(self, volume, state=VolumeState.DETACHED,
                              wait_period=60, timeout=1200):
        """
        Block until storage volume state changes to the given value

<<<<<<< HEAD
        @param      volume: Storage volume.
        @type       node: C{StorageVolume}

        @param      state: The target state to wait for
        @type       state: C{int}

        @param      wait_period: How many seconds to between each loop
                                 iteration (default is 3)
        @type       wait_period: C{int}

        @param      timeout: How many seconds to wait before timing out
                             (default is 1200)
        @type       timeout: C{int}

        @return: C{StorageVolume}
=======
        :param      volume: Storage volume.
        :type       volume: :class:`StorageVolume`

        :param      state: The target state to wait for
        :type       state: ``int``

        :param      wait_period: How many seconds to between each loop
                                 iteration (default is 3)
        :type       wait_period: ``int``

        :param      timeout: How many seconds to wait before timing out
                             (default is 1200)
        :type       timeout: ``int``

        :rtype: :class:`StorageVolume`
>>>>>>> refs/remotes/nimbusproject/trunk
        """
        start = time.time()
        end = start + timeout

        while time.time() < end:
            volumes = self.list_volumes()
            volumes = list([v for v in volumes if v.uuid == volume.uuid])

            if (len(volumes) == 1 and volumes[0].extra['state'] == state):
                return volumes[0]
            else:
                time.sleep(wait_period)
                continue

        raise LibcloudError(value='Timed out after %d seconds' % (timeout),
                            driver=self)

    def _to_nodes(self, object):
        return [self._to_node(instance) for instance in
                object.findall('Instance')]

    def _to_node(self, instance):
        public_ips = []

        ip = instance.findtext('IP')
        if ip:
            public_ips.append(ip)

        return Node(
                    id=instance.findtext('ID'),
                    name=instance.findtext('Name'),
                    state=self.NODE_STATE_MAP[int(instance.findtext('Status'))],
                    public_ips=public_ips,
                    private_ips=[],
                    driver=self.connection.driver
        )

    def _to_images(self, object):
<<<<<<< HEAD
        # Converts data retrieved from SCE /offerings/image REST call to a NodeImage
=======
        # Converts data retrieved from SCE /offerings/image REST call to
        # a NodeImage
>>>>>>> refs/remotes/nimbusproject/trunk
        return [self._to_image(image) for image in object.findall('Image')]

    def _to_image(self, image):
        # Converts an SCE Image object to a NodeImage
        imageID = image.findtext('ID')
        imageName = image.findtext('Name')
        parametersURL = image.findtext('Manifest')
        location = image.findtext('Location')
        state = image.findtext('State')
        owner = image.findtext('Owner')
        visibility = image.findtext('Visibility')
        platform = image.findtext('Platform')
        description = image.findtext('Description')
        documentation = image.findtext('Documentation')
        instanceTypes = image.findall('SupportedInstanceTypes')
        nodeSizes = self._to_node_sizes(image.find('SupportedInstanceTypes'))
        return NodeImage(id=imageID,
                         name=imageName,
                         driver=self.connection.driver,
                         extra={
                             'parametersURL': parametersURL,
                             'location': location,
                             'state': state,
                             'owner': owner,
                             'visibility': visibility,
                             'platform': platform,
                             'description': description,
                             'documentation': documentation,
<<<<<<< HEAD
=======
                             'instanceTypes': instanceTypes,
>>>>>>> refs/remotes/nimbusproject/trunk
                             'node_sizes': nodeSizes
                         }
                         )

    def _to_locations(self, object):
        return [self._to_location(location) for location in
                object.findall('Location')]

    def _to_location(self, location):
        # Converts an SCE Location object to a Libcloud NodeLocation object
        name_text = location.findtext('Name')
        description = location.findtext('Description')
        state = location.findtext('State')
        (nameVal, separator, countryVal) = name_text.partition(',')
        capabiltyElements = location.findall('Capabilities/Capability')
        capabilities = {}
        for elem in capabiltyElements:
            capabilityID = elem.attrib['id']
            entryElements = elem.findall('Entry')
            entries = []
            for entryElem in entryElements:
                key = entryElem.attrib['key']
                valueElements = elem.findall('Value')
                values = []
                for valueElem in valueElements:
                    values.append(valueElem.text)
                entry = {'key': key, 'values': values}
                entries.append(entry)
            capabilities[capabilityID] = entries
        extra = {'description': description, 'state': state,
                 'capabilities': capabilities}
        return IBMNodeLocation(id=location.findtext('ID'),
                               name=nameVal,
                               country=countryVal.strip(),
                               driver=self.connection.driver,
                               extra=extra)

    def _to_node_sizes(self, object):
        # Converts SCE SupportedInstanceTypes object to
        # a list of Libcloud NodeSize objects
        return [self._to_node_size(iType) for iType in
                object.findall('InstanceType')]

    def _to_node_size(self, object):
        # Converts to an SCE InstanceType to a Libcloud NodeSize
        return NodeSize(object.findtext('ID'),
                        object.findtext('Label'),
                        None,
                        None,
                        None,
                        object.findtext('Price/Rate'),
                        self.connection.driver)

    def _to_volumes(self, object):
        return [self._to_volume(iType) for iType in
                object.findall('Volume')]

    def _to_volume(self, object):
        # Converts an SCE Volume to a Libcloud StorageVolume
        extra = {'state': object.findtext('State'),
<<<<<<< HEAD
                'location': object.findtext('Location'),
                'instanceID': object.findtext('instanceID'),
                'owner': object.findtext('Owner'),
                'format': object.findtext('Format'),
                'createdTime': object.findtext('CreatedTime'),
                'storageAreaID': object.findtext('StorageArea/ID')}
=======
                 'location': object.findtext('Location'),
                 'instanceID': object.findtext('instanceID'),
                 'owner': object.findtext('Owner'),
                 'format': object.findtext('Format'),
                 'createdTime': object.findtext('CreatedTime'),
                 'storageAreaID': object.findtext('StorageArea/ID')}
>>>>>>> refs/remotes/nimbusproject/trunk
        return StorageVolume(object.findtext('ID'),
                             object.findtext('Name'),
                             object.findtext('Size'),
                             self.connection.driver,
                             extra)

    def _to_volume_offerings(self, object):
        return [self._to_volume_offering(iType) for iType in
                object.findall('Offerings')]

    def _to_volume_offering(self, object):
        # Converts an SCE DescribeVolumeOfferingsResponse/Offerings XML object
        # to an SCE VolumeOffering
        extra = {'label': object.findtext('Label'),
<<<<<<< HEAD
                'supported_sizes': object.findtext('SupportedSizes'),
                'formats': object.findall('SupportedFormats/Format/ID'),
                'price': object.findall('Price')}
=======
                 'supported_sizes': object.findtext('SupportedSizes'),
                 'formats': object.findall('SupportedFormats/Format/ID'),
                 'price': object.findall('Price')}
>>>>>>> refs/remotes/nimbusproject/trunk
        return VolumeOffering(object.findtext('ID'),
                              object.findtext('Name'),
                              object.findtext('Location'),
                              extra)

    def _to_addresses(self, object):
        # Converts an SCE DescribeAddressesResponse XML object to a list of
        # Address objects
        return [self._to_address(iType) for iType in
                object.findall('Address')]

    def _to_address(self, object):
        # Converts an SCE DescribeAddressesResponse/Address XML object to
        # an Address object
        extra = {'location': object.findtext('Location'),
<<<<<<< HEAD
                'type': object.findtext('Label'),
                'created_time': object.findtext('SupportedSizes'),
                'hostname': object.findtext('Hostname'),
                'instance_ids': object.findtext('InstanceID'),
                'vlan': object.findtext('VLAN'),
                'owner': object.findtext('owner'),
                'mode': object.findtext('Mode'),
                'offering_id': object.findtext('OfferingID')}
=======
                 'type': object.findtext('Label'),
                 'created_time': object.findtext('SupportedSizes'),
                 'hostname': object.findtext('Hostname'),
                 'instance_ids': object.findtext('InstanceID'),
                 'vlan': object.findtext('VLAN'),
                 'owner': object.findtext('owner'),
                 'mode': object.findtext('Mode'),
                 'offering_id': object.findtext('OfferingID')}
>>>>>>> refs/remotes/nimbusproject/trunk
        return Address(object.findtext('ID'),
                       object.findtext('IP'),
                       object.findtext('State'),
                       extra)
