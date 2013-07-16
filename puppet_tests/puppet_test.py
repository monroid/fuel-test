#!/usr/bin/env python
import os
from glob import glob
import stat


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
        self.find_verify_file()
        
    def find_verify_file(self):
        """
        Get verify script for this test if there is one.
        """
        pattern = os.path.join(self.__tests_path, self.__test_name) + '*'
        verify_files = glob(pattern)
        verify_files = [ os.path.basename(verify_file) for verify_file in verify_files if not verify_file.endswith('.pp') ]
        if verify_files:
            self.__verify_file = verify_files[0]
            self.make_verify_executable()
        else:
            self.__verify_file = None

    def make_verify_executable(self):
        """
        Set file's executable bit
        """
        file_path = os.path.join(self.__tests_path, self.__verify_file)
        if not os.path.isfile(file_path):
            return False
        file_stat = os.stat(file_path)
        result_code = os.chmod(file_path, file_stat.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH )
        return True

    def get_path(self):
        """
        Return path to directory of this test
        """
        return self.__tests_path

    def get_file(self):
        """
        Return file name of this test
        """
        return self.__test_file_name

    def get_name(self):
        """
        Return name of this test
        """
        return self.__test_name

    def get_verify_file(self):
        """
        Return verify file name
        """
        return self.__verify_file

    @property
    def path(self):
        """
        Property returns path to this test relative to module and excluding file name
        """
        return self.get_path()

    @property
    def file(self):
        """
        Property returns this tests' file name
        """
        return self.get_file()

    @property
    def name(self):
        """
        Property returns name of this test
        """
        return self.get_name()

    @property
    def verify_file(self):
        """
        Property returns verify file name
        """
        return self.get_verify_file()

    def __repr__(self):
        """
        String representation of PuppetTest
        """
        return "PuppetTest(name=%s, path=%s, file=%s)" % (self.get_name(), self.get_path(), self.get_file())
