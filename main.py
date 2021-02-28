#!/usr/bin/env pipenv run python
# -*- coding: utf-8 -*-

import logging
from pathlib import Path

import requests

CVS_FILE_ENCODING = "mac_roman"
RESIZE_IMAGE_X, RESIZE_IMAGE_Y = 400, 300


GENANKI_ID_YAML = Path("genanki_ids.yaml")
BING_SETTINGS_YAML_FILENAME = Path("bing_settings.yaml")
TEMPLATES_DIR = Path("templates")
OUTPUT_DIR = Path("output")
TMP_DIR = Path("tmp")

# index of Bing image we use
IMAGE_INDEX = 0

def download(url: str, filename: str) -> None:
    """
    Downloads a given file from a URL.

    Args:
        url: The location of the file as a Uniform Resource Locator (URL)
        filename: The name of the resource being downloaded based on a Uniform Resource Identifier (URI) fragment.
            For example: https://www.wildlifeworldwide.com/images/categories/polar_bear_watching_select_locations.jpg
            The filename = polar_bear_watching_select_locations.jpg

    Returns: None
    """
    with open(filename, 'wb') as f:
        logging.info(f"Downloading: {filename}")
        img_data = requests.get(url, headers={"User-Agent': 'Mozilla/5.0"})
        img_data.raise_for_status()
        f.write(img_data.content)