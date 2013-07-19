===========================================
Appendix B -- Fuel-test directory structure
===========================================

Fuel test suit and infrastructure
---------------------------------

All tests consist of creating virtual environments and deploying OpenStack inside it and then running Tempest [1]_
to do acceptance testing.

Directories inside fuel-test repositories:

 * ci		classes implementing test environments
 * config	Tempest test suit configuration files
 * doc		documentation folder
 * helpers	addition modules and functions used by other modules
 * puppet_tests	scripts for creation of integration Puppet tests using templates
 * tempest	scripts to prepare and run Tempest tests
 * tests	tests for different OpenStack reference architectures

other files:

 * settings.py	general settings for all OpenStack deployment scripts
 * prepare.py	Tempest test suit configuration file
 * pip-requires	list of test suit dependencies

.. [1]  Tempest --- OpenStack Acceptance Testing Suit (https://github.com/openstack/tempest)

Devops library
--------------

This library allows to create virtual environments using libvirt and KVM as a hypervizor. It can be found in this
separate repository https://github.com/Mirantis/devops.git

Directory structure:

 * bin dos.py -- virtual environments control tool
 * devops -- Devops library files
 * docs	-- documentation stubs, getstart.rst (quick start guide)
 * samples -- examples of virtual environment creation

Classes and methods
-------------------

Virtual environment creation classes (fuel_test/ci)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

 * *CiBase* (ci_base.py)  --- basic class for preparation of CI environments
 * *CiVM* (ci_bm.py) ---  class for deployment testing environment on Bare Metal (physical) servers
 * *CiBM* (ci_vm.py) ---  class for deployment testing environment on virtual machines

This classes are used by all deployment classes FullTestCase, CompactTestCase, SimpleTestCase, SingleTestCase and
other deployment modes.

Classes to run testing scripts(fuel_test/tests)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

(С) FullTestCase --- continuous integration environment deployment class. This class implements ``test_full`` method
that should be run using nosetests (https://nose.readthedocs.org). It deploys OpenStack it "Multi node HA Standalone"
variant using Fuel. Actually there is only one test that does nothing but OpenStack deployment.
There are also classes for other architecture variants such as CompactTestCase, MinimalTestCase, SimpleTestCase,
SingleTestCase and others.

FullTestCase methods:

 *  deploy -- run deployment using selected method (with astute or without it)
 *  deploy_one_by_one -- deploy using Puppet manifests
 *  deploy_by_astute -- deploy using astute
 *  prepare_astute -- creates astute configuration files and configures *Cobbler*
 *  test_full -- runs deployment test using deploy method and creates virtual machines snapshots

(С) CompactTestCase (test_compact.py) --- this class implements OpenStack Multi-node (HA) deployment (Compact) modes.

CompactTestCase class methods:

 * deploy_compact -- run deployment  of managed nodes using Puppet agent. This method is used by all other tests.
 * test_deploy_compact_quantum -- deployment test with Quantum on controller nodes.
 * test_deploy_compact_quantum_standalone -- deployment test with Quantum as a separate node.
 * test_deploy_compact_wo_quantum -- deployment test without Quantum.
 * test_deploy_compact_wo_quantum_cinder_all_by_ipaddr -- deployment test with Cinder on all nodes but without Quantum.
   Cinder nodes are defined by IP address lists.
 * test_deploy_compact_wo_quantum_cinder_all -- deployment test with Cinder on all nodes but without Quantum.
   Cinder nodes are defined by ``cinder_nodes=['all']``
 * test_deploy_compact_wo_loopback -- deployment test with Cinder on controller nodes with Swift loopback parameter.
 * test_deploy_compact_wo_ha_provider -- deployment test with Cinder on controller nodes but without HA setup.
 * deploy_by_astute	-- deploy using astute (duplicated in some classes and should be refactored)

(С) MinimalTestCase (test_minimal.py) --- this class implements OpenStack Multi-node (HA) deployment (Minimal) modes.

MinimalTestCase class methods:

 * deploy -- run deployment using selected method (with astute or without it)
 * deploy_one_by_one -- deploy using Puppet manifests
 * deploy_by_astute -- deploy using astute
 * prepare_astute -- creates astute configuration files and configures *Cobbler*
 * test_minimal -- runs deployment test using deploy method and creates virtual machines snapshots

(С) SimpleTestCase  (test_minimal.py)

SimpleTestCase class methods:

 * deploy -- run deployment using selected method (with astute or without it)
 * deploy_one_by_one -- deploy using Puppet manifests
 * deploy_by_astute -- deploy using astute
 * prepare_only_site_pp 
 * prepare_astute -- creates astute configuration files and configures *Cobbler*
 * test_simple -- runs deployment test using deploy method and creates virtual machines snapshots

(С) SingleTestCase (test_single.py)

SingleTestCase class methods:

 * deploy -- run deployment using selected method (with astute or without it)
 * deploy_one_by_one -- deploy using Puppet manifests
 * deploy_by_astute -- deploy using astute
 * prepare_only_site_pp 
 * prepare_astute -- creates astute configuration files and configures *Cobbler*
 * test_single -- runs deployment test using deploy method and creates virtual machines snapshots

(С) NoopTestCase

NoopTestCase class methods:

 * test_apply_all_modules_with_noop -- run all Puppet manifests with ``--noop`` (No Operation) option without any real
   changes to virtual system.

(С) NovaSubClassesTestCase (test_nova_subclasses.py)

NovaSubClassesTestCase class methods:

 * setUp 
 * test_deploy_nova_compute 
 * test_deploy_nova_api_compute 
 * test_deploy_nova_api_controller 
 * test_deploy_nova_network 
 * test_deploy_nova_consoleauth 
 * test_deploy_nova_rabbitmq 
 * test_deploy_nova_utilities 
 * test_deploy_nova_vncproxy 
 * test_deploy_nova_volume

(C) SwiftCase (test_swift.py) --- Swift testing class (Not Used!)
(С) CobblerClient (cobbler_client.py) -- working with *Cobbler* using its RPC.
(С) CobblerTestCase ( vm_test_case.py ) -- base class used to implement other test case deployments ("Single node",
    Multi node HA Standalone", "Multi node HA Compact Swift" and others)

(C) BaseTestCase (base_test_case.py) -- basic parent class delivered from TestCase module used to build CobblerTestCase
    (vm_test_case.py) and other test classes.

Helper modules classes and their methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Classes:

(С) Astute (astute.py)
    (F) config
    (F) test_minimal_config 
    (F) __init__	

(С) Config (config.py)
    (F) generate
    (F) yaml.safe_dump
    (F) orchestrator_common
    (F) openstack_common
    (F) ci.public_router
    (F) cobbler_common
    (F) get_ks_meta
    (F) cobbler_nodes

(С) SelfTest (iso_master.py)
    (F) get_config
    (F) _get_config
    (F) test_config

(С) Manifest (manifest.py)
(С) Template (manifest.py)
(С) Nodes (node_roles.py)
(С) NodeRoles (node_roles.py)
(С) Prepare (prepare.py)
(С) TestConfig (test_config.py)
(С) TestManifest (test_manifest.py)

Module functions.py --- contains many useful functions:

  *  udp_ping --- checks availability of given UDP port
  *  tcp_ping --- checks availability of given UDP port
  *  load --- reads a file and returns its content
  *  extract_virtual_ips --- extracts IP address from a string to dictionary
  *  write_config --- writes config file on given remote host
  *  retry --- repeats given function with 1 second interval until it pass successfully or until retry count runs out
  *  install_packages2 --- installs packages on given hosts
  *  install_packages --- installs packages on given hosts
  *  update_pms --- update repository metadata on the given hosts
  *  update_pm --- update repository metadata on the given host
  *  add_nmap --- installs ``nmap`` package on the given host
  *  add_epel_repo_yum --- ads epel repositoiry to the given host by installing ``epel-release-6-8.noarch.rpm`` package
  *  delete_epel_repo_yum --- remove epel repository from the given host
  *  add_puppet_lab_repo --- adds puppetlabs repository to the given host by installing its package.
  *  remove_puppetlab_repo --- removes puppetlabs repository from the given host.
  *  setup_puppet_client --- runs puppet client on the given host
  *  start_puppet_master --- runs puppet master on the given host
  *  start_puppet_agent --- runs puppet agent on the given host
  *  request_cerificate --- checks if a certificate is present on the given host
  *  switch_off_ip_tables --- removes all iptables rules on the given host (by iptables -F)
  *  puppet_apply --- executes ``puppet apply`` on the given host
  *  setup_puppet_master  ---  configures and runs puppet master on the given host
  *  upload_recipes --- upload puppet modules to the /etc/puppet/modules/ directory on the given host (using recipes.tar)
  *  upload_keys --- uploads ssh keys to the given host
  *  change_host_name --- changes hostname of the given host
  * update_host_name_centos --- changes name of the given host using /etc/sysconfig/network (for Red Hat based systems)
  * update_host_name_ubuntu --- changes name of the given host using /etc/hostname (for Debian bases systems)
  * add_to_hosts --- adds line to /etc/hosts file on remote host
  * check_node_ready --- checks if this node is ready using *Cobbler*
  * await_node_deploy --- checks if this node is ready using *Cobbler* waiting for the end of its deployment
  * build_astute --- assemble astute.gem on the given host using gem and gemspec
  * install_astute --- installs astute using gem
  * is_not_essex --- check OpenStack version using environment variables
