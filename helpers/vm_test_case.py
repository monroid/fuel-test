#!/usr/bin/env python

from time import sleep
import unittest
from ipaddr import IPNetwork
from helpers.base_test_case import BaseTestCase
from ci.ci_vm import CiVM
from helpers.cobbler_client import CobblerClient
from config import Config
from helpers.functions import tcp_ping, udp_ping, add_to_hosts, await_node_deploy, write_config
import iso_master
from settings import INTERFACES, PARENT_PROXY, DOMAIN_NAME, CURRENT_PROFILE, PUPPET_MASTER_VERSION


class CobblerTestCase(BaseTestCase):
    """
    Main class like unittest with common methods for deploy.
    """
    def ci(self):
        """
        Define environment mode, by default uses CiVM().
        """
        if not hasattr(self, '_ci'):
            self._ci = CiVM()
        return self._ci

    def setUp(self):
        """
        SetUp method -- update puppet modules on master node.
        """
        self.get_nodes_deployed_state()
        self.update_modules()

    def get_nodes_deployed_state(self):
        """
        Get or prepare vms(nodes) state:
            update modules on master node
            write /root/fuel.defaults
            install OS (cobbler)
        """
        if not self.environment().has_snapshot('nodes-deployed'):
            self.ci().get_empty_state()
            self.update_modules()
            self.remote().execute("killall bootstrap_admin_node.sh")
            write_config(self.remote(), "/root/fuel.defaults",
                         iso_master.get_config(
                             hostname="master",
                             domain="localdomain",
                             management_interface=INTERFACES["internal"],
                             management_ip=self.nodes().masters[
                                 0].get_ip_address_by_network_name("internal"),
                             management_mask=self.ci().internal_net_mask(),
                             external_interface=INTERFACES["public"],
                             dhcp_start_address=
                             IPNetwork(self.ci().internal_network())[50],
                             dhcp_end_address=
                             IPNetwork(self.ci().internal_network())[100],
                             mirror_type='default',
                             external_ip="",
                             external_mask="",
                             parent_proxy=PARENT_PROXY,
                             puppet_master_version=PUPPET_MASTER_VERSION))
            self.remote().execute("/usr/local/sbin/bootstrap_admin_node.sh --batch-mode")
            self.prepare_cobbler_environment()
        self.environment().revert('nodes-deployed')
        for node in self.nodes():
            node.await('internal')

    def prepare_cobbler_environment(self):
        """
        Prepare vms(nodes) state with installed os.
        """
        self.deploy_cobbler()

        self.configure_cobbler(self.ci().nodes().masters[0])

        self.deploy_nodes()

    def deploy_cobbler(self):
        """
        Prepare vms(nodes) state with cobbler settings.
        """
        nodes = self.nodes().masters

        for node in nodes:
            self.assert_cobbler_ports(
                node.get_ip_address_by_network_name('internal'))
        self.environment().snapshot('cobbler', force=True)

    def assert_cobbler_ports(self, ip):
        """
        Check closed tcp|udp ports.
        """
        closed_tcp_ports = filter(
            lambda port: not tcp_ping(self.remote().sudo.ssh, ip, port),
            [22, 53, 80, 443])
        closed_udp_ports = filter(
            lambda port: not udp_ping(
                self.remote().sudo.ssh,
                ip, port), [53, 67, 68, 69])
        self.assertEquals(
            {'tcp': [], 'udp': []},
            {'tcp': closed_tcp_ports, 'udp': closed_udp_ports})

    def _add_node(self, client, token, cobbler, node_name, node_mac0, node_mac1,
                  node_mac2, node_ip, stomp_name, gateway, net_mask):
        """

        """
        system_id = client.new_system(token)
        profile = CURRENT_PROFILE
        client.modify_system_args(system_id, token,
            ks_meta=Config().get_ks_meta('master.localdomain',
                                         stomp_name),
            name=node_name,
            hostname=node_name,
            name_servers=cobbler.get_ip_address_by_network_name('internal'),
            name_servers_search="localdomain",
            profile=profile,
            gateway=gateway,
            netboot_enabled="1")
        client.modify_system(system_id, 'modify_interface', {
            "macaddress-eth0": str(node_mac0),
            "static-eth0": "1",
            "macaddress-eth1": str(node_mac1),
            "ipaddress-eth1": str(node_ip),
            "netmask-eth1": str(net_mask),
            "dnsname-eth1": node_name + DOMAIN_NAME,
            "static-eth1": "1",
            "macaddress-eth2": str(node_mac2),
            "static-eth2": "1"
        }, token)
        client.save_system(system_id, token)
        client.sync(token)

    def add_node(self, client, token, cobbler, node, gateway, net_mask):
        node_name = node.name
        node_mac0 = str(node.interfaces[0].mac_address)
        node_mac1 = str(node.interfaces[1].mac_address)
        node_mac2 = str(node.interfaces[2].mac_address)
        node_ip = str(node.get_ip_address_by_network_name('internal'))
        self._add_node(
            client, token, cobbler, node_name,
            node_mac0, node_mac1, node_mac2, node_ip,
            stomp_name=self.ci().nodes().masters[0].name,
            gateway=gateway, net_mask=net_mask,
        )

    def configure_cobbler(self, cobbler):
        """

        """
        client = CobblerClient(cobbler.get_ip_address_by_network_name('internal'))
        token = client.login('cobbler', 'cobbler')
        master = self.environment().node_by_name('master')
        for node in self.ci().client_nodes():
            self.add_node(client,
                          token,
                          cobbler,
                          node,
                          gateway=cobbler.get_ip_address_by_network_name('internal'),
                          net_mask=self.ci().internal_net_mask()
            )

        remote = master.remote('internal',
                               login='root',
                               password='r00tme')
        add_to_hosts(
            remote,
            master.get_ip_address_by_network_name('internal'),
            master.name,
            master.name + DOMAIN_NAME)

        self.environment().snapshot('cobbler-configured', force=True)

    def deploy_nodes(self):
        """

        """
        cobbler = self.ci().nodes().masters[0]
        for node in self.ci().client_nodes():
            node.start()

        for node in self.ci().client_nodes():
            await_node_deploy(cobbler.get_ip_address_by_network_name('internal'), node.name)

        for node in self.ci().client_nodes():
            node.await('internal')

        sleep(20)

        self.environment().snapshot('nodes-deployed', force=True)


if __name__ == '__main__':
    unittest.main()




