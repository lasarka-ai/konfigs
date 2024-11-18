import pytest
from utils.file_system import VirtualFileSystem
from commands.text_commands import UniqCommand
import zipfile
import os

@pytest.fixture
def setup_text():
    # Создание временного архива
    archive_content = {
        "file1.txt": b"line1\nline2\nline2\nline3\n",
        "empty.txt": b"",
    }
    archive_path = "test_archive.zip"
    with zipfile.ZipFile(archive_path, "w") as archive:
        for name, content in archive_content.items():
            archive.writestr(name, content)

    fs = VirtualFileSystem(archive_path)
    yield fs

    # Удаление архива
    os.remove(archive_path)


@pytest.mark.parametrize("args,expected", [
    (["file1.txt"], "line1\nline2\nline3"),
    (["empty.txt"], ""),
    (["nonexistent"], "Error: No such file or directory: nonexistent")
])
def test_uniq_command(setup_text, args, expected):
    fs = setup_text
    uniq = UniqCommand(fs, None)

    result = uniq.execute(args)
    assert expected in result
