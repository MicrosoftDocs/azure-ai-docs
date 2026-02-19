---
title: 'Integrate Microsoft Foundry with your applications'
description: Learn how to retrieve and use Microsoft Foundry endpoints for third-party integrations, including comparison with Azure OpenAI v1 endpoints.
monikerRange: 'foundry-classic || foundry'
ms.topic: how-to
ms.date: 11/05/2025
titleSuffix: Microsoft Foundry
ms.service: azure-ai-foundry
ms.reviewer: deeikele
ms.author: sgilley
author: sdgilley
ms.custom: devx-track-ai
content_well_notification:
  - AI-contribution
ai-usage: ai-assisted
#customer intent: As a developer, I want to understand how to retrieve Microsoft Foundry endpoints and integrate them with third-party applications, similar to Azure OpenAI.
---

# Integrate Microsoft Foundry with your applications (Microsoft or third-party services)

[!INCLUDE [version-banner](../includes/version-banner.md)]

## Overview

Microsoft Foundry is a developer platform that lets you embed AI models, agents, evaluation tools, and Responsible AI capabilities into your workflows and applications.

You can build complete solutions in Foundry or selectively integrate its features into your custom apps and Microsoft or partner solutions.

Foundry supports multiple integration patterns, including:

* Low-code connectors as part of our Software-as-a-Services applications
* Direct REST API integration for full control
* API gateway mediation for centralized management

## Common integration patterns

### 1. Connector‑based integration

Use this pattern when your platform natively supports built-in integration to Foundry or Azure OpenAI (for example when using Microsoft Power Platform or Logic Apps).

- **Power Platform**: Use the [Azure OpenAI connector](/connectors/azureopenai/) in Power Apps, Power Automate, or Logic Apps.
- **Third-party platforms**: Various third-party software vendors provide prebuilt Azure OpenAI or Foundry modules for chat, image generation, and transcription.

### 2. Direct REST calls
Use direct REST calls when you're building your own application or when you need full control over HTTP calls. You can choose between Foundry endpoint variants to access agentic or cross-model provider APIs, or use Azure OpenAI endpoint if your integration expects OpenAI v1 semantics.

- Foundry endpoint, for stateless API integration such as model inference:
  ```REST
  POST https://{resource}.services.ai.azure.com/api/
  ```

- Foundry project endpoint, for stateful APIs such as agent service:
  ```REST
  POST https://{resource}.services.ai.azure.com/api/projects/{projectname}/
  ```

- Use the OpenAI v1‑compatible route for applications that expect the OpenAI API shape:
  ```REST
  POST https://{resource}.openai.azure.com/openai/v1/
  ```

### 3. API gateway mediation

To establish a single entry point across multiple model hosts, use [Azure API Management (APIM)](/azure/api-management/) as an AI gateway to centralize authentication, quota governance, and routing.

- Place APIM in front of Foundry or Azure OpenAI endpoints.
- Apply policies for authentication, token budgets, semantic caching, and routing.

To learn more, see [API Management for AI](/azure/api-management/azure-ai-foundry-api).

### 4. Data pipeline enrichment

- Use Microsoft Fabric notebooks or pipelines to invoke models for batch or streaming enrichment.
- Write results back to OneLake for downstream analytics and governance.

To learn more, see [Foundry in Fabric](/fabric/data-science/ai-services/ai-services-overview).

## How to use the REST API

Foundry supports direct HTTP calls for scenarios where you need full control. Use the REST API when:

- Your tool doesn't have a native Foundry or Azure OpenAI connector.
- You want to embed calls in scripts, automation pipelines, or custom adapters.
- You need compatibility with OpenAI v1 for third-party SDKs or connectors.

To call the API, you:
1. Choose the correct endpoint shape:
   - **Foundry API** (`services.ai.azure.com`) for a model-provider agnostic schema, and access to Foundry-exclusive features.
   - **OpenAI v1 compatibility** for tools expecting OpenAI request/response schema.
1. Include authentication headers:
   - `Authorization: Bearer {token}` or `api-key: {your-key}`.
1. Send a JSON payload with your model name and messages.

For full schema details, see:
- [Swagger for Foundry inference API](/rest/api/aifoundry/)
- [Swagger for OpenAI v1 compatibility](../openai/latest.md)

Sample:
```bash
curl -sS -X POST \
  "https://{resource}.services.ai.azure.com/models/chat/completions?api-version=2024-10-21" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {token-or-key}" \
  -d '{
    "model": "{foundry-deployment-or-route-name}",
    "messages": [
      {"role":"system","content":"You are a helpful assistant."},
      {"role":"user","content":"Summarize the incident in 3 bullets."}
    ]
  }'
```

## Related content

- [Authentication and authorization options in Foundry](../concepts/rbac-foundry.md)
- [Import a Foundry API in API Management](/azure/api-management/azure-ai-foundry-api)
- [AI gateway capabilities in Azure API Management](/azure/api-management/genai-gateway-capabilities)
- [Consume Fabric data agent from Foundry Services](/fabric/data-science/data-agent-foundry)
