---
title: 'How to use Browser Automation tool for Microsoft Foundry agents'
titleSuffix: Microsoft Foundry
description: Learn how to automate browser tasks using Microsoft Foundry agents.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.date: 12/11/2025
author: alvinashcraft
ms.author: aashcraft
ms.custom: azure-ai-agents
zone_pivot_groups: selection-browser-tool
---

# Browser automation tool (preview)

[!INCLUDE [feature-preview](../../../../includes/feature-preview.md)]

> [!WARNING]
> The Browser Automation tool comes with significant security risks. Both errors in judgment by the AI and the presence of malicious or confusing instructions on web pages which the AI encounters may cause it to execute commands you or others do not intend, which could compromise the security of your or other users' browsers, computers, and any accounts to which the browser or AI has access, including personal, financial, or enterprise systems. By using the Browser Automation tool, you are acknowledging that you bear responsibility and liability for any use of it and of any resulting agents you create with it, including with respect to any other users to whom you make Browser Automation tool functionality available, including through resulting agents. We strongly recommend using the Browser Automation tool on low-privilege virtual machines with no access to sensitive data or critical resources.

> [!NOTE]
> For information on optimizing tool usage, see [best practices](../../concepts/tool-best-practice.md).

The Browser Automation tool enables you to perform real-world browser tasks through natural language prompts. By using [Microsoft Playwright Workspaces](/azure/playwright-testing/overview-what-is-microsoft-playwright-testing), it facilitates multistep conversations to automate browser-based workflows such as searching, navigating, filling forms, and booking.

## Code example

> [!NOTE]
> - You need the latest prerelease package. For more information, see the [quickstart](../../../../quickstarts/get-started-code.md?view=foundry&preserve-view=true#install-and-authenticate).
> - Your connection ID should be in the format of `/subscriptions/{{subscriptionID}}/resourceGroups/{{resourceGroupName}}/providers/Microsoft.CognitiveServices/accounts/{{foundryAccountName}}/projects/{{foundryProjectName}}/connections/{{foundryConnectionName}}`.

:::zone pivot="python"
The following Python example demonstrates how to create an AI agent with Browser Automation capabilities by using the `BrowserAutomationAgentTool` and synchronous Azure AI Projects client. The agent can navigate to websites, interact with web elements, and perform tasks such as searching for stock prices. For a complete working example, ensure you have the necessary environment variables set up as indicated in the code comments.

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
    endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
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
            model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
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
:::zone-end

:::zone pivot="rest"
The following cURL sample demonstrates how to create an agent with Browser Automation tool and perform web browsing tasks using REST API.

```bash
curl --request POST \
  --url "$AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/openai/responses?api-version=$API_VERSION" \
  --H "Authorization: Bearer $AGENT_TOKEN" \
  --H "Content-Type: application/json" \
  --H "User-Agent: insomnia/11.6.1" \
  --d '{
"model": "$AZURE_AI_MODEL_DEPLOYMENT_NAME",
"input": """
            Your goal is to report the percent of Microsoft year-to-date stock price change.
            To do that, go to the website finance.yahoo.com.
            At the top of the page, you will find a search bar.
            Enter the value 'MSFT', to get information about the Microsoft stock price.
            At the top of the resulting page you will see a default chart of Microsoft stock price.
            Click on 'YTD' at the top of that chart, and report the percent value that shows up just below it.""",
"tools": [
   {
   "type": "browser_automation_preview",
   "browser_automation_preview":
        {
            "connection": {
            "project_connection_id": "$BROWSER_AUTOMATION_PROJECT_CONNECTION_ID"
        }
    }
    ]
}'
```
:::zone-end

:::zone pivot="typescript"
The following TypeScript sample demonstrates how to create an agent with Browser Automation tool, perform web browsing tasks, and process streaming responses with browser automation events. For a JavaScript version of this sample, see the [JavaScript sample for Browser Automation tool](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/ai/ai-projects/samples/v2-beta/javascript/agents/tools/agentBrowserAutomation.js) in the Azure SDK for JavaScript repository on GitHub.

```typescript
import { DefaultAzureCredential } from "@azure/identity";
import { AIProjectClient } from "@azure/ai-projects";
import "dotenv/config";

const projectEndpoint = process.env["AZURE_AI_PROJECT_ENDPOINT"] || "<project endpoint>";
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
:::zone-end

## How it works

The interaction starts when the user sends a query to an agent connected to the Browser Automation tool. For example, *"Show me all available yoga classes this week from the following url \<url\>."* When the agent receives the request, Foundry Agent Service creates an isolated browser session using your own provisioned Playwright workspace. Each session is sandboxed for privacy and security. The browser session mimics a real user browsing experience, enabling interaction with complex web UIs (for example, class schedules, filters, or booking pages). The browser performs Playwright-driven actions, such as navigating to relevant pages, and applying filters or parameters based on user preferences (such as time, location, instructor). By combining the model with Playwright, the model can see the browser screen by parsing the HTML or XML pages into DOM documents, make decisions, and perform actions like clicking, typing, and navigating websites. You should exercise caution when using this tool.

An example flow is:

1. A user sends a request to the model that includes a call to the Browser Automation tool with the URL you want to go to.

1. The Browser Automation tool receives a response from the model. If the response has action items, those items contain suggested actions to make progress toward the specified goal. For example, an action might be a screenshot so the model can assess the current state with an updated screenshot or click with X/Y coordinates indicating where the mouse should be moved.

1. The Browser Automation tool executes the action in a sandboxed environment.

1. After executing the action, The Browser Automation tool captures the updated state of the environment as a screenshot.

1. The tool sends a new request with the updated state, and repeats this loop until the model stops requesting actions or the user decides to stop.

    The Browser Automation tool supports multi-turn conversations, allowing the user to refine their request and complete a booking.

## Example scenarios

- Booking and reservations: Automate form-filling and schedule confirmation across booking portals.

- Product discovery: Navigate ecommerce or review sites, search by criteria, and extract summaries.

## Setup

1. Create a [Playwright Workspace](https://aka.ms/pww/docs/manage-workspaces) resource.

    1. [Generate an access token](https://aka.ms/pww/docs/manage-access-tokens) for the Playwright Workspace resource. 
    
    1. Access the workspace region endpoint in the **Workspace Details** page.
    1. Give the project identity a "Contributor" role on the Playwright Workspace resource, or [configure a custom role](https://aka.ms/pww/docs/manage-workspace-access). 
    
1. Create a serverless connection in the Microsoft Foundry project with the Playwright workspace region endpoint and the Playwright workspace Access Token.

    1. Go to the [Foundry portal](https://ai.azure.com/) and select your project. Go to the **Management center** and select **connected resources**.

    1. Create a new **Serverless Model** connection, and enter the following information.

        * **Target URI**: The Playwright workspace region endpoint, for example `wss://{region}.api.playwright.microsoft.com/playwrightworkspaces/{workspaceId}/browsers`. The URI should start with `wss://` instead of `https://` if presented.

        For more information on getting this value, see the [PlayWright documentation](https://aka.ms/pww/docs/configure-service-endpoint).

        * **Key**: [Get the Playwright access token](https://aka.ms/pww/docs/generate-access-token).

1. Configure your client by adding a Browser Automation tool using the Azure Playwright connection ID.

## Transparency note

Review the [transparency note](/azure/ai-foundry/responsible-ai/agents/transparency-note#enabling-autonomous-actions-with-or-without-human-input-through-action-tools) when using this tool. The Browser Automation tool is a tool that can perform real-world browser tasks through natural language prompts, enabling automated browsing activities without human intervention.

Review the [responsible AI considerations](/azure/ai-foundry/responsible-ai/agents/transparency-note#considerations-when-choosing-a-use-case) when using this tool.
