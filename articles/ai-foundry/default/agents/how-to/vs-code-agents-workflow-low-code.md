---
title: Add declarative agent workflows in Visual Studio Code
titleSuffix: Microsoft Foundry
description: Add and test declarative agent workflows in Foundry Agent Service by using the Microsoft Foundry for Visual Studio Code extension. Convert YAML workflows to Agent Framework code.
manager: mcleans
ms.service: azure-ai-foundry
content_well_notification: 
  - AI-contribution
ai-usage: ai-assisted
ms.topic: how-to
ms.date: 02/18/2026
ms.reviewer: erichen
ms.author: johalexander
author: ms-johnalex
---

# Add declarative agent workflows in Visual Studio Code

Declarative agent workflows define predefined sequences of actions for your agents using configurations rather than explicit programming logic. In this article, you add [Foundry Agent workflows](../concepts/workflow.md) to an agent and test them by using the [Microsoft Foundry for Visual Studio Code (VS Code) extension](https://marketplace.visualstudio.com/items?itemName=TeamsDevApp.vscode-ai-foundry).

After you [build an agent in Foundry Agent Service](../../../how-to/develop/vs-code-agents.md) by using the VS Code extension, you can add workflows to orchestrate multiple agents into predefined action sequences for complex automation scenarios.

> [!IMPORTANT]
> Items marked (preview) in this article are currently in public preview. This preview is provided without a service-level agreement, and isn't recommended for production workloads. For more information, see [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).

## Prerequisites

- A Foundry project with at least one deployed agent. To create one, see [Build an agent with the VS Code extension](../../../how-to/develop/vs-code-agents.md).
- At least one workflow created in the [Foundry portal](https://ai.azure.com/?cid=learnDocs). For more information about workflows, see [Foundry Agent workflows](../concepts/workflow.md).
- The [Microsoft Foundry for Visual Studio Code extension](https://marketplace.visualstudio.com/items?itemName=TeamsDevApp.vscode-ai-foundry) installed.
- A [GitHub Copilot](https://github.com/features/copilot) subscription (required for converting YAML workflows to Agent Framework code).

## View a declarative agent workflow

To view and edit a declarative agent workflow in VS Code for the Web, first navigate to the workflow in the Foundry portal:

1. In the Foundry portal, open your project that contains the workflow.
1. Select the **Workflows** tab from the left-hand menu.
1. Select the workflow you want to open.

Then choose one of the following options to open the workflow in VS Code for the Web.

### Open the YAML workflow in VS Code for the Web

1. Select the **Build** tab and then select the **YAML** button on the right-hand side.
1. Select the **Open in VS Code for Web** button. The workflow YAML file opens in the VS Code for the Web editor with the YAML definition on the left and a visual workflow graph on the right.
1. Edit the YAML as needed to modify the workflow. Changes are reflected in the visual editor.
1. When you're done, select **Deploy** from the ellipsis menu (**...**) in the upper right corner to save your changes back to Foundry.

### Open the workflow code from the Foundry portal

1. Select the **Build** tab and then select the **Code** button on the right-hand side.
1. Select the **Open in VS Code for the Web** button. The workflow code file opens in the VS Code for the Web editor with the code definition on the left and the visual workflow graph on the right.
1. Edit the code as needed to modify the workflow. Changes are reflected in the visual editor.
1. When you're done, select **Deploy** from the ellipsis menu (**...**) in the upper right corner to save your changes back to Foundry.

## Test a workflow in the local playground

Test your declarative agent workflow by using the local agent playground in the VS Code extension.

1. In the **My Resources** section of the VS Code extension, locate and select your Foundry project.
1. Select **Declarative Agents**.
1. Select the version of the workflow you want to test. 
1. The **Remote Agent Playground** pane opens and starts a conversation with your agent.

> [!TIP]
> You can also open the **Remote Agent Playground** from the **Tools** subsection and select your agent from the dropdown list.

1. In the input box at the bottom of the **Remote Agent Playground** pane, type a message and press **Enter**.
1. Review the agent's response. Verify that the response matches the expected behavior for your workflow's defined actions.

## Convert a YAML workflow to Agent Framework code

To customize your YAML-based workflows, convert them to Agent Framework code with GitHub Copilot.

1. Open the workflow YAML file in VS Code.
1. Select the **Generate Code** button on the upper right of the YAML editor.
1. Select the programming language you want to generate the code in (Python, or C#). GitHub Copilot opens a pane with code generation prompts for the selected language and generates Agent Framework code based on the YAML definition.
1. When GitHub Copilot asks if you'd like to run the generated code locally, select **Yes** to open the local visualizer. You can see each step as the agent executes.
1. Review and modify the generated code as needed to fit your requirements.
1. Right-click the generated code file and select **Deploy to Foundry** to deploy the code to your Foundry project.
1. In the Foundry portal, navigate to your project and verify that the code appears in the **Agents** section.

## Related content

- [Foundry Agent workflows](../concepts/workflow.md)
- [Build an agent with the VS Code extension](../../../how-to/develop/vs-code-agents.md)
