================
 Unit testing
================

You can use rspec puppet to check that  manifests and modules compile and contain the expected values.
It can be used to test that specific types, classes or definitions are in the compiled catalog and that the parameters
 match the expectations. The drawback of unit testing is that it takes too much time and efforts to implement
 and support in consistent state.


В отличие от обычного программного обеспечения успешность работы Puppet зависит не только от корректности кода,
но и от многих других факторов. Это значительно уменьшает эффективность модульного тестирования, но всё же не делает
его полностью бесполезным. Unit тесты Puppet могут определить многие ошибки уже при сборке каталога,
включая довольно неочевидные и незаметные, которые могут даже не появится на следующих этапах тестирования,
а только при некоторых условиях.

It is good idea to write and use unit tests while developing puppet modules.
The rspecs are also usefull as formal documentation for classes and modules.


Unit tests run fast. They does not require any dedicated virtual machines and special environments.
You can run all the unit tests with different Puppet versions on one single testing server.

It takes too much time and effort to write all needed rspecs for all the puppet modules we use.
Even when it done it could not give substantial improvement for QA testing.


Jenkins
----------------------
** at the present time we have no jobs for unit testing and no one supports the unit test development.** :





