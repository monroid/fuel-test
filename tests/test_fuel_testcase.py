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
from fuel_testcase import FuelTestCase

logging.basicConfig(
    format=':%(lineno)d: %(asctime)s %(message)s',
    level=logging.DEBUG
)

logger = logging.getLogger(__name__)
logwrap = debug(logger)


class TestNode(FuelTestCase):
    @logwrap
    @fetch_logs
    def test_client_nodes(self):
        print self.client.list_nodes()

    # @logwrap
    # @fetch_logs
    # def test_nailgun_nodes(self):
    #     self.nailgun_nodes(self.env.nodes())

    @logwrap
    @fetch_logs
    def test_devops_nodes_by_names(self):
        print self.devops_nodes_by_names(['master'])


if __name__ == '__main__':
    unittest.main()
