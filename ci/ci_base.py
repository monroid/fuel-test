#!/usr/bin/env pyton

import logging
from abc import abstractproperty, abstractmethod
from devops.helpers.helpers import _get_file_size
from ipaddr import IPNetwork
from helpers.functions import  write_config, change_host_name, request_cerificate, setup_puppet_client, setup_puppet_master, add_nmap, switch_off_ip_tables, add_to_hosts
from node_roles import NodeRoles, Nodes
from settings import EMPTY_SNAPSHOT, ISO_IMAGE, DEFAULT_RAM_SIZE
from helpers.root import root
from helpers.functions import load
from devops.manager import Manager


LOG = logging.getLogger(__name__)

class CiBase(object):
    """
    Base class for creating environment -- deploy openstack in various mode.
    """
    def __init__(self):
        """
        Constructor. Define environment and manager for manipulation with it.
        """
        self._environment = None
        self.manager = Manager()

    def get_or_create(self):
        """
        Get prepared environment or create it.
        """
        try:
            return self.manager.environment_get(self.env_name())
        except:
            self._environment = self.describe_environment()
            self._environment.define()
            return self._environment

    def get_empty_state(self):
        """
        Get 'empty' snapshot for virtual machines.
        """
        if self.environment().has_snapshot(EMPTY_SNAPSHOT):
            self.environment().revert(EMPTY_SNAPSHOT)
        else:
            self.setup_environment()

    def environment(self):
        """
        :rtype : devops.models.Environment
        """
        self._environment = self._environment or self.get_or_create()
        return self._environment

    @abstractproperty
    def env_name(self):
        """
        :rtype : string
        """
        pass

    @abstractmethod
    def define(self):
        """
        :rtype : devops.models.Environment
        """
        pass

    @abstractmethod
    def describe_environment(self):
        """
        :rtype : devops.models.Environment
        """
        pass

    @abstractproperty
    def node_roles(self):
        """
        :rtype : NodeRoles
        """
        pass

    def add_empty_volume(self, node, name, capacity=20 * 1024 * 1024 * 1024, format="qcow2", device="disk", bus='virtio'):
        """
        Attach a empty volume to virtual machine.
        """
        self.manager.node_attach_volume(node=node,
                                        device=device,
                                        bus=bus,
                                        volume=self.manager.volume_create(
                                        name=name,
                                        capacity=capacity,
                                        format=format,
                                        environment=self.environment()))

    def add_node(self, memory, name, boot=None):
        """
        Create a virtual machine in environment.
        """
        return self.manager.node_create(name=name,
                                        memory=memory,
                                        environment=self.environment())

    def describe_master_node(self, name, networks, memory=DEFAULT_RAM_SIZE):
        """
        Define master node.
        """
        node = self.add_node(memory, name, boot=['cdrom', 'hd'])
        for network in networks:
            self.manager.interface_create(network, node=node)
        self.add_empty_volume(node, name + '-system')
        self.add_empty_volume(node, name + '-iso', capacity=_get_file_size(ISO_IMAGE), format='raw', device='cdrom', bus='ide')
        return node

    def describe_empty_node(self, name, networks, memory=DEFAULT_RAM_SIZE):
        """
        Define node with default settings.
        """
        node = self.add_node(memory, name)
        for network in networks:
            self.manager.interface_create(network, node=node)
        self.add_empty_volume(node, name + '-system')
        self.add_empty_volume(node, name + '-cinder')
        return node

    def nodes(self):
        """
        Get all virtual machines of environment.
        """
        return Nodes(self.environment(), self.node_roles())

    def add_nodes_to_hosts(self, remote, nodes):
        """
        Append to /etc/hosts list of ip addresses by internal interface for all vms.
        """
        for node in nodes:
            add_to_hosts(remote,
                         node.get_ip_address_by_network_name('internal'),
                         node.name,
                         node.name + '.localdomain')

    def setup_master_node(self, master_remote, nodes):
        """
        Make the basic settings for master vm(node).
        """
        setup_puppet_master(master_remote)
        add_nmap(master_remote)
        switch_off_ip_tables(master_remote)
        self.add_nodes_to_hosts(master_remote, nodes)

    def setup_agent_nodes(self, nodes):
        """
        Make the basic settings for default vm(node).
        """
        agent_config = load(root('fuel_test', 'config', 'puppet.agent.config'))
        for node in nodes:
            if node.name != 'master':
                remote = node.remote('public', login='root', password='r00tme')
                self.add_nodes_to_hosts(remote, self.environment().nodes)
                setup_puppet_client(remote)
                write_config(remote, '/etc/puppet/puppet.conf', agent_config)
                request_cerificate(remote)

    def rename_nodes(self, nodes):
        """
        Change host name for nodes.
        """
        for node in nodes:
            remote = node.remote('public', login='root', password='r00tme')
            change_host_name(remote,
                             node.name,
                             node.name + '.localdomain')
            LOG.info("Renamed %s" % node.name)

    @abstractmethod
    def setup_environment(self):
        """
        :rtype : None
        """
        pass

    def internal_virtual_ip(self):
        """
        Get virtual ip in internal network.
        """
        return str(IPNetwork(self.environment().network_by_name('internal').ip_network)[-2])

    def floating_network(self):
        """
        Get floating subnet of public network.
        """
        prefix = IPNetwork(self.environment().network_by_name('public').ip_network).prefixlen
        return str(IPNetwork(self.environment().network_by_name('public').ip_network).subnet(new_prefix=prefix + 2)[-1])

    def public_virtual_ip(self):
        """
        Get virtual ip in public network.
        """
        prefix = IPNetwork(self.environment().network_by_name('public').ip_network).prefixlen
        return str(IPNetwork(self.environment().network_by_name('public').ip_network).subnet(new_prefix=prefix + 2)[-2][-1])

    def public_router(self):
        """
        Get route for public network.
        """
        return str(IPNetwork(self.environment().network_by_name('public').ip_network)[1])

    def internal_router(self):
        """
        Get route for internal network.
        """
        return str(IPNetwork(self.environment().network_by_name('internal').ip_network)[1])

    def fixed_network(self):
        """
        Get fixed subnet of private network.
        """
        return str(IPNetwork(self.environment().network_by_name('private').ip_network).subnet(
                new_prefix=27)[0])

    def internal_network(self):
        """
        Get internal network.
        """
        return str(IPNetwork(self.environment().network_by_name('internal').ip_network))

    def internal_net_mask(self):
        """
        Get internal netmask.
        """
        return str(IPNetwork(self.environment().network_by_name('internal').ip_network).netmask)

    def public_net_mask(self):
        """
        Get public netmask.
        """
        return str(IPNetwork(self.environment().network_by_name('public').ip_network).netmask)

    def public_network(self):
        """
        Get public network.
        """
        return str(IPNetwork(self.environment().network_by_name('public').ip_network))
