---
title: Choose an Azure resource type for AI foundry
titleSuffix: Microsoft Foundry
description: Learn about the supported Azure resource types in Microsoft Foundry portal.
reviewer: deeikele
ms.reviewer: deeikele
author: sdgilley
ms.author: sgilley
ms.date: 10/06/2025
ms.service: azure-ai-foundry
ms.topic: concept-article
ai-usage: ai-assisted
monikerRange: 'foundry-classic || foundry'
ms.custom:
  - build-aifnd
  - build-2025
---

# Choose an Azure resource type for AI foundry

[!INCLUDE [version-banner](../includes/version-banner.md)]

An Azure resource defines the scope for configuring, securing, and monitoring AI capabilities (such as models, agents, and storage) in Azure. Microsoft Foundry portal and SDK clients support multiple resource types, each optimized for a specific development or operational scenario.
<!-- Condensed introductory marketing-style content into a single concise definition with clear scope, per agent feedback. -->

## Resource Types supported with Foundry portal and SDK clients

* **Foundry** – An Azure resource that scopes design, deployment, governance, and runtime access for generative AI applications and agents, including agent service, Microsoft‑ and partner‑provided models, evaluations, Foundry Tools, and Azure OpenAI–compatible APIs. It is the default resource type for projects built in the Foundry portal.
<!-- Replaced marketing-heavy description with a concise, scoped definition that focuses on what the resource controls and where it applies, per agent feedback. -->
 
  Get started by [creating a first Foundry resource](../../ai-services/multi-service-resource.md?toc=/azure/ai-foundry/toc.json&bc=/azure/ai-foundry/breadcrumb/toc.json).

  :::image type="content" source="../media/concepts/foundry-resource.png" alt-text="Screenshot shows how Foundry resource type provided access to the superset of Azure AI capabilities including agent service, a wide selection of models, and Azure OpenAI capabilities.":::

* **Azure AI Search** – A resource used to index and retrieve data for grounding AI applications. It can be [connected](../how-to/connections-add.md) to Foundry agents to enable retrieval-augmented generation (RAG) and semantic search experiences.

* **Azure OpenAI** – A specialized resource type that provides access to OpenAI models and APIs only. For most use cases, it's recommended to use the Foundry resource, which offers backwards compatibility with all Azure OpenAI APIs.

  > [!NOTE]
  > If your IT security team hasn't enabled the superset of Foundry capabilities in your environment, then the standalone Azure OpenAI resource may still be required for you.

  [An upgrade option from Azure OpenAI to Foundry](../how-to/upgrade-azure-openai.md) is available to access all Foundry capabilities and models while keeping your existing Azure OpenAI API endpoint, state of work, and security configurations.

::: moniker range="foundry-classic"

* **Azure AI Hub** - In June 2025, we started to move most of Hub's capabilities under "Foundry" resource type. This change brings agents, models, and their tools together for development, management and governance, under a dedicated Azure resource type for Foundry.

  New features will primarily land on Foundry resource type. To learn more, see [migrate from hub-based to Foundry projects](../how-to/migrate-project.md). [Select use cases](../what-is-azure-ai-foundry.md#which-type-of-project-do-i-need), including open source model deployments, currently still require a hub resource.

::: moniker-end

## References

* [Foundry architecture](architecture.md)
* [What is Azure Resource Manager?](/azure/azure-resource-manager/management/overview)
* [Create a first Foundry resource](../../ai-services/multi-service-resource.md?toc=/azure/ai-foundry/toc.json&bc=/azure/ai-foundry/breadcrumb/toc.json)
* [Create Foundry with advanced options](../how-to/create-resource-template.md)

::: moniker range="foundry-classic"

* [Create a first AI Hub](../how-to/create-azure-ai-resource.md)
* [Create AI Hub with advanced options](../how-to/create-azure-ai-hub-template.md)

::: moniker-end