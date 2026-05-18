---
title: include file
description: include file
author: alvinashcraft
ms.author: aashcraft
ms.service: microsoft-foundry
ms.topic: include
ms.date: 05/18/2026
ms.custom: include, classic-and-new, doc-kit-assisted
ai-usage: ai-assisted
---

Web search enables models to retrieve and ground responses with real-time information from the public web before generating output. When enabled, the model can return up-to-date answers with inline citations. You can access web search through the `web_search` tool in the **Responses API**.

> [!NOTE]
> In the Azure OpenAI Responses API, use the `web_search` tool for web search.
> The preview version of the web search tool (`web_search_preview`) is supported but not recommended. It has limitations.

> [!IMPORTANT]
> - Web Search uses Grounding with Bing Search and/or Grounding with Bing Custom Search, which are [First Party Consumption Services](https://www.microsoft.com/licensing/terms/product/ForOnlineServices/EAEAS) governed by these [Grounding with Bing terms of use](https://www.microsoft.com/en-us/bing/apis/grounding-legal-enterprise) and the [Microsoft Privacy Statement](https://go.microsoft.com/fwlink/?LinkId=521839&clcid=0x409).
> - The Microsoft [Data Protection Addendum](https://aka.ms/dpa) doesn't apply to data sent to Grounding with Bing Search and/or Grounding with Bing Custom Search. When you use Grounding with Bing Search and/or Grounding with Bing Custom Search, your data flows outside your compliance and geo boundary.
> - Use of Grounding with Bing Search and Grounding with Bing Custom Search incurs costs. To learn more, see [pricing](https://www.microsoft.com/bing/apis/grounding-pricing).
> - [Learn more](#manage-web-search-tool) about how Azure admins can manage access to the use of Web search.

## Prerequisites

- An Azure OpenAI model deployed.
- An authentication method:
  - API key, or
  - Microsoft Entra ID.
- Install the client library for your language:
  - **Python**: `pip install openai azure-identity`
  - **.NET**: `dotnet add package OpenAI` and `dotnet add package Azure.Identity`
  - **JavaScript/TypeScript**: `npm install openai @azure/identity`
  - **Java**: Add `com.openai:openai-java` and `com.azure:azure-identity` to your project.
- For REST examples, set `AZURE_OPENAI_API_KEY` (API key flow) or `AZURE_OPENAI_AUTH_TOKEN` (Microsoft Entra ID flow).

## Options to use web search

Web search supports three modes. Choose the mode based on the depth and speed you need.

### Web search without reasoning

The model forwards the user query directly to the web search tool and uses top-ranked sources to ground the response. There's no multi-step planning. This mode is **fast** and best for quick lookups and timely facts.

### Agentic search with reasoning models

The model actively manages the search process and can perform web searches as part of its chain of thought, analyze results, and decide whether to keep searching. This flexibility makes agentic search well **suited for complex workflows**, but it also means searches take **longer** than quick lookups. For example, use `gpt-5.5` with `reasoning.effort` set to `medium` or `high` to balance search depth and latency.

### Deep research

Deep Research is an agent-driven mode designed for **extended investigations**. The model performs multi-step reasoning, opens and reads many pages, and synthesizes findings into a comprehensive, citation-rich response. Use this mode with `o3-deep-research`, or with `gpt-5.5` and `reasoning.effort` set to `high` or `xhigh`.

Deep Research can run for several minutes and is best for background-style workloads that prioritize completeness over speed.

## How it works

You use web search by declaring the tool `{"type": "web_search"}` in your request. The model decides whether to call the tool based on the user's prompt and your configuration.

> [!NOTE]
> Web Search in the Responses API works with GPT-4 models and later.

In the examples that follow, replace `gpt-5.5` with the name of your own model deployment. The same `assert` pattern shown in the basic Microsoft Entra ID snippets applies to the API-key snippets and the user-location and domain-filtering examples.

# [Python](#tab/python)

**Microsoft Entra ID:**

```python
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/"
token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://ai.azure.com/.default"
)

# Use the OpenAI client with the Azure v1 endpoint.
openai = OpenAI(
    base_url=endpoint,
    api_key=token_provider,
)

response = openai.responses.create(
    model="gpt-5.5",
    tools=[{"type": "web_search"}],
    input="Please perform a web search on the latest trends in renewable energy",
)

print(response.output_text)

# Verify the call succeeded.
assert response.output_text, "Empty output_text"
assert any(item.type == "web_search_call" for item in response.output), \
    "No web_search_call in response"
```

**API key:**

```python
import os
from openai import OpenAI

endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/"

openai = OpenAI(
    base_url=endpoint,
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
)

response = openai.responses.create(
    model="gpt-5.5",
    tools=[{"type": "web_search"}],
    input="Please perform a web search on the latest trends in renewable energy",
)

print(response.output_text)
```

# [C#](#tab/csharp)

**Microsoft Entra ID:**

```csharp
using Azure.Identity;
using OpenAI.Responses;
using System.ClientModel.Primitives;
using System.Diagnostics;

#pragma warning disable OPENAI001

string endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1";

BearerTokenPolicy tokenPolicy = new(
    new DefaultAzureCredential(),
    "https://ai.azure.com/.default");

ResponsesClient openAIClient = new(
    authenticationPolicy: tokenPolicy,
    options: new ResponsesClientOptions { Endpoint = new Uri(endpoint) });

CreateResponseOptions options = new()
{
    Model = "gpt-5.5",
    Tools = { ResponseTool.CreateWebSearchTool() }
};
options.InputItems.Add(ResponseItem.CreateUserMessageItem(
    "Please perform a web search on the latest trends in renewable energy"));

ResponseResult response = await openAIClient.CreateResponseAsync(options);
Console.WriteLine(response.GetOutputText());

// Verify the call succeeded.
Debug.Assert(!string.IsNullOrEmpty(response.GetOutputText()), "Empty output text");
Debug.Assert(
    response.OutputItems.Any(item => item is WebSearchCallResponseItem),
    "No web_search_call in response");
```

**API key:**

```csharp
using OpenAI.Responses;
using System.ClientModel;

#pragma warning disable OPENAI001

string endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1";
string apiKey = Environment.GetEnvironmentVariable("AZURE_OPENAI_API_KEY")!;

ResponsesClient openAIClient = new(
    credential: new ApiKeyCredential(apiKey),
    options: new ResponsesClientOptions { Endpoint = new Uri(endpoint) });

CreateResponseOptions options = new()
{
    Model = "gpt-5.5",
    Tools = { ResponseTool.CreateWebSearchTool() }
};
options.InputItems.Add(ResponseItem.CreateUserMessageItem(
    "Please perform a web search on the latest trends in renewable energy"));

ResponseResult response = await openAIClient.CreateResponseAsync(options);
Console.WriteLine(response.GetOutputText());
```

# [JavaScript](#tab/javascript)

**Microsoft Entra ID:**

```javascript
// Save this file with the .mjs extension, or add "type": "module" to your package.json.
import { OpenAI } from "openai";
import { DefaultAzureCredential, getBearerTokenProvider } from "@azure/identity";

const endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/";
const tokenProvider = getBearerTokenProvider(
  new DefaultAzureCredential(),
  "https://ai.azure.com/.default"
);

const openai = new OpenAI({
  baseURL: endpoint,
  apiKey: await tokenProvider(),
});

const response = await openai.responses.create({
  model: "gpt-5.5",
  tools: [{ type: "web_search" }],
  input: "Please perform a web search on the latest trends in renewable energy",
});

console.log(response.output_text);

// Verify the call succeeded.
console.assert(response.output_text, "Empty output_text");
console.assert(
  response.output.some((item) => item.type === "web_search_call"),
  "No web_search_call in response"
);
```

**API key:**

```javascript
import { OpenAI } from "openai";

const endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/";

const openai = new OpenAI({
  baseURL: endpoint,
  apiKey: process.env.AZURE_OPENAI_API_KEY,
});

const response = await openai.responses.create({
  model: "gpt-5.5",
  tools: [{ type: "web_search" }],
  input: "Please perform a web search on the latest trends in renewable energy",
});

console.log(response.output_text);
```

# [Java](#tab/java)

**Microsoft Entra ID:**

```java
import com.azure.identity.AuthenticationUtil;
import com.azure.identity.DefaultAzureCredentialBuilder;
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.credential.BearerTokenCredential;
import com.openai.models.responses.Response;
import com.openai.models.responses.ResponseCreateParams;
import com.openai.models.responses.WebSearchTool;

public class WebSearchExample {
    public static void main(String[] args) {
        String endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1";

        OpenAIClient openAIClient = OpenAIOkHttpClient.builder()
            .baseUrl(endpoint)
            .credential(BearerTokenCredential.create(
                AuthenticationUtil.getBearerTokenSupplier(
                    new DefaultAzureCredentialBuilder().build(),
                    "https://ai.azure.com/.default")))
            .build();

        WebSearchTool webSearchTool = WebSearchTool.builder()
            .type(WebSearchTool.Type.WEB_SEARCH)
            .build();

        ResponseCreateParams params = ResponseCreateParams.builder()
            .model("gpt-5.5")
            .input("Please perform a web search on the latest trends in renewable energy")
            .addTool(webSearchTool)
            .build();

        Response response = openAIClient.responses().create(params);
        response.output().forEach(item -> item.message().ifPresent(msg ->
            msg.content().forEach(content -> content.outputText().ifPresent(
                t -> System.out.println(t.text())))));

        // Verify the call succeeded.
        boolean hasWebSearchCall = response.output().stream()
            .anyMatch(item -> item.webSearchCall().isPresent());
        assert hasWebSearchCall : "No web_search_call in response";
    }
}
```

**API key:**

```java
import com.openai.azure.credential.AzureApiKeyCredential;
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.models.responses.Response;
import com.openai.models.responses.ResponseCreateParams;
import com.openai.models.responses.WebSearchTool;

public class WebSearchExample {
    public static void main(String[] args) {
        String endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1";

        OpenAIClient openAIClient = OpenAIOkHttpClient.builder()
            .baseUrl(endpoint)
            .credential(AzureApiKeyCredential.create(System.getenv("AZURE_OPENAI_API_KEY")))
            .build();

        WebSearchTool webSearchTool = WebSearchTool.builder()
            .type(WebSearchTool.Type.WEB_SEARCH)
            .build();

        ResponseCreateParams params = ResponseCreateParams.builder()
            .model("gpt-5.5")
            .input("Please perform a web search on the latest trends in renewable energy")
            .addTool(webSearchTool)
            .build();

        Response response = openAIClient.responses().create(params);
        response.output().forEach(item -> item.message().ifPresent(msg ->
            msg.content().forEach(content -> content.outputText().ifPresent(
                t -> System.out.println(t.text())))));
    }
}
```

# [REST](#tab/rest)

**Microsoft Entra ID:**

```bash
curl -X POST https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/responses \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AZURE_OPENAI_AUTH_TOKEN" \
  -d '{
     "model": "gpt-5.5",
     "tools": [{"type": "web_search"}],
     "input": "Please perform a web search on the latest trends in renewable energy"
    }'
```

The response returns HTTP 200 with a JSON body whose `output` array contains both a `web_search_call` item and a `message` item. If either is missing, the call didn't perform a web search.

**API key:**

```bash
curl -X POST https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/responses \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
  -d '{
     "model": "gpt-5.5",
     "tools": [{"type": "web_search"}],
     "input": "Please perform a web search on the latest trends in renewable energy"
    }'
```

---

### Response shape

A successful response that uses web search typically contains two parts:

```json
[
    {
      "id": "ws_68b9d1220b288199bf942a3e48055f3602e3b78a8dbf73ac",
      "type": "web_search_call",
      "status": "completed",
      "action": {
        "type": "search",
        "query": "latest trends in renewable energy 2025"
      }
    },
    {
      "id": "msg_68b9d123f4788199a544b6b97e65673e02e3b78a8dbf73ac",
      "type": "message",
      "status": "completed",
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "annotations": [
            {
                "type": "url_citation",
                "start_index": 1358,
                "end_index": 1462,
                "url": "https://...",
                "title": "Title..."
            }
        ],
          "text": "If you're searching for uplifting....."
        }
      ],
    }
  ]
```

- A `web_search_call` output item that records the action performed:
  - `search`: a web search action, including the query (and optionally the searched domains). **Search actions incur tool call costs** (see [pricing](https://www.microsoft.com/bing/apis/grounding-pricing)).
  - `open_page`: indicates the agent opened a page. Available with all reasoning models.
  - `find_in_page`: indicates the agent searched within an opened page. Available with all reasoning models.
- A message output item containing:
  - The grounded text in `message.content[0].text`.
  - URL citations in `message.content[0].annotations`, one or more `url_citation` objects that include the URL, title, and character ranges.

When you use a reasoning model, the `output` array also contains a `reasoning` item alongside `web_search_call` and `message`. Parse the array by `type` rather than by position.

### Control results by user location

You can refine search results by passing the approximate user location. The following fields are supported:

| Field | Description | Example |
| --- | --- | --- |
| `country` | Two-letter [ISO country/region code](https://en.wikipedia.org/wiki/ISO_3166-1). | `US` |
| `city` | Free-text city name. | `Chicago` |
| `region` | Free-text region or state name. | `Illinois` |
| `timezone` | [IANA time zone identifier](https://www.iana.org/time-zones). | `America/Chicago` |

> [!NOTE]
> The `city`, `region`, and `timezone` fields are only supported when you use the `web_search` tool (the GA version, not `web_search_preview`).

# [Python](#tab/python)

```python
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/"
token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://ai.azure.com/.default"
)

openai = OpenAI(base_url=endpoint, api_key=token_provider)

response = openai.responses.create(
    model="gpt-5.5",
    tools=[
        {
            "type": "web_search",
            "user_location": {
                "type": "approximate",
                "country": "US",
                "city": "Chicago",
                "region": "Illinois",
                "timezone": "America/Chicago",
            },
        }
    ],
    input="Give me a positive news story from the web today in my city",
)

print(response.output_text)
```

# [C#](#tab/csharp)

```csharp
using Azure.Identity;
using OpenAI.Responses;
using System.ClientModel.Primitives;

#pragma warning disable OPENAI001

string endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1";

BearerTokenPolicy tokenPolicy = new(
    new DefaultAzureCredential(),
    "https://ai.azure.com/.default");

ResponsesClient openAIClient = new(
    authenticationPolicy: tokenPolicy,
    options: new ResponsesClientOptions { Endpoint = new Uri(endpoint) });

WebSearchToolApproximateLocation location =
    WebSearchToolLocation.CreateApproximateLocation(
        country: "US",
        region: "Illinois",
        city: "Chicago",
        timezone: "America/Chicago");

CreateResponseOptions options = new()
{
    Model = "gpt-5.5",
    Tools = { ResponseTool.CreateWebSearchTool(userLocation: location) }
};
options.InputItems.Add(ResponseItem.CreateUserMessageItem(
    "Give me a positive news story from the web today in my city"));

ResponseResult response = await openAIClient.CreateResponseAsync(options);
Console.WriteLine(response.GetOutputText());
```

# [JavaScript](#tab/javascript)

```javascript
import { OpenAI } from "openai";
import { DefaultAzureCredential, getBearerTokenProvider } from "@azure/identity";

const endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/";
const tokenProvider = getBearerTokenProvider(
  new DefaultAzureCredential(),
  "https://ai.azure.com/.default"
);

const openai = new OpenAI({
  baseURL: endpoint,
  apiKey: await tokenProvider(),
});

const response = await openai.responses.create({
  model: "gpt-5.5",
  tools: [
    {
      type: "web_search",
      user_location: {
        type: "approximate",
        country: "US",
        city: "Chicago",
        region: "Illinois",
        timezone: "America/Chicago",
      },
    },
  ],
  input: "Give me a positive news story from the web today in my city",
});

console.log(response.output_text);
```

# [Java](#tab/java)

```java
import com.azure.identity.AuthenticationUtil;
import com.azure.identity.DefaultAzureCredentialBuilder;
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.credential.BearerTokenCredential;
import com.openai.models.responses.Response;
import com.openai.models.responses.ResponseCreateParams;
import com.openai.models.responses.WebSearchTool;
import com.openai.models.responses.WebSearchTool.UserLocation;

public class WebSearchLocationExample {
    public static void main(String[] args) {
        String endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1";

        OpenAIClient openAIClient = OpenAIOkHttpClient.builder()
            .baseUrl(endpoint)
            .credential(BearerTokenCredential.create(
                AuthenticationUtil.getBearerTokenSupplier(
                    new DefaultAzureCredentialBuilder().build(),
                    "https://ai.azure.com/.default")))
            .build();

        WebSearchTool webSearchTool = WebSearchTool.builder()
            .type(WebSearchTool.Type.WEB_SEARCH)
            .userLocation(UserLocation.builder()
                .country("US")
                .city("Chicago")
                .region("Illinois")
                .timezone("America/Chicago")
                .build())
            .build();

        ResponseCreateParams params = ResponseCreateParams.builder()
            .model("gpt-5.5")
            .input("Give me a positive news story from the web today in my city")
            .addTool(webSearchTool)
            .build();

        Response response = openAIClient.responses().create(params);
        response.output().forEach(item -> item.message().ifPresent(msg ->
            msg.content().forEach(content -> content.outputText().ifPresent(
                t -> System.out.println(t.text())))));
    }
}
```

# [REST](#tab/rest)

```bash
curl -X POST https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/responses \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AZURE_OPENAI_AUTH_TOKEN" \
  -d '{
    "model": "gpt-5.5",
    "tools": [
        {
            "type": "web_search",
            "user_location": {
                "type": "approximate",
                "country": "US",
                "city": "Chicago",
                "region": "Illinois",
                "timezone": "America/Chicago"
            }
        }
    ],
    "input": "Give me a positive news story from the web today in my city"
    }'
```

---

To use API key authentication, replace the Microsoft Entra credential with your API key as shown in the [basic example](#how-it-works).

### Domain filtering

You can limit results to a specific set of domains by using domain filtering. You can allowlist up to 100 URLs. You can omit the HTTP or HTTPS prefix when formatting the URLs. For example, use `microsoft.com` instead of `https://www.microsoft.com/`. Subdomains are also included in the search. Domain filtering works with the `web_search` tool only in the Responses API.

To return the sources the model consulted, set `include` to `["web_search_call.action.sources"]`. The matched source URLs appear in the `action.sources` array of the `web_search_call` output item. Each entry contains a `type` and a `url`. Page titles aren't returned in `action.sources`; the model's grounded text includes titles in the `url_citation` annotations on the message item instead.

To return the full content of pages the model consulted, set `include` to `["web_search_call.results"]`. The `web_search_call.results` option is supported only when you use a reasoning model.

# [Python](#tab/python)

```python
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/"
token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://ai.azure.com/.default"
)

openai = OpenAI(base_url=endpoint, api_key=token_provider)

response = openai.responses.create(
    model="gpt-5.5",
    reasoning={"effort": "low"},
    tools=[
        {
            "type": "web_search",
            "filters": {
                "allowed_domains": [
                    "pubmed.ncbi.nlm.nih.gov",
                    "clinicaltrials.gov",
                    "www.who.int",
                    "www.cdc.gov",
                    "www.fda.gov",
                ]
            },
        }
    ],
    tool_choice="auto",
    include=["web_search_call.action.sources"],
    input="Please perform a web search on how semaglutide is used in the treatment of diabetes.",
)

print(response.output_text)
```

# [C#](#tab/csharp)

```csharp
using Azure.Identity;
using OpenAI.Responses;
using System.ClientModel.Primitives;

#pragma warning disable OPENAI001

string endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1";

BearerTokenPolicy tokenPolicy = new(
    new DefaultAzureCredential(),
    "https://ai.azure.com/.default");

ResponsesClient openAIClient = new(
    authenticationPolicy: tokenPolicy,
    options: new ResponsesClientOptions { Endpoint = new Uri(endpoint) });

WebSearchToolFilters filters = new();
filters.AllowedDomains.Add("pubmed.ncbi.nlm.nih.gov");
filters.AllowedDomains.Add("clinicaltrials.gov");
filters.AllowedDomains.Add("www.who.int");
filters.AllowedDomains.Add("www.cdc.gov");
filters.AllowedDomains.Add("www.fda.gov");

CreateResponseOptions options = new()
{
    Model = "gpt-5.5",
    ReasoningOptions = new ResponseReasoningOptions { ReasoningEffortLevel = ResponseReasoningEffortLevel.Low },
    Tools = { ResponseTool.CreateWebSearchTool(filters: filters) },
    ToolChoice = ResponseToolChoice.CreateAutoChoice(),
    IncludedProperties = { IncludedResponseProperty.WebSearchCallActionSources }
};
options.InputItems.Add(ResponseItem.CreateUserMessageItem(
    "Please perform a web search on how semaglutide is used in the treatment of diabetes."));

ResponseResult response = await openAIClient.CreateResponseAsync(options);
Console.WriteLine(response.GetOutputText());
```

# [JavaScript](#tab/javascript)

```javascript
import { OpenAI } from "openai";
import { DefaultAzureCredential, getBearerTokenProvider } from "@azure/identity";

const endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/";
const tokenProvider = getBearerTokenProvider(
  new DefaultAzureCredential(),
  "https://ai.azure.com/.default"
);

const openai = new OpenAI({
  baseURL: endpoint,
  apiKey: await tokenProvider(),
});

const response = await openai.responses.create({
  model: "gpt-5.5",
  reasoning: { effort: "low" },
  tools: [
    {
      type: "web_search",
      filters: {
        allowed_domains: [
          "pubmed.ncbi.nlm.nih.gov",
          "clinicaltrials.gov",
          "www.who.int",
          "www.cdc.gov",
          "www.fda.gov",
        ],
      },
    },
  ],
  tool_choice: "auto",
  include: ["web_search_call.action.sources"],
  input: "Please perform a web search on how semaglutide is used in the treatment of diabetes.",
});

console.log(response.output_text);
```

# [Java](#tab/java)

```java
import com.azure.identity.AuthenticationUtil;
import com.azure.identity.DefaultAzureCredentialBuilder;
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.credential.BearerTokenCredential;
import com.openai.models.responses.Response;
import com.openai.models.responses.ResponseCreateParams;
import com.openai.models.responses.ResponseIncludable;
import com.openai.models.responses.WebSearchTool;
import com.openai.models.responses.WebSearchTool.Filters;
import java.util.List;

public class WebSearchDomainFilterExample {
    public static void main(String[] args) {
        String endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1";

        OpenAIClient openAIClient = OpenAIOkHttpClient.builder()
            .baseUrl(endpoint)
            .credential(BearerTokenCredential.create(
                AuthenticationUtil.getBearerTokenSupplier(
                    new DefaultAzureCredentialBuilder().build(),
                    "https://ai.azure.com/.default")))
            .build();

        WebSearchTool webSearchTool = WebSearchTool.builder()
            .type(WebSearchTool.Type.WEB_SEARCH)
            .filters(Filters.builder()
                .addAllowedDomain("pubmed.ncbi.nlm.nih.gov")
                .addAllowedDomain("clinicaltrials.gov")
                .addAllowedDomain("www.who.int")
                .addAllowedDomain("www.cdc.gov")
                .addAllowedDomain("www.fda.gov")
                .build())
            .build();

        ResponseCreateParams params = ResponseCreateParams.builder()
            .model("gpt-5.5")
            .input("Please perform a web search on how semaglutide is used in the treatment of diabetes.")
            .addTool(webSearchTool)
            .toolChoice(ResponseCreateParams.ToolChoice.ofOptions(
                ResponseCreateParams.ToolChoiceOptions.AUTO))
            .include(List.of(ResponseIncludable.WEB_SEARCH_CALL_ACTION_SOURCES))
            .build();

        Response response = openAIClient.responses().create(params);
        response.output().forEach(item -> item.message().ifPresent(msg ->
            msg.content().forEach(content -> content.outputText().ifPresent(
                t -> System.out.println(t.text())))));
    }
}
```

# [REST](#tab/rest)

```bash
curl -X POST https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/responses \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AZURE_OPENAI_AUTH_TOKEN" \
  -d '{
    "model": "gpt-5.5",
    "reasoning": { "effort": "low" },
    "tools": [
      {
        "type": "web_search",
        "filters": {
          "allowed_domains": [
            "pubmed.ncbi.nlm.nih.gov",
            "clinicaltrials.gov",
            "www.who.int",
            "www.cdc.gov",
            "www.fda.gov"
          ]
        }
      }
    ],
    "tool_choice": "auto",
    "include": ["web_search_call.action.sources"],
    "input": "Please perform a web search on how semaglutide is used in the treatment of diabetes."
  }'
```

---

To use API key authentication, replace the Microsoft Entra credential with your API key as shown in the [basic example](#how-it-works).

### Limitations

- Live internet access isn't supported. Azure OpenAI always treats the `external_web_access` parameter as `false`, even though the OpenAI default is `true`.
- The domain allowlist supports up to 100 URLs.
- Web search call actions incur tool call costs. For more information, see [pricing](https://www.microsoft.com/bing/apis/grounding-pricing).
- The preview version of the web search tool (`web_search_preview`) is supported but not recommended.
- The `open_page` and `find_in_page` actions are available only with reasoning models.

## Manage web search tool

You can enable or disable the `web_search` tool in the Responses API at the subscription level by using Azure CLI. This setting applies to all accounts within the specified subscription.

### Prerequisites

Before running the following commands, make sure you have the following prerequisites:

- [Azure CLI](/cli/azure/install-azure-cli) installed.
- You're signed in to Azure by using `az login`.
- You have **Owner** or **Contributor** access to the subscription.

### Disable web search

To disable the `web_search` tool for all accounts in a subscription:

```bash
az feature register --name OpenAI.BlockedTools.web_search --namespace Microsoft.CognitiveServices --subscription "<subscription-id>"
```

This command disables web search across all accounts in the specified subscription.

### Enable web search

To enable the `web_search` tool:

```bash
az feature unregister --name OpenAI.BlockedTools.web_search --namespace Microsoft.CognitiveServices --subscription "<subscription-id>"
```

This command enables Bing web search functionality for all accounts in the subscription.

## Troubleshooting

- **No citations returned**: Confirm your request includes `tools: [{"type": "web_search"}]`. If the model doesn't call the tool, prompt more explicitly to browse the web or ask for citations.
- **Tool is blocked**: Ask your subscription admin to verify the subscription feature setting for blocked tools. See [Manage web search tool](#manage-web-search-tool).
- **Authentication errors**: For API keys, verify you set `AZURE_OPENAI_API_KEY`. For Microsoft Entra ID, verify your token scope is `https://ai.azure.com/.default`.