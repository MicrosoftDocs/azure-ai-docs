---
manager: nitinme
author: heidisteen
ms.author: heidist
ms.service: azure-ai-search
ms.topic: include
ms.date: 11/20/2025
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

+ Completion of three SharePoint indexer configuration steps:

  + [Step 1: Enable a managed identity for Azure AI Search](../../search-how-to-index-sharepoint-online.md#step-1-optional-enable-system-assigned-managed-identity)
  + [Step 2: Choose between delegated or application permissions](../../search-how-to-index-sharepoint-online.md#step-2-decide-which-permissions-the-indexer-requires)
  + [Step 3: Application registration step for Microsoft Entra ID authentication](../../search-how-to-index-sharepoint-online.md#step-3-create-a-microsoft-entra-application-registration)

+ The latest preview version of the [`Azure.Search.Documents` client library](https://www.nuget.org/packages/Azure.Search.Documents/11.8.0-beta.1) for the .NET SDK.

+ Permission to create and use objects on Azure AI Search. We recommend [role-based access](../../search-security-rbac.md), but you can use [API keys](../../search-security-api-keys.md) if a role assignment isn't feasible. For more information, see [Connect to a search service](../../search-get-started-rbac.md).

## Check for existing knowledge sources

[!INCLUDE [Check for existing knowledge sources using C#](knowledge-source-check-csharp.md)]

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

### Source-specific properties

You can pass the following properties to create an indexed SharePoint knowledge source.

| Name | Description | Type | Editable | Required |
|--|--|--|--|--|
| `Name` | The name of the knowledge source, which must be unique within the knowledge sources collection and follow the [naming guidelines](/rest/api/searchservice/naming-rules) for objects in Azure AI Search. | String | No | Yes |
| `Description` | A description of the knowledge source. | String | Yes | No |
| `EncryptionKey` | A [customer-managed key](../../search-security-manage-encryption-keys.md) to encrypt sensitive information in both the knowledge source and the generated objects. | Object | Yes | No |
| `IndexedSharePointKnowledgeSourceParameters` | Parameters specific to indexed SharePoint knowledge sources: `connectionString`, `containerName`, and `query`. | Object | No | No |
| `connectionString` | The connection string to a SharePoint site. For more information, see [Connection string syntax](../../search-how-to-index-sharepoint-online.md#connection-string-format). | String | Yes | Yes |
| `containerName` | The SharePoint library to access. Use `defaultSiteLibrary` to index content from the site's default document library or `allSiteLibraries` to index content from every document library in the site. Ignore `useQuery` for now. | String | No | Yes |
| `query` | Optional [query](../../search-how-to-index-sharepoint-online.md#query) to filter SharePoint content. | String | Yes | No |

### `ingestion_parameters` properties

[!INCLUDE [C# ingestionParameters properties](knowledge-source-ingestion-parameters-csharp.md)]

## Check ingestion status

[!INCLUDE [C# knowledge source status](knowledge-source-status-csharp.md)]

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

[!INCLUDE [Delete knowledge source using C#](knowledge-source-delete-csharp.md)]
