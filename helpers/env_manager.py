#!/usr/bin/env python

from devops.helpers.helpers import ssh, tcp_ping, wait
from devops.manager import Manager
from helpers.functions import upload_recipes
from settings import BASE_IMAGE, NET_PUBLIC, NET_INTERNAL, NET_PRIVATE


class EnvManager():
    """
    Class for create environment in puppet modules testing.
    """
    env_name = "puppet-integration"
    env_node_name = "node"
    env_net_public = NET_PUBLIC
    env_net_internal = NET_INTERNAL
    env_net_private = NET_PRIVATE
    env_vol = 'vol'
    login = "root"
    password = "r00tme"

    def __init__(self, base_image=None):
        """
        Constructor for create environment.
        """
        self.manager = Manager()
        self.base_image = base_image or BASE_IMAGE
        self.environment = self.create_env()

    def create_env(self):
        try:
            return self.manager.environment_get(self.env_name)
        except:
            return self._define_env()

    def _define_env(self):
        """
        Create environment with default settings.
        """
        self.environment = self.manager.environment_create(self.env_name)

        internal = self.manager.network_create(environment=self.environment, name=self.env_net_internal, pool=None)
        external = self.manager.network_create(environment=self.environment, name=self.env_net_public, pool=None)
        private = self.manager.network_create(environment=self.environment, name=self.env_net_private, pool=None)

        node = self.manager.node_create(name=self.env_node_name, environment=self.environment)

        self.manager.interface_create(node=node, network=internal)
        self.manager.interface_create(node=node, network=external)
        self.manager.interface_create(node=node, network=private)

        volume = self.manager.volume_get_predefined(self.base_image)

        v3 = self.manager.volume_create_child(self.env_vol, backing_store=volume, environment=self.environment)

        self.manager.node_attach_volume(node=node, volume=v3)

        self.environment.define()

        self.environment.start()

        return self.environment

    def _get_public_ip(self):
        return self.environment.node_by_name(self.env_node_name).get_ip_address_by_network_name(self.env_net_public)

    def _ssh(self):
        return ssh(self._get_public_ip(), username=self.login, password=self.password).sudo.ssh

    def remote(self):
        """
        Return remote access to node by name with default login/password.
        """
        return self._ssh()

    def snapshot_exist(self, snap_name="before_test"):
        return self.environment.has_snapshot(name=snap_name)

    def create_snapshot_env(self, snap_name="", description="", force=True):
        """
        Create snapshot for environment.
        """
        self.environment.snapshot(name=snap_name, description=description, force=force)

    def revert_snapshot_env(self, snap_name="", destroy=True):
        """
        Revert environment to snapshot by name.
        """
        self.environment.revert(name=snap_name, destroy=destroy)

    def erase_env(self):
        """
        Erase environment.
        """
        self.environment.erase()

    def execute_cmd(self, command, debug=True):
        """
        Execute command on node.
        """
        return self.remote().execute(command, verbose=debug)['exit_code']

    def upload_files(self, source, dest):
        """
        Upload file(s) to node.
        """
        self.remote().upload(source, dest)

    def upload_modules(self, local_dir, remote_dir="/etc/puppet/modules/"):
        """
        Upload puppet modules.
        """
        upload_recipes(remote=self.remote(),
                       local_dir=local_dir,
                       remote_dir=remote_dir)

    def await(self, timeout=1200):
        wait(
            lambda: tcp_ping(self._get_public_ip(), 22), timeout=timeout)


if __name__ == "__main__":
    env = EnvManager('/var/lib/libvirt/images/centos64noswap_test06.qcow2')

    env.await()

    env.upload_modules('/home/alan/fuel/deployment/puppet')

    env.create_snapshot_env(snap_name="test1")

    env.execute_cmd('apt-get install mc')

    env.erase_env()



