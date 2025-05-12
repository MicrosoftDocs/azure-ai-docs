---
title: 'How to use connected agents'
titleSuffix: Azure AI Foundry
description: Learn how to create multi-agentic systems using connected agents in  AI Agent Service.
services: cognitive-services
manager: nitinme
ms.service: azure
ms.topic: how-to
ms.date: 05/02/2025
author: aahill
ms.author: aahi
recommendations: false
ms.custom: azure-ai-agents-code
zone_pivot_groups: selection-connected-agents
---

# How to use connected agents to solve tasks

Connected agents allow you to create task-specific agents that can interact seamlessly with a primary agent. This feature enables you to build multi-agent systems without the need for external orchestrators. Instead of overloading a single agent with multiple capabilities, you can divide complex tasks like customer service or sales analysis workflows among multiple agents.

## Features

* **Simplified workflow design**: Break down complex tasks across specialized agents to reduce complexity and improve clarity.
* **No custom orchestration required**: The main agent uses natural language to route tasks, eliminating the need for hardcoded logic.
* **Easy extensibility**: Add new connected agents (e.g., for translation or risk scoring) without modifying the main agent.
* **Improved reliability and traceability**: Assign focused responsibilities to each agent for easier debugging and better auditability.
* **Flexible setup options**: Configure agents using a no-code interface in the Foundry portal or programmatically via the Python SDK.

:::zone pivot="portal"

## Creating a multi-agent setup

Navigate to the **create and debug** page for your agents. In the **Connected agents** section of the setup pane, select **Add +**.


:::image type="content" source="../media/connected-agents/connected-agents-foundry.png" alt-text="A screenshot of the agents page in the Azure AI Foundry." lightbox="../media/connected-agents/connected-agents-foundry.png":::

In the window that appears, select an agent to delegate tasks to, with a unique name and a description of how and when the main agent will invoke the connected agent. Be as descriptive as possible about the circumstances in which the connected agent should be called.

:::image type="content" source="../media/connected-agents/connected-agents-foundry-2.png" alt-text="A screenshot of the connected agents screen" lightbox="../media/connected-agents/connected-agents-foundry-2.png":::

::: zone-end

:::zone pivot="python"


## Creating a multi-agent setup

To create a multi-agent setup, follow these steps:

1. Initialize the client object.

    ```python
    import os
    from azure.ai.projects import AIProjectClient
    from azure.ai.projects.models import ConnectedAgentTool, MessageRole
    from azure.identity import DefaultAzureCredential
    
    
    project_client = AIProjectClient.from_connection_string(
        credential=DefaultAzureCredential(),
        conn_str=os.environ["PROJECT_CONNECTION_STRING"],
    )
    ```

1. Create an agent that will be connected to a "main" agent.

    ```python
    connected_agent_name = "stock_price_bot"
    
    stock_price_agent = project_client.agents.create_agent(
        model=os.environ["MODEL_DEPLOYMENT_NAME"],
        name=connected_agent_name,
        instructions=(
            "Your job is to get the stock price of a company. If you don't know the realtime stock price, return the last known stock price."
        ),
    )
    ```
   
1. Initialize the connected agent tool with the agent ID, name, and description
    
    ```python
    connected_agent = ConnectedAgentTool(
        id=stock_price_agent.id, name=connected_agent_name, description="Gets the stock price of a company"
    )
    ```

1. Create the "main" agent that will use the connected agent.

    ```python
    agent = project_client.agents.create_agent(
        model=os.environ["MODEL_DEPLOYMENT_NAME"],
        name="my-agent",
        instructions="You are a helpful agent, and use the connected agent to get stock prices.",
        tools=connected_agent.definitions,
    )
    
    print(f"Created agent, ID: {agent.id}")
    ```

1. Create a thread and add a message to it.
    
    ```python
    thread = project_client.agents.create_thread()
    print(f"Created thread, ID: {thread.id}")
    
    # Create message to thread
    message = project_client.agents.create_message(
        thread_id=thread.id,
        role=MessageRole.USER,
        content="What is the stock price of Microsoft?",
    )
    print(f"Created message, ID: {message.id}")
    
    ```
    
1. Create a run and wait for it to complete. 
    
    ```python
    
    # Create and process Agent run in thread with tools
    run = project_client.agents.create_and_process_run(thread_id=thread.id, agent_id=agent.id)
    print(f"Run finished with status: {run.status}")
    
    if run.status == "failed":
        print(f"Run failed: {run.last_error}")
    
    # Delete the Agent when done
    project_client.agents.delete_agent(agent.id)
    print("Deleted agent")
    
    # Delete the connected Agent when done
    project_client.agents.delete_agent(stock_price_agent.id)
    print("Deleted connected agent")
    ```

1. Print the agent's response. The main agent will compile the responses from the connected agents and provide the response. connected agent responses are only visible to the main agent, and not to the end user.
    
    ```python
    # Print the Agent's response message with optional citation
    response_message = project_client.agents.list_messages(thread_id=thread.id).get_last_message_by_role(
        MessageRole.AGENT
    )
    if response_message:
        for text_message in response_message.text_messages:
            print(f"Agent response: {text_message.text.value}")
        for annotation in response_message.url_citation_annotations:
            print(f"URL Citation: [{annotation.url_citation.title}]({annotation.url_citation.url})")
    ```

::: zone-end