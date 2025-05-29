---
title: GenAI Prompt skill (Preview)
titleSuffix: Azure AI Search
description: Invokes Chat Completion models from Azure OpenAI or other Azure AI Foundry-hosted models at indexing time.
author: gmndrg
ms.author: gimondra
ms.service: azure-ai-search
ms.custom:
  - build-2025
ms.topic: reference
ms.date: 05/27/2025
---

# GenAI Prompt skill

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

The **GenAI (Generative AI) Prompt** skill executes a *chat completion* request against a Large Language Model (LLM) deployed in Azure AI Foundry or Azure OpenAI in Azure AI Foundry Models.  

Use this capability to create new information that can be indexed and stored as searchable content. Examples include verbalize images, summarize larger passages, simplify complex content, or any other task that an LLM can perform. The skill supports text, image, and multimodal content such as a PDF that contains text and images. It's common to use this skill combined with a data chunking skill. The following tutorials demonstrate the image verbalization scenarios with two different data chunking techniques: 

- [Tutorial: Index mixed content using image verbalizations and the Document Layout skill](tutorial-document-layout-image-verbalization.md)

- [Tutorial: Index mixed content using image verbalizations and the Document Extraction skill](tutorial-document-extraction-image-verbalization.md)

The GenAI Prompt skill is available in the [2025-05-01-preview REST API](/rest/api/searchservice/skillsets/create?view=rest-searchservice-2025-05-01-preview&preserve-view=true) only. 

## Supported models

You can use any [chat completion inference model](/azure/ai-foundry/model-inference/concepts/models) deployed in AI Foundry, such as GPT models, Deepseek R#, Llama-4-Mavericj, Cohere-command-r, and so forth.

Billing is based on the pricing of the model you use.

> [!NOTE]
> The search service connects to your model over a public endpoint, so there are no region location requirements, but if you're using an all-up Azure solution, you should check the [Azure AI Search regions](search-region-support.md) and the [Azure OpenAI model regions](/azure/ai-services/openai/concepts/models) to find suitable pairs, especially if you have data residency requirements.
>

## Prerequisites

- A deployed chat completion model (for example *gpt-4o* or any compatible Open Source Software (OSS) model) in Azure AI Foundry or Azure OpenAI.

  - Copy the endpoint from **Models + Endpoints** in the Foundry portal or from the Azure OpenAI resource subdomain (`*.openai.azure.com`).

  - Provide this endpoint in the `Uri` parameter of your skill definition.

- Authentication can be key-based with an API key from your Azure AI Foundry or Azure OpenAI resource. However, we recommend role-based access using a [search service managed identity](search-howto-managed-identities-data-sources.md) assigned to a role.

  - On Azure OpenAI, assign [**Cognitive Services OpenAI User**](/azure/ai-services/openai/how-to/role-based-access-control) to the managed identity.

  - For AI Foundry models, assign [**Azure AI User**](/azure/ai-foundry/concepts/rbac-azure-ai-foundry#azure-ai-user).

## @odata.type  

`#Microsoft.Skills.Custom.ChatCompletionSkill`

## Data limits

| Limit | Notes |
|-------|-------|
| `maxTokens` | Default is **1024** if omitted. Maximum value is model-dependent. |
| Request time-out | 30 seconds (default). Override with the `timeout` property (`PT##S`). |
| Images | Base 64–encoded images and image URLs are supported. Size limit is model-dependent. |

## Skill parameters

| Property | Type | Required | Notes |
|----------|------|----------|-------|
| `uri` | string | Yes | Public endpoint of the deployed model. |
| `apiKey` | string | Cond.* | Secret key for the model. Leave blank when using managed identity. |
| `authIdentity` | string | Cond.* | **User-assigned** managed identity client ID (*Azure OpenAI only*). Leave blank to use the **system-assigned** identity. |
| `commonModelParameters` | object | No | Standard generation controls such as `temperature`, `maxTokens`, etc. |
| `extraParameters` | object | No | Open dictionary passed through to the underlying model API. |
| `extraParametersBehavior` | string | No | `"pass-through"` \| `"drop"` \| `"error"` (default `"error"`). |
| `responseFormat` | object | No | Controls whether the model returns **text**, a free-form **JSON object**, or a strongly typed **JSON schema**. `responseFormat` payload examples: {responseFormat: { type: text }}, {responseFormat: { type: json_object }}, {responseFormat: { type: json_schema }} |

\* **Exactly one** of `apiKey`, `authIdentity`, or the service’s **system-assigned** identity must be used.

### `commonModelParameters` defaults

| Parameter | Default |
|-----------|---------|
| `model` | *(deployment default)* |
| `frequencyPenalty` | 0 |
| `presencePenalty` | 0 |
| `maxTokens` | 1024 |
| `temperature` | 0.7 |
| `seed` | *null* |
| `stop` | *null* |

## Skill inputs

| Input name | Type | Required | Description |
|------------|------|----------|-------------|
| `systemMessage` | string | Yes | System-level instruction (ex: *"You are a helpful assistant."*). |
| `userMessage` | string | Yes | User prompt. |
| `text` | string | No | Optional text appended to `userMessage` (text-only scenarios). |
| `image` | string (Base 64 data-URL) | No | Adds an image to the prompt (multimodal models only). |
| `imageDetail` | string (`low` \| `high` \| `auto`) | No | Fidelity hint for Azure OpenAI multimodal models. |

## Skill outputs

| Output name | Type | Description |
|-------------|------|-------------|
| `response` | string **or** JSON object | Model output in the format requested by `responseFormat.type`. |
| `usageInformation` | JSON object | Token counts and echo of model parameters. |

## Sample definitions

### Text-only summarization

```json
{
  "@odata.type": "#Microsoft.Skills.Custom.ChatCompletionSkill",
  "name": "Summarizer",
  "description": "Summarizes document content.",
  "context": "/document",
  "timeout": "PT30S",
  "inputs": [
    { "name": "text", "source": "/document/content" },
    { "name": "systemMessage", "source": "='You are a concise AI assistant.'" },
    { "name": "userMessage", "source": "='Summarize the following text:'" }
  ],
  "outputs": [ { "name": "response" } ],
  "uri": "https://demo.openai.azure.com/openai/deployments/gpt-4o/chat/completions",
  "apiKey": "<api-key>",
  "commonModelParameters": { "temperature": 0.3 }
}
```

### Text + image description

```json
{
  "@odata.type": "#Microsoft.Skills.Custom.ChatCompletionSkill",
  "name": "Image Describer",
  "context": "/document/normalized_images/*",
  "inputs": [
    { "name": "image", "source": "/document/normalized_images/*/data" },
    { "name": "imageDetail", "source": "=high" },
    { "name": "systemMessage", "source": "='You are a useful AI assistant.'" },
    { "name": "userMessage", "source": "='Describe this image:'" }
  ],
  "outputs": [ { "name": "response" } ],
  "uri": "https://demo.openai.azure.com/openai/deployments/gpt-4o/chat/completions",
  "authIdentity": "11111111-2222-3333-4444-555555555555",
  "responseFormat": { "type": "text" }
}
```

### Structured numerical fact-finder

```json
{
  "@odata.type": "#Microsoft.Skills.Custom.ChatCompletionSkill",
  "name": "NumericalFactFinder",
  "context": "/document",
  "inputs": [
    { "name": "systemMessage", "source": "='You are an AI assistant that helps people find information.'" },
    { "name": "userMessage", "source": "='Find all the numerical data and put it in the specified fact format.'"}, 
    { "name": "text", "source": "/document/content" }
  ],
  "outputs": [ { "name": "response" } ],
  "uri": "https://demo.openai.azure.com/openai/deployments/gpt-4o/chat/completions",
  "apiKey": "<api-key>",
  "responseFormat": {
    "type": "json_schema",
    "jsonSchemaProperties": {
      "name": "NumericalFactObj",
      "strict": true,
      "schema": {
        "type": "object",
        "properties": {
          "facts": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "number": { "type": "number" },
                "fact": { "type": "string" }
              },
              "required": [ "number", "fact" ]
            }
          }
        },
        "required": [ "facts" ],
        "additionalProperties": false
      }
    }
  }
}
```

### Sample output (truncated)

```json
{
  "response": {
    "facts": [
      { "number": 32.0, "fact": "Jordan scored 32 points per game in 1986-87." },
      { "number": 6.0,  "fact": "He won 6 NBA championships." }
    ]
  },
  "usageInformation": {
    "usage": {
      "completion_tokens": 203,
      "prompt_tokens": 248,
      "total_tokens": 451
    }
  }
}
```

### Best practices

- Chunk long documents with the **Text Split** skill to stay within the model’s context window.  
- For high-volume indexing, dedicate a separate model deployment to this skill so that token quotas for query-time RAG workloads remain unaffected.  
- To minimize latency, co-locate the model and your Azure AI Search service in the same Azure region.  
- Use `responseFormat.json_schema` with **GPT-4o** for reliable structured extraction and easier mapping to index fields.  
- Monitor token usage and submit **quota-increase requests** if the indexer saturates your Tokens per Minute (TPM) limits.  

### Errors and warnings

| Condition | Result |
|-----------|--------|
| Missing or invalid `uri` | **Error** |
| No authentication method specified | **Error** |
| Both `apiKey` and `authIdentity` supplied | **Error** |
| Unsupported model for multimodal prompt | **Error** |
| Input exceeds model token limit | **Error** |
| Model returns invalid JSON for `json_schema` | **Warning** – raw string returned in `response` |


### See also

- [Azure AI Search built-in indexers](search-indexer-overview.md)
- [Integrated vectorization](vector-search-integrated-vectorization.md)
- [How to define a skillset](cognitive-search-defining-skillset.md)  
- [How to generate chat completions with Azure AI model inference (Azure AI Foundry)](/azure/ai-foundry/model-inference/how-to/use-chat-completions)  
- [Structured outputs in Azure OpenAI](/azure/ai-services/openai/how-to/structured-outputs)  
