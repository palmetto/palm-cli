from palm.utils import *


def test_is_cmd_file():
    assert is_cmd_file('foo') is False
    assert is_cmd_file('cmd_foo.py') is True
    assert is_cmd_file('cmd_foo_bar.py') is True


def test_cmd_name_from_file():
    assert cmd_name_from_file('cmd_foo.py') == 'foo'
    assert cmd_name_from_file('cmd_foo_bar.py') == 'foo_bar'


def test_run_on_host_happy_path():
    cmd = "echo 'hello world!'"
    success, out, err = run_on_host(cmd)
    assert success == 0
    assert out == "hello world!\n"
    assert err == ''

def test_run_on_host_capture_output():
    cmd = "echo 'hello world!'"
    success, out, err = run_on_host(cmd, capture_output=True)
    assert success == 0
    assert out == None
    assert err == None