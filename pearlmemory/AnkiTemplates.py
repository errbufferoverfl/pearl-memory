from textwrap import dedent

MODEL_TEMPLATES = [
    {
        "name": "English to German",
        # Front template format
        "qfmt": """
        <div>{{Bild}}</div>
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
        <div>{{Bild}}</div>
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
