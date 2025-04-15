---
title: Integrated Vectorization Using REST APIs or Python
titleSuffix: Azure AI Search
description: Learn how to use supported data sources and embedding models for vectorization during indexing and queries in Azure AI Search.
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 04/18/2025
---

# Set up integrated vectorization in Azure AI Search using REST or Python

In this article, you learn how to use an indexer and a skillset to chunk, vectorize, and index content from a [supported data source](#supported-data-sources). The skillset calls the [Text Split skill](cognitive-search-skill-textsplit.md) or [Document Layout skill](cognitive-search-skill-document-intelligence-layout.md) for chunking and an embedding skill that's attached to a [supported embedding model](#supported-embedding-models) for chunk vectorization.

You also learn how to perform [vector search](vector-search-overview.md) by assigning a vectorizer, which you define in the index schema, to a vector field. The vectorizer should match the embedding model that encodes your content. At query time, the vectorizer is automatically used for text-to-vector conversion.

This article describes the end-to-end workflow for [integrated vectorization](vector-search-integrated-vectorization.md) using REST and Python. For portal-based instructions, see [Quickstart: Vectorize text and images in the Azure portal](search-get-started-portal-import-vectors.md).

## Prerequisites

+ An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/free/?WT.mc_id=A261C142F).

+ An [Azure AI Search service](search-create-service-portal.md) in the same region as your Azure AI services multi-service resource. We recommend the Basic tier or higher.

+ A [supported data source](#supported-data-sources).

+ A [supported embedding model](#supported-embedding-models).

+ Completion of [Quickstart: Connect without keys](search-get-started-rbac.md) and [Configure a system-assigned managed identity](search-howto-managed-identities-data-sources.md#create-a-system-managed-identity). Although you can use key-based authentication for data plane operations, this article assumes [roles and managed identities](#role-based-access), which are more secure.

+ [Visual Studio Code](https://code.visualstudio.com/download) with a [REST client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) or the [Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python).

### Supported data sources

Azure AI Search [supports various data sources](search-indexer-overview.md#supported-data-sources). However, this article only covers the data sources that work with whole files, which are described in the following table.

| Supported data source | Description |
|--|--|
| [Azure Blob Storage](search-howto-indexing-azure-blob-storage.md) | This data source works with blobs and tables. You must use a standard performance (general-purpose v2) account. Access tiers can be hot, cool, or cold. |
| [Azure Data Lake Storage (ADLS) Gen2](/azure/storage/blobs/create-data-lake-storage-account) | This is an Azure Storage account with a hierarchical namespace enabled. To confirm that you have Data Lake Storage, check the **Properties** tab on the **Overview** page.<br><br> :::image type="content" source="media/search-how-to-integrated-vectorization/data-lake-storage-account.png" alt-text="Screenshot of an Azure Data Lake Storage account in the Azure portal." border="true" lightbox="media/search-how-to-integrated-vectorization/data-lake-storage-account.png"::: |
| [OneLake](search-how-to-index-onelake-files.md) | This data source is currently in preview. For information about limitations and supported shortcuts, see [OneLake indexing](search-how-to-index-onelake-files.md). |

### Supported embedding models

Use an embedding model on an Azure AI platform in the [same region as Azure AI Search](search-create-service-portal.md#regions-with-the-most-overlap). For deployment instructions, see [Prepare your embedding model](#prepare-your-embedding-model).

| Provider | Supported models |
|--|--|
| [Azure OpenAI Service](https://aka.ms/oai/access) <sup>1, 2</sup> | text-embedding-ada-002<br>text-embedding-3-small<br>text-embedding-3-large |
| [Azure AI Foundry model catalog](/azure/ai-foundry/what-is-azure-ai-foundry) | For text:<br>Cohere-embed-v3-english<br>Cohere-embed-v3-multilingual<br><br>For images:<br>Facebook-DinoV2-Image-Embeddings-ViT-Base<br>Facebook-DinoV2-Image-Embeddings-ViT-Giant |
| [Azure AI services multi-service account](/azure/ai-services/multi-service-resource#azure-ai-services-resource-for-azure-ai-search-skills) | For text and images:<br>[Azure AI Vision multimodal](/azure/ai-services/computer-vision/how-to/image-retrieval) <sup>3</sup> (available in [select regions](/azure/ai-services/computer-vision/overview-image-analysis#region-availability))</li> |

<sup>1</sup> If you're using Azure OpenAI Service, the endpoint must have a [custom subdomain](/azure/ai-services/cognitive-services-custom-subdomains), such as `https://my-unique-name.cognitiveservices.azure.com`. If you created your service in the [Azure portal](https://portal.azure.com/), this subdomain was automatically generated during service setup. Ensure that your service has a custom subdomain before you use it with the Azure AI Search integration.

<sup>2</sup> Azure OpenAI Service resources (with access to embedding models) that were created in the [Azure AI Foundry portal](https://ai.azure.com/) aren't supported. Only Azure OpenAI Service resources created in the Azure portal are compatible with the [Azure OpenAI Embedding skill](cognitive-search-skill-azure-openai-embedding.md) integration.

<sup>3</sup> Depending on how you [attach the multi-service resource](cognitive-search-attach-cognitive-services.md), your multi-service account might need to be in the same region as your Azure AI Search service.

### Role-based access

You can use Microsoft Entra ID with role assignments or key-based authentication with full-access connection strings. For Azure AI Search service connections to other resources, we recommend role assignments.

To configure role-based access for integrated vectorization:

1. On your search service, [enable roles](search-security-enable-roles.md) and [configure a managed identity](search-howto-managed-identities-data-sources.md#create-a-system-managed-identity).

1. On your data source platform and embedding model provider, create role assignments that allow your search service to access data and models. See [Prepare your data](#prepare-your-data) and [Prepare your embedding model](#prepare-your-embedding-model).

> [!NOTE]
> Free search services support role-based connections to Azure AI Search. However, they don't support managed identities on outbound connections to Azure Storage or Azure AI Vision. This lack of support requires key-based authentication on connections between free search services and other Azure resources.
>
> For more secure connections, use the Basic tier or higher. You can then enable roles and configure a managed identity for authorized access.

## Prepare your data

In this section, you prepare your data for integrated vectorization by uploading files to a [supported data source](#supported-data-sources) and assigning roles.

### [Azure Blob Storage](#tab/prepare-data-storage)

1. Sign in to the [Azure portal](https://portal.azure.com/) and select your Azure Storage account.

1. From the left pane, select **Data Storage** > **Containers**.

1. Create a container or select an existing container, and then upload your files to the container.

1. To assign roles:

   1. From the left pane, select **Access Control (IAM)**.

   1. Select **Add** > **Add role assignment**.

   1. Under **Job function roles**, select **[Storage Blob Data Reader](search-howto-managed-identities-data-sources.md#assign-a-role)**, and then select **Next**.

   1. Under **Members**, select **Managed identity**, and then select **Select members**.

   1. Select your subscription and the managed identity of your search service.

1. To obtain a connection string:

   1. From the left pane, select **Security + networking** > **Access keys**.

   1. Copy either connection string. You specify this string later in the [Set endpoints](#set-endpoints) step.

1. (Optional) Synchronize deletions in your container with deletions in the search index. To configure your indexer for deletion detection:

   1. [Enable soft delete](/azure/storage/blobs/soft-delete-blob-enable?tabs=azure-portal#enable-blob-soft-delete-hierarchical-namespace) on your storage account. If you're using [native soft delete](search-howto-index-changed-deleted-blobs.md#native-blob-soft-delete), the next step isn't required.

   1. [Add custom metadata](search-howto-index-changed-deleted-blobs.md#soft-delete-strategy-using-custom-metadata) that an indexer can scan to determine which blobs are marked for deletion. Give your custom property a descriptive name. For example, you can name the property "IsDeleted" and set it to false. Repeat this step for every blob in the container. When you want to delete the blob, change the property to true. For more information, see [Change and delete detection when indexing from Azure Storage](search-howto-index-changed-deleted-blobs.md).

### [ADLS Gen2](#tab/prepare-data-adlsgen2)

1. Sign in to the [Azure portal](https://portal.azure.com/) and select your Azure Storage account.

1. From the left pane, select **Data Storage** > **Containers**.

1. Create a container or select an existing container, and then upload your files to the container.

1. To assign roles:

   1. From the left pane, select **Access Control (IAM)**.

   1. Select **Add** > **Add role assignment**.

   1. Under **Job function roles**, select **[Storage Blob Data Reader](search-howto-managed-identities-data-sources.md#assign-a-role)**, and then select **Next**.

   1. Under **Members**, select **Managed identity**, and then select **Select members**.

   1. Select your subscription and the managed identity of your search service.

1. To obtain a connection string:

   1. From the left pane, select **Security + networking** > **Access keys**.

   1. Copy either connection string. You specify this string later in the [Set endpoints](#set-endpoints) step.

1. (Optional) Synchronize deletions in your container with deletions in the search index. To configure your indexer for deletion detection:

   1. [Enable soft delete](/azure/storage/blobs/soft-delete-blob-enable?tabs=azure-portal#enable-blob-soft-delete-hierarchical-namespace) on your storage account.

   1. [Add custom metadata](search-howto-index-changed-deleted-blobs.md#soft-delete-strategy-using-custom-metadata) that an indexer can scan to determine which blobs are deleted. Give your custom property a descriptive name. For example, you can name the property "IsDeleted" and set it to false. Repeat this step for every blob in the container. When you want to delete the blob, change the property to true. For more information, see [Change and delete detection when indexing from Azure Storage](search-howto-index-changed-deleted-blobs.md).

### [OneLake](#tab/prepare-data-onelake)

1. Sign in to [Power BI](https://powerbi.com/) and [create a workspace](/fabric/data-engineering/tutorial-lakehouse-get-started).

1. From the left pane, select your new workspace.

1. To assign roles:

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

In this section, you prepare your Azure AI resource for integrated vectorization by assigning roles, obtaining an endpoint, and deploying a [supported embedding model](#supported-embedding-models).

### [Azure OpenAI](#tab/prepare-model-aoai)

Azure AI Search supports text-embedding-ada-002, text-embedding-3-small, and text-embedding-3-large. Internally, Azure AI Search calls the [AzureOpenAIEmbedding skill](cognitive-search-skill-azure-openai-embedding.md) to connect to Azure OpenAI.

1. Sign in to the [Azure portal](https://portal.azure.com/) and select your Azure OpenAI resource.

1. To assign roles:

   1. From the left pane, select **Access control (IAM)**.

   1. Select **Add** > **Add role assignment**.

   1. Under **Job function roles**, select **[Cognitive Services OpenAI User](/azure/ai-services/openai/how-to/role-based-access-control#azure-openai-roles)**, and then select **Next**.

   1. Under **Members**, select **Managed identity**, and then select **Select members**.

   1. Select your subscription and the managed identity of your search service.

1. To obtain an endpoint:

   1. From the left pane, select **Resource Management** > **Keys and Endpoint**.

   1. Copy the endpoint for your Azure OpenAI resource. You specify this URL later in the [Set endpoints](#set-endpoints) step.

1. To deploy an embedding model:

   1. Sign in to the [Azure AI Foundry portal](https://ai.azure.com/) and select your Azure OpenAI resource.

   1. From the left pane, select **Shared resources** > **Deployments**.

   1. Select **Deploy model** > **Deploy base model**.

   1. Set the **Inference tasks** filter to **Embeddings**.

   1. Deploy a [supported embedding model](#supported-embedding-models).

   Make a note of the model name and endpoint. Embedding skills and vectorizers assemble the full endpoint internally, so you only need the resource URI. For example, given `https://MY-ACCOUNT.openai.azure.com/openai/deployments/text-embedding-3-large/embeddings?api-version=2024-06-01`, the endpoint you should provide in skill and vectorizer definitions is `https://MY-ACCOUNT.openai.azure.com`.

### [Azure AI Vision](#tab/prepare-model-ai-vision)

Azure AI Search supports Azure AI Vision image retrieval through multimodal embeddings (version 4.0). Internally, Azure AI Search calls the [multimodal embeddings skill](cognitive-search-skill-vision-vectorize.md) to connect to Azure AI Vision.

1. Sign in to the [Azure portal](https://portal.azure.com/) and [create an Azure AI Vision resource](/azure/ai-services/computer-vision/how-to/image-retrieval?tabs=csharp#prerequisites). Make sure your Azure AI Search service is in the same region.

1. To assign roles:

   1. From the left pane, select **Access control (IAM)**.

   1. Select **Add** > **Add role assignment**.

   1. Under **Job function roles**, select **Cognitive Services User**, and then select **Next**.

   1. Under **Members**, select **Managed identity**, and then select **Select members**.

   1. Select your subscription and the managed identity of your search service.

> [!NOTE]
> The multimodal embeddings are built into your Azure AI Vision resource, so there's no model deployment step.

### [Azure AI Foundry model catalog](#tab/prepare-model-catalog)

Azure AI Search supports Azure, Cohere, and Facebook embedding models in the [Azure AI Foundry](https://ai.azure.com/) model catalog, but it doesn't currently support the OpenAI CLIP models. Internally, Azure AI Search calls the [AML skill](cognitive-search-aml-skill.md) to connect to the catalog.

For the model catalog, you should have an [Azure OpenAI resource](/azure/ai-services/openai/how-to/create-resource) and an [Azure AI Foundry project](/azure/ai-foundry/how-to/create-projects).

1. Sign in to the [Azure portal](https://portal.azure.com/) and select your Azure OpenAI resource.

1. To assign roles:

   1. From the left pane, select **Access control (IAM)**.

   1. Select **Add** > **Add role assignment**.

   1. Under **Job function roles**, select **Cognitive Services User**, and then select **Next**.

   1. Under **Members**, select **Managed identity**, and then select **Select members**.

   1. Select your subscription and the managed identity of your search service.

1. To obtain an endpoint:

   1. From the left pane, select **Resource Management** > **Keys and Endpoint**.

   1. Copy the endpoint for your Azure OpenAI resource. You specify this URL later in the [Set endpoints](#set-endpoints) step.

1. To deploy an embedding model from the model catalog:

   1. Sign in to the [Azure AI Foundry portal](https://ai.azure.com/) and select your project.

   1. From the left pane, select **My assets** > **Models + endpoints**.

   1. Select **Deploy model** > **Deploy base model**.

   1. Set the **Inference tasks** filter to **Embeddings**.

   1. Deploy a [supported embedding model](#supported-embedding-models).

   Make a note of the model name and endpoint. Embedding skills and vectorizers assemble the full endpoint internally, so you only need the resource URI. For example, given `https://MY-ACCOUNT.openai.azure.com/openai/deployments/text-embedding-3-large/embeddings?api-version=2024-06-01`, the endpoint you should provide in skill and vectorizer definitions is `https://MY-ACCOUNT.openai.azure.com`.

---

## Retrieve connection information

In this section, you gather connection information that's used in requests. The following steps assume that you're using roles.

1. Sign in to the [Azure portal](https://portal.azure.com/) and select your Azure AI Search service.

1. On the **Overview** page, copy the URL. An example search endpoint is `https://my-service.search.windows.net`.

1. To obtain your Microsoft Entra token, follow step three in [Quickstart: Connect without keys](search-get-started-rbac.md). You get the token by running the `az account get-access-token` command.

   ```Azure CLI
   az account get-access-token --scope https://search.azure.com/.default --query accessToken --output tsv
   ```

---

## Set endpoints

In this section, you specify the endpoint and token for your Azure AI Search service and the endpoint for your [supported data source](#supported-data-sources).

### [REST](#tab/set-endpoints-rest)

1. In Visual Studio Code, copy and paste the following example into your `.rest` or `.http` file.

   ```HTTP
   @baseUrl = PUT-YOUR-SEARCH-SERVICE-URL-HERE
   @token = PUT-YOUR-MICROSOFT-ENTRA-TOKEN-HERE
   @storageConnectionString = PUT-YOUR-STORAGE-CONNECTION-STRING-HERE
   @blobContainer = PUT-YOUR-BLOB-CONTAINER-NAME-HERE
   @XYZ = OneLake

   ### List existing indexes by name
   GET  {{baseUrl}}/indexes?api-version=2024-07-01&$select=name  HTTP/1.1
   Content-Type: application/json
   Authorization: Bearer {{token}}
   ```

1. Replace the following placeholders:

   1. For `@baseUrl`, enter the search endpoint you obtained in [Retrieve connection information](#retrieve-connection-information).

   1. For `@token`, enter the Microsoft Entra token you obtained in [Retrieve connection information](#retrieve-connection-information).

   1. For `@storageConnectionString`, enter the connection string you obtained in [Prepare your data](#prepare-your-data). Delete this parameter if you're using OneLake.

   1. For `@blobContainer`, enter the name of the container you created in [Prepare your data](#prepare-your-data). Delete this parameter if you're using OneLake.

   1. For `@XYZ`, enter...

1. To verify the parameters, select **Send request**.

   A response should appear in an adjacent pane. If you have existing indexes, they're listed. Otherwise, the list is empty. If the HTTP code is `200 OK`, you're ready to proceed.

### [Python](#tab/set-endpoints-python)

1. In Visual Studio Code, copy and paste the following example into your Jupyter notebook.

   ```Python
   AZURE_SEARCH_SERVICE: str = "PUT YOUR SEARCH SERVICE URL HERE"
   AZURE_OPENAI_ACCOUNT: str = "PUT YOUR AZURE OPENAI ACCOUNT URL HERE"
   AZURE_AI_MULTISERVICE_ACCOUNT: str = "PUT YOUR AZURE AI MULTISERVICE ACCOUNT URL HERE"
   AZURE_AI_MULTISERVICE_KEY: str = "PUT YOUR AZURE AI MULTISERVICE KEY HERE. ROLES ARE USED TO CONNECT. KEY IS USED FOR BILLING."
   AZURE_STORAGE_CONNECTION: str = "PUT YOUR AZURE STORAGE CONNECTION STRING HERE (see example below for syntax)"
   
   # Example connection string for a search service managed-identity connection:
   # "ResourceId=/subscriptions/FAKE-SUBCRIPTION=ID/resourceGroups/FAKE-RESOURCE-GROUP/providers/Microsoft.Storage/storageAccounts/FAKE-ACCOUNT;"
   ```

1. Replace the following placeholders:

   1. For `AZURE_SEARCH_SERVICE`, enter the search endpoint you obtained in [Retrieve connection information](#retrieve-connection-information).

   1. For `AZURE_OPENAI_ACCOUNT`, enter the endpoint you obtained in [Prepare your embedding model](#prepare-your-embedding-model). Delete this variable if you're using Azure AI Vision.

   1. For `AZURE_AI_MULTISERVICE_ACCOUNT`, enter...

   1. For `AZURE_STORAGE_CONNECTION`, enter the connection string you obtained in [Prepare your data](#prepare-your-data). Delete this parameter if you're using OneLake.

   1. For `@XYZ`, enter...

---

## Connect to your data

For indexer-based indexing, you must connect to a [supported data source](#supported-data-sources). Indexers require a data source that specifies the type, credentials, and containers.

### [REST](#tab/connect-data-rest)

1. In Visual Studio Code...

1. Use [Create Data Source](/rest/api/searchservice/data-sources/create) to define the data source.  

   ```HTTP
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

Provide the endpoints you collected in a previous step. You can leave the API keys empty if you enabled role-based authentication. Otherwise, if you can't use roles, provide API keys for each resource.

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
