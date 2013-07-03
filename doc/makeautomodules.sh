#!/bin/sh
if [ "${1}" = "" ]; then
  echo "Give path argument!"
  exit 1
fi
find "${1}" -type f -a -name '*.py' | sed -e '/__init__/d' -e 's:/:.:g' -e 's/.py//g' -e 's/^/.. automodule:: /g'
