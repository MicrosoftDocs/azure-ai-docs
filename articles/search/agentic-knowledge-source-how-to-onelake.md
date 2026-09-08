---
title: Create an Indexed OneLake Knowledge Source for Agentic Retrieval
description: Learn how to create an indexed OneLake knowledge source that defines a lakehouse, models, and enrichment pipeline for agentic retrieval in Azure AI Search.
ms.service: azure-ai-search
ms.custom: [ignite-2025, doc-kit-assisted]
ms.topic: how-to
ms.date: 09/02/2026
ai-usage: ai-assisted
zone_pivot_groups: search-csharp-python-rest
---

# Create an indexed OneLake knowledge source

[!INCLUDE [search-fiq-banner](./includes/search-fiq-banner.md)]

[!INCLUDE [GA feature](./includes/previews/agentic-retrieval-ga-feature.md)]

> [!IMPORTANT]
> These features and functionality are part of the 2026-08-01-preview REST API. The 2026-08-01-preview is licensed to you as part of your Azure subscription and is subject to the terms applicable to "Previews" in the [Microsoft Product Terms](https://www.microsoft.com/licensing/terms/welcome/welcomepage), the [Microsoft Products and Services Data Protection Addendum](https://www.microsoft.com/licensing/docs/view/Microsoft-Products-and-Services-Data-Protection-Addendum-DPA) ("DPA"), and the [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).
>
> The 2026-08-01-preview supports connections to other Microsoft services and third-party services. Use of these services is subject to their respective terms and might result in data processing or storage outside of the Azure compliance boundary, as well as data flowing into the Azure compliance boundary.
>
> The 2026-08-01-preview can't modify access permissions that were set outside of the 2026-08-01-preview. If you use the 2026-08-01-preview with access- or permission-restricted content, a timing lag will occur before the 2026-08-01-preview recognizes changes to those access or permission restrictions.
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

The generated indexer conforms to the *OneLake indexer*, whose prerequisites, supported tasks, supported document formats, supported shortcuts, and limitations also apply to OneLake knowledge sources. For more information, see the [OneLake indexer documentation](search-how-to-index-onelake-files.md) and [indexer limits](search-limits-quotas-capacity.md#indexer-limits). If the generated skillset calls an external service, that skill's input and service limits also apply.

### Usage support

| [Azure portal](get-started-portal-agentic-retrieval.md) | [Microsoft Foundry portal](/azure/ai-foundry/agents/concepts/what-is-foundry-iq#workflow) | [.NET SDK](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/CHANGELOG.md) | [Python SDK](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [Java SDK](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [JavaScript SDK](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/search/search-documents/CHANGELOG.md) | [REST API](/rest/api/searchservice/knowledge-sources) |
| -- | -- | -- | -- | -- | -- | -- |
| ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |

## Prerequisites

+ An Azure AI Search service in any [region that provides agentic retrieval](search-region-support.md).

+ Completion of the [OneLake indexer prerequisites](search-how-to-index-onelake-files.md#prerequisites).

+ Completion of the [OneLake indexer data preparation](search-how-to-index-onelake-files.md#prepare-data-for-indexing).

+ If `contentExtractionMode` is `standard`, use a Microsoft Foundry resource in a [region supported by Content Understanding in Foundry Tools](/azure/ai-services/content-understanding/language-region-support) and the `https://<resource-name>.services.ai.azure.com` endpoint. Deploy an embedding model, and deploy a multimodal chat model if you enable image verbalization.

+ Permission to create knowledge sources. Configure [keyless authentication](search-get-started-rbac.md) with the **Search Service Contributor** and **Search Index Data Contributor** roles assigned to your user account (recommended) or use an [admin API key](search-security-api-keys.md).

+ If the knowledge source specifies an Azure OpenAI model for embeddings or image verbalization, the search service must have a [managed identity](search-how-to-managed-identities.md) with **Cognitive Services User** permissions on the Microsoft Foundry resource.

::: zone pivot="csharp"

+ Required [`Azure.Search.Documents`](https://www.nuget.org/packages/Azure.Search.Documents) package:

  + For `2026-08-01-preview` features, the latest preview package: `dotnet add package Azure.Search.Documents --prerelease`

  + For `2026-04-01` features, the latest stable package: `dotnet add package Azure.Search.Documents`

+ For keyless authentication, the [`Azure.Identity`](https://www.nuget.org/packages/Azure.Identity) package: `dotnet add package Azure.Identity`

::: zone-end

::: zone pivot="python"

+ Required [`azure-search-documents`](https://pypi.org/project/azure-search-documents/#history) package:

  + For `2026-08-01-preview` features, the latest preview package: `pip install --pre azure-search-documents`

  + For `2026-04-01` features, the latest stable package: `pip install azure-search-documents`

+ For keyless authentication, the [`azure-identity`](https://pypi.org/project/azure-identity/) package: `pip install azure-identity`

::: zone-end

::: zone pivot="rest"

+ Required Search Service REST API version:

  + For preview features: [2026-08-01-preview](/rest/api/searchservice/operation-groups?view=rest-searchservice-2026-08-01-preview&preserve-view=true)

  + For generally available features: [2026-04-01](/rest/api/searchservice/operation-groups?view=rest-searchservice-2026-04-01&preserve-view=true)

+ For keyless authentication, include a [Microsoft Entra ID token](search-get-started-rbac.md?pivots=rest#get-token) in the `Authorization` header of each HTTP request.

::: zone-end

## Limitations

Private synchronization isn't supported for indexed OneLake knowledge sources. Keep `networkAccessMode` set to `public`.

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
          "modelName": "text-embedding-3-large"
        }
      },
      "chatCompletionModel": {
        "kind": "azureOpenAI",
        "azureOpenAIParameters": {
          "resourceUri": "<aoai-endpoint>",
          "deploymentId": "gpt-5-mini",
          "modelName": "gpt-5-mini"
        }
      },
      "ingestionSchedule": null,
      "aiServices": {
        "uri": "<aoai-endpoint>",
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

# [2026-08-01-preview](#tab/2026-08-01-preview)

```csharp
// Create an indexed OneLake knowledge source
using Azure.Search.Documents.Indexes;
using Azure.Search.Documents.Indexes.Models;
using Azure.Search.Documents.KnowledgeBases.Models;
using Azure.Search.Documents.Models;
using Azure.Identity;

var indexClient = new SearchIndexClient(new Uri(searchEndpoint), new DefaultAzureCredential());

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
    NetworkAccessMode = KnowledgeSourceNetworkAccessMode.Public,
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
using Azure.Identity;

var indexClient = new SearchIndexClient(new Uri(searchEndpoint), new DefaultAzureCredential());

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

# [2026-08-01-preview](#tab/2026-08-01-preview)

```python
# Create an indexed OneLake knowledge source
from azure.identity import DefaultAzureCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import IndexedOneLakeKnowledgeSource, IndexedOneLakeKnowledgeSourceParameters, KnowledgeBaseAzureOpenAIModel, AzureOpenAIVectorizerParameters, KnowledgeSourceAzureOpenAIVectorizer, KnowledgeSourceContentExtractionMode, KnowledgeSourceIngestionParameters
from azure.search.documents.knowledgebases.models import KnowledgeSourceNetworkAccessMode

index_client = SearchIndexClient(endpoint = "<search-endpoint>", credential = DefaultAzureCredential())

knowledge_source = IndexedOneLakeKnowledgeSource(
    name = "my-onelake-ks",
    description= "This knowledge source pulls content from a lakehouse.",
    encryption_key = None,
    indexed_one_lake_parameters = IndexedOneLakeKnowledgeSourceParameters(
        fabric_workspace_id = "fabric_workspace_id",
        lakehouse_id = "lakehouse_id",
        target_path = None,
        ingestion_parameters = KnowledgeSourceIngestionParameters(
            network_access_mode = KnowledgeSourceNetworkAccessMode.PUBLIC,
            identity = None,
            disable_image_verbalization = False,
            chat_completion_model = KnowledgeBaseAzureOpenAIModel(
                azure_open_ai_parameters = AzureOpenAIVectorizerParameters(
                    resource_url = "<aoai-endpoint>",
                    deployment_name = "<aoai-gpt-deployment>",
                    model_name = "<aoai-gpt-model>",
                )
            ),
            embedding_model = KnowledgeSourceAzureOpenAIVectorizer(
                azure_open_ai_parameters=AzureOpenAIVectorizerParameters(
                    resource_url = "<aoai-endpoint>",
                    deployment_name = "<aoai-embedding-deployment>",
                    model_name = "<aoai-embedding-model>",
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
from azure.identity import DefaultAzureCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import IndexedOneLakeKnowledgeSource, IndexedOneLakeKnowledgeSourceParameters, KnowledgeBaseAzureOpenAIModel, AzureOpenAIVectorizerParameters, KnowledgeSourceContentExtractionMode
from azure.search.documents.knowledgebases.models import KnowledgeSourceIngestionParameters, KnowledgeSourceAzureOpenAIVectorizer

index_client = SearchIndexClient(endpoint = "<search-endpoint>", credential = DefaultAzureCredential())

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
                    resource_url = "<aoai-endpoint>",
                    deployment_name = "<aoai-gpt-deployment>",
                    model_name = "<aoai-gpt-model>",
                )
            ),
            embedding_model = KnowledgeSourceAzureOpenAIVectorizer(
                azure_open_ai_parameters=AzureOpenAIVectorizerParameters(
                    resource_url = "<aoai-endpoint>",
                    deployment_name = "<aoai-embedding-deployment>",
                    model_name = "<aoai-embedding-model>",
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

# [2026-08-01-preview](#tab/2026-08-01-preview)

```http
### Create an indexed OneLake knowledge source
PUT {{search-endpoint}}/knowledgesources/my-onelake-ks?api-version=2026-08-01-preview
Authorization: Bearer {{search-access-token}}
Content-Type: application/json

{
    "name": "my-onelake-ks",
    "kind": "indexedOneLake",
    "description": "This knowledge source pulls content from a lakehouse.",
    "indexedOneLakeParameters": {
      "fabricWorkspaceId": "<fabric-workspace-id>",
      "lakehouseId": "<lakehouse-id>",
      "targetPath": null,
      "ingestionParameters": {
        "networkAccessMode": "public",
        "identity": null,
        "disableImageVerbalization": null,
        "chatCompletionModel": {
            "kind": "azureOpenAI",
            "azureOpenAIParameters": {
                "resourceUri": "{{aoai-endpoint}}",
                "deploymentId": "{{aoai-gpt-deployment}}",
                "modelName": "{{aoai-gpt-model}}"
            }
        },
        "embeddingModel": {
            "kind": "azureOpenAI",
            "azureOpenAIParameters": {
                "resourceUri": "{{aoai-endpoint}}",
                "deploymentId": "{{aoai-embedding-deployment}}",
                "modelName": "{{aoai-embedding-model}}"
            }
        },
        "contentExtractionMode": "minimal",
        "ingestionSchedule": null,
        "ingestionPermissionOptions": ["userIds", "groupIds"]
    }
  }
}
```

**Reference:** [Knowledge Sources - Create or Update](/rest/api/searchservice/knowledge-sources/create-or-update?view=rest-searchservice-2026-08-01-preview&preserve-view=true)

# [2026-04-01](#tab/2026-04-01)

```http
### Create an indexed OneLake knowledge source
PUT {{search-endpoint}}/knowledgesources/my-onelake-ks?api-version=2026-04-01
Authorization: Bearer {{search-access-token}}
Content-Type: application/json

{
    "name": "my-onelake-ks",
    "kind": "indexedOneLake",
    "description": "This knowledge source pulls content from a lakehouse.",
    "indexedOneLakeParameters": {
      "fabricWorkspaceId": "<fabric-workspace-id>",
      "lakehouseId": "<lakehouse-id>",
      "targetPath": null,
      "ingestionParameters": {
        "identity": null,
        "disableImageVerbalization": null,
        "chatCompletionModel": {
            "kind": "azureOpenAI",
            "azureOpenAIParameters": {
                "resourceUri": "{{aoai-endpoint}}",
                "deploymentId": "{{aoai-gpt-deployment}}",
                "modelName": "{{aoai-gpt-model}}"
            }
        },
        "embeddingModel": {
            "kind": "azureOpenAI",
            "azureOpenAIParameters": {
                "resourceUri": "{{aoai-endpoint}}",
                "deploymentId": "{{aoai-embedding-deployment}}",
                "modelName": "{{aoai-embedding-model}}"
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
> To enforce document-level permissions with `ingestionPermissionOptions`, use the 2026-08-01-preview API version. The 2026-04-01 API version doesn't support this feature.

### Use automatic per-language analyzers (preview)

[!INCLUDE [Configure automatic per-language analyzers](includes/how-tos/knowledge-source-language-analyzers.md)]

## Check ingestion status

[!INCLUDE [Check ingestion status](includes/how-tos/knowledge-source-status.md)]

## Review the generated objects

[!INCLUDE [Review the generated objects](includes/how-tos/knowledge-source-review-objects.md)]

## Assign to a knowledge base

If you're satisfied with the knowledge source, [add it to a knowledge base](agentic-retrieval-how-to-create-knowledge-base.md).

For any knowledge base that specifies an indexed OneLake knowledge source, be sure to set `includeReferenceSourceData` to `true`. This step is necessary for pulling the source document URL into the citation.

## Query a knowledge base

After you configure the knowledge base, [call the retrieve action or MCP endpoint](agentic-retrieval-how-to-retrieve.md) to query the knowledge source. Choose the configuration that matches your scenario.

### Enforce document-level permissions (preview)

To enforce document-level permissions, set `ingestionPermissionOptions` when you create this knowledge source, and then include the user's access token in the retrieve request. For more information, see [Enforce permissions at query time (preview)](agentic-retrieval-how-to-retrieve.md#enforce-permissions-at-query-time-preview).

### Surface document-embedded images (preview)

To surface document-embedded images (such as diagrams or scans) in answer synthesis responses, configure `assetStore` on this knowledge source, and then enable image serving on the knowledge base. Image serving isn't supported when `ingestionPermissionOptions` is configured. For more information, see [Surface document-embedded images in agentic retrieval (preview)](agentic-retrieval-how-to-image-serving.md).

## Delete a knowledge source

[!INCLUDE [Delete a knowledge source](includes/how-tos/knowledge-source-delete.md)]

## Related content

+ [Agentic retrieval in Azure AI Search](agentic-retrieval-overview.md)
+ [What is a knowledge source?](agentic-knowledge-source-overview.md)
+ [Create a knowledge base](agentic-retrieval-how-to-create-knowledge-base.md)
+ [Query a knowledge base](agentic-retrieval-how-to-retrieve.md)
