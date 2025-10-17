---
title: Enable or Disable Access to Web Knowledge Sources
titleSuffix: Azure AI Search
description: Learn how to enable or disable the use of web knowledge sources in your Azure subscription. By default, access is enabled, but you can disable or re-enable access using the Azure CLI.
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.custom:
  - ignite-2025
ms.topic: how-to
ms.date: 10/17/2025
---

# Manage access to web knowledge sources in your Azure subscription

> [!IMPORTANT]
> + Web Knowledge Source, which uses Grounding with Bing Search and/or Grounding with Bing Custom Search, is a [First Party Consumption Service](https://www.microsoft.com/licensing/terms/product/ForOnlineServices/EAEAS) governed by the [Grounding with Bing terms of use](https://www.microsoft.com/en-us/bing/apis/grounding-legal-enterprise) and the [Microsoft Privacy Statement](https://www.microsoft.com/en-us/privacy/privacystatement).
>
> + The [Microsoft Data Protection Addendum](https://www.microsoft.com/licensing/docs/view/Microsoft-Products-and-Services-Data-Protection-Addendum-DPA) doesn't apply to data sent to Web Knowledge Source. When Customer uses Web Knowledge Source, Customer Data flows outside the Azure compliance and Geo boundary.
>
> + Use of Web Knowledge Source incurs costs; learn more about [pricing](https://www.microsoft.com/en-us/bing/apis/grounding-pricing).
>
> + Learn more about how Azure admins can [manage access to use of Web Knowledge Source](XYZ).

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

As an Azure admin, you can use the Azure CLI to enable or disable the use of [web knowledge sources](agentic-knowledge-source-how-to-web.md) at the subscription level. This setting applies to all accounts within the specified subscription.

## Prerequisites

+ Have **Owner** or **Contributor** access to the subscription.

+ Have the [Azure CLI](cli/azure/install-azure-cli) installed. If you're not already signed in to Azure, run `az login`.

## Enable use of web knowledge sources

Access to knowledge sources is enabled by default. If access has been disabled, you can run the following command to enable it.

```azurecli
az feature register --name WebKnowledgeSourceDisabled --namespace Microsoft.Search --subscription "<subscription-id>" 
```

## Disable use of web knowledge sources

Run the following command to disable access to web knowledge sources.

```azurecli
az feature unregister --name WebKnowledgeSourceDisabled --namespace Microsoft.Search --subscription "<subscription-id>" 
```

## Related content

+ [Create a web knowledge source](agentic-knowledge-source-how-to-web.md)
+ [Agentic retrieval in Azure AI Search](search-agentic-retrieval-concept.md)
