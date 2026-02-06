---
title: Web search with the Responses API
description: Learn how to use Web search with the Responses API
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: how-to
ms.date: 11/10/2025
author: mrbullwinkle    
ms.author: mbullwin
monikerRange: 'foundry-classic || foundry'
---

# Web search (preview)

Web search enables models to retrieve and ground responses with real-time information from the public web before generating output. When enabled, the model can return up-to-date answers with inline citations. Web search is available via the `web_search_preview` tool in the **Responses API**.

> [!NOTE]
> Some SDKs may expose both `web_search_preview` and `web_search` tool types.
> Only `web_search_preview` is currently supported for Web search in the Azure OpenAI Responses API.
> The `web_search` tool type is not supported at this time and should not be used.

> [!IMPORTANT]
> * Web Search (preview) uses Grounding with Bing Search and/or Grounding with Bing Custom Search, which are [First Party Consumption Services](https://www.microsoft.com/licensing/terms/product/ForOnlineServices/EAEAS) governed by these [Grounding with Bing terms of use](https://www.microsoft.com/bing/apis/grounding-legal-enterprise) and the [Microsoft Privacy Statement](https://go.microsoft.com/fwlink/?LinkId=521839&clcid=0x409).
> * The Microsoft [Data Protection Addendum](https://aka.ms/dpa) does not apply to data sent to Grounding with Bing Search and/or Grounding with Bing Custom Search. When Customer uses Grounding with Bing Search and/or Grounding with Bing Custom Search, Customer Data will flow outside Customer’s compliance and Geo boundary.
> * Use of Grounding with Bing Search and Grounding with Bing Custom Search will incur costs; learn more about [pricing](https://www.microsoft.com/bing/apis/grounding-pricing).
> * [Learn more](/azure/ai-foundry/openai/how-to/web-search?view=foundry-classic#manage-web-search-preview-tool) about how Azure admins can manage access to the use of Web Search (preview).

## Options to use web search

Web search supports three modes. Choose the mode based on the depth and speed you need.

### Web search without reasoning 

The model forwards the user query directly to the web search tool and uses top-ranked sources to ground the response. There's no multi-step planning. This mode is **fast** and best for quick lookups and timely facts.

### Agentic search with reasoning models

The model actively manages the search process and can perform web searches as part of its chain of thought, analyze results, and decide whether to keep searching. This flexibility makes agentic search well **suited for complex workflows**, but it also means searches take **longer** than quick lookups.

### Deep research

Deep Research is an agent-driven mode designed for **extended investigations**. The model performs multi-step reasoning, may open and read many pages, and synthesizes findings into a comprehensive, citation-rich response. Use this mode with `o3-deep-research` when you need:

* Legal or scientific research
* Market and competitive analysis
* Reporting over large bodies of internal or public data

Deep Research can run for several minutes and is best for background-style workloads that prioritize completeness over speed.

## How it works

You use web search by declaring the tool in your request. The model may decide whether to call the tool based on the user’s prompt and your configuration.

> [!NOTE]
> Web Search in the Responses API works with GPT-4 models and later.

### Use web search with a non-reasoning model

**REST API - Entra ID**

```bash
curl -X POST https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/responses \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AZURE_OPENAI_AUTH_TOKEN" \
  -d '{
     "model": "gpt-4.1",
     "tools": [{"type": "web_search_preview"}],
     "input": "Please perform a web search on the latest trends in renewable energy"
    }'
```

**REST API - Key**

```bash
curl -X POST https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/responses \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
  -d '{
     "model": "gpt-4.1",
     "tools": [{"type": "web_search_preview"}],
     "input": "Please perform a web search on the latest trends in renewable energy"
    }'
```

**Python - API Key**

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
)

response = client.responses.create(   
  model="gpt-4.1", # Replace with your model deployment name
  tools=[{"type": "web_search_preview"}], 
  input="Please perform a web search on the latest trends in renewable energy"
)

print(response.output_text)
```

**Python - Entra ID**

```python
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

client = AzureOpenAI(  
  base_url = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",  
  azure_ad_token_provider=token_provider,
  api_version="latest"
)

response = client.responses.create(   
  model="gpt-4.1", # Replace with your model deployment name
  tools=[{"type": "web_search_preview"}], 
  input="Please perform a web search on the latest trends in renewable energy"
)

print(response.output_text) 
```

### Response shape

A successful response that used web search typically contains two parts:

* A `web_search_call` output item that records the action performed:
  * `search`: a web search action, including the query (and optionally the searched domains). **Search actions incur tool call costs** (see [pricing](https://www.microsoft.com/bing/apis/grounding-pricing)).
  * `open_page`: (Deep Research only) indicates the agent opened a page.
  * `find_in_page`: (Deep Research only) indicates the agent searched within an opened page.
* A message output item containing:
  * The grounded text in `message.content[0].text`
  * URL citations in `message.content[0].annotations`, one or more `url_citation` objects that include the URL, title, and character ranges

#### Example

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

### Control results by user location

You can refine search results by specifying a country/region code.

- `country`: a two-letter [ISO country/region code](https://en.wikipedia.org/wiki/ISO_3166-1) (for example, US).

**REST API - Entra ID**

```bash
curl -X POST https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/responses \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AZURE_OPENAI_AUTH_TOKEN" \
  -d '{
    "model": "gpt-4.1",
    "tools": [
        {
            "type": "web_search_preview",
            "user_location": {
                "type": "approximate",
                "country": "IN"
            }
        }
    ],
    "input": "Give me a positive news story from the web today"
    }'
```

**REST API - Key**

```bash
curl -X POST https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/responses \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
  -d '{
     "model": "gpt-4.1",
     "tools": [
        {
            "type": "web_search_preview",
            "user_location": {
                "type": "approximate",
                "country": "IN"
            }
        }
    ],
    "input": "Give me a positive news story from the web today"
    }'
```

**Python - API Key**

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
)

response = client.responses.create(   
  model="gpt-4.1", # Replace with your model deployment name
  tools= [
        {
            "type": "web_search_preview",
            "user_location": {
                "type": "approximate",
                "country": "IN"
            }
        }
    ],
    input="Give me a positive news story from the web today"
)

print(response.output_text)
```

**Python - Entra ID**

```python
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

client = AzureOpenAI(  
  base_url = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",  
  azure_ad_token_provider=token_provider,
  api_version="latest"
)

response = client.responses.create(   
  model="gpt-4.1", # Replace with your model deployment name
  tools= [
        {
            "type": "web_search_preview",
            "user_location": {
                "type": "approximate",
                "country": "IN"
            }
        }
    ],
    input="Give me a positive news story from the web today"
)

print(response.output_text) 
```

### Use with the deep research model

Set the model to `o3-deep-research` to perform multi-step research across many sources. You must include at least one data source (for example, web search or a remote Model Context Protocol (MCP) server). You can also include the **code interpreter** tool to allow the model to write and run code for analysis.

Because Deep Research may execute many browsing steps, requests can take longer and may incur multiple tool calls. For long-running analyses, consider using background execution patterns in your application.

**REST API - Entra ID**

```bash
curl -X POST https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/responses \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AZURE_OPENAI_AUTH_TOKEN" \
  -d '{
     "model": "o3-deep-research",
     "tools": [
                {"type": "web_search_preview"},
                { "type": "code_interpreter", "container": { "type": "auto" }}
              ],
     "input": "Research the economic impact of semaglutide on global healthcare systems. Include specific figures, trends, statistics, and measurable outcomes. Prioritize reliable, up-to-date sources: peer-reviewed research, health organizations (e.g., WHO, CDC), regulatory agencies, or pharmaceutical earnings reports. Include inline citations and return all source metadata. Be analytical, avoid generalities, and ensure that each section supports data-backed reasoning that could inform healthcare policy or financial modeling."
    }'
```

**REST API - Key**

```bash
curl -X POST https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/responses \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
  -d '{
     "model": "o3-deep-research",
     "tools": [
                {"type": "web_search_preview"},
                { "type": "code_interpreter", "container": { "type": "auto" }}
              ],
     "input": "Research the economic impact of semaglutide on global healthcare systems. Include specific figures, trends, statistics, and measurable outcomes. Prioritize reliable, up-to-date sources: peer-reviewed research, health organizations (e.g., WHO, CDC), regulatory agencies, or pharmaceutical earnings reports. Include inline citations and return all source metadata. Be analytical, avoid generalities, and ensure that each section supports data-backed reasoning that could inform healthcare policy or financial modeling."
    }'
```

**Python - API Key**

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
)

response = client.responses.create(   
  model="o3-deep-research", # Replace with your model deployment name
  tools=[
            {"type": "web_search_preview"},
            { "type": "code_interpreter", "container": { "type": "auto" }}
        ], 
  input="Research the economic impact of semaglutide on global healthcare systems. Include specific figures, trends, statistics, and measurable outcomes. Prioritize reliable, up-to-date sources: peer-reviewed research, health organizations (e.g., WHO, CDC), regulatory agencies, or pharmaceutical earnings reports. Include inline citations and return all source metadata. Be analytical, avoid generalities, and ensure that each section supports data-backed reasoning that could inform healthcare policy or financial modeling."
)

print(response.output_text)
```

**Python - Entra ID**

```python
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

client = AzureOpenAI(  
  base_url = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",  
  azure_ad_token_provider=token_provider,
  api_version="latest"
)

response = client.responses.create(   
  model="o3-deep-research", # Replace with your model deployment name
  tools=[
            {"type": "web_search_preview"},
            { "type": "code_interpreter", "container": { "type": "auto" }}
        ], 
  input="Research the economic impact of semaglutide on global healthcare systems. Include specific figures, trends, statistics, and measurable outcomes. Prioritize reliable, up-to-date sources: peer-reviewed research, health organizations (e.g., WHO, CDC), regulatory agencies, or pharmaceutical earnings reports. Include inline citations and return all source metadata. Be analytical, avoid generalities, and ensure that each section supports data-backed reasoning that could inform healthcare policy or financial modeling."
)

print(response.output_text)
```

## Manage web search preview tool

You can enable or disable the `web_search_preview` tool in the Responses API at the subscription level using Azure CLI. This setting applies to all accounts within the specified subscription.

### Prerequisites

Before running the commands below, ensure the following:

* [Azure CLI](/cli/azure/install-azure-cli) is installed. 
* You're signed in to Azure using `az login`
* You have **Owner** or **Contributor** access to the subscription

### Disable web search preview

To disable the `web_search_preview` tool for all accounts in a subscription:

```bash
az feature register --name OpenAI.BlockedTools.web_search --namespace Microsoft.CognitiveServices --subscription "<subscription-id>"
```

This command disables web search across all accounts in the specified subscription.

### Enable web search preview

To enable the `web_search_preview` tool:

```bash
az feature unregister --name OpenAI.BlockedTools.web_search --namespace Microsoft.CognitiveServices --subscription "<subscription-id>"
```

This command enables Bing web search functionality for all accounts in the subscription.
