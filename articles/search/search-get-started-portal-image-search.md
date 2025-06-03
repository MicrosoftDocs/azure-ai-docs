---
title: "Quickstart: Multimodal Search in the Azure portal"
titleSuffix: Azure AI Search
description: Learn how to index and search for multimodal content in the Azure portal. Run a wizard to extract and embed both text and images, and then use Search Explorer to query your multimodal index.
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: quickstart
ms.date: 06/03/2025
ms.custom:
  - references_regions
---

# Quickstart: Search for multimodal content in the Azure portal

In this quickstart, you use the **Import and vectorize data** wizard in the Azure portal to get started with [multimodal search](multimodal-search-overview.md). The wizard simplifies the process of extracting, chunking, vectorizing, and loading both text and images into a searchable index.

Unlike [Quickstart: Vector search in the Azure portal](search-get-started-portal-import-vectors.md), which processes simple text-containing images, this quickstart supports advanced image processing for multimodal RAG scenarios.

This quickstart uses a multimodal PDF from the [azure-search-sample-data](https://github.com/Azure-Samples/azure-search-sample-data/tree/main/sustainable-ai-pdf) repo. However, you can use different files and still complete this quickstart.

## Prerequisites

+ An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/free/?WT.mc_id=A261C142F).

+ An [Azure AI Search service](search-create-service-portal.md). We recommend the Basic tier or higher.

+ An [Azure Storage account](/azure/storage/common/storage-account-create). Use Azure Blob Storage or Azure Data Lake Storage Gen2 (storage account with a hierarchical namespace) on a standard performance (general-purpose v2) account. Access tiers can be hot, cool, or cold.

+ A [supported extraction method](#supported-extraction-methods).

+ A [supported embedding method](#supported-embedding-methods).

+ Familiarity with the wizard. See [Import data wizards in the Azure portal](search-import-data-portal.md).

### Supported extraction methods

For content extraction, you can choose either default extraction via Azure AI Search or enhanced extraction via [Azure AI Document Intelligence](/azure/ai-services/document-intelligence/overview). The following table describes both extraction methods.

| Method | Description |
|--|--|
| Default extraction | Extracts location metadata from PDF images only. Doesn't require another Azure AI resource. |
| Enhanced extraction | Extracts location metadata from text and images for multiple document types. Requires an [Azure AI services multi-service resource](/azure/ai-services/multi-service-resource#azure-ai-multi-services-resource-for-azure-ai-search-skills) <sup>1</sup> in a [supported region](cognitive-search-skill-document-intelligence-layout.md#supported--regions). |

<sup>1</sup> For billing purposes, you must [attach your multi-service resource](cognitive-search-attach-cognitive-services.md) to the skillset in your Azure AI Search service. Unless you use a [keyless connection](cognitive-search-attach-cognitive-services.md#bill-through-a-keyless-connection) to create the skillset, both resources must be in the same region.

### Supported embedding methods

For content embedding, you can choose either image verbalization (followed by text vectorization) or multimodal embeddings. Deployment instructions for the models are provided in a [later section](#deploy-models). The following table describes both embedding methods.

| Method | Description | Supported models |
|--|--|--|
| Image verbalization | Uses an LLM to generate natural-language descriptions of images, and then uses an embedding model to vectorize plain text and verbalized images.<br><br>Requires an [Azure OpenAI resource](/azure/ai-services/openai/how-to/create-resource) <sup>1, 2</sup> or [Azure AI Foundry project](/azure/ai-foundry/how-to/create-projects).<br><br>For text vectorization, you can also use an [Azure AI services multi-service resource](/azure/ai-services/multi-service-resource#azure-ai-multi-services-resource-for-azure-ai-search-skills) <sup>3</sup> in a [supported region](cognitive-search-skill-vision-vectorize.md). | LLMs:<br>GPT-4o<br>GPT-4o-mini<br>phi-4 <sup>4</sup><br><br>Embedding models:<br>text-embedding-ada-002<br>text-embedding-3-small<br>text-embedding-3-large |
| Multimodal embeddings | Uses an embedding model to directly vectorize both text and images.<br><br>Requires an [Azure AI Foundry project](/azure/ai-foundry/how-to/create-projects) or [Azure AI services multi-service resource](/azure/ai-services/multi-service-resource#azure-ai-multi-services-resource-for-azure-ai-search-skills) <sup>3</sup> in a [supported region](cognitive-search-skill-vision-vectorize.md). | Cohere-embed-v3-english<br>Cohere-embed-v3-multilingual |

<sup>1</sup> The endpoint of your Azure OpenAI resource must have a [custom subdomain](/azure/ai-services/cognitive-services-custom-subdomains), such as `https://my-unique-name.openai.azure.com`. If you created your resource in the [Azure portal](https://portal.azure.com/), this subdomain was automatically generated during resource setup.

<sup>2</sup> Azure OpenAI resources (with access to embedding models) that were created in the [Azure AI Foundry portal](https://ai.azure.com/?cid=learnDocs) aren't supported. You must create an Azure OpenAI resource in the Azure portal.

<sup>3</sup> For billing purposes, you must [attach your multi-service resource](cognitive-search-attach-cognitive-services.md) to the skillset in your Azure AI Search service. Unless you use a [keyless connection](cognitive-search-attach-cognitive-services.md#bill-through-a-keyless-connection) to create the skillset, both resources must be in the same region.

<sup>4</sup> `phi-4` is only available to Azure AI Foundry projects.

### Public endpoint requirements

All of the preceding resources must have public access enabled so that the Azure portal nodes can access them. Otherwise, the wizard fails. After the wizard runs, you can enable firewalls and private endpoints on the integration components for security. For more information, see [Secure connections in the import wizards](search-import-data-portal.md#secure-connections).

If private endpoints are already present and you can't disable them, the alternative is to run the respective end-to-end flow from a script or program on a virtual machine. The virtual machine must be on the same virtual network as the private endpoint. [Here's a Python code sample](https://github.com/Azure/azure-search-vector-samples/tree/main/demo-python/code/integrated-vectorization) for integrated vectorization. The same [GitHub repo](https://github.com/Azure/azure-search-vector-samples/tree/main) has samples in other programming languages.

### Check for space

If you're starting with the free service, you're limited to three indexes, three data sources, three skillsets, and three indexers. Make sure you have room for extra items before you begin. This quickstart creates one of each object.

## Configure access

Before you begin, make sure you have permissions to access content and operations. We recommend Microsoft Entra ID authentication and role-based access for authorization. You must be an **Owner** or **User Access Administrator** to assign roles. If roles aren't feasible, you can use [key-based authentication](search-security-api-keys.md) instead.

Configure the [required roles](#required-roles) and [conditional roles](#conditional-roles) identified in this section.

### Required roles

Azure AI Search and Azure Storage are required for all multimodal search scenarios.

### [**Azure AI Search**](#tab/search-perms)

Azure AI Search provides the multimodal pipeline. Configure access for yourself and your search service to read data, run the pipeline, and interact with other Azure resources.

On your Azure AI Search service:

1. [Enable role-based access](search-security-enable-roles.md).

1. [Configure a system-assigned managed identity](search-howto-managed-identities-data-sources.md#create-a-system-managed-identity).

1. [Assign the following roles](search-security-rbac.md) to yourself:

   + **Search Service Contributor**

   + **Search Index Data Contributor**

   + **Search Index Data Reader**

### [**Azure Storage**](#tab/storage-perms)

Azure Storage is both the data source for your documents and the destination for extracted images. Your search service requires access to these storage containers, which you create in the next section.

On your Azure Storage account:

+ Assign **Storage Blob Data Contributor** to your [search service identity](search-howto-managed-identities-data-sources.md#create-a-system-managed-identity).

---

### Conditional roles

The following tabs cover all wizard-compatible resources for multimodal search. Select only the tabs that apply to your chosen [extraction method](#supported-extraction-methods) and [embedding method](#supported-embedding-methods).

### [**Azure OpenAI**](#tab/openai-perms)

Azure OpenAI provides LLMs for image verbalization and embedding models for text and image vectorization. Your search service requires access to call the [GenAI Prompt skill](cognitive-search-skill-genai-prompt.md) and [Azure OpenAI Embedding skill](cognitive-search-skill-azure-openai-embedding.md).

On your Azure OpenAI resource:

+ Assign **Cognitive Services OpenAI User** to your [search service identity](search-howto-managed-identities-data-sources.md#create-a-system-managed-identity).

### [**Azure AI Foundry**](#tab/ai-foundry-perms)

The Azure AI Foundry model catalog provides LLMs for image verbalization and embedding models for text and image vectorization. Your search service requires access to call the [GenAI Prompt skill](cognitive-search-skill-genai-prompt.md) and [AML skill](cognitive-search-aml-skill.md).

On your Azure AI Foundry project:

+ Assign **Azure AI Project Manager** to your [search service identity](search-howto-managed-identities-data-sources.md#create-a-system-managed-identity).

### [**Azure AI services**](#tab/ai-services-perms)

An Azure AI multi-service resource provides multiple Azure AI services, including [Azure AI Document Intelligence](/azure/ai-services/document-intelligence/overview) for content extraction and [Azure AI Vision](/azure/ai-services/computer-vision/overview) for content embedding. Your search service requires access to call the [Document Layout skill](cognitive-search-skill-document-intelligence-layout.md) and [Azure AI Vision multimodal embeddings skill](cognitive-search-skill-vision-vectorize.md).

On your Azure AI multi-service resource:

+ Assign **Cognitive Services User** to your [search service identity](search-howto-managed-identities-data-sources.md#create-a-system-managed-identity).

---

## Prepare sample data

This quickstart uses a sample multimodal PDF, but you can also use your own files. If you're on a free search service, use fewer than 20 files to stay within the free quota for enrichment processing.

To prepare the sample data for this quickstart:

1. Sign in to the [Azure portal](https://portal.azure.com/) and select your Azure Storage account.

1. From the left pane, select **Data storage** > **Containers**.

1. Create a container, and then upload the [sample PDF](https://github.com/Azure-Samples/azure-search-sample-data/blob/main/sustainable-ai-pdf/Accelerating-Sustainability-with-AI-2025.pdf) to the container.

1. Create another container to store images extracted from the PDF.

## Deploy models

The wizard offers several options for content embedding. Image verbalization requires an LLM to describe images and an embedding model to vectorize text and image content, while direct multimodal embeddings only require an embedding model. These models are available through Azure OpenAI and Azure AI Foundry.

> [!NOTE]
> If you're using Azure AI Vision, skip this step. The multimodal embeddings are built into your Azure AI multi-service resource and don't require model deployment.

To deploy the models for this quickstart:

1. Sign in to the [Azure AI Foundry portal](https://ai.azure.com/?cid=learnDocs).

1. Select your Azure OpenAI resource or Azure AI Foundry project.

1. From the left pane, select **Model catalog**.

1. Deploy the models required for your chosen [embedding method](#supported-embedding-methods).

## Start the wizard

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

Depending on your chosen [extraction method](#supported-extraction-methods), the wizard provides configuration options for document cracking and chunking.

### [**Default extraction**](#tab/document-extraction)

The default method calls the [Document Extraction skill](cognitive-search-skill-document-extraction.md) to extract text content and generate normalized images from your documents. The [Text Split skill](cognitive-search-skill-textsplit.md) is then called to split the extracted text content into pages.

To use the Document Extraction skill:

1. On the **Content extraction** page, select **Default**.

   :::image type="content" source="media/search-get-started-portal-images/extract-your-content-doc-extraction.png" alt-text="Screenshot of the wizard page with the default method selected for content extraction." border="true" lightbox="media/search-get-started-portal-images/extract-your-content-doc-extraction.png":::

1. Select **Next**.

### [**Enhanced extraction**](#tab/document-intelligence)

Your Azure AI multi-service resource provides access to [Azure AI Document Intelligence](/azure/ai-services/document-intelligence/overview), which calls the [Document Layout skill](cognitive-search-skill-document-intelligence-layout.md) to recognize document structure and extract text and images relationally. It does so by attaching location metadata, such as page numbers and bounding polygons, to each image. The Document Layout skill also breaks text content into smaller, more manageable chunks.

To use the Document Layout skill:

1. On the **Content extraction** page, select **AI Document Intelligence**.

1. Specify your Azure subscription and multi-service resource.

1. For the authentication type, select **System assigned identity**.

1. Select the checkbox that acknowledges the billing effects of using these resources.

   :::image type="content" source="media/search-get-started-portal-images/extract-your-content-doc-intelligence.png" alt-text="Screenshot of the wizard page with Azure AI Document Intelligence selected for content extraction." border="true" lightbox="media/search-get-started-portal-images/extract-your-content-doc-intelligence.png":::

1. Select **Next**.

---

## Embed your content

During this step, the wizard uses your chosen [embedding method](#supported-embedding-methods) to generate vector representations of both text and images.

### [**Image verbalization**](#tab/image-verbalization)

The wizard calls one skill to create descriptive text for images (image verbalization) and another skill to create vector embeddings for both text and images.

For image verbalization, the [GenAI Prompt skill](cognitive-search-skill-genai-prompt.md) uses your deployed LLM to analyze each extracted image and produce a natural-language description.

For embeddings, the [Azure OpenAI Embedding skill](cognitive-search-skill-azure-openai-embedding.md), [AML skill](cognitive-search-aml-skill.md), or [Azure AI Vision multimodal embeddings skill](cognitive-search-skill-vision-vectorize.md) uses your deployed embedding model to convert text chunks and verbalized descriptions into high-dimensional vectors. These vectors enable similarity and hybrid retrieval.

To use the skills for image verbalization:

1. On the **Content embedding** page, select **Image Verbalization**.

   :::image type="content" source="media/search-get-started-portal-images/image-verbalization-tile.png" alt-text="Screenshot of the Image Verbalization tile in the wizard." border="true" lightbox="media/search-get-started-portal-images/image-verbalization-tile.png":::

1. On the **Image Verbalization** tab:

   1. For the kind, select your LLM provider: **Azure OpenAI** or **AI Foundry Hub catalog models**.

   1. Specify your Azure subscription, resource, and LLM deployment.

   1. For the authentication type, select **System assigned identity**.

   1. Select the checkbox that acknowledges the billing effects of using these resources.

      :::image type="content" source="media/search-get-started-portal-images/image-verbalization-tab.png" alt-text="Screenshot of the wizard page for verbalizing images." border="true" lightbox="media/search-get-started-portal-images/image-verbalization-tab.png":::

1. On the **Text Vectorization** tab:

   1. For the kind, select your model provider: **Azure OpenAI**, **AI Foundry Hub catalog models**, or **AI Vision vectorization**.

   1. Specify your Azure subscription, resource, and embedding model deployment.

   1. For the authentication type, select **System assigned identity**.

   1. Select the checkbox that acknowledges the billing effects of using these resources.

      :::image type="content" source="media/search-get-started-portal-images/text-vectorization-tab.png" alt-text="Screenshot of the wizard page for vectorizing text and images." border="true" lightbox="media/search-get-started-portal-images/text-vectorization-tab.png":::

1. Select **Next**.

### [**Multimodal embeddings**](#tab/multimodal-embeddings)

If the raw content of your data includes text, the wizard calls the [AML skill](cognitive-search-aml-skill.md) or [Azure AI Vision multimodal embeddings skill](cognitive-search-skill-vision-vectorize.md) to vectorize it. The same embedding skill is used to generate vector representations of images.

The wizard also calls the [Shaper skill](cognitive-search-skill-shaper.md) to enrich the output with metadata, such as page numbers. This metadata is useful for associating vectorized content with its original context in the document.

To use the skills for multimodal embeddings:

1. On the **Content embedding** page, select **Multimodal Embedding**.

   :::image type="content" source="media/search-get-started-portal-images/multimodal-embedding-tile.png" alt-text="Screenshot of the Multimodal Embedding tile in the wizard." border="true" lightbox="media/search-get-started-portal-images/multimodal-embedding-tile.png":::

1. For the kind, select your model provider: **AI Foundry Hub catalog models** or **AI Vision vectorization**.

   <!-- If it's unavailable, make sure your Azure AI Search service and Azure AI multi-service account are both in a region that [supports the AI Vision multimodal APIs](/azure/ai-services/computer-vision/how-to/image-retrieval). -->

1. Specify your Azure subscription, resource, and embedding model deployment.

1. Select the checkbox that acknowledges the billing effects of using this resource.

   :::image type="content" source="media/search-get-started-portal-images/multimodal-embeddings-options.png" alt-text="Screenshot of the wizard page for vectorizing text and images." border="true" lightbox="media/search-get-started-portal-images/multimodal-embeddings-options.png":::

1. Select **Next**.

---

## Store the extracted images

The next step is to send images extracted from your documents to Azure Storage. In Azure AI Search, this secondary storage is known as a [knowledge store](knowledge-store-concept-intro.md).

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
| content_id | Text and image vectors | String field. Document key for the index. | Retrievable, sortable, and searchable. |
| document_title | Text and image vectors | String field. Human-readable document title. | Retrievable and searchable. |
| text_document_id | Text vectors | String field. Identifies the parent document from which the text chunk originates. | Retrievable and filterable. |
| image_document_id | Image vectors | String field. Identifies the parent document from which the image originates. | Retrievable and filterable. |
| content_text | Text vectors | String field. Human-readable version of the text chunk. | Retrievable and searchable. |
| content_embedding | Text and image vectors | Collection(Edm.Single). Vector representation of text and images. | Retrievable and searchable. |
| content_path | Text and image vectors | String field. Path to the content in the storage container. | Retrievable and searchable. |
| locationMetadata | Image vectors | Edm.ComplexType. Contains metadata about the image's location in the documents. | Varies by field. |

You can't modify the generated fields or their attributes, but you can add fields if your data source provides them. For example, Azure Blob Storage provides a collection of metadata fields.

To add fields to the index schema:

1. Under **Index fields**, select **Preview and edit**.

1. Select **Add field**.

1. Select a source field from the available fields, enter a field name for the index, and accept (or override) the default data type.

1. If you want to restore the schema to its original version, select **Reset**.

## Schedule indexing

For data sources where the underlying data is volatile, you can [schedule indexing](search-howto-schedule-indexers.md) to capture changes at specific intervals or specific dates and times.

To schedule indexing:

1. On the **Advanced settings** page, under **Schedule indexing**, specify a run schedule for the indexer. We recommend **Once** for this quickstart.

   :::image type="content" source="media/search-get-started-portal-images/run-once.png" alt-text="Screenshot of the wizard page for scheduling indexing." border="true" lightbox="media/search-get-started-portal-images/run-once.png":::

1. Select **Next**.

## Finish the wizard

The final step is to review your configuration and create the necessary objects for multimodal search. If necessary, return to the previous pages in the wizard to adjust your configuration.

To finish the wizard:

1. On the **Review and create** page, specify a prefix for the objects the wizard will create. A common prefix helps you stay organized.

   :::image type="content" source="media/search-get-started-portal-images/review-create.png" alt-text="Screenshot of the wizard page for reviewing and completing the configuration." border="true" lightbox="media/search-get-started-portal-images/review-create.png":::

1. Select **Create**.

When the wizard completes the configuration, it creates the following objects:

+ An indexer that drives the indexing pipeline.

+ A data source connection to Azure Blob Storage.

+ An index with text fields, vector fields, vectorizers, vector profiles, and vector algorithms. During the wizard workflow, you can't modify the default index. Indexes conform to the [2024-05-01-preview REST API](/rest/api/searchservice/indexes/create-or-update?view=rest-searchservice-2024-05-01-preview&preserve-view=true) so that you can use preview features.

+ A skillset with the following skills:

  + The [Document Extraction skill](cognitive-search-skill-document-extraction.md) or [Document Layout skill](cognitive-search-skill-document-intelligence-layout.md) extracts text and images from source documents. The [Text Split skill](cognitive-search-skill-textsplit.md) accompanies the Document Extraction skill for data chunking, while the Document Layout skill has built-in chunking.

  + The [GenAI Prompt skill](cognitive-search-skill-genai-prompt.md) verbalizes images in natural language. If you're using direct multimodal embeddings, this skill is absent.

  + The [Azure OpenAI Embedding skill](cognitive-search-skill-azure-openai-embedding.md), [AML skill](cognitive-search-aml-skill.md), or [Azure AI Vision multimodal embeddings skill](cognitive-search-skill-vision-vectorize.md) is called once for text vectorization and once for image vectorization.

  + The [Shaper skill](cognitive-search-skill-shaper.md) enriches the output with metadata and creates new images with contextual information.

> [!TIP]
> Wizard-created objects have configurable JSON definitions. To view or modify these definitions, select **Search management** from the left pane, where you can view your indexes, indexers, data sources, and skillsets.

## Check results

This quickstart creates a multimodal index that supports [hybrid search](hybrid-search-overview.md) over both text and images. Unless you use direct multimodal embeddings, the index doesn't accept images as query inputs, which requires the [AML skill](cognitive-search-aml-skill.md) or [Azure AI Vision multimodal embeddings skill](cognitive-search-skill-vision-vectorize.md) with an equivalent vectorizer. For more information, see [Query with Search explorer](search-explorer.md).

Hybrid search is a combination of full-text queries and vector queries. When you issue a hybrid query, the search engine computes the semantic similarity between your query and the indexed vectors and ranks the results accordingly. For the index created in this quickstart, the results surface content from the `content_text` field that closely aligns with your query.

To query your multimodal index:

1. Sign in to the [Azure portal](https://portal.azure.com/) and select your Azure AI Search service.

1. From the left pane, select **Search management** > **Indexes**.

1. Select your index.

1. Select **Query options**, and then select **Hide vector values in search results**. This step makes the results more readable.

   :::image type="content" source="media/search-get-started-portal-images/query-options.png" alt-text="Screenshot of the Query Options menu in Search Explorer." border="true" lightbox="media/search-get-started-portal-images/query-options.png":::

1. Enter text for which you want to search. Our example uses `energy`.

1. To run the query, select **Search**.

   :::image type="content" source="media/search-get-started-portal-images/search-button.png" alt-text="Screenshot of the Search button in Search Explorer." border="true" lightbox="media/search-get-started-portal-images/search-button.png":::

   The results should include text and image content related to `energy` in your index. Highlights from relevant passages and image verbalizations appear in `@search.captions`, helping you quickly identify matches to your query.

## Clean up resources

This quickstart uses billable Azure resources. If you no longer need the resources, delete them from your subscription to avoid charges.

## Next steps

This quickstart introduced you to the **Import and vectorize data wizard**, which creates all of the necessary objects for multimodal search. To explore each step in detail, see the following tutorials:

+ [Tutorial: Image verbalization and Document Extraction skill](tutorial-document-extraction-image-verbalization.md)
+ [Tutorial: Image verbalization and Document Layout skill](tutorial-document-layout-image-verbalization.md)
+ [Tutorial: Multimodal embeddings and Document Extraction skill](tutorial-document-extraction-multimodal-embeddings.md)
+ [Tutorial: Multimodal embeddings and Document Layout skill](tutorial-document-layout-multimodal-embeddings.md)
