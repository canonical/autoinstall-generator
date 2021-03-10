#!/bin/bash

set -e

make readme
diff -u README.md README.md.tmp

make build
[ -f build/lib/autoinstall_generator/autoinstall-schema.json ]
