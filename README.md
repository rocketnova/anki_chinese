# Anki Chinese

## Overview

Anki Chinese is script that generates `notes` for the [Anki](https://apps.ankiweb.net) flash card program. It is specifically designed for English speakers learning Chinese who wish to learn using Taiwan/ROC zhuyin (注音符號) and Taiwan/ROC stroke order (筆順).

Anki Chinese accepts a [vocabulary list in YAML format](#usage) and outputs:

- A CSV for importing into Anki using a specific [Anki note type](#anki-note-type)
- PNG images of the Taiwan stroke order

The Taiwan stroke order is downloaded from https://stroke-order.learningweb.moe.edu.tw/character.do.

## Anki Note Type

Anki [supports importing comma separated text files](https://docs.ankiweb.net/importing.html). During import, you choose which field in the text file is mapped to which field in an existing note type.

This script is specifically meant to work with single or multi-character Chinese phrases, such as 雨, 十二月底.

This script generates the following fields:

- Chinese phrase
- English meaning
- Zhuyin
- Pinyin
- Stroke order (image)
- Character 1
- Zhuyin 1
- Pinyin 1
- Character 2
- Zhuyin 2
- Pinyin 2
- Character 3
- Zhuyin 3
- Pinyin 3
- etc

Note: The number of pairs of "character" and "zhuyin" fields you need depends on the max length of your phrases. For example, if the longest phrase in your vocabulary list is 7 characters long, add 7 pairs of character/zhuyin fields in Anki.

## Anki Card Types

This note type is designed to work with the following card types, but you can, of course, use the note fields to create whatever card types you want.

- Reading recognition: Hanzi + Zhuyin (hint) --> English meaning
- Recall: English meaning + Zhuyin (hint) --> Hanzi + stroke order (hint)
- Character 1 recognition: Character 1 --> Zhuyin
- Character 2, 3 etc

Import `card_template.apkg` to import these example card types.

## Dependencies

- [Anki desktop](https://apps.ankiweb.net)
- python3
- [pyyaml](https://pypi.org/project/PyYAML)
- [svglib](https://pypi.org/project/svglib)
- [reportlab](https://www.reportlab.org)
- 圓體W3寬注音.ttc from DynaFont (must be installed)
- Requires an internet connection to download stroke pngs

_Note: Zhuyin will NOT be generated if you do not have 圓體W3寬注音.ttc installed!_

## Usage

To generate a CSV to import into Anki, along with accompanying images:

```
python3 lib/ac_csv.py vocab_file.yml
```

where `vocab_file.yml` is a YAML-formatted file of vocabulary words to be turned into flash cards. The expected format is:

```yaml
十二月底: The end of December
雨: Rain
傘: Umbrella
颱風: Typhoon
```

This will output:

```
anki_chinese/
├── anki_import.csv
├── images/
    ├── stroke_pngs/
    ├── zhuyin_pngs/
    └── zhuyin_svgs/
```

### Options

* `--char_file char_file.txt`: This is a text file that contains a list of known characters. For example: `接臺灣歡迎陳華文張這姓叫請問謝不客氣喝茶`. If a character exists in `char_file.txt`, then Anki Chinese will not generate new single character cards in order to reduce duplicates in Anki. If a character file is NOT provided, Anki Chinese will still prevent duplicates from WITHIN the same vocab file. For example: `臺灣: Taiwan` and `臺北: Taipei` will generate only single characters 3 characters (`臺灣北`), not 4. Anki Chinese will update the character file with any new characters provided in the vocab file. This creates a handy side effect where you can see the total number of unique characters you've studied.
* `--tags "tag1 tag2 tag3"`: All the tags passed in will be applied to each row in the CSV. This means that separating each book or each chapter into a separate yaml file is recommended. You can then pass in "ch1" or "book1" tags for each yaml.
* `--update`: Using this flag will force Anki Chinese to generate all new images, even if images already exist. The default behavior is to NOT generate a new image if a file with the same name already exists).

### Importing into Anki

0. Make sure the appropriate note type and card types have been created in Anki (see above).
1. Copy all the images in `zhuyin_pngs` and `stroke_pngs` to Anki's `collection.media` folder. See https://apps.ankiweb.net/docs/manual.html#importing-media to locate the folder. Do not create subfolders in `collection.media`.
2. Import the `anki_import.csv` file into Anki. See https://apps.ankiweb.net/docs/manual.html#importing for more info. Make sure to set the last field to "Tags".

_Note: The images in `zhuyin_svgs` are used to generate the svgs and do not need to be copied into the `collection.media` folder._

You may notice that not all character/zhuyin fields are filled out in `anki_import.csv`. That's ok. Anki knows to ignore those.

### Generating images only

If you only need to generate images without creating a CSV for import, you can use the helper script:

```
python3 lib/ac_imgs.py phrase
```

where `phrase` is the Chinese phrase you want to generate images for, such as 臺灣 or 這.

This will output images in the same folders as `ac_csv.py` uses. You may optionally use the `--update` flag to overwrite existing images.

## Known Issues

### svglib

svglib has an issue where it only loads `.ttf` fonts, which can cause errors if using a `.ttc` Chinese font. `.ttc` fonts are [TrueType Collection](https://en.wikipedia.org/wiki/TrueType#TrueType_Collection) fonts, which are an extension of the TrueType format. An issue has been filed at https://github.com/deeplook/svglib/issues/226.

Currently using the manually patched version of `svglib` in the `svglibcustom` dir.

### Taiwan MOE ssl cert

The intermediate certificates for https://stroke-order.learningweb.moe.edu.tw seem to be misconfigured. See https://whatsmychaincert.com/?stroke-order.learningweb.moe.edu.tw and https://www.sslshopper.com/ssl-checker.html#hostname=https://stroke-order.learningweb.moe.edu.tw.

It appears to be an issue with https://stroke-order.learningweb.moe.edu.tw in particular, not necessarily the issuer 政府伺服器數位憑證管理中心 - G1. The same issuer is used for https://eng.taiwan.net.tw, which is correctly configured. See https://www.sslshopper.com/ssl-checker.html#hostname=https://eng.taiwan.net.tw.

Currently using an ssl context that bypasses cert verification.

**WARNING: USE AT YOUR OWN RISK.**
