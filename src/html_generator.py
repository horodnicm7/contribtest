import json
import os
import logging
import ntpath

import jinja2
from jinja2 import FileSystemLoader

from src.utils.file_system_manager import FileSystemManager

log = logging.getLogger(__name__)
logging.basicConfig()


class HtmlFileGenerator(object):
    TEMPLATE_DIRECTORY_NAME = 'layout/'

    def __init__(self, input_directory, output_directory):
        """
        Main constructor for this class
        :param input_directory: the directory from which the files used in the HTML generation are
        :param output_directory: the location of the future generated HTML files
        """
        self.input_directory_path = input_directory
        self.output_directory_path = output_directory
        self.jinja_env = jinja2.Environment(loader=FileSystemLoader(self.input_directory_path))

    @staticmethod
    def read_template_resource(file_path):
        """
        This method parses a resource file used to fill in the jinja template of a HTML file.
        :param file_path: the file's path
        :return: Tuple(dict, str)
        """
        with open(file_path, 'rt') as f:
            raw_metadata = ""
            for line in f:
                if line.strip() == '---':
                    break
                raw_metadata += line

            content = ""
            for line in f:
                content += line.strip("\n")

        return json.loads(raw_metadata), content

    def generate(self):
        """
        Generates a HTML file for every resource file (with *.rst extension), based on a jinja template.
        The generated files will be grouped under a root directory.
        :return: None
        """
        log.info("Generating site from %r", self.input_directory_path)

        # iterate over every resource file, load its corresponding template file
        # and generate the output html file based on those two
        for file_path in FileSystemManager.list_files(self.input_directory_path):
            metadata, content = HtmlFileGenerator.read_template_resource(file_path)

            template_name = metadata['layout']
            template = self.jinja_env.get_template(HtmlFileGenerator.TEMPLATE_DIRECTORY_NAME + template_name)

            # render the html file content, with the data from the resource file
            data = dict(metadata, content=content)
            html = template.render(**data)

            # get the file name, without extension
            file_name = os.path.splitext(ntpath.basename(file_path))[0]

            # build the output file path
            output_file_path = os.path.join(self.output_directory_path, file_name + ".html")

            log.info("Writing %r with template %r", output_file_path, template_name)
            FileSystemManager.write_output(output_file_path, html)
