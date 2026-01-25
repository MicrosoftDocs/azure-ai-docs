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

# Web search tool

[!INCLUDE [feature-preview](../../../../includes/feature-preview.md)]

The web search tool in Foundry Agent Service enables models to retrieve and ground responses with real-time information from the public web before generating output. When enabled, the model can return up-to-date answers with inline citations, helping you build agents that provide current, factual information to users.

> [!IMPORTANT]
> - Web Search uses Grounding with Bing Search and Grounding with Bing Custom Search, which are [First Party Consumption Services](https://www.microsoft.com/licensing/terms/product/Glossary/EAEAS#:%7E:text=First-Party%20Consumption%20Services) governed by these [Grounding with Bing terms of use](https://www.microsoft.com/bing/apis/grounding-legal-enterprise) and the [Microsoft Privacy Statement](https://go.microsoft.com/fwlink/?LinkId=521839&clcid=0x409).
> - The Microsoft [Data Protection Addendum](https://aka.ms/dpa) doesn't apply to data sent to Grounding with Bing Search and Grounding with Bing Custom Search. When you use Grounding with Bing Search and Grounding with Bing Custom Search, data transfers occur outside compliance and geographic boundaries.
> - Use of Grounding with Bing Search and Grounding with Bing Custom Search incurs costs. See [pricing](https://www.microsoft.com/bing/apis/grounding-pricing) for details.
> - See the [management section](#administrator-control-for-the-web-search-tool) for information about how Azure admins can manage access to use of web search.

## Availabe Capabilities
| Capability | Description | Use case |
| --- | --- | --- |
| general web search (preview) | Gives agents standard access to Bing's search capabilities. | Scenarios requiring broad knowledge access. |
| web search with pre-defined domains | Allows agents to search within a configurable set of public web domains. You define the parts of the web you want to draw from so users only see relevant results from domains you choose. | Scenarios requiring information management. |


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
Before you begin, make sure you have:
- If you need **web search with pre-defined domains**:
    - Azure RBAC roles:
      - **Contributor** or **Owner** role at the subscription or resource group level to create Bing resources and get resource keys.
      - **Azure AI Project Manager** role to create project connections in Foundry. For more information, see [Role-based access control for Microsoft Foundry](../../../../concepts/rbac-foundry.md?view=foundry&preserve-view=true).
    - A [Grounding with Bing Custom Search resource](https://ms.portal.azure.com/#create/Microsoft.BingGroundingCustomSearch) created and connected to your Foundry project. A paid subscription is required to create a Grounding with Bing Custom Search resource. You also need to create search configurations that store the allowed and/or blocked domains. 


## Code examples

> [!NOTE]
> - See [best practices](../../concepts/tool-best-practice.md) for information on optimizing tool usage.
> - You need the latest prerelease package. See the [quickstart](../../../../quickstarts/get-started-code.md?view=foundry&preserve-view=true#get-ready-to-code) for details.
> for pre-defined domains, Your connection ID should be in the format of `/subscriptions/{{subscriptionID}}/resourceGroups/{{resourceGroupName}}/providers/Microsoft.CognitiveServices/accounts/{{foundryAccountName}}/projects/{{foundryProjectName}}/connections/{{foundryConnectionName}}`.

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
### Web Search with pre-defined domains
```python
import os
from dotenv import load_dotenv

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition, WebSearchTool, WebSearchConfiguration

load_dotenv()

project_client = AIProjectClient(
  endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

openai_client = project_client.get_openai_client()

with project_client: 
    bing_connection = project_client.connections.get(os.environ["BING_CUSTOM_SEARCH_CONNECTION_NAME"])
    connection_id = bing_connection.id

    agent = project_client.agents.create_version(
        agent_name="MyAgent",
        definition=PromptAgentDefinition(
        model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
            instructions="You are a helpful assistant that can search the web",
            tools=[
                WebSearchTool(
                    web_search_configuration=[
                        WebSearchConfiguration(
                            project_connection_id=connection_id,
                            instance_name=os.environ["BING_CUSTOM_SEARCH_INSTANCE_NAME"],
                        )
                    ]
                )
    )
    ],
        ),
        description="Agent for web search.",
    )

    print(f"Agent created (id: {agent.id}, name: {agent.name}, version: {agent.version})")

    stream_response = openai_client.responses.create(
        stream=True,
        tool_choice="required",
        input="QUESTION_FOR_YOUR_DOMAINS",
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
### Web Search with predefined domains

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
          "type": "web_search",
          "web_search": {
            "web_search_configurations": [
              {
                "project_connection_id": "$BING_CUSTOM_SEARCH_PROJECT_CONNECTION_ID",
                "instance_name": "$BING_CUSTOM_SEARCH_INSTANCE_NAME",
              }
            ]
          }
        }
  ]
  }'
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

### Configure web search with pre-defined domains
After you have created a Grounding with Bing Custom Search resource, you can then create a search configuration and add allowed and/or blocked domains. Here are a few tips to help you take full advantage of this capability: 

- If you own a public site that you want to include in the search but Bing hasn't indexed, see the [Bing Webmaster Guidelines](https://www.bing.com/webmasters/help/webmasters-guidelines-30fba23a) for details about getting your site indexed. The webmaster documentation also provides details about getting Bing to crawl your site if the index is out of date. 
- You need at least the contributor role for the Bing Custom Search resource to create a configuration.
- You can only block certain domains and perform a search against the rest of the web (a competitor's site, for example). 
- Grounding with Bing Custom Search only returns results for domains and webpages that are public and indexed by Bing. 
  - Domain (for example, `https://www.microsoft.com`) 
  - Domain and path (for example, `https://www.microsoft.com/surface`) 
  - Webpage (for example, `https://www.microsoft.com/en-us/p/surface-earbuds/8r9cpq146064`) 


## Security and privacy considerations

- Treat web search results as untrusted input. Validate and sanitize data before you use it in downstream systems.
- Avoid sending secrets or sensitive personal data in prompts that might be forwarded to external services.
- Review the terms, privacy, and data boundary notes in the preview section of this article before enabling web search in production.

## Troubleshooting

| Issue | Cause | Resolution |
| --- | --- | --- |
| Web search isn’t used and no citations appear | The model didn’t determine that web search was needed, or the prompt didn’t request current information | Update your instructions to explicitly allow web search for up-to-date questions, and ask a query that requires current information. |
| Requests fail after enabling web search | Web search is disabled at the subscription level | Ask an admin to enable web search. See [Administrator control for the web search tool](#administrator-control-for-the-web-search-tool). |
| REST requests return authentication errors | The bearer token is missing, expired, or has insufficient permissions | Refresh your token and confirm your access to the project and agent. |
|Instance name not found for Grounding with Bing Custom Search|The instance name you provided doesn't exist in the Grounding with Bing Custom Search resource | Ensure your instance name is in the Grounding with Bing Custom Search resource you are using. Double check if your instance name is spelled correctly.|

## Administrator control for the web search tool

You can enable or disable the web search tool in Foundry Agent Service at the subscription level by using Azure CLI. This setting applies to all accounts within the specified subscription. 

### Prerequisites 

Before running the following commands, make sure that you:

1. Have [Azure CLI](/cli/azure/install-azure-cli) installed.
1. Are signed in to Azure by using `az login`. 
1. Have Owner or Contributor access to the subscription. 

### Disable Web Search 

To disable the web search tool for all accounts in a subscription, run the following command: 

```azurecli
az feature register \
  --name OpenAI.BlockedTools.web_search \
  --namespace Microsoft.CognitiveServices \
  --subscription "<subscription-id>"
```

This command disables web search across all accounts in the specified subscription. 

### Enable Web Search 

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
