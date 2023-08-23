#!/usr/bin/env python

import click
from anki_chinese.utils import *
import logging

@click.command()
@click.argument('vocab_file')
@click.option('-c', '--char-file', help='A text file containing a character list (prevents duplicate cards in Anki).')
@click.option('--no-update-char', is_flag=True, help="Must be used in conjuction with -c/--char-file. Will use an existing character list, but won't update it.")
@click.option('-t', '--tags', multiple=True, help="Tags to be applied to every entry in the CSV. Multiple tags must be double quoted.")
@click.option('-v', '--verbose', is_flag=True, help="Increase output verbosity.")
def main(vocab_file, char_file, no_update_char, tags, verbose):
    """
    Generates a CSV of Hanzi (Chinese vocabulary), English meaning, zhuyin, pinyin, and Taiwan stroke order for import into Anki.

    VOCAB_FILE is a vocab list in YAML format.

    VOCAB_FILE should be in the format: `十二月底: The end of December`
    """
    # Setup logging
    if verbose:
      loglevel = logging.DEBUG
    else:
      loglevel = logging.INFO
    logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)

    to_csv = []

    click.echo("Hello World")

    # Read files into variables.
    vocab = load_vocab(vocab_file)
    if char_file:
        char_list = load_char_list(char_file)
    else:
        char_list = ""

    click.echo(char_list)


if __name__ == "__main__":
    main()
