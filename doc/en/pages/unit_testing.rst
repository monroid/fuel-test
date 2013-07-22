=============
 Unit testing
=============

Rspec-puppet can be used to check that manifests and modules does compile and contain the expected values.
This method can be used to test that specific resources, classes and definitions in the compiled catalog have all
and expected parameters. The drawback of unit testing is that it takes too much time and efforts to implement
and support set of specs in consistent and actual state.

In contrast to usual software success of Puppet manifests depends not only on correctness of their code but on many
other factors as well. It greatly reduces effectiveness of module testing but doesn't make it useless at all.
Puppet unit tests can detect many errors during catalog compile stage including many hidden and hard to detect ones
that even may not be detected on other testing stages.

Usually it's a good idea to write and use unit tests while developing puppet modules. The Rspecs are also useful as
formal documentation for classes and modules.

Unit tests run fast. They does not require any dedicated virtual machines and special environments.
You can run all the unit tests with different Puppet versions on one single testing server using different Ruby
environments.

It would take too much time and effort to write all Rspecs for every Puppet module we use. Even when it would be done
there will be no substantial improvement neither fo developers nor for testers.

Jenkins
-------

At the present time we have no jobs for unit testing and no one supports the unit test development.





