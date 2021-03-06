# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2021-04-06

### Added

- Support for Google Translate services using API keys.
- Method that fetches example sentences and audio for the word being translated.
- 10-second sleep function between each card to prevent throttling from Azure Cognitive Services.

### Removes

- Images from the default template used to generate cards

### Changed
- Now leverages an object-oriented approach for the whole script.
- Removed check for file existence that stopped unique IDs being generated each time the program ran - causing cards to get incorrectly bundled in Anki.
- Improves exception handling in `bing_setup()` function - adds `FileNotFoundError` and `TypeError`.
- Improves exception handling in `load_ids()` function - adds `FileNotFoundError` and `TypeError`.
- Improves exception handling in `load_search_list()` function - adds `FileNotFoundError` and `TypeError`.
- Improves exception handling in `azure_translate()` function - adds `TypeError`.
- Extracts language detection in `azure_translate()` function to its own `detect_language()` function.
- From GPLv3 license to MIT.
- Uses a custom language detection factory to improve the detection of English and German words.
- Default template for flashcards.

## [1.1.0] - 2020-11-18
### Added
- Terraform template for generating a project specific resource group, Cognos Translate and Text to Speech service.
- Template for `Bing.Search.v7` however, not usable until [this issue is resolved](https://github.com/terraform-providers/terraform-provider-azurerm/issues/9102).

## [1.0.0] - 2020-11-04
### Changed
- `image_api_url` to new Bing Search API via Marketplace
- Improved handling for resizing images
- Improved handling of images missing a proper file extension
- Improved clean up of images, and sound files
- Changed URL in README to match new GitHub name
- Included `*.apkg` to .gitignore

### Added
- Missing 'missing.png' image