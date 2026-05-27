---
title: Create a Fabric Data Agent Knowledge Source
description: Learn how to create a Fabric Data Agent knowledge source, which connects a Microsoft Fabric Data Agent to an agentic retrieval pipeline in Azure AI Search for live, data-driven answers as grounding data.
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 06/02/2026
ai-usage: ai-assisted
zone_pivot_groups: search-csharp-python-rest
---

# Create a Fabric Data Agent knowledge source (preview)

> [!IMPORTANT]
> These features and functionality are part of the 2026-05-01-preview REST API. The 2026-05-01-preview is licensed to you as part of your Azure subscription and is subject to the terms applicable to "Previews" in the [Microsoft Product Terms](https://www.microsoft.com/licensing/terms/welcome/welcomepage), the [Microsoft Products and Services Data Protection Addendum](https://www.microsoft.com/licensing/docs/view/Microsoft-Products-and-Services-Data-Protection-Addendum-DPA) ("DPA"), and the [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).
>
> The 2026-05-01-preview supports connections to other Microsoft services and third-party services. Use of these services is subject to their respective terms and might result in data processing or storage outside of the Azure compliance boundary, as well as data flowing into the Azure compliance boundary.
>
> When you connect to Fabric IQ, you might incur costs, and data might be sent outside the Azure compliance boundary and processed according to the applicable service terms and data handling policies. It's your responsibility to manage whether your data will flow outside of your organization's compliance and geographic boundaries and any related implications, and that appropriate permissions, boundaries, and approvals are provisioned.
>
> You're responsible for carefully reviewing and testing applications you build in the context of your specific use cases and making all appropriate decisions and customizations. This includes implementing your own responsible AI mitigations, such as metaprompts, content filters, or other safety systems, and ensuring your applications meet appropriate quality, reliability, security, and trustworthiness standards. For more information, see the [Azure AI Search Transparency Note](/azure/foundry/responsible-ai/search/transparency-note).

A *Fabric Data Agent knowledge source* (preview) connects your [Microsoft Fabric Data Agent](/fabric/data-science/concept-data-agent) to an agentic retrieval pipeline in Azure AI Search. The data agent acts as a virtual analyst, generating and running queries against your live Microsoft Fabric data to return natural-language answers, tables, and charts as grounding data.

Unlike indexed knowledge sources, Fabric Data Agent knowledge sources query live data directly at retrieval time. No ingestion pipeline is needed. Queries require an end-user access token, which the retrieval engine uses to query the Fabric Data Agent on behalf of the end user.

### Usage support

| [Azure portal](get-started-portal-agentic-retrieval.md) | [Microsoft Foundry portal](/azure/ai-foundry/agents/concepts/what-is-foundry-iq#workflow) | [.NET SDK](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/CHANGELOG.md) | [Python SDK](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [Java SDK](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [JavaScript SDK](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/search/search-documents/CHANGELOG.md) | [REST API](/rest/api/searchservice/knowledge-sources?view=rest-searchservice-2026-05-01-preview&preserve-view=true) |
|--|--|--|--|--|--|--|
| ❌ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |

## Prerequisites

+ An Azure AI Search service in any [region that provides agentic retrieval](search-region-support.md).

+ A Microsoft Fabric workspace with a [data agent](/fabric/data-science/how-to-create-data-agent).

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

[!INCLUDE [](./includes/how-tos/knowledge-source-check.md)]

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

::: zone pivot="csharp"

```csharp
using Azure;
using Azure.Search.Documents.Indexes;
using Azure.Search.Documents.Indexes.Models;

Uri searchEndpoint = new Uri("<search-service-url>");
AzureKeyCredential credential = new AzureKeyCredential("<api-key>");
var indexClient = new SearchIndexClient(searchEndpoint, credential);

var fabricDataAgent = new FabricDataAgentKnowledgeSource(
    "<knowledge-source-name>",
    new FabricDataAgentKnowledgeSourceParameters("<fabric-workspace-id>", "<fabric-data-agent-id>"))
{
    Description = "A Fabric Data Agent knowledge source."
};

await indexClient.CreateOrUpdateKnowledgeSourceAsync(fabricDataAgent);
```

**Reference:** [SearchIndexClient](/dotnet/api/azure.search.documents.indexes.searchindexclient?view=azure-dotnet-preview&preserve-view=true)

::: zone-end

::: zone pivot="python"

```python
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    FabricDataAgentKnowledgeSource,
    FabricDataAgentKnowledgeSourceParameters,
)

index_client = SearchIndexClient(
    endpoint="<search-service-url>",
    credential=AzureKeyCredential("<api-key>")
)

knowledge_source = FabricDataAgentKnowledgeSource(
    name="<knowledge-source-name>",
    description="A Fabric Data Agent knowledge source.",
    fabric_data_agent_parameters=FabricDataAgentKnowledgeSourceParameters(
        workspace_id="<fabric-workspace-id>",
        data_agent_id="<fabric-data-agent-id>"
    )
)

index_client.create_or_update_knowledge_source(knowledge_source)
```

**Reference:** [SearchIndexClient](/python/api/azure-search-documents/azure.search.documents.indexes.searchindexclient?view=azure-python-preview&preserve-view=true)

::: zone-end

::: zone pivot="rest"

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

::: zone-end

### Source-specific properties

The following properties apply to Fabric Data Agent knowledge sources.

| Name | Description | Type | Editable | Required |
|--|--|--|--|--|
| `name` | The name of the knowledge source, which must be unique within the knowledge sources collection and follow the [naming guidelines](/rest/api/searchservice/naming-rules) for objects in Azure AI Search. | String | No | Yes |
| `kind` | The kind of knowledge source, which is `fabricDataAgent` in this case. | String | No | Yes |
| `description` | A description of the knowledge source. | String | Yes | No |
| `encryptionKey` | A [customer-managed key](search-security-manage-encryption-keys.md) to encrypt sensitive information in the knowledge source. | Object | Yes | No |
| `fabricDataAgentParameters` | Parameters specific to the Fabric Data Agent knowledge source: `workspaceId` and `dataAgentId`. | Object | No | Yes |
| `workspaceId` | The [ID of the Microsoft Fabric workspace](/fabric/data-factory/migrate-pipelines-how-to-find-your-fabric-workspace-id) that contains the data agent. | String | No | Yes |
| `dataAgentId` | The ID of the data agent to query. | String | No | Yes |

## Assign to a knowledge base

If you're satisfied with the knowledge source, continue to the next step: specify the knowledge source in a [knowledge base](agentic-retrieval-how-to-create-knowledge-base.md).

> [!IMPORTANT]
> Fabric Data Agent knowledge sources don't support the `minimal` [retrieval reasoning effort](agentic-retrieval-how-to-set-retrieval-reasoning-effort.md). Use `low` or `medium` instead.

## Query a knowledge base

After the knowledge base is configured, use the [retrieve action](agentic-retrieval-how-to-retrieve.md) to query Fabric Data Agent content. This knowledge source has unique query-time permissions enforcement and response characteristics.

### Enforce permissions at query time

Fabric Data Agent knowledge sources use an on-behalf-of (OBO) token flow. You pass the end-user access token in the `x-ms-query-source-authorization` header on the retrieve request. The token must be scoped to the Azure AI Search audience (`https://search.azure.com/.default`). The retrieval engine exchanges this token for a Microsoft Fabric–scoped token and uses it to query the Fabric Data Agent on behalf of the end user.

Standard Azure AI Search authentication is also required on the retrieve request. The `x-ms-query-source-authorization` token is passed separately and doesn't replace service authentication.

For instructions on passing the token, see [Enforce permissions at query time](agentic-retrieval-how-to-retrieve.md#enforce-permissions-at-query-time-preview).

### Fabric Data Agent–specific response fields

Fabric Data Agent knowledge sources return results in the `sourceData` object of each `references` entry and query diagnostics in the `activity` array. `sourceData` contains:

- `fabricAnswer`: The data agent's natural-language answer.
- `fabricEmbeddedResources`: Any embedded resources, such as tables and charts, when the query produces structured output.

The following example shows a retrieve response containing a Fabric Data Agent knowledge source reference and its corresponding activity record. For broader guidance on interpreting retrieve responses, see [Review the response](agentic-retrieval-how-to-retrieve.md#review-the-response).

> [!TIP]
> To receive `sourceData` for references, set `includeReferenceSourceData` to `true` on the knowledge source entry within `knowledgeSourceParams` on the retrieve request.

```json
{
  "response": [
      // ... Response omitted for brevity
  ],
  "activity": [
    {
      "type": "fabricDataAgent",
      "id": 1,
      "knowledgeSourceName": "my-fabric-data-agent-ks",
      "queryTime": "2026-05-11T19:37:11.600Z",
      "count": 1,
      "fabricDataAgentArguments": {
        "search": "my query"
      }
    },
    {
      // ... Additional activity records omitted for brevity 
    }
  ],
  "references": [
    {
      "type": "fabricDataAgent",
      "id": "0",
      "activitySource": 1,
      "rerankerScore": 2.57,
      "workspaceId": "00000000-0000-0000-0000-000000000000",
      "dataAgentId": "00000000-0000-0000-0000-000000000001",
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
