---
title: Enable or Disable Access to Web Knowledge Source
titleSuffix: Azure AI Search
description: Learn how to enable or disable the use of Web Knowledge Source in your Azure subscription. By default, access is enabled, but you can disable or re-enable access using the Azure CLI.
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.custom:
  - ignite-2025
ms.topic: how-to
ms.date: 11/19/2025
---

# Manage access to Web Knowledge Source in your Azure subscription

> [!IMPORTANT]
> + Web Knowledge Source, which uses Grounding with Bing Search and/or Grounding with Bing Custom Search, is a [First Party Consumption Service](https://www.microsoft.com/licensing/terms/product/ForOnlineServices/EAEAS) governed by the [Grounding with Bing terms of use](https://www.microsoft.com/en-us/bing/apis/grounding-legal-enterprise) and the [Microsoft Privacy Statement](https://www.microsoft.com/en-us/privacy/privacystatement).
>
> + The [Microsoft Data Protection Addendum](https://www.microsoft.com/licensing/docs/view/Microsoft-Products-and-Services-Data-Protection-Addendum-DPA) doesn't apply to data sent to Web Knowledge Source. When Customer uses Web Knowledge Source, Customer Data flows outside the Azure compliance and Geo boundary. This also means use of Web Knowledge Source waives all elevated Government Community Cloud security and compliance commitments to include data sovereignty and screened/citizenship-based support, as applicable.
>
> + Use of Web Knowledge Source incurs costs; learn more about [pricing](https://www.microsoft.com/en-us/bing/apis/grounding-pricing).

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

As an Azure admin, you can use the Azure CLI to enable or disable the use of [Web Knowledge Source](agentic-knowledge-source-how-to-web.md) at the subscription level. This setting applies to all search services within the specified subscription.

## Prerequisites

+ Have **Owner** or **Contributor** access to the subscription.

+ Have the [Azure CLI](/cli/azure/install-azure-cli) installed. If you're not already signed in to Azure, run `az login`.

## Check the current access state

To check the current status of Web Knowledge Source access, run the following command.

### [PowerShell](#tab/powershell)

```azurecli
az feature show --name WebKnowledgeSourceDisabled --namespace Microsoft.Search --subscription "<subscription-id>"
```

### [REST API](#tab/rest-api)

```http
GET https://management.azure.com/subscriptions/{{subscriptionId}}/providers/Microsoft.Features/providers/Microsoft.Search/features/WebKnowledgeSourceDisabled?api-version=2021-07-01
Authorization: Bearer {{accessToken}} // Obtain using `az account get-access-token --scope https://management.azure.com/.default --query accessToken --output tsv`
```

---

The output shows the `state` property, which indicates the current registration status:

+ `Registered` means access is **disabled**.
+ `Unregistered` means access is **enabled**, which is the default state.

## Enable use of Web Knowledge Source

Access to Web Knowledge Source is enabled by default. If access has been disabled, you can run the following command to enable it.

### [PowerShell](#tab/powershell)

```powershell
az feature unregister --name WebKnowledgeSourceDisabled --namespace Microsoft.Search --subscription "<subscription-id>"
```

### [REST API](#tab/rest-api)

```http
POST https://management.azure.com/subscriptions/{{subscriptionId}}/providers/Microsoft.Features/providers/Microsoft.Search/features/WebKnowledgeSourceDisabled/unregister?api-version=2021-07-01
Authorization: Bearer {{accessToken}} // Obtain using `az account get-access-token --scope https://management.azure.com/.default --query accessToken --output tsv`
```

---

## Disable use of Web Knowledge Source

Run the following command to disable access to Web Knowledge Source.

### [PowerShell](#tab/powershell)

```powershell
az feature register --name WebKnowledgeSourceDisabled --namespace Microsoft.Search --subscription "<subscription-id>"
```

### [REST API](#tab/rest-api)

```http
POST https://management.azure.com/subscriptions/{{subscriptionId}}/providers/Microsoft.Features/providers/Microsoft.Search/features/WebKnowledgeSourceDisabled/register?api-version=2021-07-01
Authorization: Bearer {{accessToken}} // Obtain using `az account get-access-token --scope https://management.azure.com/.default --query accessToken --output tsv`
```

---

## Related content

+ [Create a Web Knowledge Source resource](agentic-knowledge-source-how-to-web.md)
+ [Agentic retrieval in Azure AI Search](search-agentic-retrieval-concept.md)
