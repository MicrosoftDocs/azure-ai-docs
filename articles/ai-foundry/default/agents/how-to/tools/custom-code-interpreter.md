---
title: Use custom code interpreter with agents
titleSuffix: Microsoft Foundry
description: Configure a custom code interpreter for Microsoft Foundry agents. Customize Python packages and compute by using Azure Container Apps Dynamic Sessions and MCP.
services: azure-ai-agent-service
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.date: 01/19/2026
author: alvinashcraft
ms.author: aashcraft
ms.custom: pilot-ai-workflow-jan-2026
ai-usage: ai-assisted
---

# Custom code interpreter tool for agents (preview)

[!INCLUDE [feature-preview](../../../../includes/feature-preview.md)]

By using a custom code interpreter for your agent, you can customize the resources, available Python packages, and [Azure Container Apps environment](/azure/container-apps/environment) that the agent uses to run the Python code it writes. The code interpreter container exposes a Model Context Protocol (MCP) server.

Use a custom code interpreter when you need more control over the runtime than the built-in [Code Interpreter tool for agents](code-interpreter.md) provides.

For more information about MCP and how agents connect to MCP tools, see [Connect to Model Context Protocol servers (preview)](model-context-protocol.md).

## Usage support

This article uses the Azure CLI and a runnable sample project.

For the latest SDK and API support for agents tools, see [Best practices for using tools in Microsoft Foundry Agent Service](../../concepts/tool-best-practice.md).

## Prerequisites

To use the preview feature, you need the following prerequisites:

- The [Azure CLI](/cli/azure/install-azure-cli).
- Optionally install `uv` as an alternative to `pip`. `uv` is a fast package and project manager for Python projects. You can install it by following the instructions at [Installing uv](https://docs.astral.sh/uv/getting-started/installation/) in the official documentation.
- An Azure subscription and resource group with the following permissions:
  - [Azure AI Owner](/azure/role-based-access-control/built-in-roles/ai-machine-learning#azure-ai-owner)
  - [Container Apps ManagedEnvironment Contributor](/azure/role-based-access-control/built-in-roles/containers#container-apps-managedenvironments-contributor)
- The latest prerelease package. See the [quickstart](../../../../quickstarts/get-started-code.md?view=foundry&preserve-view=true) for details.

## Before you begin

This procedure provisions Azure infrastructure, including Azure Container Apps resources. Review Azure cost and governance requirements for your organization before you deploy.

## Custom code interpreter example

The following console commands and code samples show how to create an agent that uses a custom code interpreter MCP server.

### Enable MCP server for dynamic sessions

To enable the preview feature, run the following commands.

```console
az feature register --namespace Microsoft.App --name SessionPoolsSupportMCP
az provider register -n Microsoft.App
```

### Get the sample code

Clone the [sample code in the GitHub repo](https://github.com/azure-ai-foundry/foundry-samples) and navigate to the `samples/python/hosted-agents/code-interpreter-custom` folder in your terminal.

### Provision the infrastructure

To provision the infrastructure, run the following command by using the Azure CLI (`az`):

```console
az deployment group create \
    --name custom-code-interpreter \
    --subscription <your_subscription> \
    --resource-group <your_resource_group> \
    --template-file ./infra.bicep
```

> [!NOTE]
> This process can take a while. Allocating the dynamic session pool can take up to one hour, depending on the number of standby instances you request.

### Use the custom code interpreter in an agent

Copy the `.env.sample` file from the repository to `.env` and fill in the values with the output from the preceding deployment. You can find this output in the Azure portal under the resource group.

Install the Python dependencies by using `uv sync` or `pip install`. Finally, run `./main.py`.

## Verify your setup

After you provision the infrastructure and run the sample:

1. Confirm the Azure deployment completes successfully.
1. Confirm the sample can connect by using the values in your `.env` file.
1. In Microsoft Foundry, verify your agent calls the tool by using tracing. For more information, see [Best practices for using tools in Microsoft Foundry Agent Service](../../concepts/tool-best-practice.md).

## Troubleshooting

### Feature registration is still pending

If `az feature register` returns a `Registering` state, wait for the registration to complete and then run `az provider register -n Microsoft.App` again.

### Deployment fails

If `az deployment group create` fails:

- Confirm you have the required role assignments in the target subscription and resource group.
- Confirm the resource group exists and the selected region supports the deployed resources.

### The agent doesn't call the tool

Use tracing in Microsoft Foundry to confirm whether a tool call occurred. For guidance on validating tool invocation, see [Best practices for using tools in Microsoft Foundry Agent Service](../../concepts/tool-best-practice.md).

## Limitations

The APIs don't directly support file input or output, or the use of file stores. To get data in and out, you must use URLs, such as data URLs for small files and Azure Blob Service shared access signature (SAS) URLs for large files.

## Security

If you use SAS URLs to pass data in or out of the runtime:

- Use short-lived SAS tokens.
- Don't log SAS URLs or store them in source control.
- Scope permissions to the minimum required (for example, read-only or write-only).

## Clean up

To stop billing for provisioned resources, delete the resources created by the sample deployment. If you used a dedicated resource group for this article, delete the resource group.

## Related content

- [Connect to Model Context Protocol servers (preview)](model-context-protocol.md)
- [Best practices for using tools in Microsoft Foundry Agent Service](../../concepts/tool-best-practice.md)
- [Azure Container Apps Dynamic Sessions](/azure/container-apps/sessions)
- [Session pools with custom containers](/azure/container-apps/session-pool#custom-container-pool)
- [Azure Container Apps environment](/azure/container-apps/environment)
- [Install the Azure CLI](/cli/azure/install-azure-cli)
- [Code Interpreter tool for agents](code-interpreter.md)
