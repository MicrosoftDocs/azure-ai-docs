---
title: Create a SharePoint (Indexed) Knowledge Source
description: Learn how to create an indexed SharePoint knowledge source, which ingests content from SharePoint sites into a searchable index on Azure AI Search.
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 04/14/2026
zone_pivot_groups: search-csharp-python-rest
---

# Create an indexed SharePoint knowledge source

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

Use an *indexed SharePoint knowledge source* to index and query SharePoint content in an agentic retrieval pipeline. [Knowledge sources](agentic-knowledge-source-overview.md) are created independently, referenced in a [knowledge base](agentic-retrieval-how-to-create-knowledge-base.md), and used as grounding data when an agent or chatbot calls a [retrieve action](agentic-retrieval-how-to-retrieve.md) at query time.

When you create an indexed SharePoint knowledge source, you specify a SharePoint connection string, models, and properties to automatically generate the following Azure AI Search objects:

+ A data source that points to SharePoint sites.
+ A skillset that chunks and optionally vectorizes multimodal content.
+ An index that stores enriched content and meets the criteria for agentic retrieval.
+ An indexer that uses the previous objects to drive the indexing and enrichment pipeline.

### Usage support

| [Azure portal](get-started-portal-agentic-retrieval.md) | [Microsoft Foundry portal](/azure/ai-foundry/agents/concepts/what-is-foundry-iq#workflow) | [.NET SDK](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/CHANGELOG.md) | [Python SDK](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [Java SDK](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [JavaScript SDK](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/search/search-documents/CHANGELOG.md) | [REST API](/rest/api/searchservice/knowledge-sources?view=rest-searchservice-2025-11-01-preview&preserve-view=true) |
|--|--|--|--|--|--|--|
| ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |

## Prerequisites

+ Azure AI Search in any [region that provides agentic retrieval](search-region-support.md). You must have [semantic ranker enabled](semantic-how-to-enable-disable.md).

+ Completion of the [SharePoint indexer prerequisites](search-how-to-index-sharepoint-online.md#prerequisites).

+ Completion of the following SharePoint indexer configuration steps:

  + [Step 1: Enable a managed identity for Azure AI Search](search-how-to-index-sharepoint-online.md#optional-step-1-enable-a-system-assigned-managed-identity) (required only for secretless authentication; skip if using a client secret)
  + [Step 2: Choose either delegated or application permissions](search-how-to-index-sharepoint-online.md#step-2-decide-which-permissions-the-indexer-requires)
  + [Step 3: Create a Microsoft Entra application registration](search-how-to-index-sharepoint-online.md#step-3-create-a-microsoft-entra-application-registration) (for application permissions, you also configure a [client secret](search-how-to-index-sharepoint-online.md#using-client-secret) or [secretless authentication](search-how-to-index-sharepoint-online.md#using-secretless-authentication-to-obtain-application-tokens))

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

The following JSON is an example response for an indexed SharePoint knowledge source.

```json
{
  "name": "my-indexed-sharepoint-ks",
  "kind": "indexedSharePoint",
  "description": "A sample indexed SharePoint knowledge source",
  "encryptionKey": null,
  "indexedSharePointParameters": {
    "connectionString": "<redacted>",
    "containerName": "defaultSiteLibrary",
    "query": null,
    "ingestionParameters": {
      "disableImageVerbalization": false,
      "ingestionPermissionOptions": [],
      "contentExtractionMode": "minimal",
      "identity": null,
      "embeddingModel": {
        "kind": "azureOpenAI",
        "azureOpenAIParameters": {
          "resourceUri": "<redacted>",
          "deploymentId": "text-embedding-3-large",
          "apiKey": "<redacted>",
          "modelName": "text-embedding-3-large",
          "authIdentity": null
        }
      },
      "chatCompletionModel": null,
      "ingestionSchedule": null,
      "assetStore": null,
      "aiServices": null
    },
    "createdResources": {
      "datasource": "my-indexed-sharepoint-ks-datasource",
      "indexer": "my-indexed-sharepoint-ks-indexer",
      "skillset": "my-indexed-sharepoint-ks-skillset",
      "index": "my-indexed-sharepoint-ks-index"
    }
  },
  "indexedOneLakeParameters": null
}
```

> [!NOTE]
> Sensitive information is redacted. The generated resources appear at the end of the response.

## Create a knowledge source

::: zone pivot="csharp"

Run the following code to create an indexed SharePoint knowledge source.

```csharp
// Create an IndexedSharePoint knowledge source
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

var sharePointParams = new IndexedSharePointKnowledgeSourceParameters(
    connectionString: sharePointConnectionString,
    containerName: "defaultSiteLibrary")
{
    IngestionParameters = ingestionParams
};

var knowledgeSource = new IndexedSharePointKnowledgeSource(
    name: "my-indexed-sharepoint-ks",
    indexedSharePointParameters: sharePointParams)
{
    Description = "A sample indexed SharePoint knowledge source."
};

await indexClient.CreateOrUpdateKnowledgeSourceAsync(knowledgeSource);
Console.WriteLine($"Knowledge source '{knowledgeSource.Name}' created or updated successfully.");
```

::: zone-end

::: zone pivot="python"

Run the following code to create an indexed SharePoint knowledge source.

```python
# Create an indexed SharePoint knowledge source
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import IndexedSharePointKnowledgeSource, IndexedSharePointKnowledgeSourceParameters, KnowledgeBaseAzureOpenAIModel, AzureOpenAIVectorizerParameters, KnowledgeSourceAzureOpenAIVectorizer, KnowledgeSourceContentExtractionMode, KnowledgeSourceIngestionParameters

index_client = SearchIndexClient(endpoint = "search_url", credential = AzureKeyCredential("api_key"))

knowledge_source = IndexedSharePointKnowledgeSource(
    name = "my-indexed-sharepoint-ks",
    description = "A sample indexed SharePoint knowledge source.",
    encryption_key = None,
    indexed_share_point_parameters = IndexedSharePointKnowledgeSourceParameters(
        connection_string = "connection_string",
        container_name = "defaultSiteLibrary",
        query = None,
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

Use [Knowledge Sources - Create or Update (REST API)](/rest/api/searchservice/knowledge-sources/create-or-update?view=rest-searchservice-2025-11-01-preview&preserve-view=true) to create an indexed SharePoint knowledge source.

```http
PUT {{search-url}}/knowledgesources/my-indexed-sharepoint-ks?api-version=2025-11-01-preview
api-key: {{api-key}}
Content-Type: application/json

{
    "name": "my-indexed-sharepoint-ks",
    "kind": "indexedSharePoint",
    "description": "A sample indexed SharePoint knowledge source.",
    "encryptionKey": null,
    "indexedSharePointParameters": {
        "connectionString": "{{sharepoint-connection-string}}",
        "containerName": "defaultSiteLibrary",
        "query": null,
        "ingestionParameters": {
            "identity": null,
            "embeddingModel": {
                "kind": "azureOpenAI",
                "azureOpenAIParameters": {
                    "deploymentId": "text-embedding-3-large",
                    "modelName": "text-embedding-3-large",
                    "resourceUri": "{{aoai-endpoint}}",
                    "apiKey": "{{aoai-key}}"
                }
            },
            "chatCompletionModel": null,
            "disableImageVerbalization": false,
            "ingestionSchedule": null,
            "ingestionPermissionOptions": [],
            "contentExtractionMode": "minimal"
        }
    }
}
```

::: zone-end

### Source-specific properties

You can pass the following properties to create an indexed SharePoint knowledge source.

::: zone pivot="csharp"

| Name | Description | Type | Editable | Required |
|--|--|--|--|--|
| `Name` | The name of the knowledge source, which must be unique within the knowledge sources collection and follow the [naming guidelines](/rest/api/searchservice/naming-rules) for objects in Azure AI Search. | String | No | Yes |
| `Description` | A description of the knowledge source. | String | Yes | No |
| `EncryptionKey` | A [customer-managed key](search-security-manage-encryption-keys.md) to encrypt sensitive information in both the knowledge source and the generated objects. | Object | Yes | No |
| `IndexedSharePointKnowledgeSourceParameters` | Parameters specific to indexed SharePoint knowledge sources: `ConnectionString`, `ContainerName`, and `Query`. | Object | No | No |
| `ConnectionString` | The connection string to a SharePoint site. For more information, see [Connection string syntax](search-how-to-index-sharepoint-online.md#connection-string-format). | String | Yes | Yes |
| `ContainerName` | The SharePoint library to access. Use `defaultSiteLibrary` to index content from the site's default document library or `allSiteLibraries` to index content from every document library in the site. Ignore `useQuery` for now. | String | No | Yes |
| `Query` | Optional [query](search-how-to-index-sharepoint-online.md#query) to filter SharePoint content. | String | Yes | No |

::: zone-end

::: zone pivot="python"

| Name | Description | Type | Editable | Required |
|--|--|--|--|--|
| `name` | The name of the knowledge source, which must be unique within the knowledge sources collection and follow the [naming guidelines](/rest/api/searchservice/naming-rules) for objects in Azure AI Search. | String | No | Yes |
| `description` | A description of the knowledge source. | String | Yes | No |
| `encryption_key` | A [customer-managed key](search-security-manage-encryption-keys.md) to encrypt sensitive information in both the knowledge source and the generated objects. | Object | Yes | No |
| `indexed_share_point_parameters` | Parameters specific to indexed SharePoint knowledge sources: `connection_string`, `container_name`, and `query`. | Object | No | No |
| `connection_string` | The connection string to a SharePoint site. For more information, see [Connection string syntax](search-how-to-index-sharepoint-online.md#connection-string-format). | String | Yes | Yes |
| `container_name` | The SharePoint library to access. Use `defaultSiteLibrary` to index content from the site's default document library or `allSiteLibraries` to index content from every document library in the site. Ignore `useQuery` for now. | String | No | Yes |
| `query` | Optional [query](search-how-to-index-sharepoint-online.md#query) to filter SharePoint content. | String | Yes | No |

::: zone-end

::: zone pivot="rest"

| Name | Description | Type | Editable | Required |
|--|--|--|--|--|
| `name` | The name of the knowledge source, which must be unique within the knowledge sources collection and follow the [naming guidelines](/rest/api/searchservice/naming-rules) for objects in Azure AI Search. | String | No | Yes |
| `kind` | The kind of knowledge source, which is `indexedSharePoint` in this case. | String | No | Yes |
| `description` | A description of the knowledge source. | String | Yes | No |
| `encryptionKey` | A [customer-managed key](search-security-manage-encryption-keys.md) to encrypt sensitive information in both the knowledge source and the generated objects. | Object | Yes | No |
| `indexedSharePointParameters` | Parameters specific to indexed SharePoint knowledge sources: `connectionString`, `containerName`, and `query`. | Object | No | Yes |
| `connectionString` | The connection string to a SharePoint site. For more information, see [Connection string syntax](search-how-to-index-sharepoint-online.md#connection-string-format). | String | Yes | Yes |
| `containerName` | The SharePoint library to access. Use `defaultSiteLibrary` to index content from the site's default document library or `allSiteLibraries` to index content from every document library in the site. Ignore `useQuery` for now. | String | No | Yes |
| `query` | Optional [query](search-how-to-index-sharepoint-online.md#query) to filter SharePoint content. | String | Yes | No |

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

When you create an indexed SharePoint knowledge source, your search service also creates an indexer, index, skillset, and data source. We don't recommend that you edit these objects, as introducing an error or incompatibility can break the pipeline.

After you create a knowledge source, the response lists the created objects. These objects are created according to a fixed template, and their names are based on the name of the knowledge source. You can't change the object names.

We recommend using the Azure portal to validate output creation. The workflow is:

1. Check the indexer for success or failure messages. Connection or quota errors appear here.
1. Check the index for searchable content. Use Search Explorer to run queries.
1. Check the skillset to learn how your content is chunked and optionally vectorized.
1. Check the data source for connection details. Our example uses API keys for simplicity, but you can use Microsoft Entra ID for authentication and role-based access control for authorization.

## Assign to a knowledge base

If you're satisfied with the knowledge source, continue to the next step: specify the knowledge source in a [knowledge base](agentic-retrieval-how-to-create-knowledge-base.md).

For any knowledge base that specifies an indexed SharePoint knowledge source, be sure to set `includeReferenceSourceData` to `true`. This step is necessary for pulling the source document URL into the citation.

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
