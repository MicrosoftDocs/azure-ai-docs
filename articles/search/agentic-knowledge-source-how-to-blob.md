---
title: Create a Blob Knowledge Source for Agentic Retrieval
description: A blob knowledge source specifies a blob container that you want to read from. It also includes models and properties for creating an indexer, data source, skillset, and index used for agentic retrieval workloads.
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 04/28/2026
zone_pivot_groups: search-csharp-python-rest
---

# Create a blob knowledge source from Azure Blob Storage and ADLS Gen2

[!INCLUDE [GA feature](./includes/previews/agentic-retrieval-ga-feature.md)]

Use a *blob knowledge source* to index and query Azure blob content in an agentic retrieval pipeline. [Knowledge sources](agentic-knowledge-source-overview.md) are created independently, referenced in a [knowledge base](agentic-retrieval-how-to-create-knowledge-base.md), and used as grounding data when an agent or chatbot calls a [retrieve action](agentic-retrieval-how-to-retrieve.md) at query time.

When you create a blob knowledge source, you specify an external data source, models, and properties to automatically generate the following Azure AI Search objects:

+ A data source that represents a blob container.
+ A skillset that chunks and optionally vectorizes multimodal content from the container.
+ An index that stores enriched content and meets the criteria for agentic retrieval.
+ An indexer that uses the previous objects to drive the indexing and enrichment pipeline.

> [!NOTE]
> If user access is specified at the document (blob) level in Azure Storage, a knowledge source can carry permission metadata forward to indexed content in Azure AI Search. For more information, see [ADLS Gen2 permission metadata](search-indexer-access-control-lists-and-role-based-access.md) or [Blob RBAC scopes](search-blob-indexer-role-based-access.md).

### Usage support

| [Azure portal](get-started-portal-agentic-retrieval.md) | [Microsoft Foundry portal](/azure/ai-foundry/agents/concepts/what-is-foundry-iq#workflow) | [.NET SDK](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/CHANGELOG.md) | [Python SDK](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [Java SDK](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [JavaScript SDK](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/search/search-documents/CHANGELOG.md) | [REST API](/rest/api/searchservice/knowledge-sources) |
|--|--|--|--|--|--|--|
| ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |

## Prerequisites

+ Azure AI Search in any [region that provides agentic retrieval](search-region-support.md).

+ An [Azure Blob Storage](/azure/storage/common/storage-account-create) or [Azure Data Lake Storage (ADLS) Gen2](/azure/storage/blobs/create-data-lake-storage-account) account.

+ A blob container with [supported content types](search-how-to-index-azure-blob-storage.md#supported-document-formats) for text content. For optional image verbalization, the supported content type depends on whether your chat completion model can analyze and describe the image file.

+ Permission to create and use objects on Azure AI Search. We recommend [role-based access](search-security-rbac.md), but you can use [API keys](search-security-api-keys.md) if a role assignment isn't feasible. For more information, see [Connect to a search service](search-get-started-rbac.md).

::: zone pivot="csharp"

+ Required [Azure.Search.Documents](https://www.nuget.org/packages/Azure.Search.Documents) package:

  + For 2025-11-01-preview features, the latest preview package: `dotnet add package Azure.Search.Documents --prerelease`

  + For 2026-04-01 features, the latest stable package: `dotnet add package Azure.Search.Documents`

::: zone-end

::: zone pivot="python"

+ Required [azure-search-documents](https://pypi.org/project/azure-search-documents/) package:

  + For 2025-11-01-preview features, the latest preview package: `pip install azure-search-documents --pre`

  + For 2026-04-01 features, the latest stable package: `pip install azure-search-documents`

::: zone-end

::: zone pivot="rest"

+ Required REST API version:

  + For preview features: [Search Service 2025-11-01-preview](/rest/api/searchservice/operation-groups?view=rest-searchservice-2025-11-01-preview&preserve-view=true)

  + For generally available features: [Search Service 2026-04-01](/rest/api/searchservice/operation-groups?view=rest-searchservice-2026-04-01&preserve-view=true)

::: zone-end

## Check for existing knowledge sources

[!INCLUDE [Check for existing knowledge sources](includes/how-tos/knowledge-source-check.md)]

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

Run the following code to create a blob knowledge source.

::: zone pivot="csharp"

# [2025-11-01-preview](#tab/2025-11-01-preview)

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
    },
    IngestionPermissionOptions = new List<KnowledgeSourceIngestionPermissionOption>
    {
        KnowledgeSourceIngestionPermissionOption.UserIds,
        KnowledgeSourceIngestionPermissionOption.GroupIds
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

**Reference:** [SearchIndexClient](/dotnet/api/azure.search.documents.indexes.searchindexclient?view=azure-dotnet-preview&preserve-view=true), [AzureBlobKnowledgeSource](/dotnet/api/azure.search.documents.indexes.models.azureblobknowledgesource?view=azure-dotnet-preview&preserve-view=true)

# [2026-04-01](#tab/2026-04-01)

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

**Reference:** [SearchIndexClient](/dotnet/api/azure.search.documents.indexes.searchindexclient?view=azure-dotnet&preserve-view=true), [AzureBlobKnowledgeSource](/dotnet/api/azure.search.documents.indexes.models.azureblobknowledgesource?view=azure-dotnet&preserve-view=true)

---

::: zone-end

::: zone pivot="python"

# [2025-11-01-preview](#tab/2025-11-01-preview)

```python
# Create a blob knowledge source
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import AzureBlobKnowledgeSource, AzureBlobKnowledgeSourceParameters, KnowledgeBaseAzureOpenAIModel, AzureOpenAIVectorizerParameters, KnowledgeSourceContentExtractionMode
from azure.search.documents.knowledgebases.models import KnowledgeSourceIngestionParameters, KnowledgeSourceAzureOpenAIVectorizer

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
            ingestion_permission_options = ["user_ids", "group_ids"]
        )
    )
)

index_client.create_or_update_knowledge_source(knowledge_source)
print(f"Knowledge source '{knowledge_source.name}' created or updated successfully.")
```

**Reference:** [SearchIndexClient](/python/api/azure-search-documents/azure.search.documents.indexes.searchindexclient)

# [2026-04-01](#tab/2026-04-01)

```python
# Create a blob knowledge source
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import AzureBlobKnowledgeSource, AzureBlobKnowledgeSourceParameters, KnowledgeBaseAzureOpenAIModel, AzureOpenAIVectorizerParameters, KnowledgeSourceContentExtractionMode
from azure.search.documents.knowledgebases.models import KnowledgeSourceIngestionParameters, KnowledgeSourceAzureOpenAIVectorizer

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
            ingestion_schedule = None
        )
    )
)

index_client.create_or_update_knowledge_source(knowledge_source)
print(f"Knowledge source '{knowledge_source.name}' created or updated successfully.")
```

**Reference:** [SearchIndexClient](/python/api/azure-search-documents/azure.search.documents.indexes.searchindexclient)

---

::: zone-end

::: zone pivot="rest"

# [2025-11-01-preview](#tab/2025-11-01-preview)

```http
### Create a blob knowledge source
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
        "ingestionPermissionOptions": ["userIds", "groupIds"]
    }
  }
}
```

**Reference:** [Knowledge Sources - Create or Update](/rest/api/searchservice/knowledge-sources/create-or-update?view=rest-searchservice-2025-11-01-preview&preserve-view=true)

# [2026-04-01](#tab/2026-04-01)

```http
### Create a blob knowledge source
PUT {{search-url}}/knowledgesources/my-blob-ks?api-version=2026-04-01
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
        "ingestionSchedule": null
    }
  }
}
```

**Reference:** [Knowledge Sources - Create or Update](/rest/api/searchservice/knowledge-sources/create-or-update?view=rest-searchservice-2026-04-01&preserve-view=true)

---

::: zone-end

> [!NOTE]
> Document-level permissions enforcement using `ingestionPermissionOptions` requires the 2025-11-01-preview API version. 2026-04-01 doesn't support this feature.

### Source-specific properties

For both the 2025-11-01-preview and 2026-04-01 API versions, you can pass the following properties to create a blob knowledge source.

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

# [2025-11-01-preview](#tab/2025-11-01-preview)

[!INCLUDE [preview ingestionParameters properties](includes/how-tos/knowledge-source-ingestion-parameters-preview.md)]

# [2026-04-01](#tab/2026-04-01)

[!INCLUDE [GA ingestionParameters properties](includes/how-tos/knowledge-source-ingestion-parameters-ga.md)]

---

## Check ingestion status

[!INCLUDE [Check ingestion status](includes/how-tos/knowledge-source-status.md)]

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

> [!TIP]
> To enforce document-level permissions, set `ingestionPermissionOptions` when you create this knowledge source, and then include the user's access token in the retrieve request. For more information, see [Enforce permissions at query time](agentic-retrieval-how-to-retrieve.md#enforce-permissions-at-query-time).

## Delete a knowledge source

[!INCLUDE [Delete a knowledge source](includes/how-tos/knowledge-source-delete.md)]

## Related content

+ [Agentic retrieval in Azure AI Search](agentic-retrieval-overview.md)
+ [Azure AI Search blob knowledge source Python sample](https://github.com/Azure/azure-search-vector-samples/blob/main/demo-python/code/knowledge/blob-knowledge-source.ipynb)
+ [Agentic RAG: Build a reasoning retrieval engine with Azure AI Search (YouTube video)](https://www.youtube.com/watch?v=PeTmOidqHM8)
+ [Azure OpenAI demo featuring agentic retrieval](https://github.com/Azure-Samples/azure-search-openai-demo)
