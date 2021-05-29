import os

from pathlib import Path


class FileSystemManager(object):
    @staticmethod
    def list_files(directory_path):
        """
        Returns a stream of resource files from the specified directory path
        :param directory_path: directory path
        :return: Stream of strings
        """
        for name in os.listdir(directory_path):
            _, ext = os.path.splitext(name)
            if ext != '.rst':
                continue
            yield os.path.join(directory_path, name)

    @staticmethod
    def write_output(output_file_path, content):
        """
        Writes the specified content to a specified output file
        :param output_file_path: the file's path
        :param content: content to write
        :return: None
        """
        # create the directory tree if the file doesn't exist
        if not os.path.exists(output_file_path):
            Path(os.path.dirname(output_file_path)).mkdir(parents=True, exist_ok=True)

        with open(output_file_path, "wt") as f:
            f.write(content)
