---
title: Integrate Azure Functions with Foundry Agents
titleSuffix: Microsoft Foundry
description: Build custom agent tools with Azure Functions using queue-based integration. Step-by-step guide with REST examples for Foundry agents.
services: azure-ai-agent-service
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.date: 02/27/2026
author: alvinashcraft
ms.author: aashcraft
ms.custom: azure-ai-agents
---

# Use Azure Functions with Foundry Agent Service

Learn how to integrate [Azure Functions](/azure/azure-functions/functions-overview) with Microsoft Foundry agents by using a queue-based tool approach. This article shows you how to build custom serverless tools that agents can call asynchronously through Azure Queue storage. By using this approach, your agents can access enterprise systems and complex business logic with scale-to-zero pricing.

Foundry agents connect directly to the input queue monitored by Azure Functions by using a tool definition provided by `AzureFunctionsTool`. When an agent needs to use this Azure Functions hosted tool, it uses the tool definition to place a message in an input queue that's monitored by the function app in Azure Functions. An Azure Storage queue trigger invokes the function code to process the message and return a result through an output queue binding. The agent reads the message from the output queue to continue the conversation. 

Functions offer several hosting plans. The [Flex Consumption plan](/azure/azure-functions/flex-consumption-plan) is ideal for hosting your custom tools because it provides:

- Scale-to-zero serverless hosting with consumption-based pricing.
- Identity-based access to resources in Azure, including resources within virtual networks.
- Declarative data source connections through [input/output bindings](/azure/azure-functions/functions-triggers-bindings).

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

## Create an agent version

Create an agent version by using the Azure Function tool definition.

```bash
curl --request POST \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/agents/azure-function-agent-get-weather/versions?api-version=$API_VERSION \
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

## Create a response

Create a response that uses the agent version to get weather information.

```bash
curl --request POST \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/openai/responses?api-version=$API_VERSION \
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
