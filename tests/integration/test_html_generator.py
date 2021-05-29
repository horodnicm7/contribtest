import os

from src.html_generator import HtmlFileGenerator
import shutil


OUTPUT_DIRECTORY = 'output'
INPUT_DIRECTORY = 'test/source'
REFERENCE_FILES_PATH = 'test/expected_output'


def test_success():
    """
    Tests the whole HTML file generation functionality
    :return: None
    """
    # remove old tests results, if any
    if os.path.exists(OUTPUT_DIRECTORY):
        shutil.rmtree(OUTPUT_DIRECTORY)

    generator = HtmlFileGenerator(INPUT_DIRECTORY, OUTPUT_DIRECTORY)
    generator.generate()

    # compare every reference file with the generated one by the python script
    for file_name in os.listdir(REFERENCE_FILES_PATH):
        test_output_file = os.path.join(OUTPUT_DIRECTORY, file_name)
        reference_file_path = os.path.join(REFERENCE_FILES_PATH, file_name)

        if not os.path.exists(test_output_file):
            assert False

        with open(test_output_file, "rt") as test_file, \
                open(reference_file_path, "rt") as reference_file:
            test_generated_content = test_file.read()
            reference_content = reference_file.read()

        assert test_generated_content == reference_content

    # test teardown
    shutil.rmtree(OUTPUT_DIRECTORY)
