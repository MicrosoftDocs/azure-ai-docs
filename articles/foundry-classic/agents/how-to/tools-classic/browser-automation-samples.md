---
title: Use the Browser Automation Tool in Foundry Agent Service
titleSuffix: Microsoft Foundry
description: Learn how to use the Browser Automation tool in Foundry Agent Service to automate website tasks with AI agents. Follow the steps and run the sample.
services: azure-ai-agent-service
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.date: 02/02/2026
author: alvinashcraft
ms.author: aashcraft
ms.custom: azure-ai-agents
ai-usage: ai-assisted
---

# How to use the Browser Automation tool (preview)

> [!NOTE]
> This article refers to the classic version of the agents API. 
>
> 🔍 [View the new Browser Automation documentation](../../../default/agents/how-to/tools/browser-automation.md?view=foundry&preserve-view=true).

Use this article to find step-by-step instructions and code samples for using the Browser Automation tool in the Foundry Agent Service. Note that Browser Automation is currently a preview feature.

## Prerequisites

* The requirements in the [Browser Automation overview](./browser-automation.md#setup).
* Your Microsoft Foundry Project endpoint.
    
  [!INCLUDE [endpoint-string-portal](../../includes/endpoint-string-portal.md)]

  Save this endpoint to an environment variable named `PROJECT_ENDPOINT`.

* The following packages. The `BrowserAutomationTool` class requires `azure-ai-agents` version 1.2.0b2 or later. Earlier versions don't include this tool, which causes the error "The tool 'browser_automation' is not supported."

  ```console
  pip install --pre azure-ai-agents>=1.2.0b2
  pip install azure-ai-projects
  pip install azure-identity
  ```

* The **Contributor** role assigned to your Foundry project from within your Playwright workplace. 
* Your Playwright connection ID. You can find it in the Foundry portal by selecting **Management center** from the left navigation menu. Then select **Connected resources**. The URI starts with `wss://` instead of `https://` if presented. 
    
  <!--
  :::image type="content" source="../../media/tools/deep-research/bing-resource-name.png" alt-text="A screenshot showing the Playwright connection. " lightbox="../../media/tools/deep-research/bing-resource-name.png":::
  -->
  Save this name to an environment variable named `AZURE_PLAYWRIGHT_CONNECTION_NAME`.

* [!INCLUDE [model-name-portal](../../includes/model-name-portal.md)]

  Save this name to an environment variable named `MODEL_DEPLOYMENT_NAME`.

## Example code

```python
import os
from azure.ai.projects import AIProjectClient
from azure.ai.agents.models import (
    MessageRole,
    RunStepToolCallDetails,
    BrowserAutomationTool,
    RunStepBrowserAutomationToolCall,
)
from azure.identity import DefaultAzureCredential

project_client = AIProjectClient(endpoint=os.environ["PROJECT_ENDPOINT"], credential=DefaultAzureCredential())

connection_id = os.environ["AZURE_PLAYWRIGHT_CONNECTION_ID"]

# Initialize Browser Automation tool and add the connection id
browser_automation = BrowserAutomationTool(connection_id=connection_id)

with project_client:

    agents_client = project_client.agents

    # Create a new Agent that has the Browser Automation tool attached.
    # Note: To add Browser Automation tool to an existing Agent with an `agent_id`, do the following:
    # agent = agents_client.update_agent(agent_id, tools=browser_automation.definitions)
    agent = agents_client.create_agent(
        model=os.environ["MODEL_DEPLOYMENT_NAME"],
        name="my-agent",
        instructions="""
            You are an Agent helping with browser automation tasks. 
            You can answer questions, provide information, and assist with various tasks 
            related to web browsing using the Browser Automation tool available to you.
            """,
        tools=browser_automation.definitions,
    )


    print(f"Created agent, ID: {agent.id}")

    # Create thread for communication
    thread = agents_client.threads.create()
    print(f"Created thread, ID: {thread.id}")

    # Create message to thread
    message = agents_client.messages.create(
        thread_id=thread.id,
        role=MessageRole.USER,
        content="""
            Your goal is to report the percent of Microsoft year-to-date stock price change.
            To do that, go to the website finance.yahoo.com.
            At the top of the page, you will find a search bar.
            Enter the value 'MSFT', to get information about the Microsoft stock price.
            At the top of the resulting page you will see a default chart of Microsoft stock price.
            Click on 'YTD' at the top of that chart, and report the percent value that shows up just below it.
            """,
    )
    print(f"Created message, ID: {message.id}")

    # Create and process agent run in thread with tools
    print(f"Waiting for Agent run to complete. Please wait...")
    run = agents_client.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)
    print(f"Run finished with status: {run.status}")

    if run.status == "failed":
        print(f"Run failed: {run.last_error}")

    # Fetch run steps to get the details of the agent run
    run_steps = agents_client.run_steps.list(thread_id=thread.id, run_id=run.id)
    for step in run_steps:
        print(f"Step {step.id} status: {step.status}")

        if isinstance(step.step_details, RunStepToolCallDetails):
            print("  Tool calls:")
            tool_calls = step.step_details.tool_calls

            for call in tool_calls:
                print(f"    Tool call ID: {call.id}")
                print(f"    Tool call type: {call.type}")

                if isinstance(call, RunStepBrowserAutomationToolCall):
                    print(f"    Browser automation input: {call.browser_automation.input}")
                    print(f"    Browser automation output: {call.browser_automation.output}")

                    print("    Steps:")
                    for tool_step in call.browser_automation.steps:
                        print(f"      Last step result: {tool_step.last_step_result}")
                        print(f"      Current state: {tool_step.current_state}")
                        print(f"      Next step: {tool_step.next_step}")
                        print()  # add an extra newline between tool steps

                print()  # add an extra newline between tool calls

        print()  # add an extra newline between run steps

    # Optional: Delete the agent once the run is finished.
    # Comment out this line if you plan to reuse the agent later.
    agents_client.delete_agent(agent.id)
    print("Deleted agent")

    # Print the Agent's response message with optional citation
    response_message = agents_client.messages.get_last_message_by_role(thread_id=thread.id, role=MessageRole.AGENT)
    if response_message:
        for text_message in response_message.text_messages:
            print(f"Agent response: {text_message.text.value}")
        for annotation in response_message.url_citation_annotations:
            print(f"URL Citation: [{annotation.url_citation.title}]({annotation.url_citation.url})")
```

## Visualize what the agent does

Browser Automation runs in your connected Microsoft Playwright Workspaces environment. It doesn't open a visible browser window inside your local development environment.

To visualize what happens, review the Browser Automation tool-call details that the run steps return:

- The sample prints each tool call and its step-by-step progress. For example, it shows `last_step_result`, `current_state`, and `next_step`.
- The tool captures a screenshot after actions during execution and includes the updated browser state in the tool output. Review the printed `current_state` for each step to see what the model sees at that point.

For more information, see the [How it works](./browser-automation.md#how-it-works) section in the **Browser Automation** overview article.
