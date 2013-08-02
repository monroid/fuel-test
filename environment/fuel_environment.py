import os
import time
import logging
from devops.helpers.helpers import wait
from environment import Environment
from settings import EMPTY_SNAPSHOT, DOMAIN_NAME

logger = logging.getLogger('__name__')


class FuelEnvironment(Environment):
    installation_timeout = 1800
    deployment_timeout = 1800
    puppet_timeout = 1000

    def __init__(self):
        self.name = os.environ.get('ENV_NAME', 'fuel')
        super(FuelEnvironment, self).__init__(self.name)

    def wait_bootstrap(self):
        logging.info("Waiting while bootstrapping is in progress")
        log_path = "/var/log/puppet/bootstrap_admin_node.log"
        wait(
            lambda: not
            self.nodes().admin.remote('internal', 'root', 'r00tme').execute(
                "grep 'Finished catalog run' '%s'" % log_path
           )['exit_code'],
            timeout=self.puppet_timeout
        )

    def get_keys(self, node):
        params = {
            'ip': node.get_ip_address_by_network_name('internal'),
            'mask': self.get_netmask_by_netname('internal'),
            'gw': self.get_router_by_netname('internal'),
            'hostname': '.'.join(('master', DOMAIN_NAME))
        }
        keys = (
            "<Esc><Enter>\n"
            "<Wait>\n"
            "vmlinuz initrd=initrd.img ks=cdrom:/ks.cfg\n"
            " ip=%(ip)s\n"
            " netmask=%(mask)s\n"
            " gw=%(gw)s\n"
            " dns1=%(gw)s\n"
            " hostname=%(hostname)s\n"
            " <Enter>\n"
        ) % params

        return keys

    def get_environment(self):
        return self.get_empty_state() or self._prepared_environment()

    def _prepared_environment(self):
        self.start()
        time.sleep(20)
        admin = self.nodes().admin
        admin.send_keys(self.get_keys(admin))
        admin.await('internal', timeout=10 * 60)
        self.wait_bootstrap()
        time.sleep(10)
        self.environment.snapshot(EMPTY_SNAPSHOT)
