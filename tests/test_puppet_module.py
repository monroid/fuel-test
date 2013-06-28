import logging
from time import sleep
import unittest
from helpers.env_manager import EnvManager

LOG = logging.getLogger(__name__)

class TestPuppetModule(unittest.TestCase):
    def setUp(self):
        self.env = EnvManager()
        sleep(600) #TODO: add await method
        self.env.upload_modules()
        self.env.create_snapshot_env(snap_name="before_test")

    def test_acpid_on(self):
        self.env.execute_cmd("puppet apply  --modulepath=/etc/puppet/modules/acpid_on.pp")

    def test_acpid_off(self):
        self.env.execute_cmd("puppet apply  --modulepath=/etc/puppet/modules/acpid_off.pp")

    def tearDown(self):
        self.env.revert_snapshot_env("before_test")
