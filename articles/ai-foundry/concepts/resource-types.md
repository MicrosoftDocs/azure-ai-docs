---
title: Choose an Azure resource type for AI foundry
titleSuffix: Azure AI Foundry
description: Learn about the supported Azure resource types in Azure AI Foundry portal.
reviewer: deeikele
ms.reviewer: deeikele
author: sdgilley
ms.author: sgilley
ms.date: 10/09/2025
ms.service: azure-ai-foundry
ms.topic: concept-article
ms.custom:
  - build-aifnd
  - build-2025
---

# Choose an Azure resource type for AI foundry

An Azure resource is required to use and manage services in Azure. It defines the scope for configuring, securing, and monitoring the tools or capabilities you want to use—like AI models, agents, or storage.

Azure AI Foundry portal and SDK clients support multiple distinct Azure resource types, each designed to serve different development and operational needs. This article explains which use case requires which type.

## Resource Types supported with AI Foundry Portal and SDK clients

* **Azure AI Foundry** – The primary resource type for designing, deploying, and managing generative AI applications and agents. It provides access to the superset of Azure AI capabilities. This includes agent service, models sold by Microsoft and its partners, evaluations, AI Services and Azure OpenAI service capabilities. Azure AI Foundry is the recommended resource type for most applications built in Azure AI Foundry. 
 
  Get started by [creating a first AI Foundry resource](../../ai-services/multi-service-resource.md?context=/azure/ai-foundry/context/context).

  :::image type="content" source="../media/concepts/foundry-resource.png" alt-text="Screenshot shows how AI Foundry resource type provided access to the superset of Azure AI capabilities including agent service, a wide selection of models, and Azure OpenAI capabilities.":::

* **Azure AI Search** – A resource used to index and retrieve data for grounding AI applications. It can be [connected](../how-to/connections-add.md) to Azure AI Foundry agents to enable retrieval-augmented generation (RAG) and semantic search experiences.

* **Azure OpenAI** – A specialized resource type that provides access to OpenAI models and APIs only. For most use cases, it's recommended to use the Azure AI Foundry resource, which offers backwards compatibility with all Azure OpenAI APIs.

  If your IT security team hasn't enabled the superset of Foundry capabilities in your environment, then the standalone Azure OpenAI resource may still be required for you.

  [An upgrade option from Azure OpenAI to AI Foundry](../how-to/upgrade-azure-openai.md) is available to access all Foundry capabilities and models while keeping your existing Azure OpenAI API endpoint, state of work, and security configurations.

* **Azure AI Hub** - In June 2025, we started to move most of Hub's capabilities under "Azure AI Foundry" resource type. This change brings agents, models, and their tools together for development, management and governance, under a dedicated Azure resource type for AI Foundry.

  New features will primarily land on Azure AI Foundry resource type. To learn more, see [migrate from hub-based to Foundry projects](../how-to/migrate-project.md). [Select use cases](../what-is-azure-ai-foundry.md#which-type-of-project-do-i-need), including open source model deployments, currently still require a hub resource.

## References

* [Azure AI Foundry architecture](architecture.md)
* [What is Azure Resource Manager?](/azure/azure-resource-manager/management/overview)
* [Create a first AI Foundry resource](../../ai-services/multi-service-resource.md?context=/azure/ai-foundry/context/context)
* [Create AI Foundry with advanced options](../how-to/create-resource-template.md)
* [Create a first AI Hub](../how-to/create-azure-ai-resource.md)
* [Create AI Hub with advanced options](../how-to/create-azure-ai-hub-template.md)
