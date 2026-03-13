---
title: "Quickstart: Vector Search in the Azure Portal"
description: Learn how to use a wizard to automate data chunking and vectorization in a search index.
author: mattwojo
ms.author: mattwoj
ms.service: azure-ai-search
ms.custom:
  - build-2024
  - ignite-2024
ms.topic: quickstart
ms.date: 03/13/2026
---

# Quickstart: Vector search in the Azure portal

In this quickstart, you use the **Import data** wizard in the Azure portal to get started with [integrated vectorization](vector-search-integrated-vectorization.md). The wizard chunks your content and calls an embedding model to vectorize the chunks at indexing and query time.

This quickstart uses text-based PDFs and simple images from the [azure-search-sample-data](https://github.com/Azure-Samples/azure-search-sample-data/tree/main/sustainable-ai-pdf) repo. However, you can use different files and still complete this quickstart.

> [!TIP]
> Have image-rich documents? See [Quickstart: Multimodal search in the Azure portal](search-get-started-portal-image-search.md) to extract, store, and search images alongside text.

## Prerequisites

+ An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

+ An [Azure AI Search service](search-create-service-portal.md). We recommend the Basic tier or higher for managed identity support and higher limits.

+ A [supported data source](#supported-data-sources).

+ A [supported embedding model](#supported-embedding-models).

+ Familiarity with the wizard. See [Import data wizard in the Azure portal](search-import-data-portal.md).

### Supported data sources

The wizard [supports several Azure data sources](search-import-data-portal.md#data-sources). However, this quickstart only covers the data sources that work with whole files, which are described in the following table.

| Data source | Description |
|--|--|
| [Azure Blob Storage](/azure/storage/common/storage-account-create) | This data source works with blobs and tables. You must use a standard performance (general-purpose v2) account. Access tiers can be hot, cool, or cold. |
| [Azure Data Lake Storage (ADLS) Gen2](/azure/storage/blobs/create-data-lake-storage-account) | This is an Azure Storage account with a hierarchical namespace enabled. To confirm that you have Data Lake Storage, check the **Properties** tab on the **Overview** page. |
| [Microsoft OneLake](search-how-to-index-onelake-files.md) | This data source connects to OneLake files and shortcuts. |

### Supported embedding models

The portal supports the following embedding models for integrated vectorization. Deployment instructions are provided in a [later section](#prepare-embedding-model).

| Provider | Supported models |
|--|--|
| [Azure AI multi-service account](https://portal.azure.com/#create/Microsoft.CognitiveServicesAllInOne) <sup>1</sup> | For text and images: [Azure Vision multimodal](/azure/ai-services/computer-vision/how-to/image-retrieval) |
| [Microsoft Foundry hub-based project](/azure/ai-foundry/how-to/hub-create-projects) | For text:<ul><li>text-embedding-ada-002</li><li>text-embedding-3-small</li><li>text-embedding-3-large</li></ul>For text and images:<ul><li>Cohere-embed-v3-english <sup>2</sup></li><li>Cohere-embed-v3-multilingual <sup>2</sup></li></ul> |
| [Microsoft Foundry project](/azure/ai-foundry/how-to/create-projects) | For text:<ul><li>text-embedding-ada-002</li><li>text-embedding-3-small</li><li>text-embedding-3-large</li></ul> |
| [Azure OpenAI resource](/azure/ai-services/openai/how-to/create-resource) <sup>3, 4</sup> | For text:<ul><li>text-embedding-ada-002</li><li>text-embedding-3-small</li><li>text-embedding-3-large</li></ul> |

<sup>1</sup> For billing purposes, you must [attach your multi-service account](cognitive-search-attach-cognitive-services.md) to your Azure AI Search skillset. The wizard requires your search service and multi-service account to be in the [same supported region for the Azure Vision multimodal embeddings skill](cognitive-search-skill-vision-vectorize.md#supported-regions).

<sup>2</sup> The wizard only supports serverless API deployments for this model. You can use [use the Azure CLI](vector-search-integrated-vectorization-ai-studio.md#deploy-an-embedding-model-as-a-serverless-deployment) to provision the serverless deployment.

<sup>3</sup> The endpoint of your Azure OpenAI resource must have a [custom subdomain](/azure/ai-services/cognitive-services-custom-subdomains), such as `https://my-unique-name.openai.azure.com`. If you created your resource in the Azure portal, this subdomain was automatically generated during resource setup.

<sup>4</sup> Azure OpenAI resources (with access to embedding models) that were created in the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs) aren't supported. You must create an Azure OpenAI resource in the Azure portal.

### Public endpoint requirements

All of the preceding resources must have public access enabled so that the wizard can access them. Otherwise, the wizard fails. After the wizard runs, you can enable firewalls and private endpoints on the integration components for security. For more information, see [Secure connections in the import wizard](search-import-data-portal.md#secure-connections).

If private endpoints are already present and you can't disable them, the alternative option is to run the respective end-to-end flow from a script or program on a virtual machine. The virtual machine must be on the same virtual network as the private endpoint. Here's a [Python code sample](https://github.com/Azure/azure-search-vector-samples/tree/main/demo-python/code/integrated-vectorization) for integrated vectorization. The same [GitHub repo](https://github.com/Azure/azure-search-vector-samples/tree/main) has samples in other programming languages.

## Configure access

Before you begin, make sure you have permissions to access content and operations. This quickstart uses Microsoft Entra ID for authentication and role-based access for authorization. You must be an **Owner** or **User Access Administrator** to assign roles. If roles aren't feasible, use [key-based authentication](search-security-api-keys.md) instead.

Configure the [required roles](#required-roles) and [conditional roles](#conditional-roles) identified in this section.

### Required roles

Azure AI Search provides the vector search pipeline. Configure access for yourself and your search service to read data, run the pipeline, and interact with other Azure resources.

On your Azure AI Search service:

1. [Enable role-based access](search-security-enable-roles.md).

1. [Configure a system-assigned managed identity](search-how-to-managed-identities.md#create-a-system-managed-identity).

1. [Assign the following roles](search-security-rbac.md) to yourself.

   + **Search Service Contributor**

   + **Search Index Data Contributor**

   + **Search Index Data Reader**

### Conditional roles

The following tabs cover all wizard-compatible resources for vector search. Select only the tabs that apply to your chosen [data source](#supported-data-sources) and [embedding model](#supported-embedding-models).

### [**Azure Storage**](#tab/storage-access)

Azure Blob Storage and Azure Data Lake Storage Gen2 require your search service to have read access to storage containers.

On your Azure Storage account:

+ Assign **Storage Blob Data Reader** to the managed identity of your search service.

### [**Microsoft OneLake**](#tab/onelake-access)

Microsoft OneLake requires your search service to have contributor access to the workspace.

On your OneLake workspace:

1. In the upper-right corner, select **Manage access**.

1. Select **Add people or groups**.

1. Enter the name of your search service. For example, if the URL is `https://my-demo-service.search.windows.net`, the service name is `my-demo-service`.

1. Select a role. The default is **Viewer**, but you need **Contributor** to pull data into a search index.

### [**Azure OpenAI**](#tab/aoai-access)

Azure OpenAI provides embedding models for text vectorization. Your search service requires access to call the [Azure OpenAI Embedding skill](cognitive-search-skill-azure-openai-embedding.md).

On your Azure OpenAI resource:

+ Assign **Cognitive Services OpenAI User** to the managed identity of your search service.

### [**Microsoft Foundry**](#tab/foundry-access)

> [!NOTE]
> If you're using a hub-based project, skip this step. Hub-based projects support API keys instead of managed identities for authentication.

The Microsoft Foundry model catalog provides embedding models for text vectorization. Your search service requires access to call the [AML skill](cognitive-search-aml-skill.md).

On the parent resource of your Microsoft Foundry project:

+ Assign **Azure AI Project Manager** to the managed identity of your search service.

### [**Azure AI multi-service**](#tab/vision-access)

An Azure AI multi-service account provides access to multiple Azure services, including Azure Vision for multimodal embeddings. Your search service requires access to call the [Azure Vision multimodal embeddings skill](cognitive-search-skill-vision-vectorize.md).

On your multi-service account:

+ Assign **Cognitive Services User** to the managed identity of your search service.

---

## Prepare sample data

In this section, you prepare sample data for your chosen [data source](#supported-data-sources).

### [Azure Blob Storage](#tab/blob-storage)

1. Sign in to the [Azure portal](https://portal.azure.com/) and select your Azure Storage account.

1. From the left pane, select **Data storage** > **Containers**.

1. Create a container, and then upload the [health-plan PDF documents](https://github.com/Azure-Samples/azure-search-sample-data/tree/main/health-plan) used for this quickstart.

1. (Optional) Synchronize deletions in your container with deletions in the search index. To configure your indexer for deletion detection:

   1. [Enable soft delete](/azure/storage/blobs/soft-delete-blob-enable?tabs=azure-portal#enable-blob-soft-delete-hierarchical-namespace) on your storage account. If you're using [native soft delete](search-how-to-index-azure-blob-changed-deleted.md#native-blob-soft-delete), the next step isn't required.

   1. [Add custom metadata](search-how-to-index-azure-blob-changed-deleted.md#soft-delete-strategy-using-custom-metadata) that an indexer can scan to determine which blobs are marked for deletion. Give your custom property a descriptive name. For example, name the property "IsDeleted" and set it to false. Repeat this step for every blob in the container. When you want to delete the blob, change the property to true. For more information, see [Change and delete detection when indexing from Azure Storage](search-how-to-index-azure-blob-changed-deleted.md).

### [ADLS Gen2](#tab/adls-gen2)

1. Sign in to the [Azure portal](https://portal.azure.com/) and select your Azure Storage account.

1. From the left pane, select **Data storage** > **Containers**.

1. Create a container, and then upload the [health-plan PDF documents](https://github.com/Azure-Samples/azure-search-sample-data/tree/main/health-plan) used for this quickstart.

1. (Optional) Synchronize deletions in your container with deletions in the search index. To configure your indexer for deletion detection:

   1. [Enable soft delete](/azure/storage/blobs/soft-delete-blob-enable?tabs=azure-portal#enable-blob-soft-delete-hierarchical-namespace) on your storage account.  If you're using [native soft delete](search-how-to-index-azure-blob-changed-deleted.md#native-blob-soft-delete), the next step isn't required.

   1. [Add custom metadata](search-how-to-index-azure-blob-changed-deleted.md#soft-delete-strategy-using-custom-metadata) that an indexer can scan to determine which blobs are marked for deletion. Give your custom property a descriptive name. For example, name the property "IsDeleted" and set it to false. Repeat this step for every blob in the container. When you want to delete the blob, change the property to true. For more information, see [Change and delete detection when indexing from Azure Storage](search-how-to-index-azure-blob-changed-deleted.md).

### [Microsoft OneLake](#tab/onelake)

1. Sign in to [Power BI](https://powerbi.com/) and [create a workspace](/fabric/data-engineering/tutorial-lakehouse-get-started).

1. From the left pane, select your new workspace.

1. To create a lakehouse and upload the sample data:

   1. In the upper-left corner, select **New item**.

   1. Select the **Lakehouse** tile.

   1. Enter a name for your lakehouse, and then select **Create**.

   1. On the **Home** tab of your lakehouse, select **Upload files**, and then upload the [health-plan PDF documents](https://github.com/Azure-Samples/azure-search-sample-data/tree/main/health-plan) used for this quickstart.

1. At the top of your browser, copy the lakehouse URL, which has the following format: `https://msit.powerbi.com/groups/00000000-0000-0000-0000-000000000000/lakehouses/11111111-1111-1111-1111-111111111111`. Remove any query parameters, such as `?experience=power-bi`. You specify this URL later in [Connect to your data](#connect-to-your-data).

---

<a name="connect-to-azure-openai"></a>
<!-- This bookmark is used in an FWLINK. Do not change. -->

## Prepare embedding model

> [!NOTE]
> If you're using Azure Vision, skip this step. The multimodal embeddings are built into your multi-service account and don't require model deployment.

The wizard supports several embedding models from Azure OpenAI and the Microsoft Foundry model catalog. To deploy the models required for your chosen [embedding model](#supported-embedding-models), see [Deploy Microsoft Foundry Models in the Foundry portal](/azure/ai-foundry/how-to/deploy-models-openai).

## Start the wizard

1. Sign in to the [Azure portal](https://portal.azure.com/) and select your Azure AI Search service.

1. On the **Overview** page, select **Import data**.

   :::image type="content" source="media/search-import-data-portal/import-data-button.png" alt-text="Screenshot of the command to open the wizard for importing and vectorizing data.":::

1. Select your data source: **Azure Blob Storage**, **ADLS Gen2**, or **OneLake**.

1. Select **RAG**.

   :::image type="content" source="media/search-get-started-portal-import-vectors/wizard-scenarios-rag.png" alt-text="Screenshot of the RAG tile in the wizard." border="true" lightbox="media/search-get-started-portal-import-vectors/wizard-scenarios-rag.png":::

## Run the wizard

The wizard walks you through several configuration steps. This section covers each step in sequence.

### Connect to your data

In this step, you connect Azure AI Search to your chosen [data source](#supported-data-sources) for content ingestion and indexing.

### [Azure Blob Storage](#tab/blob-storage)

1. On the **Connect to your data** page, select your Azure subscription.

1. Select the storage account and container that provide the sample data.

1. If you enabled soft delete and added custom metadata in [Prepare sample data](#prepare-sample-data), select the **Enable deletion tracking** checkbox.

   + On subsequent indexing runs, the search index is updated to remove any search documents based on soft-deleted blobs on Azure Storage.

   + Blobs support either **Native blob soft delete** or **Soft delete using custom metadata**.

   + If you configured your blobs for soft delete, provide the metadata property name-value pair. We recommend **IsDeleted**. If **IsDeleted** is set to **true** on a blob, the indexer drops the corresponding search document on the next indexer run.

   + The wizard doesn't check Azure Storage for valid settings or throw an error if the requirements aren't met. Instead, deletion detection doesn't work, and your search index is likely to collect orphaned documents over time.

1. Select the **Authenticate using managed identity** checkbox. Leave the identity type as **System-assigned**.

   :::image type="content" source="media/search-get-started-portal-import-vectors/data-source-blob.png" alt-text="Screenshot of the data source page with deletion detection options." lightbox="media/search-get-started-portal-import-vectors/data-source-blob.png":::

1. Select **Next**.

### [ADLS Gen2](#tab/adls-gen2)

1. On the **Connect to your data** page, select your Azure subscription.

1. Select the storage account and container that provide the sample data.

1. If you enabled soft delete and added custom metadata in [Prepare sample data](#prepare-sample-data), select the **Enable deletion tracking** checkbox.

   + On subsequent indexing runs, the search index is updated to remove any search documents based on soft-deleted blobs on Azure Storage.

   + ADLS Gen2 indexers on Azure AI Search support **Soft delete using custom metadata** only.

   + Provide the metadata property you created for deletion detection. We recommend **IsDeleted**. If **IsDeleted** is set to **true** on a blob, the indexer drops the corresponding search document on the next indexer run.

      The wizard doesn't check Azure Storage for valid settings or throw an error if the requirements aren't met. Instead, deletion detection doesn't work, and your search index is likely to collect orphaned documents over time.

1. Select the **Authenticate using managed identity** checkbox. Leave the identity type as **System-assigned**.

   :::image type="content" source="media/search-get-started-portal-import-vectors/data-source-data-lake-storage.png" alt-text="Screenshot of the data source page with deletion detection options." lightbox="media/search-get-started-portal-import-vectors/data-source-data-lake-storage.png":::

1. Select **Next**.

### [Microsoft OneLake](#tab/onelake)

1. On the **Connect to your data** page, select **Lakehouse URL** for the connection type.

1. Paste the URL you copied in [Prepare sample data](#prepare-sample-data).

1. For the type of managed identity, select **System-assigned**.

1. Select **Next**.

---

### Vectorize your text

During this step, the wizard uses your chosen [embedding model](#supported-embedding-models) to vectorize chunked data. Chunking is built in and nonconfigurable. The effective settings are:

```json
"textSplitMode": "pages",
"maximumPageLength": 2000,
"pageOverlapLength": 500,
"maximumPagesToTake": 0, #unlimited
"unit": "characters"
```

### [Azure OpenAI](#tab/aoai)

1. On the **Vectorize your text** page, select **Azure OpenAI** for the kind.

1. Select your Azure subscription.

1. Select your Azure OpenAI resource, and then select the model you deployed in [Prepare embedding model](#prepare-embedding-model).

1. For the authentication type, select **System assigned identity**.

1. Select the checkbox that acknowledges the billing effects of using these resources.

   :::image type="content" source="media/search-get-started-portal-import-vectors/vectorize-text-aoai.png" alt-text="Screenshot of the Vectorize your text page with Azure OpenAI in the wizard." lightbox="media/search-get-started-portal-import-vectors/vectorize-text-aoai.png":::

1. Select **Next**.

### [Microsoft Foundry](#tab/foundry)

1. On the **Vectorize your text** page, select **Microsoft Foundry** for the kind.

1. Select your Azure subscription.

1. Select your project, and then select the model you deployed in [Prepare embedding model](#prepare-embedding-model).

1. For the authentication type, select **System assigned identity** if you're not using a hub-based project. Otherwise, leave it as **API key**.

1. Select the checkbox that acknowledges the billing effects of using these resources.

   :::image type="content" source="media/search-get-started-portal-import-vectors/vectorize-text-foundry.png" alt-text="Screenshot of the Vectorize your text page with the Microsoft Foundry model catalog in the wizard." lightbox="media/search-get-started-portal-import-vectors/vectorize-text-foundry.png":::

1. Select **Next**.

### [Azure Vision](#tab/vision)

1. On the **Vectorize your text** page, select **Azure Vision in Foundry Tools** for the kind.

1. Select your Azure subscription and multi-service account.

1. For the authentication type, select **System assigned identity**.

1. Select the checkbox that acknowledges the billing effects of using these resources.

   :::image type="content" source="media/search-get-started-portal-import-vectors/vectorize-text-vision.png" alt-text="Screenshot of the Vectorize your text page with Azure Vision in the wizard." lightbox="media/search-get-started-portal-import-vectors/vectorize-text-vision.png":::

1. Select **Next**.

---

### Vectorize and enrich your images

The health-plan PDFs include a corporate logo, but otherwise, there are no images. You can skip this step if you're using the sample documents.

However, if your content includes useful images, you can apply AI in one or both of the following ways:

+ Use a supported image embedding model from the Microsoft Foundry model catalog or the Azure Vision multimodal embeddings API (via a multi-service account) to vectorize images.

+ Use optical character recognition (OCR) to extract text from images. This option invokes the [OCR skill](cognitive-search-skill-ocr.md).

### [Vectorize images](#tab/vectorize-images)

1. On the **Vectorize and enrich your images** page, select the **Vectorize images** checkbox.

1. For the kind, select your model provider: **Microsoft Foundry** or **Azure Vision in Foundry Tools**.

1. Select your Azure subscription, resource, and embedding model deployment (if applicable).

1. For the authentication type, select **System assigned identity** if you're not using a hub-based project. Otherwise, leave it as **API key**.

1. Select the checkbox that acknowledges the billing effects of using these resources.

   :::image type="content" source="media/search-get-started-portal-import-vectors/vectorize-images.png" alt-text="Screenshot of the Vectorize and enrich your images page in the wizard." lightbox="media/search-get-started-portal-import-vectors/vectorize-images.png":::

1. Select **Next**.

### [Extract text from images](#tab/extract-text-images)

1. On the **Vectorize and enrich your images** page, select the **Extract text from images** checkbox.

1. Select your Azure subscription and multi-service resource.

1. For the authentication type, select **System assigned identity**.

1. Select the checkbox that acknowledges the billing effects of using these resources.

   :::image type="content" source="media/search-get-started-portal-import-vectors/extract-text-images.png" alt-text="Screenshot of the Extract text from images page in the wizard." lightbox="media/search-get-started-portal-import-vectors/extract-text-images.png":::

1. Select **Next**.

---

### Add semantic ranking

On the **Advanced settings** page, you can optionally add [semantic ranking](semantic-search-overview.md) to rerank results at the end of query execution. Reranking promotes the most semantically relevant matches to the top.

### Map new fields

On the **Advanced settings** page, you can optionally add new fields, assuming the data source provides metadata or fields that aren't picked up on the first pass. By default, the wizard generates the fields described in the following table.

| Field | Applies to | Description |
|-------|------------|-------------|
| chunk_id | Text and image vectors | Generated string field. Searchable, retrievable, and sortable. This is the document key for the index. |
| parent_id | Text vectors | Generated string field. Retrievable and filterable. Identifies the parent document from which the chunk originates. |
| chunk | Text and image vectors | String field. Human readable version of the data chunk. Searchable and retrievable, but not filterable, facetable, or sortable. |
| title | Text and image vectors | String field. Human readable document title or page title or page number. Searchable and retrievable, but not filterable, facetable, or sortable. |
| text_vector | Text vectors | Collection(Edm.single). Vector representation of the chunk. Searchable and retrievable, but not filterable, facetable, or sortable.|

You can't modify the generated fields or their attributes, but you can add new fields if your data source provides them. For example, Azure Blob Storage provides a collection of metadata fields.

To add fields to the index schema:

1. On the **Advanced settings** page, under **Index fields**, select **Preview and edit**.

1. Select **Add field**.

1. Select a source field from the available fields, enter a field name for the index, and accept (or override) the default data type.

1. If you want to restore the schema to its original version, select **Reset**.

Key points about this step:

+ The index schema provides vector and nonvector fields for chunked data.

+ Document parsing mode creates chunks (one search document per chunk).

### Schedule indexing

For data sources where the underlying data is volatile, you can [schedule indexing](search-howto-schedule-indexers.md) to capture changes at specific intervals or specific dates and times.

To schedule indexing:

1. On the **Advanced settings** page, under **Schedule indexing**, specify a run schedule for the indexer. We recommend **Once** for this quickstart.

   :::image type="content" source="media/search-get-started-portal-images/run-once.png" alt-text="Screenshot of the wizard page for scheduling indexing." border="true" lightbox="media/search-get-started-portal-images/run-once.png":::

1. Select **Next**.

## Finish the wizard

The final step is to review your configuration and create the necessary objects for vector search. If necessary, return to the previous pages in the wizard to adjust your configuration.

To finish the wizard:

1. On the **Review and create** page, specify a prefix for the objects that the wizard creates. A common prefix helps you stay organized.

   :::image type="content" source="media/search-get-started-portal-import-vectors/review-create.png" alt-text="Screenshot of the wizard page for reviewing and completing the configuration." border="true" lightbox="media/search-get-started-portal-import-vectors/review-create.png":::

1. Select **Create**.

### Wizard-created objects

When the wizard completes the configuration, it creates the following objects:

| Object | Description |
|--|--|
| Data source | Represents a connection to your chosen data source. |
| Index | Contains vector fields, vectorizers, vector profiles, and vector algorithms. You can't modify the default index during the wizard workflow. Indexes conform to the [latest preview REST API](/rest/api/searchservice/indexes/create-or-update?view=rest-searchservice-2025-11-01-preview&preserve-view=true) so that you can use preview features. |
| Skillset | Contains the following skills and configuration:<br><ul><li>The [Text Split skill](cognitive-search-skill-textsplit.md) for chunking.</li><li>The [Azure OpenAI Embedding skill](cognitive-search-skill-azure-openai-embedding.md), [AML skill](cognitive-search-aml-skill.md), or [Azure Vision multimodal embeddings skill](cognitive-search-skill-vision-vectorize.md) for vectorization.</li><li>The [index projections](index-projections-concept-intro.md) configuration, which maps data from one document in the data source to its corresponding chunks in a "child" index.</li></ul> |
| Indexer | Drives the indexing pipeline, with field mappings and output field mappings (if applicable). |

> [!TIP]
> Wizard-created objects have configurable JSON definitions. To view or modify these definitions, select **Search management** from the left pane, where you can view your indexes, indexers, data sources, and skillsets.

## Check results

Search Explorer accepts text strings as input and then vectorizes the text for vector query execution.

To query your vector index:

1. In the Azure portal, go to **Search Management** > **Indexes**, and then select your index.

1. Select **Query options**, and then select **Hide vector values in search results**. This step makes the results more readable.

   :::image type="content" source="media/search-get-started-portal-import-vectors/query-options.png" alt-text="Screenshot of the button for query options." lightbox="media/search-get-started-portal-import-vectors/query-options.png":::

1. From the **View** menu, select **JSON view** so you can enter text for your vector query in the `text` vector query parameter.

   :::image type="content" source="media/search-get-started-portal-import-vectors/select-json-view.png" alt-text="Screenshot of the menu command for opening the JSON view." lightbox="media/search-get-started-portal-import-vectors/select-json-view.png":::

   The default query is an empty search (`"*"`) but includes parameters for returning the number matches. It's a hybrid query that runs text and vector queries in parallel. It also includes semantic ranking and specifies which fields to return in the results through the `select` statement.

   ```json
    {
      "search": "*",
      "count": true,
      "vectorQueries": [
        {
          "kind": "text",
          "text": "*",
          "fields": "text_vector,image_vector"
        }
      ],
      "queryType": "semantic",
      "semanticConfiguration": "my-demo-semantic-configuration",
      "captions": "extractive",
      "answers": "extractive|count-3",
      "queryLanguage": "en-us",
      "select": "chunk_id,text_parent_id,chunk,title,image_parent_id"
    }
   ```

1. Replace both asterisk (`*`) placeholders with a question related to health plans, such as `Which plan has the lowest deductible?`.

   ```json
    {
      "search": "Which plan has the lowest deductible?",
      "count": true,
      "vectorQueries": [
        {
          "kind": "text",
          "text": "Which plan has the lowest deductible?",
          "fields": "text_vector,image_vector"
        }
      ],
      "queryType": "semantic",
      "semanticConfiguration": "my-demo-semantic-configuration",
      "captions": "extractive",
      "answers": "extractive|count-3",
      "queryLanguage": "en-us",
      "select": "chunk_id,text_parent_id,chunk,title"
    }
   ```

1. To run the query, select **Search**.

   :::image type="content" source="media/search-get-started-portal-import-vectors/search-results.png" alt-text="Screenshot of search results." lightbox="media/search-get-started-portal-import-vectors/search-results.png":::

   Each document is a chunk of the original PDF. The `title` field shows which PDF the chunk comes from. Each `chunk` is long. You can copy and paste one into a text editor to read the entire value.

1. To see all of the chunks from a specific document, add a filter for the `title_parent_id` field for a specific PDF. You can check the **Fields** tab of your index to confirm the field is filterable.

   ```json
   {
      "select": "chunk_id,text_parent_id,chunk,title",
      "filter": "text_parent_id eq 'aHR0cHM6Ly9oZWlkaXN0c3RvcmFnZWRlbW9lYXN0dXMuYmxvYi5jb3JlLndpbmRvd3MubmV0L2hlYWx0aC1wbGFuLXBkZnMvTm9ydGh3aW5kX1N0YW5kYXJkX0JlbmVmaXRzX0RldGFpbHMucGRm0'",
      "count": true,
      "vectorQueries": [
          {
             "kind": "text",
             "text": "*",
             "k": 5,
             "fields": "text_vector"
          }
       ]
   }
   ```

## Clean up resources

[!INCLUDE [clean up resources (paid)](includes/resource-cleanup-paid.md)]

## Next step

This quickstart introduced you to the **Import data** wizard, which creates all of the necessary objects for integrated vectorization. To explore each step in detail, see [Set up integrated vectorization in Azure AI Search](search-how-to-integrated-vectorization.md).
