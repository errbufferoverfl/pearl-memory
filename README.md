<!-- PROJECT SHIELDS -->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![GPLv3 License][license-shield]][license-url]

<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/errbufferoverfl/pearl-memory">
    <img src="images/logo.gif" alt="Pearl Memory Logo" width="100" height="100">
  </a>

  <h3 align="center">Pearl Memory</h3>

  <p align="center">
    A Python script for creating German Anki cards. The script loads a CSV file of words to search, gets a translation
    using Azure Cognitive Services translate and text to speech to generate the primary content, to help enforce the
    learning process uses images sourced from Bing Image API.
    <br />
    <a href="https://github.com/errbufferoverfl/pearl-memory"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/errbufferoverfl/pearl-memory">View Demo</a>
    ·
    <a href="https://github.com/errbufferoverfl/pearl-memory/issues">Report Bug</a>
    ·
    <a href="https://github.com/errbufferoverfl/pearl-memory/issues">Request Feature</a>
  </p>
</p>

<!-- TABLE OF CONTENTS -->

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Prerequisites](#prerequisites)
* [Getting Started](#getting-started)
* [Usage](#usage)
* [Roadmap](#roadmap)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)
* [Acknowledgements](#acknowledgements)

<!-- ABOUT THE PROJECT -->
# About the Project

<p align="center">
  <a href="https://github.com/errbufferoverfl/pearl-memory">
    <img src="images/pearl-memory_01.png" alt="product-screenshot" width="300" height="300">
  </a>
</p>

<!-- ABOUT THE PROJECT -->
## Built With

Built with Python 3 for Anki.

<!-- prerequisites -->
# Prerequisites

* [Anki](https://apps.ankiweb.net/)
* [Azure Cognitive Services - Translate](https://azure.microsoft.com/en-au/services/cognitive-services/translator/)
* [Azure Cognitive Services - Text to Speech](https://azure.microsoft.com/en-au/services/cognitive-services/text-to-speech/)
* [Bing Search v7 Marketplace Resource](https://azure.microsoft.com/en-au/pricing/details/cognitive-services/search-api/)
* [Python 3.7](https://www.python.org/)

<!-- GETTING STARTED -->
# Getting Started

To get a local copy up and running on macOS use the following steps.

1. Clone the repo.
```sh
git clone https://github.com/errbufferoverfl/pearl-memory.git
```
2. Install Python packages.
```sh
pipenv install
```
3. Configure a Bing API key, Azure Translator API and Azure Text to Speech API.

4. In `bing_settings.yaml` replace the `BING-API-KEY`, `AZURE_TRANSLATE_KEY` and `AZURE_SPEECH_KEY`.

5. Ensure the `translate_subscription_region` and `voice_subscription_region` is set to the region your resource is
deployed in. Check [Speech-to-text, text-to-speech, and translation Regions](https://docs.microsoft.com/en-au/azure/cognitive-services/speech-service/regions#speech-sdk) for 
region short codes.

6. Populate the `anki_search.csv` with the words you wish to turn into flash cards. You can use English or German words 
and Pearl Memory will handle the translation to and from their respective language, this isn't perfect and some phrases
such as `der Lenz` may not be 100% accurate.

<!-- USAGE EXAMPLES -->
## Usage Examples

```sh
pipenv shell
./pearl-memory.py
```

<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/errbufferoverfl/pearl-memory/issues) for a list of proposed features 
(and known issues).

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. 
Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<!-- LICENSE -->
## License

Distributed under the GPLv3 License. See [LICENSE.md](LICENSE.md) for more information.

<!-- CONTACT -->
## Contact

errbufferoverfl - [@errbufferoverfl](https://twitter.com/errbufferoverfl)

Project Link: [https://github.com/errbufferoverfl/pearl-memory](https://github.com/errbufferoverfl/pearl-memory)

<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements

* [Jean-Michel Moreau](https://github.com/jm-moreau)

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/errbufferoverfl/pearl-memory.svg?style=flat-square
[contributors-url]: https://github.com/errbufferoverfl/pearl-memory/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/errbufferoverfl/pearl-memory.svg?style=flat-square
[forks-url]: https://github.com/errbufferoverfl/pearl-memory/network/members
[stars-shield]: https://img.shields.io/github/stars/errbufferoverfl/pearl-memory.svg?style=flat-square
[stars-url]: https://github.com/errbufferoverfl/pearl-memory/stargazers
[issues-shield]: https://img.shields.io/github/issues/errbufferoverfl/pearl-memory.svg?style=flat-square
[issues-url]: https://github.com/errbufferoverfl/pearl-memory/issues
[license-shield]: https://img.shields.io/github/license/errbufferoverfl/pearl-memory.svg?style=flat-square
[license-url]: https://github.com/errbufferoverfl/pearl-memory/blob/master/LICENSE.md
[product-screenshot]: images/screenshot.png
