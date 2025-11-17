---
title: 'How to use Browser Automation tool for Microsoft Foundry agents'
titleSuffix: Microsoft Foundry
description: Learn how to automate browser tasks using Microsoft Foundry agents.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.date: 11/13/2025
author: aahill
ms.author: aahi
ms.custom: azure-ai-agents
---

# Browser automation tool (preview)

> [!WARNING]
> The Browser Automation tool comes with significant security risks. Both errors in judgment by the AI and the presence of malicious or confusing instructions on web pages which the AI encounters may cause it to execute commands you or others do not intend, which could compromise the security of your or other users' browsers, computers, and any accounts to which the browser or AI has access, including personal, financial, or enterprise systems. By using the Browser Automation tool, you are acknowledging that you bear responsibility and liability for any use of it and of any resulting agents you create with it, including with respect to any other users to whom you make Browser Automation tool functionality available, including through resulting agents. We strongly recommend using the Browser Automation tool on low-privilege virtual machines with no access to sensitive data or critical resources.


The Browser Automation tool enables users to perform real-world browser tasks through natural language prompts. Powered by [Microsoft Playwright Workspaces](/azure/playwright-testing/overview-what-is-microsoft-playwright-testing), it facilitates multi-turn conversations to automate browser-based workflows such as searching, navigating, filling forms, and booking.

## Code example
> [!NOTE]
> You will need the latest prerelease package. See the [quickstart](../../../../quickstarts/get-started-code.md?view=foundry&preserve-view=true#install-and-authenticate) for details.

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


## How it works

The interaction begins when the user sends a user query to an agent connected to the Browser Automation tool. For example, *"Show me all available yoga classes this week from the following url \<url\>."* Upon receiving the request, Foundry Agent Service creates an isolated browser session using your own provisioned Playwright workspace. Each session is sandboxed for privacy and security. The browser session mimics a real user browsing experience, enabling interaction with complex web UIs (for example, class schedules, filters, or booking pages). The browser performs Playwright-driven actions, such as navigating to relevant pages, and applying filters or parameters based on user preferences (such as time, location, instructor). Combining the model with Playwright allows the model to see the browser screen by parsing the HTML or XML pages into DOM documents, make decisions, and perform actions like clicking, typing, and navigating websites. You should exercise caution when using this tool.

An example flow would be:

1. A user sends a request to the model that includes a call to the Browser Automation tool with the URL you want to go to.

1. The Browser Automation tool receives a response from the model. If the response has action items, those items contain suggested actions to make progress toward the specified goal. For example an action might be a screenshot so the model can assess the current state with an updated screenshot or click with X/Y coordinates indicating where the mouse should be moved.

1. The Browser Automation tool executes the action in a sandboxed environment.

1. After executing the action, The Browser Automation tool captures the updated state of the environment as a screenshot.

1. The tool sends a new request with the updated state, and repeats this loop until the model stops requesting actions or the user decides to stop.

    The Browser Automation tool supports multi-turn conversations, allowing the user to refine their request and complete a booking.

## Example scenarios:

- Booking & Reservations: Automate form-filling and schedule confirmation across booking portals.

- Product Discovery: Navigate ecommerce or review sites, search by criteria, and extract summaries.

## Setup

1. Create a [Playwright Workspace](https://aka.ms/pww/docs/manage-workspaces) resource.

    1. [Generate an access token](https://aka.ms/pww/docs/manage-access-tokens) for the Playwright Workspace resource. 
    
    1. Access the workspace region endpoint in the **Workspace Details** page.
    1. Give the project identity a "Contributor" role on the Playwright Workspace resource, or [configure a custom role](https://aka.ms/pww/docs/manage-workspace-access). 
    
1. Create a serverless connection in the Microsoft Foundry project with the Playwright workspace region endpoint and the Playwright workspace Access Token.

    1. Go to the [Foundry portal](https://ai.azure.com/) and select your project. Go to the **Management center** and select **connected resources**.

    1. Create a new **Serverless Model** connection, and enter the following information.

        * **Target URI**: The Playwright workspace region endpoint, for example `wss://{region}.api.playwright.microsoft.com/playwrightworkspaces/{workspaceId}/browsers`. The URI should start with `wss://` instead of `https://` if presented.

        For more information on getting this value, see the [PlayWright documentation](https://aka.ms/pww/docs/configure-service-endpoint)

        * **Key**: [Get the Playwright access token](https://aka.ms/pww/docs/generate-access-token)

1. Configure your client by adding a Browser Automation tool using the Azure Playwright connection ID.

## Transparency note

Review the [transparency note](/azure/ai-foundry/responsible-ai/agents/transparency-note#enabling-autonomous-actions-with-or-without-human-input-through-action-tools) when using this tool. The Browser Automation tool is a tool that can perform real-world browser tasks through natural language prompts, enabling automated browsing activities without human intervention.

Review the [responsible AI considerations](/azure/ai-foundry/responsible-ai/agents/transparency-note#considerations-when-choosing-a-use-case) when using this tool.
