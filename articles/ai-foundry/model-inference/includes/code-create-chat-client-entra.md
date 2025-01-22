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
pip install azure-ai-inference>=1.0.0b5
```

> [!WARNING]
> Azure AI Services resource requires the version `azure-ai-inference>=1.0.0b5` for Python.

Then, you can use the package to consume the model. The following example shows how to create a client to consume chat completions with Entra ID:

```python
import os
from azure.ai.inference import ChatCompletionsClient
from azure.identity import AzureDefaultCredential

model = ChatCompletionsClient(
    endpoint=os.environ["AZUREAI_ENDPOINT_URL"],
    credential=AzureDefaultCredential(),
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
import { AzureDefaultCredential } from "@azure/identity";

const client = new ModelClient(
    process.env.AZUREAI_ENDPOINT_URL, 
    new AzureDefaultCredential()
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
ChatCompletionsClient client = new ChatCompletionsClient(
    new Uri(Environment.GetEnvironmentVariable("AZURE_INFERENCE_ENDPOINT")),
    new DefaultAzureCredential(includeInteractiveCredentials: true)
);
```

# [REST](#tab/rest)

Use the reference section to explore the API design and which parameters are available and indicate authentication token in the header `Authorization`. For example, the reference section for [Chat completions](reference-model-inference-chat-completions.md) details how to use the route `/chat/completions` to generate predictions based on chat-formatted instructions. Notice that the path `/models` is included to the root of the URL:

__Request__

```HTTP/1.1
POST models/chat/completions?api-version=2024-04-01-preview
Authorization: Bearer <bearer-token>
Content-Type: application/json
```
---