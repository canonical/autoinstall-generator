

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


def run(args, **kwargs):
    return subprocess.run(args, capture_output=True, text=True, **kwargs)


def file_contents(path):
    with open(path, 'r') as f:
        return f.read()


def test_invoke():
    ec = os.system(cmd)
    assert os.WIFEXITED(ec)
    assert 2 == os.WEXITSTATUS(ec)


def test_convert():
    out = tempfile.NamedTemporaryFile()
    assert 0 == os.system(f'{cmd} {preseed_path} {out.name}')
    expected = file_contents(autoinstall_path)
    actual = file_contents(out.name)
    assert expected == actual


def test_stdout():
    process = run([cmd, preseed_path])
    assert 0 == process.returncode
    expected = file_contents(autoinstall_path)
    assert expected == str(process.stdout)


def test_pipe():
    process = run([cmd, '-'], input=file_contents(preseed_path))
    assert 0 == process.returncode
    expected = file_contents(autoinstall_path)
    assert expected == str(process.stdout)


def test_help():
    assert 0 == os.system(f'{cmd} --help')
