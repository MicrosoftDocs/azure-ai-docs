---
title: "Quickstart: Agentic Retrieval in the Azure portal"
titleSuffix: Azure AI Search
description: Learn how to use agentic retrieval in the Azure portal for a conversational search experience powered by Azure AI Search and Azure OpenAI models.
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.custom:
  - ignite-2025
ms.topic: quickstart
ms.date: 02/05/2026
---

# Quickstart: Agentic retrieval in the Azure portal

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

In this quickstart, you use [agentic retrieval](agentic-retrieval-overview.md) in the Azure portal to create a conversational search experience powered by documents indexed in Azure AI Search and a large language model (LLM) from Azure OpenAI in Foundry Models.

The portal guides you through the process of creating the following objects:

+ A *knowledge source* that references a container in Azure Blob Storage. When you create a blob knowledge source, Azure AI Search automatically generates an index and other pipeline objects to ingest and enrich your content for agentic retrieval.

+ A *knowledge base* that uses agentic retrieval to infer the underlying information need, plan and execute subqueries, and formulate a natural-language answer using the optional answer synthesis output mode.

Afterwards, you test the knowledge base by submitting a complex query that requires information from multiple documents and reviewing the synthesized answer.

> [!IMPORTANT]
> The portal now uses the 2025-11-01-preview REST APIs for knowledge sources and knowledge bases. If you previously created agentic retrieval objects in the portal, those objects use the 2025-08-01-preview and are subject to breaking changes. We recommend that you [migrate existing objects and code](agentic-retrieval-how-to-migrate.md) as soon as possible.

## Prerequisites

+ An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

+ An [Azure AI Search service](search-create-service-portal.md) in any [region that provides agentic retrieval](search-region-support.md).

+ An [Azure Blob Storage account](/azure/storage/common/storage-account-create).

+ A [Microsoft Foundry project](/azure/ai-foundry/how-to/create-projects) and resource. When you create a project, the resource is automatically created.

+ For text-to-vector conversion, an embedding model [deployed to your project](/azure/ai-foundry/how-to/deploy-models-openai). You can use any `text-embedding` model, such as `text-embedding-3-large`.

+ For query planning and answer generation, an LLM [deployed to your project](/azure/ai-foundry/how-to/deploy-models-openai). You can use any [portal-supported LLM](#supported-llms).

### Supported LLMs

Although agentic retrieval [programmatically supports several LLMs](agentic-retrieval-how-to-create-knowledge-base.md#supported-models), the portal currently supports the following LLMs:

+ `gpt-4o`
+ `gpt-4o-mini`
+ `gpt-5`
+ `gpt-5-mini`
+ `gpt-5-nano`

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

+ Assign **Storage Blob Data Reader** to your [search service identity](search-how-to-managed-identities.md#create-a-system-managed-identity).

### [Microsoft Foundry](#tab/foundry-perms)

Microsoft Foundry provides the Azure OpenAI models used for embeddings, query planning, and answer generation. Grant your search service permission to use these models.

On your Microsoft Foundry resource:

+ Assign **Cognitive Services User** to your [search service identity](search-how-to-managed-identities.md#create-a-system-managed-identity).

---

> [!IMPORTANT]
> Agentic retrieval has two token-based billing models:
>
> + Billing from Azure AI Search for agentic retrieval.
> + Billing from Azure OpenAI for query planning and answer synthesis.
>
> For more information, see [Availability and pricing of agentic retrieval](agentic-retrieval-overview.md#availability-and-pricing).

## Prepare sample data

This quickstart uses sample JSON documents from NASA's Earth at Night e-book, but you can also use your own files. The documents describe general science topics and images of Earth at night as observed from space.

To prepare the sample data for this quickstart:

1. Sign in to the [Azure portal](https://portal.azure.com/) and select your Azure Blob Storage account.

1. From the left pane, select **Data storage** > **Containers**.

1. Create a container named **earth-at-night-data**.

1. Upload the [sample JSON documents](https://github.com/Azure-Samples/azure-search-sample-data/tree/main/nasa-e-book/earth-at-night-json) to the container.

## Create a knowledge source

A knowledge source is a reusable reference to your source data. In this section, you create a [blob knowledge source](agentic-knowledge-source-how-to-blob.md), which triggers the creation of a *data source*, *skillset*, *index*, and *indexer* to automate data indexing and enrichment. You review these objects in a later section.

You also configure a *vectorizer*, which uses your deployed embedding model to convert text into vectors and match documents based on semantic similarity. The vectorizer, vector fields, and vectors will be added to the auto-generated index.

To create the knowledge source for this quickstart:

1. Sign in to the [Azure portal](https://portal.azure.com/) and select your search service.

1. From the left pane, select **Agentic retrieval** > **Knowledge sources**.

1. Select **Add knowledge source** > **Add knowledge source**.

1. Select **Azure blob (Indexed)**.

1. Enter **earth-at-night-ks** for the name, and then select your subscription, storage account, and container with the sample data.

1. Select the **Authenticate using managed identity** checkbox. Leave the identity type as **System-assigned**.

1. Under **Enable text vectorization**, select **Add vectorizer**.

1. Select **Azure AI Foundry** for the kind, and then select your subscription, project, and embedding model deployment.

1. Select **System assigned identity** for the authentication type.

1. Save the vectorizer.

1. Create the knowledge source.

   :::image type="content" source="media/get-started-portal-agentic-retrieval/create-knowledge-source.png" alt-text="Screenshot of the knowledge source configuration for this quickstart." lightbox="media/get-started-portal-agentic-retrieval/create-knowledge-source.png" :::

## Create a knowledge base

A knowledge base uses your knowledge source and deployed LLM to orchestrate agentic retrieval. When a user submits a complex query, the LLM generates subqueries that are sent simultaneously to your knowledge source. Azure AI Search then semantically ranks the results for relevance and combines the best results into a single, unified response.

The output mode determines how the knowledge base formulates answers. You can either use extractive data for verbatim content or [answer synthesis](agentic-retrieval-how-to-answer-synthesis.md) for natural-language answer generation. By default, the portal uses answer synthesis.

To create the knowledge base for this quickstart:

1. From the left pane, select **Agentic retrieval** > **Knowledge bases**.

1. Select **Add knowledge base** > **Add knowledge base**.

1. Enter **earth-at-night-kb** for the name.

1. Under **Chat completion model**, select **Add model deployment**.

1. Select **Azure AI Foundry** for the kind, and then select your subscription, project, and LLM deployment.

1. Select **System assigned identity** for the authentication type.

1. Save the model deployment.

1. Under **Knowledge sources**, select **earth-at-night-ks**.

1. Create the knowledge base.

   :::image type="content" source="media/get-started-portal-agentic-retrieval/create-knowledge-base.png" alt-text="Screenshot of the knowledge base configuration for this quickstart." lightbox="media/get-started-portal-agentic-retrieval/create-knowledge-base.png" :::

## Test agentic retrieval

The portal provides a chat playground where you can submit `retrieve` requests to the knowledge base, whose responses include references to your knowledge sources and debug information about the retrieval process.

To query the knowledge base:

1. Use the chat box to send the following query.

    ```
    Why do suburban belts display larger December brightening than urban cores even though absolute light levels are higher downtown? Why is the Phoenix nighttime street grid is so sharply visible from space, whereas large stretches of the interstate between midwestern cities remain comparatively dim?
    ```

1. Review the synthesized, citation-backed answer, which should be similar to the following example.

    ```
    Suburban belts show larger December brightening in satellite nighttime lights than urban cores mainly because of relative (percentage) change effects and differences in how light is used and distributed. Areas with lower baseline light (suburbs, residential streets) can increase lighting use or reflect more light in winter and so show a bigger percent change, while bright urban cores are already near sensor saturation so their relative increase is small. The retrieved material explains that brightest lights are generally the most urbanized but not necessarily the most populated, and that poor or low‑light areas can have large populations but low availability or use of electric lights; thus lower‑light suburbs can exhibit larger relative changes when seasonal lighting rises.
    ```

1. Select the debug icon to review the activity log, which should be similar to the following JSON.

    ```JSON
    [
      {
        "type": "modelQueryPlanning",
        "id": 0,
        "inputTokens": 1518,
        "outputTokens": 284,
        "elapsedMs": 3001
      },
      {
        "type": "azureBlob",
        "id": 1,
        "knowledgeSourceName": "earth-at-night-ks",
        "queryTime": "2025-12-12T18:54:28.792Z",
        "count": 1,
        "elapsedMs": 456,
        "azureBlobArguments": {
          "search": "causes of December brightening in satellite nighttime lights suburban vs urban cores"
        }
      },
      {
        "type": "azureBlob",
        "id": 2,
        "knowledgeSourceName": "earth-at-night-ks",
        "queryTime": "2025-12-12T18:54:29.389Z",
        "count": 3,
        "elapsedMs": 596,
        "azureBlobArguments": {
          "search": "factors affecting seasonal variation in nighttime lights December winter brightening suburban belts urban cores"
        }
      },
      {
        "type": "azureBlob",
        "id": 3,
        "knowledgeSourceName": "earth-at-night-ks",
        "queryTime": "2025-12-12T18:54:29.862Z",
        "count": 6,
        "elapsedMs": 472,
        "azureBlobArguments": {
          "search": "why is Phoenix street grid highly visible at night from space compared to dim interstates in the Midwest reasons lighting patterns road lighting urban form"
        }
      },
      {
        "type": "agenticReasoning",
        "id": 4,
        "retrievalReasoningEffort": {
          "kind": "low"
        },
        "reasoningTokens": 111243
      },
      {
        "type": "modelAnswerSynthesis",
        "id": 5,
        "inputTokens": 7514,
        "outputTokens": 1058,
        "elapsedMs": 12334
      }
    ]
    ```

   The activity log offers insight into the steps taken during retrieval, including query planning and execution, semantic ranking, and answer synthesis. For more information, see [Review the activity array](agentic-retrieval-how-to-retrieve.md#review-the-activity-array).

## Review the created objects

Azure AI Search automatically generates a data source, skillset, index, and indexer for each blob knowledge source. These objects form an end-to-end pipeline for data ingestion, enrichment, chunking, and vectorization. You can review these objects to learn how your data is processed for agentic retrieval.

To review the auto-generated objects:

1. From the left pane, select **Search management**.

1. Check the data source to verify the connection to your blob storage container.

1. Check the skillset to see how your content is chunked and vectorized using your embedding model.

1. Check the index to see how your content is indexed and exposed for retrieval, including which fields are searchable and filterable and which fields store vectors for similarity search.

1. Check the indexer for success or failure messages. Connection or quota errors appear here.

## Clean up resources

[!INCLUDE [clean up resources (paid)](includes/resource-cleanup-paid.md)]

You can also delete the knowledge source and knowledge base on their respective portal pages. When you delete the knowledge source, the portal prompts you to delete the associated data source, skillset, index, and indexer.

## Next step

> [!div class="nextstepaction"]
> [Learn more about agentic retrieval](/azure/search/agentic-retrieval-overview)
