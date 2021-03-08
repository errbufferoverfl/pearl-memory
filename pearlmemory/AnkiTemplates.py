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

MODEL_TEMPLATES = [
    {
        "name": "English to German",
        # Front template format
        "qfmt": """
        {{#Bild}}<div>{{Bild}}</div>{{/Bild}}
        {{#English Word or Phrase}}
        <div style='font-family: Arial; font-size: 14px;'>
            {{English Word or Phrase}}
        </div>
        {{/English Word or Phrase}}
        """,
        # Back template Format
        "afmt": """
        {{#Deutsch Wort oder Ausdruck}}
        <div style='font-family: Arial; font-size: 14px;'>
            {{Deutsch Wort oder Ausdruck}}
        </div>{{/Deutsch Wort oder Ausdruck}}
        {{#Audio}}
        <div style='font-family: Arial; font-size: 14px;'>
            {{Audio}}
        </div>
        {{/Audio}}
        """
    },
    {
        "name": "German to English",
        # Front template format
        "qfmt": """
        {{#Bild}}<div>{{Bild}}</div>{{/Bild}}
        {{#English Word or Phrase}}
        <div style='font-family: Arial; font-size: 14px;'>
            {{English Word or Phrase}}
        </div>
        {{/English Word or Phrase}}
        """,
        # Back template Format
        "afmt": """
        {{#Deutsch Wort oder Ausdruck}}
        <div style='font-family: Arial; font-size: 14px;'>
            {{Deutsch Wort oder Ausdruck}}
        </div>{{/Deutsch Wort oder Ausdruck}}
        {{#Audio}}
        <div style='font-family: Arial; font-size: 14px;'>
            {{Audio}}
        </div>
        {{/Audio}}
        """
    },
    {
        "name": "Spelling",
        # Front template format
        "qfmt": """
        <div>Kannst du es buchstabieren?</div>
        {{#English Word or Phrase}}
        <div style='font-family: Arial; font-size: 14px;'>
            {{English Word or Phrase}}
        </div>
        {{/English Word or Phrase}}
        """,
        # Back template Format
        "afmt": """
        {{#Deutsch Wort oder Ausdruck}}
        <div style='font-family: Arial; font-size: 14px;'>
            {{Deutsch Wort oder Ausdruck}}
        </div>{{/Deutsch Wort oder Ausdruck}}
        {{#Audio}}
        <div style='font-family: Arial; font-size: 14px;'>
            {{Audio}}
        </div>
        {{/Audio}}
        """
    },
]
