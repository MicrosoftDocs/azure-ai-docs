---
title: 'How to use the Computer Use Tool'
titleSuffix: Azure AI Foundry
description: Find code samples and instructions for using the Computer Use model in the Azure AI Foundry Agent Service.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-agent-service
ms.topic: how-to
ms.date: 08/22/2025
author: aahill
ms.author: aahi
---

# How to use the Computer Use Tool

Use this article to learn how to use the Computer Use tool with the Azure AI Projects SDK.

## Prerequisites

* The requirements in the [Computer Use Tool overview](./deep-research.md).
* Your Azure AI Foundry Project endpoint.

    
    [!INCLUDE [endpoint-string-portal](../../includes/endpoint-string-portal.md)]

    Save this endpoint to an environment variable named `PROJECT_ENDPOINT`.

* The deployment name of your Computer Use model. You can find it in **Models + Endpoints** in the left navigation menu.

   :::image type="content" source="../../media/tools/computer-use-model-deployment.png" alt-text="A screenshot showing the model deployment screen the AI Foundry portal." lightbox="../../media/tools/computer-use-model-deployment.png":::
    
    Save the name of your model's deployment name as an environment variable named `COMPUTER_USE_MODEL_DEPLOYMENT_NAME`.

The Computer Use tool requires the latest prerelease versions of the `azure-ai-projects` library. First we recommend creating a [virtual environment](https://docs.python.org/3/library/venv.html) to work in:

```console
python -m venv env
# after creating the virtual environment, activate it with:
.\env\Scripts\activate
```

You can install the package with the following command:

```console
pip install --pre azure-ai-projects, azure-identity, azure-ai-agents 
```

## Code example

The following code sample shows a basic API request. Once the initial API request is sent, you would perform a loop where the specified action is performed in your application code, sending a screenshot with each turn so the model can evaluate the updated state of the environment. You can see an example integration for a similar API in the [Azure OpenAI documentation](../../../openai/how-to/computer-use.md#playwright-integration). 

```python
from azure.ai.projects import AIProjectClient
from azure.ai.agents.models import ComputerUseTool
from azure.identity import DefaultAzureCredential
import os
import time

# Initialize client
project_client = AIProjectClient(
    endpoint=os.environ["PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

# Create agent with computer use capability (similar to OpenAI but enhanced)
computer_use_tool = ComputerUseTool(
    display_width=1024,
    display_height=768,
    environment="browser"  # "browser", "mac", "windows", "ubuntu"
)

agent = project_client.agents.create_agent(
    model=os.environ["COMPUTER_USE_MODEL_DEPLOYMENT_NAME"],  # computer-capable model
    name="computer-assistant",
    instructions="You are an assistant that can interact with computer interfaces to help users automate tasks. Always take a screenshot first to understand the current state.",
    tools=[computer_use_tool]
)

# Create a thread for persistent computer automation
thread = project_client.agents.create_thread()

# Ask agent to automate a task
message = project_client.agents.create_message(
    thread_id=thread.id,
    role="user",
    content="Check the latest Azure AI news on bing.com and summarize the top 3 articles"
)

# Run the agent - it will use computer use tool automatically
run = project_client.agents.create_run(
    thread_id=thread.id,
    agent_id=agent.id
)

# Poll for completion and get results
while run.status in ["queued", "in_progress", "requires_action"]:
    if run.status == "requires_action":
        # Handle safety checks or user confirmations
        required_action = run.required_action
        if required_action.type == "computer_call":
            # User must acknowledge safety checks
            project_client.agents.submit_tool_outputs(
                thread_id=thread.id,
                run_id=run.id,
                tool_outputs=[
                    # TODO
                ]
            )
    
    time.sleep(1)
    run = project_client.agents.retrieve_run(thread_id=thread.id, run_id=run.id)

# Get the final response
messages = project_client.agents.list_messages(thread_id=thread.id)
print(messages.data[0].content[0].text.value) 
```

## Next steps

* [Python agent samples](https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples/microsoft/python/getting-started-agents)
* [Azure OpenAI Computer Use example Playwright integration](../../../openai/how-to/computer-use.md#playwright-integration)
    * The Azure OpenAI API has implementation differences compared to the Agent Service, and these examples may need to be adapted to work with agents.