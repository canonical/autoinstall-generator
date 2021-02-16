
from convert import (convert, ConversionType, convert_file)
# import pytest


expected_lines = '''\
d-i debian-installer/locale string en_US
d-i keyboard-configuration/xkb-keymap select us
d-i netcfg/choose_interface select auto
d-i netcfg/get_hostname string unassigned-hostname
d-i netcfg/get_domain string unassigned-domain
d-i netcfg/wireless_wep string
d-i mirror/country string manual
d-i mirror/http/hostname string http.us.debian.org
d-i mirror/http/directory string /debian
d-i mirror/http/proxy string
d-i clock-setup/utc boolean true
d-i time/zone string US/Eastern
d-i clock-setup/ntp boolean true
d-i partman-auto/method string lvm
d-i partman-auto-lvm/guided_size string max
d-i partman-lvm/device_remove_lvm boolean true
d-i partman-md/device_remove_md boolean true
d-i partman-lvm/confirm boolean true
d-i partman-lvm/confirm_nooverwrite boolean true
d-i partman-auto/choose_recipe select atomic
d-i partman-partitioning/confirm_write_new_label boolean true
d-i partman/choose_partition select finish
d-i partman/confirm boolean true
d-i partman/confirm_nooverwrite boolean true
d-i partman-md/confirm boolean true
d-i partman-partitioning/confirm_write_new_label boolean true
d-i partman/choose_partition select finish
d-i partman/confirm boolean true
d-i partman/confirm_nooverwrite boolean true
d-i grub-installer/only_debian boolean true
d-i grub-installer/with_other_os boolean true
d-i finish-install/reboot_in_progress note'''


preseed_path = 'autoinstall-generator/tests/data/example-preseed.txt'


def test_reader():

    converted = []

    with open(preseed_path, 'r') as preseed_file:
        for line in preseed_file.readlines():
            directive = convert(line)
            if directive.convert_type != ConversionType.PassThru:
                converted.append(directive.orig_input.strip())

    expected = expected_lines.split('\n')
    assert expected == converted


def test_convert_file():
    actual = convert_file(preseed_path)
    expected = '''\
keyboard:
  layout: us
locale: en_US
'''
    assert expected == actual
