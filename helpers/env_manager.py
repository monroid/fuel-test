#!/usr/bin/env python

from time import sleep
import tarfile

from helpers.functions import root
from devops.manager import Manager


class EnvManager():
    """
    Class for create environment in puppet modules testing.
    """
    login = "root"
    password = "r00tme"

    def __init__(self, base_image='/var/lib/libvirt/images/ubuntu-12.04.1-server-amd64-base.qcow2'):
        """
        Constructor for create environment.
        """
        self.manager = Manager()
        self.environment = self.manager.environment_create('test_env')
        self.base_image = base_image
        self._create_env()

    def _create_env(self):
        """
        Create environment with default settings.
        """
        internal = self.manager.network_create(environment=self.environment, name='internal', pool=None)
        external = self.manager.network_create(environment=self.environment, name='external', pool=None)
        private = self.manager.network_create(environment=self.environment, name='private', pool=None)

        node = self.manager.node_create(name='node', environment=self.environment)

        self.manager.interface_create(node=node, network=internal)
        self.manager.interface_create(node=node, network=external)
        self.manager.interface_create(node=node, network=private)

        volume = self.manager.volume_get_predefined(self.base_image)

        v3 = self.manager.volume_create_child('test_vol', backing_store=volume, environment=self.environment)

        self.manager.node_attach_volume(node=node, volume=v3)

        self.environment.define()

        self.environment.start()

    def _remote(self, node_name='node', net_name='public'):
        """
        Return remote access to node by name with default login/password.
        """
        return self.environment().node_by_name(node_name).remote(net_name, login=self.login, password=self.password)


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
        self._remote(node_name=node_name, net_name=net_name).execute(command)

    def upload(self, source, dest, node_name='node', net_name='public'):
        """
        Upload file(s) to node.
        """
        self._remote(node_name=node_name, net_name=net_name).upload(source, dest)

    def upload_modules(self, node_name='node', remote_dir="/etc/puppet/modules/"):
        """
        Upload puppet modules.
        """
        module_dir = root('deployment', 'puppet')

        remote = self._remote(node_name=node_name)

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


