---
title: Get started building a chat app using the prompt flow SDK
titleSuffix: Azure AI Studio
description: This article provides instructions on how to build a custom chat app in Python using the prompt flow SDK.
manager: scottpolly
ms.service: azure-ai-studio
ms.custom: build-2024, devx-track-azurecli, devx-track-python
ms.topic: how-to
ms.date: 10/31/2024
ms.reviewer: dantaylo
ms.author: sgilley
author: sdgilley
---

# Build a custom chat app in Python using Azure AI SDK

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

In this quickstart, we walk you through setting up your local development environment with the prompt flow SDK. We write a prompt, run it as part of your app code, trace the LLM calls being made, and run a basic evaluation on the outputs of the LLM.

## Prerequisites

* Before you can follow this quickstart, complete the [AI Studio playground quickstart](../quickstarts/get-started-playground.md) to deploy a **gpt-4o-mini** model into a project.

## Install the Azure CLI and sign in 

[!INCLUDE [Install the Azure CLI](../includes/install-cli.md)]

## Create a new Python environment

[!INCLUDE [Install Python](../includes/install-python.md)]

## Install packages

[!INCLUDE [Install the Azure AI SDK](../includes/install-ai-sdk.md)]

## Configure your environment variables

Your project connection string is required to call the Azure OpenAI service from your code. In this quickstart, you save this value in a `.env` file, which is a file that contains environment variables that your application can read. 

1. Create a `.env` file, and paste the following code:

    ```text
    PROJECT_CONNECTION_STRING=<your-connection-string>
    ```

You find your connection string in the Azure AI Studio project you created in the [AI Studio playground quickstart](../quickstarts/get-started-playground.md).  Open the project, then find the connection string on the **Overview** page.  Copy the connection string and paste it into the `.env` file.

:::image type="content" source="../media/quickstarts/azure-ai-sdk/connection-string.png" alt-text="Screenshot shows the overview page of a project and the location of the connection string.":::

> [!WARNING]
> Key based authentication is supported but isn't recommended by Microsoft. If you want to use keys you can add your key to the `.env`, but please ensure that your `.env` is in your `.gitignore` file so that you don't accidentally check it into your git repository.

## Build your chat app

> [!IMPORTANT]
> The rest of this tutorial shows the cells of Python code for you to run in a Jupyter notebook. Copy/paste the cells below or download the notebook from @@@CAN WE GIVE A LINK?

## Create a project client

Create a client connected to your AI project.  This client is used to access all the resources in your project.

```python
import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

project = AIProjectClient.from_connection_string(
    conn_str=os.environ['PROJECT_CONNECTION_STRING'],
    credential=DefaultAzureCredential()
)
```

## Run a chat completions call

 Run a chat completions call and print the response. Feel free to play with the system and user messages.

```Python
chat = project.inference.get_chat_completions_client()
response = chat.complete(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are an AI assistant that speaks like a techno punk rocker from 2350. Be cool but not too cool. Ya dig?"},
        {"role": "user", "content": "Hey, can you help me with my taxes? I'm a freelancer."},
    ]
)

print(response.choices[0].message.content)
```

## Generate prompt from user input and a prompt template

The previous code uses hardcoded input and output messages. In a real app you'd take input from a client application, generate a system message with internal instructions to the model, and then call the LLM with all of the messages.

First let's define a `get_chat_response` function that takes messages and context, generates a system message using a prompt template, and calls a model.

> [!NOTE]
> The prompt template uses mustache format.

```python
from azure.ai.inference.prompts import PromptTemplate

def get_chat_response(messages, context):
    # create a prompt template from an inline string (using mustache syntax)
    prompt_template = PromptTemplate.from_message(prompt_template="""
        system:
        You are an AI assistant that speaks like a techno punk rocker from 2350. Be cool but not too cool. Ya dig? Refer to the user by their first name, try to work their last name into a pun.

        The user's first name is {{first_name}} and their last name is {{last_name}}.
        """)
    
    # generate system message from the template, passing in the context as variables
    system_message = prompt_template.render(data=context)

    # add the prompt messages to the user messages
    response = chat.complete(
        model="gpt-4o", 
        messages=system_message + messages,
        temperature=1,
        frequency_penalty=0.5,
        presence_penalty=0.5)

    return response
```

The get_chat_response function could be easily added as a route to a FastAPI or Flask app to enable calling this function from a front-end web application.

Now let's simulate passing information from a frontend application to this function:

```python
response = get_chat_response(
    messages=[{"role": "user", "content": "what city has the best food in the world?"}],
    context = {
      "first_name": "Dan",
      "last_name": "Taylor"
   }
)
print(response.choices[0].message.content)
```

## Enable tracing and log to studio

The Azure SDK uses `opentelemetry` for instrumentation and logging. Before you can log to Azure AI Studio, attach an Application Insights resource to your project.

1. Navigate to your project in [Azure AI Studio](https://ai.azure.com/)
1. Select the **Tracing** page on the left hand side.
1. Select **Create New** to attach a new Application Insights resource to your project.

Next, install the `opentelemetry` SDK:

```python
%pip install azure-monitor-opentelemetry
```

Now enable tracing with output to the console:

```python
import os
from azure.monitor.opentelemetry import configure_azure_monitor

os.environ['AZURE_TRACING_GEN_AI_CONTENT_RECORDING_ENABLED'] = 'true'
# Enable Azure Monitor tracing
application_insights_connection_string = project.telemetry.get_connection_string()
if not application_insights_connection_string:
    print("Application Insights was not enabled for this project.")
    print("Enable it via the 'Tracing' tab in your AI Studio project page.")
    exit()
    
configure_azure_monitor(connection_string=application_insights_connection_string)
```

Finally, run an inferencing call. The call is logged to Azure AI Studio.  This code prints a link to the traces.

```python
response = chat.complete(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are an AI assistant that speaks like a techno punk rocker from 2350. Be cool but not too cool. Ya dig?"},
        {"role": "user", "content": "Hey, can you help me with my taxes? I'm a freelancer."},
    ]
)

print("View traces at:")
print(f"https://int.ai.azure.com/project-monitoring?wsid=/subscriptions/{project.scope['subscription_id']}/resourceGroups/{project.scope['resource_group_name']}/providers/Microsoft.MachineLearningServices/workspaces/{project.scope['project_name']}")
```

## Next step

> [!div class="nextstepaction"]
> [Add data and use retrieval augmented generation (RAG) to build a custom chat app](../tutorials/copilot-sdk-create-resources.md)
