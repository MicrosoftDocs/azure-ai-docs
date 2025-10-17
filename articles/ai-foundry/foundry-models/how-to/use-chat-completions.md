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

This article explains how to generate chat completions with Azure AI Foundry Model deployments by using the unified OpenAI v1 chat completion endpoint, also referred to as the v1 Azure OpenAI APIs. The unified endpoint eliminates the need for separate Azure-specific code paths.

## Prerequisites

To use chat completion models in your application, you need:

[!INCLUDE [how-to-prerequisites](../includes/how-to-prerequisites.md)]

* A chat completions model deployment. If you don't have one, see [Add and configure Foundry Models](create-model-deployments.md) to add a chat completions model to your resource.


## v1 Azure OpenAI APIs

The v1 Azure OpenAI APIs use the `OpenAI()` client instead of the deprecated  `AzureOpenAI()` client. The v1 Azure OpenAI APIs add support for:

- Ongoing access to the latest features, with no need to frequently specify new values for the `api-version` parameter.
- OpenAI client support with minimal code changes to swap between OpenAI and Azure OpenAI when using key-based authentication.
- OpenAI client support for token-based authentication and automatic token refresh without the need to take a dependency on a separate Azure OpenAI client.
- Chat completions calls with Foundry Models from providers like DeepSeek and Grok, which support the v1 chat completions syntax.

For more information on the v1 Azure OpenAI APIs, see [API evolution](../../openai/api-version-lifecycle.md#api-evolution) and the [v1 OpenAPI 3.0 spec](https://github.com/Azure/azure-rest-api-specs/blob/main/specification/ai/data-plane/OpenAI.v1/azure-v1-v1-generated.json).

## Generate chat completions

For Azure OpenAI in Foundry Models, use the [Responses API](../../openai/supported-languages.md#responses-api)) to make chat completion calls. For other [Foundry Models sold directly by Azure](../concepts/models-sold-directly-by-azure.md), such as DeepSeek and Grok models, the v1 Azure OpenAI API also allows you to make chat completion calls by using the v1 chat completions syntax.

In the following examples, you create the client to consume the model and then send a basic request to the model. 

> [!NOTE]
> Use keyless authentication with Microsoft Entra ID. If that's not possible, use an API key and store it in Azure Key Vault. You can use an environment variable for testing outside of your Azure environments.

### Use the responses API

# [Python](#tab/python)

[Python v1 examples](../../openai/supported-languages.md).

**API key authentication**:

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/"
)

response = client.responses.create(   
  model="gpt-4.1-nano", # Replace with your deployment name 
  input="This is a test.",
)

print(response.model_dump_json(indent=2)) 
```

Notice the following details of the previous code:

- Uses the `OpenAI()` client instead of the deprecated `AzureOpenAI()` client.
- Passes the Azure OpenAI endpoint appended with `/openai/v1/` as the `base_url`.
- Doesn't have to provide the `api-version` parameter with the v1 GA API.
- Sets the `model` parameter to the underlying **deployment name** you chose when you deployed the model. This name isn't the same as the name of the model you deployed.

To use the API key with environment variables set for `OPENAI_BASE_URL` and `OPENAI_API_KEY`:

```python
client = OpenAI()
```


**Microsoft Entra authentication**:

Microsoft Entra authentication only supports Azure OpenAI resources. Complete the following steps:

1. Install the Azure Identity client library:

    ```bash
    pip install azure-identity
    ```

1. Define an environment variable named `AZURE_TOKEN_CREDENTIALS`, and set it according to the environment in which the code runs:
    - In Azure, set it to `ManagedIdentityCredential`.
        > [!IMPORTANT]
        > If you use a user-assigned managed identity, define an environment variable named `AZURE_CLIENT_ID`. Set it to the client ID of the managed identity. If you don't set that environment variable, `DefaultAzureCredential` assumes a system-assigned managed identity.
    - In local development, set it to `dev`.
    The Azure Identity library's `DefaultAzureCredential` reads this environment variable. For more information, see [Exclude a credential type category](/azure/developer/python/sdk/authentication/credential-chains?tabs=dac#exclude-a-credential-type-category).

1. Use the following code to configure the OpenAI client object, specify your deployment, and generate responses.   

    ```python
    import os
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
        model ="gpt-4.1-nano",  # Replace with your deployment name 
        input = "This is a test" 
    )
    
    print(response.model_dump_json(indent=2)) 
    ```

    Notice the following details of the previous code:

    - Uses the `OpenAI()` client instead of the deprecated `AzureOpenAI()` client.
    - Passes the Azure OpenAI endpoint appended with `/openai/v1/` as the `base_url`.
    - Sets the `api_key` parameter to `token_provider`. This setting enables automatic retrieval and refresh of an authentication token instead of using a static API key.
    - Doesn't have to provide the `api-version` parameter with the v1 GA API.
    - Sets the `model` parameter to the underlying **deployment name** you chose when you deployed the model. This name isn't the same as the name of the model you deployed.

# [C#](#tab/dotnet)

[C# v1 examples](../../openai/supported-languages.md)

**API key authentication**:

```csharp
using OpenAI;
using System;
using System.ClientModel;

OpenAIClient client = new(
    new ApiKeyCredential("{your-api-key}"),
    new OpenAIClientOptions()
    {
        Endpoint = new("https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/"),
    })
```

**Microsoft Entra authentication**:

Microsoft Entra authentication only supports Azure OpenAI resources. Complete the following steps:

1. Install the Azure Identity client library:

    ```dotnetcli
    dotnet add package Azure.Identity
    ```
1. Define an environment variable named `AZURE_TOKEN_CREDENTIALS`, and set it according to the environment in which the code runs:
    - In Azure, set it to `ManagedIdentityCredential`.
        > [!IMPORTANT]
        > If you use a user-assigned managed identity, define an environment variable named `AZURE_CLIENT_ID`. Set it to the client ID of the managed identity. If you don't set that environment variable, `DefaultAzureCredential` assumes a system-assigned managed identity.
    - In local development, set it to `dev`.
    The Azure Identity library's `DefaultAzureCredential` reads this environment variable. For more information, see [Exclude a credential type category](/dotnet/azure/sdk/authentication/credential-chains?tabs=dac#exclude-a-credential-type-category).

1. Use the following code to configure the OpenAI client object, specify your deployment, and generate responses.  

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
    
    string deploymentName = "my-gpt-4.1-nano-deployment";
    OpenAIResponseClient response = client.GetOpenAIResponseClient(deploymentName);
    
    ```

# [JavaScript](#tab/javascript)

[JavaScript v1 examples](../../openai/supported-languages.md)

**API key authentication**:

```javascript
const client = new OpenAI({
    baseURL: "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
    apiKey: "{your-api-key}" 
});
```

To use the API key with environment variables set for `OPENAI_BASE_URL` and `OPENAI_API_KEY`:

```javascript
const client = new OpenAI();
```

**Microsoft Entra authentication**:

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

**API key authentication**:

```go
client := openai.NewClient(
    option.WithBaseURL("https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/"),
    option.WithAPIKey("{your-api-key}")
)
```

To use the API key with environment variables set for `OPENAI_BASE_URL` and `OPENAI_API_KEY`:

```go
client := openai.NewClient()
```


**Microsoft Entra authentication**:

```go
tokenCredential, err := azidentity.NewDefaultAzureCredential(nil)

client := openai.NewClient(
    option.WithBaseURL("https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/"),
    azure.WithTokenCredential(tokenCredential)
)
```

# [Java](#tab/Java)

[Java v1 examples](../../openai/supported-languages.md)

**API key authentication**:

```java

OpenAIClient client = OpenAIOkHttpClient.builder()
                .baseUrl("https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/")
                .apiKey(apiKey)
                .build();
```

To use the API key with environment variables set for `OPENAI_BASE_URL` and `OPENAI_API_KEY`:

```java
OpenAIClient client = OpenAIOkHttpClient.builder()
                .fromEnv()
                .build();
```

**Microsoft Entra authentication**:

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

**API key authentication**:

```bash
curl -X POST https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/responses \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
  -d '{
     "model": "gpt-4.1-nano",
     "input": "This is a test"
    }'
```

**Microsoft Entra authentication**:

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

For Azure OpenAI in Foundry Models, use the [Responses API](../../openai/supported-languages.md#responses-api). However, for other Foundry Models from providers like DeepSeek and Grok, the v1 API allows you to make chat completions calls, as these models support the OpenAI v1 chat completions syntax.

`base_url` accepts both `https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/` and `https://YOUR-RESOURCE-NAME.services.ai.azure.com/openai/v1/` formats.

# [Python](#tab/python)

**API key authentication**:
```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
)

completion = client.chat.completions.create(
  model="grok-3-mini", # Replace with your model deployment name.
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "When was Microsoft founded?"}
  ]
)

#print(completion.choices[0].message)
print(completion.model_dump_json(indent=2))
```


**Microsoft Entra authentication**:

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

**API key authentication**:

```csharp
using OpenAI;
using OpenAI.Chat;
using System.ClientModel;

string keyFromEnvironment = Environment.GetEnvironmentVariable("AZURE_OPENAI_API_KEY");

ChatClient client = new(
    model: "grok-3-mini",
    credential: new ApiKeyCredential(keyFromEnvironment),
    options: new OpenAIClientOptions() { 
    
        Endpoint = new Uri("https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/")
   }
);

ChatCompletion completion = client.CompleteChat("Tell me about the bitter lesson.'");

Console.WriteLine($"[ASSISTANT]: {completion.Content[0].Text}");

```

**Microsoft Entra authentication**:

A secure, keyless authentication approach is to use Microsoft Entra ID (formerly Azure Active Directory) via the [Azure Identity library](/dotnet/api/overview/azure/identity-readme?view=azure-dotnet&preserve-view=true ). To use the library:

```dotnetcli
dotnet add package Azure.Identity
```

Use the desired credential type from the library. For example, [`DefaultAzureCredential`](/dotnet/api/azure.identity.defaultazurecredential?view=azure-dotnet&preserve-view=true):

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

**API key authentication**:

API keys aren't recommended for production use because they're less secure than other authentication methods.

```javascript
import { OpenAI } from "openai";

const client = new OpenAI({
    baseURL: "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
    apiKey: process.env['OPENAI_API_KEY'] //Your Azure OpenAI API key
});

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

**Microsoft Entra authentication**:

```cmd
npm install @azure/identity
```

To authenticate the `OpenAI` client, use the `getBearerTokenProvider` function from the `@azure/identity` package. This function creates a token provider that `OpenAI` uses internally to obtain tokens for each request. Create the token provider as follows:

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

**API key authentication**:

```go
package main

import (
    "context"
    "fmt"

    "github.com/openai/openai-go/v2"
    "github.com/openai/openai-go/v2/option"
)

func main() {
    // Create a client with Azure OpenAI endpoint and API key
    client := openai.NewClient(
        option.WithBaseURL("https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/"),
        option.WithAPIKey("API-KEY-HERE"),
    )

    // Make a completion request
    chatCompletion, err := client.Chat.Completions.New(context.TODO(), openai.ChatCompletionNewParams{
        Messages: []openai.ChatCompletionMessageParamUnion{
            openai.UserMessage("Tell me about the bitter lesson"),
        },
        Model: "grok-3-mini", // Use your deployed model name on Azure
    })
    if err != nil {
        panic(err.Error())
    }

    fmt.Println(chatCompletion.Choices[0].Message.Content)
}
```

**Microsoft Entra authentication**:

Use the [azidentity](https://pkg.go.dev/github.com/Azure/azure-sdk-for-go/sdk/azidentity) module for Microsoft Entra ID authentication with Azure OpenAI.

```go
package main

import (
    "context"
    "fmt"

    "github.com/Azure/azure-sdk-for-go/sdk/azidentity"
    "github.com/openai/openai-go/v3"
    "github.com/openai/openai-go/v3/azure"
    "github.com/openai/openai-go/v3/option"
)

func main() {
    // Create an Azure credential
    tokenCredential, err := azidentity.NewDefaultAzureCredential(nil)
    if err != nil {
        panic(fmt.Sprintf("Failed to create credential: %v", err))
    }

    // Create a client with Azure OpenAI endpoint and token credential
    client := openai.NewClient(
        option.WithBaseURL("https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/"),
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

**API key authentication**:

```java
OpenAIClient client = OpenAIOkHttpClient.builder()
                .baseUrl("https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/")
                .apiKey(apiKey)
                .build();
```

**Microsoft Entra authentication**:

Authentication with Microsoft Entra ID requires some initial setup:

Add the Azure Identity package:

```xml
<dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-identity</artifactId>
    <version>1.18.0</version>
</dependency>
```

After setup, you can choose which type of credential from `azure.identity` to use. As an example, `DefaultAzureCredential` can be used to authenticate the client: Set the values of the client ID, tenant ID, and client secret of the Microsoft Entra ID application as environment variables: AZURE_CLIENT_ID, AZURE_TENANT_ID, AZURE_CLIENT_SECRET.

Authorization is easiest using `DefaultAzureCredential`. It finds the best credential to use in its running environment. However, use of `DefaultAzureCredential` is only recommended for testing, not for production.  

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

**API key authentication**:

```bash
curl -X POST https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
  -d '{
      "model": "grok-3-mini",
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

**Microsoft Entra authentication**:

```bash
curl -X POST https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AZURE_OPENAI_AUTH_TOKEN" \
  -d '{
      "model": "grok-3-mini",
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

---

## Related content

- [Work with chat completions models](../../openai/how-to/chatgpt.md)
- [Switch between OpenAI and Azure OpenAI endpoints](/azure/developer/ai/how-to/switching-endpoints)
- [Use embeddings models](../../model-inference/how-to/use-embeddings.md)
- [Use image embeddings models](../../model-inference/how-to/use-image-embeddings.md)
- [Use reasoning models](../../model-inference/how-to/use-chat-reasoning.md)
- [Basic Azure AI Foundry chat reference architecture](/azure/architecture/ai-ml/architecture/basic-azure-ai-foundry-chat)
