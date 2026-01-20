---
title: Synchronous Azure Translator translation REST API guide
description: "Synchronous translation HTTP REST API guide"
author: laujan
manager: nitinme
ms.service: azure-ai-translator
ms.topic: quickstart
ms.date: 12/05/2025
ms.author: lajanuar
recommendations: false
---

<!-- markdownlint-disable MD033 -->
<!-- markdownlint-disable MD001 -->
<!-- markdownlint-disable MD024 -->
<!-- markdownlint-disable MD036 -->
<!-- markdownlint-disable MD049 -->

# Synchronous document translation

Reference</br>
Feature: **Azure Translator → Document translation**</br>
API Version: **2024-05-01**</br>
HTTP method: **POST**

* Use the `translate document` method to synchronously translate a single document.
* The method doesn't require an Azure Blob storage account.
* The final response contains the translated document and is returned directly to the calling client.

> [!IMPORTANT]
>
> **All API requests to the Document translation feature require a custom domain endpoint that's located on your resource overview page in the Azure portal**.

## Request URL

```
https://{your-document-translation-endpoint}/translator/document:translate?api-version=2024-05-01&sourceLanguage=en&targetLanguage=fr
```

## Request headers

To call the synchronous translation feature via the REST API, include the following headers with each request.

|Header|Value| Condition  |
|---|:--- |:---|
|**Ocp-Apim-Subscription-Key** |Your Translator key from the Azure portal.|&bullet; ***Required***|

## Request parameters

### Required Query parameters

|Query parameter | Description |
| --- | --- |
|**api-version** | _Required parameter_.<br>Version of the API requested by the client. Current value is `2024-05-01`. |
|**targetLanguage**|_Required parameter_.<br>Specifies the language of the output document. The target language must be one of the supported languages included in the translation scope.|


### Optional Query parameters

|Query parameter | Description |
| --- | --- |
|**sourceLanguage**|Specifies the language of the input document. If the `sourceLanguage` parameter isn't specified, automatic language detection is applied to determine the source language.|
|**allowFallback**|&bull; A boolean specifying that the service is allowed to fall back to a `generalnn` system when a custom system doesn't exist. Accepted values are: `true` (default) or `false`. <br>&bull; `allowFallback=false` specifies that the translation should only use systems trained for the category specified  by the request.<br>&bull; If no system is found with the specific category, the request returns a 400 status code. <br>&bull; `allowFallback=true` specifies that the service is allowed to fall back to a `generalnn` system when a custom system doesn't exist.|
|**category**|A string specifying the category (domain) for the translation. This parameter is used to get translations from a customized system built with [Custom Translator](../../custom-translator/how-to/translate-with-custom-model.md#how-to-translate). To use your deployed customized system for synchronous document translation, add the `Category ID` from your Custom Translator project details to the `category` parameter. The default value is: `generalnn`.|
> [!NOTE]
> While `sourceLanguage` is optional, we strongly recommend specifying it explicitly. Providing the source language produces better quality translations than relying on automatic detection.

### Request Body

|Name |Description|Content Type|Condition|
|---|---|---|---|
|**document**| Source document to be translated.|Any one of the [supported document formats](../overview.md#supported-document-and-glossary-formats).|***Required***|
|**glossary**|Document containing a list of terms with definitions to use during the translation process.|Any one of the supported [glossary formats](get-supported-glossary-formats.md).|***Optional***|

### Response Status Codes

|Status Code| Description|
|---|---|
|200| The request was successful, and the translated document is returned.
|400 | Invalid or missing request parameters.
|401| Authentication failed. Check subscription key or token.
|429| Rate limits exceeded. Retry after a short delay.
|500| Unexpected service error. Retry or contact support with request details.
|503| Service temporarily unavailable. Retry later.

> [!NOTE]
> Errors return a JSON response including an `error` object.

**Example JSON Error Response**

```json
{
  "error": {
    "code": "InvalidRequest",
    "message": "The 'targetLanguage' parameter is required.",
    "innerError": {
      "requestId": "d3e4f6a9-0000-4a9b-8ad3-bdcd1323aa00",
      "date": "2025-10-15T10:05:23Z"
    }
  }
}
```

## Translate a Word document

```bash
curl --request POST \
  --url 'https://{your-document-translation-endpoint}/translator/document:translate?api-version=2024-05-01&sourceLanguage=en&targetLanguage=fr' \
  --header 'Ocp-Apim-Subscription-Key: <your-subscription-key>' \
  --form 'document=@<path-to-your-document>/your-document-file.docx' \
  --output translated-document-fr.docx
  
  ```
### Parameters

  | Parameter | Description |
|------------|-------------|
| `{your-document-translation-endpoint}` | Your Document Translation endpoint. Example: `https://your-resource-name.cognitiveservices.azure.com` |
| `<your-subscription-key>` | Your Translator subscription key. |
| `sourceLanguage` | *(Optional)* The source language code. Example: `en`. Autodetected if not specified. |
| `targetLanguage` | **(Required)** The target language code to translate into. Example: `fr`. |
| `document` | The path to the file to translate. |

For more information, *see* [Supported Document Formats](../overview.md).

## Translate a Word document with a Glossary

```bash
curl --request POST \
  --url 'https://{your-document-translation-endpoint}/translator/document:translate?api-version=2024-05-01&sourceLanguage=en&targetLanguage=fr' \
  --header 'Ocp-Apim-Subscription-Key: <your-subscription-key>' \
  --form 'document=@<path-to-your-document>/your-document-file.docx' \
  --form 'glossary=@<path-to-your-document>/glossary.tsv' \
  --output translated-document-fr.docx

```

### Parameters

| Parameter | Description |
|------------|-------------|
| `{your-document-translation-endpoint}` | Your Document Translation endpoint. Example: `https://your-resource-name.cognitiveservices.azure.com` |
| `<your-subscription-key>` | Your Translator subscription key. |
| `sourceLanguage` | *(Optional)* The source language code. Example: `en`. Autodetected if not specified. |
| `targetLanguage` | **(Required)** The target language code to translate into. Example: `fr`. |
| `document` | Path to the file for translation. |
| `glossary` | Path to the glossary file. |

For more information, *see* [Use glossaries with Document Translation](../how-to-guides/create-use-glossaries.md).


## Next steps

> [!div class="nextstepaction"]
> [Try the document translation quickstart](../quickstarts/client-library-sdks.md "Learn more about batch translation for multiple files.")
