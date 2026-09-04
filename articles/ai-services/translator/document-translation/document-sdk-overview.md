---
title: Document translation SDKs
titleSuffix: Foundry Tools
description: Use the Document translation SDKs for C#, Java, JavaScript, and Python to add batch and synchronous document translation to your applications.
author: laujan
manager: mcleans
ms.service: azure-translator-foundry-tools
ms.custom: devx-track-dotnet, devx-track-js, devx-track-python, devx-track-java
ms.topic: how-to
ms.date: 08/07/2026
ms.author: lajanuar
recommendations: false
ai-usage: ai-assisted
---

<!-- markdownlint-disable MD024 -->
<!-- markdownlint-disable MD036 -->
<!-- markdownlint-disable MD001 -->
<!-- markdownlint-disable MD051 -->
<!-- markdownlint-disable MD025 -->
# Document translation SDKs

Document translation is a cloud-based feature of Azure Translator in Foundry Tools. It supports asynchronous batch translation and synchronous single-document translation across supported languages and file formats. The Document translation software development kits (SDKs) help you integrate these REST API capabilities into your applications.

## Prerequisites

To use a Document translation SDK, you need:

* An active [Azure subscription](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
* A [single-service Azure Translator resource](https://portal.azure.com/#create/Microsoft.CognitiveServicesTextTranslation).
* The custom endpoint and key for your Translator resource.
* For asynchronous batch translation, an Azure Blob Storage account with source and target containers. For authorization options, see [Storage container authorization](quickstarts/client-library-sdks.md#storage-container-authorization).

## Supported languages

Document translation SDK supports the following programming languages:

| Language and SDK version | Package | Client library | Default API version |
| --- | --- | --- | --- |
| `.NET/C# 3.0.0` | [NuGet](https://www.nuget.org/packages/Azure.AI.Translation.Document/3.0.0) | [Azure SDK for .NET](/dotnet/api/overview/azure/ai.translation.document-readme?view=azure-dotnet&preserve-view=true) | `2026-03-01` |
| `Python 2.0.0` | [PyPI](https://pypi.org/project/azure-ai-translation-document/2.0.0/) | [Azure SDK for Python](/python/api/overview/azure/ai-translation-document-readme?view=azure-python&preserve-view=true) | `2026-03-01` |
| `JavaScript/TypeScript 1.0.0` | [npm](https://www.npmjs.com/package/@azure/ai-translation-document/v/1.0.0) | [Azure SDK for JavaScript](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/translation/ai-translation-document/README.md) | `2026-03-01` |
| `Java 2.0.0` | [Maven Central](https://central.sonatype.com/artifact/com.azure/azure-ai-translation-document/2.0.0) | [Azure SDK for Java](/java/api/overview/azure/ai-translation-document-readme?view=azure-java-stable&preserve-view=true) | `2026-03-01` |

## Changelog and release history

This section provides a version-based description of Document translation feature and capability releases, changes, updates, and enhancements.

### [.NET/C#](#tab/csharp)

**Version 3.0.0** </br>

##### [**Changelog/Release History**](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/translation/Azure.AI.Translation.Document/CHANGELOG.md#300-2026-08-01)

##### [README](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/translation/Azure.AI.Translation.Document/README.md)

##### [Samples](https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/translation/Azure.AI.Translation.Document/samples)

### [Python](#tab/python)

**Version 2.0.0** </br>

##### [**Changelog/Release History**](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/translation/azure-ai-translation-document/CHANGELOG.md)

##### [README](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/translation/azure-ai-translation-document/README.md)

##### [Samples](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/translation/azure-ai-translation-document/samples)

### [JavaScript/TypeScript](#tab/javascript)

**Version 1.0.0** </br>

##### [**Changelog/Release History**](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/translation/ai-translation-document/CHANGELOG.md#100-2026-08-01)

##### [README](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/translation/ai-translation-document/README.md)

##### [Samples](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/translation/ai-translation-document/samples)

### [Java](#tab/java)

**Version 2.0.0** </br>

##### [**Changelog/Release History**](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/translation/azure-ai-translation-document/CHANGELOG.md)

##### [README](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/translation/azure-ai-translation-document/README.md)

##### [Samples](https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/translation/azure-ai-translation-document/src/samples/java/com/azure/ai/translation/document)

---

## Use Document translation SDK in your applications

The Document translation SDK enables the use and management of the Translation service in your application. The SDK builds on the underlying Document translation REST APIs for use within your programming language paradigm. Choose your preferred programming language:

### 1. Install the SDK client library

### [.NET/C#](#tab/csharp)

```dotnetcli
dotnet add package Azure.AI.Translation.Document --version 3.0.0
```

```powershell
Install-Package Azure.AI.Translation.Document -Version 3.0.0
```

### [Python](#tab/python)

```bash
pip install azure-ai-translation-document==2.0.0
```

### [JavaScript/TypeScript](#tab/javascript)

```bash
npm install @azure/ai-translation-document@1.0.0
```

### [Java](#tab/java)

```xml
<dependency>
  <groupId>com.azure</groupId>
  <artifactId>azure-ai-translation-document</artifactId>
  <version>2.0.0</version>
</dependency>
```

---

### 2. Import the SDK client library into your application

### [.NET/C#](#tab/csharp)

```csharp
using System;
using Azure.Core;
using Azure.AI.Translation.Document;
```

### [Python](#tab/python)

```python
from azure.ai.translation.document import DocumentTranslationClient
from azure.ai.translation.document import SingleDocumentTranslationClient
from azure.core.credentials import AzureKeyCredential
```

### [JavaScript/TypeScript](#tab/javascript)

```typescript
import {
  DocumentTranslationClient,
  SingleDocumentTranslationClient,
} from "@azure/ai-translation-document";
import type { KeyCredential } from "@azure/core-auth";
```

### [Java](#tab/java)

```java
import com.azure.ai.translation.document.DocumentTranslationClient;
import com.azure.ai.translation.document.DocumentTranslationClientBuilder;
import com.azure.ai.translation.document.SingleDocumentTranslationClient;
import com.azure.ai.translation.document.SingleDocumentTranslationClientBuilder;
import com.azure.core.credential.AzureKeyCredential;
```

---

### 3. Authenticate the client

### [.NET/C#](#tab/csharp)

Create an instance of the `DocumentTranslationClient` object to interact with the Document translation SDK, and then call methods on that client object to interact with the service. The `DocumentTranslationClient` is the primary interface for using the Document translation client library. It provides both synchronous and asynchronous methods to perform operations.

***Asynchronous batch translation***

```csharp
private static readonly string endpoint = "<your-custom-endpoint>";
private static readonly string key = "<your-key>";

DocumentTranslationClient client = new DocumentTranslationClient(new Uri(endpoint), new AzureKeyCredential(key));

```

***Synchronous single document translation***

```csharp
private static readonly string endpoint = "<your-custom-endpoint>";
private static readonly string key = "<your-key>";

SingleDocumentTranslationClient client = new SingleDocumentTranslationClient(new Uri(endpoint), new AzureKeyCredential(key));

```

### [Python](#tab/python)

Create an instance of the `DocumentTranslationClient` object to interact with the Document translation SDK, and then call methods on that client object to interact with the service. The `DocumentTranslationClient` is the primary interface for using the Document translation client library. It provides both synchronous and asynchronous methods to perform operations.

***Asynchronous batch translation***

```python
endpoint = "<endpoint>"
key = "<api-key>"

client = DocumentTranslationClient(endpoint, AzureKeyCredential(key))

```

***Synchronous single document translation***

```python
endpoint = "<endpoint>"
key = "<api-key>"

client = SingleDocumentTranslationClient(endpoint, AzureKeyCredential(key))
```

### [JavaScript/TypeScript](#tab/javascript)

Create a `DocumentTranslationClient` for batch translation or a
`SingleDocumentTranslationClient` for synchronous translation.

***Asynchronous batch translation***

```typescript
const endpoint = "<endpoint>";
const credential: KeyCredential = { key: "<api-key>" };

const client = new DocumentTranslationClient(endpoint, credential);
```

***Synchronous single document translation***

```typescript
const endpoint = "<endpoint>";
const credential: KeyCredential = { key: "<api-key>" };

const client = new SingleDocumentTranslationClient(endpoint, credential);
```

### [Java](#tab/java)

Create a `DocumentTranslationClient` for batch translation or a `SingleDocumentTranslationClient` for synchronous translation.

***Asynchronous batch translation***

```java
String endpoint = "<endpoint>";
String key = "<api-key>";

DocumentTranslationClient client = new DocumentTranslationClientBuilder()
    .endpoint(endpoint)
    .credential(new AzureKeyCredential(key))
    .buildClient();
```

***Synchronous single document translation***

```java
String endpoint = "<endpoint>";
String key = "<api-key>";

SingleDocumentTranslationClient client =
    new SingleDocumentTranslationClientBuilder()
        .endpoint(endpoint)
        .credential(new AzureKeyCredential(key))
        .buildClient();

```

---

### 4. Build your application

### [.NET/C#](#tab/csharp)

***Asynchronous batch translation***

Document translation batch interfaces require the following input:

1. Upload your files to an Azure Blob Storage source container (sourceUri).
1. Provide a target container where the translated documents can be written (targetUri).
1. Include the target language code (targetLanguage).

```csharp

Uri sourceUri = new Uri("<your-source-container-url>");
Uri targetUri = new Uri("<your-target-container-url>");
string targetLanguage = "<target-language-code>";

DocumentTranslationInput input = new DocumentTranslationInput(sourceUri, targetUri, targetLanguage);
```

***Synchronous single document translation***

[Single document translation](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/translation/Azure.AI.Translation.Document/samples/Sample5_SynchronousTranslation.md)

### [Python](#tab/python)

***Asynchronous batch translation***

Document translation batch interfaces require the following input:

1. Upload your files to an Azure Blob Storage source container (sourceUri).
1. Provide a target container where the translated documents can be written (targetUri).
1. Include the target language code (targetLanguage).

```python
sourceUrl = "<your-source container-url>"
targetUrl = "<your-target-container-url>"
targetLanguage = "<target-language-code>"

poller = client.begin_translation(sourceUrl, targetUrl, targetLanguage)
result = poller.result()

```

***Synchronous single document translation***

[Single document translation](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/translation/azure-ai-translation-document/samples/sample_single_document_translation.py)

### [JavaScript/TypeScript](#tab/javascript)

***Asynchronous batch translation***

Batch translation requires source and target Azure Blob Storage container URLs.
Include SAS tokens in the URLs when your authorization configuration requires
them.

```typescript
const poller = client.startTranslation({
  inputs: [
    {
      source: { sourceUrl: "<source-container-url>" },
      targets: [
        {
          targetUrl: "<target-container-url>",
          language: "<target-language-code>",
        },
      ],
    },
  ],
});

const result = await poller.pollUntilDone();
console.log(`Translation status: ${result.status}`);
```

***Synchronous single document translation***

For a complete example, see [Synchronous document translation](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/translation/ai-translation-document/README.md#synchronous-document-translation).

### [Java](#tab/java)

The Java client library supports asynchronous batch translation and synchronous single-document translation. For complete examples, see the [Java samples](https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/translation/azure-ai-translation-document/src/samples/java/com/azure/ai/translation/document).

---

## Help options

The [`Microsoft Q&A`](/answers/tags/132/azure-translator) and [Stack Overflow](https://stackoverflow.com/questions/tagged/microsoft-translator) forums are available for the developer community to ask and answer questions about Azure Text translation and other services. Microsoft monitors the forums and replies to questions that the community has yet to answer.

> [!TIP]
> To make sure that we see your Microsoft `Q&A` question, tag it with **`microsoft-translator`**.
> To make sure that we see your Stack Overflow question, tag it with **`Azure Translator`**.
>

## Next steps

>[!div class="nextstepaction"]
> [**Document translation SDK quickstart**](quickstarts/client-library-sdks.md) [**Document translation v1.1 REST API reference**](reference/rest-api-guide.md).
