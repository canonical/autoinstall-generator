
import subprocess
import tempfile
import pytest

cmd = './autoinstall_generator/bin/autoinstall_generator'
# FIXME redundant file paths with reader
data = 'autoinstall_generator/tests/data'
preseed_path = f'{data}/preseed.txt'
autoinstall_path = f'{data}/preseed2autoinstall.yaml'

simple_path = f'{data}/simple.txt'


def run(args, **kwargs):
    return subprocess.run(args, capture_output=True, text=True, **kwargs)


def file_contents(path):
    with open(path, 'r') as f:
        return f.read()


def file_lines(path):
    with open(path, 'r') as f:
        return [line.strip('\n') for line in f.readlines()]


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


@pytest.mark.skip('debug overhaul')
def test_convert_debug():
    out = tempfile.NamedTemporaryFile()
    process = run([cmd, preseed_path, out.name, '--debug'])
    assert 0 == process.returncode
    preseed_lines = file_lines(preseed_path)
    commented_input = ''.join([f'# {line}\n' for line in preseed_lines])
    expected = file_contents(autoinstall_path) + commented_input
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
    expected = 'usage: autoinstall_generator'
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


@pytest.mark.skip('debug overhaul')
def test_simple_debug():
    process = run([cmd, simple_path, '--debug'])
    assert 0 == process.returncode
    expected = '''\
locale: en_US
version: 1
# d-i debian-installer/locale string en_US
'''
    assert expected == str(process.stdout)
