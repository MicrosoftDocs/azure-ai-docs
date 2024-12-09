---
title: Document Intelligence SDK target REST API 2023-07-31 (GA) latest.
titleSuffix: Azure AI services
description: The Document Intelligence 2023-07-31 (GA) software development kits (SDKs) expose Document Intelligence models, features, and capabilities that are in active development for C#, Java, JavaScript, or Python programming language.
author: laujan
manager: nitinme
ms.service: azure-ai-document-intelligence
ms.custom:
  - devx-track-python
ms.topic: conceptual
ms.date: 05/06/2024
ms.author: lajanuar
monikerRange: 'doc-intel-3.1.0'
--- 


<!-- markdownlint-disable MD024 -->
<!-- markdownlint-disable MD036 -->
<!-- markdownlint-disable MD001 -->
<!-- markdownlint-disable MD051 -->

# SDK target: REST API 2023-07-31 (GA)

![Document Intelligence checkmark](../media/yes-icon.png) **REST API version 2023-07-31 (GA)**

Azure AI Document Intelligence is a cloud service that uses machine learning to analyze text and structured data from documents. The Document Intelligence software development kit (SDK) is a set of libraries and tools that enable you to easily integrate Document Intelligence models and capabilities into your applications. Document Intelligence SDK is available across platforms in C#/.NET, Java, JavaScript, and Python programming languages.

## Supported programming languages

Document Intelligence SDK supports the following languages and platforms:

| Language → Document Intelligence SDK version &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;| Package| Supported API version &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;| Platform support |
|:----------------------:|:----------|:----------| :----------------:|
| [**.NET/C# → latest (GA)**](/dotnet/api/overview/azure/ai.formrecognizer-readme?view=azure-dotnet&preserve-view=true)|[NuGet](https://www.nuget.org/packages/Azure.AI.FormRecognizer/4.1.0)|[2023-07-31 (GA)](/rest/api/aiservices/document-models/analyze-document?view=rest-aiservices-2023-07-31&preserve-view=true&tabs=HTTP)|
|[**Java → latest (GA)**](https://azuresdkdocs.blob.core.windows.net/$web/java/azure-ai-formrecognizer/4.1.0/index.html) |[Maven repository](https://mvnrepository.com/artifact/com.azure/azure-ai-formrecognizer/4.1.0) |[2023-07-31 (GA)](/rest/api/aiservices/document-models/analyze-document?view=rest-aiservices-2023-07-31&preserve-view=true&tabs=HTTP)|[Windows, macOS, Linux](/java/openjdk/install)|
|[**JavaScript → latest (GA)**](https://azuresdkdocs.blob.core.windows.net/$web/javascript/azure-ai-form-recognizer/5.0.0/index.html)| [npm](https://www.npmjs.com/package/@azure/ai-form-recognizer)| [2023-07-31 (GA)](/rest/api/aiservices/document-models/analyze-document?view=rest-aiservices-2023-07-31&preserve-view=true&tabs=HTTP)| [Browser, Windows, macOS, Linux](https://nodejs.org/en/download/) |
|[**Python → latest (GA)**](https://azuresdkdocs.blob.core.windows.net/$web/python/azure-ai-formrecognizer/3.3.0/index.html) | [PyPI](https://pypi.org/project/azure-ai-formrecognizer/3.3.0/)| [2023-07-31 (GA)](/rest/api/aiservices/document-models/analyze-document?view=rest-aiservices-2023-07-31&preserve-view=true&tabs=HTTP)|[Windows, macOS, Linux](/azure/developer/python/configure-local-development-environment?tabs=windows%2Capt%2Ccmd#use-the-azure-cli)|

For more information on other SDK versions, see:

* [`2024-02-29` v4.0 (preview)](sdk-overview-v4-0.md)

* [`2022-08-31` v3.0 (GA)](sdk-overview-v3-0.md)
* [`v2.1` (GA)](../v21/sdk-overview-v2-1.md)

## Supported Clients

The following tables present the correlation between each SDK version the supported API versions of the Document Intelligence service.

### [C#/.NET](#tab/csharp)

| Language| SDK version | API version (default) &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; | Supported clients|
| :------ | :-----------|:---------- | :-----------------|
|**.NET/C# 4.1.0**| v3.1 latest (GA)| 2023-07-31|**DocumentAnalysisClient**</br>**DocumentModelAdministrationClient** |
|**.NET/C# 4.0.0**| v3.0 (GA)| 2022-08-31|  **DocumentAnalysisClient**</br>**DocumentModelAdministrationClient** |
|**.NET/C# 3.1.x**| v2.1 |  v2.1 |  **FormRecognizerClient**</br>**FormTrainingClient** |
|**.NET/C# 3.0.x**| v2.0 | v2.0 |  **FormRecognizerClient**</br>**FormTrainingClient** |

### [Java](#tab/java)

| Language| SDK version | API version &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; | Supported clients|
| :------ | :-----------|:---------- | :-----------------|
|**Java 4.1.0**| v3.1 latest (GA)| 2023-07-31 (default)|**DocumentAnalysisClient**</br>**DocumentModelAdministrationClient** |
|**Java 4.0.0**</br>| v3.0 (GA)| 2022-08-31|  **DocumentAnalysisClient**</br>**DocumentModelAdministrationClient** |
|**Java 3.1.x**| v2.1 |  v2.1 |  **FormRecognizerClient**</br>**FormTrainingClient** |
|**Java 3.0.x**| v2.0| v2.0 |  **FormRecognizerClient**</br>**FormTrainingClient** |

### [JavaScript](#tab/javascript)

| Language| SDK version | API version (default) &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; | Supported clients|
| :------ | :-----------|:---------- | :-----------------|
|**JavaScript 5.0.0**| v3.1 latest (GA)| 2023-07-31 (default)|**DocumentAnalysisClient**</br>**DocumentModelAdministrationClient** |
|**JavaScript 4.0.0**</br>| v3.0 (GA)| 2022-08-31|  **DocumentAnalysisClient**</br>**DocumentModelAdministrationClient** |
|**JavaScript 3.1.x**</br>| v2.1 |  v2.1 |  **FormRecognizerClient**</br>**FormTrainingClient** |
|**JavaScript 3.0.x**</br>| v2.0| v2.0 |  **FormRecognizerClient**</br>**FormTrainingClient** |

### [Python](#tab/python)

| Language| SDK version | API version (default) &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; | Supported clients|
| :------ | :-----------|:---------- | :-----------------|
| **Python 3.3.0**| v3.1 (latest (GA)| 2023-07-31 (default) |  **DocumentAnalysisClient**</br>**DocumentModelAdministrationClient**|
| **Python 3.2.x**| v3.0 (GA)| 2022-08-31|  **DocumentAnalysisClient**</br>**DocumentModelAdministrationClient**|
| **Python 3.1.x**| v2.1 |  v2.1  |  **FormRecognizerClient**</br>**FormTrainingClient** |
| **Python 3.0.0** | v2.0 |  v2.0 |**FormRecognizerClient**</br>**FormTrainingClient** |

---

## Use Document Intelligence SDK in your applications

The Document Intelligence SDK enables the use and management of the Document Intelligence service in your application. The SDK builds on the underlying Document Intelligence REST API allowing you to easily use those APIs within your programming language paradigm. Here's how you use the Document Intelligence SDK for your preferred language:

### 1. Install the SDK client library

### [C#/.NET](#tab/csharp)

```dotnetcli
dotnet add package Azure.AI.FormRecognizer --version 4.1.0
```

```powershell
Install-Package Azure.AI.FormRecognizer -Version 4.1.0
```

### [Java](#tab/java)

```xml
  <dependency>
  <groupId>com.azure</groupId>
  <artifactId>azure-ai-formrecognizer</artifactId>
  <version>4.1.0</version>
  </dependency>
```

```kotlin
implementation("com.azure:azure-ai-formrecognizer:4.1.0")
```

### [JavaScript](#tab/javascript)

```javascript
npm i @azure/ai-form-recognizer@5.0.0
```

### [Python](#tab/python)

```python
pip install azure-ai-formrecognizer==3.3.0
```

---

### 2. Import the SDK client library into your application

### [C#/.NET](#tab/csharp)

```csharp
using Azure;
using Azure.AI.FormRecognizer.DocumentAnalysis;
```

### [Java](#tab/java)

```java
import com.azure.ai.formrecognizer.*;
import com.azure.ai.formrecognizer.models.*;
import com.azure.ai.formrecognizer.DocumentAnalysisClient.*;

import com.azure.core.credential.AzureKeyCredential;
```

### [JavaScript](#tab/javascript)

```javascript
const { AzureKeyCredential, DocumentAnalysisClient } = require("@azure/ai-form-recognizer");
```

### [Python](#tab/python)

```python
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
```

---

### 3. Set up authentication

There are two supported methods for authentication:

* Use a [Document Intelligence API key](#use-your-api-key) with AzureKeyCredential from azure.core.credentials.

* Use a [token credential from azure-identity](#use-an-azure-active-directory-azure-ad-token-credential) to authenticate with [Microsoft Entra ID](/azure/active-directory/fundamentals/active-directory-whatis).

#### Use your API key

Here's where to find your Document Intelligence API key in the Azure portal:

:::image type="content" source="../media/containers/keys-and-endpoint.png" alt-text="Screenshot of the keys and endpoint location in the Azure portal.":::

[!INCLUDE [Microsoft Entra ID or AKV](~/reusable-content/ce-skilling/azure/includes/ai-services/security/microsoft-entra-id-akv.md)]

### [C#/.NET](#tab/csharp)

```csharp

//set `<your-endpoint>` and `<your-key>` variables with the values from the Azure portal to create your `AzureKeyCredential` and `DocumentAnalysisClient` instance
string key = "<your-key>";
string endpoint = "<your-endpoint>";
AzureKeyCredential credential = new AzureKeyCredential(key);
DocumentAnalysisClient client = new DocumentAnalysisClient(new Uri(endpoint), credential);
```

### [Java](#tab/java)

```java

// create your `DocumentAnalysisClient` instance and `AzureKeyCredential` variable
DocumentAnalysisClient client = new DocumentAnalysisClientBuilder()
            .credential(new AzureKeyCredential("<your-key>"))
            .endpoint("<your-endpoint>")
            .buildClient();
```

### [JavaScript](#tab/javascript)

```javascript

// create your `DocumentAnalysisClient` instance and `AzureKeyCredential` variable
async function main() {
    const client = new DocumentAnalysisClient("<your-endpoint>", new AzureKeyCredential("<your-key>"));
```

### [Python](#tab/python)

```python

# create your `DocumentAnalysisClient` instance and `AzureKeyCredential` variable
    document_analysis_client = DocumentAnalysisClient(endpoint="<your-endpoint>", credential=AzureKeyCredential("<your-key>"))
```

---

<a name='use-an-azure-active-directory-azure-ad-token-credential'></a>

#### Use a Microsoft Entra token credential

> [!NOTE]
> Regional endpoints do not support Microsoft Entra authentication. Create a [custom subdomain](../../../ai-services/authentication.md?tabs=powershell#create-a-resource-with-a-custom-subdomain) for your resource in order to use this type of authentication.

Authorization is easiest using the `DefaultAzureCredential`. It provides a default token credential, based upon the running environment, capable of handling most Azure authentication scenarios.

### [C#/.NET](#tab/csharp)

Here's how to acquire and use the [DefaultAzureCredential](/dotnet/api/azure.identity.defaultazurecredential?view=azure-dotnet&preserve-view=true) for .NET applications:

1. Install the [Azure Identity library for .NET](/dotnet/api/overview/azure/identity-readme):

    ```console
        dotnet add package Azure.Identity
    ```

    ```powershell
        Install-Package Azure.Identity
    ```

1. [Register a Microsoft Entra application and create a new service principal](../../../ai-services/authentication.md?tabs=powershell#assign-a-role-to-a-service-principal).

1. Grant access to Document Intelligence by assigning the **`Cognitive Services User`** role to your service principal.

1. Set the values of the client ID, tenant ID, and client secret in the Microsoft Entra application as environment variables: **`AZURE_CLIENT_ID`**, **`AZURE_TENANT_ID`**, and **`AZURE_CLIENT_SECRET`**, respectively.

1. Create your **`DocumentAnalysisClient`** instance including the **`DefaultAzureCredential`**:

    ```csharp
    string endpoint = "<your-endpoint>";
    var client = new DocumentAnalysisClient(new Uri(endpoint), new DefaultAzureCredential());
    ```

For more information, *see* [Authenticate the client](https://github.com/Azure/azure-sdk-for-net/tree/Azure.AI.FormRecognizer_4.0.0-beta.4/sdk/formrecognizer/Azure.AI.FormRecognizer#authenticate-the-client).

### [Java](#tab/java)

Here's how to acquire and use the [DefaultAzureCredential](/java/api/com.azure.identity.defaultazurecredential?view=azure-java-stable&preserve-view=true) for Java applications:

1. Install the [Azure Identity library for Java](/java/api/overview/azure/identity-readme?view=azure-java-stable&preserve-view=true):

    ```xml
    <dependency>
        <groupId>com.azure</groupId>
        <artifactId>azure-identity</artifactId>
        <version>1.5.3</version>
    </dependency>
    ```

1. [Register a Microsoft Entra application and create a new service principal](../../../ai-services/authentication.md?tabs=powershell#assign-a-role-to-a-service-principal).

1. Grant access to Document Intelligence by assigning the **`Cognitive Services User`** role to your service principal.

1. Set the values of the client ID, tenant ID, and client secret of the Microsoft Entra application as environment variables: **`AZURE_CLIENT_ID`**, **`AZURE_TENANT_ID`**, and **`AZURE_CLIENT_SECRET`**, respectively.

1. Create your **`DocumentAnalysisClient`** instance and **`TokenCredential`** variable:

    ```java
    TokenCredential credential = new DefaultAzureCredentialBuilder().build();
    DocumentAnalysisClient documentAnalysisClient = new DocumentAnalysisClientBuilder()
        .endpoint("{your-endpoint}")
        .credential(credential)
        .buildClient();
    ```

For more information, *see* [Authenticate the client](https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/formrecognizer/azure-ai-formrecognizer#authenticate-the-client).

### [JavaScript](#tab/javascript)

Here's how to acquire and use the [DefaultAzureCredential](/javascript/api/@azure/identity/defaultazurecredential?view=azure-node-latest&preserve-view=true) for JavaScript applications:

1. Install the [Azure Identity library for JavaScript](/javascript/api/overview/azure/identity-readme?view=azure-node-latest&preserve-view=true):

    ```javascript
    npm install @azure/identity
    ```

1. [Register a Microsoft Entra application and create a new service principal](../../../ai-services/authentication.md?tabs=powershell#assign-a-role-to-a-service-principal).

1. Grant access to Document Intelligence by assigning the **`Cognitive Services User`** role to your service principal.

1. Set the values of the client ID, tenant ID, and client secret of the Microsoft Entra application as environment variables: **`AZURE_CLIENT_ID`**, **`AZURE_TENANT_ID`**, and **`AZURE_CLIENT_SECRET`**, respectively.

1. Create your **`DocumentAnalysisClient`** instance including the **`DefaultAzureCredential`**:

    ```javascript
    const { DocumentAnalysisClient } = require("@azure/ai-form-recognizer");
    const { DefaultAzureCredential } = require("@azure/identity");

    const client = new DocumentAnalysisClient("<your-endpoint>", new DefaultAzureCredential());
    ```

For more information, *see* [Create and authenticate a client](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/formrecognizer/ai-form-recognizer#create-and-authenticate-a-client).

### [Python](#tab/python)

Here's how to acquire and use the [DefaultAzureCredential](/python/api/azure-identity/azure.identity.defaultazurecredential?view=azure-python&preserve-view=true) for Python applications.

1. Install the [Azure Identity library for Python](/python/api/overview/azure/identity-readme?view=azure-python&preserve-view=true):

    ```python
    pip install azure-identity
    ```

1. [Register a Microsoft Entra application and create a new service principal](../../../ai-services/authentication.md?tabs=powershell#assign-a-role-to-a-service-principal).

1. Grant access to Document Intelligence by assigning the **`Cognitive Services User`** role to your service principal.

1. Set the values of the client ID, tenant ID, and client secret of the Microsoft Entra application as environment variables: **`AZURE_CLIENT_ID`**, **`AZURE_TENANT_ID`**, and **`AZURE_CLIENT_SECRET`**, respectively.

1. Create your **`DocumentAnalysisClient`** instance including the **`DefaultAzureCredential`**:

    ```python
    from azure.identity import DefaultAzureCredential
    from azure.ai.formrecognizer import DocumentAnalysisClient

    credential = DefaultAzureCredential()
    document_analysis_client = DocumentAnalysisClient(
        endpoint="https://<my-custom-subdomain>.cognitiveservices.azure.com/",
        credential=credential
    )
    ```

For more information, *see* [Authenticate the client](https://github.com/Azure/azure-sdk-for-python/tree/azure-ai-formrecognizer_3.2.0b5/sdk/formrecognizer/azure-ai-formrecognizer#authenticate-the-client).

---

### 4. Build your application

Create a client object to interact with the Document Intelligence SDK, and then call methods on that client object to interact with the service. The SDKs provide both synchronous and asynchronous methods. For more insight, try a [quickstart](../quickstarts/get-started-sdks-rest-api.md?view=doc-intel-3.0.0&preserve-view=true) in a language of your choice.

## Help options

The [Microsoft Q & A](/answers/topics/azure-form-recognizer.html) and [Stack Overflow](https://stackoverflow.com/questions/tagged/azure-form-recognizer) forums are available for the developer community to ask and answer questions about Azure AI Document Intelligence and other services. Microsoft monitors the forums and replies to questions that the community has yet to answer. To make sure that we see your question, tag it with **`azure-form-recognizer`**.

## Next steps

> [!div class="nextstepaction"]
>Explore  [**Document Intelligence REST API 2023-07-31**](/rest/api/aiservices/document-models/analyze-document?view=rest-aiservices-2023-07-31&preserve-view=true&tabs=HTTP) operations.
