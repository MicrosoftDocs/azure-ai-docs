---
title: Work with Foundry Classic agents and MCP server tools in Visual Studio Code
titleSuffix: Microsoft Foundry
description: Add Model Context Protocol (MCP) server tools to your Foundry Classic agents by using the Microsoft Foundry for Visual Studio Code extension.
manager: mcleans
ms.service: azure-ai-foundry
content_well_notification:
  - AI-contribution
ai-usage: ai-assisted
ms.topic: how-to
ms.date: 02/19/2026
ms.reviewer: erichen
ms.author: johalexander
author: ms-johnalex
monikerRange: foundry-classic 
---

# Work with Foundry Classic agents and MCP server tools in Visual Studio Code (preview)

In this article, you add and use [Model Context Protocol (MCP)](../../agents/how-to/tools-classic/model-context-protocol.md) server tools with agents in Foundry Agent Service. You use the [Microsoft Foundry for Visual Studio Code extension](https://marketplace.visualstudio.com/items?itemName=TeamsDevApp.vscode-ai-foundry) to configure and test MCP tool-calling agents.

> [!NOTE]
> This article refers to the classic version of the agents API.

After you [build an agent in Agent Service](./vs-code-agents.md) by using the Visual Studio Code (VS Code) extension, you can add MCP tools to your agent. Adding an MCP server allows your agent to:

- Access up-to-date information from your APIs and services.
- Retrieve relevant context to enhance the quality of responses from your AI models.

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

## Prerequisites

- An Azure subscription. If you don't have one, [create one for free](https://azure.microsoft.com/free/).
- A Foundry project with a deployed model.
- [Visual Studio Code](https://code.visualstudio.com/) with the [Microsoft Foundry for Visual Studio Code extension](https://marketplace.visualstudio.com/items?itemName=TeamsDevApp.vscode-ai-foundry) installed.
- An existing agent created through the VS Code extension. To create one, follow the steps in [Work with Agent Service in Visual Studio Code](./vs-code-agents.md).
- A remote MCP server URL to connect to your agent.

## Create an agent in the designer

To create an agent, follow the steps in [Create an agent in the designer](./vs-code-agents.md#create-an-agent-in-the-designer).

## Add an MCP server tool to the agent

After you create your agent, you can add tools to it, including MCP tools. For more information about available tools, see [Tools for agents](../../agents/how-to/tools-classic/overview.md).

You can bring multiple remote MCP servers by adding them as tools. For each tool, you need to provide a unique **Server Label** value within the same agent and a **Server URL** value that points to the remote MCP server.

> [!WARNING]
> The remote MCP servers that you use with the MCP tool in this article are not from Microsoft. Microsoft doesn't test or verify these servers. For details, see [Considerations for using non-Microsoft services and servers](../../agents/how-to/tools-classic/model-context-protocol.md#considerations-for-using-non-microsoft-services-and-servers).

To add an MCP server tool to your agent, follow these steps:

1. In the designer, in the upper-right corner of the **TOOL** section, select the **Add tool** button. In the dropdown list, select the **MCP Server** tool.

1. Find the remote MCP server that you want to connect to, such as the GitHub MCP server. Create or update a Foundry agent with an MCP tool by using the following information:

    1. **Server URL**: The URL of the MCP server; for example, `https://gitmcp.io/Azure/azure-rest-api-specs`.

    1. **Server Label**: A unique identifier of this MCP server to the agent; for example, `fetch_rest_api_docs`.


1. In the **Allowed tools** dropdown list, choose which tools the MCP server can use.

1. After you enter the required information, select the **Create tool** button. The MCP tool appears in the **TOOL** section of the agent designer.

### Deploy the agent to Foundry

After you add an MCP tool, deploy the agent to Foundry so that it's available for testing and use.

1. In the designer, select the **Create Agent on Microsoft Foundry** button.

1. In VS Code, refresh the **Resources** view. The deployed agent appears in the **Classic Agents** subsection.

## View deployed agent details

After you deploy an agent, you can inspect its configuration and interact with it. Select the deployed agent in the **Resources** view to open the **AGENT PREFERENCES** pane in view-only mode. You can:

- Select the **Edit Agent** button to view the agent designer and the .yaml definition of the agent for editing.
- Select the **View Code** button to create a sample code file that uses the agent.
- Select the **Open Playground** button to open the agent playground.

### Edit a deployed agent

To modify your agent's configuration after deployment, follow these steps:

1. On the **AGENT PREFERENCES** pane, select the **Edit Agent** button. The agent designer opens with the agent's .yaml file.

1. Edit the agent's configuration, such as the model, tools, and instructions.

1. After you finish editing, select the **Update Agent on Microsoft Foundry** button to save your changes. The updated configuration deploys to Foundry.

### Test the agent with MCP tools in the playground

Use the agent playground to verify that your MCP server tools work correctly with the deployed agent.

1. Right-click your deployed agent that has an **MCP Server** tool, and then select the **Open Playground** option. This action starts a thread with your agent so that you can send messages.

1. On the **Remote Agent Playground** pane, enter a prompt such as **Give me an example for creating a container app** and send it.

1. Select the authentication method for the MCP server tool and proceed. Authentication methods vary depending on the MCP server. Common options include API key, OAuth, or no authentication for public servers.

1. Select the approval preference for the MCP server tool and proceed. You can choose **Ask every time** to review each tool call, or **Always allow** to let the agent invoke MCP tools automatically.

1. If you chose **Ask every time** for your approval preference, you need to approve or reject each tool call before the agent proceeds.

1. The agent uses the model and the MCP server tools that you configured to retrieve the information. After the agent finishes processing, the response appears in the playground. The source of the information appears in the section for agent annotations.

## Troubleshoot MCP server connections

If you encounter issues when you use MCP server tools with your agent, try the following resolutions.

| Issue | Resolution |
| ----- | ---------- |
| MCP server URL is unreachable | Verify that the URL is correct and that the server is running. Check your network connection and any firewall rules that might block outbound requests from VS Code. |
| Authentication failures | Confirm that you selected the correct authentication method for the MCP server. If the server requires an API key or OAuth token, verify that the credentials are valid and not expired. |
| Tools don't appear in the allowed tools list | Refresh the tool list by closing and reopening the MCP tool dialog. Verify that the MCP server correctly exposes its tools through the standard MCP protocol. |
| Agent returns errors when invoking an MCP tool | Check the agent annotations in the playground for error details. The MCP server might be returning an error response. Verify the server is healthy and that the tool call parameters are correct. |

## Clean up resources

The Azure resources that you created in this article are billed to your Azure subscription. If you don't expect to need these resources in the future, delete them to avoid incurring more charges.

### Delete your agents

To remove agents that you no longer need:

1. In VS Code, refresh the **Resources** view. Expand the **Classic Agents** subsection to display the list of deployed agents.

1. Right-click the deployed agent that you want to delete, and then select **Delete**.

### Delete your models

To remove deployed models that you no longer need:

1. In VS Code, refresh the **Resources** view. Expand the **Models** subsection to display the list of deployed models.

1. Right-click the deployed model that you want to delete, and then select **Delete**.

### Delete your connected tools

To remove connected tool resources that you no longer need, delete them individually in the [Azure portal](https://portal.azure.com):

1. Open the [Azure portal](https://portal.azure.com).

1. Go to the resource group that contains your Foundry project.

1. Find the specific tool resource that you want to delete, and select it.

1. Select the **Delete** button and confirm the deletion.

> [!WARNING]
> Don't delete the entire resource group unless you want to remove all resources within it. Deleting a resource group removes all resources it contains, including your Foundry project and deployed models.

## Related content

- [Model Context Protocol (MCP) tool](../../agents/how-to/tools-classic/model-context-protocol.md)
- [Tools for agents](../../agents/how-to/tools-classic/overview.md)
- [Work with Agent Service in Visual Studio Code](./vs-code-agents.md)
- [Get started with Foundry projects in VS Code](./get-started-projects-vs-code.md)
- [File search tool](../../agents/how-to/tools-classic/file-search.md)
- [Code interpreter tool](../../agents/how-to/tools-classic/code-interpreter.md)
