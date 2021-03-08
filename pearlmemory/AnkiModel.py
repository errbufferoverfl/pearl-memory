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
from pathlib import Path

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
    css = "templates/anki.css"

    def __init__(self):
        super(AnkiModel, self).__init__(name="Simple Vocabulary",
                                        model_id=self.__create_id(),
                                        fields=self.fields,
                                        templates=self.templates,
                                        css=self.css)

    def __str__(self):
        return f"<AnkiModel {self.model_id}>"

    @staticmethod
    def __create_id() -> int:
        """
        Creates a maybe unique ID for the Anki ID.

        Returns: The first five digits of a UUID4 integer.
        """
        return int(str(uuid.uuid4().int)[:5])