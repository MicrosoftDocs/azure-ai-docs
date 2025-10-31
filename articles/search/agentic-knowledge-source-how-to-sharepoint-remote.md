---
title: Create a SharePoint (Remote) Knowledge Source
titleSuffix: Azure AI Search
description: A remote Sharepoint knowledge source tells the agentic retrieval engine to query SharePoint sites directly.
manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 10/31/2025
---

# Create a remote SharePoint knowledge source

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

A *remote SharePoint knowledge source* uses the [Copilot Retrieval API](/microsoft-365-copilot/extensibility/api/ai-services/retrieval/overview) to query textual content directly from SharePoint and OneDrive, returning results to the agentic retrieval engine for merging, ranking, and response formulation. There's no search index used by this knowledge source, and only textual content is queried.

At query time, the knowledge source uses the identity of the caller to retrieve content from Microsoft 365. There's no SharePoint endpoint in the knowledge source, but your Azure tenant and the Microsoft 365 tenant must use the same Microsoft Entra ID tenant, and the caller's identity must be recognized by both tenants.

+ You can use filters to scope search by URLs, date ranges, file types, and other metadata.

+ SharePoint permissions and Purview labels are honored in requests for content.

+ Usage is billed through Microsoft 365 and a Copilot license.

Like any other knowledge source, you specify a remote SharePoint knowledge source in a [knowledge base](agentic-retrieval-how-to-create-knowledge-base.md), and use the results as grounding data when an agent or chatbot calls a [retrieve](/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2025-11-01-preview&preserve-view=true) action at query time.

## Prerequisites

+ Azure AI Search in an Azure tenant, configured for Microsoft Entra ID authentication.

+ SharePoint Online in a Microsoft 365 tenant, under the same Microsoft Entra ID tenant as Azure.

+ A personal access token for local development or a user's identity from a client application. 

For local developement, the agentic retrieval engine uses your access token to call SharePoint on your behalf. For more information about using a personal access token on requests, see [Connect to Azure AI Search](search-get-started-rbac.md).

To try the examples in this article, we recommend [Visual Studio Code](https://code.visualstudio.com/download) with the [REST Client extension](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) for sending preview REST API calls to Azure AI Search. Currently, there's no portal support.

## Limitations

The following limitations in the [Copilot Retrieval API](/microsoft-365-copilot/extensibility/api/ai-services/retrieval/overview) apply to remote SharePoint knowledge sources.

+ There's no support for Copilot connectors. Content is retrieved from OneDrive and SharePoint.

+ Limit of 200 requests per user per hour.

+ Query character limit of 1,500 characters.

+ Hybrid queries are only supported for the following file extensions: .doc, .docx, .pptx, .pdf, .aspx, and .one.

+ Multimodal retrieval (nontextual content, including tables, images, and charts) isn't supported.

+ Maximum of 25 results from a query.

+ Results are returned by Copilot Retrieval API as unordered.

+ Invalid filter expressions (Keyword Query Language KQL) are ignored and the query continues to execute without the filter.

## Check for existing knowledge sources

[!INCLUDE [Check for existing knowledge sources](includes/how-tos/knowledge-source-check-rest.md)]

The following JSON is an example response for a remote SharePoint knowledge source. Notice that the knowledge source specifies a single index name and which fields in the index to include in the query.

```json
{
  "name": "my-sharepoint-ks",
  "kind": "remoteSharePoint",
  "description": "A sample remote sharepoint knowledge source",
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

To create a remote SharePoint knowledge source:

1. Set environment variables at the top of your file.

    ```http
    @search-url = <YOUR SEARCH SERVICE URL>
    @api-key = <YOUR SEARCH SERVICE ADMIN API KEY>
    @aoai-endpoint = <YOUR AZURE OPENAI RESOURCE PROVIDING A CHAT COMPLETION MODEL>
    @aoai-key = <YOUR AZURE OPENAI KEY>
    @access-token = <YOUR PERSONAL ACCESS TOKEN USED FOR RETRIEVING PERMITTED CONTENT ON SHAREPOINT>
    ```

    API keys are used for your client connection to Azure AI Search and Azure OpenAI. Your access token is used by Azure AI Search to connect to SharePoint Online on your behalf. You can only retrieve content that you're permitted to access. For more information about getting a personal access token and other values, see [Connect to Azure AI Search](search-get-started-rbac.md). You can also use your personal access token to access Azure AI Search and Azure OpenAI if you [set up role assignments on each resource](search-security-rbac.md). Using keys allows you to omit this step.

1. Use the 2025-11-01-preview of [Knowledge Sources - Create or Update (REST API)](/rest/api/searchservice/knowledge-sources/create-or-update?view=rest-searchservice-2025-11-01-preview&preserve-view=true) or an Azure SDK preview package that provides equivalent functionality to formulate the request.

    ```http
    POST {{search-url}}/knowledgesources/my-remote-sharepoint-ks?api-version=2025-11-01-preview
    api-key: {{api-key}}
    Content-Type: application/json
    
    {
        "name": "my-remote-sharepoint-ks",
        "kind": "remoteSharePoint",
        "description": "This knowledge source queries a remote SharePoint site for text and images.",
        "encryptionKey": null,
        "remoteSharePointParameters": {
            "filterExpression": "filetype:docx",
            "resourceMetadata": [ "Author", "Title" ],
            "containerTypeId": null
        }
    }
    ```

1. Select **Send Request**.

<!-- Should we include a response and do we need to say anything about purview sensitivity labels? -->

### Source-specific properties

You can pass the following properties to create a remote SharePoint knowledge source.

| Name | Description | Type | Required |
|--|--|--|--|
| `name` | The name of the knowledge source, which must be unique within the knowledge sources collection and follow the [naming guidelines](/rest/api/searchservice/naming-rules) for objects in Azure AI Search. | String | Yes |
| `kind` | The kind of knowledge source, which is `remoteSharePoint` in this case. | String | Yes |
| `description` | A description of the knowledge source. | String | No |
| `encryptionKey` | A [customer-managed key](search-security-manage-encryption-keys.md) to encrypt sensitive information in both the knowledge source and the generated objects. | Object | No |
| `remoteSharePointParameters` | Parameters specific to remote SharePoint knowledge sources: `filterExpression`, `resourceMetadata`, and `containerTypeId`. | Object | No |
| `filterExpression` | An expression written in the SharePoint in Keyword Query Language (KQL), used to specify sites and paths to content. | String | No |
| `resourceMetadata` | A comma-delimited list of the standard metadata fields: author, file name, creation date, content type, and file type. | Array | No |
| `containerTypeId` | Ignored for now. | String| No |

<!-- SharePoint embedded is containers. Many moving parts. Defer for now. -->

### Filter expression examples

Learn more about the full [Keyword Query Language (KQL)](/microsoft-365-copilot/extensibility/api/ai-services/retrieval/copilotroot-retrieval?pivots=graph-v1#example-7-use-filter-expressions) syntax reference.

+ Filter to a single site by ID: `"filterExpression": "SiteID:\"00aa00aa-bb11-cc22-dd33-44ee44ee44ee\""`

+ Filter to multiple sites by ID: `"filterExpression": "SiteID:\"00aa00aa-bb11-cc22-dd33-44ee44ee44ee\" OR SiteID:\"11bb11bb-cc22-dd33-ee44-55ff55ff55ff\""`

+ Filter to files under a specific path: `"filterExpression": "Path:\"https://my-demo.sharepoint.com/sites/miml/Shared Documents/en/mydocs\""`

+ Filter to a specific date range: `"filterExpression": "LastModifiedTime >= 2024-07-22 AND LastModifiedTime <= 2025-01-08"`

+ Filter to files of a specific file type: `"filterExpression": "FileExtension:\"docx\" OR FileExtension:\"pdf\" OR FileExtension:\"pptx\""`

+ Filter to files of a specific information protection label: `"filterExpression": "InformationProtectionLabelId:\"f0ddcc93-d3c0-4993-b5cc-76b0a283e252\""`

## Assign to a knowledge base

If you're satisfied with the index, continue to the next step: specifying the knowledge source in a [knowledge base](agentic-retrieval-how-to-create-knowledge-base.md).

Within the knowledge base, there are more properties to set on the knowledge source that are specific to query operations.

<!-- Deviating from pattern here. SharePoint remote needs answerSynthesis-->
Here's an example of a knowledge base that specifies a remote SharePoint knowledge source, with some key points:

+ Make sure you set `outputMode` to `answerSynthesis`.
+ Answer synthesis requires that you set the `retrievalReasoningEffort` to `low`.

Currently, GPT 4 series is recommended for chat completion in agentic retrieval.

```json
{
  "name": "remote-sp-kb",
  "description": "Retrieves SharePoint and OneDrive content from a trusted Microsoft 365 tenant.",
  "retrievalInstructions": null,
  "answerInstructions": null,
  "outputMode": "answerSynthesis",
  "knowledgeSources": [
    {
      "name": "my-sharepoint-ks"
    }
  ],
  "models": [
    {
      "kind": "azureOpenAI",
      "azureOpenAIParameters": {
        "resourceUri": "<redacted>",
        "deploymentId": "gpt-4.1-mini",
        "apiKey": "<redacted>",
        "modelName": "gpt-4.1-mini",
        "authIdentity": null
      }
    }
  ],
  "encryptionKey": null,
  "retrievalReasoningEffort": {
    "kind": "low"
  }
}
```

## Retrieve content

The retrieve action provides the user identity that authorizes access to content in Microsoft 365. For local development, set the `x-ms-query-source-authorization` header to provide the access token you previously set as a variable.

```http
POST {{search-url}}/knowledgebases/remote-sp-kb/retrieve?api-version={{api-version}}
api-key: {{api-key}}
Content-Type: application/json
x-ms-query-source-authorization: {{access-token}}

{
    "messages": [
        {
            "role": "user",
            "content": [
                { "type": "text", "text": "what was covered in the keynote doc for Ignite 2024" }
            ]
        }
    ],
    "includeActivity": true,
    "knowledgeSourceParams": [
        {
            "knowledgeSourceName": "remote-sp-kb",
            "kind": "remoteSharePoint",
            "includeReferences": true,
            "includeReferenceSourceData": true
        }
    ]
}
```

Queries asking questions about the content itself are more effective then questions about where a file is located or when it was last updated. For example, if you ask, "where is the keynote doc for Ignite 2024", you might get "No relevant content was found for your query" because the content itself doesn't disclose its location. A filter on metadata is a better solution for file location queries.

However, if you ask "what is the keynote doc for Ignite 2024", the response includes the synthesized answer, plus the URL and other metadata.

```json
{
    "resourceMetadata": {
        "Author": "Nuwan Amarathunga;Nurul Izzati",
        "Title": "Ignite 2024 Keynote Address"
    }
},
"rerankerScore": 2.489522,
"webUrl": "https://contoso-my.sharepoint.com/keynotes/nuamarth_contoso_com/Documents/Keynote-Ignite-2024.docx",
"searchSensitivityLabelInfo": {
        "displayName": "Confidential\\Contoso Extended",
        "sensitivityLabelId": "aaaaaaaa-0b0b-1c1c-2d2d-333333333333",
        "tooltip": "Data is classified and protected. Contoso Full Time Employees (FTE) and non-employees can edit, reply, forward and print. Recipient can unprotect content with the right justification.",
        "priority": 5,
        "color": "#FF8C00",
        "isEncrypted": true
    }
```

## Delete a knowledge source

[!INCLUDE [Delete knowledge source](includes/how-tos/knowledge-source-delete-rest.md)]

## Related content

+ [Agentic retrieval in Azure AI Search](agentic-retrieval-overview.md)

+ [Agentic RAG: build a reasoning retrieval engine with Azure AI Search (YouTube video)](https://www.youtube.com/watch?v=PeTmOidqHM8)

+ [Azure OpenAI Demo featuring agentic retrieval](https://github.com/Azure-Samples/azure-search-openai-demo)
