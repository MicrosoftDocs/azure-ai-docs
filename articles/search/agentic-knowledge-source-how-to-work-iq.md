---
title: Create a Work IQ Knowledge Source (Preview)
description: Learn how to create a Work IQ knowledge source to ground an agentic retrieval pipeline in Azure AI Search with organizational intelligence from Work IQ.
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 06/02/2026
ai-usage: ai-assisted
zone_pivot_groups: search-csharp-python-rest
---

# Create a Work IQ knowledge source (preview)

> [!IMPORTANT]
> These features and functionality are part of the 2026-05-01-preview REST API version. The 2026-05-01-preview is licensed to you as part of your Azure subscription and is subject to the terms applicable to "Previews" in the [Microsoft Product Terms](https://www.microsoft.com/licensing/terms/welcome/welcomepage), the [Microsoft Products and Services Data Protection Addendum](https://www.microsoft.com/licensing/docs/view/Microsoft-Products-and-Services-Data-Protection-Addendum-DPA) ("DPA"), and the [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).
> 
> These 2026-05-01-preview features and functionality support connections to other Microsoft services and third-party services. Use of these services is subject to their respective terms and might result in data processing or storage outside of the Azure compliance boundary, as well as data flowing into the Azure compliance boundary.

A *Work IQ knowledge source* (preview) connects [Work IQ](/microsoft-365/copilot/extensibility/work-iq) to an agentic retrieval pipeline in Azure AI Search, providing intelligence from your organization's Microsoft 365 content as grounding data.

Unlike indexed knowledge sources, a Work IQ knowledge source (preview) queries Work IQ directly at retrieval time. No ingestion pipeline is needed. Queries require an end-user access token, which the retrieval engine uses to call Work IQ on the caller's behalf.

### Usage support

| [Azure portal](get-started-portal-agentic-retrieval.md) | [Microsoft Foundry portal](/azure/ai-foundry/agents/concepts/what-is-foundry-iq#workflow) | [.NET SDK](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/CHANGELOG.md) | [Python SDK](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [Java SDK](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [JavaScript SDK](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/search/search-documents/CHANGELOG.md) | [REST API](/rest/api/searchservice/knowledge-sources?view=rest-searchservice-2026-05-01-preview&preserve-view=true) |
|--|--|--|--|--|--|--|
| ❌ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |

## Prerequisites

+ An Azure AI Search service in any [region that provides agentic retrieval](search-region-support.md).

+ Permission to create and use objects on Azure AI Search. We recommend [role-based access](search-security-rbac.md), but you can use [API keys](search-security-api-keys.md) if a role assignment isn't feasible. For more information, see [Connect to a search service](search-get-started-rbac.md).

+ Each end user who queries through this knowledge source must have a Microsoft 365 Copilot license.

+ The Azure AI Search service, the Work IQ environment, and end users must be in the same Microsoft Entra tenant. Cross-tenant retrieval isn't supported.

+ Approved access to Work IQ retrieval through Azure AI Search. For more information, see [Request access to Work IQ retrieval](#request-access-to-work-iq-retrieval).

+ The [2026-05-01-preview](/rest/api/searchservice/operation-groups?view=rest-searchservice-2026-05-01-preview&preserve-view=true) version of the Search Service REST APIs.

### Request access to Work IQ retrieval

Work IQ retrieval through Azure AI Search is off by default and requires a Microsoft-approved request before use.

To request access:

1. Register the `EnableFoundryIQWithWorkIQ` feature flag on your Azure subscription.

   ```azurecli
   az feature register --namespace Microsoft.Search --name EnableFoundryIQWithWorkIQ --subscription "<your-subscription-guid>"
   ```

1. Have a Microsoft Entra administrator for your tenant submit the following form: [FORM](form) <!-- TO-DO (PM): Add form link when available. -->
    
1. Wait for Microsoft to enable access manually after reviewing and approving the request.

> [!TIP]
> Registering a preview feature requires the **Owner** or **Contributor** built-in role on the subscription, which is a separate role from the Microsoft Entra administrator who submits the form. The two responsibilities can be held by different people in your organization. For more information about the registration mechanism, see [Set up preview features in Azure subscription](/azure/azure-resource-manager/management/preview-features).

## Check for existing knowledge sources

[!INCLUDE [](./includes/how-tos/knowledge-source-check.md)]

The following JSON is an example response for a Work IQ knowledge source (preview).

```json
{
  "name": "my-workiq-ks",
  "kind": "workIQ",
  "description": "A sample Work IQ knowledge source.",
  "encryptionKey": null
}
```

## Create a knowledge source

Run the following code to create a Work IQ knowledge source (preview).

::: zone pivot="csharp"

```csharp
using Azure;
using Azure.Search.Documents.Indexes;
using Azure.Search.Documents.Indexes.Models;

var indexClient = new SearchIndexClient(new Uri(searchEndpoint), new AzureKeyCredential(apiKey));

// TO-DO (PM): Verify class name WorkIQKnowledgeSource
var knowledgeSource = new WorkIQKnowledgeSource(name: "my-workiq-ks")
{
    Description = "A sample Work IQ knowledge source."
};

await indexClient.CreateOrUpdateKnowledgeSourceAsync(knowledgeSource);
Console.WriteLine($"Knowledge source '{knowledgeSource.Name}' created or updated successfully.");
```

**Reference:** [SearchIndexClient](/dotnet/api/azure.search.documents.indexes.searchindexclient?view=azure-dotnet-preview&preserve-view=true)

::: zone-end

::: zone pivot="python"

```python
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import WorkIQKnowledgeSource  # TO-DO (PM): Verify class name

index_client = SearchIndexClient(endpoint=search_endpoint, credential=AzureKeyCredential(api_key))

knowledge_source = WorkIQKnowledgeSource(
    name="my-workiq-ks",
    description="A sample Work IQ knowledge source."
)

index_client.create_or_update_knowledge_source(knowledge_source=knowledge_source)
print(f"Knowledge source '{knowledge_source.name}' created or updated successfully.")
```

**Reference:** [SearchIndexClient](/python/api/azure-search-documents/azure.search.documents.indexes.searchindexclient?view=azure-python-preview&preserve-view=true)

::: zone-end

::: zone pivot="rest"

```http
### Create a Work IQ knowledge source
PUT {{search-url}}/knowledgesources/my-workiq-ks?api-version=2026-05-01-preview
api-key: {{api-key}}
Content-Type: application/json

{
  "name": "my-workiq-ks",
  "kind": "workIQ",
  "description": "A sample Work IQ knowledge source."
}
```

**Reference:** [Knowledge Sources - Create or Update](/rest/api/searchservice/knowledge-sources/create-or-update?view=rest-searchservice-2026-05-01-preview&preserve-view=true)

::: zone-end

### Source-specific properties

<!-- TO-DO (PM): Confirm whether these properties are correct for Work IQ knowledge sources and update as needed. -->

The following properties apply to Work IQ knowledge sources (preview).

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

<!-- TO-DO (PM): Confirm the following details about query-time permissions and response characteristics for Work IQ knowledge sources and update as needed. -->

> [!IMPORTANT]
> Work IQ can take 40–60 seconds or more to respond. To avoid timeout errors, set `maxRuntimeInSeconds` on the retrieve request to `120` or higher.

### Enforce permissions at query time

Work IQ knowledge sources (preview) use an on-behalf-of (OBO) token flow. You pass an access token scoped to the Azure AI Search audience (`https://search.azure.com/.default`) on the retrieve request. The retrieval engine exchanges this token for a Work IQ–scoped token and uses it to query Work IQ on behalf of the end user.

Because Work IQ knowledge sources (preview) don't use a search index, no ingestion-time permissions configuration is needed. The access token is the only requirement.

For instructions on passing the token, see [Enforce permissions at query time](agentic-retrieval-how-to-retrieve.md#enforce-permissions-at-query-time).

### Work IQ–specific response fields

Work IQ knowledge sources (preview) return results in the `references` array and query diagnostics in the `activity` array. Each reference entry contains:

- `sourceData.extracts[].text`: Grounded text passages from Work IQ.
- `attributions[].seeMoreWebUrl`: A link to the source document in Microsoft 365.

The following example shows a retrieve response containing a Work IQ knowledge source reference and its corresponding activity record. For broader guidance on interpreting retrieve responses, see [Review the response](agentic-retrieval-how-to-retrieve.md#review-the-response).

```json
{
  "response": [
      // ... Response omitted for brevity
  ],
  "activity": [
    {
      "type": "workIQ",
      "id": 0,
      "knowledgeSourceName": "my-workiq-ks",
      "queryTime": "2026-05-01T19:25:23.683Z",
      "count": 1,
      "elapsedMs": 1137,
      "workIQArguments": {
        "search": "my query"
      }
    },
    {
       // ... Additional activity records omitted for brevity       
    }
  ],
  "references": [
    {
      "type": "workIQ",
      "id": "83dd7d40",
      "activitySource": 0,
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

[!INCLUDE [](./includes/how-tos/knowledge-source-delete.md)]

## Related content

+ [Agentic retrieval in Azure AI Search](agentic-retrieval-overview.md)
+ [What is a knowledge source?](agentic-knowledge-source-overview.md)
+ [Create a knowledge base](agentic-retrieval-how-to-create-knowledge-base.md)
+ [Query a knowledge base](agentic-retrieval-how-to-retrieve.md)
