---
title: "What is Microsoft Foundry?"
description: "Microsoft Foundry is a trusted platform that empowers developers to drive innovation and shape the future with AI in a safe, secure, and responsible way."
author: sdgilley
ms.author: sgilley
ms.reviewer: sgilley
ms.date: 06/23/2026
ms.service: microsoft-foundry
ms.subservice: foundry-platform
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

Microsoft Foundry unifies agents, models, and tools under a single management grouping with built-in enterprise-readiness capabilities including tracing, monitoring, evaluations, and customizable enterprise setup configurations. The platform provides streamlined management through unified role-based access control (RBAC), networking, and policies under one Azure resource provider namespace.

> [!TIP]
> * Coming from Azure OpenAI? [Upgrade your Azure OpenAI resource to a Foundry resource](./how-to/upgrade-azure-openai.md) while preserving your endpoint, API keys, and existing state. 
> * Using hub-based projects? Hub-based projects are accessible in the [Foundry (classic) portal](../foundry-classic/what-is-foundry.md). New investments are focused on Foundry projects in the new portal.

## Get started

Build your first agent in minutes, or open the portal to explore models and tools.

> [!div class="nextstepaction"]
> [Build with models and agents](./quickstarts/get-started-code.md)

[Open the Foundry portal](https://ai.azure.com) | [Get an Azure account](https://azure.microsoft.com/pricing/purchase-options/azure-account)

## What you can build

| Capability | Description |
|---|---|
| **Agents** | Build declarative [prompt agents](./agents/quickstarts/prompt-agent.md) in the portal or SDK, or deploy [hosted agents](./agents/quickstarts/quickstart-hosted-agent.md) that run your own code. Learn more in [Foundry Agent Service](./agents/overview.md). |
| **Models** | Access more than 1,900 models from Microsoft, OpenAI, Anthropic, Meta, and others. Browse the [Foundry Models catalog](./concepts/foundry-models-overview.md). |
| **Tools and knowledge** | Extend agents with built-in tools, memory, and retrieval from the [tool catalog](./agents/concepts/tool-catalog.md). |

## Enterprise-ready platform

Foundry brings production capabilities to every project:

- **Observability:** Trace, monitor, and evaluate agents and models with built-in dashboards. See [Observability](./concepts/observability.md).
- **Governance and security:** Apply Microsoft Entra identity, role-based access control, content filters, network isolation, and Azure Policy. See the [Foundry control plane](./control-plane/overview.md).
- **One management plane:** Manage agents, models, and tools as a single Azure resource with unified access control, networking, and policies.

[!INCLUDE [previous-current](includes/previous-current.md)]

## Related content

- [What is Foundry Agent Service?](./agents/overview.md)
- [Foundry Models](./concepts/foundry-models-overview.md)
- [What's new in Microsoft Foundry](./whats-new-foundry.md)
- [Microsoft Foundry portal general availability overview](concepts/general-availability.md)
- [Upgrade your Azure OpenAI resource to a Foundry resource](./how-to/upgrade-azure-openai.md)
- [Find hub-based projects in the Foundry (classic) portal](../foundry-classic/what-is-foundry.md)
