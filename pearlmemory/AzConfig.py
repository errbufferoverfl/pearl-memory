import os

import uuid
from azure.cognitiveservices.speech import ResultFuture
from azure.cognitiveservices.speech.audio import AudioOutputConfig
import azure.cognitiveservices.speech as speechsdk

class AzConf:
    AZURE_SPEECH_KEY = os.environ.get("AZ-SPEECH-KEY")
    AZURE_TRANSLATE_KEY = os.environ.get("AZ-TRANS-KEY")
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