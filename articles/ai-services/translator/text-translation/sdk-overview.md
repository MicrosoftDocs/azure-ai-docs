---
title: Azure Text translation SDKs 
titleSuffix: Foundry Tools
description: Azure Text translation software development kits (SDKs) expose Text translation features and capabilities, using C#, Java, JavaScript, and Python programming language.
author: laujan
manager: nitinme
ms.service: azure-ai-translator
ms.custom: devx-track-python
ms.topic: how-to
ms.date: 11/18/2025
ms.author: lajanuar
recommendations: false
---

<!-- markdownlint-disable MD024 -->
<!-- markdownlint-disable MD036 -->
<!-- markdownlint-disable MD001 -->
<!-- markdownlint-disable MD051 -->

# Azure Translator in Foundry Tools SDK

Azure Translator is a cloud-based REST API feature of the Azure Translator. The Text translation API enables quick and accurate source-to-target text translations in real time. The Text translation software development kit (SDK) is a set of libraries and tools that enable you to easily integrate Text translation REST API capabilities into your applications. Text translation SDK is available across programming platforms in C#/.NET, Java, JavaScript, and Python.

## Supported languages

Text translation SDK supports the programming languages and platforms:

| Language → SDK version | Package|Client library| Supported API version|
|:----------------------:|:----------|:----------|:-------------|
|[.NET/C# → 1.0.0](https://github.com/Azure/azure-sdk-for-net/tree/Azure.AI.Translation.Text_1.0.0/sdk/translation/Azure.AI.Translation.Text/)|[NuGet](https://www.nuget.org/packages/Azure.AI.Translation.Text/1.0.0)|[Azure SDK for .NET](/dotnet/api/overview/azure/ai.translation.text-readme?view=azure-dotnet&preserve-view=true)|Translator v3.0|
|[Java&#x2731; → 1.0.0](https://github.com/Azure/azure-sdk-for-java/tree/azure-ai-translation-text_1.1.1/sdk/translation/azure-ai-translation-text/)|[Maven repository](https://mvnrepository.com/artifact/com.azure/azure-ai-translation-text/1.0.0)|[Azure SDK for Java](/java/api/overview/azure/ai-translation-text-readme?view=azure-java-stable&preserve-view=true)|Translator v3.0|
|[JavaScript → 1.0.0](https://github.com/Azure/azure-sdk-for-js/tree/@azure-rest/ai-translation-text_1.0.1/sdk/translation/ai-translation-text-rest/)|[npm](https://www.npmjs.com/package/@azure-rest/ai-translation-text/v/1.0.0)|[Azure SDK for JavaScript](/javascript/api/overview/azure/text-translation?view=azure-node-preview&preserve-view=true) |Translator v3.0 |
|[Python → 1.0.1](https://github.com/Azure/azure-sdk-for-python/tree/azure-ai-translation-text_1.0.1/sdk/translation/azure-ai-translation-text/)|[PyPi](https://pypi.org/project/azure-ai-translation-text/1.0.1/)|[Azure SDK for Python](/python/api/overview/azure/ai-translation-text-readme?view=azure-python&preserve-view=true) |Translator v3.0|

&#x2731; The Azure Translator SDK for Java is tested and supported on Windows, Linux, and macOS platforms. It isn't tested on other platforms and doesn't support Android deployments.

## Changelog and release history

This section provides a version-based description of Text translation feature and capability releases, changes, updates, and enhancements.

#### Azure Translator in Foundry Tools Text SDK May 2024 (GA) release

This release includes the following updates:

### [**C#**](#tab/csharp)

* **Version 1.0.0 (2024-05-21)**
* **Targets Text translation v3.0**
* **GA version release**

[**Package (NuGet)**](https://www.nuget.org/packages/Azure.AI.Translation.Text/1.0.0)

[**Changelog/Release History**](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/translation/Azure.AI.Translation.Text/CHANGELOG.md#100-2024-05-21)

[**README**](https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/translation/Azure.AI.Translation.Text#readme)

[**Samples**](https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/translation/Azure.AI.Translation.Text/samples)

### [**Java**](#tab/java)

* **Version 1.0.0 (2024-05-21)**
* **Targets Text translation v3.0**
* **GA version release**

[**Package (MVN)**](https://mvnrepository.com/artifact/com.azure/azure-ai-translation-text/1.0.0)

[**Changelog/Release History**](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/translation/azure-ai-translation-text/CHANGELOG.md#100-2024-05-21)

[**README**](https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/translation/azure-ai-translation-text#readme)

[**Samples**](https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/translation/azure-ai-translation-text#next-steps)

### [**JavaScript**](#tab/javascript)

* **Version 1.0.0 (2024-05-21)**
* **Targets Text translation v3.0**
* **GA version release**

[**Package (npm)**](https://www.npmjs.com/package/@azure-rest/ai-translation-text/v/1.0.0)

[**Changelog/Release History**](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/translation/ai-translation-text-rest/CHANGELOG.md#100-2024-05-21)

[**README**](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/translation/ai-translation-text-rest/README.md)

[**Samples**](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/translation/ai-translation-text-rest/samples/v1)

### [**Python**](#tab/python)

* **Version 1.0.0 (2024-05-23)**
* **Targets Text translation v3.0**
* **GA version release**

[**Package (PyPi)**](https://pypi.org/project/azure-ai-translation-text/1.0.1/)

[**Changelog/Release History**](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/translation/azure-ai-translation-text/CHANGELOG.md#100-2024-05-23)

[**README**](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/translation/azure-ai-translation-text/README.md)

[**Samples**](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/translation/azure-ai-translation-text/samples)

---

#### Azure Translator in Foundry Tools Text SDK April 2023 preview release

This release includes the following updates:

### [**C#**](#tab/csharp)

* **Version 1.0.0-beta.1 (2023-04-17)**
* **Targets Text translation v3.0**
* **Initial version release**

[**Package (NuGet)**](https://www.nuget.org/packages/Azure.AI.Translation.Text/1.0.0-beta.1)

[**Changelog/Release History**](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/translation/Azure.AI.Translation.Text/CHANGELOG.md#100-beta1-2023-04-17)

[**README**](https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/translation/Azure.AI.Translation.Text#readme)

[**Samples**](https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/translation/Azure.AI.Translation.Text/samples)

### [**Java**](#tab/java)

* **Version 1.0.0-beta.1 (2023-04-18)**
* **Targets Text translation v3.0**
* **Initial version release**

[**Package (MVN)**](https://mvnrepository.com/artifact/com.azure/azure-ai-translation-text/1.0.0-beta.1)

[**Changelog/Release History**](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/translation/azure-ai-translation-text/CHANGELOG.md#100-beta1-2023-04-18)

[**README**](https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/translation/azure-ai-translation-text#readme)

[**Samples**](https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/translation/azure-ai-translation-text#next-steps)

### [**JavaScript**](#tab/javascript)

* **Version 1.0.0-beta.1 (2023-04-18)**
* **Targets Text translation v3.0**
* **Initial version release**

[**Package (npm)**](https://www.npmjs.com/package/@azure-rest/ai-translation-text/v/1.0.0-beta.1)

[**Changelog/Release History**](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/translation/ai-translation-text-rest/CHANGELOG.md#100-beta1-2023-04-18)

[**README**](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/translation/ai-translation-text-rest/README.md)

[**Samples**](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/translation/ai-translation-text-rest/samples/v1)

### [**Python**](#tab/python)

* **Version 1.0.0b1 (2023-04-19)**
* **Targets Text translation v3.0**
* **Initial version release**

[**Package (PyPi)**](https://pypi.org/project/azure-ai-translation-text/1.0.0b1/)

[**Changelog/Release History**](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/translation/azure-ai-translation-text/CHANGELOG.md#100b1-2023-04-19)

[**README**](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/translation/azure-ai-translation-text/README.md)

[**Samples**](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/translation/azure-ai-translation-text/samples)

---

## Use Text translation SDK in your applications

The Text translation SDK enables the use and management of the Text translation service in your application. The SDK builds on the underlying Text translation REST API allowing you to easily use those APIs within your programming language paradigm. Here's how you use the Text translation SDK for your preferred programming language:

### 1. Install the SDK client library

### [C#/.NET](#tab/csharp)

```dotnetcli
dotnet add package Azure.AI.Translation.Text --version 1.0.0-beta.1
```

```powershell
Install-Package Azure.AI.Translation.Text -Version 1.0.0-beta.1
```

### [Java](#tab/java)

```xml
<dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-ai-translation-text</artifactId>
    <version>1.0.0-beta.1</version>
</dependency>
```

```kotlin
implementation("com.azure:azure-ai-translation-text:1.0.0-beta.1")
```

### [JavaScript](#tab/javascript)

```javascript
npm i @azure-rest/ai-translation-text@1.0.0-beta.1
```

### [Python](#tab/python)

```python
pip install azure-ai-translation-text==1.0.0b1
```

---

### 2. Import the SDK client library into your application

### [C#/.NET](#tab/csharp)

```csharp
using Azure;
using Azure.AI.Translation.Text;
```

### [Java](#tab/java)

```java
import java.util.List;
import java.util.ArrayList;
import com.azure.ai.translation.text.models.*;
import com.azure.ai.translation.text.TextTranslationClientBuilder;
import com.azure.ai.translation.text.TextTranslationClient;

import com.azure.core.credential.AzureKeyCredential;
```

### [JavaScript](#tab/javascript)

```javascript
const {TextTranslationClient } = require("@azure-rest/ai-translation-text").default;
```

### [Python](#tab/python)

```python
from azure.core.credentials import AzureKeyCredential
from azure.ai.translation.text import TextTranslationClient
```

---

### 3. Authenticate the client

Interaction with the Translator using the client library begins with creating an instance of the `TextTranslationClient`class. You need your API key and region to instantiate a client object.
The Text translation API key is found in the Azure portal:

:::image type="content" source="../media/keys-and-endpoint-text-sdk.png" alt-text="Screenshot of the keys and endpoint location in the Azure portal.":::

### [C#/.NET](#tab/csharp)

**Using the global endpoint (default)**

```csharp
string key = "<your-key>";

AzureKeyCredential credential = new(key);
TextTranslationClient client = new(credential);
```

**Using a regional endpoint**

```csharp

Uri endpoint = new("<your-endpoint>");
string key = "<your-key>";
string region = "<region>";

AzureKeyCredential credential = new(key);
TextTranslationClient client = new(credential, region);
```

### [Java](#tab/java)

**Using the global endpoint (default)**

```java

String apiKey = "<your-key>";
AzureKeyCredential credential = new AzureKeyCredential(apiKey);

TextTranslationClient client = new TextTranslationClientBuilder()
            .credential(credential)
            .buildClient();
```

**Using a regional endpoint**

```java
String apiKey = "<your-key>";
String endpoint = "<your-endpoint>";
String region = "<region>";

AzureKeyCredential credential = new AzureKeyCredential(apiKey);

TextTranslationClient client = new TextTranslationClientBuilder()
.credential(credential)
.region(region)
.endpoint(endpoint)
.buildClient();

```

### [JavaScript](#tab/javascript)

```javascript

const TextTranslationClient = require("@azure-rest/ai-translation-text").default,

const apiKey = "<your-key>";
const endpoint = "<your-endpoint>";
const region = "<region>";

```

### [Python](#tab/python)

```python

from azure.ai.translation.text import TextTranslationClient, TranslatorCredential
from azure.ai.translation.text.models import InputTextItem
from azure.core.exceptions import HttpResponseError

key = "<your-key>"
endpoint = "<your-endpoint>"
region = "<region>"


credential = TranslatorCredential(key, region)
text_translator = TextTranslationClient(endpoint=endpoint, credential=credential)
```

---

### 4. Build your application

### [C#/.NET](#tab/csharp)

Create a client object to interact with the Text translation SDK, and then call methods on that client object to interact with the service. The SDKs provide both synchronous and asynchronous methods. For more insight, *see* the Text translation [sample repository](https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/translation/Azure.AI.Translation.Text/samples) for .NET/C#.

### [Java](#tab/java)

Create a client object to interact with the Text translation SDK, and then call methods on that client object to interact with the service. The SDKs provide both synchronous and asynchronous methods. For more insight, *see* the Text translation [sample repository](https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/translation/azure-ai-translation-text/src/samples/java/com/azure/ai/translation/text) for Java.

### [JavaScript](#tab/javascript)

Create a client object to interact with the Text translation SDK, and then call methods on that client object to interact with the service. The SDKs provide both synchronous and asynchronous methods. For more insight, *see* the Text translation [sample repository](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/translation/ai-translation-text-rest/samples/v1) for JavaScript or TypeScript.

### [Python](#tab/python)

Create a client object to interact with the Text translation SDK, and then call methods on that client object to interact with the service. The SDKs provide both synchronous and asynchronous methods. For more insight, *see* the Text translation [sample repository](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/translation/azure-ai-translation-text/samples) for Python.

---

## Help options

The [Microsoft Q & A](/answers/tags/132/azure-translator) and [Stack Overflow](https://stackoverflow.com/questions/tagged/azure-text-translation) forums are available for the developer community to ask and answer questions about Azure Translator and other services. Microsoft monitors the forums and replies to questions that the community has yet to answer. To make sure that we see your question, tag it with **`azure-text-translation`**.

## Next steps

>[!div class="nextstepaction"]
> [**Text translation quickstart**](quickstart/client-library-sdk.md)

>[!div class="nextstepaction"]
> [**Text translation v3.0 reference guide**](reference/v3/reference.md)
