---
title: Automate browser tasks with Foundry agents
titleSuffix: Microsoft Foundry
description: Automate web browsing tasks with the Browser Automation tool in Microsoft Foundry agents. Create isolated Playwright sessions for navigation and form filling.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.date: 02/04/2026
author: alvinashcraft
ms.author: aashcraft
ms.custom: azure-ai-agents, dev-focus, pilot-ai-workflow-jan-2026
ai-usage: ai-assisted
zone_pivot_groups: selection-browser-tool
#CustomerIntent: As a developer building AI agents, I want to automate web browsing tasks so that my agents can interact with external websites and extract information.
---

# Automate browser tasks with the Browser Automation tool (preview)

[!INCLUDE [feature-preview](../../../../includes/feature-preview.md)]

This article explains how to configure and use the Browser Automation tool with Foundry agents to automate web browsing workflows.

> [!WARNING]
> The Browser Automation tool comes with significant security risks. Both errors in judgment by the AI and the presence of malicious or confusing instructions on web pages that the AI encounters can cause it to execute commands you or others don't intend. These actions can compromise the security of your or other users' browsers, computers, and any accounts to which the browser or AI has access, including personal, financial, or enterprise systems. By using the Browser Automation tool, you acknowledge that you bear responsibility and liability for any use of it and of any resulting agents you create with it. This responsibility extends to any other users to whom you make Browser Automation tool functionality available, including through resulting agents. Use the Browser Automation tool on low-privilege virtual machines with no access to sensitive data or critical resources.

For guidance on optimizing tool usage, see [Best practices for using tools in Microsoft Foundry Agent Service](../../concepts/tool-best-practice.md).

In Microsoft Foundry, the Browser Automation tool enables you to perform real-world browser tasks through natural language prompts. When you use it with Foundry Agent Service, it creates isolated browser sessions in your provisioned Playwright workspace.

By using [Microsoft Playwright Workspaces](https://aka.ms/pww/docs/manage-workspaces), you can automate browser-based workflows such as searching, navigating, filling forms, and booking.

### Usage support

| Microsoft Foundry support | Python SDK | C# SDK | JavaScript SDK | Java SDK | REST API | Basic agent setup | Standard agent setup |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ✔️ | ✔️ | ✔️ | ✔️ | - | ✔️ | ✔️ | ✔️ |

## How it works

The interaction starts when the user sends a query to an agent connected to the Browser Automation tool. For example, *"Show me all available yoga classes this week from the following URL \<url\>."* When the agent receives the request, Foundry Agent Service creates an isolated browser session using your provisioned Playwright workspace. Each session is sandboxed for privacy and security.

The browser performs Playwright-driven actions, such as navigating to relevant pages and applying filters or parameters based on user preferences (such as time, location, and instructor). By combining the model with Playwright, the model can parse HTML or XML into DOM documents, make decisions, and perform actions like selecting UI elements, typing, and navigating websites. Exercise caution when using this tool.

An example flow is:

1. A user sends a request to the model that includes a call to the Browser Automation tool with the URL you want to go to.
1. The Browser Automation tool receives a response from the model. If the response has action items, those items contain suggested actions to make progress toward the specified goal. For example, an action might be a screenshot so the model can assess the current state with an updated screenshot or click with X/Y coordinates indicating where the mouse should be moved.
1. The Browser Automation tool executes the action in a sandboxed environment.
1. After executing the action, the Browser Automation tool captures the updated state of the environment as a screenshot.
1. The tool sends a new request with the updated state, and repeats this loop until the model stops requesting actions or the user decides to stop.

   The Browser Automation tool supports multi-turn conversations, allowing the user to refine their request and complete a booking.

## Prerequisites

Before you begin, make sure you have:

- An Azure subscription. [Create one for free](https://azure.microsoft.com/free/).
- Contributor or Owner role on a resource group.
- A Foundry project with a configured endpoint.
- An AI model deployed in your project (for example, `gpt-4o`).
- A Playwright workspace resource.
- A project connection set up for your Playwright workspace.

### SDK requirements

For Python examples, install the required packages:

```bash
pip install azure-ai-projects azure-identity python-dotenv
```

For the latest features, you might need the prerelease version:

```bash
pip install azure-ai-projects --pre --upgrade
```

### Environment variables

For the SDK examples, set these environment variables:

| Variable | Description | Format |
|----------|-------------|--------|
| `FOUNDRY_PROJECT_ENDPOINT` | Your Foundry project endpoint URL | `https://{account-name}.services.ai.azure.com/api/projects/{project-name}` |
| `FOUNDRY_MODEL_DEPLOYMENT_NAME` | Your deployed model name | `gpt-4o` |
| `BROWSER_AUTOMATION_PROJECT_CONNECTION_ID` | The connection resource ID | See the format that follows |

**Get your project endpoint**: Open your project in the [Foundry portal](https://ai.azure.com), and copy the endpoint from the project overview page.

**Connection ID format**: Use `/subscriptions/{{subscriptionID}}/resourceGroups/{{resourceGroupName}}/providers/Microsoft.CognitiveServices/accounts/{{foundryAccountName}}/projects/{{foundryProjectName}}/connections/{{foundryConnectionName}}`. You can find this value on the tool's details page after you connect the Browser Automation tool.

## Set up Browser Automation

### Step 1: Create a Playwright workspace

1. In the [Azure portal](https://portal.azure.com), create a [Playwright Workspace](https://aka.ms/pww/docs/manage-workspaces) resource.
1. After the workspace is created, go to **Settings** > **Access Management**.
1. Confirm the **Playwright Service Access Token** authentication method is enabled.
1. Select **Generate Token**, enter a name (for example, `foundry-connection`), and choose an expiry period.
1. **Copy the token immediately**. You can't view it again after closing the page.
1. On the workspace **Overview** page, copy the **Browser endpoint** (it starts with `wss://`).
1. Give the project identity a Contributor role on the Playwright workspace resource, or [configure a custom role](https://aka.ms/pww/docs/manage-workspace-access).

### Step 2: Connect the Browser Automation tool in Foundry

1. Go to the [Foundry portal](https://ai.azure.com/nextgen) and select your project.
1. Select **Build** > **Tools**.
1. Select **Connect a tool**.
1. In the **Configured** tab, select **Browser Automation**, then select **Add tool**.
1. Fill in the required fields:
   - **Name**: A unique name for your connection.
   - **Playwright workspace region endpoint**: Paste the `wss://` endpoint you copied.
   - **Access token**: Paste the access token you generated.
1. Select **Connect**.

After the connection is created, you can view the **Project connection ID** on the tool's details page. Use this value for the `BROWSER_AUTOMATION_PROJECT_CONNECTION_ID` environment variable.

## Code example

After you run a sample, verify the tool was called by using tracing in Microsoft Foundry. For guidance on validating tool invocation, see [Best practices for using tools in Microsoft Foundry Agent Service](../../concepts/tool-best-practice.md). If you use streaming, you can also look for `browser_automation_preview_call` events.

> [!NOTE]
> - You need the latest prerelease package. For more information, see the [quickstart](../../../../quickstarts/get-started-code.md?view=foundry&preserve-view=true).
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

connection_id = os.environ["BROWSER_AUTOMATION_PROJECT_CONNECTION_ID"]

tool = BrowserAutomationAgentTool(
    browser_automation_preview=BrowserAutomationToolParameters(
        connection=BrowserAutomationToolConnectionParameters(
            project_connection_id=connection_id,
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

When you create the agent, you see output similar to:

```console
Agent created (id: ..., name: ..., version: ...)
```

During streaming, you might also see deltas and tool-call details. Output varies based on the website content and model behavior.
:::zone-end

:::zone pivot="csharp"
## Use BrowserAutomationAgentTool with agents example

Before running this sample, complete the setup steps in [Set up Browser Automation](#set-up-browser-automation).

The following C# example demonstrates how to create an AI agent with Browser Automation capabilities by using the `BrowserAutomationAgentTool` and synchronous Azure AI Projects client. The agent can navigate to websites, interact with web elements, and perform tasks such as searching for stock prices. The example uses synchronous programming model for simplicity. For an asynchronous version, see the [Sample for use of BrowserAutomationAgentTool and Agents](https://github.com/Azure/azure-sdk-for-net/blob/feature/ai-foundry/agents-v2/sdk/ai/Azure.AI.Projects.OpenAI/samples/Sample23_BrowserAutomationTool.md) sample in the Azure SDK for .NET repository on GitHub.

```csharp
// Create the Agent client and read the required environment variables.
// Note that Browser automation operations can take longer than usual
// and require the request timeout to be at least 5 minutes.
var projectEndpoint = System.Environment.GetEnvironmentVariable("FOUNDRY_PROJECT_ENDPOINT");
var modelDeploymentName = System.Environment.GetEnvironmentVariable("FOUNDRY_MODEL_DEPLOYMENT_NAME");
var playwrightConnectionId = System.Environment.GetEnvironmentVariable("BROWSER_AUTOMATION_PROJECT_CONNECTION_ID");
AIProjectClientOptions options = new()
{
    NetworkTimeout = TimeSpan.FromMinutes(5)
};
AIProjectClient projectClient = new(endpoint: new Uri(projectEndpoint), tokenProvider: new DefaultAzureCredential(), options: options);

// Create the Browser Automation tool using the Playwright connection.
BrowserAutomationPreviewTool playwrightTool = new(
    new BrowserAutomationToolParameters(
    new BrowserAutomationToolConnectionParameters(playwrightConnectionId)
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

// Create the response stream. Also set ToolChoice = ResponseToolChoice.CreateRequiredChoice()
// on the ResponseCreationOptions to ensure the agent uses the Browser Automation tool.
ProjectResponsesClient responseClient = projectClient.OpenAI.GetProjectResponsesClientForAgent(agentVersion.Name);
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
projectClient.Agents.DeleteAgentVersion(agentName: agentVersion.Name, agentVersion: agentVersion.Version);
```

### What this code does

This example creates an agent version with the Browser Automation tool enabled, sends a prompt that requires tool usage, and prints streaming updates as the agent works through the browser steps.

### Required inputs

- Environment variables: `FOUNDRY_PROJECT_ENDPOINT`, `FOUNDRY_MODEL_DEPLOYMENT_NAME`, `BROWSER_AUTOMATION_PROJECT_CONNECTION_ID`.
- A Playwright connection created in your Foundry project.

### Expected output

You see streaming progress messages, such as text deltas, and a completed response. The output varies based on the website content and model behavior.
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
const deploymentName = process.env["FOUNDRY_MODEL_DEPLOYMENT_NAME"] || "<model deployment name>";
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

This example creates an agent version with the Browser Automation tool enabled, sends a prompt that requires tool usage, and processes streaming events, including browser automation call events, as they arrive.

### Required inputs

- Environment variables: `FOUNDRY_PROJECT_ENDPOINT`, `FOUNDRY_MODEL_DEPLOYMENT_NAME`, `BROWSER_AUTOMATION_PROJECT_CONNECTION_ID`.

### Expected output

You see an "Agent created ..." message, streaming text output, and optionally, browser call details when the tool is invoked. The output varies based on the website content and model behavior.
:::zone-end

## Limitations

- **Trusted sites only**: Use this tool only with sites you trust. Avoid pages that prompt for credentials, payments, or other sensitive actions.
- **Page volatility**: Web pages can change at any time. Your agent might fail if the page layout, labels, or navigation flows change. Build error handling into your workflows.
- **Complex single-page applications**: JavaScript-heavy SPAs with dynamic content might not render correctly.

## Cost considerations

This tool uses a Playwright workspace resource to run browser sessions. Review the Playwright workspace documentation for pricing and usage details.

## Troubleshooting

### The agent doesn't use the tool

- Confirm you created the agent with the Browser Automation tool enabled.
- In your request, require tool usage (for example, `tool_choice="required"`).
- Use tracing in Microsoft Foundry to confirm whether a tool call occurred. For guidance, see [Best practices for using tools in Microsoft Foundry Agent Service](../../concepts/tool-best-practice.md).

### Connection or authorization errors

- Confirm `BROWSER_AUTOMATION_PROJECT_CONNECTION_ID` matches the Playwright workspace connection resource ID in your project.
- Confirm the project identity has access to the Playwright workspace resource.
- If you recently rotated the Playwright access token, update the Foundry project connection key.

:::zone pivot="python"

### Python SDK errors

- **Workspace not found**: Verify your `FOUNDRY_PROJECT_ENDPOINT` uses the correct format: `https://{account-name}.services.ai.azure.com/api/projects/{project-name}`. Don't use the legacy Azure ML endpoint format.
- **Unexpected keyword argument errors**: Ensure you're using the latest version of `azure-ai-projects`. Run `pip install azure-ai-projects --pre --upgrade` to update.
- **Import errors**: Install all required packages: `pip install azure-ai-projects azure-identity python-dotenv`.

:::zone-end

### Requests time out

Browser automation can take longer than typical requests.

- Increase the client timeout (the C# sample sets a 5-minute timeout).
- Reduce the scope of your prompt (for example, fewer pages and fewer interactions).

## Clean up

- Delete the agent version you created for testing.
- Revoke or rotate the Playwright access token if you no longer need it.
- Remove the project connection if it’s no longer required. For more information, see [Add a connection in Microsoft Foundry](../../../../how-to/connections-add.md).


## Example scenarios

- Booking and reservations: Automate form filling and schedule confirmation across booking portals.

- Product discovery: Navigate ecommerce or review sites, search by criteria, and extract summaries.

## Transparency note

Review the [transparency note](../../../../responsible-ai/agents/transparency-note.md#enabling-autonomous-actions-with-or-without-human-input-through-action-tools) when using this tool. The Browser Automation tool is a tool that can perform real-world browser tasks through natural language prompts, enabling automated browsing activities without human intervention.

Review the [responsible AI considerations](../../../../responsible-ai/agents/transparency-note.md#considerations-when-choosing-a-use-case) when using this tool.

## Related content

- [Best practices for using tools in Microsoft Foundry Agent Service](../../concepts/tool-best-practice.md)
- [Computer use tool for agents](computer-use.md)
- [Add a connection in Microsoft Foundry](../../../../how-to/connections-add.md)
- [Quickstart: Create your first agent](../../../../quickstarts/get-started-code.md)
