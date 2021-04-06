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
import errno
import json
import logging
import mimetypes
import os
import sys
from pathlib import Path

import PIL
import azure.cognitiveservices.speech as speechsdk
import genanki
import langdetect
import requests
from PIL import Image
from azure.cognitiveservices.speech.audio import AudioOutputConfig
from resizeimage import resizeimage, imageexceptions
from slugify import slugify

from pearlmemory import AzConfig


class AnkiCard:
    OUTPUT_DIRECTORY = Path("./tmp").absolute()
    AZ_CONF = AzConfig.AzConf()
    translation_dict = {"en": "", "de": ""}

    def __init__(self, word: str):
        self.word = word
        self.translation_endpoint = self.__detect_language(word)
        self.audio = self.__voice_translate()
        self.image = self.__download_word_image()

    def __detect_language(self, word) -> str:
        if langdetect.detect(word) == 'en':
            translate_api_url = self.AZ_CONF.TRANSLATE_API_URL.format('en', 'de')
            self.translation_dict["en"] = word
        elif langdetect.detect(word) == 'de':
            translate_api_url = self.AZ_CONF.TRANSLATE_API_URL.format('de', 'en')
            self.translation_dict["de"] = word
        else:
            translate_api_url = self.AZ_CONF.TRANSLATE_API_URL.format('de', 'en')
            self.translation_dict["de"] = word
        return translate_api_url

    def __translate_word(self) -> json:
        return requests.post(
            url=self.translation_endpoint,
            headers=self.AZ_CONF.AZURE_HEADERS,
            json=[{"text": f"{self.word}"}]
        ).json()[0]['translations'][0]['text']

    def __voice_translate(self) -> str:
        # Define the path to tmp/sound
        audio_path = self.OUTPUT_DIRECTORY / "sound"
        # Generate the wav name using a slugified version of the German word.
        wav_name = f"{slugify(self.translation_dict['de'], separator='_')}.wav"
        # Join all the path ingredients together
        audio_file = audio_path / wav_name

        # Convert to a string because AudioOutputConfig doesn't like the libpath representation.
        audio_path_str = audio_file.absolute()

        # AudioOutputConfig specifies the parent directory must already exist so we ensure that `/tmp/sound` exists.
        if not audio_path.exists():
            os.makedirs(audio_path)

        try:
            speech_config = speechsdk.SpeechConfig(
                subscription=self.AZ_CONF.AZURE_SPEECH_KEY,
                region=self.AZ_CONF.VOICE_SUBSCRIPTION_REGION
            )
        except ValueError:
            logging.critical("Subscription key must be given. Ensure 'AZURE_SPEECH_KEY' environment variable is set.")
            sys.exit(errno.EPERM)
        try:
            audio_config = AudioOutputConfig(filename=str(audio_path_str))
        except NameError:
            # Because of the `audio_path` check we should never hit this exception unless the user has deleted the tmp
            # folder between line 113 and now.
            logging.critical(f"'{audio_path}' does not exist. Unable to create '{wav_name}'.")
            sys.exit(errno.ENOENT)

        speech_synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=speech_config,
            audio_config=audio_config
        )

        ssml_string = self.AZ_CONF.AZURE_SSML_CONF.open().read().format(self.translation_dict['de'])

        result = speech_synthesizer.speak_ssml_async(ssml_string).get()

        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            logging.info(f"Speech synthesised for text {self.translation_dict['de']}.")
            return audio_path_str
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            logging.error(f"Speech synthesis canceled: {cancellation_details.reason}.")
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                if cancellation_details.error_details:
                    logging.error(f"Error details: {cancellation_details.error_details}.")
            logging.error("Did you update the subscription info?")

    def __download_word_image(self):
        params = self.AZ_CONF.BING_PARAMS
        params["q"] = self.translation_dict["de"] + f" language:de loc:de"

        response = requests.get(
            url=self.AZ_CONF.IMAGE_API_URL,
            headers=self.AZ_CONF.BING_HEADERS,
            params=params
        )
        response.raise_for_status()

        search_results = response.json()

        return self.__download_image(search_results['value'][0]['contentUrl'])

    def __download_image(self, url: str):
        img_data = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        img_data.raise_for_status()

        # Identify MIME type and then set the extension type
        img_mime_type = mimetypes.guess_type(url.split("?")[0], strict=True)
        img_extension = mimetypes.guess_extension(img_mime_type[0], strict=True)

        img_path = self.OUTPUT_DIRECTORY / "imgs"
        img_name = f"{slugify(self.translation_dict['de'], separator='_')}{img_extension}"

        img_file = img_path / img_name

        if not img_path.exists():
            os.makedirs(img_path)

        with open(img_file, "wb") as f:
            logging.info(f"Downloading: {img_name}")
            f.write(img_data.content)
            self.__resize_image(img_file)

        return img_file

    @staticmethod
    def __resize_image(img_path: str):
        with open(img_path, 'r+b') as f:
            try:
                with Image.open(f) as image:
                    logging.info(f"Resizing image: {img_path}")
                    try:
                        cover = resizeimage.resize_cover(image, [600, 800])
                    except imageexceptions.ImageSizeError as image_err:
                        logging.warning(image_err.message)
                        img = Image.open(f)
                        img.save(img_path)
                    else:
                        cover.save(img_path, image.format)
            except PIL.UnidentifiedImageError:
                logging.warning("Cannot identify image file, deleting")
