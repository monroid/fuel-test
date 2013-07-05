#!/usr/bin/env python

import tarfile
from time import sleep
from devops.helpers.helpers import ssh, tcp_ping, wait

from helpers.functions import root
from devops.manager import Manager


class EnvManager():
    """
    Class for create environment in puppet modules testing.
    """
    env_name = "puppet-integration"
    env_node_name = "node"
    env_net_public = 'public'
    env_net_internal = 'internal'
    env_net_private = 'private'
    env_vol = 'vol'
    login = "root"
    password = "r00tme"

    def __init__(self, base_image=None):
        """
        Constructor for create environment.
        """
        self.manager = Manager()
        self.base_image = base_image or '/var/lib/libvirt/images/ubuntu-12.04.1-server-amd64-base.qcow2'
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
        remote = self.remote()

        tar_file = None
        try:
            tar_file = remote.open('/tmp/recipes.tar', 'wb')

            with tarfile.open(fileobj=tar_file, mode='w', dereference=True) as tar:
                tar.add(local_dir, arcname='')

            remote.mkdir(remote_dir)
            remote.check_call('tar xmf /tmp/recipes.tar --overwrite -C %s' % remote_dir)
        finally:
            if tar_file:
                tar_file.close()

    def await(self, timeout=1200):
        wait(
            lambda: tcp_ping(self._get_public_ip(), 22), timeout=timeout)


if __name__ == "__main__":
    env = EnvManager()

    env.await()

    env.upload_modules('/home/alan/fuel/deployment/puppet')

    env.create_snapshot_env(snap_name="test1")

    env.execute_cmd('apt-get install mc')

    env.erase_env()



