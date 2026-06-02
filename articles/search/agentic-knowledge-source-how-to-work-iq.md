---
title: Create a Work IQ Knowledge Source
description: Learn how to create a Work IQ knowledge source to ground an agentic retrieval pipeline in Azure AI Search with organizational intelligence from Work IQ.
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 06/02/2026
ai-usage: ai-assisted
zone_pivot_groups: search-csharp-python-rest
---

# Create a Work IQ knowledge source (preview)

> [!IMPORTANT]
> These features and functionality are part of the 2026-05-01-preview REST API. The 2026-05-01-preview is licensed to you as part of your Azure subscription and is subject to the terms applicable to "Previews" in the [Microsoft Product Terms](https://www.microsoft.com/licensing/terms/welcome/welcomepage), the [Microsoft Products and Services Data Protection Addendum](https://www.microsoft.com/licensing/docs/view/Microsoft-Products-and-Services-Data-Protection-Addendum-DPA) ("DPA"), and the [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).
> 
> The 2026-05-01-preview supports connections to other Microsoft services and third-party services. Use of these services is subject to their respective terms and might result in data processing or storage outside of the Azure compliance boundary, as well as data flowing into the Azure compliance boundary.
>
> When you connect to Work IQ, you might incur costs, and data might be sent outside the Azure compliance boundary and processed according to the applicable service terms and data handling policies. It's your responsibility to manage whether your data will flow outside of your organization's compliance and geographic boundaries and any related implications, and that appropriate permissions, boundaries, and approvals are provisioned.
>
> You're responsible for carefully reviewing and testing applications you build in the context of your specific use cases and making all appropriate decisions and customizations. This includes implementing your own responsible AI mitigations, such as metaprompts, content filters, or other safety systems, and ensuring your applications meet appropriate quality, reliability, security, and trustworthiness standards. For more information, see the [Azure AI Search Transparency Note](/azure/foundry/responsible-ai/search/transparency-note).

A *Work IQ knowledge source* (preview) connects [Work IQ](/microsoft-365/copilot/extensibility/work-iq) to an agentic retrieval pipeline in Azure AI Search, providing intelligence from your organization's Microsoft 365 content as grounding data.

Unlike indexed knowledge sources, a Work IQ knowledge source queries Work IQ directly at retrieval time. No ingestion pipeline is needed. Queries require an end-user access token, which the retrieval engine uses to call Work IQ on the caller's behalf.

> [!WARNING]
> In this preview, a Work IQ knowledge source may use Work IQ capabilities that perform actions, not just retrieve information. Use it with care, limit access to trusted applications and users, and review your scenario's permissions and governance controls before enabling it.

### Usage support

| [Azure portal](get-started-portal-agentic-retrieval.md) | [Microsoft Foundry portal](/azure/ai-foundry/agents/concepts/what-is-foundry-iq#workflow) | [.NET SDK](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/CHANGELOG.md) | [Python SDK](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [Java SDK](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [JavaScript SDK](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/search/search-documents/CHANGELOG.md) | [REST API](/rest/api/searchservice/knowledge-sources?view=rest-searchservice-2026-05-01-preview&preserve-view=true) |
|--|--|--|--|--|--|--|
| ❌ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |

## Prerequisites

+ An Azure AI Search service in any [region that provides agentic retrieval](search-region-support.md).

+ Each end user who queries through this knowledge source must have a Microsoft 365 Copilot license.

+ The Azure AI Search service, the Work IQ environment, and end users must be in the same Microsoft Entra tenant. Cross-tenant retrieval isn't supported.

+ Approved access to Work IQ retrieval through Azure AI Search. For more information, see [Request access to Work IQ retrieval](#request-access-to-work-iq-retrieval).

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

## Request access to Work IQ retrieval

Work IQ retrieval through Azure AI Search is off by default and requires a Microsoft-approved request before use.

To request access:

1. Register the `EnableFoundryIQWithWorkIQ` feature flag on your Azure subscription.

   ```azurecli
   az feature register --namespace Microsoft.Search --name EnableFoundryIQWithWorkIQ --subscription "<your-subscription-guid>"
   ```

1. Re-register the `Microsoft.Search` resource provider.

   ```azurecli
   az provider register -n Microsoft.Search --subscription "<your-subscription-guid>"
   ```

1. Have a Microsoft Entra administrator for your tenant submit the [Work IQ access request form](https://aka.ms/foundry-iq-work-iq-admin-consent-form).
    
1. Wait for Microsoft to enable access after reviewing and approving the request.

    > [!TIP]
    > Registering a preview feature requires the **Owner** or **Contributor** built-in role on the subscription, which is a separate role from the Microsoft Entra administrator who submits the form. The two responsibilities can be held by different people in your organization. For more information about the registration mechanism, see [Set up preview features in Azure subscription](/azure/azure-resource-manager/management/preview-features).

## Data governance and compliance

Work IQ operates entirely within the Microsoft 365 trust boundary. The following commitments apply when you route agent requests through Work IQ.

### Data residency

Work IQ retrieves data from your organization's Microsoft 365 tenant. Data doesn't leave your tenant or cross regional boundaries during retrieval. The data's location follows your Microsoft 365 tenant data residency configuration, not your Azure AI Search service region. For details, see [Data, Privacy, and Security for Microsoft 365 Copilot](/microsoft-365/copilot/microsoft-365-copilot-privacy).

### Privacy and data handling

All Work IQ requests are governed by [Data, Privacy, and Security for Microsoft 365 Copilot](/microsoft-365/copilot/microsoft-365-copilot-privacy). Key commitments:

- Work IQ doesn't use customer content to train or improve underlying AI models.

### Access control and permissions

Work IQ enforces Microsoft 365 permissions automatically on every request. Agents can only access data that the signed-in user is already authorized to see. No elevation of privilege is possible.

- Role-based access control, sensitivity labels, and information barriers defined in Microsoft 365 are respected.

### Compliance certifications

Work IQ inherits Microsoft 365's compliance certifications. For details, see [Data, Privacy, and Security for Microsoft 365 Copilot](/microsoft-365/copilot/microsoft-365-copilot-privacy).

## Check for existing knowledge sources

[!INCLUDE [](./includes/how-tos/knowledge-source-check.md)]

The following JSON is an example response for a Work IQ knowledge source.

```json
{
  "name": "my-workiq-ks",
  "kind": "workIQ",
  "description": "A sample Work IQ knowledge source.",
  "encryptionKey": null
}
```

## Create a knowledge source

Run the following code to create a Work IQ knowledge source.

::: zone pivot="csharp"

```csharp
using Azure;
using Azure.Search.Documents.Indexes;
using Azure.Search.Documents.Indexes.Models;

Uri searchEndpoint = new Uri("<search-service-url>");
AzureKeyCredential credential = new AzureKeyCredential("<api-key>");
var indexClient = new SearchIndexClient(searchEndpoint, credential);

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
from azure.search.documents.indexes.models import WorkIQKnowledgeSource

index_client = SearchIndexClient(
    endpoint="<search-service-url>",
    credential=AzureKeyCredential("<api-key>")
)

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

Work IQ knowledge sources use an on-behalf-of (OBO) token flow. You pass the end-user access token in the `x-ms-query-source-authorization` header on the retrieve request. The token must be scoped to the Azure AI Search audience (`https://search.azure.com/.default`). The retrieval engine exchanges this token for a Work IQ–scoped token and uses it to query Work IQ on behalf of the end user.

Standard Azure AI Search authentication is also required on the retrieve request. The `x-ms-query-source-authorization` token is passed separately and doesn't replace service authentication.

For instructions on passing the token, see [Enforce permissions at query time](agentic-retrieval-how-to-retrieve.md#enforce-permissions-at-query-time-preview).

### Work IQ–specific response fields

Work IQ knowledge sources return results in the `references` array and query diagnostics in the `activity` array. Each reference entry contains:

- `sourceData.extracts[].text`: Grounded text passages from Work IQ.
- `attributions[].seeMoreWebUrl`: A link to the source document in Microsoft 365.

The following example shows a retrieve response containing a Work IQ knowledge source reference and its corresponding activity record. For broader guidance on interpreting retrieve responses, see [Review the response](agentic-retrieval-how-to-retrieve.md#review-the-response).

> [!TIP]
> To receive `sourceData` for references, set `includeReferenceSourceData` to `true` on the knowledge source entry within `knowledgeSourceParams` on the retrieve request.

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

## Delete a knowledge source

[!INCLUDE [](./includes/how-tos/knowledge-source-delete.md)]

## Related content

+ [Agentic retrieval in Azure AI Search](agentic-retrieval-overview.md)
+ [What is a knowledge source?](agentic-knowledge-source-overview.md)
+ [Create a knowledge base](agentic-retrieval-how-to-create-knowledge-base.md)
+ [Query a knowledge base](agentic-retrieval-how-to-retrieve.md)
