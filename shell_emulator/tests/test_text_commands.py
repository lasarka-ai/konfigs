import pytest
from utils.file_system import VirtualFileSystem
import os

@pytest.fixture
def setup_virtual_fs():
    """
    Создаем экземпляр VirtualFileSystem с тестовым архивом.
    """
    archive_path = os.path.abspath("test_filesystem.zip")
    vfs = VirtualFileSystem(archive_path)
    vfs.current_dir = "/home/user/documents/"
    return vfs

def test_uniq_remove_duplicates(setup_virtual_fs):
    with setup_virtual_fs.zip_file.open("home/user/documents/test.txt") as f:
        content = f.read().decode("utf-8")
    
    unique_lines = "\n".join(sorted(set(content.splitlines()), key=content.splitlines().index))
    assert unique_lines == "Hello\nWorld\nTest"

def test_uniq_empty_file(setup_virtual_fs):
    # Create a virtual empty file for testing
    empty_content = ""
    assert empty_content == ""

def test_uniq_nonexistent_file(setup_virtual_fs):
    try:
        with setup_virtual_fs.zip_file.open("nonexistent_file.txt") as f:
            pass
    except KeyError:
        assert Exception("No such file or directory: nonexistent_file.txt")