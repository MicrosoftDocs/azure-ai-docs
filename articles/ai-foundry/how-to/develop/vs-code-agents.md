---
title: Work with Foundry Agent Service in Visual Studio Code
titleSuffix: Microsoft Foundry
description: Use this article to learn how to use Foundry Agent Service directly in Visual Studio Code.
manager: mcleans
ms.service: azure-ai-foundry
content_well_notification: 
  - AI-contribution
ai-usage: ai-assisted
ms.topic: how-to
ms.date: 10/22/2025
ms.reviewer: erichen
ms.author: johalexander
author: ms-johnalex
monikerRange: foundry-classic || foundry
---

# Work with Foundry Agent Service in Visual Studio Code (preview)

After you [get started with the Microsoft Foundry for Visual Studio Code extension](./get-started-projects-vs-code.md), use [Foundry Agent Service](/azure/ai-services/agents/overview) to build agents. Agents are microservices that:

- Answer questions by using their training data or search other sources with retrieval-augmented generation (RAG).
- Perform specific actions.
- Automate complete workflows.

Agents combine AI models with tools to access and interact with your data.

Foundry developers can stay productive by developing, testing, and deploying agents in the familiar environment of Visual Studio Code (VS Code).

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

## Create and edit an Azure AI agent within the designer view

Follow these steps to create an Azure AI agent:

1. [Sign in to your Azure resources](./get-started-projects-vs-code.md#sign-in-to-your-resources).

1. [Set your default project](./get-started-projects-vs-code.md#create-a-project).

1. [Deploy a model](./get-started-projects-vs-code.md#deploy-a-model-from-the-model-catalog) to use with your agent.

1. In the **Foundry Extension** view, find the **Resources** section.

1. Select the plus (**+**) icon next to the **Agents** subsection to create a new AI agent.

    :::image type="content" source="../../media/how-to/get-started-projects-vs-code/select-agent-plus.png" alt-text="Screenshot of the plus sign next to the Agents subsection.":::

### Interact with your agent in the designer

After you choose your save location, both the agent .yaml file and the designer view open so that you can edit your AI agent. Perform the following tasks in the agent designer:

1. In the prompt, enter a name for your agent.

1. In the dropdown list, select the name of your model deployment. The deployment name is what you chose when you deployed an existing model.

1. The extension generates the **Id** value. Configure the following fields:

   - Add a description for your agent.
   - Set system instructions.
   - Configure tools for agent use.

   :::image type="content" source="../../media/how-to/get-started-projects-vs-code/agent-designer.png" alt-text="Screenshot of the agent designer for editing and interacting with an AI agent." lightbox="../../media/how-to/get-started-projects-vs-code/agent-designer.png":::

1. To save the .yaml file, select **File** > **Save** on the VS Code menu bar.

### Explore the Azure AI agent's .yaml definition

Your AI agent's .yaml file was opened at the same time that the designer was. This file contains the details and setup information for your agent. It's similar to the following .yaml file example:

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

## Add tools to the Azure AI agent

Agent Service has the following set of tools that you can use to interact with your data sources. These tools are available in the Foundry for Visual Studio Code extension.

- [Grounding with Bing search](/azure/ai-foundry/agents/how-to/tools/bing-grounding)
- [File search](/azure/ai-services/agents/how-to/tools/file-search?tabs=python&pivots=overview)
- [Code interpreter](/azure/ai-foundry/agents/how-to/tools/code-interpreter)
- [OpenAPI specified tools](/azure/ai-foundry/agents/how-to/tools/openapi-spec)
- [Model Context Protocol (MCP)](/azure/ai-foundry/agents/how-to/tools/model-context-protocol)

For more information about using MCP tools, see [Work with Agent Service and MCP server tools in Visual Studio Code (preview)](./vs-code-agents-mcp.md).

### Add a tool to the AI agent

1. In the designer, in the upper-right corner of the **TOOL** section, select **Add tool**. In the dropdown list, select the tool that you want to add.

    :::image type="content" source="../../media/how-to/get-started-projects-vs-code/agent-tool-plus.png" alt-text="Screenshot of selections in the agent designer for adding a tool." lightbox="../../media/how-to/get-started-projects-vs-code/agent-tool-plus.png":::

1. The designer displays the appropriate pane to configure the tool, as shown in the following images:

    - Grounding with Bing search:

      :::image type="content" source="../../media/how-to/get-started-projects-vs-code/agent-bing-tool-dialog.png" alt-text="Screenshot of the pane for the Grounding with Bing search tool." lightbox="../../media/how-to/get-started-projects-vs-code/agent-bing-tool-dialog.png":::

    - File search:

      :::image type="content" source="../../media/how-to/get-started-projects-vs-code/agent-file-search-tool-dialog.png" alt-text="Screenshot of the pane for the file upload tool." lightbox="../../media/how-to/get-started-projects-vs-code/agent-file-search-tool-dialog.png":::

    - Code interpreter:

      :::image type="content" source="../../media/how-to/get-started-projects-vs-code/agent-ci-tool-dialog.png" alt-text="Screenshot of the pane for the code interpreter tool." lightbox="../../media/how-to/get-started-projects-vs-code/agent-ci-tool-dialog.png":::

    - OpenAPI 3.0 specified tools:

      :::image type="content" source="../../media/how-to/get-started-projects-vs-code/agent-openapi-tool-dialog.png" alt-text="Screenshot of the pane for the OpenAPI 3.0 specified tools." lightbox="../../media/how-to/get-started-projects-vs-code/agent-openapi-tool-dialog.png":::

1. After you enter the required information, select **Create and connect**, **Upload and save**, or **Create Tool**. The button varies according to the pane.

When you add a tool, you can also add any new assets that it needs. For example, if you add a file search tool, you can use an existing vector store asset or make a new asset for your vector store to host your uploaded files.

## Create an Azure AI agent on Foundry

Create your agent directly on Foundry by using the following steps:

1. In the designer, select the **Create Agent on Foundry** button.

    :::image type="content" source="../../media/how-to/get-started-projects-vs-code/agent-deploy.png" alt-text="Screenshot of the agent designer with the button for creating an agent on Foundry highlighted." lightbox="../../media/how-to/get-started-projects-vs-code/agent-deploy.png":::

1. In VS Code, refresh the **Azure Resources** view. The deployed agent appears in the **Agents** subsection.

    :::image type="content" source="../../media/how-to/get-started-projects-vs-code/agent-deployed.png" alt-text="Screenshot of a deployed agent in the Azure Resources view." lightbox="../../media/how-to/get-started-projects-vs-code/agent-deployed.png":::

## View the details of the deployed AI agent

Selecting the deployed agent opens the **AGENT PREFERENCES** pane in a view-only mode. You can:

- Select the **Edit Agent** button to view the agent designer and the .yaml definition of the agent for editing.
- Select the **Open Code File** button to create a sample code file that uses the agent.
- Select the **Open Playground** button to open the agent playground.

:::image type="content" source="../../media/how-to/get-started-projects-vs-code/deployed-agent-view.png" alt-text="Screenshot of the pane for agent preferences, with the Edit Agent, Open Code File, and Open Playground buttons highlighted." lightbox="../../media/how-to/get-started-projects-vs-code/deployed-agent-view.png":::

## Edit and update the deployed AI agent

1. On the **AGENT PREFERENCES** pane, select the **Edit Agent** button. The agent designer opens with the agent's .yaml file.

1. Edit the agent's configuration, such as the model, tools, and instructions.

1. After you finish editing, select the **Update Agent on Foundry** button to save your changes.

:::image type="content" source="../../media/how-to/get-started-projects-vs-code/update-agent.png" alt-text="Screenshot of the pane for agent preferences, with the Update Agent on Foundry button highlighted." lightbox="../../media/how-to/get-started-projects-vs-code/update-agent.png":::

## Create a sample code file

1. Right-click your deployed agent, and then select the **Open Code File** option. Or, on the **AGENT PREFERENCES** pane, select the **Open Code File** button.

    :::image type="content" source="../../media/how-to/get-started-projects-vs-code/open-agent-code-file.png" alt-text="Screenshot of the agent shortcut menu with the Open Code File option highlighted." lightbox="../../media/how-to/get-started-projects-vs-code/open-agent-code-file.png":::

1. In the **Choose your preferred SDK** dropdown list, select your preferred SDK for the agent code file, and then select the <kbd>Enter</kbd> key.

    :::image type="content" source="../../media/how-to/get-started-projects-vs-code/choose-agent-preferred-sdk.png" alt-text="Screenshot of the dropdown list for selecting an SDK as part of agent code file selection." lightbox="../../media/how-to/get-started-projects-vs-code/choose-agent-preferred-sdk.png":::

1. In the **Choose a language** dropdown list, select your preferred language for the agent code file, and then select the <kbd>Enter</kbd> key.

    :::image type="content" source="../../media/how-to/get-started-projects-vs-code/choose-agent-language.png" alt-text="Screenshot of the dropdown list for choosing a language as part of agent code file selection." lightbox="../../media/how-to/get-started-projects-vs-code/choose-agent-language.png":::

1. In the **Choose an auth method** dropdown list, select your preferred authentication method for the agent code file, and then select the <kbd>Enter</kbd> key.

    :::image type="content" source="../../media/how-to/get-started-projects-vs-code/choose-agent-authn-method.png" alt-text="Screenshot of the dropdown list for choosing an authentication method as part of agent code file selection." lightbox="../../media/how-to/get-started-projects-vs-code/choose-agent-authn-method.png":::

### Explore the sample code file

The following Python sample code file demonstrates a basic call to interact with the agent through the Foundry Projects API.

:::image type="content" source="../../media/how-to/get-started-projects-vs-code/sample-agent-code-file.png" alt-text="Screenshot of a generated agent sample code file." lightbox="../../media/how-to/get-started-projects-vs-code/sample-agent-code-file.png":::

## Interact with agents by using the agent playground

1. Right-click your deployed agent, and then select the **Open Playground** option.

   Alternatively, select the **Agent Playground** link in the **Tools** subsection, and then select your agent from the dropdown list.

   This step opens the **Agent Playground** pane and starts a thread with your agent so that you can send messages.

    :::image type="content" source="../../media/how-to/get-started-projects-vs-code/agent-display-playground.png" alt-text="Screenshot of the agent playground in Visual Studio Code." lightbox="../../media/how-to/get-started-projects-vs-code/agent-display-playground.png":::

1. Enter your prompt and view the outputs.

   This example uses **Bing Grounding** to illustrate a web search for information. The agent uses the model and tools that you configured in the agent designer. The source of the information appears in the section for agent annotations.

    :::image type="content" source="../../media/how-to/get-started-projects-vs-code/agent-playground-run.png" alt-text="Screenshot of the Agent Playground pane with agent annotations highlighted in VS Code." lightbox="../../media/how-to/get-started-projects-vs-code/agent-playground-run.png":::

## Explore threads

The **Threads** subsection displays the threads created during a run with your agent. In the **Azure Resources** view, expand the **Threads** subsection to view the list.

:::image type="content" source="../../media/how-to/get-started-projects-vs-code/thread-list.png" alt-text="Screenshot of the threads in the Threads subsection." lightbox="../../media/how-to/get-started-projects-vs-code/thread-list.png":::

Keep these terms in mind as you explore threads:

- A *thread* is a conversation session between an agent and a user. Threads store messages and automatically handle truncation to fit content into a model's context.

- A *message* is a single interaction between the agent and the user. Messages can include text, images, and other files. Messages are stored as a list on the thread.

- A *run* is a single execution of an agent. Each run can have multiple threads, and each thread can have multiple messages. The agent uses its configuration and a thread's messages to perform tasks by calling models and tools. As part of a run, the agent appends messages to the thread.

### View thread details

To view the **THREAD DETAILS** pane, select a thread.

:::image type="content" source="../../media/how-to/get-started-projects-vs-code/thread-view.png" alt-text="Screenshot of the pane for thread details." lightbox="../../media/how-to/get-started-projects-vs-code/thread-view.png":::

### View run details

To view run information in a JSON file, select the **View run info** button on the **THREAD DETAILS** pane. The following screenshot shows an example JSON file.

:::image type="content" source="../../media/how-to/get-started-projects-vs-code/run-file.png" alt-text="Screenshot of an example JSON file of run details." lightbox="../../media/how-to/get-started-projects-vs-code/run-file.png":::

## Clean up resources

The Azure resources that you created in this article are billed to your Azure subscription. If you don't expect to need these resources in the future, delete them to avoid incurring more charges.

### Delete your agents

[!INCLUDE [tip-left-pane](../../includes/tip-left-pane.md)]

1. In VS Code, refresh the **Azure Resources** view. Expand the **Agents** subsection to display the list of deployed agents.
1. Right-click the deployed agent that you want to delete, and then select **Delete**.

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
