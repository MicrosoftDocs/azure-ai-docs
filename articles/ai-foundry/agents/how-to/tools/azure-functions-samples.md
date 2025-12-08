---
title: How to use Azure Functions with Azure Storage Queues
titleSuffix: Microsoft Foundry
description: Learn how to use Azure Functions with Azure Storage Queues to extend Azure AI Agents with custom tools.
services: azure-ai-agent-service
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.date: 11/20/2025
author: alvinashcraft
ms.author: aashcraft
ms.custom: azure-ai-agents
zone_pivot_groups: selection-azure-functions-samples
---

# How to use queue-based Azure Functions with Microsoft Foundry agents

[!INCLUDE [classic-banner](../../../includes/classic-banner.md)]


This article shows how to use a queue-based integrated tool approach to enable Microsoft Foundry agents to access code deployed to Azure Functions. In this approach, agents access tool code asynchronously in Azure Functions by means of separate input and output message queues in Azure Queue storage. 

Foundry agents connect directly to the input queue monitored by Azure Functions by using a tool definition provided by `AzureFunctionsTool`. When an agent needs to use this Azure Functions hosted tool, it uses the tool definition to place a message in an input queue that's monitored by the function app in Azure Functions. An Azure Storage queue trigger invokes the function code to process the message and return a result through an output queue binding. The agent reads the message from the output queue to continue the conversation. 

  

## Prerequisites

* A prepared environment. See the [overview](azure-functions.md) article for details.

> [!NOTE] 
> You must have a [A deployed agent with the standard setup](../../environment-setup.md#choose-your-setup). The basic agent setup isn't supported.

::: zone pivot="python"

> [!TIP]
> You can find a complete working sample on [GitHub](https://github.com/Azure-Samples/azure-functions-ai-services-agent-python)

## Define a function for your agent to call

Start by defining an Azure queue trigger function that processes function calls from the queue. For example:

```python
app = func.FunctionApp()

@app.queue_trigger(arg_name="msg", queue_name="azure-function-foo-input", connection="STORAGE_CONNECTION")
@app.queue_output(arg_name="outputQueue", queue_name="azure-function-foo-output", connection="STORAGE_CONNECTION")  

def queue_trigger(inputQueue: func.QueueMessage, outputQueue: func.Out[str]):
    try:
        messagepayload = json.loads(inputQueue.get_body().decode("utf-8"))
        logging.info(f'The function receives the following message: {json.dumps(messagepayload)}')
        location = messagepayload["location"]
        weather_result = f"Weather is {len(location)} degrees and sunny in {location}"
        response_message = {
            "Value": weather_result,
            "CorrelationId": messagepayload["CorrelationId"]
        }
        logging.info(f'The function returns the following message through the {outputQueue} queue: {json.dumps(response_message)}')

        outputQueue.set(json.dumps(response_message))

    except Exception as e:
        logging.error(f"Error processing message: {e}")
```

## Configure the Azure Function tool

First, define the Azure Function tool, specifying its name, description, parameters, and storage queue configurations.

```python
import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import AzureFunctionStorageQueue, AzureFunctionTool

# Retrieve the storage service endpoint from environment variables
storage_service_endpoint = os.environ["STORAGE_SERVICE_ENDPONT"]

# Define the Azure Function tool
azure_function_tool = AzureFunctionTool(
    name="foo",  # Name of the tool
    description="Get answers from the foo bot.",  # Description of the tool's purpose
    parameters={  # Define the parameters required by the tool
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "The question to ask."},
            "outputqueueuri": {"type": "string", "description": "The full output queue URI."},
        },
    },
    input_queue=AzureFunctionStorageQueue(  # Input queue configuration
        queue_name="azure-function-foo-input",
        storage_service_endpoint=storage_service_endpoint,
    ),
    output_queue=AzureFunctionStorageQueue(  # Output queue configuration
        queue_name="azure-function-foo-output",
        storage_service_endpoint=storage_service_endpoint,
    ),
)
```

## Create an AI project client and agent

Next, create an AI project client and then create an agent, attaching the Azure Function tool defined previously.

```python
# Initialize the AIProjectClient
project_client = AIProjectClient(
    endpoint=os.environ["PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential()
)
# Create an agent with the Azure Function tool
agent = project_client.agents.create_agent(
    model=os.environ["MODEL_DEPLOYMENT_NAME"],  # Model deployment name
    name="azure-function-agent-foo",  # Name of the agent
    instructions=(
        "You are a helpful support agent. Use the provided function any time the prompt contains the string "
        "'What would foo say?'. When you invoke the function, ALWAYS specify the output queue URI parameter as "
        f"'{storage_service_endpoint}/azure-function-tool-output'. Always respond with \"Foo says\" and then the response from the tool."
    ),
    tools=azure_function_tool.definitions,  # Attach the tool definitions to the agent
)
print(f"Created agent, agent ID: {agent.id}")

```

## Create a thread for the agent

```python
# Create a thread for communication
thread = project_client.agents.threads.create()
print(f"Created thread, thread ID: {thread.id}")
```

## Create a run and check the output

```python
# Create a message in the thread
message = project_client.agents.messages.create(
    thread_id=thread.id,
    role="user",
    content="What is the most prevalent element in the universe? What would foo say?",  
)
print(f"Created message, message ID: {message['id']}")

# Create and process a run for the agent to handle the message
run = project_client.agents.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)
print(f"Run finished with status: {run.status}")

# Check if the run failed
if run.status == "failed":
    print(f"Run failed: {run.last_error}")
```


## Get the result of the run

```python
# Retrieve and print all messages from the thread
messages = project_client.agents.messages.list(thread_id=thread.id)
for msg in messages:
    print(f"Role: {msg['role']}, Content: {msg['content']}")# Get messages from the assistant thread

# Get the last message from the assistant
last_msg = messages.get_last_text_message_by_sender("assistant")
if last_msg:
    print(f"Last Message: {last_msg.text.value}")

# Delete the agent once done
project_client.agents.delete_agent(agent.id)
print(f"Deleted agent")
```

For any issues with the Python code, create an issue on the [sample code repository](https://github.com/azure-ai-foundry/foundry-samples)

::: zone-end

::: zone pivot="rest"

## Create an agent

In the sample below we create a client and an agent that has the tools definition for the Azure Function

Follow the [REST API Quickstart](../../quickstart.md?pivots=rest-api) to set the right values for the environment variables `AGENT_TOKEN`, `AZURE_AI_FOUNDRY_PROJECT_ENDPOINT` and `API_VERSION`. 

```bash
curl --request POST \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/assistants?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN" \
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

## Create a thread for the agent

```bash
curl --request POST \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/threads?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d ''
```

## Create a run and check the output

```bash
curl --request POST \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/threads/thread_abc123/messages?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
      "role": "user",
      "content": "What is the weather in Seattle, WA?"
    }'
```

```bash
curl --request POST \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/threads/thread_abc123/runs?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "assistant_id": "asst_abc123",
  }'
```

```bash
curl --request GET \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/threads/thread_abc123/runs/run_abc123?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN"
```

## Get the result of the run

```bash
curl --request GET \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/threads/thread_abc123/messages?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN"
```

::: zone-end

<!--
::: zone pivot="typescript"

## Define a function for your agent to call

Start by defining an Azure Function queue trigger function that will process AI function calls from the queue. 

:::code language="TypeScript" source="~/azure-functions-ai-services-agent-javascript/app/src/functions/queueGetWeather.ts" :::

## Create an AI project client and agent

In the sample below we create a client and an agent that has the AI tools definition for the Azure Function. The term `function` is used in two contexts within the AI tool definition: 

* Azure Function: the type of tool. This is the Azure Functions app.
* Function: the Http trigger function `GetWeather` within the Azure Function to call when the tool is invoked in the AI Project. 

:::code language="TypeScript" source="~/azure-functions-ai-services-agent-javascript/app/src/azureProjectInit.ts" id="CreateAgent" :::

## Create a thread for the agent

:::code language="TypeScript" source="~/azure-functions-ai-services-agent-javascript/app/src/azureProjectInit.ts" id="CreateThread" :::

## Create a run and check the output

:::code language="TypeScript" source="~/azure-functions-ai-services-agent-javascript/app/src/functions/httpPrompt.ts" id="CreateMessage" :::

## Get the result of the run

:::code language="TypeScript" source="~/azure-functions-ai-services-agent-javascript/app/src/functions/httpPrompt.ts" id="ListMessages" :::

For any issues with the TypeScript code, create an issue on the [sample code repository](https://github.com/Azure-Samples/azure-functions-ai-services-agent-javascript/issues)


::: zone-end
-->
::: zone pivot="csharp"

> [!TIP]
> You can find a complete working sample on [GitHub](https://github.com/Azure-Samples/azure-functions-ai-services-agent-dotnet)

## Prerequisites for .NET Azure Function Sample
To make a function call, we need to create and deploy the Azure function. In the code snippet, we have an example of function on C# which can be used by the earlier code.

```csharp
namespace FunctionProj
{
    public class Response
    {
        public required string Value { get; set; }
        public required string CorrelationId { get; set; }
    }

    public class Arguments
    {
        public required string OutputQueueUri { get; set; }
        public required string CorrelationId { get; set; }
    }

    public class Foo
    {
        private readonly ILogger<Foo> _logger;

        public Foo(ILogger<Foo> logger)
        {
            _logger = logger;
        }

        [Function("Foo")]
        public void Run([QueueTrigger("azure-function-foo-input")] Arguments input, FunctionContext executionContext)
        {
            var logger = executionContext.GetLogger("Foo");
            logger.LogInformation("C# Queue function processed a request.");

            // We have to provide the Managed identity for function resource
            // and allow this identity a Queue Data Contributor role on the storage account.
            var cred = new DefaultAzureCredential();
            var queueClient = new QueueClient(new Uri(input.OutputQueueUri), cred,
                    new QueueClientOptions { MessageEncoding = QueueMessageEncoding.Base64 });

            var response = new Response
            {
                Value = "Bar",
                // Important! Correlation ID must match the input correlation ID.
                CorrelationId = input.CorrelationId
            };

            var jsonResponse = JsonSerializer.Serialize(response);
            queueClient.SendMessage(jsonResponse);
        }
    }
}
```

In this code we define function input and output class: `Arguments` and `Response` respectively. These two data classes are serialized in JSON. It's important that these both contain the `CorrelationId`, which is the same between input and output.

In our example the function is stored in the storage account, created with the AI hub. For that we need to allow key access to that storage. In the Azure portal, go to Storage account > Settings > Configuration and set "Allow storage account key access" to Enabled. If it isn't done, the error that is displayed is "The remote server returned an error: (403) Forbidden." To create the function resource that will host our function, install azure-cli python package and run the next command:

```shell
pip install -U azure-cli
az login
az functionapp create --resource-group your-resource-group --consumption-plan-location region --runtime dotnet-isolated --functions-version 4 --name function_name --storage-account storage_account_already_present_in_resource_group --app-insights existing_or_new_application_insights_name
```

This function writes data to the output queue and hence needs to be authenticated to Azure, so we'll need to assign the function system identity and provide it `Storage Queue Data Contributor`. To do that in Azure portal, select the function, located in `your-resource-group` resource group and in Settings > Identity, switch it on and select Save. After that assign the `Storage Queue Data Contributor` permission on storage account used by our function (`storage_account_already_present_in_resource_group` in the script above) for the assigned system managed identity.

Now we'll create the function itself. Install [.NET](https://dotnet.microsoft.com/download) and [Core Tools](https://go.microsoft.com/fwlink/?linkid=2174087) and create the function project using next commands.

```shell
func init FunctionProj --worker-runtime dotnet-isolated --target-framework net8.0
cd FunctionProj
func new --name foo --template "HTTP trigger" --authlevel "anonymous"
dotnet add package Azure.Identity
dotnet add package Microsoft.Azure.Functions.Worker.Extensions.Storage.Queues --prerelease
```

> [!NOTE]
> There's an "Azure Queue Storage trigger," however the attempt to use it results in error for now.
We have created a project, containing HTTP-triggered Azure function with the logic in `Foo.cs` file. As far as we need to trigger Azure function by a new message in the queue, we replace the content of a Foo.cs by the C# sample code above.
To deploy the function, run the command from dotnet project folder:

```shell
func azure functionapp publish function_name
```

In the `storage_account_already_present_in_resource_group` select the `Queue service` and create two queues: `azure-function-foo-input` and `azure-function-tool-output`. The same queues are used in our sample. To check that the function is working, place the next message into the `azure-function-foo-input` and replace `storage_account_already_present_in_resource_group` by the actual resource group name, or just copy the output queue address.

```json
{
  "OutputQueueUri": "https://storage_account_already_present_in_resource_group.queue.core.windows.net/azure-function-tool-output",
  "CorrelationId": "42"
}
```

Next, we monitor the output queue or the message. You should receive the next message.

```json
{
  "Value": "Bar",
  "CorrelationId": "42"
}
```
The input `CorrelationId` is the same as output.

> [!TIP]
> Place multiple messages to input queue and keep second internet browser window with the output queue open and hit the refresh button on the portal user interface, so that you won't miss the message. If the message instead went to `azure-function-foo-input-poison` queue, the function completed with error, check your setup.
After testing the function and making sure it works, make sure that the Azure AI Project has the following roles for the storage account: `Storage Account Contributor`, `Storage Blob Data Contributor`, `Storage File Data Privileged Contributor`, `Storage Queue Data Contributor` and `Storage Table Data Contributor`. Now the function is ready to be used by the agent.

In the example below we're calling function "foo," which responds "Bar."

## Create a client, tool definition and agent

Get the necessary configuration, initialize the `PersistentAgentsClient`, define the `AzureFunctionToolDefinition` for the Azure Function, and then create the agent.

```csharp
using Azure;
using Azure.AI.Agents.Persistent;
using Azure.Identity;
using Microsoft.Extensions.Configuration;
using System.Text.Json;

//Get configuration from appsettings.json.
IConfigurationRoot configuration = new ConfigurationBuilder()
    .SetBasePath(AppContext.BaseDirectory)
    .AddJsonFile("appsettings.json", optional: false, reloadOnChange: true)
    .Build();

var projectEndpoint = configuration["ProjectEndpoint"];
var modelDeploymentName = configuration["ModelDeploymentName"];
var storageQueueUri = configuration["StorageQueueURI"];
//Initialize PersistentAgentsClient.
PersistentAgentsClient client = new(projectEndpoint, new DefaultAzureCredential());

//Define Azure Function tool definition.
AzureFunctionToolDefinition azureFnTool = new(
    name: "foo",
    description: "Get answers from the foo bot.",
    inputBinding: new AzureFunctionBinding(
        new AzureFunctionStorageQueue(
            queueName: "azure-function-foo-input",
            storageServiceEndpoint: storageQueueUri
        )
    ),
    outputBinding: new AzureFunctionBinding(
        new AzureFunctionStorageQueue(
            queueName: "azure-function-tool-output",
            storageServiceEndpoint: storageQueueUri
        )
    ),
    parameters: BinaryData.FromObjectAsJson(
            new
            {
                Type = "object",
                Properties = new
                {
                    query = new
                    {
                        Type = "string",
                        Description = "The question to ask.",
                    },
                    outputqueueuri = new
                    {
                        Type = "string",
                        Description = "The full output queue uri."
                    }
                },
            },
        new JsonSerializerOptions() { PropertyNamingPolicy = JsonNamingPolicy.CamelCase }
    )
);

//Create agent and give it the Azure Function tool.
PersistentAgent agent = client.Administration.CreateAgent(
    model: modelDeploymentName,
    name: "azure-function-agent-foo",
    instructions: "You are a helpful support agent. Use the provided function any "
    + "time the prompt contains the string 'What would foo say?'. When you invoke "
    + "the function, ALWAYS specify the output queue uri parameter as "
    + $"'{storageQueueUri}/azure-function-tool-output'. Always responds with "
    + "\"Foo says\" and then the response from the tool.",
    tools: [azureFnTool]
);
```
## Create a thread and add a message

Next, create a new persistent agent thread and add an initial user message to it.

```csharp
PersistentAgentThread thread = client.Threads.CreateThread();

client.Messages.CreateMessage(
    thread.Id,
    MessageRole.User,
    "What is the most prevalent element in the universe? What would foo say?");
```

### Create and monitor a run

Then, create a run for the agent on the thread and poll its status until it completes or requires action.

```csharp
ThreadRun run = client.Runs.CreateRun(thread.Id, agent.Id);

do
{
    Thread.Sleep(TimeSpan.FromMilliseconds(500));
    run = client.Runs.GetRun(thread.Id, run.Id);
}
while (run.Status == RunStatus.Queued
    || run.Status == RunStatus.InProgress
    || run.Status == RunStatus.RequiresAction);
```

## Process the results

After the run is complete, we retrieve and process the messages from the thread.

```csharp
Pageable<PersistentThreadMessage> messages = client.Messages.GetMessages(
    threadId: thread.Id,
    order: ListSortOrder.Ascending
);

foreach (PersistentThreadMessage threadMessage in messages)
{
    foreach (MessageContent content in threadMessage.ContentItems)
    {
        switch (content)
        {
            case MessageTextContent textItem:
                Console.WriteLine($"[{threadMessage.Role}]: {textItem.Text}");
                break;
        }
    }
}
```

## Clean up resources
Finally, clean up the created resources by deleting the thread and the agent.

```csharp
client.Threads.DeleteThread(thread.Id);
client.Administration.DeleteAgent(agent.Id);
```
    
::: zone-end

:::zone pivot="java"

## Code example

```java
package com.example.agents;

import com.azure.ai.agents.persistent.MessagesClient;
import com.azure.ai.agents.persistent.PersistentAgentsAdministrationClient;
import com.azure.ai.agents.persistent.PersistentAgentsClient;
import com.azure.ai.agents.persistent.PersistentAgentsClientBuilder;
import com.azure.ai.agents.persistent.RunsClient;
import com.azure.ai.agents.persistent.ThreadsClient;
import com.azure.ai.agents.persistent.implementation.models.CreateAgentRequest;
import com.azure.ai.agents.persistent.models.AzureFunctionBinding;
import com.azure.ai.agents.persistent.models.AzureFunctionDefinition;
import com.azure.ai.agents.persistent.models.AzureFunctionStorageQueue;
import com.azure.ai.agents.persistent.models.AzureFunctionToolDefinition;
import com.azure.ai.agents.persistent.models.CreateRunOptions;
import com.azure.ai.agents.persistent.models.FunctionDefinition;
import com.azure.ai.agents.persistent.models.MessageImageFileContent;
import com.azure.ai.agents.persistent.models.MessageRole;
import com.azure.ai.agents.persistent.models.MessageTextContent;
import com.azure.ai.agents.persistent.models.PersistentAgent;
import com.azure.ai.agents.persistent.models.PersistentAgentThread;
import com.azure.ai.agents.persistent.models.RunStatus;
import com.azure.ai.agents.persistent.models.ThreadMessage;
import com.azure.ai.agents.persistent.models.ThreadRun;
import com.azure.ai.agents.persistent.models.MessageContent;
import com.azure.core.http.HttpHeaderName;
import com.azure.core.http.rest.PagedIterable;
import com.azure.core.http.rest.RequestOptions;
import com.azure.core.util.BinaryData;
import com.azure.identity.DefaultAzureCredentialBuilder;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

public class AgentExample {

    public static void main(String[] args) {

        // variables for authenticating requests to the agent service 
        String projectEndpoint = System.getenv("PROJECT_ENDPOINT");
        String modelName = System.getenv("MODEL_DEPLOYMENT_NAME");
        String storageQueueUri = System.getenv("STORAGE_QUEUE_URI");
        String azureFunctionName = System.getenv("AZURE_FUNCTION_NAME");

        PersistentAgentsClientBuilder clientBuilder = new PersistentAgentsClientBuilder().endpoint(projectEndpoint)
            .credential(new DefaultAzureCredentialBuilder().build());
        PersistentAgentsClient agentsClient = clientBuilder.buildClient();
        PersistentAgentsAdministrationClient administrationClient = agentsClient.getPersistentAgentsAdministrationClient();
        ThreadsClient threadsClient = agentsClient.getThreadsClient();
        MessagesClient messagesClient = agentsClient.getMessagesClient();
        RunsClient runsClient = agentsClient.getRunsClient();

        FunctionDefinition fnDef = new FunctionDefinition(
            azureFunctionName,
            BinaryData.fromObject(
                mapOf(
                    "type", "object",
                    "properties", mapOf(
                        "location",
                        mapOf("type", "string", "description", "The location to look up")
                    ),
                    "required", new String[]{"location"}
                )
            )
        );
        AzureFunctionDefinition azureFnDef = new AzureFunctionDefinition(
            fnDef,
            new AzureFunctionBinding(new AzureFunctionStorageQueue(storageQueueUri, "agent-input")),
            new AzureFunctionBinding(new AzureFunctionStorageQueue(storageQueueUri, "agent-output"))
        );
        AzureFunctionToolDefinition azureFnTool = new AzureFunctionToolDefinition(azureFnDef);

        String agentName = "azure_function_example";
        RequestOptions requestOptions = new RequestOptions()
            .setHeader(HttpHeaderName.fromString("x-ms-enable-preview"), "true");
        CreateAgentRequest createAgentRequestObj = new CreateAgentRequest(modelName)
            .setName(agentName)
            .setInstructions("You are a helpful agent. Use the provided function any time "
                + "you are asked with the weather of any location")
            .setTools(Arrays.asList(azureFnTool));
        BinaryData createAgentRequest = BinaryData.fromObject(createAgentRequestObj);
        PersistentAgent agent = administrationClient.createAgentWithResponse(createAgentRequest, requestOptions)
            .getValue().toObject(PersistentAgent.class);

        PersistentAgentThread thread = threadsClient.createThread();
        ThreadMessage createdMessage = messagesClient.createMessage(
            thread.getId(),
            MessageRole.USER,
            "What is the weather in Seattle, WA?");

        try {
            //run agent
            CreateRunOptions createRunOptions = new CreateRunOptions(thread.getId(), agent.getId())
                .setAdditionalInstructions("");
            ThreadRun threadRun = runsClient.createRun(createRunOptions);

            waitForRunCompletion(thread.getId(), threadRun, runsClient);
            printRunMessages(messagesClient, thread.getId());
        } catch (InterruptedException e) {
            throw new RuntimeException(e);
        } finally {
            //cleanup
            threadsClient.deleteThread(thread.getId());
            administrationClient.deleteAgent(agent.getId());
        }
    }

    // Use "Map.of" if available
    @SuppressWarnings("unchecked")
    private static <T> Map<String, T> mapOf(Object... inputs) {
        Map<String, T> map = new HashMap<>();
        for (int i = 0; i < inputs.length; i += 2) {
            String key = (String) inputs[i];
            T value = (T) inputs[i + 1];
            map.put(key, value);
        }
        return map;
    }
    
    // A helper function to print messages from the agent
    public static void printRunMessages(MessagesClient messagesClient, String threadId) {

        PagedIterable<ThreadMessage> runMessages = messagesClient.listMessages(threadId);
        for (ThreadMessage message : runMessages) {
            System.out.print(String.format("%1$s - %2$s : ", message.getCreatedAt(), message.getRole()));
            for (MessageContent contentItem : message.getContent()) {
                if (contentItem instanceof MessageTextContent) {
                    System.out.print((((MessageTextContent) contentItem).getText().getValue()));
                } else if (contentItem instanceof MessageImageFileContent) {
                    String imageFileId = (((MessageImageFileContent) contentItem).getImageFile().getFileId());
                    System.out.print("Image from ID: " + imageFileId);
                }
                System.out.println();
            }
        }
    }

    // a helper function to wait until a run has completed running
    public static void waitForRunCompletion(String threadId, ThreadRun threadRun, RunsClient runsClient)
        throws InterruptedException {

        do {
            Thread.sleep(500);
            threadRun = runsClient.getRun(threadId, threadRun.getId());
        }
        while (
            threadRun.getStatus() == RunStatus.QUEUED
                || threadRun.getStatus() == RunStatus.IN_PROGRESS
                || threadRun.getStatus() == RunStatus.REQUIRES_ACTION);

        if (threadRun.getStatus() == RunStatus.FAILED) {
            System.out.println(threadRun.getLastError().getMessage());
        }
    }
}
```

:::zone-end