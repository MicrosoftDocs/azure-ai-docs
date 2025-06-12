---
title: 'Grounding with Azure Functions code samples'
titleSuffix: Azure AI Foundry
description: Find code samples to enable Azure AI Agents to use Azure Functions.
services: azure-ai-agent-service
manager: nitinme
ms.service: azure-ai-agent-service
ms.topic: how-to
ms.date: 04/15/2025
author: aahill
ms.author: aahi
ms.custom: azure-ai-agents
---

# Use Azure Functions with Azure AI Foundry Agent Service

The Azure AI Foundry Agent Service integrates with Azure Functions, enabling you to create intelligent, event-driven applications with minimal overhead. This combination allows AI-driven workflows to leverage the scalability and flexibility of serverless computing, making it easier to build and deploy solutions that respond to real-time events or complex workflows. 
 
Azure Functions provide support for triggers and bindings, which simplify how your AI Agents interact with external systems and services. Triggers determine when a function executes—such as an HTTP request, message from a queue, or a file upload to Azure Blob Storage and allows agents to act dynamically based on incoming events. 
 
Meanwhile, bindings facilitate streamlined connections to input or output data sources, such as databases or APIs, without requiring extensive boilerplate code. For instance, you can configure a trigger to execute an Azure Function whenever a customer message is received in a chatbot and use output bindings to send a response via the Azure AI Agent.

### Supported models

To use all features of function calling including parallel functions, you need to use a model that was released after November 6, 2023.

## Prerequisites

* [Azure Functions Core Tools v4.x](/azure/azure-functions/functions-run-local)
* [A deployed agent with the standard setup](/azure/ai-services/agents/ai-services/agents/environment-setupchoose-your-setup)
    > [!NOTE] 
    > The basic agent setup is not supported.
* [Azurite](https://github.com/Azure/Azurite)

## Prepare your local environment

The following examples highlight how to use the Azure AI Foundry Agent Service function calling where function calls are placed on a storage queue by the Agent Service to be processed by an Azure Function listening to that queue.

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
