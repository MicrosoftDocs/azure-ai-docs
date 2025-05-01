---
title: Document translation SDKs
titleSuffix: Azure AI services
description: Document translation software development kits (SDKs) expose Document translation features and capabilities, using C#, Java, JavaScript, and Python programming language.
author: laujan
manager: nitinme
ms.service: azure-ai-translator
ms.custom: devx-track-python
ms.topic: conceptual
ms.date: 04/14/2025
ms.author: lajanuar
recommendations: false
---

<!-- markdownlint-disable MD024 -->
<!-- markdownlint-disable MD036 -->
<!-- markdownlint-disable MD001 -->
<!-- markdownlint-disable MD051 -->

# Document translation SDKs

Document translation is a cloud-based REST API feature of the Azure AI Translator service. The Document translation API enables quick and accurate source-to-target whole document translations, asynchronously, in supported languages and various file formats. The Document translation software development kit (SDK) is a set of libraries and tools that enable you to easily integrate Document translation REST API capabilities into your applications.

## Supported languages

Document translation SDK supports the following programming languages:

| Language → SDK version | Package|Client library| Supported API version|
|:----------------------|:----------|:----------|:-------------|
|🆕 `.NET/C# → 2.0.0`| [NuGet](https://www.nuget.org/packages/Azure.AI.Translation.Document/2.0.0) | [Azure SDK for .NET](/dotnet/api/overview/azure/ai.translation.document-readme?view=azure-dotnet&preserve-view=true) | 
|🆕 `Python → 1.0.0`|[PyPi](https://pypi.org/project/azure-ai-translation-document/1.0.0/)|[Azure SDK for Python](/python/api/overview/azure/ai-translation-document-readme?view=azure-python-preview&preserve-view=true)|

## Changelog and release history

This section provides a version-based description of Document translation feature and capability releases, changes, updates, and enhancements.

### [C#/.NET](#tab/csharp)

**Version 2.0.0** </br>

##### [**Changelog/Release History**](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/translation/Azure.AI.Translation.Document/CHANGELOG.md#200-2024-11-15)

##### [README](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/translation/Azure.AI.Translation.Document/README.md)

##### [Samples](https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/translation/Azure.AI.Translation.Document/samples)

### [Python](#tab/python)

**Version 1.0.0** </br>

##### [**Changelog/Release History**](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/translation/azure-ai-translation-document/CHANGELOG.md)

##### [README](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/translation/azure-ai-translation-document/README.md)

##### [Samples](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/translation/azure-ai-translation-document/samples)

---

## Use Document translation SDK in your applications

The Document translation SDK enables the use and management of the Translation service in your application. The SDK builds on the underlying Document translation REST APIs for use within your programming language paradigm. Choose your preferred programming language:

### 1. Install the SDK client library

### [C#/.NET](#tab/csharp)

```dotnetcli
dotnet add package Azure.AI.Translation.Document --version 2.0.0
```

```powershell
Install-Package Azure.AI.Translation.Document -Version 2.0.0
```

### [Python](#tab/python)

```python
pip install azure-ai-translation-document==1.0.0
```

---

### 2. Import the SDK client library into your application

### [C#/.NET](#tab/csharp)

```csharp
using System;
using Azure.Core;
using Azure.AI.Translation.Document;
```

### [Python](#tab/python)

```python
from azure.ai.translation.document import DocumentTranslationClient
from azure.core.credentials import AzureKeyCredential
```

---

### 3. Authenticate the client

### [C#/.NET](#tab/csharp)

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

SingleDocumentTranslationClient client = new SingleDocumentTranslationClient(new Uri(endpoint), new AzureKeyCredential(apiKey));

```

### [Python](#tab/python)

Create an instance of the `DocumentTranslationClient` object to interact with the Document translation SDK, and then call methods on that client object to interact with the service. The `DocumentTranslationClient` is the primary interface for using the Document translation client library. It provides both synchronous and asynchronous methods to perform operations.

***Asynchronous batch translation***

```python
  endpoint = "<endpoint>"
  key = "<apiKey>"

  client = DocumentTranslationClient(endpoint, AzureKeyCredential(key))

```

***Synchronous single document translation***

```python
  endpoint = "<endpoint>"
  key = "<apiKey>"

  client = SingleDocumentTranslationClient(endpoint, AzureKeyCredential(key))

```

---

### 4. Build your application

### [C#/.NET](#tab/csharp)

***Asynchronous batch translation***

Document translation batch interfaces require the following input:

1. Upload your files to an Azure Blob Storage source container (sourceUri).
1. Provide a target container where the translated documents can be written (targetUri).
1. Include the target language code (targetLanguage).

```csharp

Uri sourceUri = new Uri("<your-source container-url");
Uri targetUri = new Uri("<your-target-container-url>");
string targetLanguage = "<target-language-code>";

DocumentTranslationInput input = new DocumentTranslationInput(sourceUri, targetUri, targetLanguage)
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

---

## Help options

The [`Microsoft Q&A`](/answers/tags/132/azure-translator) and [Stack Overflow](https://stackoverflow.com/questions/tagged/microsoft-translator) forums are available for the developer community to ask and answer questions about Azure Text translation and other services. Microsoft monitors the forums and replies to questions that the community has yet to answer.

> [!TIP]
> To make sure that we see your Microsoft `Q&A` question, tag it with **`microsoft-translator`**.
> To make sure that we see your Stack Overflow question, tag it with **`Azure AI Translator`**.
>

## Next steps

>[!div class="nextstepaction"]
> [**Document translation SDK quickstart**](quickstarts/client-library-sdks.md) [**Document translation v1.1 REST API reference**](reference/rest-api-guide.md)
