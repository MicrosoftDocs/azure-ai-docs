---
title: Work with Declarative (Low-code) Agent workflows in Visual Studio Code
titleSuffix: Microsoft Foundry
description: Use this article to learn how to use low-code declarative workflows with Foundry Agent Service directly in VS Code.
manager: mcleans
ms.service: azure-ai-foundry
content_well_notification: 
  - AI-contribution
ai-usage: ai-assisted
ms.topic: how-to
ms.date: 11/17/2025
ms.reviewer: erichen
ms.author: johalexander
author: ms-johnalex
---

# Work with Declarative (Low-code) Agent workflows in Visual Studio Code (preview)

In this article, you learn how to add and use [Foundry Agent workflows](../concepts/workflow.md) with Azure AI agents by using the [Microsoft Foundry for Visual Studio Code extension](https://marketplace.visualstudio.com/items?itemName=TeamsDevApp.vscode-ai-foundry).

After you [build an agent in Foundry Agent Service](
/azure/ai-foundry/how-to/develop/vs-code-agents?view=foundry&tabs=windows-powershell&pivots=python&preserve-view=true) by using this Visual Studio Code (VS Code) extension, you can add workflows to your agent.

Foundry Workflows is a UI-based tool in Foundry that creates declarative, predefined sequences of actions including agents, as in Microsoft Agent Framework Workflows.

Workflows let you build intelligent automation systems that blend AI agents with business processes in a visual way. Traditional single-agent systems struggle to handle complex tasks with many parts. When you orchestrate multiple agents, each with specialized skills or roles, you create systems that are more robust, adaptive, and capable of solving real-world problems together.

## What is a declarative agent?
A declarative agent is an AI agent that operates based on predefined rules, workflows, or configurations instead of explicit programming logic. This approach lets users define what the agent should do and how it should behave through high-level specifications. Declarative agents make it easier to create and manage complex interactions without deep coding knowledge.

## View a declarative agent workflow 
For declarative agent workflows start by creating a workflow in [Microsoft Foundry](https://ai.azure.com/?cid=learnDocs). The following sections guide you through the steps to view and test a simple workflow that uses an agent to process user input.

1. In Foundry, navigate to your project that contains the workflow you want to work with.
1. Select the **Workflows** tab from the left-hand menu.
1. Select the workflow you want to open in VS Code.

### Open in VS Code - YAML based workflow playground

1. Select the **Build** tab and then select the **YAML** button on the right-hand side.
1. Open the YAML directly from Foundry by selecting the **Open in VS Code for Web** button.
1. This action opens the workflow YAML file in the VS Code for Web editor.
1. View both the YAML definition and the visual representation of the workflow in the editor.
1. Edit the YAML as needed to modify the workflow and see the changes reflected in the visual editor.
1. When you're done, save your changes directly back to Foundry from the VS Code for Web editor by selecting Deploy from the ellipsis menu (...) in the upper right corner.

### Open in VS Code from Foundry 

1. In Foundry, navigate to your project that contains the workflow you want to work with.
1. Select the **Workflows** tab from the left-hand menu.  
1. Select the workflow you want to open in VS Code.
1. Select the **Build** tab and then select the **Code** button on the right-hand side.   
1. Select the **Open in VS Code for the Web** button. 
1. This action opens the workflow code file in the VS Code for Web editor.
1. View both the code definition and the visual representation of the workflow in the editor.
1.   Edit the YAML as needed to modify the workflow and see the changes reflected in the visual editor.
1. When you're done, save your changes directly back to Foundry from the VS Code for Web editor by selecting Deploy from the ellipsis menu (...) in the upper right corner. 

## Test workflow in playground

To test the workflow in the VS Code extension playground, follow these steps:

1. In the "My Resources" section of the VS Code extension, locate and select your Foundry project.
2. Select **Declarative Agents**.
1. Select the version of the workflow you want to test.
1. Right-click the workflow and select **Open in Local Agent Playground**.
    Alternatively, select the **Local Agent Playground** link in the **Tools** subsection, and then select your agent from the dropdown list.
    This step opens the **Local Agent Playground** pane and starts a conversation with your agent so that you can send messages.
1. In the input box at the bottom of the **Local Agent Playground** pane, type a message to send to the agent and press **Enter**.
1. Review the agent's response in the conversation.

## Convert YAML based workflow to Agent Framework code

To customize your YAML-based workflows, convert it to Agent Framework code using GitHub Copilot using the following steps:
1. Open the workflow YAML file in VS Code.
1. Select **Generate Code** button on the top-right of the YAML editor.
1. Select **Generate with Copilot** from the dropdown menu.
1. Select the programming language you want to generate the code in (Python, C#, or YAML).
1. In the GitHub Copilot pane that opens, the extension creates the code generation prompts for the selected language.
1. GitHub Copilot generates Agent Framework code based on the YAML definition.
1. GitHub Copilot will ask you if you'd like to run the generated code locally in the VS Code extension's local agent playground.
1. The local visualizer opens, and you can see each step as the agent executes.
1. Review and modify the generated code as needed to fit your requirements.
1. Right-click the generated code file and select **Deploy to Foundry** to deploy the code back to your Foundry project.
1. In Foundry, navigate to your project and verify that the code has been successfully deployed.
