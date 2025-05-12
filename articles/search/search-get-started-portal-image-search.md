---
title: "Quickstart: Multimodal Search in the Azure portal"
titleSuffix: Azure AI Search
description: Learn how to search for multimodal content on an Azure AI Search index in the Azure portal. Run a wizard to vectorize text and images, and then use Search Explorer to provide multimodal content as your query input.
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: quickstart
ms.date: 05/09/2025
ms.custom:
  - references_regions
---

# Quickstart: Search for multimodal content in the Azure portal

In this quickstart, you use the **Import and vectorize data wizard** in the Azure portal to get started with multimodal search. Multimodality refers to the ability to process and query over multiple types of data, such as text and images.

The sample data consists of a multimodal PDF in the [azure-search-sample-data](https://github.com/Azure-Samples/azure-search-sample-data/tree/main/sustainable-ai-pdf) repo, but you can use different files and still follow this quickstart.

## Prerequisites

+ An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/free/?WT.mc_id=A261C142F).

+ An [Azure Storage account](/azure/storage/common/storage-account-create) to store files as blobs. Use Azure Blob Storage or Azure Data Lake Storage Gen2 (a storage account with a hierarchical namespace) on a standard performance (general-purpose v2) account. Access tiers can be hot, cool, or cold.

+ An [Azure AI services multi-service account](/azure/ai-services/multi-service-resource#azure-ai-services-resource-for-azure-ai-search-skills) for image vectorization, which requires the Azure AI Vision multimodal embeddings. For regional availability, see the [Azure AI Vision documentation](/azure/ai-services/computer-vision/overview-image-analysis#region-availability).

+ An [Azure AI Search service](search-create-service-portal.md) for indexing and queries. Your service can be on any tier, but it must be in the [same region as your Azure AI multi-service account](search-create-service-portal.md#regions-with-the-most-overlap).

  + The pricing tier determines how many blobs you can index. We used the free tier to create this quickstart and limited the content to one PDF.

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

1. Sign in to the [Azure portal](https://portal.azure.com/) and go to your Azure Storage account.

1. From the left pane, select **Data storage** > **Containers**.

1. Create a container, and then upload the [sample PDF](https://github.com/Azure-Samples/azure-search-sample-data/blob/main/sustainable-ai-pdf/Accelerating-Sustainability-with-AI-2025.pdf) to the container.

1. Create another container to store images extracted from the PDF.

## Start the wizard

If your Azure AI Search service and Azure AI multi-service account are in the [same region](/azure/ai-services/computer-vision/how-to/image-retrieval) and tenant, and if your Azure Storage blob container has the default configuration, you're ready to proceed.

To start the wizard for multimodal search:

1. Sign in to the [Azure portal](https://portal.azure.com/) and go to your Azure AI Search service.

1. On the **Overview** page, select **Import and vectorize data wizard**.

   :::image type="content" source="media/search-get-started-portal-import-vectors/command-bar-quickstart-wizard.png" alt-text="Screenshot of the command to open the wizard for importing and vectorizing data.":::

1. Select your data source: **Azure Blob Storage** or **Azure Data Lake Storage Gen2**.

1. Select the **Multimodal RAG** tile.

## Connect to your data

Azure AI Search requires a connection to the data source that contains the sample data. In this case, the data source is an Azure Storage account.

To connect to your data source:

1. On the **Connect to your data** page, specify the Azure subscription.

1. Select the storage account and container that provide the data. Use the default values for the remaining boxes.

   :::image type="content" source="media/search-get-started-portal-images/connect-to-your-data.png" alt-text="Screenshot of the wizard page for setting up a data connection." border="true" lightbox="media/search-get-started-portal-images/connect-to-your-data.png":::

1. Select **Next**.

## Extract your content

The next step is to select a method for document cracking and chunking. The default method uses the [Document Extraction skill](cognitive-search-skill-document-extraction.md) to extract content and metadata from documents, which includes generating normalized images. The [Text Split skill](cognitive-search-skill-textsplit.md) is then used to split the extracted content into pages.

To use the default extraction method:

1. On the **Content extraction** page, select the **Default** tile.

   :::image type="content" source="media/search-get-started-portal-images/extract-your-content.png" alt-text="Screenshot of the wizard page for selecting a content extraction method." border="true" lightbox="media/search-get-started-portal-images/extract-your-content.png":::

1. Select **Next**.

## Embed your content

If the raw content includes text, or if the Document Extraction skill produces text, the wizard calls the [Azure AI Vision multimodal embeddings skill](cognitive-search-skill-vision-vectorize.md) to vectorize the text. The same embedding skill is used to generate vector representations of images.

The wizard also calls the [Shaper skill](cognitive-search-skill-shaper.md) to enrich the output with metadata, such as page numbers. This metadata is useful for associating vectorized content with its original context in the document.

To generate embeddings for your text and images:

1. On the **Content embedding** page, select the **Multimodal Embedding** tile.

1. Select **AI Vision vectorization** for the embedding kind. If it's unavailable, make sure your Azure AI Search service and Azure AI multi-service account are both in a region that [supports the AI Vision multimodal APIs](/azure/ai-services/computer-vision/how-to/image-retrieval).

1. Specify the subscription, multi-service account, and authentication type.

1. Select the checkbox that acknowledges the billing effects of using this resource.

   :::image type="content" source="media/search-get-started-portal-images/vectorize-your-text.png" alt-text="Screenshot of the wizard page for vectorizing text and images." border="true" lightbox="media/search-get-started-portal-images/vectorize-your-text.png":::

1. Select **Next**.

## Store the extracted images

The next step is to save any images extracted from your documents in Azure Storage. In Azure AI Search, this is known as a knowledge store.

To store the extracted images:

1. On the **Image output** page, specify the subscription.

1. Select the storage account and blob container you created to store the images.

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

1. Select **Add new**.

1. Select a source field from the list of available fields, provide a field name for the index, and accept the default data type or override as needed.

   + Metadata fields are searchable but not retrievable, filterable, facetable, or sortable.

1. Select **Reset** if you want to restore the schema to its original version.

## Schedule indexing

For data sources where the underlying data is volatile, you can schedule indexing to capture changes at specific intervals or specific dates and times.

To schedule indexing:

1. On the **Advanced settings** page, under **Schedule indexing**, specify a [run schedule](search-howto-schedule-indexers.md) for the indexer. We recommend **Once** for this quickstart.

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

  + The [Document Extraction skill](cognitive-search-skill-document-extraction.md) extracts both text and images from the documents.

  + The [Text Split skill](cognitive-search-skill-textsplit.md) adds data chunking.

  + The [Azure AI Vision multimodal embeddings skill](cognitive-search-skill-vision-vectorize.md) vectorizes text produced by the Document Extraction skill.

  + The [Azure AI Vision multimodal embeddings skill](cognitive-search-skill-vision-vectorize.md) is called again to vectorize images.

  + The [Shaper skill](cognitive-search-skill-shaper.md) enriches the output with metadata and creates new images with contextual information.

## Check results

Search Explorer accepts text, images, and vectors as query inputs. For images, Search Explorer vectorizes the image and sends the vector as a query input to the search engine. Image vectorization assumes that your index has a vectorizer definition, which the **Import and vectorize data wizard** creates based on your embedding model inputs.

The following steps assume that you're searching for images. For the other two query types, see [Quickstart: Keyword search](search-get-started-portal.md#query-with-search-explorer) and [Quickstart: Vector search](search-get-started-portal-import-vectors.md#check-results).

To use Search Explorer for image search:

1. Sign in to the [Azure portal](https://portal.azure.com/) and go to your Azure AI Search service.

1. From the left pane, select **Search management** > **Indexes**, and then select the index you created.

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

This quickstart introduced you to the **Import and vectorize data wizard** that creates all of the necessary objects for multimodal search. If you want to explore each step in detail, try an [integrated vectorization sample](https://github.com/Azure/azure-search-vector-samples/blob/main/demo-python/code/integrated-vectorization/azure-search-integrated-vectorization-sample.ipynb).
