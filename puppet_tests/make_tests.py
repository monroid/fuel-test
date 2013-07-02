#!/usr/bin/env python
"""
MakeTests is a script to create tests scripts for every Puppet module using jinja2 templates.
"""

import jinja2
import os

from helpers.interface import Interface
from puppet_module import PuppetModule


class MakeTests:
    """
    This is main class. It finds all modules in the given directory and creates tests for them.
    You should give constructor following arguments:

        - *local_modules_path* Path to puppet modules which will be scanned for test files
        - *tests_directory_path* Output directory where files will be written
        - *modules_path* (Optional) Use this path to modules on test host system instead of local_modules_path.
          Useful when path to puppet modules differ on machine where tests are made and where they are executed.
    """

    def __init__(self, tests_directory_path, local_modules_path, modules_path=None, debug_level=0):
        """
        Constructor
        """
        self.interface = Interface(debug_level=debug_level)
        self.interface.debug('Starting MakeTests', 1)

        if not os.path.isdir(local_modules_path):
            self.interface.error('No such dir: ' + local_modules_path, 1)

        if not os.path.isdir(tests_directory_path):
            self.interface.error('No such dir: ' + tests_directory_path, 1)

        self.__local_modules_path = local_modules_path
        self.__modules_path = local_modules_path
        if modules_path:
            self.__modules_path = modules_path
        self.__tests_directory_path = tests_directory_path

        self.__default_template_file = 'puppet_module_test.py'
        self.__test_file_name_prefix = 'TestPuppetModule'

        self.__modules = []
        self.__module_templates = {}
        self.__make_tests_dir = os.path.dirname(os.path.abspath(__file__))

        self.set_templates_dir('puppet_tests/templates')
        self.set_internal_modules_path('/etc/puppet/modules')
        self.set_internal_manifests_path('/etc/puppet/manifests')

        self.find_modules()

    def set_templates_dir(self, template_dir):
        """
        Set directory to take templates from
        """
        if not os.path.isdir(template_dir):
            self.interface.error("No such dir: " + template_dir, 1)
        self.__template_directory_path = template_dir
        self.__template_loader = jinja2.FileSystemLoader(searchpath=template_dir)
        self.__template_environment = templateEnv = jinja2.Environment(
            loader=self.__template_loader,
        )

    def set_module_template_overrides(self, module_templates_dictionary):
        """
        Set module template file override dictionary
        """
        if type(module_templates_dictionary) is dict:
            self.__module_templates = module_templates_dictionary
        else:
            self.interface.error("Argument is not Dictionary", 1)

    def set_default_template_file(self, template_file):
        """
        Set default script template file
        """
        self.__default_template_file = template_file

    def set_internal_modules_path(self, internal_modules_path):
        """
        Set path to modules inside virtual machine
        """
        self.__internal_modules_path = internal_modules_path

    def set_internal_manifests_path(self, internal_manifests_path):
        """
        Set path to manifests directory inside virtual machine
        """
        self.__internal_manifests_path = internal_manifests_path

    def get_modules_list(self):
        """
        Get list of PuppetModule objects
        """
        return self.__modules

    def find_modules(self):
        """
        Find all Puppet modules in module_library_path
        and create array of PuppetModule objects
        """
        self.interface.debug('Starting findModules in "%s"' % self.__local_modules_path, 2)
        for module_dir in os.listdir(self.__local_modules_path):
            full_local_module_path = os.path.join(self.__local_modules_path, module_dir)
            full_local_tests_path = os.path.join(full_local_module_path, 'tests')
            if not os.path.isdir(full_local_tests_path):
                continue
            self.interface.debug('Found Puppet module: "%s"' % full_local_module_path, 3)
            puppet_module = PuppetModule(full_local_module_path, self.interface)
            self.__modules.append(puppet_module)

    def compile_script(self, module):
        """
        Compile script template for given module and return it
        """
        template_file = self.__module_templates.get(module.get_name(), self.__default_template_file)
        template = self.__template_environment.get_template(template_file)
        general = {
            'modules_path': self.__modules_path,
            'local_modules_path': self.__local_modules_path,
            'internal_modules_path': self.__internal_modules_path,
            'internal_manifests_path': self.__internal_manifests_path,
            'tests_directory_path': self.__tests_directory_path,
        }
        compiled_template = template.render(module = module, **general)
        return compiled_template

    def save_script(self, module):
        """
        Saves compiled script to a file
        """
        file_name = self.__test_file_name_prefix + module.get_name().title() + '.py'
        full_file_path = os.path.join(self.__tests_directory_path, file_name)
        script_content = self.compile_script(module)
        script_file = open(full_file_path, 'w+')
        script_file.write(script_content)
        script_file.close()

    def make_all_scripts(self):
        """
        Compile and save to tests_directory_path all the test scripts. Main procedure.
        """
        self.interface.debug('Starting makeAllScripts', 2)
        for module in self.get_modules_list():
            self.interface.debug('Processing module: "%s"' % module.get_name(), 3)
            self.save_script(module)

    def remove_all_tests(self):
        """
        Remove all tests from tests_directory_path
        """
        self.interface.debug('Starting removeAllTests in "%s"' % self.__tests_directory_path, 2)
        file_list = os.listdir(self.__tests_directory_path)
        for test_file in file_list:
            if not test_file.endswith('.py'):
                continue
            if not test_file.startswith('TestPuppetModule'):
                continue
            full_file_path = os.path.join(self.__tests_directory_path, test_file)
            self.interface.debug('Removing test file: "%s"' % full_file_path, 3)
            os.remove(full_file_path)
