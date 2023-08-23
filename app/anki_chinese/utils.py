#!/usr/bin/env python

import yaml
import logging

def load_vocab(vocab_file):
    """
    Parses yaml containing vocabulary.
    Expects the following format
      HANZI: MEANING
    Example:
      臺灣: Taiwan
      接: To pick someone up
    """
    vocab = ''
    with open(vocab_file) as vf:
        vocab = yaml.safe_load(vf)
    logging.debug(f"Loaded vocab file: {vocab_file}")

def load_char_list(char_file):
    """
    Parses the character list into a variable.
    The character list file should contain no more than 1 copy of each Chinese character.
    It is acts as a flat file database of learned characters.
    """
    chars = ''
    with open(char_file) as cf:
        chars = cf.read().replace('\n', '')
    logging.debug(f"Loaded character file: {char_file}")
    return chars

