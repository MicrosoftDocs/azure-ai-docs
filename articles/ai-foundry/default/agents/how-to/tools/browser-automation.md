---
title: Use Browser Automation Tool with Foundry agents
titleSuffix: Microsoft Foundry
description: Learn to use the Browser Automation tool with Microsoft Foundry agents to automate web tasks in Playwright workspaces. Follow the steps to get started.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.date: 12/12/2025
author: alvinashcraft
ms.author: aashcraft
ms.custom: azure-ai-agents, dev-focus
ai-usage: ai-assisted
zone_pivot_groups: selection-browser-tool
---

# Browser automation tool (preview)

[!INCLUDE [feature-preview](../../../../includes/feature-preview.md)]

> [!WARNING]
> The Browser Automation tool comes with significant security risks. Both errors in judgment by the AI and the presence of malicious or confusing instructions on web pages which the AI encounters may cause it to execute commands you or others do not intend, which could compromise the security of your or other users' browsers, computers, and any accounts to which the browser or AI has access, including personal, financial, or enterprise systems. By using the Browser Automation tool, you are acknowledging that you bear responsibility and liability for any use of it and of any resulting agents you create with it, including with respect to any other users to whom you make Browser Automation tool functionality available, including through resulting agents. We strongly recommend using the Browser Automation tool on low-privilege virtual machines with no access to sensitive data or critical resources.

> [!NOTE]
> For information on optimizing tool usage, see [best practices](../../concepts/tool-best-practice.md).

In Microsoft Foundry, the Browser Automation tool enables you to perform real-world browser tasks through natural language prompts. When you use it with Foundry Agent Service, it creates isolated browser sessions in your provisioned Playwright workspace.

By using [Microsoft Playwright Workspaces](/azure/playwright-testing/overview-what-is-microsoft-playwright-testing), you can automate browser-based workflows such as searching, navigating, filling forms, and booking.

### Usage support

| Microsoft Foundry support | Python SDK | C# SDK | JavaScript SDK | Java SDK | REST API | Basic agent setup | Standard agent setup |
|---------|---------|---------|---------|---------|---------|---------|---------|
| ✔️ | ✔️ | ✔️ | ✔️ | - | ✔️ | ✔️ | ✔️ |

## Prerequisites

Before you begin, make sure you have:

- An Azure subscription with the right permissions.
- A Foundry project with a configured endpoint.
- An AI model deployed in your project.
- A Playwright workspace resource.
- Azure RBAC role: Contributor or Owner on the Foundry project. [TO VERIFY]
- Azure RBAC role: Contributor on the Playwright workspace resource (or an equivalent custom role).
- A project connection set up for your Playwright workspace.

For the SDK examples, set these environment variables:

- `FOUNDRY_PROJECT_ENDPOINT`: Your Foundry project endpoint URL.
- `FOUNDRY_MODEL_DEPLOYMENT_NAME`: Your deployed model name.
- `BROWSER_AUTOMATION_PROJECT_CONNECTION_ID`: The connection resource ID for the Playwright workspace connection.

Your connection ID should be in the following format: `/subscriptions/{{subscriptionID}}/resourceGroups/{{resourceGroupName}}/providers/Microsoft.CognitiveServices/accounts/{{foundryAccountName}}/projects/{{foundryProjectName}}/connections/{{foundryConnectionName}}`.

## Set up Browser Automation

1. Create a [Playwright Workspace](https://aka.ms/pww/docs/manage-workspaces) resource.

  1. [Generate an access token](https://aka.ms/pww/docs/manage-access-tokens) for the Playwright workspace resource.
  1. Copy the workspace region endpoint from the **Workspace Details** page.
  1. Give the project identity a Contributor role on the Playwright workspace resource, or [configure a custom role](https://aka.ms/pww/docs/manage-workspace-access).

1. Create a serverless connection in your Foundry project using the Playwright workspace region endpoint and Playwright workspace access token.

  1. Go to the [Foundry portal](https://ai.azure.com/) and select your project.
  1. Select **Management center**, then select **Connected resources**.
  1. Create a new **Serverless Model** connection.
  1. Set **Target URI** to the Playwright workspace region endpoint. It starts with `wss://`.

    For more information, see the Playwright documentation for [configuring the service endpoint](https://aka.ms/pww/docs/configure-service-endpoint).

  1. Set **Key** to your Playwright access token.

## Code example

> [!NOTE]
> - You need the latest prerelease package. For more information, see the [quickstart](../../../../quickstarts/get-started-code.md?view=foundry&preserve-view=true#install-and-authenticate).
> - This article assumes you already created the Playwright workspace connection. See the prerequisites section.

:::zone pivot="python"
## Use BrowserAutomationAgentTool with agents example

The following Python example demonstrates how to create an AI agent with browser automation capabilities by using the `BrowserAutomationAgentTool` and synchronous Azure AI Projects client. The agent can navigate to websites, interact with web elements, and perform tasks such as searching for stock prices. For a complete working example, ensure you have the necessary environment variables set up as indicated in the code comments.

```python
import os
import json
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    PromptAgentDefinition,
    BrowserAutomationAgentTool,
    BrowserAutomationToolParameters,
    BrowserAutomationToolConnectionParameters,
)

load_dotenv()

project_client = AIProjectClient(
    endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

openai_client = project_client.get_openai_client()

tool = BrowserAutomationAgentTool(
    browser_automation_preview=BrowserAutomationToolParameters(
        connection=BrowserAutomationToolConnectionParameters(
            project_connection_id=os.environ["BROWSER_AUTOMATION_PROJECT_CONNECTION_ID"],
        )
    )
)

with project_client:
    agent = project_client.agents.create_version(
        agent_name="MyAgent",
        definition=PromptAgentDefinition(
            model=os.environ["FOUNDRY_MODEL_DEPLOYMENT_NAME"],
            instructions="""You are an Agent helping with browser automation tasks. 
            You can answer questions, provide information, and assist with various tasks 
            related to web browsing using the Browser Automation tool available to you.""",
            tools=[tool],
        ),
    )
    print(f"Agent created (id: {agent.id}, name: {agent.name}, version: {agent.version})")

    stream_response = openai_client.responses.create(
        stream=True,
        tool_choice="required",
        input="""
            Your goal is to report the percent of Microsoft year-to-date stock price change.
            To do that, go to the website finance.yahoo.com.
            At the top of the page, you will find a search bar.
            Enter the value 'MSFT', to get information about the Microsoft stock price.
            At the top of the resulting page you will see a default chart of Microsoft stock price.
            Click on 'YTD' at the top of that chart, and report the percent value that shows up just below it.""",
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
            item = event.item
            if item.type == "browser_automation_preview_call":  # TODO: support browser_automation_preview_call schema
                arguments_str = getattr(item, "arguments", "{}")

                # Parse the arguments string into a dictionary
                arguments = json.loads(arguments_str)
                query = arguments.get("query")

                print(f"Call ID: {getattr(item, 'call_id')}")
                print(f"Query arguments: {query}")
        elif event.type == "response.completed":
            print(f"\nFollow-up completed!")
            print(f"Full response: {event.response.output_text}")
```

### What this code does

This example creates an agent version with the Browser Automation tool enabled, then sends a prompt that requires the agent to use the tool. It also processes streaming events so you can observe progress and tool calls.

### Required inputs

- Environment variables: `FOUNDRY_PROJECT_ENDPOINT`, `FOUNDRY_MODEL_DEPLOYMENT_NAME`, `BROWSER_AUTOMATION_PROJECT_CONNECTION_ID`.

### Expected output

When the agent is created, you see output similar to:

```console
Agent created (id: ..., name: ..., version: ...)
```

During streaming, you might also see deltas and tool-call details. Output varies based on the website content and model behavior.
:::zone-end

:::zone pivot="csharp"
## Use BrowserAutomationAgentTool with agents example

[Playwright](https://playwright.dev/) is a Node.js library for browser automation. Microsoft provides the [Azure Playwright workspace](/javascript/api/overview/azure/playwright-readme), which can execute Playwright-based tasks triggered by an agent using the BrowserAutomationAgentTool.

### Create Azure Playwright workspace

1. Deploy an Azure Playwright workspace.
1. In the **Get started** section, open **2. Set up authentication**.
1. **Select Service Access Token**, and then choose **Generate Token**.
   
   > [!IMPORTANT]
   > Save the token immediately. After you close the page, you can't view it again.

### Configure Microsoft Foundry

1. On the left panel, select **Management center**.
1. Choose **Connected resources**.
1. Create a new connection of type **Serverless Model**.
1. Provide a name, and then paste your Access Token into the **Key** field.
1. Set the Playwright Workspace Browser endpoint as the **Target URI**. You can find this endpoint on the Workspace **Overview page**. It begins with `wss://`.

### Create the sample

The following C# example demonstrates how to create an AI agent with Browser Automation capabilities by using the `BrowserAutomationAgentTool` and synchronous Azure AI Projects client. The agent can navigate to websites, interact with web elements, and perform tasks such as searching for stock prices. The example uses synchronous programming model for simplicity. For an asynchronous version, see the [Sample for use of BrowserAutomationAgentTool and Agents](https://github.com/Azure/azure-sdk-for-net/blob/feature/ai-foundry/agents-v2/sdk/ai/Azure.AI.Projects.OpenAI/samples/Sample23_BrowserAutomationTool.md) sample in the Azure SDK for .NET repository on GitHub.

```csharp
// Create the Agent client and read the required environment variables.
// Note that Browser automation operations can take longer than usual
// and require the request timeout to be at least 5 minutes.
var projectEndpoint = System.Environment.GetEnvironmentVariable("PROJECT_ENDPOINT");
var modelDeploymentName = System.Environment.GetEnvironmentVariable("MODEL_DEPLOYMENT_NAME");
var playwrightConnectionName = System.Environment.GetEnvironmentVariable("PLAYWRIGHT_CONNECTION_NAME");
AIProjectClientOptions options = new()
{
    NetworkTimeout = TimeSpan.FromMinutes(5)
};
AIProjectClient projectClient = new(endpoint: new Uri(projectEndpoint), tokenProvider: new DefaultAzureCredential(), options: options);

// Create the Browser Automation tool using the Playwright connection.
AIProjectConnection playwrightConnection = projectClient.Connections.GetConnection(playwrightConnectionName);
BrowserAutomationAgentTool playwrightTool = new(
    new BrowserAutomationToolParameters(
        new BrowserAutomationToolConnectionParameters(playwrightConnection.Id)
    ));

// Create the Agent version with the Browser Automation tool.
PromptAgentDefinition agentDefinition = new(model: modelDeploymentName)
{
    Instructions = "You are an Agent helping with browser automation tasks.\n" +
    "You can answer questions, provide information, and assist with various tasks\n" +
    "related to web browsing using the Browser Automation tool available to you.",
    Tools = { playwrightTool }
};
AgentVersion agentVersion = projectClient.Agents.CreateAgentVersion(
    agentName: "myAgent",
    options: new(agentDefinition));

// To parse the stream obtained from the Agent, create a ParseResponse helper method.
private static void ParseResponse(StreamingResponseUpdate streamResponse)
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
        Console.WriteLine($"Response done with full message: {textDoneUpdate.Text}");
    }
    else if (streamResponse is StreamingResponseErrorUpdate errorUpdate)
    {
        throw new InvalidOperationException($"The stream has failed with the error: {errorUpdate.Message}");
    }
}

// Create the response stream. Also set ToolChoice = ResponseToolChoice.CreateRequiredChoice()
// on the ResponseCreationOptions to ensure the agent uses the Browser Automation tool.
ProjectResponsesClient responseClient = projectClient.OpenAI.GetProjectResponsesClientForAgent(agentVersion.Name);
ResponseCreationOptions responseOptions = new()
{
    ToolChoice = ResponseToolChoice.CreateRequiredChoice()
};
foreach (StreamingResponseUpdate update in responseClient.CreateResponseStreaming(
        userInputText: "Your goal is to report the percent of Microsoft year-to-date stock price change.\n" +
        "To do that, go to the website finance.yahoo.com.\n" +
        "At the top of the page, you will find a search bar.\n" +
        "Enter the value 'MSFT', to get information about the Microsoft stock price.\n" +
        "At the top of the resulting page you will see a default chart of Microsoft stock price.\n" +
        "Click on 'YTD' at the top of that chart, and report the percent value that shows up just below it.",
        options: responseOptions))
{
    ParseResponse(update);
}

// Delete the Agent version to clean up resources.
projectClient.Agents.DeleteAgentVersion(agentName: agentVersion.Name, agentVersion: agentVersion.Version);
```

### What this code does

This example creates an agent version with the Browser Automation tool enabled, sends a prompt that requires tool usage, and prints streaming updates as the agent works through the browser steps.

### Required inputs

- Environment variables: `PROJECT_ENDPOINT`, `MODEL_DEPLOYMENT_NAME`, `PLAYWRIGHT_CONNECTION_NAME`.
- A Playwright connection created in your Foundry project.

### Expected output

You see streaming progress messages (for example, text deltas) and a completed response. Output varies based on the website content and model behavior.
:::zone-end

:::zone pivot="rest"
The following cURL sample demonstrates how to create an agent with Browser Automation tool and perform web browsing tasks using REST API.

```bash
curl --request POST \
  --url "${FOUNDRY_PROJECT_ENDPOINT}/openai/responses?api-version=${API_VERSION}" \
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
      "type": "browser_automation_preview",
      "browser_automation_preview": {
        "connection": {
          "project_connection_id": "${BROWSER_AUTOMATION_PROJECT_CONNECTION_ID}"
        }
      }
    }
  ]
}
JSON
```
:::zone-end

:::zone pivot="typescript"
## Use Browser Automation tool with agents example

The following TypeScript sample demonstrates how to create an agent with Browser Automation tool, perform web browsing tasks, and process streaming responses with browser automation events. For a JavaScript version of this sample, see the [JavaScript sample for Browser Automation tool](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/ai/ai-projects/samples/v2-beta/javascript/agents/tools/agentBrowserAutomation.js) in the Azure SDK for JavaScript repository on GitHub.

```typescript
import { DefaultAzureCredential } from "@azure/identity";
import { AIProjectClient } from "@azure/ai-projects";
import "dotenv/config";

const projectEndpoint = process.env["FOUNDRY_PROJECT_ENDPOINT"] || "<project endpoint>";
const deploymentName = process.env["MODEL_DEPLOYMENT_NAME"] || "<model deployment name>";
const browserAutomationProjectConnectionId =
  process.env["BROWSER_AUTOMATION_PROJECT_CONNECTION_ID"] ||
  "<browser automation project connection id>";

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
  const project = new AIProjectClient(projectEndpoint, new DefaultAzureCredential());
  const openAIClient = await project.getOpenAIClient();

  console.log("Creating agent with Browser Automation tool...");

  const agent = await project.agents.createVersion("MyAgent", {
    kind: "prompt",
    model: deploymentName,
    instructions: `You are an Agent helping with browser automation tasks. 
            You can answer questions, provide information, and assist with various tasks 
            related to web browsing using the Browser Automation tool available to you.`,
    // Define Browser Automation tool
    tools: [
      {
        type: "browser_automation_preview",
        browser_automation_preview: {
          connection: {
            project_connection_id: browserAutomationProjectConnectionId,
          },
        },
      },
    ],
  });
  console.log(`Agent created (id: ${agent.id}, name: ${agent.name}, version: ${agent.version})`);

  console.log("\nSending browser automation request with streaming...");
  const streamResponse = await openAIClient.responses.create(
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
        agent: { name: agent.name, type: "agent_reference" },
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

This example creates an agent version with the Browser Automation tool enabled, sends a prompt that requires tool usage, and processes streaming events (including browser automation call events) as they arrive.

### Required inputs

- Environment variables: `FOUNDRY_PROJECT_ENDPOINT`, `MODEL_DEPLOYMENT_NAME`, `BROWSER_AUTOMATION_PROJECT_CONNECTION_ID`.

### Expected output

You see an "Agent created ..." message, streaming text output, and (optionally) browser call details when the tool is invoked. Output varies based on the website content and model behavior.
:::zone-end

## How it works

The interaction starts when the user sends a query to an agent connected to the Browser Automation tool. For example, *"Show me all available yoga classes this week from the following URL <url>."* When the agent receives the request, Foundry Agent Service creates an isolated browser session using your provisioned Playwright workspace. Each session is sandboxed for privacy and security.

The browser performs Playwright-driven actions, such as navigating to relevant pages and applying filters or parameters based on user preferences (such as time, location, and instructor). By combining the model with Playwright, the model can parse HTML or XML into DOM documents, make decisions, and perform actions like selecting UI elements, typing, and navigating websites. Exercise caution when using this tool.

An example flow is:

1. A user sends a request to the model that includes a call to the Browser Automation tool with the URL you want to go to.

1. The Browser Automation tool receives a response from the model. If the response has action items, those items contain suggested actions to make progress toward the specified goal. For example, an action might be a screenshot so the model can assess the current state with an updated screenshot or click with X/Y coordinates indicating where the mouse should be moved.

1. The Browser Automation tool executes the action in a sandboxed environment.

1. After executing the action, the Browser Automation tool captures the updated state of the environment as a screenshot.

1. The tool sends a new request with the updated state, and repeats this loop until the model stops requesting actions or the user decides to stop.

    The Browser Automation tool supports multi-turn conversations, allowing the user to refine their request and complete a booking.

## Example scenarios

- Booking and reservations: Automate form filling and schedule confirmation across booking portals.

- Product discovery: Navigate ecommerce or review sites, search by criteria, and extract summaries.

## Transparency note

Review the [transparency note](/azure/ai-foundry/responsible-ai/agents/transparency-note#enabling-autonomous-actions-with-or-without-human-input-through-action-tools) when using this tool. The Browser Automation tool is a tool that can perform real-world browser tasks through natural language prompts, enabling automated browsing activities without human intervention.

Review the [responsible AI considerations](/azure/ai-foundry/responsible-ai/agents/transparency-note#considerations-when-choosing-a-use-case) when using this tool.
