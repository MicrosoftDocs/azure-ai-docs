---
title: Query Knowledge Base via API or MCP
description: Learn how to query a knowledge base using the retrieve action or MCP endpoint in Azure AI Search using REST APIs, Azure SDKs, or any MCP-compatible client.
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 06/02/2026
ai-usage: ai-assisted
zone_pivot_groups: search-csharp-python-rest
---

# Query a knowledge base using the retrieve action or MCP endpoint

[!INCLUDE [GA feature](./includes/previews/agentic-retrieval-ga-feature.md)]

> [!IMPORTANT]
> These features and functionality are part of the 2026-05-01-preview REST API. The 2026-05-01-preview is licensed to you as part of your Azure subscription and is subject to the terms applicable to "Previews" in the [Microsoft Product Terms](https://www.microsoft.com/licensing/terms/welcome/welcomepage), the [Microsoft Products and Services Data Protection Addendum](https://www.microsoft.com/licensing/docs/view/Microsoft-Products-and-Services-Data-Protection-Addendum-DPA) ("DPA"), and the [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).
>
> The 2026-05-01-preview supports connections to other Microsoft services and third-party services. Use of these services is subject to their respective terms and might result in data processing or storage outside of the Azure compliance boundary, as well as data flowing into the Azure compliance boundary.
>
> It's your responsibility to manage whether your data will flow outside of your organization's compliance and geographic boundaries and any related implications, and that appropriate permissions, boundaries, and approvals are provisioned.
>
> You're responsible for carefully reviewing and testing applications you build in the context of your specific use cases and making all appropriate decisions and customizations. This includes implementing your own responsible AI mitigations, such as metaprompts, content filters, or other safety systems, and ensuring your applications meet appropriate quality, reliability, security, and trustworthiness standards. For more information, see the [Azure AI Search Transparency Note](/azure/foundry/responsible-ai/search/transparency-note).

In an agentic retrieval pipeline, the [retrieve action](/rest/api/searchservice/knowledge-retrieval/retrieve) invokes parallel query processing from a knowledge base. You can call the retrieve action directly using the Search Service REST APIs or an Azure SDK. Each knowledge base also exposes a Model Context Protocol (MCP) endpoint for consumption by MCP-compatible agents.

This article explains how to call both retrieval methods with optional permissions enforcement and interpret the three-pronged response. To set up a pipeline that connects Azure AI Search to Foundry Agent Service via MCP, see [Tutorial: Build an end-to-end agentic retrieval solution](agentic-retrieval-how-to-create-pipeline.md).

## Prerequisites

+ An Azure AI Search service with a [knowledge base](agentic-retrieval-how-to-create-knowledge-base.md).

+ Permissions to query knowledge bases. Configure [keyless authentication](search-get-started-rbac.md) with the **Search Index Data Reader** role assigned to your user account (recommended) or use an [API key](search-security-api-keys.md).

+ If the knowledge base specifies an LLM, the search service must have a [managed identity](search-how-to-managed-identities.md) with **Cognitive Services User** permissions on the Microsoft Foundry resource.

::: zone pivot="csharp"

+ Required [`Azure.Search.Documents`](https://www.nuget.org/packages/Azure.Search.Documents) package:

  + For 2026-05-01-preview features, the latest preview package: `dotnet add package Azure.Search.Documents --prerelease`

  + For 2026-04-01 features, the latest stable package: `dotnet add package Azure.Search.Documents`

::: zone-end

::: zone pivot="python"

+ Required [`azure-search-documents`](https://pypi.org/project/azure-search-documents/#history) package:

  + For 2026-05-01-preview features, the latest preview package: `pip install --pre azure-search-documents`

  + For 2026-04-01 features, the latest stable package: `pip install azure-search-documents`

::: zone-end

::: zone pivot="rest"

+ Required REST API version:

  + For preview features: [Search Service 2026-05-01-preview](/rest/api/searchservice/operation-groups?view=rest-searchservice-2026-05-01-preview&preserve-view=true)

  + For generally available features: [Search Service 2026-04-01](/rest/api/searchservice/operation-groups?view=rest-searchservice-2026-04-01&preserve-view=true)

::: zone-end

## Call the retrieve action

You specify the retrieve action on a knowledge base. The request body includes the query input and an optional list of knowledge sources to target.

> [!IMPORTANT]
> The 2026-04-01 API version only supports the `intents` input and minimal, extractive retrieval. Preview-only capabilities, including the `messages` input, query planning, answer synthesis, and configurable reasoning effort, aren't supported. For full functionality, use the 2026-05-01-preview.

:::zone pivot="csharp"

# [2026-05-01-preview](#tab/2026-05-01-preview)

```csharp
using Azure;
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
using Azure;
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

# [2026-05-01-preview](#tab/2026-05-01-preview)

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

result = kb_client.retrieve(request)
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

result = kb_client.retrieve(request)
print(result.response[0].content[0].text)
```

**Reference:** [KnowledgeBaseRetrievalClient](/python/api/azure-search-documents/azure.search.documents.knowledgebases.knowledgebaseretrievalclient), [KnowledgeBaseRetrievalRequest](/python/api/azure-search-documents/azure.search.documents.knowledgebases.models.knowledgebaseretrievalrequest)

---

:::zone-end

:::zone pivot="rest"

# [2026-05-01-preview](#tab/2026-05-01-preview)

```http
@search-url = <YOUR SEARCH SERVICE URL> // Example: https://my-service.search.windows.net
@accessToken = <YOUR ACCESS TOKEN> // Run: az account get-access-token --scope https://search.azure.com/.default --query accessToken -o tsv

POST {{search-url}}/knowledgebases/{{knowledge-base-name}}/retrieve?api-version=2026-05-01-preview
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

**Reference:** [Knowledge Retrieval - Retrieve](/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2026-05-01-preview&preserve-view=true)

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

### Request parameters

Pass the following parameters to call the retrieve action.

# [2026-05-01-preview](#tab/2026-05-01-preview)

| Name | Description | Type | Editable | Required |
|--|--|--|--|--|
| `messages` | Contains the chat conversation history sent to the agentic retrieval pipeline. The LLM determines the query from the conversation history. The message format is similar to Azure OpenAI APIs. Supported only if the [retrieval reasoning effort](agentic-retrieval-how-to-set-retrieval-reasoning-effort.md) is low or medium. | Object | Yes | No |
| `messages.role` | Defines where the message came from, such as `assistant` or `user`. The model you use determines which roles are valid. | String | Yes | No |
| `messages.content` | The message or prompt sent to the LLM. Must be text. | Array | Yes | No |
| `includeActivity` | When `true`, the response includes an `activity` array that describes the steps the pipeline ran, such as query planning, search index calls, and answer synthesis. Defaults to `false`. For a usage example, see [Inspect model names in activity logs](#inspect-model-names-in-activity-logs). | Boolean | Yes | No |
| `maxOutputDocuments` | Caps the number of grounding documents returned by the retrieve call. Applies after per-source candidate selection. If `maxOutputSize` is also set, both constraints apply, and whichever limit is reached first wins. The service can return fewer documents than this parameter's value if fewer results survive ranking, thresholding, or deduplication. For a usage example and a table of setting combinations, see [Limit final grounding documents](#limit-final-grounding-documents). | Integer | Yes | No |
| `maxOutputSize` | Limits the size, in tokens, of the grounded response payload. Documents that don't fit under the limit are omitted from the response. If `maxOutputDocuments` is also set, both constraints apply, and whichever limit is reached first wins. For a usage example and a table of setting combinations, see [Limit final grounding documents](#limit-final-grounding-documents). | Integer | Yes | No |
| `retrievalReasoningEffort` | Sets the retrieval reasoning effort for the request and overrides the knowledge base default. For valid values and tradeoffs, see [Set the retrieval reasoning effort (preview)](agentic-retrieval-how-to-set-retrieval-reasoning-effort.md). | Object | Yes | No |
| `knowledgeSourceParams` | Overrides default retrieval settings per knowledge source. Useful for customizing the query or response at query time. | Object | Yes | No |
| `knowledgeSourceParams.knowledgeSourceName` | Name of the knowledge source the entry applies to. The knowledge source must already be attached to the knowledge base. | String | Yes | Yes |
| `knowledgeSourceParams.kind` | Discriminator for the knowledge source type, such as `searchIndex`, `web`, `azureBlob`, or `sharepoint`. Must match the underlying knowledge source kind. | String | Yes | Yes |
| `knowledgeSourceParams.alwaysQuerySource` | When `true`, the pipeline always queries this knowledge source instead of relying on the planner to decide. Useful when a source must always participate in the response. This parameter is independent of `failOnError`. To require a source to always run and fail the request if it errors, set both to `true`. | Boolean | Yes | No |
| `knowledgeSourceParams.failOnError` | When `true`, the retrieve request fails with `502 Bad Gateway` and an error message that identifies the knowledge source that couldn't be queried, instead of returning a partial response from the remaining sources. Defaults to `false`, which means the pipeline favors availability and returns results from other sources when one fails. Independent of `alwaysQuerySource`, which controls whether the source is attempted at all; `failOnError` controls what happens when that attempt fails. For a usage example, see [Require a knowledge source to succeed](#require-a-knowledge-source-to-succeed). | Boolean | Yes | No |
| `knowledgeSourceParams.maxOutputDocuments` | Caps the number of candidate documents this knowledge source contributes before the final result selection. Use `50` for cross-region compatibility because some preview regions cap this per-source parameter at 50. Doesn't control the final number of grounding documents returned to the caller. The service can return fewer documents when fewer matches are available or when internal limits apply. For a usage example, see [Tune candidate documents per knowledge source](#tune-candidate-documents-per-knowledge-source). | Integer | Yes | No |
| `knowledgeSourceParams.includeReferences` | When `true`, the response includes a `references` array that identifies the documents that contributed to the answer for this source. For a usage example, see [Set references for each knowledge source](#set-references-for-each-knowledge-source). | Boolean | Yes | No |
| `knowledgeSourceParams.includeReferenceSourceData` | When `true`, references include the source data fields configured on the knowledge source. For a usage example, see [Set references for each knowledge source](#set-references-for-each-knowledge-source). | Boolean | Yes | No |
| `knowledgeSourceParams.rerankerThreshold` | Minimum reranker score that a candidate document must have to be included in the result set for this source. | Number | Yes | No |
| `knowledgeSourceParams.filterAddOn` | OData filter appended to the persisted `baseFilter` (if any) for search index knowledge sources, narrowing the source query at request time. For filter syntax and examples, see [Filter search index knowledge sources at query time](#filter-search-index-knowledge-sources-at-query-time). | String | Yes | No |

# [2026-04-01](#tab/2026-04-01)

| Name | Description | Type | Editable | Required |
|--|--|--|--|--|
| `intents` | A list of search intents sent to the agentic retrieval pipeline. Each intent specifies a query type and a search string. | Array | Yes | Yes |
| `intents.type` | The query type. The only valid value is `semantic`. | String | Yes | Yes |
| `intents.search` | The search string for the query. | String | Yes | Yes |
| `knowledgeSourceParams` | Overrides default retrieval settings per knowledge source. Useful for customizing the query or response at query time. | Object | Yes | No |

---

### Include images in retrieve responses (preview)

For [blob](agentic-knowledge-source-how-to-blob.md), [indexed OneLake](agentic-knowledge-source-how-to-onelake.md), and [indexed SharePoint](agentic-knowledge-source-how-to-sharepoint-indexed.md) knowledge sources configured with an asset store, you can return document-embedded images alongside text and inject them into the answer synthesis prompt. Set `enableImageServing` on the matching entry in `knowledgeSourceParams` to override the default that's set on the knowledge base definition.

Image serving runs only when `outputMode` is `answerSynthesis` and requires the 2026-05-01-preview REST API or an equivalent Azure SDK preview package. For setup steps, the precedence table, and how to inspect image serving statistics, see [Surface document-embedded images in agentic retrieval (preview)](agentic-retrieval-how-to-image-serving.md).

### Search index behavior

For knowledge sources that target a search index, all `searchable` fields are in scope for query execution. The implied query type is `semantic`, and there's no search mode.

If the index includes vector fields, you need a valid vectorizer definition so the agentic retrieval engine can vectorize query inputs. Otherwise, vector fields are ignored.

For more information, see [Create an index for agentic retrieval](agentic-retrieval-how-to-create-index.md).

## Call the MCP endpoint

> [!IMPORTANT]
> MCP implementations are susceptible to risks, such as attacks, cascading failures, and loss of human oversight. You can mitigate these risks by vetting MCP servers for security and reliability, following [Microsoft's recommended practices](/azure/api-management/secure-mcp-servers) and [industry best practices](https://modelcontextprotocol.io/specification/draft/basic/security_best_practices), and implementing approval mechanisms and monitoring cascading behaviors.

[MCP](https://modelcontextprotocol.io/) is an open protocol that standardizes how AI applications connect to external data sources and tools.

In Azure AI Search, each knowledge base is a standalone MCP server that exposes the `knowledge_base_retrieve` tool. Any MCP-compatible client, including [Foundry Agent Service](/azure/ai-foundry/agents/overview), [GitHub Copilot](https://github.com/features/copilot), [Claude](https://claude.ai), and [Cursor](https://cursor.com), can invoke this tool to query the knowledge base.

### Authenticate to the MCP endpoint

Each knowledge base has an MCP endpoint at the following URL:

```
https://<your-search-service>.search.windows.net/knowledgebases/<your-knowledge-base>/mcp?api-version=<api-version>
```

When you invoke the `knowledge_base_retrieve` tool at this endpoint, you authenticate both the Azure OpenAI Responses API call and the MCP request to Azure AI Search. For the MCP request, use one of the following authentication methods:

+ [Pass a bearer token](#use-a-bearer-token-for-mcp-authentication) in the `Authorization` header (recommended)
+ [Pass an admin key](#use-an-admin-key-for-mcp-authentication) in the `api-key` header

> [!TIP]
> Each MCP client configures custom headers differently. For example:
>
> + In [Foundry Agent Service](/azure/ai-foundry/agents/how-to/foundry-iq-connect), you configure authentication via a project connection and add the MCP tool to an agent. The service automatically injects the required headers on MCP requests.
>
> + In [GitHub Copilot](https://docs.github.com/en/copilot/how-tos/provide-context/use-mcp/extend-copilot-chat-with-mcp) and similar clients, you configure headers in the MCP server JSON, such as `mcp.json`.

### Use a bearer token for MCP authentication

The recommended method for MCP authentication is a bearer token, which avoids storing sensitive keys in configuration files. The identity behind the token must have the **Search Index Data Reader** role assigned on the search service. For more information, see [Connect your app to Azure AI Search using identities](search-security-rbac-client-code.md).

:::zone pivot="python"

```python
import os
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import OpenAI

# Set the MCP endpoint for your knowledge base
mcp_server_url = (
    "https://<your-search-service>.search.windows.net/"
    "knowledgebases/<your-knowledge-base>/mcp?api-version=<api-version>"
)

# Create the Azure OpenAI client
client = OpenAI(
    base_url="https://<your-resource-name>.openai.azure.com/openai/v1/",
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
)

# Acquire a bearer token provider for Azure AI Search
search_token_provider = get_bearer_token_provider(
    DefaultAzureCredential(),
    "https://search.azure.com/.default",
)

# Call the Responses API and pass the MCP auth header
response = client.responses.create(
    model="MODEL_NAME",
    input="What causes the strongest nighttime brightness patterns in this dataset?",
    tools=[
        {
            "type": "mcp",
            "server_label": "search_kb",
            "server_url": mcp_server_url,
            "allowed_tools": ["knowledge_base_retrieve"],
            "headers": {
                "Authorization": f"Bearer {search_token_provider()}"
            },
            "require_approval": "never",
        }
    ],
)

# Print the generated answer
print(response.output_text)
```

**Reference:** [DefaultAzureCredential](/python/api/azure-identity/azure.identity.defaultazurecredential), [OpenAI Python API library](https://github.com/openai/openai-python)

:::zone-end

:::zone pivot="csharp"

```csharp
#pragma warning disable OPENAI001

using Azure.Core;
using Azure.Identity;
using OpenAI.Responses;
using System;
using System.Collections.Generic;
using System.ClientModel;
using System.ClientModel.Primitives;

// Define the Azure OpenAI endpoint and MCP server URL
string openAiEndpoint = "https://<your-resource-name>.openai.azure.com/openai/v1";
string mcpServerUrl =
    "https://<your-service-name>.search.windows.net/"
    + "knowledgebases/<your-knowledge-base-name>/mcp?api-version=<api-version>";

// Create the Azure OpenAI Responses client
ResponsesClient openAIClient = new(
    credential: new ApiKeyCredential(Environment.GetEnvironmentVariable("AZURE_OPENAI_API_KEY")!),
    options: new ResponsesClientOptions { Endpoint = new Uri(openAiEndpoint) });

// Acquire a bearer token for Azure AI Search
DefaultAzureCredential credential = new();
string searchToken = credential.GetToken(
    new TokenRequestContext(new[] { "https://search.azure.com/.default" })
).Token;

// Configure the MCP tool and include the auth header
McpTool mcpTool = ResponseTool.CreateMcpTool(
    serverLabel: "search_kb",
    serverUri: new Uri(mcpServerUrl),
    headers: new Dictionary<string, string>
    {
        ["Authorization"] = $"Bearer {searchToken}",
    },
    allowedTools: new[] { "knowledge_base_retrieve" },
    toolCallApprovalPolicy: new McpToolCallApprovalPolicy(
        GlobalMcpToolCallApprovalPolicy.NeverRequireApproval)
);

// Build the request payload
CreateResponseOptions options = new()
{
    Model = "MODEL_NAME",
    InputItems =
    {
        ResponseItem.CreateUserMessageItem(
            "What causes the strongest nighttime brightness patterns in this dataset?")
    },
    Tools = { mcpTool }
};

// Execute the request and print the answer
ResponseResult response = await openAIClient.CreateResponseAsync(options);
Console.WriteLine(response.GetOutputText());
```

**Reference:** [DefaultAzureCredential](/dotnet/api/azure.identity.defaultazurecredential), [OpenAI .NET library](https://github.com/openai/openai-dotnet)

:::zone-end

:::zone pivot="rest"

```http
// This code snippet is currently unavailable.
```

:::zone-end

### Use an admin key for MCP authentication

An admin key grants full read-write access to the search service, so you should only use it in development environments or when a bearer token isn't available. For more information, see [Connect to Azure AI Search using API keys](search-security-api-keys.md).

:::zone pivot="python"

```python
import os
from openai import OpenAI

# Set the MCP endpoint for your knowledge base
mcp_server_url = (
    "https://<your-search-service>.search.windows.net/"
    "knowledgebases/<your-knowledge-base>/mcp?api-version=<api-version>"
)

# Create the Azure OpenAI client
client = OpenAI(
    base_url="https://<your-resource-name>.openai.azure.com/openai/v1/",
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
)

# Set the Azure AI Search admin key
search_admin_key = os.environ["AZURE_SEARCH_ADMIN_KEY"]

# Call the Responses API and pass the MCP auth header
response = client.responses.create(
    model="MODEL_NAME",
    input="What causes the strongest nighttime brightness patterns in this dataset?",
    tools=[
        {
            "type": "mcp",
            "server_label": "search_kb",
            "server_url": mcp_server_url,
            "allowed_tools": ["knowledge_base_retrieve"],
            "headers": {
                "api-key": search_admin_key,
            },
            "require_approval": "never",
        }
    ],
)

# Print the generated answer
print(response.output_text)
```

**Reference:** [OpenAI Python API library](https://github.com/openai/openai-python), [ApiKeyCredential](/python/api/azure-core/azure.core.credentials.azurekeycredential)

:::zone-end

:::zone pivot="csharp"

```csharp
#pragma warning disable OPENAI001

using System;
using System.Collections.Generic;
using System.ClientModel;
using OpenAI.Responses;

// Define the Azure OpenAI endpoint and MCP server URL
string openAiEndpoint = "https://<your-resource-name>.openai.azure.com/openai/v1";
string mcpServerUrl =
    "https://<your-service-name>.search.windows.net/"
    + "knowledgebases/<your-knowledge-base-name>/mcp?api-version=<api-version>";

// Create the Azure OpenAI Responses client
ResponsesClient openAIClient = new(
    credential: new ApiKeyCredential(Environment.GetEnvironmentVariable("AZURE_OPENAI_API_KEY")!),
    options: new ResponsesClientOptions { Endpoint = new Uri(openAiEndpoint) });

// Set the Azure AI Search admin key
var searchAdminKey = Environment.GetEnvironmentVariable("AZURE_SEARCH_ADMIN_KEY")!;

// Configure the MCP tool and include the auth header
McpTool mcpTool = ResponseTool.CreateMcpTool(
    serverLabel: "search_kb",
    serverUri: new Uri(mcpServerUrl),
    headers: new Dictionary<string, string>
    {
        ["api-key"] = searchAdminKey,
    },
    allowedTools: new[] { "knowledge_base_retrieve" },
    toolCallApprovalPolicy: new McpToolCallApprovalPolicy(
        GlobalMcpToolCallApprovalPolicy.NeverRequireApproval)
);

// Build the request payload
CreateResponseOptions options = new()
{
    Model = "MODEL_NAME",
    InputItems =
    {
        ResponseItem.CreateUserMessageItem(
            "What causes the strongest nighttime brightness patterns in this dataset?")
    },
    Tools = { mcpTool }
};

// Execute the request and print the answer
ResponseResult response = await openAIClient.CreateResponseAsync(options);
Console.WriteLine(response.GetOutputText());
```

**Reference:** [OpenAI .NET library](https://github.com/openai/openai-dotnet), [ApiKeyCredential](/dotnet/api/system.clientmodel.apikeycredential)

:::zone-end

:::zone pivot="rest"

```http
// This code snippet is currently unavailable.
```

:::zone-end

## Filter search index knowledge sources at query time

When retrieving from a search index knowledge source, you can apply an [OData filter](search-query-odata-filter.md) at query time to narrow the results to specific documents or fields. The filter expression uses OData syntax and is passed via the `filterAddOn` parameter.

### Filter syntax and examples

The `filterAddOn` parameter accepts OData filter expressions. Example patterns include:

- **Metadata fields**: `city eq 'Phoenix'`, `status eq 'active'`
- **Date ranges**: `publishDate ge 2024-01-01 and publishDate le 2024-12-31`
- **Numeric ranges**: `price ge 100 and price le 5000`
- **Text matching**: `substringof('climate', description)`, `indexof(title, 'urgent') ge 0`
- **Logical operators**: `(category eq 'News' or category eq 'Analysis') and status eq 'published'`

:::zone pivot="csharp"

```csharp
using Azure;
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

result = kb_client.retrieve(request)
print(result.response[0].content[0].text)
```

:::zone-end

:::zone pivot="rest"

```http
POST https://<YOUR SEARCH SERVICE>.search.windows.net/knowledgebases/<YOUR KNOWLEDGE BASE NAME>/retrieve?api-version=2026-05-01-preview
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

You can combine multiple filters to further refine results.

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

## Enforce permissions at query time (preview)

> [!IMPORTANT]
> The 2026-05-01-preview can't modify access permissions that were set outside of the 2026-05-01-preview. If you use the 2026-05-01-preview with access- or permission-restricted content, a timing lag will occur before the 2026-05-01-preview recognizes changes to those access or permission restrictions.

If your knowledge sources contain permission-protected content, the retrieval engine can filter results so that each user only sees the documents they're authorized to access. You enable this filtering by passing the end user's identity on the retrieve request. Without the identity token, results from permission-enabled knowledge sources are returned unfiltered.

Permissions enforcement has two parts:

- [**Ingestion time**](#ingestion-time-configuration): For indexed knowledge sources only, set `ingestionPermissionOptions` to ingest permission metadata alongside content.

- [**Query time**](#query-time-authorization): Pass the user's access token in the `x-ms-query-source-authorization` header.

### Ingestion-time configuration

The following table shows which knowledge sources require ingestion-time configuration and how each source enforces permissions.

| Knowledge source | Requires `ingestionPermissionOptions` | How permissions are enforced |
|---|---|---|
| [Blob or ADLS Gen2](agentic-knowledge-source-how-to-blob.md#ingestion-parameters-properties) | ✅ | Ingested RBAC scopes, ACLs, or Microsoft Purview matched against user identity. |
| [OneLake](agentic-knowledge-source-how-to-onelake.md#ingestion-parameters-properties) | ✅ | Ingested document Microsoft Purview sensitivity labels matched against user identity. |
| [Indexed SharePoint](agentic-knowledge-source-how-to-sharepoint-indexed.md#ingestion-parameters-properties) | ✅ | Ingested SharePoint ACLs or Microsoft Purview sensitivity labels matched against user identity. |
| [Remote SharePoint](agentic-knowledge-source-how-to-sharepoint-remote.md#assign-to-a-knowledge-base) | ❌ | Copilot Retrieval API queries SharePoint directly using the user's token. |
| [Fabric Data Agent](agentic-knowledge-source-how-to-fabric-data-agent.md#enforce-permissions-at-query-time) | ❌ | The retrieval engine exchanges the user's token for a Microsoft Fabric–scoped token and queries the data agent on their behalf. |
| [Fabric Ontology](agentic-knowledge-source-how-to-fabric-ontology.md#enforce-permissions-at-query-time) | ❌ | The retrieval engine exchanges the user's token for a Microsoft Fabric–scoped token and queries the ontology item on their behalf. |
| [Work IQ](agentic-knowledge-source-how-to-work-iq.md#enforce-permissions-at-query-time) | ❌ | The retrieval engine exchanges the user's token for a Work IQ–scoped token and queries Work IQ on their behalf. |

> [!IMPORTANT]
> If `ingestionPermissionOptions` wasn't configured when the indexed knowledge source was created, no permission metadata exists in the index. Results are returned unfiltered, regardless of the header. To fix this, recreate the knowledge source with the appropriate `ingestionPermissionOptions` values.

### Query-time authorization

To pass the end user's identity, include an access token scoped to `https://search.azure.com/.default` on the retrieve request. This token is separate from the service credential used to access the search service. It doesn't need search service permissions and only represents the user whose content access is evaluated. For more information, see [Query-time ACL and RBAC enforcement](search-query-access-control-rbac-enforcement.md).

:::zone pivot="csharp"

In the .NET SDK, pass the token as the `xMsQuerySourceAuthorization` parameter on `RetrieveAsync`:

```csharp
using Azure;
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
from azure.identity import DefaultAzureCredential
from azure.core.credentials import get_bearer_token_provider
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

POST {{search-url}}/knowledgebases/{{knowledge-base-name}}/retrieve?api-version=2026-05-01-preview
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

**Reference:** [Knowledge Retrieval - Retrieve](/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2026-05-01-preview&preserve-view=true)

:::zone-end

## Review the response

Successful retrieval returns a `200 OK` status code. If the knowledge base fails to retrieve from one or more knowledge sources, the service returns a `206 Partial Content` status code. The response only includes results from sources that succeeded. The activity array contains details about the partial response as errors.

The retrieve action returns three main components:

# [2026-05-01-preview](#tab/2026-05-01-preview)

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

+ The `maxOutputSizeInTokens` property (`maxOutputSize` in 2026-05-01-preview) on the retrieve request determines the length of the string.

    > [!IMPORTANT]
    > A document that exceeds the `maxOutputSizeInTokens` output budget can be omitted from the response. The activity array includes a warning when the most relevant document exceeds the maximum output size. To retain more content, increase `maxOutputSizeInTokens`. For more information, see [Troubleshoot empty responses](#troubleshoot-empty-responses).

### Activity array

The activity array outputs the query plan, which provides operational transparency for tracking operations, billing implications, and resource invocations. It also includes subqueries sent to the retrieval pipeline and errors for any retrieval failures, such as inaccessible knowledge sources.

The output includes the following components.

# [2026-05-01-preview](#tab/2026-05-01-preview)

| Section | Description |
|---------|-------------|
| `modelQueryPlanning` | For knowledge bases that use an LLM for query planning, this section reports on the token counts used for input, and the token count for the subqueries. Includes a `modelName` field with the public model name (not the deployment name) of the model that ran the activity. |
| Source-specific activity | For each knowledge source included in the query, this section reports on elapsed time and which arguments were used in the query, including semantic ranker. Knowledge source types include `searchIndex`, `azureBlob`, and other [supported knowledge sources](agentic-knowledge-source-overview.md#supported-knowledge-sources). |
| `agenticReasoning` | This section reports on token consumption for agentic reasoning during retrieval, which depends on the specified [retrieval reasoning effort](agentic-retrieval-how-to-set-retrieval-reasoning-effort.md). |
| `modelAnswerSynthesis` | For knowledge bases that use [answer synthesis](agentic-retrieval-how-to-answer-synthesis.md), this section reports on the token count for formulating the answer, and the token count of the answer output. Includes a `modelName` field with the public model name (not the deployment name) of the model that ran the activity. |
| `modelWebSummarization` | For knowledge bases that use web summarization, this section reports on token consumption for summarizing web results. Includes a `modelName` field with the public model name (not the deployment name) of the model that ran the activity. |
| `imageServing` | For knowledge sources that have [image serving](agentic-retrieval-how-to-image-serving.md) enabled, this section reports `imagesRetrieved`, `imagesSentToModel`, `totalImageSizeBytes`, and whether indexing-time `verbalizationUsed` was on. To find the number of dropped images, subtract `imagesSentToModel` from `imagesRetrieved`. |

# [2026-04-01](#tab/2026-04-01)

| Section | Description |
|---------|-------------|
| Source-specific activity | For each knowledge source included in the query, this section reports on elapsed time and which arguments were used in the query, including semantic ranker. Knowledge source types include `searchIndex`, `azureBlob`, and other [supported knowledge sources](agentic-knowledge-source-overview.md#supported-knowledge-sources). |
| `agenticReasoning` | This section reports on token consumption for agentic reasoning during retrieval. |

---

Here's an example of the activity array:

# [2026-05-01-preview](#tab/2026-05-01-preview)

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

## Inspect sensitivity label metadata in the response (preview)

> [!IMPORTANT]
> The 2026-05-01-preview can't modify access permissions that were set outside of the 2026-05-01-preview. If you use the 2026-05-01-preview with access- or permission-restricted content, a timing lag will occur before the 2026-05-01-preview recognizes changes to those access or permission restrictions.

When you query a knowledge base that ingests [Microsoft Purview sensitivity labels](search-indexer-sensitivity-labels.md), the retrieve response includes label metadata at two levels:

| Location | Field | Description |
|---|---|---|
| Per reference | `sensitivityLabelInfo` | The sensitivity label applied to each document returned in the `references` array. |
| Response | `metadata.responseSensitivityLabelInfo` | An aggregate label that represents the highest-priority sensitivity label across all referenced documents in the response. Useful for client-side display banners and policy enforcement. |

Microsoft Graph computes the response-level label from the per-reference labels using the [Microsoft Purview label inheritance rules](/purview/sensitivity-labels). Typically, the most restrictive label wins.

The following example shows a retrieve response with two referenced documents (one `Confidential`, one `Internal`) and the resulting response-level label.

```json
{
  "response": [
    {
      "role": "assistant",
      "content": [
        { "type": "text", "text": "[ ... grounding data ... ]" }
      ]
    }
  ],
  "references": [
    {
      "type": "azureBlob",
      "id": "0",
      "activitySource": 1,
      "docKey": "contract-2026.pdf",
      "sensitivityLabelInfo": {
        "labelId": "<label-guid>",
        "labelName": "Confidential",
        "color": "#FF0000",
        "tooltip": "Confidential — Recipients can read but not forward.",
        "isEncrypted": true,
        "priority": 3
      },
      "sourceData": null
    },
    {
      "type": "azureBlob",
      "id": "1",
      "activitySource": 1,
      "docKey": "policy-overview.pdf",
      "sensitivityLabelInfo": {
        "labelId": "<label-guid>",
        "labelName": "Internal",
        "color": "#FFA500",
        "tooltip": "For internal use only.",
        "isEncrypted": false,
        "priority": 1
      },
      "sourceData": null
    }
  ],
  "metadata": {
    "responseSensitivityLabelInfo": {
      "labelId": "<label-guid>",
      "labelName": "Confidential",
      "color": "#FF0000",
      "tooltip": "Confidential — Recipients can read but not forward.",
      "isEncrypted": true,
      "priority": 3
    }
  }
}
```

### Reference types that surface sensitivity labels

The field name and availability of label metadata depend on the knowledge source type that produced each reference.

| Reference `type` | Label field | Available when... |
|---|---|---|
| `azureBlob` | `sensitivityLabelInfo` | The blob knowledge source includes `sensitivityLabel` in `ingestionPermissionOptions`. |
| `indexedOneLake` | `sensitivityLabelInfo` | The OneLake knowledge source includes `sensitivityLabel` in `ingestionPermissionOptions`. |
| `indexedSharePoint` | `sensitivityLabelInfo` | The SharePoint-indexed knowledge source includes `sensitivityLabel` in `ingestionPermissionOptions`. |
| `searchIndex` | `sensitivityLabelInfo` | The underlying index has `purviewEnabled` set to `true` and a field marked with `sensitivityLabel: true`. |

### Display and audit recommendations

- Use `sensitivityLabelInfo.labelId` to look up the full label definition through the [Microsoft Graph sensitivity label APIs](/graph/api/sensitivitylabel-get) when you need additional properties, such as policy controls or permissions.

- Use `metadata.responseSensitivityLabelInfo` to render a response-level sensitivity banner or apply policy controls, such as disabling copy and share, across the answer.

- If your knowledge source points to a chunked index, such as one populated through integrated vectorization or a custom Text Split skill, make sure the skillset [projects the sensitivity label to each chunk row](search-indexer-sensitivity-labels.md#6-configure-index-projections-in-your-skillset-if-applicable). Without this mapping, chunk-level references aren't filtered correctly at query time.

- For auditable administrative access to labeled content, see [Elevated read for administrative investigations](search-query-sensitivity-labels.md#elevated-read-for-administrative-investigations-preview).

### MCP server behavior

The MCP endpoint exposed by each knowledge base surfaces the same sensitivity label fields as the REST API. When an MCP-compatible client invokes the `knowledge_base_retrieve` tool, the tool result contains the same per-reference `sensitivityLabelInfo` and response-level `metadata.responseSensitivityLabelInfo` documented earlier in this section. MCP clients enforce label-aware display and policy controls based on these fields.

## Retrieve action examples (preview)

The following examples illustrate different ways to call the retrieve action using the 2026-05-01-preview API version, which supports the full feature set, including answer synthesis and a configurable reasoning effort. For 2026-04-01 usage, see the previous sections.

+ [Inspect model names in activity logs](#inspect-model-names-in-activity-logs)
+ [Require a knowledge source to succeed](#require-a-knowledge-source-to-succeed)
+ [Tune candidate documents per knowledge source](#tune-candidate-documents-per-knowledge-source)
+ [Limit final grounding documents](#limit-final-grounding-documents)
+ [Override default reasoning effort and set request limits](#override-default-reasoning-effort-and-set-request-limits)
+ [Set references for each knowledge source](#set-references-for-each-knowledge-source)
+ [Use minimal reasoning effort](#use-minimal-reasoning-effort)

### Inspect model names in activity logs

Model-backed activity records include a `modelName` field when `includeActivity` is enabled. Use this field to confirm which configured model handled query planning, answer synthesis, or web summarization during a retrieve request.

:::zone pivot="csharp"

```csharp
var retrievalRequest = new KnowledgeBaseRetrievalRequest();
retrievalRequest.Messages.Add(
    new KnowledgeBaseMessage(
        content: new[] {
            new KnowledgeBaseMessageTextContent("Which policy applies to returns?")
        }
    ) { Role = "user" }
);
retrievalRequest.IncludeActivity = true;

var result = await kbClient.RetrieveAsync(retrievalRequest);
foreach (var entry in result.Value.Activity)
{
    Console.WriteLine($"{entry.Type} modelName={entry.ModelName}");
}
```

**Reference:** [KnowledgeBaseRetrievalClient](/dotnet/api/azure.search.documents.knowledgebases.knowledgebaseretrievalclient?view=azure-dotnet-preview&preserve-view=true), [KnowledgeBaseRetrievalRequest](/dotnet/api/azure.search.documents.knowledgebases.models.knowledgebaseretrievalrequest?view=azure-dotnet-preview&preserve-view=true)

:::zone-end

:::zone pivot="python"

```python
request = KnowledgeBaseRetrievalRequest(
    messages=[
        KnowledgeBaseMessage(
            role="user",
            content=[KnowledgeBaseMessageTextContent(text="Which policy applies to returns?")],
        )
    ],
    include_activity=True,
)

result = kb_client.retrieve(request)
for entry in result.activity:
    print(entry.type, "modelName=", getattr(entry, "model_name", None))
```

**Reference:** [KnowledgeBaseRetrievalClient](/python/api/azure-search-documents/azure.search.documents.knowledgebases.knowledgebaseretrievalclient), [KnowledgeBaseRetrievalRequest](/python/api/azure-search-documents/azure.search.documents.knowledgebases.models.knowledgebaseretrievalrequest)

:::zone-end

:::zone pivot="rest"

```http
POST {{search-url}}/knowledgebases/{{knowledge-base-name}}/retrieve?api-version=2026-05-01-preview
Authorization: Bearer {{accessToken}}
Content-Type: application/json

{
    "messages": [
        {
            "role": "user",
            "content": [
                { "type": "text", "text": "Which policy applies to returns?" }
            ]
        }
    ],
    "includeActivity": true
}
```

**Reference:** [Knowledge Retrieval - Retrieve](/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2026-05-01-preview&preserve-view=true)

:::zone-end

The following response excerpt shows activity records with `modelName`.

```json
{
  "activity": [
    {
      "type": "modelQueryPlanning",
      "id": 0,
      "modelName": "gpt-5-mini",
      "inputTokens": 1842,
      "outputTokens": 87,
      "elapsedMs": 1923
    },
    {
      "type": "searchIndex",
      "id": 1,
      "knowledgeSourceName": "operations-ks",
      "count": 12,
      "elapsedMs": 234
    },
    {
      "type": "modelAnswerSynthesis",
      "id": 2,
      "modelName": "gpt-5-mini",
      "inputTokens": 2418,
      "outputTokens": 179,
      "elapsedMs": 931
    }
  ]
}
```

### Require a knowledge source to succeed

Set `failOnError` in `knowledgeSourceParams` to mark a knowledge source as required. Use this parameter when a partial answer would be misleading or noncompliant if that source is unavailable.

:::zone pivot="csharp"

```csharp
var retrievalRequest = new KnowledgeBaseRetrievalRequest();
retrievalRequest.Messages.Add(
    new KnowledgeBaseMessage(
        content: new[] {
            new KnowledgeBaseMessageTextContent("Which HR policy applies?")
        }
    ) { Role = "user" }
);
retrievalRequest.KnowledgeSourceParams.Add(
    new SearchIndexKnowledgeSourceParams("hr-policy-ks")
    {
        FailOnError = true,
        AlwaysQuerySource = true
    }
);
retrievalRequest.KnowledgeSourceParams.Add(
    new SearchIndexKnowledgeSourceParams("hr-faq-ks")
);

var result = await kbClient.RetrieveAsync(retrievalRequest);
```

**Reference:** [SearchIndexKnowledgeSourceParams](/dotnet/api/azure.search.documents.knowledgebases.models.searchindexknowledgesourceparams?view=azure-dotnet-preview&preserve-view=true)

:::zone-end

:::zone pivot="python"

```python
request = KnowledgeBaseRetrievalRequest(
    messages=[
        KnowledgeBaseMessage(
            role="user",
            content=[KnowledgeBaseMessageTextContent(text="Which HR policy applies?")],
        )
    ],
    knowledge_source_params=[
        SearchIndexKnowledgeSourceParams(
            knowledge_source_name="hr-policy-ks",
            fail_on_error=True,
            always_query_source=True,
        ),
        SearchIndexKnowledgeSourceParams(
            knowledge_source_name="hr-faq-ks",
        ),
    ],
)

result = kb_client.retrieve(request)
```

**Reference:** [SearchIndexKnowledgeSourceParams](/python/api/azure-search-documents/azure.search.documents.knowledgebases.models.searchindexknowledgesourceparams)

:::zone-end

:::zone pivot="rest"

```http
POST {{search-url}}/knowledgebases/{{knowledge-base-name}}/retrieve?api-version=2026-05-01-preview
Authorization: Bearer {{accessToken}}
Content-Type: application/json

{
    "messages": [
        {
            "role": "user",
            "content": [
                { "type": "text", "text": "Which HR policy applies?" }
            ]
        }
    ],
    "knowledgeSourceParams": [
        {
            "knowledgeSourceName": "hr-policy-ks",
            "kind": "searchIndex",
            "failOnError": true,
            "alwaysQuerySource": true
        },
        {
            "knowledgeSourceName": "hr-faq-ks",
            "kind": "searchIndex"
        }
    ]
}
```

**Reference:** [Knowledge Retrieval - Retrieve](/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2026-05-01-preview&preserve-view=true)

:::zone-end

### Tune candidate documents per knowledge source

Set `maxOutputDocuments` in `knowledgeSourceParams` to cap how many candidate documents a specific knowledge source contributes before final result selection. Use this parameter when you want to bound one source's input to the pipeline without affecting others.

:::zone pivot="csharp"

```csharp
var retrievalRequest = new KnowledgeBaseRetrievalRequest();
retrievalRequest.Messages.Add(
    new KnowledgeBaseMessage(
        content: new[] {
            new KnowledgeBaseMessageTextContent("What safety procedures apply?")
        }
    ) { Role = "user" }
);
retrievalRequest.KnowledgeSourceParams.Add(
    new SearchIndexKnowledgeSourceParams("operations-ks")
    {
        MaxOutputDocuments = 50
    }
);

var result = await kbClient.RetrieveAsync(retrievalRequest);
```

**Reference:** [SearchIndexKnowledgeSourceParams](/dotnet/api/azure.search.documents.knowledgebases.models.searchindexknowledgesourceparams?view=azure-dotnet-preview&preserve-view=true)

:::zone-end

:::zone pivot="python"

```python
request = KnowledgeBaseRetrievalRequest(
    messages=[
        KnowledgeBaseMessage(
            role="user",
            content=[KnowledgeBaseMessageTextContent(text="What safety procedures apply?")],
        )
    ],
    knowledge_source_params=[
        SearchIndexKnowledgeSourceParams(
            knowledge_source_name="operations-ks",
            max_output_documents=50,
        ),
    ],
)

result = kb_client.retrieve(request)
```

**Reference:** [SearchIndexKnowledgeSourceParams](/python/api/azure-search-documents/azure.search.documents.knowledgebases.models.searchindexknowledgesourceparams)

:::zone-end

:::zone pivot="rest"

```http
POST {{search-url}}/knowledgebases/operations-kb/retrieve?api-version=2026-05-01-preview
Authorization: Bearer {{accessToken}}
Content-Type: application/json

{
    "messages": [
        {
            "role": "user",
            "content": [
                { "type": "text", "text": "What safety procedures apply?" }
            ]
        }
    ],
    "knowledgeSourceParams": [
        {
            "knowledgeSourceName": "operations-ks",
            "kind": "searchIndex",
            "maxOutputDocuments": 50
        }
    ]
}
```

**Reference:** [Knowledge Retrieval - Retrieve](/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2026-05-01-preview&preserve-view=true)

:::zone-end


### Limit final grounding documents

The top-level `maxOutputDocuments` parameter caps how many grounding documents are returned in the final retrieve response. Use this parameter when your application needs a predictable citation or reference count.

:::zone pivot="csharp"

```csharp
var retrievalRequest = new KnowledgeBaseRetrievalRequest();
retrievalRequest.Messages.Add(
    new KnowledgeBaseMessage(
        content: new[] {
            new KnowledgeBaseMessageTextContent("What is the return policy?")
        }
    ) { Role = "user" }
);
retrievalRequest.OutputMode = "extractedData";
retrievalRequest.MaxOutputDocuments = 3;
retrievalRequest.MaxOutputSize = 6000;

var result = await kbClient.RetrieveAsync(retrievalRequest);
```

**Reference:** [KnowledgeBaseRetrievalRequest](/dotnet/api/azure.search.documents.knowledgebases.models.knowledgebaseretrievalrequest?view=azure-dotnet-preview&preserve-view=true)

:::zone-end

:::zone pivot="python"

```python
request = KnowledgeBaseRetrievalRequest(
    messages=[
        KnowledgeBaseMessage(
            role="user",
            content=[KnowledgeBaseMessageTextContent(text="What is the return policy?")],
        )
    ],
    output_mode="extractedData",
    max_output_documents=3,
    max_output_size=6000,
)

result = kb_client.retrieve(request)
```

**Reference:** [KnowledgeBaseRetrievalRequest](/python/api/azure-search-documents/azure.search.documents.knowledgebases.models.knowledgebaseretrievalrequest)

:::zone-end

:::zone pivot="rest"

```http
POST {{search-url}}/knowledgebases/{{knowledge-base-name}}/retrieve?api-version=2026-05-01-preview
Authorization: Bearer {{accessToken}}
Content-Type: application/json

{
    "messages": [
        {
            "role": "user",
            "content": [
                { "type": "text", "text": "What is the return policy?" }
            ]
        }
    ],
    "outputMode": "extractedData",
    "maxOutputDocuments": 3,
    "maxOutputSize": 6000
}
```

**Reference:** [Knowledge Retrieval - Retrieve](/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2026-05-01-preview&preserve-view=true)

:::zone-end

The following table shows how `maxOutputDocuments` and `maxOutputSize` interact across all four combinations.

| `maxOutputDocuments` | `maxOutputSize` | Behavior |
| --- | --- | --- |
| Unspecified | Unspecified | Uses the default `maxOutputSize` response limit behavior. |
| Unspecified | Specified | Discards documents once the payload-size limit is reached. |
| Specified | Unspecified | Returns up to the specified number of grounding documents and doesn't apply a `maxOutputSize` limit. |
| Specified | Specified | Returns up to `maxOutputDocuments` documents or however many documents fit under `maxOutputSize`, whichever limit applies first. |


### Override default reasoning effort and set request limits

This example specifies [answer synthesis](agentic-retrieval-how-to-answer-synthesis.md), so the retrieval reasoning effort must be `low` or `medium`. It also sets `maxRuntimeInSeconds` to cap total request latency and `maxOutputSize` to bound the response payload.

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

result = kb_client.retrieve(request)
print(result.response[0].content[0].text)
```

**Reference:** [KnowledgeBaseRetrievalClient](/python/api/azure-search-documents/azure.search.documents.knowledgebases.knowledgebaseretrievalclient), [KnowledgeBaseRetrievalRequest](/python/api/azure-search-documents/azure.search.documents.knowledgebases.models.knowledgebaseretrievalrequest)

:::zone-end

:::zone pivot="rest"

```http
POST {{search-url}}/knowledgebases/kb-override/retrieve?api-version=2026-05-01-preview
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

**Reference:** [Knowledge Retrieval - Retrieve](/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2026-05-01-preview&preserve-view=true)

:::zone-end

### Set references for each knowledge source

Use `includeReferences` and `includeReferenceSourceData` in `knowledgeSourceParams` to control which sources appear in the references array and how much source data each entry includes. This example uses the knowledge base's default reasoning effort.

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

result = kb_client.retrieve(request)
print(result.response[0].content[0].text)
```

**Reference:** [KnowledgeBaseRetrievalClient](/python/api/azure-search-documents/azure.search.documents.knowledgebases.knowledgebaseretrievalclient), [SearchIndexKnowledgeSourceParams](/python/api/azure-search-documents/azure.search.documents.knowledgebases.models.searchindexknowledgesourceparams)

:::zone-end

:::zone pivot="rest"

```http
POST {{search-url}}/knowledgebases/kb-medium-example/retrieve?api-version=2026-05-01-preview
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

**Reference:** [Knowledge Retrieval - Retrieve](/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2026-05-01-preview&preserve-view=true)

:::zone-end


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

result = kb_client.retrieve(request)
print(result.response[0].content[0].text)
```

**Reference:** [KnowledgeBaseRetrievalClient](/python/api/azure-search-documents/azure.search.documents.knowledgebases.knowledgebaseretrievalclient), [KnowledgeBaseRetrievalRequest](/python/api/azure-search-documents/azure.search.documents.knowledgebases.models.knowledgebaseretrievalrequest)

:::zone-end

:::zone pivot="rest"

```http
POST {{search-url}}/knowledgebases/kb-minimal/retrieve?api-version=2026-05-01-preview
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

**Reference:** [Knowledge Retrieval - Retrieve](/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2026-05-01-preview&preserve-view=true)

:::zone-end

## Troubleshoot empty responses

A document can be found during the search step but still be omitted from the final response if its grounded content exceeds the `maxOutputSizeInTokens` (`maxOutputSize` in 2026-05-01-preview) output budget. When this happens, the activity array shows that matches were found, and the activity record includes a warning that the most relevant document exceeded the maximum output size. The references array and grounded response content are empty for that document. To retain more content, increase `maxOutputSizeInTokens`.

To avoid this behavior, index large source documents as smaller chunks with stable identifiers and source metadata. This applies especially to long manuals, policies, or knowledge base articles.

## Related content

+ [Agentic retrieval in Azure AI Search](agentic-retrieval-overview.md)
+ [Query-time ACL and RBAC enforcement](search-query-access-control-rbac-enforcement.md)
+ [Use a blob indexer or knowledge source to ingest RBAC scopes metadata](search-blob-indexer-role-based-access.md)
+ [Agentic RAG: Build a reasoning retrieval engine with Azure AI Search (YouTube video)](https://www.youtube.com/watch?v=PeTmOidqHM8)
+ [Azure OpenAI demo featuring agentic retrieval](https://github.com/Azure-Samples/azure-search-openai-demo)
