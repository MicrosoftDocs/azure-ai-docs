---
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: include
ms.date: 06/30/2025
ms.author: lajanuar
---

[Reference documentation](https://go.microsoft.com/fwlink/?linkid=2239169)

Use this quickstart to send language detection requests using the REST API. In the following example, you'll use cURL to identify the language that a text sample was written in.

## Prerequisites

* Azure subscription - [Create one for free](https://azure.microsoft.com/free/cognitive-services)


## Setting up

[!INCLUDE [Create an Azure resource](../../../includes/create-resource.md)]

[!INCLUDE [Get your key and endpoint](../../../includes/get-key-endpoint.md)]

[!INCLUDE [Create environment variables](../../../includes/environment-variables.md)]


## Create a JSON file with the example request body

In a code editor, create a new file named `test_languagedetection_payload.json` and copy the following JSON example. This example request will be sent to the API in the next step.

```json
{
    "kind": "LanguageDetection",
    "parameters": {
        "modelVersion": "latest"
    },
    "analysisInput":{
        "documents":[
            {
                "id":"1",
                "text": "This is a document written in English."
            }
        ]
    }
}
```
Save `test_detection_payload.json` somewhere on your computer. For example, your desktop.

## Send a language detection request

Use the following commands to send the API request using the program you're using. Copy the command into your terminal, and run it.

parameter  |Description  |
|---------|---------|
|`-X POST <endpoint>`     | Specifies your endpoint for accessing the API.        |
|`-H Content-Type: application/json`     | The content type for sending JSON data.          |
|`-H "Ocp-Apim-Subscription-Key:<key>`    | Specifies the key for accessing the API.        |
|`-d <documents>`     | The JSON containing the documents you want to send.         |

Save `test_languagedetection_payload.json` somewhere on your computer. For example, your desktop. 

## Send a language detection API request

Use the following commands to send the API request using the program you're using. Copy the command into your terminal, and run it.

|Parameter  |Description  |
|---------|---------|
|`-X POST <endpoint>`     | Specifies your endpoint for accessing the API.        |
|`-H Content-Type: application/json`     | The content type for sending JSON data.          |
|`-H "Ocp-Apim-Subscription-Key:<key>`    | Specifies the key for accessing the API.        |
|`-d <documents>`     | The JSON containing the documents you want to send.         |

# [Windows](#tab/windows)

 Replace `C:\Users\<myaccount>\Desktop\test_languagedetection_payload.json` with the location of the example JSON request file you created in the previous step.

### Command prompt

```terminal
curl -X POST "%LANGUAGE_ENDPOINT%/language/:analyze-text?api-version=2023-11-15-preview" ^
-H "Content-Type: application/json" ^
-H "Ocp-Apim-Subscription-Key: %LANGUAGE_KEY%" ^
-d "@C:\Users\<myaccount>\Desktop\test_languagedetection_payload.json"
```

### PowerShell

```terminal
curl.exe -X POST $env:LANGUAGE_ENDPOINT/language/:analyze-text?api-version=2023-11-15-preview `
-H "Content-Type: application/json" `
-H "Ocp-Apim-Subscription-Key: $env:LANGUAGE_KEY" `
-d "@C:\Users\<myaccount>\Desktop\test_languagedetection_payload.json"
```

#### [Linux](#tab/linux)

Use the following commands to send the API request using the program you're using. Replace `/home/mydir/test_languagedetection_payload.json` with the location of the example JSON request file you created in the previous step.

```terminal
curl -X POST $LANGUAGE_ENDPOINT/language/:analyze-text?api-version=2023-11-15-preview \
-H "Content-Type: application/json" \
-H "Ocp-Apim-Subscription-Key: $LANGUAGE_KEY" \
-d "@/home/mydir/test_languagedetection_payload.json"
```

#### [macOS](#tab/macos)

Use the following commands to send the API request using the program you're using. Replace `/home/mydir/test_languagedetection_payload.json` with the location of the example JSON request file you created in the previous step.

```terminal
curl -X POST $LANGUAGE_ENDPOINT/language/:analyze-text?api-version=2023-11-15-preview \
-H "Content-Type: application/json" \
-H "Ocp-Apim-Subscription-Key: $LANGUAGE_KEY" \
-d "@/home/mydir/test_languagedetection_payload.json"
```

---

Use the following commands to send the API request using the program you're using. Replace `/home/mydir/test_detection_payload.json` with the location of the example JSON request file you created in the previous step.

```terminal
curl -X POST $LANGUAGE_ENDPOINT/language/:analyze-text?api-version=2023-11-15-preview \
-H "Content-Type: application/json" \
-H "Ocp-Apim-Subscription-Key: $LANGUAGE_KEY" \
-d "@/home/mydir/test_detection_payload.json"
```

---

## JSON response

```json
{
    "kind": "LanguageDetectionResults",
    "results": {
        "documents": [
            {
                "id": "1",
                "detectedLanguage": {
                    "name": "English",
                    "iso6391Name": "en",
                    "confidenceScore": 1.0,
                    "script": "Latin",
                    "scriptCode": "Latn"
                },
                "warnings": []
            }
        ],
        "errors": [],
        "modelVersion": "2023-12-01"
    }
}
```

[!INCLUDE [clean up environment variables](../../../includes/clean-up-variables.md)]
