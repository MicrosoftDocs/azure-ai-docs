---
manager: nitinme
ms.service: azure-ai-model-inference
ms.custom:
ms.topic: include
ms.date: 10/08/2024
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

Then, you can use the package to consume the model. The following example shows how to create a client to consume chat completions:

```python
import os
from azure.ai.inference import EmbeddingsClient
from azure.core.credentials import AzureKeyCredential

client = EmbeddingsClient(
    endpoint=os.environ["AZUREAI_ENDPOINT_URL"],
    credential=AzureKeyCredential(os.environ["AZUREAI_ENDPOINT_KEY"]),
)
```

If you are using an endpoint with support for Entra ID, you can create your client as follows:

```python
import os
from azure.ai.inference import EmbeddingsClient
from azure.identity import AzureDefaultCredential

client = EmbeddingsClient(
    endpoint=os.environ["AZUREAI_ENDPOINT_URL"],
    credential=AzureDefaultCredential(),
)
```

Explore our [samples](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-inference/samples) and read the [API reference documentation](https://aka.ms/azsdk/azure-ai-inference/python/reference) to get yourself started.

# [JavaScript](#tab/javascript)

Install the package `@azure-rest/ai-inference` using npm:

```bash
npm install @azure-rest/ai-inference
```

Then, you can use the package to consume the model. The following example shows how to create a client to consume embeddings:

```javascript
import ModelClient from "@azure-rest/ai-inference";
import { isUnexpected } from "@azure-rest/ai-inference";
import { AzureKeyCredential } from "@azure/core-auth";

const client = new ModelClient(
    process.env.AZUREAI_ENDPOINT_URL, 
    new AzureKeyCredential(process.env.AZUREAI_ENDPOINT_KEY)
);
```

For endpoint with support for Microsoft Entra ID, you can create your client as follows:

```javascript
import ModelClient from "@azure-rest/ai-inference";
import { isUnexpected } from "@azure-rest/ai-inference";
import { AzureDefaultCredential } from "@azure/identity";

const client = new ModelClient(
    process.env.AZUREAI_ENDPOINT_URL, 
    new AzureDefaultCredential()
);
```

Explore our [samples](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/ai/ai-inference-rest/samples) and read the [API reference documentation](https://aka.ms/AAp1kxa) to get yourself started.

# [C#](#tab/csharp)

Install the Azure AI inference library with the following command:

```dotnetcli
dotnet add package Azure.AI.Inference --prerelease
```

For endpoint with support for Microsoft Entra ID (formerly Azure Active Directory), install the `Azure.Identity` package:

```dotnetcli
dotnet add package Azure.Identity
```

Import the following namespaces:

```csharp
using Azure;
using Azure.Identity;
using Azure.AI.Inference;
```

Then, you can use the package to consume the model. The following example shows how to create a client to consume embeddings:

```csharp
EmbeddingsClient client = new EmbeddingsClient(
    new Uri(Environment.GetEnvironmentVariable("AZURE_INFERENCE_ENDPOINT")),
    new AzureKeyCredential(Environment.GetEnvironmentVariable("AZURE_INFERENCE_CREDENTIAL"))
);
```

For endpoint with support for Microsoft Entra ID (formerly Azure Active Directory):

```csharp
EmbeddingsClient client = new EmbeddingsClient(
    new Uri(Environment.GetEnvironmentVariable("AZURE_INFERENCE_ENDPOINT")),
    new DefaultAzureCredential(includeInteractiveCredentials: true)
);
```

Explore our [samples](https://aka.ms/azsdk/azure-ai-inference/csharp/samples) and read the [API reference documentation](https://aka.ms/azsdk/azure-ai-inference/csharp/reference) to get yourself started.

# [REST](#tab/rest)

Use the reference section to explore the API design and which parameters are available. For example, the reference section for [Embeddings](../../../ai-studio/reference/reference-model-inference-embeddings.md) details how to use the route `/embeddings` to generate predictions based on chat-formatted instructions. Notice that the path `/models` is included to the root of the URL:

__Request__

```HTTP/1.1
POST models/embeddings?api-version=2024-04-01-preview
Authorization: Bearer <bearer-token>
Content-Type: application/json
```
---