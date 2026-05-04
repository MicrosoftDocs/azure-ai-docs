---
title: "How to get started with an AI template"
description: "Find, explore, and deploy AI solution templates from the Foundry portal to accelerate your development."
keywords: ai templates, solution accelerators, foundry templates, code samples
ms.service: microsoft-foundry
ms.custom:
  - classic-and-new
  - dev-focus
  - ignite-2024
  - doc-kit-assisted
ms.topic: how-to
ms.date: 04/08/2026
ms.reviewer: varundua
ms.author: sgilley
author: sdgilley
ai-usage: ai-assisted
#customer intent: As a developer, I want to jump start my journey with an AI template.
---

# Get started with an AI template

In this article, you find, explore, and deploy AI solution templates from the Foundry portal.

AI solution templates are prebuilt, task-specific templates that include customizable code samples, preintegrated Azure services, and GitHub-hosted quick-start guides. Use templates to skip boilerplate setup and focus on building solutions for use cases like voice agents, release management, and data unification.

> [!IMPORTANT]
> Starter templates, manifests, code samples, and other resources made available by Microsoft or its partners ("samples") are designed to assist in accelerating development of agents and AI solutions for specific scenarios. Review all provided resources and carefully test output behavior in the context of your use case. AI responses might be inaccurate and AI actions should be monitored with human oversight. Learn more in the transparency documents for [Agent Service](../../responsible-ai/agents/transparency-note.md) and [Agent Framework](https://github.com/microsoft/agent-framework/blob/main/TRANSPARENCY_FAQ.md).  
>
>Agents and AI solutions you create might be subject to legal and regulatory requirements, might require licenses, or might not be suitable for all industries, scenarios, or use cases. By using any sample, you acknowledge that Agents, AI solutions, or other output created using those samples are solely your responsibility, and that you will comply with all applicable laws, regulations, and relevant safety standards, terms of service, and codes of conduct.

## Templates for common AI scenarios

Jump start development with these templates for common AI scenarios, including sample code and architecture guidance.

| Scenario | GitHub repo | Documentation |
|:---|:---|:---|
| AI chat | [Sample code](https://github.com/Azure-Samples/get-started-with-ai-chat) | - [Architecture guidance: Baseline Microsoft Foundry chat](/azure/architecture/ai-ml/architecture/baseline-azure-ai-foundry-chat)<br><br>- [GitHub README resources](https://github.com/Azure-Samples/get-started-with-ai-chat?tab=readme-ov-file#resources) |
| AI agents | [Sample code](https://github.com/Azure-Samples/get-started-with-ai-agents) | - [GitHub README resources](https://github.com/Azure-Samples/get-started-with-ai-agents?tab=readme-ov-file#resources) |
| Conversation insights | [Sample code](https://github.com/microsoft/Conversation-Knowledge-Mining-Solution-Accelerator) | - [Architecture guidance: Conversation knowledge mining](/azure/architecture/ai-ml/idea/unlock-insights-from-conversational-data)<br><br>- [GitHub README resources](https://github.com/microsoft/Conversation-Knowledge-Mining-Solution-Accelerator#resources) |
| Multi-agent workflow automation | [Sample code](https://github.com/microsoft/Multi-Agent-Custom-Automation-Engine-Solution-Accelerator) | - [Architecture guidance: Build a multiple-agent workflow automation solution](/azure/architecture/ai-ml/idea/multiple-agent-workflow-automation)<br><br>- [GitHub README resources](https://github.com/microsoft/Multi-Agent-Custom-Automation-Engine-Solution-Accelerator#resources) |
| Multi-modal content processing | [Sample code](https://github.com/microsoft/content-processing-solution-accelerator) | - [Architecture guidance: Extract and map information from unstructured content](/azure/architecture/ai-ml/idea/multi-modal-content-processing)<br><br>- [GitHub README resources](https://github.com/microsoft/content-processing-solution-accelerator#resources) |
| Document generation | [Sample code](https://github.com/microsoft/document-generation-solution-accelerator) | - [Architecture guidance: Build a document generation system](/azure/architecture/ai-ml/idea/generate-documents-from-your-data)<br><br>- [GitHub README resources](https://github.com/microsoft/document-generation-solution-accelerator#resources) |
| Client meeting enhancement | [Sample code](https://github.com/microsoft/Build-your-own-copilot-Solution-Accelerator) | - [GitHub README resources](https://github.com/microsoft/Build-your-own-copilot-Solution-Accelerator#resources) |
| Code modernization | [Sample code](https://github.com/microsoft/Modernize-your-code-solution-accelerator) | - [GitHub README resources](https://github.com/microsoft/Modernize-your-code-solution-accelerator#resources) |
| Conversational agent | [Sample code](https://github.com/Azure-Samples/Azure-Language-OpenAI-Conversational-Agent-Accelerator) | - [GitHub README resources](https://github.com/Azure-Samples/Azure-Language-OpenAI-Conversational-Agent-Accelerator#resources) |

> [!TIP]
> Each template includes a GitHub README with setup, deployment, and customization instructions. Start there for the fastest path forward.

## Prerequisites

- [!INCLUDE [azure-subscription](../../includes/azure-subscription.md)]
- Appropriate RBAC role to create Foundry resources. For details, see [Role-based access control](../../concepts/rbac-foundry.md).
- A [Foundry project](../create-projects.md).

## Start with a sample application

1. [!INCLUDE [version-sign-in](../../includes/version-sign-in.md)]
1. Select **Discover** from the upper-right navigation.
1. Select **Solution templates** from the left pane.
1. Select **Open in GitHub** to view the entire sample application.
1. In some cases, you can also view a step-by-step tutorial that explains the AI code.

[!INCLUDE [ai-template-get-started 1](../../includes/how-to-develop-ai-template-get-started-1.md)]