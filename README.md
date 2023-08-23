# Anki Chinese

## Overview

Anki Chinese is script that generates `notes` for the [Anki](https://apps.ankiweb.net) flash card program. It is specifically designed for English speakers learning Chinese who wish to learn using Taiwan/ROC zhuyin (注音符號) and Taiwan/ROC stroke order (筆順).

Anki Chinese accepts a [vocabulary list in YAML format](#usage) and outputs:

- A CSV for importing into Anki using a specific [Anki note type](#anki-note-type)
- PNG images of the Taiwan stroke order

The Taiwan stroke order is downloaded from <https://stroke-order.learningweb.moe.edu.tw/teaching_resources.do?lang=zh_TW>.

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

## Requirements

- Docker: This application has been dockerized to minimize required native dependencies.
- Internet connection: To download stroke order images.

## Usage

To generate a CSV to import into Anki, along with accompanying images:

1. Put your vocab file into the `./data` directory
2. Build the docker image: `docker compose build`
3. Run the script: `docker compose run --rm app poetry run csv data/VOCAB_FILE [options]`

<details>
<summary>Breakdown of the docker command</summary>
This is a complex docker command. Here's what it's doing:
- `docker compose run`: Runs a [one-time command](https://docs.docker.com/engine/reference/commandline/compose_run/).
- `--rm`: Removes the container after it exits. This means you don't have to do any cleanup.
- `app`: The service that docker compose will run. Matches a named service in docker-compose.yml.
- `poetry`: The command that should be run inside the container. In our case, it's the [poetry](https://python-poetry.org/docs/) package manager.
- `run`: Tells poetry what to do. In this case run a script.
- `csv`: Tells poetry which script to run. Matches a named script in the `[tool.poetry.scripts]` section of `./app/pyproject.toml`.
- `data/VOCAB_FILE [options]`: The arguments and options that the csv script accepts.
</details>

`VOCAB_FILE` should be a YAML-formatted file of vocabulary words to be turned into flash cards. The expected format is:

```yaml
十二月底: The end of December
雨: Rain
傘: Umbrella
颱風: Typhoon
```

This will output:

```
data/
├── import_into_anki.csv
└── images/
    └── stroke_order/
        └── *.png
```

### Options

Run `docker compose run --rm app poetry run csv --help` to see the options.

* `--char_file char_file.txt`: Pass in a text file that contains a list of characters that you have already imported into Anki.
    * Note that the docker-compose.yml is configured to bind mount the `./data` directory, so if you want to use this option, put your character file in the data directory and use the flag like so: `--char_file data/char_file.txt`.
    * For example: `接臺灣歡迎陳華文張這姓叫請問謝不客氣喝茶`.
    * If a character exists in `char_file.txt`, then Anki Chinese will not generate new single character cards in order to reduce duplicates in Anki.
    * If a character file is NOT provided, Anki Chinese will still prevent duplicates from WITHIN the same vocab file. For example: `臺灣: Taiwan` and `臺北: Taipei` will generate only single characters 3 characters (`臺灣北`), not 4.
    * Anki Chinese will update the character file with any new characters provided in the vocab file. This creates a handy side effect where you can see the total number of unique characters you've studied.
* `--no-update-chars`: If you use the `--char_file` option, you can use the `--no-update-chars` option to tell Anki Chinese to only read from the character file to prevent duplicates, but Anki Chinese will not update it with any new characters.
* `--force-update-images`: Using this flag will tell Anki Chinese to not to update any existing images. The default behavior is to NOT generate a new image if a file with the same name already exists).
* `-t, --tags`: All the tags passed in will be applied to each row in the CSV. This means that separating each book or each chapter into a separate yaml file is recommended. You can then pass in "ch1" or "book1" tags for each yaml.
    * Multiple tags can be passed in using this option multiple times. Example: `-t "tag1" -t "tag2" -t "tag3"`
    * Note that Anki cannot support tags that contain spaces.

### Importing into Anki

0. Make sure the appropriate note type and card types have been created in Anki (see above).
1. Copy all the images in `./data/images/stroke_order` to Anki's `collection.media` folder.
    * See https://apps.ankiweb.net/docs/manual.html#importing-media for instructions on how to locate the folder. Do not create subfolders in `collection.media`.
2. Import the `anki_import.csv` file into Anki.
    * See https://apps.ankiweb.net/docs/manual.html#importing for more info. Make sure to set the last field to "Tags".

You may notice that not all character/zhuyin/pinyin fields are filled out in `anki_import.csv`. That's ok. Anki knows to ignore those.
