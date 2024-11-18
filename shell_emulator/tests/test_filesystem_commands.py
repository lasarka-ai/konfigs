import pytest
from utils.file_system import VirtualFileSystem
from commands.filesystem_commands import LSCommand
import zipfile
import os

@pytest.fixture
def setup_filesystem():
    # Создание временного архива
    archive_content = {
        "dir1/": None,
        "dir1/file1.txt": b"content",
        "file1.txt": b"line1\nline2\nline3",
    }
    archive_path = "test_archive.zip"
    with zipfile.ZipFile(archive_path, "w") as archive:
        for name, content in archive_content.items():
            if content is None:
                archive.writestr(name, "")
            else:
                archive.writestr(name, content)

    fs = VirtualFileSystem(archive_path)
    yield fs

    # Удаление архива
    os.remove(archive_path)


def test_ls_command(setup_filesystem):
    fs = setup_filesystem
    ls = LSCommand(fs, None)

    # Проверяем содержимое корня
    result = ls.execute([])
    assert "dir1" in result
    assert "file1.txt" in result
