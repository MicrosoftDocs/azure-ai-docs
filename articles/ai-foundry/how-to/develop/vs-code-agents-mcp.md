---
title: Work with Foundry Agent Service and MCP Server Tools in Visual Studio Code
titleSuffix: Microsoft Foundry
description: Use this article to learn how to use MCP server tools with Foundry Agent Service directly in VS Code.
manager: mcleans
ms.service: azure-ai-foundry
content_well_notification: 
  - AI-contribution
ai-usage: ai-assisted
ms.topic: how-to
ms.date: 09/24/2025
ms.reviewer: erichen
ms.author: johalexander
author: ms-johnalex
monikerRange: foundry-classic || foundry
---

# Work with Foundry Agent Service and MCP server tools in Visual Studio Code (preview)

In this article, you learn how to add and use [Model Context Protocol (MCP)](/azure/ai-foundry/agents/how-to/tools/model-context-protocol) tools with Azure AI agents by using the [Microsoft Foundry for Visual Studio Code extension](https://marketplace.visualstudio.com/items?itemName=TeamsDevApp.vscode-ai-foundry).

After you [build an agent in Foundry Agent Service](./vs-code-agents.md) by using this Visual Studio Code (VS Code) extension, you can add MCP tools to your agent.

Using or building an MCP server allows your agent to:

- Access up-to-date information from your APIs and services.
- Retrieve relevant context to enhance the quality of responses from your AI models.

Agents combine AI models with tools to access and interact with your data.

Foundry developers can stay productive by developing, testing, and deploying MCP tool-calling agents in the familiar environment of VS Code.

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

## Create an Azure AI agent within the designer view

To create an Azure AI agent, follow the steps in [Create and edit Azure AI agents within the designer view](./vs-code-agents.md#create-and-edit-an-azure-ai-agent-within-the-designer-view).

## Add an existing MCP server tool to the AI agent

After you create your agent, you can add tools to it, including MCP tools. For more information about available tools, see [Tools for Azure AI agents](/azure/ai-foundry/agents/how-to/tools/overview).

You can bring multiple remote MCP servers by adding them as tools. For each tool, you need to provide a unique **Server Label** value within the same agent and a **Server URL** value that points to the remote MCP server.

> [!WARNING]
> The remote MCP servers that you use with the MCP tool in this article are not from Microsoft. Microsoft doesn't test or verify these servers. For details, see [Considerations for using non-Microsoft services and servers](/azure/ai-foundry/agents/how-to/tools/model-context-protocol?branch=pr-en-us-6966#considerations-for-using-non-microsoft-services-and-servers).

To add an existing MCP server tool to your AI agent, follow these steps:

1. In the designer, in the upper-right corner of the **TOOL** section, select the **Add tool** button. In the dropdown list, select the **MCP Server** tool.

1. Find the remote MCP server that you want to connect to, such as the GitHub MCP server. Create or update a Foundry agent with an MCP tool by using the following information:

    1. **Server URL**: The URL of the MCP server; for example, `https://gitmcp.io/Azure/azure-rest-api-specs`.

    1. **Server Label**: A unique identifier of this MCP server to the agent; for example, `fetch_rest_api_docs`.

    :::image type="content" source="../../media/how-to/get-started-projects-vs-code/agent-mcp-tool-dialog.png" alt-text="Screenshot of the dialog for creating an MCP tool." lightbox="../../media/how-to/get-started-projects-vs-code/agent-mcp-tool-dialog.png":::

1. In the **Allowed tools** dropdown list, choose which tools the MCP server can use.

    :::image type="content" source="../../media/how-to/get-started-projects-vs-code/agent-select-mcp-tool.png" alt-text="Screenshot of the list of allowed tools in the dialog for creating an MCP tool." lightbox="../../media/how-to/get-started-projects-vs-code/agent-select-mcp-tool.png":::

1. After you enter the required information, select the **Create tool** button.

### Create an Azure AI agent on Foundry

After you add an MCP tool, you can create an agent directly on Foundry by using the following steps:

1. In the designer, select the **Create Agent on Foundry** button.

    :::image type="content" source="../../media/how-to/get-started-projects-vs-code/agent-deploy.png" alt-text="Screenshot of the agent designer with the button for creating an agent on Foundry highlighted." lightbox="../../media/how-to/get-started-projects-vs-code/agent-deploy.png":::

1. In VS Code, refresh the **Azure Resources** view. The deployed agent appears in the **Agents** subsection.

    :::image type="content" source="../../media/how-to/get-started-projects-vs-code/agent-deployed.png" alt-text="Screenshot of a deployed agent in the Azure Resources view." lightbox="../../media/how-to/get-started-projects-vs-code/agent-deployed.png":::

## View the details of a deployed AI agent

Selecting the deployed agent opens the **AGENT PREFERENCES** pane in a view-only mode. You can:

- Select the **Edit Agent** button to view the agent designer and the .yaml definition of the agent for editing.
- Select the **Open Code File** button to create a sample code file that uses the agent.
- Select the **Open Playground** button to open the agent playground.

:::image type="content" source="../../media/how-to/get-started-projects-vs-code/deployed-agent-view.png" alt-text="Screenshot of the pane for agent preferences with the Edit Agent, Open Code File, and Open Playground buttons highlighted." lightbox="../../media/how-to/get-started-projects-vs-code/deployed-agent-view.png":::

### Edit and update the deployed AI agent

1. On the **AGENT PREFERENCES** pane, select the **Edit Agent** button. The agent designer opens with the agent's .yaml file.

1. Edit the agent's configuration, such as the model, tools, and instructions.

1. After you finish editing, select the **Update Agent on Foundry** button to save your changes.

:::image type="content" source="../../media/how-to/get-started-projects-vs-code/update-agent.png" alt-text="Screenshot of the pane for agent preferences with the Update Agent on Foundry button highlighted." lightbox="../../media/how-to/get-started-projects-vs-code/update-agent.png":::

### Interact with agents by using the MCP server tool in the agent playground

1. Right-click your deployed agent that has an **MCP Server** tool, and then select the **Open Playground** option. This action starts a thread with your agent so that you can send messages.

1. On the **Agent Playground** pane, enter a prompt such as **Give me an example for creating a container app** and send it.

1. Select the authentication method for the MCP server tool and proceed.

    :::image type="content" source="../../media/how-to/get-started-projects-vs-code/mcp-tool-authentication.png" alt-text="Screenshot of the MCP server tool's authentication prompt in the agent playground." lightbox="../../media/how-to/get-started-projects-vs-code/mcp-tool-authentication.png":::

1. Select the approval preference for the MCP server tool and proceed.

    :::image type="content" source="../../media/how-to/get-started-projects-vs-code/mcp-tool-approval-preference.png" alt-text="Screenshot of the MCP server tool's approval preference in the agent playground." lightbox="../../media/how-to/get-started-projects-vs-code/mcp-tool-approval-preference.png":::

1. If you chose **Ask every time** for your approval preference, you need to approve or reject the tool call.

    :::image type="content" source="../../media/how-to/get-started-projects-vs-code/mcp-approve-tool.png" alt-text="Screenshot of the MCP server tool's approval prompt in the agent playground." lightbox="../../media/how-to/get-started-projects-vs-code/mcp-approve-tool.png":::

1. The agent uses the model and the MCP server tools that you configured in the agent designer to retrieve the information. The source of the information appears in the section for agent annotations.

    :::image type="content" source="../../media/how-to/get-started-projects-vs-code/mcp-tool-response.png" alt-text="Screenshot of the agent playground with agent annotations highlighted in Visual Studio Code after use of the MCP server tool." lightbox="../../media/how-to/get-started-projects-vs-code/mcp-tool-response.png":::

## Clean up resources

The Azure resources that you created in this article are billed to your Azure subscription. If you don't expect to need these resources in the future, delete them to avoid incurring more charges.

### Delete your agents

[!INCLUDE [tip-left-pane](../../includes/tip-left-pane.md)]

1. In the [Foundry portal](https://ai.azure.com/?cid=learnDocs), on the left menu, select **Agents**.

1. Select the agent that you want to delete, and then select **Delete**.

   :::image type="content" source="../../media/how-to/get-started-projects-vs-code/delete-agent.png" alt-text="Screenshot of the Foundry portal with the Delete command for a selected agent." lightbox="../../media/how-to/get-started-projects-vs-code/delete-agent.png":::

### Delete your models

1. In VS Code, refresh the **Azure Resources** view. Expand the **Models** subsection to display the list of deployed models.

1. Right-click the deployed model that you want to delete, and then select **Delete**.

    :::image type="content" source="../../media/how-to/get-started-projects-vs-code/delete-model.png" alt-text="Screenshot of the shortcut menu with the Delete command for a selected model." lightbox="../../media/how-to/get-started-projects-vs-code/delete-model.png":::

### Delete your connected tools

1. Open the Azure portal.

1. Select the Azure resource group that contains the tool.

1. Select the **Delete** button.

## Related content

- Learn about the tools that you can use with Azure AI agents, such as [file search](/azure/ai-services/agents/how-to/tools/file-search?tabs=python&pivots=overview) or [code interpreter](/azure/ai-services/agents/how-to/tools/code-interpreter?tabs=python&pivots=overview).
