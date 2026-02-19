---
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: include
ms.date: 02/17/2026
ms.author: mopeakande
author: msakande
---

# [Python](#tab/python)

Install the packages `openai` and `azure-identity` using your package manager, like pip:

```bash
pip install --upgrade openai azure-identity
```

The following example shows how to create a client to consume chat completions and then generate and print out the response:


```python

from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

client = OpenAI(  
  base_url = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",  
  api_key=token_provider,
)
response = client.chat.completions.create(
  model="DeepSeek-R1", # Replace with your model deployment name.
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "How many languages are in the world?"}
  ]
)

#print(response.choices[0].message)
print(response.model_dump_json(indent=2))
```

# [JavaScript](#tab/javascript)

First install the Azure Identity client library before you can use DefaultAzureCredential:

Install the packages `openai` and `@azure/identity` using npm:

```bash
npm install openai @azure/identity
```

To authenticate the `OpenAI` client, use the `getBearerTokenProvider` function from the `@azure/identity` package. This function creates a token provider that `OpenAI` uses internally to obtain tokens for each request. 

The following code creates the token provider, creates a client to consume chat completions, and generates the response:

```javascript
import { DefaultAzureCredential, getBearerTokenProvider } from "@azure/identity";
import { OpenAI } from "openai";

const tokenProvider = getBearerTokenProvider(
    new DefaultAzureCredential(),
    'https://cognitiveservices.azure.com/.default');

const client = new OpenAI({
    baseURL: "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
    apiKey: tokenProvider
});

const messages = [
    { role: 'system', content: 'You are a helpful assistant.' },
    { role: 'user', content: 'How many languages are in the world?' }
];

// Make the API request with top-level await
const result = await client.chat.completions.create({ 
    messages, 
    model: 'DeepSeek-R1', // Your model deployment name
    max_tokens: 100 
});

// Print the full response
console.log('Full response:', result);

// Print just the message content from the response
console.log('Response content:', result.choices[0].message.content);
```

# [C#](#tab/csharp)

First install the [Azure Identity library](/dotnet/api/overview/azure/identity-readme?view=azure-dotnet&preserve-view=true) before you can use DefaultAzureCredential:


```dotnetcli
dotnet add package Azure.Identity
```

Use the desired credential type from the library. For example, [`DefaultAzureCredential`](/dotnet/api/azure.identity.defaultazurecredential?view=azure-dotnet&preserve-view=true). Then create the token provider, create a client to consume chat completions, and generate the response.

```csharp
using Azure.Identity;
using OpenAI;
using OpenAI.Chat;
using System.ClientModel.Primitives;

#pragma warning disable OPENAI001

BearerTokenPolicy tokenPolicy = new(
    new DefaultAzureCredential(),
    "https://cognitiveservices.azure.com/.default");

ChatClient client = new(
    model: "DeepSeek-R1", // Replace with your model deployment name.
    authenticationPolicy: tokenPolicy,
    options: new OpenAIClientOptions() { 
        Endpoint = new Uri("https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1")
   }
);

ChatCompletion completion = client.CompleteChat("How many languages are in the world?");

Console.WriteLine($"[ASSISTANT]: {completion.Content[0].Text}");
```


# [Java](#tab/java)

Authentication with Microsoft Entra ID requires some initial setup:

Add the Azure Identity package:

```xml
<dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-identity</artifactId>
    <version>1.18.0</version>
</dependency>
```

After setup, you can choose which type of credential from `azure.identity` to use. As an example, `DefaultAzureCredential` can be used to authenticate the client.

Authentication is straightforward using `DefaultAzureCredential`. It finds the best credential to use in its running environment.

```java
Credential tokenCredential = BearerTokenCredential.create(
        AuthenticationUtil.getBearerTokenSupplier(
                new DefaultAzureCredentialBuilder().build(),
                "https://cognitiveservices.azure.com/.default"));
OpenAIClient client = OpenAIOkHttpClient.builder()
        .baseUrl("https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/")
        .credential(tokenCredential)
        .build();
```

For more information about Azure OpenAI keyless authentication, see [Use Azure OpenAI without keys](/azure/developer/ai/keyless-connections?tabs=java%2Cazure-cli).

**Chat completion**:

```java
package com.example;

import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.models.ChatModel;
import com.openai.models.chat.completions.ChatCompletion;
import com.openai.models.chat.completions.ChatCompletionCreateParams;

public class OpenAITest {
    public static void main(String[] args) {
        String resourceName = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1";
        String modelDeploymentName = "DeepSeek-R1"; // Replace with your model deployment name.

        try {
            OpenAIClient client = OpenAIOkHttpClient.builder()
                    .baseUrl(resourceName)
                    // Set the Azure Entra ID
                    .credential(BearerTokenCredential.create(AuthenticationUtil.getBearerTokenSupplier(
                        new DefaultAzureCredentialBuilder().build(), "https://cognitiveservices.azure.com/.default")))
                    .build();

           ChatCompletionCreateParams params = ChatCompletionCreateParams.builder()
              .addUserMessage("How many languages are in the world?")
              .model(modelDeploymentName)
              .build();
           ChatCompletion chatCompletion = client.chat().completions().create(params);
        }
    }
}
```

# [REST](#tab/rest)


```bash
curl -X POST https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AZURE_OPENAI_AUTH_TOKEN" \
  -d '{
      "model": "DeepSeek-R1",
      "messages": [
      {
        "role": "system",
        "content": "You are a helpful assistant."
      },
      {
        "role": "user",
        "content": "How many languages are in the world?"
      }
    ]
  }'
```

To retrieve a response:

```bash
curl -X GET https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/chat/completions/{response_id} \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AZURE_OPENAI_AUTH_TOKEN"
```

---
