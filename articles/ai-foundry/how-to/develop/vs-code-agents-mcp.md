---
title: Work with Azure AI Foundry Agent Service and MCP Server tools using the Azure AI Foundry for Visual Studio Code extension
titleSuffix: Azure AI Foundry
description: Use this article to learn how to use MCP Server tools with Azure AI Foundry Agent Service directly in VS Code.
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
---

# Work with Azure AI Foundry Agent Service and MCP Server tools in Visual Studio Code (Preview)

In this article, you learn how to add and use the [Model Context Protocol (MCP)](/azure/ai-foundry/agents/how-to/tools/model-context-protocol) tool with Azure AI Agents using the [Azure AI Foundry for Visual Studio Code extension](https://marketplace.visualstudio.com/items?itemName=ms-ai-foundry.vscode-ai-foundry).

After you [build an agent with the Azure AI Foundry Agent Service](./vs-code-agents.md) using this Visual Studio Code extension, you can add [Model Context Protocol (MCP)](/azure/ai-foundry/agents/how-to/tools/model-context-protocol) tools to your agent. 

 Using or building an MCP server allows your agent to:

- Access up-to-date information from your APIs and services.
- Retrieve relevant context to enhance the quality of responses from your AI models.

Agents combine AI models with tools to access and interact with your data.

Azure AI Foundry developers can stay productive by developing, testing, and deploying MCP tool calling agents in the familiar and powerful environment of VS Code.

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

## Create an Azure AI Agent for MCP Tool calling within the designer view 

Follow these steps to create an Azure AI Agent to add MCP tools:

1. First, finish the [Create and edit Azure AI Agents within the designer view](./get-started-projects-vs-code.md##create-and-edit-azure-ai-agents-within-the-designer-view) section to sign in to and create your Azure resources and agent.

After creating your agent, you can add tools to it, including MCP tools.

> [!NOTE]
> For more information about the other tools you can use with Azure AI Agents, see [Tools for Azure AI Agents](/azure/ai-foundry/agents/how-to/tools/overview).

## Add an existing MCP Server tool to the AI Agent

You can bring multiple remote MCP servers by adding them as tools. For each tool, you need to provide a unique `Server Label` value within the same agent and a `Server URL` value that points to the remote MCP server.

> [!WARNING]
> The remote MCP servers you use with the MCP tool in this article are made by third parties, not Microsoft. Microsoft doesn't test or verify these servers. For details, see [Considerations for using non-Microsoft services and servers](/azure/ai-foundry/agents/how-to/tools/model-context-protocol?branch=pr-en-us-6966#considerations-for-using-non-microsoft-services-and-servers).

To add an existing MCP Server tool to your AI Agent, follow these steps:

  1. Select the **Add tool** button in the top-right corner of the **TOOL** section in the designer to show the dropdown. Choose the **MCP Server** tool.
    
1. Find the remote MCP server that you want to connect to, such as the GitHub MCP server. Create or update an Azure AI Foundry agent with a mcp tool with the following information:

    1. `Server URL`: The URL of the MCP server; for example, [https://gitmcp.io/Azure/azure-rest-api-specs](https://gitmcp.io/Azure/azure-rest-api-specs).

    1. `Server Label`: A unique identifier of this MCP server to the agent; for example, `fetch_rest_api_docs`.

    :::image type="content" source="../../media/how-to/get-started-projects-vs-code/agent-mcp-tool-dialog.png" alt-text="Screenshot of the MCP Server tool dialog box." lightbox="../../media/how-to/get-started-projects-vs-code/agent-mcp-tool-dialog.png":::

 1. Next, select the **Allowed tools** dropdown to choose which tools the MCP server can use:

    :::image type="content" source="../../media/how-to/get-started-projects-vs-code/agent-select-mcp-tool.png" alt-text="Screenshot of the MCP Server tool dialog box with the 'Allowed tools' dropdown highlighted." lightbox="../../media/how-to/get-started-projects-vs-code/agent-select-mcp-tool.png":::

    > [!WARNING]
    > When you add an allowed tool, you can also pass a set of headers that the MCP server requires. Currently, there's an issue when running an agent with MCP server that requires authentication in agent playground. For more information about this issue: https://github.com/microsoft/ai-foundry-for-vscode/issues/150

1. After entering the required information, select the **Create tool** button in the bottom-left corner.

### Create Azure AI Agents on the Azure AI Foundry Studio

After you add an MCP tool, update your agent directly on Azure AI Foundry with the following steps:

1.  Select the **Create on Azure AI Foundry** button in the bottom-left of the designer.

    :::image type="content" source="../../media/how-to/get-started-projects-vs-code/agent-deploy.png" alt-text="Screenshot of the Agent designer with the 'Deploy to Azure AI Foundry' button highlighted." lightbox="../../media/how-to/get-started-projects-vs-code/agent-deploy.png":::

1. In the VS Code navbar, refresh the **Azure Resources** view. The deployed agent is displayed under the **Agents** subsection.

    :::image type="content" source="../../media/how-to/get-started-projects-vs-code/agent-deployed.png" alt-text="Screenshot of the 'Azure Resources' view. The deployed agent is highlighted under the 'Agents' subsection." lightbox="../../media/how-to/get-started-projects-vs-code/agent-deployed.png":::

#### View the deployed AI Agent details

Selecting the deployed agent opens the **Agent Preferences** page in a view only mode.  

- Select the **Edit Agent** button to view the Agent designer and yaml definition of the agent for editing. 
- Select the **Open Code File** button to create a sample code file that uses the agent. 
- Select the **Open Playground** button to open the **Agent Playground**.

    :::image type="content" source="../../media/how-to/get-started-projects-vs-code/deployed-agent-view.png" alt-text="Screenshot of the Agent Preferences page with the 'Edit Agent', 'Open Code File', and 'Open Playground' buttons highlighted." lightbox="../../media/how-to/get-started-projects-vs-code/deployed-agent-view.png":::

### Edit and update the deployed AI Agent

To edit the deployed agent, select the **Edit Agent** button in the **Agent Preferences** page. The agent designer opens with the agent .yaml file.
Edit the agent's configuration, such as the model, tools, and instructions. After you finish editing, select the **Update on Azure AI Foundry** button in the lower left corner to save your changes.

:::image type="content" source="../../media/how-to/get-started-projects-vs-code/update-agent.png" alt-text="Screenshot of the Agent Preferences page with the 'Update on Azure AI Foundry' button highlighted." lightbox="../../media/how-to/get-started-projects-vs-code/update-agent.png":::

### Interact with Agents using the MCP Server tool in agents playground

1. Right select on your deployed agent that has an **MCP Server** tool and select the **Open Playground** option, as you did in the previous steps. This action starts a thread with your agent and lets you send messages.
1. After the **Playground** page is displayed, type a prompt such as "Give me an example for creating a container app" and send it. 
1. Select the authentication mode for the MCP Server tool. Choose the appropriate authentication method and proceed, as in the following image.

    :::image type="content" source="../../media/how-to/get-started-projects-vs-code/mcp-tool-authentication.png" alt-text="Screenshot of the MCP Server tool authentication prompt in the Agents Playground." lightbox="../../media/how-to/get-started-projects-vs-code/mcp-tool-authentication.png":::
1. Next, select the approval preference for the MCP Server tool. Choose the appropriate approval preference and proceed, as in the following image.

    :::image type="content" source="../../media/how-to/get-started-projects-vs-code/mcp-tool-approval-preference.png" alt-text="Screenshot of the MCP Server tool approval preference in the Agents Playground." lightbox="../../media/how-to/get-started-projects-vs-code/mcp-tool-approval-preference.png":::

1. If you chose `Ask every time` for your approval preference, you need to approve or reject the tool call, as in the following image.

    :::image type="content" source="../../media/how-to/get-started-projects-vs-code/mcp-approve-tool.png" alt-text="Screenshot of the MCP Server tool approval prompt in the Agents Playground." lightbox="../../media/how-to/get-started-projects-vs-code/mcp-approve-tool.png":::

1. The agent uses the model and the MCP Server tools you configured in the agent designer to retrieve the information. The source of the information is displayed in the **Agent Annotations** section, highlighted in the following image.
    :::image type="content" source="../../media/how-to/get-started-projects-vs-code/mcp-tool-response.png" alt-text="Screenshot of the Agents Playground page with agent annotations highlighted in VS Code after using the MCP Server tool." lightbox="../../media/how-to/get-started-projects-vs-code/mcp-tool-response.png":::

## Cleanup resources

The Azure resources that you created in this article are billed to your Azure subscription. If you don't expect to need these resources in the future, delete them to avoid incurring more charges.

### Delete your agents

[!INCLUDE [tip-left-pane](../../includes/tip-left-pane.md)]

Delete the deployed agent in the [online AI Foundry portal](https://ai.azure.com/?cid=learnDocs). Select **Agents** from the navigation menu on the left, select your agent, then select the **Delete** button.

:::image type="content" source="../../media/how-to/get-started-projects-vs-code/delete-agent.png" alt-text="Screenshot of the AI Foundry portal with Agents from the navigation menu on the left and the Delete button highlighted." lightbox="../../media/how-to/get-started-projects-vs-code/delete-agent.png":::

### Delete your models

1. In the VS Code navbar, refresh the **Azure Resources** view. Expand the **Models** subsection to display the list of deployed models.

1. Right-click on your deployed model to delete and select the **Delete** option.

    :::image type="content" source="../../media/how-to/get-started-projects-vs-code/delete-model.png" alt-text="Screenshot of the model context menu with the Delete option highlighted." lightbox="../../media/how-to/get-started-projects-vs-code/delete-model.png":::

### Delete your tools

Delete the connected tool with the following steps:

1. Open the Azure portal
1. Select the Azure Resource Group containing the tool.
1. Select the **Delete** button.  

##    Next steps

- Learn about the tools you can use with Azure AI Agents, such as [file search](/azure/ai-services/agents/how-to/tools/file-search?tabs=python&pivots=overview), or [code interpreter](/azure/ai-services/agents/how-to/tools/code-interpreter?tabs=python&pivots=overview).
