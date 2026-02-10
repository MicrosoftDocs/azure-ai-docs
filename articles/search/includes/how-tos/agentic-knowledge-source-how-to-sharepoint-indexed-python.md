---
manager: nitinme
author: heidisteen
ms.author: heidist
ms.service: azure-ai-search
ms.topic: include
ms.date: 02/04/2026
---

[!INCLUDE [Feature preview](../previews/preview-generic.md)]

Use an *indexed SharePoint knowledge source* to index and query SharePoint content in an agentic retrieval pipeline. [Knowledge sources](../../agentic-knowledge-source-overview.md) are created independently, referenced in a [knowledge base](../../agentic-retrieval-how-to-create-knowledge-base.md), and used as grounding data when an agent or chatbot calls a [retrieve action](../../agentic-retrieval-how-to-retrieve.md) at query time.

When you create an indexed SharePoint knowledge source, you specify a SharePoint connection string, models, and properties to automatically generate the following Azure AI Search objects:

+ A data source that points to SharePoint sites.
+ A skillset that chunks and optionally vectorizes multimodal content.
+ An index that stores enriched content and meets the criteria for agentic retrieval.
+ An indexer that uses the previous objects to drive the indexing and enrichment pipeline.

### Usage support

| [Azure portal](../../get-started-portal-agentic-retrieval.md) | [Microsoft Foundry portal](/azure/ai-foundry/agents/concepts/what-is-foundry-iq#workflow) | [.NET SDK](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/CHANGELOG.md) | [Python SDK](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [Java SDK](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [JavaScript SDK](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/search/search-documents/CHANGELOG.md) | [REST API](/rest/api/searchservice/knowledge-sources?view=rest-searchservice-2025-11-01-preview&preserve-view=true) |
|--|--|--|--|--|--|--|
| ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |

## Prerequisites

+ Azure AI Search in any [region that provides agentic retrieval](../../search-region-support.md). You must have [semantic ranker enabled](../../semantic-how-to-enable-disable.md).

+ Completion of the [SharePoint indexer prerequisites](../../search-how-to-index-sharepoint-online.md#prerequisites).

+ Completion of the following SharePoint indexer configuration steps:

  + [Step 1: Enable a managed identity for Azure AI Search](../../search-how-to-index-sharepoint-online.md#step-1-optional-enable-system-assigned-managed-identity) (required only for secretless authentication; skip if using a client secret)
  + [Step 2: Choose either delegated or application permissions](../../search-how-to-index-sharepoint-online.md#step-2-decide-which-permissions-the-indexer-requires)
  + [Step 3: Create a Microsoft Entra application registration](../../search-how-to-index-sharepoint-online.md#step-3-create-a-microsoft-entra-application-registration) (for application permissions, you also configure a [client secret](../../search-how-to-index-sharepoint-online.md#using-client-secret) or [secretless authentication](../../search-how-to-index-sharepoint-online.md#using-secretless-authentication-to-obtain-application-tokens))

+ The latest preview version of the [`azure-search-documents` client library](https://pypi.org/project/azure-search-documents/11.7.0b2/) for Python.

+ Permission to create and use objects on Azure AI Search. We recommend [role-based access](../../search-security-rbac.md), but you can use [API keys](../../search-security-api-keys.md) if a role assignment isn't feasible. For more information, see [Connect to a search service](../../search-get-started-rbac.md).

## Check for existing knowledge sources

[!INCLUDE [Check for existing knowledge sources using Python](knowledge-source-check-python.md)]

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
                    # TRIMMED FOR BREVITY
                )
            ),
            embedding_model = KnowledgeSourceAzureOpenAIVectorizer(
                azure_open_ai_parameters=AzureOpenAIVectorizerParameters(
                    # TRIMMED FOR BREVITY
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

### Source-specific properties

You can pass the following properties to create an indexed SharePoint knowledge source.

| Name | Description | Type | Editable | Required |
|--|--|--|--|--|
| `name` | The name of the knowledge source, which must be unique within the knowledge sources collection and follow the [naming guidelines](/rest/api/searchservice/naming-rules) for objects in Azure AI Search. | String | No | Yes |
| `description` | A description of the knowledge source. | String | Yes | No |
| `encryption_key` | A [customer-managed key](../../search-security-manage-encryption-keys.md) to encrypt sensitive information in both the knowledge source and the generated objects. | Object | Yes | No |
| `indexed_share_point_parameters` | Parameters specific to indexed SharePoint knowledge sources: `connection_string`, `container_name`, and `query`. | Object | No | No |
| `connection_string` | The connection string to a SharePoint site. For more information, see [Connection string syntax](../../search-how-to-index-sharepoint-online.md#connection-string-format). | String | Yes | Yes |
| `container_name` | The SharePoint library to access. Use `defaultSiteLibrary` to index content from the site's default document library or `allSiteLibraries` to index content from every document library in the site. Ignore `useQuery` for now. | String | No | Yes |
| `query` | Optional [query](../../search-how-to-index-sharepoint-online.md#query) to filter SharePoint content. | String | Yes | No |

### `ingestion_parameters` properties

[!INCLUDE [Python ingestionParameters properties](knowledge-source-ingestion-parameters-python.md)]

## Check ingestion status

[!INCLUDE [Python knowledge source status](knowledge-source-status-python.md)]

## Review the created objects

When you create an indexed SharePoint knowledge source, your search service also creates an indexer, index, skillset, and data source. We don't recommend that you edit these objects, as introducing an error or incompatibility can break the pipeline.

After you create a knowledge source, the response lists the created objects. These objects are created according to a fixed template, and their names are based on the name of the knowledge source. You can't change the object names.

We recommend using the Azure portal to validate output creation. The workflow is:

1. Check the indexer for success or failure messages. Connection or quota errors appear here.
1. Check the index for searchable content. Use Search Explorer to run queries.
1. Check the skillset to learn how your content is chunked and optionally vectorized.
1. Check the data source for connection details. Our example uses API keys for simplicity, but you can use Microsoft Entra ID for authentication and role-based access control for authorization.

## Assign to a knowledge base

If you're satisfied with the knowledge source, continue to the next step: specify the knowledge source in a [knowledge base](../../search-agentic-retrieval-how-to-create.md).

For any knowledge base that specifies an indexed SharePoint knowledge source, be sure to set `includeReferenceSourceData` to `true`. This step is necessary for pulling the source document URL into the citation.

After the knowledge base is configured, use the [retrieve action](../../agentic-retrieval-how-to-retrieve.md) to query the knowledge source.

## Delete a knowledge source

[!INCLUDE [Delete knowledge source using Python](knowledge-source-delete-python.md)]
