#!/usr/bin/env python

# Import project modules
import csv
import sys
import yaml
#from svglibcustom.svglibcustom import svg2rlg
#from reportlab.graphics import renderPDF, renderPM
import ssl
import urllib.request
import os.path
import logging

IMG_DIR = "images"
SVG_DIR = f"{IMG_DIR}/zhuyin_svgs"
PNG_DIR = f"{IMG_DIR}/zhuyin_pngs"
STROKE_DIR = f"{IMG_DIR}/stroke_pngs"
CSV_FILE = "anki_import.csv"

# Generates a Zhuyin SVG for each phrase.
# The DFPYuanW3-ZhuInW.ttc font must be installed.
def gen_svg(text, update):
    svg_filename = f"{SVG_DIR}/{text}.svg"
    if update == False and os.path.isfile(svg_filename) == True:
        return None
    else:
        svg="""
    <svg viewBox="0 0 400 100" preserveAspectRatio="xMidYMid meet" xmlns="http://www.w3.org/2000/svg">
      <text fill="black" font-family="圓體W3寬注音#DFPYuanW3-ZhuInW-BFW,圓體W3寬注音" font-size="80px" x="200" y="70" text-anchor="middle">{}</text>
    </svg>
    """.format(text)[1:-1]
        with open(svg_filename, "w+") as file:
            file.write(svg)
        logging.debug(f"Wrote: {svg_filename}")

# Generates a Zhuyin PNG using the SVG.
# SVG must already exist.
def gen_png(text, update):
    png_filename = f"{PNG_DIR}/{text}.png"
    if update == False and os.path.isfile(png_filename) == True:
        return None
    else:
        drawing = svg2rlg(f"{SVG_DIR}/{text}.svg")
        renderPM.drawToFile(drawing, png_filename, fmt="PNG")
        logging.debug(f"Wrote: {png_filename}")

# Requests the stroke order PNGs from https://stroke-order.learningweb.moe.edu.tw
def gen_stroke(text, update):
    stroke_tags = ""
    for char in text:
        stroke_filename = f"{STROKE_DIR}/{char}-stroke.png"
        if update == False and os.path.isfile(stroke_filename) == True:
            stroke_tags = stroke_tags + stroke_tag(char)
            continue
        else:
            try:
                big5char = char.encode("big5", "strict").hex().upper()
                url = f"https://stroke-order.learningweb.moe.edu.tw/words/{big5char}.png"
                # Hack to ignore SSL warnings, since the intermediate certificates for
                # https://stroke-order.learningweb.moe.edu.tw seem to be misconfigured.
                # See https://whatsmychaincert.com/?stroke-order.learningweb.moe.edu.tw
                # USE AT YOUR OWN RISK.
                context = ssl._create_unverified_context()
                try:
                    with urllib.request.urlopen(url, context=context) as response, open(stroke_filename, 'wb') as file:
                        # A `bytes` object
                        data = response.read()
                        file.write(data)
                        stroke_tags = stroke_tags + stroke_tag(char)
                        logging.debug(f"Wrote: {stroke_filename}")
                except urllib.error.HTTPError as error:
                    # MOE will return 404 for characters that have no stroke image available
                    # Example: https://stroke-order.learningweb.moe.edu.tw/characterQueryResult.do?word=%E6%BF%95
                    logging.warning(f"No stroke found for: {char}")
            except UnicodeEncodeError as error:
                # Some more archaic or variant characters do not have a big5 encoding
                logging.warning(f"No big5 encoding for: {char}. Recommendation: manually download an appropriate stroke image, if one exists")
    return stroke_tags

# Returns the character(s) as zhuyin via wiktionary lookup.
def get_zhuyin(chars):
    import requests
    import re
    from bs4 import BeautifulSoup
    url = f"https://en.wiktionary.org/wiki/{chars}"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    audio = soup.select('audio source[data-title=MP3]')
    print(audio)
    stroke_url = soup.find_all(src=re.compile("-order.gif"))
    print(stroke_url)
    zhuyin = soup.select('.Bopo')[0]
    print(zhuyin.prettify())
    print(zhuyin.string)
    print(gen_stroke(chars, False))

def get_stroke_order(char):
    return ''
    
# Returns True if the character does not yet exist in the characterlist
def is_new_char(char_list, char):
    return char_list.find(char) == -1

# Returns the HTML string Anki expects for char images.
def char_tag(char):
    return f"<img src=\"{char}.png\" />"

# Returns the HTML string Anki expects for stroke images.
def stroke_tag(char):
    return f"<img src=\"{char}-stroke.png\" />"


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
    logging.debug(f"Loaded vocab file: {vocab_file}")
    return vocab

# Parses the character list into a variable.
# The character list file should contain no more than 1 copy of each Chinese character.
# It is acts as a flat file database to demonstrate known characters.
def load_char_list(char_file):
    chars = ''
    with open(char_file) as cf:
        chars = cf.read().replace('\n', '')
    logging.debug(f"Loaded character file: {char_file}")
    return chars

# Writes a string to a file.
def write_text(file, string):
    with open(file, "w+") as cf:
        cf.write(string)

# Writes a dictionary to a CSV formatted file.
def write_csv(to_csv):
    with open(CSV_FILE, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in to_csv:
            writer.writerow(row)

# Creates image directories if they do not already exist
def make_image_dirs():
    dirs = [IMG_DIR, SVG_DIR, PNG_DIR, STROKE_DIR]
    for dir in dirs:
        if os.path.isdir(dir) == False:
            os.mkdir(dir)
            logging.debug(f"Created: {dir}")
