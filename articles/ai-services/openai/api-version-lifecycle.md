---
title: Azure OpenAI in Azure AI Foundry Models API version lifecycle
description: Learn more about API version retirement in Azure OpenAI.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-openai
ms.topic: conceptual 
ms.date: 05/25/2025
author: mrbullwinkle
ms.author: mbullwin
recommendations: false
ms.custom:
---

# Azure OpenAI in Azure AI Foundry Models API lifecycle

This article is to help you understand the support lifecycle for Azure OpenAI APIs.

> [!NOTE]
> New API response objects may be added to the API response without version changes. We recommend you only parse the response objects you require.
>
> The `2025-04-01-preview` Azure OpenAI spec uses OpenAPI 3.1, is a known issue that this is currently not fully supported by [Azure API Management](/azure/api-management/api-management-key-concepts)

## API evolution

Historically, Azure OpenAI received monthly updates of new API versions. Taking advantage of new features required constantly updating code and environment variables with each new API release. Azure OpenAI also required the extra step of using Azure specific clients which created overhead when migrating code between OpenAI and Azure OpenAI. Starting in May 2025, you can now opt in to our next generation of v1 Azure OpenAI APIs which add support for:

- Ongoing access to the latest features with no need to update `api-version` each month.
- OpenAI client support with minimal code changes to swap between OpenAI and Azure OpenAI when using key-based authentication.

For the initial preview launch we are only supporting a subset of the inference API. While in preview, operations may have incomplete functionality that will be continually expanded.

## Code changes

# [API Key](#tab/key)

### Last generation API 

```python
import os
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
    api_version="2025-04-01-preview",
    azure_endpoint="https://YOUR-RESOURCE-NAME.openai.azure.com")
    )

response = client.responses.create(
    model="gpt-4.1-nano", # Replace with your model deployment name 
    input="This is a test."
)

print(response.model_dump_json(indent=2)) 
```

### Next generation API

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
    default_query={"api-version": "preview"}, 
)

response = client.responses.create(   
  model="gpt-4.1-nano", # Replace with your model deployment name 
  input="This is a test.",
)

print(response.model_dump_json(indent=2)) 
```

- `OpenAI()` client is used instead of `AzureOpenAI()`.
- `base_url` passes the Azure OpenAI endpoint and `/openai/v1` is appended to the endpoint address.
- `default_query={"api-version": "preview"}` indicates that the version-less always up-to-date preview API is being used.

Once we release the GA next generation v1 API, we will support two values: `latest` and `preview`. If `api-version` is not passed traffic is automatically routed to the `latest` GA version. Currently only `preview` is supported.

# [Microsoft Entra ID](#tab/entra)

### Last generation API 

```python
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

client = AzureOpenAI(
  azure_endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/", 
  azure_ad_token_provider=token_provider,
  api_version="2025-04-01-preview"
)

response = client.responses.create(
    model="gpt-4.1-nano", # Replace with your model deployment name 
    input="This is a test."
)

print(response.model_dump_json(indent=2)) 
```

### Next generation API


```python
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

client = AzureOpenAI(  
  base_url = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",  
  azure_ad_token_provider=token_provider,
  api_version="preview"
)

response = client.responses.create(
    model="gpt-4.1-nano",
    input= "This is a test" 
)

print(response.model_dump_json(indent=2)) 
```

- `AzureOpenAI()` is used to take advantage of automatic token refresh provided by `azure_ad_token_provider`.
- `base_url` passes the Azure OpenAI endpoint and `/openai/v1` is appended to the endpoint address.
- `api-version="preview"` indicates that the version-less always up-to-date preview API is being used.

Once we release the GA next generation v1 API, we will support two values: `latest` and `preview`. If `api-version` is not passed traffic is automatically routed to the `latest` GA version. Currently only `preview` is supported.

# [REST](#tab/rest)

### Last generation API 

**API Key**:

```bash
curl -X POST https://YOUR-RESOURCE-NAME.openai.azure.com/openai/responses?api-version=2025-04-01-preview \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
  -d '{
     "model": "gpt-4.1-nano",
     "input": "This is a test"
    }'
```

**Microsoft Entra ID**:

```bash
curl -X POST https://YOUR-RESOURCE-NAME.openai.azure.com/openai/responses?api-version=2025-04-01-preview \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AZURE_OPENAI_AUTH_TOKEN" \
  -d '{
     "model": "gpt-4.1-nano",
     "input": "This is a test"
    }'
```

### Next generation API

**API Key**:

```bash
curl -X POST https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/responses?api-version=preview \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
  -d '{
     "model": "gpt-4.1-nano",
     "input": "This is a test"
    }'
```

**Microsoft Entra ID**:

```bash
curl -X POST https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/responses?api-version=preview \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AZURE_OPENAI_AUTH_TOKEN" \
  -d '{
     "model": "gpt-4o",
     "input": "This is a test"
    }'
```

# [Output](#tab/output)

```json
{
  "id": "resp_682f7eb5dc408190b491cbbe57be2fbf0f98d661c3dc276d",
  "created_at": 1747943093.0,
  "error": null,
  "incomplete_details": null,
  "instructions": null,
  "metadata": {},
  "model": "gpt-4.1-nano",
  "object": "response",
  "output": [
    {
      "id": "msg_682f7eb61d908190926a004c15c5ddd00f98d661c3dc276d",
      "content": [
        {
          "annotations": [],
          "text": "Hello! It looks like you've sent a test message. How can I assist you today?",
          "type": "output_text"
        }
      ],
      "role": "assistant",
      "status": "completed",
      "type": "message"
    }
  ],
  "parallel_tool_calls": true,
  "temperature": 1.0,
  "tool_choice": "auto",
  "tools": [],
  "top_p": 1.0,
  "background": null,
  "max_output_tokens": null,
  "previous_response_id": null,
  "reasoning": {
    "effort": null,
    "generate_summary": null,
    "summary": null
  },
  "service_tier": "default",
  "status": "completed",
  "text": {
    "format": {
      "type": "text"
    }
  },
  "truncation": "disabled",
  "usage": {
    "input_tokens": 12,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 19,
    "output_tokens_details": {
      "reasoning_tokens": 0
    },
    "total_tokens": 31
  },
  "user": null,
  "store": true
}
```

---

## Preview API releases

Azure OpenAI API latest releases:

- [**NEW** v1 Preview API](reference-preview-latest.md)
- Inference: [2025-04-01-preview](reference-preview.md)
- Authoring: [2025-04-01-preview](authoring-reference-preview.md)

## Changes between v1 preview release and 2025-04-01-preview

- [v1 preview API](#api-evolution)
- [Video generation support](./concepts/video-generation.md)
- **NEW** Responses API features:
    * Remote Model Context Protocol (MCP) servers tool integration
    * Support for asynchronous background tasks
    * Encrypted reasoning items
    * Image generation  

## Changes between 2025-04-01-preview and 2025-03-01-preview

- [`GPT-image-1` support](/azure/ai-services/openai/how-to/dall-e)
- [Reasoning summary for `o3` and `o4-mini`](/azure/ai-services/openai/how-to/reasoning)
- [Evaluation API](/azure/ai-services/openai/authoring-reference-preview#evaluation---create)

## Changes between 2025-03-01-preview and 2025-02-01-preview

- [Responses API](./how-to/responses.md)
- [Computer use](./how-to/computer-use.md)

## Changes between 2025-02-01-preview and 2025-01-01-preview

- [Stored completions (distillation)](./how-to/stored-completions.md#stored-completions-api) API support.

## Changes between 2025-01-01-preview and 2024-12-01-preview

- `prediction` parameter added for [predicted outputs](./how-to/predicted-outputs.md) support.
- `gpt-4o-audio-preview` [model support](./audio-completions-quickstart.md).

## Changes between 2024-12-01-preview and 2024-10-01-preview

- `store`, and `metadata` parameters added for [stored completions support](./how-to/stored-completions.md).
- `reasoning_effort` added for latest [reasoning models](./how-to/reasoning.md).
- `user_security_context` added for [Microsoft Defender for Cloud integration](https://aka.ms/TP4AI/Documentation/EndUserContext).

## Changes between 2024-09-01-preview and 2024-08-01-preview

- `max_completion_tokens` added to support `o1-preview` and `o1-mini` models. `max_tokens` does not work with the **o1 series** models.
- `parallel_tool_calls` added.
- `completion_tokens_details` & `reasoning_tokens` added.
- `stream_options` & `include_usage` added.

## Changes between 2024-07-01-preview and 2024-08-01-preview API specification

- [Structured outputs support](./how-to/structured-outputs.md).
- Large file upload API added.
- On your data changes:
    * [Mongo DB integration](./reference-preview.md#example-7).
    * `role_information` parameter removed.
    *  [`rerank_score`](https://github.com/Azure/azure-rest-api-specs/blob/2b700e5e84d4a95880d373e6a4bce5d16882e4b5/specification/cognitiveservices/data-plane/AzureOpenAI/inference/preview/2024-08-01-preview/inference.json#L5532) added to citation object.
    * AML datasource removed.
    * AI Search vectorization integration improvements.

## Changes between 2024-5-01-preview and 2024-07-01-preview API specification

- [Batch API support added](./how-to/batch.md)
- [Vector store chunking strategy parameters](/azure/ai-services/openai/reference-preview?#request-body-17)
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

## Latest GA API release

Azure OpenAI API version [2024-10-21](./reference.md) is currently the latest GA API release. This API version is the replacement for the previous `2024-06-01` GA API release.

## Updating API versions

We recommend first testing the upgrade to new API versions to confirm there's no impact to your application from the API update before making the change globally across your environment.

If you're using the OpenAI Python or JavaScript client libraries, or the REST API, you'll need to update your code directly to the latest preview API version.

If you're using one of the Azure OpenAI SDKs for C#, Go, or Java, you'll instead need to update to the latest version of the SDK. Each SDK release is hardcoded to work with specific versions of the Azure OpenAI API.

## Next steps

- [Learn more about Azure OpenAI](overview.md)
- [Learn about working with Azure OpenAI models](./how-to/working-with-models.md)
