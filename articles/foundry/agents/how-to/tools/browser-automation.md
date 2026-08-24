---
title: "Automate browser tasks with Foundry agents"
description: "Automate web browsing tasks with the Browser Automation tool in Microsoft Foundry agents. Create isolated Playwright sessions for navigation and form filling."
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
ms.custom: azure-ai-agents, dev-focus, pilot-ai-workflow-jan-2026, doc-kit-assisted
ai-usage: ai-assisted
zone_pivot_groups: selection-browser-tool
#CustomerIntent: As a developer building AI agents, I want to automate web browsing tasks so that my agents can interact with external websites and extract information.
---

# Automate browser tasks with the Browser Automation tool (preview)
[!INCLUDE [feature-preview](../../../includes/feature-preview.md)]

This article explains how to configure and use the Browser Automation tool with Foundry agents to automate web browsing workflows.

[!INCLUDE [toolbox-recommended](../../includes/toolbox-recommended.md)]

> [!WARNING]
> The Browser Automation Tool comes with significant security risks. When you use the Browser Automation Tool, an AI spins up remote browsers sessions to perform actions and can use credentials you explicitly share with the agent, such as to email, financial accounts, social networks, and enterprise systems. The AI agent may make mistakes and may be fooled by malicious data it may encounter on the Internet.
>
> You're responsible for reviewing and testing your applications and implementing your own responsible AI mitigations. By using the Browser Automation Tool, you are acknowledging that you bear responsibility and liability for any use of it and all outcomes. Use judgment in deciding which credentials you provide to your browser sessions. See the [Foundry Agent Service transparency note](/azure/foundry/responsible-ai/agents/transparency-note).

Browser Automation Tool (BAT) enables scalable, reliable browser-based automation within Foundry agents. BAT is available as an MCP tool powered by Playwright workspaces as its headless browser infrastructure layer. It integrates seamlessly with modern agentic workflows while providing enterprise-grade security, observability, and extensibility.

Browser Automation Tool (BAT) provides a comprehensive platform for browser automation through:

- [Playwright Workspaces](https://aka.ms/pww/docs) (a Generally Available service) as the infrastructure layer
- Real-time debugging with Live View
- Take control for human-in-the-loop scenarios
- Support for private website browsing (Private preview)
- Built-in observability for reliability and optimization
- Flexible orchestration layers

> [!NOTE]
> The private website feature in Playwright Workspaces is currently available in private preview.
> Interested users can fill out this [form](https://aka.ms/pww/private-website-enrolment-form) to enroll for the private preview.

## Prerequisites

Before you begin, make sure you have:

- An Azure subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- **Foundry User** role on the Foundry project for day-to-day agent development and use.

  [!INCLUDE [role-rename-note](../../../includes/role-rename-note.md)]
- **Foundry Project Manager** role on the Foundry project if you create the project connection.
- **Contributor** role on the target resource group only while you create the Playwright workspace. This role is required for resource provisioning. Activate it just in time through Microsoft Entra Privileged Identity Management (PIM), and deactivate it after provisioning. Day-to-day agent developers and runtime users don't need this role.
- A Foundry project with a configured endpoint.
- An AI model deployed in your project (for example, `gpt-5.4`).
- A Playwright workspace resource.
- A project connection set up for your Playwright workspace.

### SDK requirements

For Python examples, install the required packages:

```bash
pip install "azure-ai-projects>=2.0.0"
```

The .NET SDK is currently in preview. For more information, see the [quickstart](../../../quickstarts/get-started-code.md).

### Configuration

**Get your project endpoint**: Open your project in the [Foundry portal](https://ai.azure.com), and copy the endpoint from the project overview page. The format is `https://{account-name}.services.ai.azure.com/api/projects/{project-name}`.

**Connection ID format**: Use `/subscriptions/{{subscriptionID}}/resourceGroups/{{resourceGroupName}}/providers/Microsoft.CognitiveServices/accounts/{{foundryAccountName}}/projects/{{foundryProjectName}}/connections/{{foundryConnectionName}}`. You can find this value on the tool's details page after you connect the Browser Automation tool.

## Usage support

The following table shows SDK and setup support.

| Microsoft Foundry support | Python SDK | C# SDK | JavaScript SDK | Java SDK | REST API | Basic agent setup | Standard agent setup |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |

## How it works

The interaction starts when the user sends a query to an agent connected to the Browser Automation tool. For example, *"Show me all available yoga classes this week from the following URL \<url\>."* When the agent receives the request, Foundry Agent Service creates an isolated browser session using your provisioned Playwright workspace. Each session is sandboxed for privacy and security.

The browser performs Playwright-driven actions, such as navigating to relevant pages and applying filters or parameters based on user preferences (such as time, location, and instructor). By combining the model with Playwright, the model can parse HTML or XML into DOM documents, make decisions, and perform actions like selecting UI elements, typing, and navigating websites. Exercise caution when using this tool.

An example flow is:

1. A user sends a request to the model that includes a call to the Browser Automation tool with the URL you want to go to.
1. The Browser Automation tool receives a response from the model. If the response has action items, those items contain suggested actions to make progress toward the specified goal. For example, an action might be a screenshot so the model can assess the current state with an updated screenshot or click with X/Y coordinates indicating where the mouse should be moved.
1. The Browser Automation tool executes the action in a sandboxed environment.
1. After executing the action, the Browser Automation tool captures the updated state of the environment as a screenshot.
1. The tool sends a new request with the updated state, and repeats this loop until the model stops requesting actions or the user decides to stop.

  The Browser Automation tool supports multi-turn conversations, allowing the user to refine their request and complete form filling and web scraping scenarios.

## Set up Browser Automation

### Create a Playwright workspace

1. In the [Azure portal](https://portal.azure.com), create a [Playwright Workspace](https://aka.ms/pww/docs/manage-workspaces) resource.
1. After the workspace is created, go to **Settings** > **Access Management**.
1. Confirm the **Playwright Service Access Token** authentication method is enabled.
1. Select **Generate Token**, enter a name (for example, `foundry-connection`), and choose an expiry period.
1. **Copy the token immediately**. You can't view it again after closing the page.
1. On the workspace **Overview** page, copy the **Browser endpoint** (it starts with `wss://`).
1. [Configure a custom role](https://aka.ms/pww/docs/manage-workspace-access) with only the Playwright permissions that the project identity requires. If a custom role isn't available, assign **Contributor** only at the Playwright workspace resource scope.

### Connect the Browser Automation tool in Foundry

1. Go to the [Foundry portal](https://ai.azure.com/nextgen) and select your project.
2. Select **Build** > **Tools**.
3. Select **Create a toolbox**.
4. Fill in the **Name** and **Description** for your toolbox.
5. Under **Tools**, click on **Add**
6. Select **Browser Automation** and click **Add tool**
7. Enter the required fields
   - **Connection name**: Unique name for your connection
   - **Playwright Workspace**: Select the Playwright Workspace resource.
   - **Auth Type**: Select the authentication type for your connection.
8. Select **Connect**.
9. Click on **Publish** to save the toolbox

After the toolbox is created, you can view the **Project connection ID** on the tool's details page. Use this value as the browser automation connection ID in your code.

### Add browser automation to a toolbox with the Azure Developer CLI

To add browser automation to a Toolbox, use the Azure Developer CLI to create a Playwrite workspace. *This article assumes you already have a Playwright workspace resource. See the prerequisites section.*

1. Create the Playwright Workspace connection.

```bash
azd ai connection create my-browser-conn \
  --kind PlaywrightWorkspace \
  --target wss://your-browser-endpoint.api.playwright.microsoft.com/playwrightworkspaces/browsers \
  --auth-type api-key \
  --key "<playwright-workspaces-access-token>"
```

`--kind PlaywrightWorkspace` requires exact PascalCase.

2. Define the toolbox (my-toolbox.yaml)

```yaml
description: Browser Automation toolbox
tools:
  - type: browser_automation_preview
    project_connection_id: my-browser-conn
```

3. Create the toolbox

```bash
azd ai toolbox create my-toolbox --from-file my-toolbox.yaml
```

## Browser Automation tool definitions

After you run a sample, verify the tool was called by using tracing in Microsoft Foundry. For guidance on validating tool invocation, see [Best practices for using tools in Microsoft Foundry Agent Service](../../concepts/tool-best-practice.md). If you use streaming, you can also look for `browser_automation_preview_call` events.

> [!NOTE]
> - The .NET SDK is currently in preview. For more information, see the [quickstart](../../../quickstarts/get-started-code.md).

```csharp
ProjectsAgentTool tool = new BrowserAutomationPreviewTool(
    new BrowserAutomationToolOptions(
        new BrowserAutomationToolConnectionParameters("<BROWSER_AUTOMATION_PROJECT_CONNECTION_ID>")
    )
);
```

```javascript
const tools = [
  {
    type: "browser_automation_preview",
    name: "<OPTIONAL_TOOL_NAME>",
    description: "<Optional description for the model>",
    browser_automation_preview: {
      connection: {
          project_connection_id: "<BROWSER_AUTOMATION_PROJECT_CONNECTION_ID>"
      }
    }
  },
];
```

:::zone pivot="python"
## Use BrowserAutomationPreviewTool with agents example

The following Python example demonstrates how to create an AI agent with browser automation capabilities. Select **Prompt Agents** to use the Azure AI Projects SDK to create a server-side prompt agent, or **Hosted Agents** to use the Agent Framework [`FoundryChatClient`](../../quickstarts/responses-api.md) to build an ephemeral, in-process agent.

### Prompt agents

```python
import json
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    PromptAgentDefinition,
  BrowserAutomationPreviewTool,
    BrowserAutomationToolParameters,
    BrowserAutomationToolConnectionParameters,
)

# Format: "https://resource_name.ai.azure.com/api/projects/project_name"
PROJECT_ENDPOINT = "your_project_endpoint"
BROWSER_CONNECTION_ID = "your-browser-automation-connection-id"

# Create clients to call Foundry API
project = AIProjectClient(
    endpoint=PROJECT_ENDPOINT,
    credential=DefaultAzureCredential(),
)
openai = project.get_openai_client()

tool = BrowserAutomationPreviewTool(
    browser_automation_preview=BrowserAutomationToolParameters(
        connection=BrowserAutomationToolConnectionParameters(
            project_connection_id=BROWSER_CONNECTION_ID,
        )
    )
)

agent = project.agents.create_version(
    agent_name="MyAgent",
    definition=PromptAgentDefinition(
        model="gpt-4.1-mini",
        instructions="""You are an Agent helping with browser automation tasks. 
        You can answer questions, provide information, and assist with various tasks 
        related to web browsing using the Browser Automation tool available to you.""",
        tools=[tool],
    ),
)
print(f"Agent created (id: {agent.id}, name: {agent.name}, version: {agent.version})")

stream_response = openai.responses.create(
    stream=True,
    tool_choice="required",
    input="""
        Your goal is to report the percent of Microsoft year-to-date stock price change.
        To do that, go to the website finance.yahoo.com.
        At the top of the page, you will find a search bar.
        Enter the value 'MSFT', to get information about the Microsoft stock price.
        At the top of the resulting page you will see a default chart of Microsoft stock price.
        Click on 'YTD' at the top of that chart, and report the percent value that shows up just below it.""",
    extra_body={"agent_reference": {"name": agent.name, "type": "agent_reference"}},
)

for event in stream_response:
    if event.type == "response.created":
        print(f"Follow-up response created with ID: {event.response.id}")
    elif event.type == "response.output_text.delta":
        print(f"Delta: {event.delta}")
    elif event.type == "response.output_text.done":
        print(f"\nFollow-up response done!")
    elif event.type == "response.output_item.done":
        item = event.item
        if item.type == "browser_automation_preview_call":
            arguments_str = getattr(item, "arguments", "{}")

            # Parse the arguments string into a dictionary
            arguments = json.loads(arguments_str)
            query = arguments.get("query")

            print(f"Call ID: {getattr(item, 'call_id')}")
            print(f"Query arguments: {query}")
    elif event.type == "response.completed":
        print(f"\nFollow-up completed!")
        print(f"Full response: {event.response.output_text}")

print("\nCleaning up...")
project.agents.delete_version(agent_name=agent.name, agent_version=agent.version)
print("Agent deleted")
```

### What this code does

This example creates an agent version with the Browser Automation tool enabled, then sends a prompt that requires the agent to use the tool. It also processes streaming events so you can observe progress and tool calls.

### Required inputs

- A Foundry project endpoint and a browser automation connection ID. See [Configuration](#configuration) for details.

### Expected output

When you create the agent, you see output similar to:

```console
Agent created (id: ..., name: ..., version: ...)
```

During streaming, you might also see deltas and tool-call details. Output varies based on the website content and model behavior.

### Hosted agents

This sample uses [`FoundryChatClient`](../../quickstarts/responses-api.md) from the Microsoft Agent Framework to create the `browser-automation-toolbox` and connect to its MCP endpoint with `FoundryToolbox`. Install the packages with `pip install agent-framework-foundry azure-ai-projects`, replace `PROJECT_ENDPOINT` and `BROWSER_CONNECTION_ID` with your project values, and sign in with `az login`. For the complete hosted-agent toolbox pattern, see the [full sample](https://aka.ms/foundry-toolbox-maf).

```python
import asyncio

from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient, FoundryToolbox
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
  BrowserAutomationPreviewToolboxTool,
    BrowserAutomationToolParameters,
    BrowserAutomationToolConnectionParameters,
)
from azure.identity import AzureCliCredential

PROJECT_ENDPOINT = "https://<account>.services.ai.azure.com/api/projects/<project>"
BROWSER_CONNECTION_ID = "your-browser-automation-connection-id"


async def main() -> None:
    credential = AzureCliCredential()

    # 1. Add the Browser Automation tool to a toolbox. Using a toolbox is the recommended way
    #    to give agents tools: you curate tools once and reuse the toolbox across agents.
    #    See /azure/foundry/agents/concepts/toolbox-overview
    project = AIProjectClient(endpoint=PROJECT_ENDPOINT, credential=credential)
    tool = BrowserAutomationPreviewToolboxTool(
        browser_automation_preview=BrowserAutomationToolParameters(
            connection=BrowserAutomationToolConnectionParameters(
                project_connection_id=BROWSER_CONNECTION_ID,
            )
        )
    )
    toolbox = project.toolboxes.create_version(
        name="browser-automation-toolbox",
        description="Toolbox with the Browser Automation tool",
        tools=[tool],
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
        instructions=(
            "You help with browser automation tasks. Use the Browser Automation tool "
            "to navigate and read information from websites."
        ),
        tools=[toolbox_tool],
    )

    result = await agent.run(
        "Go to finance.yahoo.com, search for MSFT, click 'YTD' on the price chart, "
        "and report the year-to-date percent change."
    )
    print(f"Agent: {result.text}")


if __name__ == "__main__":
    asyncio.run(main())
```

### Expected output

The agent navigates the live website through the Browser Automation tool in the toolbox and reports the YTD value it observes. Output varies based on website content:

```console
Agent: The year-to-date change for MSFT is approximately +18.4%.
```

For the complete hosted-agent toolbox pattern, see the [full sample](https://aka.ms/foundry-toolbox-maf).

---

:::zone-end

:::zone pivot="csharp"
## Use BrowserAutomationPreviewTool with agents example

Before running this sample, complete the setup steps in [Set up Browser Automation](#set-up-browser-automation).

The following C# example demonstrates how to create an AI agent with Browser Automation capabilities. Select **Prompt Agents** to use the Azure AI Projects SDK to create a server-side prompt agent, or **Hosted Agents** to use the Microsoft Agent Framework to build an ephemeral, in-process agent.

### Prompt agents

This example uses synchronous methods of the Azure AI Projects client library. For an example that uses asynchronous methods, see the [Sample for use of BrowserAutomationPreviewTool and Agents](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/ai/Azure.AI.Extensions.OpenAI/samples/Sample23_BrowserAutomationTool.md) sample in the Azure SDK for .NET repository on GitHub.

```csharp
using System;
using Azure.AI.Projects;
using Azure.AI.Extensions.OpenAI;
using Azure.Identity;

// Format: "https://resource_name.ai.azure.com/api/projects/project_name"
var projectEndpoint = "your_project_endpoint";
var browserConnectionId = "your-browser-automation-connection-id";

// Note that Browser automation operations can take longer than usual
// and require the request timeout to be at least 5 minutes.
AIProjectClientOptions options = new()
{
    NetworkTimeout = TimeSpan.FromMinutes(5)
};
AIProjectClient projectClient = new(endpoint: new Uri(projectEndpoint), tokenProvider: new DefaultAzureCredential(), options: options);

// Create the Browser Automation tool using the Playwright connection.
BrowserAutomationPreviewTool playwrightTool = new(
    new BrowserAutomationToolParameters(
        new BrowserAutomationToolConnectionParameters(browserConnectionId)
    ));

// Create the Agent version with the Browser Automation tool.
DeclarativeAgentDefinition agentDefinition = new(model: "gpt-4.1-mini")
{
    Instructions = "You are an Agent helping with browser automation tasks.\n" +
    "You can answer questions, provide information, and assist with various tasks\n" +
    "related to web browsing using the Browser Automation tool available to you.",
    Tools = { playwrightTool }
};
AgentVersion agentVersion = projectClient.AgentAdministrationClient.CreateAgentVersion(
    agentName: "myAgent",
    options: new(agentDefinition));

// Create the response stream. Also set ToolChoice = ResponseToolChoice.CreateRequiredChoice()
// on the ResponseCreationOptions to ensure the agent uses the Browser Automation tool.
ProjectResponsesClient responseClient = projectClient.ProjectOpenAIClient.GetProjectResponsesClientForAgent(agentVersion.Name);
CreateResponseOptions responseOptions = new()
{
    ToolChoice = ResponseToolChoice.CreateRequiredChoice(),
    StreamingEnabled = true,
    InputItems =
    {
        ResponseItem.CreateUserMessageItem("Your goal is to report the percent of Microsoft year-to-date stock price change.\n" +
            "To do that, go to the website finance.yahoo.com.\n" +
            "At the top of the page, you will find a search bar.\n" +
            "Enter the value 'MSFT', to get information about the Microsoft stock price.\n" +
            "At the top of the resulting page you will see a default chart of Microsoft stock price.\n" +
            "Click on 'YTD' at the top of that chart, and report the percent value that shows up just below it.")
    }
};
foreach (StreamingResponseUpdate update in responseClient.CreateResponseStreaming(options: responseOptions))
{
    if (update is StreamingResponseCreatedUpdate createUpdate)
    {
        Console.WriteLine($"Stream response created with ID: {createUpdate.Response.Id}");
    }
    else if (update is StreamingResponseOutputTextDeltaUpdate textDelta)
    {
        Console.WriteLine($"Delta: {textDelta.Delta}");
    }
    else if (update is StreamingResponseOutputTextDoneUpdate textDoneUpdate)
    {
        Console.WriteLine($"Response done with full message: {textDoneUpdate.Text}");
    }
    else if (update is StreamingResponseErrorUpdate errorUpdate)
    {
        throw new InvalidOperationException($"The stream has failed with the error: {errorUpdate.Message}");
    }
}

// Delete the Agent version to clean up resources.
projectClient.AgentAdministrationClient.DeleteAgentVersion(agentName: agentVersion.Name, agentVersion: agentVersion.Version);
```

### What this code does

This example creates an agent version with the Browser Automation tool enabled, sends a prompt that requires tool usage, and prints streaming updates as the agent works through the browser steps.

### Required inputs

- A Foundry project endpoint and a browser automation connection ID. See [Configuration](#configuration) for details.
- A Playwright connection created in your Foundry project.

### Expected output

You see streaming progress messages, such as text deltas, and a completed response. The output varies based on the website content and model behavior.

### Hosted agents

This sample creates the Browser Automation toolbox with the Azure AI Projects SDK, and then uses the Microsoft Agent Framework `AddFoundryToolboxes` integration to make the tool available to the hosted agent. Install the Agent Framework packages, set the `AZURE_AI_PROJECT_ENDPOINT`, `AZURE_AI_MODEL_DEPLOYMENT_NAME`, and `BROWSER_AUTOMATION_CONNECTION_ID` environment variables, and sign in with `az login`.

```csharp
using System.IO;
using System.Runtime.CompilerServices;
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

string projectEndpoint = Environment.GetEnvironmentVariable("AZURE_AI_PROJECT_ENDPOINT")
    ?? "https://<account>.services.ai.azure.com/api/projects/<project>";
string deploymentName = Environment.GetEnvironmentVariable("AZURE_AI_MODEL_DEPLOYMENT_NAME") ?? "gpt-5-mini";
string browserConnectionId = Environment.GetEnvironmentVariable("BROWSER_AUTOMATION_CONNECTION_ID")
    ?? "your-browser-automation-connection-id";

var openAiEndpoint = new Uri(projectEndpoint).GetLeftPart(UriPartial.Authority);
DefaultAzureCredential credential = new();

// 1. Create the Browser Automation tool and add it to a toolbox. Using a toolbox is the
//    recommended way to give agents tools. See /azure/foundry/agents/concepts/toolbox-overview
AIProjectClient projectClient = new(endpoint: new Uri(projectEndpoint), tokenProvider: credential);
ProjectsAgentTool browserTool = new BrowserAutomationPreviewTool(
    new BrowserAutomationToolParameters(
        new BrowserAutomationToolConnectionParameters(browserConnectionId)
    ));
ToolboxVersion toolboxVersion = projectClient.AgentAdministrationClient
    .GetAgentToolboxes().CreateToolboxVersion(
        toolboxName: "browser-automation-toolbox",
        tools: [browserTool],
        description: "Toolbox with the Browser Automation tool");

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

The hosted agent connects to the Browser Automation tool through the toolbox MCP endpoint and uses the browser to complete the requested web task. Output varies based on website content and model behavior:

```console
Agent: The year-to-date change for MSFT is approximately +18.4%.
```

For the complete hosted-agent toolbox pattern, see the [full sample](https://aka.ms/foundry-toolbox-maf).

---

:::zone-end

:::zone pivot="rest"
Get an access token:

```bash
AGENT_TOKEN=$(az account get-access-token --scope https://ai.azure.com/.default --query accessToken -o tsv)
```

This access token is short-lived. Keep it only in the current shell or process. Never commit, store, print, or log it. Run the command again after it expires. SDK flows use `DefaultAzureCredential` where supported, but these REST requests require the bearer token.

The recommended way to add Browser Automation is through a toolbox, then attach the toolbox to your agent as an MCP tool. See [What is a toolbox?](../../concepts/toolbox-overview.md)

1. Create a toolbox that contains the Browser Automation tool:

```bash
curl --request POST \
  --url "$FOUNDRY_PROJECT_ENDPOINT/toolboxes/browser-automation-toolbox/versions?api-version=v1" \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "description": "Toolbox with the Browser Automation tool",
    "tools": [
      {
        "type": "browser_automation_preview",
        "browser_automation_preview": {
          "connection": {
            "project_connection_id": "'"$BROWSER_AUTOMATION_PROJECT_CONNECTION_ID"'"
          }
        }
      }
    ]
  }'
```

   The toolbox exposes an MCP-compatible endpoint at `$FOUNDRY_PROJECT_ENDPOINT/toolboxes/browser-automation-toolbox/versions/<version>/mcp?api-version=v1`, where `<version>` is the version returned by the previous call.

1. Create a remote-tool project connection that points at the toolbox endpoint, using a user Entra token so the caller's identity is passed through (audience `https://ai.azure.com`).

```bash
azd ai connection create browser-automation-toolbox-conn \
  --kind remote-tool \
  --target "$FOUNDRY_PROJECT_ENDPOINT/toolboxes/browser-automation-toolbox/versions/<version>/mcp?api-version=v1" \
  --auth-type user-entra-token \
  --audience https://ai.azure.com
```

1. Create a response that uses the toolbox by attaching it as an MCP tool.

```bash
curl --request POST \
  --url "${FOUNDRY_PROJECT_ENDPOINT}/openai/v1/responses" \
  --header "Authorization: Bearer ${AGENT_TOKEN}" \
  --header "Content-Type: application/json" \
  --header "User-Agent: insomnia/11.6.1" \
  --data @- <<JSON
{
  "model": "${FOUNDRY_MODEL_DEPLOYMENT_NAME}",
  "input": [
    {
      "role": "user",
      "content": [
        {
          "type": "input_text",
          "text": "Your goal is to report the percent of Microsoft year-to-date stock price change."
        },
        {
          "type": "input_text",
          "text": "Go to finance.yahoo.com, search for MSFT, select YTD on the chart, and report the percent value shown."
        }
      ]
    }
  ],
  "tools": [
    {
      "type": "mcp",
      "server_label": "toolbox",
      "server_url": "${FOUNDRY_PROJECT_ENDPOINT}/toolboxes/browser-automation-toolbox/versions/<version>/mcp?api-version=v1",
      "require_approval": "never",
      "project_connection_id": "browser-automation-toolbox-conn"
    }
  ]
}
JSON
```

:::zone-end

:::zone pivot="typescript"
## Use Browser Automation tool with agents example

The following TypeScript sample demonstrates how to create an agent with the Browser Automation tool, perform web browsing tasks, and process streaming responses with browser automation events. For a JavaScript version of this sample, see the [JavaScript sample for Browser Automation tool](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/ai/ai-projects/samples/v2/javascript/agents/tools/agentBrowserAutomation.js) in the Azure SDK for JavaScript repository on GitHub.

```typescript
import { DefaultAzureCredential } from "@azure/identity";
import { AIProjectClient } from "@azure/ai-projects";

// Format: "https://resource_name.ai.azure.com/api/projects/project_name"
const PROJECT_ENDPOINT = "your_project_endpoint";
const BROWSER_CONNECTION_ID = "your-browser-automation-connection-id";

const handleBrowserCall = (item: any) => {
  // TODO: support browser_automation_preview_call schema
  const callId = item.call_id;
  const argumentsStr = item.arguments;

  // Parse the arguments string into a dictionary
  let query = null;
  if (argumentsStr && typeof argumentsStr === "string") {
    try {
      const argumentsObj = JSON.parse(argumentsStr);
      query = argumentsObj.query;
    } catch (e) {
      console.error("Failed to parse arguments:", e);
    }
  }

  console.log(`Call ID: ${callId ?? "None"}`);
  console.log(`Query arguments: ${query ?? "None"}`);
};

export async function main(): Promise<void> {
  // Create clients to call Foundry API
  const project = new AIProjectClient(PROJECT_ENDPOINT, new DefaultAzureCredential());
  const openai = project.getOpenAIClient();

  console.log("Creating a toolbox with the Browser Automation tool...");

  // 1. Add the Browser Automation tool to a toolbox. Using a toolbox is the recommended
  //    way to give agents tools. See /azure/foundry/agents/concepts/toolbox-overview
  const toolbox = await project.toolboxes.createVersion(
    "browser-automation-toolbox",
    [
      {
        type: "browser_automation_preview",
        browser_automation_preview: {
          connection: {
            project_connection_id: BROWSER_CONNECTION_ID,
          },
        },
      },
    ],
    { description: "Toolbox with the Browser Automation tool" },
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
  //    azd ai connection create browser-automation-toolbox-conn \
  //      --kind remote-tool \
  //      --target "<toolboxMcpUrl>" \
  //      --auth-type user-entra-token \
  //      --audience https://ai.azure.com
  const toolboxConnectionName = "browser-automation-toolbox-conn";

  // 4. Attach the toolbox to a prompt agent as an MCP tool.
  const agent = await project.agents.createVersion("MyAgent", {
    kind: "prompt",
    model: "gpt-4.1-mini",
    instructions: `You are an Agent helping with browser automation tasks. 
            You can answer questions, provide information, and assist with various tasks 
            related to web browsing using the Browser Automation tool available to you.`,
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

  console.log("\nSending browser automation request with streaming...");
  const streamResponse = await openai.responses.create(
    {
      input: `Your goal is to report the percent of Microsoft year-to-date stock price change.
            To do that, go to the website finance.yahoo.com.
            At the top of the page, you will find a search bar.
            Enter the value 'MSFT', to get information about the Microsoft stock price.
            At the top of the resulting page you will see a default chart of Microsoft stock price.
            Click on 'YTD' at the top of that chart, and report the percent value that shows up just below it.`,
      stream: true,
    },
    {
      body: {
        agent_reference: { name: agent.name, type: "agent_reference" },
        tool_choice: "required",
      },
    },
  );

  // Process the streaming response
  for await (const event of streamResponse) {
    if (event.type === "response.created") {
      console.log(`Follow-up response created with ID: ${event.response.id}`);
    } else if (event.type === "response.output_text.delta") {
      process.stdout.write(event.delta);
    } else if (event.type === "response.output_text.done") {
      console.log("\n\nFollow-up response done!");
    } else if (
      event.type === "response.output_item.done" ||
      event.type === "response.output_item.added"
    ) {
      const item = event.item as any;
      if (item.type === "browser_automation_preview_call") {
        handleBrowserCall(item);
      }
    } else if (event.type === "response.completed") {
      console.log("\nFollow-up completed!");
    }
  }

  // Clean up resources by deleting the agent version
  // This prevents accumulation of unused resources in your project
  console.log("\nCleaning up resources...");
  await project.agents.deleteVersion(agent.name, agent.version);
  console.log("Agent deleted");

  console.log("\nBrowser Automation sample completed!");
}

main().catch((err) => {
  console.error("The sample encountered an error:", err);
});
```

### What this code does

This example creates an agent version with the Browser Automation tool enabled, sends a prompt that requires tool usage, and processes streaming events, including browser automation call events, as they arrive.

### Required inputs

- A Foundry project endpoint and a browser automation connection ID. See [Configuration](#configuration) for details.

### Expected output

You see an "Agent created ..." message, streaming text output, and optionally, browser call details when the tool is invoked. The output varies based on the website content and model behavior.
:::zone-end

:::zone pivot="java"

## Use browser automation in a Java agent

Update these values in your Java agent after you create the toolbox:

- `projectEndpoint` — Your project endpoint.
- `toolboxMcpUrl` — The MCP endpoint for the toolbox version that contains the Browser Automation tool.
- `toolboxConnectionName` — The remote-tool project connection name for the toolbox endpoint.

Add the dependency to your `pom.xml`:

```xml
<dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-ai-agents</artifactId>
    <version>2.2.0</version>
</dependency>
```

> [!TIP]
> **Recommended:** For most agents, add the Browser Automation tool through a [toolbox](../../concepts/toolbox-overview.md) and attach the toolbox to your agent as an MCP tool. The Java SDK doesn't yet expose a toolbox creation API, so create the toolbox by using the [Python](?pivots=python), [REST API](?pivots=rest), [C#](?pivots=csharp), or [TypeScript](?pivots=typescript) example, or the [Foundry portal](../../how-to/tools/toolbox.md), and then reference its MCP endpoint from your Java agent as an `McpTool`.

:::zone-end

## Limitations

- **Trusted sites only**: Use this tool only with sites you trust. Avoid pages that prompt for credentials, payments, or other sensitive actions.
- **Page volatility**: Web pages can change at any time. Your agent might fail if the page layout, labels, or navigation flows change. Build error handling into your workflows.
- **Complex single-page applications**: JavaScript-heavy SPAs with dynamic content might not render correctly.

## Cost considerations

This tool uses a Playwright workspace resource to run browser sessions. Review the Playwright workspace documentation for pricing and usage details. For guidance on optimizing tool usage, see [Best practices for using tools in Microsoft Foundry Agent Service](../../concepts/tool-best-practice.md).

## Troubleshooting

### The agent doesn't use the tool

- Confirm you created the agent with the Browser Automation tool enabled.
- In your request, require tool usage (for example, `tool_choice="required"`).
- Use tracing in Microsoft Foundry to confirm whether a tool call occurred. For guidance, see [Best practices for using tools in Microsoft Foundry Agent Service](../../concepts/tool-best-practice.md).

### Connection or authorization errors

- Confirm the browser automation connection ID matches the Playwright workspace connection resource ID in your project.
- Confirm the project identity has access to the Playwright workspace resource.
- If you recently rotated the Playwright access token, update the Foundry project connection key.

:::zone pivot="python"

### Python SDK errors

- **Workspace not found**: Verify your project endpoint uses the correct format: `https://{account-name}.services.ai.azure.com/api/projects/{project-name}`. Don't use the legacy Azure ML endpoint format.
- **Unexpected keyword argument errors**: Ensure you're using the latest version of `azure-ai-projects`. Run `pip install "azure-ai-projects>=2.0.0" --upgrade` to update.
- **Import errors**: Install all required packages: `pip install "azure-ai-projects>=2.0.0"`.

:::zone-end

### Requests time out

Browser automation can take longer than typical requests.

- Increase the client timeout (the C# sample sets a 5-minute timeout).
- Reduce the scope of your prompt (for example, fewer pages and fewer interactions).

## Clean up

- Delete the agent version you created for testing.
- Revoke or rotate the Playwright access token if you no longer need it.
- Remove the project connection if it’s no longer required. For more information, see [Add a connection in Microsoft Foundry](../../../how-to/connections-add.md).

## Example scenarios

- Form filling: Handles diverse form types with validation, DOM, authentication, compliance, and supporting multi-turn reasoning.

- Web scraping: Navigates authenticated sites to scrape, compare, and structure data across sources.

## Transparency note

Review the [transparency note](../../../responsible-ai/agents/transparency-note.md) when using this tool. The Browser Automation tool is a tool that can perform real-world browser tasks through natural language prompts, enabling automated browsing activities without human intervention.

Review the [responsible AI considerations](../../../responsible-ai/agents/transparency-note.md) when using this tool.

## Related content

- [Best practices for using tools in Microsoft Foundry Agent Service](../../concepts/tool-best-practice.md)
- [Computer use tool for agents](computer-use.md)
- [Add a connection in Microsoft Foundry](../../../how-to/connections-add.md)
- [Quickstart: Create your first agent](../../../quickstarts/get-started-code.md)
