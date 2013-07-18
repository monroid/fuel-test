=============
Introduction
=============
Fuel-test is a suite of libraries and scripts for QA testing of the Fuel library (https://fuel.mirantis.com/).

The main goal is the check functionality and accordance to specs of Fuel on the following environments:

- single
- simple
- minimal
- compact
- full

Fuel-test provides support for

- Syntax and Style Check
- Unit testing (rspec)
- Integration testing of puppet modules
- System testing
- Tempest test suite ( for OpenStack )

Fuel-test includes standalone checks for each Fuel module to simplify deployment and troubleshooting of the whole system.
Regular automated testing of full deployment form the basis of Continuous integration (CI).
The traditional waterfall or iterative development with integration phase in the end leads to the greater risk of multiple integration conflicts and failures.

In the waterfall projects without  CI practices, development team time and energy was regularly drained in the period lead-
ing up to a release by what was known as the Integration Phase.  This was hard work, sometimes involving
the integration of months of conflicting changes. It was very hard to anticipate the types
of issues that would crop up, and even harder to fix them, as it could involve reworking
code that had been written weeks or months before. This painful process, fraught with
risk and danger, often lead to significant delivery delays, unplanned costs and, as a
result, unhappy clients. Continuous Integration is intended  to address these issues.
Continuous Integration, in its simplest form, involves a tool that monitors your version
control system for changes. Whenever a change is detected, this tool automatically
compiles and tests your application. If something goes wrong, the tool immediately
notifies the developers so that they can fix the issue immediately.

 Combined with automated end-to-end acceptance tests, CI can also act as a communication tool, pub-
lishing a clear picture of the current state of development efforts. And it can simplify
and accelerate delivery by helping you automate the deployment process, letting you
deploy the latest version of your application either automatically or as a one-click
process.
In essence, Continuous Integration is about reducing risk by providing faster feedback.
First and foremost, it is designed to help identify and fix integration and regression
issues faster, resulting in smoother, quicker delivery, and fewer bugs. By providing
better visibility for both technical and non-technical team members on the state of the
project, Continuous Integration can open and facilitate communication channels be-
tween team members and encourage collaborative problem solving and process im-
provement. And, by automating the deployment process, Continuous Integration helps
you get your software into the hands of the testers and the end users faster, more reli-
ably, and with less effort.
This idea of automated deployment is important. Indeed, if you take automating the
deployment process to its logical conclusion, you could push every build that passes
the necessary automated tests into production.


Continuous integration (CI) together with test driven development (TDD) are parts of Agile software development.
