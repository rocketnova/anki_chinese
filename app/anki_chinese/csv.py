#!/usr/bin/env python

import click
from anki_chinese.utils import *
import logging

@click.command()
@click.argument('vocab_file')
@click.option('-c', '--char-file', help='A text file containing a character list (prevents duplicate cards in Anki).')
@click.option('--no-update-chars', is_flag=True, help="Must be used in conjuction with -c/--char-file. Will use an existing character list, but won't update it.")
@click.option('--no-update-images', is_flag=True, help="Skip updating existing images.")
@click.option('-t', '--tags', multiple=True, help="Tags to be applied to every entry in the CSV. Multiple tags must be double quoted.")
@click.option('-v', '--verbose', is_flag=True, help="Increase output verbosity.")
def main(vocab_file, char_file, no_update_chars, no_update_images, tags, verbose):
    """
    Generates a CSV of Chinese vocabulary, English meaning, zhuyin, pinyin, and Taiwan stroke order for import into Anki.

    VOCAB_FILE is a vocab list in YAML format.

    VOCAB_FILE should be in the format: `十二月底: The end of December`
    """
    # Setup logging.
    if verbose:
      loglevel = logging.DEBUG
    else:
      loglevel = logging.INFO
    logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)

    # Read files into variables.
    vocab = load_vocab(vocab_file)
    if char_file:
        char_list = load_char_list(char_file)
    else:
        char_list = ""

    # Prepare image directors.
    stroke_dir = "images/stroke_order"
    make_image_dirs(["images", stroke_dir])

    # For each new vocab word, create a new CSV row entry that contains:
    # - Chinese phrase
    # - English meaning
    # - Zhuyin for the phrase
    # - Pinyin for the phrase
    # - Image tag(s) for the stroke order for the characters in the phrase
    # - For each unique character in the phrase:
    #   - Hanzi
    #   - Zhuyin
    #   - Pinyin
    rows = []
    longest_phrase_count = 0
    for phrase, meaning in vocab.items():
        # Append the phrase and meaning to the row.
        row = [phrase, meaning]

        # Add zhuyin and pinyin to the row.
        row.append(get_zhuyin(phrase))
        row.append(get_pinyin(phrase))

        # Add stroke order to the row.
        stroke_tags = gen_stroke(phrase, stroke_dir, no_update_images)
        row.append(stroke_tags)

        # Process each character in the Chinese phrase.
        for char in phrase:
            # If the character is not in the char_list, add it.
            if is_new_char(char_list, char) == True:
                char_list = char_list + char
                # Add the character, zhuyin, and pinyin to the row.
                # Skip phrases that are only 1 character long since it would just be a duplicate.
                if len(phrase) > 1:
                    row.append(char)
                    row.append(get_zhuyin(char))
                    row.append(get_pinyin(char))

        # Keep track of the longest vocab phrase.
        # This gets output as a warning when the csv is created.
        if len(phrase) > longest_phrase_count:
            longest_phrase_count = len(phrase)

        # Save the row.
        rows.append(row)
        logging.debug(f"Adding row: {row}")

    # Make all rows the same length.
    # Add tags as the last field.
    max_length = len(max(rows, key=len))
    for row in rows:
        row[:] = row + [''] * (max_length - len(row)) + [' '.join(tags)]

    # Update the character file.
    if char_file and no_update_chars == False:
        write_text(char_file, char_list)

    # Write the CSV.
    write_csv(rows, "import_into_anki.csv")

    # Print summary.
    logging.info(f"Generated CSV for {len(rows)} vocabulary phrases.")
    if (longest_phrase_count > 0):
        logging.warning(f"Anki note type must be able to support at least {int(longest_phrase_count)} character fields.")


if __name__ == "__main__":
    main()
