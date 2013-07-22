====================
 Integration testing
====================

Integration testing provides functional testing for a single Puppet module or for a group of modules. To run this
tests you have to prepare a special testing manifests in the *tests* directory of your module.

These manifests usually can also be an good example how the module can be used. Usually each of these tests check
one of module's parts, functions or common use cases.

Fuel-test contains some scripts to make use of this testing manifests. They can run all of the module's tests and
collect their results into Jenkins using **xUnit** XML format.

Integration tests provide much wider coverage than modular ones. They can check functionality of one or more modules
in required environments. So both code consistency and functionality are tested.

Test manifests are relatively easy to write and integration testing is also much more useful for developers. So
it would be better to focus ot it rather then on unit testing.

Testing algorithm
-----------------

In order to implement integration testing you should create special testing environment fist.
Then you can start to apply the Puppet module inside this environment and check the results.

The process of testing can be described by the following steps:

.. image:: images/integration_tests_scheme.png
   :alt: integration tests scheme
   :align: center

1. Create virtual system from prepared image with supported operating system.
2. Take a snapshot of the clean state of operating system in order to be able to revert it.
3. Run the first test in the testing environment and save the results.
4. Revert to the snapshot of the clean state.
5. Run the next test, save the result and revert once again.
6. Collect all the test results as xUnit and put it into Jenkins.

Implementing test
-----------------

To implement integration testing with Jenkins you need to create a set of test scripts for each puppet module.
Every test script should create testing environment and run all the tests for its module.
To simplify creating of such set of test scripts it is a good idea to utilize the power of template engine.

This is the scheme of this process:

.. image:: images/make_tests_templates.png
   :alt: Scheme of the integration testing
   :align: center

- First you should prepare the script implementing the aforementioned testing algorithm and make it as template.
- Then use MakeTests script to scan directory containing Puppet modules and find all the test manifests.
- It takes script's template expands paths and names for each module and creates a method to run each test manifest.
- All of these scripts are saved into a special directory.
- The Jenkins' job is created. It should run all test method of every test script and collect their results as XML file.

Using MakeTests script
----------------------

MakeTests script has 5 classes:

- **MakeTests** - main class of the script. It provides the program startup, reading and writing of files.
- **PuppetModule** - represents each Puppet module.  MakeTests object creates list of objects for each Puppet module.
- **PuppetTest** -  represents single test. PuppetModule object creates list of these objects for each test manifest.
- **Interface** - helper class.  Provides features for error and debug messages output.
- **Color** - helper class. For colorizing text output on terminal.

MakeTests accepts the following arguments:

mandatory:
- Path to directory to store the scripts built from templates.
- Path to directory with Puppet modules to be tested.
optional:
- (-m) path to directory with puppet modules on the testing environment. It is useful when you create tests not on the
system you intend to run them.
- (-t) path to the directory with templates.
- (-f) file with default template
- (-k) keep all the  previous tests

Using templates
---------------

MakeTests uses the **jinja2** template engine. It uses by default template from **templates** directory.
You can specify another template using the -f option.

You can use this set of variables inside your template:

**General variables**

- *modules_path* - Path to puppet modules on testing host system.
- *local_modules_path* - Path to modules on the system where tests were created. Usually equals to modules_path.
- *internal_modules_path* - Path to modules inside a guest virtual system.
- *internal_manifests_path* - Path to manifests inside a guest virtual system.
- *tests_directory_path* - Path to the directory containing test files.

**PuppetModule**

- *module.name* - Name of this Puppet module.
- *module.path* - Path to the Puppet module on the system where tests were built.
- *module.tests* - A list of PuppetTest objects representing every test file of this module.
- *module.dependencies* - List of direct dependencies this module depends on.

**PuppetTest**

- *test.name* - Name of this test.
- *test.path* - Path to this test. Relative to module and excluding file name.
- *test.file* - NAme of the file which this test represents.

Template files can include other template files giving you an ability to make a complex script from many pieces. Some
of these pieces can be shared by several scripts. Templates can also extend other templates by replacing some of
its blocks.

Inside your template you can use loops, control logic and different filters. You can learn more about **jinja2**
template engine here http://jinja.pocoo.org and learn all its syntax from this
file http://jinja.pocoo.org/docs/jinja-docs.pdf

Jenkins
-------

This task is made to support integration testing

http://jenkins-product.srt.mirantis.net:8080/view/puppet_integration/
