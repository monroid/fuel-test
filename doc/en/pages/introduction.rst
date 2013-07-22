============
Introduction
============

Fuel-test is a suite of libraries and scripts for QA testing of the Fuel library (https://fuel.mirantis.com/).
The main goal of this project is to check the functionality and accordance to specs on the following environments:

- single
- simple
- minimal
- compact
- full

Fuel-test provides support for:

- Syntax and Style Check
- Unit testing (Rspec)
- Integration testing of puppet modules
- System testing
- Tempest test suite (for OpenStack)

This library also includes tools to check every single Puppet module using it's tests. Regular automated testing of
entire system is one of the base principals of Continuous Integration methodology. During usual waterfall or iterative
development process Integration Phase usually is one of last phases. Sometimes it could become very complex and time
consuming especially when there are some unexpected problems. It can lead to additional costs and even postponing of
the next release of the product.

Moving to Continuous Integration could decrease these risks and help with early error detection. Continuous integration
(CI) together with test driven development (TDD) are the parts of Agile software development paradigm.
