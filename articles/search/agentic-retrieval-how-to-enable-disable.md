---
title: Enable or Disable Agentic Retrieval Billing
description: Learn how to configure billing consent for agentic retrieval in Azure AI Search using the knowledgeRetrieval service property.
ms.service: azure-ai-search
ms.update-cycle: 180-days
ms.topic: how-to
ms.date: 06/16/2026
ai-usage: ai-assisted
---

# Enable or disable agentic retrieval billing

Agentic retrieval is a premium feature billed by usage. By default, all search services are enrolled in the free plan, which provides a monthly allowance at no charge. To enable continued access after the free quota is consumed, you can switch to the standard plan.

Starting with Search Service REST API version 2026-04-01, billing consent for semantic ranker and agentic retrieval is separate. Use `knowledgeRetrieval` to control paid agentic retrieval usage independently of `semanticSearch`.

## Prerequisites

- An Azure AI Search service in any [region that provides agentic retrieval](search-region-support.md).

- **Owner** or **Contributor** permissions on the search service.

- Search Management REST API version [2026-03-01-preview](/rest/api/searchmanagement/services/create-or-update?view=rest-searchmanagement-2026-03-01-preview&preserve-view=true) or later to set the `knowledgeRetrieval` property.

## Billing split

[!INCLUDE [billing-split-version-compatibility](includes/billing-split-version-compatibility.md)]

For Search Service REST API version 2026-04-01 and later, `knowledgeRetrieval` controls agentic retrieval billing independently of `semanticSearch`. To control semantic ranker billing, see [Enable or disable semantic ranker billing](semantic-how-to-enable-disable.md).

For Search Service REST API version 2025-11-01-preview and earlier, `semanticSearch` controls consent for both semantic ranker and paid agentic retrieval usage. The `knowledgeRetrieval` property is ignored.

## Billing plans

Agentic retrieval has two billing plans. For pricing by currency, see [Azure AI Search pricing](https://azure.microsoft.com/pricing/details/search).

| Plan | Description | Availability |
| --- | --- | --- |
| Free (default) | Provides a monthly token allowance at no charge. After the free allowance is consumed, requests that would incur paid usage return a payment-required error. | Available on all pricing tiers. |
| Standard | Pay-as-you-go pricing after the monthly free allowance is consumed. | Requires the Basic tier or higher. |

## Enable agentic retrieval billing

Follow these steps to switch agentic retrieval to the standard billing plan.

### [Azure portal](#tab/portal)

1. Go to your search service in the [Azure portal](https://portal.azure.com).

1. On the **Overview** page, make sure the pricing tier is Basic or higher.

1. From the left pane, select **Settings** > **Premium features**.

1. Under **Knowledge retrieval**, select **Select plan** in the **Standard** card.

    :::image type="content" source="media/agentic-retrieval-how-to-enable-disable/agentic-enable.png" alt-text="Screenshot of the Premium features page in the Azure portal, showing the Knowledge retrieval Standard plan selected." lightbox="media/agentic-retrieval-how-to-enable-disable/agentic-enable.png" border="true":::

### [REST](#tab/rest)

Use [Services - Create Or Update](/rest/api/searchmanagement/services/create-or-update?view=rest-searchmanagement-2026-03-01-preview&preserve-view=true#knowledgeretrieval) (Search Management REST API) to set `knowledgeRetrieval` to `standard`:

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

---

## Disable agentic retrieval billing

Follow these steps to switch agentic retrieval back to the free billing plan.

### [Azure portal](#tab/portal)

1. Go to your search service in the [Azure portal](https://portal.azure.com).

1. From the left pane, select **Settings** > **Premium features**.

1. Under **Knowledge retrieval**, select **Select plan** in the **Free** card.

    :::image type="content" source="media/agentic-retrieval-how-to-enable-disable/agentic-disable.png" alt-text="Screenshot of the Premium features page in the Azure portal, showing the Knowledge retrieval Free plan selected." lightbox="media/agentic-retrieval-how-to-enable-disable/agentic-disable.png" border="true":::

### [REST](#tab/rest)

Use [Services - Create or Update](/rest/api/searchmanagement/services/create-or-update?view=rest-searchmanagement-2026-03-01-preview&preserve-view=true#knowledgeretrieval) (Search Management REST API) to set `knowledgeRetrieval` to `free`:

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

---

## Related content

- [Agentic retrieval in Azure AI Search](agentic-retrieval-overview.md)
- [Enable or disable semantic ranker billing](semantic-how-to-enable-disable.md)
