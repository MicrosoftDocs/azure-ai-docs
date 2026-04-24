---
title: Create an Indexed OneLake Knowledge Source for Agentic Retrieval
description: Learn how to create an indexed OneLake knowledge source in Azure AI Search. An indexed OneLake knowledge source specifies a lakehouse, models, and properties that create an enrichment pipeline for agentic retrieval workloads.
ms.service: azure-ai-search
ms.custom:
  - ignite-2025
ms.topic: how-to
ms.date: 04/14/2026
zone_pivot_groups: search-csharp-python-rest
---

# Create an indexed OneLake knowledge source

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

Use an *indexed OneLake knowledge source* to index and query Microsoft OneLake files in an agentic retrieval pipeline. [Knowledge sources](agentic-knowledge-source-overview.md) are created independently, referenced in a [knowledge base](agentic-retrieval-how-to-create-knowledge-base.md), and used as grounding data when an agent or chatbot calls a [retrieve action](agentic-retrieval-how-to-retrieve.md) at query time.

When you create an indexed OneLake knowledge source, you specify an external data source, models, and properties to automatically generate the following Azure AI Search objects:

+ A data source that represents a lakehouse.
+ A skillset that chunks and optionally vectorizes multimodal content from the lakehouse.
+ An index that stores enriched content and meets the criteria for agentic retrieval.
+ An indexer that uses the previous objects to drive the indexing and enrichment pipeline.

The generated indexer conforms to the *OneLake indexer*, whose prerequisites, supported tasks, supported document formats, supported shortcuts, and limitations also apply to OneLake knowledge sources. For more information, see the [OneLake indexer documentation](search-how-to-index-onelake-files.md).

### Usage support

| [Azure portal](get-started-portal-agentic-retrieval.md) | [Microsoft Foundry portal](/azure/ai-foundry/agents/concepts/what-is-foundry-iq#workflow) | [.NET SDK](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/CHANGELOG.md) | [Python SDK](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [Java SDK](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [JavaScript SDK](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/search/search-documents/CHANGELOG.md) | [REST API](/rest/api/searchservice/knowledge-sources?view=rest-searchservice-2025-11-01-preview&preserve-view=true) |
|--|--|--|--|--|--|--|
| ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |

## Prerequisites

+ Azure AI Search in any [region that provides agentic retrieval](search-region-support.md). You must have [semantic ranker enabled](semantic-how-to-enable-disable.md).

+ Completion of the [OneLake indexer prerequisites](search-how-to-index-onelake-files.md#prerequisites).

+ Completion of the [OneLake indexer data preparation](search-how-to-index-onelake-files.md#prepare-data-for-indexing).

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

The following JSON is an example response for an indexed OneLake knowledge source.

```json
{
  "name": "my-onelake-ks",
  "kind": "indexedOneLake",
  "description": "A sample indexed OneLake knowledge source.",
  "encryptionKey": null,
  "indexedOneLakeParameters": {
    "fabricWorkspaceId": "<REDACTED>",
    "lakehouseId": "<REDACTED>",
    "targetPath": null,
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
          "modelName": "text-embedding-3-large"
        }
      },
      "chatCompletionModel": {
        "kind": "azureOpenAI",
        "azureOpenAIParameters": {
          "resourceUri": "<REDACTED>",
          "deploymentId": "gpt-5-mini",
          "apiKey": "<REDACTED>",
          "modelName": "gpt-5-mini"
        }
      },
      "ingestionSchedule": null,
      "aiServices": {
        "uri": "<REDACTED>",
        "apiKey": "<REDACTED>"
      }
    },
    "createdResources": {
    "datasource": "my-onelake-ks-datasource",
    "indexer": "my-onelake-ks-indexer",
    "skillset": "my-onelake-ks-skillset",
    "index": "my-onelake-ks-index"
    }
  }
}
```

> [!NOTE]
> Sensitive information is redacted. The generated resources appear at the end of the response.

## Create a knowledge source

::: zone pivot="csharp"

Run the following code to create an indexed OneLake knowledge source.

```csharp
// Create an IndexedOneLake knowledge source
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

var oneLakeParams = new IndexedOneLakeKnowledgeSourceParameters(
    fabricWorkspaceId: fabricWorkspaceId,
    lakehouseId: lakehouseId)
{
    IngestionParameters = ingestionParams
};

var knowledgeSource = new IndexedOneLakeKnowledgeSource(
    name: "my-onelake-ks",
    indexedOneLakeParameters: oneLakeParams)
{
    Description = "This knowledge source pulls content from a lakehouse."
};

await indexClient.CreateOrUpdateKnowledgeSourceAsync(knowledgeSource);
Console.WriteLine($"Knowledge source '{knowledgeSource.Name}' created or updated successfully.");
```

::: zone-end

::: zone pivot="python"

Run the following code to create an indexed OneLake knowledge source.

```python
# Create an indexed OneLake knowledge source
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import IndexedOneLakeKnowledgeSource, IndexedOneLakeKnowledgeSourceParameters, KnowledgeBaseAzureOpenAIModel, AzureOpenAIVectorizerParameters, KnowledgeSourceAzureOpenAIVectorizer, KnowledgeSourceContentExtractionMode, KnowledgeSourceIngestionParameters

index_client = SearchIndexClient(endpoint = "search_url", credential = AzureKeyCredential("api_key"))

knowledge_source = IndexedOneLakeKnowledgeSource(
    name = "my-onelake-ks",
    description= "This knowledge source pulls content from a lakehouse.",
    encryption_key = None,
    indexed_one_lake_parameters = IndexedOneLakeKnowledgeSourceParameters(
        fabric_workspace_id = "fabric_workspace_id",
        lakehouse_id = "lakehouse_id",
        target_path = None,
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

Use [Knowledge Sources - Create or Update (REST API)](/rest/api/searchservice/knowledge-sources/create-or-update?view=rest-searchservice-2025-11-01-preview&preserve-view=true) to create an indexed OneLake knowledge source.

```http
PUT {{search-url}}/knowledgesources/my-onelake-ks?api-version=2025-11-01-preview
api-key: {{api-key}}
Content-Type: application/json

{
    "name": "my-onelake-ks",
    "kind": "indexedOneLake",
    "description": "This knowledge source pulls content from a lakehouse.",
    "indexedOneLakeParameters": {
      "fabricWorkspaceId": "<YOUR FABRIC WORKSPACE GUID>",
      "lakehouseId": "<YOUR LAKEHOUSE GUID>",
      "targetPath": null,
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

You can pass the following properties to create an indexed OneLake knowledge source.

::: zone pivot="csharp"

| Name | Description | Type | Editable | Required |
|--|--|--|--|--|
| `Name` | The name of the knowledge source, which must be unique within the knowledge sources collection and follow the [naming guidelines](/rest/api/searchservice/naming-rules) for objects in Azure AI Search. | String | No | Yes |
| `Description` | A description of the knowledge source. | String | Yes | No |
| `EncryptionKey` | A [customer-managed key](search-security-manage-encryption-keys.md) to encrypt sensitive information in both the knowledge source and the generated objects. | Object | Yes | No |
| `IndexedOneLakeKnowledgeSourceParameters` | Parameters specific to OneLake knowledge sources: `FabricWorkspaceId`, `LakehouseId`, and `TargetPath`. | Object |  | Yes |
| `FabricWorkspaceId` | The GUID of the workspace that contains the lakehouse. | String | No | Yes |
| `LakehouseId` | The GUID of the lakehouse. | String | No | Yes |
| `TargetPath` | A folder or shortcut within the lakehouse. When unspecified, the entire lakehouse is indexed. | String | No | No |

::: zone-end

::: zone pivot="python"

| Name | Description | Type | Editable | Required |
|--|--|--|--|--|
| `name` | The name of the knowledge source, which must be unique within the knowledge sources collection and follow the [naming guidelines](/rest/api/searchservice/naming-rules) for objects in Azure AI Search. | String | No | Yes |
| `description` | A description of the knowledge source. | String | Yes | No |
| `encryption_key` | A [customer-managed key](search-security-manage-encryption-keys.md) to encrypt sensitive information in both the knowledge source and the generated objects. | Object | Yes | No |
| `indexed_one_lake_parameters` | Parameters specific to OneLake knowledge sources: `fabric_workspace_id`, `lakehouse_id`, and `target_path`. | Object |  | Yes |
| `fabric_workspace_id` | The GUID of the workspace that contains the lakehouse. | String | No | Yes |
| `lakehouse_id` | The GUID of the lakehouse. | String | No | Yes |
| `target_path` | A folder or shortcut within the lakehouse. When unspecified, the entire lakehouse is indexed. | String | No | No |

::: zone-end

::: zone pivot="rest"

| Name | Description | Type | Editable | Required |
|--|--|--|--|--|
| `name` | The name of the knowledge source, which must be unique within the knowledge sources collection and follow the [naming guidelines](/rest/api/searchservice/naming-rules) for objects in Azure AI Search. | String | No | Yes |
| `kind` | The kind of knowledge source, which is `indexedOneLake` in this case. | String | No | Yes |
| `description` | A description of the knowledge source. | String | Yes | No |
| `encryptionKey` | A [customer-managed key](search-security-manage-encryption-keys.md) to encrypt sensitive information in both the knowledge source and the generated objects. | Object | Yes | No |
| `indexedOneLakeParameters` | Parameters specific to OneLake knowledge sources: `fabricWorkspaceId`, `lakehouseId`, and `targetPath`. | Object |  | Yes |
| `fabricWorkspaceId` | The GUID of the workspace that contains the lakehouse. | String | No | Yes |
| `lakehouseId` | The GUID of the lakehouse. | String | No | Yes |
| `targetPath` | A folder or shortcut within the lakehouse. When unspecified, the entire lakehouse is indexed. | String | No | No |

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

When you create an indexed OneLake knowledge source, your search service also creates an indexer, index, skillset, and data source. We don't recommend that you edit these objects, as introducing an error or incompatibility can break the pipeline.

After you create a knowledge source, the response lists the created objects. These objects are created according to a fixed template, and their names are based on the name of the knowledge source. You can't change the object names.

We recommend using the Azure portal to validate output creation. The workflow is:

1. Check the indexer for success or failure messages. Connection or quota errors appear here.
1. Check the index for searchable content. Use Search Explorer to run queries.
1. Check the skillset to learn how your content is chunked and optionally vectorized.
1. Check the data source for connection details. Our example uses API keys for simplicity, but you can use Microsoft Entra ID for authentication and role-based access control for authorization.

## Assign to a knowledge base

If you're satisfied with the knowledge source, continue to the next step: specify the knowledge source in a [knowledge base](agentic-retrieval-how-to-create-knowledge-base.md).

For any knowledge base that specifies an indexed OneLake knowledge source, be sure to set `includeReferenceSourceData` to `true`. This step is necessary for pulling the source document URL into the citation.

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
+ [Agentic RAG: Build a reasoning retrieval engine with Azure AI Search (YouTube video)](https://www.youtube.com/watch?v=PeTmOidqHM8)
+ [Azure OpenAI demo featuring agentic retrieval](https://github.com/Azure-Samples/azure-search-openai-demo)
