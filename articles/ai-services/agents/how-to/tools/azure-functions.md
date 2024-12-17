---
title: 'How to use Azure Functions with the Azure AI Search tool'
titleSuffix: Azure OpenAI
description: Learn how to use Azure functions with Azure AI Agents.
services: azure-ai-agent-service
manager: nitinme
ms.service: azure
ms.topic: how-to
ms.date: 12/11/2024
author: aahill
ms.author: aahi
ms.custom: azure-ai-agents
zone_pivot_groups: selection-function-calling
---
::: zone pivot="overview"

The Azure AI Agents service integrates with Azure Functions, enabling you to create intelligent, event-driven applications with minimal overhead. This combination allows AI-driven workflows to leverage the scalability and flexibility of serverless computing, making it easier to build and deploy solutions that respond to real-time events or complex workflows. 
 
Azure Functions provide support for triggers and bindings, which simplify how your AI Agents interact with external systems and services. Triggers determine when a function executes—such as an HTTP request, message from a queue, or a file upload to Azure Blob Storage and allows agents to act dynamically based on incoming events. 
 
Meanwhile, bindings facilitate streamlined connections to input or output data sources, such as databases or APIs, without requiring extensive boilerplate code. For instance, you can configure a trigger to execute an Azure Function whenever a customer message is received in a chatbot and use output bindings to send a response via the Azure AI Agent.

## Prerequisites

* [Azure Functions Core Tools v4.x](/azure/azure-functions/functions-run-local)
* [Azure AI Agent Service](../../../../ai-studio/how-to/develop/sdk-overview.md?tabs=sync&pivots=programming-language-python#azure-ai-agent-service)
* [Azurite](https://github.com/Azure/Azurite)

## Prepare your local environment

The following examples highlight how to use the Azure AI Agent service function calling where function calls are placed on a storage queue by the Agent service to be processed by an Azure Function listening to that queue.

You can find the template and code used here on [GitHub](https://github.com/Azure-Samples/azure-functions-ai-services-agent-python).

### Create Azure resources for local and cloud dev-test

Once you have your Azure subscription, run the following in a new terminal window to create Azure OpenAI and other resources needed:

```bash
azd init --template https://github.com/Azure-Samples/azure-functions-ai-services-agent-python
```
#### Mac/Linux:

```bash
chmod +x ./infra/scripts/*.sh 
```
#### Windows:

```Powershell
set-executionpolicy remotesigned
```

### Provision resources

Run the following command to create the required resources in Azure.
```bash
azd provision
```

### Create local.settings.json 

> [!NOTE]
> This file should be in the same folder as `host.json`. It is automatically created if you ran `azd provision`.

```json
{
  "IsEncrypted": false,
  "Values": {
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "STORAGE_CONNECTION__queueServiceUri": "https://<storageaccount>.queue.core.windows.net",
    "PROJECT_CONNECTION_STRING": "<project connnection for AI Project>",
    "AzureWebJobsStorage": "UseDevelopmentStorage=true"
    }
}
```

::: zone-end

::: zone pivot="code-example"

# Azure AI Agents function calling with Azure Functions

Azure AI Agents supports function calling, which allows you to describe the structure of functions to an Assistant and then return the functions that need to be called along with their arguments. This example shows how to use Azure Functions to process the function calls through queue messages in Azure Storage. You can see a complete working sample on https://github.com/Azure-Samples/azure-functions-ai-services-agent-python

### Supported models

To use all features of function calling including parallel functions, you need to use a model that was released after November 6, 2023.


## Define a function for your agent to call

Start by defining an Azure Function queue trigger function that will process function calls from the queue. 

```python
# Function to get the weather from an Azure Storage queue where the AI Agent will send function call information
# It returns the mock weather to an output queue with the correlation id for the AI Agent service to pick up the result of the function call
@app.function_name(name="GetWeather")
@app.queue_trigger(arg_name="msg", queue_name="input", connection="STORAGE_CONNECTION")  
def process_queue_message(msg: func.QueueMessage) -> None:
    logging.info('Python queue trigger function processed a queue item')

    # Queue to send message to
    queue_client = QueueClient(
        os.environ["STORAGE_CONNECTION__queueServiceUri"],
        queue_name="output",
        credential=DefaultAzureCredential(),
        message_encode_policy=BinaryBase64EncodePolicy(),
        message_decode_policy=BinaryBase64DecodePolicy()
    )

    # Get the content of the function call message
    messagepayload = json.loads(msg.get_body().decode('utf-8'))
    location = messagepayload['location']
    correlation_id = messagepayload['CorrelationId']

    # Send message to queue. Sends a mock message for the weather
    result_message = {
        'Value': 'Weather is 74 degrees and sunny in ' + location,
        'CorrelationId': correlation_id
    }
    queue_client.send_message(json.dumps(result_message).encode('utf-8'))

    logging.info(f"Sent message to output queue with message {result_message}")
```


## Create an AI project client and agent

In the sample below we create a client and an agent that has the tools definition for the Azure Function

```python
# Initialize the client and create agent for the tools Azure Functions that the agent can use

# Create a project client
project_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(),
    conn_str=os.environ["PROJECT_CONNECTION_STRING"]
)

# Get the connection string for the storage account to send and receive the function calls to the queues
storage_connection_string = os.environ["STORAGE_CONNECTION__queueServiceUri"]

# Create an agent with the Azure Function tool to get the weather
agent = project_client.agents.create_agent(
    model="gpt-4o-mini",
    name="azure-function-agent-get-weather",
    instructions="You are a helpful support agent. Answer the user's questions to the best of your ability.",
    headers={"x-ms-enable-preview": "true"},
    tools=[
        {
            "type": "azure_function",
            "azure_function": {
                "function": {
                    "name": "GetWeather",
                    "description": "Get the weather in a location.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {"type": "string", "description": "The location to look up."}
                        },
                        "required": ["location"]
                    }
                },
                "input_binding": {
                    "type": "storage_queue",
                    "storage_queue": {
                        "queue_service_uri": storage_connection_string,
                        "queue_name": "input"
                    }
                },
                "output_binding": {
                    "type": "storage_queue",
                    "storage_queue": {
                        "queue_service_uri": storage_connection_string,
                        "queue_name": "output"
                    }
                }
            }
        }
    ],
)
```

## Create a thread for the agent

```python
# Create a thread
thread = project_client.agents.create_thread()
print(f"Created thread, thread ID: {thread.id}")
```

## Create a run and check the output

```python
# Send the prompt to the agent
message = project_client.agents.create_message(
    thread_id=thread.id,
    role="user",
    content="What is the weather in Seattle, WA?",
)
print(f"Created message, message ID: {message.id}")

# Run the agent
run = project_client.agents.create_run(thread_id=thread.id, assistant_id=agent.id)
# Monitor and process the run status. The function call should be placed on the input queue by the Agent service for the Azure Function to pick up when requires_action is returned
while run.status in ["queued", "in_progress", "requires_action"]:
    time.sleep(1)
    run = project_client.agents.get_run(thread_id=thread.id, run_id=run.id)

    if run.status not in ["queued", "in_progress", "requires_action"]:
        break

print(f"Run finished with status: {run.status}")
```

### Get the result of the run

```python
# Get messages from the assistant thread
messages = project_client.agents.get_messages(thread_id=thread.id)
print(f"Messages: {messages}")

# Get the last message from the assistant
last_msg = messages.get_last_text_message_by_sender("assistant")
if last_msg:
    print(f"Last Message: {last_msg.text.value}")

# Delete the agent once done
project_client.agents.delete_agent(agent.id)
print("Deleted agent")
```

::: zone-end
