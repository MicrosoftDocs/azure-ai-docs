---
title: Start translation
titleSuffix: Foundry Tools
description: Start a document translation request with the Document translation service.
manager: nitinme
ms.author: lajanuar
author: laujan
ms.service: azure-ai-translator
ms.topic: reference
ms.date: 11/18/2025
---

# Start batch translation

<!-- markdownlint-disable MD036 -->

**Reference**</br>
Feature: **Azure Translator → Document translation**</br>
API Version (GA): **2024-05-01** </br>
API Version (preview): **2025-12-01-preview**—adds support for [image file translation](#translate-image-files).</br>
HTTP method: **POST**

* Use the `Start Translation` method to execute an asynchronous batch translation request.
* The method requires an Azure Blob storage account with storage containers for your source and translated documents.

## Request URL

> [!IMPORTANT]
>
> **All API requests to the Document translation feature require a custom domain endpoint that's located on your resource overview page in the Azure portal**.

```bash
  curl -i -X POST "{document-translation-endpoint}/translator/document/batches?api-version={date}"

```

## Request headers

Request headers are:

|Headers|Description|Condition|
|--- |--- |---|
|**Ocp-Apim-Subscription-Key**|Your Translator API key from the Azure portal.|***Required***|
|**Ocp-Apim-Subscription-Region**|The region where your resource was created. |***Required*** when using a regional (geographic) resource like **West US**.</br>&bullet.|
|**Content-Type**|The content type of the payload. The accepted value is **application/json** or **charset=UTF-8**.|***Required***|

## BatchRequest (body)

* Each request can contain multiple documents and must contain a source and target container for each document. Source media types: `application/json`, `text/json`, `application/*+json`.

* The prefix and suffix filter (if supplied) are used to filter folders. The prefix is applied to the subpath after the container name.

* Glossaries can be included in the request. If the glossary is invalid or unreachable during translation, an error is indicated in the document status.

* If a file with the same name already exists in the target destination, the job fails.

* The targetUrl for each target language must be unique.

```json

{
  "inputs": [
    {
      "source": {
        "sourceUrl": "https://myblob.blob.core.windows.net/Container/",
        "filter": {
          "prefix": "FolderA",
          "suffix": ".txt"
        },
        "language": "en",
        "storageSource": "AzureBlob"
      },
      "targets": [
        {
          "targetUrl": "https://myblob.blob.core.windows.net/TargetUrl/",
          "category": "general",
          "language": "fr",
          "glossaries": [
            {
              "glossaryUrl": "https://myblob.blob.core.windows.net/Container/myglossary.xlf",
              "format": "XLIFF",
              "version": "2.0",
              "storageSource": "AzureBlob"
            }
          ],
          "storageSource": "AzureBlob"
        }
      ],
      "storageType": "Folder"
    }
  ],
}

```

## Inputs

Definition for the input batch translation request.

|Key parameter|Type|Required|Request parameters|Description|
|--- |---|---|---|--|
|**inputs**| `array`|True|&bullet; source (object)</br></br>&bullet; targets (array)</br></br>&bullet; storageType (string)|Input source data.|

### inputs.source

Definition for the source data.

|Key parameter|Type|Required|Request parameters|Description|
|--- |---|---|---|--|
|**inputs.source** |`object`|True|&bullet; sourceUrl (string)</br></br>&bullet; filter (object)</br></br>&bullet; language (string)</br></br>&bullet; storageSource (string)|Source data for input documents.|
|**inputs.source.sourceUrl**|`string`|True|&bullet; string|Container location for the source file or folder.|
|**inputs.source.filter**|`object`|False|&bullet; prefix (string)</br></br>&bullet; suffix (string)|Case-sensitive strings to filter documents in the source path.|
|**inputs.source.filter.prefix**|`string`|False|&bullet; string|Case-sensitive prefix string to filter documents in the source path for translation. Often used to designate subfolders for translation. Example: "_FolderA_".|
|**inputs.source.filter.suffix**|`string`|False|&bullet; string|Case-sensitive suffix string to filter documents in the source path for translation. Most often used for file extensions. Example: "_.txt_"|
|**inputs.source.language**|`string`|False|&bullet; string|The language code for the source documents. If not specified, autodetect is implemented.
|**inputs.source.storageSource**|`string`|False|&bullet; string|Storage source for inputs. Defaults to `AzureBlob`.|

### inputs.targets

Definition for target and glossaries data.

|Key parameter|Type|Required|Request parameters|Description|
|--- |---|---|---|--|
|**inputs.targets**|`array`|True|&bullet; targetUrl (string)</br></br>&bullet; category (string)</br></br>&bullet; language (string)</br></br>&bullet; glossaries (array)</br></br>&bullet; storageSource (string)|Targets and glossaries data for translated documents.|
|**inputs.targets.targetUrl**|`string`|True|&bullet; string|Location of the container location for translated documents.|
|**inputs.targets.category**|`string`|False|&bullet; string|Classification or category for the translation request. Example: _general_.|
|**inputs.targets.language**|`string`|True|&bullet; string|Target language code. Example: "_fr_".|
|**inputs.targets.glossaries**|`array`|False|&bullet; glossaryUrl (string)</br></br>&bullet; format (string)</br></br>&bullet; version (string)</br></br>&bullet; storageSource (string)|_See_ [Create and use glossaries](../how-to-guides/create-use-glossaries.md)|
|**inputs.targets.glossaries.glossaryUrl**|`string`|True (if using glossaries)|&bullet; string|Location of the glossary. The file extension is used to extract the formatting if the format parameter isn't supplied. If the translation language pair isn't present in the glossary, it isn't applied.|
|**inputs.targets.glossaries.format**|`string`|False|&bullet; string|Specified file format for glossary. To check if your file format is supported, _see_ [Get supported glossary formats](get-supported-glossary-formats.md).|
|**inputs.targets.glossaries.version**|`string`|False|&bullet; string|Version indicator. Example: "_2.0_".|
|**inputs.targets.glossaries.storageSource**|`string`|False|&bullet; string|Storage source for glossaries. Defaults to `_AzureBlob_`.|
|**inputs.targets.storageSource**|`string`|False|&bullet; string|Storage source for targets.defaults to `_AzureBlob_`.|

### inputs.storageType

Definition of the storage entity for input documents.

|Key parameter|Type|Required|Request parameters|Description|
|--- |---|---|---|--|
|**inputs.storageType**|`string`|False|&bullet;`Folder`</br></br>&bullet; `File`|Storage type of the input documents source string. Only "_Folder_" or "_File_" are valid values.|

## Options

Definition for the input batch translation request.

|Key parameter|Type|Required|Request parameters|Description|
|--- |---|---|---|--|
|**options**|`object`|False|Source information for input documents.|
|**options.experimental**|`boolean`|False|&bullet;`true`</br></br>&bullet; `false`|Indicates whether the request includes an experimental feature (if applicable). Only the booleans _`true`_ or _`false`_ are valid values.|

## Example request

The following are examples of batch requests.

> [!NOTE]
> In the following examples, limited access is granted to the contents of an Azure Storage container [using a shared access signature(SAS)](/azure/storage/common/storage-sas-overview) token.

### Translate all documents in a container

```json
{
    "inputs": [
        {
            "source": {
                "sourceUrl": "https://my.blob.core.windows.net/source-en?{SAS-token-query-string}"
            },
            "targets": [
                {
                    "targetUrl": "https://my.blob.core.windows.net/target-fr?{SAS-token-query-string}",
                    "language": "fr"
                }
            ]
        }
    ]
}
```

### Translate a specific document in a container

* Specify "storageType": `File`.
* Create source URL & SAS token for the specific blob/document.
* Specify the target filename as part of the target URL – though the SAS token is still for the container.

This sample request shows a single document translated into two target languages.

```json
{
    "inputs": [
        {
            "storageType": "File",
            "source": {
                "sourceUrl": "https://my.blob.core.windows.net/source-en/source-english.docx?{SAS-token-query-string}"
            },
            "targets": [
                {
                    "targetUrl": "https://my.blob.core.windows.net/target/try/Target-Spanish.docx?{SAS-token-query-string}",
                    "language": "es"
                },
                {
                    "targetUrl": "https://my.blob.core.windows.net/target/try/Target-German.docx?{SAS-token-query-string}",
                    "language": "de"
                }
            ]
        }
    ]
}
```

> [!TIP]
> This method returns the job `id` parameter for the [get-translation-status](get-translation-status.md), [get-documents-status](get-documents-status.md), [get-document-status](get-document-status.md), and [cancel-translation](cancel-translation.md) request query strings.

* You can find the job `id`  in the POST `start-batch-translation` method response Header `Operation-Location`  URL value. The alphanumeric string following the `/document/` parameter is the operation's job **`id`**:

    |**Response header**|**Response URL**|
    |-----------------------|----------------|
    |Operation-Location   | {document-translation-endpoint}/translator/document/`9dce0aa9-78dc-41ba-8cae-2e2f3c2ff8ec`?api-version=2024-05-01|

* You can also use a [get-translations-status](../reference/get-translations-status.md) request to retrieve a list of translation jobs and their `id`s.

### Translate all documents in a container applying glossaries

```json
{
    "inputs": [
        {
            "source": {
                "sourceUrl": "https://my.blob.core.windows.net/source-en?{SAS-token-query-string}"
            },
            "targets": [
                {
                    "targetUrl": "https://my.blob.core.windows.net/target-fr?{SAS-token-query-string}",
                    "language": "fr",
                    "glossaries": [
                        {
                            "glossaryUrl": "https://my.blob.core.windows.net/glossaries/en-fr.xlf?{SAS-token-query-string}",
                            "format": "xliff",
                            "version": "1.2"
                        }
                    ]

                }
            ]
        }
    ]
}
```

### Translate a specific folder in a container

Make sure you specify the folder name (case sensitive) as prefix in filter.

```json
{
    "inputs": [
        {
            "source": {
                "sourceUrl": "https://my.blob.core.windows.net/source-en?{SAS-token-query-string}",
                "filter": {
                    "prefix": "MyFolder/"
                }
            },
            "targets": [
                {
                    "targetUrl": "https://my.blob.core.windows.net/target-fr?{SAS-token-query-string}",
                    "language": "fr"
                }
            ]
        }
    ]
}
```
## Translate image files

 > [!IMPORTANT]
 > The Document Translation image translation feature is a "preview" licensed to you as part of your Azure subscription. This release is subject to terms applicable to "Previews" in the [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms) and the [Microsoft Products and Services Data Protection Addendum (DPA)](https://www.microsoft.com/licensing/docs/view/microsoft-products-and-services-data-protection-addendum-dpa).

### Request configuration (image files)

For image files translation, submit your image via a standard batch [Document Translation REST API call](#translate-all-documents-in-a-container), specifying API version **2025-12-01-preview**. No further configuration is required.

### Supported formats (image files)
|File Extension|Description|
|--|--|
|`.bmp `|A bitmap image file format used to store digital images in an uncompressed form, preserving high-quality visual details.|
|`.jpeg` |A Joint Photographic Experts Group image file that uses a lossy compression method to reduce file size. This format doesn't support transparent backgrounds.|
|`.png`| A Portable Network Graphics file that uses lossless compression, supports transparency, and can display up to 16 million color.|
|`.webp`|A Web Picture image format that uses both lossy and lossless image compression methods to minimize file size while preserving high image quality.|

### Supported languages (image files)

For details on supported languages, *see* [Document Translation language support](../../language-support.md#document-translation-scanned-pdf-and-image-support).

## Response status codes

The following are the possible HTTP status codes that a request returns.

|Status Code|Description|
|--- |--- |
|202|Accepted. Successful request and the batch request created. The header Operation-Location indicates a status url with the operation ID.HeadersOperation-Location: string|
|400|Bad Request. Invalid request. Check input parameters.|
|401|Unauthorized. Check your credentials.|
|429|Request rate is too high.|
|500|Internal Server Error.|
|503|Service is currently unavailable. Try again later.|
|Other Status Codes|&bullet; Too many requests. The server is temporary unavailable|

## Error response

|Key parameter|Type|Description|
|--- |--- |--- |
|code|`string`|Enums containing high-level error codes. Accepted values:</br/>&bullet; InternalServerError</br>&bullet; InvalidArgument</br>&bullet; InvalidRequest</br>&bullet; RequestRateTooHigh</br>&bullet; ResourceNotFound</br>&bullet; ServiceUnavailable</br>&bullet; Unauthorized|
|message|`string`|Gets high-level error message.|
|innerError|InnerTranslationError|New Inner Error format that conforms to Foundry Tools API Guidelines. This error message contains required properties: ErrorCode, message, and optional properties target, details(key value pair), and inner error(it can be nested).|
|inner.Errorcode|`string`|Gets code error string.|
|innerError.message|`string`|Gets high-level error message.|
|innerError.target|`string`|Gets the source of the error. For example, it would be `documents` or `document id` if the document is invalid.|

### Example error response

```JSON
{
  "error": {
    "code": "ServiceUnavailable",
    "message": "Service is temporary unavailable",
    "innerError": {
      "code": "ServiceTemporaryUnavailable",
      "message": "Service is currently unavailable.  Please try again later"
    }
  }
}
```

## Next steps

Follow our quickstart to learn more about using Document translation and the client library.

> [!div class="nextstepaction"]
> [Get started with Document translation](../how-to-guides/use-rest-api-programmatically.md)
