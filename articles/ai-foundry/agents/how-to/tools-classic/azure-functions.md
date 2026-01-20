---
title: 'Use Azure Functions with Foundry Agent Service'
titleSuffix: Microsoft Foundry
description: Learn how to build custom tools with code hosted in Azure Functions and integrate them with Microsoft Foundry agents.
services: azure-ai-agent-service
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.date: 11/20/2025
author: alvinashcraft
ms.author: aashcraft
ms.custom: azure-ai-agents
---

# Use Azure Functions with Foundry Agent Service

[!INCLUDE [classic-banner](../../../includes/classic-banner.md)]


[Azure Functions](/azure/azure-functions/functions-overview) is a serverless compute service that you can use to extend your Foundry Agent Service agents with custom tools built using code. This approach is especially useful when you need your agent to integrate with systems within your enterprise.

Functions offer several hosting plans. The [Flex Consumption plan](/azure/azure-functions/flex-consumption-plan) is ideal for hosting your custom tools because it provides:

- Scale-to-zero serverless hosting with consumption-based pricing.
- Identity-based access to resources in Azure, including resources within virtual networks.
- Declarative data source connections through [input/output bindings](/azure/azure-functions/functions-triggers-bindings).

## When to use Azure Functions vs function calling

While [function calling](function-calling.md) allows you to define tools that run in-process with your agent code, hosting custom tools on Azure Functions provides additional enterprise capabilities when you need:

- **Separation of concerns**: Isolate your business logic from agent code, enabling independent development, testing, and deployment cycles.
- **Centralized management**: Create reusable tools that multiple agents, applications, or teams can consume consistently.
- **Security isolation**: Control agent access to tools separately from tool access to enterprise resources. This approach allows you to assign agents only the specific permissions they need to call the tool without having to provide direct access to underlying databases, APIs, or networks.
- **External dependencies**: Leverage non-Microsoft libraries, specific runtime environments, or your legacy system integrations.
- **Complex operations**: Handle multistep workflows and data transformations, or offload computationally intensive operations.
- **Asynchronous processing**: Execute long-running operations with retry capabilities and resilient message handling.

## Integration options

Foundry Agent Service provides two primary ways for your agents to access Azure Functions-hosted tools:

| Feature | Model Context Protocol (MCP) servers | Azure Queue storage-based tools  |
|---------|------|------|
| **How does it work?** | Agents connect to your function app in Azure by using the MCP protocol. The function app itself serves as a custom MCP server, exposing your individual functions as tools. A custom MCP server abstracts the complexity of hosting and exposing tools from your agent project and promotes reusability of your code. | Agents communicate with tool code in your function app in Azure through Queue storage by placing messages in a queue, which triggers tool code execution. The function app listens to the input queues, processes messages asynchronously, and returns a response to a second queue. |
| **When to use it?** | ✔ Best for leveraging the industry standard protocol for agent tool integration.<br/>✔ Provides real-time, synchronous interactions with immediate responses. | ✔ Best for asynchronous workflows that don't require real time responses.<br/>✔ Ideal for background processing and reliable message delivery with retry capabilities. |
| **SDK configuration** | Generic [MCP tool](model-context-protocol-samples.md) | Specific [Azure Functions tool](azure-functions-samples.md) |
| **Get started** | [How to use Azure Functions with MCP](/azure/azure-functions/functions-create-ai-enabled-apps#remote-mcp-servers) | [How to use Azure Functions with queues](azure-functions-samples.md) |

For HTTP-trigger functions, you can also integrate by describing the function through an OpenAPI specification and registering it as a callable tool by using the [OpenAPI tool](openapi-spec.md) in your agent configuration. This approach provides flexibility for existing HTTP-based functions, but it requires additional setup to define the API specification.

## Supported models

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
* An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

### Usage support

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
+ Agent platform in Foundry, including:
  + Services account
  + Model deployment
  + Project
  + Agents
  + Search
  + Azure Cosmos DB account (used by search)
+ Azure Storage (required by Functions and AI agents) and Application Insights (recommended)
+ Access policies and roles for your accounts
+ Service-to-service connections using managed identities (instead of stored connection strings)

You can also use these integrated Azure resources in the article [How to use queue-based Azure Functions with Microsoft Foundry agents](azure-functions-samples.md).

Post-provision scripts also create a `local.settings.json` file, which Functions requires to run locally. The generated file should look like this:

```json
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "UseDevelopmentStorage=true",
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "STORAGE_CONNECTION__queueServiceUri": "https://<storageaccount>.queue.core.windows.net",
    "PROJECT_CONNECTION_STRING": "<project connection for AI Project>"
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