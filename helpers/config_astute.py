import yaml
from environment.environment import Environment
from settings import DOMAIN_NAME


class Config():
    def __init__(self, env):
        self.env = env
        self.master_ip = env.nodes().admin.get_ip_address_by_network_name('internal')

    def generate(self, **kwargs):
        config = {
            "attributes": self.attributes(**kwargs),
            "engine": self.engine(**kwargs)
        }

        #config.update(self.cobbler_nodes())

        return yaml.safe_dump(config, default_flow_style=False)

    # def orchestrator_common(self, ci, template):
    #     config = {"task_uuid": "deployment_task"}
    #     attributes = {"attributes": {"deployment_mode": template.deployment_mode, "deployment_engine": "simplepuppet"}}
    #     config.update(attributes)
    #
    #     return config
    #
    # def openstack_common(self, ci, nodes, quantums, cinder, quantum_netnode_on_cnt, create_networks, quantum, swift,
    #                      loopback, use_syslog, cinder_nodes):
    #     if not cinder_nodes: cinder_nodes = []
    #     if not quantums: quantums = []
    #
    #     node_configs = Manifest().generate_node_configs_list(ci, nodes)
    #
    #     master = ci.nodes().masters[0]
    #
    #     config = {"auto_assign_floating_ip": True,
    #               "create_networks": create_networks,
    #               "default_gateway": ci.public_router(),
    #               "deployment_id": Manifest().deployment_id(ci),
    #               "dns_nameservers": Manifest().generate_dns_nameservers_list(ci),
    #               "external_ip_info": Manifest().external_ip_info(ci, quantums),
    #               "fixed_range": Manifest().fixed_network(ci),
    #               "floating_range": Manifest().floating_network(ci),
    #               "internal_interface": Manifest().internal_interface(),
    #               "internal_netmask": ci.internal_net_mask(),
    #               "internal_virtual_ip": ci.internal_virtual_ip(),
    #               "mirror_type": Manifest().mirror_type(),
    #               "nagios_master": ci.nodes().controllers[0].name + DOMAIN_NAME,
    #               "network_manager": "nova.network.manager.FlatDHCPManager",
    #               "nv_physical_volumes": ["/dev/vdb"],
    #               "private_interface": Manifest().private_interface(),
    #               "public_interface": Manifest().public_interface(),
    #               "public_netmask": ci.public_net_mask(),
    #               "public_virtual_ip": ci.public_virtual_ip(),
    #               "quantum": quantum,
    #               "repo_proxy": "http://%s:3128" % master.get_ip_address_by_network_name('internal'),
    #               "segment_range": "900:999",
    #               "swift": swift,
    #               "swift_loopback": loopback,
    #               "syslog_server": str(master.get_ip_address_by_network_name('internal')),
    #               "use_syslog": use_syslog,
    #               "cinder": cinder,
    #               "quantum_netnode_on_cnt": quantum_netnode_on_cnt
    #     }
    #
    #     config.update({"cinder_nodes": cinder_nodes})
    #
    #     config.update({"nodes": node_configs})
    #
    #     return config
    #
    # def cobbler_common(self, ci):
    #     config = {"gateway": str(ci.nodes().masters[0].get_ip_address_by_network_name('internal')),
    #               "name-servers": str(ci.nodes().masters[0].get_ip_address_by_network_name('internal')),
    #               "name-servers-search": "localdomain",
    #               "profile": CURRENT_PROFILE}
    #
    #     ksmeta = self.get_ks_meta(ci.nodes().masters[0].name + DOMAIN_NAME, ci.nodes().masters[0].name)
    #
    #     config.update({"ksmeta": ksmeta})
    #
    #     return config
    #
    # def get_ks_meta(self, puppet_master, mco_host):
    #     return ("puppet_auto_setup=1 "
    #             "puppet_master=%(puppet_master)s "
    #             "puppet_version=%(puppet_version)s "
    #             "puppet_enable=0 "
    #             "mco_auto_setup=1 "
    #             "ntp_enable=1 "
    #             "mco_pskey=un0aez2ei9eiGaequaey4loocohjuch4Ievu3shaeweeg5Uthi "
    #             "mco_stomphost=%(mco_host)s "
    #             "mco_stompport=61613 "
    #             "mco_stompuser=mcollective "
    #             "mco_stomppassword=AeN5mi5thahz2Aiveexo "
    #             "mco_enable=1 "
    #             "interface_extra_eth0_peerdns=no "
    #             "interface_extra_eth1_peerdns=no "
    #             "interface_extra_eth2_peerdns=no "
    #             "interface_extra_eth2_promisc=yes "
    #             "interface_extra_eth2_userctl=yes "
    #            ) % {'puppet_master': puppet_master,
    #                 'puppet_version': PUPPET_VERSION,
    #                 'mco_host': mco_host
    #            }
    #
    # def cobbler_nodes(self, ci, nodes):
    #     all_nodes = {}
    #     for node in nodes:
    #         interfaces = {
    #             INTERFACES.get('internal'):
    #                 {
    #                     "mac": node.interfaces.filter(network__name='internal')[0].mac_address,
    #                     "static": 1,
    #                     "ip-address": str(node.get_ip_address_by_network_name('internal')),
    #                     "netmask": ci.internal_net_mask(),
    #                     "dns-name": node.name + DOMAIN_NAME,
    #                     "management": "1"
    #                 }
    #         }
    #         interfaces_extra = {
    #             "eth0":
    #                 {"peerdns": 'no'},
    #             "eth1":
    #                 {"peerdns": 'no'},
    #             "eth2":
    #                 {"peerdns": 'no',
    #                  "promisc": 'yes',
    #                  "userctl": 'yes'}
    #         }
    #         all_nodes.update({node.name: {"hostname": node.name,
    #                                       "interfaces": interfaces,
    #                                       "interfaces_extra": interfaces_extra,
    #                                       }
    #         }
    #     )
    #
    #     return all_nodes

    def attributes(self, **kwargs):
        attr = {'use_cow_images': kwargs.get('use_cow_images', True),
                'libvirt_type': kwargs.get('libvirt_type', 'qemu'),
                'dns_nameservers': [kwargs.get('master_ip', self.master_ip)],
                'verbose': kwargs.get('verbose', True),
                'debug': kwargs.get('verbose', True),
                'auto_assign_floating_ip': kwargs.get('auto_assign_floating_ip', True),
                'start_guests_on_host_boot': kwargs.get('start_guests_on_host_boot', True),
                'create_networks': kwargs.get('create_networks', True),
                'compute_scheduler_driver': kwargs.get('compute_scheduler_driver', 'nova.scheduler.multi.MultiScheduler'),
                'quantum': kwargs.get('quantum', True),
                'master_hostname': kwargs.get('master_hostname', 'controller-01'),
                'nagios': kwargs.get('nagios', False),
                'nagios_master': kwargs.get('nagios_master', 'master' + DOMAIN_NAME),
                'proj_name': kwargs.get('proj_name', self.env.name),
                'management_vip': kwargs.get('management_vip', self.env.internal_virtual_ip()),
                'public_vip': kwargs.get('public_vip', self.env.public_virtual_ip()),
                'novanetwork_parameters': {
                                            'fixed_network_range': kwargs.get('fixed_network_range', 'CIDR'),
                                            'vlan_start': kwargs.get('vlan_start', '<1-1024>'),
                                            'network_manager': kwargs.get('network_manager', ':TODO'),
                                            'network_size': kwargs.get('network_size', ':TODO'),
                                        },
                'quantum_parameters': {
                                        'tenant_network_type': kwargs.get('tenant_network_type', 'gre'),
                                        'segment_range': kwargs.get('segment_range', '! 300:500'),
                                        'metadata_proxy_shared_secret': kwargs.get('metadata_proxy_shared_secret', 'quantum'),
                                    },
                'mysql': {
                            'root_password': kwargs.get('root_password', 'root'),
                        },

                'glance': {
                            'db_password': kwargs.get('glance_db_password', 'glance'),
                            'user_password': kwargs.get('glance_user_password', 'glance'),
                        },

                'swift': {
                            'user_password': kwargs.get('swift_user_password', 'swift_pass'),
                        },

                'nova': {
                            'db_password': kwargs.get('nova_db_password', 'nova'),
                            'user_password': kwargs.get('nova_user_password', 'nova'),
                        },
                'access': {
                            'password': kwargs.get('access_password', 'admin'),
                            'user': kwargs.get('access_user', 'admin'),
                            'tenant': kwargs.get('tenant', 'admin'),
                            'email': kwargs.get('email', 'admin@example.org'),

                        },
                'keystone': {
                            'db_password': kwargs.get('keystone_db_password', 'keystone'),
                            'admin_token': kwargs.get('admin_token', 'nova'),
                        },
                'quantum_access': {
                            'user_password': kwargs.get('quantum_user_password', 'quantum'),
                            'db_password': kwargs.get('quantum_db_password', 'quantum'),
                        },
                'rabbit': {
                            'password': kwargs.get('rabbit_password', 'nova'),
                            'user': kwargs.get('rabbit_user', 'nova'),
                        },
                'cinder': {
                            'password': kwargs.get('cinder_password', 'cinder'),
                            'user': kwargs.get('cinder_user', 'cinder'),
                        },
                'base_syslog': {
                            'syslog_port': kwargs.get('base_syslog_port', '514'),
                            'syslog_server': kwargs.get('base_syslog_server', self.master_ip),
                        },
                'syslog': {
                            'syslog_port': kwargs.get('syslog_port', '514'),
                            'syslog_transport': kwargs.get('syslog_transport', 'udp'),
                            'syslog_server': kwargs.get('syslog_server', self.master_ip),
                        },
                'floating_network_range': [kwargs.get('floating_network_range', self.master_ip)],
                'deployment_id': kwargs.get('deployment_id', 1),
                'deployment_mode': kwargs.get('deployment_mode', 'ha'),
                'deployment_source': kwargs.get('deployment_source', 'cli'),
                'deployment_engine': kwargs.get('deployment_engine', 'nailyfact'),
                }

        return attr

    def engine(self, **kwargs):
        engine = {
                    'url': kwargs.get('url', 'http://localhost/cobbler_api'),
                    'username': kwargs.get('username', 'cobbler'),
                    'password': kwargs.get('password', 'cobbler')
        }

        return engine


if __name__ == "__main__":
    env = Environment()
    config_yaml = Config(env)
    print config_yaml.generate()

