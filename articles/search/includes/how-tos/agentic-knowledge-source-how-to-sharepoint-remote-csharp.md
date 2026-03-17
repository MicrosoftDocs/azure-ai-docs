---
ms.service: azure-ai-search
ms.topic: include
ms.date: 03/17/2026
---

[!INCLUDE [Feature preview](../previews/preview-generic.md)]

A *remote SharePoint knowledge source* uses the [Copilot Retrieval API](/microsoft-365-copilot/extensibility/api/ai-services/retrieval/overview) to query textual content directly from SharePoint in Microsoft 365. No search index or connection string is needed. Only textual content is queried, and usage is billed through Microsoft 365 and a Copilot license.

To limit sites or constrain search, set a [filter expression](#filter-expression-examples) to scope by URLs, date ranges, file types, and other metadata. The caller's identity must be recognized by both the Azure tenant and the Microsoft 365 tenant because the retrieval engine queries SharePoint on behalf of the user.

Like any other knowledge source, you specify a remote SharePoint knowledge source in a [knowledge base](../../agentic-retrieval-how-to-create-knowledge-base.md) and use the results as grounding data when an agent or chatbot calls a [retrieve action](../../agentic-retrieval-how-to-retrieve.md) at query time.

### Usage support

| [Azure portal](../../get-started-portal-agentic-retrieval.md) | [Microsoft Foundry portal](/azure/ai-foundry/agents/concepts/what-is-foundry-iq#workflow) | [.NET SDK](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/CHANGELOG.md) | [Python SDK](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [Java SDK](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [JavaScript SDK](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/search/search-documents/CHANGELOG.md) | [REST API](/rest/api/searchservice/knowledge-sources?view=rest-searchservice-2025-11-01-preview&preserve-view=true) |
|--|--|--|--|--|--|--|
| ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |

## Prerequisites

+ Azure AI Search in any [region that provides agentic retrieval](../../search-region-support.md). You must have [semantic ranker enabled](../../semantic-how-to-enable-disable.md). 

+ SharePoint in a Microsoft 365 tenant that's under the same Microsoft Entra ID tenant as Azure.

+ A Microsoft 365 Copilot license for query-time access to SharePoint content.

+ The latest [`Azure.Search.Documents` preview package](https://www.nuget.org/packages/Azure.Search.Documents/11.8.0-beta.1): `dotnet add package Azure.Search.Documents --prerelease`

+ Permission to create and use objects on Azure AI Search. We recommend [role-based access](../../search-security-rbac.md), but you can use [API keys](../../search-security-api-keys.md) if a role assignment isn't feasible.

## Limitations

The following limitations in the [Copilot Retrieval API](/microsoft-365-copilot/extensibility/api/ai-services/retrieval/overview) apply to remote SharePoint knowledge sources.

+ There's no support for Copilot connectors or OneDrive content. Content is retrieved from SharePoint sites only.

+ Limit of 200 requests per user per hour.

+ Query character limit of 1,500 characters.

+ Hybrid queries are only supported for the following file extensions: .doc, .docx, .pptx, .pdf, .aspx, and .one.

+ Multimodal retrieval (nontextual content, including tables, images, and charts) isn't supported.

+ Maximum of 25 results from a query.

+ Results are returned by Copilot Retrieval API as unordered.

+ Invalid Keyword Query Language (KQL) filter expressions are ignored and the query continues to execute without the filter.

## Check for existing knowledge sources

[!INCLUDE [Check for existing knowledge sources using C#](knowledge-source-check-csharp.md)]

The following JSON is an example response for a remote SharePoint knowledge source.

```json
{
  "name": "my-sharepoint-ks",
  "kind": "remoteSharePoint",
  "description": "A sample remote SharePoint knowledge source",
  "encryptionKey": null,
  "remoteSharePointParameters": {
    "filterExpression": "filetype:docx",
    "containerTypeId": null,
    "resourceMetadata": [
      "Author",
      "Title"
    ]
  }
}
```

## Create a knowledge source

Run the following code to create a remote SharePoint knowledge source.

```csharp
// Create a remote SharePoint knowledge source
using Azure.Search.Documents.Indexes;
using Azure.Search.Documents.Indexes.Models;
using Azure.Search.Documents.KnowledgeBases.Models;
using Azure;

var indexClient = new SearchIndexClient(new Uri(searchEndpoint), credential);

var knowledgeSource = new RemoteSharePointKnowledgeSource(name: "my-remote-sharepoint-ks")
{
    Description = "This knowledge source queries .docx files in a trusted Microsoft 365 tenant.",
    RemoteSharePointParameters = new RemoteSharePointKnowledgeSourceParameters()
    {
        FilterExpression = "filetype:docx",
        ResourceMetadata = { "Author", "Title" }
    }
};

await indexClient.CreateOrUpdateKnowledgeSourceAsync(knowledgeSource);
Console.WriteLine($"Knowledge source '{knowledgeSource.Name}' created or updated successfully.");
```

### Source-specific properties

You can pass the following properties to create a remote SharePoint knowledge source.

| Name | Description | Type | Editable | Required |
|--|--|--|--|--|
| `name` | The name of the knowledge source, which must be unique within the knowledge sources collection and follow the [naming guidelines](/rest/api/searchservice/naming-rules) for objects in Azure AI Search. | String | No | Yes |
| `description` | A description of the knowledge source. | String | Yes | No |
| `encryptionKey` | A [customer-managed key](../../search-security-manage-encryption-keys.md) to encrypt sensitive information in the knowledge source. | Object | Yes | No |
| `remoteSharePointParameters` | Parameters specific to remote SharePoint knowledge sources: `filterExpression`, `resourceMetadata`, and `containerTypeId`. | Object | No | No |
| `filterExpression` | An expression written in the SharePoint [KQL](/sharepoint/dev/general-development/keyword-query-language-kql-syntax-reference), which is used to specify sites and paths to content. | String | Yes |No |
| `resourceMetadata` | A comma-delimited list of standard metadata fields: author, file name, creation date, content type, and file type. | Array | Yes | No |
| `containerTypeId` | Container ID for the SharePoint Embedded connection. When unspecified, SharePoint Online is used. | String | Yes | No |

### Filter expression examples

Not all SharePoint properties are supported in the `filterExpression`. For a list of supported properties, see the [API reference](/microsoft-365-copilot/extensibility/api/ai-services/retrieval/copilotroot-retrieval). For queryable properties, see [Queryable](/graph/connecting-external-content-manage-schema#queryable).

Learn more about [KQL filters](/microsoft-365-copilot/extensibility/api/ai-services/retrieval/copilotroot-retrieval?pivots=graph-v1#example-7-use-filter-expressions) in the syntax reference.

| Example | Filter expression |
|---------|-------------------|
| Filter to a single site by ID | `"filterExpression": "SiteID:\"00aa00aa-bb11-cc22-dd33-44ee44ee44ee\""` |
| Filter to multiple sites by ID | `"filterExpression": "SiteID:\"00aa00aa-bb11-cc22-dd33-44ee44ee44ee\" OR SiteID:\"11bb11bb-cc22-dd33-ee44-55ff55ff55ff\""` |
| Filter to files under a specific path | `"filterExpression": "Path:\"https://my-demo.sharepoint.com/sites/mysite/Shared Documents/en/mydocs\""` |
| Filter to a specific date range | `"filterExpression": "LastModifiedTime >= 2024-07-22 AND LastModifiedTime <= 2025-01-08"` |
| Filter to files of a specific file type | `"filterExpression": "FileExtension:\"docx\" OR FileExtension:\"pdf\" OR FileExtension:\"pptx\""` |
| Filter to files of a specific information protection label | `"filterExpression": "InformationProtectionLabelId:\"f0ddcc93-d3c0-4993-b5cc-76b0a283e252\""` |

## Assign to a knowledge base

If you're satisfied with the knowledge source, continue to the next step: specify the knowledge source in a [knowledge base](../../agentic-retrieval-how-to-create-knowledge-base.md).

## Query a knowledge base

After the knowledge base is configured, use the [retrieve action](../../agentic-retrieval-how-to-retrieve.md) to query SharePoint content. Remote SharePoint has source-specific behaviors for query-time filtering, query formulation, response fields, and permissions enforcement.

### Apply a KQL filter at query time

You can pass a `filterExpressionAddOn` in the `knowledgeSourceParams` on the retrieve request to apply a KQL filter at query time. If you specify `filterExpressionAddOn` on the retrieve request and a `filterExpression` on the knowledge source definition, the filters are AND'd together.

```csharp
var retrievalRequest = new KnowledgeBaseRetrievalRequest();
retrievalRequest.Messages.Add(
    new KnowledgeBaseMessage(
        content: new[] {
            new KnowledgeBaseMessageTextContent("contoso product planning")
        }
    ) { Role = "user" }
);
retrievalRequest.KnowledgeSourceParams.Add(
    new RemoteSharePointKnowledgeSourceParams("my-remote-sharepoint-ks")
    {
        FilterExpressionAddOn = "filetype:docx"
    }
);

var result = await kbClient.RetrieveAsync(
    retrievalRequest, xMsQuerySourceAuthorization: token
);
```

### Write effective queries

Queries that ask about the content itself are more effective than questions about where a file is located or when it was last updated. For example, "Where is the keynote doc for Ignite 2024" might return no results because the content itself doesn't disclose its location. A `filterExpression` on metadata is a better approach for file location or date-specific queries.

A more effective question is "What is the keynote doc for Ignite 2024". The response includes the synthesized answer, query activity and token counts, plus the URL and other metadata.

### SharePoint-specific response fields

Remote SharePoint results include fields that don't appear for other knowledge source types, such as `resourceMetadata`, `webUrl`, and `searchSensitivityLabelInfo`.

```json
{
    "resourceMetadata": {
        "Author": "Nuwan Amarathunga;Nurul Izzati",
        "Title": "Ignite 2024 Keynote Address"
    },
    "rerankerScore": 2.489522,
    "webUrl": "https://contoso-my.sharepoint.com/keynotes/Documents/Keynote-Ignite-2024.docx",
    "searchSensitivityLabelInfo": {
        "displayName": "Confidential\\Contoso Extended",
        "sensitivityLabelId": "aaaaaaaa-0b0b-1c1c-2d2d-333333333333",
        "tooltip": "Data is classified and protected.",
        "priority": 5,
        "color": "#FF8C00",
        "isEncrypted": true
    }
}
```

### Enforce permissions at query time

Remote SharePoint knowledge sources can enforce SharePoint permissions at query time. To enable this filtering, include the end user's access token in the retrieve request. The retrieval engine passes the token to the Copilot Retrieval API, which queries SharePoint and returns only content to which the user has access. SharePoint permissions and Microsoft Purview sensitivity labels are honored.

Because remote SharePoint doesn't use a search index, no ingestion-time permissions configuration is needed. The access token is the only requirement.

For instructions on passing the token, see [Enforce permissions at query time](../../agentic-retrieval-how-to-retrieve.md#enforce-permissions-at-query-time).

## Delete a knowledge source

[!INCLUDE [Delete knowledge source using C#](knowledge-source-delete-csharp.md)]
