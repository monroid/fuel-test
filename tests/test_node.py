#    Copyright 2013 Mirantis, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


import logging
import unittest
from helpers.decorators import snapshot_errors, debug, fetch_logs
from tests.fuel_testcase import FuelTestCase

logging.basicConfig(
    format=':%(lineno)d: %(asctime)s %(message)s',
    level=logging.DEBUG
)

logger = logging.getLogger(__name__)
logwrap = debug(logger)


class TestNode(FuelTestCase):
    @snapshot_errors
    @logwrap
    @fetch_logs
    def test_nodes_provision(self):
        self.bootstrap_nodes()
        self.generate_astute_config()
        ps_out = self.get_master_ssh().execute('ls -al /root/')['stdout']
        logging.debug('Output of /root: %s' % ps_out)
        res = self.get_master_ssh().check_stderr("astute -f /root/astute.yaml -c provision", True)
        self.assertEqual(0, res)


if __name__ == '__main__':
    unittest.main()
