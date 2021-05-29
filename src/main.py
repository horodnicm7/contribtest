import sys

from src.html_generator import HtmlFileGenerator


def main():
    site_generator = HtmlFileGenerator(sys.argv[1], sys.argv[2])
    site_generator.generate()


if __name__ == '__main__':
    main()
