---
manager: nitinme
ms.service: azure-ai-model-inference
ms.topic: include
ms.date: 1/21/2025
ms.author: fasantia
author: santiagxf
---

# [Python](#tab/python)

Install the package `azure-ai-inference` using your package manager, like pip:

```bash
pip install azure-ai-inference
```

Then, you can use the package to consume the model. The following example shows how to create a client to consume chat completions with Entra ID:

```python
import os
from azure.ai.inference import ChatCompletionsClient
from azure.identity import DefaultAzureCredential

client = ChatCompletionsClient(
    endpoint="https://<resource>.services.ai.azure.com/models",
    credential=DefaultAzureCredential(),
    credential_scopes=["https://cognitiveservices.azure.com/.default"],
)
```

# [JavaScript](#tab/javascript)

Install the package `@azure-rest/ai-inference` using npm:

```bash
npm install @azure-rest/ai-inference
```

Then, you can use the package to consume the model. The following example shows how to create a client to consume chat completions with Entra ID:

```javascript
import ModelClient from "@azure-rest/ai-inference";
import { isUnexpected } from "@azure-rest/ai-inference";
import { DefaultAzureCredential } from "@azure/identity";

const clientOptions = { credentials: { "https://cognitiveservices.azure.com" } };

const client = new ModelClient(
    "https://<resource>.services.ai.azure.com/models", 
    new DefaultAzureCredential(),
    clientOptions,
);
```

# [C#](#tab/csharp)

Install the Azure AI inference library with the following command:

```dotnetcli
dotnet add package Azure.AI.Inference --prerelease
```

Install the `Azure.Identity` package:

```dotnetcli
dotnet add package Azure.Identity
```

Import the following namespaces:

```csharp
using Azure;
using Azure.Identity;
using Azure.AI.Inference;
```

Then, you can use the package to consume the model. The following example shows how to create a client to consume chat completions with Entra ID:

```csharp
TokenCredential credential = new DefaultAzureCredential();
AzureAIInferenceClientOptions clientOptions = new AzureAIInferenceClientOptions();
BearerTokenAuthenticationPolicy tokenPolicy = new BearerTokenAuthenticationPolicy(credential, new string[] { "https://cognitiveservices.azure.com/.default" });
clientOptions.AddPolicy(tokenPolicy, HttpPipelinePosition.PerRetry);

ChatCompletionsClient client = new ChatCompletionsClient(
    new Uri("https://<resource>.services.ai.azure.com/models"),
    credential,
    clientOptions.
);
```

# [Java](#tab/java)

Add the package to your project:

```xml
<dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-ai-inference</artifactId>
    <version>1.0.0-beta.4</version>
</dependency>
<dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-identity</artifactId>
    <version>1.15.3</version>
</dependency>
```

Then, you can use the package to consume the model. The following example shows how to create a client to consume chat completions:

```java
TokenCredential defaultCredential = new DefaultAzureCredentialBuilder().build();
ChatCompletionsClient client = new ChatCompletionsClientBuilder()
    .credential(defaultCredential)
    .endpoint("https://<resource>.services.ai.azure.com/models")
    .buildClient();
```

Explore our [samples](https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/ai/azure-ai-inference/src/samples) and read the [API reference documentation](https://aka.ms/azsdk/azure-ai-inference/java/reference) to get yourself started.

# [REST](#tab/rest)

Use the reference section to explore the API design and which parameters are available and indicate authentication token in the header `Authorization`. For example, the reference section for [Chat completions](.././reference/reference-model-inference-chat-completions.md) details how to use the route `/chat/completions` to generate predictions based on chat-formatted instructions. Notice that the path `/models` is included to the root of the URL:

__Request__

```HTTP/1.1
POST https://<resource>.services.ai.azure.com/models/chat/completions?api-version=2024-05-01-preview
Authorization: Bearer <bearer-token>
Content-Type: application/json
```

Tokens have to be issued with scope `https://cognitiveservices.azure.com/.default`.

For testing purposes, the easiest way to get a valid token for your user account is to use the Azure CLI. In a console, run the following Azure CLI command:

```azurecli
az account get-access-token --resource https://cognitiveservices.azure.com --query "accessToken" --output tsv
```
---
