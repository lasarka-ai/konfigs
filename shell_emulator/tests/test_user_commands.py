import pytest
from commands.user_commands import WhoCommand
import getpass

class MockLogger:
    def __init__(self):
        self.logs = []

    def log_command(self, command):
        self.logs.append(command)

    def read_logs(self):
        return "\n".join(self.logs)


@pytest.fixture
def setup_user():
    logger = MockLogger()
    return logger


def test_who_command(setup_user, mocker):
    logger = setup_user
    mocker.patch("getpass.getuser", return_value="test_user")
    who = WhoCommand(logger)

    result = who.execute([])
    assert "test_user" in result
    assert "console" in result


def test_who_command_logging(setup_user, mocker):
    logger = setup_user
    mocker.patch("getpass.getuser", return_value="test_user")
    who = WhoCommand(logger)

    who.execute([])
    assert "who" in logger.read_logs()
