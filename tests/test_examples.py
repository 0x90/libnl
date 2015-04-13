"""Tests for all examples."""

import os
import subprocess
import sys

import pytest


def check_output(cmd):
    """Python 2.6 subprocess.check_output stand-in."""
    if hasattr(subprocess, 'check_output'):
        return subprocess.check_output(cmd)
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    stdout = proc.communicate()[0]
    code = proc.returncode
    if code:
        raise subprocess.CalledProcessError(code, cmd)
    return stdout


def test_list_network_interfaces(ifacesi):
    """Test list_network_interfaces.py."""
    path = os.path.join(os.path.dirname(__file__), '../examples/python', 'list_network_interfaces.py')
    stdout = check_output([sys.executable, path, 'print'])
    if hasattr(stdout, 'decode'):
        stdout = stdout.decode('ascii')
    stdout_split = stdout.splitlines()
    assert 'Sent 20 bytes to the kernel.' == stdout_split.pop(0)
    for index, name in ifacesi:
        assert 'Found network interface {0}: {1}'.format(index, name) == stdout_split.pop(0)
    assert not stdout_split


@pytest.mark.skipif('not os.path.exists("/sys/class/net/wlan0")')
def test_show_wifi_interface_all():
    """Test show_wifi_interface.py showing all interfaces."""
    path = os.path.join(os.path.dirname(__file__), '..', 'show_wifi_interface.py')
    stdout = check_output([sys.executable, path, 'print'])
    if hasattr(stdout, 'decode'):
        stdout = stdout.decode('ascii')
    assert 'NL80211_ATTR_MAC' in stdout


@pytest.mark.skipif('not os.path.exists("/sys/class/net/wlan0")')
def test_show_wifi_interface_wlan0():
    """Test show_wifi_interface.py showing just wlan0."""
    path = os.path.join(os.path.dirname(__file__), '../examples/python', 'show_wifi_interface.py')
    stdout = check_output([sys.executable, path, 'print', 'wlan0'])
    if hasattr(stdout, 'decode'):
        stdout = stdout.decode('ascii')
    assert 'NL80211_ATTR_MAC' in stdout


@pytest.mark.skipif('not os.path.exists("/sys/class/net/wlan0")')
def test_scan_access_points_no_sudo():
    """Test scan_access_points.py without root privileges."""
    path = os.path.join(os.path.dirname(__file__), '../examples/python', 'scan_access_points.py')
    stdout = check_output([sys.executable, path, '-n', 'wlan0'])
    if hasattr(stdout, 'decode'):
        stdout = stdout.decode('ascii')
    assert 'results of previous scan' in stdout


@pytest.mark.skipif('not os.path.exists("/sys/class/net/wlan0") or os.getuid() != 0')
def test_scan_access_points():
    """Test scan_access_points.py with root privileges."""
    path = os.path.join(os.path.dirname(__file__), '../examples/python', 'scan_access_points.py')
    stdout = check_output([sys.executable, path, 'wlan0'])
    if hasattr(stdout, 'decode'):
        stdout = stdout.decode('ascii')
    assert 'Scanning for access points' in stdout
