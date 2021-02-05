
import yaml


password = '$6$wdAcoXrU039hKYPd$508Qvbe7ObUnxoj15DRCkzC3qO7edjH0VV7BPNRD'\
            'YK4QR8ofJaEEF2heacn0QgD.f8pO8SNp83XNdWG6tocBM1'
identity = {
    'identity': {
        'hostname': 'ubuntu',
        'password': password,
        'realname': '',
        'username': 'ubuntu',
    }
}


def test_roundtrip():
    expected_text = '''\
a: 1
b:
  c: 3
  d: 4
'''

    actual_yaml = yaml.safe_load(expected_text)
    expected_yaml = {'a': 1, 'b': {'c': 3, 'd': 4}}
    assert expected_yaml == actual_yaml

    actual_text = yaml.dump(actual_yaml, default_flow_style=False)
    assert expected_text == actual_text


def test_ai_identity_fullquote():
    expected_text = f'''\
'identity':
  'hostname': 'ubuntu'
  'password': '{password}'
  'realname': ''
  'username': 'ubuntu'
'''
    actual_text = yaml.dump(identity, default_flow_style=False,
                            default_style="'")
    assert expected_text == actual_text


def test_ai_identity():
    expected_text = f'''\
identity:
  hostname: ubuntu
  password: {password}
  realname: ''
  username: ubuntu
'''
    actual_text = yaml.dump(identity, default_flow_style=False)
    assert expected_text == actual_text


def test_to_file(tmpdir):
    dest = tmpdir.join('out.yaml')

    with open(dest.strpath, 'w') as out:
        yaml.dump(identity, out, default_flow_style=False)

    expected_yaml_path = 'preseed_to_autoinstall/tests/data/identity.yaml'

    with open(expected_yaml_path, 'r') as expected_yaml_file:
        expected_yaml = expected_yaml_file.read()
        assert expected_yaml == dest.read()
