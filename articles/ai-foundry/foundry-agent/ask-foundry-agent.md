---
title: Ask AI for help
titleSuffix: Microsoft Foundry
description: Learn how to ask AI for help, getting your questions answered and tasks supported.
ms.service: azure-ai-foundry
ms.date: 10/27/2025
ms.reviewer: sgilley
ms.author: jeomhove
author: jfomhover
ms.topic: concept-article
monikerRange: 'foundry-classic || foundry'
---

# Ask AI for help (preview)

## Overview

[!INCLUDE [version-banner](../includes/version-banner.md)]

::: moniker range="foundry-classic"

Our portal offers the ability to ask AI to assist you in Microsoft Foundry. To start using AI to ask questions, simply click on its icon located in the top right bar of the [!INCLUDE [classic-link](../includes/classic-link.md)] portal. A chat window opens where you can type your questions and receive answers in real-time.

:::image type="content" source="../media/ask-foundry-agent/ask-foundry.png" alt-text="Screenshot shows the Ask AI button in the top right bar of the Foundry (classic) portal.":::

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

## Capabilities

**What This AI Can Do** - The Ask AI experience is designed to provide assistance by answering questions based on:

- **Documentation**: This documentation includes details about Foundry such as Quickstarts, How-tos or reference documentation of the Microsoft Foundry SDK. The agent can help you navigate the documentation, or find answers for you.
- **Model Catalog**: Provide information about specific models in the Foundry model catalog, including their capabilities and features.
- **Troubleshooting**: Help diagnose and resolve common Foundry issues by searching the troubleshooting knowledge base and providing step-by-step solutions.

**What This AI Cannot Do** - While the agent is a powerful tool, it has some limitations:

- **No Access to Your Resources**: the agent can't access your Azure resources. For example, it can't answer questions like "How much capacity do I have?" or "What is the status of my deployment?"
- **Limited Scope**: It's restricted to answering questions related to the Foundry documentation and model catalog. It can't provide support for unrelated Azure services or external systems.

Use the agent to make the most of the Foundry experience but keep its scope and limitations in mind when asking questions.

::: moniker-end


::: moniker range="foundry"

Our portal offers the ability to ask AI to assist you in Foundry. To start using AI to ask questions or complete tasks, select its icon located in the top right bar of the [!INCLUDE [classic-link](../includes/classic-link.md)] portal. A chat window opens where you can type your questions and receive answers in real-time. You can also ask the agent to run tasks for you.

:::image type="content" source="../default/media/ask-foundry-agent/ask-ai.png" alt-text="Screenshot shows the Ask AI button in the top right bar of the Foundry portal.":::

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

## Capabilities

**What This AI Can Do** - The Ask AI experience is designed to provide assistance by answering questions and performing tasks through specialized sub-agents:

- **Documentation**: This documentation includes details about Foundry such as Quickstarts, How-tos or reference documentation of the Microsoft Foundry SDK. The agent can help you navigate the documentation, or find answers for you.
- **Model Catalog**: Provide information about specific models in the model catalog, including their capabilities and features.
- **Troubleshooting**: Help diagnose and resolve common Foundry issues by searching the troubleshooting knowledge base and providing step-by-step solutions.
- **Quota & Model Operations**: Deploy models, debug deployment issues, find deployment details, check quota and capacity in specific regions, and delete model deployments.
- **Model Analysis**: Recommend models based on cost, performance, or quality, compare models using benchmark data across quality, cost, throughput, safety, and latency criteria, and analyze operational data for Azure OpenAI deployments.
- **Monitoring Dashboard Insights**: Interpret evaluation dashboard visualizations, identify patterns and anomalies in monitoring data, and suggest optimizations based on performance metrics.
- **Evaluation Management**: Manage evaluation workflows for large language models and agents, including setup, execution, and monitoring of evaluation jobs. 

**What This AI Cannot Do** - While the agent is a powerful tool, it has some limitations and constraints:

- **Limited Scope**: It's restricted to answering questions related to the Foundry documentation and model catalog. It can't provide support for unrelated Azure services or external systems.
- **Call External APIs**: This AI experience can only call for a specific subset of Foundry APIs. It cannot access the web or APIs external to Microsoft.
- **Bypass Permissions**: This AI experience can execute actions on your behalf. It requires you to have the right permissions for those actions. This agent cannot perform an action that you would not be able to do yourself.

Use the agent to make the most of the Foundry experience but keep its scope and limitations in mind when asking questions.

## Actions and approvals

When you ask the Ask AI agent to perform tasks that require accessing or modifying your Azure resources, the agent proposes actions for you to review and approve before execution. This approval flow ensures you maintain oversight over what actions are performed on your behalf.

:::image type="content" source="../default/media/ask-foundry-agent/ask-ai-approval-flow.png" alt-text="Screenshot shows the Ask AI chat on the right side of Foundry portal. The Ask AI agent is responding a user query by proposing to run an action for the user to approve.":::

The actions are drawn from the tools made available under the [Foundry MCP Server](../default/mcp/available-tools.md).

To make this approval flow easier, you can **change the approval settings** to pre-approve some actions depending on their scope. Access the approval settings by selecting the settings icon in the Ask AI prompt chat box. By default, this experience is set to pre-approve **System access** actions. You can change these settings anytime, and they will be persisted beyond your session.

:::image type="content" source="../default/media/ask-foundry-agent/ask-ai-approval-settings.png" alt-text="Screenshot shows the Ask AI prompt chat box, showing the location of the approval settings.":::

## Best practices and security guidance

The Ask AI experience relies on the [Foundry MCP Server](../default/mcp/get-started.md). In doing so, it implements the [same best practices and security guidance](../default/mcp/security-best-practices.md).

> [!IMPORTANT]
> By using this preview feature, you are acknowledging and consenting to any cross-region processing that may occur. As an example, an EU resource accessed by a US user could be routed through US infrastructure. If your organization requires strict in-region processing, do not use Ask AI (preview) or restrict its use to scenarios that remain within your selected region.

::: moniker-end

## Responsible AI FAQ for Ask AI

### What is Ask AI in Foundry?

It's an AI agent that enables users of Foundry to navigate its capabilities, identify models, and understand how to use its resources to build generative AI applications. For an overview of how the agent works and a summary of its capabilities, see the overview above.

### What is the current status of the Ask AI feature?

It is available in Foundry as a preview feature.

### Are the Ask AI results reliable?

The agent is designed to generate the best possible responses within the context to which it has access. However, like any AI system, the agent's responses are not always perfect. All of the agent's responses should be carefully tested, reviewed, and vetted before using the responses in Foundry or for your application.

### How do I provide feedback on Ask AI?

If you see a response that is inaccurate, or does not support your needs use the thumbs-down button below the response to submit feedback. You can also submit feedback on your overall experience by using the Foundry feedback button on the top menu.

### What should I do if I see unexpected or offensive content?

The Foundry team has built the agent guided by our [AI principles](https://www.microsoft.com/ai/principles-and-approach) and [Responsible AI Standard](https://aka.ms/RAIStandardPDF). We have prioritized mitigating exposing customers to offensive content. However, you might still see unexpected results. We're constantly working to improve our technology to prevent the output of harmful content.

If you encounter harmful or inappropriate content in the system, select the thumbs-down icon below the response to provide feedback or report a concern.

### How current is the information provided by the agent?

We update the agent daily to keep it up to date with the latest information. In most cases, the information the agent provides is up to date. However, there might be some delay between new Foundry announcements and updates to the agent.
