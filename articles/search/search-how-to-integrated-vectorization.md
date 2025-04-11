---
title: Integrated Vectorization Using REST APIs or Python
titleSuffix: Azure AI Search
description: Learn how to use supported data sources and embedding models for vectorization during indexing and queries in Azure AI Search.
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 04/11/2025
---

# Set up integrated vectorization in Azure AI Search using REST or Python

In this article, you learn how to use an indexer and a skillset to chunk, vectorize, and index content from a [supported data source](#supported-data-sources). The skillset calls the [Text Split skill](cognitive-search-skill-textsplit.md) or [Document Layout skill](cognitive-search-skill-document-intelligence-layout.md) for chunking and an embedding skill that's attached to a [supported embedding model](#supported-embedding-models) for chunk vectorization.

You also learn how to perform [vector search](vector-search-overview.md) by assigning a vectorizer, which you define in the index schema, to a vector field. The vectorizer should match the embedding model that encodes your content. At query time, the vectorizer is automatically used for text-to-vector conversion.

This article describes the end-to-end workflow for [integrated vectorization](vector-search-integrated-vectorization.md) using REST and Python. For portal-based instructions, see [Quickstart: Vectorize text and images in the Azure portal](search-get-started-portal-import-vectors.md).

## Prerequisites

+ An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/free/?WT.mc_id=A261C142F).

+ An [Azure AI Search service](search-create-service-portal.md). We recommend the Basic tier or higher.

+ An [Azure AI services multi-service resource](/azure/ai-services/multi-service-resource) in the same region as your Azure AI Search service.

+ A [supported data source](#supported-data-sources).

+ A [supported embedding model](#supported-embedding-models).

+ [Visual Studio Code](https://code.visualstudio.com/download) with a [REST client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) or the [Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python).

### Supported data sources

Azure AI Search [supports various data sources](search-indexer-overview.md#supported-data-sources). However, this article only covers the data sources that work with whole files, which are described in the following table.

| Supported data source | Description |
|--|--|
| [Azure Blob Storage](search-howto-indexing-azure-blob-storage.md) | This data source works with blobs and tables. You must use a standard performance (general-purpose v2) account. Access tiers can be hot, cool, or cold. |
| [Azure Data Lake Storage (ADLS) Gen2](/azure/storage/blobs/create-data-lake-storage-account) | This is an Azure Storage account with a hierarchical namespace enabled. To confirm that you have Data Lake Storage, check the **Properties** tab on the **Overview** page.<br><br> :::image type="content" source="media/search-how-to-integrated-vectorization/data-lake-storage-account.png" alt-text="Screenshot of an Azure Data Lake Storage account in the Azure portal." border="true" lightbox="media/search-how-to-integrated-vectorization/data-lake-storage-account.png"::: |
| [OneLake lakehouse](search-how-to-index-onelake-files.md) | This data source is currently in preview. |

### Supported embedding models

Use an embedding model on an Azure AI platform in the [same region as Azure AI Search](search-create-service-portal.md#regions-with-the-most-overlap). For deployment instructions, see [Prepare your embedding model](#prepare-your-embedding-model).

| Provider | Supported models |
|--|--|
| [Azure OpenAI Service](https://aka.ms/oai/access) <sup>1, 2</sup> | <ul><li>text-embedding-ada-002</li><li>text-embedding-3-small</li><li>text-embedding-3-large |
| [Azure AI Foundry model catalog](/azure/ai-foundry/what-is-azure-ai-foundry) | For text:<ul><li>Cohere-embed-v3-english</li><li>Cohere-embed-v3-multilingual</li></ul>For images:<ul><li>Facebook-DinoV2-Image-Embeddings-ViT-Base</li><li>Facebook-DinoV2-Image-Embeddings-ViT-Giant</li></ul> |
| [Azure AI services multi-service account](/azure/ai-services/multi-service-resource#azure-ai-services-resource-for-azure-ai-search-skills) | For text and images:<ul><li>[Azure AI Vision multimodal](/azure/ai-services/computer-vision/how-to/image-retrieval) <sup>3</sup> (available in [select regions](/azure/ai-services/computer-vision/overview-image-analysis#region-availability))</li> |

<sup>1</sup> If you're using Azure OpenAI Service, the endpoint must have a [custom subdomain](/azure/ai-services/cognitive-services-custom-subdomains), such as `https://my-unique-name.cognitiveservices.azure.com`. If you created your service in the [Azure portal](https://portal.azure.com/), this subdomain was automatically generated during service setup. Ensure that your service has a custom subdomain before you use it with the Azure AI Search integration.

<sup>2</sup> Azure OpenAI Service resources (with access to embedding models) that were created in [Azure AI Foundry portal](https://ai.azure.com/) aren't supported. Only Azure OpenAI Service resources created in the Azure portal are compatible with the [Azure OpenAI Embedding skill](cognitive-search-skill-azure-openai-embedding.md) integration.

<sup>3</sup> Depending on how you [attach the multi-service resource](cognitive-search-attach-cognitive-services.md), your multi-service account might need to be in the same region as your Azure AI Search service.

### Permissions

You can use Microsoft Entra ID with role assignments or key-based authentication with full-access connection strings. For Azure AI Search service connections to other resources, we recommend role assignments.

To configure role-based access:

1. On your search service, [enable roles](search-security-enable-roles.md) and [configure a managed identity](search-howto-managed-identities-data-sources.md#create-a-system-managed-identity).

1. On your data source platform and embedding model provider, create role assignments that allow your search service to access data and models. See [Prepare your data](#prepare-your-data) and [Prepare your embedding model](#prepare-your-embedding-model).

> [!NOTE]
> Free search services support role-based connections to Azure AI Search. However, they don't support managed identities on outbound connections to Azure Storage or Azure AI Vision. This lack of support requires key-based authentication on connections between free search services and other Azure resources.
>
> For more secure connections, use the Basic tier or higher. You can then enable roles and configure a managed identity for authorized access.

## Prepare your data

In this section, you prepare your data for integrated vectorization by uploading files to a [supported data source](#supported-data-sources) and assigning resource permissions.

### [Azure Blob Storage](#tab/prepare-data-storage)

1. Sign in to the [Azure portal](https://portal.azure.com/) and select your Azure Storage account.

1. From the left pane, select **Data Storage** > **Containers**.

1. Create a container or select an existing container, and then upload your files to the container.

1. To assign permissions:

   1. If you're using roles, select **Access Control (IAM)** from the left pane, and then assign the [Storage Blob Data Reader](search-howto-managed-identities-data-sources.md#assign-a-role) role to your search service identity.

   1. If you're using key-based authentication, select **Security + networking** > **Access keys** from the left pane, and then copy a connection string for your storage account.

1. (Optional) Synchronize deletions in your container with deletions in the search index. To configure your indexer for deletion detection:

   1. [Enable soft delete](/azure/storage/blobs/soft-delete-blob-enable?tabs=azure-portal#enable-blob-soft-delete-hierarchical-namespace) on your storage account. If you're using [native soft delete](search-howto-index-changed-deleted-blobs.md#native-blob-soft-delete), the second step isn't required.

   1. [Add custom metadata](search-howto-index-changed-deleted-blobs.md#soft-delete-strategy-using-custom-metadata) that an indexer can scan to determine which blobs are marked for deletion. Give your custom property a descriptive name. For example, you can name the property "IsDeleted" and set it to false. Repeat this step for every blob in the container. When you want to delete the blob, change the property to true. For more information, see [Change and delete detection when indexing from Azure Storage](search-howto-index-changed-deleted-blobs.md).

### [ADLS Gen2](#tab/prepare-data-adlsgen2)

1. Sign in to the [Azure portal](https://portal.azure.com/) and select your Azure Storage account.

1. From the left pane, select **Data Storage** > **Containers**.

1. Create a container or select an existing container, and then upload your files to the container.

1. To assign permissions:

   1. If you're using roles, select **Access Control (IAM)** from the left pane, and then assign the [Storage Blob Data Reader](search-howto-managed-identities-data-sources.md#assign-a-role) role to your search service identity.

   1. If you're using key-based authentication, select **Security + networking** > **Access keys** from the left pane, and then copy a connection string for your storage account.

1. (Optional) Synchronize deletions in your container with deletions in the search index. To configure your indexer for deletion detection:

   1. [Enable soft delete](/azure/storage/blobs/soft-delete-blob-enable?tabs=azure-portal#enable-blob-soft-delete-hierarchical-namespace) on your storage account.

   1. [Add custom metadata](search-howto-index-changed-deleted-blobs.md#soft-delete-strategy-using-custom-metadata) that an indexer can scan to determine which blobs are deleted. Give your custom property a descriptive name. For example, you can name the property "IsDeleted" and set it to false. Repeat this step for every blob in the container. When you want to delete the blob, change the property to true. For more information, see [Change and delete detection when indexing from Azure Storage](search-howto-index-changed-deleted-blobs.md).

### [OneLake](#tab/prepare-data-onelake)

1. Sign in to [Power BI](https://powerbi.com/) and [create a workspace](/fabric/data-engineering/tutorial-lakehouse-get-started).

1. From the left pane, select **Workspaces** and open your new workspace.

1. To assign permissions:

   1. In the upper-right corner, select **Manage access**.

   1. Select **Add people or groups**.

   1. Enter the name of your search service. For example, if the URL is `https://my-demo-service.search.windows.net`, the search service name is `my-demo-service`.

   1. Select a role. The default is **Viewer**, but you need **Contributor** to pull data into a search index.

1. To load your data:

   1. From the **Power BI** switcher in the lower-left corner, select **Data Engineering**.

   1. On the **Data Engineering** pane, select **Lakehouse** to create a lakehouse.

   1. Provide a name, and then select **Create** to create and open the new lakehouse.

   1. Select **Upload files** to upload your data.

1. To specify your lakehouse in REST or Python, copy the URL or get the workspace and lakehouse IDs. The URL has the following format: `https://msit.powerbi.com/groups/00000000-0000-0000-0000-000000000000/lakehouses/11111111-1111-1111-1111-111111111111?experience=power-bi`.

---

## Prepare your embedding model

In this section, you prepare your Azure AI resource for integrated vectorization by assigning resource permissions and deploying a [supported embedding model](#supported-embedding-models).

### [Azure OpenAI](#tab/prepare-model-aoai)

Azure AI Search supports text-embedding-ada-002, text-embedding-3-small, and text-embedding-3-large. Internally, Azure AI Search calls the [AzureOpenAIEmbedding skill](cognitive-search-skill-azure-openai-embedding.md) to connect to Azure OpenAI.

1. Sign in to the [Azure portal](https://portal.azure.com/) and select your Azure OpenAI resource.

1. To assign permissions:

   1. If you're using roles, select **Access control (IAM)** from the left pane, and then assign the [Cognitive Services OpenAI User](/azure/ai-services/openai/how-to/role-based-access-control#azure-openai-roles) role to your search service identity.

   1. If you're using key-based authentication, select **Resource Management** > **Keys and Endpoint** from the left pane, and then copy an endpoint or API key for your Azure OpenAI resource.

1. From the left pane, select **Resource Management** > **Model deployments**, and then select **Manage Deployments** to open Azure AI Foundry.

1. Copy the deployment name of **text-embedding-ada-002** or another [supported embedding model](#supported-embedding-models). If you don't have an embedding model, deploy one now.

### [Azure AI Vision](#tab/prepare-model-ai-vision)

Azure AI Search supports Azure AI Vision image retrieval through multimodal embeddings (version 4.0). Internally, Azure AI Search calls the [multimodal embeddings skill](cognitive-search-skill-vision-vectorize.md) to connect to Azure AI Vision.

1. Sign in to the [Azure portal](https://portal.azure.com/) and [create an Azure AI Vision resource](/azure/ai-services/computer-vision/how-to/image-retrieval?tabs=csharp#prerequisites). Make sure your Azure AI Search service is in the same region.

1. To assign permissions:

   1. If you're using roles, select **Access control (IAM)** from the left pane, and then assign the **Cognitive Services User** role to your search service identity.

   1. If you're using key-based authentication, select **Resource Management** > **Keys and Endpoint** from the left pane, and then copy an endpoint or API key for your Azure AI Vision resource.

1. Add deployment steps.

### [Azure AI Foundry model catalog](#tab/prepare-model-catalog)

Azure AI Search supports Azure, Cohere, and Facebook embedding models in the [Azure AI Foundry](https://ai.azure.com/) model catalog, but it doesn't currently support the OpenAI CLIP models. Internally, Azure AI Search calls the [AML skill](cognitive-search-aml-skill.md) to connect to the catalog.

1. For the model catalog, you should have an [Azure OpenAI resource](/azure/ai-services/openai/how-to/create-resource), a [hub in Azure AI Foundry portal](/azure/ai-foundry/how-to/create-projects), and a [project](/azure/ai-foundry/how-to/create-projects). Hubs and projects with the same name can share connection information and permissions.

1. To deploy an embedding model to the model catalog in your project:

   1. Select **Models + Endpoints**, and then select **Deploy a model**.

   1. Select **Deploy base model**.

   1. Filter by inference task set to **Embeddings**.

   1. Deploy one of the [supported embedding models](#supported-embedding-models).

---

## Connect to your data

For indexer-based indexing, you must connect to a [supported data source](#supported-data-sources). Indexers require a data source that specifies the type, credentials, and containers.

### [REST](#tab/connect-data-rest)

1. Use [Create Data Source](/rest/api/searchservice/data-sources/create) to define the data source.  

   ```http
    POST https://my-search-service.search.windows.net/datasources?api-version=2024-07-01 
    {
        "name": "my-data-source",
        "description": null,
        "type": "azureblob",
        "subtype": null,
        "credentials": {
           "connectionString": "DefaultEndpointsProtocol=https;AccountName=my-account-name"
        },
        "container": {
           "name": "my-blob-in-azure-blob",
           "query": ""
        }
    }
   ```

1. Set `type` to your data source: `azureblob`, `azureadlsgen2`, or `onelake`.

1. Set `credentials` to...

1. Set `container` to...

### [Python](#tab/connect-data-python)

---

## Create a skillset

### Call a built-in skill to chunk your content

### Call an embedding skill to vectorize the chunks

## Create a vector index

## Add a vectorizer to the index

See vector-search-how-to-configure-vectorizer#define-a-vectorizer-and-vector-profile.

## Create an indexer

## Create vector queries

See vector-search-how-to-query.

## Related content

+ [Integrated vectorization sample](https://github.com/Azure/azure-search-vector-samples/blob/main/demo-python/code/integrated-vectorization/azure-search-integrated-vectorization-sample.ipynb)
