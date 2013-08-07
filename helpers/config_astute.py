import yaml
from environment.environment import Environment
from settings import DOMAIN_NAME_WDOT


class Config():
    def __init__(self, env):
        self.env = env
        self.master_ip = self.env.get_master_ip()

    def generate(self, **kwargs):
        config = {
            "attributes": self.attributes(**kwargs),
            "engine": self.engine(**kwargs),
            "nodes": self.nodes(**kwargs)
        }

        return yaml.safe_dump(config, default_flow_style=False)

    def nodes(self, **kwargs):
        nodes = {}
        for node in self.env.nodes().slaves:
            node_info = {
                            "id": 1,
                            "uid": 1,
                            "name": node.name,
                            "mac": node.interfaces.filter(network__name='internal')[0].mac_address,
                            "ip": str(node.get_ip_address_by_network_name('internal')),
                            "profile": kwargs.get('profile', 'centos-x86_64'),
                            "fqdn": node.name + DOMAIN_NAME_WDOT,
                            "power_type": 'ssh',
                            "power_user": 'root',
                            "power_pass": "/root/.ssh/bootstrap.rsa",
                            "power_address": str(node.get_ip_address_by_network_name('internal')),
                            "netboot_enabled": 1,
                            "name_servers": "! '%s'" % self.master_ip,
                            "puppet_master": kwargs.get('puppet_master', 'master' + DOMAIN_NAME_WDOT),
                            "ks_meta": self._get_ks_meta(node),
                            "interfaces": self._get_interfaces(node),
                            "interfaces_extra": self._get_interfaces_extra(),
                            "meta": self._get_meta(node),
                            "error_type": ""
            }

            nodes.update({node.name: node_info})

        return nodes

    def _get_interfaces_extra(self):
        return {"eth0": {"onboot": 'yes',
                         "peerdns": 'no'},
                "eth1": {"onboot": 'no',
                         "peerdns": 'no'},
                "eth2": {"onboot": 'no',
                        "peerdns": 'no'},

                }

    def _get_ks_meta(self, node):
        return True

    def _get_interfaces(self, node):
        return True

    def _get_meta(self, node):
        return True

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
                'nagios_master': kwargs.get('nagios_master', 'master' + DOMAIN_NAME_WDOT),
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

    def power_info(self, **kwargs):
        power = {
                    'power_type': kwargs.get('power_type', 'ssh'),
                    'power_user': kwargs.get('power_user', 'root'),
                    'name_servers': kwargs.get('name_servers', self.master_ip),
                    'power_pass': kwargs.get('power_pass', '/root/.ssh/bootstrap.rsa'),
                    'netboot_enabled': kwargs.get('netboot_enabled', '1')

        }

        return power

    def task_uuid(self, deployment_task='deployment_task'):
        return {'task_uuid': deployment_task}

    def ks_meta(self, **kwargs):
        meta = {
                    'mco_enable': kwargs.get('mco_enable', 1),
                    'mco_vhost': kwargs.get('mco_vhost', 'mcollective'),
                    'mco_pskey': kwargs.get('mco_pskey', 'unset'),
                    'mco_user': kwargs.get('mco_user', 'mcollective'),
                    'puppet_enable': kwargs.get('puppet_enable', 0),
                    'install_log_2_syslog': kwargs.get('install_log_2_syslog', 1),
                    'mco_password': kwargs.get('mco_password', 'marionette'),
                    'puppet_auto_setup': kwargs.get('puppet_auto_setup', 1),
                    'puppet_master': kwargs.get('puppet_master', 'master' + DOMAIN_NAME_WDOT),
                    'mco_auto_setup': kwargs.get('mco_auto_setup', 1),
                    'auth_key': kwargs.get('auth_key', '""'),
                    'puppet_version': kwargs.get('puppet_version', '2.7.19'),
                    'mco_connector': kwargs.get('mco_connector', 'rabbitmq'),
                    'mco_host': kwargs.get('mco_host', self.master_ip)
        }

        return meta


if __name__ == "__main__":
    env = Environment()
    config_yaml = Config(env)
    print config_yaml.generate()

