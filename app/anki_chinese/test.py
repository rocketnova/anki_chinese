#!/usr/bin/env python

import click
import yaml

@click.command()
@click.argument('vocab_file', type=click.File('rb'))
@click.option('-c', '--char-file', type=click.File('wb'), help='A text file containing a character list (prevents duplicate cards in Anki).')
@click.option('--no-update-char', is_flag=True, help="Must be used in conjuction with -c/--char-file. Will use an existing character list, but won't update it.")
@click.option('-t', '--tags', multiple=True, help="Tags to be applied to every entry in the CSV. Multiple tags must be double quoted.")
@click.option('-v', '--verbose', help="Increase output verbosity.")
def main(vocab_file, char_file, no_update_char, tags, verbose):
    """
    Generates a CSV of Hanzi (Chinese vocabulary), English meaning, zhuyin, pinyin, and Taiwan stroke order for import into Anki.

    VOCAB_FILE is a vocab list in YAML format.

    VOCAB_FILE should be in the format: `十二月底: The end of December`
    """

    to_csv = []

    click.echo("Hello World")
    for tag in tags:
        click.echo(tag)


# Parses yaml containing vocabulary.
# Expects the following format
#   PHRASE: MEANING
# Example:
#   臺灣: Taiwan
#   接: To pick someone up
def load_vocab(vocab_file):
    vocab = ''
    with open(vocab_file) as vf:
        vocab = yaml.safe_load(vf)

if __name__ == "__main__":
    main()
