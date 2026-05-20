---
title: Create a Fabric Ontology Knowledge Source (Preview)
description: Learn how to create a Fabric Ontology knowledge source, which connects a Microsoft Fabric ontology to an agentic retrieval pipeline in Azure AI Search for ontology-backed answers.
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 06/02/2026
ai-usage: ai-assisted
zone_pivot_groups: search-csharp-python-rest
---

# Create a Fabric Ontology knowledge source (preview)

> [!IMPORTANT]
> These features and functionality are part of the 2026-05-01-preview REST API version. The 2026-05-01-preview is licensed to you as part of your Azure subscription and is subject to the terms applicable to "Previews" in the [Microsoft Product Terms](https://www.microsoft.com/licensing/terms/welcome/welcomepage), the [Microsoft Products and Services Data Protection Addendum](https://www.microsoft.com/licensing/docs/view/Microsoft-Products-and-Services-Data-Protection-Addendum-DPA) ("DPA"), and the [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).
>
> These 2026-05-01-preview features and functionality support connections to other Microsoft services and third-party services. Use of these services is subject to their respective terms and might result in data processing or storage outside of the Azure compliance boundary, as well as data flowing into the Azure compliance boundary.

A *Fabric Ontology knowledge source* (preview) connects your [Microsoft Fabric ontology](/fabric/iq/ontology/overview) to an agentic retrieval pipeline in Azure AI Search, providing ontology-defined entities, relationships, and content as grounding data. Because ontologies capture how your business defines its data, agents can answer in business terms rather than reasoning over raw tables and columns.

Unlike indexed knowledge sources, Fabric Ontology knowledge sources query live data directly. No ingestion pipeline is needed. Queries require an end-user access token, which the retrieval engine uses to authenticate with Microsoft Fabric on the caller's behalf.

### Usage support

| [Azure portal](get-started-portal-agentic-retrieval.md) | [Microsoft Foundry portal](/azure/ai-foundry/agents/concepts/what-is-foundry-iq#workflow) | [.NET SDK](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/CHANGELOG.md) | [Python SDK](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [Java SDK](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [JavaScript SDK](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/search/search-documents/CHANGELOG.md) | [REST API](/rest/api/searchservice/knowledge-sources?view=rest-searchservice-2026-05-01-preview&preserve-view=true) |
|--|--|--|--|--|--|--|
| ❌ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |

## Prerequisites

+ An Azure AI Search service in any [region that provides agentic retrieval](search-region-support.md).

+ A Microsoft Fabric workspace with the [required tenant settings for ontology](/fabric/iq/ontology/overview-tenant-settings) and an [ontology item](/fabric/iq/ontology/tutorial-1-create-ontology).

+ Your search service and workspace must be in the same Microsoft Entra ID tenant.

+ Permission to create and use objects on Azure AI Search. We recommend [role-based access](search-security-rbac.md), but you can use [API keys](search-security-api-keys.md) if a role assignment isn't feasible. For more information, see [Connect to a search service](search-get-started-rbac.md).

+ The [2026-05-01-preview](/rest/api/searchservice/operation-groups?view=rest-searchservice-2026-05-01-preview&preserve-view=true) version of the Search Service REST APIs.

## Check for existing knowledge sources

[!INCLUDE [](./includes/how-tos/knowledge-source-check.md)]

The following JSON is an example response for a Fabric Ontology knowledge source.

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

Run the following code to create a Fabric Ontology knowledge source.

::: zone pivot="csharp"

```csharp
using Azure;
using Azure.Search.Documents.Indexes;
using Azure.Search.Documents.Indexes.Models;

Uri searchEndpoint = new Uri("<search-service-url>");
AzureKeyCredential credential = new AzureKeyCredential("<api-key>");
var indexClient = new SearchIndexClient(searchEndpoint, credential);

var knowledgeSource = new FabricOntologyKnowledgeSource("<knowledge-source-name>")
{
    Description = "A Fabric Ontology knowledge source.",
    FabricOntologyParameters = new FabricOntologyKnowledgeSourceParameters(
        workspaceId: "<fabric-workspace-id>",
        ontologyId: "<fabric-ontology-id>"
    )
};

await indexClient.CreateOrUpdateKnowledgeSourceAsync(knowledgeSource);
```

**Reference:** [SearchIndexClient](/dotnet/api/azure.search.documents.indexes.searchindexclient?view=azure-dotnet-preview&preserve-view=true)

::: zone-end

::: zone pivot="python"

```python
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    FabricOntologyKnowledgeSource,
    FabricOntologyKnowledgeSourceParameters,
)

index_client = SearchIndexClient(
    endpoint="<search-service-url>",
    credential=AzureKeyCredential("<api-key>")
)

knowledge_source = FabricOntologyKnowledgeSource(
    name="<knowledge-source-name>",
    description="A Fabric Ontology knowledge source.",
    fabric_ontology_parameters=FabricOntologyKnowledgeSourceParameters(
        workspace_id="<fabric-workspace-id>",
        ontology_id="<fabric-ontology-id>"
    )
)

index_client.create_or_update_knowledge_source(knowledge_source)
```

**Reference:** [SearchIndexClient](/python/api/azure-search-documents/azure.search.documents.indexes.searchindexclient?view=azure-python-preview&preserve-view=true)

::: zone-end

::: zone pivot="rest"

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

::: zone-end

### Source-specific properties

The following properties apply to Fabric Ontology knowledge sources.

| Name | Description | Type | Editable | Required |
|--|--|--|--|--|
| `name` | The name of the knowledge source, which must be unique within the knowledge sources collection and follow the [naming guidelines](/rest/api/searchservice/naming-rules) for objects in Azure AI Search. | String | No | Yes |
| `kind` | The kind of knowledge source, which is `fabricOntology` in this case. | String | No | Yes |
| `description` | A description of the knowledge source. | String | Yes | No |
| `encryptionKey` | A [customer-managed key](search-security-manage-encryption-keys.md) to encrypt sensitive information in the knowledge source. | Object | Yes | No |
| `fabricOntologyParameters` | Parameters specific to the Fabric Ontology knowledge source: `workspaceId` and `ontologyId`. | Object | No | Yes |
| `workspaceId` | The [ID of the Microsoft Fabric workspace](/fabric/data-factory/migrate-pipelines-how-to-find-your-fabric-workspace-id) that contains the ontology item. Must be a valid GUID. | String | Yes | Yes |
| `ontologyId` | The ID of the ontology item to query. Must be a valid GUID. | String | Yes | Yes |

## Assign to a knowledge base

If you're satisfied with the knowledge source, continue to the next step: specify the knowledge source in a [knowledge base](agentic-retrieval-how-to-create-knowledge-base.md).

> [!NOTE]
> Fabric Ontology knowledge sources don't support the `minimal` [retrieval reasoning effort](agentic-retrieval-how-to-set-retrieval-reasoning-effort.md). Use `low` or `medium` instead.

## Query a knowledge base

After the knowledge base is configured, use the [retrieve action](agentic-retrieval-how-to-retrieve.md) to query Fabric Ontology content. This knowledge source has unique query-time permissions enforcement and response characteristics.

### Enforce permissions at query time

Fabric Ontology knowledge sources use an on-behalf-of (OBO) token flow. You pass the end-user access token in the `x-ms-query-source-authorization` header on the retrieve request. The token must be scoped to the Azure AI Search audience (`https://search.azure.com/.default`). The retrieval engine exchanges this token for a Microsoft Fabric–scoped token and uses it to query the ontology item on behalf of the end user.

Standard Azure AI Search authentication is also required on the retrieve request. The `x-ms-query-source-authorization` token is passed separately and doesn't replace service authentication.

For instructions on passing the token, see [Enforce permissions at query time](agentic-retrieval-how-to-retrieve.md#enforce-permissions-at-query-time).

### Fabric Ontology–specific response fields

Fabric Ontology knowledge sources return results in the `sourceData` object of each `references` entry and query diagnostics in the `activity` array. `sourceData` contains:

- `fabricAnswer`: The ontology's natural-language answer.
- `fabricRawData`: The structured data that grounded the answer, returned in CSV format.

The following example shows a retrieve response containing a Fabric Ontology knowledge source reference and its corresponding activity record. For broader guidance on interpreting retrieve responses, see [Review the response](agentic-retrieval-how-to-retrieve.md#review-the-response).

> [!TIP]
> To receive `sourceData` for references, set `knowledgeSourceParams.includeReferenceSourceData` to `true` on the retrieve request.

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

## Delete a knowledge source

[!INCLUDE [](./includes/how-tos/knowledge-source-delete.md)]

## Related content

+ [Agentic retrieval in Azure AI Search](agentic-retrieval-overview.md)
+ [What is a knowledge source?](agentic-knowledge-source-overview.md)
+ [Create a knowledge base](agentic-retrieval-how-to-create-knowledge-base.md)
+ [Query a knowledge base](agentic-retrieval-how-to-retrieve.md)
