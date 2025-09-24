---
title: Choose an Azure resource type for AI foundry
titleSuffix: Azure AI Foundry
description: Learn about the supported Azure resource types in Azure AI Foundry portal.
reviewer: deeikele
ms.reviewer: deeikele
author: sdgilley
ms.author: sgilley
ms.date: 07/22/2025
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

* **Azure AI Foundry** – The primary resource type for designing, deploying, and managing generative AI applications and agents. It provides access to the supserset of Azure AI capabilities including agent service, models that are hosted using a serverless hosting model, evaluations, AI Services such as Speech and Language service and Azure OpenAI service capablitities. Azure AI Foundry is the recommended resource type for most applications built in Azure AI Foundry. 
 
  Get started by [creating a first AI Foundry resource](../../ai-services/multi-service-resource.md?context=/azure/ai-foundry/context/context).

  :::image type="content" source="../media/concepts/foundry-resource.png" alt-text="Screenshot shows how AI Foundry resource type provided access to the supser of Azure AI capabilities including agent service, a wide selection of models, and Azure OpenAI capabilities.":::

* **Azure AI Search** – A resource used to index and retrieve data for grounding AI applications. It can be [connected](../how-to/connections-add.md) to Azure AI Foundry agents to enable retrieval-augmented generation (RAG) and semantic search experiences.

* **Azure OpenAI** – A specialized resource type that provides access to OpenAI models such as GPT-4 and GPT-4o. It offers a subset of the capabilities available in Azure AI Foundry and provides solely access to Azure OpenAI models and APIs. [Upgrade from Azure OpenAI to Azure AI Foundry](../how-to/upgrade-azure-openai.md) to gain access to more capabilities while keeping the existing Azure OpenAI API endpoint, state of work, and security configurations.

* **Azure AI Hub** – Use this resource type in combination with your Azure AI Foundry resource to additionally access open-source model hosting and customization capabilities via the Azure Machine Learning APIs. 

  In June 2025, we started to move most of Hub's capabilities under "Azure AI Foundry" resource type. This change brings the management of agents, models and tools together for management and governance, and a more cohesive developer experience, under a dedicated Azure resource type for AI Foundry. New features will only release on Azure AI Foundry resource. To learn more, see [migrate from hub-based to Foundry projects](../how-to/migrate-project?tabs=azure-ai-foundry).

## References

* [Azure AI Foundy architecture](architecture.md)
* [What is Azure Resource Manager?](/azure/azure-resource-manager/management/overview)
* [Create a first AI Foundry resource](../../ai-services/multi-service-resource.md?context=/azure/ai-foundry/context/context)
* [Create AI Foundry with advanced options](../how-to/create-resource-template.md)
* [Create a first AI Hub](../how-to/create-azure-ai-resource.md)
* [Create AI Hub with advanced options](../how-to/create-azure-ai-hub-template.md)
