#!/usr/bin/env python
import os


class PuppetTest:
    """
    This class represents single test of the Puppet module.
    """

    def __init__(self, test_file_path):
        """
        You should give this constructor path to test file.
        """
        self.__test_file_path = test_file_path
        self.__tests_path = os.path.dirname(self.__test_file_path)
        self.__test_file_name = os.path.basename(self.__test_file_path)
        self.__test_name = self.__test_file_name.replace('.pp', '')

    def get_path(self):
        """
        Returns path to directory of this test
        """
        return self.__tests_path

    def get_file(self):
        """
        Returns file name of this test
        """
        return self.__test_file_name

    def get_name(self):
        """
        Returns name of this test
        """
        return self.__test_name

    @property
    def path(self):
        return self.get_path()

    @property
    def file(self):
        return self.get_file()

    @property
    def name(self):
        return self.get_name()

    def __repr__(self):
        """
        String representation of PuppetTest
        """
        return "PuppetTest(name=%s, path=%s, file=%s)" % (self.get_name(), self.get_path(), self.get_file())

