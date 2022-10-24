from importlib.machinery import ModuleSpec


def test_all_commands(test_plugin):
    assert test_plugin.all_commands() == ["foo"]


def test_get_command(test_plugin):
    result = test_plugin.get_command("foo")

    assert isinstance(result, ModuleSpec)
    assert result.name == "foo"


def test_command_map(test_plugin):
    result = test_plugin.command_map()

    assert len(result.keys()) == 1
    assert result["foo"] == "mock"
