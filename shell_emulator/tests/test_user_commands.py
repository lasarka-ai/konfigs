import pytest
from commands.user_commands import WhoCommand, WhoamiCommand
from utils.logger import Logger

class TestWhoCommand:
    @pytest.fixture
    def setup(self):
        logger = Logger('test.log')
        return WhoCommand(logger)
    
    def test_who_output_format(self, setup):
        result = setup.execute([])
        assert len(result.split()) >= 3  # username, console, timestamp
    
    def test_who_username(self, setup):
        result = setup.execute([])
        assert result.split()[0] == os.getlogin()
    
    def test_who_console(self, setup):
        result = setup.execute([])
        assert 'console' in result

class TestWhoamiCommand:
    @pytest.fixture
    def setup(self):
        logger = Logger('test.log')
        return WhoamiCommand(logger)
    
    def test_whoami_output(self, setup):
        result = setup.execute([])
        assert result == os.getlogin()
    
    def test_whoami_no_args(self, setup):
        result = setup.execute([])
        assert len(result.split()) == 1
    
    def test_whoami_ignore_args(self, setup):
        result = setup.execute(['arg1', 'arg2'])
        assert result == os.getlogin()