#!/usr/bin/env python
import os
import sys
import re

path = os.path.abspath(__file__)
path = os.path.dirname(path)
path = os.path.dirname(path)
sys.path.insert(0, path)

from puppet_test import PuppetTest


class PuppetModule:
    """
    This class represents Puppet module
    """

    def __init__(self, local_module_path, interface):
        """
        You should give this constructor the full path to the module and interface object.
        """
        self.__local_module_path = local_module_path
        self.interface = interface
        self.__module_name = os.path.basename(self.__local_module_path)

        self.__tests = []
        self.__dependencies = []

        self.find_tests()

        self.__comment_regexp = re.compile(r'^\s*#')
        self.__dependency_regexp = re.compile(r'^\s*dependency\s*[\'\"]*([^\'\"]+)[\'\"]*')

    def find_dependencies(self):
        """
        Get dependencies of this module from Modulefile if present
        """
        module_file = 'Modulefile'
        dependencies = []
        module_file_path = os.path.join(self.__local_module_path, module_file)
        if not os.path.isfile(module_file_path):
            self.__dependencies = dependencies
            return False
        opened_file = open(module_file_path, 'r')
        for line in opened_file.readlines():
            if re.match(self.__comment_regexp, line):
                # skip commented line
                continue
            match = re.match(self.__dependency_regexp, line)
            if match:
                # found dependency line
                dependency_name = match.group(1).split('/')[-1]
                dependencies.append(dependency_name)
        self.__dependencies = dependencies
        return True

    def find_tests(self):
        """
        Find all tests in this module and fill tests array with PuppetTest objects.
        """
        current_path = os.path.abspath(os.curdir)
        try:
            # try to change directory to test's folder
            os.chdir(self.__local_module_path)
        except OSError as error:
            self.interface.error("Cannot change directory to %s: %s" % (self.__local_module_path, error.message))
        else:
            # if change was successful start looking for tests
            for root, dirs, files in os.walk('tests'):
                for test_file in files:
                    if not test_file[-3:] == '.pp':
                        continue
                    test_file_path = os.path.join(root, test_file)
                    puppet_test = PuppetTest(test_file_path)
                    self.__tests.append(puppet_test)
        finally:
            # try to restore original folder on exit
            try:
                os.chdir(current_path)
            except OSError as error:
                self.interface.error("Cannot change directory to %s: %s" % (self.__local_module_path, error.message), 1)

    def get_tests(self):
        """
        Return array of PuppetTest objects found in this module
        """
        return self.__tests

    def get_name(self):
        """
        Return module's name
        """
        return self.__module_name

    def get_path(self):
        """
        Return full path to this module
        """
        return self.__local_module_path

    def get_dependencies(self):
        """
        Return list of module dependencies
        """
        return self.__dependencies

    @property
    def tests(self):
        """
        Property returns list of tests
        """
        return self.get_tests()

    @property
    def name(self):
        """
        Property returns module name
        """
        return self.get_name()

    @property
    def path(self):
        """
        Property returns path to this module
        """
        return self.get_path()

    @property
    def dependencies(self):
        """
        Property returns list of module dependencies
        """
        return self.get_dependencies()

    def __repr__(self):
        """
        String representation of PuppetModule
        """
        tests_string = ''
        if len(self.tests) > 0:
            tests = [repr(test) for test in self.tests]
            tests_string += ", ".join(tests)
        tpl = "PuppetModule(name=%s, path=%s, tests=[%s]" % (self.get_name(), self.get_path(), tests_string)

        return tpl
