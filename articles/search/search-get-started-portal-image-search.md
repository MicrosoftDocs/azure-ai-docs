---
title: "Quickstart: Multimodal Search in the Azure portal"
titleSuffix: Azure AI Search
description: Learn how to search for multimodal content on an Azure AI Search index in the Azure portal. Run a wizard to vectorize text and images, and then use Search Explorer to provide an image as your query input.
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: quickstart
ms.date: 05/20/2025
ms.custom:
  - references_regions
---

# Quickstart: Search for multimodal content in the Azure portal

In this quickstart, you use the **Import and vectorize data wizard** in the Azure portal to get started with [multimodal search](multimodal-search-overview.md). Multimodality refers to the ability to process and query over multiple types of data, such as text and images.

The sample data consists of a multimodal PDF in the [azure-search-sample-data](https://github.com/Azure-Samples/azure-search-sample-data/tree/main/sustainable-ai-pdf) repo, but you can use different files and still follow this quickstart.

## Prerequisites

+ An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/free/?WT.mc_id=A261C142F).

+ An [Azure Storage account](/azure/storage/common/storage-account-create). Use Azure Blob Storage or Azure Data Lake Storage Gen2 (storage account with a hierarchical namespace) on a standard performance (general-purpose v2) account. Access tiers can be hot, cool, or cold.

+ An [Azure AI services multi-service account](/azure/ai-services/multi-service-resource#azure-ai-services-resource-for-azure-ai-search-skills) in East US, West Europe, or North Central US.

+ An [Azure AI Search service](search-create-service-portal.md) in the same region as your Azure AI multi-service account. You can use any pricing tier.

+ An [Azure OpenAI resource](/azure/ai-services/openai/how-to/create-resource).

+ Familiarity with the wizard. See [Import data wizards in the Azure portal](search-import-data-portal.md).

### Public endpoint requirements

All of the preceding resources must have public access enabled so that the Azure portal nodes can access them. Otherwise, the wizard fails. After the wizard runs, you can enable firewalls and private endpoints on the integration components for security. For more information, see [Secure connections in the import wizards](search-import-data-portal.md#secure-connections).

If private endpoints are already present and you can't disable them, the alternative is to run the respective end-to-end flow from a script or program on a virtual machine. The virtual machine must be on the same virtual network as the private endpoint. [Here's a Python code sample](https://github.com/Azure/azure-search-vector-samples/tree/main/demo-python/code/integrated-vectorization) for integrated vectorization. The same [GitHub repo](https://github.com/Azure/azure-search-vector-samples/tree/main) has samples in other programming languages.

### Role-based access

A free search service supports role-based access control on connections to Azure AI Search, but it doesn't support managed identities on outbound connections to Azure Storage or Azure AI Vision. This level of support means you must use key-based authentication on connections between a free search service and other Azure services. For more secure connections:

+ Use the Basic tier or higher.

+ [Configure a system-assigned managed identity](search-howto-managed-identities-data-sources.md#create-a-system-managed-identity) and role assignments to admit requests from Azure AI Search on other Azure services.

### Check for space

If you're starting with the free service, you're limited to three indexes, three data sources, three skillsets, and three indexers. Make sure you have room for extra items before you begin. This quickstart creates one of each object.

## Prepare sample data

This quickstart uses a sample multimodal PDF, but you can also use your own files. If you're on a free search service, use fewer than 20 files to stay within the free quota for enrichment processing.

To prepare the sample data for this quickstart:

1. Sign in to the [Azure portal](https://portal.azure.com/) and select your Azure Storage account.

1. From the left pane, select **Data storage** > **Containers**.

1. Create a container, and then upload the [sample PDF](https://github.com/Azure-Samples/azure-search-sample-data/blob/main/sustainable-ai-pdf/Accelerating-Sustainability-with-AI-2025.pdf) to the container.

1. Create another container to store images extracted from the PDF.

## Prepare models

The wizard requires a large language model (LLM) to verbalize images and an embedding model to generate vector representations of text and images. Both models are available through Azure OpenAI.

Multimodal search supports several models, but this quickstart assumes `gpt-4o` for the LLM and `text-embedding-3-large` for the embedding model.

To prepare the models for this quickstart:

1. Sign in to the [Azure AI Foundry portal](https://ai.azure.com) and select your Azure OpenAI resource.

1. From the left pane, select **Model catalog**.

1. Deploy `gpt-4o` and `text-embedding-3-large`.

## Start the wizard

If your Azure Storage blob container has the default configuration, and if your Azure AI Search service and Azure AI multi-service account are in the [same supported region](cognitive-search-skill-document-intelligence-layout.md) and tenant, you're ready to proceed.

To start the wizard for multimodal search:

1. Sign in to the [Azure portal](https://portal.azure.com/) and select your Azure AI Search service.

1. On the **Overview** page, select **Import and vectorize data**.

   :::image type="content" source="media/search-get-started-portal-import-vectors/command-bar.png" alt-text="Screenshot of the command to open the wizard for importing and vectorizing data.":::

1. Select your data source: **Azure Blob Storage** or **Azure Data Lake Storage Gen2**.

   :::image type="content" source="media/search-get-started-portal-images/select-data-source.png" alt-text="Screenshot of the options for selecting a data source in the wizard." border="true" lightbox="media/search-get-started-portal-images/select-data-source.png":::

1. Select **Multimodal RAG**.

   :::image type="content" source="media/search-get-started-portal-images/wizard-scenarios-multimodal-rag.png" alt-text="Screenshot of the Multimodal RAG tile in the wizard." border="true" lightbox="media/search-get-started-portal-images/wizard-scenarios-multimodal-rag.png":::

## Connect to your data

Azure AI Search requires a connection to a data source for content ingestion and indexing. In this case, the data source is your Azure Storage account.

To connect to your data:

1. On the **Connect to your data** page, specify your Azure subscription.

1. Select the storage account and container to which you uploaded the sample data.

1. Select the **Authenticate using managed identity** checkbox. Leave the identity type as **System-assigned**.

   :::image type="content" source="media/search-get-started-portal-images/connect-to-your-data.png" alt-text="Screenshot of the wizard page for setting up a data connection." border="true" lightbox="media/search-get-started-portal-images/connect-to-your-data.png":::

1. Select **Next**.

## Extract your content

The next step is to select a method for document cracking and chunking.

Your Azure AI multi-service account provides access to the [Document Layout skill](cognitive-search-skill-document-intelligence-layout.md), which extracts page numbers, bounding polygons, and other location metadata from both text and images. The Document Layout skill also breaks large documents into smaller, more manageable chunks.

To use the Document Layout skill:

1. On the **Content extraction** page, select **AI Document Intelligence**.

1. Specify your Azure subscription and Azure AI multi-service account.

1. For the authentication type, select **System assigned identity**.

1. Select the checkbox that acknowledges the billing effects of using these resources.

   :::image type="content" source="media/search-get-started-portal-images/extract-your-content.png" alt-text="Screenshot of the wizard page for selecting a content extraction method." border="true" lightbox="media/search-get-started-portal-images/extract-your-content.png":::

1. Select **Next**.

## Embed your content

During this step, the wizard calls two skills to generate both descriptive text for images (image verbalization) and vector embeddings for text and images.

For image verbalization, the [GenAI Prompt skill](cognitive-search-skill-genai-prompt.md) uses the LLM you deployed to analyze each extracted image and produce a natural-language description.

For text and image embeddings, the [Azure OpenAI Embedding skill](cognitive-search-skill-azure-openai-embedding.md) uses the embedding model you deployed to convert the text chunks and verbalized descriptions into high-dimensional vectors. These vectors enable similarity and hybrid retrieval.

To use the GenAI Prompt skill and Azure OpenAI Embedding skill:

1. On the **Content embedding** page, select **Image Verbalization**.

   :::image type="content" source="media/search-get-started-portal-images/image-verbalization-tile.png" alt-text="Screenshot of the Image Verbalization tile in the wizard." border="true" lightbox="media/search-get-started-portal-images/image-verbalization-tile.png":::

1. On the **Image Verbalization** tab:

   1. For the kind, select **Azure OpenAI**.

   1. Specify your Azure subscription, Azure OpenAI resource, and LLM deployment. This quickstart assumes `gpt-4o`.

   1. For the authentication type, select **System assigned identity**.

   1. Select the checkbox that acknowledges the billing effects of using these resources.

      :::image type="content" source="media/search-get-started-portal-images/image-verbalization-tab.png" alt-text="Screenshot of the wizard page for verbalizing images." border="true" lightbox="media/search-get-started-portal-images/image-verbalization-tab.png":::

1. On the **Text Vectorization** tab:

   1. For the kind, select **Azure OpenAI**.

   1. Specify your Azure subscription, Azure OpenAI resource, and embedding model deployment. This quickstart assumes `text-embedding-3-large`.

   1. For the authentication type, select **System assigned identity**.

   1. Select the checkbox that acknowledges the billing effects of using these resources.

      :::image type="content" source="media/search-get-started-portal-images/text-vectorization-tab.png" alt-text="Screenshot of the wizard page for vectorizing text and images." border="true" lightbox="media/search-get-started-portal-images/text-vectorization-tab.png":::

1. Select **Next**.

## Store the extracted images

The next step is to save any images extracted from your documents in Azure Storage. In Azure AI Search, this is known as a knowledge store.

To store the extracted images:

1. On the **Image output** page, specify your Azure subscription.

1. Select the storage account and blob container you created to store the images.

1. Select the **Authenticate using managed identity** checkbox. Leave the identity type as **System-assigned**.

   :::image type="content" source="media/search-get-started-portal-images/store-images.png" alt-text="Screenshot of the wizard page for storing the extracting images." border="true" lightbox="media/search-get-started-portal-images/store-images.png":::

1. Select **Next**.

## Map new fields

On the **Advanced settings** page, you can optionally add fields to the index schema. By default, the wizard generates the fields described in the following table.

| Field | Applies to | Description | Attributes |
|--|--|--|--|
| content_id | Text and image vectors | String field. Document key for the index. | Searchable, retrievable, sortable, filterable, and facetable. |
| document_title | Text and image vectors | String field. Human-readable document title, page title, or page number. | Searchable, retrievable, sortable, filterable, and facetable. |
| text_document_id | Text vectors | String field. Identifies the parent document from which the text chunk originates. | Retrievable and filterable. |
| image_document_id | Image vectors | String field. Identifies the parent document from which the image chunk originates. | Searchable, retrievable, sortable, filterable, and facetable. |
| content_text | Text vectors | String field. Human-readable version of the text chunk. | Searchable, retrievable, sortable, filterable, and facetable. |
| content_embedding | Image vectors | Collection(Edm.Single). Vector representation of the image chunk. | Searchable and retrievable. |
| content_path | Text and image vectors | String field. Path to the content in the storage container. | Retrievable, sortable, filterable, and facetable. |
| locationMetadata | Text and image vectors | Edm.ComplexType. Contains metadata about the content's location. | Varies by field. |

You can't modify the generated fields or their attributes, but you can add fields if your data source provides them. For example, Azure Blob Storage provides a collection of metadata fields.

To add fields to the index schema:

1. Under **Index fields**, select **Preview and edit**.

1. Select **Add field**.

1. Select a source field from the available fields, enter a field name for the index, and accept (or override) the default data type.

   > [!NOTE]
   > Metadata fields are searchable but not retrievable, filterable, facetable, or sortable.

1. Select **Reset** if you want to restore the schema to its original version.

## Schedule indexing

For data sources where the underlying data is volatile, you can [schedule indexing](search-howto-schedule-indexers.md) to capture changes at specific intervals or specific dates and times.

To schedule indexing:

1. On the **Advanced settings** page, under **Schedule indexing**, specify a run schedule for the indexer. We recommend **Once** for this quickstart.

   :::image type="content" source="media/search-get-started-portal-images/run-once.png" alt-text="Screenshot of the wizard page for scheduling indexing." border="true" lightbox="media/search-get-started-portal-images/run-once.png":::

1. Select **Next**.

## Finish the wizard

The final step is to review your configuration and create the objects required for multimodal search. If necessary, return to previous pages in the wizard to adjust your configuration.

To finish the wizard:

1. On the **Review and create** page, specify a prefix for the objects the wizard will create. A common prefix helps you stay organized.

   :::image type="content" source="media/search-get-started-portal-images/review-create.png" alt-text="Screenshot of the wizard page for reviewing and completing the configuration." border="true" lightbox="media/search-get-started-portal-images/review-create.png":::

1. Select **Create**.

When the wizard completes the configuration, it creates the following objects:

+ An indexer that drives the indexing pipeline.

+ A data source connection to Azure Blob Storage.

+ An index with text fields, vector fields, vectorizers, vector profiles, and vector algorithms. During the wizard workflow, you can't modify the default index. Indexes conform to the [2024-05-01-preview REST API](/rest/api/searchservice/indexes/create-or-update?view=rest-searchservice-2024-05-01-preview&preserve-view=true) so that you can use preview features.

+ A skillset with the following skills:

  + The [Document Layout skill](cognitive-search-skill-document-intelligence-layout.md) splits documents into text chunks and extracts images with location data.

  + The [GenAI Prompt skill](cognitive-search-skill-genai-prompt.md) generates natural-language descriptions (verbalizations) of images.

  + The [Azure OpenAI Embedding skill](cognitive-search-skill-azure-openai-embedding.md) vectorizes each text chunk.

  + The [Azure OpenAI Embedding skill](cognitive-search-skill-azure-openai-embedding.md) is called again to vectorize each image verbalization.

  + The [Shaper skill](cognitive-search-skill-shaper.md) enriches the output with metadata and creates new images with contextual information.

> [!TIP]
> Wizard-created objects have configurable JSON definitions. To view or modify these definitions, select **Search management** from the left pane, where you can view your indexes, indexers, data sources, and skillsets.

## Check results

Search Explorer accepts text, images, and vectors as query inputs. For images, Search Explorer vectorizes the image and sends the vector as a query input to the search engine. Image vectorization assumes that your index has a vectorizer definition, which the **Import and vectorize data wizard** creates based on your embedding model inputs.

The following steps assume that you're searching for images. For the other two query types, see [Quickstart: Keyword search](search-get-started-portal.md#query-with-search-explorer) and [Quickstart: Vector search](search-get-started-portal-import-vectors.md#check-results).

To use Search Explorer for image search:

1. Sign in to the [Azure portal](https://portal.azure.com/) and select your Azure AI Search service.

1. From the left pane, select **Search management** > **Indexes**, and then select your index.

1. Select the **Search explorer** tab.

1. From the **View** menu, select **Image view**.

   :::image type="content" source="media/search-get-started-portal-images/select-image-view.png" alt-text="Screenshot of the command for selecting image view." border="true" lightbox="media/search-get-started-portal-images/select-image-view.png":::

1. Drag or select a [sample PNG](https://github.com/Azure-Samples/azure-search-sample-data/blob/main/sustainable-ai-pdf) from your local folder. The PNGs come directly from the sample PDF used in this quickstart.

1. Select **Search** to run the query.

   The top match should be the image for which you searched. Because a [vector search](vector-search-overview.md) matches on similar vectors, the search engine returns any document that's sufficiently similar to the query input, up to the `k` number of results. For more advanced queries that include relevance tuning, switch to the JSON view.

   :::image type="content" source="media/search-get-started-portal-images/image-search.png" alt-text="Screenshot of the search results for image search." border="true" lightbox="media/search-get-started-portal-images/image-search.png":::

1. Try other query options to compare search outcomes:

   + (Recommended) Hide vectors for more readable results.

   + Select a vector field to query over. The default is text vectors, but you can specify the image vector to exclude text vectors from query execution.

## Clean up resources

This quickstart uses billable Azure resources. If you no longer need the resources, delete them from your subscription to avoid charges.

## Next step

This quickstart introduced you to the **Import and vectorize data wizard**, which creates all of the necessary objects for multimodal search. To explore each step in detail, see [Tutorial: Index mixed content using image verbalizations and the Document Layout skill](tutorial-multimodal-index-image-verbalization-skill.md).
