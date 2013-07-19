====================================================
Appendix A -- Preparation of the testing environment
====================================================

To create a testing on a local computer you shall do following steps:

 - Install required packages::

    sudo apt-get install postgresql libpq-dev python-dev libvirt-bin qemu kvm python-libvirt python-libxml2
    python-virtualenv python-pip gksu-polkit

    # Minimal libvirt-bin package version required is 0.9.13-0ubuntu12.1

 - Setup and activate virtualenv:

    - sudo easy_install pip
    - sudo pip install virtualenv
    - virtualenv --system-site-packages venv
    - source ./venv/bin/activate

 - Add user to necessary groups and configule polkit to access libvirt if your distribution did not already
   make all needed configuration::

     sudo adduser user libvirtd
     sudo adduser user kvm

     # Because of strange devops bug, some disks for virtual nodes would be created with owner root.root,
     # while it should be libvirt-qemu.kvm.
     # To workaround this, both libvirt-qemu and user also should be added to root group::

     sudo adduser user root; sudo adduser libvirt-qemu root
     sudo '/bin/bash' -c "echo \"

     [Allow libvirt management permissions]
     Identity=unix-group:libvirt
     Action=org.libvirt.unix.manage
     ResultAny=yes
     ResultInactive=yes
     ResultActive=yes
     \">/etc/polkit-1/localauthority/50-local.d/50-nova.pkla"

     sudo service libvirt-bin restart

 - Workaround for missing libvirt for pip if you have problems with importing it
   (change paths according to Linux distro and python version used)::

    cp -Rf /usr/lib/python2.7/dist-packages/*libvirt* ./venv/lib/python2.7/site-packages
    cp -Rf /usr/lib/python2.7/dist-packages/*libxml2* ./venv/lib/python2.7/site-packages

 - Install required dependencies::

    pip install -r fuel_test/pip-requires
    pip install psycopg2 ipaddr pyyaml

 - Check Postgres cluster status, create new one if there is no, and set access mode for trust
   (warning: it is unsecure)::

    pg_lsclusters
    sudo pg_createcluster 9.1 main
    sudo sed -i "s/peer/trust/g" /etc/postgresql/9.1/main/pg_hba.conf; sudo service postgresql restart

 - Configure access and create required tables in DB::

    django-admin.py syncdb --settings devops.settings

 - Build iso for tests::

    export USEEXTIF=eth0
    cd fuel/iso
    make iso
    cd build/iso
    ls -la
    sudo md5sum fuel-centos-6.4-x86_64-*.iso

 - Configure env var for iso file::

     export ISO_IMAGE=/home/user/fuel-centos-6.4-x86_64-3.0.iso

 - Run tests::

     nosetests -w fuel_test

 - To manage deployed environments you shall use the dos.py::

     usage: dos.py [-h] {list,show,erase,start,destroy,suspend,resume,revert,snapshot}

 - KVM tuning -- To increase IO perfomance for virtual machines use::

     sudo sysctl -w vm.swappiness=0; sudo sysctl -p

 - Bash shell example::

     source ./venv/bin/activate
     export test_name=fuel_test.cobbler.test_full:FullTestCase.test_full
     export ENV_NAME=user-local-centos-full
     export fuel_release=/home/user/fuel
     export PUPPET_GEN=2
     export CREATE_SNAPSHOTS=true
     export CLEAN=true
     export ASTUTE_USE=false
     export erase=false
     export USE_ISO=true
     export ISO_IMAGE=/home/user/fuel-centos-6.4-x86_64-3.0.iso

     export CONTROLLERS=3
     export COMPUTES=2
     export STORAGES=2
     export PROXIES=2
     export OS_FAMILY=centos
     export CURRENT_PROFILE=centos64_x86_64
     export PUBLIC_POOL=10.99.0.0/24:27
     export PUBLIC_FORWARD=nat

     pushd $fuel_release
     nosetests -w $fuel_release $test_name --with-xunit -s -d -l DEBUG | tee deploy.log
     popd