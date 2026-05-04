---
title: Create a Fabric Ontology Knowledge Source
description: Learn how to create a Fabric Ontology knowledge source, which connects a Microsoft Fabric semantic model to an agentic retrieval pipeline in Azure AI Search for ontology-backed answers.
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 05/04/2026
ai-usage: ai-assisted
---

# Create a Fabric Ontology knowledge source

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

A *Fabric Ontology knowledge source* connects a Microsoft Fabric ontology to an agentic retrieval pipeline in Azure AI Search. A Fabric ontology represents enterprise knowledge as entities, relationships, and rules — a semantic model that describes *how* business concepts relate to one another, not just what the raw data contains.

At query time, the retrieval engine converts the query into a call to the Fabric ontology's Model Context Protocol (MCP) endpoint. The ontology returns a natural-language answer and the structured data that grounded it, without requiring a separate LLM call to interpret the query.

Like any other knowledge source, you specify a Fabric Ontology knowledge source in a [knowledge base](agentic-retrieval-how-to-create-knowledge-base.md) and use the results as grounding data when an agent or chatbot calls a [retrieve action](agentic-retrieval-how-to-retrieve.md) at query time.

### When to use Fabric Ontology

Use a Fabric Ontology knowledge source when your most important information is modeled as business entities and their relationships in Fabric, and answers depend on reasoning over how those concepts connect — for example, "Which airline routes had the most delays last quarter?"

If your data lives in tables or files behind a Fabric Data Agent, use a [Fabric Data Agent knowledge source](agentic-knowledge-source-how-to-fabric-data-agent.md) instead. A Fabric Ontology knowledge source is purpose-built for semantically modeled data where the ontology itself is the source of truth.

### Usage support

| [Azure portal](get-started-portal-agentic-retrieval.md) | [Microsoft Foundry portal](/azure/ai-foundry/agents/concepts/what-is-foundry-iq#workflow) | [.NET SDK](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/CHANGELOG.md) | [Python SDK](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [Java SDK](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [JavaScript SDK](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/search/search-documents/CHANGELOG.md) | [REST API](/rest/api/searchservice/knowledge-sources?view=rest-searchservice-2026-05-01-preview&preserve-view=true) |
|--|--|--|--|--|--|--|
| ❌ | ❌ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |

<!-- TO-DO (PM): Confirm portal and SDK support for Build and update this table as needed. -->

## Prerequisites

+ An Azure AI Search service in any [region that provides agentic retrieval](search-region-support.md).

+ A Microsoft Fabric workspace with an ontology item configured. Your search service and workspace must be in the same Microsoft Entra ID tenant. <!-- TO-DO (PM): Confirm any specific Fabric SKU (for example, F64 capacity) or workspace settings required to use a Fabric ontology as a knowledge source. -->

+ Permission to create and use objects on Azure AI Search. We recommend [role-based access](search-security-rbac.md), but you can use [API keys](search-security-api-keys.md) if a role assignment isn't feasible. For more information, see [Connect to a search service](search-get-started-rbac.md).

+ The [2026-05-01-preview](/rest/api/searchservice/operation-groups?view=rest-searchservice-2026-05-01-preview&preserve-view=true) version of the Search Service REST APIs.

## Check for existing knowledge sources

<!-- TO-DO (writer): Replace with [!INCLUDE [knowledge-source-check-rest](./includes/how-tos/knowledge-source-check-rest.md)] when C# and Python are added to this article. -->

A knowledge source is a top-level, reusable object. Knowing about existing knowledge sources is helpful for either reuse or naming new objects.

Run the following code to list knowledge sources by name and type.

```http
### List knowledge sources by name and type
GET {{search-url}}/knowledgesources?api-version={{api-version}}&$select=name,kind
api-key: {{api-key}}
```

**Reference:** [Knowledge Sources - List](/rest/api/searchservice/knowledge-sources/list?view=rest-searchservice-2026-05-01-preview&preserve-view=true)

You can also return a single knowledge source by name to review its JSON definition.

```http
### Get a knowledge source definition
GET {{search-url}}/knowledgesources/{{knowledge-source-name}}?api-version={{api-version}}
api-key: {{api-key}}
```

**Reference:** [Knowledge Sources - Get](/rest/api/searchservice/knowledge-sources/get?view=rest-searchservice-2026-05-01-preview&preserve-view=true)

The following JSON is an example response for a Fabric Ontology knowledge source.

```json
{
  "name": "my-fabric-ontology-ks",
  "kind": "fabricOntology",
  "description": "A Fabric Ontology knowledge source.",
  "encryptionKey": null,
  "fabricOntologyParameters": {
    "fabricEndpoint": "https://api.fabric.microsoft.com",
    "workspaceId": "00000000-0000-0000-0000-000000000000",
    "ontologyId": "00000000-0000-0000-0000-000000000001"
  }
}
```

## Create a knowledge source

> [!IMPORTANT]
> Always set `fabricEndpoint` explicitly in the knowledge source definition. Omitting it causes `405` or `502` errors at query time.

Run the following code to create a Fabric Ontology knowledge source.

```http
### Create a Fabric Ontology knowledge source
PUT {{search-url}}/knowledgesources/my-fabric-ontology-ks?api-version=2026-05-01-preview
api-key: {{api-key}}
Content-Type: application/json

{
  "name": "my-fabric-ontology-ks",
  "kind": "fabricOntology",
  "description": "A Fabric Ontology knowledge source.",
  "fabricOntologyParameters": {
    "fabricEndpoint": "https://api.fabric.microsoft.com",
    "workspaceId": "{fabric-workspace-id}",
    "ontologyId": "{fabric-ontology-id}"
  }
}
```

**Reference:** [Knowledge Sources - Create or Update](/rest/api/searchservice/knowledge-sources/create-or-update?view=rest-searchservice-2026-05-01-preview&preserve-view=true)

### Source-specific properties

The following properties apply to Fabric Ontology knowledge sources.

| Name | Description | Type | Editable | Required |
|--|--|--|--|--|
| `name` | The name of the knowledge source, which must be unique within the knowledge sources collection and follow the [naming guidelines](/rest/api/searchservice/naming-rules) for objects in Azure AI Search. | String | No | Yes |
| `kind` | The type identifier for the knowledge source. Must be `fabricOntology`. | String | No | Yes |
| `description` | A description of the knowledge source. | String | Yes | No |
| `encryptionKey` | A [customer-managed key](search-security-manage-encryption-keys.md) to encrypt sensitive information in the knowledge source. | Object | Yes | No |
| `fabricOntologyParameters` | An object containing the parameters that identify the Fabric ontology endpoint. All child parameters are required. | Object | No | Yes |
| `fabricEndpoint` | The base URL of the Fabric API. Always specify this value — omitting it causes query-time errors. | String | No | Yes |
| `workspaceId` | The GUID of the Microsoft Fabric workspace that contains the ontology. | String | No | Yes |
| `ontologyId` | The GUID of the Fabric ontology item to query. | String | No | Yes |

## Assign to a knowledge base

If you're satisfied with the knowledge source, continue to the next step: specify the knowledge source in a [knowledge base](agentic-retrieval-how-to-create-knowledge-base.md).

Fabric Ontology knowledge sources can coexist with indexed and other remote sources in the same knowledge base. When a query targets multiple knowledge sources, the retrieval engine merges and reranks results from all sources before returning a unified response.

## Query a knowledge base

After the knowledge base is configured, use the [retrieve action](agentic-retrieval-how-to-retrieve.md) to query Fabric Ontology content. This knowledge source has specific query-time authentication requirements and a distinctive response structure.

### Enforce permissions at query time

Fabric Ontology knowledge sources use an on-behalf-of (OBO) token flow. You pass an access token scoped to the Azure AI Search audience (`https://search.azure.com/.default`) on the retrieve request. The retrieval engine exchanges this token for a Fabric-scoped token and uses it to call the Fabric ontology MCP endpoint on behalf of the end user.

Because Fabric Ontology doesn't use a search index, no ingestion-time permissions configuration is needed. The access token is the only requirement. <!-- TO-DO (PM): Confirm what Fabric workspace role (Viewer, Contributor, or Admin) the end user's delegated identity requires to query the ontology. -->

For instructions on passing the token, see [Enforce permissions at query time](agentic-retrieval-how-to-retrieve.md#enforce-permissions-at-query-time).

### Fabric Ontology–specific response fields

When the retrieval engine queries a Fabric Ontology knowledge source, the ontology returns a natural-language answer synthesized from its semantic model alongside the raw structured data that produced it. Both values appear in the `sourceData` object of each reference entry.

- **`fabricAnswer`** — A natural-language response generated by the Fabric ontology from its entity model.
- **`fabricRawData`** — The structured data that grounded the answer, returned in CSV format.

The following example shows a retrieve response containing a Fabric Ontology reference. The `activity` record shows the search argument sent to the ontology, and the `references` array shows the answer alongside its underlying structured data. The `response` content uses inline `ref_id` markers to associate answer text with specific references.

```json
{
  "response": [
    {
      "content": [
        {
          "type": "text",
          "text": "[{\"ref_id\":0,\"content\":\"There are 3 airlines with domestic routes: Delta (47), United (38), and American (29).\"}]"
        }
      ]
    }
  ],
  "activity": [
    {
      "type": "fabricOntology",
      "id": 1,
      "knowledgeSourceName": "my-fabric-ontology-ks",
      "fabricOntologyArguments": {
        "search": "Which airlines operate domestic routes?"
      }
    }
  ],
  "references": [
    {
      "type": "fabricOntology",
      "id": "0",
      "activitySource": 1,
      "workspaceId": "00000000-0000-0000-0000-000000000000",
      "ontologyId": "00000000-0000-0000-0000-000000000001",
      "sourceData": {
        "fabricAnswer": "There are 3 airlines with domestic routes: Delta, United, and American.",
        "fabricRawData": "Airline,Routes\nDelta,47\nUnited,38\nAmerican,29"
      }
    }
  ]
}
```

> [!TIP]
> To receive `sourceData` in the response, set `includeReferenceSourceData` to `true` in `knowledgeSourceParams` of the retrieve request.

## Delete a knowledge source

<!-- TO-DO (writer): Replace with [!INCLUDE [knowledge-source-delete-rest](./includes/how-tos/knowledge-source-delete-rest.md)] when C# and Python are added to this article. -->

Before you can delete a knowledge source, you must delete any knowledge base that references it or update the knowledge base definition to remove the reference.

If you try to delete a knowledge source that's in use, the action fails and returns a list of affected knowledge bases.

To delete a knowledge source:

1. Get a list of all knowledge bases on your search service.

    ```http
    ### Get knowledge bases
    GET {{search-url}}/knowledgebases?api-version={{api-version}}&$select=name
    api-key: {{api-key}}
    ```

   **Reference:** [Knowledge Bases - List](/rest/api/searchservice/knowledge-bases/list?view=rest-searchservice-2026-05-01-preview&preserve-view=true)

   An example response might look like the following:

   ```json
   {
     "@odata.context": "https://my-search-service.search.windows.net/$metadata#knowledgebases(name)",
     "value": [
       { "name": "my-kb" },
       { "name": "my-kb-2" }
     ]
   }
   ```

1. Get an individual knowledge base definition to check for knowledge source references.

    ```http
    ### Get a knowledge base definition
    GET {{search-url}}/knowledgebases/{{knowledge-base-name}}?api-version={{api-version}}
    api-key: {{api-key}}
    ```

   **Reference:** [Knowledge Bases - Get](/rest/api/searchservice/knowledge-bases/get?view=rest-searchservice-2026-05-01-preview&preserve-view=true)

   An example response might look like the following:

   ```json
   {
     "name": "my-kb",
     "description": null,
     "retrievalInstructions": null,
     "answerInstructions": null,
     "outputMode": null,
     "knowledgeSources": [
       { "name": "my-fabric-ontology-ks" }
     ],
     "models": [],
     "encryptionKey": null,
     "retrievalReasoningEffort": { "kind": "low" }
   }
   ```

1. Either delete the knowledge base or, if you have multiple knowledge sources, update the knowledge base to remove the source. This example shows deletion.

    ```http
    ### Delete a knowledge base
    DELETE {{search-url}}/knowledgebases/{{knowledge-base-name}}?api-version={{api-version}}
    api-key: {{api-key}}
    ```

   **Reference:** [Knowledge Bases - Delete](/rest/api/searchservice/knowledge-bases/delete?view=rest-searchservice-2026-05-01-preview&preserve-view=true)

1. Delete the knowledge source.

    ```http
    ### Delete a knowledge source
    DELETE {{search-url}}/knowledgesources/{{knowledge-source-name}}?api-version={{api-version}}
    api-key: {{api-key}}
    ```

   **Reference:** [Knowledge Sources - Delete](/rest/api/searchservice/knowledge-sources/delete?view=rest-searchservice-2026-05-01-preview&preserve-view=true)

## Related content

+ [What is a knowledge source?](agentic-knowledge-source-overview.md)
+ [Agentic retrieval in Azure AI Search](agentic-retrieval-overview.md)
+ [Create a knowledge base](agentic-retrieval-how-to-create-knowledge-base.md)
+ [Query a knowledge base](agentic-retrieval-how-to-retrieve.md)
