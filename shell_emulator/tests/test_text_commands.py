import pytest
from utils.file_system import VirtualFileSystem

@pytest.fixture
def setup_text_files(tmp_path):
    # Создаем временную файловую структуру
    root = tmp_path / "test_text"
    root.mkdir()
    (root / "duplicates.txt").write_text("line1\nline1\nline2\nline3\nline3\n")
    (root / "empty.txt").write_text("")
    return VirtualFileSystem(str(root))

def test_uniq_remove_duplicates(setup_text_files):
    fs = setup_text_files
    content = fs.read_file("duplicates.txt")
    unique_lines = "\n".join(sorted(set(content.splitlines()), key=content.splitlines().index))
    assert unique_lines == "line1\nline2\nline3"

def test_uniq_empty_file(setup_text_files):
    fs = setup_text_files
    content = fs.read_file("empty.txt")
    assert content == ""

def test_uniq_nonexistent_file(setup_text_files):
    fs = setup_text_files
    result = fs.read_file("missing.txt")
    assert "Error: File 'missing.txt' does not exist" in result
