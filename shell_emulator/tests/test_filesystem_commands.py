import pytest
from utils.file_system import VirtualFileSystem
import os

@pytest.fixture
def setup_virtual_fs():
    """
    Создаёт экземпляр VirtualFileSystem на основе архива test_filesystem.zip.
    """
    archive_path = os.path.abspath("test_filesystem.zip")

    if not os.path.isfile(archive_path):
        raise FileNotFoundError(f"Test archive {archive_path} not found. Run create_test_filesystem to generate it.")

    vfs = VirtualFileSystem(archive_path)
    vfs.current_dir = "/"
    return vfs


def test_ls_root_directory(setup_virtual_fs):
    """
    Тест команды `list_directory` для корневого каталога.
    """
    vfs = setup_virtual_fs
    result = vfs.list_directory("home/user/")
    expected = ["downloads", "documents"]
    assert sorted(result) == sorted(expected), f"Unexpected root contents: {result}"


def test_ls_home_directory(setup_virtual_fs):
    """
    Тест команды `list_directory` для директории `/home`.
    """
    vfs = setup_virtual_fs
    vfs.change_directory("/home/user/downloads")
    result = vfs.list_directory()
    expected = []
    assert sorted(result) == sorted(expected), f"Unexpected home contents: {result}"


def test_ls_documents_directory(setup_virtual_fs):
    """
    Тест команды `list_directory` для директории `/home/user/documents`.
    """
    vfs = setup_virtual_fs
    vfs.change_directory("/home/user/documents/")
    result = vfs.list_directory()
    expected = ["test.txt"]
    assert sorted(result) == sorted(expected), f"Unexpected documents contents: {result}"


def test_ls_nonexistent_directory(setup_virtual_fs):
    """
    Тест команды `change_directory` для несуществующего каталога.
    """
    vfs = setup_virtual_fs
    with pytest.raises(Exception, match="No such directory"):
        vfs.change_directory("/nonexistent_dir")


def test_read_test_file(setup_virtual_fs):
    """
    Тест чтения содержимого файла в директории `/home/user/documents`.
    """
    vfs = setup_virtual_fs
    vfs.change_directory("/home/user/documents/")
    result = vfs.list_directory()
    if "test.txt" in result:
        with vfs.zip_file.open("home/user/documents/test.txt") as f:
            content = f.read().decode("utf-8")
            expected_content = "Hello\nHello\nWorld\nWorld\nTest\n"
            assert content == expected_content, "Test file content does not match expected."