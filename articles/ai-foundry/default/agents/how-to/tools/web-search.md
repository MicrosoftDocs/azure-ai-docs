---
title: Use web search tool in Foundry Agent Service
titleSuffix: Microsoft Foundry
description: Learn how to use the web search tool in Foundry Agent Service to retrieve real-time information and ground AI responses. Get code examples for Python, C#, JavaScript, and REST API.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.date: 01/20/2026
author: alvinashcraft
ms.author: aashcraft
ms.custom: 
    - azure-ai-agents
    - references_regions
    - dev-focus
    - pilot-ai-workflow-jan-2026
ai-usage: ai-assisted
zone_pivot_groups: selection-web-search
---

# Web search tool (preview)

[!INCLUDE [feature-preview](../../../../includes/feature-preview.md)]

The web search tool in Foundry Agent Service enables models to retrieve and ground responses with real-time information from the public web before generating output. When enabled, the model can return up-to-date answers with inline citations, helping you build agents that provide current, factual information to users.

> [!IMPORTANT]
> - Web Search(preview) uses Grounding with Bing Search and Grounding with Bing Custom Search, which are [First Party Consumption Services](https://www.microsoft.com/licensing/terms/product/Glossary/EAEAS#:%7E:text=First-Party%20Consumption%20Services) governed by these [Grounding with Bing terms of use](https://www.microsoft.com/bing/apis/grounding-legal-enterprise) and the [Microsoft Privacy Statement](https://go.microsoft.com/fwlink/?LinkId=521839&clcid=0x409).
> - The Microsoft [Data Protection Addendum](https://aka.ms/dpa) doesn't apply to data sent to Grounding with Bing Search and Grounding with Bing Custom Search. When you use Grounding with Bing Search and Grounding with Bing Custom Search, data transfers occur outside compliance and geographic boundaries.
> - Use of Grounding with Bing Search and Grounding with Bing Custom Search incurs costs. See [pricing](https://www.microsoft.com/bing/apis/grounding-pricing) for details.
> - See the [management section](#administrator-control-for-the-web-search-tool) for information about how Azure admins can manage access to use of web search.

### Usage support

| Microsoft Foundry support | Python SDK | C# SDK | JavaScript SDK | Java SDK | REST API | Basic agent setup | Standard agent setup |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ✔️ | ✔️ | ✔️ | ✔️ | - | ✔️ | ✔️ | ✔️ |

## Prerequisites

- A [basic or standard agent environment](../../../../agents/environment-setup.md)
- The latest prerelease package. See the [quickstart](../../../../quickstarts/get-started-code.md?view=foundry&preserve-view=true#install-and-authenticate) for details.
- Azure credentials configured for authentication (such as `DefaultAzureCredential`).
- Environment variables configured:
  - `AZURE_AI_PROJECT_ENDPOINT` (or `PROJECT_ENDPOINT`): Your Foundry project endpoint URL.
  - `AZURE_AI_MODEL_DEPLOYMENT_NAME` (or `MODEL_DEPLOYMENT_NAME`): Your model deployment name.

## Code examples

> [!NOTE]
> - See [best practices](../../concepts/tool-best-practice.md) for information on optimizing tool usage.
> - You need the latest prerelease package. See the [quickstart](../../../../quickstarts/get-started-code.md?view=foundry&preserve-view=true#get-ready-to-code) for details.

:::zone pivot="python"
### General Web Search

The following example shows how to set up the AI Project client by using the Azure Identity library for authentication.

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

with project_client:
    agent = project_client.agents.create_version(
        agent_name="MyAgent",
        definition=PromptAgentDefinition(
        model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
            instructions="You are a helpful assistant that can search the web",
            tools=[
          WebSearchPreviewTool(
            user_location=ApproximateLocation(country="GB", city="London", region="London")
          )
            ],
        ),
        description="Agent for web search.",
    )

    print(f"Agent created (id: {agent.id}, name: {agent.name}, version: {agent.version})")

    stream_response = openai_client.responses.create(
        stream=True,
        tool_choice="required",
        input="What is today's date and weather in Seattle?",
        extra_body={"agent": {"name": agent.name, "type": "agent_reference"}},
    )

    for event in stream_response:
        if event.type == "response.created":
            print(f"Follow-up response created with ID: {event.response.id}")
        elif event.type == "response.output_text.delta":
            print(f"Delta: {event.delta}")
        elif event.type == "response.text.done":
            print(f"\nFollow-up response done!")
        elif event.type == "response.output_item.done":
            if event.item.type == "message":
                item = event.item
                if item.content[-1].type == "output_text":
                    text_content = item.content[-1]
                    for annotation in text_content.annotations:
                        if annotation.type == "url_citation":
                            print(f"URL Citation: {annotation.url}")
        elif event.type == "response.completed":
            print(f"\nFollow-up completed!")
            print(f"Full response: {event.response.output_text}")
```
:::zone-end

:::zone pivot="csharp"

### General Web Search

In this example, you use the agent to perform the web search in the given location. The example in this section uses synchronous calls. For an asynchronous example, see the [sample code](https://github.com/Azure/azure-sdk-for-net/blob/feature/ai-foundry/agents-v2/sdk/ai/Azure.AI.Projects.OpenAI/samples/Sample13_WebSearch.md) in the Azure SDK for .NET repository on GitHub.

```csharp
// Create project client and read the environment variables, which will be used in the next steps.
var projectEndpoint = System.Environment.GetEnvironmentVariable("PROJECT_ENDPOINT");
var modelDeploymentName = System.Environment.GetEnvironmentVariable("MODEL_DEPLOYMENT_NAME");
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

**Expected output**

The following is an example of the expected output when running the C# code:

```console
Creating agent with web search tool...
Agent created (id: 12345, name: myAgent, version: 1)
Response: The agent returns a grounded response that includes citations.
Agent deleted
```
:::zone-end

:::zone pivot="rest-api"
### General Web Search

The following example shows how to create a response by using an agent that has the web search tool enabled.

```bash
curl --request POST \
  --url "$FOUNDRY_PROJECT_ENDPOINT/openai/responses?api-version=$API_VERSION" \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "model": "$FOUNDRY_MODEL_DEPLOYMENT_NAME",
    "input": "Tell me about the latest news about AI",
    "tool_choice": "required",
    "tools": [
      {
        "type": "web_search_preview"
      }
    ]
  }'
```

#### Expected output

The following example shows the expected output when using the web search tool via the REST API:

```json
{
  "id": "resp_abc123xyz",
  "object": "response",
  "created_at": 1702345678,
  "status": "completed",
  "output_text": "Here is a grounded response with citations.",
  "output_items": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "Here is a grounded response with citations.",
          "annotations": [
            {
              "type": "url_citation",
              "url": "https://contoso.com/example-source",
              "start_index": 0,
              "end_index": 43
            }
          ]
        }
      ]
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

const projectEndpoint = process.env["AZURE_AI_PROJECT_ENDPOINT"] || "<project endpoint>";
const deploymentName = process.env["MODEL_DEPLOYMENT_NAME"] || "<model deployment name>";

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
Response: The agent returns a grounded response that includes citations.
Cleaning up resources...
Conversation deleted
Agent deleted
Web search sample completed!
```
:::zone-end

## Configure the web search tool

You can configure web search behavior when you create your agent.

### Optional parameters for general web search

- `user_location`: Helps web search return results relevant to a user’s geography. Use an approximate location when you want results localized to a country/region/city.
- `search_context_size`: Controls how much context window space to use for the search. Supported values are `low`, `medium`, and `high`. The default is `medium`.


## Security and privacy considerations

- Treat web search results as untrusted input. Validate and sanitize data before you use it in downstream systems.
- Avoid sending secrets or sensitive personal data in prompts that might be forwarded to external services.
- Review the terms, privacy, and data boundary notes in the preview section of this article before enabling web search in production.

## Troubleshooting

| Issue | Cause | Resolution |
| --- | --- | --- |
| Web search isn't used and no citations appear | Model didn't determine web search was needed | Update your instructions to explicitly allow web search for up-to-date questions, and ask a query that requires current information. |
| Requests fail after enabling web search | Web search is disabled at the subscription level | Ask an admin to enable web search. See [Administrator control for the web search tool](#administrator-control-for-the-web-search-tool). |
| REST requests return authentication errors | Bearer token is missing, expired, or has insufficient permissions | Refresh your token and confirm your access to the project and agent. |
| Search returns outdated information | Web content not recently indexed | Refine your query to explicitly request the most recent information. Results depend on Bing's indexing schedule. |
| No results for specific topics | Query too narrow or content not indexed | Broaden your search query. Some niche topics might have limited web coverage. |
| Rate limiting errors (429) | Too many requests in a short time period | Implement exponential backoff and retry logic. Consider spacing out requests. |
| Inconsistent citation formatting | Response format varies by query type | Standardize citation handling in your application code. Parse both inline and reference-style citations. |
| Tool not available for deployment | Regional or model limitations | Confirm web search is available in your region and with your model deployment. Check [tool best practices](../../concepts/tool-best-practice.md). |

## Administrator control for the web search tool

You can enable or disable the web search tool in Foundry Agent Service at the subscription level by using Azure CLI. This setting applies to all accounts within the specified subscription. 

### Prerequisites 

Before running the following commands, make sure that you:

1. Have [Azure CLI](/cli/azure/install-azure-cli) installed.
1. Are signed in to Azure by using `az login`. 
1. Have Owner or Contributor access to the subscription. 

### Disable Bing Web Search 

To disable the web search tool for all accounts in a subscription, run the following command: 

```azurecli
az feature register \
  --name OpenAI.BlockedTools.web_search \
  --namespace Microsoft.CognitiveServices \
  --subscription "<subscription-id>"
```

This command disables web search across all accounts in the specified subscription. 

### Enable Bing Web Search 

To enable the web search tool, run the following command: 

```azurecli
az feature unregister \
  --name OpenAI.BlockedTools.web_search \
  --namespace Microsoft.CognitiveServices \
  --subscription "<subscription-id>"
```

This command enables web search functionality for all accounts in the subscription. 

## Next steps

> [!div class="nextstepaction"]
> [Review tool best practices](../../concepts/tool-best-practice.md)

> [!div class="nextstepaction"]
> [Set up an agent environment](../../../../agents/environment-setup.md)
