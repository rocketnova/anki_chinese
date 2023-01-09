#!/usr/bin/env python

# Requires:
# - Google Cloud Translation account
# - google-cloud-translate==2.0.0
# Before each use run `export GOOGLE_APPLICATION_CREDENTIALS="/home/user/Downloads/service-account-file.json"`

import argparse, logging
from ac_util import *
from gtrans import trans

def load_text(text_file):
    with open(text_file) as ct:
        text_st = ct.read()
    logging.debug(f"Loaded text file: {text_file}")
    return text_st

# Expects:
# TITLE (Optional)
# <empty line> (Required if passing in title)
# SECTION TITLE
# SECTION TEXT
# <empty line>
# SECTION TITLE
# SECTION TEXT
# <empty line>
# etc
def main(args, loglevel):
    logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)

    text_file = args.text_file
    is_book = args.book
    tags = args.tags
    rows = []
    title = ''

    text_st = load_text(text_file)
    sections = text_st.split('\n\n')

    if is_book == True:
        title = sections.pop(0)

    for s in sections:
        s_lines = s.split('\n')
        s_title = s_lines.pop(0)
        s_text = '\n'.join(s_lines)
        logging.debug(s_text)

        s_en = trans(s_text, 'en')
        rows.append([s_title, s_text, s_en, title, tags])

    logging.debug(rows)
    write_csv(rows)


# Standard boilerplate to call the main() function to begin the program.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                                      description = "Generates a CSV of Chinese text to be imported into Anki",
                                      epilog = "As an alternative to the commandline, params can be placed in a file, one per line, and specified on the commandline like '%(prog)s @params.conf'.",
                                      fromfile_prefix_chars = '@' )
    parser.add_argument(
                        "text_file",
                        help = "A plain text file")
    parser.add_argument(
                        "-b",
                        "--book",
                        help="Indicate that the text_file is composed of book chapters separated by empty lines. First line should be the book title",
                        action="store_true")
    parser.add_argument(
                        "-t",
                        "--tags",
                        help="Tags to be applied every entry in the CSV. Multiple tags must be double quoted",
                        metavar = "TAGS")
    parser.add_argument(
                        "-v",
                        "--verbose",
                        help="Increase output verbosity",
                        action="store_true")
    args = parser.parse_args()

    # Setup logging
    if args.verbose:
      loglevel = logging.DEBUG
    else:
      loglevel = logging.INFO

    main(args, loglevel)
