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
import os

import uuid
from pathlib import Path


class AzConf:
    AZURE_SPEECH_KEY = os.environ.get("AZ-SPEECH-KEY")
    AZURE_TRANSLATE_KEY = os.environ.get("AZ-TRANS-KEY")
    AZURE_SSML_CONF = Path("ssml.xml")
    BING_SEARCH_KEY = os.environ.get("AZ-SEARCH-KEY")

    VOICE_SUBSCRIPTION_REGION = (
        os.environ.get("AZ-SUB-REGION") if os.environ.get("AZ-SUB-REGION") is not None else "australiaeast"
    )

    TRANSLATE_SUBSCRIPTION_REGION = (
        os.environ.get("AZ-TRANS-REGION") if os.environ.get("AZ-TRANS-REGION") is not None else "australiaeast"
    )

    IMAGE_API_URL = "https://api.bing.microsoft.com/v7.0/images/search"
    TRANSLATE_API_URL = "https://api.cognitive.microsofttranslator.com/translate?api-version=3.0&from={}&to={}"

    ACCEPTED_IMG_FORMATS = ['jpeg', 'jpg', 'png', 'gif']

    AZURE_HEADERS = {
        'Ocp-Apim-Subscription-Key': AZURE_TRANSLATE_KEY,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4()),
        'Ocp-Apim-Subscription-Region': TRANSLATE_SUBSCRIPTION_REGION
    }

    BING_HEADERS = {"Ocp-Apim-Subscription-Key": f"{BING_SEARCH_KEY}"}
    BING_PARAMS = {
        "mkt": "de-DE",
        "imageType": "Photo",
        "count": "3"
    }