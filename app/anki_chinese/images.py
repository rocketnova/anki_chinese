#!/usr/bin/env python
# Template based on https://gist.github.com/opie4624/3896526

# Import template modules
import argparse, logging
from ac_util import *

# Generates zhuyin and stroke order images from a Chinese phrase.
# - SVGs: 學.svg
# - PNGs: 學.png
# - Stroke PNGs: 學-stroke.png
def main(args, loglevel):
    logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)

    phrase = args.phrase
    update = args.update

    make_image_dirs()
    gen_svg(phrase, update)
    gen_png(phrase, update)
    gen_stroke(phrase, update)

    for char in phrase:
        if len(phrase) > 1:
            gen_svg(char, update)
            gen_png(char, update)

# Standard boilerplate to call the main() function to begin the program.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                                      description = "Generates zhuyin images and Taiwan stroke order for a Chinese phrase.",
                                      epilog = "As an alternative to the commandline, params can be placed in a file, one per line, and specified on the commandline like '%(prog)s @params.conf'.",
                                      fromfile_prefix_chars = '@' )
    parser.add_argument(
                        "phrase",
                        help = "A phrase in Chinese")
    parser.add_argument(
                        "-u",
                        "--update",
                        help="Update (overwrite) any existing images",
                        action="store_true")
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
