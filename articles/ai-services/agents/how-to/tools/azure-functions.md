---
title: How to use Azure Functions with the Azure AI Agent Service
titleSuffix: Azure OpenAI
description: Learn how to use Azure functions with Azure AI Agents.
services: azure-ai-agent-service
manager: nitinme
ms.service: azure-ai-agent-service
ms.topic: how-to
ms.date: 01/30/2025
author: aahill
ms.author: aahi
ms.custom: azure-ai-agents
zone_pivot_groups: selection-function-calling
---

# Use Azure Functions with Azure AI Agent Service

::: zone pivot="overview"

The Azure AI Agent Service integrates with Azure Functions, enabling you to create intelligent, event-driven applications with minimal overhead. This combination allows AI-driven workflows to leverage the scalability and flexibility of serverless computing, making it easier to build and deploy solutions that respond to real-time events or complex workflows. 
 
Azure Functions provide support for triggers and bindings, which simplify how your AI Agents interact with external systems and services. Triggers determine when a function executes—such as an HTTP request, message from a queue, or a file upload to Azure Blob Storage and allows agents to act dynamically based on incoming events. 
 
Meanwhile, bindings facilitate streamlined connections to input or output data sources, such as databases or APIs, without requiring extensive boilerplate code. For instance, you can configure a trigger to execute an Azure Function whenever a customer message is received in a chatbot and use output bindings to send a response via the Azure AI Agent.

## Prerequisites

* [Azure Functions Core Tools v4.x](/azure/azure-functions/functions-run-local)
* [Azure AI Agent Service](../../../../ai-foundry/how-to/develop/sdk-overview.md?tabs=sync&pivots=programming-language-python#azure-ai-foundry-agent-service)
* [Azurite](https://github.com/Azure/Azurite)

## Prepare your local environment

The following examples highlight how to use the Azure AI Agent Service function calling where function calls are placed on a storage queue by the Agent Service to be processed by an Azure Function listening to that queue.

You can find the template and code used here on [GitHub](https://github.com/Azure-Samples/azure-functions-ai-services-agent-python).

## Usage support

|Azure AI foundry support  | Python SDK |	C# SDK | REST API | Basic agent setup | Standard agent setup |
|---------|---------|---------|---------|---------|---------|
|  | ✔️ |  | ✔️ | | ✔️ |

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

## Run your app using Visual Studio Code

1. Open the folder in a new terminal.
1. Run the `code .` code command to open the project in Visual Studio Code.
1. In the command palette (F1), type `Azurite: Start`, which enables debugging with local storage for Azure Functions runtime.
1. Press **Run/Debug (F5)** to run in the debugger. Select **Debug anyway** if prompted about local emulator not running.
1. Send POST `prompt` endpoints respectively using your HTTP test tool. If you have the [RestClient](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) extension installed, you can execute requests directly from the [`test.http`](https://github.com/Azure-Samples/azure-functions-ai-services-agent-python/blob/main/app/test.http) project file.


## Deploy to Azure

Run this command to provision the function app, with any required Azure resources, and deploy your code:

```shell
azd up
```

You're prompted to supply these required deployment parameters:

| Parameter | Description |
| ---- | ---- |
| _Environment name_ | An environment that's used to maintain a unique deployment context for your app. You won't be prompted if you created the local project using `azd init`.|
| _Azure subscription_ | Subscription in which your resources are created.|
| _Azure location_ | Azure region in which to create the resource group that contains the new Azure resources. Only regions that currently support the Flex Consumption plan are shown.|

After publish completes successfully, `azd` provides you with the URL endpoints of your new functions, but without the function key values required to access the endpoints. To learn how to obtain these same endpoints along with the required function keys, see [Invoke the function on Azure](/azure/azure-functions/create-first-function-azure-developer-cli?pivots=programming-language-dotnet#invoke-the-function-on-azure) in the companion article [Quickstart: Create and deploy functions to Azure Functions using the Azure Developer CLI](/azure/azure-functions/create-first-function-azure-developer-cli?pivots=programming-language-dotnet).

## Redeploy your code

You can run the `azd up` command as many times as you need to both provision your Azure resources and deploy code updates to your function app.

> [!NOTE]
> Deployed code files are always overwritten by the latest deployment package.

## Clean up resources

When you're done working with your function app and related resources, you can use this command to delete the function app and its related resources from Azure and avoid incurring any further costs (--purge does not leave a soft delete of AI resource and recovers your quota):

```shell
azd down --purge
```

::: zone-end

::: zone pivot="code-example"

Azure AI Agents supports function calling, which allows you to describe the structure of functions to an Assistant and then return the functions that need to be called along with their arguments. This example shows how to use Azure Functions to process the function calls through queue messages in Azure Storage. You can see a complete working sample on https://github.com/Azure-Samples/azure-functions-ai-services-agent-python

### Supported models

To use all features of function calling including parallel functions, you need to use a model that was released after November 6, 2023.


## Define a function for your agent to call

Start by defining an Azure Function queue trigger function that will process function calls from the queue. 

```python
# Function to get the weather from an Azure Storage queue where the AI Agent will send function call information
# It returns the mock weather to an output queue with the correlation id for the AI Agent Service to pick up the result of the function call
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

# [Python](#tab/python)
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

# [REST API](#tab/rest)
Follow the [REST API Quickstart](../../quickstart.md?pivots=rest-api) to set the right values for the environment variables `AZURE_AI_AGENTS_TOKEN` and `AZURE_AI_AGENTS_ENDPOINT`. Then create the agent using:
```console
curl $AZURE_AI_AGENTS_ENDPOINT/assistants?api-version=2024-12-01-preview \
  -H "Authorization: Bearer $AZURE_AI_AGENTS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "instructions": "You are a helpful support agent. Answer the user's questions to the best of your ability.",
    "name": "azure-function-agent-get-weather",
    "model": "gpt-4o-mini",
    "tools": [
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
                    "queue_service_endpoint": "https://storageaccount.queue.core.windows.net",
                    "queue_name": "input"
                }
            },
            "output_binding": {
                "type": "storage_queue",
                "storage_queue": {
                    "queue_service_endpoint": "https://storageaccount.queue.core.windows.net",
                    "queue_name": "output"
                }
            }
        }
      }
    ]
  }'
```

---

## Create a thread for the agent

# [Python](#tab/python)
```python
# Create a thread
thread = project_client.agents.create_thread()
print(f"Created thread, thread ID: {thread.id}")
```

# [REST API](#tab/rest)
```console
curl $AZURE_AI_AGENTS_ENDPOINT/threads?api-version=2024-12-01-preview \
  -H "Authorization: Bearer $AZURE_AI_AGENTS_TOKEN" \
  -H "Content-Type: application/json" \
  -d ''
```
---

## Create a run and check the output

# [Python](#tab/python)
```python
# Send the prompt to the agent
message = project_client.agents.create_message(
    thread_id=thread.id,
    role="user",
    content="What is the weather in Seattle, WA?",
)
print(f"Created message, message ID: {message.id}")

# Run the agent
run = project_client.agents.create_run(thread_id=thread.id, agent_id=agent.id)
# Monitor and process the run status. The function call should be placed on the input queue by the Agent Service for the Azure Function to pick up when requires_action is returned
while run.status in ["queued", "in_progress", "requires_action"]:
    time.sleep(1)
    run = project_client.agents.get_run(thread_id=thread.id, run_id=run.id)

    if run.status not in ["queued", "in_progress", "requires_action"]:
        break

print(f"Run finished with status: {run.status}")
```
# [REST API](#tab/rest)
```console
curl $AZURE_AI_AGENTS_ENDPOINT/threads/thread_abc123/messages?api-version=2024-12-01-preview \
  -H "Authorization: Bearer $AZURE_AI_AGENTS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
      "role": "user",
      "content": "What is the weather in Seattle, WA?"
    }'
```

```console
curl $AZURE_AI_AGENTS_ENDPOINT/threads/thread_abc123/runs?api-version=2024-12-01-preview \
  -H "Authorization: Bearer $AZURE_AI_AGENTS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "assistant_id": "asst_abc123",
  }'
```

```console
curl $AZURE_AI_AGENTS_ENDPOINT/threads/thread_abc123/runs/run_abc123?api-version=2024-12-01-preview \
  -H "Authorization: Bearer $AZURE_AI_AGENTS_TOKEN"
```

---
## Get the result of the run

# [Python](#tab/python)
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

# [REST API](#tab/rest)
```console
curl $AZURE_AI_AGENTS_ENDPOINT/threads/thread_abc123/messages?api-version=2024-12-01-preview \
  -H "Authorization: Bearer $AZURE_AI_AGENTS_TOKEN"
```

::: zone-end
