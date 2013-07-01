#!/usr/bin/env python

import unittest
from helpers.vm_test_case import CobblerTestCase
from helpers.config import Config
from helpers.functions import write_config
from helpers.manifest import Template, Manifest
from settings import CREATE_SNAPSHOTS, ASTUTE_USE, PUPPET_AGENT_COMMAND


class MinimalTestCase(CobblerTestCase):
    """
    Deploy openstack in minimal mode.
    Supports multiple deployment tool --- astute or puppet.
    By default:

    - master x1
    - controller x?
    - compute x?
    - storage x?
    - proxy x?
    - quantum x0
    """
    def deploy(self):
        """
        Deploy environment.
        """
        if ASTUTE_USE:
            self.prepare_astute()
            self.deploy_by_astute()
        else:
            self.deploy_one_by_one()

    def deploy_one_by_one(self):
        """
        Deploy via puppet.
        """
        manifest = Manifest().generate_openstack_manifest(
            template=Template.minimal(),
            ci=self.ci(),
            controllers=self.nodes().controllers,
            quantums=self.nodes().quantums,
            quantum=True)
        
        Manifest().write_manifest(remote=self.remote(), manifest=manifest)
        
        self.validate(self.nodes().controllers[:1], PUPPET_AGENT_COMMAND)
        self.validate(self.nodes().controllers[1:], PUPPET_AGENT_COMMAND)
        self.validate(self.nodes().controllers[:1], PUPPET_AGENT_COMMAND)
        self.validate(self.nodes().computes, PUPPET_AGENT_COMMAND)

    def deploy_by_astute(self):
        """
        Run astute command.
        """
        self.remote().check_stderr("astute -f /root/astute.yaml -v", True)

    def prepare_astute(self):
        """
        Prepare config files for astute.
        """
        config = Config().generate(
                template=Template.minimal(),
                ci=self.ci(),
                nodes = self.nodes().controllers + self.nodes().computes,
                quantums=self.nodes().quantums,
                quantum=True,
                cinder_nodes=['controller']
            )
        print "Generated config.yaml:", config
        config_path = "/root/config.yaml"
        write_config(self.remote(), config_path, str(config))
        self.remote().check_call("cobbler_system -f %s" % config_path)
        self.remote().check_stderr("openstack_system -c %s -o /etc/puppet/manifests/site.pp -a /root/astute.yaml" % config_path, True)

    def test_minimal(self):
        """
        Unittest for deploy.
        """
        self.deploy()

        if CREATE_SNAPSHOTS:
            self.environment().snapshot('minimal', force=True)

if __name__ == '__main__':
    unittest.main()
