#!/usr/bin/env python
"""
Script for creating Puppet integration tests scripts using template engine.
"""

import argparse
from puppet_tests.make_tests import MakeTests

parser = argparse.ArgumentParser()
parser.add_argument("tests", type=str, help="Directory to save tests")
parser.add_argument("modules", type=str, help="Path to Puppet modules")
parser.add_argument("-m", "--modules_path", type=str, help="Path to Puppet modules on the test server", default=None)
parser.add_argument("-t", "--templates_path", type=str, help="Path to the test script templates directory", default=None)
parser.add_argument("-f", "--template_file", type=str, help="Default template file name", default=None)
parser.add_argument("-k", "--keep_tests", action='store_true', help="Keep previous test files", default=False)
parser.add_argument("-d", "--debug", type=int, choices=[0, 1, 2, 3], help="Set debug level (0-3)", default=0)

args = parser.parse_args()
MT = MakeTests(args.tests, args.modules, args.modules_path, args.debug)
if args.templates_path is not None:
    MT.set_templates_dir(args.templates_path)
if args.template_file is not None:
    MT.set_default_template_file(args.template_file)
if not args.keep_tests:
    MT.remove_all_tests()

MT.make_all_scripts()
