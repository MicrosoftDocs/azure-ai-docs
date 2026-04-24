---
title: Enable or Disable Semantic Ranker Billing
description: Learn how to set the billing plan for semantic ranker in Azure AI Search, including how to switch between the free and standard plans.
ms.service: azure-ai-search
ms.update-cycle: 180-days
ms.custom:
  - ignite-2023
ms.topic: how-to
ms.date: 04/24/2026
ai-usage: ai-assisted
---

# Enable or disable semantic ranker billing

Semantic ranker is a premium feature billed by usage. By default, all search services are enrolled in the free plan, which provides a monthly request allowance at no charge. To enable continued access after the free quota is consumed, you can switch to the standard plan.

Starting with Search Service REST API version 2026-04-01, billing consent for semantic ranker and agentic retrieval is separate. Use `semanticSearch` to control billing for semantic ranker and `knowledgeRetrieval` to control billing for agentic retrieval.

## Prerequisites

- An Azure AI Search service in any [region that provides semantic ranker](search-region-support.md).

- **Owner** or **Contributor** permissions on the search service.

- Search Management REST API version [2026-03-01-preview](/rest/api/searchmanagement/services/create-or-update?view=rest-searchmanagement-2026-03-01-preview&preserve-view=true) or later to set the `semanticSearch` property.

## Billing split and portal behavior

[!INCLUDE [billing-split-version-compatibility](includes/billing-split-version-compatibility.md)]

For Search Service REST API version 2026-04-01 and later, `semanticSearch` affects only semantic ranker billing. To control agentic retrieval billing, see [Enable or disable agentic retrieval billing](agentic-retrieval-how-to-enable-disable.md).

For Search Service REST API version 2025-11-01-preview and earlier, `semanticSearch` controls consent for both semantic ranker and paid agentic retrieval usage.

### Portal behavior

The Azure portal uses Search Service REST API version 2025-11-01-preview, which sets the `semanticSearch` property. On this version, `semanticSearch` controls billing consent for both semantic ranker and agentic retrieval, so the **Settings** > **Premium features** toggle affects both features.

## Billing plans

Semantic ranker has two billing plans. For pricing by currency, see the [Azure AI Search pricing page](https://azure.microsoft.com/pricing/details/search).

| Plan | Description |
|------|-------------|
| Free (default) | Provides 1,000 free semantic ranker requests per month. After the free allowance is consumed, semantic ranker requests return a billing error. Available on all pricing tiers. |
| Standard | Pay-as-you-go pricing after the monthly free allowance is consumed. Rather than removing the free allowance, the standard plan enables continued usage beyond the 1,000 requests. Requires Basic tier or higher. |

## Enable semantic ranker billing

Follow these steps to switch semantic ranker to the standard billing plan. The billing plan applies at the service level and affects all indexes.

### [**Azure portal**](#tab/portal)

> [!IMPORTANT]
> Currently, using the portal to switch plans also affects agentic retrieval billing. For more information, see [Portal behavior](#portal-behavior).

1. Go to your search service in the [Azure portal](https://portal.azure.com).

1. On the **Overview** page, make sure the pricing tier is Basic or higher.

1. From the left pane, select **Settings** > **Premium features**.

1. Select **Standard**.

### [**REST**](#tab/rest)

Use [Services - Create Or Update](/rest/api/searchmanagement/services/create-or-update?view=rest-searchmanagement-2026-03-01-preview&preserve-view=true#searchsemanticsearch) (Search Management REST API) to set `semanticSearch` to `standard`:

```http
PATCH https://management.azure.com/subscriptions/{{subscriptionId}}/resourcegroups/{{resource-group}}/providers/Microsoft.Search/searchServices/{{search-service-name}}?api-version=2026-03-01-preview
Content-Type: application/json
Authorization: Bearer {{token}}

{
  "properties": {
    "semanticSearch": "standard"
  }
}
```

Management REST API calls are authenticated through Microsoft Entra ID. For instructions on how to authenticate, see [Manage your Azure AI Search service with REST APIs](search-manage-rest.md).

> [!NOTE]
> Create or Update supports two HTTP methods: PUT and PATCH. Both PUT and PATCH can be used to update existing services, but only PUT can be used to create a new service. If PUT is used to update an existing service, it replaces all properties in the service with their defaults if they aren't specified in the request. When PATCH is used to update an existing service, it only replaces properties that are specified in the request. When using PUT to update an existing service, it's possible to accidentally introduce an unexpected scaling or configuration change. When enabling semantic ranking on an existing service, it's recommended to use PATCH instead of PUT.

---

## Disable semantic ranker billing

Follow these steps to switch semantic ranker back to the free billing plan.

### [**Azure portal**](#tab/portal)

> [!IMPORTANT]
> Currently, using the portal to switch plans also affects agentic retrieval billing. For more information, see [Portal behavior](#portal-behavior).

1. Go to your search service in the [Azure portal](https://portal.azure.com).

1. From the left pane, select **Settings** > **Premium features**.

1. Select **Free**.

   :::image type="content" source="media/semantic-search-overview/semantic-search-billing.png" alt-text="Screenshot of enabling semantic ranking in the Azure portal." border="true":::

### [**REST**](#tab/rest)

Use [Services - Create or Update](/rest/api/searchmanagement/services/create-or-update?view=rest-searchmanagement-2026-03-01-preview&preserve-view=true#searchsemanticsearch) (Search Management REST API) to set `semanticSearch` to `free`:

```http
PATCH https://management.azure.com/subscriptions/{{subscriptionId}}/resourcegroups/{{resource-group}}/providers/Microsoft.Search/searchServices/{{search-service-name}}?api-version=2026-03-01-preview
Content-Type: application/json
Authorization: Bearer {{token}}

{
  "properties": {
    "semanticSearch": "free"
  }
}
```

Management REST API calls are authenticated through Microsoft Entra ID. For instructions on how to authenticate, see [Manage your Azure AI Search service with REST APIs](search-manage-rest.md).

> [!NOTE]
> The `disabled` value is no longer valid in Search Management REST API version 2026-03-01-preview and later. Existing services with `semanticSearch` set to `disabled` are automatically treated as `free`.

---

## Next step

> [!div class="nextstepaction"]
> [Configure semantic ranker](semantic-how-to-configure.md)
