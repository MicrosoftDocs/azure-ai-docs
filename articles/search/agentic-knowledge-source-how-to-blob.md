---
title: Create a Blob Knowledge Source for Agentic Retrieval
description: Learn how to create a blob knowledge source in Azure AI Search that ingests content from Azure Blob Storage or ADLS Gen2 for agentic retrieval.
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 09/02/2026
ai-usage: ai-assisted
ms.custom: doc-kit-assisted
zone_pivot_groups: search-csharp-python-rest
---

# Create a blob knowledge source from Azure Blob Storage or ADLS Gen2

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

A *blob knowledge source* ingests Azure Blob Storage or ADLS Gen2 content into an agentic retrieval pipeline in Azure AI Search. [Knowledge sources](agentic-knowledge-source-overview.md) are created independently, referenced in a [knowledge base](agentic-retrieval-how-to-create-knowledge-base.md), and used as grounding data when the knowledge base is [queried at runtime](agentic-retrieval-how-to-retrieve.md).

When you create a blob knowledge source, you specify an external data source, models, and properties to automatically generate the following Azure AI Search objects:

+ A data source that represents a blob container.
+ A skillset that chunks and optionally vectorizes multimodal content from the container.
+ An index that stores enriched content and meets the criteria for agentic retrieval.
+ An indexer that uses the previous objects to drive the indexing and enrichment pipeline.

The generated indexer conforms to the *blob indexer*, whose prerequisites, supported document formats, and limitations also apply to blob knowledge sources. For more information, see the [blob indexer documentation](search-how-to-index-azure-blob-storage.md) and [indexer limits](search-limits-quotas-capacity.md#indexer-limits). If the generated skillset calls an external service, that skill's input and service limits also apply.

> [!NOTE]
> If user access is specified at the document (blob) level in Azure Storage, a knowledge source can carry permission metadata forward to indexed content in Azure AI Search. For more information, see [ADLS Gen2 permission metadata](search-indexer-access-control-lists-and-role-based-access.md) or [Blob RBAC scopes](search-blob-indexer-role-based-access.md).

### Usage support

| [Azure portal](get-started-portal-agentic-retrieval.md) | [Microsoft Foundry portal](/azure/ai-foundry/agents/concepts/what-is-foundry-iq#workflow) | [.NET SDK](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/CHANGELOG.md) | [Python SDK](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [Java SDK](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [JavaScript SDK](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/search/search-documents/CHANGELOG.md) | [REST API](/rest/api/searchservice/knowledge-sources) |
| -- | -- | -- | -- | -- | -- | -- |
| ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |

## Prerequisites

+ An Azure AI Search service in any [region that provides agentic retrieval](search-region-support.md).

+ An [Azure Blob Storage](/azure/storage/common/storage-account-create) or [Azure Data Lake Storage (ADLS) Gen2](/azure/storage/blobs/create-data-lake-storage-account) account.

+ A blob container with [supported content types](search-how-to-index-azure-blob-storage.md#supported-document-formats) for text content. For optional image verbalization, the supported content type depends on whether your chat completion model can analyze and describe the image file.

+ If `contentExtractionMode` is `standard`, use a Microsoft Foundry resource in a [region supported by Content Understanding in Foundry Tools](/azure/ai-services/content-understanding/language-region-support) with a `https://<resource-name>.services.ai.azure.com` endpoint. The resource must have an embedding model deployment and, if you enable image verbalization, a multimodal chat model deployment.

+ Permission to create knowledge sources. Configure [keyless authentication](search-get-started-rbac.md) with the **Search Service Contributor** and **Search Index Data Contributor** roles assigned to your user account (recommended) or use an [admin API key](search-security-api-keys.md).

+ A [managed identity](search-how-to-managed-identities.md) for the search service with **Storage Blob Data Reader** at the source storage-account scope and **Cognitive Services User** on the Microsoft Foundry resource. If you configure an asset store in a different storage account, also assign **Storage Blob Data Contributor** at that storage-account scope. If the source and asset containers share an account, **Storage Blob Data Contributor** provides both source read access and asset-store read/write access.

+ If you set `networkAccessMode` to `private`, complete the following requirements:

  + Use an [S2, S3, L1, or L2 search service](search-sku-tier.md#tier-descriptions).

  + Enable a system-assigned or user-assigned managed identity on the search service, grant it the **Storage Blob Data Reader** role on the storage account, and use a `ResourceId=/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.Storage/storageAccounts/<storage-account>` connection string. For a user-assigned identity, also set `ingestionParameters.identity`.

  + Create and approve a shared private link to the storage account with the `blob` group ID. For ADLS Gen2, create and approve both `blob` and `dfs` shared private links.

  + Create and approve a shared private link for each protected model endpoint. Use the `openai_account` group ID for Azure OpenAI endpoints and `foundry_account` for Foundry resource endpoints.

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
          "modelName": "text-embedding-3-large",
          "authIdentity": null
        }
      },
      "chatCompletionModel": {
        "kind": "azureOpenAI",
        "azureOpenAIParameters": {
          "resourceUri": "<aoai-endpoint>",
          "deploymentId": "gpt-5-mini",
          "modelName": "gpt-5-mini",
          "authIdentity": null
        }
      },
      "ingestionSchedule": null,
      "assetStore": null,
      "aiServices": {
        "uri": "<aoai-endpoint>",
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

# [2026-08-01-preview](#tab/2026-08-01-preview)

```csharp
// Create a blob knowledge source
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

var blobParams = new AzureBlobKnowledgeSourceParameters(
    connectionString: connectionString,
    containerName: containerName
)
{
    IsADLSGen2 = false,
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

# [2026-08-01-preview](#tab/2026-08-01-preview)

```python
# Create a blob knowledge source
from azure.identity import DefaultAzureCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import AzureBlobKnowledgeSource, AzureBlobKnowledgeSourceParameters, KnowledgeBaseAzureOpenAIModel, AzureOpenAIVectorizerParameters, KnowledgeSourceAzureOpenAIVectorizer, KnowledgeSourceContentExtractionMode, KnowledgeSourceIngestionParameters
from azure.search.documents.knowledgebases.models import KnowledgeSourceNetworkAccessMode

index_client = SearchIndexClient(endpoint = "<search-endpoint>", credential = DefaultAzureCredential())

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
# Create a blob knowledge source
from azure.identity import DefaultAzureCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import AzureBlobKnowledgeSource, AzureBlobKnowledgeSourceParameters, KnowledgeBaseAzureOpenAIModel, AzureOpenAIVectorizerParameters, KnowledgeSourceContentExtractionMode
from azure.search.documents.knowledgebases.models import KnowledgeSourceIngestionParameters, KnowledgeSourceAzureOpenAIVectorizer

index_client = SearchIndexClient(endpoint = "<search-endpoint>", credential = DefaultAzureCredential())

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
### Create a blob knowledge source
PUT {{search-endpoint}}/knowledgesources/my-blob-ks?api-version=2026-08-01-preview
Authorization: Bearer {{search-access-token}}
Content-Type: application/json

{
  "name": "my-blob-ks",
  "kind": "azureBlob",
  "description": "This knowledge source pulls from a blob storage container.",
  "encryptionKey": null,
  "azureBlobParameters": {
  "connectionString": "ResourceId=<storage-resource-id>",
    "containerName": "<blob-container-name>",
    "folderPath": null,
    "isADLSGen2": false,
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
### Create a blob knowledge source
PUT {{search-endpoint}}/knowledgesources/my-blob-ks?api-version=2026-04-01
Authorization: Bearer {{search-access-token}}
Content-Type: application/json

{
  "name": "my-blob-ks",
  "kind": "azureBlob",
  "description": "This knowledge source pulls from a blob storage container.",
  "encryptionKey": null,
  "azureBlobParameters": {
  "connectionString": "ResourceId=<storage-resource-id>",
    "containerName": "<blob-container-name>",
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

### Restrict ingestion to a private network (preview)

Starting with the `2026-08-01-preview` API version, `networkAccessMode` controls the network environment in which the generated indexer for a blob knowledge source runs. This setting affects ingestion only and doesn't change knowledge base retrieve requests or responses.

`networkAccessMode` defaults to `public`, which preserves existing public network behavior. When `networkAccessMode` is `private`, the generated indexer runs in the [private execution environment](search-howto-run-reset-indexers.md#indexer-execution-environment). It uses approved [shared private links](search-indexer-howto-access-private.md) to access the Azure Blob Storage or ADLS Gen2 source connection and supported Azure dependencies, such as Azure OpenAI models and Microsoft Foundry resources.

To configure and verify private network access:

[!INCLUDE [Configure private network ingestion](includes/how-tos/knowledge-source-private-network.md)]

### Use automatic per-language analyzers (preview)

[!INCLUDE [Configure automatic per-language analyzers](includes/how-tos/knowledge-source-language-analyzers.md)]

## Check ingestion status

[!INCLUDE [Check ingestion status](includes/how-tos/knowledge-source-status.md)]

## Review the generated objects

[!INCLUDE [Review the generated objects](includes/how-tos/knowledge-source-review-objects.md)]

## Assign to a knowledge base

If you're satisfied with the knowledge source, [add it to a knowledge base](agentic-retrieval-how-to-create-knowledge-base.md).

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
+ [Python sample: Azure AI Search blob knowledge source](https://github.com/Azure/azure-search-vector-samples/blob/main/demo-python/code/knowledge/blob-knowledge-source.ipynb)
