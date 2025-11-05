---
title: Create a SharePoint (Indexed) Knowledge Source
titleSuffix: Azure AI Search
description: An indexed SharePoint knowledge source ingests content from SharePoint sites into a searchable index on Azure AI Search.
manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 11/05/2025
---

# Create an indexed SharePoint knowledge source

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

An *indexed SharePoint knowledge source* ingests content from SharePoint sites into a searchable index on Azure AI Search. [Knowledge sources](agentic-knowledge-source-overview.md) are created independently, referenced in a [knowledge base](agentic-retrieval-how-to-create-knowledge-base.md), and used as grounding data when an agent or chatbot calls a [retrieve](/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2025-11-01-preview&preserve-view=true) action at query time.

When you create an indexed SharePoint knowledge source, you specify a SharePoint connection string, models, and properties to automatically generate the following Azure AI Search objects:

+ A data source that points to SharePoint sites.
+ A skillset that chunks and optionally vectorizes multimodal content.
+ An index that stores enriched content and meets the criteria for agentic retrieval.
+ An indexer that uses the previous objects to drive the indexing and enrichment pipeline.

## Prerequisites

+ Azure AI Search in an Azure tenant, configured for Microsoft Entra ID authentication.

+ SharePoint in a Microsoft 365 tenant, under the same Microsoft Entra ID tenant as Azure.

+ A personal access token for local development or a user's identity from a client application. 

For local development, the agentic retrieval engine uses your access token to call SharePoint on your behalf. For more information about using a personal access token on requests, see [Connect to Azure AI Search](search-get-started-rbac.md).

To try the examples in this article, we recommend [Visual Studio Code](https://code.visualstudio.com/download) with the [REST Client extension](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) for sending preview REST API calls to Azure AI Search. Currently, there's no portal support.

The generated indexer conforms to the *SharePoint indexer*, whose prerequisites, supported tasks, supported document formats, supported shortcuts, and limitations also apply to indexed SharePoint knowledge sources. For more information, see the [SharePoint indexer documentation](search-how-to-index-sharepoint-online.md).

## Check for existing knowledge sources

[!INCLUDE [Check for existing knowledge sources](includes/how-tos/knowledge-source-check-rest.md)]

The following JSON is an example response for an indexed SharePoint knowledge source.

```json
{
  "name": "my-demo-indexed-sharepoint-ks",
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
      "datasource": "my-demo-indexed-sharepoint-ks-datasource",
      "indexer": "my-demo-indexed-sharepoint-ks-indexer",
      "skillset": "my-demo-indexed-sharepoint-ks-skillset",
      "index": "my-demo-indexed-sharepoint-ks-index"
    }
  },
  "indexedOneLakeParameters": null
}
```

> [!NOTE]
> Sensitive information is redacted. The generated resources appear at the end of the response.

## Create a knowledge source

To create an indexed SharePoint knowledge source:

1. Set environment variables at the top of your file.

    ```http
    @search-url = <YOUR SEARCH SERVICE URL>
    @api-key = <YOUR SEARCH SERVICE ADMIN API KEY>
    @aoai-endpoint = <YOUR AZURE OPENAI RESOURCE PROVIDING A CHAT COMPLETION MODEL>
    @aoai-key = <YOUR AZURE OPENAI KEY>
    @access-token = <YOUR PERSONAL ACCESS TOKEN USED FOR RETRIEVING PERMITTED CONTENT ON SHAREPOINT>
    @sharepoint-connection-string=SharePointOnlineEndpoint=https://<YOUR SERVICE NAME>.sharepoint.com/sites/<YOUR SITE>;ApplicationId=<YOUR APPLICATION ID>;ApplicationSecret=<YOUR APPLICATION SECRET>;TenantId=<YOUR TENANT>

    ```

    [API keys](search-security-api-keys.md) are used for your client connection to Azure AI Search and Azure OpenAI. Your access token is used by Azure AI Search to connect to SharePoint in Microsoft 365 on your behalf. You can only retrieve content that you're permitted to access. For more information about getting a personal access token and other values, see [Connect to Azure AI Search](search-get-started-rbac.md).

    > [!NOTE]
    > You can also use your personal access token to access Azure AI Search and Azure OpenAI if you [set up role assignments on each resource](search-security-rbac.md). Using API keys allows you to omit this step in this example.

1. Use the 2025-11-01-preview of [Knowledge Sources - Create or Update (REST API)](/rest/api/searchservice/knowledge-sources/create-or-update?view=rest-searchservice-2025-11-01-preview&preserve-view=true) or an Azure SDK preview package that provides equivalent functionality to formulate the request.

    ```http
    POST {{search-url}}/knowledgesources/my-demo-indexed-sharepoint-ks?api-version=2025-11-01-preview
    api-key: {{api-key}}
    Content-Type: application/json
    
    {
        "name": "my-demo-indexed-sharepoint-ks",
        "kind": "indexedSharePoint",
        "description": "A sample indexed SharePoint knowledge source.",
        "encryptionKey": null,
        "indexedSharePointParameters": {
            "connectionString": "{{sharepoint-connection-string}}",
            "containerName": "defaultSiteLibrary",
            "query": null,
            "ingestionParameters": {
                "identity": null,
                "embeddingModel": {
                    "kind": "azureOpenAI",
                    "azureOpenAIParameters": {
                        "deploymentId": "text-embedding-3-large",
                        "modelName": "text-embedding-3-large",
                        "resourceUri": "{{aoai-endpoint}}",
                        "apiKey": "{{aoai-key}}"
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

   An embedding model is used to create a vector field counterpart to the primary chunked textual content, which adds vector query support to the agentic pipeline. You can omit the embedding model if you don't need vectors.

   A chat completion model is used in the generated skillset. If you enable image verbalization and specify a chat completion model, the model is used to verbalize image content on the SharePoint site. You can omit the chat completion model if you don't need this capability.

1. Select **Send Request**.

<!-- Can't find an explanation of the query parameter in the spec. -->
### Source-specific properties

You can pass the following properties to create a indexed SharePoint knowledge source.

| Name | Description | Type | Editable | Required |
|--|--|--|--|--|
| `name` | The name of the knowledge source, which must be unique within the knowledge sources collection and follow the [naming guidelines](/rest/api/searchservice/naming-rules) for objects in Azure AI Search. | String | No | Yes |
| `kind` | The kind of knowledge source, which is `indexedSharePoint` in this case. | String | No | Yes |
| `description` | A description of the knowledge source. | String | Yes | No |
| `encryptionKey` | A [customer-managed key](search-security-manage-encryption-keys.md) to encrypt sensitive information in both the knowledge source and the generated objects. | Object | Yes | No |
| `indexedSharePointParameters` | Parameters specific to indexed SharePoint knowledge sources: `connectionString`, `containerName`, and `query`. | Object | No | No |
| `connectionString` | An expression written in the SharePoint in [Keyword Query Language (KQL)](/sharepoint/dev/general-development/keyword-query-language-kql-syntax-reference), used to specify sites and paths to content. | String | Yes |No |
| `query` | Ignore for now. | String | Yes | No |

### `ingestionParameters` properties

[!INCLUDE [Knowledge source ingestionParameters properties](./includes/how-tos/knowledge-source-ingestion-parameters.md)]

## Check ingestion status

[!INCLUDE [Knowledge source status](./includes/how-tos/knowledge-source-status.md)]

## Review the created objects

When you create an indexed SharePoint knowledge source, your search service also creates an indexer, index, skillset, and data source. We don't recommend that you edit these objects, as introducing an error or incompatibility can break the pipeline.

After you create a knowledge source, the response lists the created objects. These objects are created according to a fixed template, and their names are based on the name of the knowledge source. You can't change the object names.

We recommend using the Azure portal to validate output creation. The workflow is:

1. Check the indexer for success or failure messages. Connection or quota errors appear here.
1. Check the index for searchable content. Use Search Explorer to run queries.
1. Check the skillset to learn how your content is chunked and optionally vectorized.
1. Check the data source for connection details. Our example uses API keys for simplicity, but you can use Microsoft Entra ID for authentication and role-based access control for authorization.

## Assign to a knowledge base

If you're satisfied with the index, continue to the next step: specify the knowledge source in a [knowledge base](search-agentic-retrieval-how-to-create.md).

After the knowledge base is configured, use the [retrieve action](agentic-retrieval-how-to-retrieve.md) to query the knowledge source.

## Retrieve content

The retrieve action on the knowledge base provides the user identity that authorizes access to content in Microsoft 365. 

Azure AI Search uses the Microsoft Graph API to exchange the access token for an on-behalf of (OBO) token, which is then used to call the Copilot Retrieval API on behalf of the user identity. The access token is provided in the retrieve endpoint as an HTTP header `x-ms-query-source-authorization`.

Make sure that you [generate the access token](search-get-started-rbac.md?pivots=rest#get-token) for the Azure tenant, not the Microsoft 365 tenant.

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
            "filterExpressionAddOn": "ModifiedBy:\"Adele Vance\"",
            "knowledgeSourceName": "remote-sp-kb",
            "kind": "remoteSharePoint",
            "includeReferences": true,
            "includeReferenceSourceData": true
        }
    ]
}
```

The retrieve request also takes a KQL filter (`filterExpressionAddOn`) in case you want to apply constraints at query time. If you specify filters for both Copilot retrieval and agentic retrieval, the filters are AND'd together.

Queries asking questions about the content itself are more effective than questions about where a file is located or when it was last updated. For example, if you ask, "where is the keynote doc for Ignite 2024", you might get "No relevant content was found for your query" because the content itself doesn't disclose its location. A filter on metadata is a better solution for file location or date-specific queries.

A better question to ask is "what is the keynote doc for Ignite 2024". The response includes the synthesized answer, query activity and token counts, plus the URL and other metadata.

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
