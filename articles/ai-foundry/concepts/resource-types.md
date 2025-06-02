---
title: Choose an Azure resource type for AI foundry
titleSuffix: Azure AI Foundry
description: Learn about the supported Azure resource types in Azure AI Foundry portal.
author: deeikele
ms.author: deeikele
manager: scottpolly
reviewer: larryfr
ms.reviewer: larryfr
ms.date: 05/18/2025
ms.service: azure-ai-foundry
ms.topic: conceptual
ms.custom:
  - build-aifnd
---

# Choose an Azure resource type for AI foundry

An Azure resource is required to use and manage services in Azure. It defines the scope for configuring, securing, and monitoring the tools or capabilities you want to use—like AI models, agents, or storage.

AI Foundry Portal and SDK clients support multiple distinct Azure resource types, each designed to serve different development and operational needs. This article explains which use case requires which type.

## Resource Types supported with AI Foundry

* **Azure AI Foundry** – The primary resource type for designing, deploying, and managing generative AI applications and agents. It provides access to agent service, models that are hosted using a serverless hosting model, evaluations, and Azure OpenAI service. This is the recommended resource type for most applications built in Azure AI Foundry. 
 
  Get started by [creating a first AI Foundry resource](../../ai-services/multi-service-resource.md?context=/azure/ai-foundry/context/context).

* **Azure AI Hub** – Use this resource type in combination with Azure AI Foundry to additionally access open-source model hosting and fine-tuning capabilities, as well as Azure Machine Learning capabilities. When you create an AI Hub, an Azure AI Foundry resource is automatically provisioned. Hub resources can be used in both AI Foundry Portal and Machine Learning Studio.

* **Azure AI Search** – A resource used to index and retrieve data for grounding AI applications. It can be [connected](../how-to/connections-add.md) to Azure AI Foundry agents to enable retrieval-augmented generation (RAG) and semantic search experiences.

* **Azure OpenAI** – A specialized resource type that provides access to OpenAI models such as GPT-4 and GPT-4o. It offers a subset of the capabilities available in Azure AI Foundry and provides solely access to Azure OpenAI APIs.

## References

* [What is Azure Resource Manager?](/azure/azure-resource-manager/management/overview)
* [Create a first AI Foundry resource](../../ai-services/multi-service-resource.md?context=/azure/ai-foundry/context/context)
* [Create AI Foundry with advanced options](../how-to/create-resource-template.md)
* [Create a first AI Hub](../how-to/create-azure-ai-resource.md)
* [Create AI Hub with advanced options](../how-to/create-azure-ai-hub-template.md)
