---
title: Azure OpenAI in Microsoft Foundry Models API version lifecycle
description: Learn about the Azure OpenAI API lifecycle, including the v1 API and changes from previous API versions.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: concept-article 
ms.date: 01/31/2026
author: mrbullwinkle
ms.author: mbullwin
recommendations: false
monikerRange: 'foundry-classic || foundry'
---

# Azure OpenAI in Microsoft Foundry Models API lifecycle

Azure OpenAI APIs follow a structured lifecycle. This article covers the new v1 API, which simplifies authentication, removes the need for dated `api-version` parameters, and supports cross-provider model calls.

> [!NOTE]
> New API response objects may be added to the API response at any time. We recommend you only parse the response objects you require.
>

## Prerequisites

- An Azure subscription - [Create one for free](https://azure.microsoft.com/free/cognitive-services)
- An [Azure OpenAI resource](/azure/ai-foundry/openai/how-to/create-resource) deployed in a [supported region](https://azure.microsoft.com/explore/global-infrastructure/products-by-region/?products=cognitive-services)
- At least one [model deployment](../foundry-models/how-to/deploy-foundry-models.md)

## API evolution

Previously, Azure OpenAI received monthly updates of new API versions. Taking advantage of new features required constantly updating code and environment variables with each new API release. Azure OpenAI also required the extra step of using Azure specific clients which created overhead when migrating code between OpenAI and Azure OpenAI.

Starting in August 2025, you can now opt in to our next generation v1 Azure OpenAI APIs which add support for:

- Ongoing access to the latest features with no need to specify new `api-version`'s each month.
- Faster API release cycle with new features launching more frequently.
- OpenAI client support with minimal code changes to swap between OpenAI and Azure OpenAI when using key-based authentication.
- OpenAI client support for token based authentication and automatic token refresh without the need to take a dependency on a separate Azure OpenAI client.
- Make chat completions calls with models from other providers like DeepSeek and Grok which support the v1 chat completions syntax.

Access to new API calls that are still in preview will be controlled by passing feature specific preview headers allowing you to opt in to the features you want, without having to swap API versions. Alternatively, some features will indicate preview status through their API path and don't require an additional header.

Examples:

- `/openai/v1/evals` is in preview and requires passing an `"aoai-evals":"preview"` header.
- `/openai/v1/fine_tuning/alpha/graders/` is in preview and requires no custom header due to the presence of `alpha` in the API path.

For the initial v1 Generally Available (GA) API launch we're only supporting a subset of the inference and authoring API capabilities. All GA features are supported for use in production. We'll be rapidly adding support for more capabilities soon.  

## Code changes

# [Python](#tab/python)

### v1 API

[Python v1 examples](./supported-languages.md)

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

**API Key** with environment variables set for `OPENAI_BASE_URL` and `OPENAI_API_KEY`:

```python
client = OpenAI()
```

**Microsoft Entra ID**:

> [!IMPORTANT]
> Handling automatic token refresh was previously handled through use of the `AzureOpenAI()` client. The v1 API removes this dependency, by adding automatic token refresh support to the `OpenAI()` client.

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

### v1 API

[C# v1 examples](./supported-languages.md)

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

### v1 API

[JavaScript v1 examples](./supported-languages.md)

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

### v1 API

[Go v1 examples](./supported-languages.md)

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

[Java v1 examples](./supported-languages.md)

### v1 API

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

### v1 API

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

## Model support

For Azure OpenAI models we recommend using the [Responses API](./supported-languages.md), however, the v1 API also allows you to make chat completions calls with models from other providers like DeepSeek and Grok which support the OpenAI v1 chat completions syntax.

`base_url` will accept both `https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/` and `https://YOUR-RESOURCE-NAME.services.ai.azure.com/openai/v1/` formats.

> [!NOTE]
> Responses API also works with Foundry Models sold directly by Azure, such as Microsoft AI, DeepSeek, and Grok models. To learn how to use the Responses API with these models, see [How to generate text responses with Microsoft Foundry Models](../foundry-models/how-to/generate-responses.md).

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
  model="MAI-DS-R1", # Replace with your model deployment name.
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
    model: "MAI-DS-R1", // Replace with your model deployment name.
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
    model: 'MAI-DS-R1', // model deployment name
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
	"log"

	"github.com/Azure/azure-sdk-for-go/sdk/azidentity"
	"github.com/openai/openai-go/v3"
	"github.com/openai/openai-go/v3/azure"
	"github.com/openai/openai-go/v3/option"
)

func main() {
	// Create an Azure credential
	tokenCredential, err := azidentity.NewDefaultAzureCredential(nil)
	if err != nil {
		log.Fatalf("Failed to create credential: %s", err)
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
		Model: "MAI-DS-R1", // Use your deployed model name on Azure
	})
	if err != nil {
		log.Fatalf("Failed to get chat completions: %s", err)
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
        String modelDeploymentName = "MAI-DS-R1"; //replace with your model deployment name

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
      "model": "MAI-DS-R1",
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

### Status

Generally Available features are supported for use in production.

| API Path                               | Status              |
|----------------------------------------|---------------------|
| `/openai/v1/chat/completions`          | Generally Available |
| `/openai/v1/embeddings`                | Generally Available |
| `/openai/v1/evals`                     | Preview             |
| `/openai/v1/files`                     | Generally Available |
| `/openai/v1/fine_tuning/jobs/{fine_tuning_job_id}/checkpoints/{fine_tuning_checkpoint_id}/copy` | Preview |
| `/openai/v1/fine_tuning/alpha/graders/`| Preview             |
| `/openai/v1/fine_tuning/`              | Generally Available |
| `/openai/v1/models`                    | Generally Available |
| `/openai/v1/responses`                 | Generally Available |
| `/openai/v1/vector_stores`             | Generally Available |

### Preview headers

| API Path                              | Header                   |
|---------------------------------------|:-------------------------|
| `/openai/v1/evals`                    | `"aoai-evals":"preview"` |
| `/openai/v1/fine_tuning/jobs/{fine_tuning_job_id}/checkpoints/{fine_tuning_checkpoint_id}/copy` | `"aoai-copy-ft-checkpoints" : "preview"` |

## Changes between v1 preview release and 2025-04-01-preview

- [v1 preview API](#api-evolution)
- [Video generation support](./concepts/video-generation.md)
- **NEW** Responses API features:
    * Remote Model Context Protocol (MCP) servers tool integration
    * Support for asynchronous background tasks
    * Encrypted reasoning items
    * Image generation  

## Changes between 2025-04-01-preview and 2025-03-01-preview

- [`GPT-image-1` support](/azure/ai-foundry/openai/how-to/dall-e)
- [Reasoning summary for `o3` and `o4-mini`](/azure/ai-foundry/openai/how-to/reasoning)
- [Evaluation API](/azure/ai-foundry/openai/authoring-reference-preview#evaluation---create)

## Changes between 2025-03-01-preview and 2025-02-01-preview

- [Responses API](./how-to/responses.md)
- Computer use

## Changes between 2025-02-01-preview and 2025-01-01-preview

- Stored completions (distillation API support).

## Changes between 2025-01-01-preview and 2024-12-01-preview

- `prediction` parameter added for [predicted outputs](./how-to/predicted-outputs.md) support.
- `gpt-4o-audio-preview` [model support](./audio-completions-quickstart.md).

## Changes between 2024-12-01-preview and 2024-10-01-preview

- `store`, and `metadata` parameters added for stored completions support.
- `reasoning_effort` added for latest [reasoning models](./how-to/reasoning.md).
- `user_security_context` added for [Microsoft Defender for Cloud integration](https://aka.ms/TP4AI/Documentation/EndUserContext).

## Changes between 2024-09-01-preview and 2024-08-01-preview

- `max_completion_tokens` added to support `o1-preview` and `o1-mini` models. `max_tokens` doesn't work with the **o1 series** models.
- `parallel_tool_calls` added.
- `completion_tokens_details` & `reasoning_tokens` added.
- `stream_options` & `include_usage` added.

## Changes between 2024-07-01-preview and 2024-08-01-preview API specification

- [Structured outputs support](./how-to/structured-outputs.md).
- Large file upload API added.
- On your data changes:
    * Mongo DB integration.
    * `role_information` parameter removed.
    *  [`rerank_score`](https://github.com/Azure/azure-rest-api-specs/blob/2b700e5e84d4a95880d373e6a4bce5d16882e4b5/specification/cognitiveservices/data-plane/AzureOpenAI/inference/preview/2024-08-01-preview/inference.json#L5532) added to citation object.
    * AML datasource removed.
    * AI Search vectorization integration improvements.

## Changes between 2024-5-01-preview and 2024-07-01-preview API specification

- [Batch API support added](./how-to/batch.md)
- [Vector store chunking strategy parameters](/azure/ai-foundry/openai/reference-preview?#request-body-17)
- `max_num_results` that the file search tool should output.

## Changes between 2024-04-01-preview and 2024-05-01-preview API specification

- Assistants v2 support - [File search tool and vector storage](https://go.microsoft.com/fwlink/?linkid=2272425)
- Fine-tuning [checkpoints](https://github.com/Azure/azure-rest-api-specs/blob/9583ed6c26ce1f10bbea92346e28a46394a784b4/specification/cognitiveservices/data-plane/AzureOpenAI/authoring/preview/2024-05-01-preview/azureopenai.json#L586), [seed](https://github.com/Azure/azure-rest-api-specs/blob/9583ed6c26ce1f10bbea92346e28a46394a784b4/specification/cognitiveservices/data-plane/AzureOpenAI/authoring/preview/2024-05-01-preview/azureopenai.json#L1574), [events](https://github.com/Azure/azure-rest-api-specs/blob/9583ed6c26ce1f10bbea92346e28a46394a784b4/specification/cognitiveservices/data-plane/AzureOpenAI/authoring/preview/2024-05-01-preview/azureopenai.json#L529)
- On your data updates
- DALL-E 2 now supports model deployment and can be used with the latest preview API.
- Content filtering updates

## Changes between 2024-03-01-preview and 2024-04-01-preview API specification

- **Breaking Change**: Enhancements parameters removed. This impacts the `gpt-4` **Version:** `vision-preview` model.
- [timestamp_granularities](https://github.com/Azure/azure-rest-api-specs/blob/fbc90d63f236986f7eddfffe3dca6d9d734da0b2/specification/cognitiveservices/data-plane/AzureOpenAI/inference/preview/2024-04-01-preview/inference.json#L5217) parameter added.
- [`audioWord`](https://github.com/Azure/azure-rest-api-specs/blob/fbc90d63f236986f7eddfffe3dca6d9d734da0b2/specification/cognitiveservices/data-plane/AzureOpenAI/inference/preview/2024-04-01-preview/inference.json#L5286) object added.
- Additional TTS [`response_formats: wav & pcm`](https://github.com/Azure/azure-rest-api-specs/blob/fbc90d63f236986f7eddfffe3dca6d9d734da0b2/specification/cognitiveservices/data-plane/AzureOpenAI/inference/preview/2024-04-01-preview/inference.json#L5333).


## Known issues

- The `2025-04-01-preview` Azure OpenAI spec uses OpenAPI 3.1. It's a known issue that this version isn't fully supported by [Azure API Management](/azure/api-management/api-management-key-concepts).


## Next steps

- [Learn more about Azure OpenAI](../foundry-models/concepts/models-sold-directly-by-azure.md)
- [Learn about working with Azure OpenAI models](./how-to/working-with-models.md)
- [Supported programming languages for the v1 API](./supported-languages.md)
- [Azure OpenAI quotas and limits](/azure/ai-foundry/openai/quotas-limits)
- [v1 OpenAPI 3.0 spec](https://github.com/Azure/azure-rest-api-specs/blob/main/specification/ai/data-plane/OpenAI.v1/azure-v1-v1-generated.json)
