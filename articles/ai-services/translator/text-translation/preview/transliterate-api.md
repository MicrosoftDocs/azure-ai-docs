---
title: Azure AI Translator 2025-05-01-preview transliterate method
titleSuffix: Azure AI services
description: Convert text from one script to another script with the Azure AI Translator 2025-05-01-preview transliterate method.
author: laujan
manager: nitinme
ms.service: azure-ai-translator
ms.topic: reference
ms.date: 09/04/2025
ms.author: lajanuar
---

# Transliterate (2025-05-01-preview)

The Text transliteration API maps your source language script or alphabet to a target language script or alphabet.

## Request URL

Send a `POST` request to:

```bash
https://api.cognitive.microsofttranslator.com/transliterate?api-version=2025-05-01-preview
```

For more information on Translator service selected network and private endpoint configuration and support, *see* [**Virtual Network Support**](../reference/authentication.md#virtual-network-support).

## Request headers

Request headers include:

| Headers | Description |
| --- | --- |
| **Authentication headers** | _Required request header_.<br/>See [available options for authentication](../reference/authentication.md). |
| **Content-Type** | _Required request header_.<br/>Specifies the content type of the payload. Accepted values are: `application/json`; `charset=UTF-8`|
| **Content-Length** | _Optional_.<br/>The length of the request body. |
| **X-ClientTraceId** | _Optional_.<br/>A client-generated GUID to uniquely identify the request. You can omit this optional header if you include the trace ID in the query string using a query parameter named `ClientTraceId`. |


#### Request parameters

Request parameters passed with the request are as follows:

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
|**api-version**|string|True|Version of the API requested by the client. Accepted value is 2025-05-01-preview.|
|**text** | string | True | Source text for translation. |
| **textType** | string | False | Defines whether the text being translated is plain text or HTML text. Any HTML needs to be a well-formed, complete element. Accepted values are: plain (default) or html. |
| **language** | string | False | Specifies the language code for the `source` text. If not specified, the system autodetects the language of the source text. Accepted values are list of language code supported by the specified model. |
| **script** | string | False | **Specifies the script of the source text**. |
| **targets** | array | True | User-specified values for the translated (target) text. |
| **targets.language** | string | True |The language code for the translated (target) text *specified in the targets array*. Accepted values are [supported language](../../../language-support.md) codes for the translation operation.|


#### Targets array (user-specified values for translated text)

| Parameter | Type | Required? | Description |
| --- | --- | --- | --- |
| **targets.language** | string | True |The language code for the translated (`target`) text *specified in the `targets` array*. Accepted values are [supported language](../../../language-support.md) codes for the translation operation.|
| **targets.script** | string | False | Specify the script of the transliterated text. |
| **targets.allowFallback** | string | False | If the desired model doesn't support a particular pair of source and target languages, an alternative approach may be employed. In such cases, the service may default to utilizing a general system as a substitute. This action ensures that translations can still be provided even when the preferred model is unavailable. Default is `true`. If `false` system returns an error if language pair isn't supported. |

## Request body

The body of the request is a JSON array. Each array element is a JSON object with a string property named `Text`, which represents the string to convert.

```json
[
    {"Text":"こんにちは"},
    {"Text":"さようなら"}
]
```

The following limitations apply:

* The array can have at most 10 elements.
* The text value of an array element can't exceed 1,000 characters including spaces.
* The entire text included in the request can't exceed 5,000 characters including spaces.

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

       An example JSON response is:

       ```json
       [
           {"text":"konnnichiha","script":"Latn"},
           {"text":"sayounara","script":"Latn"}
       ]
       ```

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

The following example shows how to convert two Japanese strings into Romanized Japanese.

The JSON payload for the request in this example:

```json
[{"text":"こんにちは","script":"jpan"},{"text":"さようなら","script":"jpan"}]
```

If you're using cURL in a command-line window that doesn't support Unicode characters, take the following JSON payload and save it into a file named `request.txt`. Be sure to save the file with `UTF-8` encoding.

```
curl -X POST "https://api.cognitive.microsofttranslator.com/transliterate?api-version=2025-05-01-preview&language=ja&fromScript=Jpan&toScript=Latn" -H "X-ClientTraceId: 875030C7-5380-40B8-8A03-63DACCF69C11" -H "Ocp-Apim-Subscription-Key: <client-secret>" -H "Content-Type: application/json" -d @request.txt
```
