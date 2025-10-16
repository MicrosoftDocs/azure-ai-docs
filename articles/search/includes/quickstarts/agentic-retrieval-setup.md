---
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: include
ms.date: 10/16/2025
---

## Configure access

Before you begin, make sure you have permissions to access content and operations. We recommend Microsoft Entra ID for authentication and role-based access for authorization. You must be an **Owner** or **User Access Administrator** to assign roles. If roles aren't feasible, use [key-based authentication](../../search-security-api-keys.md) instead.

To configure access for this quickstart, select both of the following tabs.

### [Azure AI Search](#tab/search-perms)

Azure AI Search provides the agentic retrieval pipeline. Configure access for yourself and your search service to read and write data, interact with Azure AI Foundry, and run the pipeline.

To configure access for Azure AI Search:

1. Sign in to the [Azure portal](https://portal.azure.com/) and select your search service.

1. [Enable role-based access](../../search-security-enable-roles.md).

1. [Create a system-assigned managed identity](../../search-how-to-managed-identities.md#create-a-system-managed-identity).

1. [Assign the following roles](../../search-security-rbac.md#how-to-assign-roles-in-the-azure-portal) to yourself.

    + **Search Service Contributor**

    + **Search Index Data Contributor**

    + **Search Index Data Reader**

### [Azure AI Foundry](#tab/foundry-perms)

Azure AI Foundry provides the Azure OpenAI models used for embeddings, query planning, and answer generation. Grant your search service permission to use these models.

To configure access for Azure AI Foundry:

1. Sign in to the [Azure portal](https://portal.azure.com/) and select your Azure AI Foundry resource.

1. Assign **Cognitive Services User** to the managed identity of your search service.

---

> [!IMPORTANT]
> Agentic retrieval has two token-based billing models:
>
> + Billing from Azure AI Search for semantic ranking.
> + Billing from Azure OpenAI for query planning and answer synthesis.
>
> Semantic ranking is free in the initial public preview. After the preview, standard token billing applies. For more information, see [Availability and pricing of agentic retrieval](../../agentic-retrieval-overview.md#availability-and-pricing).

## Get endpoints

Each Azure AI Search service and Azure AI Foundry resource has an *endpoint*, which is a unique URL that identifies and provides network access to the resource. In a later section, you specify these endpoints to connect to your resources programmatically.

To get the endpoints for this quickstart, select both of the following tabs.

### [Azure AI Search](#tab/search-endpoint)

1. Sign in to the [Azure portal](https://portal.azure.com/) and select your search service.

1. From the left pane, select **Overview**.

1. Make a note of the endpoint, which should look like `https://my-service.search.windows.net`.

### [Azure AI Foundry](#tab/foundry-endpoint)

1. Sign in to the [Azure portal](https://portal.azure.com/) and select your Azure AI Foundry resource.

1. From the left pane, select **Resource Management** > **Keys and Endpoint**.

1. Select the **OpenAI** tab.

1. Make a note of the endpoint, which should look like `https://my-resource.openai.azure.com`.

---

## Deploy models

To use agentic retrieval, you must deploy two Azure OpenAI models to your Azure AI Foundry resource:

+ An embedding model for text-to-vector conversion. This quickstart uses `text-embedding-3-large`, but you can use any `text-embedding` model.

+ An LLM for query planning and answer generation. This quickstart uses `gpt-5-mini`, but you can use any [supported LLM for agentic retrieval](../../agentic-retrieval-how-to-create-knowledge-base.md#supported-models).

For deployment instructions, see [Deploy Azure OpenAI models with Azure AI Foundry](/azure/ai-foundry/how-to/deploy-models-openai).
