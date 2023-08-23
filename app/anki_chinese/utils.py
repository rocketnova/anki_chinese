#!/usr/bin/env python

import yaml
import csv
import logging
import os.path

def load_vocab(vocab_file):
    """
    Parses yaml containing vocabulary.
    Expects the following format
      PHRASE: MEANING
    Example:
      臺灣: Taiwan
      接: To pick someone up
    """
    vocab = ''
    with open(vocab_file) as vf:
        vocab = yaml.safe_load(vf)
    logging.debug(f"Loaded vocab file: {vocab_file}")
    return vocab

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

def make_image_dirs(dirs):
    """
    Creates image directories if they do not already exist
    """
    for dir in dirs:
        if os.path.isdir(dir) == False:
            os.mkdir(dir)
            logging.debug(f"Created: {dir}")

def is_new_char(char_list, char):
    """
    Returns True if the character does not yet exist in the character list
    """
    return char_list.find(char) == -1

def write_text(file, string):
    """
    Writes a string to a file.
    """
    with open(file, "w+") as cf:
        cf.write(string)

def write_csv(rows, filename):
    """
    Writes a dictionary to a CSV formatted file.
    """
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        for row in rows:
            writer.writerow(row)

