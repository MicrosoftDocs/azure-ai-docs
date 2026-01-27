---
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: include
ms.date: 11/14/2025
---

[!INCLUDE [Feature preview](../previews/preview-generic.md)]

Use a *OneLake knowledge source* to index and query Microsoft OneLake files in an agentic retrieval pipeline. [Knowledge sources](../../agentic-knowledge-source-overview.md) are created independently, referenced in a [knowledge base](../../agentic-retrieval-how-to-create-knowledge-base.md), and used as grounding data when an agent or chatbot calls a [retrieve action](../../agentic-retrieval-how-to-retrieve.md) at query time.

When you create a OneLake knowledge source, you specify an external data source, models, and properties to automatically generate the following Azure AI Search objects:

+ A data source that represents a lakehouse.
+ A skillset that chunks and optionally vectorizes multimodal content from the lakehouse.
+ An index that stores enriched content and meets the criteria for agentic retrieval.
+ An indexer that uses the previous objects to drive the indexing and enrichment pipeline.

The generated indexer conforms to the *OneLake indexer*, whose prerequisites, supported tasks, supported document formats, supported shortcuts, and limitations also apply to OneLake knowledge sources. For more information, see the [OneLake indexer documentation](../../search-how-to-index-onelake-files.md).

### Usage support

| [Azure portal](../../get-started-portal-agentic-retrieval.md) | [Microsoft Foundry portal](/azure/ai-foundry/agents/concepts/what-is-foundry-iq#workflow) | [.NET SDK](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/CHANGELOG.md) | [Python SDK](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [Java SDK](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [JavaScript SDK](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/search/search-documents/CHANGELOG.md) | [REST API](/rest/api/searchservice/knowledge-sources?view=rest-searchservice-2025-11-01-preview&preserve-view=true) |
|--|--|--|--|--|--|--|
| ❌ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |

## Prerequisites

+ Azure AI Search in any [region that provides agentic retrieval](../../search-region-support.md). You must have [semantic ranker enabled](../../semantic-how-to-enable-disable.md).

+ Completion of the [OneLake indexer prerequisites](../../search-how-to-index-onelake-files.md#prerequisites).

+ Completion of the [OneLake indexer data preparation](../../search-how-to-index-onelake-files.md#prepare-data-for-indexing).

+ The latest preview version of the [`azure-search-documents` client library](https://pypi.org/project/azure-search-documents/11.7.0b2/) for Python.

+ Permission to create and use objects on Azure AI Search. We recommend [role-based access](../../search-security-rbac.md), but you can use [API keys](../../search-security-api-keys.md) if a role assignment isn't feasible. For more information, see [Connect to a search service](../../search-get-started-rbac.md).

## Check for existing knowledge sources

[!INCLUDE [Check for existing knowledge sources using Python](knowledge-source-check-python.md)]

The following JSON is an example response for a OneLake knowledge source.

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

Run the following code to create a OneLake knowledge source.

```python
# Create a OneLake knowledge source
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

You can pass the following properties to create a OneLake knowledge source.

| Name | Description | Type | Editable | Required |
|--|--|--|--|--|
| `name` | The name of the knowledge source, which must be unique within the knowledge sources collection and follow the [naming guidelines](/rest/api/searchservice/naming-rules) for objects in Azure AI Search. | String | Yes | Yes |
| `description` | A description of the knowledge source. | String | Yes | No |
| `encryption` | A [customer-managed key](../../search-security-manage-encryption-keys.md) to encrypt sensitive information in both the knowledge source and the generated objects. | Object | Yes | No |
| `indexed_one_lake_parameters` | Parameters specific to OneLake knowledge sources: `fabric_workspace_id`, `lakehouse_id`, and `target_path`. | Object |  | Yes |
| `fabric_workspace_id` | The GUID of the workspace that contains the lakehouse. | String | No | Yes |
| `lakehouse_id` | The GUID of the lakehouse. | String | No | Yes |
| `target_path` | A folder or shortcut within the lakehouse. When unspecified, the entire lakehouse is indexed. | String | No | No |

### `ingestionParameters` properties

[!INCLUDE [Python ingestionParameters properties](knowledge-source-ingestion-parameters-python.md)]

## Check ingestion status

[!INCLUDE [Python knowledge source status](knowledge-source-status-python.md)]

## Review the created objects

When you create a OneLake knowledge source, your search service also creates an indexer, index, skillset, and data source. We don't recommend that you edit these objects, as introducing an error or incompatibility can break the pipeline.

After you create a knowledge source, the response lists the created objects. These objects are created according to a fixed template, and their names are based on the name of the knowledge source. You can't change the object names.

We recommend using the Azure portal to validate output creation. The workflow is:

1. Check the indexer for success or failure messages. Connection or quota errors appear here.
1. Check the index for searchable content. Use Search Explorer to run queries.
1. Check the skillset to learn how your content is chunked and optionally vectorized.
1. Check the data source for connection details. Our example uses API keys for simplicity, but you can use Microsoft Entra ID for authentication and role-based access control for authorization.

## Assign to a knowledge base

If you're satisfied with the knowledge source, continue to the next step: specify the knowledge source in a [knowledge base](../../search-agentic-retrieval-how-to-create.md).

For any knowledge base that specifies a OneLake knowledge source, be sure to set `includeReferenceSourceData` to `true`. This step is necessary for pulling the source document URL into the citation.

After the knowledge base is configured, use the [retrieve action](../../agentic-retrieval-how-to-retrieve.md) to query the knowledge source.

## Delete a knowledge source

[!INCLUDE [Delete knowledge source using Python](knowledge-source-delete-python.md)]
