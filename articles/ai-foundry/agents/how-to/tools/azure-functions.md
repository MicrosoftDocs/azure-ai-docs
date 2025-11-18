---
title: 'Grounding with Azure Functions code samples'
titleSuffix: Microsoft Foundry
description: Find code samples to enable Azure AI Agents to use Azure Functions.
services: azure-ai-agent-service
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.date: 11/04/2025
author: aahill
ms.author: aahi
ms.custom: azure-ai-agents
monikerRange: 'foundry-classic || foundry'
---

# Use Azure Functions with Foundry Agent Service

The Foundry Agent Service integrates with Azure Functions, enabling you to create intelligent, event-driven applications with minimal overhead. This combination allows AI-driven workflows to leverage the scalability and flexibility of serverless computing, making it easier to build and deploy solutions that respond to real-time events or complex workflows.

Currently, direct integration with Azure Functions is only supported for functions triggered by Azure Storage Queues. Other trigger types, such as HTTP or Blob Storage, are not natively supported at this time.

Azure Functions provide support for triggers and bindings, which simplify how your AI Agents interact with external systems and services. Triggers determine when a function executes—such as an HTTP request, message from a queue, or a file upload to Azure Blob Storage—and allow agents to act dynamically based on incoming events.

For HTTP-triggered Azure Functions, integration is possible by describing the function through an OpenAPI specification and registering it as a callable tool in the agent configuration. Alternatively, you can implement a queue-based wrapper function that receives messages from the agent and internally invokes the HTTP logic, enabling the use of the existing queue-based integration.

Meanwhile, bindings facilitate streamlined connections to input or output data sources, such as databases or APIs, without requiring extensive boilerplate code. For instance, you can configure a trigger to execute an Azure Function whenever a customer message is received in a chatbot and use output bindings to send a response via the Azure AI Agent.

### Supported models

To use all features of function calling, including parallel functions, you need to use a model that was released after November 6, 2023.

## Create and deploy the queue-based tool integration sample 

The rest of this article demonstrates how to use an Azure Developer CLI (`azd`) sample that configures a Foundry Agent Service project with Functions to support queue-based tool integration for agents.

> [!NOTE]  
> For detailed instructions on how to define and host Functions-based tools as MCP servers, see [Host MCP servers in Azure Functions](/azure/azure-functions/functions-create-ai-enabled-apps#remote-mcp-servers).

### Prerequisites

* [Azure Functions Core Tools v4.x](/azure/azure-functions/functions-run-local)
* [A deployed agent with the standard setup](../../environment-setup.md#choose-your-setup)
    > [!NOTE] 
    > The basic agent setup isn't supported.
* [Azurite](https://github.com/Azure/Azurite)

## Prepare your local environment

The following examples highlight how to use the Agent Service function calling where function calls are placed on a storage queue by the Agent Service to be processed by an Azure Function listening to that queue.

You can find the template and code used here on [GitHub](https://github.com/Azure-Samples/azure-functions-ai-services-agent-python).

## Usage support

|Azure AI foundry support  | Python SDK |	C# SDK | Java SDK | REST API | Basic agent setup | Standard agent setup |
|---------|---------|---------|---------|---------|---------|---------|
|  | ✔️ | ✔️ | ✔️ | ✔️ | | ✔️ | 

### Initialize the project template

This project uses `azd` to simplify creating Azure resources and deploying your code. This deployment follows current best practices for secure and scalable Functions deployments. You can find the template and code used here on [GitHub](https://github.com/Azure-Samples/azure-functions-ai-services-agent-python).  

1. Run this `azd init` command in a terminal window to initialize your project from the azd template:

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
| Select an Azure Subscription to use | Choose the subscription in which you want your resources to be created.|
| _location_ deployment parameter | Azure region in which to create the resource group that contains the new Azure resources. Only regions that currently support the Flex Consumption plan are shown.|
| _vnetEnabled_ deployment parameter | While the template supports creating resources inside a virtual network, to simplify deployment and testing, choose `False`. |

The `main.bicep` deployment file is then read by `azd` and used to create these resources in Azure:

+ Flex Consumption plan and function app
+ Agent platform in AI Foundry, including:
  + Services account
  + Model deployment
  + Project
  + Agents
  + Search
  + Azure Cosmos DB account (used by search)
+ Azure Storage (required by Functions and AI agents) and Application Insights (recommended)
+ Access policies and roles for your accounts
+ Service-to-service connections using managed identities (instead of stored connection strings)

You can also use these integrated Azure resources in the article [How to use queue-based Azure Functions with Azure AI Foundry agents](azure-functions-samples.md).

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
1. Run the `code .` code command to open the project in Visual Studio Code.
1. In the command palette (F1), type `Azurite: Start`, which enables debugging with local storage for the Functions runtime.
1. Press **Run/Debug (F5)** to run in the debugger. Select **Debug anyway** if prompted about local emulator not running.
1. Send POST `prompt` endpoints respectively using your HTTP test tool. If you have the [RestClient](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) extension installed, you can execute requests directly from the [`test.http`](https://github.com/Azure-Samples/azure-functions-ai-services-agent-python/blob/main/app/test.http) project file.


### Deploy to Azure

Run this `azd deploy` command to publish your project code to the function app and related Azure resources you just provisioned:

```shell
azd deploy
```

After publishing completes successfully, `azd` provides you with the URL endpoints of your new functions, but without the function key values required to access the endpoints. You can use the Azure Functions Core Tools command `func azure functionapp list-functions` with the `--show-keys` option to obtain the keys for your function endpoints. For more information, see [Work with access keys in Azure Functions](/azure/azure-functions/function-keys-how-to?branch=main&tabs=azure-cli#get-your-function-access-keys).

### Redeploy your code

You can run also the `azd up` command as many times as you need to both provision your Azure resources and deploy code updates to your function app.

> [!NOTE]
> Deployed code files are always overwritten by the latest deployment package.

### Clean up resources

When you're done working with your function app and related resources, use this command to delete the function app and its related resources from Azure and avoid incurring any further costs (`--purge` doesn't leave a soft delete of AI resource and recovers your quota):

```shell
azd down --purge
```