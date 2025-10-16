---
title: How to use chat completions with Azure AI Foundry Models
titleSuffix: Azure AI Foundry
description: Learn how to generate chat completions with Azure AI Foundry Models
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: how-to
ms.date: 10/15/2025
ms.author: mopeakande
author: msakande
ms.reviewer: achand
reviewer: achandmsft
ms.custom: generated
---

# How to generate chat completions with Azure AI Foundry Models

This article explains how to use chat completions with Azure AI Foundry Model deployments.

## Prerequisites

To use chat completion models in your application, you need:

[!INCLUDE [how-to-prerequisites](../includes/how-to-prerequisites.md)]

* A chat completions model deployment. If you don't have one, see [Add and configure Foundry Models](create-model-deployments.md) to add a chat completions model to your resource.


## Use chat completions

For Foundry Models, including Azure OpenAI models, we recommend using the [Responses API](../../openai/supported-languages.md). However, the v1 API also allows you to make chat completions calls with other [Foundry Models sold directly by Azure](../concepts/models-sold-directly-by-azure.md), such as DeepSeek and Grok models, which support the OpenAI v1 chat completions syntax.

In the following examples, you first create the client to consume the model. Then, create a basic request to the model. 


### Use the responses API

This section uses the v1 API.

# [Python](#tab/python)

[Python v1 examples](../../openai/supported-languages.md).

**API Key**:

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/"
)

response = client.responses.create(   
  model="gpt-4.1-nano", # Replace with your model deployment name 
  input="This is a test.",
)

print(response.model_dump_json(indent=2)) 
```

- `OpenAI()` client is used instead of `AzureOpenAI()`.
- `base_url` passes the Azure OpenAI endpoint and `/openai/v1` is appended to the endpoint address.
- `api-version` is no longer a required parameter with the v1 GA API.

To use API key with environment variables set for `OPENAI_BASE_URL` and `OPENAI_API_KEY`:

```python
client = OpenAI()
```


**Microsoft Entra ID**:

> [!IMPORTANT]
> Automatic token refresh handling was previously done through use of the `AzureOpenAI()` client. The v1 API removes this dependency by adding automatic token refresh support to the `OpenAI()` client.

```python
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

client = OpenAI(  
  base_url = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",  
  api_key = token_provider  
)

response = client.responses.create(
    model="gpt-4.1-nano",
    input= "This is a test" 
)

print(response.model_dump_json(indent=2)) 
```

- `base_url` passes the Azure OpenAI endpoint and `/openai/v1` is appended to the endpoint address.
- `api_key` parameter is set to `token_provider`, enabling automatic retrieval and refresh of an authentication token instead of using a static API key.

# [C#](#tab/dotnet)

[C# v1 examples](../../openai/supported-languages.md)

**API Key**:

```csharp
OpenAIClient client = new(
    new ApiKeyCredential("{your-api-key}"),
    new OpenAIClientOptions()
    {
        Endpoint = new("https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/"),
    })
```

**Microsoft Entra ID**:

To use Entra ID, you also need the following package:

```bash
    dotnet add package Azure.Identity
```

```csharp
#pragma warning disable OPENAI001

BearerTokenPolicy tokenPolicy = new(
    new DefaultAzureCredential(),
    "https://cognitiveservices.azure.com/.default");
OpenAIClient client = new(
    authenticationPolicy: tokenPolicy,
    options: new OpenAIClientOptions()
    {
        Endpoint = new("https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/"),
    })
```

# [JavaScript](#tab/javascript)

[JavaScript v1 examples](../../openai/supported-languages.md)

**API Key**:

```javascript
const client = new OpenAI({
    baseURL: "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
    apiKey: "{your-api-key}" 
});
```

**API Key** with environment variables set for `OPENAI_BASE_URL` and `OPENAI_API_KEY`:

```javascript
const client = new OpenAI();
```

**Microsoft Entra ID**:

```javascript
const tokenProvider = getBearerTokenProvider(
    new DefaultAzureCredential(),
    'https://cognitiveservices.azure.com/.default');
const client = new OpenAI({
    baseURL: "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
    apiKey: tokenProvider
});
```

# [Go](#tab/go)

[Go v1 examples](../../openai/supported-languages.md)

**API Key**:

```go
client := openai.NewClient(
    option.WithBaseURL("https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/"),
    option.WithAPIKey("{your-api-key}")
)
```

**API Key** with environment variables set for `OPENAI_BASE_URL` and `OPENAI_API_KEY`:

```go
client := openai.NewClient()
```


**Microsoft Entra ID**:

```go
tokenCredential, err := azidentity.NewDefaultAzureCredential(nil)

client := openai.NewClient(
    option.WithBaseURL("https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/"),
    azure.WithTokenCredential(tokenCredential)
)
```

# [Java](#tab/Java)

[Java v1 examples](../../openai/supported-languages.md)

**API Key**:

```java

OpenAIClient client = OpenAIOkHttpClient.builder()
                .baseUrl("https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/")
                .apiKey(apiKey)
                .build();
```

**API Key** with environment variables set for `OPENAI_BASE_URL` and `OPENAI_API_KEY`:

```java
OpenAIClient client = OpenAIOkHttpClient.builder()
                .fromEnv()
                .build();
```

**Microsoft Entra ID**:

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

# [REST](#tab/rest)

**API Key**:

```bash
curl -X POST https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/responses \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
  -d '{
     "model": "gpt-4.1-nano",
     "input": "This is a test"
    }'
```

**Microsoft Entra ID**:

```bash
curl -X POST https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/responses \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AZURE_OPENAI_AUTH_TOKEN" \
  -d '{
     "model": "gpt-4o",
     "input": "This is a test"
    }'
```

---

### Use the chat completions API

For Foundry Models, including Azure OpenAI models, we recommend using the [Responses API](../../openai/supported-languages.md). However, the v1 API also allows you to make chat completions calls with other Foundry Models from providers like DeepSeek and Grok, as these models support the OpenAI v1 chat completions syntax.

`base_url` will accept both `https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/` and `https://YOUR-RESOURCE-NAME.services.ai.azure.com/openai/v1/` formats.

# [Python](#tab/python)

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
completion = client.chat.completions.create(
  model="grok-3-mini", # Replace with your model deployment name.
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Tell me about the attention is all you need paper"}
  ]
)

#print(completion.choices[0].message)
print(completion.model_dump_json(indent=2))
```

# [C#](#tab/dotnet)

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
    model: "grok-3-mini", // Replace with your model deployment name.
    authenticationPolicy: tokenPolicy,
    options: new OpenAIClientOptions() { 
    
        Endpoint = new Uri("https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1")
   }
);

ChatCompletion completion = client.CompleteChat("Tell me about the attention is all you need paper");

Console.WriteLine($"[ASSISTANT]: {completion.Content[0].Text}");
```

# [JavaScript](#tab/javascript)

```javascript
import { DefaultAzureCredential, getBearerTokenProvider } from "@azure/identity";
import { OpenAI } from "openai";

const tokenProvider = getBearerTokenProvider(
    new DefaultAzureCredential(),
    'https://cognitiveservices.azure.com/.default');
const client = new OpenAI({
    baseURL: "https://YOUR-RESOURCE_NAME.openai.azure.com/openai/v1/",
    apiKey: tokenProvider
});

const messages = [
    { role: 'system', content: 'You are a helpful assistant.' },
    { role: 'user', content: 'Tell me about the attention is all you need paper' }
];

// Make the API request with top-level await
const result = await client.chat.completions.create({ 
    messages, 
    model: 'grok-3-mini', // model deployment name
    max_tokens: 100 
});

// Print the full response
console.log('Full response:', result);

// Print just the message content from the response
console.log('Response content:', result.choices[0].message.content);
```

# [Go](#tab/go)

```go
package main

import (
    "context"
    "fmt"

    "github.com/Azure/azure-sdk-for-go/sdk/azidentity"
    "github.com/openai/openai-go/v3"
    "github.com/openai/openai-go/v3/azure"
    "github.com/openai/openai-go/v2/option"
)

func main() {
    // Create an Azure credential
    tokenCredential, err := azidentity.NewDefaultAzureCredential(nil)
    if err != nil {
        panic(fmt.Sprintf("Failed to create credential: %v", err))
    }

    // Create a client with Azure OpenAI endpoint and token credential
    client := openai.NewClient(
        option.WithBaseURL("https://YOUR-RESOURCE_NAME.openai.azure.com/openai/v1/"),
        azure.WithTokenCredential(tokenCredential),
    )

    // Make a completion request
    chatCompletion, err := client.Chat.Completions.New(context.TODO(), openai.ChatCompletionNewParams{
        Messages: []openai.ChatCompletionMessageParamUnion{
            openai.UserMessage("Explain what the bitter lesson is?"),
        },
        Model: "grok-3-mini", // Use your deployed model name on Azure
    })
    if err != nil {
        panic(err.Error())
    }

    fmt.Println(chatCompletion.Choices[0].Message.Content)
}
```

# [Java](#tab/Java)

```java
package com.example;

import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.models.ChatModel;
import com.openai.models.chat.completions.ChatCompletion;
import com.openai.models.chat.completions.ChatCompletionCreateParams;

public class OpenAITest {
    public static void main(String[] args) {
        // Get API key from environment variable for security
        String apiKey = System.getenv("OPENAI_API_KEY");
        String resourceName = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1";
        String modelDeploymentName = "grok-3-mini"; //replace with you model deployment name

        try {
            OpenAIClient client = OpenAIOkHttpClient.builder()
                    .baseUrl(resourceName)
                    .apiKey(apiKey)
                    .build();

           ChatCompletionCreateParams params = ChatCompletionCreateParams.builder()
              .addUserMessage("Explain what the bitter lesson is?")
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
      "model": "grok-3-mini",
      "messages": [
      {
        "role": "developer",
        "content": "You are a helpful assistant."
      },
      {
        "role": "user",
        "content": "Explain what the bitter lesson is?"
      }
    ]
  }'
```

---

## v1 API support

- [v1 OpenAPI 3.0 spec](https://github.com/Azure/azure-rest-api-specs/blob/main/specification/ai/data-plane/OpenAI.v1/azure-v1-v1-generated.json)


## Related content

- [Work with chat completions models](../../openai/how-to/chatgpt.md)
- [Use embeddings models](../../model-inference/how-to/use-embeddings.md)
- [Use image embeddings models](../../model-inference/how-to/use-image-embeddings.md)
- [Use reasoning models](../../model-inference/how-to/use-chat-reasoning.md)
- [Basic Azure AI Foundry chat reference architecture](/azure/architecture/ai-ml/architecture/basic-azure-ai-foundry-chat)
