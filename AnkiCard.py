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
import logging
import os

import genanki
import uuid

import langdetect
import requests
from azure.cognitiveservices.speech import ResultFuture
from azure.cognitiveservices.speech.audio import AudioOutputConfig
import azure.cognitiveservices.speech as speechsdk


class AzConf:
    AZURE_SPEECH_KEY = os.environ.get("AZ-SPEECH-KEY")
    AZURE_TRANSLATE_KEY = os.environ.get("AZ-TRANS-KEY")
    BING_SEARCH_KEY = os.environ.get("AZ-SEARCH-KEY")

    VOICE_SUBSCRIPTION_REGION = os.environ.get("AZ-SUB-REGION")
    TRANSLATE_SUBSCRIPTION_REGION = os.environ.get("AZ-TRANS-REGION")

    IMAGE_API_URL = "https://api.bing.microsoft.com/v7.0/images/search"
    TRANSLATE_API_URL = "https://api.cognitive.microsofttranslator.com/translate?api-version=3.0&from={}&to={}"

    ACCEPTED_IMG_FORMATS = ['jpeg', 'jpg', 'png', 'gif']

    AZURE_HEADERS = {
        'Ocp-Apim-Subscription-Key': AZURE_TRANSLATE_KEY,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4()),
        'Ocp-Apim-Subscription-Region': TRANSLATE_SUBSCRIPTION_REGION
    }

    BING_HEADERS = {"Ocp-Apim-Subscription-Key": "{}"}
    BING_PARAMS = {
        'mkt': "{}",
        'imageType': "{}",
        'count': "{}"
    }


class AnkiCard:
    config = AzConf
    translation_endpoint = str
    translation = dict()
    audio = ResultFuture
    image = str

    def __init__(self, az_config: AzConf, word: str ):
        self.word = word
        self.translation_endpoint = self.__detect_language()
        self.audio = self.__voice_translate()
        self.image = self.__image_download()
        self.config = az_config

    def __detect_language(self, word):
        if langdetect.detect(word) == 'en':
            translate_api_url = self.config.TRANSLATE_API_URL.format('en', 'de')
        elif langdetect.detect(word) == 'de':
            translate_api_url = self.config.TRANSLATE_API_URL.format('de', 'en')
        else:
            # If we're unsure default to German? maybe not the most ideal outcome though
            translate_api_url = self.config.TRANSLATE_API_URL.format('de', 'en')
        return translate_api_url

    def __translate_word(self):
        return requests.post(
            url=self.translation_endpoint,
            headers=self.config.AZURE_HEADERS,
            json=[{"text": f"{self.word}"}]
        ).json()[0]['translations'][0]['text']

    def __voice_translate(self):
        filename = f"{self.word}.wav"
        speech_config = speechsdk.SpeechConfig(
            subscription=self.config.AZURE_SPEECH_KEY,
            region=self.config.VOICE_SUBSCRIPTION_REGION
        )
        audio_config = AudioOutputConfig(filename=filename)

        speech_synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=speech_config,
            audio_config=audio_config
        )
        ssml_string = open("ssml.xml", "r").read().format(search)

        result = speech_synthesizer.speak_ssml_async(ssml_string).get()

        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            logging.info(f"Speech synthesized to speaker for text {search}.")
            return filename
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            logging.error(f"Speech synthesis canceled: {cancellation_details.reason}.")
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                if cancellation_details.error_details:
                    logging.error(f"Error details: {cancellation_details.error_details}.")
            logging.error("Did you update the subscription info?")

    def __image_download(self):
        return "Image"

    def create_card(self):
        return "Card"


class AnkiDeck(genanki.Deck):
    deck_id = str
    model_id = str

    def __init__(self, title: str):
        super().__init__(name=title, deck_id=str(self.__create_id()))

    @staticmethod
    def __create_id() -> int:
        """
        Creates a maybe unique ID for the Anki ID.

        Returns: The first five digits of a UUID4 integer.
        """
        return int(str(uuid.uuid4().int)[:5])

    def __str__(self):
        return f"<AnkiDeck {self.name} {self.deck_id}>"
