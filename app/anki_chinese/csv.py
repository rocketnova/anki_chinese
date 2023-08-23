#!/usr/bin/env python
# Template based on https://gist.github.com/opie4624/3896526

# Import template modules
import argparse, logging
from ac_util import *

# Generates a CSV of Chinese vocabulary with accompanying zhuyin images and Taiwan stroke order for import into Anki.
# - CSV: anki-import.csv (will append tags as the last field)
# - SVGs: 學.svg
# - PNGs: 學.png
# - Stroke PNGs: 學-stroke.png
def main(args, loglevel):
    logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)

    vocab_file = args.vocab_file
    char_file = args.char_file
    no_update_char = args.no_update_char
    update = args.update
    tags = args.tags
    to_csv = []

    # Read files into variables.
    vocab = load_vocab(vocab_file)
    if char_file:
        char_list = load_char_list(char_file)
    else:
        char_list = ""

    # Prepare image directors.
    make_image_dirs()

    # For each new vocab word, create a new CSV row entry that contains:
    # - Chinese phrase
    # - English meaning
    # - Image tag of zhuyin for the phrase
    # - Image tag(s) for the stroke order for the characters in the phrase
    # - For each unique character in the phrase:
    #   - Chinese character
    #   - Image tag of zhuyin
    for phrase, meaning in vocab.items():
        row = [phrase, meaning]

        gen_svg(phrase, update)
        gen_png(phrase, update)
        row.append(char_tag(phrase))

        stroke_tags = gen_stroke(phrase, update)
        # DEBUG START
        # stroke_tages = ""
        # for char in phrase:
        #     stroke_tags = stroke_tags + stroke_tag(char)
        # DEBUG END
        row.append(stroke_tags)

        for char in phrase:
            # Update the running list of known characters if it is not already known
            if is_new_char(char_list, char) == True:
                char_list = char_list + char
                # Append the character and zhuyin for each character in the phrase.
                # Skip phrases that are only 1 character long since it would just be a duplicate.
                if len(phrase) > 1:
                    gen_svg(char, update)
                    gen_png(char, update)
                    row.append(char)
                    row.append(char_tag(char))
        to_csv.append(row)
        logging.debug(f"Appending: {row}")

    max_length = len(max(to_csv, key=len))
    # Subtract # non character fields (Chinese phrase, English meaning, Phrase zhuyin, Phrase strokes)
    # Don't include tags, which is added later
    max_char = (max_length - 4) / 2

    # Make all rows the same length.
    # Add tags as the last field.
    for row in to_csv:
        row[:] = row + [''] * (max_length - len(row)) + [tags]

    # Update the character file.
    if char_file and no_update_char == False:
        write_text(char_file, char_list)

    # Write the CSV.
    write_csv(to_csv)

    # Print summary.
    logging.info(f"Generated CSV for {len(to_csv)} characters.")
    if (max_char > 0):
        logging.warning(f"Anki must be able to support at least {int(max_char)} character fields.")


# Standard boilerplate to call the main() function to begin the program.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                                      description = "Generates a CSV of Chinese vocabulary with accompanying zhuyin images and Taiwan stroke order for import into Anki.",
                                      epilog = "As an alternative to the commandline, params can be placed in a file, one per line, and specified on the commandline like '%(prog)s @params.conf'.",
                                      fromfile_prefix_chars = '@' )
    parser.add_argument(
                        "vocab_file",
                        help = "A vocab list in YAML format")
    parser.add_argument(
                        "-c",
                        "--char-file",
                        help = "A text file containing a character list (prevents duplicate cards in Anki)")
    parser.add_argument(
                        "--no-update-char",
                        help="Must be used in conjuction with -c/--char-file. Will read in an existing character file, but won't update it",
                        action="store_true")
    parser.add_argument(
                        "-t",
                        "--tags",
                        help="Tags to be applied every entry in the CSV. Multiple tags must be double quoted",
                        metavar = "TAGS")
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
