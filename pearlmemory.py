#!/usr/bin/env pipenv run python
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

import csv
import logging
import os
import re
import uuid
from pathlib import Path
from textwrap import dedent
from typing import Dict, Tuple

import PIL
import genanki
import requests
import ruamel.yaml
from PIL import Image
from bs4 import BeautifulSoup as bs
from resizeimage import resizeimage

search_csv_filename = "anki_search.csv"
csv_file_encoding = 'mac_roman'
genanki_id_yaml = "genanki_ids.yaml"
bing_settings_yaml_filename = 'bing_settings.yaml'
resize_image_x, resize_image_y = 400, 300
collins = "https://www.collinsdictionary.com/dictionary/german-english/{}"

# index of Bing image we use
image_idx = 0


def create_id() -> int:
    return int(str(uuid.uuid4().int)[:5])


def download(url, filename) -> None:
    with open(filename, 'wb') as f:
        logging.info(f'Downloading: {filename}')
        img_data = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        img_data.raise_for_status()
        f.write(img_data.content)


def bing_setup() -> Tuple[Dict, Dict, Dict]:
    settings = {}
    with open(bing_settings_yaml_filename, 'r') as stream:
        try:
            settings = ruamel.yaml.load(stream, Loader=ruamel.yaml.Loader)
            logging.info('Loaded Bing API settings.')
        except ruamel.yaml.YAMLError as exc:
            logging.critical(exc)
        else:
            headers = {"Ocp-Apim-Subscription-Key": settings['subscription_key']}
            params = {
                'setLang': settings['setLang'],
                'mkt': settings['mkt'],
                'imageType': settings['imageType'],
                'count': settings['count']
            }

            return headers, params, settings


def load_ids() -> Dict:
    ids = dict()
    with open(genanki_id_yaml, 'r') as stream:
        try:
            ids = ruamel.yaml.load(stream, Loader=ruamel.yaml.Loader)
        except ruamel.yaml.YAMLError as exc:
            logging.critical(exc)
    return ids


def load_search_list() -> list:
    search_list = []
    with open(search_csv_filename, encoding=csv_file_encoding) as f:
        reader = csv.reader(f)
        for row in reader:
            # assuming no header in csv file
            search_list.append(row[0])
    return search_list


def write_genaki() -> None:
    if not Path(genanki_id_yaml).is_file():
        with open(genanki_id_yaml, 'wt') as file:
            file.write('deck_id: ' + str(create_id()) + '\n')
            file.write('model_id: ' + str(create_id()) + '\n')


def get_search_term_data(search_list: list, request_headers: dict, request_parameters: dict, settings: dict) -> list:
    results = []
    for search in search_list:
        logging.info('Processing: ' + search)
        result = {'word': search}

        # process collins search
        collins_query = collins.format(search)
        result['collins_query'] = collins_query
        collins_req = requests.get(collins_query, headers={'User-Agent': 'Mozilla/5.0'})
        collins_data = collins_req.text
        collins_soup = bs(collins_data, "html.parser")

        # get definition
        result['definition'] = collins_soup.find('span', attrs={'class': 'cit type-translation quote'}).text.strip()

        # get part of speech
        result['pos'] = collins_soup.find('span',
                                          attrs={'class': 'pos'}).text.strip()

        # create article for nouns
        regex = re.compile(r"(masculine|feminine|neuter)\s(noun)")
        match = regex.match(result['pos'])
        if match is not None:
            if match.group(0) == "feminine":
                result['article'] = "die"
            elif match.group(1) == "masculine":
                result['article'] = "der"
            elif match.group(2) == "neuter":
                result['article'] = "das"

        try:
            # get IPA
            result['ipa'] = collins_soup.find('span', attrs={'class': 'form pron type-'}).text.strip()
        except AttributeError:
            logging.error(f"No IPA found, skipping: {search}")
            continue
        else:
            # get audio file url
            sound_attrs = {'class': " ".join(['hwd_sound',
                                              'sound',
                                              'audio_play_button',
                                              'icon-volume-up',
                                              'ptr'])}

            sound_element = collins_soup.find('a', attrs=sound_attrs)
            try:
                result['sound_url'] = sound_element.get('data-src-mp3')
            except AttributeError:
                logging.error(f"No 'data-src-mp3' element found, skipping: {search}")
                continue
            else:
                # download files
                result['audio_file'] = search + '_pronounce.mp3'

                # if file doesn't exist locally then save it
                if not Path(result['audio_file']).is_file():
                    download(result['sound_url'], result['audio_file'])
                else:
                    logging.warning("File exists, skipping: " + result['audio_file'])

        # process bing image
        bing_advanced_query = f" language:{settings['language']} loc:{settings['loc']}"
        request_parameters['q'] = search + bing_advanced_query
        response = requests.get(settings['image_api_url'], headers=request_headers, params=request_parameters)
        response.raise_for_status()
        search_results = response.json()

        result['bing_results_json'] = search_results
        result['image_url'] = search_results['value'][image_idx]['contentUrl']
        result['image_page_url'] = search_results['value'][image_idx]['hostPageUrl']

        # get end of url after last /
        original_image_filename = result['image_url'].rsplit('/', 1)[-1]
        original_image_ext = original_image_filename.rsplit('.', 1)[-1]

        result['image_file_original'] = original_image_filename.split('?')[0]
        result['image_file'] = search + "." + original_image_ext

        # download image file
        if not Path(result['image_file']).is_file():
            try:
                download(result['image_url'], result['image_file'])
            except (requests.HTTPError, requests.exceptions.SSLError):
                logging.warning("Couldn't download image, skipping")
                result['image_file'] = None
        else:
            logging.warning("File exists, skipping: " + result['image_file'])

        # resize image file
        resized_filename = search + "_resized." + original_image_ext

        if Path(result['image_file']).is_file() and not Path(resized_filename).is_file():
            with open(result['image_file'], 'r+b') as f:
                try:
                    with Image.open(f) as image:
                        logging.info("Resizing image: " + result['image_file'])
                        resized_filename = search + "_resized." + original_image_ext
                        cover = resizeimage.resize_cover(image, [resize_image_x, resize_image_y])
                        cover.save(resized_filename, image.format)
                except PIL.UnidentifiedImageError:
                    logging.warning("Cannot identify image file, deleting")
                    os.remove(result['image_file'])
        result['image_file_resized'] = resized_filename

        results.append(result)
    logging.info("Completed Queries!")
    return results


def create_anki_model(ids: dict) -> genanki.Model:
    # Create Anki model
    my_model = genanki.Model(
        int(ids['model_id']),
        'French - 5k (Genaki)',
        fields=[
            {'name': 'Word or Phrase'},
            {'name': 'Article'},
            {'name': 'Part of Speech'},
            {'name': 'Definition'},
            {'name': 'Picture'},
            {'name': 'Audio'},
            {'name': 'IPA'},
            {'name': 'Mnemonic'},
            {'name': 'Source'}
        ],
        templates=[
            {
                'name': 'Picture2Word',
                'qfmt': "<div style='font-family: Arial; font-size: 20px;'>{{Picture}}</div>",
                'afmt': dedent("""\
                    <div style='font-family: Arial; font-size: 20px;'>{{Audio}}</div>
                    <div style='font-family: Arial; font-size: 20px;'>{{#Article}}{{Article}}{{/Article}}&nbsp;{{Word or Phrase}}</div>
                    <div style='font-family: Arial; font-size: 20px;'>{{Part of Speech}}</div>
                    <div style='font-family: Arial; font-size: 20px;'>{{Mnemonic}}</div>
                    {{#Source}}<div style='font-family: Arial; font-size: 20px;'>{{Source}}</div>{{/Source}}
                    """),
            },
            {
                'name': 'Word2Picture',
                'qfmt': dedent("""\
                  <div style='font-family: Arial; font-size: 20px;'>{{Audio}}</div>
                  <div style='font-family: Arial; font-size: 20px;'>{{#Article}}{{Article}}{{/Article}}&nbsp;{{Word or Phrase}}</div>
                  <div style='font-family: Arial; font-size: 20px;'>{{Part of Speech}}</div>
                      """),
                'afmt': dedent("""\
                    {{#Picture}}<div style='font-family: Arial; font-size: 20px;'>{{Picture}}</div>{{/Picture}}
                    {{#Definition}}<div style='font-family: Arial; font-size: 20px;'>{{Definition}}</div>{{/Definition}}
                    {{#Source}}<div style='font-family: Arial; font-size: 20px;'>{{Source}}</div>{{/Source}}
                    """)
            },
            {
                'name': 'Spelling',
                'qfmt': dedent("""\
                    Peut tu l'épeler?
                    <div style='font-family: Arial; font-size: 20px;'>{{Audio}}</div>
                    <div style='font-family: Arial; font-size: 20px;'>{{Picture}}</div>
                    """),
                'afmt': dedent("""\
                    <div style='font-family: Arial; font-size: 20px;'>{{#Article}}{{Article}}{{/Article}}&nbsp;{{Word or Phrase}}</div>
                    {{#Source}}<div style='font-family: Arial; font-size: 20px;'>{{Source}}</div>{{/Source}}
                    """)
            },
            {
                'name': 'Article',
                'qfmt': dedent("""\
                    {{#Article}}
                    <div style='font-family: Arial; font-size: 20px;'>[...] {{Word or Phrase}}</div>
                    {{/Article}}
                    """),
                'afmt': dedent("""\
                    <div style='font-family: Arial; font-size: 20px;'>{{Article}}&nbsp;{{Word or Phrase}}</div>
                    <div style='font-family: Arial; font-size: 20px;'>{{Mnemonic}}</div>
                    {{#Source}}<div style='font-family: Arial; font-size: 20px;'>{{Source}}</div>{{/Source}}
                    """)
            },
            {
                'name': 'Pronuncation',
                'qfmt': dedent("""\
                    {{#Audio}}{{#IPA}}<div style='font-family: Arial; font-size: 20px;'>
                    Comment prononcez-vous ce mot?
                    <BR>
                    <BR>
                    {{Word or Phrase}}
                    </div>{{/IPA}}{{/Audio}}
                    """),
                'afmt': dedent("""\
                    <div style='font-family: Arial; font-size: 20px;'>{{IPA}}</div>
                    <div style='font-family: Arial; font-size: 20px;'>{{Audio}}</div>
                    {{#Source}}<div style='font-family: Arial; font-size: 20px;'>Sources:&nbsp;{{Source}}</div>{{/Source}}
                    """)
            }
        ],
        css=""".card {
     font-family: arial;
     font-size: 20px;
     text-align: center;
     color: black;
     background-color: white;
    }"""
    )
    return my_model


def create_notes(results: list, genaki_model: genanki.Model) -> list:
    my_notes = []
    for item in results:
        my_note = genanki.Note(
            model=genaki_model,
            fields=[
                item['word'],
                item.get('article', ''),
                item.get('pos', ''),  # part of speech
                item.get('definition', ''),
                '<img src="{}">'.format(item['image_file_resized']),
                "[sound:{}]".format(item.get('audio_file', '').format(r's')),  # [sound:sound.mp3] format for anki decks
                item.get('ipa', ''),
                "",  # no predefined mnemonic ;)
                '<a href="{}">collins</a><br><a href="{}">image-page</a>'.format(item['collins_query'],
                                                                                 item['image_page_url'])
            ])
        my_notes.append(my_note)

    return my_notes


def create_deck(ids: dict, notes: list) -> genanki.Deck:
    genaki_deck = genanki.Deck(
        int(ids['deck_id']),
        'German-Genanki')

    for note in notes:
        genaki_deck.add_note(note)

    return genaki_deck


def create_media_database(results: list) -> list:
    media = [x.get('image_file_resized') for x in results if x['image_file'] is not None]
    media.extend([x['audio_file'] for x in results if x['audio_file'] is not None])

    return media


def package_deck(gaki_deck: genanki.Deck, media: list):
    de_package = genanki.Package(gaki_deck)
    de_package.media_files = media

    return de_package


def clean_up(results: list) -> None:
    [os.remove(x['image_file']) for x in results if x['image_file'] is not None]
    [os.remove(x['audio_file']) for x in results if x['audio_file'] is not None]


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    write_genaki()
    genaki_ids = load_ids()
    req_headers, req_params, yaml_settings = bing_setup()
    search_list = load_search_list()
    search_results = get_search_term_data(search_list, req_headers, req_params, yaml_settings)
    genaki_model = create_anki_model(genaki_ids)
    genaki_notes = create_notes(search_results, genaki_model)
    genaki_deck = create_deck(genaki_ids, genaki_notes)
    media_db = create_media_database(search_results)
    de_pack = package_deck(genaki_deck, media_db)

    de_pack.write_to_file('de_learning_package.apkg')
    clean_up(search_results)
