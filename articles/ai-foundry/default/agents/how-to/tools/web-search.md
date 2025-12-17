---
title: Use web search tool in Foundry Agent Service
titleSuffix: Microsoft Foundry
description: Learn how to use the web search tool in Foundry Agent Service to retrieve real-time information and ground AI responses. Get code examples for Python, C#, JavaScript, and REST API.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.date: 12/17/2025
author: alvinashcraft
ms.author: aashcraft
ms.custom: azure-ai-agents, references_regions, dev-focus
ai-usage: ai-assisted
zone_pivot_groups: selection-web-search
---

# Web search tool (preview)

[!INCLUDE [feature-preview](../../../../includes/feature-preview.md)]

The web search tool in Foundry Agent Service enables models to retrieve and ground responses with real-time information from the public web before generating output. When enabled, the model can return up-to-date answers with inline citations, helping you build agents that provide current, factual information to users.

> [!IMPORTANT]
> - Web Search (preview) uses Grounding with Bing Search and Grounding with Bing Custom Search, which are [First Party Consumption Services](https://www.microsoft.com/licensing/terms/product/Glossary/EAEAS#:%7E:text=First-Party%20Consumption%20Services) governed by these [Grounding with Bing terms of use](https://www.microsoft.com/en-us/bing/apis/grounding-legal-enterprise) and the [Microsoft Privacy Statement](https://go.microsoft.com/fwlink/?LinkId=521839&clcid=0x409).
> - The Microsoft [Data Protection Addendum](https://aka.ms/dpa) doesn't apply to data sent to Grounding with Bing Search and Grounding with Bing Custom Search. When you use Grounding with Bing Search and Grounding with Bing Custom Search, data transfers occur outside compliance and geographic boundaries.
> - Use of Grounding with Bing Search and Grounding with Bing Custom Search incurs costs. See [pricing](https://www.microsoft.com/bing/apis/grounding-pricing) for details.
> - See the [management section](#administrator-control-for-the-web-search-tool) for information about how Azure admins can manage access to use of web search.

### Usage support

| Microsoft Foundry support | Python SDK | C# SDK | JavaScript SDK | Java SDK | REST API | Basic agent setup | Standard agent setup |
|---------|---------|---------|---------|---------|---------|---------|---------|
| ✔️ | ✔️ | ✔️ | ✔️ | - | ✔️ | ✔️ | ✔️ |

## Code examples

> [!NOTE]
> See [best practices](../../concepts/tool-best-practice.md) for information on optimizing tool usage.

:::zone pivot="python"
### Set up the AI Project client

The following example shows how to set up the AI Project client by using the Azure Identity library for authentication.

```python
import os
from dotenv import load_dotenv

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition, WebSearchPreviewTool, ApproximateLocation

load_dotenv()

project_client = AIProjectClient(
    endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

openai_client = project_client.get_openai_client()
```

### Create an agent with the web search tool

The following example shows how to create an agent version that uses the web search tool.

```python
from azure.ai.projects.models import PromptAgentDefinition, WebSearchPreviewTool, ApproximateLocation

agent = project_client.agents.create_version(
    agent_name="MyAgent",
    definition=PromptAgentDefinition(
        model=os.environ["FOUNDRY_MODEL_DEPLOYMENT_NAME"],
        instructions="You are a helpful assistant that can search the web",
        tools=[
            WebSearchPreviewTool()
        ],
    ),
    description="Agent for web search.",
)
```

### Expected output

The following is an example of the expected output when creating an agent with the web search tool:

```console
Agent created (id: 12345, name: MyAgent, version: 1)
```
:::zone-end

:::zone pivot="csharp"

In this example, you use the agent to perform the web search in the given location. The example in this section uses synchronous calls. For an asynchronous example, see the [sample code](https://github.com/Azure/azure-sdk-for-net/blob/feature/ai-foundry/agents-v2/sdk/ai/Azure.AI.Projects.OpenAI/samples/Sample13_WebSearch.md) in the Azure SDK for .NET repository on GitHub.

```csharp
// Create project client and read the environment variables, which will be used in the next steps.
var projectEndpoint = System.Environment.GetEnvironmentVariable("FOUNDRY_PROJECT_ENDPOINT");
var modelDeploymentName = System.Environment.GetEnvironmentVariable("FOUNDRY_MODEL_DEPLOYMENT_NAME");
AIProjectClient projectClient = new(endpoint: new Uri(projectEndpoint), tokenProvider: new DefaultAzureCredential());

// Create an agent capable of using Web search and set the location to "London" in the WebSearchToolLocation.
PromptAgentDefinition agentDefinition = new(model: modelDeploymentName)
{
    Instructions = "You are a helpful assistant that can search the web",
    Tools = {
        ResponseTool.CreateWebSearchTool(userLocation: WebSearchToolLocation.CreateApproximateLocation(
            country: "GB",
            city: "London",
            region: "London"
            )
        ),
    }
};
AgentVersion agentVersion = projectClient.Agents.CreateAgentVersion(
    agentName: "myAgent",
    options: new(agentDefinition));

// Ask a question related to London.
ProjectResponsesClient responseClient = projectClient.OpenAI.GetProjectResponsesClientForAgent(agentVersion.Name);

ResponseResult response = responseClient.CreateResponse("Show me the latest London Underground service updates");

// Create the response and throw an exception if the response contains an error.
Assert.That(response.Status, Is.EqualTo(ResponseStatus.Completed));
Console.WriteLine(response.GetOutputText());

// Delete the created agent version.
projectClient.Agents.DeleteAgentVersion(agentName: agentVersion.Name, agentVersion: agentVersion.Version);
```

## Expected output

The following is an example of the expected output when running the C# code:

```console
Creating agent with web search tool...
Agent created (id: 12345, name: myAgent, version: 1)
Response: The latest London Underground service updates are as follows: [1] "The London Underground is currently experiencing delays on the Central Line due to signal failure. [2] "Planned engineering works are scheduled for the Jubilee Line this weekend." For more details, visit https://tfl.gov.uk.uk/modes/tube/status/
Agent deleted
```
:::zone-end

:::zone pivot="rest-api"
### Create an agent with the web search tool

The following example shows how to create an agent version that uses the web search tool via the REST API.

```bash
curl --request POST \
  --url $FOUNDRY_PROJECT_ENDPOINT/agents/$AGENTVERSION_NAME/versions?api-version=$API_VERSION \
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

### Create a response by using the web search tool

The following example shows how to create a response by using the web search tool via the REST API.

```bash
curl --request POST \
  --url $FOUNDRY_PROJECT_ENDPOINT/openai/responses?api-version=$API_VERSION \
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

### Expected output

The following example shows the expected output when using the web search tool via the REST API:

```json
{
  "id": "response-id",
  "object": "response",
  "created": 1697059200,
  "model": "gpt-5",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": [
          {
            "type": "output_text",
            "text": "The weather in Seattle today is mostly cloudy with a high of 65°F (18°C) and a low of 50°F (10°C). There is a chance of light rain in the afternoon. For more details, you can check [source](https://www.weather.com/weather/today/l/Seattle+WA)."
          }
        ]
      },
      "finish_reason": "stop"
    }
  ]
}
```
:::zone-end

:::zone pivot="typescript"
## Use the web search tool with TypeScript

The following TypeScript example demonstrates how to create an agent with the web search tool. For an example that uses JavaScript, see the [sample code](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/ai/ai-projects/samples/v2-beta/javascript/agents/tools/agentWebSearch.js) example in the Azure SDK for JavaScript repository on GitHub.

```typescript
import { DefaultAzureCredential } from "@azure/identity";
import { AIProjectClient } from "@azure/ai-projects";
import "dotenv/config";

const projectEndpoint = process.env["FOUNDRY_PROJECT_ENDPOINT"] || "<project endpoint>";
const deploymentName = process.env["FOUNDRY_MODEL_DEPLOYMENT_NAME"] || "<model deployment name>";

export async function main(): Promise<void> {
  // Create AI Project client
  const project = new AIProjectClient(projectEndpoint, new DefaultAzureCredential());
  const openAIClient = await project.getOpenAIClient();

  console.log("Creating agent with web search tool...");

  // Create Agent with web search tool
  const agent = await project.agents.createVersion("agent-web-search", {
    kind: "prompt",
    model: deploymentName,
    instructions: "You are a helpful assistant that can search the web",
    tools: [
      {
        type: "web_search_preview",
        user_location: {
          type: "approximate",
          country: "GB",
          city: "London",
          region: "London",
        },
      },
    ],
  });
  console.log(`Agent created (id: ${agent.id}, name: ${agent.name}, version: ${agent.version})`);

  // Create a conversation for the agent interaction
  const conversation = await openAIClient.conversations.create();
  console.log(`Created conversation (id: ${conversation.id})`);

  // Send a query to search the web
  console.log("\nSending web search query...");
  const response = await openAIClient.responses.create(
    {
      conversation: conversation.id,
      input: "Show me the latest London Underground service updates",
    },
    {
      body: { agent: { name: agent.name, type: "agent_reference" } },
    },
  );
  console.log(`Response: ${response.output_text}`);

  // Clean up resources
  console.log("\nCleaning up resources...");
  await openAIClient.conversations.delete(conversation.id);
  console.log("Conversation deleted");

  await project.agents.deleteVersion(agent.name, agent.version);
  console.log("Agent deleted");

  console.log("\nWeb search sample completed!");
}

main().catch((err) => {
  console.error("The sample encountered an error:", err);
});
```

### Expected output

The following example shows the expected output when running the TypeScript code:

```console
Creating agent with web search tool...
Agent created (id: 12345, name: agent-web-search, version: 1)
Created conversation (id: 67890)
Sending web search query...
Response: The latest London Underground service updates are as follows: [1] "The London Underground is currently experiencing delays on the Central Line due to signal failure. [2] "Planned engineering works are scheduled for the Jubilee Line this weekend." For more details, visit https://tfl.gov.uk.uk/modes/tube/status/
Cleaning up resources...
Conversation deleted
Agent deleted
Web search sample completed!
```
:::zone-end

## Options for using the web search tool

Web search supports two primary modes. Choose the mode based on the depth and speed you need. 

- Non reasoning web search
   - The model forwards the user query directly to the web search tool and uses top-ranked sources to ground the response. There's no multistep planning. This mode is fast and best for quick lookups and timely facts.
- Reasoning web search
   - Use reasoning models like `gpt-5` to actively manage the search process. It uses web search results as part of the chain of thoughts.
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

Before running the following commands, make sure that you:

1. Have [Azure CLI](/cli/azure/install-azure-cli) installed.
1. Are signed in to Azure by using `az login`. 
1. Have Owner or Contributor access to the subscription. 

### Disable Bing Web Search 

To disable the web search tool for all accounts in a subscription, run the following command: 

`az feature register --name OpenAI.BlockedTools.web_search --namespace Microsoft.CognitiveServices --subscription "<subscription-id>" `

This command disables web search across all accounts in the specified subscription. 

### Enable Bing Web Search 

To enable the web search tool, run the following command: 

`az feature unregister --name OpenAI.BlockedTools.web_search --namespace Microsoft.CognitiveServices --subscription "<subscription-id>"` 

This command enables web search functionality for all accounts in the subscription. 
