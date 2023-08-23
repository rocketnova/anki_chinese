#!/usr/bin/env python

import yaml
import csv
import logging
import os.path
import urllib.request
import urllib.parse
from dragonmapper import hanzi

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

def get_zhuyin(chars):
    """
    Returns the zhuyin for the input.
    """
    return hanzi.to_zhuyin(chars)

def get_pinyin(chars):
    """
    Returns the pinyin for the input.
    """
    return hanzi.to_pinyin(chars)

def get_stroke_tag(char):
    """
    Returns the HTML string Anki expects for stroke images.
    """
    return f"<img src=\"{char}-stroke.png\" />"

def gen_stroke(phrase, stroke_dir, no_update_images):
    """
    Downloads the stroke order PNGs
    """
    stroke_tags = ""
    for char in phrase:
        stroke_filename = f"{stroke_dir}/{char}-stroke.png"
        if no_update_images == True and os.path.isfile(stroke_filename) == True:
            stroke_tags = stroke_tags + get_stroke_tag(char)
            continue
        else:
            escaped_char = urllib.parse.quote(char)
            url = f"https://raw.githubusercontent.com/rocketnova/anki_chinese/main/stroke-order.learningweb.moe.edu.tw/6057png/{escaped_char}.png"
            try:
                with urllib.request.urlopen(url) as response, open(stroke_filename, 'wb') as file:
                    # A `bytes` object
                    data = response.read()
                    file.write(data)
                    stroke_tags = stroke_tags + get_stroke_tag(char)
                    logging.debug(f"Wrote: {stroke_filename}")
            except urllib.error.HTTPError as error:
                # MOE will return 404 for characters that have no stroke image available
                logging.warning(f"No stroke found for: {char}")
    return stroke_tags

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

