---
title: Create a Fabric Ontology Knowledge Source
description: Learn how to create a Fabric Ontology knowledge source, which connects a Microsoft Fabric ontology to an agentic retrieval pipeline in Azure AI Search for ontology-backed answers.
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 06/02/2026
ai-usage: ai-assisted
zone_pivot_groups: search-csharp-python-rest
---

# Create a Fabric Ontology knowledge source (preview)

> [!IMPORTANT]
> These features and functionality are part of the 2026-05-01-preview REST API. The 2026-05-01-preview is licensed to you as part of your Azure subscription and is subject to the terms applicable to "Previews" in the [Microsoft Product Terms](https://www.microsoft.com/licensing/terms/welcome/welcomepage), the [Microsoft Products and Services Data Protection Addendum](https://www.microsoft.com/licensing/docs/view/Microsoft-Products-and-Services-Data-Protection-Addendum-DPA) ("DPA"), and the [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).
>
> The 2026-05-01-preview supports connections to other Microsoft services and third-party services. Use of these services is subject to their respective terms and might result in data processing or storage outside of the Azure compliance boundary, as well as data flowing into the Azure compliance boundary.
>
> When you connect to Fabric IQ, you might incur costs, and data might be sent outside the Azure compliance boundary and processed according to the applicable service terms and data handling policies. It's your responsibility to manage whether your data will flow outside of your organization's compliance and geographic boundaries and any related implications, and that appropriate permissions, boundaries, and approvals are provisioned.
>
> You're responsible for carefully reviewing and testing applications you build in the context of your specific use cases and making all appropriate decisions and customizations. This includes implementing your own responsible AI mitigations, such as metaprompts, content filters, or other safety systems, and ensuring your applications meet appropriate quality, reliability, security, and trustworthiness standards. For more information, see the [Azure AI Search Transparency Note](/azure/foundry/responsible-ai/search/transparency-note).

A *Fabric Ontology knowledge source* (preview) connects your [Microsoft Fabric ontology](/fabric/iq/ontology/overview) to an agentic retrieval pipeline in Azure AI Search. [Knowledge sources](agentic-knowledge-source-overview.md) are created independently, referenced in a [knowledge base](agentic-retrieval-how-to-create-knowledge-base.md), and used as grounding data when the knowledge base is [queried at runtime](agentic-retrieval-how-to-retrieve.md).

Because ontologies capture how your business defines its data, agents can answer in business terms rather than reasoning over raw tables and columns. This makes Fabric Ontology knowledge sources useful when you want retrieval grounded in business concepts and relationships instead of raw schema details.

Unlike indexed knowledge sources, Fabric Ontology knowledge sources query live data directly at retrieval time. No ingestion pipeline is needed. Queries require an end-user access token, which the retrieval engine uses to authenticate with Microsoft Fabric on the caller's behalf.

### Usage support

| [Azure portal](get-started-portal-agentic-retrieval.md) | [Microsoft Foundry portal](/azure/ai-foundry/agents/concepts/what-is-foundry-iq#workflow) | [.NET SDK](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/CHANGELOG.md) | [Python SDK](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [Java SDK](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [JavaScript SDK](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/search/search-documents/CHANGELOG.md) | [REST API](/rest/api/searchservice/knowledge-sources?view=rest-searchservice-2026-05-01-preview&preserve-view=true) |
|--|--|--|--|--|--|--|
| ❌ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |

## Prerequisites

+ An Azure AI Search service in any [region that provides agentic retrieval](search-region-support.md).

+ A Microsoft Fabric workspace with the [required tenant settings for ontology](/fabric/iq/ontology/overview-tenant-settings) and an [ontology item](/fabric/iq/ontology/tutorial-1-create-ontology).

+ Your search service and workspace must be in the same Microsoft Entra ID tenant.

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

## Data governance and compliance

Fabric IQ processes requests within the Microsoft Fabric compliance boundary for your workspace's region. The following commitments apply when you route agent queries through Fabric IQ.

### Data residency

Fabric IQ retrieves and processes data within the region where your Microsoft Fabric workspace resides. Data doesn't cross regional boundaries during query execution. The applicable region and its compliance scope are determined by your workspace location. For the list of supported regions and the compliance frameworks each region satisfies, see [Microsoft Fabric region availability](/fabric/admin/region-availability).

> [!NOTE]
> If your Azure AI Search service is in a different Azure region than your Fabric workspace, query results are returned cross-region. Review [Microsoft Fabric region availability](/fabric/admin/region-availability) and your organization's data residency requirements before connecting a Fabric workspace in a different region.

### Compliance certifications

Fabric IQ inherits Microsoft Fabric's compliance certifications for the workspace region. For compliance documentation, audit reports, and the frameworks applicable to each region, see [Microsoft Fabric region availability](/fabric/admin/region-availability).

## Check for existing knowledge sources

[!INCLUDE [Check for existing knowledge sources](includes/how-tos/knowledge-source-check.md)]

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

var fabricOntology = new FabricOntologyKnowledgeSource(
    "<knowledge-source-name>",
    new FabricOntologyKnowledgeSourceParameters("<fabric-workspace-id>", "<fabric-ontology-id>"))
{
    Description = "A Fabric Ontology knowledge source."
};

await indexClient.CreateOrUpdateKnowledgeSourceAsync(fabricOntology);
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

If you're satisfied with the knowledge source, [add it to a knowledge base](agentic-retrieval-how-to-create-knowledge-base.md).

> [!NOTE]
> Fabric Ontology knowledge sources don't support the `minimal` [retrieval reasoning effort](agentic-retrieval-how-to-set-retrieval-reasoning-effort.md). Use `low` or `medium` instead.

## Query a knowledge base

After the knowledge base is configured, [call the retrieve action or MCP endpoint](agentic-retrieval-how-to-retrieve.md) to query Fabric Ontology content. This knowledge source has unique query-time permissions enforcement and response characteristics.

### Enforce permissions at query time

Fabric Ontology knowledge sources use an on-behalf-of (OBO) token flow. You pass the end-user access token in the `x-ms-query-source-authorization` header on the retrieve request. The token must be scoped to the Azure AI Search audience (`https://search.azure.com/.default`). The retrieval engine exchanges this token for a Microsoft Fabric–scoped token and uses it to query the ontology item on behalf of the end user.

Standard Azure AI Search authentication is also required on the retrieve request. The `x-ms-query-source-authorization` token is passed separately and doesn't replace service authentication.

For instructions on passing the token, see [Enforce permissions at query time](agentic-retrieval-how-to-retrieve.md#enforce-permissions-at-query-time-preview).

### Fabric Ontology–specific response fields

Fabric Ontology knowledge sources return results in the `sourceData` object of each `references` entry and query diagnostics in the `activity` array. `sourceData` contains:

- `fabricAnswer`: The ontology's natural-language answer.
- `fabricRawData`: The structured data that grounded the answer, returned in CSV format.

The following example shows a retrieve response containing a Fabric Ontology knowledge source reference and its corresponding activity record. For broader guidance on interpreting retrieve responses, see [Review the response](agentic-retrieval-how-to-retrieve.md#review-the-response).

> [!TIP]
> To receive `sourceData` for references, set `includeReferenceSourceData` to `true` on the knowledge source entry within `knowledgeSourceParams` on the retrieve request.

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

[!INCLUDE [Delete a knowledge source](includes/how-tos/knowledge-source-delete.md)]

## Related content

+ [Agentic retrieval in Azure AI Search](agentic-retrieval-overview.md)
+ [What is a knowledge source?](agentic-knowledge-source-overview.md)
+ [Create a knowledge base](agentic-retrieval-how-to-create-knowledge-base.md)
+ [Query a knowledge base](agentic-retrieval-how-to-retrieve.md)
