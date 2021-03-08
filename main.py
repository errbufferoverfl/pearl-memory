#!/usr/bin/env pipenv run python
# -*- coding: utf-8 -*-
"""
pearlmemory is a variation of french-genanki-jupyter made for German
learners.

Copyright (C) 2020  errbufferoverfl.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import csv
import errno
import logging
import os
import shutil
import sys
from pathlib import Path

import genanki
from slugify import slugify

from pearlmemory.AnkiCard import AnkiCard
from pearlmemory.AnkiDeck import AnkiDeck
from pearlmemory.AnkiModel import AnkiModel

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

    # import the word list
    words = import_translate_list()

    anki_model = AnkiModel()

    anki_cards = list()
    for word in words:
        anki_cards.append(AnkiCard(word=word))

    deck = AnkiDeck(title=deck_name, anki_cards=anki_cards)
    deck_notes = deck.create_notes(anki_model)

    for note in deck_notes:
        deck.add_note(note)

    package = deck.package_deck(deck)

    package.write_to_file('package.apkg')

    shutil.rmtree("./tmp/imgs")
    shutil.rmtree("./tmp/sound")
