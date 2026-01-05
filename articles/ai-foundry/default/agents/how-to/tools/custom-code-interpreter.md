---
title: Use custom code interpreter with agents
titleSuffix: Microsoft Foundry
description: Learn how to configure and use the custom code interpreter tool with agents in Microsoft Foundry. Customize resources, Python packages, and Container Apps environments.
services: azure-ai-agent-service
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.date: 12/03/2025
author: alvinashcraft
ms.author: aashcraft
---

# Custom code interpreter tool for agents (preview)

[!INCLUDE [feature-preview](../../../../includes/feature-preview.md)]

With a custom code interpreter for your agent, you can customize the resources, available Python packages, and [Container Apps environment](/azure/container-apps/environment) that the agent uses to run the Python code it writes. The code interpreter container is exposed through a Model Context Protocol (MCP) server.

## Prerequisites

To use the preview feature, you need the following prerequisites:

- The [Azure CLI](/cli/azure/install-azure-cli).
- Optionally install `uv` as an alternative to `pip`. `uv` is a fast package and project manager for Python projects. You can install it by following the instructions at [Installing uv](https://docs.astral.sh/uv/getting-started/installation/) in the official documentation.
- An Azure subscription and resource group with the following permissions:
  - [Azure AI Owner](/azure/role-based-access-control/built-in-roles/ai-machine-learning#azure-ai-owner)
  - [Container Apps ManagedEnvironment Contributor](/azure/role-based-access-control/built-in-roles/containers#container-apps-managedenvironments-contributor)
- The latest prerelease package. See the [quickstart](../../../../quickstarts/get-started-code.md?view=foundry&preserve-view=true#install-and-authenticate) for details.

## Custom code interpreter example

The following console commands and code samples show how to create an agent that uses a custom code interpreter MCP server.

### Enable MCP server for dynamic sessions

To enable the preview feature, run the following commands.

```console
az feature register --namespace Microsoft.App --name SessionPoolsSupportMCP
az provider register -n Microsoft.App
```

### Get the sample code

Clone the [sample code in the GitHub repo](https://github.com/azure-ai-foundry/foundry-samples) and navigate to the folder `samples/python/hosted-agents/code-interpreter-custom` in your terminal.

### Provision the infrastructure

To provision the infrastructure, run the following command with the Azure CLI (`az`):

```console
az deployment group create \
    --name custom-code-interpreter \
    --subscription <your_subscription> \
    --resource-group <your_resource_group> \
    --template-file ./infra.bicep
```

> [!NOTE]
> This process can take a while! Allocating the dynamic session pool can take up to 1 hour, depending on the number of standby instances you request.

### Use the custom code interpreter in an agent

Copy the `.env.sample` file from the repository to `.env` and fill in the values with the output from the preceding deployment. You can find this output in the Azure portal under the resource group.

Install the Python dependencies (`uv sync` or `pip install`). Finally, run `./main.py`.

## Limitations

The APIs don't directly support file input/output or the use of file stores. To get data in and out, you must use URLs, such as data URLs for small files and Azure Blob Service SAS URLs for large files.

## Related content

- [Azure Container Apps Dynamic Sessions](/azure/container-apps/sessions)
- [Session Pools with Custom Containers](/azure/container-apps/session-pool#custom-container-pool)
- [Code Interpreter tool for agents](code-interpreter.md)
