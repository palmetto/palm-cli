from palm.utils import *


def test_is_cmd_file():
    assert is_cmd_file('foo') is False
    assert is_cmd_file('cmd_foo.py') is True
    assert is_cmd_file('cmd_foo_bar.py') is True


def test_cmd_name_from_file():
    assert cmd_name_from_file('cmd_foo.py') == 'foo'
    assert cmd_name_from_file('cmd_foo_bar.py') == 'foo_bar'
