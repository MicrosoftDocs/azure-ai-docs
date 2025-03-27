---
title: Translator v4.0 Reference
titleSuffix: Azure AI services
description: Reference documentation for the Azure AI Translator v4.0 operations and capabilities.
author: laujan
manager: nitinme
ms.service: azure-ai-translator
ms.topic: reference
ms.date: 03/24/2025
ms.author: lajanuar
---

# Translator v4.0

Azure AI Translator v4.0 is our latest cloud-based, multilingual neural machine translation service and provides robust and scalable translation capabilities suitable for diverse applications. Translator service supports over 100 languages and dialects, making it ideal for businesses, developers, and organizations seeking to seamlessly integrate multilingual communication. Translator is an optimal solution for managing extensive multilingual content and easily integrates with your applications and workflows through a single REST API call and supports multiple programming languages. Azure AI Translator prioritizes data security and privacy, complying with regulations like GDPR, HIPAA, and ISO/SOC, thus ensuring that it's a reliable solution for handling sensitive and confidential information.

## What's new?

Azure AI Translator v4.0 is designed toe be **backwards compatible** with Translator v3.0, requiring minimal updates for existing customers. In addition, Translator v4.0 offers several new feature updates and expanded capabilities:

* **LLM choice**. You can choose a large language model based for translation based on quality, cost, and other factors, while avoiding costs associated with prompt engineering and quality evaluations.

* **Adaptive custom translation**. New features enable adaptive custom translations using datasets or reference pairs to ensure more accurate and contextually relevant translations.

* **Enhanced translation**. The API supports a range of parameters, including text type, language codes, and options for tone and gender, providing more nuanced translation outputs.

## Base URLs

Typically, The nearest datacenter to the point of origin manages requests to Translator. However, if there's a datacenter failure when utilizing the global endpoint, requests may be redirected beyond the initial geography.

To ensure that requests are handled within a specific region, utilize the designated geographical endpoint so all requests are processed within the datacenters of the chosen geography.

✔️ Feature: **Translator Text** </br>

| Service endpoint | Request processing data center |
|------------------|--------------------------|
|**Global (recommended):**</br>**`api.cognitive.microsofttranslator.com`**|Closest available data center.|
|**Americas:**</br>**`api-nam.cognitive.microsofttranslator.com`**|East US 2 &bull; West US 2|
|**Asia Pacific:**</br>**`api-apc.cognitive.microsofttranslator.com`**|Japan East &bull; Southeast Asia|
|**Europe (except Switzerland):**</br>**`api-eur.cognitive.microsofttranslator.com`**|France Central &bull; West Europe|
|**Switzerland:**</br> For more information, *see* [Switzerland service endpoints](#switzerland-service-endpoints).|Switzerland North &bull; Switzerland West|

#### Switzerland service endpoints

Customers with a resource located in Switzerland North or Switzerland West can ensure that their Text API requests are served within Switzerland. To ensure that requests are handled in Switzerland, create the Translator resource in the `Resource region` `Switzerland North` or `Switzerland West`, then use the resource`s custom endpoint in your API requests.

For example: If you create a Translator resource in Azure portal with `Resource region` as `Switzerland North` and your resource name is `my-swiss-n`, then your custom endpoint is `https&#8203;://my-swiss-n.cognitiveservices.azure.com`. And a sample request to translate is:

```curl
// Pass secret key and region using headers to a custom endpoint
curl -X POST "https://my-swiss-n.cognitiveservices.azure.com/translator/text/v3.0/translate?to=fr" \
-H "Ocp-Apim-Subscription-Key: xxx" \
-H "Ocp-Apim-Subscription-Region: switzerlandnorth" \
-H "Content-Type: application/json" \
-d "[{`Text`:`Hello`}]" -v
```

Custom Translator isn't currently available in Switzerland.

## Request headers

Request headers include:

| Headers | Description |
| --- | --- |
| **Authentication headers** | _Required request header_.<br/>See [available options for authentication](../authentication.md). |
| **Content-Type** | _Required request header_.<br/>Specifies the content type of the payload. Accepted values are: `application/json`; `charset=UTF-8`|
| **Content-Length** | _Optional_.<br/>The length of the request body. |
| **X-ClientTraceId** | _Optional_.<br/>A client-generated GUID to uniquely identify the request. You can omit this optional header if you include the trace ID in the query string using a query parameter named `ClientTraceId`. |

## Request body parameters

Request parameters passed on the query string are as follows:

#### Query parameters

| Parameter | Type | Required? | Description |
| --- | --- | --- | --- |
|**api-version**|string|True|Version of the API requested by the client.|
| **text** | string | True | Source text for translation. |
| **textType** | string | False | Defines whether the text being translated is plain text or HTML text. Any HTML needs to be a well-formed, complete element. Possible values are: plain (default) or html. |
| **language** | string | False | The language code for the source text. If not specified, the system autodetects the language of the source text. Possible values are list of language code supported by the specified model. |
| **script** | string | False | Specify the script of the source text. |

#### Targets array parameters

| Parameter | Type | Required? | Description |
| --- | --- | --- | --- |
| **targets** | array | True | Targets for text translation. |
| **targets.language** | string | True | The language code for the translated text. Possible values are list of language code supported by the specified model. |
| **targets.script** | string | False | Specify the script of the translated text. |
|**targets.deploymentName** | string | False | Default is `general`, which uses `NMT` system. `gpt-4o-mini` uses GPT-4o-mini model. `gpt-4o` uses GPT-4o model. `<custom model id>` uses the custom `NMT` model tuned by customer. |
| **targets.allowFallback** | string | False | If the specified model isn't supported for a given source and target language pair, the service is permitted to revert to a general system. This action ensures that translations can still be provided even when the preferred model is unavailable. Default is `true`. If `false` system returns an error if language pair isn't supported. |
| **targets.grade** | string | False | Default is `basic`. For example, translation produced by simple prompt like `translate <source text> from <source language> to <target language>`|
| **targets.tone** | string | False | Desired tone of target translation. Enum: Formal, informal, neutral. |
| **targets.gender** **\*** | string | False | Desired gender of target translation.|
| **targets.adaptiveDatasetId** | string | False | Reference dataset ID having sentence pair to generate adaptive customized translation |
| **targets.referenceTextPairs** | string | False | Reference text pairs to generate adaptive customized translation |
| **targets.referenceTextPairs.source** | string | False | Source text in reference text pair. |
| **targets.referenceTextPairs.target** | string | False | Target text in reference text pair. |
| **targets.profanityAction** | string | False | Specifies how profanities should be treated in translations. Possible values are: `NoAction` (default), `Marked`, or `Deleted`. |
| **targets.profanityMarker** | string | False | Specifies how profanities should be marked in translations. Possible values are `Asterisk` (default) or Tag. |
| **targets.instruct** | string | False | Free flow textual instruction for `LLM` translation. This parameter negates all other key parameters within `targets`.|

**\*** Gender-specific translations with optional targets.gender parameter

| Source text | Target gender | Expected gender in translation |
| --- | --- | --- |
| Neutral |  | Neutral /  **Random**: if target language doesn't have a gender-neutral term. |
| Female |  | Female / **Neutral**: if target language is gender neutral. |
| Male |  | Male / **Neutral**: if target language is gender neutral. |
| Neutral | Female | Female / **Neutral**: if target language is gender neutral. |
| Female | Female |
| Male | Female |
| Neutral | Male | Male / **Neutral**: if target language is gender neutral. |
| Female | Male |
| Male | Male |


## Examples

#### Translate text

***Request***

```bash
 [ { "text": "Doctor is available next Monday. Do you want to schedule an appointment?", "targets": [ {     "language": "es"} ] } ] |
```

***Response***

```bash
[ { "detectedLanguage": { "language": "en", "score": 1     }, "translations": [ { "text": "La médica estará disponible el próximo lunes. ¿Desea programar una cita?", "language": "es", "sourceCharacters": 72} ]   } ]
```

***Response Header***

```bash
"sourceCharactersCharged": 72
```

#### Translate source text into multiple languages

***Request***

```bash
[ { "text": "Doctor is available next Monday. Do you want to schedule an appointment?", "targets": [ {     "language": "es"} , {     "language": "de"} ] } ]
```

***Response***

```bash
[ { "detectedLanguage": { "language": "en", "score": 1     }, "translations": [ { "text": "La médica estará disponible el próximo lunes. ¿Desea programar una cita?", "language": "es", "sourceCharacters": 72} , { "text": "Der Arzt ist nächsten Montag verfügbar. Möchten Sie einen Termin vereinbaren?", "language": "de", "sourceCharacters": 72} ]   } ]
```

***Response Header***

```bash
"sourceCharactersCharged": 144
```

#### Translate text using `GPT-4o mini` and `NMT` deployments

Here, users request specific `GPT` models for deployment.

***Request***

```bash
 [ { "text": "Doctor is available next Monday. Do you want to schedule an appointment?", "targets": [ {     "language": "es", " deploymentName": "gpt-4o-mini"} , {     "language": "de"} ] } ]
```

***Response***

```bash
| [ { "detectedLanguage": { "language": "en", "score": 1     }, "translations": [ { "text": "La médica estará disponible el próximo lunes. ¿Desea programar una cita?", "language": "es", "instructionTokens": 12,  "sourceTokens": 14,  "targetTokens": 16} , { "text": "Der Arzt ist nächsten Montag verfügbar. Möchten Sie einen Termin vereinbaren?", "language": "de", "sourceCharacters": 72} ]   } ]
```

***Response Header***

```bash
"sourceCharactersCharged": 72 
"sourceTokensCharged": 26
"targetTokensCharged": 16
```

#### Translate specifying gender and tone using `GPT-4o mini` deployment

***Request***

```bash
[ { "text": "Doctor is available next Monday. Do you want to schedule an appointment?", "targets": [ {     "language": "es", "model": "gpt-4o-mini", "tone": "formal", "gender": "female"},  {  "language": "es", "model": "gpt-4o-mini", "tone": "formal", "gender": "male"} ] } ]
```

***Response***

```bash
[ { "detectedLanguage": { "language": "en", "score": 1     }, "translations": [ { "text": "La médica estará disponible el próximo lunes. ¿Desea programar una cita?", "language": "es", "promptTokens": 12,  "sourceTokens": 14,  "targetTokens": 16}, { "text": "El médico estará disponible el próximo lunes. ¿Desea programar una cita?", "language": "es", "instructionTokens": 12,  "sourceTokens": 14,  "targetTokens": 16} ]   } ]
```

***Response Header***

```bash
"sourceTokensCharged": 52
"targetTokensCharged": 32
```

#### Text translation request applying adaptive custom translation with dataset

Adaptive custom translation deploys on Translator service infrastructure. Charges are based on source characters.

***Request***

```bash
[ { "text": "Doctor is available next Monday. Do you want to schedule an appointment?", "targets": [ {     "language": "es", "adaptiveDatasetId": "TMS-en-es-hr-020"} ] } ]
```

***Response***

```bash
[ { "detectedLanguage": { "language": "en", "score": 1     }, "translations": [ { "text": "La médica estará disponible el próximo lunes. ¿Desea programar una cita?", "language": "es", "sourceCharacters": 72, "targetChaaracters": 72} ]   } ]
```

***Response Header***

```bash
"sourceCharactersCharged": 72 "targetChaaractersCharged": 72
```

#### Text translation request applying Adaptive custom translation with reference pairs

***Request***

```bash
[ { "text": "Doctor is available next Monday. Do you want to schedule an appointment?", "targets": [ {     "language": "es", "referenceTextPairs": [ {  "source": "text_in_en",  "target": " text_in_es"}, { "source": " text_in_en",  "target": " text_in_es" }] } ] } ]
```

***Response***

```bash
[ { "detectedLanguage": { "language": "en", "score": 1     }, "translations": [ { "text": "La médica estará disponible el próximo lunes. ¿Desea programar una cita?", "language": "es", "sourceCharacters": 72, "targetChaaracters": 72} ] } ]
```

***Response Header***

```bash
"sourceCharactersCharged": 72 
"targetCharactersCharged": 72
```

#### Text translation request using custom translation

***Request***

```bash
[ { "text": "Doctor is available next Monday. Do you want to schedule an appointment?", "targets": [ {     "language": "es", "model": "CT-model-en-es-hr-020"} ] } ]
```

***Response***

```bash
[ { "detectedLanguage": { "language": "en", "score": 1     }, "translations": [ { "text": "La médica estará disponible el próximo lunes. ¿Desea programar una cita?", "language": "es", "sourceCharacters": 72} ]   } ]
```

***Response Header***

```bash
"sourceCharactersCharged": 72
```




