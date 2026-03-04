---
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: include
ms.date: 02/23/2026
---

## Configure access

Before you begin, make sure you have permissions to access content and operations. This quickstart uses Microsoft Entra ID for authentication and role-based access for authorization. You must be an **Owner** or **User Access Administrator** to assign roles. If roles aren't feasible, use [key-based authentication](../../search-security-api-keys.md) instead.

To configure access for this quickstart:

1. Sign in to the [Azure portal](https://portal.azure.com).

1. On your Azure AI Search service:

    1. [Enable role-based access](../../search-security-enable-roles.md).

    1. [Create a system-assigned managed identity](../../search-how-to-managed-identities.md#create-a-system-managed-identity).

    1. [Assign the following roles](../../search-security-rbac.md) to your user account: **Search Service Contributor**, **Search Index Data Contributor**, and **Search Index Data Reader**.

1. On your Microsoft Foundry resource, assign **Cognitive Services User** to the managed identity of your search service.

> [!IMPORTANT]
> Agentic retrieval has two token-based billing models:
>
> + Billing from Azure AI Search for agentic retrieval.
> + Billing from Azure OpenAI for query planning and answer synthesis.
>
> For more information, see [Availability and pricing of agentic retrieval](../../agentic-retrieval-overview.md#availability-and-pricing).

## Get endpoints

Each Azure AI Search service and Microsoft Foundry resource has an *endpoint*, which is a unique URL that identifies and provides network access to the resource. In a later section, you specify these endpoints to connect to your resources programmatically.

To get the endpoints for this quickstart:

1. Sign in to the [Azure portal](https://portal.azure.com).

1. On your Azure AI Search service:

    1. From the left pane, select **Overview**.
    
    1. Copy the URL, which should look like `https://my-service.search.windows.net`.

1. On your Microsoft Foundry resource:

    1. From the left pane, select **Resource Management** > **Keys and Endpoint**.

    1. Copy the URL on the **OpenAI** tab, which should look like `https://my-resource.openai.azure.com/`.
