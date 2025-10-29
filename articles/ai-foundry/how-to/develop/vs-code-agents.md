---
title: Work with Azure AI Foundry Agent Service in Visual Studio Code
titleSuffix: Azure AI Foundry
description: Use this article to learn how to use Azure AI Foundry Agent Service directly in Visual Studio Code.
manager: mcleans
ms.service: azure-ai-foundry
content_well_notification: 
  - AI-contribution
ai-usage: ai-assisted
ms.topic: how-to
zone_pivot_groups: ai-foundry-vsc-extension-languages
ms.date: 10/16/2025
ms.reviewer: erichen
ms.author: johalexander
author: ms-johnalex
---

# Work with Azure AI Foundry Agent Service in Visual Studio Code (preview)

After you [get started with the Azure AI Foundry for Visual Studio Code extension](./get-started-projects-vs-code.md), use [Azure AI Foundry Agent Service](/azure/ai-services/agents/overview) to build agents. Agents are microservices that:

- Answer questions by using their training data or search other sources with retrieval-augmented generation (RAG).
- Perform specific actions.
- Automate complete workflows.

Agents combine AI models with tools to access and interact with your data.

Azure AI Foundry developers can stay productive by developing, testing, and deploying agents in the familiar environment of Visual Studio Code (VS Code).

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

## Create and edit an Azure AI agent within the designer view

Follow these steps to create an Azure AI agent:

1. [Sign in to your Azure resources](./get-started-projects-vs-code.md#sign-in-to-your-resources).

1. [Set your default project](./get-started-projects-vs-code.md#create-a-project).

1. [Deploy a model](./get-started-projects-vs-code.md#deploy-a-model-from-the-model-catalog) to use with your agent.

1. In the **Azure AI Foundry Extension** view, find the **Resources** section.

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

Azure AI Foundry Agent Service has the following set of tools that you can use to interact with your data sources. These tools are available in the Azure AI Foundry for Visual Studio Code extension.

- [Grounding with Bing search](/azure/ai-foundry/agents/how-to/tools/bing-grounding)
- [File search](/azure/ai-services/agents/how-to/tools/file-search?tabs=python&pivots=overview)
- [Code interpreter](/azure/ai-foundry/agents/how-to/tools/code-interpreter)
- [OpenAPI specified tools](/azure/ai-foundry/agents/how-to/tools/openapi-spec)
- [Model Context Protocol (MCP)](/azure/ai-foundry/agents/how-to/tools/model-context-protocol)

For more information about using MCP tools, see [Work with Azure AI Foundry Agent Service and MCP server tools in Visual Studio Code (preview)](./vs-code-agents-mcp.md).

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

## Create an Azure AI agent on Azure AI Foundry

Create your agent directly on Azure AI Foundry by using the following steps:

1. In the designer, select the **Create Agent on Azure AI Foundry** button.

    :::image type="content" source="../../media/how-to/get-started-projects-vs-code/agent-deploy.png" alt-text="Screenshot of the agent designer with the button for creating an agent on Azure AI Foundry highlighted." lightbox="../../media/how-to/get-started-projects-vs-code/agent-deploy.png":::

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

1. After you finish editing, select the **Update Agent on Azure AI Foundry** button to save your changes.

:::image type="content" source="../../media/how-to/get-started-projects-vs-code/update-agent.png" alt-text="Screenshot of the pane for agent preferences, with the Update Agent on Azure AI Foundry button highlighted." lightbox="../../media/how-to/get-started-projects-vs-code/update-agent.png":::

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

The following Python sample code file demonstrates a basic call to interact with the agent through the Azure AI Foundry Projects API.

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

## Work with multi-agent workflows

You can use the Azure AI Foundry for Visual Studio Code extension to create multi-agent workflows. A multi-agent workflow is a sequence of agents that work together to accomplish a task. Each agent in the workflow can have its own model, tools, and instructions.

### Create a new multi-agent workflow

1. Open the command palette (<kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd>).

1. Run this command: `>Azure AI Foundry: Create a New Multi-agent Workflow`.

1. Select a programming language.

1. Select a folder where you want to save your new workflow.

1. Enter a name for your workflow project.

A new folder is created with the necessary files for your multi-agent workflow project, including a sample code file to get you started.

### Install dependencies

Install the required dependencies for your multi-agent workflow project. The dependencies vary based on the programming language that you selected when you created the project.

::: zone pivot="python"

Install the following packages from the source:

```bash
    git clone https://github.com/microsoft/agent-framework.git
    pip install -e agent-framework/python/packages/azure-ai -e agent-framework/python/packages/core
```

::: zone-end

::: zone pivot="csharp"

#### Prerequisites

To run the sample multi-agent workflow C# project, ensure that you have an Azure AI Foundry project or an Azure OpenAI resource.

#### Setup and installation

1. Download and install the .NET 9 SDK from the [official .NET website](https://dotnet.microsoft.com/download).

1. Go to your project directory and run this command to get the necessary NuGet packages:

    ```bash
    dotnet restore
    ```

1. The sample workflow project creates an .env file with the necessary environment variables. Create or update the .env file with your Azure OpenAI credentials:

    ```
    # Your Azure OpenAI endpoint
    AZURE_OPENAI_ENDPOINT=https://<your-openai-resource>.openai.azure.com/
       
    # Your Azure OpenAI API key
    AZURE_OPENAI_API_KEY=<your-api-key>
       
    # Your model deployment name in Azure OpenAI
    MODEL_DEPLOYMENT_NAME=<your-model-deployment-name>
    ```

    > [!IMPORTANT]
    > Never commit the .env file to version control. Add it to your .gitignore file.

::: zone-end

### Run your multi-agent workflow locally

::: zone pivot="csharp"

Before you run `dotnet run` locally, set up the required environment variables. You can get these values from the [Azure AI Foundry portal](https://ai.azure.com/?cid=learnDocs).

1. Set up your environment variables based on your operating system:

   #### [Windows (PowerShell)](#tab/windows-powershell)

   ```powershell
   $env:AZURE_OPENAI_ENDPOINT="https://your-resource-name.openai.azure.com/"
   $env:MODEL_DEPLOYMENT_NAME="your-deployment-name"
   $env:AZURE_OPENAI_API_KEY="your-api-key"
   ```

   #### [Windows (command prompt)](#tab/windows-command-prompt)

   ```dos
   set AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
   set MODEL_DEPLOYMENT_NAME=your-deployment-name
   set AZURE_OPENAI_API_KEY=your-api-key
   ```

   #### [macOS/Linux (Bash)](#tab/macos-linux-bash)

   ```bash
   export AZURE_OPENAI_ENDPOINT="https://your-resource-name.openai.azure.com/"
   export MODEL_DEPLOYMENT_NAME="your-deployment-name"
   export AZURE_OPENAI_API_KEY="your-api-key"
   ```

    ---

1. Run the application by using the following commands:

    ```bash
    dotnet build
    dotnet run
    ```

::: zone-end

::: zone pivot="python"

Update the .env file in the root directory of your project and add the following environment variables:

```
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key
MODEL_DEPLOYMENT_NAME=your-deployment-name
```

Run the application by using this command:

```bash
python workflow.py
```

### Visualize multi-agent workflow execution

By using the Azure AI Foundry for Visual Studio Code extension, you can visualize the interactions between agents and how they collaborate to achieve your desired outcome.

Enable visualization in your workflows by adding the following code snippet:

```python
from agent_framework.observability import setup_observability
setup_observability(vs_code_extension_port=4317) # Default port is 4317
```

To monitor and visualize your multi-agent workflow execution in real time (currently available for Python interactive mode only):

1. Open the command palette (<kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd>).

1. Run this command: `>Azure AI Foundry: Visualize the Multi-Agent Workflow`.

A new tab opens in VS Code to display the execution graph. The visualization updates itself automatically as your workflow progresses, to show the flow between agents and their interactions.

#### Port conflicts

If you find any port conflicts, change the visualization port by setting the `FOUNDRY_OTLP_PORT` environment variable. Update the observability port in the `workflow.py` file accordingly.

For example, to change the port to 4318, use this command:

```bash
  export FOUNDRY_OTLP_PORT=4318
```

In `workflow.py`, update the port number in the observability configuration:

```python
  setup_observability(vs_code_extension_port=4318)
```

::: zone-end

## Clean up resources

The Azure resources that you created in this article are billed to your Azure subscription. If you don't expect to need these resources in the future, delete them to avoid incurring more charges.

### Delete your agents

[!INCLUDE [tip-left-pane](../../includes/tip-left-pane.md)]

1. In the [Azure AI Foundry portal](https://ai.azure.com/?cid=learnDocs), on the left menu, select **Agents**.

1. Select the agent that you want to delete, and then select **Delete**.

    :::image type="content" source="../../media/how-to/get-started-projects-vs-code/delete-agent.png" alt-text="Screenshot of the Azure AI Foundry portal with the Delete command for a selected agent." lightbox="../../media/how-to/get-started-projects-vs-code/delete-agent.png":::

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
