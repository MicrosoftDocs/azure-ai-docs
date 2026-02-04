---
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: include
ms.date: 01/22/2026
ms.author: fasantia
author: santiagxf
---

# [Python](#tab/python)

Install the OpenAI SDK using a package manager like pip:

```bash
pip install openai
```

For Microsoft Entra ID authentication, also install:

```bash
pip install azure-identity
```

Use the package to consume the model. The following example shows how to create a client to consume chat completions with Microsoft Entra ID and make a test call to the chat completions endpoint with your model deployment.

Replace `<resource>` with your Foundry resource name. Find it in the Azure portal or by running `az cognitiveservices account list`. Replace `DeepSeek-V3.1` with your actual deployment name.

```python
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), 
    "https://cognitiveservices.azure.com/.default"
)

client = OpenAI(
    base_url="https://<resource>.openai.azure.com/openai/v1/",
    api_key=token_provider,
)

completion = client.chat.completions.create(
    model="DeepSeek-V3.1",  # Required: your deployment name
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is Azure AI?"}
    ]
)

print(completion.choices[0].message.content)
```

Expected output

```output
Azure AI is a comprehensive suite of artificial intelligence services and tools from Microsoft that enables developers to build intelligent applications. It includes services for natural language processing, computer vision, speech recognition, and machine learning capabilities.
```

Reference: [OpenAI Python SDK](https://github.com/openai/openai-python) and [DefaultAzureCredential class](/python/api/azure-identity/azure.identity.defaultazurecredential).

# [C#](#tab/csharp)

Install the OpenAI SDK:

```dotnetcli
dotnet add package OpenAI
```

For Microsoft Entra ID authentication, also install the `Azure.Identity` package:

```dotnetcli
dotnet add package Azure.Identity
```

Import the following namespaces:

```csharp
using Azure.Identity;
using OpenAI;
using OpenAI.Chat;
using System.ClientModel.Primitives;
```

Then, use the package to consume the model. The following example shows how to create a client to consume chat completions with Microsoft Entra ID, and then make a test call to the chat completions endpoint with your model deployment.

Replace `<resource>` with your Foundry resource name (find it in the Azure portal). Replace `gpt-4o-mini` with your actual deployment name.


```csharp
#pragma warning disable OPENAI001

BearerTokenPolicy tokenPolicy = new(
    new DefaultAzureCredential(),
    "https://cognitiveservices.azure.com/.default"
);

ChatClient client = new(
    model: "gpt-4o-mini", // Your deployment name
    authenticationPolicy: tokenPolicy,
    options: new OpenAIClientOptions() {
        Endpoint = new Uri("https://<resource>.openai.azure.com/openai/v1/")
    }
);

ChatCompletion completion = client.CompleteChat(
    new SystemChatMessage("You are a helpful assistant."),
    new UserChatMessage("What is Azure AI?")
);

Console.WriteLine(completion.Content[0].Text);
```

Expected output:

```output
Azure AI is a comprehensive suite of artificial intelligence services and tools from Microsoft that enables developers to build intelligent applications. It includes services for natural language processing, computer vision, speech recognition, and machine learning capabilities.
```

Reference: [OpenAI .NET SDK](https://github.com/openai/openai-dotnet) and [DefaultAzureCredential class](/dotnet/api/azure.identity.defaultazurecredential).

# [JavaScript](#tab/javascript)

Install the OpenAI SDK with npm:

```bash
npm install openai
```

For Microsoft Entra ID authentication, also install:

```bash
npm install @azure/identity
```

Then, use the package to consume the model. The following example shows how to create a client to consume chat completions with Microsoft Entra ID, and then make a test call to the chat completions endpoint with your model deployment.

Replace `<resource>` with your Foundry resource name (find it in the Azure portal or by running `az cognitiveservices account list`). Replace `DeepSeek-V3.1` with your actual deployment name.

```javascript
import { DefaultAzureCredential, getBearerTokenProvider } from "@azure/identity";
import { OpenAI } from "openai";

const tokenProvider = getBearerTokenProvider(
    new DefaultAzureCredential(),
    'https://cognitiveservices.azure.com/.default'
);

const client = new OpenAI({
    baseURL: "https://<resource>.openai.azure.com/openai/v1/",
    apiKey: tokenProvider
});

const completion = await client.chat.completions.create({
    model: "DeepSeek-V3.1", // Required: your deployment name
    messages: [
        { role: "system", content: "You are a helpful assistant." },
        { role: "user", content: "What is Azure AI?" }
    ]
});

console.log(completion.choices[0].message.content);
```

Expected output:

```output
Azure AI is a comprehensive suite of artificial intelligence services and tools from Microsoft that enables developers to build intelligent applications. It includes services for natural language processing, computer vision, speech recognition, and machine learning capabilities.
```

Reference: [OpenAI Node.js SDK](https://github.com/openai/openai-node) and [DefaultAzureCredential class](/javascript/api/@azure/identity/defaultazurecredential).

# [Java](#tab/java)

Add the OpenAI SDK to your project. Check the [OpenAI Java GitHub repository](https://github.com/openai/openai-java) for the latest version and installation instructions.

For Microsoft Entra ID authentication, also add:

```xml
<dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-identity</artifactId>
    <version>1.18.0</version>
</dependency>
```

Then, use the package to consume the model. The following example shows how to create a client to consume chat completions with Microsoft Entra ID, and then make a test call to the chat completions endpoint with your model deployment.

Replace `<resource>` with your Foundry resource name (find it in the Azure portal). Replace `DeepSeek-V3.1` with your actual deployment name.

```java
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.azure.identity.DefaultAzureCredential;
import com.azure.identity.DefaultAzureCredentialBuilder;
import com.openai.models.chat.completions.*;

DefaultAzureCredential tokenCredential = new DefaultAzureCredentialBuilder().build();

OpenAIClient client = OpenAIOkHttpClient.builder()
    .baseUrl("https://<resource>.openai.azure.com/openai/v1/")
    .credential(BearerTokenCredential.create(
        AuthenticationUtil.getBearerTokenSupplier(
            tokenCredential, 
            "https://cognitiveservices.azure.com/.default"
        )
    ))
    .build();

ChatCompletionCreateParams params = ChatCompletionCreateParams.builder()
    .addSystemMessage("You are a helpful assistant.")
    .addUserMessage("What is Azure AI?")
    .model("DeepSeek-V3.1") // Required: your deployment name
    .build();

ChatCompletion completion = client.chat().completions().create(params);
System.out.println(completion.choices().get(0).message().content());
```

Expected output:

```output
Azure AI is a comprehensive suite of artificial intelligence services and tools from Microsoft that enables developers to build intelligent applications. It includes services for natural language processing, computer vision, speech recognition, and machine learning capabilities.
```

Reference: [OpenAI Java SDK](https://github.com/openai/openai-java) and [DefaultAzureCredential class](/java/api/com.azure.identity.defaultazurecredential).

# [REST](#tab/rest)

Explore the API design in the reference section to see which parameters are available. Indicate the authentication token in the header `Authorization`. For example, the [Chat completion](../../openai/latest.md#create-chat-completion) reference section details how to use the `/chat/completions` route to generate predictions based on chat-formatted instructions. The path `/models` is included in the root of the URL:

__Request__

Replace `<resource>` with your Foundry resource name (find it in the Azure portal or by running `az cognitiveservices account list`). Replace `MAI-DS-R1` with your actual deployment name.

The base_url will accept both `https://<resource>.openai.azure.com/openai/v1/` and `https://<resource>.services.ai.azure.com/openai/v1/` formats.

```bash
curl -X POST https://<resource>.openai.azure.com/openai/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AZURE_OPENAI_AUTH_TOKEN" \
  -d '{
      "model": "MAI-DS-R1",
      "messages": [
      {
        "role": "system",
        "content": "You are a helpful assistant."
      },
      {
        "role": "user",
        "content": "Explain what the bitter lesson is?"
      }
    ]
  }'
```

__Response__

If authentication is successful, you receive a `200 OK` response with chat completion results in the response body:

```json
{
  "id": "chatcmpl-...",
  "object": "chat.completion",
  "created": 1738368234,
  "model": "MAI-DS-R1",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "The bitter lesson refers to a key insight in AI research that emphasizes the importance of general-purpose learning methods that leverage computation, rather than human-designed domain-specific approaches. It suggests that methods which scale with increased computation tend to be more effective in the long run."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 28,
    "completion_tokens": 52,
    "total_tokens": 80
  }
}
```

Tokens must be issued with scope `https://cognitiveservices.azure.com/.default`.

For testing purposes, the easiest way to get a valid token for your user account is to use the Azure CLI. In a console, run the following Azure CLI command:

```azurecli
az account get-access-token --resource https://cognitiveservices.azure.com --query "accessToken" --output tsv
```

This command outputs an access token that you can store in the `$AZURE_OPENAI_AUTH_TOKEN` environment variable.

Reference: [Chat Completions API](../../openai/latest.md#create-chat-completion)

---
