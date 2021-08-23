#!/bin/bash

set -e

make readme
diff -u README.md README.md.tmp

make build
[ -f build/lib/autoinstall_generator/autoinstall-schema.json ]

for cfg in test/* ; do
    PYTHONPATH=$(realpath .) \
        autoinstall_generator/cmd/autoinstall-generator.py $cfg -cd
done
