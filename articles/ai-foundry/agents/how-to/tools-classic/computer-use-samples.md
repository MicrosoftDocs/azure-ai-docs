---
title: 'How to use the Computer Use Tool'
titleSuffix: Microsoft Foundry
description: Find code samples and instructions for using the Computer Use model in the Foundry Agent Service.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.date: 12/16/2025
author: alvinashcraft
ms.author: aashcraft
---

# How to use the Computer Use Tool

> [!NOTE]
> This document refers to the classic version of the agents API. 
>
> 🔍 [View the new Computer Use documentation](../../../default/agents/how-to/tools/computer-use.md?view=foundry&preserve-view=true).




Use this article to learn how to use the Computer Use tool with the Azure AI Projects SDK.

## Prerequisites

* The requirements in the [Computer Use Tool overview](./deep-research.md).
* Your Microsoft Foundry Project endpoint.

    
    [!INCLUDE [endpoint-string-portal](../../includes/endpoint-string-portal.md)]

    Save this endpoint to an environment variable named `PROJECT_ENDPOINT`.

* The deployment name of your Computer Use model. You can find it in **Models + Endpoints** in the left navigation menu.

   :::image type="content" source="../../media/tools/computer-use-model-deployment.png" alt-text="A screenshot showing the model deployment screen the Foundry portal." lightbox="../../media/tools/computer-use-model-deployment.png":::
    
    Save the name of your model's deployment name as an environment variable named `COMPUTER_USE_MODEL_DEPLOYMENT_NAME`.

* Before using the tool, you need to set up an environment that can capture screenshots and execute the recommended actions by the agent. We recommend using a sandboxed environment, such as Playwright for safety reasons.

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
import os, time, base64
from typing import List
from azure.ai.agents.models._models import ComputerScreenshot, TypeAction
from azure.ai.projects import AIProjectClient
from azure.ai.agents.models import (
    MessageRole,
    RunStepToolCallDetails,
    RunStepComputerUseToolCall,
    ComputerUseTool,
    ComputerToolOutput,
    MessageInputContentBlock,
    MessageImageUrlParam,
    MessageInputTextBlock,
    MessageInputImageUrlBlock,
    RequiredComputerUseToolCall,
    SubmitToolOutputsAction,
)
from azure.identity import DefaultAzureCredential

def image_to_base64(image_path: str) -> str:
    """
    Convert an image file to a Base64-encoded string.

    :param image_path: The path to the image file (e.g. 'image_file.png')
    :return: A Base64-encoded string representing the image.
    :raises FileNotFoundError: If the provided file path does not exist.
    :raises OSError: If there's an error reading the file.
    """
    if not os.path.isfile(image_path):
        raise FileNotFoundError(f"File not found at: {image_path}")

    try:
        with open(image_path, "rb") as image_file:
            file_data = image_file.read()
        return base64.b64encode(file_data).decode("utf-8")
    except Exception as exc:
        raise OSError(f"Error reading file '{image_path}'") from exc

asset_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../assets/cua_screenshot.jpg"))
action_result_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../assets/cua_screenshot_next.jpg"))
project_client = AIProjectClient(endpoint=os.environ["PROJECT_ENDPOINT"], credential=DefaultAzureCredential())

# Initialize Computer Use tool with a browser-sized viewport
environment = os.environ.get("COMPUTER_USE_ENVIRONMENT", "windows")
computer_use = ComputerUseTool(display_width=1026, display_height=769, environment=environment)

with project_client:

    agents_client = project_client.agents

    # Create a new Agent that has the Computer Use tool attached.
    agent = agents_client.create_agent(
        model=os.environ["MODEL_DEPLOYMENT_NAME"],
        name="my-agent-computer-use",
        instructions="""
            You are an computer automation assistant. 
            Use the computer_use_preview tool to interact with the screen when needed.
            """,
        tools=computer_use.definitions,
    )

    print(f"Created agent, ID: {agent.id}")

    # Create thread for communication
    thread = agents_client.threads.create()
    print(f"Created thread, ID: {thread.id}")

    input_message = (
        "I can see a web browser with bing.com open and the cursor in the search box."
        "Type 'movies near me' without pressing Enter or any other key. Only type 'movies near me'."
    )
    image_base64 = image_to_base64(asset_file_path)
    img_url = f"data:image/jpeg;base64,{image_base64}"
    url_param = MessageImageUrlParam(url=img_url, detail="high")
    content_blocks: List[MessageInputContentBlock] = [
        MessageInputTextBlock(text=input_message),
        MessageInputImageUrlBlock(image_url=url_param),
    ]
    # Create message to thread
    message = agents_client.messages.create(thread_id=thread.id, role=MessageRole.USER, content=content_blocks)
    print(f"Created message, ID: {message.id}")

    run = agents_client.runs.create(thread_id=thread.id, agent_id=agent.id)
    print(f"Created run, ID: {run.id}")

    # create a fake screenshot showing the text typed in
    result_image_base64 = image_to_base64(action_result_file_path)
    result_img_url = f"data:image/jpeg;base64,{result_image_base64}"
    computer_screenshot = ComputerScreenshot(image_url=result_img_url)

    while run.status in ["queued", "in_progress", "requires_action"]:
        time.sleep(1)
        run = agents_client.runs.get(thread_id=thread.id, run_id=run.id)

        if run.status == "requires_action" and isinstance(run.required_action, SubmitToolOutputsAction):
            print("Run requires action:")
            tool_calls = run.required_action.submit_tool_outputs.tool_calls
            if not tool_calls:
                print("No tool calls provided - cancelling run")
                agents_client.runs.cancel(thread_id=thread.id, run_id=run.id)
                break

            tool_outputs = []
            for tool_call in tool_calls:
                if isinstance(tool_call, RequiredComputerUseToolCall):
                    print(tool_call)
                    try:
                        action = tool_call.computer_use_preview.action
                        print(f"Executing computer use action: {action.type}")
                        if isinstance(action, TypeAction):
                            print(f"  Text to type: {action.text}")
                            #(add hook to input text in managed environment API here)

                            tool_outputs.append(
                                ComputerToolOutput(tool_call_id=tool_call.id, output=computer_screenshot)
                            )
                        if isinstance(action, ComputerScreenshot):
                            print(f"  Screenshot requested")
                            # (add hook to take screenshot in managed environment API here)

                            tool_outputs.append(
                                ComputerToolOutput(tool_call_id=tool_call.id, output=computer_screenshot)
                            )
                    except Exception as e:
                        print(f"Error executing tool_call {tool_call.id}: {e}")

            print(f"Tool outputs: {tool_outputs}")
            if tool_outputs:
                agents_client.runs.submit_tool_outputs(thread_id=thread.id, run_id=run.id, tool_outputs=tool_outputs)

        print(f"Current run status: {run.status}")

    print(f"Run completed with status: {run.status}")
    if run.status == "failed":
        print(f"Run failed: {run.last_error}")

    # Fetch run steps to get the details of the agent run
    run_steps = agents_client.run_steps.list(thread_id=thread.id, run_id=run.id)
    for step in run_steps:
        print(f"Step {step.id} status: {step.status}")
        print(step)

        if isinstance(step.step_details, RunStepToolCallDetails):
            print("  Tool calls:")
            run_step_tool_calls = step.step_details.tool_calls

            for call in run_step_tool_calls:
                print(f"    Tool call ID: {call.id}")
                print(f"    Tool call type: {call.type}")

                if isinstance(call, RunStepComputerUseToolCall):
                    details = call.computer_use_preview
                    print(f"    Computer use action type: {details.action.type}")

                print()  # extra newline between tool calls

        print()  # extra newline between run steps

    # Optional: Delete the agent once the run is finished.
    agents_client.delete_agent(agent.id)
    print("Deleted agent")
```

## Next steps

* [Python agent samples](https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples-classic/python/getting-started-agents)
* [Azure OpenAI Computer Use example Playwright integration](../../../openai/how-to/computer-use.md#playwright-integration)
    * The Azure OpenAI API has implementation differences compared to the Agent Service, and these examples may need to be adapted to work with agents.