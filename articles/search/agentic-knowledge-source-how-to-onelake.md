---
title: Create an Indexed OneLake Knowledge Source for Agentic Retrieval
description: Learn how to create an indexed OneLake knowledge source in Azure AI Search. An indexed OneLake knowledge source specifies a lakehouse, models, and properties that create an enrichment pipeline for agentic retrieval workloads.
ms.service: azure-ai-search
ms.custom:
  - ignite-2025
ms.topic: how-to
ms.date: 06/02/2026
ai-usage: ai-assisted
zone_pivot_groups: search-csharp-python-rest
---

# Create an indexed OneLake knowledge source

[!INCLUDE [GA feature](./includes/previews/agentic-retrieval-ga-feature.md)]

> [!IMPORTANT]
> These features and functionality are part of the 2026-05-01-preview REST API. The 2026-05-01-preview is licensed to you as part of your Azure subscription and is subject to the terms applicable to "Previews" in the [Microsoft Product Terms](https://www.microsoft.com/licensing/terms/welcome/welcomepage), the [Microsoft Products and Services Data Protection Addendum](https://www.microsoft.com/licensing/docs/view/Microsoft-Products-and-Services-Data-Protection-Addendum-DPA) ("DPA"), and the [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).
>
> The 2026-05-01-preview supports connections to other Microsoft services and third-party services. Use of these services is subject to their respective terms and might result in data processing or storage outside of the Azure compliance boundary, as well as data flowing into the Azure compliance boundary.
>
> The 2026-05-01-preview can't modify access permissions that were set outside of the 2026-05-01-preview. If you use the 2026-05-01-preview with access- or permission-restricted content, a timing lag will occur before the 2026-05-01-preview recognizes changes to those access or permission restrictions.
>
> It's your responsibility to manage whether your data will flow outside of your organization's compliance and geographic boundaries and any related implications, and that appropriate permissions, boundaries, and approvals are provisioned.
>
> You're responsible for carefully reviewing and testing applications you build in the context of your specific use cases and making all appropriate decisions and customizations. This includes implementing your own responsible AI mitigations, such as metaprompts, content filters, or other safety systems, and ensuring your applications meet appropriate quality, reliability, security, and trustworthiness standards. For more information, see the [Azure AI Search Transparency Note](/azure/foundry/responsible-ai/search/transparency-note).

An *indexed OneLake knowledge source* ingests Microsoft OneLake files into an agentic retrieval pipeline in Azure AI Search. [Knowledge sources](agentic-knowledge-source-overview.md) are created independently, referenced in a [knowledge base](agentic-retrieval-how-to-create-knowledge-base.md), and used as grounding data when the knowledge base is [queried at runtime](agentic-retrieval-how-to-retrieve.md).

When you create an indexed OneLake knowledge source, you specify an external data source, models, and properties to automatically generate the following Azure AI Search objects:

+ A data source that represents a lakehouse.
+ A skillset that chunks and optionally vectorizes multimodal content from the lakehouse.
+ An index that stores enriched content and meets the criteria for agentic retrieval.
+ An indexer that uses the previous objects to drive the indexing and enrichment pipeline.

The generated indexer conforms to the *OneLake indexer*, whose prerequisites, supported tasks, supported document formats, supported shortcuts, and limitations also apply to OneLake knowledge sources. For more information, see the [OneLake indexer documentation](search-how-to-index-onelake-files.md).

### Usage support

| [Azure portal](get-started-portal-agentic-retrieval.md) | [Microsoft Foundry portal](/azure/ai-foundry/agents/concepts/what-is-foundry-iq#workflow) | [.NET SDK](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/CHANGELOG.md) | [Python SDK](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [Java SDK](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [JavaScript SDK](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/search/search-documents/CHANGELOG.md) | [REST API](/rest/api/searchservice/knowledge-sources) |
|--|--|--|--|--|--|--|
| ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |

## Prerequisites

+ An Azure AI Search service in any [region that provides agentic retrieval](search-region-support.md).

+ Completion of the [OneLake indexer prerequisites](search-how-to-index-onelake-files.md#prerequisites).

+ Completion of the [OneLake indexer data preparation](search-how-to-index-onelake-files.md#prepare-data-for-indexing).

+ Permissions to create knowledge sources. Configure [keyless authentication](search-get-started-rbac.md) with the **Search Service Contributor** role assigned to your user account (recommended) or use an [API key](search-security-api-keys.md).

+ If the knowledge source specifies an Azure OpenAI model for embeddings or image verbalization, the search service must have a [managed identity](search-how-to-managed-identities.md) with **Cognitive Services User** permissions on the Microsoft Foundry resource.

::: zone pivot="csharp"

+ Required [`Azure.Search.Documents`](https://www.nuget.org/packages/Azure.Search.Documents) package:

  + For 2026-05-01-preview features, the latest preview package: `dotnet add package Azure.Search.Documents --prerelease`

  + For 2026-04-01 features, the latest stable package: `dotnet add package Azure.Search.Documents`

::: zone-end

::: zone pivot="python"

+ Required [`azure-search-documents`](https://pypi.org/project/azure-search-documents/#history) package:

  + For 2026-05-01-preview features, the latest preview package: `pip install --pre azure-search-documents`

  + For 2026-04-01 features, the latest stable package: `pip install azure-search-documents`

::: zone-end

::: zone pivot="rest"

+ Required REST API version:

  + For preview features: [Search Service 2026-05-01-preview](/rest/api/searchservice/operation-groups?view=rest-searchservice-2026-05-01-preview&preserve-view=true)

  + For generally available features: [Search Service 2026-04-01](/rest/api/searchservice/operation-groups?view=rest-searchservice-2026-04-01&preserve-view=true)

::: zone-end

## Check for existing knowledge sources

[!INCLUDE [Check for existing knowledge sources](includes/how-tos/knowledge-source-check.md)]

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
          "resourceUri": "<your-foundry-resource-endpoint>",
          "deploymentId": "gpt-5-mini",
          "apiKey": "<REDACTED>",
          "modelName": "gpt-5-mini"
        }
      },
      "ingestionSchedule": null,
      "aiServices": {
        "uri": "<your-foundry-resource-endpoint>",
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

## Create a knowledge source

Run the following code to create an indexed OneLake knowledge source.

::: zone pivot="csharp"

# [2026-05-01-preview](#tab/2026-05-01-preview)

```csharp
// Create an indexed OneLake knowledge source
using Azure.Search.Documents.Indexes;
using Azure.Search.Documents.Indexes.Models;
using Azure.Search.Documents.Models;
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

**Reference:** [SearchIndexClient](/dotnet/api/azure.search.documents.indexes.searchindexclient?view=azure-dotnet-preview&preserve-view=true), [IndexedOneLakeKnowledgeSource](/dotnet/api/azure.search.documents.indexes.models.indexedonelakeknowledgesource?view=azure-dotnet-preview&preserve-view=true)

# [2026-04-01](#tab/2026-04-01)

```csharp
// Create an indexed OneLake knowledge source
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

**Reference:** [SearchIndexClient](/dotnet/api/azure.search.documents.indexes.searchindexclient?view=azure-dotnet&preserve-view=true), [IndexedOneLakeKnowledgeSource](/dotnet/api/azure.search.documents.indexes.models.indexedonelakeknowledgesource?view=azure-dotnet&preserve-view=true)

---

::: zone-end

::: zone pivot="python"

# [2026-05-01-preview](#tab/2026-05-01-preview)

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
# Create an indexed OneLake knowledge source
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import IndexedOneLakeKnowledgeSource, IndexedOneLakeKnowledgeSourceParameters, KnowledgeBaseAzureOpenAIModel, AzureOpenAIVectorizerParameters, KnowledgeSourceContentExtractionMode
from azure.search.documents.knowledgebases.models import KnowledgeSourceIngestionParameters, KnowledgeSourceAzureOpenAIVectorizer

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

# [2026-05-01-preview](#tab/2026-05-01-preview)

```http
### Create an indexed OneLake knowledge source
PUT {{search-url}}/knowledgesources/my-onelake-ks?api-version=2026-05-01-preview
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
        "ingestionPermissionOptions": ["userIds", "groupIds"]
    }
  }
}
```

**Reference:** [Knowledge Sources - Create or Update](/rest/api/searchservice/knowledge-sources/create-or-update?view=rest-searchservice-2026-05-01-preview&preserve-view=true)

# [2026-04-01](#tab/2026-04-01)

```http
### Create an indexed OneLake knowledge source
PUT {{search-url}}/knowledgesources/my-onelake-ks?api-version=2026-04-01
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
        "ingestionSchedule": null
    }
  }
}
```

**Reference:** [Knowledge Sources - Create or Update](/rest/api/searchservice/knowledge-sources/create-or-update?view=rest-searchservice-2026-04-01&preserve-view=true)

---

::: zone-end

> [!NOTE]
> Document-level permissions enforcement using `ingestionPermissionOptions` requires the 2026-05-01-preview API version. 2026-04-01 doesn't support this feature.

### Source-specific properties

The following properties apply to indexed OneLake knowledge sources.

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

# [2026-05-01-preview](#tab/2026-05-01-preview)

[!INCLUDE [preview ingestionParameters properties](includes/how-tos/knowledge-source-ingestion-parameters-preview.md)]

# [2026-04-01](#tab/2026-04-01)

[!INCLUDE [GA ingestionParameters properties](includes/how-tos/knowledge-source-ingestion-parameters-ga.md)]

---

## Check ingestion status

[!INCLUDE [Check ingestion status](includes/how-tos/knowledge-source-status.md)]

## Review the generated objects

[!INCLUDE [Review the generated objects](includes/how-tos/knowledge-source-review-objects.md)]

## Assign to a knowledge base

If you're satisfied with the knowledge source, [add it to a knowledge base](agentic-retrieval-how-to-create-knowledge-base.md).

For any knowledge base that specifies an indexed OneLake knowledge source, be sure to set `includeReferenceSourceData` to `true`. This step is necessary for pulling the source document URL into the citation.

## Query a knowledge base

After the knowledge base is configured, [call the retrieve action or MCP endpoint](agentic-retrieval-how-to-retrieve.md) to query the knowledge source. This knowledge source supports optional configurations for document-level permissions enforcement and document-embedded image surfacing.

### Enforce document-level permissions

To enforce document-level permissions, set `ingestionPermissionOptions` when you create this knowledge source, and then include the user's access token in the retrieve request. For more information, see [Enforce permissions at query time (preview)](agentic-retrieval-how-to-retrieve.md#enforce-permissions-at-query-time-preview).

### Surface document-embedded images

To surface document-embedded images (such as diagrams or scans) in answer synthesis responses, configure `assetStore` on this knowledge source, and then enable image serving on the knowledge base. For more information, see [Surface document-embedded images in agentic retrieval (preview)](agentic-retrieval-how-to-image-serving.md).

## Delete a knowledge source

[!INCLUDE [Delete a knowledge source](includes/how-tos/knowledge-source-delete.md)]

## Known errors

If you get the following similar temporary error when creating a knowledge source with `contentExtractionMode` with `Standard` as a value:
Failed to create custom analyzer 'azs_tmp': BadRequest - {"error":{"code":"InvalidRequest","message":"Invalid request.","innererror":{"code":"DefaultsNotSet","message":"Defaults have not yet been set. Call 'PATCH /contentunderstanding/defaults' first."}}}

Refer to [this Content Understanding setup](/azure/ai-services/content-understanding/tutorial/create-custom-analyzer?tabs=portal%2Cdocument&pivots=programming-language-rest#prerequisites) so you can define the default values, so you can proceed with the knowledge store creation, right after.

## Related content

+ [Agentic retrieval in Azure AI Search](agentic-retrieval-overview.md)
+ [What is a knowledge source?](agentic-knowledge-source-overview.md)
+ [Create a knowledge base](agentic-retrieval-how-to-create-knowledge-base.md)
+ [Query a knowledge base](agentic-retrieval-how-to-retrieve.md)
