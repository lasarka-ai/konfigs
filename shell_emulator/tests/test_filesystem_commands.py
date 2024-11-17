import pytest
from commands.filesystem_commands import LSCommand, CDCommand
from utils.file_system import VirtualFileSystem
from utils.logger import Logger
import os
import zipfile

class TestLSCommand:
    @pytest.fixture
    def setup(self):
        # Create test zip file
        with zipfile.ZipFile('test_fs.zip', 'w') as zf:
            zf.writestr('dir1/', '')
            zf.writestr('dir1/file1.txt', 'content1')
            zf.writestr('dir1/file2.txt', 'content2')
        
        fs = VirtualFileSystem('test_fs.zip')
        logger = Logger('test.log')
        return LSCommand(fs, logger)
    
    def test_ls_root(self, setup):
        result = setup.execute([])
        assert 'dir1' in result
    
    def test_ls_directory(self, setup):
        result = setup.execute(['dir1'])
        assert 'file1.txt' in result
        assert 'file2.txt' in result
    
    def test_ls_nonexistent(self, setup):
        result = setup.execute(['nonexistent'])
        assert 'No such directory' in result

class TestCDCommand:
    @pytest.fixture
    def setup(self):
        with zipfile.ZipFile('test_fs.zip', 'w') as zf:
            zf.writestr('dir1/', '')
            zf.writestr('dir1/subdir/', '')
        
        fs = VirtualFileSystem('test_fs.zip')
        logger = Logger('test.log')
        return CDCommand(fs, logger)
    
    def test_cd_valid(self, setup):
        result = setup.execute(['dir1'])
        assert result == ''
    
    def test_cd_subdir(self, setup):
        setup.execute(['dir1'])
        result = setup.execute(['subdir'])
        assert result == ''
    
    def test_cd_nonexistent(self, setup):
        result = setup.execute(['nonexistent'])
        assert 'No such directory' in result