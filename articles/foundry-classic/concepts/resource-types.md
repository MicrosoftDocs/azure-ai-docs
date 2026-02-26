---
title: Choose an Azure resource type for Foundry
titleSuffix: Microsoft Foundry
description: Learn about the supported Azure resource types in Microsoft Foundry portal.
reviewer: deeikele
ms.reviewer: deeikele
author: sdgilley
ms.author: sgilley
ms.date: 01/23/2026
ms.service: azure-ai-foundry
ms.topic: concept-article
ai-usage: ai-assisted
ms.custom:
  - build-aifnd
  - build-2025
  - dev-focus
---

# Choose an Azure resource type for Foundry

[!INCLUDE [classic-banner](../includes/classic-banner.md)]

Microsoft Foundry portal and SDK clients support multiple Azure resource types, each designed for different development and operational needs. This article helps you choose the right resource type for your AI development scenario.

## Resource types supported with Foundry portal and SDK clients

* **Foundry** – An Azure resource that scopes design, deployment, governance, and runtime access for generative AI applications and agents, including agent service, Microsoft‑ and partner‑provided models, evaluations, Foundry Tools, and Azure OpenAI–compatible APIs. It is the default resource type for projects built in the Foundry portal.
 
  [Create your first Foundry resource](../../ai-services/multi-service-resource.md?toc=/azure/ai-foundry/toc.json&bc=/azure/ai-foundry/breadcrumb/toc.json).

  :::image type="content" source="../media/concepts/foundry-resource.png" alt-text="Screenshot shows how Foundry resource type provided access to the superset of Azure AI capabilities including agent service, a wide selection of models, and Azure OpenAI capabilities.":::

* **Azure AI Search** – A resource you use to index and retrieve data for grounding AI applications. You can [connect](../how-to/connections-add.md) it to Foundry agents to enable retrieval-augmented generation (RAG) and semantic search experiences.

* **Azure OpenAI** – A specialized resource type that provides access to OpenAI models and APIs only. For most use cases, use the Foundry resource, which offers backward compatibility with all Azure OpenAI APIs.

  > [!NOTE]
  > If your IT security team doesn't enable the superset of Foundry capabilities in your environment, you might need the standalone Azure OpenAI resource.

  [An upgrade option from Azure OpenAI to Foundry](../how-to/upgrade-azure-openai.md) is available to access all Foundry capabilities and models while keeping your existing Azure OpenAI API endpoint, state of work, and security configurations.

* **Azure AI Hub** - In June 2025, Microsoft started to move most of Hub's capabilities under "Foundry" resource type. This change brings agents, models, and their tools together for development, management and governance, under a dedicated Azure resource type for Foundry.

  New features primarily land on Foundry resource type. To learn more, see [migrate from hub-based to Foundry projects](../how-to/migrate-project.md). [Select use cases](../what-is-foundry.md#which-type-of-project-do-i-need), including open source model deployments, currently still require a hub resource.

## Related content

* [Foundry architecture](architecture.md)
* [What is Azure Resource Manager?](/azure/azure-resource-manager/management/overview)
* [Create a first Foundry resource](../../ai-services/multi-service-resource.md?toc=/azure/ai-foundry/toc.json&bc=/azure/ai-foundry/breadcrumb/toc.json)
* [Create Foundry with advanced options](../how-to/create-resource-template.md)
* [Create a first AI Hub](../how-to/create-azure-ai-resource.md)
* [Create AI Hub with advanced options](../how-to/create-azure-ai-hub-template.md)

