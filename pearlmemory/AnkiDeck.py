from typing import List

import genanki
import uuid

from pearlmemory.AnkiCard import AnkiCard


class AnkiDeck(genanki.Deck):
    deck_id = str
    anki_cards = List[AnkiCard]

    def __init__(self, title: str, anki_cards: List[AnkiCard]):
        super().__init__(name=title, deck_id=str(self.__create_id()))
        self.anki_cards = anki_cards

    def build_media_lib(self):
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

    def create_media_library(self):
        return

    def __str__(self):
        return print(f"<AnkiDeck {self.name} {self.deck_id} {len(self.anki_cards)}>")
