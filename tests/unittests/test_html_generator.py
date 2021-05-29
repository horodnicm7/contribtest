import os
from json import JSONDecodeError
from unittest.mock import patch, MagicMock, mock_open

import pytest

from src.html_generator import HtmlFileGenerator


@patch('src.utils.file_system_manager.FileSystemManager.list_files', new=MagicMock(return_value=["/input/res.rst"]))
@patch('src.html_generator.HtmlFileGenerator.read_template_resource', new=MagicMock(return_value=(
        {"title": "My awesome site", "layout": "home.html"},
        "content"
    )))
@patch('src.utils.file_system_manager.FileSystemManager.write_output')
def test_generate_success(write_mock):
    generator = HtmlFileGenerator("/input", "/output")

    template_mock = MagicMock()
    template_mock.render = MagicMock(return_value="<h1>My awesome site</h1>\ncontent\n")

    generator.jinja_env = MagicMock()
    generator.jinja_env.get_template = MagicMock(return_value=template_mock)

    generator.generate()

    write_mock.assert_called_once_with(os.path.join("/output", "res.html"), "<h1>My awesome site</h1>\ncontent\n")


def test_read_template_resource_invalid_json():
    mocked_open_result = "{\"titlinvalid json \"layout: \"home.html\"}\n---\nsome content"
    with patch("builtins.open", mock_open(read_data=mocked_open_result)), \
         pytest.raises(JSONDecodeError):
        HtmlFileGenerator.read_template_resource('/path')


def test_read_template_resource_no_content():
    mocked_open_result = "{\"title\": \"My awesome site\", \"layout\": \"home.html\"}\n---\n"
    with patch("builtins.open", mock_open(read_data=mocked_open_result)):
        result = HtmlFileGenerator.read_template_resource('/path')
        assert result == ({"title": "My awesome site", "layout": "home.html"}, "")


def test_read_template_resource_success():
    mocked_open_result = "{\"title\": \"My awesome site\", \"layout\": \"home.html\"}\n---\nsome content"
    with patch("builtins.open", mock_open(read_data=mocked_open_result)):
        result = HtmlFileGenerator.read_template_resource('/path')
        assert result == ({"title": "My awesome site", "layout": "home.html"}, "some content")
