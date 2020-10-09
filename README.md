<!-- PROJECT SHIELDS -->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![GPLv3 License][license-shield]][license-url]

<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/errbufferoverfl/pearlmemory">
    <img src="images/logo.png" alt="Pearl Memory Logo" width="80" height="80">
  </a>

  <h3 align="center">Pearl Memory</h3>

  <p align="center">
    A Python script for creating German Anki cards. The script loads a CSV file of words to search, then it gets 
    data from Bing image search, and the Collins dictionary. The script tries to get culture/language specific images 
    but is often hilariously bad at this.
    <br />
    <a href="https://github.com/errbufferoverfl/pearlmemory"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/errbufferoverfl/pearlmemory">View Demo</a>
    ·
    <a href="https://github.com/errbufferoverfl/pearlmemory/issues">Report Bug</a>
    ·
    <a href="https://github.com/errbufferoverfl/pearlmemory/issues">Request Feature</a>
  </p>
</p>

<!-- TABLE OF CONTENTS -->

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
* [Roadmap](#roadmap)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)
* [Acknowledgements](#acknowledgements)

<!-- ABOUT THE PROJECT -->
# About the Project

[![Pearlmemory Screen Shot][product-screenshot]](https://example.com)

<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running on macOS use the following steps.

1. Clone the repo.
```sh
git clone https://github.com/errbufferoverfl/pearlmemory.git
```
2. Install Python packages.
```sh
pipenv install
```
3. Configure a Bing API key.

4. Replace the `BING-API-KEY` in `bing_settings.yaml` with Key 1 from Azure.

5. Populate the `anki_search.csv` with the words you wish to turn into flash cards. You'll get the best results if you
do not include the gender of the word (die, der, das).

<!-- USAGE EXAMPLES -->
## Usage Examples

```sh
pipenv shell
./pearlmemory.py
```

<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/errbufferoverfl/pearlmemory/issues) for a list of proposed features 
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

Project Link: [https://github.com/errbufferoverfl/repo_name](https://github.com/errbufferoverfl/pearlmemory)

<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements

* [Jean-Michel Moreau](https://github.com/jm-moreau)

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/errbufferoverfl/repo.svg?style=flat-square
[contributors-url]: https://github.com/errbufferoverfl/repo/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/errbufferoverfl/repo.svg?style=flat-square
[forks-url]: https://github.com/errbufferoverfl/repo/network/members
[stars-shield]: https://img.shields.io/github/stars/errbufferoverfl/repo.svg?style=flat-square
[stars-url]: https://github.com/errbufferoverfl/repo/stargazers
[issues-shield]: https://img.shields.io/github/issues/errbufferoverfl/repo.svg?style=flat-square
[issues-url]: https://github.com/errbufferoverfl/repo/issues
[license-shield]: https://img.shields.io/github/license/errbufferoverfl/repo.svg?style=flat-square
[license-url]: https://github.com/errbufferoverfl/repo/blob/master/LICENSE.txt
[product-screenshot]: images/screenshot.png