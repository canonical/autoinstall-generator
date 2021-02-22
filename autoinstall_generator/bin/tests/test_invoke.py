

import os
import subprocess
import tempfile

# import pytest
# @pytest.mark.skip('not yet')

cmd = './autoinstall_generator/bin/autoinstall_generator'
# FIXME redundant file paths with reader
data = 'autoinstall_generator/tests/data'
preseed_path = f'{data}/preseed.txt'
autoinstall_path = f'{data}/preseed2autoinstall.yaml'


def file_contents(path):
    with open(path, 'r') as f:
        return f.read()


def test_invoke():
    assert 512 == os.system(cmd)


def test_convert():
    out = tempfile.NamedTemporaryFile()
    assert 0 == os.system(f'{cmd} {preseed_path} {out.name}')
    expected = file_contents(autoinstall_path)
    actual = file_contents(out.name)
    assert expected == actual


def test_stdout():
    process = subprocess.run([cmd, preseed_path], capture_output=True,
                             text=True)
    assert 0 == process.returncode
    expected = file_contents(autoinstall_path)
    assert expected == str(process.stdout)


def test_help():
    assert 0 == os.system(f'{cmd} --help')
