---
title: Query Knowledge Base via APIs or MCP
description: Learn how to Query a knowledge base using the retrieve action or MCP endpoint in Azure AI Search using REST APIs, Azure SDKs, or any MCP-compatible client.
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 04/23/2026
ai-usage: ai-assisted
zone_pivot_groups: search-csharp-python-rest
---

# Query a knowledge base using the retrieve action or MCP endpoint

[!INCLUDE [GA feature](./includes/previews/agentic-retrieval-ga-feature.md)]

In an agentic retrieval pipeline, the [retrieve action](/rest/api/searchservice/knowledge-retrieval/retrieve) invokes parallel query processing from a knowledge base. You can call the retrieve action directly using the Search Service REST APIs or an Azure SDK. Each knowledge base also exposes a Model Context Protocol (MCP) endpoint for consumption by MCP-compatible agents.

This article explains how to call both retrieval methods with optional permissions enforcement and interpret the three-pronged response. To set up a pipeline that connects Azure AI Search to Foundry Agent Service via MCP, see [Tutorial: Build an end-to-end agentic retrieval solution](agentic-retrieval-how-to-create-pipeline.md).

## Prerequisites

+ An Azure AI Search service with a [knowledge base](agentic-retrieval-how-to-create-knowledge-base.md).

+ Permissions to query the knowledge base. Configure [keyless authentication](search-get-started-rbac.md) with the **Search Index Data Reader** role assigned to your user account (recommended) or use an [API key](search-security-api-keys.md).

+ If the knowledge base specifies an LLM, the search service must have a [managed identity](search-how-to-managed-identities.md) with **Cognitive Services User** permissions on the Microsoft Foundry resource.

::: zone pivot="csharp"

+ Required [Azure.Search.Documents](https://www.nuget.org/packages/Azure.Search.Documents) package:

  + For 2025-11-01-preview features, the latest preview package: `dotnet add package Azure.Search.Documents --prerelease`

  + For 2026-04-01 features, the latest stable package: `dotnet add package Azure.Search.Documents`

::: zone-end

::: zone pivot="python"

+ Required [azure-search-documents](https://pypi.org/project/azure-search-documents/) package:

  + For 2025-11-01-preview features, the latest preview package: `pip install azure-search-documents --pre`

  + For 2026-04-01 features, the latest stable package: `pip install azure-search-documents`

::: zone-end

::: zone pivot="rest"

+ Required REST API version:

  + For preview features: [Search Service 2025-11-01-preview](/rest/api/searchservice/operation-groups?view=rest-searchservice-2025-11-01-preview&preserve-view=true)

  + For generally available features: [Search Service 2026-04-01](/rest/api/searchservice/operation-groups?view=rest-searchservice-2026-04-01&preserve-view=true)

::: zone-end

## Call the retrieve action

You specify the retrieve action on a knowledge base. The request body includes the query input and an optional list of knowledge sources to target.

:::zone pivot="csharp"

# [2025-11-01-preview](#tab/2025-11-01-preview)

```csharp
using Azure.Identity;
using Azure.Search.Documents.KnowledgeBases;
using Azure.Search.Documents.KnowledgeBases.Models;

// Create knowledge base retrieval client
var kbClient = new KnowledgeBaseRetrievalClient(
    endpoint: new Uri("<YOUR SEARCH SERVICE URL>"),
    knowledgeBaseName: "<YOUR KNOWLEDGE BASE NAME>",
    tokenCredential: new DefaultAzureCredential()
);

var retrievalRequest = new KnowledgeBaseRetrievalRequest();
retrievalRequest.Messages.Add(
    new KnowledgeBaseMessage(
        content: new[] {
            new KnowledgeBaseMessageTextContent(
                "You can answer questions about the Earth at night. "
                + "Sources have a JSON format with a ref_id that must be cited in the answer. "
                + "If you do not have the answer, respond with 'I do not know'."
            )
        }
    ) { Role = "assistant" }
);
retrievalRequest.Messages.Add(
    new KnowledgeBaseMessage(
        content: new[] {
            new KnowledgeBaseMessageTextContent(
                "Why is the Phoenix nighttime street grid so sharply visible from space, "
                + "whereas large stretches of the interstate between midwestern cities remain comparatively dim?"
            )
        }
    ) { Role = "user" }
);

var result = await kbClient.RetrieveAsync(retrievalRequest);
Console.WriteLine(
    (result.Value.Response[0].Content[0] as KnowledgeBaseMessageTextContent)!.Text
);
```

**Reference:** [KnowledgeBaseRetrievalClient](/dotnet/api/azure.search.documents.knowledgebases.knowledgebaseretrievalclient?view=azure-dotnet-preview&preserve-view=true), [KnowledgeBaseRetrievalRequest](/dotnet/api/azure.search.documents.knowledgebases.models.knowledgebaseretrievalrequest?view=azure-dotnet-preview&preserve-view=true)

# [2026-04-01](#tab/2026-04-01)

```csharp
using Azure.Identity;
using Azure.Search.Documents.KnowledgeBases;
using Azure.Search.Documents.KnowledgeBases.Models;

// Create knowledge base retrieval client
var kbClient = new KnowledgeBaseRetrievalClient(
    endpoint: new Uri("<YOUR SEARCH SERVICE URL>"),
    knowledgeBaseName: "<YOUR KNOWLEDGE BASE NAME>",
    tokenCredential: new DefaultAzureCredential()
);

var retrievalRequest = new KnowledgeBaseRetrievalRequest();
retrievalRequest.Intents.Add(
    new KnowledgeRetrievalSemanticIntent(
        "Why is the Phoenix nighttime street grid so sharply visible from space, "
        + "whereas large stretches of the interstate between midwestern cities remain comparatively dim?"
    )
);

var result = await kbClient.RetrieveAsync(retrievalRequest);
Console.WriteLine(
    (result.Value.Response[0].Content[0] as KnowledgeBaseMessageTextContent)!.Text
);
```

**Reference:** [KnowledgeBaseRetrievalClient](/dotnet/api/azure.search.documents.knowledgebases.knowledgebaseretrievalclient?view=azure-dotnet&preserve-view=true), [KnowledgeBaseRetrievalRequest](/dotnet/api/azure.search.documents.knowledgebases.models.knowledgebaseretrievalrequest?view=azure-dotnet&preserve-view=true)

---

:::zone-end

:::zone pivot="python"

# [2025-11-01-preview](#tab/2025-11-01-preview)

```python
from azure.identity import DefaultAzureCredential
from azure.search.documents.knowledgebases import KnowledgeBaseRetrievalClient
from azure.search.documents.knowledgebases.models import (
    KnowledgeBaseMessage,
    KnowledgeBaseMessageTextContent,
    KnowledgeBaseRetrievalRequest,
    SearchIndexKnowledgeSourceParams,
)

# Create knowledge base retrieval client
kb_client = KnowledgeBaseRetrievalClient(
    endpoint="<YOUR SEARCH SERVICE URL>",
    knowledge_base_name="<YOUR KNOWLEDGE BASE NAME>",
    credential=DefaultAzureCredential(),
)

request = KnowledgeBaseRetrievalRequest(
    messages=[
        KnowledgeBaseMessage(
            role="assistant",
            content=[
                KnowledgeBaseMessageTextContent(
                    text="You can answer questions about the Earth at night. "
                    "Sources have a JSON format with a ref_id that must be cited in the answer. "
                    "If you do not have the answer, respond with 'I do not know'."
                )
            ],
        ),
        KnowledgeBaseMessage(
            role="user",
            content=[
                KnowledgeBaseMessageTextContent(
                    text="Why is the Phoenix nighttime street grid so sharply visible from space, "
                    "whereas large stretches of the interstate between midwestern cities remain comparatively dim?"
                )
            ],
        ),
    ],
    knowledge_source_params=[
        SearchIndexKnowledgeSourceParams(
            knowledge_source_name="earth-at-night-blob-ks",
        )
    ],
)

result = kb_client.retrieve(retrieval_request=request)
print(result.response[0].content[0].text)
```

**Reference:** [KnowledgeBaseRetrievalClient](/python/api/azure-search-documents/azure.search.documents.knowledgebases.knowledgebaseretrievalclient), [KnowledgeBaseRetrievalRequest](/python/api/azure-search-documents/azure.search.documents.knowledgebases.models.knowledgebaseretrievalrequest)

# [2026-04-01](#tab/2026-04-01)

```python
from azure.identity import DefaultAzureCredential
from azure.search.documents.knowledgebases import KnowledgeBaseRetrievalClient
from azure.search.documents.knowledgebases.models import (
    KnowledgeRetrievalSemanticIntent,
    KnowledgeBaseRetrievalRequest,
    SearchIndexKnowledgeSourceParams,
)

# Create knowledge base retrieval client
kb_client = KnowledgeBaseRetrievalClient(
    endpoint="<YOUR SEARCH SERVICE URL>",
    knowledge_base_name="<YOUR KNOWLEDGE BASE NAME>",
    credential=DefaultAzureCredential(),
)

request = KnowledgeBaseRetrievalRequest(
    intents=[
        KnowledgeRetrievalSemanticIntent(
            search="Why is the Phoenix nighttime street grid so sharply visible from space, "
            "whereas large stretches of the interstate between midwestern cities remain comparatively dim?"
        )
    ],
    knowledge_source_params=[
        SearchIndexKnowledgeSourceParams(
            knowledge_source_name="earth-at-night-blob-ks",
        )
    ],
)

result = kb_client.retrieve(retrieval_request=request)
print(result.response[0].content[0].text)
```

**Reference:** [KnowledgeBaseRetrievalClient](/python/api/azure-search-documents/azure.search.documents.knowledgebases.knowledgebaseretrievalclient), [KnowledgeBaseRetrievalRequest](/python/api/azure-search-documents/azure.search.documents.knowledgebases.models.knowledgebaseretrievalrequest)

---

:::zone-end

:::zone pivot="rest"

# [2025-11-01-preview](#tab/2025-11-01-preview)

```http
@search-url = <YOUR SEARCH SERVICE URL> // Example: https://my-service.search.windows.net
@accessToken = <YOUR ACCESS TOKEN> // Run: az account get-access-token --scope https://search.azure.com/.default --query accessToken -o tsv

POST {{search-url}}/knowledgebases/{{knowledge-base-name}}/retrieve?api-version=2025-11-01-preview
Content-Type: application/json
Authorization: Bearer {{accessToken}}

{
    "messages": [
        {
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": "You can answer questions about the Earth at night. Sources have a JSON format with a ref_id that must be cited in the answer. If you do not have the answer, respond with 'I do not know'."
                }
            ]
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Why is the Phoenix nighttime street grid so sharply visible from space, whereas large stretches of the interstate between midwestern cities remain comparatively dim?"
                }
            ]
        }
    ],
    "knowledgeSourceParams": [
        {
            "knowledgeSourceName": "earth-at-night-blob-ks",
            "kind": "searchIndex"
        }
    ]
}
```

**Reference:** [Knowledge Retrieval - Retrieve](/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2025-11-01-preview&preserve-view=true)

# [2026-04-01](#tab/2026-04-01)

```http
@search-url = <YOUR SEARCH SERVICE URL> // Example: https://my-service.search.windows.net
@accessToken = <YOUR ACCESS TOKEN> // Run: az account get-access-token --scope https://search.azure.com/.default --query accessToken -o tsv

POST {{search-url}}/knowledgebases/{{knowledge-base-name}}/retrieve?api-version=2026-04-01
Content-Type: application/json
Authorization: Bearer {{accessToken}}

{
    "intents": [
        {
            "type": "semantic",
            "search": "Why is the Phoenix nighttime street grid so sharply visible from space, whereas large stretches of the interstate between midwestern cities remain comparatively dim?"
        }
    ],
    "knowledgeSourceParams": [
        {
            "knowledgeSourceName": "earth-at-night-blob-ks",
            "kind": "searchIndex"
        }
    ]
}
```

**Reference:** [Knowledge Retrieval - Retrieve](/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2026-04-01&preserve-view=true)

---

:::zone-end

> [!IMPORTANT]
> The 2026-04-01 API version only supports the `intents` input and minimal, extractive retrieval. Preview-only capabilities, including the `messages` input, query planning, answer synthesis, and configurable reasoning effort, aren't supported. For full functionality, use the 2025-11-01-preview.

## Filter at query time (Search index)

When retrieving from a search index knowledge source, you can apply an [OData filter](search-query-odata-filter.md) at query time to narrow the results to specific documents or fields. The filter expression uses OData syntax and is passed via the `filterAddOn` parameter.

### Filter syntax and examples

The `filterAddOn` parameter accepts OData filter expressions. Example patterns include:

- **Metadata fields**: `city eq 'Phoenix'`, `status eq 'active'`
- **Date ranges**: `publishDate ge 2024-01-01 and publishDate le 2024-12-31`
- **Numeric ranges**: `price ge 100 and price le 5000`
- **Text matching**: `substringof('climate', description)`, `indexof(title, 'urgent') ge 0`
- **Logical operators**: `(category eq 'News' or category eq 'Analysis') and status eq 'published'`

**Example filter expressions:**

- `status eq 'published'`
- `created ge 2025-01-01`
- `city eq 'Redmond' and department eq 'Engineering'`
- `(priority eq 'High' or priority eq 'Critical') and resolved eq false`

### Examples by language

:::zone pivot="csharp"

```csharp
using Azure.Identity;
using Azure.Search.Documents.KnowledgeBases;
using Azure.Search.Documents.KnowledgeBases.Models;

var kbClient = new KnowledgeBaseRetrievalClient(
    endpoint: new Uri("<YOUR SEARCH SERVICE URL>"),
    knowledgeBaseName: "<YOUR KNOWLEDGE BASE NAME>",
    tokenCredential: new DefaultAzureCredential()
);

var retrievalRequest = new KnowledgeBaseRetrievalRequest();

retrievalRequest.Messages.Add(
    new KnowledgeBaseMessage(
        content: new[] {
            new KnowledgeBaseMessageTextContent(
                "You are a support agent. Answer questions based on published documentation. "
                + "If you don't know the answer, say so."
            )
        }
    ) { Role = "assistant" }
);

retrievalRequest.Messages.Add(
    new KnowledgeBaseMessage(
        content: new[] {
            new KnowledgeBaseMessageTextContent(
                "What is the process for submitting an expense report?"
            )
        }
    ) { Role = "user" }
);

// Apply a filter to search only published documents
var searchIndexParams = new SearchIndexKnowledgeSourceParams(
    knowledgeSourceName: "internal-documentation-ks"
);
searchIndexParams.FilterAddOn = "status eq 'published'";

retrievalRequest.KnowledgeSourceParams.Add(searchIndexParams);

var result = await kbClient.RetrieveAsync(retrievalRequest);
Console.WriteLine(
    (result.Value.Response[0].Content[0] as KnowledgeBaseMessageTextContent)!.Text
);
```

:::zone-end

:::zone pivot="python"

```python
from azure.identity import DefaultAzureCredential
from azure.search.documents.knowledgebases import KnowledgeBaseRetrievalClient
from azure.search.documents.knowledgebases.models import (
    KnowledgeBaseMessage,
    KnowledgeBaseMessageTextContent,
    KnowledgeBaseRetrievalRequest,
    SearchIndexKnowledgeSourceParams,
)

kb_client = KnowledgeBaseRetrievalClient(
    endpoint="<YOUR SEARCH SERVICE URL>",
    knowledge_base_name="<YOUR KNOWLEDGE BASE NAME>",
    credential=DefaultAzureCredential(),
)

request = KnowledgeBaseRetrievalRequest(
    messages=[
        KnowledgeBaseMessage(
            role="assistant",
            content=[
                KnowledgeBaseMessageTextContent(
                    text="You are a support agent. Answer questions based on published documentation. "
                    "If you don't know the answer, say so."
                )
            ],
        ),
        KnowledgeBaseMessage(
            role="user",
            content=[
                KnowledgeBaseMessageTextContent(
                    text="What is the process for submitting an expense report?"
                )
            ],
        ),
    ],
    knowledge_source_params=[
        SearchIndexKnowledgeSourceParams(
            knowledge_source_name="internal-documentation-ks",
            # Apply a filter to search only published documents
            filter_add_on="status eq 'published'",
        )
    ],
)

result = kb_client.retrieve(retrieval_request=request)
print(result.response[0].content[0].text)
```

:::zone-end

:::zone pivot="rest"

```http
POST https://<YOUR SEARCH SERVICE>.search.windows.net/knowledgebases/<YOUR KNOWLEDGE BASE NAME>/retrieve?api-version=2025-11-01-preview
Content-Type: application/json
Authorization: Bearer <YOUR ACCESS TOKEN>

{
    "messages": [
        {
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": "You are a support agent. Answer questions based on published documentation. If you don't know the answer, say so."
                }
            ]
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "What is the process for submitting an expense report?"
                }
            ]
        }
    ],
    "knowledgeSourceParams": [
        {
            "knowledgeSourceName": "internal-documentation-ks",
            "kind": "searchIndex",
            "filterAddOn": "status eq 'published'"
        }
    ]
}
```

:::zone-end

### Multi-filter example

You can combine multiple filters to refine results further:

:::zone pivot="csharp"

```csharp
searchIndexParams.FilterAddOn = "(status eq 'published' or status eq 'internal') and created ge 2025-01-01";
```

:::zone-end

:::zone pivot="python"

```python
filter_add_on="(status eq 'published' or status eq 'internal') and created ge 2025-01-01"
```

:::zone-end

:::zone pivot="rest"

```json
{
    "knowledgeSourceName": "internal-documentation-ks",
    "kind": "searchIndex",
    "filterAddOn": "(status eq 'published' or status eq 'internal') and created ge 2025-01-01"
}
```

:::zone-end

### Request parameters

Pass the following parameters to call the retrieve action.

# [2025-11-01-preview](#tab/2025-11-01-preview)

| Name | Description | Type | Editable | Required |
|--|--|--|--|--|
| `messages` | Contains the chat conversation history sent to the agentic retrieval pipeline. The LLM determines the query from the conversation history. The message format is similar to Azure OpenAI APIs. Supported only if the [retrieval reasoning effort](agentic-retrieval-how-to-set-retrieval-reasoning-effort.md) is low or medium. | Object | Yes | No |
| `messages.role` | Defines where the message came from, such as `assistant` or `user`. The model you use determines which roles are valid. | String | Yes | No |
| `messages.content` | The message or prompt sent to the LLM. Must be text. | String | Yes | No |
| `knowledgeSourceParams` | Overrides default retrieval settings per knowledge source. Useful for customizing the query or response at query time. | Object | Yes | No |

# [2026-04-01](#tab/2026-04-01)

| Name | Description | Type | Editable | Required |
|--|--|--|--|--|
| `intents` | A list of search intents sent to the agentic retrieval pipeline. Each intent specifies a query type and a search string. | Array | Yes | Yes |
| `intents.type` | The query type. The only valid value is `semantic`. | String | Yes | Yes |
| `intents.search` | The search string for the query. | String | Yes | Yes |
| `knowledgeSourceParams` | Overrides default retrieval settings per knowledge source. Useful for customizing the query or response at query time. | Object | Yes | No |

---

### Retrieval from a search index

For knowledge sources that target a search index, all `searchable` fields are in scope for query execution. The implied query type is `semantic`, and there's no search mode.

If the index includes vector fields, you need a valid vectorizer definition so the agentic retrieval engine can vectorize query inputs. Otherwise, vector fields are ignored.

For more information, see [Create an index for agentic retrieval](agentic-retrieval-how-to-create-index.md).

## Call the MCP endpoint

[MCP](https://modelcontextprotocol.io/) is an open protocol that standardizes how AI applications connect to external data sources and tools.

In Azure AI Search, each knowledge base is a standalone MCP server that exposes the `knowledge_base_retrieve` tool. Any MCP-compatible client, including [Foundry Agent Service](/azure/ai-foundry/agents/overview), [GitHub Copilot](https://github.com/features/copilot), [Claude](https://claude.ai), and [Cursor](https://cursor.com), can invoke this tool to query the knowledge base.

### MCP endpoint format

Each knowledge base has an MCP endpoint at the following URL:
```
https://<your-service-name>.search.windows.net/knowledgebases/<your-knowledge-base-name>/mcp?api-version=<api-version>
```

The API version you specify determines what the connection returns. With `2025-11-01-preview`, the knowledge base can return synthesized answers when the underlying knowledge base is configured with an LLM and a compatible reasoning effort. With `2026-04-01`, retrieval is always minimal and extractive, and the connection returns grounding data only.

### Authenticate to the MCP endpoint

The MCP endpoint requires authentication via custom headers. You have two options:

+ **(Recommended)** Pass a bearer token in the `Authorization` header. The identity behind the token must have the **Search Index Data Reader** role assigned on the search service. This approach avoids storing keys in configuration files. For more information, see [Connect your app to Azure AI Search using identities](search-security-rbac-client-code.md).

+ Pass an admin key in the `api-key` header. An admin key provides full read-write access to the search service, so use it with caution. For more information, see [Connect to Azure AI Search using API keys](search-security-api-keys.md).

> [!TIP]
> Each MCP client configures custom headers differently. For example:
>
> + In [Foundry Agent Service](/azure/ai-foundry/agents/how-to/foundry-iq-connect), you configure authentication via a project connection and add the MCP tool to an agent. The service automatically injects the required headers on MCP requests.
>
> + In [GitHub Copilot](https://docs.github.com/en/copilot/how-tos/provide-context/use-mcp/extend-copilot-chat-with-mcp), [Claude Desktop](https://support.claude.com/en/articles/10949351-getting-started-with-local-mcp-servers-on-claude-desktop), and similar clients, you configure headers in the MCP server JSON, such as `mcp.json`.

## Enforce permissions at query time

> [!NOTE]
> Although knowledge retrieval is generally available, permissions enforcement remains in preview. You must use the 2025-11-01-preview API version for both ingestion-time and query-time configuration. Preview features are provided without a service-level agreement and aren't recommended for production workloads. For more information, see [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).

If your knowledge sources contain permission-protected content, the retrieval engine can filter results so that each user only sees the documents they're authorized to access. You enable this filtering by passing the end user's identity on the retrieve request. Without the identity token, results from permission-enabled knowledge sources are returned unfiltered.

Permissions enforcement has two parts:

- [**Ingestion time**](#ingestion-time-configuration): For indexed knowledge sources only, set `ingestionPermissionOptions` to ingest permission metadata alongside content.

- [**Query time**](#query-time-authorization): Pass the user's access token in the `x-ms-query-source-authorization` header.

### Ingestion-time configuration

The following table shows which knowledge sources require ingestion-time configuration and how each source enforces permissions.

| Knowledge source | Requires `ingestionPermissionOptions` | How permissions are enforced |
|---|---|---|
| [Blob or ADLS Gen2](agentic-knowledge-source-how-to-blob.md#ingestion-parameters-properties) | ✅ | Ingested RBAC scopes or ACLs matched against user identity. |
| [OneLake](agentic-knowledge-source-how-to-onelake.md#ingestion-parameters-properties) | ✅ | Ingested RBAC scopes or ACLs matched against user identity. |
| [Indexed SharePoint](agentic-knowledge-source-how-to-sharepoint-indexed.md#ingestion-parameters-properties) | ✅ | Ingested SharePoint ACLs matched against user identity. |
| [Remote SharePoint](agentic-knowledge-source-how-to-sharepoint-remote.md#assign-to-a-knowledge-base) | ❌ | Copilot Retrieval API queries SharePoint directly using the user's token. |
| [Fabric Data Agent](agentic-knowledge-source-how-to-fabric-data-agent.md#enforce-permissions-at-query-time) | ❌ | The retrieval engine exchanges the user's token for a Microsoft Fabric–scoped token and queries the data agent on their behalf. |
| [Work IQ](agentic-knowledge-source-how-to-work-iq.md#enforce-permissions-at-query-time) | ❌ | The retrieval engine exchanges the user's token for a Work IQ–scoped token and queries Work IQ on their behalf. |

> [!IMPORTANT]
> If `ingestionPermissionOptions` wasn't configured when the indexed knowledge source was created, no permission metadata exists in the index. Results are returned unfiltered, regardless of the header. To fix this, update or recreate the knowledge source with the appropriate `ingestionPermissionOptions` values and [reindex](search-howto-run-reset-indexers.md).

### Query-time authorization

To pass the end user's identity, include an access token scoped to `https://search.azure.com/.default` on the retrieve request. This token is separate from the service credential used to access the search service. It doesn't need search service permissions and only represents the user whose content access is evaluated. For more information, see [Query-time ACL and RBAC enforcement](search-query-access-control-rbac-enforcement.md).

:::zone pivot="csharp"

In the .NET SDK, pass the token as the `xMsQuerySourceAuthorization` parameter on `RetrieveAsync`:

```csharp
using Azure;
using Azure.Identity;
using Azure.Search.Documents.KnowledgeBases;
using Azure.Search.Documents.KnowledgeBases.Models;

// Service credential: Authenticates to the search service
var serviceCredential = new DefaultAzureCredential();

// User identity token: Represents the end user for document-level permissions filtering
var userTokenContext = new Azure.Core.TokenRequestContext(
    new[] { "https://search.azure.com/.default" }
);
string userToken = (await serviceCredential.GetTokenAsync(userTokenContext)).Token;

// Create the retrieval client with the service credential
var kbClient = new KnowledgeBaseRetrievalClient(
    endpoint: new Uri("<YOUR SEARCH SERVICE URL>"),
    knowledgeBaseName: "<YOUR KNOWLEDGE BASE NAME>",
    tokenCredential: serviceCredential
);

var request = new KnowledgeBaseRetrievalRequest();
request.Messages.Add(
    new KnowledgeBaseMessage(
        content: new[] {
            new KnowledgeBaseMessageTextContent(
                "What companies are in the financial sector?")
        }
    ) { Role = "user" }
);

// Pass the user identity token for permissions filtering
var result = await kbClient.RetrieveAsync(
    request, xMsQuerySourceAuthorization: userToken);

var text = (result.Value.Response[0].Content[0] as KnowledgeBaseMessageTextContent)!.Text;
Console.WriteLine(text);
```

**Reference:** [KnowledgeBaseRetrievalClient](/dotnet/api/azure.search.documents.knowledgebases.knowledgebaseretrievalclient?view=azure-dotnet-preview&preserve-view=true), [KnowledgeBaseRetrievalRequest](/dotnet/api/azure.search.documents.knowledgebases.models.knowledgebaseretrievalrequest?view=azure-dotnet-preview&preserve-view=true)

:::zone-end

:::zone pivot="python"

In the Python SDK, pass the token as the `x_ms_query_source_authorization` parameter on `retrieve`:

```python
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from azure.search.documents.knowledgebases import KnowledgeBaseRetrievalClient
from azure.search.documents.knowledgebases.models import (
    KnowledgeBaseMessage, KnowledgeBaseMessageTextContent,
    KnowledgeBaseRetrievalRequest,
)

# Service credential: Authenticates to the search service
service_credential = DefaultAzureCredential()

# User identity token: Represents the end user for document-level permissions filtering
user_token_provider = get_bearer_token_provider(
    service_credential, "https://search.azure.com/.default")
user_token = user_token_provider()

# Create the retrieval client with the service credential
kb_client = KnowledgeBaseRetrievalClient(
    endpoint="<YOUR SEARCH SERVICE URL>",
    knowledge_base_name="<YOUR KNOWLEDGE BASE NAME>",
    credential=service_credential,
)

request = KnowledgeBaseRetrievalRequest(
    messages=[
        KnowledgeBaseMessage(
            role="user",
            content=[KnowledgeBaseMessageTextContent(
                text="What companies are in the financial sector?")],
        )
    ]
)

# Pass the user identity token for permissions filtering
result = kb_client.retrieve(
    retrieval_request=request, x_ms_query_source_authorization=user_token)
print(result.response[0].content[0].text)
```

**Reference:** [KnowledgeBaseRetrievalClient](/python/api/azure-search-documents/azure.search.documents.knowledgebases.knowledgebaseretrievalclient), [KnowledgeBaseRetrievalRequest](/python/api/azure-search-documents/azure.search.documents.knowledgebases.models.knowledgebaseretrievalrequest)

:::zone-end

:::zone pivot="rest"

In the REST API, include the `x-ms-query-source-authorization` header with the user's access token:

```http
@search-url = <YOUR SEARCH SERVICE URL>
@accessToken = <YOUR ACCESS TOKEN> // Service credential
@userAccessToken = <USER ACCESS TOKEN> // User identity token

POST {{search-url}}/knowledgebases/{{knowledge-base-name}}/retrieve?api-version=2025-11-01-preview
Authorization: Bearer {{accessToken}}
Content-Type: application/json
x-ms-query-source-authorization: {{userAccessToken}}

{
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "What companies are in the financial sector?"
                }
            ]
        }
    ]
}
```

**Reference:** [Knowledge Retrieval - Retrieve](/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2025-11-01-preview&preserve-view=true)

:::zone-end

## Review the response

Successful retrieval returns a `200 OK` status code. If the knowledge base fails to retrieve from one or more knowledge sources, the service returns a `206 Partial Content` status code. The response only includes results from sources that succeeded. Details about the partial response appear as errors in the activity array.

The retrieve action returns three main components:

# [2025-11-01-preview](#tab/2025-11-01-preview)

+ [Extracted response](#extracted-response) or [synthesized answer](agentic-retrieval-how-to-answer-synthesis.md) (depending on output mode)
+ [Activity array](#activity-array)
+ [References array](#references-array)

# [2026-04-01](#tab/2026-04-01)

+ [Extracted response](#extracted-response) (2026-04-01 doesn't support answer synthesis)
+ [Activity array](#activity-array)
+ [References array](#references-array)

---

### Extracted response

The extracted response is a single, unified string that you typically pass to an LLM. The LLM consumes the string as grounding data and uses it to formulate a response. Your API call to the LLM includes the unified string and instructions for the model, such as whether to use the grounding exclusively or as a supplement.

The body of the response is structured in the chat message style format, and the content is serialized JSON.

```json
"response": [
    {
        "role": "assistant",
        "content": [
            {
                "type": "text",
                "text": "[{\"ref_id\":\"0\",\"title\":\"Urban Structure\",\"terms\":\"Location of Phoenix, Grid of City Blocks, Phoenix Metropolitan Area at Night\",\"content\":\"<content chunk redacted>\"}]"
            }
        ]
    }
]
```

Key points:

+ `content.type` has one valid value: `text`.

+ `content.text` is a JSON-encoded string containing the most relevant documents (or chunks) found in the search index, given the query and chat history inputs. This string is your grounding data that an LLM uses to formulate a response to the user's question.

  + This portion of the response consists of 200 chunks or fewer, excluding any results that fail to meet the minimum threshold of a 2.5 reranker score.

  + The string starts with the reference ID of the chunk (used for citation purposes), and any fields specified in the semantic configuration of the target index. In this example, assume the semantic configuration in the target index has a "title" field, a "terms" field, and a "content" field.

+ The `maxOutputSizeInTokens` property (`maxOutputSize` in 2025-11-01-preview) on the retrieve request determines the length of the string.

    > [!IMPORTANT]
    > A document that exceeds the `maxOutputSizeInTokens` output budget can be silently omitted from the response without a warning. For more information, see [Troubleshoot empty responses](#troubleshoot-empty-responses).

### Activity array

The activity array outputs the query plan, which provides operational transparency for tracking operations, billing implications, and resource invocations. It also includes subqueries sent to the retrieval pipeline and errors for any retrieval failures, such as inaccessible knowledge sources.

The output includes the following components:

# [2025-11-01-preview](#tab/2025-11-01-preview)

| Section | Description |
|---------|-------------|
| modelQueryPlanning | For knowledge bases that use an LLM for query planning, this section reports on the token counts used for input, and the token count for the subqueries. |
| source-specific activity | For each knowledge source included in the query, this section reports on elapsed time and which arguments were used in the query, including semantic ranker. Knowledge source types include `searchIndex`, `azureBlob`, and other [supported knowledge sources](agentic-knowledge-source-overview.md#supported-knowledge-sources). |
| agenticReasoning | This section reports on token consumption for agentic reasoning during retrieval, which depends on the specified [retrieval reasoning effort](agentic-retrieval-how-to-set-retrieval-reasoning-effort.md). |
| modelAnswerSynthesis | For knowledge bases that use [answer synthesis](agentic-retrieval-how-to-answer-synthesis.md), this section reports on the token count for formulating the answer, and the token count of the answer output. |

# [2026-04-01](#tab/2026-04-01)

| Section | Description |
|---------|-------------|
| source-specific activity | For each knowledge source included in the query, this section reports on elapsed time and which arguments were used in the query, including semantic ranker. Knowledge source types include `searchIndex`, `azureBlob`, and other [supported knowledge sources](agentic-knowledge-source-overview.md#supported-knowledge-sources). |
| agenticReasoning | This section reports on token consumption for agentic reasoning during retrieval. |

---

> [!NOTE]
> The `modelQueryPlanning` and `modelAnswerSynthesis` sections don't appear in the 2026-04-01 activity array because query planning and answer synthesis are preview-only features. For full activity output, use the 2025-11-01-preview.

Here's an example of the activity array:

# [2025-11-01-preview](#tab/2025-11-01-preview)

```json
  "activity": [
    {
      "type": "modelQueryPlanning",
      "id": 0,
      "inputTokens": 2302,
      "outputTokens": 109,
      "elapsedMs": 2396
    },
    {
      "type": "searchIndex",
      "id": 1,
      "knowledgeSourceName": "demo-financials-ks",
      "queryTime": "2025-11-04T19:25:23.683Z",
      "count": 26,
      "elapsedMs": 1137,
      "searchIndexArguments": {
        "search": "List of companies in the financial sector according to SEC GICS classification",
        "filter": null,
        "sourceDataFields": [ ],
        "searchFields": [ ],
        "semanticConfigurationName": "en-semantic-config"
      }
    },
    {
      "type": "searchIndex",
      "id": 2,
      "knowledgeSourceName": "demo-healthcare-ks",
      "queryTime": "2025-11-04T19:25:24.186Z",
      "count": 17,
      "elapsedMs": 494,
      "searchIndexArguments": {
        "search": "List of companies in the financial sector according to SEC GICS classification",
        "filter": null,
        "sourceDataFields": [ ],
        "searchFields": [ ],
        "semanticConfigurationName": "en-semantic-config"
      }
    },
    {
      "type": "agenticReasoning",
      "id": 3,
      "retrievalReasoningEffort": {
        "kind": "low"
      },
      "reasoningTokens": 103368
    },
    {
      "type": "modelAnswerSynthesis",
      "id": 4,
      "inputTokens": 5821,
      "outputTokens": 344,
      "elapsedMs": 3837
    }
  ]
```

# [2026-04-01](#tab/2026-04-01)

```json
  "activity": [
    {
      "type": "searchIndex",
      "id": 0,
      "knowledgeSourceName": "demo-financials-ks",
      "queryTime": "2025-11-04T19:25:23.683Z",
      "count": 26,
      "elapsedMs": 1137,
      "searchIndexArguments": {
        "search": "List of companies in the financial sector according to SEC GICS classification",
        "filter": null,
        "sourceDataFields": [ ],
        "searchFields": [ ],
        "semanticConfigurationName": "en-semantic-config"
      }
    },
    {
      "type": "searchIndex",
      "id": 1,
      "knowledgeSourceName": "demo-healthcare-ks",
      "queryTime": "2025-11-04T19:25:24.186Z",
      "count": 17,
      "elapsedMs": 494,
      "searchIndexArguments": {
        "search": "List of companies in the financial sector according to SEC GICS classification",
        "filter": null,
        "sourceDataFields": [ ],
        "searchFields": [ ],
        "semanticConfigurationName": "en-semantic-config"
      }
    },
    {
      "type": "agenticReasoning",
      "id": 2,
      "reasoningTokens": 103368
    }
  ]
```

---

### References array

The references array comes directly from the underlying grounding data. It includes the `sourceData` used to generate the response and consists of every document the agentic retrieval engine finds and semantically ranks. Fields in the `sourceData` include an `id` and semantic fields: `title`, `terms`, and `content`.

The `id` acts as a reference ID for an item within a specific response. It's not the document key in the search index. You use it for providing citations. The `activitySource` field cross-references the `id` of the activity entry that produced the reference, which is useful for citation linking.

Here's an example of the references array:

```json
  "references": [
    {
      "type": "searchIndex",
      "id": "0",
      "activitySource": 2,
      "docKey": "earth_at_night_508_page_104_verbalized",
      "sourceData": null
    },
    {
      "type": "searchIndex",
      "id": "1",
      "activitySource": 2,
      "docKey": "earth_at_night_508_page_105_verbalized",
      "sourceData": null
    }
  ]
```

## Examples

The following examples illustrate different ways to call the retrieve action using the 2025-11-01-preview API version, which supports the full feature set, including answer synthesis and a configurable reasoning effort. For 2026-04-01 usage, see the previous sections.

+ [Override default reasoning effort and set request limits](#override-default-reasoning-effort-and-set-request-limits)
+ [Set references for each knowledge source](#set-references-for-each-knowledge-source)
+ [Use minimal reasoning effort](#use-minimal-reasoning-effort)

### Override default reasoning effort and set request limits

This example specifies [answer synthesis](agentic-retrieval-how-to-answer-synthesis.md), so the retrieval reasoning effort must be low or medium.

:::zone pivot="csharp"

```csharp
var retrievalRequest = new KnowledgeBaseRetrievalRequest();
retrievalRequest.Messages.Add(
    new KnowledgeBaseMessage(
        content: new[] {
            new KnowledgeBaseMessageTextContent("What companies are in the financial sector?")
        }
    ) { Role = "user" }
);
retrievalRequest.RetrievalReasoningEffort = new KnowledgeRetrievalLowReasoningEffort();
retrievalRequest.OutputMode = "answerSynthesis";
retrievalRequest.MaxRuntimeInSeconds = 30;
retrievalRequest.MaxOutputSize = 6000;

var result = await kbClient.RetrieveAsync(retrievalRequest);
Console.WriteLine(
    (result.Value.Response[0].Content[0] as KnowledgeBaseMessageTextContent)!.Text
);
```

**Reference:** [KnowledgeBaseRetrievalClient](/dotnet/api/azure.search.documents.knowledgebases.knowledgebaseretrievalclient?view=azure-dotnet-preview&preserve-view=true), [KnowledgeBaseRetrievalRequest](/dotnet/api/azure.search.documents.knowledgebases.models.knowledgebaseretrievalrequest?view=azure-dotnet-preview&preserve-view=true)

:::zone-end

:::zone pivot="python"

```python
from azure.search.documents.knowledgebases.models import KnowledgeRetrievalLowReasoningEffort

request = KnowledgeBaseRetrievalRequest(
    messages=[
        KnowledgeBaseMessage(
            role="user",
            content=[KnowledgeBaseMessageTextContent(text="What companies are in the financial sector?")],
        )
    ],
    retrieval_reasoning_effort=KnowledgeRetrievalLowReasoningEffort(),
    output_mode="answerSynthesis",
    max_runtime_in_seconds=30,
    max_output_size=6000,
)

result = kb_client.retrieve(retrieval_request=request)
print(result.response[0].content[0].text)
```

**Reference:** [KnowledgeBaseRetrievalClient](/python/api/azure-search-documents/azure.search.documents.knowledgebases.knowledgebaseretrievalclient), [KnowledgeBaseRetrievalRequest](/python/api/azure-search-documents/azure.search.documents.knowledgebases.models.knowledgebaseretrievalrequest)

:::zone-end

:::zone pivot="rest"

```http
POST {{search-url}}/knowledgebases/kb-override/retrieve?api-version=2025-11-01-preview
Authorization: Bearer {{accessToken}}
Content-Type: application/json

{
    "messages": [
        {
            "role": "user",
            "content": [
                { "type": "text", "text": "What companies are in the financial sector?" }
            ]
        }
    ],
    "retrievalReasoningEffort": { "kind": "low" },
    "outputMode": "answerSynthesis",
    "maxRuntimeInSeconds": 30,
    "maxOutputSize": 6000
}
```

**Reference:** [Knowledge Retrieval - Retrieve](/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2025-11-01-preview&preserve-view=true)

:::zone-end

### Set references for each knowledge source

This example uses the default reasoning effort specified in the knowledge base. The focus of this example is specification of how much information to include in the response.

:::zone pivot="csharp"

```csharp
var retrievalRequest = new KnowledgeBaseRetrievalRequest();
retrievalRequest.Messages.Add(
    new KnowledgeBaseMessage(
        content: new[] {
            new KnowledgeBaseMessageTextContent("What companies are in the financial sector?")
        }
    ) { Role = "user" }
);
retrievalRequest.IncludeActivity = true;
retrievalRequest.KnowledgeSourceParams.Add(
    new SearchIndexKnowledgeSourceParams("demo-financials-ks")
    {
        IncludeReferences = true,
        IncludeReferenceSourceData = true
    }
);

retrievalRequest.KnowledgeSourceParams.Add(
    new SearchIndexKnowledgeSourceParams("demo-communicationservices-ks")
    {
        IncludeReferences = false,
        IncludeReferenceSourceData = false
    }
);

retrievalRequest.KnowledgeSourceParams.Add(
    new SearchIndexKnowledgeSourceParams("demo-healthcare-ks")
    {
        IncludeReferences = true,
        IncludeReferenceSourceData = false,
        AlwaysQuerySource = true
    }
);

var result = await kbClient.RetrieveAsync(retrievalRequest);
Console.WriteLine(
    (result.Value.Response[0].Content[0] as KnowledgeBaseMessageTextContent)!.Text
);
```

**Reference:** [KnowledgeBaseRetrievalClient](/dotnet/api/azure.search.documents.knowledgebases.knowledgebaseretrievalclient?view=azure-dotnet-preview&preserve-view=true), [KnowledgeBaseRetrievalRequest](/dotnet/api/azure.search.documents.knowledgebases.models.knowledgebaseretrievalrequest?view=azure-dotnet-preview&preserve-view=true)

:::zone-end

:::zone pivot="python"

```python
from azure.search.documents.knowledgebases.models import SearchIndexKnowledgeSourceParams

request = KnowledgeBaseRetrievalRequest(
    messages=[
        KnowledgeBaseMessage(
            role="user",
            content=[KnowledgeBaseMessageTextContent(text="What companies are in the financial sector?")],
        )
    ],
    include_activity=True,
    knowledge_source_params=[
        SearchIndexKnowledgeSourceParams(
            knowledge_source_name="demo-financials-ks",
            include_references=True,
            include_reference_source_data=True,
        ),
        SearchIndexKnowledgeSourceParams(
            knowledge_source_name="demo-communicationservices-ks",
            include_references=False,
            include_reference_source_data=False,
        ),
        SearchIndexKnowledgeSourceParams(
            knowledge_source_name="demo-healthcare-ks",
            include_references=True,
            include_reference_source_data=False,
            always_query_source=True,
        ),
    ],
)

result = kb_client.retrieve(retrieval_request=request)
print(result.response[0].content[0].text)
```

**Reference:** [KnowledgeBaseRetrievalClient](/python/api/azure-search-documents/azure.search.documents.knowledgebases.knowledgebaseretrievalclient), [SearchIndexKnowledgeSourceParams](/python/api/azure-search-documents/azure.search.documents.knowledgebases.models.searchindexknowledgesourceparams)

:::zone-end

:::zone pivot="rest"

```http
POST {{search-url}}/knowledgebases/kb-medium-example/retrieve?api-version=2025-11-01-preview
Authorization: Bearer {{accessToken}}
Content-Type: application/json

{
    "messages": [
        {
            "role": "user",
            "content": [
                { "type": "text", "text": "What companies are in the financial sector?" }
            ]
        }
    ],
    "includeActivity": true,
    "knowledgeSourceParams": [
        {
            "knowledgeSourceName": "demo-financials-ks",
            "kind": "searchIndex",
            "includeReferences": true,
            "includeReferenceSourceData": true
        },
        {
            "knowledgeSourceName": "demo-communicationservices-ks",
            "kind": "searchIndex",
            "includeReferences": false,
            "includeReferenceSourceData": false
        },
        {
            "knowledgeSourceName": "demo-healthcare-ks",
            "kind": "searchIndex",
            "includeReferences": true,
            "includeReferenceSourceData": false,
            "alwaysQuerySource": true
        }
    ]
}
```

**Reference:** [Knowledge Retrieval - Retrieve](/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2025-11-01-preview&preserve-view=true)

:::zone-end

> [!NOTE]
> For indexed OneLake or indexed SharePoint knowledge sources, set `includeReferenceSourceData` to `true` to include source document URLs in citations.

### Use minimal reasoning effort

In this example, there's no LLM for intelligent query planning or answer synthesis. The query string goes to the agentic retrieval engine for keyword search or hybrid search.

:::zone pivot="csharp"

```csharp
var retrievalRequest = new KnowledgeBaseRetrievalRequest();
retrievalRequest.Intents.Add(
    new KnowledgeRetrievalSemanticIntent("what is a brokerage")
);

var result = await kbClient.RetrieveAsync(retrievalRequest);
Console.WriteLine(
    (result.Value.Response[0].Content[0] as KnowledgeBaseMessageTextContent)!.Text
);
```

**Reference:** [KnowledgeBaseRetrievalClient](/dotnet/api/azure.search.documents.knowledgebases.knowledgebaseretrievalclient?view=azure-dotnet&preserve-view=true), [KnowledgeBaseRetrievalRequest](/dotnet/api/azure.search.documents.knowledgebases.models.knowledgebaseretrievalrequest?view=azure-dotnet&preserve-view=true)

:::zone-end

:::zone pivot="python"

```python
from azure.search.documents.knowledgebases.models import (
    KnowledgeBaseRetrievalRequest,
    KnowledgeRetrievalSemanticIntent,
)

request = KnowledgeBaseRetrievalRequest(
    intents=[
        KnowledgeRetrievalSemanticIntent(
            search="what is a brokerage",
        )
    ]
)

result = kb_client.retrieve(retrieval_request=request)
print(result.response[0].content[0].text)
```

**Reference:** [KnowledgeBaseRetrievalClient](/python/api/azure-search-documents/azure.search.documents.knowledgebases.knowledgebaseretrievalclient), [KnowledgeBaseRetrievalRequest](/python/api/azure-search-documents/azure.search.documents.knowledgebases.models.knowledgebaseretrievalrequest)

:::zone-end

:::zone pivot="rest"

```http
POST {{search-url}}/knowledgebases/kb-minimal/retrieve?api-version=2025-11-01-preview
Authorization: Bearer {{accessToken}}
Content-Type: application/json

{
    "intents": [
        {
            "type": "semantic",
            "search": "what is a brokerage"
        }
    ]
}
```

**Reference:** [Knowledge Retrieval - Retrieve](/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2025-11-01-preview&preserve-view=true)

:::zone-end

## Troubleshoot empty responses

A document can be found during the search step but still be omitted from the final response if its grounded content exceeds the `maxOutputSizeInTokens` (`maxOutputSize` in 2025-11-01-preview) output budget. When this happens, the activity array shows that matches were found, but the references array and grounded response content are empty for that document. No truncation warning or explicit error is returned.

To avoid this behavior, index large source documents as smaller chunks with stable identifiers and source metadata. This applies especially to long manuals, policies, or knowledge base articles.

## Related content

+ [Agentic retrieval in Azure AI Search](agentic-retrieval-overview.md)
+ [Query-time ACL and RBAC enforcement](search-query-access-control-rbac-enforcement.md)
+ [Use a blob indexer or knowledge source to ingest RBAC scopes metadata](search-blob-indexer-role-based-access.md)
+ [Agentic RAG: Build a reasoning retrieval engine with Azure AI Search (YouTube video)](https://www.youtube.com/watch?v=PeTmOidqHM8)
+ [Azure OpenAI demo featuring agentic retrieval](https://github.com/Azure-Samples/azure-search-openai-demo)
