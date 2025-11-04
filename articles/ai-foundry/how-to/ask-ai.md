---
title: Ask AI for help
titleSuffix: Azure AI Foundry
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

Our portal offers the ability to ask AI to assist you in Azure AI Foundry. To start using AI to ask questions, simply click on its icon located in the top right bar of the [!INCLUDE [classic-link](../includes/classic-link.md)] portal. A chat window opens where you can type your questions and receive answers in real-time.

:::image type="content" source="../media/ask-ai/ask-ai-classic.png" alt-text="Screenshot shows the Ask AI button in the top right bar of the Azure AI Foundry classic portal.":::

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

## Capabilities

**What This AI Can Do** - The Ask AI experience is designed to provide assistance by answering questions based on:

- **Azure AI Foundry Documentation**: This documentation includes details about Azure AI Foundry such as Quickstarts, How-Tos or reference documentation of the Azure AI Foundry SDK. The agent can help you navigate the documentation, or find answers for you.
- **Model Catalog**: The model catalog is a comprehensive hub for discovering, evaluating, and deploying a wide range of AI models. It features hundreds of models from various providers, including Azure OpenAI in Foundry Models, Mistral, Meta, Cohere, NVIDIA, and Hugging Face, as well as models trained by Microsoft. The agent can provide information about the models available in the Azure AI Foundry catalog.

**What This AI Cannot Do** - While the agent is a powerful tool, it has some limitations:

- **No Access to Your Resources**: the agent can't access your Azure resources. For example, it can't answer questions like "How much capacity do I have?" or "What is the status of my deployment?"
- **Limited Scope**: It's restricted to answering questions related to the Azure AI Foundry documentation and model catalog. It can't provide support for unrelated Azure services or external systems.

Use the agent to make the most of the Azure AI Foundry experience but keep its scope and limitations in mind when asking questions.

::: moniker-end


::: moniker range="foundry"

Our portal offers the ability to ask AI to assist you in Azure AI Foundry. To start using AI to ask questions or complete tasks, simply click on its icon located in the top right bar of the [!INCLUDE [classic-link](../includes/classic-link.md)] portal. A chat window opens where you can type your questions and receive answers in real-time. You can also ask the agent to run tasks for you.

:::image type="content" source="../media/ask-ai/ask-ai.png" alt-text="Screenshot shows the Ask AI button in the top right bar of the Azure AI Foundry portal.":::

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

## Capabilities

**What This AI Can Do** - The Ask AI experience is designed to provide assistance by answering questions based on:

- **Azure AI Foundry Documentation**: This documentation includes details about Azure AI Foundry such as Quickstarts, How-Tos or reference documentation of the Azure AI Foundry SDK. The agent can help you navigate the documentation, or find answers for you.
- **Model Catalog**: The model catalog is a comprehensive hub for discovering, evaluating, and deploying a wide range of AI models. It features hundreds of models from various providers, including Azure OpenAI in Foundry Models, Mistral, Meta, Cohere, NVIDIA, and Hugging Face, as well as models trained by Microsoft. The agent can provide information about the models available in the Azure AI Foundry catalog.
- **Quota and Model Operations**: The agent can look for existing quota in your subscription, and can manage your model deployments for you.

**What This AI Cannot Do** - While the agent is a powerful tool, it has some limitations and constraints:

- **Call External APIs**: This AI experience can only call for a specific subset of Azure AI Foundry APIs. It cannot access the web or APIs external to Microsoft.
- **Bypass Permissions**: This AI experience can execute actions on your behalf, but it will require you to have the right permissions for those actions. This agent cannot perform an action that you would not be able to do yourself.

Use the agent to make the most of the Azure AI Foundry experience but keep its scope and limitations in mind when asking questions.

::: moniker-end

## Responsible AI FAQ for the Foundry agent

### What is Ask AI in Azure AI Foundry?

It is an AI agent that enables users of Azure AI Foundry to navigate its capabilities, identify models, and understand how to use its resources to build generative AI applications. For an overview of how the agent works and a summary of its capabilities, see the overview above.

### What is the current status of the Ask AI feature?

It is available in Azure AI Foundry as a preview feature.

### Are the Ask AI results reliable?

The agent is designed to generate the best possible responses within the context to which it has access. However, like any AI system, the agent's responses are not always perfect. All of the agent's responses should be carefully tested, reviewed, and vetted before using the responses in Azure AI Foundry or for your application.

### How do I provide feedback on Ask AI?

If you see a response that is inaccurate, or does not support your needs use the thumbs-down button below the response to submit feedback. You can also submit feedback on your overall experience by using the Azure AI Foundry feedback button on the top menu.

### What should I do if I see unexpected or offensive content?

The Azure AI Foundry team has built the agent guided by our [AI principles](https://www.microsoft.com/ai/principles-and-approach) and [Responsible AI Standard](https://aka.ms/RAIStandardPDF). We have prioritized mitigating exposing customers to offensive content. However, you might still see unexpected results. We're constantly working to improve our technology to prevent the output of harmful content.

If you encounter harmful or inappropriate content in the system, select the thumbs-down icon below the response to provide feedback or report a concern.

### How current is the information provided by the agent?

We update the agent daily to keep it up to date with the latest information. In most cases, the information the agent provides is up to date. However, there might be some delay between new Azure AI Foundry announcements and updates to the agent.
