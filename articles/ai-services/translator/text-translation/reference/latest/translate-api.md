---
title: Azure AI Translator 2025-05-01-preview translate method
titleSuffix: Azure AI services
description: Understand the parameters, headers, and body messages for the Azure AI Translator 2025-05-01-preview translate method.
author: laujan
manager: nitinme
ms.service: azure-ai-translator
ms.topic: reference
ms.date: 04/22/2025
ms.author: lajanuar
---

# Translate (2025-05-01-preview)

The Text translation API enables you to translate your source language text into a specified target language text.

>[!IMPORTANT]
> * Azure AI Translator REST API `2025-05-01-preview` is new version of the Azure AI Translator REST API **with breaking changes**.
> * It's essential to thoroughly test your code against the new release before migrating any production applications from Azure AI Translator v3.0.
> * Make sure to review your code and internal workflows for adherence to best practices and restrict your production code to versions that you fully test.


## Request URL

**Send a `POST` request to**:

```bash
https://api.cognitive.microsofttranslator.com/translate?api-version=2025-05-01-preview

```

For more information on Translator service selected network and private endpoint configuration and support, *see* [**Virtual Network Support**](../authentication.md#virtual-network-support).

## Request headers

Request headers include:

| Headers | Description |
| --- | --- |
| **Authentication headers** | _Required request header_.<br/>See [available options for authentication](../authentication.md). |
| **Content-Type** | _Required request header_.<br/>Specifies the content type of the payload. Accepted values are: `application/json`; `charset=UTF-8`|
| **Content-Length** | _Optional_.<br/>The length of the request body. |
| **X-ClientTraceId** | _Optional_.<br/>A client-generated GUID to uniquely identify the request. You can omit this optional header if you include the trace ID in the query string using a query parameter named `ClientTraceId`. |

#### Request parameters

Request parameters passed with the request are as follows:

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
|**`api-version`**|string|True|Version of the API requested by the client. Accepted value is `2025-05-01-preview`.|
|**`text`** | string | True | Source text for translation. |
| **`targets`** | array | True | User-specified values for the translated (`target`) text. |
| **`language`** | string | True |The language code for the translated (`target`) text *specified in the `targets` array*. Accepted values are [supported language](../../../language-support.md) codes for the translation operation.|
| **textType** | string | False | Defines whether the text being translated is plain text or HTML text. Any HTML needs to be a well-formed, complete element. Accepted values are: plain (default) or html. |
| **language** | string | False | Specifies the language code for the `source` text. If not specified, the system autodetects the language of the source text. Accepted values are list of language code supported by the specified model. |
| **script** | string | False | Specifies the script of the source text. |

#### Targets array (user-specified values for translated text)

| Parameter | Type | Required? | Description |
| --- | --- | --- | --- |
| **targets.language** | string | True |The language code for the translated (`target`) text *specified in the `targets` array*. Accepted values are [supported language](../../../language-support.md) codes for the translation operation.|
| **targets.script** | string | False | Specify the script of the translated text. |
|**targets.deploymentName** | string | False | Default is `general`, which uses `NMT` system. `your-model-name-gpt-4o-mini` is an example deployment name for the GPT-4o-mini model. `gpt-4o` uses GPT-4o model.<br> `<categoryID>` uses the custom `NMT` model tuned by customer.<br>  |
| **targets.allowFallback** | string | False | If the desired model doesn't support a particular pair of source and target languages, an alternative approach may be employed. In such cases, the service may default to utilizing a general system as a substitute. This action ensures that translations can still be provided even when the preferred model is unavailable. Default is `true`. If `false` system returns an error if language pair isn't supported. |
| **targets.tone** | string | False | Desired tone of target translation. Accepted values are `formal`, `informal`, or `neutral`. |
| **targets.gender** (For more information, *see* [Gender-specific translations](#gender-specific-translations))| string | False | Desired gender of target translation. Accepted values are `male`, `female`, or `neutral`.|
| **targets.adaptiveDatasetId** | string | False | Reference dataset ID having sentence pair to generate adaptive customized translation. The maximum number of reference text pairs to generate adaptive customized translation is five (5).|
| **targets.referenceTextPairs** | string | False | Reference text pairs to generate adaptive customized translation. |
| **targets.referenceTextPairs.source** | string | False | Source text in reference text pair. If provided, `adaptiveDatasetId` is ignored. |
| **targets.referenceTextPairs.target** | string | False | Target text in reference text pair. |
| **targets.profanityAction** | string | False | Specifies how profanities should be treated in translations. Accepted values are: `NoAction` (default), `Marked`, or `Deleted`. |
| **targets.profanityMarker** | string | False | Specifies how profanities should be marked in translations. Accepted values are `Asterisk` (default) or Tag. |

##### Gender-specific translations

The following table shows gender-specific translations with the optional targets array gender parameter.

| Source text | Target gender | Expected gender in translation |
| --- | --- | --- |
| Neutral | Not indicated | Neutral /  **Random**: if target language doesn't have a gender-neutral term. |
| Female | Not indicated | Female / **Neutral**: if target language is gender neutral. |
| Male |Not indicated | Male / **Neutral**: if target language is gender neutral. |
| Neutral<br>Female<br>Male  | → Female<br>→ Female<br>→ Female | Female / **Neutral**: if target language is gender neutral. |
| Neutral<br>Female<br>Male | → Male<br>→ Male<br>→ Male | Male / **Neutral**: if target language is gender neutral. |

## Request body

The request body is formatted as a JSON array, where each element is a JSON object. Each object contains a required property named `text`, representing the string to be translated, and a required `targets` array. The `targets` array includes the required `language` property that specifies the language code for the translation.

```json
[
  {
    "text": "I would really like to drive your car around the block a few times.",
    "language": "en",
    "targets": [
      {
        "language": "es"
      }
    ]
  }
]
```
For information on character and array limits, _see_ [Request limits](../../../service-limits.md#character-and-array-limits-per-request).

## Response body

A successful response is a JSON array with one result for each string in the input array. A result object includes the following properties:

* `detectedLanguage`: An object describing the detected language through the following properties:

  * `language`: A string representing the code of the detected language.

  * `score`: A float value indicating the confidence in the result. The score is between zero and one and a low score indicates a low confidence.

  The `detectedLanguage` property is only present in the result object when language `autodetection` is requested.

* `translations`: An array of translation results. The size of the array matches the number of target languages specified through the `to` query parameter. Each element in the array includes:

  * `text`: A string giving the translated text.

  * `language`: A string representing the language code of the target language.

  * `transliteration`: An object giving the translated text in the script specified by the `toScript` parameter.

    * `script`: A string specifying the target script.

    * `text`: A string giving the translated text in the target script.

    The `transliteration` object isn't included if transliteration doesn't take place.


* `sourceText`: An object with a single string property named `text`, which gives the input text in the default script of the source language. `sourceText` property is present only when the input is expressed in a script that's not the usual script for the language. For example, if the input were Arabic written in Latin script, then `sourceText.text` would be the same Arabic text converted into Arab script`.`

Examples of JSON responses are provided in the [examples](#examples) section.

## Response headers

| Headers | Description |
| --- | --- |
| X-requestid | Value generated by the service to identify the request used for troubleshooting purposes. |
| X-mt-system | Specifies the system type that was used for translation for each 'to' language requested for translation. The value is a comma-separated list of strings. Each string indicates a type:  </br></br>*Custom - Request includes a custom system and at least one custom system was used during translation.*</br> Team - All other requests |
| X-metered-usage |Specifies consumption (the number of characters for which the user is charged) for the translation job request. For example, if the word "Hello" is translated from English (en) to French (fr), this field returns the value `5`.|

## Examples

#### Translate

***Request***

```json
 [
  {
    "text": "Doctor is available next Monday. Do you want to schedule an appointment?",
    "language": "en",
    "targets": [
      {
        "language": "es"
      }
    ]
  }
]
```

***Response***

```JSON
[
  {
    "detectedLanguage": {
      "language": "en",
      "score": 1
    },
    "translations": [
      {
        "text": "La médica estará disponible el próximo lunes. ¿Desea programar una cita?",
        "language": "es",
        "sourceCharacters": 72
      }
    ]
  }
]
```

***Response Header***

```bash
"sourceCharactersCharged": 72
```

#### Translate source text into multiple languages

***Request***

```json
[
  {
    "text": "Doctor is available next Monday. Do you want to schedule an appointment?",
    "language": "en",
    "targets": [
      {
        "language": "es"
      },
      {
        "language": "de"
      }
    ]
  }
]
```

***Response***

```json
[
  {
    "detectedLanguage": {
      "language": "en",
      "score": 1
    },
    "translations": [
      {
        "text": "La médica estará disponible el próximo lunes. ¿Desea programar una cita?",
        "language": "es",
        "sourceCharacters": 72
      },
      {
        "text": "Der Arzt ist nächsten Montag verfügbar. Möchten Sie einen Termin vereinbaren?",
        "language": "de",
        "sourceCharacters": 72
      }
    ]
  }
]
```

***Response Header***

```bash
"sourceCharactersCharged": 144
```

#### Translate using `GPT-4o mini` and `NMT` deployments

Here, users request specific `GPT` models for deployment.

***Request***

```json
 [
  {
    "text": "Doctor is available next Monday. Do you want to schedule an appointment?",
    "language": "en",
    "targets": [
      {
        "language": "es",
        " deploymentName": "your-gpt-4omini-deployment-name"
      },
      {
        "language": "de"
      }
    ]
  }
]
```

***Response***

```json
[
  {
    "detectedLanguage": {
      "language": "en",
      "score": 1
    },
    "translations": [
      {
        "text": "La médica estará disponible el próximo lunes. ¿Desea programar una cita?",
        "language": "es",
        "instructionTokens": 12,
        "sourceTokens": 14,
        "targetTokens": 16
      },
      {
        "text": "Der Arzt ist nächsten Montag verfügbar. Möchten Sie einen Termin vereinbaren?",
        "language": "de",
        "sourceCharacters": 72
      }
    ]
  }
]

```

***Response Header***

```bash
"sourceCharactersCharged": 72
"sourceTokensCharged": 26
"targetTokensCharged": 16
```

#### Translate specifying gender and tone using `GPT-4o mini` deployment

***Request***

```json
[
  {
    "text": "Doctor is available next Monday. Do you want to schedule an appointment?",
    "language": "en",
    "targets": [
      {
        "language": "es",
        "deploymentName": "your-gpt-4omini-deployment-name",
        "tone": "formal",
        "gender": "female"
      },
      {
        "language": "es",
        "deploymentName": "your-gpt-4omini-deployment-name",
        "tone": "formal",
        "gender": "male"
      }
    ]
  }
]
```

***Response***

```json
[
  {
    "detectedLanguage": {
      "language": "en",
      "score": 1
    },
    "translations": [
      {
        "text": "La médica estará disponible el próximo lunes. ¿Desea programar una cita?",
        "language": "es",
        "promptTokens": 12,
        "sourceTokens": 14,
        "targetTokens": 16
      },
      {
        "text": "El médico estará disponible el próximo lunes. ¿Desea programar una cita?",
        "language": "es",
        "instructionTokens": 12,
        "sourceTokens": 14,
        "targetTokens": 16
      }
    ]
  }
]
```

***Response Header***

```bash
"sourceTokensCharged": 52
"targetTokensCharged": 32
```

#### Text translation request applying adaptive custom translation with dataset

Adaptive custom translation deploys on Translator service infrastructure. Charges are based on source characters.

***Request***

```json
[
  {
    "text": "Doctor is available next Monday. Do you want to schedule an appointment?",
    "language": "en",
    "targets": [
      {
        "language": "es",
        "adaptiveDatasetId": "TMS-en-es-hr-020"
      }
    ]
  }
]

```

***Response***

```json
[
  {
    "detectedLanguage": {
      "language": "en",
      "score": 1
    },
    "translations": [
      {
        "text": "La médica estará disponible el próximo lunes. ¿Desea programar una cita?",
        "language": "es",
        "sourceCharacters": 72,
        "targetChaaracters": 72
      }
    ]
  }
]
```

***Response Header***

```bash
"sourceCharactersCharged": 72 "targetChaaractersCharged": 72
```

#### Text translation request applying Adaptive custom translation with reference pairs

***Request***

```json
[
  {
    "text": "Doctor is available next Monday. Do you want to schedule an appointment?",
    "language": "en",
    "targets": [
      {
        "language": "es",
        "referenceTextPairs": [
          {
            "source": "text_in_en",
            "target": " text_in_es"
          },
          {
            "source": " text_in_en",
            "target": " text_in_es"
          }
        ]
      }
    ]
  }
]
```

***Response***

```json
[
  {
    "detectedLanguage": {
      "language": "en",
      "score": 1
    },
    "translations": [
      {
        "text": "La médica estará disponible el próximo lunes. ¿Desea programar una cita?",
        "language": "es",
        "sourceCharacters": 72,
        "targetCharacters": 72
      }
    ]
  }
]
```

***Response Header***

```bash
"sourceCharactersCharged": 72
"targetCharactersCharged": 72
```

#### Text translation request using custom translation

***Request***

```json
[
  {
    "text": "Doctor is available next Monday. Do you want to schedule an appointment?",
    "language": "en",
    "targets": [
      {
        "language": "es",
        "deploymentName": "f16e83fb-3af8-4d45-9290-10a516f9dfc4-GENERAL"
      }
    ]
  }
]
```

***Response***

```json
[
  {
    "detectedLanguage": {
      "language": "en",
      "score": 1
    },
    "translations": [
      {
        "text": "La médica estará disponible el próximo lunes. ¿Desea programar una cita?",
        "language": "es",
        "sourceCharacters": 72
      }
    ]
  }
]
```

***Response Header***

```bash
"sourceCharactersCharged": 72
```

## Next steps

> [!div class="nextstepaction"]
> [View 2025-05-01-preview migration guide](../../how-to/migrate-to-latest.md)
