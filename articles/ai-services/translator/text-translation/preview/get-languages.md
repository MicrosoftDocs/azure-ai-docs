---
title: Translator 2025-10-01-preview languages method
titleSuffix: Foundry Tools
description: The languages method displays the set of languages currently supported by Azure Translator in Foundry Tools 2025-10-01-preview.
author: laujan
manager: nitinme
ms.service: azure-ai-translator
ms.topic: reference
ms.date: 11/18/2025
ms.author: lajanuar
---

<!-- markdownlint-disable MD033 -->

# Languages (2025-10-01-preview)

Get the set of languages currently supported by the latest Azure Translator version.
## Request URL

Send a `GET` request to:

```bash
https://api.cognitive.microsofttranslator.com/languages?api-version=2025-10-01-preview

```

For virtual networks, use your custom domain endpoint:

```bash
https://<your-custom-domain>.cognitiveservices.azure.com/languages?api-version=2025-10-01-preview
```

For more information on Translator selected network and private endpoint configuration and support, *see* [**Virtual Network Support**](../reference/authentication.md#virtual-network-support).

## Request parameters

Request parameters passed on the query string are:

|Query parameters|Description|
|---|---|
|api-version|**Required parameter**<br><br>The version of the API requested by the client. Value must be `2025-10-01-preview`.|
|scope|**Optional parameter**.<br><br>A comma-separated list of names defining the group of languages to return. Allowed group names are: `translation`,`transliteration`, and `models`. If no scope is given, then all groups are returned, which is equivalent to passing `scope=translation,transliteration,models`.|

*See* [response body](#response-body).

Request headers are:

|Headers|Description|
|---|---|
|Accept-Language|**Optional request header**.<br><br>The language to use for user interface strings. Some of the fields in the response are names of languages or names of regions. Use this parameter to define the language in which these names are returned. The language is specified by providing a well-formed `BCP` 47 language tag. For instance, use the value `fr` to request names in French or use the value `zh-Hant` to request names in Chinese Traditional.<br/>Names are provided in the English language when a target language isn't specified or when localization isn't available.|
|X-ClientTraceId|**Optional request header**.<br>A client-generated GUID to uniquely identify the request.|

Authentication isn't required to get language resources.

## Response body

A client uses the `scope` query parameter to define which groups of languages to list.

* `scope=translation` provides languages supported to translate text from one language to another language;

* `scope=transliteration` provides capabilities for converting text in one language from one script to another script;

* `scope=models` provides list of available LLM models.

A client may retrieve several groups simultaneously by specifying a comma-separated list of names. For example, `scope=translation,transliteration,models` would return supported languages for all groups.

A successful response is a JSON object with one property for each requested group:

```json
{
    "translation": {
        //... set of languages supported to translate text (scope=translation)
    },
    "transliteration": {
        //... set of languages supported to convert between scripts (scope=transliteration)
    },
    "models": {
        //... set of supported LLM models
    }
}
```

The value for each property is as follows.

* `translation` property

  The value of the `translation` property is an associative array of (key, value) pairs. Each key is a `BCP` 47 language tag. A key identifies a language for which text can be translated to or translated from. The value associated with the key is a JSON object with properties that describe the language:

  * `name`: Display name of the language in the locale requested via `Accept-Language` header.

  * `nativeName`: Display name of the language in the locale native for this language.

  * `dir`: Directionality, which is `rtl` for right-to-left languages or `ltr` for left-to-right languages.

  An example is:

  ```json
  {
    "translation": {
      ...
      "fr": {
        "name": "French",
        "nativeName": "Français",
        "dir": "ltr"
      },
      ...
    }
  }
  ```

* `transliteration` property

  The value of the `transliteration` property is an associative array of (key, value) pairs. Each key is a `BCP` 47 language tag. A key identifies a language for which text can be converted from one script to another script. The value associated with the key is a JSON object with properties that describe the language and its supported scripts:

  * `name`: Display name of the language in the locale requested via `Accept-Language` header.

  * `nativeName`: Display name of the language in the locale native for this language.

  * `scripts`: List of scripts to convert from. Each element of the `scripts` list has properties:

    * `code`: Code identifying the script.

    * `name`: Display name of the script in the locale requested via `Accept-Language` header.

    * `nativeName`: Display name of the language in the locale native for the language.

    * `dir`: Directionality, which is `rtl` for right-to-left languages or `ltr` for left-to-right languages.

    * `toScripts`: List of scripts available to convert text to. Each element of the `toScripts` list has properties `code`, `name`, `nativeName`, and `dir` as described earlier.

  An example is:

  ```json
  {
    "transliteration": {
      ...
      "ja": {
        "name": "Japanese",
        "nativeName": "日本語",
        "scripts": [
          {
            "code": "Jpan",
            "name": "Japanese",
            "nativeName": "日本語",
            "dir": "ltr",
            "toScripts": [
              {
                "code": "Latn",
                "name": "Latin",
                "nativeName": "ラテン語",
                "dir": "ltr"
              }
            ]
          },
          {
            "code": "Latn",
            "name": "Latin",
            "nativeName": "ラテン語",
            "dir": "ltr",
            "toScripts": [
              {
                "code": "Jpan",
                "name": "Japanese",
                "nativeName": "日本語",
                "dir": "ltr"
              }
            ]
          }
        ]
      },
      ...
    }
  }
  ```

The structure of the response object doesn't change without a change in the version of the API. For the same version of the API, the list of available languages may change over time because Microsoft Translator continually extends the list of languages supported by its services.

The list of supported languages doesn't change frequently. To save network bandwidth and improve responsiveness, a client application should consider caching language resources and the corresponding entity tag (`ETag`). Then, the client application can periodically (for example, once every 24 hours) query the service to fetch the latest set of supported languages. Passing the current `ETag` value in an `If-None-Match` header field allows the service to optimize the response. If the resource isn't modified, the service returns status code 304 and an empty response body.

## Response headers

|Headers|Description|
|--- |--- |
|ETag|Current value of the entity tag for the requested groups of supported languages. To make subsequent requests more efficient, the client may send the `ETag` value in an `If-None-Match` header field.|
|X-RequestId|Value generated by the service to identify the request. It's used for troubleshooting purposes.|

## Response status codes

If an error occurs, the request also returns a JSON error response. The error code is a 6-digit number combining the 3-digit HTTP status code followed by a 3-digit number to further categorize the error. Common error codes can be found on the [Translator status code reference page](../reference/status-response-codes.md).

## Examples

The following example shows how to retrieve languages supported for text translation.

 ```bash
curl "https://api.cognitive.microsofttranslator.com/languages?api-version=2025-10-01-preview&scope=translation"
```

## Related content

For more information, *see* [Language support](../../../language-support.md).
