---
ms.service: azure-ai-search
ms.topic: include
ms.date: 11/14/2025
---

[!INCLUDE [Feature preview](../previews/preview-generic.md)]

A *remote SharePoint knowledge source* uses the [Copilot Retrieval API](/microsoft-365-copilot/extensibility/api/ai-services/retrieval/overview) to query textual content directly from SharePoint in Microsoft 365, returning results to the agentic retrieval engine for merging, ranking, and response formulation. There's no search index used by this knowledge source, and only textual content is queried.

At query time, the remote SharePoint knowledge source calls the Copilot Retrieval API on behalf of the user identity, so no connection strings are needed in the knowledge source definition. All content to which a user has access is in-scope for knowledge retrieval. To limit sites or constrain search, set a [filter expression](/sharepoint/dev/general-development/keyword-query-language-kql-syntax-reference). Your Azure tenant and the Microsoft 365 tenant must use the same Microsoft Entra ID tenant, and the caller's identity must be recognized by both tenants.

+ You can use filters to scope search by URLs, date ranges, file types, and other metadata.

+ SharePoint permissions and Purview labels are honored in requests for content.

+ Usage is billed through Microsoft 365 and a Copilot license.

Like any other knowledge source, you specify a remote SharePoint knowledge source in a [knowledge base](../../agentic-retrieval-how-to-create-knowledge-base.md) and use the results as grounding data when an agent or chatbot calls a [retrieve action](../../agentic-retrieval-how-to-retrieve.md) at query time.

### Usage support

| [Azure portal](../../get-started-portal-agentic-retrieval.md) | [Microsoft Foundry portal](/azure/ai-foundry/agents/concepts/what-is-foundry-iq#workflow) | [.NET SDK](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/CHANGELOG.md) | [Python SDK](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [Java SDK](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [JavaScript SDK](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/search/search-documents/CHANGELOG.md) | [REST API](/rest/api/searchservice/knowledge-sources?view=rest-searchservice-2025-11-01-preview&preserve-view=true) |
|--|--|--|--|--|--|--|
| ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |

## Prerequisites

+ Azure AI Search in any [region that provides agentic retrieval](../../search-region-support.md). You must have [semantic ranker enabled](../../semantic-how-to-enable-disable.md). 

+ SharePoint in a Microsoft 365 tenant that's under the same Microsoft Entra ID tenant as Azure.

+ A personal access token for local development or a user's identity from a client application.

+ The [2025-11-01-preview](/rest/api/searchservice/operation-groups?view=rest-searchservice-2025-11-01-preview&preserve-view=true) version of the Search Service REST APIs.

+ Permission to create and use objects on Azure AI Search. We recommend [role-based access](../../search-security-rbac.md), but you can use [API keys](../../search-security-api-keys.md) if a role assignment isn't feasible.

For local development, the agentic retrieval engine uses your access token to call SharePoint on your behalf. For more information about using a personal access token on requests, see [Connect to Azure AI Search](../../search-get-started-rbac.md).

<!-- invalid filter expression will return a 400 soon, so we should be able to remove this limitation -->

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

[!INCLUDE [Check for existing knowledge sources using REST](knowledge-source-check-rest.md)]

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

Use [Knowledge Sources - Create or Update (REST API)](/rest/api/searchservice/knowledge-sources/create-or-update?view=rest-searchservice-2025-11-01-preview&preserve-view=true) to create a remote SharePoint knowledge source.

[API keys](../../search-security-api-keys.md) are used for your client connection to Azure AI Search and Azure OpenAI. Your access token is used by Azure AI Search to connect to SharePoint in Microsoft 365 on your behalf. You can only retrieve content that you're permitted to access. For more information about getting a personal access token and other values, see [Connect to Azure AI Search](../../search-get-started-rbac.md).

> [!NOTE]
> You can also use your personal access token to access Azure AI Search and Azure OpenAI if you [set up role assignments on each resource](../../search-security-rbac.md). Using API keys allows you to omit this step in this example.

```http
POST {{search-url}}/knowledgesources/my-remote-sharepoint-ks?api-version=2025-11-01-preview
api-key: {{api-key}}
Content-Type: application/json

{
    "name": "my-remote-sharepoint-ks",
    "kind": "remoteSharePoint",
    "description": "This knowledge source queries .docx files in a trusted Microsoft 365 tenant.",
    "encryptionKey": null,
    "remoteSharePointParameters": {
        "filterExpression": "filetype:docx",
        "resourceMetadata": [ "Author", "Title" ],
        "containerTypeId": null
    }
}
```

<!-- Should we include a response and do we need to say anything about purview sensitivity labels? -->

### Source-specific properties

You can pass the following properties to create a remote SharePoint knowledge source.

| Name | Description | Type | Editable | Required |
|--|--|--|--|--|
| `name` | The name of the knowledge source, which must be unique within the knowledge sources collection and follow the [naming guidelines](/rest/api/searchservice/naming-rules) for objects in Azure AI Search. | String | No | Yes |
| `kind` | The kind of knowledge source, which is `remoteSharePoint` in this case. | String | No | Yes |
| `description` | A description of the knowledge source. | String | Yes | No |
| `encryptionKey` | A [customer-managed key](../../search-security-manage-encryption-keys.md) to encrypt sensitive information in the knowledge source. | Object | Yes | No |
| `remoteSharePointParameters` | Parameters specific to remote SharePoint knowledge sources: `filterExpression`, `resourceMetadata`, and `containerTypeId`. | Object | No | No |
| `filterExpression` | An expression written in the SharePoint [KQL](/sharepoint/dev/general-development/keyword-query-language-kql-syntax-reference), which is used to specify sites and paths to content. | String | Yes |No |
| `resourceMetadata` | A comma-delimited list of standard metadata fields: author, file name, creation date, content type, and file type. | Array | Yes | No |
| `containerTypeId` | Container ID for the SharePoint Embedded connection. When unspecified, SharePoint Online is used. | String | Yes | No |

### Filter expression examples

Not all SharePoint properties are supported in the `filterExpression`. For a list of supported properties, see the [API reference](/microsoft-365-copilot/extensibility/api/ai-services/retrieval/copilotroot-retrieval). Here's some more information about queryable properties that you can use in filter: [queryable properties](/graph/connecting-external-content-manage-schema#queryable).

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

If you're satisfied with the knowledge source, continue to the next step: specify the knowledge source in a [knowledge base](../../search-agentic-retrieval-how-to-create.md).

After the knowledge base is configured, use the [retrieve action](../../agentic-retrieval-how-to-retrieve.md) to query the knowledge source.

## Permissions and retrieval

Remote SharePoint enforces SharePoint permissions at query time. The retrieval engine uses the caller's access token, passed via the `x-ms-query-source-authorization` header, to query SharePoint content on behalf of the user through the Copilot Retrieval API. Only content the user has access to is returned. SharePoint permissions and Purview sensitivity labels are honored in requests for content.

Because remote SharePoint doesn't use a search index, no ingestion-time permissions configuration is needed. The `x-ms-query-source-authorization` header is the only requirement.

For instructions on calling the retrieve action with the authorization header, see [Enforce permissions at query time](../../agentic-retrieval-how-to-retrieve.md#enforce-permissions-at-query-time).

## Delete a knowledge source

[!INCLUDE [Delete knowledge source using REST](knowledge-source-delete-rest.md)]
