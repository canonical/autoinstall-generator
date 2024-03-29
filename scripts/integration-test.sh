#!/bin/bash

set -e

make readme
diff -u README.md README.md.tmp

make build
[ -f build/lib/autoinstall_generator/autoinstall-schema.json ]

invoke() {
    PYTHONPATH=$(realpath .) \
        autoinstall_generator/cmd/autoinstall-generator.py "$@"
}

for cfg in test/* ; do
    invoke -cd $cfg
    invoke -cd - < $cfg
done
