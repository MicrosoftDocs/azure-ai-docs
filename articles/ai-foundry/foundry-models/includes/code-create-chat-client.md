---
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
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

Then, you can use the package to consume the model. The following example shows how to create a client to consume chat completions:

```python
import os
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential

client = ChatCompletionsClient(
    endpoint="https://<resource>.services.ai.azure.com/models",
    credential=AzureKeyCredential(os.environ["AZURE_INFERENCE_CREDENTIAL"]),
)
```

Explore our [samples](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-inference/samples) and read the [API reference documentation](https://aka.ms/azsdk/azure-ai-inference/python/reference) to get yourself started.

# [JavaScript](#tab/javascript)

Install the package `@azure-rest/ai-inference` using npm:

```bash
npm install @azure-rest/ai-inference
```

Then, you can use the package to consume the model. The following example shows how to create a client to consume chat completions:

```javascript
import ModelClient from "@azure-rest/ai-inference";
import { isUnexpected } from "@azure-rest/ai-inference";
import { AzureKeyCredential } from "@azure/core-auth";

const client = new ModelClient(
    "https://<resource>.services.ai.azure.com/models", 
    new AzureKeyCredential(process.env.AZURE_INFERENCE_CREDENTIAL)
);
```

Explore our [samples](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/ai/ai-inference-rest/samples) and read the [API reference documentation](/javascript/api/@azure-rest/ai-inference) to get yourself started.

# [C#](#tab/csharp)

Install the Azure AI inference library with the following command:

```dotnetcli
dotnet add package Azure.AI.Inference --prerelease
```

Import the following namespaces:

```csharp
using Azure;
using Azure.Identity;
using Azure.AI.Inference;
```

Then, you can use the package to consume the model. The following example shows how to create a client to consume chat completions:

```csharp
ChatCompletionsClient client = new ChatCompletionsClient(
    new Uri("https://<resource>.services.ai.azure.com/models"),
    new AzureKeyCredential(Environment.GetEnvironmentVariable("AZURE_INFERENCE_CREDENTIAL"))
);
```

Explore our [samples](https://aka.ms/azsdk/azure-ai-inference/csharp/samples) and read the [API reference documentation](https://aka.ms/azsdk/azure-ai-inference/csharp/reference) to get yourself started.

# [Java](#tab/java)

Add the package to your project:

```xml
<dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-ai-inference</artifactId>
    <version>1.0.0-beta.1</version>
</dependency>
```

Then, you can use the package to consume the model. The following example shows how to create a client to consume chat completions:

```java
ChatCompletionsClient client = new ChatCompletionsClientBuilder()
    .credential(new AzureKeyCredential("{key}"))
    .endpoint("https://<resource>.services.ai.azure.com/models")
    .buildClient();
```

Explore our [samples](https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/ai/azure-ai-inference/src/samples) and read the [API reference documentation](https://aka.ms/azsdk/azure-ai-inference/java/reference) to get yourself started.


# [REST](#tab/rest)

Use the reference section to explore the API design and which parameters are available. For example, the reference section for [Chat completions](/rest/api/aifoundry/model-inference/get-chat-completions/get-chat-completions) details how to use the route `/chat/completions` to generate predictions based on chat-formatted instructions. Notice that the path `/models` is included to the root of the URL:

__Request__

```HTTP/1.1
POST https://<resource>.services.ai.azure.com/models/chat/completions?api-version=2024-05-01-preview
api-key: <api-key>
Content-Type: application/json
```
---
