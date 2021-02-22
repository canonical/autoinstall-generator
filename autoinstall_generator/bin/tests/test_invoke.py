
import subprocess
import tempfile

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
    process = run([cmd])
    assert 2 == process.returncode


def test_convert():
    out = tempfile.NamedTemporaryFile()
    process = run([cmd, preseed_path, out.name])
    assert 0 == process.returncode
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
    process = run([cmd, '--help'])
    assert 0 == process.returncode
