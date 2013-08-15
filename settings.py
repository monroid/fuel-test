import os

#[main]
OS_FAMILY = os.environ.get('OS_FAMILY', "centos")

DEFAULT_IMAGES = {
    'centos': '/var/lib/libvirt/images/centos6.4-base.qcow2',
    'ubuntu': '/var/lib/libvirt/images/ubuntu-12.04.1-server-amd64-p2.qcow2',
}

BASE_IMAGE = os.environ.get('BASE_IMAGE', DEFAULT_IMAGES.get(OS_FAMILY))

TEST_REPO = os.environ.get('TEST_REPO', 'false') == 'true'

ISO_IMAGE = os.environ.get('ISO_IMAGE', '/home/user/fuel-centos-6.4-x86_64-3.0.iso')
ISO_PATH = os.environ.get('ISO_PATH', '/home/alan/git/fuelweb/build/iso/fuelweb-centos-6.4-x86_64.iso')

PARENT_PROXY = os.environ.get('PARENT_PROXY', '')

PROFILES_COBBLER_COMMON = {
    'centos': 'centos64_x86_64',
    'ubuntu': 'ubuntu_1204_x86_64'
}

CURRENT_PROFILE = PROFILES_COBBLER_COMMON.get(OS_FAMILY)

ASTUTE_USE = os.environ.get('ASTUTE_USE', 'false') == 'true'

DOMAIN_NAME = os.environ.get('DOMAIN_NAME', 'localdomain')
DOMAIN_NAME_WDOT = '.' + DOMAIN_NAME

PUPPET_AGENT_COMMAND = 'puppet agent -tvd --evaltrace 2>&1'

SETUP_TIMEOUT = int(os.environ.get('SETUP_TIMEOUT', 600))

EMPTY_SNAPSHOT = os.environ.get('EMPTY_SNAPSHOT', 'empty')

LOGS_DIR = os.environ.get('LOGS_DIR', '/home/alan/test-logs')

#[tempest]
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'nova'
ADMIN_TENANT_ESSEX = 'openstack'
ADMIN_TENANT_FOLSOM = 'admin'

CIRROS_IMAGE = os.environ.get('CIRROS_IMAGE', 'http://srv08-srt.srt.mirantis.net/cirros-0.3.0-x86_64-disk.img')

#[nodes]
CONTROLLERS = int(os.environ.get('CONTROLLERS', 2))
COMPUTES = int(os.environ.get('COMPUTES', 2))
STORAGES = int(os.environ.get('STORAGES', 0))
PROXIES = int(os.environ.get('PROXIES', 0))
QUANTUMS = int(os.environ.get('QUANTUMS', 0))
DEFAULT_RAM_SIZE = int(os.environ.get('DEFAULT_RAM_SIZE', 1024))
COMPUTE_RAM_SIZE = int(os.environ.get('COMPUTE_RAM_SIZE', 2048))

#[puppet]
PUPPET_GEN = os.environ.get('PUPPET_GEN', "2")
PUPPET_VERSIONS = {
    'centos': {
        "2": '2.7.19-1.el6',
        "3": '3.0.1-1.el6',
        },
    'ubuntu': {
        "2": '2.7.19-1puppetlabs2',
        "3": '3.0.1-1puppetlabs1'
    },
}

PUPPET_VERSION = PUPPET_VERSIONS.get(OS_FAMILY).get(PUPPET_GEN)
PUPPET_MASTER_VERSION = PUPPET_VERSIONS.get('centos').get(PUPPET_GEN)

PUPPET_CLIENT_PACKAGES = {
    'centos': {
        "2": 'puppet-2.7.19-1.el6',
        "3": 'puppet-3.0.1-1.el6',
        },
    'ubuntu': {
        "2": 'puppet=2.7.19-1puppetlabs2 puppet-common=2.7.19-1puppetlabs2',
        "3": 'puppet=3.0.1-1puppetlabs1 puppet-common=3.0.1-1puppetlabs1'
    },
}

PUPPET_CLIENT_PACKAGE = PUPPET_CLIENT_PACKAGES.get(OS_FAMILY).get(PUPPET_GEN)
PUPPET_MASTER_SERVICE = 'thin'

#[errors]
ERROR_PREFIXES = {
    "2": "err: ",
    "3": "Error: ",
}

ERROR_PREFIX = ERROR_PREFIXES.get(PUPPET_GEN)

WARNING_PREFIXES = {
    "2": "warning: ",
    "3": "Warning: ",
}

WARNING_PREFIX = WARNING_PREFIXES.get(PUPPET_GEN)

#[network]
NET_PUBLIC = 'public'

NET_INTERNAL = 'internal'

NET_PRIVATE = 'private'

INTERFACE_ORDER = (
    NET_INTERNAL,
    NET_PUBLIC,
    NET_PRIVATE
)

INTERFACES = {
    NET_PUBLIC: 'eth0',
    NET_INTERNAL: 'eth1',
    NET_PRIVATE: 'eth2',
}

FORWARDING = {
    NET_PUBLIC: None,
    NET_INTERNAL: os.environ.get('PUBLIC_FORWARD', 'nat'),
    NET_PRIVATE: None,
}

DHCP = {
    NET_PUBLIC: False,
    NET_INTERNAL: False,
    NET_PRIVATE: False,
}

DEFAULT_POOLS = {
    'centos': {
        'public': '10.108.0.0/16:24',
        'private': '10.108.0.0/16:24',
        'internal': '10.108.0.0/16:24',
        },
    'ubuntu': {
        'public': '10.107.0.0/16:24',
        'private': '10.107.0.0/16:24',
        'internal': '10.107.0.0/16:24',
        },
}

POOLS = {
    NET_PUBLIC: os.environ.get('PUBLIC_POOL', DEFAULT_POOLS.get(OS_FAMILY).get('public')).split(':'),
    NET_PRIVATE: os.environ.get('PRIVATE_POOL', DEFAULT_POOLS.get(OS_FAMILY).get('private')).split(':'),
    NET_INTERNAL: os.environ.get('INTERNAL_POOL', DEFAULT_POOLS.get(OS_FAMILY).get('internal')).split(':')
}

NETWORK_MANAGERS = {
    "flat": 'FlatDHCPManager',
    'vlan': 'VlanManager'
}