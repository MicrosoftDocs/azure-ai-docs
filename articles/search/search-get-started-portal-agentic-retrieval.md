---
title: "Quickstart: Use Agentic Retrieval in the Azure portal"
titleSuffix: Azure AI Search
description: Learn how to use agentic retrieval in the Azure portal for a conversational search experience powered by Azure AI Search and Azure OpenAI models.
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.custom:
  - ignite-2025
ms.topic: quickstart
ms.date: 10/16/2025
---

# Quickstart: Use agentic retrieval in the Azure portal

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

In this quickstart, you use [agentic retrieval](agentic-retrieval-overview.md) in the Azure portal to create a conversational search experience powered by documents indexed in Azure AI Search and large language models (LLMs) from Azure OpenAI in Azure AI Foundry Models.

The portal guides you through the process of configuring and creating the following objects:

+ A *knowledge source* that supplies content for indexing and retrieval. Although agentic retrieval [supports multiple knowledge sources](agentic-knowledge-source-overview.md#supported-knowledge-sources), this quickstart uses Azure Blob Storage to create a blob knowledge source.

+ A *knowledge base* that uses an LLM to infer the underlying information need, plan queries, and surface relevant documents from your knowledge source. To optionally generate natural-language answers, this quickstart uses the answer synthesis modality.

Afterwards, you test the knowledge base by submitting a complex query that requires information from multiple documents and reviewing the synthesized answer.

> [!IMPORTANT]
> Because the portal uses the 2025-08-01-preview REST API version for agentic retrieval, the knowledge source and knowledge base created in this quickstart aren't compatible with the latest 2025-11-01-preview. For help with breaking changes, see [Migrate your agentic retrieval code](agentic-retrieval-how-to-migrate.md).

## Prerequisites

+ An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

+ An [Azure AI Search service](search-create-service-portal.md) on the Basic tier or higher with [semantic ranker enabled](semantic-how-to-enable-disable.md).

+ An [Azure Blob Storage account](/azure/storage/common/storage-account-create).

+ An [Azure AI Foundry project](/ai-foundry/how-to/create-projects) and Azure AI Foundry resource. When you create a project, the resource is automatically created.

## Configure access

Before you begin, make sure you have permissions to access content and operations. We recommend Microsoft Entra ID for authentication and role-based access for authorization. You must be an **Owner** or **User Access Administrator** to assign roles. If roles aren't feasible, use [key-based authentication](search-security-api-keys.md) instead.

To configure access for this quickstart, select each of the following tabs.

### [Azure AI Search](#tab/search-perms)

Azure AI Search provides the agentic retrieval pipeline. Configure access for yourself and your search service to read and write data, interact with other Azure services, and run the pipeline.

On your Azure AI Search service:

1. [Enable role-based access](search-security-enable-roles.md).

1. [Configure a system-assigned managed identity](search-how-to-managed-identities.md#create-a-system-managed-identity).

1. [Assign the following roles](search-security-rbac.md) to yourself.

   + **Search Service Contributor**

   + **Search Index Data Contributor**

   + **Search Index Data Reader**

### [Azure Blob Storage](#tab/storage-perms)

Azure Blob Storage stores your source documents for indexing and retrieval. Grant your search service permission to read, write, and delete the documents.

On your Azure Blob Storage account:

+ Assign **Storage Blob Data Contributor** to your [search service identity](search-how-to-managed-identities.md#create-a-system-managed-identity).

### [Azure AI Foundry](#tab/foundry-perms)

Azure AI Foundry provides the Azure OpenAI models used for embeddings, query planning, and answer generation. Grant your search service permission to use these models.

On your Azure AI Foundry resource:

+ Assign **Cognitive Services User** to your [search service identity](search-how-to-managed-identities.md#create-a-system-managed-identity).

---

> [!IMPORTANT]
> Agentic retrieval has two token-based billing models:
>
> + Billing from Azure AI Search for semantic ranking.
> + Billing from Azure OpenAI for query planning and answer synthesis.
>
> Semantic ranking is free in the initial public preview. After the preview, standard token billing applies. For more information, see [Availability and pricing of agentic retrieval](agentic-retrieval-overview.md#availability-and-pricing).

## Deploy models

To use agentic retrieval, you must deploy two Azure OpenAI models to your Azure AI Foundry resource:

+ An embedding model for text-to-vector conversion. This quickstart uses `text-embedding-3-large`, but you can use any `text-embedding` model.

+ An LLM for query planning and answer generation. This quickstart uses `gpt-5-mini`, but you can use any [supported LLM for agentic retrieval](agentic-retrieval-how-to-create-knowledge-base.md#supported-models).

For deployment instructions, see [Deploy Azure OpenAI models with Azure AI Foundry](/azure/ai-foundry/how-to/deploy-models-openai).

## Prepare sample data

This quickstart uses sample JSON documents from NASA's Earth at Night e-book, but you can also use your own files. The documents describe general science topics and images of Earth at night as observed from space.

To prepare the sample data for this quickstart:

1. Sign in to the [Azure portal](https://portal.azure.com/) and select your Azure Blob Storage account.

1. From the left pane, select **Data storage** > **Containers**.

1. Create a container named **earth-at-night-data**.

1. Upload the [sample JSON documents](https://github.com/Azure-Samples/azure-search-sample-data/tree/main/nasa-e-book/earth-at-night-json) to the container.

## Create a knowledge source

A knowledge source is a reusable reference to your source data. In this section, you create a blob knowledge source, which triggers the creation of a *data source*, *skillset*, *index*, and *indexer* to automate data indexing and enrichment. You review these objects in a later section.

You also configure a *vectorizer*, which uses your deployed embedding model to convert text into vectors and match documents based on semantic similarity. The vectorizer, vector fields, and vectors will be added to the auto-generated index.

To create the knowledge source for this quickstart:

1. Sign in to the [Azure portal](https://portal.azure.com/) and select your search service.

1. From the left pane, select **Knowledge retrieval** > **Knowledge sources**.

1. Select **Add knowledge source**.

1. Enter **earth-at-night-ks** for the name.

1. Select **Azure blob knowledge source**, and then select your subscription, storage account, and container with the sample data.

1. Select the **Authenticate using managed identity** checkbox. Leave the identity type as **System-assigned**.

1. Select **Add vectorizer**.

1. Select **Azure AI Foundry Models** for the kind, and then select your subscription, project, and embedding model deployment.

1. Select **System managed identity** for the authentication type.

1. Select **Create**.

## Create a knowledge base

A knowledge base uses your knowledge source and deployed LLM to orchestrate agentic retrieval. When a user submits a complex query, the knowledge base decomposes it into focused subqueries, sends the subqueries simultaneously to your knowledge source, reranks the results for relevance, and combines the best results into a single, unified response.

By default, the knowledge base outputs raw content from your knowledge source, but you can enable the answer synthesis modality for natural-language answer generation.

ADD NOTE ABOUT TERMINOLOGY DIFF

To create the knowledge base for this quickstart:

1. From the left pane, select **Knowledge retrieval** > **Knowledge bases**.

1. Select **Add knowledge base**.

1. Enter **earth-at-night-kb** for the name.

1. Under **Add model deployment**, select **Select a deployment**.

1. Select **Azure AI Foundry Models** for the kind, and then select your subscription, project, and model deployment.

1. Select **System managed identity** for the authentication type.

1. Save the model deployment.

1. Under **Add knowledge**, select **earth-at-night-ks**.

1. Under **Advanced configurations**, select **Answer synthesis** for the output mode.

1. Create the knowledge base.

## Test agentic retrieval

The portal provides a chat playground where you can submit queries to the knowledge base and review its responses, which include references to source documents and debug information about the retrieval process.

To query the knowledge base:

1. Use the chat box to send the following query.

    ```plaintext
    Why do suburban belts display larger December brightening than urban cores even though absolute light levels are higher downtown? Why is the Phoenix nighttime street grid is so sharply visible from space, whereas large stretches of the interstate between midwestern cities remain comparatively dim?
    ```

1. Review the response, references, and debug information.

   <!-- Add more details -->

## Review the created objects

Azure AI Search automatically generates a data source, skillset, index, and indexer for each blob knowledge source. These objects form an end-to-end pipeline for data ingestion, enrichment, chunking, and vectorization. You should review these objects to learn how your data is processed for agentic retrieval.

To review the auto-generated objects:

1. From the left pane, select **Search management**.

1. Check the data source to verify the connection to your blob storage container.

1. Check the skillset to see how your content is chunked and vectorized using your embedding model.

1. Check the index to see how your content is organized for retrieval, including which fields are searchable and filterable and which fields store vectors for similarity search.

1. Check the indexer for success or failure messages. Connection or quota errors appear here.

## Clean up resources

When you work in your own subscription, it's a good idea to finish a project by determining whether you still need the resources you created. Resources that are left running can cost you money.

In the Azure portal, you can manage your Azure AI Search, Azure Blob Storage, and Azure AI Foundry resources by selecting **All resources** or **Resource groups** from the left pane.

You can also delete the knowledge source and knowledge base on their respective portal pages. When you delete the knowledge source, the portal prompts you to delete the associated data source, skillset, index, and indexer.

## Next step

> [!div class="nextstepaction"]
> [Learn more about agentic retrieval](/azure/search/agentic-retrieval-overview)
