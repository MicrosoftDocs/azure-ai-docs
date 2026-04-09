---
title: "How to get started with an AI template"
description: "Find, explore, and deploy AI solution templates from the Foundry portal to accelerate your development."
keywords: ai templates, solution accelerators, foundry templates, code samples
ms.service: azure-ai-foundry
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
>Agents and AI solutions you create might be subject to legal and regulatory requirements, might require licenses, or might not be suitable for all industries, scenarios, or use cases. By using any sample, you acknowledge that Agents, AI solutions, or other output created using those samples are solely your responsibility, and that you will comply with all applicable laws, regulations, and relevant safety standards, terms of service, and codes of conduct.  

Available templates:

| Template | Popular customer use cases |
|----------|----------------------------|
| [Get started with AI chat](https://github.com/Azure-Samples/get-started-with-ai-chat) | Build interactive chat applications<br><br>[Baseline Microsoft Foundry chat reference architecture](/azure/architecture/ai-ml/architecture/baseline-azure-ai-foundry-chat) |
| [Get started with AI agents](https://github.com/Azure-Samples/get-started-with-ai-agents) | Create autonomous AI agents |
| [Build agentic apps to unify data](https://github.com/microsoft/agentic-applications-for-unified-data-foundation-solution-accelerator/tree/main) | Embed analytics across applications with instant data visualization for:<br>• Sales performance analysis<br>• Customer insights and reporting<br>• Natural language analysis on structured data |
| [Create a multi-agent release manager assistant](https://github.com/Azure-Samples/openai/tree/main/Agent_Based_Samples/release_manager) | Enable AI-powered release planning for:<br>• Cross-system release coordination<br>• Real-time dependency mapping and release health assessment<br>• Advanced visualization for retrieved insights<br>• Safe update mechanisms built into AI agents |
| [Create a call center voice agent](https://github.com/Azure-Samples/call-center-voice-agent-accelerator) | Develop interactive voice agents for:<br>• Customer support<br>• Product catalog navigation<br>• Self-service solutions |
| [Unlock insights from conversational data](https://github.com/microsoft/Conversation-Knowledge-Mining-Solution-Accelerator) | Extract knowledge from conversations<br><br>[Build a conversation knowledge mining solution](/azure/architecture/ai-ml/idea/unlock-insights-from-conversational-data) |
| [Multi-agent workflow automation](https://github.com/microsoft/Multi-Agent-Custom-Automation-Engine-Solution-Accelerator) | Automate complex workflows<br><br>[Build a multiple-agent workflow automation solution](/azure/architecture/ai-ml/idea/multiple-agent-workflow-automation) |
| [Multi-modal content processing](https://github.com/microsoft/content-processing-solution-accelerator) | Process diverse content types<br><br>[Extract and map information from unstructured content](/azure/architecture/ai-ml/idea/multi-modal-content-processing) |
| [Generate documents from your data](https://github.com/microsoft/document-generation-solution-accelerator) | Create documents automatically<br><br>[Build a document generation system](/azure/architecture/ai-ml/idea/generate-documents-from-your-data) |
| [Improve client meetings with agents](https://github.com/microsoft/Build-your-own-copilot-Solution-Accelerator) | Enhance meeting productivity |
| [Modernize your code with agents](https://github.com/microsoft/Modernize-your-code-solution-accelerator) | Update legacy code |
| [Build your conversational agent](https://github.com/Azure-Samples/Azure-Language-OpenAI-Conversational-Agent-Accelerator) | Create conversational experiences |
| [Retrieve and summarize SharePoint data](https://github.com/microsoft/app-with-sharepoint-knowledge)  | Retrieve content from SharePoint sites |

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
