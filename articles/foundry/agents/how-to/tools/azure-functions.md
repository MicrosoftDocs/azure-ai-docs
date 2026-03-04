---
title: Integrate Azure Functions with Foundry Agents
titleSuffix: Microsoft Foundry
description: Build custom agent tools with Azure Functions using queue-based integration. Step-by-step guide with code examples for Foundry agents.
services: azure-ai-agent-service
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.date: 03/03/2026
author: alvinashcraft
ms.author: aashcraft
ms.custom: azure-ai-agents, doc-kit-assisted
zone_pivot_groups: selection-azure-function-tool
ai-usage: ai-assisted
---

# Use Azure Functions with Foundry Agent Service

Learn how to integrate [Azure Functions](/azure/azure-functions/functions-overview) with Microsoft Foundry agents by using a queue-based tool approach. This article shows you how to build custom serverless tools that agents can call asynchronously through Azure Queue storage. By using this approach, your agents can access enterprise systems and complex business logic with scale-to-zero pricing.

Foundry agents connect directly to the input queue monitored by Azure Functions by using a tool definition provided by `AzureFunctionsTool`. When an agent needs to use this Azure Functions hosted tool, it uses the tool definition to place a message in an input queue that's monitored by the function app in Azure Functions. An Azure Storage queue trigger invokes the function code to process the message and return a result through an output queue binding. The agent reads the message from the output queue to continue the conversation. 

Functions offer several hosting plans. The [Flex Consumption plan](/azure/azure-functions/flex-consumption-plan) is ideal for hosting your custom tools because it provides:

- Scale-to-zero serverless hosting with consumption-based pricing.
- Identity-based access to resources in Azure, including resources within virtual networks.
- Declarative data source connections through [input/output bindings](/azure/azure-functions/functions-triggers-bindings).

## Usage support

✔️ (GA) indicates general availability, ✔️ (Preview) indicates public preview, and a dash (-) indicates the feature isn't available.

| Microsoft Foundry support | Python SDK | C# SDK | JavaScript SDK | Java SDK | REST API | Basic agent setup | Standard agent setup |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ✔️ | ✔️ (GA) | ✔️ (Preview) | ✔️ (GA) | ✔️ (Preview) | ✔️ (GA) | - | ✔️ |

## Prerequisites

- The latest prerelease package. See the [quickstart](../../../quickstarts/get-started-code.md) for installation details.
- [Azure Functions Core Tools v4.x](/azure/azure-functions/functions-run-local)
- [A deployed agent with the standard setup](../../environment-setup.md#choose-your-setup)

  > [!NOTE] 
  > The basic agent setup isn't supported.

- [Azurite](https://github.com/Azure/Azurite)
- An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

## Code samples

The following code samples demonstrate how to define an Azure Function tool that gets weather information for a specified location by using queue-based integration.

:::zone pivot="python"

### Install the package

Install the Azure AI Projects client library:

```bash
pip install azure-ai-projects azure-identity
```

### Define the tool and create an agent

```python
import os
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    AzureFunctionBinding,
    AzureFunctionDefinition,
    AzureFunctionStorageQueue,
    AzureFunctionDefinitionFunction,
    AzureFunctionTool,
    PromptAgentDefinition,
)

endpoint = os.environ["FOUNDRY_PROJECT_ENDPOINT"]

with (
    DefaultAzureCredential() as credential,
    AIProjectClient(endpoint=endpoint, credential=credential) as project_client,
    project_client.get_openai_client() as openai_client,
):
    tool = AzureFunctionTool(
        azure_function=AzureFunctionDefinition(
            input_binding=AzureFunctionBinding(
                storage_queue=AzureFunctionStorageQueue(
                    queue_name=os.environ["STORAGE_INPUT_QUEUE_NAME"],
                    queue_service_endpoint=os.environ["STORAGE_QUEUE_SERVICE_ENDPOINT"],
                )
            ),
            output_binding=AzureFunctionBinding(
                storage_queue=AzureFunctionStorageQueue(
                    queue_name=os.environ["STORAGE_OUTPUT_QUEUE_NAME"],
                    queue_service_endpoint=os.environ["STORAGE_QUEUE_SERVICE_ENDPOINT"],
                )
            ),
            function=AzureFunctionDefinitionFunction(
                name="GetWeather",
                description="Get the weather in a location.",
                parameters={
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The location to look up.",
                        }
                    },
                },
            ),
        )
    )

    agent = project_client.agents.create_version(
        agent_name="azure-function-agent-get-weather",
        definition=PromptAgentDefinition(
            model=os.environ["FOUNDRY_MODEL_DEPLOYMENT_NAME"],
            instructions="You are a helpful support agent. Answer the user's questions to the best of your ability.",
            tools=[tool],
        ),
    )
    print(f"Agent created (id: {agent.id}, name: {agent.name}, version: {agent.version})")
```

### Create a response

```python
    response = openai_client.responses.create(
        input="What is the weather in Seattle, WA?",
        extra_body={"agent_reference": {"name": agent.name, "type": "agent_reference"}},
    )

    print(f"Response: {response.output_text}")
```

### Clean up

```python
    project_client.agents.delete_version(agent_name=agent.name, agent_version=agent.version)
    print("Agent deleted")
```

### Write the Azure Function

The previous code samples show how to define the Azure Function tool on the agent side. You also need to write the function that processes the queue messages. The function receives input from the input queue, runs your custom logic, and returns a result through the output queue.

The following example shows a queue-triggered function that gets weather information for a location. The function parses the incoming message, extracts the function arguments, and returns a response with a `CorrelationId` that the agent uses to match the result to the original request.

```python
import azure.functions as func
import logging
import json

app = func.FunctionApp()


# Queue trigger receives agent tool calls from the input queue
# and returns results through the output queue binding
@app.queue_trigger(
    arg_name="msg",
    queue_name="get-weather-input-queue",
    connection="STORAGE_CONNECTION",
)
@app.queue_output(
    arg_name="outputQueue",
    queue_name="get-weather-output-queue",
    connection="STORAGE_CONNECTION",
)
def queue_trigger(
    msg: func.QueueMessage, outputQueue: func.Out[str]
):
    try:
        # Parse the incoming message from the agent
        messagepayload = json.loads(
            msg.get_body().decode("utf-8")
        )
        logging.info("Received: %s", json.dumps(messagepayload))

        # Extract the function arguments
        function_args = messagepayload.get("function_args", {})
        location = function_args.get("location")

        # Run your custom logic (replace with real API calls)
        weather_result = (
            f"Weather is {len(location)} degrees "
            f"and sunny in {location}"
        )

        # Return result with the CorrelationId from the request
        response_message = {
            "Value": weather_result,
            "CorrelationId": messagepayload["CorrelationId"],
        }
        outputQueue.set(json.dumps(response_message))

    except Exception as e:
        logging.error("Error processing message: %s", e)
```

> [!IMPORTANT]
> The response message must include the `CorrelationId` from the original message. The agent uses this value to match the function output to the correct tool call.

For the full sample, see [Azure Functions weather sample](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/agents/tools/get_weather_func_app.py) in the Azure SDK for Python repository.

:::zone-end

:::zone pivot="csharp"

### Install the packages

Install the Azure AI Projects client libraries:

```dotnetcli
dotnet add package Azure.AI.Projects --prerelease
dotnet add package Azure.AI.Projects.OpenAI --prerelease
dotnet add package Azure.Identity
```

### Define the tool and create an agent

```csharp
using System;
using System.Text.Json;
using Azure.AI.Projects;
using Azure.AI.Projects.OpenAI;
using Azure.Identity;

var projectEndpoint = Environment.GetEnvironmentVariable("FOUNDRY_PROJECT_ENDPOINT");
var modelDeploymentName = Environment.GetEnvironmentVariable("FOUNDRY_MODEL_DEPLOYMENT_NAME");
var storageQueueUri = Environment.GetEnvironmentVariable("STORAGE_QUEUE_URI");

AIProjectClient projectClient = new(
    endpoint: new Uri(projectEndpoint),
    tokenProvider: new DefaultAzureCredential());

AzureFunctionDefinitionFunction functionDefinition = new(
    name: "GetWeather",
    parameters: BinaryData.FromObjectAsJson(
        new
        {
            Type = "object",
            Properties = new
            {
                location = new
                {
                    Type = "string",
                    Description = "The location to look up.",
                }
            }
        },
        new JsonSerializerOptions() { PropertyNamingPolicy = JsonNamingPolicy.CamelCase }
    )
)
{
    Description = "Get the weather in a location.",
};

AzureFunctionTool azureFnTool = new(
    new AzureFunctionDefinition(
        function: functionDefinition,
        inputBinding: new AzureFunctionBinding(
            new AzureFunctionStorageQueue(
                queueServiceEndpoint: storageQueueUri,
                queueName: "input")),
        outputBinding: new AzureFunctionBinding(
            new AzureFunctionStorageQueue(
                queueServiceEndpoint: storageQueueUri,
                queueName: "output"))
    )
);

PromptAgentDefinition agentDefinition = new(model: modelDeploymentName)
{
    Instructions = "You are a helpful support agent. Answer the user's questions "
        + "to the best of your ability.",
    Tools = { azureFnTool },
};

AgentVersion agentVersion = await projectClient.Agents.CreateAgentVersionAsync(
    agentName: "azure-function-agent-get-weather",
    options: new(agentDefinition));
Console.WriteLine($"Agent created (id: {agentVersion.Id}, name: {agentVersion.Name}, "
    + $"version: {agentVersion.Version})");
```

### Create a response

```csharp
ProjectResponsesClient responseClient =
    projectClient.OpenAI.GetProjectResponsesClientForAgent(agentVersion.Name);

CreateResponseOptions responseOptions = new()
{
    InputItems =
    {
        ResponseItem.CreateUserMessageItem("What is the weather in Seattle, WA?")
    },
};

ResponseResult response = await responseClient.CreateResponseAsync(responseOptions);
Console.WriteLine(response.GetOutputText());
```

### Clean up

```csharp
await projectClient.Agents.DeleteAgentVersionAsync(
    agentName: agentVersion.Name,
    agentVersion: agentVersion.Version);
Console.WriteLine("Agent deleted");
```

### Write the Azure Function

The previous code samples show how to define the Azure Function tool on the agent side. You also need to write the function that processes the queue messages. The function receives input from the input queue, runs your custom logic, and returns a result through the output queue.

The following example shows a queue-triggered function that gets weather information for a location. This example uses the [isolated worker model](/azure/azure-functions/dotnet-isolated-process-guide). The function parses the incoming message, extracts the function arguments, and returns a response with a `CorrelationId` that the agent uses to match the result to the original request.

```csharp
using System.Text.Json;
using Microsoft.Azure.Functions.Worker;
using Microsoft.Extensions.Logging;

public class GetWeather
{
    private readonly ILogger<GetWeather> _logger;

    public GetWeather(ILogger<GetWeather> logger)
    {
        _logger = logger;
    }

    // Queue trigger receives agent tool calls from the input
    // queue and returns results through the output queue
    [Function("GetWeather")]
    [QueueOutput(
        "get-weather-output-queue",
        Connection = "STORAGE_CONNECTION")]
    public string Run(
        [QueueTrigger(
            "get-weather-input-queue",
            Connection = "STORAGE_CONNECTION")]
        string message)
    {
        _logger.LogInformation("Received: {Message}", message);

        // Parse the incoming message from the agent
        var payload = JsonSerializer.Deserialize<JsonElement>(
            message);
        var correlationId = payload
            .GetProperty("CorrelationId").GetString();
        var functionArgs = payload
            .GetProperty("function_args");
        var location = functionArgs
            .GetProperty("location").GetString();

        // Run your custom logic (replace with real API calls)
        var weatherResult =
            $"Weather is {location!.Length} degrees "
            + $"and sunny in {location}";

        // Return result with the CorrelationId from the request
        var response = new
        {
            Value = weatherResult,
            CorrelationId = correlationId,
        };
        return JsonSerializer.Serialize(response);
    }
}
```

> [!IMPORTANT]
> The response message must include the `CorrelationId` from the original message. The agent uses this value to match the function output to the correct tool call.

:::zone-end

:::zone pivot="java"

### Install the package

Add the Azure AI Agents dependency to your `pom.xml`:

```xml
<dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-ai-agents</artifactId>
    <version>1.0.0-beta.1</version>
</dependency>
<dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-identity</artifactId>
</dependency>
```

### Define the tool and create an agent

```java
import com.azure.ai.agents.*;
import com.azure.ai.agents.models.*;
import com.azure.core.util.BinaryData;
import com.azure.core.util.Configuration;
import com.azure.identity.DefaultAzureCredentialBuilder;
import com.openai.models.responses.Response;
import com.openai.models.responses.ResponseCreateParams;

import java.util.*;

String endpoint = Configuration.getGlobalConfiguration().get("AZURE_AGENTS_ENDPOINT");
String model = Configuration.getGlobalConfiguration().get("AZURE_AGENTS_MODEL");
String storageQueueUri = Configuration.getGlobalConfiguration().get("STORAGE_QUEUE_URI");

AgentsClientBuilder builder = new AgentsClientBuilder()
    .credential(new DefaultAzureCredentialBuilder().build())
    .endpoint(endpoint)
    .serviceVersion(AgentsServiceVersion.getLatest());

AgentsClient agentsClient = builder.buildAgentsClient();
ResponsesClient responsesClient = builder.buildResponsesClient();

// Define the function parameters
Map<String, BinaryData> parameters = new HashMap<>();
parameters.put("type", BinaryData.fromString("\"object\""));
parameters.put("properties", BinaryData.fromString(
    "{\"location\": {\"type\": \"string\", "
    + "\"description\": \"The location to look up.\"}}"));

AzureFunctionDefinitionFunction function =
    new AzureFunctionDefinitionFunction("GetWeather", parameters)
        .setDescription("Get the weather in a location.");

AzureFunctionTool azureFnTool = new AzureFunctionTool(
    new AzureFunctionDefinition(
        function,
        new AzureFunctionBinding(
            new AzureFunctionStorageQueue(storageQueueUri, "input")),
        new AzureFunctionBinding(
            new AzureFunctionStorageQueue(storageQueueUri, "output"))
    )
);

PromptAgentDefinition agentDefinition = new PromptAgentDefinition(model)
    .setInstructions("You are a helpful support agent. Answer the user's "
        + "questions to the best of your ability.")
    .setTools(Collections.singletonList(azureFnTool));

AgentVersionDetails agent = agentsClient.createAgentVersion(
    "azure-function-agent-get-weather", agentDefinition);
System.out.printf("Agent created (id: %s, name: %s, version: %s)%n",
    agent.getId(), agent.getName(), agent.getVersion());
```

### Create a response

```java
AgentReference agentReference = new AgentReference(agent.getName())
    .setVersion(agent.getVersion());

Response response = responsesClient.createWithAgent(
    agentReference,
    ResponseCreateParams.builder()
        .input("What is the weather in Seattle, WA?"));

System.out.println("Response: " + response.output());
```

### Clean up

```java
agentsClient.deleteAgentVersion(agent.getName(), agent.getVersion());
System.out.println("Agent deleted");
```

### Write the Azure Function

The previous code samples show how to define the Azure Function tool on the agent side. You also need to write the function that processes the queue messages. The function receives input from the input queue, runs your custom logic, and returns a result through the output queue.

The following example shows a queue-triggered function that gets weather information for a location. The function parses the incoming message, extracts the function arguments, and returns a response with a `CorrelationId` that the agent uses to match the result to the original request.

```java
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import com.microsoft.azure.functions.*;
import com.microsoft.azure.functions.annotation.*;

import java.util.logging.Logger;

public class GetWeather {

    // Queue trigger receives agent tool calls from the input
    // queue and returns results through the output queue
    @FunctionName("GetWeather")
    @QueueOutput(
        name = "output",
        queueName = "get-weather-output-queue",
        connection = "STORAGE_CONNECTION")
    public String run(
            @QueueTrigger(
                name = "msg",
                queueName = "get-weather-input-queue",
                connection = "STORAGE_CONNECTION")
            String message,
            final ExecutionContext context) {

        Logger logger = context.getLogger();
        logger.info("Received: " + message);

        // Parse the incoming message from the agent
        JsonObject payload =
            JsonParser.parseString(message)
                .getAsJsonObject();
        String correlationId =
            payload.get("CorrelationId").getAsString();
        JsonObject functionArgs =
            payload.getAsJsonObject("function_args");
        String location =
            functionArgs.get("location").getAsString();

        // Run your custom logic (replace with real API calls)
        String weatherResult =
            "Weather is " + location.length()
            + " degrees and sunny in " + location;

        // Return result with the CorrelationId
        JsonObject response = new JsonObject();
        response.addProperty("Value", weatherResult);
        response.addProperty(
            "CorrelationId", correlationId);
        return response.toString();
    }
}
```

> [!IMPORTANT]
> The response message must include the `CorrelationId` from the original message. The agent uses this value to match the function output to the correct tool call.

:::zone-end

:::zone pivot="typescript"

### Install the packages

Install the Azure AI Projects client library:

```bash
npm install @azure/ai-projects @azure/identity
```

### Define the tool and create an agent

```typescript
import { AIProjectClient } from "@azure/ai-projects";
import { DefaultAzureCredential } from "@azure/identity";
import "dotenv/config";

const projectEndpoint = process.env["FOUNDRY_PROJECT_ENDPOINT"] || "";
const deploymentName = process.env["FOUNDRY_MODEL_DEPLOYMENT_NAME"] || "";
const storageQueueEndpoint = process.env["STORAGE_QUEUE_SERVICE_ENDPOINT"] || "";
const inputQueueName = process.env["STORAGE_INPUT_QUEUE_NAME"] || "input";
const outputQueueName = process.env["STORAGE_OUTPUT_QUEUE_NAME"] || "output";

const project = new AIProjectClient(projectEndpoint, new DefaultAzureCredential());
const openAIClient = project.getOpenAIClient();

const agent = await project.agents.createVersion(
  "azure-function-agent-get-weather",
  {
    kind: "prompt",
    model: deploymentName,
    instructions:
      "You are a helpful support agent. Answer the user's questions to the best of your ability.",
    tools: [
      {
        type: "azure_function",
        azure_function: {
          function: {
            name: "GetWeather",
            description: "Get the weather in a location.",
            parameters: {
              type: "object",
              properties: {
                location: {
                  type: "string",
                  description: "The location to look up.",
                },
              },
            },
          },
          input_binding: {
            type: "storage_queue",
            storage_queue: {
              queue_service_endpoint: storageQueueEndpoint,
              queue_name: inputQueueName,
            },
          },
          output_binding: {
            type: "storage_queue",
            storage_queue: {
              queue_service_endpoint: storageQueueEndpoint,
              queue_name: outputQueueName,
            },
          },
        },
      },
    ],
  },
);
console.log(`Agent created (id: ${agent.id}, name: ${agent.name}, version: ${agent.version})`);
```

### Create a response

```typescript
const response = await openAIClient.responses.create(
  {
    input: "What is the weather in Seattle, WA?",
  },
  {
    body: {
      agent: { name: agent.name, type: "agent_reference" },
    },
  },
);
console.log(`Response: ${response.output_text}`);
```

### Clean up

```typescript
await project.agents.deleteVersion(agent.name, agent.version);
console.log("Agent deleted");
```

### Write the Azure Function

The previous code samples show how to define the Azure Function tool on the agent side. You also need to write the function that processes the queue messages. The function receives input from the input queue, runs your custom logic, and returns a result through the output queue.

The following example shows a queue-triggered function that gets weather information for a location. This example uses the [v4 programming model](/azure/azure-functions/functions-reference-node). The function parses the incoming message, extracts the function arguments, and returns a response with a `CorrelationId` that the agent uses to match the result to the original request.

```typescript
import {
  app,
  InvocationContext,
  output,
} from "@azure/functions";

// Define the output queue binding
const queueOutput = output.storageQueue({
  queueName: "get-weather-output-queue",
  connection: "STORAGE_CONNECTION",
});

interface AgentMessage {
  CorrelationId: string;
  function_args: { location: string };
}

// Queue trigger receives agent tool calls from the input
// queue and returns results through the output queue
async function getWeather(
  message: unknown,
  context: InvocationContext
): Promise<void> {
  const payload = message as AgentMessage;
  context.log("Received:", JSON.stringify(payload));

  // Extract the function arguments
  const location = payload.function_args.location;

  // Run your custom logic (replace with real API calls)
  const weatherResult =
    `Weather is ${location.length} degrees ` +
    `and sunny in ${location}`;

  // Return result with the CorrelationId from the request
  const response = {
    Value: weatherResult,
    CorrelationId: payload.CorrelationId,
  };
  context.extraOutputs.set(queueOutput, response);
}

// Register the queue trigger function
app.storageQueue("getWeather", {
  queueName: "get-weather-input-queue",
  connection: "STORAGE_CONNECTION",
  extraOutputs: [queueOutput],
  handler: getWeather,
});
```

> [!IMPORTANT]
> The response message must include the `CorrelationId` from the original message. The agent uses this value to match the function output to the correct tool call.

:::zone-end

:::zone pivot="rest"

### Create an agent version

Create an agent version by using the Azure Function tool definition.

```bash
curl --request POST \
  --url $FOUNDRY_PROJECT_ENDPOINT/agents/azure-function-agent-get-weather/versions?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Agent with Azure Function tool",
    "definition": {
      "kind": "prompt",
      "model": "gpt-4o-mini",
      "instructions": "You are a helpful support agent. Answer the user's questions to the best of your ability.",
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
    }
  }'
```

### Create a response

Create a response that uses the agent version to get weather information.

```bash
curl --request POST \
  --url $FOUNDRY_PROJECT_ENDPOINT/openai/responses?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "input": "What is the weather in Seattle, WA?",
    "agent": {
      "name": "azure-function-agent-get-weather",
      "type": "agent_reference"
    }
  }'
```

### Write the Azure Function

The REST API examples show how to configure the Azure Function tool definition. The Azure Function itself is server-side code that you write in a supported Functions language. Select one of the other languages (Python, C#, Java, or TypeScript) to see the function implementation.

:::zone-end

## When to use Azure Functions vs function calling

While [function calling](function-calling.md) enables you to define tools that run in-process with your agent code, hosting custom tools on Azure Functions provides extra enterprise capabilities when you need:

- **Separation of concerns**: Isolate your business logic from agent code, so you can develop, test, and deploy independently.
- **Centralized management**: Create reusable tools that multiple agents, applications, or teams can use consistently.
- **Security isolation**: Control agent access to tools separately from tool access to enterprise resources. This approach means you can assign agents only the specific permissions they need to call the tool without having to provide direct access to underlying databases, APIs, or networks.
- **External dependencies**: Use non-Microsoft libraries, specific runtime environments, or your legacy system integrations.
- **Complex operations**: Handle multistep workflows and data transformations, or offload computationally intensive operations.
- **Asynchronous processing**: Execute long-running operations with retry capabilities and resilient message handling.

## Integration options

Foundry Agent Service provides two primary ways for your agents to access Azure Functions-hosted tools:

| Feature | Model Context Protocol (MCP) servers | Azure Queue storage-based tools |
| ------ | ------ | ------ |
| **How does it work?** | Agents connect to your function app in Azure by using the MCP protocol. The function app itself serves as a custom MCP server, exposing your individual functions as tools. A custom MCP server abstracts the complexity of hosting and exposing tools from your agent project and promotes reusability of your code. | Agents communicate with tool code in your function app in Azure through Queue storage by placing messages in a queue, which triggers tool code execution. The function app listens to the input queues, processes messages asynchronously, and returns a response to a second queue. |
| **When to use it?** | ✔ Best for leveraging the industry standard protocol for agent tool integration.<br/>✔ Provides real-time, synchronous interactions with immediate responses. | ✔ Best for asynchronous workflows that don't require real time responses.<br/>✔ Ideal for background processing and reliable message delivery with retry capabilities. |
| **SDK configuration** | Generic [MCP tool](model-context-protocol.md) | Specific (see [Code samples](#code-samples) above) |
| **Get started** | [How to use Azure Functions with MCP](/azure/azure-functions/functions-create-ai-enabled-apps#remote-mcp-servers) | See [Code samples](#code-samples) above. |

For HTTP-trigger functions, you can also integrate by describing the function through an OpenAPI specification and registering it as a callable tool by using the [OpenAPI tool](openapi.md) in your agent configuration. This approach provides flexibility for existing HTTP-based functions, but it requires additional setup to define the API specification.

## Supported models

To use all features of function calling, including parallel functions, use a model that was released after November 6, 2023.

## Create and deploy the queue-based tool integration sample

To use an Azure Developer CLI (`azd`) sample that configures an agent with Functions to support queue-based tool integration for agents, follow these steps:

> [!NOTE]  
> For detailed instructions on how to define and host Functions-based tools as MCP servers, see [Host MCP servers in Azure Functions](/azure/azure-functions/functions-create-ai-enabled-apps#remote-mcp-servers).

### Initialize the project template

This project uses `azd` to simplify creating Azure resources and deploying your code. This deployment follows current best practices for secure and scalable Functions deployments. You can find the template and code used here on [GitHub](https://github.com/Azure-Samples/azure-functions-ai-services-agent-python).  

1. Run the following `azd init` command in a terminal window to initialize your project from the azd template:

    ```bash
    azd init --template azure-functions-ai-services-agent-python
    ```

 When prompted, provide an environment name, such as `ai-services-agent-python`. In `azd`, the environment maintains a unique deployment context for your app, and you can define more than one. The environment name is also used in the name of the resource group and other resources you create in Azure.    

1. Run this command to allow local setup scripts to run successfully, which depends on your local operating system: 

    #### [Mac/Linux](#tab/mac-linux)
    
    ```bash
    chmod +x ./infra/scripts/*.sh 
    ```
    #### [Windows](#tab/windows)
    
    ```Powershell
    set-executionpolicy remotesigned
    ```
    ---

### Provision resources

Run the `azd provision` command to create the required resources in Azure:

```bash
azd provision
```

When prompted, provide these required deployment parameters:

| Prompt | Description |
| ---- | ---- |
| Select an Azure Subscription to use | Choose the subscription in which you want to create your resources. |
| _location_ deployment parameter | Azure region to create the resource group that contains the new Azure resources. Only regions that currently support the Flex Consumption plan are shown. |
| _vnetEnabled_ deployment parameter | While the template supports creating resources inside a virtual network, choose `False` to simplify deployment and testing. |

`azd` reads the `main.bicep` deployment file and uses it to create these resources in Azure:

+ Flex Consumption plan and function app
+ Agent platform in Foundry, including:
  + Services account
  + Model deployment
  + Project
  + Agents
  + Search
  + Azure Cosmos DB account (used by search)
+ Azure Storage (required by Functions and AI agents) and Application Insights (recommended)
+ Access policies and roles for your accounts
+ Service-to-service connections that use managed identities (instead of stored connection strings)

Post-provision scripts also create a `local.settings.json` file, which Functions requires to run locally. The generated file should look like this:

```json
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "UseDevelopmentStorage=true",
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "STORAGE_CONNECTION__queueServiceUri": "https://<storageaccount>.queue.core.windows.net",
    "PROJECT_CONNECTION_STRING": "<project connnection for AI Project>"
    }
}
```

### Run your app in Visual Studio Code

1. Open the folder in a new terminal.
1. Run the `code .` command to open the project in Visual Studio Code.
1. In the command palette (F1), type `Azurite: Start`. This action enables debugging by using local storage for the Functions runtime.
1. Press **Run/Debug (F5)** to run the debugger. Select **Debug anyway** if prompted about local emulator not running.
1. Send POST `prompt` endpoints respectively by using your HTTP test tool. If you have the [RestClient](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) extension installed, you can execute requests directly from the [`test.http`](https://github.com/Azure-Samples/azure-functions-ai-services-agent-python/blob/main/app/test.http) project file.

### Deploy to Azure

Run this `azd deploy` command to publish your project code to the function app and related Azure resources you just provisioned:

```shell
azd deploy
```

After publishing completes successfully, `azd` provides you with the URL endpoints of your new functions, but without the function key values required to access the endpoints. You can use the Azure Functions Core Tools command `func azure functionapp list-functions` with the `--show-keys` option to get the keys for your function endpoints. For more information, see [Work with access keys in Azure Functions](/azure/azure-functions/function-keys-how-to?branch=main&tabs=azure-cli#get-your-function-access-keys).

### Redeploy your code

Run the `azd up` command as many times as you need to both provision your Azure resources and deploy code updates to your function app.

> [!NOTE]
> The latest deployment package always overwrites deployed code files.

### Clean up resources

When you're done working with your function app and related resources, use this command to delete the function app and its related resources from Azure and avoid incurring any further costs. The `--purge` option doesn't leave a soft delete of AI resource and recovers your quota:

```shell
azd down --purge
```
