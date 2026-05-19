---
title: Create a Fabric Ontology Knowledge Source (Preview)
description: Learn how to create a Fabric Ontology knowledge source, which connects a Microsoft Fabric ontology to an agentic retrieval pipeline in Azure AI Search for ontology-backed answers.
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 06/02/2026
ai-usage: ai-assisted
---

# Create a Fabric Ontology knowledge source (preview)

> [!IMPORTANT]
> The 2026-05-01-preview REST API version is licensed to you as part of your Azure subscription and is subject to the terms applicable to "Previews" in the [Microsoft Product Terms](https://www.microsoft.com/licensing/terms/welcome/welcomepage), the [Microsoft Products and Services Data Protection Addendum ("DPA")](https://www.microsoft.com/licensing/docs/view/Microsoft-Products-and-Services-Data-Protection-Addendum-DPA), and the [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).

A *Fabric Ontology knowledge source* (preview) connects your [Microsoft Fabric ontology](/fabric/iq/ontology/overview) to an agentic retrieval pipeline in Azure AI Search, providing ontology-defined entities, relationships, and content as grounding data. Because ontologies capture how your business defines its data, agents can answer in business terms rather than reasoning over raw tables and columns.

Unlike indexed knowledge sources, Fabric Ontology knowledge sources (preview) query live data directly. No ingestion pipeline is needed. Queries require an end-user access token, which the retrieval engine uses to authenticate with Microsoft Fabric on the caller's behalf.

### Usage support

| [Azure portal](get-started-portal-agentic-retrieval.md) | [Microsoft Foundry portal](/azure/ai-foundry/agents/concepts/what-is-foundry-iq#workflow) | [.NET SDK](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/CHANGELOG.md) | [Python SDK](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [Java SDK](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [JavaScript SDK](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/search/search-documents/CHANGELOG.md) | [REST API](/rest/api/searchservice/knowledge-sources?view=rest-searchservice-2026-05-01-preview&preserve-view=true) |
|--|--|--|--|--|--|--|
| ❌ | ❌ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |

<!-- TO-DO (PM): Confirm portal and SDK support for Build and update this table as needed. -->

## Prerequisites

+ An Azure AI Search service in any [region that provides agentic retrieval](search-region-support.md).

+ A Microsoft Fabric workspace with an [ontology item](/fabric/iq/ontology/tutorial-1-create-ontology). Your search service and workspace must be in the same Microsoft Entra ID tenant. <!-- TO-DO (PM): Confirm any specific Fabric SKU (for example, F64 capacity) or workspace settings required to use a Fabric ontology as a knowledge source. -->

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

**Reference:** [Knowledge Sources - List](/rest/api/searchservice/knowledge-sources/list)

You can also return a single knowledge source by name to review its JSON definition.

```http
### Get a knowledge source definition
GET {{search-url}}/knowledgesources/{{knowledge-source-name}}?api-version={{api-version}}
api-key: {{api-key}}
```

**Reference:** [Knowledge Sources - Get](/rest/api/searchservice/knowledge-sources/get)

The following JSON is an example response for a Fabric Ontology knowledge source (preview).

```json
{
  "name": "my-fabric-ontology-ks",
  "kind": "fabricOntology",
  "description": "A Fabric Ontology knowledge source.",
  "encryptionKey": null,
  "fabricOntologyParameters": {
    "workspaceId": "00000000-0000-0000-0000-000000000000",
    "ontologyId": "00000000-0000-0000-0000-000000000001"
  }
}
```

## Create a knowledge source

Run the following code to create a Fabric Ontology knowledge source (preview).

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
    "workspaceId": "{fabric-workspace-id}",
    "ontologyId": "{fabric-ontology-id}"
  }
}
```

**Reference:** [Knowledge Sources - Create or Update](/rest/api/searchservice/knowledge-sources/create-or-update?view=rest-searchservice-2026-05-01-preview&preserve-view=true)

### Source-specific properties

<!-- TO-DO (PM): Confirm whether these properties are correct for Fabric Ontology knowledge sources and update as needed. -->

The following properties apply to Fabric Ontology knowledge sources (preview).

| Name | Description | Type | Editable | Required |
|--|--|--|--|--|
| `name` | The name of the knowledge source, which must be unique within the knowledge sources collection and follow the [naming guidelines](/rest/api/searchservice/naming-rules) for objects in Azure AI Search. | String | No | Yes |
| `kind` | The kind of knowledge source, which is `fabricOntology` in this case. | String | No | Yes |
| `description` | A description of the knowledge source. | String | Yes | No |
| `encryptionKey` | A [customer-managed key](search-security-manage-encryption-keys.md) to encrypt sensitive information in the knowledge source. | Object | Yes | No |
| `fabricOntologyParameters` | Parameters specific to the Fabric Ontology knowledge source: `workspaceId` and `ontologyId`. | Object | No | Yes |
| `workspaceId` | The [ID of the Microsoft Fabric workspace](/fabric/data-factory/migrate-pipelines-how-to-find-your-fabric-workspace-id) that contains the ontology item. | String | No | Yes |
| `ontologyId` | The ID of the ontology item to query. | String | No | Yes |

## Assign to a knowledge base

If you're satisfied with the knowledge source, continue to the next step: specify the knowledge source in a [knowledge base](agentic-retrieval-how-to-create-knowledge-base.md).

> [!NOTE]
> Fabric Ontology knowledge sources (preview) don't support the `minimal` [retrieval reasoning effort](agentic-retrieval-how-to-set-retrieval-reasoning-effort.md). Use `low` or `medium` instead. <!-- TO-DO (PM): Is answer synthesis also required? -->

## Query a knowledge base

After the knowledge base is configured, use the [retrieve action](agentic-retrieval-how-to-retrieve.md) to query Fabric Ontology content. This knowledge source has unique query-time permissions enforcement and response characteristics.

<!-- TO-DO (PM): Confirm the following details about query-time permissions and response characteristics for Fabric Ontology knowledge sources and update as needed. -->

### Enforce permissions at query time

Fabric Ontology knowledge sources (preview) use an on-behalf-of (OBO) token flow. You pass an access token scoped to the Azure AI Search audience (`https://search.azure.com/.default`) on the retrieve request. The retrieval engine exchanges this token for a Microsoft Fabric–scoped token and uses it to query the ontology item on behalf of the end user.

Because Fabric Ontology knowledge sources (preview) don't use a search index, no ingestion-time permissions configuration is needed. The access token is the only requirement.

For instructions on passing the token, see [Enforce permissions at query time](agentic-retrieval-how-to-retrieve.md#enforce-permissions-at-query-time).

### Fabric Ontology–specific response fields

Fabric Ontology knowledge sources (preview) return results in the `sourceData` object of each `references` entry and query diagnostics in the `activity` array. `sourceData` contains:

- `fabricAnswer`: The ontology's natural-language answer.
- `fabricRawData`: The structured data that grounded the answer, returned in CSV format.

The following example shows a retrieve response containing a Fabric Ontology knowledge source reference and its corresponding activity record. For broader guidance on interpreting retrieve responses, see [Review the response](agentic-retrieval-how-to-retrieve.md#review-the-response).

```json
{
  "response": [
      // ... Response omitted for brevity
  ],
  "activity": [
    {
      "type": "fabricOntology",
      "id": 1,
      "knowledgeSourceName": "my-fabric-ontology-ks",
      "queryTime": "2026-05-11T20:29:24Z",
      "count": 1,
      "fabricOntologyArguments": {
        "search": "Which airlines operate domestic routes?"
      }
    },
    {
      // ... Additional activity records omitted for brevity 
    }
  ],
  "references": [
    {
      "type": "fabricOntology",
      "id": "0",
      "activitySource": 1,
      "sourceData": {
        "fabricAnswer": "There are 3 airlines with domestic routes: Delta, United, and American.",
        "fabricRawData": "Airline,Routes\nDelta,47\nUnited,38\nAmerican,29"
      },
      "rerankerScore": 0,
      "workspaceId": "00000000-0000-0000-0000-000000000000",
      "ontologyId": "00000000-0000-0000-0000-000000000001"
    },
    {
      // ... Additional references omitted for brevity
    }
  ]
}
```

> [!TIP]
> To receive `sourceData` for references, set `knowledgeSourceParams.includeReferenceSourceData` to `true` on the retrieve request.

## Delete a knowledge source

<!-- TO-DO (writer): Replace with [!INCLUDE [knowledge-source-delete-rest](./includes/how-tos/knowledge-source-delete-rest.md)] when C# and Python are added to this article. -->

Before you can delete a knowledge source, you must delete any knowledge base that references it or update the knowledge base definition to remove the reference. For knowledge sources that generate an index and indexer pipeline, all *generated objects* are also deleted. However, if you used an existing index to create a knowledge source, your index isn't deleted.

If you try to delete a knowledge source that's in use, the action fails and returns a list of affected knowledge bases.

To delete a knowledge source:

1. Get a list of all knowledge bases on your search service.

    ```http
    ### Get knowledge bases
    GET {{search-url}}/knowledgebases?api-version={{api-version}}&$select=name
    api-key: {{api-key}}
    ```

   **Reference:** [Knowledge Bases - List](/rest/api/searchservice/knowledge-bases/list)

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

   **Reference:** [Knowledge Bases - Get](/rest/api/searchservice/knowledge-bases/get)

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

   **Reference:** [Knowledge Bases - Delete](/rest/api/searchservice/knowledge-bases/delete)

1. Delete the knowledge source.

    ```http
    ### Delete a knowledge source
    DELETE {{search-url}}/knowledgesources/{{knowledge-source-name}}?api-version={{api-version}}
    api-key: {{api-key}}
    ```

   **Reference:** [Knowledge Sources - Delete](/rest/api/searchservice/knowledge-sources/delete)

## Related content

+ [Agentic retrieval in Azure AI Search](agentic-retrieval-overview.md)
+ [What is a knowledge source?](agentic-knowledge-source-overview.md)
+ [Create a knowledge base](agentic-retrieval-how-to-create-knowledge-base.md)
+ [Query a knowledge base](agentic-retrieval-how-to-retrieve.md)
