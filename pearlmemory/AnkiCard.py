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
import shutil
import sys
from pathlib import Path

import PIL
import azure.cognitiveservices.speech as speechsdk
import langdetect
import requests
from PIL import Image
from azure.cognitiveservices.speech.audio import AudioOutputConfig
from bs4 import BeautifulSoup
from resizeimage import resizeimage, imageexceptions
from slugify import slugify

from pearlmemory import Config


def init_detector_factory():
    # instantiate the DetectorFactory
    factory = langdetect.detector_factory.DetectorFactory()
    factory.load_profile(langdetect.detector_factory.PROFILES_DIRECTORY)
    detector = factory.create()
    detector.set_prior_map({"en": 0.5, "de": 0.5})

    return detector


class AnkiCard:
    OUTPUT_DIRECTORY = Path("./tmp").absolute()
    CONFIG = Config.Config()

    def __init__(self, word: str):
        self.word = word
        self.translation_dict = self.__translate_word(word)
        self.audio = self.__voice_translate(self.translation_dict["de"])
        self.image = self.__download_word_image()
        self.satze = self.__get_example_satze()
        self.satze_audio = self.__generate_satze_audio()

    def __translate_word(self, word):
        translation_dict = {"en": "", "de": "", "artikle": ""}

        detector_factory = init_detector_factory()
        detector_factory.append(word)
        logging.info(f"Word: {word} has been identified as: {detector_factory.detect()}")
        if detector_factory.detect() == 'en':
            translate_api_url = self.CONFIG.TRANSLATE_API_URL.format('en', 'de')
            translation_dict["en"] = word
            translation_dict["de"] = self.__request_translation(translate_api_url)
        elif detector_factory.detect() == 'de':
            translate_api_url = self.CONFIG.TRANSLATE_API_URL.format('de', 'en')
            translation_dict["de"] = word
            translation_dict["en"] = self.__request_translation(translate_api_url)
        else:
            translate_api_url = self.CONFIG.TRANSLATE_API_URL.format('de', 'en')
            translation_dict["de"] = word
            translation_dict["en"] = self.__request_translation(translate_api_url)

        translation_dict["artikle"] = self.__identify_article(translation_dict["de"])
        return translation_dict

    @staticmethod
    def __identify_article(word: str):
        de_articles = ["die", "der", "das"]
        if word.startswith(tuple(de_articles)):
            return word.split(" ")[0]

    def __request_translation(self, translation_url: str) -> json:
        if "microsoft" in translation_url:
            return self.__request_azure_translation(translation_url)
        else:
            return self.__request_google_translation(translation_url)

    def __request_google_translation(self, translation_url: str) -> json:
        return requests.post(
            url=f"{translation_url}&q=[{self.word}]",
        ).json()["data"]["translations"][0]["translatedText"].strip("[]")

    def __request_azure_translation(self, translation_url: str) -> json:
        return requests.post(
            url=translation_url,
            headers=self.CONFIG.AZURE_HEADERS,
            json=[{"text": f"{self.word}"}]
        ).json()[0]['translations'][0]['text']

    def __generate_satze_audio(self):
        sentence_audio = list()
        german_sentences = self.satze[1::2]
        for sentence in german_sentences:
            sentence_audio.append(self.__voice_translate(sentence))

        return sentence_audio

    def __voice_translate(self, phrase: str) -> str:
        # Define the path to tmp/sound
        audio_path = self.OUTPUT_DIRECTORY / "sound"
        # Generate the wav name using a slugified version of the German word.
        wav_name = f"{slugify(phrase, separator='_')}.wav"
        # Join all the path ingredients together
        audio_file = audio_path / wav_name

        # Convert to a string because AudioOutputConfig doesn't like the libpath representation.
        audio_path_str = audio_file.absolute()

        # AudioOutputConfig specifies the parent directory must already exist so we ensure that `/tmp/sound` exists.
        if not audio_path.exists():
            os.makedirs(audio_path)

        try:
            speech_config = speechsdk.SpeechConfig(
                subscription=self.CONFIG.AZURE_SPEECH_KEY,
                region=self.CONFIG.VOICE_SUBSCRIPTION_REGION
            )
            audio_config = AudioOutputConfig(filename=str(audio_path_str))
        except NameError:
            # Because of the `audio_path` check we should never hit this exception unless the user has deleted the tmp
            # folder between line 113 and now.
            logging.critical(f"'{audio_path}' does not exist. Unable to create '{wav_name}'.")
            sys.exit(errno.ENOENT)
        except ValueError:
            logging.critical("Subscription key must be given. Ensure 'AZURE_SPEECH_KEY' environment variable is set.")
            sys.exit(errno.EPERM)

        speech_synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=speech_config,
            audio_config=audio_config
        )

        ssml_string = self.CONFIG.AZURE_SSML_CONF.open().read().format(phrase)

        result = speech_synthesizer.speak_ssml_async(ssml_string).get()

        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            logging.info(f"Speech synthesised for text {phrase}.")
            return audio_path_str
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            logging.error(f"Speech synthesis canceled: {cancellation_details.reason}.")
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                if cancellation_details.error_details:
                    logging.error(f"Error details: {cancellation_details.error_details}.")
            logging.error("Did you update the subscription info?")

    def __download_word_image(self):
        params = self.CONFIG.BING_PARAMS
        params["q"] = self.translation_dict["de"] + f" language:de loc:de"

        response = requests.get(
            url=self.CONFIG.AZURE_IMAGE_API_URL,
            headers=self.CONFIG.BING_HEADERS,
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
        try:
            img_extension = mimetypes.guess_extension(img_mime_type[0], strict=True)
        except AttributeError:
            img_data = Path("./templates/missing.png")
            img_extension = ".png"

        img_path = self.OUTPUT_DIRECTORY / "imgs"
        img_name = f"{slugify(self.translation_dict['de'], separator='_')}{img_extension}"

        img_file = img_path / img_name

        if not img_path.exists():
            os.makedirs(img_path)

        with open(img_file, "wb") as f:
            logging.info(f"Downloading: {img_name}")
            try:
                f.write(img_data.content)
            except AttributeError:
                shutil.copyfile(img_data, img_file)
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

    def __get_example_satze(self):
        req = requests.get(f"https://context.reverso.net/translation/english-german/{self.translation_dict['en']}",
                           headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(req.text, 'lxml')
        sentences = [x.text.strip() for x in soup.find_all('span', {'class': 'text'}) if '\n' in x.text]
        return sentences[:8]
