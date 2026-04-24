---
title: Enable or Disable Agentic Retrieval Billing
description: Learn how to configure billing consent for agentic retrieval in Azure AI Search using the knowledgeRetrieval service property.
ms.service: azure-ai-search
ms.update-cycle: 180-days
ms.topic: how-to
ms.date: 04/24/2026
ai-usage: ai-assisted
---

# Enable or disable agentic retrieval billing

Agentic retrieval is a premium feature billed by usage. By default, all search services are enrolled in the free plan, which provides a monthly request allowance at no charge. For continued access after the free quota is consumed, you can switch to the standard plan. For pricing by currency, see the [Azure AI Search pricing page](https://azure.microsoft.com/pricing/details/search).

Starting with Search Service REST API version 2026-04-01, billing consent for semantic ranker and agentic retrieval is separate. Use `knowledgeRetrieval` to control paid agentic retrieval usage independently of `semanticSearch`.

## Prerequisites

- An Azure AI Search service in a [region that provides agentic retrieval](search-region-support.md). The free plan is available on all pricing tiers. The standard plan requires a billable tier (Basic or higher).

- **Owner** or **Contributor** permissions on the search service.

- [Search Management REST API](/rest/api/searchmanagement/services/create-or-update?view=rest-searchmanagement-2026-03-01-preview&preserve-view=true) version `2026-03-01-preview` or later to set the `knowledgeRetrieval` property.

## Version compatibility and portal behavior

You set billing consent using the Search Management REST API. The following table shows which property takes effect based on the Search Service REST API version your application uses.

| Search Service REST API version | Agentic retrieval billing | Semantic ranker billing |
|---|---|---|
| [2026-04-01](/rest/api/searchservice/operation-groups?view=rest-searchservice-2026-04-01&preserve-view=true) or later | Controlled by `knowledgeRetrieval` | Controlled by `semanticSearch` |
| [2025-11-01-preview](/rest/api/searchservice/operation-groups?view=rest-searchservice-2025-11-01-preview&preserve-view=true) and earlier | Controlled by `semanticSearch` | Controlled by `semanticSearch` |

For Search Service REST API version 2026-04-01 and later, `knowledgeRetrieval` controls agentic retrieval billing independently of `semanticSearch`. To control semantic ranker billing, see [Enable or disable semantic ranker billing](semantic-how-to-enable-disable.md).

For Search Service REST API version 2025-11-01-preview and earlier, `semanticSearch` controls consent for both semantic ranker and paid agentic retrieval usage. The `knowledgeRetrieval` property is ignored.

### Portal behavior

The Azure portal uses Search Service REST API version 2025-11-01-preview, which doesn't support separate billing controls for agentic retrieval and semantic ranker. To change agentic retrieval billing consent through the portal, use the **Settings** > **Premium features** toggle. This toggle also affects semantic ranker billing.

## Enable agentic retrieval billing

Follow these steps to allow paid agentic retrieval usage beyond the free monthly quota. The free plan includes 50 million agentic reasoning tokens per month. After the free quota is consumed, requests that would incur paid usage return a payment-required error until you switch to the standard plan.

### [**Azure portal**](#tab/portal)

Currently, the portal doesn't expose a dedicated billing control for agentic retrieval. You must use REST to manage billing consent. For more information, see [Portal behavior](#portal-behavior).

### [**REST**](#tab/rest)

To allow paid agentic retrieval usage after the free monthly quota is consumed, use [Services - Create Or Update](/rest/api/searchmanagement/services/create-or-update?view=rest-searchmanagement-2026-03-01-preview&preserve-view=true#knowledgeretrieval) (Search Management REST API) to set `knowledgeRetrieval` to `standard`:

```http
PATCH https://management.azure.com/subscriptions/{{subscriptionId}}/resourcegroups/{{resource-group}}/providers/Microsoft.Search/searchServices/{{search-service-name}}?api-version=2026-03-01-preview
Content-Type: application/json
Authorization: Bearer {{token}}

{
  "properties": {
    "knowledgeRetrieval": "standard"
  }
}
```

Management REST API calls are authenticated through Microsoft Entra ID. For instructions, see [Manage your Azure AI Search service with REST APIs](search-manage-rest.md).

> [!IMPORTANT]
> If you previously relied on `semanticSearch` to enable paid agentic retrieval usage, you must explicitly set `knowledgeRetrieval` to `standard` before you migrate agentic retrieval workloads to Search Service REST API version 2026-04-01 or later. Existing `semanticSearch=standard` consent doesn't carry over to `knowledgeRetrieval`.

## Disable paid agentic retrieval billing

Follow these steps to disable paid agentic retrieval usage. With paid usage disabled, agentic retrieval continues to work within the monthly free quota. After the free quota is consumed, requests that would incur paid usage return a payment-required error until you switch back to the standard plan.

### [**Azure portal**](#tab/portal)

Currently, the portal doesn't expose a dedicated billing control for agentic retrieval. You must use REST to manage billing consent. For more information, see [Portal behavior](#portal-behavior).

### [**REST**](#tab/rest)

To stop paid agentic retrieval usage, use [Services - Create or Update](/rest/api/searchmanagement/services/create-or-update?view=rest-searchmanagement-2026-03-01-preview&preserve-view=true#knowledgeretrieval) (Search Management REST API) to set `knowledgeRetrieval` to `free`:

```http
PATCH https://management.azure.com/subscriptions/{{subscriptionId}}/resourcegroups/{{resource-group}}/providers/Microsoft.Search/searchServices/{{search-service-name}}?api-version=2026-03-01-preview
Content-Type: application/json
Authorization: Bearer {{token}}

{
  "properties": {
    "knowledgeRetrieval": "free"
  }
}
```

Management REST API calls are authenticated through Microsoft Entra ID. For instructions on how to authenticate, see [Manage your Azure AI Search service with REST APIs](search-manage-rest.md).

## Related content

- [Agentic retrieval in Azure AI Search](agentic-retrieval-overview.md)
- [Enable or disable semantic ranker billing](semantic-how-to-enable-disable.md)
