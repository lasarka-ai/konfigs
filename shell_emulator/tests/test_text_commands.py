import pytest
from commands.text_commands import UniqCommand
from utils.logger import Logger
import tempfile

class TestUniqCommand:
    @pytest.fixture
    def setup(self):
        logger = Logger('test.log')
        return UniqCommand(logger)
    
    def test_uniq_basic(self, setup):
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write('line1\nline1\nline2\nline3\nline3\n')
        
        result = setup.execute([f.name])
        assert result == 'line1\nline2\nline3'
    
    def test_uniq_all_unique(self, setup):
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write('line1\nline2\nline3\n')
        
        result = setup.execute([f.name])
        assert result == 'line1\nline2\nline3'
    
    def test_uniq_all_same(self, setup):
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write('line1\nline1\nline1\n')
        
        result = setup.execute([f.name])
        assert result == 'line1'