---
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: include
ms.date: 5/21/2025
ms.author: fasantia
author: santiagxf
---

# [Python](#tab/python)

Install the package `openai` using your package manager, like pip:

```bash
pip install openai --upgrade
```

Then, you can use the package to consume the model. The following example shows how to create a client to consume chat completions:

```python
import os
from openai import AzureOpenAI
    
client = AzureOpenAI(
    azure_endpoint = "https://<resource>.services.ai.azure.com"
    api_key=os.getenv("AZURE_INFERENCE_CREDENTIAL"),  
    api_version="2024-10-21",
)
```

# [JavaScript](#tab/javascript)

Install the package `openai` using npm:

```bash
npm install openai
```

Then, you can use the package to consume the model. The following example shows how to create a client to consume chat completions:

```javascript
import { AzureKeyCredential } from "@azure/openai";

const endpoint = "https://<resource>.services.ai.azure.com";
const apiKey = new AzureKeyCredential(process.env.AZURE_INFERENCE_CREDENTIAL);
const apiVersion = "2024-10-21"

const client = new AzureOpenAI({ 
    endpoint, 
    apiKey, 
    apiVersion, 
    "deepseek-v3-0324"
});
```

Here, `deepseek-v3-0324` is the name of a model deployment in the Microsoft Foundry resource.

# [C#](#tab/csharp)

Install the OpenAI library with the following command:

```dotnetcli
dotnet add package Azure.AI.OpenAI --prerelease
```

You can use the package to consume the model. The following example shows how to create a client to consume chat completions:

```csharp
AzureOpenAIClient client = new(
    new Uri("https://<resource>.services.ai.azure.com"),
    new ApiKeyCredential(Environment.GetEnvironmentVariable("AZURE_INFERENCE_CREDENTIAL"))
);
```

# [Java](#tab/java)

Add the package to your project:

```xml
<dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-ai-openai</artifactId>
    <version>1.0.0-beta.16</version>
</dependency>
```

Then, you can use the package to consume the model. The following example shows how to create a client to consume chat completions:

```java
OpenAIClient client = new OpenAIClientBuilder()
    .credential(new AzureKeyCredential("{key}"))
    .endpoint("https://<resource>.services.ai.azure.com")
    .buildClient();
```


# [REST](#tab/rest)

Use the reference section to explore the API design and which parameters are available. For example, the reference section for Chat completions details how to use the route `/chat/completions` to generate predictions based on chat-formatted instructions:

__Request__

```HTTP/1.1
POST https://<resource>.services.ai.azure.com/openai/deployments/deepseek-v3-0324/chat/completions?api-version=2024-10-21
api-key: <api-key>
Content-Type: application/json
```

Here, `deepseek-v3-0324` is the name of a model deployment in the Foundry resource.

---
