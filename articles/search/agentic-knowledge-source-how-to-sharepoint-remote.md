---
title: Create a SharePoint (Remote) Knowledge Source
description: Learn how to create a remote SharePoint knowledge source, which tells an agentic retrieval engine in Azure AI Search to query SharePoint sites directly.
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 06/02/2026
ai-usage: ai-assisted
zone_pivot_groups: search-csharp-python-rest
---

# Create a remote SharePoint knowledge source (preview)

[!INCLUDE [Preview feature](./includes/previews/agentic-retrieval-preview-feature.md)]

> [!IMPORTANT]
> These features and functionality are part of the 2026-05-01-preview REST API. The 2026-05-01-preview is licensed to you as part of your Azure subscription and is subject to the terms applicable to "Previews" in the [Microsoft Product Terms](https://www.microsoft.com/licensing/terms/welcome/welcomepage), the [Microsoft Products and Services Data Protection Addendum](https://www.microsoft.com/licensing/docs/view/Microsoft-Products-and-Services-Data-Protection-Addendum-DPA) ("DPA"), and the [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).
>
> The 2026-05-01-preview supports connections to other Microsoft services and third-party services. Use of these services is subject to their respective terms and might result in data processing or storage outside of the Azure compliance boundary, as well as data flowing into the Azure compliance boundary.
>
> It's your responsibility to manage whether your data will flow outside of your organization's compliance and geographic boundaries and any related implications, and that appropriate permissions, boundaries, and approvals are provisioned.
>
> You're responsible for carefully reviewing and testing applications you build in the context of your specific use cases and making all appropriate decisions and customizations. This includes implementing your own responsible AI mitigations, such as metaprompts, content filters, or other safety systems, and ensuring your applications meet appropriate quality, reliability, security, and trustworthiness standards. For more information, see the [Azure AI Search Transparency Note](/azure/foundry/responsible-ai/search/transparency-note).

A *remote SharePoint knowledge source* (preview) uses the [Copilot Retrieval API](/microsoft-365-copilot/extensibility/api/ai-services/retrieval/overview) (preview) to query textual content directly from SharePoint in Microsoft 365. [Knowledge sources](agentic-knowledge-source-overview.md) are created independently, referenced in a [knowledge base](agentic-retrieval-how-to-create-knowledge-base.md), and used as grounding data when the knowledge base is [queried at runtime](agentic-retrieval-how-to-retrieve.md).

The Copilot Retrieval API searches textual content across your organization's SharePoint sites and libraries, with Microsoft 365 permissions automatically enforced. This makes remote SharePoint knowledge sources useful when your agent needs to retrieve content from SharePoint sites your users already have access to.

To limit sites or constrain search, set a [filter expression](#filter-expression-examples) to scope by URLs, date ranges, file types, and other metadata. The caller's identity must be recognized by both the Azure tenant and the Microsoft 365 tenant because the retrieval engine queries SharePoint on behalf of the user.

Unlike indexed knowledge sources, a remote SharePoint knowledge source queries textual content directly from SharePoint at retrieval time. No search index or connection string is needed. Only textual content is queried, and usage is billed through Microsoft 365 and a Copilot license.

### Usage support

| [Azure portal](get-started-portal-agentic-retrieval.md) | [Microsoft Foundry portal](/azure/ai-foundry/agents/concepts/what-is-foundry-iq#workflow) | [.NET SDK](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/CHANGELOG.md) | [Python SDK](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [Java SDK](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [JavaScript SDK](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/search/search-documents/CHANGELOG.md) | [REST API](/rest/api/searchservice/knowledge-sources?view=rest-searchservice-2026-05-01-preview&preserve-view=true) |
|--|--|--|--|--|--|--|
| ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |

## Prerequisites

+ An Azure AI Search service in any [region that provides agentic retrieval](search-region-support.md). 

+ SharePoint in a Microsoft 365 tenant that's under the same Microsoft Entra ID tenant as Azure.

+ A Microsoft 365 Copilot license for query-time access to SharePoint content.

+ Permissions to create knowledge sources. Configure [keyless authentication](search-get-started-rbac.md) with the **Search Service Contributor** role assigned to your user account (recommended) or use an [API key](search-security-api-keys.md).

::: zone pivot="csharp"

+ The latest [`Azure.Search.Documents`](https://www.nuget.org/packages/Azure.Search.Documents) preview package: `dotnet add package Azure.Search.Documents --prerelease`

::: zone-end

::: zone pivot="python"

+ The latest [`azure-search-documents`](https://pypi.org/project/azure-search-documents/#history) preview package: `pip install --pre azure-search-documents`

::: zone-end

::: zone pivot="rest"

+ The [2026-05-01-preview](/rest/api/searchservice/operation-groups?view=rest-searchservice-2026-05-01-preview&preserve-view=true) version of the Search Service REST APIs.

::: zone-end

## Limitations and considerations

The following limitations and considerations in the [Copilot Retrieval API](/microsoft-365-copilot/extensibility/api/ai-services/retrieval/overview) apply to remote SharePoint knowledge sources.

+ There's no support for Copilot connectors or OneDrive content. Content is retrieved from SharePoint sites only.

+ Limit of 200 requests per user per hour.

+ Query character limit of 1,500 characters.

+ Hybrid queries are only supported for the following file extensions: `.doc`, `.docx`, `.pptx`, `.pdf`, `.aspx`, and `.one`.

+ Multimodal retrieval (nontextual content, including tables, images, and charts) isn't supported.

+ Maximum of 25 results from a query.

+ Results are returned by the Copilot Retrieval API as unordered.

+ Invalid Keyword Query Language (KQL) filter expressions are ignored, and the query continues to execute without the filter.

## Check for existing knowledge sources

[!INCLUDE [Check for existing knowledge sources](includes/how-tos/knowledge-source-check.md)]

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

::: zone pivot="csharp"

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

**Reference:** [SearchIndexClient](/dotnet/api/azure.search.documents.indexes.searchindexclient?view=azure-dotnet-preview&preserve-view=true), [RemoteSharePointKnowledgeSource](/dotnet/api/azure.search.documents.indexes.models.remotesharepointknowledgesource?view=azure-dotnet-preview&preserve-view=true)

::: zone-end

::: zone pivot="python"

```python
# Create a remote SharePoint knowledge source
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import RemoteSharePointKnowledgeSource, RemoteSharePointKnowledgeSourceParameters

index_client = SearchIndexClient(endpoint = "search_url", credential = AzureKeyCredential("api_key"))

knowledge_source = RemoteSharePointKnowledgeSource(
    name = "my-remote-sharepoint-ks",
    description= "This knowledge source queries .docx files in a trusted Microsoft 365 tenant.",
    encryption_key = None,
    remote_share_point_parameters = RemoteSharePointKnowledgeSourceParameters(
        filter_expression = "filetype:docx",
        resource_metadata = ["Author", "Title"],
        container_type_id = None
    )
)

index_client.create_or_update_knowledge_source(knowledge_source)
print(f"Knowledge source '{knowledge_source.name}' created or updated successfully.")
```

**Reference:** [SearchIndexClient](/python/api/azure-search-documents/azure.search.documents.indexes.searchindexclient)

::: zone-end

::: zone pivot="rest"

```http
### Create a remote SharePoint knowledge source
PUT {{search-url}}/knowledgesources/my-remote-sharepoint-ks?api-version=2026-05-01-preview
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

**Reference:** [Knowledge Sources - Create or Update](/rest/api/searchservice/knowledge-sources/create-or-update?view=rest-searchservice-2026-05-01-preview&preserve-view=true)

::: zone-end

### Source-specific properties

The following properties apply to remote SharePoint knowledge sources.

::: zone pivot="csharp"

| Name | Description | Type | Editable | Required |
|--|--|--|--|--|
| `Name` | The name of the knowledge source, which must be unique within the knowledge sources collection and follow the [naming guidelines](/rest/api/searchservice/naming-rules) for objects in Azure AI Search. | String | No | Yes |
| `Description` | A description of the knowledge source. | String | Yes | No |
| `EncryptionKey` | A [customer-managed key](search-security-manage-encryption-keys.md) to encrypt sensitive information in the knowledge source. | Object | Yes | No |
| `RemoteSharePointParameters` | Parameters specific to remote SharePoint knowledge sources: `FilterExpression`, `ResourceMetadata`, and `ContainerTypeId`. | Object | No | No |
| `FilterExpression` | An expression written in the SharePoint [KQL](/sharepoint/dev/general-development/keyword-query-language-kql-syntax-reference), which is used to specify sites and paths to content. | String | Yes | No |
| `ResourceMetadata` | An array of standard metadata fields: author, file name, creation date, content type, and file type. | Array | Yes | No |
| `ContainerTypeId` | Container ID for the SharePoint Embedded connection. When unspecified, SharePoint Online is used. | String | Yes | No |

::: zone-end

::: zone pivot="python"

| Name | Description | Type | Editable | Required |
|--|--|--|--|--|
| `name` | The name of the knowledge source, which must be unique within the knowledge sources collection and follow the [naming guidelines](/rest/api/searchservice/naming-rules) for objects in Azure AI Search. | String | No | Yes |
| `description` | A description of the knowledge source. | String | Yes | No |
| `encryption_key` | A [customer-managed key](search-security-manage-encryption-keys.md) to encrypt sensitive information in the knowledge source. | Object | Yes | No |
| `remote_share_point_parameters` | Parameters specific to remote SharePoint knowledge sources: `filter_expression`, `resource_metadata`, and `container_type_id`. | Object | No | No |
| `filter_expression` | An expression written in the SharePoint [KQL](/sharepoint/dev/general-development/keyword-query-language-kql-syntax-reference), which is used to specify sites and paths to content. | String | Yes | No |
| `resource_metadata` | An array of standard metadata fields: author, file name, creation date, content type, and file type. | Array | Yes | No |
| `container_type_id` | Container ID for the SharePoint Embedded connection. When unspecified, SharePoint Online is used. | String | Yes | No |

::: zone-end

::: zone pivot="rest"

| Name | Description | Type | Editable | Required |
|--|--|--|--|--|
| `name` | The name of the knowledge source, which must be unique within the knowledge sources collection and follow the [naming guidelines](/rest/api/searchservice/naming-rules) for objects in Azure AI Search. | String | No | Yes |
| `kind` | The kind of knowledge source, which is `remoteSharePoint` in this case. | String | No | Yes |
| `description` | A description of the knowledge source. | String | Yes | No |
| `encryptionKey` | A [customer-managed key](search-security-manage-encryption-keys.md) to encrypt sensitive information in the knowledge source. | Object | Yes | No |
| `remoteSharePointParameters` | Parameters specific to remote SharePoint knowledge sources: `filterExpression`, `resourceMetadata`, and `containerTypeId`. | Object | No | No |
| `filterExpression` | An expression written in the SharePoint [KQL](/sharepoint/dev/general-development/keyword-query-language-kql-syntax-reference), which is used to specify sites and paths to content. | String | Yes | No |
| `resourceMetadata` | An array of standard metadata fields: author, file name, creation date, content type, and file type. | Array | Yes | No |
| `containerTypeId` | Container ID for the SharePoint Embedded connection. When unspecified, SharePoint Online is used. | String | Yes | No |

::: zone-end

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

If you're satisfied with the knowledge source, [add it to a knowledge base](agentic-retrieval-how-to-create-knowledge-base.md).

## Query a knowledge base

After the knowledge base is configured, [call the retrieve action or MCP endpoint](agentic-retrieval-how-to-retrieve.md) to query SharePoint content. Remote SharePoint has source-specific behaviors for query-time filtering, query formulation, response fields, and permissions enforcement.

### Apply a KQL filter at query time

::: zone pivot="csharp"

You can pass a `FilterExpressionAddOn` in the `KnowledgeSourceParams` on the retrieve request to apply a KQL filter at query time. If you specify `FilterExpressionAddOn` on the retrieve request and a `FilterExpression` on the knowledge source definition, the filters are AND'd together.

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

**Reference:** [KnowledgeBaseRetrievalClient](/dotnet/api/azure.search.documents.knowledgebases.knowledgebaseretrievalclient?view=azure-dotnet-preview&preserve-view=true), [KnowledgeBaseRetrievalRequest](/dotnet/api/azure.search.documents.knowledgebases.models.knowledgebaseretrievalrequest?view=azure-dotnet-preview&preserve-view=true)

::: zone-end

::: zone pivot="python"

You can pass a `filter_expression_add_on` in the `knowledge_source_params` on the retrieve request to apply a KQL filter at query time. If you specify `filter_expression_add_on` on the retrieve request and a `filter_expression` on the knowledge source definition, the filters are AND'd together.

```python
from azure.search.documents.knowledgebases.models import (
    KnowledgeBaseMessage,
    KnowledgeBaseMessageTextContent,
    KnowledgeBaseRetrievalRequest,
    RemoteSharePointKnowledgeSourceParams,
)

request = KnowledgeBaseRetrievalRequest(
    messages=[
        KnowledgeBaseMessage(
            role="user",
            content=[
                KnowledgeBaseMessageTextContent(
                    text="contoso product planning"
                )
            ],
        )
    ],
    knowledge_source_params=[
        RemoteSharePointKnowledgeSourceParams(
            knowledge_source_name="my-remote-sharepoint-ks",
            filter_expression_add_on="filetype:docx",
        )
    ],
)

result = kb_client.retrieve(
    retrieval_request=request,
    x_ms_query_source_authorization=token,
)
```

**Reference:** [KnowledgeBaseRetrievalClient](/python/api/azure-search-documents/azure.search.documents.knowledgebases.knowledgebaseretrievalclient), [KnowledgeBaseRetrievalRequest](/python/api/azure-search-documents/azure.search.documents.knowledgebases.models.knowledgebaseretrievalrequest)

::: zone-end

::: zone pivot="rest"

You can pass a `filterExpressionAddOn` in the `knowledgeSourceParams` on the retrieve request to apply a KQL filter at query time. If you specify `filterExpressionAddOn` on the retrieve request and a `filterExpression` on the knowledge source definition, the filters are AND'd together.

```http
### Retrieve knowledge base content
POST {{search-url}}/knowledgebases/{{knowledge-base-name}}/retrieve?api-version=2026-05-01-preview
Authorization: Bearer {{accessToken}}
Content-Type: application/json
x-ms-query-source-authorization: {{user-access-token}}

{
    "messages": [
        {
            "role": "user",
            "content": [
                { "type": "text", "text": "contoso product planning" }
            ]
        }
    ],
    "knowledgeSourceParams": [
        {
            "knowledgeSourceName": "my-remote-sharepoint-ks",
            "kind": "remoteSharePoint",
            "filterExpressionAddOn": "filetype:docx"
        }
    ]
}
```

**Reference:** [Knowledge Retrieval - Retrieve](/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2026-05-01-preview&preserve-view=true)

::: zone-end

### Write effective queries

::: zone pivot="csharp"

Queries that ask about the content itself are more effective than questions about where a file is located or when it was last updated. For example, "Where is the keynote doc for Ignite 2024" might return no results because the content itself doesn't disclose its location. A `FilterExpression` on metadata is a better approach for file location or date-specific queries.

::: zone-end

::: zone pivot="python"

Queries that ask about the content itself are more effective than questions about where a file is located or when it was last updated. For example, "Where is the keynote doc for Ignite 2024" might return no results because the content itself doesn't disclose its location. A `filter_expression` on metadata is a better approach for file location or date-specific queries.

::: zone-end

::: zone pivot="rest"

Queries that ask about the content itself are more effective than questions about where a file is located or when it was last updated. For example, "Where is the keynote doc for Ignite 2024" might return no results because the content itself doesn't disclose its location. A `filterExpression` on metadata is a better approach for file location or date-specific queries.

::: zone-end

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

For instructions on passing the token, see [Enforce permissions at query time](agentic-retrieval-how-to-retrieve.md#enforce-permissions-at-query-time-preview).

## Delete a knowledge source

[!INCLUDE [Delete a knowledge source](includes/how-tos/knowledge-source-delete.md)]

## Related content

+ [Agentic retrieval in Azure AI Search](agentic-retrieval-overview.md)
+ [What is a knowledge source?](agentic-knowledge-source-overview.md)
+ [Create a knowledge base](agentic-retrieval-how-to-create-knowledge-base.md)
+ [Query a knowledge base](agentic-retrieval-how-to-retrieve.md)
