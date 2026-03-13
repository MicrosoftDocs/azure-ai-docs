---
title: "What is Microsoft Foundry?"
description: "Microsoft Foundry is a trusted platform that empowers developers to drive innovation and shape the future with AI in a safe, secure, and responsible way."
author: sdgilley
ms.author: sgilley
ms.reviewer: sgilley
ms.date: 11/06/2025
ms.service: azure-ai-foundry
ms.topic: overview
ai-usage: ai-assisted
ms.custom:
  - classic-and-new
  - ignite-2023
  - build-2024
  - ignite-2024
  - build-aifnd
  - build-2025
  - doc-kit-assisted
keywords:
  - Foundry Tools
  - cognitive
# customer intent: As a developer, I want to understand what Microsoft Foundry is so that I can use it to build AI applications.
---

# What is Microsoft Foundry?

**Microsoft Foundry** is a unified Azure platform-as-a-service offering for enterprise AI operations, model builders, and application development. This foundation combines production-grade infrastructure with friendly interfaces, enabling developers to focus on building applications rather than managing infrastructure.

Microsoft Foundry unifies agents, models, and tools under a single management grouping with built-in enterprise-readiness capabilities including tracing, monitoring, evaluations, and customizable enterprise setup configurations. The platform provides streamlined management through unified role-based access control (RBAC), networking, and policies under one Azure resource provider namespace.

> [!TIP]
> * Coming from Azure OpenAI? [Upgrade your Azure OpenAI resource to a Foundry resource](./how-to/upgrade-azure-openai.md) while preserving your endpoint, API keys, and existing state. 
> * Using hub-based projects? Hub-based projects are accessible in the [Foundry (classic) portal](../foundry-classic/what-is-foundry.md). New investments are focused on Foundry projects in the new portal.

[!INCLUDE [previous-current](includes/previous-current.md)]

## Who is Foundry for?

Microsoft Foundry serves three primary audiences:
* Application developers building AI-powered products with agents, models, and tools. Start with the [quickstart](./quickstarts/get-started-code.md)
* ML engineers and data scientists who [fine-tune models](./openai/concepts/fine-tuning-considerations.md), [run evaluations](./observability/concepts/trace-agent-concept.md), and [manage model deployments](./foundry-models/how-to/monitor-models.md). 
* IT administrators and platform engineers who govern AI resources, enforce policies, and manage access across teams. See [security](./concepts/architecture.md#security-driven-separation-of-concerns) and governance and [Foundry Control Plane](./control-plane/overview.md).

## Key capabilities

### Build agents

* **[Multi-agent orchestration and workflows](agents/concepts/workflow.md)** – Build collaborative agent behavior and complex workflow execution using SDKs for C# and Python.
* **[Tool catalog](agents/concepts/tool-catalog.md)** – Connect over 1,400 tools through public and private catalogs.
* **[Memory](agents/concepts/what-is-memory.md)** – Retain and recall contextual information across interactions without requiring repeated input.
* **[Foundry IQ knowledge integration](agents/concepts/what-is-foundry-iq.md)** – Ground agent responses in enterprise or web content with citation-backed answers.
* **[Publishing](agents/how-to/publish-copilot.md)** – Publish agents to Microsoft 365, Teams, BizChat, or containerized deployments.

### Operate and govern

* **[Real-time observability](observability/how-to/how-to-monitor-agents-dashboard.md#set-up-continuous-evaluation)** – Monitor performance and governance with built-in metrics and model tracking.
* **Centralized AI asset management** – Manage all agents, models, and tools from the **Operate** section, including agents registered from other clouds.
* **Enterprise controls** – Full authentication support for MCP and A2A, AI gateway integration, and Azure Policy integration.

## Microsoft Foundry API and SDKs

The [Microsoft Foundry API](/rest/api/aifoundry/) is designed specifically for building agentic applications and provides a consistent contract for working across different model providers. The API is complemented by SDKs to make it easy to integrate AI capabilities into your applications. [SDK Client libraries](how-to/develop/sdk-overview.md) are available for:

- Python
- C#
- JavaScript/TypeScript (preview)
- Java (preview)

The [Microsoft Foundry for VS Code Extension](how-to/develop/get-started-projects-vs-code.md) helps you explore models and develop agents directly in your development environment.

## Foundry portal

The [Microsoft Foundry portal](https://ai.azure.com) is where you manage projects, deploy models, build agents, and monitor your AI assets. To use the current version, make sure the **New Foundry** toggle in the banner is set to on.

:::image type="icon" source="media/version-banner/new-foundry.png" alt-text="Screenshot of New Foundry toggle in the banner.":::

> [!TIP]
> See [Find features in the Foundry portal](how-to/navigate-from-classic.md) if you're used to the Foundry (classic) portal and not sure where to find things now.

### Choosing a project

In the Foundry portal, the project you're working with appears in the upper-left corner of most pages. 
* If you see a long list of projects instead, select a project to begin. This brings you to the **Home** page with the project name in the upper-left corner.
* To switch to another recently used project, select the project name in the upper-left corner, then select the other project. 
* To see all of your Foundry projects, select the project name in the upper-left corner, then select **View all projects**. Select the next project you want to work on.

### Find other resources

The Foundry portal displays only the **default** project for each Foundry resource, not other resources or hub-based projects you might have created in Foundry (classic). If you created multiple projects under the same Foundry resource, you can identify which project is the default by checking the Microsoft Foundry (classic) portal. The default project is marked with (default) next to its name.

To find these other resources,  select the project name in the upper-left corner, then select **View all resources**.  A new browser tab opens the Foundry (classic) portal.  [Switch to Microsoft Foundry (classic) documentation]() to work with these other resources in the Foundry (classic) portal.

### Disable preview features

[!INCLUDE [disable-preview](includes/disable-preview.md)]

## Pricing and billing

Microsoft Foundry is monetized through individual products customers access and consume in the platform, including API and models, complete AI toolchain, and responsible AI and enterprise grade production at scale products. Each product has its own billing model and price. 

The platform is free to use and explore. Pricing occurs at the deployment level. 

Using Foundry also incurs costs associated with the underlying services. To learn more, read [Plan and manage costs for Foundry Tools](./concepts/manage-costs.md).

## Region availability

Foundry is available in most regions where Foundry Tools are available. For more information, see [region support for Microsoft Foundry](reference/region-support.md).

## How to get access

You need an [Azure account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).  Then sign in to [Microsoft Foundry](https://ai.azure.com?cid=learnDocs).

## Related content

- [Quickstart: Get started with Microsoft Foundry](./tutorials/quickstart-create-foundry-resources.md)- [Create a project](./how-to/create-projects.md)
- [Get started with an AI template](how-to/develop/ai-template-get-started.md)
- [What's new in Microsoft Foundry documentation?](whats-new-foundry.md)
