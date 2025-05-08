---
title: "Quickstart: Vector Search in the Azure Portal"
titleSuffix: Azure AI Search
description: Learn how to use a wizard to automate data chunking and vectorization in a search index.
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.custom:
  - build-2024
  - ignite-2024
ms.topic: quickstart
ms.date: 05/08/2025
---

# Quickstart: Vectorize text in the Azure portal

In this quickstart, you use the **Quickstart wizard** in the Azure portal to get started with [integrated vectorization](vector-search-integrated-vectorization.md). The wizard chunks your content and calls an embedding model to vectorize content during indexing and for queries.

The sample data for this quickstart consists of text-based PDFs, but you can also use images and follow this quickstart to vectorize them.

## Prerequisites

+ An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/free/?WT.mc_id=A261C142F).

+ An [Azure AI Search service](search-create-service-portal.md). We recommend the Basic tier or higher.

+ A [supported data source](#supported-data-sources) with the sample [health-plan PDF documents](https://github.com/Azure-Samples/azure-search-sample-data/tree/main/health-plan) sample documents.

+ A [supported embedding model](#supported-embedding-models).

+ Familiarity with the wizard. See [Import data wizards in the Azure portal](search-import-data-portal.md).

### Supported data sources

The **Quickstart wizard** [supports a wide range of Azure data sources](search-import-data-portal.md#supported-data-sources-and-scenarios). However, this quickstart only covers the data sources that work with whole files, which are described in the following table.

| Supported data source | Description |
|--|--|
| [Azure Blob Storage](search-howto-indexing-azure-blob-storage.md) | This data source works with blobs and tables. You must use a standard performance (general-purpose v2) account. Access tiers can be hot, cool, or cold. |
| [Azure Data Lake Storage (ADLS) Gen2](/azure/storage/blobs/create-data-lake-storage-account) | This is an Azure Storage account with a hierarchical namespace enabled. To confirm that you have Data Lake Storage, check the **Properties** tab on the **Overview** page.<br><br> :::image type="content" source="media/search-get-started-portal-import-vectors/data-lake-storage.png" alt-text="Screenshot of an Azure Data Lake Storage account in the Azure portal." border="true" lightbox="media/search-get-started-portal-import-vectors/data-lake-storage.png"::: |
| [OneLake](search-how-to-index-onelake-files.md) | This data source is currently in preview. For information about limitations and supported shortcuts, see [OneLake indexing](search-how-to-index-onelake-files.md). |

### Supported embedding models

For integrated vectorization, you must use one of the following embedding models on an Azure AI platform in the [same region as Azure AI Search](search-create-service-portal.md#regions-with-the-most-overlap). Deployment instructions are provided in a [later section](#prepare-embedding-models).

| Provider | Supported models |
|--|--|
| [Azure OpenAI Service](/azure/ai-services/openai/how-to/create-resource) <sup>1, 2</sup> | text-embedding-ada-002<br>text-embedding-3-small<br>text-embedding-3-large |
| [Azure AI services multi-service resource](/azure/ai-services/multi-service-resource#azure-ai-services-resource-for-azure-ai-search-skills) <sup>3</sup> | For text and images: [Azure AI Vision multimodal](/azure/ai-services/computer-vision/how-to/image-retrieval) <sup>4</sup></li> |
| [Azure AI Foundry model catalog](/azure/ai-foundry/what-is-azure-ai-foundry) | For text:<br>Cohere-embed-v3-english<br>Cohere-embed-v3-multilingual<br><br>For images:<br>Facebook-DinoV2-Image-Embeddings-ViT-Base<br>Facebook-DinoV2-Image-Embeddings-ViT-Giant |

<sup>1</sup> The endpoint of your Azure OpenAI resource must have a [custom subdomain](/azure/ai-services/cognitive-services-custom-subdomains), such as `https://my-unique-name.openai.azure.com`. If you created your resource in the [Azure portal](https://portal.azure.com/), this subdomain was automatically generated during resource setup.

<sup>2</sup> Azure OpenAI resources (with access to embedding models) that were created in the [Azure AI Foundry portal](https://ai.azure.com/) aren't supported. Only Azure OpenAI resources created in the Azure portal are compatible with the [Azure OpenAI Embedding skill](cognitive-search-skill-azure-openai-embedding.md) integration.

<sup>3</sup> For billing purposes, you must [attach your Azure AI multi-service resource](cognitive-search-attach-cognitive-services.md) to the skillset in your Azure AI Search service. Unless you use a [keyless connection (preview)](cognitive-search-attach-cognitive-services.md#bill-through-a-keyless-connection) to create the skillset, both resources must be in the same region.

<sup>4</sup> The Azure AI Vision multimodal embedding model is available in [select regions](/azure/ai-services/computer-vision/overview-image-analysis#region-availability).

### Public endpoint requirements

For the purposes of this quickstart, all of the preceding resources must have public access enabled so that the Azure portal nodes can access them. Otherwise, the wizard fails. After the wizard runs, you can enable firewalls and private endpoints on the integration components for security. For more information, see [Secure connections in the import wizards](search-import-data-portal.md#secure-connections).

If private endpoints are already present and you can't disable them, the alternative option is to run the respective end-to-end flow from a script or program on a virtual machine. The virtual machine must be on the same virtual network as the private endpoint. Here's a [Python code sample](https://github.com/Azure/azure-search-vector-samples/tree/main/demo-python/code/integrated-vectorization) for integrated vectorization. The same [GitHub repo](https://github.com/Azure/azure-search-vector-samples/tree/main) has samples in other programming languages.

### Role-based access

You can use Microsoft Entra ID with role assignments or key-based authentication with full-access connection strings. For Azure AI Search connections to other resources, we recommend role assignments. This quickstart assumes roles.

Free search services support role-based connections to Azure AI Search. However, they don't support managed identities on outbound connections to Azure Storage or Azure AI Vision. This lack of support requires key-based authentication on connections between free search services and other Azure resources. For more secure connections, use the Basic tier or higher, and then enable roles and configure a managed identity.

To configure the recommended role-based access:

1. On your search service, [enable roles](search-security-enable-roles.md) and [configure a system-assigned managed identity](search-howto-managed-identities-data-sources.md#create-a-system-managed-identity).

1. On your data source platform and embedding model provider, create role assignments that allow your search service to access data and models. See [Prepare sample data](#prepare-sample-data) and [Prepare embedding models](#prepare-embedding-models).

> [!NOTE]
> If you can't progress through the wizard because options aren't available (for example, you can't select a data source or an embedding model), revisit the role assignments. Error messages indicate that models or deployments don't exist, when the real cause is that the search service doesn't have permission to access them.

### Check for space

If you're starting with the free service, you're limited to three indexes, data sources, skillsets, and indexers. Basic limits you to 15. This quickstart creates one of each object, so make sure you have room for extra items before you begin.

## Prepare sample data

This section points you to the content that works for this quickstart. Before you proceed, make sure you completed the prerequisites for [role-based access](#role-based-access).

### [Azure Blob Storage](#tab/sample-data-storage)

1. Sign in to the [Azure portal](https://portal.azure.com/) and select your Azure Storage account.

1. From the left pane, select **Data storage** > **Containers**.

1. Create a new container, and then upload the [health-plan PDF documents](https://github.com/Azure-Samples/azure-search-sample-data/tree/main/health-plan) used for this quickstart.

1. To assign roles:

   1. From the left pane, select **Access Control (IAM)**.

   1. Select **Add** > **Add role assignment**.

   1. Under **Job function roles**, select **[Storage Blob Data Reader](search-howto-managed-identities-data-sources.md#assign-a-role)**, and then select **Next**.

   1. Under **Members**, select **Managed identity**, and then select **Select members**.

   1. Select your subscription and the managed identity of your search service.

1. (Optional) Synchronize deletions in your container with deletions in the search index. To configure your indexer for deletion detection:

   1. [Enable soft delete](/azure/storage/blobs/soft-delete-blob-enable?tabs=azure-portal#enable-blob-soft-delete-hierarchical-namespace) on your storage account. If you're using [native soft delete](search-howto-index-changed-deleted-blobs.md#native-blob-soft-delete), the next step isn't required.

   1. [Add custom metadata](search-howto-index-changed-deleted-blobs.md#soft-delete-strategy-using-custom-metadata) that an indexer can scan to determine which blobs are marked for deletion. Give your custom property a descriptive name. For example, you can name the property "IsDeleted" and set it to false. Repeat this step for every blob in the container. When you want to delete the blob, change the property to true. For more information, see [Change and delete detection when indexing from Azure Storage](search-howto-index-changed-deleted-blobs.md).

### [ADLS Gen2](#tab/sample-data-adlsgen2)

1. Sign in to the [Azure portal](https://portal.azure.com/) and select your Azure Storage account.

1. From the left pane, select **Data storage** > **Containers**.

1. Create a new container, and then upload the [health-plan PDF documents](https://github.com/Azure-Samples/azure-search-sample-data/tree/main/health-plan) used for this quickstart.

1. To assign roles:

   1. From the left pane, select **Access Control (IAM)**.

   1. Select **Add** > **Add role assignment**.

   1. Under **Job function roles**, select **[Storage Blob Data Reader](search-howto-managed-identities-data-sources.md#assign-a-role)**, and then select **Next**.

   1. Under **Members**, select **Managed identity**, and then select **Select members**.

   1. Select your subscription and the managed identity of your search service.

1. (Optional) Synchronize deletions in your container with deletions in the search index. To configure your indexer for deletion detection:

   1. [Enable soft delete](/azure/storage/blobs/soft-delete-blob-enable?tabs=azure-portal#enable-blob-soft-delete-hierarchical-namespace) on your storage account.

   1. [Add custom metadata](search-howto-index-changed-deleted-blobs.md#soft-delete-strategy-using-custom-metadata) that an indexer can scan to determine which blobs are marked for deletion. Give your custom property a descriptive name. For example, you can name the property "IsDeleted" and set it to false. Repeat this step for every blob in the container. When you want to delete the blob, change the property to true. For more information, see [Change and delete detection when indexing from Azure Storage](search-howto-index-changed-deleted-blobs.md).

### [OneLake](#tab/sample-data-onelake)

1. Sign in to [Power BI](https://powerbi.com/) and [create a workspace](/fabric/data-engineering/tutorial-lakehouse-get-started).

1. From the left pane, select your new workspace.

1. To assign roles to your workspace:

   1. In the upper-right corner, select **Manage access**.

   1. Select **Add people or groups**.

   1. Enter the name of your search service. For example, if the URL is `https://my-demo-service.search.windows.net`, the service name is `my-demo-service`.

   1. Select a role. The default is **Viewer**, but you need **Contributor** to pull data into a search index.

1. To create a lakehouse and upload the sample data:

   1. In the upper-left corner, select **New item**.

   1. Select the **Lakehouse** tile.

   1. Enter a name for your lakehouse, and then select **Create**.

   1. On the **Home** tab of your lakehouse, select **Upload files**, and then upload the [health-plan PDF documents](https://github.com/Azure-Samples/azure-search-sample-data/tree/main/health-plan) used for this quickstart.

1. At the top of your browser, copy the lakehouse URL, which has the following format: `https://msit.powerbi.com/groups/00000000-0000-0000-0000-000000000000/lakehouses/11111111-1111-1111-1111-111111111111?experience=power-bi`. You specify this URL later in [Connect to your data](#connect-to-your-data).

---

<a name="connect-to-azure-openai"></a>
<!-- This bookmark is used in an FWLINK. Do not change. -->

## Prepare embedding models

The wizard can use embedding models deployed from Azure OpenAI, Azure AI Vision, or from the model catalog in the [Azure AI Foundry portal](https://ai.azure.com/).

### [Azure OpenAI](#tab/model-aoai)

The wizard supports text-embedding-ada-002, text-embedding-3-large, and text-embedding-3-small. Internally, the wizard calls the [AzureOpenAIEmbedding skill](cognitive-search-skill-azure-openai-embedding.md) to connect to Azure OpenAI.

1. Sign in to the [Azure portal](https://portal.azure.com/) and select your Azure OpenAI resource.

1. To assign roles:

   1. From the left pane, select **Access control (IAM)**.

   1. Select **Add** > **Add role assignment**.

   1. Under **Job function roles**, select **[Cognitive Services OpenAI User](/azure/ai-services/openai/how-to/role-based-access-control#azure-openai-roles)**, and then select **Next**.

   1. Under **Members**, select **Managed identity**, and then select **Select members**.

   1. Select your subscription and the managed identity of your search service.

1. To deploy an embedding model:

   1. Sign in to the [Azure AI Foundry portal](https://ai.azure.com/) and select your Azure OpenAI resource.

   1. From the left pane, select **Model catalog**.

   1. Deploy a [supported embedding model](#supported-embedding-models).

### [Azure AI Vision](#tab/model-ai-vision)

The wizard supports Azure AI Vision image retrieval through multimodal embeddings (version 4.0). Internally, the wizard calls the [multimodal embeddings skill](cognitive-search-skill-vision-vectorize.md) to connect to Azure AI Vision.

1. Sign in to the [Azure portal](https://portal.azure.com/) and select your Azure AI multi-service resource.

1. To assign roles:

   1. From the left pane, select **Access control (IAM)**.

   1. Select **Add** > **Add role assignment**.

   1. Under **Job function roles**, select **Cognitive Services User**, and then select **Next**.

   1. Under **Members**, select **Managed identity**, and then select **Select members**.

   1. Select your subscription and the managed identity of your search service.

The multimodal embeddings are built into your Azure AI multi-service resource, so there's no model deployment step. You should now be able to select the Azure AI Vision vectorizer in the **Quickstart wizard**.

> [!NOTE]
> If you can't select the Azure AI Vision vectorizer, make sure you have an Azure AI Vision resource in a supported region. Also make sure the managed identity of your search service has **Cognitive Services User** permissions.

### [Azure AI Foundry model catalog](#tab/model-catalog)

The wizard supports Azure, Cohere, and Facebook embedding models in the Azure AI Foundry model catalog, but it doesn't currently support the OpenAI CLIP models. Internally, the wizard calls the [AML skill](cognitive-search-aml-skill.md) to connect to the catalog.

For the model catalog, you should have an [Azure AI Foundry project](/azure/ai-foundry/how-to/create-projects) with a [hub that's connected to an Azure OpenAI resource and an Azure AI Search service](/azure/ai-foundry/how-to/create-projects#create-a-project).

1. Sign in to the [Azure portal](https://portal.azure.com/) and select your Azure OpenAI resource.

1. To assign roles:

   1. From the left pane, select **Access control (IAM)**.

   1. Select **Add** > **Add role assignment**.

   1. Under **Job function roles**, select **Cognitive Services User**, and then select **Next**.

   1. Under **Members**, select **Managed identity**, and then select **Select members**.

   1. Select your subscription and the managed identity of your search service.

1. To deploy an embedding model:

   1. Sign in to the [Azure AI Foundry portal](https://ai.azure.com/) and select your project.

   1. From the left pane, select **Model catalog**.

   1. Deploy a [supported embedding model](#supported-embedding-models).

---

## Start the wizard

1. Sign in to the [Azure portal](https://portal.azure.com/) and go to your Azure AI Search service.

1. On the **Overview** page, select **Quickstart wizard**.

   :::image type="content" source="media/search-get-started-portal-import-vectors/command-bar-quickstart-wizard.png" alt-text="Screenshot of the command to open the wizard for importing and vectorizing data.":::

1. Select your data source: **Azure Blob Storage**, **Azure Data Lake Storage Gen2**, or **Fabric OneLake files (Preview)**.

1. Select the **RAG** tile.

## Connect to your data

The next step is to connect to a data source to use for the search index.

### [Azure Blob Storage](#tab/connect-data-storage)

1. On **Connect to your data**, specify your Azure subscription.

1. Choose the storage account and container that provide the sample data.

1. Specify whether you want [deletion detection](search-howto-index-changed-deleted-blobs.md) support. On subsequent indexing runs, the search index is updated to remove any search documents based on soft-deleted blobs on Azure Storage.

   + Blobs support either **Native blob soft delete** or **Soft delete using custom data**.

   + You must have previously [enabled soft delete](/azure/storage/blobs/soft-delete-blob-overview) on Azure Storage and optionally [added custom metadata](search-howto-index-changed-deleted-blobs.md#soft-delete-strategy-using-custom-metadata) that indexing can recognize as a deletion flag. For more information about these steps, see [Prepare sample data](#prepare-sample-data).

   + If you configured your blobs for **soft delete using custom data**, provide the metadata property name-value pair in this step. We recommend **IsDeleted**. If **IsDeleted** is set to **true** on a blob, the indexer drops the corresponding search document on the next indexer run.

   The wizard doesn't check Azure Storage for valid settings or throw an error if the requirements aren't met. Instead, deletion detection doesn't work, and your search index is likely to collect orphaned documents over time.

   :::image type="content" source="media/search-get-started-portal-import-vectors/data-source-blob.png" alt-text="Screenshot of the data source page with deletion detection options.":::

1. Select the **Authenticate using managed identity** checkbox.

   + For the type of managed identity, select **System-assigned**.

   + The identity should have a **Storage Blob Data Reader** role on Azure Storage. For more information about this step, see [Prepare sample data](#prepare-sample-data).

   + Don't skip this step. A connection error occurs during indexing if the wizard can't connect to Azure Storage.

1. Select **Next**.

### [ADLS Gen2](#tab/connect-data-adlsgen2)

1. On **Connect to your data**, specify your Azure subscription.

1. Choose the storage account and container that provide the sample data.

1. Specify whether you want [deletion detection](search-howto-index-changed-deleted-blobs.md) support. On subsequent indexing runs, the search index is updated to remove any search documents based on soft-deleted blobs on Azure Storage.

   + ADLS Gen2 indexers on Azure AI Search support the **Soft delete using custom data** approach only.

   + You must have previously [enabled soft delete](/azure/storage/blobs/soft-delete-blob-overview) on Azure Storage and [added custom metadata](search-howto-index-changed-deleted-blobs.md#soft-delete-strategy-using-custom-metadata) that indexing can recognize as a deletion flag. For more information about these steps, see [Prepare sample data](#prepare-sample-data).
   
   + Provide the metadata property you created for deletion detection. We recommend "IsDeleted". If "IsDeleted" is set to true on a blob, the indexer drops the corresponding search document on the next indexer run.

   The wizard doesn't check Azure Storage for valid settings or throw an error if the requirements aren't met. Instead, deletion detection doesn't work, and your search index is likely to collect orphaned documents over time.

   :::image type="content" source="media/search-get-started-portal-import-vectors/data-source-data-lake-storage.png" alt-text="Screenshot of the data source page with deletion detection options.":::

1. Specify whether you want your search service to [connect to Azure Storage using its managed identity](search-howto-managed-identities-storage.md).

   + You're prompted to choose either a system-managed or user-managed identity. 
   + The identity should have a **Storage Blob Data Reader** role on Azure Storage. 
   + Don't skip this step. A connection error occurs during indexing if the wizard can't connect to Azure Storage.

1. Select **Next**.

### [OneLake](#tab/connect-data-onelake)

Support for OneLake indexing is in preview. For more information about supported shortcuts and limitations, see ([OneLake indexing](search-how-to-index-onelake-files.md)).

1. On **Connect to your data**, select **OneLake**.

1. Specify the type of connection:

   + Lakehouse URL
   + Workspace ID and Lakehouse ID

1. For OneLake, specify the lakehouse URL, or provide the workspace and lakehouse IDs.

1. Specify whether you want your search service to connect to OneLake using its system or user managed identity. You must use a managed identity and roles for search connections to OneLake.

1. Select **Next**.

---

## Vectorize your text

In this step, specify the embedding model for vectorizing chunked data.

Chunking is built in and nonconfigurable. The effective settings are:

```json
"textSplitMode": "pages",
"maximumPageLength": 2000,
"pageOverlapLength": 500,
"maximumPagesToTake": 0, #unlimited
"unit": "characters"
```

1. On the **Vectorize your text** page, choose the source of the embedding model:

   + Azure OpenAI
   + Azure AI Foundry model catalog
   + An existing Azure AI Vision multimodal resource in the same region as Azure AI Search. If there's no [Azure AI services multi-service account](/azure/ai-services/multi-service-resource#azure-ai-services-resource-for-azure-ai-search-skills) in the same region, this option isn't available.

1. Choose the Azure subscription.

1. Make selections according to the resource:

   + For Azure OpenAI, choose an existing deployment of text-embedding-ada-002, text-embedding-3-large, or text-embedding-3-small.

   + For Azure AI Foundry catalog, choose an existing deployment of an Azure or Cohere embedding model.

   + For AI Vision multimodal embeddings, select the account.

   For more information, see [Prepare embedding models](#prepare-embedding-models) earlier in this article.

1. Specify whether you want your search service to authenticate using an API key or managed identity.

   + The identity should have a **Cognitive Services User** role on the Azure AI services multi-services account.

1. Select the checkbox that acknowledges the billing effects of using these resources.

   :::image type="content" source="media/search-get-started-portal-import-vectors/vectorize-text.png" alt-text="Screenshot of the vectorize text page in the wizard.":::

1. Select **Next**.

## Vectorize and enrich your images

The health plan PDFs include a corporate logo, but otherwise there are no images. You can skip this step if you're using the sample documents.

However, if you work with content that includes useful images, you can apply AI in two ways:

+ Use a supported image embedding model from the catalog, or choose the Azure AI Vision multimodal embeddings API to vectorize images.

+ Use optical character recognition (OCR) to recognize text in images. This option invokes the [OCR skill](cognitive-search-skill-ocr.md) to read text from images.

Azure AI Search and your Azure AI resource must be in the same region or configured for [keyless billing connections](cognitive-search-attach-cognitive-services.md).

1. On the **Vectorize your images** page, specify the kind of connection the wizard should make. For image vectorization, the wizard can connect to embedding models in [Azure AI Foundry portal](https://ai.azure.com/) or Azure AI Vision.

1. Specify the subscription.

1. For the Azure AI Foundry model catalog, specify the project and deployment. For more information, see [Prepare embedding models](#prepare-embedding-models) earlier in this article.

1. Optionally, you can crack binary images (for example, scanned document files) and [use OCR](cognitive-search-skill-ocr.md) to recognize text.

1. Select the checkbox that acknowledges the billing effects of using these resources.

   :::image type="content" source="media/search-get-started-portal-import-vectors/vectorize-images.png" alt-text="Screenshot of the vectorize images page in the wizard.":::

1. Select **Next**.

## Add semantic ranking

On the **Advanced settings** page, you can optionally add [semantic ranking](semantic-search-overview.md) to rerank results at the end of query execution. Reranking promotes the most semantically relevant matches to the top.

## Map new fields

Key points about this step:

+ Index schema provides vector and nonvector fields for chunked data. 
+ You can add fields, but you can't delete or modify generated fields.
+ Document parsing mode creates chunks (one search document per chunk).

On the **Advanced settings** page, you can optionally add new fields assuming the data source provides metadata or fields that aren't picked up on the first pass. By default, the wizard generates the following fields with these attributes:

| Field | Applies to | Description |
|-------|------------|-------------|
| chunk_id | Text and image vectors | Generated string field. Searchable, retrievable, sortable. This is the document key for the index. |
| text_parent_id | Text vectors | Generated string field. Retrievable, filterable. Identifies the parent document from which the chunk originates. |
| chunk | Text and image vectors | String field. Human readable version of the data chunk. Searchable and retrievable, but not filterable, facetable, or sortable. |
| title | Text and image vectors | String field. Human readable document title or page title or page number. Searchable and retrievable, but not filterable, facetable, or sortable. |
| text_vector | Text vectors | Collection(Edm.single). Vector representation of the chunk.  Searchable and retrievable, but not filterable, facetable, or sortable.|

You can't modify the generated fields or their attributes, but you can add new fields if your data source provides them. For example, Azure Blob Storage provides a collection of metadata fields.

1. Select **Add new**.

1. Choose a source field from the list of available fields, provide a field name for the index, and accept the default data type or override as needed.

   Metadata fields are searchable, but not retrievable, filterable, facetable, or sortable. 

1. Select **Reset** if you want to restore the schema to its original version.

## Schedule indexing

On the **Advanced settings** page, you can optionally specify a [run schedule](search-howto-schedule-indexers.md) for the indexer.

1. Select **Next** when you're done with the **Advanced settings** page.

## Finish the wizard

1. On the **Review your configuration** page, specify a prefix for the objects that the wizard creates. A common prefix helps you stay organized.

1. Select **Create**.

When the wizard completes the configuration, it creates the following objects:

+ Data source connection.

+ Index with vector fields, vectorizers, vector profiles, and vector algorithms. You can't design or modify the default index during the wizard workflow. Indexes conform to the [2024-05-01-preview REST API](/rest/api/searchservice/indexes/create-or-update?view=rest-searchservice-2024-05-01-preview&preserve-view=true).

+ Skillset with the [Text Split skill](cognitive-search-skill-textsplit.md) for chunking and an embedding skill for vectorization. The embedding skill is either the [AzureOpenAIEmbeddingModel skill](cognitive-search-skill-azure-openai-embedding.md) for Azure OpenAI or the [AML skill](cognitive-search-aml-skill.md) for the Azure AI Foundry model catalog. The skillset also has the [index projections](index-projections-concept-intro.md) configuration that allows data to be mapped from one document in the data source to its corresponding chunks in a "child" index.

+ Indexer with field mappings and output field mappings (if applicable).

## Check results

Search Explorer accepts text strings as input and then vectorizes the text for vector query execution.

1. In the Azure portal, go to **Search Management** > **Indexes**, and then select the index that you created.

1. Select **Query options** and hide vector values in search results. This step makes your search results easier to read.

   :::image type="content" source="media/search-get-started-portal-import-vectors/query-options.png" alt-text="Screenshot of the button for query options.":::

1. On the **View** menu, select **JSON view** so that you can enter text for your vector query in the `text` vector query parameter.

   :::image type="content" source="media/search-get-started-portal-import-vectors/select-json-view.png" alt-text="Screenshot of the menu command for opening the JSON view.":::

   The default query is an empty search (`"*"`), but includes parameters for returning the number matches. It's a hybrid query that runs text and vector queries in parallel. It includes semantic ranking. It specifies which fields to return in the results through the `select` statement.

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

1. Select **Search** to run the query.

   :::image type="content" source="media/search-get-started-portal-import-vectors/search-results.png" alt-text="Screenshot of search results.":::

   Each document is a chunk of the original PDF. The `title` field shows which PDF the chunk comes from. Each `chunk` is quite long. You can copy and paste one into a text editor to read the entire value.

1. To see all of the chunks from a specific document, add a filter for the `title_parent_id` field for a specific PDF. You can check the **Fields** tab of your index to confirm this field is filterable.

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

## Clean up

Azure AI Search is a billable resource. If you no longer need it, delete it from your subscription to avoid charges.

## Next step

This quickstart introduced you to the **Import and vectorize data** wizard that creates all of the necessary objects for integrated vectorization. If you want to explore each step in detail, try an [integrated vectorization sample](https://github.com/Azure/azure-search-vector-samples/blob/main/demo-python/code/integrated-vectorization/azure-search-integrated-vectorization-sample.ipynb).
