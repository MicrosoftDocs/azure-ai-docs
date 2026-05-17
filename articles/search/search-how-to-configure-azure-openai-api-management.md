---
title: Use Azure API Management with Azure OpenAI skills and vectorizers
titleSuffix: Azure AI Search
description: Configure Azure API Management as a gateway to Azure OpenAI or Microsoft Foundry model deployments for the Azure OpenAI embedding skill, Azure OpenAI vectorizer, and GenAI prompt skill in Azure AI Search.
ms.reviewer: gimondra
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 05/17/2026
ai-usage: ai-assisted
---

# Use Azure API Management with Azure OpenAI skills and vectorizers in Azure AI Search

You can place [Azure API Management](/azure/api-management/api-management-key-concepts) in front of [Azure OpenAI in Microsoft Foundry Models](/azure/ai-services/openai/overview) and [Microsoft Foundry](/azure/ai-foundry/what-is-foundry) deployments to centralize routing, load balancing, throttling, and observability for Azure AI Search workloads that use Foundry models. This article describes the supported scenarios, the recommended authentication and role-based access control (RBAC) pattern, and how to optionally make the connection from Azure AI Search private.

## Supported scenarios

You can call a Microsoft Foundry model deployment through API Management from these Azure AI Search features:

+ [Azure OpenAI embedding skill](cognitive-search-skill-azure-openai-embedding.md)
+ [Azure OpenAI vectorizer](vector-search-vectorizer-azure-open-ai.md)
+ [GenAI prompt skill](cognitive-search-skill-genai-prompt.md)

For each, set the skill or vectorizer endpoint to the API Management gateway URL, either `https://<resource-name>.azure-api.net` or an [API Management custom domain](/azure/api-management/configure-custom-domain).

## Unsupported scenarios

API Management isn't supported as a gateway for:

+ The large language model (LLM) used by the [Azure Content Understanding skill](cognitive-search-skill-content-understanding.md).
+ The LLM used by a [knowledge base in agentic retrieval](agentic-retrieval-overview.md).


## Architecture

There are two common flows. Both use the same API Management configuration on the backend side.

### Public path

Azure AI Search calls the API Management gateway over its public endpoint. API Management authenticates to the Microsoft Foundry resource and forwards the request.

```
Azure AI Search (skill or vectorizer)
   └─▶ API Management gateway (azure-api.net or custom domain)
          [API Management policies authenticate the caller]
          [API Management's managed identity authenticates to Foundry]
          └─▶ Azure OpenAI in Foundry Models / Microsoft Foundry resource
```

### Private path from Azure AI Search to API Management

When the search service must reach API Management privately, create a [shared private link](search-indexer-howto-access-private.md) from the search service to the API Management instance, and run indexers in the [private execution environment](search-indexer-howto-access-private.md#step-4-configure-the-indexer-to-run-in-the-private-environment).

```
Azure AI Search (private indexer execution)
   └─▶ Shared private link (Microsoft.ApiManagement/service, group "Gateway")
          └─▶ API Management private endpoint
                 └─▶ Microsoft Foundry resource (public or private endpoint)
```

API Management to Foundry is the standard backend pattern. For deeper topology guidance, including multi-region, multi-instance, and active-active or active-passive variants, see [Use a gateway in front of multiple Azure OpenAI deployments or instances](/azure/architecture/ai-ml/guide/azure-openai-gateway-multi-backend) and [Overview of generative AI gateway capabilities in Azure API Management](/azure/api-management/genai-gateway-capabilities).

## Configure the endpoint in your skill or vectorizer

Set the skill or vectorizer endpoint to the API Management gateway URL:

| Feature | Property | Value |
|---|---|---|
| [Azure OpenAI embedding skill](cognitive-search-skill-azure-openai-embedding.md) | `resourceUri` | `https://<apim-name>.azure-api.net` or API Management custom domain |
| [Azure OpenAI vectorizer](vector-search-vectorizer-azure-open-ai.md) | `resourceUri` | `https://<apim-name>.azure-api.net` or API Management custom domain |
| [GenAI prompt skill](cognitive-search-skill-genai-prompt.md) | `uri` | `https://<apim-name>.azure-api.net` or API Management custom domain |


## Authentication and RBAC

Two identities are involved. They have different responsibilities and different role assignments.

| Identity | Where credentials are presented | Role or mechanism |
|---|---|---|
| Azure AI Search managed identity | At the API Management gateway | Authorized by API Management policies. No role on the Microsoft Foundry resource is required when you use the credential-termination pattern below. |
| API Management managed identity | At the Microsoft Foundry resource | **Cognitive Services OpenAI User** on the Microsoft Foundry resource. |

The recommended pattern is **credential termination and re-establishment**: the caller authenticates to API Management, and API Management uses its own managed identity to authenticate to the Microsoft Foundry resource. This pattern is described in [Azure OpenAI authorization](/azure/architecture/ai-ml/guide/azure-openai-gateway-multi-backend#azure-openai-authorization) in the AOAI gateway architecture guide.

### Authentication options at the API Management gateway

Choose one of the following options for how Azure AI Search authenticates to API Management. For details and policy examples, see [Authenticate and authorize access to LLM APIs by using API Management](/azure/api-management/api-management-authenticate-authorize-ai-apis).

+ **Subscription key**. API Management stores the Microsoft Foundry resource API key in a [named value](/azure/api-management/api-management-howto-properties), and a policy passes it on the backend request. Characteristics: simplest to configure; uses the `set-header` policy with the `api-key` header; the search service sends only the API Management subscription key, so no Microsoft Entra ID role is required on the search service managed identity.
+ **Managed identity at the gateway with OAuth validation**. API Management uses the [`validate-azure-ad-token`](/azure/api-management/validate-azure-ad-token-policy) policy to validate a Microsoft Entra ID token presented by the search service managed identity. Use this option for defense in depth.
+ **API Management managed identity to the backend (required for the recommended pattern)**. [Enable a system-assigned or user-assigned managed identity](/azure/api-management/api-management-howto-use-managed-service-identity) on the API Management instance, and assign it the **Cognitive Services OpenAI User** role on the Microsoft Foundry resource. See [Authenticate with managed identity](/azure/api-management/api-management-authenticate-authorize-ai-apis#authenticate-with-managed-identity) and [Role-based access control for Azure OpenAI](/azure/ai-foundry/openai/how-to/role-based-access-control).

> [!TIP]
> When you [import a Microsoft Foundry API](/azure/api-management/azure-ai-foundry-api) into API Management, the backend and managed identity wiring is created automatically.

For circuit-breaker, retry, and backend pool guidance, see [Backends in API Management](/azure/api-management/backends).

## Private connectivity from Azure AI Search to API Management

Skip this section if Azure AI Search calls API Management over its public endpoint.

To restrict outbound traffic from the search service to a private channel:

1. Create a shared private link from the search service to the API Management instance. Use the `Microsoft.ApiManagement/service` resource type and the `Gateway` group ID. For steps, see [Make outbound connections through a shared private link](search-indexer-howto-access-private.md).
1. Approve the private endpoint connection on the API Management instance.
1. Configure indexers that use the skill or vectorizer to run in the [private execution environment](search-indexer-howto-access-private.md#step-4-configure-the-indexer-to-run-in-the-private-environment).

The shared private link counts against the [shared private link limit](search-limits-quotas-capacity.md#shared-private-link-resource-limits) for your search service tier.

## Private connectivity from API Management to the Microsoft Foundry resource

The private channel from API Management to the Microsoft Foundry resource is independent of the search-to-API Management connection and is configured on the API Management side. For options, see:

+ [Use a virtual network with Azure API Management](/azure/api-management/virtual-network-concepts)
+ [Configure Azure OpenAI networking](/azure/ai-foundry/openai/how-to/network)

## Related content

+ [Azure OpenAI embedding skill](cognitive-search-skill-azure-openai-embedding.md)
+ [Azure OpenAI vectorizer](vector-search-vectorizer-azure-open-ai.md)
+ [GenAI prompt skill](cognitive-search-skill-genai-prompt.md)
+ [Make outbound connections through a shared private link](search-indexer-howto-access-private.md)
+ [Use a gateway in front of multiple Azure OpenAI deployments or instances](/azure/architecture/ai-ml/guide/azure-openai-gateway-multi-backend)
+ [Overview of generative AI gateway capabilities in Azure API Management](/azure/api-management/genai-gateway-capabilities)
+ [Authenticate and authorize access to LLM APIs by using API Management](/azure/api-management/api-management-authenticate-authorize-ai-apis)
