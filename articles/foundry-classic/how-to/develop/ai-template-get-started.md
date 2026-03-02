---
title: "How to get started with an AI template (classic)"
description: "Find, explore, and deploy AI solution templates from the Foundry portal to accelerate your development. (classic)"
keywords: ai templates, solution accelerators, foundry templates, code samples
ms.service: azure-ai-foundry
ms.custom:
  - classic-and-new
  - dev-focus
  - ignite-2024
ms.topic: how-to
ms.date: 01/05/2026
ms.reviewer: varundua
ms.author: sgilley
author: sdgilley
ai-usage: ai-assisted
#customer intent: As a developer, I want to jump start my journey with an AI template.
ROBOTS: NOINDEX, NOFOLLOW
---

# Get started with an AI template (classic)

[!INCLUDE [classic-banner](../../includes/classic-banner.md)]

In this article, you find, explore, and deploy AI solution templates from the Foundry portal.

AI solution templates are prebuilt, task-specific templates that include customizable code samples, preintegrated Azure services, and GitHub-hosted quick-start guides. Use templates to skip boilerplate setup and focus on building solutions for use cases like voice agents, release management, and data unification.

> [!IMPORTANT]
> Starter templates, manifests, code samples, and other resources made available by Microsoft or its partners ("samples") are designed to assist in accelerating development of agents and AI solutions for specific scenarios. Review all provided resources and carefully test output behavior in the context of your use case. AI responses might be inaccurate and AI actions should be monitored with human oversight. Learn more in the transparency documents for [Agent Service](../../responsible-ai/agents/transparency-note.md) and [Agent Framework](https://github.com/microsoft/agent-framework/blob/main/TRANSPARENCY_FAQ.md).  
>
>Agents and AI solutions you create might be subject to legal and regulatory requirements, might require licenses, or might not be suitable for all industries, scenarios, or use cases. By using any sample, you acknowledge that Agents, AI solutions, or other output created using those samples are solely your responsibility, and that you will comply with all applicable laws, regulations, and relevant safety standards, terms of service, and codes of conduct.  

Available templates include:

* [Get started with AI chat](https://github.com/Azure-Samples/get-started-with-ai-chat)
* [Get started with AI agents](https://github.com/Azure-Samples/get-started-with-ai-agents)
* [Unlock insights from conversational data](https://github.com/microsoft/Conversation-Knowledge-Mining-Solution-Accelerator)
* [Multi-agent workflow automation](https://github.com/microsoft/Multi-Agent-Custom-Automation-Engine-Solution-Accelerator)
* [Multi-modal content processing](https://github.com/microsoft/content-processing-solution-accelerator)
* [Generate documents from your data](https://github.com/microsoft/document-generation-solution-accelerator)
* [Improve client meetings with agents](https://github.com/microsoft/Build-your-own-copilot-Solution-Accelerator)
* [Modernize your code with agents](https://github.com/microsoft/Modernize-your-code-solution-accelerator)
* [Build your conversational agent](https://github.com/Azure-Samples/Azure-Language-OpenAI-Conversational-Agent-Accelerator)

> [!TIP]
> Each template includes a GitHub README with setup, deployment, and customization instructions. Start there for the fastest path forward.

## Prerequisites

- [!INCLUDE [azure-subscription](../../../foundry/includes/azure-subscription.md)]
- Appropriate RBAC role to create Foundry resources. For details, see [Role-based access control](../../concepts/rbac-foundry.md).
- Either a [[!INCLUDE [fdp-project-name](../../../foundry/includes/fdp-project-name.md)]](../create-projects.md) or a [[!INCLUDE [hub-project-name](../../../foundry/includes/hub-project-name.md)]](../hub-create-projects.md).
## Start with a sample application

[!INCLUDE [tip-left-pane](../../includes/tip-left-pane.md)]

1. [!INCLUDE [version-sign-in](../../includes/version-sign-in.md)]
1. Open your project.
1. On the left pane, select **Templates**.
1. Find the solution template you want to use.
1. Select **Open in Github** to view the entire sample application.
1. In some cases, you can also view a step-by-step tutorial that explains the AI code.

## Explore the sample application

When you view the GitHub repository for your sample, check the README for more instructions and information on how to deploy your own version of the application.

Instructions vary by sample, but most include how to:

* Open the solution in the location of your choice:
  * GitHub Codespaces
  * VS Code Dev Containers
  * Your local IDE
* Deploy the application to Azure
* Test the application

The README also includes information about the application, such as the use case, architecture, and pricing information.

## Deploy and customize templates

Most templates support quick-deploy options that launch in minutes. These architectures and implementations are customizable while staying [Well-Architected Framework](/azure/well-architected/) aligned by using [Azure Verified Modules](/azure/azure-resource-manager/bicep/azure-verified-modules). Use tools such as [PSRule](https://aka.ms/ps-rule) and [TFLint](https://github.com/terraform-linters/tflint) to test that your modified implementation is production-ready.

After you deploy, verify that the application is running:

1. Open the deployment URL shown in the terminal output.
1. Confirm the application loads and responds to your input.

## Benefits of AI solution templates

AI templates in Microsoft Foundry provide:

* **Faster time-to-value**: Skip boilerplate code and infrastructure setup to move from concept to production quickly.
* **Reduced engineering overhead**: Preintegrated Azure services eliminate deployment friction.
* **Trusted infrastructure**: Build with confidence on Microsoft's secure, scalable AI platform.
* **Modular and interoperable foundation**: Scale solutions efficiently across your organization.
* **Best practices built-in**: Use proven patterns and frameworks for production-ready solutions.

## Related content

- [Quickstart: Get started with Foundry](../../quickstarts/get-started-code.md)
- [Role-based access control for Microsoft Foundry](../../concepts/rbac-foundry.md)
- [What is Microsoft Foundry?](../../what-is-foundry.md)
