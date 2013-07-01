#!/usr/bin/env python

from time import sleep
import tarfile

from helpers.functions import root
from devops.manager import Manager


class EnvManager():
    """
    Class for create environment in puppet modules testing.
    """
    env_name = "puppet_integration"
    env_node_name = env_name + "node"
    env_net_public = env_name + 'public'
    env_net_internal = env_name + 'internal'
    env_net_private = env_name + 'private'
    env_vol = env_name + '_vol'
    login = "root"
    password = "r00tme"

    def __init__(self, base_image='/var/lib/libvirt/images/ubuntu-12.04.1-server-amd64-base.qcow2'):
        """
        Constructor for create environment.
        """
        self.manager = Manager()
        self.environment = self.manager.environment_create(self.env_name)
        self.base_image = base_image
        self.create_env()

    def create_env(self):
        try:
            return self.manager.environment_get(self.env_name)
        except:
            self._define_env()

    def _define_env(self):
        """
        Create environment with default settings.
        """
        internal = self.manager.network_create(environment=self.environment, name=self.env_net_internal, pool=None)
        external = self.manager.network_create(environment=self.environment, name=self.env_net_external, pool=None)
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

    def _remote(self):
        """
        Return remote access to node by name with default login/password.
        """
        return self.environment().node_by_name(self.env_node_name).remote(self.env_net_public,
                                                                          login=self.login,
                                                                          password=self.password)


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

    def execute_cmd(self, command, node_name='node', net_name='public'):
        """
        Execute command on node.
        """
        self._remote(node_name=self.env_node_name, net_name=self.env_net_public).execute(command)

    def upload_files(self, source, dest, node_name='node', net_name='public'):
        """
        Upload file(s) to node.
        """
        self._remote(node_name=node_name, net_name=net_name).upload(source, dest)

    def upload_modules(self, node_name='node', remote_dir="/etc/puppet/modules/"):
        """
        Upload puppet modules.
        """
        module_dir = root('fuel_test', 'deployment', 'puppet')

        remote = self._remote(node_name=self.env_node_name)

        tar_file = None
        try:
            tar_file = remote.open('/tmp/recipes.tar', 'wb')

            with tarfile.open(fileobj=tar_file, mode='w', dereference=True) as tar:
                tar.add(module_dir, arcname='')

            remote.mkdir(remote_dir)
            remote.check_call('tar xmf /tmp/recipes.tar --overwrite -C %s' % remote_dir)
        finally:
            if tar_file:
                tar_file.close()


if __name__ == "__main__":
    env = EnvManager()

    sleep(600) #TODO: add await method

    env.create_snapshot_env(snap_name="test1")

    env.execute_cmd('apt-get install mc')

    env.erase_env()


