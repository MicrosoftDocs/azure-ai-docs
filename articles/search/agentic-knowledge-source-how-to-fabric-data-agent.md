---
title: Create a Fabric Data Agent Knowledge Source
description: Learn how to create a Fabric Data Agent knowledge source, which tells an agentic retrieval engine in Azure AI Search to query a Microsoft Fabric Data Agent directly.
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 05/01/2026
ai-usage: ai-assisted
---

# Create a Fabric Data Agent knowledge source

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

A *Fabric Data Agent knowledge source* connects your [Microsoft Fabric Data Agent](/fabric/data-science/concept-data-agent) to an agentic retrieval pipeline in Azure AI Search. At query time, the retrieval engine queries the Fabric Data Agent directly. No intermediate LLM call is involved. You specify the workspace and data agent IDs, and the retrieval engine handles authentication and query formulation.

Like any other knowledge source, you specify a Fabric Data Agent knowledge source in a [knowledge base](agentic-retrieval-how-to-create-knowledge-base.md) and use the results as grounding data when an agent or chatbot calls a [retrieve action](agentic-retrieval-how-to-retrieve.md) at query time.

### Usage support

| [Azure portal](get-started-portal-agentic-retrieval.md) | [Microsoft Foundry portal](/azure/ai-foundry/agents/concepts/what-is-foundry-iq#workflow) | [.NET SDK](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/CHANGELOG.md) | [Python SDK](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [Java SDK](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [JavaScript SDK](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/search/search-documents/CHANGELOG.md) | [REST API](/rest/api/searchservice/knowledge-sources?view=rest-searchservice-2026-05-01-preview&preserve-view=true) |
|--|--|--|--|--|--|--|
| ❌ | ❌ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |

<!-- TO-DO (PM): Confirm portal and SDK support for Build and update this table as needed. -->

## Prerequisites

+ An Azure AI Search service in any [region that provides agentic retrieval](search-region-support.md).

+ A Microsoft Fabric workspace with a [Fabric Data Agent configured](/fabric/data-science/how-to-create-data-agent). Your search service and workspace must be in the same Microsoft Entra ID tenant. <!-- TO-DO (PM): Confirm any specific Fabric SKU (for example, F64 capacity), workspace settings, or same-tenant requirements required to use a Fabric Data Agent as a knowledge source. -->

+ Permission to create and use objects on Azure AI Search. We recommend [role-based access](search-security-rbac.md), but you can use [API keys](search-security-api-keys.md) if a role assignment isn't feasible. For more information, see [Connect to a search service](search-get-started-rbac.md).

+ The [2026-05-01-preview](/rest/api/searchservice/operation-groups?view=rest-searchservice-2026-05-01-preview&preserve-view=true) version of the Search Service REST APIs.

## Check for existing knowledge sources

<!-- TO-DO (writer): Add inline REST code based on articles/search/includes/how-tos/knowledge-source-check.md. -->

A knowledge source is a top-level, reusable object. Knowing about existing knowledge sources is helpful for either reuse or naming new objects.

Run the following code to list knowledge sources by name and type.

```http
### List knowledge sources by name and type
GET {{search-url}}/knowledgesources?api-version={{api-version}}&$select=name,kind
api-key: {{api-key}}
```

**Reference:** [Knowledge Sources - List](/rest/api/searchservice/knowledge-sources/list)

You can also return a single knowledge source by name to review its JSON definition.

```http
### Get a knowledge source definition
GET {{search-url}}/knowledgesources/{{knowledge-source-name}}?api-version={{api-version}}
api-key: {{api-key}}
```

**Reference:** [Knowledge Sources - Get](/rest/api/searchservice/knowledge-sources/get)

The following JSON is an example response for a Fabric Data Agent knowledge source.

```json
{
  "name": "my-fabric-data-agent-ks",
  "kind": "fabricDataAgent",
  "description": "A Fabric Data Agent knowledge source.",
  "encryptionKey": null,
  "fabricDataAgentParameters": {
    "workspaceId": "00000000-0000-0000-0000-000000000000",
    "dataAgentId": "00000000-0000-0000-0000-000000000001"
  }
}
```

## Create a knowledge source

Run the following code to create a Fabric Data Agent knowledge source.

```http
### Create a Fabric Data Agent knowledge source
PUT {{search-url}}/knowledgesources/my-fabric-data-agent-ks?api-version=2026-05-01-preview
api-key: {{api-key}}
Content-Type: application/json

{
  "name": "my-fabric-data-agent-ks",
  "kind": "fabricDataAgent",
  "description": "A Fabric Data Agent knowledge source.",
  "fabricDataAgentParameters": {
    "workspaceId": "{fabric-workspace-id}",
    "dataAgentId": "{fabric-data-agent-id}"
  }
}
```

**Reference:** [Knowledge Sources - Create or Update](/rest/api/searchservice/knowledge-sources/create-or-update?view=rest-searchservice-2026-05-01-preview&preserve-view=true)

### Source-specific properties

The following properties apply to a Fabric Data Agent knowledge source.

| Name | Description | Type | Editable | Required |
|--|--|--|--|--|
| `name` | The name of the knowledge source, which must be unique within the knowledge sources collection and follow the [naming guidelines](/rest/api/searchservice/naming-rules) for objects in Azure AI Search. | String | No | Yes |
| `kind` | The kind of knowledge source, which is `"fabricDataAgent"` in this case. | String | No | Yes |
| `description` | A description of the knowledge source. | String | Yes | No |
| `encryptionKey` | A [customer-managed key](search-security-manage-encryption-keys.md) to encrypt sensitive information in the knowledge source. | Object | Yes | No |
| `fabricDataAgentParameters` | Parameters specific to the Fabric Data Agent knowledge source: `workspaceId` and `dataAgentId`. | Object | No | Yes |
| `workspaceId` | The ID of the Microsoft Fabric workspace that contains the data agent. | String | No | Yes |
| `dataAgentId` | The ID of the Fabric Data Agent to query. | String | No | Yes |

## Assign to a knowledge base

If you're satisfied with the knowledge source, continue to the next step: specify the knowledge source in a [knowledge base](agentic-retrieval-how-to-create-knowledge-base.md).

## Query a knowledge base

After the knowledge base is configured, use the [retrieve action](agentic-retrieval-how-to-retrieve.md) to query Fabric Data Agent content. The retrieval engine calls the Fabric Data Agent on behalf of your application and returns results as grounding data.

> [!IMPORTANT]
> Fabric Data Agent knowledge sources don't support `minimal` [reasoning effort](agentic-retrieval-how-to-retrieve.md#set-reasoning-effort). Use `low` or `medium` instead.

### Enforce permissions at query time

Fabric Data Agent knowledge sources require the end user's access token at query time. Include the token in the retrieve request, and the retrieval engine passes it to the Fabric Data Agent to authenticate the call on behalf of the end user.

<!-- TO-DO (PM): Confirm whether Power BI row-level security is enforced on underlying semantic models when the Fabric Data Agent is queried via the on-behalf-of flow. -->

Because Fabric Data Agent doesn't use a search index, no ingestion-time permissions configuration is needed. The access token is the only requirement.

For instructions on passing the token, see [Enforce permissions at query time](agentic-retrieval-how-to-retrieve.md#enforce-permissions-at-query-time).

### Fabric Data Agent–specific response fields

Fabric Data Agent responses can include two types of content:

- A natural-language answer (`fabricAnswer`)
- Embedded resources, such as tables, charts, or datasets (`fabricEmbeddedResources`)

The retrieval engine passes through the Fabric Data Agent's response directly and integrates it with results from other knowledge sources.

The following example shows a reference entry from a Fabric Data Agent knowledge source. To receive `sourceData`, set `includeReferenceSourceData` to `true` in the `knowledgeSourceParams` of the retrieve request.

<!-- TO-DO (PM): Confirm the JSON serialization names of the embedded resource subfields (`title`, `mimeType`, `content`). -->

```json
{
  "type": "fabricDataAgent",
  "id": "0",
  "activitySource": 1,
  "workspaceId": "00000000-0000-0000-0000-000000000000",
  "dataAgentId": "00000000-0000-0000-0000-000000000001",
  "rerankerScore": 2.57,
  "sourceData": {
    "fabricAnswer": "There were 47 airline delays in Q1 2026. The majority occurred on transcontinental routes.",
    "fabricEmbeddedResources": [
      {
        "title": "Q1 2026 Airline Operations Report",
        "mimeType": "text/csv",
        "content": "Route | Delays | Avg. Delay (min)\n--- | --- | ---\nJFK–LAX | 18 | 42\nORD–MIA | 12 | 31"
      }
    ]
  }
}
```


## Delete a knowledge source

<!-- TO-DO (writer): Add inline REST code based on articles/search/includes/how-tos/knowledge-source-delete.md. -->

Before you can delete a knowledge source, you must delete any knowledge base that references it or update the knowledge base definition to remove the reference. For knowledge sources that generate an index and indexer pipeline, all *generated objects* are also deleted. However, if you used an existing index to create a knowledge source, your index isn't deleted.

If you try to delete a knowledge source that's in use, the action fails and returns a list of affected knowledge bases.

To delete a knowledge source:

1. Get a list of all knowledge bases on your search service.

    ```http
    ### Get knowledge bases
    GET {{search-url}}/knowledgebases?api-version={{api-version}}&$select=name
    api-key: {{api-key}}
    ```

   **Reference:** [Knowledge Bases - List](/rest/api/searchservice/knowledge-bases/list?view=rest-searchservice-2026-04-01&preserve-view=true)

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
    GET {{search-url}}/knowledgebases/{{knowledge-base-name}}?api-version={{api-version}}
    api-key: {{api-key}}
    ```

   **Reference:** [Knowledge Bases - Get](/rest/api/searchservice/knowledge-bases/get?view=rest-searchservice-2026-04-01&preserve-view=true)

   An example response might look like the following:

   ```json
    {
      "name": "my-kb",
      "description": null,
      "retrievalInstructions": null,
      "answerInstructions": null,
      "outputMode": null,
      "knowledgeSources": [
        {
          "name": "my-blob-ks",
        }
      ],
      "models": [],
      "encryptionKey": null,
      "retrievalReasoningEffort": {
        "kind": "low"
      }
    }
   ```

1. Either delete the knowledge base or, if you have multiple knowledge sources, update the knowledge base to remove the source. This example shows deletion.

    ```http
    ### Delete a knowledge base
    DELETE {{search-url}}/knowledgebases/{{knowledge-base-name}}?api-version={{api-version}}
    api-key: {{api-key}}
    ```

   **Reference:** [Knowledge Bases - Delete](/rest/api/searchservice/knowledge-bases/delete?view=rest-searchservice-2026-04-01&preserve-view=true)

1. Delete the knowledge source.

    ```http
    ### Delete a knowledge source
    DELETE {{search-url}}/knowledgesources/{{knowledge-source-name}}?api-version={{api-version}}
    api-key: {{api-key}}
    ```

   **Reference:** [Knowledge Sources - Delete](/rest/api/searchservice/knowledge-sources/delete?view=rest-searchservice-2026-04-01&preserve-view=true)

## Related content

+ [What is a knowledge source?](agentic-knowledge-source-overview.md)
+ [Agentic retrieval in Azure AI Search](agentic-retrieval-overview.md)
+ [Create a knowledge base](agentic-retrieval-how-to-create-knowledge-base.md)
+ [Query a knowledge base](agentic-retrieval-how-to-retrieve.md)
