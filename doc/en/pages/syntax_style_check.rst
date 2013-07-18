=========================
 Syntax and Style Check
==========================

The simplest type of testing. It checks puppet  modules and manifests for syntax errors using the Puppet agent.
You can run agent with the command::

    puppet parser validate manifest.pp

You can also check the erb templates. You should expand the template and pass it to the Ruby interpreter using syntax check option::

    erb -P -x -T ’-’ mytemplate.erb | ruby -c

Puppet code should follow the style guide provided by PuppetLabs.

http://docs.puppetlabs.com/guides/style_guide.html

You need to install puppet-lint first::

    gem install puppet-lint

And then you can check the syntax and style with the command::

    puppet-lint --with-filename manifest.pp

All these checks can be performed with modern integrated IDE environments like Geppetto IDE.

Jenkins
----------------------
** Jenkins jobs provided for syntax and style checking of Puppet files **

- http://jenkins-product.srt.mirantis.net:8080/view/fuel/job/fuel-puppet-3.0.1-parseonly-essex/
- http://jenkins-product.srt.mirantis.net:8080/view/fuel/job/fuel-puppet-3.0.1-parseonly-folsom/
- http://jenkins-product.srt.mirantis.net:8080/view/fuel/job/fuel-puppet-2.7-parseonly-folsom/
- http://jenkins-product.srt.mirantis.net:8080/view/fuel/job/fuel-puppet-2.7-parseonly-essex/
