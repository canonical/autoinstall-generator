
import subprocess
from subprocess import PIPE
import tempfile

cmd = './autoinstall_generator/cmd/autoinstall-generator.py'
# FIXME redundant file paths with reader
data = 'autoinstall_generator/tests/data'
preseed_path = f'{data}/preseed.txt'
autoinstall_path = f'{data}/preseed2autoinstall.yaml'
autoinstall_debug_path = f'{data}/preseed2autoinstall_debug.yaml'

simple_path = f'{data}/simple.txt'


def run(args, **kwargs):
    return subprocess.run(args, universal_newlines=True,
                          stdout=PIPE, stderr=PIPE, **kwargs)


def file_contents(path):
    with open(path, 'r') as f:
        return f.read()


def test_invoke():
    process = run([cmd])
    assert 2 == process.returncode


def test_convert():
    out = tempfile.NamedTemporaryFile()
    process = run([cmd, preseed_path, out.name])
    assert 0 == process.returncode
    expected = file_contents(autoinstall_path)
    actual = file_contents(out.name)
    assert expected == actual


def test_convert_debug():
    out = tempfile.NamedTemporaryFile()
    process = run([cmd, preseed_path, out.name, '--debug'])
    assert 0 == process.returncode
    expected = file_contents(autoinstall_debug_path)
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
    process = run([cmd, '--help'])
    actual = process.stdout.split('\n')[0]
    expected = 'usage: autoinstall-generator'
    assert actual.startswith(expected)
    assert 0 == process.returncode


def test_bad_infile():
    process = run([cmd, '/does/not/exist'])
    found_exception = False
    for line in process.stderr.split('\n'):
        if line.startswith('FileNotFound'):
            found_exception = True
            break

    assert found_exception
    assert 0 != process.returncode


def test_simple_debug():
    process = run([cmd, simple_path, '--debug'])
    assert 0 == process.returncode
    expected = '''\
locale: en_US
version: 1
# 1:   Directive: d-i debian-installer/locale string en_US
#      Mapped to: locale: en_US
'''
    assert expected == str(process.stdout)


def test_simple_cloud_config():
    for arg in ['-c', '--cloud']:
        process = run([cmd, simple_path, arg])
        assert 0 == process.returncode
        expected = '''\
#cloud-config
autoinstall:
  locale: en_US
  version: 1
'''
        assert expected == str(process.stdout)
