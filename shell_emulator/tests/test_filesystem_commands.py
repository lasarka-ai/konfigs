import pytest
import os
from utils.file_system import VirtualFileSystem

@pytest.fixture
def setup_filesystem(tmp_path):
    # Создаём временную файловую структуру
    root = tmp_path / "test_fs"
    root.mkdir()
    (root / "dir1").mkdir()
    (root / "dir1" / "file1.txt").write_text("content")
    (root / "file2.txt").write_text("example")
    return VirtualFileSystem(str(root))

def test_ls_root_directory(setup_filesystem):
    fs = setup_filesystem
    result = fs.list_directory("/")
    assert "dir1" in result
    assert "file2.txt" in result

def test_ls_subdirectory(setup_filesystem):
    fs = setup_filesystem
    result = fs.list_directory("dir1")
    assert "file1.txt" in result

def test_ls_nonexistent_directory(setup_filesystem):
    fs = setup_filesystem
    result = fs.list_directory("nonexistent")
    assert "Error: Directory 'nonexistent' does not exist" in result
