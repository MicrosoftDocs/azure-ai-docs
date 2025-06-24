---
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: include
ms.date: 6/15/2025
---

## Configure role-based access

You can use search service API keys or Microsoft Entra ID with role assignments. Keys are easier to start with, but roles are more secure. This quickstart assumes roles.

To configure the recommended role-based access:

1. Sign in to the [Azure portal](https://portal.azure.com/).

1. [Enable role-based access](../../search-security-enable-roles.md) on your Azure AI Search service.

1. On your Azure AI Search service, [assign the following roles](../../search-security-rbac.md#how-to-assign-roles-in-the-azure-portal) to yourself.

    + **Search Service Contributor**

    + **Search Index Data Contributor**

    + **Search Index Data Reader**

For agentic retrieval, Azure AI Search also needs access to your Azure OpenAI Foundry resource. 

1. [Create a system-assigned managed identity](../../search-howto-managed-identities-data-sources.md#create-a-system-managed-identity) on your Azure AI Search service. Here's how to do it using the Azure CLI:

   ```azurecli
   az search service update --name YOUR-SEARCH-SERVICE-NAME --resource-group YOUR-RESOURCE-GROUP-NAME --identity-type SystemAssigned
   ```
   
    If you already have a managed identity, you can skip this step.

1. On your Azure AI Foundry resource, assign **Cognitive Services User** to the managed identity that you created for your search service. 

## Deploy models

To use agentic retrieval, you must deploy [one of the supported Azure OpenAI models](../../search-agentic-retrieval-how-to-create.md#supported-models) to your Azure AI Foundry resource:

+ A chat model for query planning and answer generation. We use `gpt-4.1-mini` in this quickstart. Optionally, you can use a different model for query planning and another for answer generation, but this quickstart uses the same model for simplicity.

+ An embedding model for vector queries. We use `text-embedding-3-large` in this quickstart, but you can use any embedding model that supports the `text-embedding` task.

To deploy the Azure OpenAI models:

1. Sign in to the [Azure AI Foundry portal](https://ai.azure.com/?cid=learnDocs) and select your Azure AI Foundry resource.

1. From the left pane, select **Model catalog**.

1. Select **gpt-4.1-mini**, and then select **Use this model**.

1. Specify a deployment name. To simplify your code, we recommend **gpt-4.1-mini**.

1. Leave the default settings.

1. Select **Deploy**.

1. Repeat the previous steps, but this time deploy the **text-embedding-3-large** embedding model.

## Get endpoints

In your code, you specify the following endpoints to establish connections with your Azure AI Search service and Azure AI Foundry resource. These steps assume that you [configured role-based access as described previously](#configure-role-based-access). 

To obtain your service endpoints:

1. Sign in to the [Azure portal](https://portal.azure.com/).

1. On your Azure AI Search service:

    1. From the left pane, select **Overview**.

    1. Copy the URL, which should be similar to `https://my-service.search.windows.net`. 

1. On your Azure AI Foundry resource:

    1. From the left pane, select **Resource Management** > **Keys and Endpoint**. 

    1. Select the **OpenAI** tab and copy the URL that looks similar to `https://my-resource.openai.azure.com`.

> [!IMPORTANT]
> Agentic retrieval has two token-based billing models:
>
> + Billing from Azure OpenAI for query planning.
> + Billing from Azure AI Search for query execution (semantic ranking).
>
> Semantic ranking is free in the initial public preview. After the preview, standard token billing applies. For more information, see [Availability and pricing of agentic retrieval](../../search-agentic-retrieval-concept.md#availability-and-pricing).
