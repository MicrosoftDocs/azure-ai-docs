---
title: "Use web search tool in Foundry Agent Service"
description: "Use the web search tool in Foundry Agent Service to retrieve real-time information and ground AI responses. Includes code examples."
services: cognitive-services
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.date: 03/30/2026
author: alvinashcraft
ms.author: aashcraft
ms.custom: 
    - azure-ai-agents
    - references_regions
    - dev-focus
    - pilot-ai-workflow-jan-2026
    - doc-kit-assisted
ai-usage: ai-assisted
zone_pivot_groups: selection-web-search
---

# Web search tool

The web search tool in Foundry Agent Service enables models to retrieve and ground responses with real-time information from the public web before generating output. When enabled, the model can return up-to-date answers with inline citations, helping you build agents that provide current, factual information to users.

> [!IMPORTANT]
> - Web Search uses Grounding with Bing Search and Grounding with Bing Custom Search, which are [First Party Consumption Services](https://www.microsoft.com/licensing/terms/product/Glossary/EAEAS#:%7E:text=First-Party%20Consumption%20Services) governed by these [Grounding with Bing terms of use](https://www.microsoft.com/bing/apis/grounding-legal-enterprise) and the [Microsoft Privacy Statement](https://go.microsoft.com/fwlink/?LinkId=521839&clcid=0x409).
> - The Microsoft [Data Protection Addendum](https://aka.ms/dpa) doesn't apply to data sent to Grounding with Bing Search and Grounding with Bing Custom Search. When you use Grounding with Bing Search and Grounding with Bing Custom Search, data transfers occur outside compliance and geographic boundaries.
> - Use of Grounding with Bing Search and Grounding with Bing Custom Search incurs costs. See [pricing](https://www.microsoft.com/bing/apis/grounding-pricing) for details.
> - See the [management section](#administrator-control-for-the-web-search-tool) for information about how Azure admins can manage access to use of web search.

### Usage support

The following table shows SDK and setup support.

| Microsoft Foundry support | Python SDK | C# SDK | JavaScript SDK | Java SDK | REST API | Basic agent setup | Standard agent setup |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |

## Prerequisites

- A [basic or standard agent environment](../../../agents/environment-setup.md)
- The latest SDK package. The .NET SDK is currently in preview. See the [quickstart](../../../quickstarts/get-started-code.md#install-and-authenticate) for details.
- Azure credentials configured for authentication (such as `DefaultAzureCredential`).
- Your Foundry project endpoint URL and a model deployment name.

## Code examples

> [!NOTE]
> See [best practices](../../concepts/tool-best-practice.md) for information on optimizing tool usage.

:::zone pivot="python"
### General Web Search

The following example shows how to set up the AI Project client by using the Azure Identity library for authentication.

```python
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    PromptAgentDefinition,
    WebSearchTool,
    WebSearchApproximateLocation,
)

# Format: "https://resource_name.ai.azure.com/api/projects/project_name"
PROJECT_ENDPOINT = "your_project_endpoint"

# Create clients to call Foundry API
project = AIProjectClient(
    endpoint=PROJECT_ENDPOINT,
    credential=DefaultAzureCredential(),
)
openai = project.get_openai_client()

# Create an agent with the web search tool
agent = project.agents.create_version(
    agent_name="MyAgent",
    definition=PromptAgentDefinition(
        model="gpt-5-mini",
        instructions="You are a helpful assistant that can search the web",
        tools=[
            WebSearchTool(
                user_location=WebSearchApproximateLocation(
                    country="GB", city="London", region="London"
                )
            )
        ],
    ),
    description="Agent for web search.",
)
print(f"Agent created (id: {agent.id}, name: {agent.name}, version: {agent.version})")

# Send a query and stream the response
stream_response = openai.responses.create(
    stream=True,
    tool_choice="required",
    input="What is today's date and weather in Seattle?",
    extra_body={"agent_reference": {"name": agent.name, "type": "agent_reference"}},
)

# Process streaming events
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

project.agents.delete_version(agent_name=agent.name, agent_version=agent.version)
print("Agent deleted")
```

#### Expected output

```output
Agent created: <agent-name> (version 1)
Response: The latest trends in renewable energy include ...
URL Citation: https://example.com/source

Follow-up completed!
Full response: Based on current data ...
Agent deleted
```

### Domain-Restricted Search with Bing Custom Search

The following example shows how to restrict web search to specific domains using a Bing Custom Search instance. This approach gives you control over which websites your agent can search.

```python
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    PromptAgentDefinition,
    WebSearchTool,
    WebSearchConfiguration,
)

# Format: "https://resource_name.ai.azure.com/api/projects/project_name"
PROJECT_ENDPOINT = "your_project_endpoint"
BING_CUSTOM_SEARCH_CONNECTION_ID = "your_bing_custom_search_connection_id"
BING_CUSTOM_SEARCH_INSTANCE_NAME = "your_bing_custom_search_instance_name"

# Create clients to call Foundry API
project = AIProjectClient(
    endpoint=PROJECT_ENDPOINT,
    credential=DefaultAzureCredential(),
)
openai = project.get_openai_client()

# Create an agent with the web search tool and custom search configuration
agent = project.agents.create_version(
    agent_name="MyAgent",
    definition=PromptAgentDefinition(
        model="gpt-5-mini",
        instructions="You are a helpful assistant that can search the web",
        tools=[
            WebSearchTool(
                custom_search_configuration=WebSearchConfiguration(
                    project_connection_id=BING_CUSTOM_SEARCH_CONNECTION_ID,
                    instance_name=BING_CUSTOM_SEARCH_INSTANCE_NAME,
                )
            )
        ],
    ),
    description="Agent for domain-restricted web search.",
)
print(f"Agent created (id: {agent.id}, name: {agent.name}, version: {agent.version})")

# Send a query and stream the response
stream_response = openai.responses.create(
    stream=True,
    tool_choice="required",
    input="What are the latest updates from Microsoft Learn?",
    extra_body={"agent_reference": {"name": agent.name, "type": "agent_reference"}},
)

# Process streaming events
for event in stream_response:
    if event.type == "response.created":
        print(f"Response created with ID: {event.response.id}")
    elif event.type == "response.output_text.delta":
        print(f"Delta: {event.delta}")
    elif event.type == "response.text.done":
        print(f"\nResponse done!")
    elif event.type == "response.output_item.done":
        if event.item.type == "message":
            item = event.item
            if item.content[-1].type == "output_text":
                text_content = item.content[-1]
                for annotation in text_content.annotations:
                    if annotation.type == "url_citation":
                        print(f"URL Citation: {annotation.url}")
    elif event.type == "response.completed":
        print(f"\nResponse completed!")
        print(f"Full response: {event.response.output_text}")

project.agents.delete_version(agent_name=agent.name, agent_version=agent.version)
print("Agent deleted")
```

#### Expected output

```output
Agent created (id: abc123, name: MyAgent, version: 1)
Response created with ID: resp_456
Delta: Based on your custom search ...
Response done!
URL Citation: https://your-allowed-domain.com/article

Response completed!
Full response: Based on your custom search ...
Agent deleted
```

#### Tips for domain-restricted search

Grounding with Bing Custom Search is a powerful tool that you can use to select a subspace of the web to limit your agent's grounding knowledge. Here are a few tips to help you take full advantage of this capability:

- If you own a public site that you want to include in the search but Bing hasn't indexed, see the [Bing Webmaster Guidelines](https://www.bing.com/webmasters/help/webmasters-guidelines-30fba23a) for details about getting your site indexed. The webmaster documentation also provides details about getting Bing to crawl your site if the index is out of date.
- You need at least the **Contributor** role for the Bing Custom Search resource to create a configuration.
- You can block certain domains and perform a search against the rest of the web (a competitor's site, for example).
- Grounding with Bing Custom Search only returns results for domains and webpages that are public and indexed by Bing.
- You can specify different levels of granularity:
  - Domain (for example, `https://www.microsoft.com`)
  - Domain and path (for example, `https://www.microsoft.com/surface`)
  - Webpage (for example, `https://www.microsoft.com/en-us/p/surface-earbuds/8r9cpq146064`)

### Deep Research with Web Search

The following example shows how to use the `o3-deep-research` model with the web search tool. This approach replaces the deprecated [Deep Research tool](../../../../foundry-classic/agents/how-to/tools-classic/deep-research.md), enabling multi-step research using public web data directly through the web search tool.

> [!NOTE]
> Set the `AZURE_AI_MODEL_DEPLOYMENT_NAME` environment variable to your `o3-deep-research` deployment name.

```python
import os
import sys
from dotenv import load_dotenv

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition, WebSearchPreviewTool

load_dotenv()

project_client = AIProjectClient(
    endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

openai_client = project_client.get_openai_client()

with project_client:
    # Create Agent with web search tool using o3-deep-research model
    agent = project_client.agents.create_version(
        agent_name="MyDeepResearchAgent",
        definition=PromptAgentDefinition(
            model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
            instructions="You are a helpful assistant that can search the web",
            tools=[
                WebSearchPreviewTool()
            ],
        ),
        description="Agent for deep research with web search.",
    )
    print(f"Agent created (id: {agent.id}, name: {agent.name}, version: {agent.version})")

    # Create a conversation for the agent interaction
    conversation = openai_client.conversations.create()
    print(f"Created conversation (id: {conversation.id})")

    # Send a query to search the web
    response = openai_client.responses.create(
        stream=True,
        conversation=conversation.id,
        input="What are the latest advancements in quantum computing?",
        extra_body={"agent": {"name": agent.name, "type": "agent_reference"}},
    )

    # Process streaming events as they arrive
    for event in response:
        if event.type == "response.created":
            print(f"Stream response created with ID: {event.response.id}")
        elif event.type == "response.output_text.delta":
            print(f"Delta: {event.delta}")
        elif event.type == "response.text.done":
            print(f"\nResponse done with full message: {event.text}")
        elif event.type == "response.completed":
            print(f"\nResponse completed!")
            print(f"Full response: {event.response.output_text}")

    print("\nCleaning up...")
    project_client.agents.delete_version(agent_name=agent.name, agent_version=agent.version)
    print("Agent deleted")
```
:::zone-end

:::zone pivot="csharp"

### General Web Search

In this example, you use the agent to perform the web search in the given location. The example in this section uses synchronous calls. For an asynchronous example, see the [sample code](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/ai/Azure.AI.Extensions.OpenAI/samples/Sample13_WebSearch.md) in the Azure SDK for .NET repository on GitHub.

```csharp
using System;
using Azure.AI.Projects;
using Azure.AI.Extensions.OpenAI;
using Azure.Identity;

// Format: "https://resource_name.ai.azure.com/api/projects/project_name"
var projectEndpoint = "your_project_endpoint";

// Create project client to call Foundry API
AIProjectClient projectClient = new(
    endpoint: new Uri(projectEndpoint),
    tokenProvider: new DefaultAzureCredential());

// Create an agent with the web search tool
DeclarativeAgentDefinition agentDefinition = new(model: "gpt-5-mini")
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

// Create the response and verify it completed.
Console.WriteLine($"Response status: {response.Status}");
Console.WriteLine(response.GetOutputText());

// Delete the created agent version.
projectClient.Agents.DeleteAgentVersion(agentName: agentVersion.Name, agentVersion: agentVersion.Version);
```

**Expected output**

The following is an example of the expected output when running the C# code:

```console
Response status: Completed
The London Underground currently has service disruptions on ...
Agent deleted
```

### Domain restricted web search
To enable your Agent to use Web Search with Grounding with Bing Custom Search instance.

1. First, we need to create project client and read the environment variables, which will be used in the next steps.

```C# Snippet:Sample_CreateAgentClient_WebSearchCustomStreaming
var projectEndpoint = System.Environment.GetEnvironmentVariable("PROJECT_ENDPOINT");
var modelDeploymentName = System.Environment.GetEnvironmentVariable("MODEL_DEPLOYMENT_NAME");
var connectionName = System.Environment.GetEnvironmentVariable("CUSTOM_BING_CONNECTION_NAME");
var customInstanceName = System.Environment.GetEnvironmentVariable("BING_CUSTOM_SEARCH_INSTANCE_NAME");
AIProjectClient projectClient = new(endpoint: new Uri(projectEndpoint), tokenProvider: new DefaultAzureCredential());
```

2. Create an Agent capable of using Web search on Grounding with Bing Custom Search instance.

Synchronous sample:
```C# Snippet:Sample_CreateAgent_WebSearchCustomStreaming_Sync
AIProjectConnection bingConnection = projectClient.Connections.GetConnection(connectionName: connectionName);
WebSearchTool webSearchTool = ResponseTool.CreateWebSearchTool();
webSearchTool.CustomSearchConfiguration = new(bingConnection.Id, customInstanceName);
DeclarativeAgentDefinition agentDefinition = new(model: modelDeploymentName)
{
    Instructions = "You are a helpful agent.",
    Tools = { webSearchTool }
};
AgentVersion agentVersion = projectClient.Agents.CreateAgentVersion(
    agentName: "myAgent",
    options: new(agentDefinition));
```

Asynchronous sample:
```C# Snippet:Sample_CreateAgent_WebSearchCustomStreaming_Async
AIProjectConnection bingConnection = projectClient.Connections.GetConnection(connectionName: connectionName);
WebSearchTool webSearchTool = ResponseTool.CreateWebSearchTool();
webSearchTool.CustomSearchConfiguration = new(bingConnection.Id, customInstanceName);
DeclarativeAgentDefinition agentDefinition = new(model: modelDeploymentName)
{
    Instructions = "You are a helpful agent.",
    Tools = { webSearchTool }
};
AgentVersion agentVersion = await projectClient.Agents.CreateAgentVersionAsync(
    agentName: "myAgent",
    options: new(agentDefinition));
```

3. To get the formatted annotation we have created the `GetFormattedAnnotation` method.

```C# Snippet:Sample_FormatReference_WebSearchCustomStreaming
private static string GetFormattedAnnotation(ResponseItem item)
{
    if (item is MessageResponseItem messageItem)
    {
        foreach (ResponseContentPart content in messageItem.Content)
        {
            foreach (ResponseMessageAnnotation annotation in content.OutputTextAnnotations)
            {
                if (annotation is UriCitationMessageAnnotation uriAnnotation)
                {
                    return $" [{uriAnnotation.Title}]({uriAnnotation.Uri})";
                }
            }
        }
    }
    return "";
}
```

4. Ask the question and stream the response.

Synchronous sample:
```C# Snippet:Sample_StreamResponse_WebSearchCustomStreaming_Sync
ProjectResponsesClient responseClient = projectClient.OpenAI.GetProjectResponsesClientForAgent(agentVersion.Name);

string annotation = "";
string text = "";
CreateResponseOptions options = new()
{
    ToolChoice = ResponseToolChoice.CreateRequiredChoice(),
    InputItems = { ResponseItem.CreateUserMessageItem("How many medals did the USA win in the 2024 summer olympics?") },
};
foreach (StreamingResponseUpdate streamResponse in responseClient.CreateResponseStreaming(options))
{
    if (streamResponse is StreamingResponseCreatedUpdate createUpdate)
    {
        Console.WriteLine($"Stream response created with ID: {createUpdate.Response.Id}");
    }
    else if (streamResponse is StreamingResponseOutputTextDeltaUpdate textDelta)
    {
        Console.WriteLine($"Delta: {textDelta.Delta}");
    }
    else if (streamResponse is StreamingResponseOutputTextDoneUpdate textDoneUpdate)
    {
        text = textDoneUpdate.Text;
    }
    else if (streamResponse is StreamingResponseOutputItemDoneUpdate itemDoneUpdate)
    {
        if (annotation.Length == 0)
        {
            annotation = GetFormattedAnnotation(itemDoneUpdate.Item);
        }
    }
    else if (streamResponse is StreamingResponseErrorUpdate errorUpdate)
    {
        throw new InvalidOperationException($"The stream has failed: {errorUpdate.Message}");
    }
}
Console.WriteLine($"{text}{annotation}");
```

Asynchronous sample:
```C# Snippet:Sample_StreamResponse_WebSearchCustomStreaming_Async
ProjectResponsesClient responseClient = projectClient.OpenAI.GetProjectResponsesClientForAgent(agentVersion.Name);

string annotation = "";
string text = "";
CreateResponseOptions options = new()
{
    ToolChoice = ResponseToolChoice.CreateRequiredChoice(),
    InputItems = { ResponseItem.CreateUserMessageItem("How many medals did the USA win in the 2024 summer olympics?") },
};
await foreach (StreamingResponseUpdate streamResponse in responseClient.CreateResponseStreamingAsync(options))
{
    if (streamResponse is StreamingResponseCreatedUpdate createUpdate)
    {
        Console.WriteLine($"Stream response created with ID: {createUpdate.Response.Id}");
    }
    else if (streamResponse is StreamingResponseOutputTextDeltaUpdate textDelta)
    {
        Console.WriteLine($"Delta: {textDelta.Delta}");
    }
    else if (streamResponse is StreamingResponseOutputTextDoneUpdate textDoneUpdate)
    {
        text = textDoneUpdate.Text;
    }
    else if (streamResponse is StreamingResponseOutputItemDoneUpdate itemDoneUpdate)
    {
        if (annotation.Length == 0)
        {
            annotation = GetFormattedAnnotation(itemDoneUpdate.Item);
        }
    }
    else if (streamResponse is StreamingResponseErrorUpdate errorUpdate)
    {
        throw new InvalidOperationException($"The stream has failed: {errorUpdate.Message}");
    }
}
Console.WriteLine($"{text}{annotation}");
```

5. Finally, delete all the resources we have created in this sample.

Synchronous sample:
```C# Snippet:Sample_Cleanup_WebSearchCustomStreaming_Sync
projectClient.Agents.DeleteAgentVersionAsync(agentName: agentVersion.Name, agentVersion: agentVersion.Version);
```

Asynchronous sample:
```C# Snippet:Sample_Cleanup_WebSearchCustomStreaming_Async
await projectClient.Agents.DeleteAgentVersionAsync(agentName: agentVersion.Name, agentVersion: agentVersion.Version);
```
**Expected output**

The following is an example of the expected output when running the C# code:

```console
Response status: Completed
The London Underground currently has service disruptions on ...
Agent deleted
```
:::zone-end

:::zone pivot="rest-api"
### General Web Search

Get an access token:

```bash
export AGENT_TOKEN=$(az account get-access-token --scope "https://ai.azure.com/.default" --query accessToken -o tsv)
```

The following example shows how to create a response by using an agent that has the web search tool enabled.

```bash
curl --request POST \
  --url "$FOUNDRY_PROJECT_ENDPOINT/openai/v1/responses" \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "model": "'$FOUNDRY_MODEL_DEPLOYMENT_NAME'",
    "input": "Tell me about the latest news about AI",
    "tool_choice": "required",
    "tools": [
      {
        "type": "web_search"
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
### Domain restricted web search

Get an access token:

```bash
export AGENT_TOKEN=$(az account get-access-token --scope "https://ai.azure.com/.default" --query accessToken -o tsv)
```

The following example shows how to create a response by using an agent that has the web search tool enabled.

```bash
curl --request POST \
  --url "$FOUNDRY_PROJECT_ENDPOINT/openai/v1/responses" \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "model": "'$FOUNDRY_MODEL_DEPLOYMENT_NAME'",
    "input": "Tell me about the latest news about AI",
    "tool_choice": "required",
    "tools": [
      {
        "type": "web_search",
        "custom_search_configuration": [
          {
            "project_connection_id": "'$BING_CUSTOM_SEARCH_PROJECT_CONNECTION_ID'",
            "instance_name": "'$BING_CUSTOM_SEARCH_INSTANCE_NAME'",
          }
        ]
      }
    ]
  }'
```
:::zone-end

:::zone pivot="typescript"
## Use the web search tool with TypeScript

The following TypeScript example demonstrates how to create an agent with the web search tool. For an example that uses JavaScript, see the [sample code](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/ai/ai-projects/samples/v2-beta/javascript/agents/tools/agentWebSearch.js) example in the Azure SDK for JavaScript repository on GitHub.

```typescript
// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

/**
 * This sample demonstrates how to run Prompt Agent operations using the Web Search Tool.
 *
 * @summary This sample demonstrates how to create an agent with web search capabilities,
 * send a query to search the web, and clean up resources.
 *
 * @warning Web Search tool uses Grounding with Bing, which has additional costs and terms: [terms of use](https://www.microsoft.com/bing/apis/grounding-legal-enterprise) and [privacy statement](https://go.microsoft.com/fwlink/?LinkId=521839&clcid=0x409). Customer data will flow outside the Azure compliance boundary. Learn more [here](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/web-search?pivots=rest-api)
 *
 * @azsdk-weight 100
 */

import { DefaultAzureCredential } from "@azure/identity";
import { AIProjectClient } from "@azure/ai-projects";
import "dotenv/config";

const projectEndpoint = process.env["AZURE_AI_PROJECT_ENDPOINT"] || "<project endpoint>";
const deploymentName = process.env["MODEL_DEPLOYMENT_NAME"] || "<model deployment name>";

export async function main(): Promise<void> {
  // Create AI Project client
  const project = new AIProjectClient(projectEndpoint, new DefaultAzureCredential());
  const openAIClient = project.getOpenAIClient();

  console.log("Creating agent with web search tool...");

  // Create Agent with web search tool
  const agent = await project.agents.createVersion("agent-web-search", {
    kind: "prompt",
    model: deploymentName,
    instructions: "You are a helpful assistant that can search the web",
    tools: [
      {
        type: "web_search",
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
Agent created (id: 12345, name: agent-web-search, version: 1)
Response: The agent returns a grounded response that includes citations.
Agent deleted
```
:::zone-end

:::zone pivot="java"

## Use web search in a Java agent

Add the dependency to your `pom.xml`:

```xml
<dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-ai-agents</artifactId>
    <version>2.0.0</version>
</dependency>
```

### Create an agent with web search

```java
import com.azure.ai.agents.AgentsClient;
import com.azure.ai.agents.AgentsClientBuilder;
import com.azure.ai.agents.ResponsesClient;
import com.azure.ai.agents.models.AgentReference;
import com.azure.ai.agents.models.AgentVersionDetails;
import com.azure.ai.agents.models.AzureCreateResponseOptions;
import com.azure.ai.agents.models.PromptAgentDefinition;
import com.azure.ai.agents.models.WebSearchTool;
import com.azure.identity.DefaultAzureCredentialBuilder;
import com.openai.models.responses.Response;
import com.openai.models.responses.ResponseCreateParams;

import java.util.Collections;

public class WebSearchExample {
    public static void main(String[] args) {
        // Format: "https://resource_name.ai.azure.com/api/projects/project_name"
        String projectEndpoint = "your_project_endpoint";

        AgentsClientBuilder builder = new AgentsClientBuilder()
            .credential(new DefaultAzureCredentialBuilder().build())
            .endpoint(projectEndpoint);

        AgentsClient agentsClient = builder.buildAgentsClient();
        ResponsesClient responsesClient = builder.buildResponsesClient();

        // Create web search tool with user location
        WebSearchPreviewTool webSearchTool = new WebSearchTool();

        // Create agent with web search tool
        PromptAgentDefinition agentDefinition = new PromptAgentDefinition("gpt-5-mini")
            .setInstructions("You are a helpful assistant that can search the web for current information.")
            .setTools(Collections.singletonList(webSearchTool));

        AgentVersionDetails agent = agentsClient.createAgentVersion("web-search-agent", agentDefinition);
        System.out.printf("Agent created: %s (version %s)%n", agent.getName(), agent.getVersion());

        // Create a response
        AgentReference agentReference = new AgentReference(agent.getName())
            .setVersion(agent.getVersion());

        Response response = responsesClient.createAzureResponse(
            new AzureCreateResponseOptions().setAgentReference(agentReference),
            ResponseCreateParams.builder()
                .input("What are the latest trends in renewable energy?"));

        System.out.println("Response: " + response.output());

        // Clean up
        agentsClient.deleteAgentVersion(agent.getName(), agent.getVersion());
    }
}
```

### Expected output

```output
Agent created: web-search-agent (version 1)
Response: [ResponseOutputItem with web search results about renewable energy trends ...]
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

## Known limitations

For information about web search behavior and limitations in the Responses API, see [Web search with the Responses API](../../../openai/how-to/web-search.md).

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
> [Set up an agent environment](../../../agents/environment-setup.md)
