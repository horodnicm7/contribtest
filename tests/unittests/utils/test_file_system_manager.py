import os

from unittest.mock import patch, MagicMock, mock_open

from src.utils.file_system_manager import FileSystemManager


def test_list_files_no_resource_files(monkeypatch):
    def mocked_listdir(path):
        return ["a.css", "b.html"]

    monkeypatch.setattr(os, 'listdir', mocked_listdir)
    assert list(FileSystemManager.list_files("/some_path")) == []


def test_list_files_found_resource_files_success(monkeypatch):
    def mocked_listdir(path):
        return ["a.css", "b.html", "c.rst", "w.rst"]

    monkeypatch.setattr(os, 'listdir', mocked_listdir)
    assert list(FileSystemManager.list_files("/some_path")) == [os.path.join("/some_path", "c.rst"),
                                                                os.path.join("/some_path", "w.rst")]


def test_write_output_no_tree_path(monkeypatch):
    monkeypatch.setattr(os.path, 'exists', MagicMock(return_value=False))

    with patch('pathlib.Path.mkdir', new=MagicMock()) as mocked_mkdir, \
            patch("builtins.open", mock_open(read_data="data")), \
            patch('typing.IO.write', MagicMock()):
        FileSystemManager.write_output("/path", "content")

        mocked_mkdir.assert_called_once_with(parents=True, exist_ok=True)


def test_write_output_existing_tree_path(monkeypatch):
    monkeypatch.setattr(os.path, 'exists', MagicMock(return_value=True))

    with patch('pathlib.Path.mkdir', new=MagicMock()) as mocked_mkdir, \
            patch("builtins.open", mock_open(read_data="data")), \
            patch('typing.IO.write', MagicMock()):
        FileSystemManager.write_output("/path", "content")

        mocked_mkdir.assert_not_called()
