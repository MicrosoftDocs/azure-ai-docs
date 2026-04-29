---
title: Create a Blob Knowledge Source for Agentic Retrieval
description: A blob knowledge source specifies a blob container that you want to read from. It also includes models and properties for creating an indexer, data source, skillset, and index used for agentic retrieval workloads.
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 04/14/2026
zone_pivot_groups: search-csharp-python-rest
---

# Create a blob knowledge source from Azure Blob Storage and ADLS Gen2

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

Use a *blob knowledge source* to index and query Azure blob content in an agentic retrieval pipeline. [Knowledge sources](agentic-knowledge-source-overview.md) are created independently, referenced in a [knowledge base](agentic-retrieval-how-to-create-knowledge-base.md), and used as grounding data when an agent or chatbot calls a [retrieve action](agentic-retrieval-how-to-retrieve.md) at query time.

Unlike a [search index knowledge source](agentic-knowledge-source-how-to-search-index.md), which specifies an existing and qualified index, a blob knowledge source specifies an external data source, models, and properties to automatically generate the following Azure AI Search objects:

+ A data source that represents a blob container.
+ A skillset that chunks and optionally vectorizes multimodal content from the container.
+ An index that stores enriched content and meets the criteria for agentic retrieval.
+ An indexer that uses the previous objects to drive the indexing and enrichment pipeline.

> [!NOTE]
> If user access is specified at the document (blob) level in Azure Storage, a knowledge source can carry permission metadata forward to indexed content in Azure AI Search. For more information, see [ADLS Gen2 permission metadata](search-indexer-access-control-lists-and-role-based-access.md) or [Blob RBAC scopes](search-blob-indexer-role-based-access.md).

### Usage support

| [Azure portal](get-started-portal-agentic-retrieval.md) | [Microsoft Foundry portal](/azure/ai-foundry/agents/concepts/what-is-foundry-iq#workflow) | [.NET SDK](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/CHANGELOG.md) | [Python SDK](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [Java SDK](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [JavaScript SDK](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/search/search-documents/CHANGELOG.md) | [REST API](/rest/api/searchservice/knowledge-sources?view=rest-searchservice-2025-11-01-preview&preserve-view=true) |
|--|--|--|--|--|--|--|
| ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |

## Prerequisites

+ Azure AI Search in any [region that provides agentic retrieval](search-region-support.md). You must have [semantic ranker enabled](semantic-how-to-enable-disable.md).

+ An [Azure Blob Storage](/azure/storage/common/storage-account-create) or [Azure Data Lake Storage (ADLS) Gen2](/azure/storage/blobs/create-data-lake-storage-account) account.

+ A blob container with [supported content types](search-how-to-index-azure-blob-storage.md#supported-document-formats) for text content. For optional image verbalization, the supported content type depends on whether your chat completion model can analyze and describe the image file.

+ Permission to create and use objects on Azure AI Search. We recommend [role-based access](search-security-rbac.md), but you can use [API keys](search-security-api-keys.md) if a role assignment isn't feasible. For more information, see [Connect to a search service](search-get-started-rbac.md).

::: zone pivot="csharp"

+ The latest [`Azure.Search.Documents` preview package](https://www.nuget.org/packages/Azure.Search.Documents/11.8.0-beta.1): `dotnet add package Azure.Search.Documents --prerelease`

::: zone-end

::: zone pivot="python"

+ The latest [`azure-search-documents` preview package](https://pypi.org/project/azure-search-documents/11.7.0b2/): `pip install --pre azure-search-documents`

::: zone-end

::: zone pivot="rest"

+ The [2025-11-01-preview](/rest/api/searchservice/operation-groups?view=rest-searchservice-2025-11-01-preview&preserve-view=true) version of the Search Service REST APIs.

::: zone-end

## Check for existing knowledge sources

::: zone pivot="csharp"

[!INCLUDE [Check for existing knowledge sources using C#](includes/how-tos/knowledge-source-check-csharp.md)]

::: zone-end

::: zone pivot="python"

[!INCLUDE [Check for existing knowledge sources using Python](includes/how-tos/knowledge-source-check-python.md)]

::: zone-end

::: zone pivot="rest"

[!INCLUDE [Check for existing knowledge sources using REST](includes/how-tos/knowledge-source-check-rest.md)]

::: zone-end

The following JSON is an example response for a blob knowledge source.

```json
{
  "name": "my-blob-ks",
  "kind": "azureBlob",
  "description": "A sample blob knowledge source.",
  "encryptionKey": null,
  "azureBlobParameters": {
    "connectionString": "<REDACTED>",
    "containerName": "blobcontainer",
    "folderPath": null,
    "isADLSGen2": false,
    "ingestionParameters": {
      "disableImageVerbalization": false,
      "ingestionPermissionOptions": [],
      "contentExtractionMode": "standard",
      "identity": null,
      "embeddingModel": {
        "kind": "azureOpenAI",
        "azureOpenAIParameters": {
          "resourceUri": "<REDACTED>",
          "deploymentId": "text-embedding-3-large",
          "apiKey": "<REDACTED>",
          "modelName": "text-embedding-3-large",
          "authIdentity": null
        }
      },
      "chatCompletionModel": {
        "kind": "azureOpenAI",
        "azureOpenAIParameters": {
          "resourceUri": "<REDACTED>",
          "deploymentId": "gpt-5-mini",
          "apiKey": "<REDACTED>",
          "modelName": "gpt-5-mini",
          "authIdentity": null
        }
      },
      "ingestionSchedule": null,
      "assetStore": null,
      "aiServices": {
        "uri": "<REDACTED>",
        "apiKey": "<REDACTED>"
      }
    },
    "createdResources": {
      "datasource": "my-blob-ks-datasource",
      "indexer": "my-blob-ks-indexer",
      "skillset": "my-blob-ks-skillset",
      "index": "my-blob-ks-index"
    }
  }
}
```

> [!NOTE]
> Sensitive information is redacted. The generated resources appear at the end of the response.

## Create a knowledge source

::: zone pivot="csharp"

Run the following code to [create a blob knowledge source](/dotnet/api/azure.search.documents.indexes.models.azureblobknowledgesource?view=azure-dotnet-preview&preserve-view=true).

```csharp
// Create a blob knowledge source
using Azure.Search.Documents.Indexes;
using Azure.Search.Documents.Indexes.Models;
using Azure.Search.Documents.KnowledgeBases.Models;
using Azure;

var indexClient = new SearchIndexClient(new Uri(searchEndpoint), new AzureKeyCredential(apiKey));

var chatCompletionParams = new AzureOpenAIVectorizerParameters
{
    ResourceUri = new Uri(aoaiEndpoint),
    DeploymentName = aoaiGptDeployment,
    ModelName = aoaiGptModel
};

var embeddingParams = new AzureOpenAIVectorizerParameters
{
    ResourceUri = new Uri(aoaiEndpoint),
    DeploymentName = aoaiEmbeddingDeployment,
    ModelName = aoaiEmbeddingModel
};

var ingestionParams = new KnowledgeSourceIngestionParameters
{
    DisableImageVerbalization = false,
    ChatCompletionModel = new KnowledgeBaseAzureOpenAIModel(azureOpenAIParameters: chatCompletionParams),
    EmbeddingModel = new KnowledgeSourceAzureOpenAIVectorizer
    {
        AzureOpenAIParameters = embeddingParams
    }
};

var blobParams = new AzureBlobKnowledgeSourceParameters(
    connectionString: connectionString,
    containerName: containerName
)
{
    IsAdlsGen2 = false,
    IngestionParameters = ingestionParams
};

var knowledgeSource = new AzureBlobKnowledgeSource(
    name: "my-blob-ks",
    azureBlobParameters: blobParams
)
{
    Description = "This knowledge source pulls from a blob storage container."
};

await indexClient.CreateOrUpdateKnowledgeSourceAsync(knowledgeSource);
Console.WriteLine($"Knowledge source '{knowledgeSource.Name}' created or updated successfully.");
```

::: zone-end

::: zone pivot="python"

Run the following code to create a blob knowledge source.

```python
# Create a blob knowledge source
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import AzureBlobKnowledgeSource, AzureBlobKnowledgeSourceParameters, KnowledgeBaseAzureOpenAIModel, AzureOpenAIVectorizerParameters, KnowledgeSourceAzureOpenAIVectorizer, KnowledgeSourceContentExtractionMode, KnowledgeSourceIngestionParameters

index_client = SearchIndexClient(endpoint = "search_url", credential = AzureKeyCredential("api_key"))

knowledge_source = AzureBlobKnowledgeSource(
    name = "my-blob-ks",
    description = "This knowledge source pulls from a blob storage container.",
    encryption_key = None,
    azure_blob_parameters = AzureBlobKnowledgeSourceParameters(
        connection_string = "blob_connection_string",
        container_name = "blob_container_name",
        folder_path = None,
        is_adls_gen2 = False,
        ingestion_parameters = KnowledgeSourceIngestionParameters(
            identity = None,
            disable_image_verbalization = False,
            chat_completion_model = KnowledgeBaseAzureOpenAIModel(
                azure_open_ai_parameters = AzureOpenAIVectorizerParameters(
                    resource_url = "aoai_endpoint",
                    deployment_name = "aoai_gpt_deployment",
                    model_name = "aoai_gpt_model",
                    api_key = "aoai_api_key"
                )
            ),
            embedding_model = KnowledgeSourceAzureOpenAIVectorizer(
                azure_open_ai_parameters=AzureOpenAIVectorizerParameters(
                    resource_url = "aoai_endpoint",
                    deployment_name = "aoai_embedding_deployment",
                    model_name = "aoai_embedding_model",
                    api_key = "aoai_api_key"
                )
            ),
            content_extraction_mode = KnowledgeSourceContentExtractionMode.MINIMAL,
            ingestion_schedule = None,
            ingestion_permission_options = None
        )
    )
)

index_client.create_or_update_knowledge_source(knowledge_source)
print(f"Knowledge source '{knowledge_source.name}' created or updated successfully.")
```

::: zone-end

::: zone pivot="rest"

Use [Knowledge Sources - Create or Update (REST API)](/rest/api/searchservice/knowledge-sources/create-or-update?view=rest-searchservice-2025-11-01-preview&preserve-view=true) to create a blob knowledge source.

```http
PUT {{search-url}}/knowledgesources/my-blob-ks?api-version=2025-11-01-preview
api-key: {{api-key}}
Content-Type: application/json

{
  "name": "my-blob-ks",
  "kind": "azureBlob",
  "description": "This knowledge source pulls from a blob storage container.",
  "encryptionKey": null,
  "azureBlobParameters": {
    "connectionString": "<YOUR AZURE STORAGE CONNECTION STRING>",
    "containerName": "<YOUR BLOB CONTAINER NAME>",
    "folderPath": null,
    "isADLSGen2": false,
    "ingestionParameters": {
        "identity": null,
        "disableImageVerbalization": null,
        "chatCompletionModel": {
            "kind": "azureOpenAI",
            "azureOpenAIParameters": {
                "resourceUri": "{{aoai-endpoint}}",
                "deploymentId": "{{aoai-gpt-deployment}}",
                "modelName": "{{aoai-gpt-model}}",
                "apiKey": "{{aoai-key}}"
            }
        },
        "embeddingModel": {
            "kind": "azureOpenAI",
            "azureOpenAIParameters": {
                "resourceUri": "{{aoai-endpoint}}",
                "deploymentId": "{{aoai-embedding-deployment}}",
                "modelName": "{{aoai-embedding-model}}",
                "apiKey": "{{aoai-key}}"
            }
        },
        "contentExtractionMode": "minimal",
        "ingestionSchedule": null,
        "ingestionPermissionOptions": []
    }
  }
}
```

::: zone-end

### Source-specific properties

You can pass the following properties to create a blob knowledge source.

::: zone pivot="csharp"

| Name | Description | Type | Editable | Required |
|--|--|--|--|--|
| `Name` | The name of the knowledge source, which must be unique within the knowledge sources collection and follow the [naming guidelines](/rest/api/searchservice/naming-rules) for objects in Azure AI Search. | String | No | Yes |
| `Description` | A description of the knowledge source. | String | Yes | No |
| `EncryptionKey` | A [customer-managed key](search-security-manage-encryption-keys.md) to encrypt sensitive information in both the knowledge source and the generated objects. | Object | Yes | No |
| `AzureBlobParameters` | Parameters specific to blob knowledge sources: `ConnectionString`, `ContainerName`, `FolderPath`, and `IsAdlsGen2`. | Object |  | No |
| `ConnectionString` | A key-based [connection string](search-how-to-index-azure-blob-storage.md#supported-credentials-and-connection-strings) or, if you're using a managed identity, the resource ID. | String | No | Yes |
| `ContainerName` | The name of the blob storage container. | String | No | Yes |
| `FolderPath` | A folder within the container. | String | No | No |
| `IsAdlsGen2` | The default is `False`. Set to `True` if you're using an ADLS Gen2 storage account. | Boolean | No | No |

::: zone-end

::: zone pivot="python"

| Name | Description | Type | Editable | Required |
|--|--|--|--|--|
| `name` | The name of the knowledge source, which must be unique within the knowledge sources collection and follow the [naming guidelines](/rest/api/searchservice/naming-rules) for objects in Azure AI Search. | String | No | Yes |
| `description` | A description of the knowledge source. | String | Yes | No |
| `encryption_key` | A [customer-managed key](search-security-manage-encryption-keys.md) to encrypt sensitive information in both the knowledge source and the generated objects. | Object | Yes | No |
| `azure_blob_parameters` | Parameters specific to blob knowledge sources: `connection_string`, `container_name`, `folder_path`, and `is_adls_gen2`. | Object |  | No |
| `connection_string` | A key-based [connection string](search-how-to-index-azure-blob-storage.md#supported-credentials-and-connection-strings) or, if you're using a managed identity, the resource ID. | String | No | Yes |
| `container_name` | The name of the blob storage container. | String | No | Yes |
| `folder_path` | A folder within the container. | String | No | No |
| `is_adls_gen2` | The default is `False`. Set to `True` if you're using an ADLS Gen2 storage account. | Boolean | No | No |

::: zone-end

::: zone pivot="rest"

| Name | Description | Type | Editable | Required |
|--|--|--|--|--|
| `name` | The name of the knowledge source, which must be unique within the knowledge sources collection and follow the [naming guidelines](/rest/api/searchservice/naming-rules) for objects in Azure AI Search. | String | No | Yes |
| `kind` | The kind of knowledge source, which is `azureBlob` in this case. | String | No | Yes |
| `description` | A description of the knowledge source. | String | Yes | No |
| `encryptionKey` | A [customer-managed key](search-security-manage-encryption-keys.md) to encrypt sensitive information in both the knowledge source and the generated objects. | Object | Yes | No |
| `azureBlobParameters` | Parameters specific to blob knowledge sources: `connectionString`, `containerName`, `folderPath`, and `isADLSGen2`. | Object |  | No |
| `connectionString` | A key-based [connection string](search-how-to-index-azure-blob-storage.md#supported-credentials-and-connection-strings) or, if you're using a managed identity, the resource ID. | String | No | Yes |
| `containerName` | The name of the blob storage container. | String | No | Yes |
| `folderPath` | A folder within the container. | String | No | No |
| `isADLSGen2` | The default is `false`. Set to `true` if you're using an ADLS Gen2 storage account. | Boolean | No | No |

::: zone-end

### Ingestion parameters properties

::: zone pivot="csharp"

[!INCLUDE [C# ingestionParameters properties](includes/how-tos/knowledge-source-ingestion-parameters-csharp.md)]

::: zone-end

::: zone pivot="python"

[!INCLUDE [Python ingestionParameters properties](includes/how-tos/knowledge-source-ingestion-parameters-python.md)]

::: zone-end

::: zone pivot="rest"

[!INCLUDE [REST ingestionParameters properties](includes/how-tos/knowledge-source-ingestion-parameters-rest.md)]

::: zone-end

## Check ingestion status

::: zone pivot="csharp"

[!INCLUDE [C# knowledge source status](includes/how-tos/knowledge-source-status-csharp.md)]

::: zone-end

::: zone pivot="python"

[!INCLUDE [Python knowledge source status](includes/how-tos/knowledge-source-status-python.md)]

::: zone-end

::: zone pivot="rest"

[!INCLUDE [REST knowledge source status](includes/how-tos/knowledge-source-status-rest.md)]

::: zone-end

## Review the created objects

When you create a blob knowledge source, your search service also creates an indexer, index, skillset, and data source. We don't recommend that you edit these objects, as introducing an error or incompatibility can break the pipeline.

After you create a knowledge source, the response lists the created objects. These objects are created according to a fixed template, and their names are based on the name of the knowledge source. You can't change the object names.

We recommend using the Azure portal to validate output creation. The workflow is:

1. Check the indexer for success or failure messages. Connection or quota errors appear here.
1. Check the index for searchable content. Use Search Explorer to run queries.
1. Check the skillset to learn how your content is chunked and optionally vectorized.
1. Check the data source for connection details. Our example uses API keys for simplicity, but you can use Microsoft Entra ID for authentication and role-based access control for authorization.

## Assign to a knowledge base

If you're satisfied with the knowledge source, continue to the next step: specify the knowledge source in a [knowledge base](agentic-retrieval-how-to-create-knowledge-base.md).

After the knowledge base is configured, use the [retrieve action](agentic-retrieval-how-to-retrieve.md) to query the knowledge source.

::: zone pivot="csharp"

> [!TIP]
> To enforce document-level permissions, set `IngestionPermissionOptions` when you create this knowledge source, and then include the user's access token in the retrieve request. For more information, see [Enforce permissions at query time](agentic-retrieval-how-to-retrieve.md#enforce-permissions-at-query-time).

::: zone-end

::: zone pivot="python"

> [!TIP]
> To enforce document-level permissions, set `ingestion_permission_options` when you create this knowledge source, and then include the user's access token in the retrieve request. For more information, see [Enforce permissions at query time](agentic-retrieval-how-to-retrieve.md#enforce-permissions-at-query-time).

::: zone-end

::: zone pivot="rest"

> [!TIP]
> To enforce document-level permissions, set `ingestionPermissionOptions` when you create this knowledge source, and then include the user's access token in the retrieve request. For more information, see [Enforce permissions at query time](agentic-retrieval-how-to-retrieve.md#enforce-permissions-at-query-time).

::: zone-end

## Delete a knowledge source

::: zone pivot="csharp"

[!INCLUDE [Delete knowledge source using C#](includes/how-tos/knowledge-source-delete-csharp.md)]

::: zone-end

::: zone pivot="python"

[!INCLUDE [Delete knowledge source using Python](includes/how-tos/knowledge-source-delete-python.md)]

::: zone-end

::: zone pivot="rest"

[!INCLUDE [Delete knowledge source using REST](includes/how-tos/knowledge-source-delete-rest.md)]

::: zone-end

## Related content

+ [Agentic retrieval in Azure AI Search](agentic-retrieval-overview.md)
+ [Azure AI Search blob knowledge source Python sample](https://github.com/Azure/azure-search-vector-samples/blob/main/demo-python/code/knowledge/blob-knowledge-source.ipynb)
+ [Agentic RAG: Build a reasoning retrieval engine with Azure AI Search (YouTube video)](https://www.youtube.com/watch?v=PeTmOidqHM8)
+ [Azure OpenAI demo featuring agentic retrieval](https://github.com/Azure-Samples/azure-search-openai-demo)
