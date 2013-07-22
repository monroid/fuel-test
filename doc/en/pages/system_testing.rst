==============
System Testing
==============

System testing checks the entire system not just some of its components. It consists of doing complete deployment
of OpenStack using Fuel library. First it makes *iso* images for all supported operating systems, then runs the
deployment process inside virtual environments and finally proceeds to testing phase to check does everything work
as expected.

There are several supported reference architectures that are being tested:

- single
- simple
- minimal
- compact
- full

Scheme of system testing process:

.. image:: images/system_test_process_overview_small.png
    :alt: Scheme of system testing process
    :align: center

Prepare Stage
-------------

- fuel-iso -- the image of the last version of Fuel library to deploy from. It is always built automatically by
  testing scripts using some predefined settings:

    Example of setting to build *ISO* image:

    - export USEEXTIF=eth0 - predefined main network interface of the virtual environment.
    - export TGTDRIVE=vda - name of the virtual disk for system installation.
    - export ISO_URL=http://172.18.67.168/centos-repo/centos-6.4/ - path to the *iso* image.
    - export MIRANTIS_MIRROR=http://172.18.67.168/centos-repo/epel-fuel-folsom-2.1/mirror.internal.list - path to the
      custom repository to get all packages from.

- prepare virtualenv https://pypi.python.org/pypi/virtualenv. See Appendix A.
- install all needed packages into created virtualenv, https://github.com/monroid/fuel-test/blob/master/pip-requires.
  See Appendix A.
- configure testing script using this configuration file https://github.com/Mirantis/fuel-test/blob/master/settings.py
  or using environment variables.

  Example of environment variable to configure deployment process:

    - export DEBUG=true
    - export PUPPET_GEN=2
    - export ASTUTE_USE=false
    - export MIRROR_TYPE=default
    - export ISO_IMAGE=/home/jenkins/workspace/fuel_iso_for_tests_srv08/fuel/iso/build/iso/fuel-centos-6.4-x86_64-3.0.iso
    - export CONTROLLERS=3
    - export COMPUTES=3
    - export STORAGES=0
    - export PROXIES=0
    - export QUANTUMS=0
    - export OS_FAMILY=centos
    - export CURRENT_PROFILE=centos64_x86_64

Deployment Stage
----------------

To run the system test you should:

  - activate virtualenv::

    source ./venv/bin/activate

  - run the test::

    nosetests fuel fuel_test.cobbler.test_compact:CompactTestCase.test_deploy_compact_quantum --with-xunit -s -d -l DEBUG

There are several system test versions you can run:

    - fuel-test.tests.test_single
    - fuel-test.tests.test_simple
    - fuel-test.tests.test_minimal:MinimalTestCase.test_minimal
    - fuel-test.tests.test_compact:CompactTestCase.test_deploy_compact_quantum
    - fuel-test.tests.test_compact:CompactTestCase.test_deploy_compact_wo_quantum
    - fuel-test.tests.test_quantum_standalone_no_swift:QstTestCase.test_quantum_standalone_no_swift
    - fuel-test.tests.test_full:FullTestCase.test_full

System test stages are following:

    - install OS on the master node.
    - configure *Cobbler* and install OS on all managed systems
    - prepare *Puppet* configuration
    - deploy *OpenStack* on all managed systems using orchestration tools and *Puppet*

Success or failure of the deployment can de be determined by *Puppet* agent logs analysis.

Tempest
-------

If system deployment went without errors then testing scripts proceed to the acceptance testing stage. It creates user
and tenants using Tempest tool. Then it tries to create cloud based virtual system inside deployed *OpenStack*
instance.

If all stages passed without errors deployment can be considered successful. Regardless of outcome all results are
stored in Jenkins in *xUnit* format.

Jenkins
-------

ISO:
    - http://jenkins-product.srt.mirantis.net:8080/view/fuel-iso/
    - http://jenkins-product.srt.mirantis.net:8080/view/fuel-iso/job/fuel_iso_for_tests_srv07/
    - http://jenkins-product.srt.mirantis.net:8080/view/fuel-iso/job/fuel_iso_for_tests_srv08/
    - http://jenkins-product.srt.mirantis.net:8080/view/fuel-iso/job/fuel_iso_grizzly_msk_for_service

System tests:

    - http://jenkins-product.srt.mirantis.net:8080/view/tempest/
    - http://jenkins-product.srt.mirantis.net:8080/view/tempest/job/grizzly-compact/
    - http://jenkins-product.srt.mirantis.net:8080/view/tempest/job/grizzly-full/
    - http://jenkins-product.srt.mirantis.net:8080/view/tempest/job/grizzly-simple/
    - http://jenkins-product.srt.mirantis.net:8080/view/tempest/job/tempest-grizzly-ubuntu/
