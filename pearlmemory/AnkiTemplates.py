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
        "name": "German to English",
        # Front template format
        "qfmt": """
{{Wort_DE}}{{Audio_Wort}}
        """,
        # Back template Format
        "afmt": """
{{#Artikel}}{{Artikel}}{{/Artikel}}
{{Wort_DE}}
{{#Plural}}{{Plural}}{{/Plural}}
{{Audio_Wort}}

<div style='font-family: Arial; font-size: 16px;'>
{{#Verbformen}}<br>Verbformen: {{Verbformen}}{{/Verbformen}}
{{#Hinweis}}<br>Hinweis: {{Hinweis}}{{/Hinweis}}
</div>

<hr id=answer>

{{Wort_EN}}

<hr>

<div style="display:none">[sound:_LongSilence.mp3]</div>

{{#Satz1_DE}}
<div style='font-family: Arial; font-size: 16px;'>{{Satz1_DE}}{{Audio_S1}}</div>
<div style='font-family: Arial; font-size: 14px;'>{{hint:Satz1_EN}}</div><br>
{{/Satz1_DE}}

{{#Satz2_DE}}
<div style='font-family: Arial; font-size: 16px;'>{{Satz2_DE}}{{Audio_S2}}</div>
<div style='font-family: Arial; font-size: 14px;'>{{hint:Satz2_EN}}</div><br>
{{/Satz2_DE}}

{{#Satz3_DE}}
<div style='font-family: Arial; font-size: 16px;'>{{Satz3_DE}}{{Audio_S3}}</div>
<div style='font-family: Arial; font-size: 14px;'>{{hint:Satz3_EN}}</div><br>
{{/Satz3_DE}}

{{#Satz4_DE}}
<div style='font-family: Arial; font-size: 16px;'>{{Satz4_DE}}{{Audio_S4}}</div>
<div style='font-family: Arial; font-size: 14px;'>{{hint:Satz4_EN}}</div><br>
{{/Satz4_DE}}
        """
    },
]
