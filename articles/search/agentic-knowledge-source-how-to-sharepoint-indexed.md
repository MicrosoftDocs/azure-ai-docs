---
title: Create a SharePoint (Indexed) Knowledge Source
description: Learn how to create an indexed SharePoint knowledge source, which ingests content from SharePoint sites into a searchable index on Azure AI Search.
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 08/14/2026
ai-usage: ai-assisted
ms.custom: doc-kit-assisted
zone_pivot_groups: search-csharp-python-rest
---

# Create an indexed SharePoint knowledge source (preview)

[!INCLUDE [search-fiq-banner](./includes/search-fiq-banner.md)]

[!INCLUDE [Preview feature](./includes/previews/agentic-retrieval-preview-feature.md)]

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

An *indexed SharePoint knowledge source* (preview) ingests SharePoint content into an agentic retrieval pipeline in Azure AI Search. [Knowledge sources](agentic-knowledge-source-overview.md) are created independently, referenced in a [knowledge base](agentic-retrieval-how-to-create-knowledge-base.md), and used as grounding data when the knowledge base is [queried at runtime](agentic-retrieval-how-to-retrieve.md).

When you create an indexed SharePoint knowledge source, you specify a SharePoint connection string, models, and properties to automatically generate the following Azure AI Search objects:

+ A data source that points to SharePoint sites and uses the connection string unchanged. The generated data source follows the SharePoint indexer's [`TenantId` rules](search-how-to-index-sharepoint-online.md#connection-string-format).
+ A skillset that chunks and optionally vectorizes multimodal content.
+ An index that stores enriched content and meets the criteria for agentic retrieval.
+ An indexer that uses the previous objects to drive the indexing and enrichment pipeline.

The generated indexer conforms to the *SharePoint in Microsoft 365 indexer*, whose prerequisites, supported document formats, and limitations also apply to indexed SharePoint knowledge sources. For more information, see the [SharePoint indexer documentation](search-how-to-index-sharepoint-online.md) and [indexer limits](search-limits-quotas-capacity.md#indexer-limits). If the generated skillset calls an external service, that skill's input and service limits also apply.

### Usage support

| [Azure portal](get-started-portal-agentic-retrieval.md) | [Microsoft Foundry portal](/azure/ai-foundry/agents/concepts/what-is-foundry-iq#workflow) | [.NET SDK](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/CHANGELOG.md) | [Python SDK](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [Java SDK](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [JavaScript SDK](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/search/search-documents/CHANGELOG.md) | [REST API](/rest/api/searchservice/knowledge-sources?view=rest-searchservice-2026-08-01-preview&preserve-view=true) |
| -- | -- | -- | -- | -- | -- | -- |
| ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |

## Prerequisites

+ An Azure AI Search service in any [region that provides agentic retrieval](search-region-support.md).

+ Completion of the [SharePoint indexer prerequisites](search-how-to-index-sharepoint-online.md#prerequisites).

+ Completion of the following SharePoint indexer configuration steps:

  + [Step 1: Enable a managed identity for Azure AI Search](search-how-to-index-sharepoint-online.md#optional-step-1-enable-a-system-assigned-managed-identity) (required only for secretless authentication; skip if using a client secret)

  + [Step 2: Choose either delegated or application permissions](search-how-to-index-sharepoint-online.md#step-2-decide-which-permissions-the-indexer-requires)

  + [Step 3: Create a Microsoft Entra application registration](search-how-to-index-sharepoint-online.md#step-3-create-a-microsoft-entra-application-registration) (for application permissions, you also configure a [client secret](search-how-to-index-sharepoint-online.md#using-client-secret) or [secretless authentication](search-how-to-index-sharepoint-online.md#using-secretless-authentication-to-obtain-application-tokens))

+ If `contentExtractionMode` is `standard`, use a Microsoft Foundry resource in a [region supported by Content Understanding in Foundry Tools](/azure/ai-services/content-understanding/language-region-support) and the `https://<resource-name>.services.ai.azure.com` endpoint. Deploy an embedding model, and deploy a multimodal chat model if you enable image verbalization.

+ Permission to create knowledge sources. Configure [keyless authentication](search-get-started-rbac.md) with the **Search Service Contributor** and **Search Index Data Contributor** roles assigned to your user account (recommended) or use an [admin API key](search-security-api-keys.md).

+ If the knowledge source specifies an Azure OpenAI model for embeddings or image verbalization, the search service must have a [managed identity](search-how-to-managed-identities.md) with **Cognitive Services User** permissions on the Microsoft Foundry resource.

+ If you set `networkAccessMode` to `private`, complete the following requirements:

  + Use an [S2, S3, L1, or L2 search service](search-sku-tier.md#tier-descriptions).

  + Keep the SharePoint connection string, Microsoft Entra application, and SharePoint permissions described in the previous prerequisites. SharePoint Online isn't a supported shared private link target, so private mode doesn't make this source connection private.

  + For each protected model endpoint, enable a managed identity on the search service, grant it the **Cognitive Services User** role on the resource, and create and approve a shared private link. Use the `openai_account` group ID for Azure OpenAI endpoints and `foundry_account` for Foundry resource endpoints.

::: zone pivot="csharp"

+ The latest [`Azure.Search.Documents`](https://www.nuget.org/packages/Azure.Search.Documents) preview package: `dotnet add package Azure.Search.Documents --prerelease`

+ For keyless authentication, the [`Azure.Identity`](https://www.nuget.org/packages/Azure.Identity) package: `dotnet add package Azure.Identity`

::: zone-end

::: zone pivot="python"

+ The latest [`azure-search-documents`](https://pypi.org/project/azure-search-documents/#history) preview package: `pip install --pre azure-search-documents`

+ For keyless authentication, the [`azure-identity`](https://pypi.org/project/azure-identity/) package: `pip install azure-identity`

::: zone-end

::: zone pivot="rest"

+ The [2026-08-01-preview](/rest/api/searchservice/operation-groups?view=rest-searchservice-2026-08-01-preview&preserve-view=true) version of the Search Service REST API.

+ For keyless authentication, include a [Microsoft Entra ID token](search-get-started-rbac.md?pivots=rest#get-token) in the `Authorization` header of each HTTP request.

::: zone-end

## Check for existing knowledge sources

[!INCLUDE [Check for existing knowledge sources](includes/how-tos/knowledge-source-check.md)]

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

## Create a knowledge source

Run the following code to create an indexed SharePoint knowledge source.

::: zone pivot="csharp"

```csharp
// Create an IndexedSharePoint knowledge source
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
    NetworkAccessMode = KnowledgeSourceNetworkAccessMode.Public,
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

**Reference:** [SearchIndexClient](/dotnet/api/azure.search.documents.indexes.searchindexclient?view=azure-dotnet-preview&preserve-view=true), [IndexedSharePointKnowledgeSource](/dotnet/api/azure.search.documents.indexes.models.indexedsharepointknowledgesource?view=azure-dotnet-preview&preserve-view=true)

::: zone-end

::: zone pivot="python"

```python
# Create an indexed SharePoint knowledge source
from azure.identity import DefaultAzureCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import IndexedSharePointKnowledgeSource, IndexedSharePointKnowledgeSourceParameters, KnowledgeBaseAzureOpenAIModel, AzureOpenAIVectorizerParameters, KnowledgeSourceContentExtractionMode
from azure.search.documents.knowledgebases.models import KnowledgeSourceIngestionParameters, KnowledgeSourceNetworkAccessMode, KnowledgeSourceAzureOpenAIVectorizer

index_client = SearchIndexClient(endpoint = "<search-endpoint>", credential = DefaultAzureCredential())

knowledge_source = IndexedSharePointKnowledgeSource(
    name = "my-indexed-sharepoint-ks",
    description = "A sample indexed SharePoint knowledge source.",
    encryption_key = None,
    indexed_share_point_parameters = IndexedSharePointKnowledgeSourceParameters(
        connection_string = "connection_string",
        container_name = "defaultSiteLibrary",
        query = None,
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
            ingestion_permission_options = None
        )
    )
)

index_client.create_or_update_knowledge_source(knowledge_source)
print(f"Knowledge source '{knowledge_source.name}' created or updated successfully.")
```

**Reference:** [SearchIndexClient](/python/api/azure-search-documents/azure.search.documents.indexes.searchindexclient)

::: zone-end

::: zone pivot="rest"

```http
### Create an indexed SharePoint knowledge source
PUT {{search-endpoint}}/knowledgesources/my-indexed-sharepoint-ks?api-version=2026-08-01-preview
Authorization: Bearer {{search-access-token}}
Content-Type: application/json

{
    "name": "my-indexed-sharepoint-ks",
    "kind": "indexedSharePoint",
    "description": "A sample indexed SharePoint knowledge source.",
    "encryptionKey": null,
    "indexedSharePointParameters": {
        "connectionString": "{{sharepoint-federated-connection-string}}",
        "containerName": "defaultSiteLibrary",
        "query": null,
        "ingestionParameters": {
            "networkAccessMode": "public",
            "identity": null,
            "embeddingModel": {
                "kind": "azureOpenAI",
                "azureOpenAIParameters": {
                    "deploymentId": "text-embedding-3-large",
                    "modelName": "text-embedding-3-large",
                    "resourceUri": "{{aoai-endpoint}}"
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

**Reference:** [Knowledge Sources - Create or Update](/rest/api/searchservice/knowledge-sources/create-or-update?view=rest-searchservice-2026-08-01-preview&preserve-view=true)

::: zone-end

### Protect Azure dependencies during ingestion

Starting with the `2026-08-01-preview` API version, `networkAccessMode` controls the network environment in which the generated indexer for an indexed SharePoint knowledge source runs. This setting affects ingestion only and doesn't change knowledge base retrieve requests or responses.

`networkAccessMode` defaults to `public`, which preserves existing public network behavior. When `networkAccessMode` is `private`, the generated indexer runs in the [private execution environment](search-howto-run-reset-indexers.md#indexer-execution-environment). It uses approved [shared private links](search-indexer-howto-access-private.md) to access supported Azure dependencies, such as Azure OpenAI models and Microsoft Foundry resources.

> [!IMPORTANT]
> For indexed SharePoint knowledge sources, private mode applies only to supported Azure dependencies. SharePoint Online isn't a supported shared private link target, so the SharePoint source connection remains public.

To configure and verify private access to supported Azure dependencies:

[!INCLUDE [Configure private network ingestion](includes/how-tos/knowledge-source-private-network.md)]

## Check ingestion status

[!INCLUDE [Check ingestion status](includes/how-tos/knowledge-source-status.md)]

## Review the generated objects

[!INCLUDE [Review the generated objects](includes/how-tos/knowledge-source-review-objects.md)]

## Assign to a knowledge base

If you're satisfied with the knowledge source, [add it to a knowledge base](agentic-retrieval-how-to-create-knowledge-base.md).

For any knowledge base that specifies an indexed SharePoint knowledge source, be sure to set `includeReferenceSourceData` to `true`. This step is necessary for pulling the source document URL into the citation.

## Query a knowledge base

After you configure the knowledge base, [call the retrieve action or MCP endpoint](agentic-retrieval-how-to-retrieve.md) to query the knowledge source. Choose the configuration that matches your scenario.

### Enforce document-level permissions

To enforce document-level permissions, set `ingestionPermissionOptions` when you create this knowledge source, and then include the user's access token in the retrieve request. For more information, see [Enforce permissions at query time (preview)](agentic-retrieval-how-to-retrieve.md#enforce-permissions-at-query-time-preview).

For missing, unexpected, or failed results from an indexed SharePoint permission query, see [Troubleshoot SharePoint permission filtering](troubleshoot-sharepoint-query-permission-filtering.md).

### Surface document-embedded images

To surface document-embedded images (such as diagrams or scans) in answer synthesis responses, configure `assetStore` on this knowledge source, and then enable image serving on the knowledge base. Image serving isn't supported when `ingestionPermissionOptions` is configured. For more information, see [Surface document-embedded images in agentic retrieval (preview)](agentic-retrieval-how-to-image-serving.md).

## Delete a knowledge source

[!INCLUDE [Delete a knowledge source](includes/how-tos/knowledge-source-delete.md)]

## Known errors

The generated SharePoint data source and indexer use the same Microsoft Entra tenant validation and authentication behavior as directly configured SharePoint indexers. For tenant-related failures, review the [generated indexer's status and execution history](search-monitor-indexers.md), and then follow the [`Invalid AAD tenant` remediation](cognitive-search-common-errors-warnings.md#error-invalid-aad-tenant).

## Related content

+ [Agentic retrieval in Azure AI Search](agentic-retrieval-overview.md)
+ [What is a knowledge source?](agentic-knowledge-source-overview.md)
+ [Create a knowledge base](agentic-retrieval-how-to-create-knowledge-base.md)
+ [Query a knowledge base](agentic-retrieval-how-to-retrieve.md)
