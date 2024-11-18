import pytest
from unittest.mock import patch
import getpass

class MockLogger:
    def __init__(self):
        self.logs = []

    def log(self, message):
        self.logs.append(message)

    def read_logs(self):
        return "\n".join(self.logs)

class WhoCommand:
    def __init__(self, logger):
        self.logger = logger

    def execute(self, args):
        self.logger.log("who")
        return getpass.getuser()
    
@pytest.fixture
def setup_user():
    return MockLogger()

@patch("getpass.getuser", return_value="test_user")
def test_who_command_return_value(mock_getuser, setup_user):
    logger = setup_user
    who = WhoCommand(logger)
    result = who.execute([])
    assert result == "test_user"

@patch("getpass.getuser", return_value="test_user")
def test_who_command_logs_command(mock_getuser, setup_user):
    logger = setup_user
    who = WhoCommand(logger)
    who.execute([])
    assert "who" in logger.read_logs()

@patch("getpass.getuser", return_value="test_user")
def test_who_command_logging_multiple_calls(mock_getuser, setup_user):
    logger = setup_user
    who = WhoCommand(logger)
    who.execute([])
    who.execute([])
    logs = logger.read_logs()
    assert logs.count("who") == 2