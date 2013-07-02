import logging
from time import sleep
import unittest
from helpers.env_manager import EnvManager

LOG = logging.getLogger(__name__)

class TestPuppetModule{{ module.name|title }}(unittest.TestCase):
    def setUp(self):
        self.env = EnvManager()
        self.env.await()
        if not self.env.snapshot_exist(snap_name="before_test"):
            self.env.create_snapshot_env(snap_name="before_test")
        self.env.upload_files('{{ modules_path }}/{{ module.name }}', '{{ internal_modules_path }}')

{% for test in module.tests %}
    def test_{{ test.name|title }}(self):
        self.env.execute_cmd("puppet apply --verbose --detailed-exitcodes --modulepath='{{ internal_modules_path }}' '{{ internal_modules_path }}/{{ module.name }}/{{ test.path }}/{{ test.file }}'")
{% endfor %}

    def tearDown(self):
        self.env.revert_snapshot_env("before_test")

if __name__ == '__main__':
    unittest.main()
