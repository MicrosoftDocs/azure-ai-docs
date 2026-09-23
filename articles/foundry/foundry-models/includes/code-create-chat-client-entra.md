---
manager: mcleans
ms.service: microsoft-foundry
ms.subservice: foundry-model-inference
ms.topic: include
ms.date: 07/31/2026
ms.author: fasantia
author: santiagxf
ai-usage: ai-assisted
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

Use the package to consume the model. The following example shows how to create a client and make a test call to the Responses API by using Microsoft Entra ID and your model deployment.

Replace `<resource>` with your Foundry resource name. Find it in the Azure portal or by running `az cognitiveservices account list`. Replace `deepseek-v3-0324` with your actual deployment name.

```python
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), 
    "https://ai.azure.com/.default"
)

client = OpenAI(
    base_url="https://<resource>.openai.azure.com/openai/v1/",
    api_key=token_provider,
)

response = client.responses.create(
    model="deepseek-v3-0324",  # Replace with your model deployment name.
    input="What is Azure AI?",
)

print(response.output_text)
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

Then, use the package to consume the model. The following example shows how to create a client and make a test call to the Responses API by using Microsoft Entra ID and your model deployment.

Replace `<resource>` with your Foundry resource name (find it in the Azure portal). Replace `deepseek-v3-0324` with your actual deployment name.

```csharp
using Azure.Identity;
using OpenAI;
using OpenAI.Responses;
using System.ClientModel.Primitives;

#pragma warning disable OPENAI001

BearerTokenPolicy tokenPolicy = new(
    new DefaultAzureCredential(),
    "https://ai.azure.com/.default"
);

OpenAIResponseClient client = new(
    model: "deepseek-v3-0324", // Replace with your model deployment name.
    authenticationPolicy: tokenPolicy,
    options: new OpenAIClientOptions()
    {
        Endpoint = new Uri("https://<resource>.openai.azure.com/openai/v1/")
    }
);

OpenAIResponse response = client.CreateResponse("What is Azure AI?");

Console.WriteLine(response.GetOutputText());
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

Then, use the package to consume the model. The following example shows how to create a client and make a test call to the Responses API by using Microsoft Entra ID and your model deployment.

Replace `<resource>` with your Foundry resource name (find it in the Azure portal or by running `az cognitiveservices account list`). Replace `deepseek-v3-0324` with your actual deployment name.

```javascript
import { DefaultAzureCredential, getBearerTokenProvider } from "@azure/identity";
import { OpenAI } from "openai";

const tokenProvider = getBearerTokenProvider(
    new DefaultAzureCredential(),
    'https://ai.azure.com/.default'
);

const client = new OpenAI({
    baseURL: "https://<resource>.openai.azure.com/openai/v1/",
    apiKey: tokenProvider
});

const response = await client.responses.create({
    model: "deepseek-v3-0324", // Replace with your model deployment name.
    input: "What is Azure AI?"
});

console.log(response.output_text);
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

Then, use the package to consume the model. The following example shows how to create a client and make a test call to the Responses API by using Microsoft Entra ID and your model deployment.

Replace `<resource>` with your Foundry resource name (find it in the Azure portal). Replace `deepseek-v3-0324` with your actual deployment name.

```java
import com.azure.identity.AuthenticationUtil;
import com.azure.identity.DefaultAzureCredential;
import com.azure.identity.DefaultAzureCredentialBuilder;
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.credential.BearerTokenCredential;
import com.openai.models.responses.Response;
import com.openai.models.responses.ResponseCreateParams;

DefaultAzureCredential tokenCredential = new DefaultAzureCredentialBuilder().build();

OpenAIClient client = OpenAIOkHttpClient.builder()
    .baseUrl("https://<resource>.openai.azure.com/openai/v1/")
    .credential(BearerTokenCredential.create(
        AuthenticationUtil.getBearerTokenSupplier(
            tokenCredential, 
            "https://ai.azure.com/.default"
        )
    ))
    .build();

ResponseCreateParams params = ResponseCreateParams.builder()
    .model("deepseek-v3-0324") // Replace with your model deployment name.
    .input("What is Azure AI?")
    .build();

Response response = client.responses().create(params);

// The Responses API has no single output-text accessor; concatenate the output items.
response.output().stream()
    .flatMap(item -> item.message().stream())
    .flatMap(message -> message.content().stream())
    .flatMap(content -> content.outputText().stream())
    .forEach(outputText -> System.out.println(outputText.text()));
```

Expected output:

```output
Azure AI is a comprehensive suite of artificial intelligence services and tools from Microsoft that enables developers to build intelligent applications. It includes services for natural language processing, computer vision, speech recognition, and machine learning capabilities.
```

Reference: [OpenAI Java SDK](https://github.com/openai/openai-java) and [DefaultAzureCredential class](/java/api/com.azure.identity.defaultazurecredential).

# [REST](#tab/rest)

Explore the API design in the [reference section](/rest/api/microsoft-foundry/azureopenai/responses?view=rest-microsoft-foundry-v1&preserve-view=true) to see which parameters are available. Insert the authentication (bearer) token in the `Authorization` header.

For example, the [Responses API](/rest/api/microsoft-foundry/azureopenai/responses?view=rest-microsoft-foundry-v1&preserve-view=true) reference section details how to use the `/responses` route to generate predictions. The `/openai/v1/` path is included in the root of the URL:

__Request__

Replace `<resource>` with your Foundry resource name (find it in the Azure portal or by running `az cognitiveservices account list`). Replace `deepseek-v3-0324` with your actual deployment name.

The base URL accepts both `https://<resource>.openai.azure.com/openai/v1/` and `https://<resource>.services.ai.azure.com/openai/v1/` formats.

```bash
curl -X POST https://<resource>.openai.azure.com/openai/v1/responses \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AZURE_OPENAI_AUTH_TOKEN" \
  -d '{
      "model": "deepseek-v3-0324",
      "input": "Explain what the bitter lesson is?"
    }'
```

__Response__

If authentication is successful, you receive a `200 OK` response with the response results in the response body:

```json
{
  "id": "resp_...",
  "object": "response",
  "created_at": 1738368234,
  "model": "deepseek-v3-0324",
  "status": "completed",
  "output": [
    {
      "type": "message",
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "The bitter lesson refers to a key insight in AI research that emphasizes the importance of general-purpose learning methods that leverage computation, rather than human-designed domain-specific approaches. It suggests that methods which scale with increased computation tend to be more effective in the long run."
        }
      ]
    }
  ],
  "usage": {
    "input_tokens": 28,
    "output_tokens": 52,
    "total_tokens": 80
  }
}
```

Tokens must be issued with scope `https://ai.azure.com/.default`.

For testing purposes, the easiest way to get a valid token for your user account is to use the Azure CLI. In a console, sign in and request a token by running the following Azure CLI commands:

```azurecli
az login
az account get-access-token --resource https://ai.azure.com --query "accessToken" --output tsv
```

This command outputs an access token that you can store in the `$AZURE_OPENAI_AUTH_TOKEN` environment variable.

Reference: [Responses API](/rest/api/microsoft-foundry/azureopenai/responses?view=rest-microsoft-foundry-v1&preserve-view=true)

---
