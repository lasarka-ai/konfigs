import pytest
from utils.file_system import VirtualFileSystem
from zipfile import ZipFile


@pytest.fixture
def setup_virtual_fs(tmp_path):
    """
    Создаёт экземпляр VirtualFileSystem с тестовым архивом.
    """
    # Создаём временный zip-архив для тестов
    archive_path = tmp_path / "test_archive.zip"

    # Инициализация содержимого архива
    with ZipFile(archive_path, "w") as archive:
        archive.writestr("documents/test.txt", "Hello\nWorld\nTest")
        archive.writestr("downloads/", "")

    # Диагностика содержимого архива
    with ZipFile(archive_path, "r") as archive:
        print("Archive contents:", archive.namelist())

    vfs = VirtualFileSystem(str(archive_path))
    vfs.current_dir = "/"  # Устанавливаем текущую директорию на корень
    return vfs


def test_ls_root_directory(setup_virtual_fs):
    """
    Тест команды `list_directory` для корневого каталога.
    """
    vfs = setup_virtual_fs
    result = vfs.list_directory("/")
    assert result == ["documents", "downloads"], f"Unexpected root contents: {result}"


def test_ls_subdirectory(setup_virtual_fs):
    """
    Тест команды `list_directory` для существующего подкаталога.
    """
    vfs = setup_virtual_fs
    vfs.change_directory("/documents")
    result = vfs.list_directory()
    assert result == ["test.txt"], f"Unexpected documents contents: {result}"


def test_ls_nonexistent_directory(setup_virtual_fs):
    """
    Тест команды `change_directory` для несуществующего каталога.
    """
    vfs = setup_virtual_fs
    with pytest.raises(Exception, match="No such directory"):
        vfs.change_directory("/nonexistent_dir")
