---
title: Use Foundry Agent Service Web Search
titleSuffix: Microsoft Foundry
description: Learn how to use the web search tool in Foundry Agent Service to retrieve real-time information and ground responses with up-to-date web data.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.date: 12/08/2025
author: alvinashcraft
ms.author: aashcraft
ms.custom: azure-ai-agents, references_regions
zone_pivot_groups: selection-web-search
---

# Web search tool (preview)

[!INCLUDE [feature-preview](../../../../includes/feature-preview.md)]

Web search enables models to retrieve and ground responses with real-time information from the public web before generating output. When enabled, the model can return up-to-date answers with inline citations.

> [!IMPORTANT]
> - Web Search (preview) uses Grounding with Bing Search and Grounding with Bing Custom Search, which are [First Party Consumption Services](https://www.microsoft.com/licensing/terms/product/Glossary/EAEAS#:%7E:text=First-Party%20Consumption%20Services) governed by these [Grounding with Bing terms of use](https://www.microsoft.com/en-us/bing/apis/grounding-legal-enterprise) and the [Microsoft Privacy Statement](https://go.microsoft.com/fwlink/?LinkId=521839&clcid=0x409).
> - The Microsoft [Data Protection Addendum](https://aka.ms/dpa) doesn't apply to data sent to Grounding with Bing Search and Grounding with Bing Custom Search. When you use Grounding with Bing Search and Grounding with Bing Custom Search, data transfers occur outside compliance and geographic boundaries.
> - Use of Grounding with Bing Search and Grounding with Bing Custom Search incurs costs. See [pricing](https://www.microsoft.com/bing/apis/grounding-pricing) for details.
> - See the [management section](#admin-control-for-web-search-tool) for information about how Azure admins can manage access to use of web search.

:::zone pivot="python"
> [!NOTE]
> See [best practices](../../concepts/tool-best-practice.md) for information on optimizing tool usage.

```python
import os
from dotenv import load_dotenv

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition, WebSearchPreviewTool, ApproximateLocation

load_dotenv()

project_client = AIProjectClient(
    endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

openai_client = project_client.get_openai_client()
```
### Create an agent with the web search tool

```python
from azure.ai.projects.models import PromptAgentDefinition, WebSearchPreviewTool, ApproximateLocation

agent = project_client.agents.create_version(
    agent_name="MyAgent",
    definition=PromptAgentDefinition(
        model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
        instructions="You are a helpful assistant that can search the web",
        tools=[
            WebSearchPreviewTool()
        ],
    ),
    description="Agent for web search.",
)
```
:::zone-end

:::zone pivot="csharp"

For C# usage, see the [Sample web search with agent in Azure.AI.Projects.OpenAI](https://github.com/Azure/azure-sdk-for-net/blob/feature/ai-foundry/agents-v2/sdk/ai/Azure.AI.Projects.OpenAI/samples/Sample13_WebSearch.md) example in the Azure SDK for .NET repository on GitHub.

:::zone-end

:::zone pivot="rest-api"

### Create an agent with the web search tool
```bash
curl --request POST \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/agents/$AGENTVERSION_NAME/versions?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{
  "description": "Test agent version description",
  "definition": {
    "kind": "prompt",
    "model": "{{model}}",
    "tools": [
      {
        "type": "web_search_preview"
      }
    ],
    "instructions": "You are a helpful assistant that can search the web for current information. When users ask questions that require up-to-date information, use the web search tool to find relevant results."
  }
}'
```
### Create a response with the web search tool
```bash
curl --request POST \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/openai/responses?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
  "agent": {
    "type": "agent_reference",
    "name": "{{agentVersion.name}}",
    "version": "{{agentVersion.version}}"
  },
  "input": [{
    "type": "message",
    "role": "user",
    "content": [
      {
        "type": "input_text",
        "text": "how is the weather in seattle today?"
      }
    ]
  }],
  "stream": true
}'
```
:::zone-end


## Options for using web search

Web search supports two primary modes. Choose the mode based on the depth and speed you need. 

- Non reasoning web search
   - The model forwards the user query directly to the web search tool and uses top-ranked sources to ground the response. There's no multistep planning. This mode is fast and best for quick lookups and timely facts.
- Reasoning web search
   - You can use the reasoning models like `gpt-5` to actively manage the search process. It uses web search results as part of the chain of thoughts.
- Deep Research
   - Deep Research is an agent-driven mode designed for extended investigations. The model performs multistep reasoning, might open and read many pages, and synthesizes findings into a comprehensive, citation-rich response. Use this mode with `o3-deep-research` when you need:
      - Legal or scientific research
      - Market and competitive analysis
      - Reporting over large bodies of internal or public data 

Deep Research can run for several minutes and is best for background-style workloads that prioritize completeness over speed.

> [!NOTE]
> You can only use file upload with a basic agent setup. With a standard agent setup you can use file upload or bring your own blob storage.

## Administrator control for the web search tool

You can enable or disable the web search tool in Foundry Agent Service at the subscription level by using Azure CLI. This setting applies to all accounts within the specified subscription. 

### Prerequisites 

Before running the following commands, ensure that you:

1. Have [Azure CLI](/cli/azure/install-azure-cli) installed.
1. Are signed in to Azure using `az login`. 
1. Have Owner or Contributor access to the subscription. 

### Disable Bing Web Search 

To disable the web search tool for all accounts in a subscription, run the following command: 

`az feature register --name OpenAI.BlockedTools.web_search --namespace Microsoft.CognitiveServices --subscription "<subscription-id>" `

This command disables web search across all accounts in the specified subscription. 

### Enable Bing Web Search 

To enable the web search tool, run the following command: 

`az feature unregister --name OpenAI.BlockedTools.web_search --namespace Microsoft.CognitiveServices --subscription "<subscription-id>"` 

This command enables web search functionality for all accounts in the subscription. 
