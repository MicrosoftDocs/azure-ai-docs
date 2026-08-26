---
title: "Use web search tool in Foundry Agent Service"
description: "Use the web search tool in Foundry Agent Service to retrieve real-time information and ground AI responses. Includes code examples."
services: cognitive-services
manager: mcleans
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.topic: how-to
ms.date: 08/05/2026
author: mattwojo
reviewer: lindazqli
ms.author: mattwoj
ms.reviewer: zhuoqunli
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

The web search tool in Foundry Agent Service enables the agent's Foundry model to retrieve and ground responses with real-time information from the public web before generating output. When enabled, the model can return up-to-date answers with inline citations, helping you build agents that provide current, factual information to users.

> [!IMPORTANT]
> - Web Search uses Grounding with Bing Search and Grounding with Bing Custom Search, which are [First Party Consumption Services](https://www.microsoft.com/licensing/terms/product/Glossary/EAEAS#:%7E:text=First-Party%20Consumption%20Services) governed by these [Grounding with Bing terms of use](https://www.microsoft.com/bing/apis/grounding-legal-enterprise) and the [Microsoft Privacy Statement](https://go.microsoft.com/fwlink/?LinkId=521839&clcid=0x409).
> - The Microsoft [Data Protection Addendum](https://aka.ms/dpa) doesn't apply to data sent to Grounding with Bing Search and Grounding with Bing Custom Search. When you use Grounding with Bing Search and Grounding with Bing Custom Search, data transfers occur outside compliance and geographic boundaries.
> - Use of Grounding with Bing Search and Grounding with Bing Custom Search incurs costs. See [pricing](https://www.microsoft.com/bing/apis) for details.
> - See the [management section](#administrator-control-for-the-web-search-tool) for information about how Azure admins can manage access to use of web search.

[!INCLUDE [toolbox-recommended](../../includes/toolbox-recommended.md)]

**Usage support**

The following table shows SDK and setup support.

| Microsoft Foundry support | Python SDK | C# SDK | JavaScript SDK | Java SDK | REST API | Basic agent setup | Standard agent setup |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |

## Prerequisites

- A [basic or standard agent environment](../../../agents/environment-setup.md)
- The latest SDK package. The .NET SDK is currently in preview. See the [quickstart](../../../quickstarts/get-started-code.md#install-and-authenticate) for details.
- **Foundry User** role on the Foundry project to create and run agents.

    [!INCLUDE [role-rename-note](../../../includes/role-rename-note.md)]
- **Foundry Project Manager** role on the Foundry project if you create the remote-tool project connection for domain-restricted search.
- Azure credentials configured for authentication (such as `DefaultAzureCredential`).
- Your Foundry project endpoint URL and a model deployment name.

## Choose a web grounding scenario

| Scenario | Choose it when | Start here |
| --- | --- | --- |
| General Web Search | Your agent needs current information from the public web without a separate Bing resource or project connection. | [Add web search directly to a prompt agent](#add-web-search-directly-to-an-agent). |
| Domain-restricted Bing Custom Search | Search results must come from public domains configured in your Bing Custom Search instance. | [Configure domain-restricted search](#domain-restricted-search-with-bing-custom-search). |
| Deep research | Your `o3-deep-research` agent needs multi-step research and synthesis. | [Use direct web search for deep research](#deep-research-with-web-search). |
| Bing grounding tools | You need the explicit `bing_grounding` or `bing_custom_search_preview` tool type with a Bing project connection. | [Use Grounding with Bing Search tools](bing-tools.md). |

## Add web search directly to an agent

Start with the **Prompt Agents** tab. It adds `WebSearchTool` directly to a server-side agent and doesn't require a toolbox or a separate Bing project connection. This path provides the shortest route to a grounded response with citations.

The **Hosted Agents** tab uses `WebSearchToolboxTool` to add web search to a [toolbox](../../concepts/toolbox-overview.md), then connects to the toolbox MCP endpoint. Keep the direct-agent and toolbox tool types separate because they apply to different API surfaces.

> [!NOTE]
> For information on optimizing tool usage, see [best practices](../../concepts/tool-best-practice.md).

:::zone pivot="python"
### General web search

The following example shows how to give an agent access to web search. Select **Prompt Agents** to use the Azure AI Projects SDK to create a server-side prompt agent, or **Hosted Agents** to use the Agent Framework [`FoundryChatClient`](../../quickstarts/responses-api.md) to build an ephemeral, in-process agent.

### Prompt agents

#### Create the agent and run a search

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
    elif event.type == "response.output_text.done":
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

### Hosted agents

This sample uses [`FoundryChatClient`](../../quickstarts/responses-api.md) from the Microsoft Agent Framework and connects to the toolbox MCP endpoint using `FoundryToolbox`. Install the package with `pip install agent-framework-foundry`, set the `FOUNDRY_PROJECT_ENDPOINT` and `FOUNDRY_MODEL` environment variables, and sign in with `az login`. For the complete hosted-agent toolbox pattern, see the [full sample](https://aka.ms/foundry-toolbox-maf).

#### Create a toolbox and run a hosted agent

```python
import asyncio

from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient, FoundryToolbox
from azure.identity import AzureCliCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import WebSearchToolboxTool, WebSearchApproximateLocation

PROJECT_ENDPOINT = "https://<account>.services.ai.azure.com/api/projects/<project>"


async def main() -> None:
    credential = AzureCliCredential()

    # 1. Create the web search tool and add it to a toolbox. Using a toolbox is the
    #    recommended way to give agents tools: curate tools once and reuse the
    #    toolbox across agents. See /azure/foundry/agents/concepts/toolbox-overview
    project = AIProjectClient(endpoint=PROJECT_ENDPOINT, credential=credential)
    toolbox = project.toolboxes.create_version(
        name="web-search-toolbox",
        description="Toolbox with the web search tool",
        tools=[
            WebSearchToolboxTool(
                user_location=WebSearchApproximateLocation(
                    country="GB", city="London", region="London"
                )
            )
        ],
    )

    # 2. The toolbox exposes an MCP-compatible endpoint.
    TOOLBOX_MCP_URL = (
        f"{PROJECT_ENDPOINT}/toolboxes/{toolbox.name}"
        f"/versions/{toolbox.version}/mcp?api-version=v1"
    )

    # 3. Attach the toolbox to the hosted agent as an MCP tool.
, timeout=120.0)
    toolbox_tool = FoundryToolbox(credential, url=TOOLBOX_MCP_URL)

agent = Agent(
        client=FoundryChatClient(credential=credential),
        instructions="You are a research assistant. Use web search to find current information.",
        tools=[toolbox_tool],
    )

    result = await agent.run("What are the latest updates to Microsoft Foundry?")
    print(f"Agent: {result.text}")

    # Print any URL citations returned by the web search tool.
    for message in result.messages:
        for content in message.contents:
            for annotation in getattr(content, "annotations", None) or []:
                url = getattr(annotation, "url", None)
                if url:
                    title = getattr(annotation, "title", None) or ""
                    print(f"URL Citation: [{title}]({url})")


if __name__ == "__main__":
    asyncio.run(main())
```

### Expected output

The agent answers using fresh information from the web and prints any URL citations the tool returned. Output varies as content on the web changes:

```console
Agent: The latest updates to Microsoft Foundry include ...
URL Citation: [Microsoft Foundry documentation](https://learn.microsoft.com/azure/ai-foundry/)
```

The web search tool executes server-side in the Foundry Responses API. You can combine it with local function tools by adding additional entries (for example, a `@tool`-decorated function) to the `tools` list. For more, see [Quickstart: Use the Foundry Responses API](../../quickstarts/responses-api.md).

---

### Domain-restricted search with Bing Custom Search

The following example shows how to restrict web search to specific domains using a Bing Custom Search instance. This approach gives you control over which websites your agent can search.

#### Create the Bing Custom Search connection with the Azure Developer CLI

The `azd ai connection create` command doesn't currently support the
`GroundingWithBingCustomSearch` connection category. Define the connection in
`azure.yaml` instead, and run `azd provision`:

```yaml
resources:
  - kind: connection
    name: bing-custom-search
    category: GroundingWithBingCustomSearch
    target: https://api.bing.microsoft.com/
    credentials:
      type: ApiKey
      key: <bing-custom-search-key>
```

Don't commit the key to source control. Inject it from a secure store before
you run:

```bash
azd provision
```

#### Create the toolbox and domain-restricted agent

```python
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    PromptAgentDefinition,
    WebSearchToolboxTool,
    WebSearchConfiguration,
    MCPTool,
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

# 1. Add the web search tool and custom search configuration to a toolbox.
toolbox = project.toolboxes.create_version(
    name="web-search-toolbox",
    description="Toolbox with the web search tool",
    tools=[
        WebSearchToolboxTool(
            custom_search_configuration=WebSearchConfiguration(
                project_connection_id=BING_CUSTOM_SEARCH_CONNECTION_ID,
                instance_name=BING_CUSTOM_SEARCH_INSTANCE_NAME,
            )
        )
    ],
)

# 2. The toolbox exposes an MCP-compatible endpoint.
TOOLBOX_MCP_URL = (
    f"{PROJECT_ENDPOINT}/toolboxes/{toolbox.name}"
    f"/versions/{toolbox.version}/mcp?api-version=v1"
)

# 3. Create a remote-tool project connection that points at the toolbox endpoint.
#    Use a user Entra token so the caller's identity is passed through
#    (audience https://ai.azure.com). Create the connection once, for example with
#    the Azure Developer CLI:
#
#    azd ai connection create web-search-toolbox-conn \
#      --kind remote-tool \
#      --target "<TOOLBOX_MCP_URL>" \
#      --auth-type user-entra-token \
#      --audience https://ai.azure.com
TOOLBOX_CONNECTION_NAME = "web-search-toolbox-conn"

# 4. Attach the toolbox to a prompt agent as an MCP tool.
agent = project.agents.create_version(
    agent_name="MyAgent",
    definition=PromptAgentDefinition(
        model="gpt-5-mini",
        instructions="You are a helpful assistant that can search the web",
        tools=[
            MCPTool(
                server_label="toolbox",
                server_url=TOOLBOX_MCP_URL,
                require_approval="never",
                project_connection_id=TOOLBOX_CONNECTION_NAME,
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
    elif event.type == "response.output_text.done":
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
- To create a configuration, activate the **Contributor** role on the Bing Custom Search resource just in time through Microsoft Entra PIM. Deactivate the role after configuration. Day-to-day agent developers and runtime users don't need this role.
- You can block certain domains and perform a search against the rest of the web (a competitor's site, for example).
- Grounding with Bing Custom Search only returns results for domains and webpages that are public and indexed by Bing.
- You can specify different levels of granularity:
  - Domain (for example, `https://www.microsoft.com`)
  - Domain and path (for example, `https://www.microsoft.com/surface`)
  - Webpage (for example, `https://www.microsoft.com/en-us/p/surface-earbuds/8r9cpq146064`)

### Deep research with web search

The following example shows how to use the `o3-deep-research` model with the direct web search preview tool. This approach replaces the deprecated [Deep Research tool](../../../../foundry-classic/agents/how-to/tools-classic/deep-research.md). Don't route web search through a toolbox for deep research because the model requires the direct Responses web search tool.

#### Create the deep research agent

```python
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition, WebSearchPreviewTool

# Format: "https://resource_name.ai.azure.com/api/projects/project_name"
PROJECT_ENDPOINT = "your_project_endpoint"

# Create clients to call Foundry API
project = AIProjectClient(
    endpoint=PROJECT_ENDPOINT,
    credential=DefaultAzureCredential(),
)
openai = project.get_openai_client()

# Create a prompt agent with the direct web search preview tool.
agent = project.agents.create_version(
    agent_name="MyDeepResearchAgent",
    definition=PromptAgentDefinition(
        model="o3-deep-research",
        instructions="You are a helpful assistant that can search the web",
        tools=[WebSearchPreviewTool()],
    ),
    description="Agent for deep research with web search.",
)
print(f"Agent created (id: {agent.id}, name: {agent.name}, version: {agent.version})")

# Create a conversation for the agent interaction
conversation = openai.conversations.create()
print(f"Created conversation (id: {conversation.id})")

# Send a query to search the web
stream_response = openai.responses.create(
    stream=True,
    conversation=conversation.id,
    input="What are the latest advancements in quantum computing?",
    extra_body={"agent_reference": {"name": agent.name, "type": "agent_reference"}},
)

# Process streaming events as they arrive
for event in stream_response:
    if event.type == "response.created":
        print(f"Response created with ID: {event.response.id}")
    elif event.type == "response.output_text.delta":
        print(f"Delta: {event.delta}")
    elif event.type == "response.output_text.done":
        print(f"\nResponse done!")
    elif event.type == "response.completed":
        print(f"\nResponse completed!")
        print(f"Full response: {event.response.output_text}")

# Clean up resources
project.agents.delete_version(agent_name=agent.name, agent_version=agent.version)
print("Agent deleted")
```
:::zone-end

:::zone pivot="csharp"

### General web search

The following example shows how to give an agent access to web search. Select **Prompt Agents** to use the Azure AI Projects SDK to create a server-side prompt agent, or **Hosted Agents** to use the Microsoft Agent Framework to build an ephemeral, in-process agent.

### Prompt agents

In this example, you use the agent to perform the web search in the given location. The example in this section uses synchronous calls. For an asynchronous example, see the [sample code](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/ai/Azure.AI.Extensions.OpenAI/samples/Sample13_WebSearch.md) in the Azure SDK for .NET repository on GitHub.

#### Create the agent and run a search

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
AgentVersion agentVersion = projectClient.AgentAdministrationClient.CreateAgentVersion(
    agentName: "myAgent",
    options: new(agentDefinition));

// Ask a question related to London.
ProjectResponsesClient responseClient = projectClient.ProjectOpenAIClient.GetProjectResponsesClientForAgent(agentVersion.Name);

ResponseResult response = responseClient.CreateResponse("Show me the latest London Underground service updates");

// Create the response and verify it completed.
Console.WriteLine($"Response status: {response.Status}");
Console.WriteLine(response.GetOutputText());

// Delete the created agent version.
projectClient.AgentAdministrationClient.DeleteAgentVersion(agentName: agentVersion.Name, agentVersion: agentVersion.Version);
```

**Expected output**

The following is an example of the expected output when running the C# code:

```console
Response status: Completed
The London Underground currently has service disruptions on ...
Agent deleted
```

### Hosted agents

This sample creates the web-search toolbox with the Azure AI Projects SDK, then uses the Microsoft Agent Framework `AddFoundryToolboxes` integration to make web search available to the hosted agent. Set the `AZURE_AI_PROJECT_ENDPOINT`, `AZURE_OPENAI_ENDPOINT`, and `AZURE_AI_MODEL_DEPLOYMENT_NAME` environment variables, and sign in with `az login`.

#### Create a toolbox and run a hosted agent

```csharp
using Azure.AI.AgentServer.Responses;
using Azure.AI.AgentServer.Responses.Models;
using Azure.AI.OpenAI;
using Azure.AI.Projects;
using Azure.AI.Extensions.OpenAI;
using Azure.Identity;
using Microsoft.Agents.AI;
using Microsoft.Agents.AI.Foundry.Hosting;
using Microsoft.Extensions.DependencyInjection;
using OpenAI.Chat;

const string AgentInstructions = "You are a helpful assistant that can search the web to find current information and answer questions accurately.";
const string AgentName = "WebSearchAgent";

string projectEndpoint = Environment.GetEnvironmentVariable("AZURE_AI_PROJECT_ENDPOINT")
    ?? "https://<account>.services.ai.azure.com/api/projects/<project>";
string openAiEndpoint = Environment.GetEnvironmentVariable("AZURE_OPENAI_ENDPOINT")
    ?? throw new InvalidOperationException("AZURE_OPENAI_ENDPOINT is not set.");
string deploymentName = Environment.GetEnvironmentVariable("AZURE_AI_MODEL_DEPLOYMENT_NAME") ?? "gpt-5-mini";

DefaultAzureCredential credential = new();

// 1. Create the web search tool and add it to a toolbox. Using a toolbox is the
//    recommended way to give agents tools. See /azure/foundry/agents/concepts/toolbox-overview
AIProjectClient projectClient = new(
    endpoint: new Uri(projectEndpoint),
    tokenProvider: credential);
ProjectsAgentTool webTool = ProjectsAgentTool.AsProjectTool(
    ResponseTool.CreateWebSearchTool(userLocation: WebSearchToolLocation.CreateApproximateLocation(
        "GB", "London", "London")));
ToolboxVersion toolboxVersion = projectClient.AgentAdministrationClient
    .GetAgentToolboxes().CreateToolboxVersion(
        toolboxName: "web-search-toolbox",
        tools: [webTool],
        description: "Toolbox with the web search tool");

// Create the hosted agent and register the toolbox integration.
AIAgent agent = projectClient.AsAIAgent(
    model: deploymentName,
    instructions: "You are a helpful assistant with access to the toolbox tools.",
    name: "hosted-toolbox-agent");

var builder = WebApplication.CreateBuilder(args);
builder.Services.AddFoundryResponses(agent);
builder.Services.AddFoundryToolboxes(credential, toolboxVersion.Name);

var app = builder.Build();
app.MapFoundryResponses();
app.Run();
```

### Expected output

The agent answers using fresh information from the web and prints any URL citations the tool returned. Output varies as content on the web changes:

```console
Response: Today in Seattle it is mostly cloudy with a high near 55°F ...
Title: National Weather Service – Seattle
URL: https://www.weather.gov/sew/
```

The hosted agent connects to one toolbox endpoint and discovers the web search tool at runtime. You can add other tools to the toolbox without changing the hosted-agent code.

---

### Domain-restricted web search
To enable your Agent to use Web Search with Grounding with Bing Custom Search instance.

1. First, create the project client and define the values used in the next steps.

```C# Snippet:Sample_CreateAgentClient_WebSearchCustomStreaming
// Format: "https://resource_name.ai.azure.com/api/projects/project_name"
var projectEndpoint = "your_project_endpoint";
var modelDeploymentName = "gpt-4.1-mini";
var connectionName = "your_custom_bing_connection_name";
var customInstanceName = "your_bing_custom_search_instance_name";
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
AgentVersion agentVersion = projectClient.AgentAdministrationClient.CreateAgentVersion(
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
AgentVersion agentVersion = await projectClient.AgentAdministrationClient.CreateAgentVersionAsync(
    agentName: "myAgent",
    options: new(agentDefinition));
```

1. Call the `GetFormattedAnnotation` method to format the annotation.

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
ProjectResponsesClient responseClient = projectClient.ProjectOpenAIClient.GetProjectResponsesClientForAgent(agentVersion.Name);

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
ProjectResponsesClient responseClient = projectClient.ProjectOpenAIClient.GetProjectResponsesClientForAgent(agentVersion.Name);

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

1. Delete all resources that the sample created.

Synchronous sample:
```C# Snippet:Sample_Cleanup_WebSearchCustomStreaming_Sync
projectClient.AgentAdministrationClient.DeleteAgentVersionAsync(agentName: agentVersion.Name, agentVersion: agentVersion.Version);
```

Asynchronous sample:
```C# Snippet:Sample_Cleanup_WebSearchCustomStreaming_Async
await projectClient.AgentAdministrationClient.DeleteAgentVersionAsync(agentName: agentVersion.Name, agentVersion: agentVersion.Version);
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
### General web search

Get an access token:

```bash
export AGENT_TOKEN=$(az account get-access-token --scope "https://ai.azure.com/.default" --query accessToken -o tsv)
```

The recommended way to add web search is through a toolbox, then attach the toolbox to your agent as an MCP tool. See [What is a toolbox?](../../concepts/toolbox-overview.md)

1. Create a toolbox that contains the web search tool:

    ```bash
    curl --request POST \
      --url "$FOUNDRY_PROJECT_ENDPOINT/toolboxes/web-search-toolbox/versions?api-version=v1" \
            -H "Authorization: Bearer $AGENT_TOKEN" \
      -H "Content-Type: application/json" \
      --data '{
        "description": "Toolbox with the web search tool",
        "tools": [
          { "type": "web_search" }
        ]
      }'
    ```

   The toolbox exposes an MCP-compatible endpoint at `$FOUNDRY_PROJECT_ENDPOINT/toolboxes/web-search-toolbox/versions/<version>/mcp?api-version=v1`, where `<version>` is the version returned by the previous call.

1. Create a remote-tool project connection that points at the toolbox endpoint, using a user Entra token so the caller's identity is passed through (audience `https://ai.azure.com`).
    
    ```bash
    azd ai connection create web-search-toolbox-conn \
      --kind remote-tool \
      --target "$FOUNDRY_PROJECT_ENDPOINT/toolboxes/web-search-toolbox/versions/<version>/mcp?api-version=v1" \
      --auth-type user-entra-token \
      --audience https://ai.azure.com
    ```

1. Create a response that uses the toolbox by attaching it as an MCP tool.

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
            "type": "mcp",
            "server_label": "toolbox",
            "server_url": "'$FOUNDRY_PROJECT_ENDPOINT'/toolboxes/web-search-toolbox/versions/<version>/mcp?api-version=v1",
            "require_approval": "never",
            "project_connection_id": "web-search-toolbox-conn"
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
    "output": [
    {
            "id": "msg_abc123xyz",
      "type": "message",
            "role": "assistant",
            "status": "completed",
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
### Domain-restricted web search

Get an access token:

```bash
export AGENT_TOKEN=$(az account get-access-token --scope "https://ai.azure.com/.default" --query accessToken -o tsv)
```

The recommended way to add domain-restricted web search is through a toolbox, then attach the toolbox to your agent as an MCP tool.

1. Create a toolbox that contains the domain-restricted web search tool:

    ```bash
    curl --request POST \
      --url "$FOUNDRY_PROJECT_ENDPOINT/toolboxes/web-search-toolbox/versions?api-version=v1" \
            -H "Authorization: Bearer $AGENT_TOKEN" \
      -H "Content-Type: application/json" \
      --data '{
        "description": "Toolbox with the domain-restricted web search tool",
        "tools": [
          {
            "type": "web_search",
            "custom_search_configuration": {
              "project_connection_id": "'$BING_CUSTOM_SEARCH_PROJECT_CONNECTION_ID'",
              "instance_name": "'$BING_CUSTOM_SEARCH_INSTANCE_NAME'"
            }
          }
        ]
      }'
    ```

1. Create a remote-tool project connection that points at the toolbox endpoint, using a user Entra token so the caller's identity is passed through (audience `https://ai.azure.com`).

    ```bash
    azd ai connection create web-search-toolbox-conn \
      --kind remote-tool \
      --target "$FOUNDRY_PROJECT_ENDPOINT/toolboxes/web-search-toolbox/versions/<version>/mcp?api-version=v1" \
      --auth-type user-entra-token \
      --audience https://ai.azure.com
    ```
    
1. Create a response that uses the toolbox by attaching it as an MCP tool.

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
            "type": "mcp",
            "server_label": "toolbox",
            "server_url": "'$FOUNDRY_PROJECT_ENDPOINT'/toolboxes/web-search-toolbox/versions/<version>/mcp?api-version=v1",
            "require_approval": "never",
            "project_connection_id": "web-search-toolbox-conn"
          }
        ]
      }'
    ```
:::zone-end

:::zone pivot="typescript"
## Use the web search tool with TypeScript

The following TypeScript example demonstrates how to create an agent with the web search tool. For an example that uses JavaScript, see the [sample code](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/ai/ai-projects/samples/v2/javascript/agents/tools/agentWebSearch.js) in the Azure SDK for JavaScript repository on GitHub.

### Create a toolbox-backed agent

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

// Format: "https://resource_name.ai.azure.com/api/projects/project_name"
const PROJECT_ENDPOINT = "your_project_endpoint";

export async function main(): Promise<void> {
  // Create AI Project client
  const project = new AIProjectClient(PROJECT_ENDPOINT, new DefaultAzureCredential());
  const openai = project.getOpenAIClient();

  console.log("Creating a toolbox with the web search tool...");

  // 1. Add the web search tool to a toolbox. Using a toolbox is the recommended
  //    way to give agents tools. See /azure/foundry/agents/concepts/toolbox-overview
  const toolbox = await project.toolboxes.createVersion(
    "web-search-toolbox",
    [
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
    { description: "Toolbox with the web search tool" },
  );

  // 2. The toolbox exposes an MCP-compatible endpoint.
  const toolboxMcpUrl =
    `${PROJECT_ENDPOINT}/toolboxes/${toolbox.name}` +
    `/versions/${toolbox.version}/mcp?api-version=v1`;

  // 3. Create a remote-tool project connection that points at the toolbox endpoint.
  //    Use a user Entra token so the caller's identity is passed through
  //    (audience https://ai.azure.com). Create the connection once, for example
  //    with the Azure Developer CLI:
  //
  //    azd ai connection create web-search-toolbox-conn \
  //      --kind remote-tool \
  //      --target "<toolboxMcpUrl>" \
  //      --auth-type user-entra-token \
  //      --audience https://ai.azure.com
  const toolboxConnectionName = "web-search-toolbox-conn";

  // 4. Attach the toolbox to a prompt agent as an MCP tool.
  const agent = await project.agents.createVersion("agent-web-search", {
    kind: "prompt",
    model: "gpt-5-mini",
    instructions: "You are a helpful assistant that can search the web",
    tools: [
      {
        type: "mcp",
        server_label: "toolbox",
        server_url: toolboxMcpUrl,
        require_approval: "never",
        project_connection_id: toolboxConnectionName,
      },
    ],
  });
  console.log(`Agent created (id: ${agent.id}, name: ${agent.name}, version: ${agent.version})`);

  // Create a conversation for the agent interaction
  const conversation = await openai.conversations.create();
  console.log(`Created conversation (id: ${conversation.id})`);

  // Send a query to search the web
  console.log("\nSending web search query...");
  const response = await openai.responses.create(
    {
      conversation: conversation.id,
      input: "Show me the latest London Underground service updates",
    },
    {
    body: { agent_reference: { name: agent.name, type: "agent_reference" } },
    },
  );
  console.log(`Response: ${response.output_text}`);

  // Clean up resources
  console.log("\nCleaning up resources...");
  await openai.conversations.delete(conversation.id);
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

> [!TIP]
> **Recommended:** For most agents, add the web search tool through a [toolbox](../../concepts/toolbox-overview.md) and attach the toolbox to your agent as an MCP tool. The Java SDK doesn't yet expose a toolbox creation API, so create the toolbox by using the [Python](?pivots=python), [REST API](?pivots=rest-api), [C#](?pivots=csharp), or [TypeScript](?pivots=typescript) example, or the [Foundry portal](../../how-to/tools/toolbox.md). Then, reference its MCP endpoint from your Java agent as an `McpTool`. The following example attaches the web search tool directly to the agent.

Add the dependency to your `pom.xml`:

```xml
<dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-ai-agents</artifactId>
    <version>2.2.0</version>
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
        WebSearchTool webSearchTool = new WebSearchTool();

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

### Web search response format over MCP

> [!NOTE]
> When Web Search returns results over MCP, the response is a `resource` content item containing the synthesized answer with inline Markdown source links. URL citations are in `content[].resource._meta.annotations[]`. For example:
>
> ```json
> {
>   "jsonrpc": "2.0",
>   "id": "ws-call-1",
>   "result": {
>     "_meta": {
>       "tool_configuration": {
>         "type": "web_search",
>         "name": "web-search-default"
>       }
>     },
>     "content": [
>       {
>         "type": "resource",
>         "resource": {
>           "uri": "about:web-search-answer",
>           "mimeType": "text/plain",
>           "text": "Here are the latest updates on Azure OpenAI Service...\n\n- **GPT-image-1 Release (January 7, 2026)** Microsoft introduced GPT-image-1 ([serverless-solutions.com](https://...)).\n\n..."
>         },
>         "annotations": {
>           "audience": ["assistant"]
>         },
>         "_meta": {
>           "annotations": [
>             {
>               "type": "url_citation",
>               "url": "https://www.serverless-solutions.com/blog/...",
>               "title": "Microsoft expands Foundry with powerful new OpenAI models",
>               "start_index": 741,
>               "end_index": 879
>             }
>           ],
>           "action": {
>             "type": "search",
>             "query": "Azure OpenAI service updates 2026",
>             "queries": ["Azure OpenAI service updates 2026"]
>           },
>           "response_id": "resp_001fcebcc300..."
>         }
>       }
>     ],
>     "isError": false
>   }
> }
> ```

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
1. Activate **Contributor** at subscription scope just in time through Microsoft Entra PIM. Subscription scope is required because this setting applies to all Foundry resources in the subscription. Deactivate the role after changing the setting. Day-to-day agent developers and runtime users don't need this role.

### Disable web search

To disable the web search tool for all accounts in a subscription, run the following command: 

```azurecli
az feature register \
  --name OpenAI.BlockedTools.web_search \
  --namespace Microsoft.CognitiveServices \
  --subscription "<subscription-id>"
```

This command disables web search across all accounts in the specified subscription. 

### Enable web search

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
