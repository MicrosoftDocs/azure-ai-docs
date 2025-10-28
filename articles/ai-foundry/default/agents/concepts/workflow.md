---
title: Build a Workflow in Azure AI Foundry
titleSuffix: Azure AI Foundry
description: This article explains how to build a Workflow in Azure AI Foundry using agents. 
ms.service: azure-ai-foundry
ms.custom:
  - build-2025
  - code01
ms.topic: tutorial
ms.date: 10/25/2025
ms.reviewer: fniedtner
ms.author: ssalgado
manager: nitinme
author: ssalgadodev
#customer intent: As a developer, I want to learn how to build a workflow.
---

# Build a Workflow in Azure AI Foundry

Workflows are a UI-based tool in Foundry to create declarative workflows, a predefined sequence of actions including agents, as in Microsoft Agent Framework Workflows.

Workflows enable you to build intelligent automation systems that seamlessly blend AI agents with business processes, in a visual manner. Traditional single-agent systems are limited in their ability to handle complex, multi-faceted tasks. By orchestrating multiple agents, each with specialized skills or roles, we can create systems that are more robust, adaptive, and capable of solving real-world problems collaboratively.

## Prerequisites

- [!INCLUDE [azure-subscription](../../../includes/azure-subscription.md)]
* A [project in Azure AI Foundry](/azure/ai-foundry/how-to/create-projects) in the westus2 region.

## Create a workflow

In Azure AI Foundry, you can choose to create a blank workflow or choose from one of the premade configured options. For this tutorial, we will be creating a Sequential workflow. If you want to learn more about different types of workflows, see the [workflow concepts](#workflow-concepts) section of this article. 

### Creating a Sequential workflow

1. Go to [Foundry Portal](https://eastus2euap.ai.azure.com/nextgen/r/LThb9AdWSnaqlSi_ntO2JQ,rg-vkintali-5609,,vkintali-prod-westus2-resource,vkintali-prod-westus2/Build/workflows?flight=ignite_preview%3Dfalse%2Cnextgen_canary).
2. Select **Create new workflow** and **Sequential**.
3. Assign an agent to the agent nodes by selecting each agent node in the workflow and selecting the [desired agent](#adding-existing) or [create a new one](#create-new-agents).
4. When you make changes to the workflow, select **Save** in the visualizer to save any changes.
5. Select **Run Workflow**.
6. Interact with the workflow in the chat window.
7. (Optional) you can add new nodes to your workflow with steps found in the [adding nodes to your workflow](#adding-nodes-to-your-workflow) section.

> [!IMPORTANT]
> Workflows are not saved automatically. Select **Save** every time you want to save changes to your workflow.

## Workflow Concepts

To start creating a new workflow, you can begin with a blank workflow or select one of the templates of pre-defined orchestration patterns [Microsoft Agent Framework Workflows Orchestrations | Microsoft Learn](/agent-framework/user-guide/workflows/orchestrations/overview).

| Pattern    | Description                                                        | Typical Use Case                                         |
|------------|--------------------------------------------------------------------|----------------------------------------------------------|
| Concurrent | Broadcasts a task to all agents, collects results independently.   | Parallel analysis, independent subtasks, ensemble decision making. |
| Sequential | Passes the result from one agent to the next in a defined order.   | Step-by-step workflows, pipelines, multi-stage processing. |
| Handoff    | Dynamically passes control between agents based on context or rules.| Dynamic workflows, escalation, fallback, or expert handoff scenarios. |
| Magentic   | Inspired by MagenticOne.                                           | Complex, generalist multi-agent collaboration.           |

## Adding nodes to your workflow

When selecting a pre-built workflow, you should see a workflow of nodes displayed in the builder. Each node corresponds to a specific action or component and performs a step in sequence. You can modify the order of the nodes by selecting the three dots on the node and selecting **move**. You can add new nodes by selecting the **+** icon in the workspace.

Nodes define the building blocks of your workflow. Common node types include:

- **Agent**: Invoke an agent.
- **Logic**: If/Else, Go To, For Each.
- **Data Transformation**: Set Variable, Parse Value.
- **Basic chat**: Send a message or ask a question to an agent.

## Add Agents to your Workflow

You can add any Foundry agent from your project to the workflow. Agent nodes also allow you to create new agents, configure their model, prompt, and tools, giving them customized capabilities.
For more advanced options and comprehensive agent creation, visit the Foundry Agent tab in the AI Foundry portal.

### Adding Existing

1. Select the '+' sign in the workflow visualizer.
2. In the pop-up dropdown, select **Invoke agent**.
3. In the "Create new agent" window, select **existing**.
4. Type the agent name to search for existing agents in your Foundry project.
5. Select the desired agent to add it into your workflow.

### Create new agents

1. Select the '+' sign in the workflow visualizer.
2. In the pop-up dropdown, select **Invoke agent**.
3. Enter an agent name and description of what the agent does.
4. Select **Add**.
5. Configure the agent in the invoke an agent window.
6. Select **Save**.

## Additional features

- **YAML Visualizer View toggle**: The workflow will be stored in a YAML file, it can be modified in the visualizer and the YAML view. Saving will create a new version; you have access to the version history. The visualizer and the YAML are editable. You can edit the YAML file and any changes to the file will be reflected in the visualizer.
- **Versioning**: Each time you save your workflow, a new, unchangeable version is created. To view the version history or delete older versions, open the Version dropdown located to the left of the Save button.
- **Add Notes to your workflow visualizer**: You can add notes on the workflow visualizer to add additional context or information regarding your workflow. In the upper left corner of the workflow visualizer, select **Add note**.
