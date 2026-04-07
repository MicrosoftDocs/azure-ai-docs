---
title: include file
description: include file
author: sdgilley
ms.author: sgilley
ms.reviewer: deeikele
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 03/19/2026
ms.custom: include, classic-and-new
---



## Choose an integration pattern

Foundry supports multiple integration patterns:

* Low-code connectors for software as a service (SaaS) platforms like Power Platform
* Direct REST API integration for full control
* API gateway mediation for centralized management

The following sections describe each pattern.

### Use connector-based integration

Use this pattern when your platform natively supports built-in integration to Foundry or Azure OpenAI (for example when using Microsoft Power Platform or Logic Apps).

- **Power Platform**: Use the [Azure OpenAI connector](/connectors/azureopenai/) in Power Apps, Power Automate, or Logic Apps.
- **Third-party platforms**: Various third-party software vendors provide prebuilt Azure OpenAI or Foundry modules for chat, image generation, and transcription.

### Call the REST API directly

Use direct REST calls when you're building your own application or when you need full control over HTTP calls. Choose between Foundry endpoint variants to access agentic or cross-model provider APIs, or use Azure OpenAI endpoint if your integration expects OpenAI v1 semantics.

- **Foundry endpoint** for stateless API integration such as model inference:
  ```REST
  POST https://{resource}.services.ai.azure.com/api/
  ```

- **Foundry project endpoint** for stateful APIs such as agent service:
  ```REST
  POST https://{resource}.services.ai.azure.com/api/projects/{projectname}/
  ```

- **OpenAI v1-compatible route** for applications that expect the OpenAI API shape:
  ```REST
  POST https://{resource}.openai.azure.com/openai/v1/
  ```

  > [!IMPORTANT]
  > Don't use the Foundry Model Inference API (`https://<resource>.services.ai.azure.com/models` path) for new integrations. The Azure AI Inference beta SDK is deprecated and will be retired on May 30, 2026. Use the OpenAI v1-compatible route instead. For details, see the [migration guide](../how-to/model-inference-to-openai-migration.md).

### Route through an API gateway

To establish a single entry point across multiple model hosts, use [Azure API Management (APIM)](/azure/api-management/) as an AI gateway to centralize authentication, quota governance, and routing.

1. Place APIM in front of Foundry or Azure OpenAI endpoints.
1. Apply policies for authentication, token budgets, semantic caching, and routing.

To learn more, see [API Management for AI](/azure/api-management/azure-ai-foundry-api).

### Enrich data pipelines

1. Use Microsoft Fabric notebooks or pipelines to invoke models for batch or streaming enrichment.
1. Write results back to OneLake for downstream analytics and governance.

To learn more, see [Foundry in Fabric](/fabric/data-science/ai-services/ai-services-overview).

## Send a REST API request

Foundry supports direct HTTP calls for scenarios where you need full control. Use the REST API when:

- Your tool doesn't have a native Foundry or Azure OpenAI connector.
- You want to embed calls in scripts, automation pipelines, or custom adapters.
- You need compatibility with OpenAI v1 for third-party SDKs or connectors.

To call the API:

1. Choose the correct endpoint shape:
   - **Foundry API** (`services.ai.azure.com`) for a model-provider agnostic schema and access to Foundry-exclusive features.
   - **OpenAI v1 compatibility** for tools expecting OpenAI request/response schema.
1. Include authentication headers:
   - `Authorization: Bearer {entra-token}` for Microsoft Entra ID authentication (recommended).
   - `api-key: {your-key}` for API key authentication.
1. Send a JSON payload with your model name and messages.

For full schema details, see:
- [Swagger for Foundry REST API](/rest/api/aifoundry/)
- [Swagger for OpenAI v1 compatibility](../openai/latest.md)

The following examples use Microsoft Entra ID authentication. Replace the placeholder values with your own.

# [Foundry](#tab/foundry)

Replace YOUR-FOUNDRY-RESOURCE-NAME and YOUR-PROJECT-NAME with your values. This example calls the Responses API:

```console
export AZURE_AI_AUTH_TOKEN=$(az account get-access-token --resource https://ai.azure.com --query accessToken -o tsv)
```

:::code language="console" source="~/foundry-samples-main/samples/REST/quickstart/quickstart-responses.sh":::

# [OpenAI v1](#tab/openai)

Replace YOUR-FOUNDRY-RESOURCE-NAME and YOUR-DEPLOYMENT-NAME with your values. This example calls the chat completions API:

```console
export AZURE_AI_AUTH_TOKEN=$(az account get-access-token --resource https://cognitiveservices.azure.com --query accessToken -o tsv)

curl -sS -X POST \
  "https://YOUR-FOUNDRY-RESOURCE-NAME.openai.azure.com/openai/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AZURE_AI_AUTH_TOKEN" \
  -d '{
    "model": "YOUR-DEPLOYMENT-NAME",
    "messages": [
      {"role":"system","content":"You are a helpful assistant."},
      {"role":"user","content":"What is the size of France in square miles?"}
    ]
  }'
```

---

A successful response returns a JSON payload:

# [Foundry](#tab/foundry)

```json
{
  "id": "<response-id>",
  "object": "response",
  "model": "gpt-4.1-mini",
  "status": "completed",
  "output": [
    {
      "type": "message",
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "The size of France is approximately 248,573 square miles."
        }
      ],
      "status": "completed"
    }
  ],
  "usage": {
    "input_tokens": 17,
    "output_tokens": 14,
    "total_tokens": 31
  }
}
```

# [OpenAI v1](#tab/openai)

```json
{
  "id": "<chat-completion-id>",
  "object": "chat.completion",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "The size of France is approximately 248,573 square miles."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 27,
    "completion_tokens": 14,
    "total_tokens": 41
  }
}
```

---

For the full SDK reference, see the [SDK overview](../how-to/develop/sdk-overview.md).

## Troubleshoot common integration issues

| Error | Cause | Resolution |
|-------|-------|------------|
| `401 Unauthorized` | Invalid or expired token/key | Regenerate your API key or refresh your Entra token. See [authentication options](../concepts/rbac-foundry.md). |
| `404 Not Found` | Wrong endpoint path or resource name | Verify your resource name and endpoint format match the patterns in [Choose an integration pattern](#choose-an-integration-pattern). |
| `429 Too Many Requests` | Rate limit exceeded | Implement retry with exponential backoff, or [increase quota](../how-to/quota.md). |
| DNS resolution failure | Wrong domain | Use `services.ai.azure.com` for Foundry or `openai.azure.com` for OpenAI compatibility. |

