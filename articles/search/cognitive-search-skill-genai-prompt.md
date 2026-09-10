---
title: GenAI Prompt Skill
description: Invokes chat completion models from Azure OpenAI or other Microsoft Foundry-hosted models to create content at indexing time.
ms.reviewer: gimondra
ms.service: azure-ai-search
ms.custom:
  - build-2025
ms.topic: reference
ms.date: 07/28/2026
ai-usage: ai-assisted
---

# GenAI Prompt skill

[!INCLUDE [search-fiq-banner](./includes/search-fiq-banner.md)]

> [!IMPORTANT]
> These features and functionality support connections to other Microsoft services and third-party services. Use of these services is subject to their respective terms and might result in data processing or storage outside of the Azure compliance boundary, as well as data flowing into the Azure compliance boundary.
>
> It's your responsibility to manage whether your data will flow outside of your organization's compliance and geographic boundaries and any related implications, and that appropriate permissions, boundaries, and approvals are provisioned.
>
> You're responsible for carefully reviewing and testing applications you build in the context of your specific use cases and making all appropriate decisions and customizations. This includes implementing your own responsible AI mitigations, such as metaprompts, content filters, or other safety systems, and ensuring your applications meet appropriate quality, reliability, security, and trustworthiness standards. For more information, see the [Azure AI Search Transparency Note](/azure/foundry/responsible-ai/search/transparency-note).

The **GenAI (Generative AI) Prompt** skill executes a *chat completion* request against a large language model (LLM) deployed in [Azure OpenAI in Foundry Models](/azure/ai-services/openai/overview) or [Microsoft Foundry](../ai-foundry/what-is-foundry.md). Use this skill to create new information that can be indexed and stored as searchable content.

Here are some examples of how the GenAI prompt skill can help you create content:

- Verbalize images
- Summarize large passages of text
- Simplify complex content
- Perform any other task that you can articulate in a prompt

The GenAI Prompt skill is generally available in the [2026-04-01 Search Service REST API](/rest/api/searchservice/skillsets/create-or-update?view=rest-searchservice-2026-04-01&preserve-view=true) and in Azure SDKs that target this version. This skill supports text, image, and multimodal content, such as images with visuals and text extracted from PDF files.

> [!TIP]
> It's common to combine this skill with a data chunking skill. The [Multimodal tutorial](tutorial-multimodal.md) demonstrates image verbalization with two different data chunking strategies.

## Supported models

- You can use any [chat completion inference model](../ai-foundry/foundry-models/concepts/models.md) deployed in Foundry, such as GPT models, DeepSeek-R#, Llama-4-Maverick, and Cohere-command-r. For GPT models specifically, only the chat completions API endpoints are supported. Endpoints using the Azure OpenAI Responses API (containing `/openai/responses` in the URI) aren't currently compatible.

- For image verbalization, the model you use to analyze the image determines what image formats are supported.

- For GPT-5 models, the `temperature` parameter is not supported in the same way as previous models. If defined, it must be set to `1.0`, as other values will result in errors.

- Billing is based on the pricing of the model you use.

> [!NOTE]
> The search service connects to your model over a public endpoint, so there are no region location requirements. However, if you're using an all-up Azure solution, you should check the [Azure AI Search regions](search-region-support.md) and the [Azure OpenAI model regions](/azure/ai-services/openai/concepts/models) to find suitable pairs, especially if you have data residency requirements.

## Prerequisites

- An [Azure OpenAI in Foundry Models resource](../ai-foundry/openai/how-to/create-resource.md) or [Foundry project](../ai-foundry/how-to/create-projects.md).

- A [supported model](#supported-models) deployed to your resource or project.

  - For Azure OpenAI, copy the endpoint with the `openai.azure.com` domain from the **Keys and Endpoint** page in the Azure portal. Use this endpoint for the `Uri` parameter in this skill.

  - For Foundry, copy the target URI for the deployment from the **Models** page in the Foundry portal. Use this endpoint for the `Uri` parameter in this skill.

- Authentication can be key-based with an API key from your Foundry or Azure OpenAI resource. However, we recommend role-based access using a [search service managed identity](search-how-to-managed-identities.md) assigned to a role.

  - On Azure OpenAI, assign [**Cognitive Services OpenAI User**](/azure/ai-services/openai/how-to/role-based-access-control) to the managed identity.

  - On Foundry, assign [**Foundry User**](../ai-foundry/concepts/rbac-foundry.md#built-in-roles) to the managed identity.

    [!INCLUDE [role-rename-note](../foundry/includes/role-rename-note.md)]

## @odata.type  

`#Microsoft.Skills.Custom.ChatCompletionSkill`

## Data limits

| Limit | Notes |
|-------|-------|
| `maxTokens` | Default is **1024** if omitted. Maximum value is model-dependent. |
| Request time-out | Fixed at 30 seconds. Consider this limit when you choose a model for bulk indexing, as reasoning models (such as o1 and o3) might exceed it. |
| Images | Base 64–encoded images and image URLs are supported. Size limit is model-dependent. |

## Skill parameters

| Property | Type | Required | Notes |
|----------|------|----------|-------|
| `uri` | string | Yes | Endpoint of the deployed model. Supported domains are:<p><ul><li>`openai.azure.com`</li><li>`services.ai.azure.com`</li><li>`cognitiveservices.azure.com`</li></ul><p>[Azure API Management](/azure/api-management/api-management-key-concepts) endpoints are also supported, including API Management custom domains. For setup, including authentication, RBAC, and optional private connectivity, see [Use Azure API Management with Azure OpenAI skills and vectorizers](search-how-to-configure-azure-openai-api-management.md). |
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
        "properties": "{\"facts\":{\"type\":\"array\",\"items\":{\"type\":\"object\",\"properties\":{\"number\":{\"type\":\"number\"},\"fact\":{\"type\":\"string\"}},\"required\":[\"number\",\"fact\"]}}}",
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
| Model returns invalid JSON for `json_schema` | **Warning**: Raw string returned in `response` |

## Security considerations for managed identity authentication

When the GenAI Prompt skill uses managed identity authentication, Azure AI Search obtains a Microsoft Entra access token for the Foundry Tools audience (`https://cognitiveservices.azure.com`) and includes it in requests sent to the endpoint specified by `uri`. Managed identity authentication applies when `authIdentity` is set, or when both `apiKey` and `authIdentity` are empty and the service uses the system-assigned identity.

The endpoint referenced by `uri` is expected to be your own Azure OpenAI or Foundry resource. Supported domains are:

- `openai.azure.com`
- `cognitiveservices.azure.com`
- `services.ai.azure.com`

[Azure API Management (APIM)](/azure/api-management/api-management-key-concepts) endpoints (`*.azure-api.net`) and custom domains that front these resources are also supported. Because a custom domain or APIM hostname can't be verified from its name alone, Azure AI Search validates these endpoints with a live connectivity check at configuration time rather than by domain matching. You're responsible for configuring and maintaining the relationship between the endpoint and the Azure OpenAI or Foundry resource behind it.

> [!NOTE]
> A managed identity token issued for the Foundry Tools audience is valid against any Foundry Tools or Azure OpenAI resource the identity is authorized on. Sending it to an untrusted endpoint could expose the token.

### Recommended security practices

To help maintain a secure deployment, follow these practices:

- Set `uri` only to endpoints you own and trust. Prefer the Foundry Tools domains listed earlier. If you use an APIM or custom-domain endpoint, confirm it fronts your own resource before enabling managed identity. A trusted-looking hostname isn't proof of ownership.
- Apply the principle of least privilege to the managed identity used by the search service:
  - On Azure OpenAI, assign only **Cognitive Services OpenAI User**.
  - On Foundry, assign only **Foundry User**. Avoid granting broader roles.
- Use [Network Security Perimeter (NSP)](search-security-network-security-perimeter.md) and private endpoints or VNet integration to restrict which endpoints the search service can reach and which sources the target resource accepts requests from.
- If you use an APIM or custom-domain endpoint, ensure the gateway validates inbound requests and forwards them only to the intended backend. You should also review its access policies periodically.
- Prefer managed identity over `apiKey`. If you use `apiKey`, store and rotate it securely and don't embed it in source control. The service rejects configurations that set both `apiKey` and `authIdentity`.
- Periodically review skillset definitions, managed identity role assignments, and APIM and custom-domain configurations to confirm that `uri` values, access controls, and identity permissions remain current and appropriate. Review configuration changes through your established change-management and security-review processes.
- Monitor Azure OpenAI, Foundry Tools, and Foundry sign-in logs, authentication events, and access logs for unexpected or unauthorized activity.
- Remove unused skills, endpoints, role assignments, and API keys that are no longer required.

### Restrict access to skillset configuration

Users who can create, modify, or run skillsets control both the destination endpoint (`uri`) and the authentication configuration used by the skill. Because the skill sends a managed identity token for the Foundry Tools audience to that endpoint, restrict these permissions to trusted administrators and follow your standard change-management and security-review processes when configuring managed identity–enabled skills.

## See also

- [Azure AI Search built-in indexers](search-indexer-overview.md)
- [Integrated vectorization](vector-search-integrated-vectorization.md)
- [How to define a skillset](cognitive-search-defining-skillset.md)  
- [How to generate chat completions with Azure AI model inference (Foundry)](../ai-foundry/foundry-models/how-to/use-chat-completions.md)  
- [Structured outputs in Azure OpenAI](/azure/ai-services/openai/how-to/structured-outputs)  
