
from autoinstall_generator.convert import convert, ConversionType, Directive
from autoinstall_generator.merging import convert_file
import json
import jsonschema
import pytest
import yaml


@pytest.fixture(autouse=True)
def reset_largest_lineno():
    Directive.largest_linenumber = 0


expected_lines = '''\
d-i debian-installer/locale string en_US
d-i debian-installer/language string en
d-i debian-installer/country string NL
d-i debian-installer/locale string en_GB.UTF-8'''

data = 'autoinstall_generator/tests/data'
preseed_path = f'{data}/preseed.txt'
simple_path = f'{data}/simple.txt'
autoinstall_path = f'{data}/preseed2autoinstall.yaml'


def test_reader():
    converted = []

    with open(preseed_path, 'r') as preseed_file:
        for line in preseed_file.readlines():
            directive = convert(line)
            if directive.convert_type != ConversionType.PassThru:
                converted.append(directive.orig_input.strip())

    expected = expected_lines.split('\n')
    assert expected == converted[:4]


def test_convert_file():
    with open(preseed_path, 'r') as preseed:
        actual = convert_file(preseed)
    with open(autoinstall_path, 'r') as autoinstall:
        expected = autoinstall.read()
    assert expected == actual


def test_validate():
    with open(autoinstall_path, 'r') as fp:
        ai = yaml.safe_load(fp.read())

    with open('autoinstall-schema.json', 'r') as fp:
        schema_data = fp.read()
        schema = json.loads(schema_data)

    jsonschema.validate(ai, schema)


def test_convert_simple_debug():
    with open(simple_path, 'r') as simple:
        actual = convert_file(simple, True)
    expected = '''\
locale: en_US
version: 1
# 1:   Directive: d-i debian-installer/locale string en_US
#      Mapped to: locale: en_US
'''
    assert expected == actual
