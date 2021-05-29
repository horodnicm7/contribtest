# generate site from static pages, loosely inspired by Jekyll
# run like this:
#   ./generate.py test/source output
# the generated `output` should be the same as `test/expected_output`
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

    def __init__(self, input_folder, output_folder):
        self.input_folder_path = input_folder
        self.output_folder_path = output_folder
        self.jinja_env = jinja2.Environment(loader=FileSystemLoader(self.input_folder_path))

    @staticmethod
    def read_template_resource(file_path):
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
        log.info("Generating site from %r", self.input_folder_path)

        # iterate over every resource file, load its corresponding template file
        # and generate the output html file based on those two
        for file_path in FileSystemManager.list_files(self.input_folder_path):
            metadata, content = HtmlFileGenerator.read_template_resource(file_path)

            template_name = metadata['layout']
            template = self.jinja_env.get_template(HtmlFileGenerator.TEMPLATE_DIRECTORY_NAME + template_name)

            # render the html file content, with the data from the resource file
            data = dict(metadata, content=content)
            html = template.render(**data)

            # get the file name, without extension
            file_name = os.path.splitext(ntpath.basename(file_path))[0]

            # build the output file path
            output_file_path = os.path.join(self.output_folder_path, file_name + ".html")

            log.info("Writing %r with template %r", output_file_path, template_name)
            FileSystemManager.write_output(output_file_path, html)
