---
title: Create a SharePoint (Remote) Knowledge Source
titleSuffix: Azure AI Search
description: A remote Sharepoint knowledge source tells the agentic retrieval engine to query SharePoint sites directly.
manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 10/30/2025
---

# Create a remote SharePoint knowledge source

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

A *remote SharePoint knowledge source* specifies a connection to a SharePoint site and pulls textual and image content directly from SharePoint, returning results to the agentic retrieval engine for merging, ranking, and response formulation. There is no search index used by this knowledge source.

Like any other knowledge source, you specify a remote SharePoint knowledge source in a [knowledge base](agentic-retrieval-how-to-create-knowledge-base.md), and use the results as grounding data when an agent or chatbot calls a [retrieve](/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2025-11-01-preview&preserve-view=true) action at query time.

## Prerequisites

+ Azure AI Search in an Azure tenant.

+ SharePoint Online in an M365 tenant.

To try the examples in this article, we recommend [Visual Studio Code](https://code.visualstudio.com/download) with the [REST Client extension](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) for sending preview REST API calls to Azure AI Search. Currently, there's no portal support.

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
    @api-key = <YOUR ADMIN API KEY>
    ```

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

### Source-specific properties

You can pass the following properties to create a remote SharePoint knowledge source.

| Name | Description | Type | Required |
|--|--|--|--|
| `name` | The name of the knowledge source, which must be unique within the knowledge sources collection and follow the [naming guidelines](/rest/api/searchservice/naming-rules) for objects in Azure AI Search. | String | Yes |
| `kind` | The kind of knowledge source, which is `remoteSharePoint` in this case. | String | Yes |
| `description` | A description of the knowledge source. | String | No |
| `encryptionKey` | A [customer-managed key](search-security-manage-encryption-keys.md) to encrypt sensitive information in both the knowledge source and the generated objects. | Object | No |
| `remoteSharePointParameters` | Parameters specific to remote SharePoint knowledge sources: `filterExpression`, `resourceMetadata`, and `containerTypeId`. | Object | No |
| `filterExpression` | XXX| String | No |
| `resourceMetadata` | XXX | Array | No |
| `containerTypeId` | XXX | String| No |

## Assign to a knowledge base

If you're satisfied with the index, continue to the next step: specifying the knowledge source in a [knowledge base](agentic-retrieval-how-to-create-knowledge-base.md).

Within the knowledge base, there are more properties to set on the knowledge source that are specific to query operations.

<!-- Deviating from pattern here. Is there anything special in the KB definition for remote SharePoint? -->
Here's an example of a knowledge base that specifies a remote SharePoint knowledge source.

```json
{
  "name": "remote-sp-kb",
  "description": "A sample federated SharePoint knowledge base",
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
        "deploymentId": "gpt-5-mini",
        "apiKey": "<redacted>",
        "modelName": "gpt-5-mini",
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

## Delete a knowledge source

[!INCLUDE [Delete knowledge source](includes/how-tos/knowledge-source-delete-rest.md)]

## Related content

+ [Agentic retrieval in Azure AI Search](agentic-retrieval-overview.md)

+ [Agentic RAG: build a reasoning retrieval engine with Azure AI Search (YouTube video)](https://www.youtube.com/watch?v=PeTmOidqHM8)

+ [Azure OpenAI Demo featuring agentic retrieval](https://github.com/Azure-Samples/azure-search-openai-demo)
