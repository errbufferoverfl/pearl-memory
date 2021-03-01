#!/usr/bin/env pipenv run python
# -*- coding: utf-8 -*-
import csv
import errno
import logging
import os
import sys
from pathlib import Path

import genanki
from slugify import slugify

from pearlmemory.AnkiCard import AzConf, AnkiDeck, AnkiCard

SEARCH_CVS_FILENAME = Path("anki_search.csv")


def import_translate_list() -> list:
    translation_list = list()
    try:
        with SEARCH_CVS_FILENAME.open(encoding="utf-8") as stream:
            reader = csv.reader(stream)
            for row in reader:
                translation_list.append(row[0])
    except FileNotFoundError:
        logging.critical(f"Unable to locate '{SEARCH_CVS_FILENAME}'. Check it exists.")
        sys.exit(errno.EIO)
    except TypeError:
        logging.critical(f"Unable to load '{SEARCH_CVS_FILENAME}'. Check it is populated.")
        sys.exit(errno.EIO)
    else:
        return translation_list


def package_deck(new_deck: genanki.Deck, media: list) -> genanki.Package:
    de_package = genanki.Package(new_deck)
    de_package.media_files = media

    return de_package


def clean_up() -> None:
    os.rmdir(Path("tmp"))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    deck_name = input("Please enter your deck name: ")
    deck_name = slugify(deck_name, separator=" ")

    az_config = AzConf()
    deck = AnkiDeck(title=deck_name)

    # import the word list
    words = import_translate_list()

    anki_model = genanki.Model(
        model_id=

    )

    for word in words:
        card = AnkiCard(az_config=az_config, word=word)
        card.create_card()