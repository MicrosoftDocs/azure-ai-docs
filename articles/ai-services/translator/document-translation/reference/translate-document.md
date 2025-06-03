---
title: Synchronous Azure AI Translator translation REST API guide
description: "Synchronous translation HTTP REST API guide"
author: laujan
manager: nitinme
ms.service: azure-ai-translator
ms.topic: quickstart
ms.date: 04/14/2025
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
Feature: **Azure AI Translator → Document translation**</br>
API Version: **2024-05-01**</br>
HTTP method: **POST**

* Use the `translate document` method to synchronously translate a single document.
* The method doesn't require an Azure Blob storage account.
* The final response contains the translated document and is returned directly to the calling client.

> [!IMPORTANT]
>
> **All API requests to the Document translation feature require a custom domain endpoint that is located on your resource overview page in the Azure portal**.

## Request URL

```bash
curl -i -X POST "{your-document-translation-endpoint}/translator/document:translate?sourceLanguage=en&targetLanguage=hi&api-version={date}" -H "Ocp-Apim-Subscription-Key:{your-key}"  -F "document={path-to-your-document-with-file-extension};type={ContentType}/{file-extension}" -F "glossary={path-to-your-glossary-with-file-extension};type={ContentType}/{file-extension}" -o "{path-to-output-file}"

```

## Request headers

To call the synchronous translation feature via the REST API, include the following headers with each request.

|Header|Value| Condition  |
|---|:--- |:---|
|**Ocp-Apim-Subscription-Key** |Your Translator service key from the Azure portal.|&bullet; ***Required***|

## Request parameters

Query string parameters:

### Required parameters

|Query parameter | Description |
| --- | --- |
|**api-version** | _Required parameter_.<br>Version of the API requested by the client. Current value is `2024-05-01`. |
|**targetLanguage**|_Required parameter_.<br>Specifies the language of the output document. The target language must be one of the supported languages included in the translation scope.|
|&bull; **document=**<br> &bull; **type=**|_Required parameters_.<br>&bull; Path to the file location for your source document and file format type.</br> &bull; Ex: **"document=@C:\Test\Test-file.txt;type=text/html**|
|**--output**|_Required parameter_.<br> &bull; File path for the target file location. Your translated file is printed to the output file.</br> &bull; Ex: **"C:\Test\Test-file-output.txt"**. The file extension should be the same as the source file.|

### Optional parameters

|Query parameter | Description |
| --- | --- |
|**sourceLanguage**|Specifies the language of the input document. If the `sourceLanguage` parameter isn't specified, automatic language detection is applied to determine the source language.|
|&bull; **glossary=**<br> &bull; **type=**|&bull; Path to the file location for your custom glossary and file format type.</br> &bull; Ex:**"glossary=@D:\Test\SDT\test-simple-glossary.csv;type=text/csv**|
|**allowFallback**|&bull; A boolean specifying that the service is allowed to fall back to a `generalnn` system when a custom system doesn't exist. Accepted values are: `true` (default) or `false`. <br>&bull; `allowFallback=false` specifies that the translation should only use systems trained for the category specified  by the request.<br>&bull; If no system is found with the specific category, the request returns a 400 status code. <br>&bull; `allowFallback=true` specifies that the service is allowed to fall back to a `generalnn` system when a custom system doesn't exist.|
|**category**|A string specifying the category (domain) for the translation. This parameter is used to get translations from a customized system built with [Custom Translator](../../custom-translator/how-to/translate-with-custom-model.md#how-to-translate). To use your deployed customized system for synchronous document translation, add the `Category ID` from your Custom Translator project details to the `category` parameter. The default value is: `generalnn`.|

### Request Body

|Name |Description|Content Type|Condition|
|---|---|---|---|
|**document**| Source document to be translated.|Any one of the [supported document formats](../overview.md#synchronous-supported-document-formats).|***Required***|
|**glossary**|Document containing a list of terms with definitions to use during the translation process.|Any one of the supported [glossary formats](get-supported-glossary-formats.md).|***Optional***|

## Next steps

> [!div class="nextstepaction"]
> [Try the document translation quickstart](../quickstarts/client-library-sdks.md "Learn more about batch translation for multiple files.")
