---
title: Create a Work IQ Knowledge Source
description: Learn how to create a Work IQ knowledge source to ground an agentic retrieval pipeline in Azure AI Search with organizational intelligence from Work IQ.
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 05/06/2026
ai-usage: ai-assisted
---

# Create a Work IQ knowledge source

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

A *Work IQ knowledge source* connects [Work IQ](/microsoft-365/copilot/extensibility/work-iq) to your agentic retrieval pipeline in Azure AI Search, providing intelligence from your organization's Microsoft 365 content as grounding data.

Unlike indexed knowledge sources, a Work IQ knowledge source queries Work IQ directly at retrieval time. No ingestion pipeline is needed. Queries require an end-user access token, which the retrieval engine uses to call Work IQ on the caller's behalf.

### Usage support

| [Azure portal](get-started-portal-agentic-retrieval.md) | [Microsoft Foundry portal](/azure/ai-foundry/agents/concepts/what-is-foundry-iq#workflow) | [.NET SDK](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/CHANGELOG.md) | [Python SDK](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [Java SDK](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [JavaScript SDK](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/search/search-documents/CHANGELOG.md) | [REST API](/rest/api/searchservice/knowledge-sources?view=rest-searchservice-2026-05-01-preview&preserve-view=true) |
|--|--|--|--|--|--|--|
| ❌ | ❌ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |

<!-- TO-DO (PM): Confirm which, if any, portal or SDK surfaces will support Work IQ KS in this preview. Update the usage support table accordingly. -->

## Prerequisites

+ Azure AI Search in any [region that provides agentic retrieval](search-region-support.md). You must have [semantic ranker enabled](semantic-how-to-enable-disable.md).

+ A Work IQ environment that is already configured and accessible to the calling tenant. <!-- TO-DO (PM): What Work IQ environment prerequisites does the caller need? Is there a provisioning step, a license requirement (for example, a Microsoft 365 Copilot license), or a service enablement flag that must be set before creating this knowledge source? -->

+ Permission to create and use objects on Azure AI Search. We recommend [role-based access](search-security-rbac.md), but you can use [API keys](search-security-api-keys.md) if a role assignment isn't feasible. For more information, see [Connect to a search service](search-get-started-rbac.md).

+ The [2026-05-01-preview](/rest/api/searchservice/operation-groups?view=rest-searchservice-2026-05-01-preview&preserve-view=true) version of the Search Service REST APIs.

## Check for existing knowledge sources

<!-- TO-DO (writer): Replace the following inline REST with [!INCLUDE [Check for existing knowledge sources using REST](includes/how-tos/knowledge-source-check-rest.md)] when C# and Python are added to this article. -->

A knowledge source is a top-level, reusable object. Knowing about existing knowledge sources is helpful for either reuse or naming new objects.

Run the following code to list knowledge sources by name and type.

```http
### List knowledge sources by name and type
GET {{search-url}}/knowledgesources?api-version=2026-05-01-preview&$select=name,kind
api-key: {{api-key}}
```

**Reference:** [Knowledge Sources - List](/rest/api/searchservice/knowledge-sources/list)

You can also return a single knowledge source by name to review its JSON definition.

```http
### Get a knowledge source definition
GET {{search-url}}/knowledgesources/{{knowledge-source-name}}?api-version=2026-05-01-preview
api-key: {{api-key}}
```

**Reference:** [Knowledge Sources - Get](/rest/api/searchservice/knowledge-sources/get)

The following JSON is an example response for a Work IQ knowledge source.

```json
{
  "name": "my-workiq-ks",
  "kind": "workIQ",
  "description": "Organizational intelligence from Work IQ.",
  "encryptionKey": null
}
```

## Create a knowledge source

Run the following code to create a Work IQ knowledge source. 

```http
### Create a Work IQ knowledge source
PUT {{search-url}}/knowledgesources/my-workiq-ks?api-version=2026-05-01-preview
api-key: {{api-key}}
Content-Type: application/json

{
  "name": "my-workiq-ks",
  "kind": "workIQ",
  "description": "Organizational intelligence from Work IQ."
}
```

**Reference:** [Knowledge Sources - Create or Update)](/rest/api/searchservice/knowledge-sources/create-or-update?view=rest-searchservice-2026-05-01-preview&preserve-view=true)

### Source-specific properties

The following properties apply to Work IQ knowledge sources.

| Name | Description | Type | Editable | Required |
|--|--|--|--|--|
| `name` | The name of the knowledge source, which must be unique within the knowledge sources collection and follow the [naming guidelines](/rest/api/searchservice/naming-rules) for objects in Azure AI Search. | String | No | Yes |
| `kind` | The kind of knowledge source, which is `workIQ` in this case. | String | No | Yes |
| `description` | A description of the knowledge source. | String | Yes | No |
| `encryptionKey` | A [customer-managed key](search-security-manage-encryption-keys.md) to encrypt sensitive information in the knowledge source. | Object | Yes | No |

## Assign to a knowledge base

If you're satisfied with the knowledge source, continue to the next step: specify the knowledge source in a [knowledge base](agentic-retrieval-how-to-create-knowledge-base.md).

## Query a knowledge base

After the knowledge base is configured, use the [retrieve action](agentic-retrieval-how-to-retrieve.md) to query Work IQ content. This knowledge source has unique query-time permissions enforcement and response characteristics.

> [!IMPORTANT]
> Work IQ can take 40–60 seconds or more to respond. To avoid timeout errors, set `maxRuntimeInSeconds` on the retrieve request to `120` or higher.

### Enforce permissions at query time

Work IQ knowledge sources use an on-behalf-of (OBO) token flow. You pass an access token scoped to the Azure AI Search audience (`https://search.azure.com/.default`) on the retrieve request. The retrieval engine exchanges this token for a Work IQ–scoped token and uses it to query Work IQ on behalf of the end user.

Because Work IQ knowledge sources don't use a search index, no ingestion-time permissions configuration is needed. The access token is the only requirement.

For instructions on passing the token, see [Enforce permissions at query time](agentic-retrieval-how-to-retrieve.md#enforce-permissions-at-query-time).

### Work IQ–specific response fields

Work IQ reference entries return the following content:

- Grounded text passages from Work IQ (`sourceData.extracts[].text`)
- A link to the source document in Microsoft 365 (`attributions[].seeMoreWebUrl`)

The following example shows a reference and activity entry from a Work IQ knowledge source. The `activity` record shows the search argument sent to Work IQ, and the `references` array shows the grounded text and its source attribution.

```json
{
  "references": [
    {
      "type": "workIQ",
      "id": "83dd7d40",
      "activitySource": 1,
      "rerankerScore": 3.5,
      "attributions": [
        {
          "seeMoreWebUrl": "https://..."
        }
      ],
      "sourceData": {
        "extracts": [
          {
            "text": "Have your VPN username and password ready."
          }
        ]
      }
    }
  ],
  "activity": [
    {
      "type": "workIQ",
      "id": 1,
      "elapsedMs": 1137,
      "knowledgeSourceName": "my-workiq-ks",
      "queryTime": "2026-05-01T19:25:23.683Z",
      "count": 1,
      "workIQArguments": {
        "search": "my query"
      }
    }
  ]
}
```

> [!TIP]
> To receive `sourceData` in the response, set `includeReferenceSourceData` to `true` in `knowledgeSourceParams` of the retrieve request.

## Delete a knowledge source

<!-- TO-DO (writer): Replace the following inline REST with [!INCLUDE [Delete knowledge source using REST](includes/how-tos/knowledge-source-delete-rest.md)] when C# and Python are added to this article. -->

BBefore you can delete a knowledge source, you must delete any knowledge base that references it or update the knowledge base definition to remove the reference.

If you try to delete a knowledge source that's in use, the action fails and returns a list of affected knowledge bases.

To delete a knowledge source:

1. Get a list of all knowledge bases on your search service.

    ```http
    ### Get knowledge bases
    GET {{search-url}}/knowledgebases?api-version=2026-05-01-preview&$select=name
    api-key: {{api-key}}
    ```

   **Reference:** [Knowledge Bases - List](/rest/api/searchservice/knowledge-bases/list)

   An example response might look like the following:

   ```json
    {
        "@odata.context": "https://my-search-service.search.windows.net/$metadata#knowledgebases(name)",
        "value": [
          {
            "name": "my-kb"
          },
          {
            "name": "my-kb-2"
          }
        ]
    }
   ```

1. Get an individual knowledge base definition to check for knowledge source references.

    ```http
    ### Get a knowledge base definition
    GET {{search-url}}/knowledgebases/{{knowledge-base-name}}?api-version=2026-05-01-preview
    api-key: {{api-key}}
    ```

   **Reference:** [Knowledge Bases - Get](/rest/api/searchservice/knowledge-bases/get)

   An example response might look like the following:

   ```json
    {
      "name": "my-kb",
      "description": null,
      "retrievalInstructions": null,
      "answerInstructions": null,
      "outputMode": "answerSynthesis",
      "knowledgeSources": [
        {
          "name": "my-mcp-server-ks"
        }
      ],
      "models": [],
      "encryptionKey": null,
      "retrievalReasoningEffort": {
        "kind": "low"
      }
    }
   ```

1. Either delete the knowledge base or, if you have multiple knowledge sources, update the knowledge base to remove the reference. This example shows deletion.

    ```http
    ### Delete a knowledge base
    DELETE {{search-url}}/knowledgebases/{{knowledge-base-name}}?api-version=2026-05-01-preview
    api-key: {{api-key}}
    ```

   **Reference:** [Knowledge Bases - Delete](/rest/api/searchservice/knowledge-bases/delete)

1. Delete the knowledge source.

    ```http
    ### Delete a knowledge source
    DELETE {{search-url}}/knowledgesources/{{knowledge-source-name}}?api-version=2026-05-01-preview
    api-key: {{api-key}}
    ```

   **Reference:** [Knowledge Sources - Delete](/rest/api/searchservice/knowledge-sources/delete)

## Related content

+ [What is a knowledge source?](agentic-knowledge-source-overview.md)
+ [Create a knowledge base](agentic-retrieval-how-to-create-knowledge-base.md)
+ [Query a knowledge base (APIs or MCP)](agentic-retrieval-how-to-retrieve.md)
+ [Agentic retrieval in Azure AI Search](agentic-retrieval-overview.md)
