#!/bin/sh
file="${0}"
dir=`dirname ${file}`
cd "${dir}" || exit 1
python make_tests.py -d3 -m "/tmp/puppet" "tests" "test_data"
