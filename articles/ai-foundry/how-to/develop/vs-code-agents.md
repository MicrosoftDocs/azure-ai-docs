---
title: Create and manage Foundry Classic agents in Visual Studio Code
titleSuffix: Microsoft Foundry
description: Create, configure, test, and deploy Foundry Classic agents directly in Visual Studio Code by using the Foundry Agent Service extension and designer.
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
#CustomerIntent: As a developer, I want to create and manage Foundry Classic agents in Visual Studio Code so that I can build, test, and deploy agents without leaving my IDE.
---

# Create and manage Foundry Classic agents in Visual Studio Code (preview)

[!INCLUDE [version-banner](../../includes/version-banner.md)]

[Foundry Agent Service](../../agents/overview.md?view=foundry-classic&preserve-view=true) lets you build, configure, and deploy agents without leaving Visual Studio Code (VS Code). In this article, you create an agent by using the designer, add tools, test the agent in the playground, generate sample code, and clean up resources when you're done.

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

## Prerequisites

- An Azure subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account).
- Access to [Foundry Agent Service](../../agents/overview.md?view=foundry-classic&preserve-view=true).
- [Visual Studio Code](https://code.visualstudio.com/) installed.
- The [Microsoft Foundry for VS Code extension](./get-started-projects-vs-code.md) installed and signed in.
- A [deployed model](./get-started-projects-vs-code.md#deploy-a-model-from-the-model-catalog) in your project.

## Create an agent in the designer

The designer provides a visual interface for configuring your agent's name, model, instructions, and tools.

1. [Sign in to your Azure resources](./get-started-projects-vs-code.md#sign-in-to-your-resources).

1. [Set your default project](./get-started-projects-vs-code.md#create-a-project).

1. In the **Foundry Extension** view, find the **Classic** subsection in the **Resources** section.

1. Select the plus (**+**) icon next to the **Classic Agents** subsection to create a new agent.

### Configure the agent in the designer

After you choose a save location, the agent .yaml file and the designer view open. Configure the following settings:

1. In the prompt, enter a name for your agent.

1. In the dropdown list, select the name of your model deployment. The deployment name is what you chose when you deployed an existing model.

1. The extension generates the **Id** value. Configure the following fields:

   - Add a description for your agent.
   - Set system instructions.
   - Configure tools for agent use.


1. To save the .yaml file, select **File** > **Save** on the VS Code menu bar.

### Review the agent YAML definition

The .yaml file opens alongside the designer and contains the configuration details for your agent. The format is similar to the following example:

```yaml
# yaml-language-server: $schema=https://aka.ms/ai-foundry-vsc/agent/1.0.0
version: 1.0.0
name: my-agent
description: Description of the agent
id: ''
metadata:
  authors:
    - author1
    - author2
  tags:
    - tag1
    - tag2
model:
  id: 'gpt-4o-1'
  options:
    temperature: 1
    top_p: 1
instructions: Instructions for the agent
tools: []
```

## Add tools to the agent

Agent Service provides the following tools to extend your agent's capabilities and connect to your data sources:

- [Grounding with Bing search](../../agents/how-to/tools-classic/bing-grounding.md)
- [File search](../../agents/how-to/tools-classic/file-search.md)
- [Code interpreter](../../agents/how-to/tools-classic/code-interpreter.md)
- [OpenAPI specified tools](../../agents/how-to/tools-classic/openapi-spec.md)
- [Model Context Protocol (MCP)](../../agents/how-to/tools-classic/model-context-protocol.md)

For more information about using MCP tools, see [Work with Agent Service and MCP server tools in Visual Studio Code (preview)](./vs-code-agents-mcp.md).

### Add a tool to the agent

1. In the designer, in the upper-right corner of the **TOOL** section, select **Add tool**. In the dropdown list, select the tool that you want to add.

    :::image type="content" source="../../media/how-to/get-started-projects-vs-code/agent-tool-plus.png" alt-text="Screenshot showing the Add tool dropdown in the agent designer with the list of available tool types." lightbox="../../media/how-to/get-started-projects-vs-code/agent-tool-plus.png":::

1. The designer displays the appropriate pane to configure the tool, as shown in the following images:

    - Grounding with Bing search:

      :::image type="content" source="../../media/how-to/get-started-projects-vs-code/agent-bing-tool-dialog.png" alt-text="Screenshot of the pane for the Grounding with Bing search tool." lightbox="../../media/how-to/get-started-projects-vs-code/agent-bing-tool-dialog.png":::

    - File search:

      :::image type="content" source="../../media/how-to/get-started-projects-vs-code/agent-file-search-tool-dialog.png" alt-text="Screenshot showing the File search tool configuration pane with file upload options." lightbox="../../media/how-to/get-started-projects-vs-code/agent-file-search-tool-dialog.png":::

    - Code interpreter:

      :::image type="content" source="../../media/how-to/get-started-projects-vs-code/agent-ci-tool-dialog.png" alt-text="Screenshot of the pane for the code interpreter tool." lightbox="../../media/how-to/get-started-projects-vs-code/agent-ci-tool-dialog.png":::

    - OpenAPI 3.0 specified tools:

      :::image type="content" source="../../media/how-to/get-started-projects-vs-code/agent-openapi-tool-dialog.png" alt-text="Screenshot of the pane for the OpenAPI 3.0 specified tools." lightbox="../../media/how-to/get-started-projects-vs-code/agent-openapi-tool-dialog.png":::

1. After you enter the required information, select **Create and connect**, **Upload and save**, or **Create Tool**. The button label varies by tool type.

   After the tool is created, it appears in the **TOOL** section of the designer.

When you add a tool, you can also add any new assets that it needs. For example, if you add a file search tool, you can use an existing vector store asset or create a new one to host your uploaded files.

## Deploy the agent to Foundry

After you finish configuring your agent, deploy it to Foundry so it runs in the cloud.

1. In the designer, select the **Create Agent on Microsoft Foundry** button.

1. In VS Code, refresh the **Resources** view. The deployed agent appears in the **Classic Agents** subsection.

## View deployed agent details

Select a deployed agent to open the **AGENT PREFERENCES** pane in view-only mode. From this pane, you can:

- Select **Edit Agent** to open the agent designer and .yaml definition for editing.
- Select **View Code** to generate a sample code file that uses the agent.
- Select **Open Playground** to open the remote agent playground.

## Update a deployed agent

You can modify a deployed agent's configuration and sync the changes back to Foundry.

1. On the **AGENT PREFERENCES** pane, select **Edit Agent**. The agent designer opens with the agent's .yaml file.

1. Edit the agent's configuration, such as the model, tools, and instructions.

1. Select the **Update Agent on Microsoft Foundry** button to save your changes. The updated configuration takes effect immediately.

## Generate a sample code file

The extension generates boilerplate code for interacting with your deployed agent programmatically.

1. Right-click your deployed agent, and then select **View Code**. Or, on the **AGENT PREFERENCES** pane, select the **View Code** button.

1. In the **Choose your preferred SDK** dropdown list, select your SDK.

1. In the **Choose a language** dropdown list, select your language.

1. In the **Choose an auth method** dropdown list, select your authentication method.

The extension generates a code file in your selected language and opens it in the editor.

### Review the sample code file

The generated code file demonstrates a basic call to interact with the agent through the Foundry Projects API. The following screenshot shows a Python example:

:::image type="content" source="../../media/how-to/get-started-projects-vs-code/sample-agent-code-file.png" alt-text="Screenshot showing a generated Python code file with imports, client initialization, and agent interaction calls." lightbox="../../media/how-to/get-started-projects-vs-code/sample-agent-code-file.png":::

## Test the agent in the playground

Use the playground to send messages to your deployed agent and verify its behavior.

1. Right-click your deployed agent, and then select **Open Playground**.

   Alternatively, select the **Remote Agent Playground** link in the **Tools** subsection, select your agent type, and then select your agent from the dropdown lists.

   The **Remote Agent Playground** pane opens and starts a thread with your agent.

1. Enter your prompt and view the outputs.

   This example uses **Bing Grounding** to illustrate a web search for information. The agent uses the model and tools that you configured in the agent designer. The source of the information appears in the section for agent annotations.

    :::image type="content" source="../../media/how-to/get-started-projects-vs-code/agent-playground-run.png" alt-text="Screenshot showing the Agent Playground pane displaying a Bing Grounding response with agent annotations highlighting the source." lightbox="../../media/how-to/get-started-projects-vs-code/agent-playground-run.png":::

## View agent threads

The **Threads** subsection displays the conversation threads created during runs with your agent. In the **Classic** section under the **Resources** view, expand the **Threads** subsection to view the list.

:::image type="content" source="../../media/how-to/get-started-projects-vs-code/thread-list.png" alt-text="Screenshot showing the Threads subsection in the Classic section view with a list of conversation threads." lightbox="../../media/how-to/get-started-projects-vs-code/thread-list.png":::

> [!NOTE]
> A *thread* is a conversation session between an agent and a user. Threads store messages and automatically handle truncation to fit content into a model's context. A *message* is a single interaction that can include text, images, and other files. A *run* is a single execution of an agent that can span multiple threads and messages.

### View thread details

To view the **THREAD DETAILS** pane, select a thread from the list.

### View run details

To view run information, select the **View run info** button on the **THREAD DETAILS** pane. A .json file opens with the details of the run, including the agent configuration, messages, and tool calls.

## Clean up resources

If you don't need the resources you created, delete them to avoid ongoing charges to your Azure subscription.

### Delete your agents

[!INCLUDE [tip-left-pane](../../includes/tip-left-pane.md)]

1. In VS Code, refresh the **Azure Resources** view.
1. Expand the **Agents** subsection to display the list of deployed agents.
1. Right-click the agent that you want to delete, and then select **Delete**.

### Delete your models

1. In VS Code, refresh the **Resources** view. Expand the **Models** subsection to display the list of deployed models.

1. Right-click the model that you want to delete, and then select **Delete**.

### Delete your connected tools

1. Open the [Azure portal](https://portal.azure.com).

1. Go to the resource group that contains the tool resource.

1. Select the resource, and then select **Delete**.

## Related content

 - [Work with Agent Service and MCP server tools in Visual Studio Code (preview)](./vs-code-agents-mcp.md) to add MCP tools to your agents.
- [Agent tools overview](../../agents/how-to/tools-classic/overview.md) for details on file search, code interpreter, and other available tools.
- [Foundry Agent Service overview](../../agents/overview.md?view=foundry-classic&preserve-view=true) for a deeper look at agent concepts and capabilities.
