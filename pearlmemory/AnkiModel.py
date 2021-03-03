import genanki
import uuid

from pearlmemory import AnkiTemplates


class AnkiModel(genanki.Model):
    model_id = str
    fields = [
        {"name": "Deutsch Wort oder Ausdruck"},
        {"name": "English Word or Phrase"},
        {"name": "Bild"},
        {"name": "Audio"},
    ]
    templates = AnkiTemplates.MODEL_TEMPLATES
    css = ""

    def __init__(self):
        super(AnkiModel, self).__init__(name="Deutsch Wort oder Ausdruck", model_id=str(self.__create_id()))

    @staticmethod
    def __create_id() -> int:
        """
        Creates a maybe unique ID for the Anki ID.

        Returns: The first five digits of a UUID4 integer.
        """
        return int(str(uuid.uuid4().int)[:5])

    def __str__(self):
        return f"<AnkiModel {self.deck_id}>"
