---
title: How to use the browser automation tool with the Azure AI Foundry Agent Service
titleSuffix: Azure AI Foundry
description: Learn how to automate browser use and interact with websites using AI Agents.
services: azure-ai-agent-service
manager: nitinme
ms.service: azure-ai-agent-service
ms.topic: how-to
ms.date: 07/29/2025
author: aahill
ms.author: aahi
ms.custom: azure-ai-agents
---

# How to use the browser automation tool (preview)

Use this article to find step-by-step instructions and code samples for using the browser automation tool in the Azure AI Foundry Agent Service.

## Prerequisites

* The requirements in the [browser automation overview](./deep-research.md).
* Your Azure AI Foundry Project endpoint.
    
    [!INCLUDE [endpoint-string-portal](../../includes/endpoint-string-portal.md)]

    Save this endpoint to an environment variable named `PROJECT_ENDPOINT`.


[!INCLUDE [model-name-portal](../../includes/model-name-portal.md)]

    
* Your playwright connection ID. You can find it in the Azure AI Foundry portal by selecting **Management center** from the left navigation menu. Then select **Connected resources**.
    
    :::image type="content" source="../../media/tools/deep-research/bing-resource-name.png" alt-text="A screenshot showing the Playwright connection. " lightbox="../../media/tools/deep-research/bing-resource-name.png":::



```python
import os
from azure.identity import DefaultAzureCredential
from azure.ai.agents import AgentsClient
from azure.ai.agents.models import MessageRole
from azure.ai.projects import AIProjectClient

project_endpoint = "https://<your-ai-services-resource-name>.services.ai.azure.com/api/projects/<your-project-name>"

project_client = AIProjectClient(
    endpoint=project_endpoint,
    credential=DefaultAzureCredential()
)

playwright_connection = project_client.connections.get(
    name="connection-1-microsoft-playwright"
)
print(playwright_connection.id)

with project_client:
    agent = project_client.agents.create_agent(
        model="gpt-4o", 
        name="my-agent", 
        instructions="use the tool to respond", 
        tools=[{
            "type": "browser_automation",
            "browser_automation": {
            "connection": {
                "id": playwright_connection.id,
            }
        }
        }],
    )

    print(f"Created agent, ID: {agent.id}")

    thread = project_client.agents.threads.create()
    print(f"Created thread and run, ID: {thread.id}")

    # Create message to thread
    message = project_client.agents.messages.create(
        thread_id=thread.id, 
        role="user", 
        content="something you want the tool to perform")
    print(f"Created message: {message['id']}")

    # Create and process an Agent run in thread with tools
    run = project_client.agents.runs.create_and_process(
        thread_id=thread.id, 
        agent_id=agent.id,
        )
    print(f"Run created, ID: {run.id}")
    print(f"Run finished with status: {run.status}")

    if run.status == "failed":
        print(f"Run failed: {run.last_error}")

    run_steps = project_client.agents.run_steps.list(thread_id=thread.id, run_id=run.id)
    for step in run_steps:
        print(step)
        print(f"Step {step['id']} status: {step['status']}")

        # Check if there are tool calls in the step details
        step_details = step.get("step_details", {})
        tool_calls = step_details.get("tool_calls", [])

        if tool_calls:
            print("  Tool calls:")
            for call in tool_calls:
                print(f"    Tool Call ID: {call.get('id')}")
                print(f"    Type: {call.get('type')}")

                function_details = call.get("function", {})
                if function_details:
                    print(f"    Function name: {function_details.get('name')}")
        print()  # add an extra newline between steps

    # Delete the Agent when done
    project_client.agents.delete_agent(agent.id)
    print("Deleted agent")

    # Fetch and log all messages
    response_message = project_client.agents.messages.get_last_message_by_role(thread_id=thread.id, role=MessageRole.AGENT)
    if response_message:
        for text_message in response_message.text_messages:
            print(f"Agent response: {text_message.text.value}")
        for annotation in response_message.url_citation_annotations:
            print(f"URL Citation: [{annotation.url_citation.title}]({annotation.url_citation.url})")
```