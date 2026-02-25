---
title: "What is Microsoft Foundry? (temp)"
description: "Microsoft Foundry is a trusted platform that empowers developers to drive innovation and shape the future with AI in a safe, secure, and responsible way. (temp)"
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
keywords:
  - Foundry Tools
  - cognitive
# customer intent: As a developer, I want to understand what Microsoft Foundry is so that I can use it to build AI applications.
---

# What is Microsoft Foundry? (temp)

**Microsoft Foundry** is a unified Azure platform-as-a-service offering for enterprise AI operations, model builders, and application development. This foundation combines production-grade infrastructure with friendly interfaces, enabling developers to focus on building applications rather than managing infrastructure.

Microsoft Foundry unifies agents, models, and tools under a single management grouping with built-in enterprise-readiness capabilities including tracing, monitoring, evaluations, and customizable enterprise setup configurations. The platform provides streamlined management through unified role-based access control (RBAC), networking, and policies under one Azure resource provider namespace.

> [!TIP]
> Azure AI Foundry is now Microsoft Foundry. Screenshots appearing throughout this documentation are in the process of being updated.
>

[!INCLUDE [foundry-portals](includes/foundry-portals.md)]

## Microsoft Foundry (new)

**Microsoft Foundry (new)** delivers a modernized experience with powerful enhancements designed for flexibility and scale:

* **[Multi-Agent Orchestration and Workflows](agents/concepts/workflow.md)** – Build advanced automation using SDKs for C# and Python that enable collaborative agent behavior and complex workflow execution.
* **[Expanded Integration Options](agents/how-to/publish-copilot.md)** – Publish agents to Microsoft 365, Teams, and BizChat, plus leverage containerized deployments for greater portability.
* **[Expanded Tool Access](agents/concepts/tool-catalog.md)** – Access the Foundry tool catalog (preview) with a public tool catalog and your own private catalogs, connecting over 1,400 tools in Microsoft Foundry.
* **[Enhanced Memory Capabilities](agents/concepts/what-is-memory.md)** – Use memory to help your agent retain and recall contextual information across interactions. Memory maintains continuity, adapts to user needs, and delivers tailored experiences without requiring repeated input.
* **[Knowledge Integration](agents/concepts/what-is-foundry-iq.md)** – Connect your agent to a Foundry IQ knowledge base to ground responses in enterprise or web content. This integration provides reliable, citation-backed answers for multi-turn conversations.
* **[Real-Time Observability](observability/how-to/how-to-monitor-agents-dashboard.md#set-up-continuous-evaluation-python-sdk)** – Monitor performance and governance using built-in metrics and model tracking tools.
* **Enhanced Enterprise Support** – Use open protocols in Foundry Agent Service with full authentication support in MCP and A2A tool, AI gateway integration, and Azure Policy integration.
* **Centralized AI asset management** – Observe, optimize, and manage 100% of your AI assets (agents, models, tools) in one place, the **Operate** section. Register agents from other clouds, get alerts when an agent or model requires your attention, and effectively manage your AI fleet health as that fleet scales.
* **Optimized Developer Experience** – Experience faster load times and dynamic prefetching for smooth development and deployment.
* **Streamlined Navigation** – Navigate efficiently with a redesigned interface that places key controls where you need them, improving workflow efficiency.

## Choosing a project

In the Foundry (new) portal, the project you're working with appears in the upper-left corner of most pages. 
* If you see a long list of projects instead, select a project to begin. This brings you to the **Home** page with the project name in the upper-left corner.
* To switch to another recently used project, select the project name in the upper-left corner, then select the other project. 
* To see all of your Foundry projects, select the project name in the upper-left corner, then select **View all projects**. Select the next project you want to work on.

## Find other resources

The Foundry (new) portal displays only the **default** project for each Foundry resource, not other resources or hub-based projects you might have created in Foundry (classic). If you created multiple projects under the same Foundry resource, you can identify which project is the default by checking the Microsoft Foundry (classic) portal. The default project is marked with (default) next to its name.

To find these other resources,  select the project name in the upper-left corner, then select **View all resources**.  A new browser tab opens the Foundry (classic) portal.  [Switch to Microsoft Foundry (classic) documentation]() to work with these other resources in the Foundry (classic) portal.

## Disable preview features

Use your organization controls to limit production environments to general availability supported capabilities, and validate current feature status before rollout decisions. For role-based control guidance, see [Disable preview features by using role-based access control](./concepts/disable-preview-features-with-rbac.md). For tag-based suppression in the Foundry portal, see [Hide preview features with Azure tags](./how-to/disable-preview-features.md).

## Microsoft Foundry API and SDKs

The [Microsoft Foundry API](/rest/api/aifoundry/) is designed specifically for building agentic applications and provides a consistent contract for working across different model providers. The API is complemented by SDKs to make it easy to integrate AI capabilities into your applications. [SDK Client libraries](how-to/develop/sdk-overview.md) are available for:

- Python
- C#
- JavaScript/TypeScript (preview)
- Java (preview)

The [Microsoft Foundry for VS Code Extension](how-to/develop/get-started-projects-vs-code.md) helps you explore models and develop agents directly in your development environment.

## Pricing and billing

Microsoft Foundry is monetized through individual products customers access and consume in the platform, including API and models, complete AI toolchain, and responsible AI and enterprise grade production at scale products. Each product has its own billing model and price. 

The platform is free to use and explore. Pricing occurs at the deployment level. 

Using Foundry also incurs costs associated with the underlying services. To learn more, read [Plan and manage costs for Foundry Tools](./concepts/manage-costs.md).

## Region availability

Foundry is available in most regions where Foundry Tools are available. For more information, see [region support for Microsoft Foundry](reference/region-support.md).

## How to get access

You need an [Azure account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).  Then sign in to [Microsoft Foundry](https://ai.azure.com?cid=learnDocs) and turn on the **Try the new Foundry** toggle.

## Related content

- [Quickstart: Get started with Microsoft Foundry](./tutorials/quickstart-create-foundry-resources.md)- [Create a project](./how-to/create-projects.md)
- [Get started with an AI template](how-to/develop/ai-template-get-started.md)
- [What's new in Microsoft Foundry documentation?](whats-new-foundry.md)
