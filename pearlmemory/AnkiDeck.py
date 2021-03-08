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
from typing import List

import genanki
import uuid

from pearlmemory.AnkiCard import AnkiCard


class AnkiDeck(genanki.Deck):
    deck_id = str
    anki_cards = List[AnkiCard]

    def __init__(self, title: str, anki_cards: List[AnkiCard]):
        super().__init__(name=title, deck_id=self.__create_id())
        self.anki_cards = anki_cards

    def __build_media_lib(self):
        media = list()
        for card in self.anki_cards:
            media.append(card.image)
            media.append(card.audio)

        return media

    @staticmethod
    def __create_id() -> int:
        """
        Creates a maybe unique ID for the Anki ID.

        Returns: The first five digits of a UUID4 integer.
        """
        return int(str(uuid.uuid4().int)[:5])

    def package_deck(self, anki_deck: genanki.Deck) -> genanki.Package:
        package = genanki.Package(anki_deck)
        package.media_files = self.__build_media_lib()

        return package

    def create_notes(self, model: genanki.Model):
        notes = list()
        for card in self.anki_cards:
            notes.append(genanki.Note(
                model=model,
                fields=[card.translation_dict["de"],
                        card.translation_dict["en"],
                        f'<img src="{card.image.name}">',
                        f"[sound:{card.audio.name}]"]))

        return notes

    def __str__(self):
        return print(f"<AnkiDeck {self.name} {self.deck_id} {len(self.anki_cards)}>")
