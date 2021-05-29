import os

from pathlib import Path


class FileSystemManager(object):
    @staticmethod
    def list_files(folder_path):
        for name in os.listdir(folder_path):
            _, ext = os.path.splitext(name)
            if ext != '.rst':
                continue
            yield os.path.join(folder_path, name)

    @staticmethod
    def write_output(output_file_path, content):
        # create the directory tree if the file doesn't exist
        if not os.path.exists(output_file_path):
            Path(os.path.dirname(output_file_path)).mkdir(parents=True, exist_ok=True)

        with open(output_file_path, "wt") as f:
            f.write(content)
