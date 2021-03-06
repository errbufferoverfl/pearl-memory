<!-- PROJECT SHIELDS -->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]

<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/errbufferoverfl/pearl-memory">
    <img src="images/logo.gif" alt="Pearl Memory Logo" width="100" height="100">
  </a>

  <h3 align="center">Pearl Memory</h3>

  <p align="center">
    A Python script for creating German Anki cards. The script loads a CSV file of words to search, gets a translation using Azure Cognitive Services translate and text to speech to generate the primary content. Pearl Memory also supports Google for translation services not for text to speech.
    <br />
    <a href="https://github.com/errbufferoverfl/pearl-memory/blob/main/README.md"><strong>Explore the docs »</strong></a>
    <br />
    <br />
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
    <img src="images/pearlmemory_01.png" alt="product-screenshot" width="300" height="300">
  </a>
</p>

<!-- ABOUT THE PROJECT -->
## Built With

Built with Python 3, on Azure Cognos Services and Google Translate.

<!-- PREREQUISITES -->
# Prerequisites

* [Anki](https://apps.ankiweb.net/)
* [Azure Cognitive Services - Translate](https://azure.microsoft.com/en-au/services/cognitive-services/translator/)
* [Azure Cognitive Services - Text to Speech](https://azure.microsoft.com/en-au/services/cognitive-services/text-to-speech/)
* [Bing Search v7 Marketplace Resource](https://azure.microsoft.com/en-au/pricing/details/cognitive-services/search-api/)
* [Python 3.7](https://www.python.org/)

## Optional

For better and more consistent translation, you can now use Google Translate. **Note:** You only need the Translation API Basic tier.
* [Google Translate Basic API](https://cloud.google.com/translate)

The following additional tools are needed if you want to automatically build the Azure Services - the Terraform file will not deploy the Google Translate API services so this still needs to be done manually.

* [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)
* [Terraform](https://www.terraform.io/)

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

3. Configure a Bing API key, Azure Translator API and Azure Text to Speech API. This can be done automatically using Terraform by running:
```
terraform plan
terraform apply
```
_The Bing resource still needs to be created manually, because of a known issue with the Azure API._

**Note:** Bing.Search.v7 APIs haven't been correctly migrated for Terraform use yet so you will need to manually create this asset. You can see the [GitHub issue](https://github.com/terraform-providers/terraform-provider-azurerm/issues/9102) for more details.

**Note:** By default this will deploy (non-global) resources in `australiaeast` using the name "pearl-memory", you can change these values by specifying alternatives using the `var` flag like:

```
terraform apply  -var="name=my-awesome-flashcard-generator" -var="region=brazilsouth"
```

Once the services have been successfully deployed via Terraform, you should see output similar to the following:

```
Apply complete! Resources: 2 added, 0 changed, 0 destroyed.

Outputs:

az-speech-cog-key = <sensitive>
az-translate-cog-key = <sensitive>
```

These outputs can be found in the `.tfstate` file and can be used for the following steps.

4. (Optional: Google) If you are planning on using the Google Translation API, you will need to create a [Google Cloud Platform account](https://console.cloud.google.com/). Once you have logged into the Google Cloud Platform (GCP) console, using the GCP search bar, search for "Cloud Translation API" and follow the steps to create a new project.

5. Create an API key (not a service account) for this service, and ensure you scope the keys to only the translation service so if they are compromised the impact caused is minimised.

6. Create three environment variables:

```
AZ-SEARCH-KEY   Bing Search API Key

# If you are using Google do not create this key
AZ-TRANS-KEY    Azure Translate Key
AZ-SPEECH-KEY   Azure Speech Key

# If you are using Google create this key
GOOGLE-TRANS-KEY  Google Translate Key created in step 4.
```

If you *aren't* using the `auestralianeast` region in Azure you'll also want to set the following environment variables:

```
AZ-SUB-REGION     brazilsouth
AZ-TRANS-REGION   brazilsouth
```

Check [Speech-to-text, text-to-speech, and translation Regions](https://docs.microsoft.com/en-au/azure/cognitive-services/speech-service/regions#speech-sdk) for the region short codes.

6. Populate the `anki_search.csv` with the words you wish to turn into flash cards. You can use English or German words and Pearl Memory will handle the translation to and from their respective language.

<!-- USAGE EXAMPLES -->
## Usage Examples

```sh
pipenv shell
./pearl-memory.py
Please enter your deck name: My New Deck Name
```

<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/errbufferoverfl/pearl-memory/issues) for a list of proposed features (and known issues). Pull requests are always welcome!

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. 
Any contributions you make is **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b issue_no_feature_description`)
3. Commit your Changes (`git commit -m "Adds some amazing feature"`)
4. Push to the Branch (`git push origin issue_no_feature_description`)
5. Open a Pull Request

<!-- LICENSE -->
## License

Distributed under the MIT License. See [LICENSE](LICENSE.txt) for more information.

<!-- CONTACT -->
## Contact

* errbufferoverfl - [@errbufferoverfl](https://twitter.com/errbufferoverfl)

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
[license-url]: https://github.com/errbufferoverfl/pearl-memory/blob/master/LICENSE.txt
[product-screenshot]: images/screenshot.png
