---
title: "Microsoft Foundry architecture (classic)"
description: "Learn about the architecture of Microsoft Foundry. (classic)"
ms.service: azure-ai-foundry
ms.custom:
  - classic-and-new
  - build-2024
  - ignite-2024
ms.topic: concept-article
ms.date: 01/06/2026
ms.reviewer: deeikele
ms.author: sgilley
author: sdgilley
ai-usage: ai-assisted

ROBOTS: NOINDEX, NOFOLLOW
---

# Microsoft Foundry architecture (classic) 

**Currently viewing:** :::image type="icon" source="../../foundry/media/yes-icon.svg" border="false"::: **Foundry (classic) portal version** - [Switch to version for the new Foundry portal](../../foundry/concepts/architecture.md)

[!INCLUDE [architecture 1](../../foundry/includes/concepts-architecture-1.md)]

## Azure AI resource types and providers

Within the Azure AI product family, you can use these [Azure resource providers](/azure/azure-resource-manager/management/resource-providers-and-types) that support user needs at different layers in the stack.

| Resource provider | Purpose | Supports resource type kinds |
| --- | --- | --- |
| Microsoft.CognitiveServices | Supports Agentic and GenAI application development composing and customizing prebuilt models. | Foundry; Azure OpenAI service; Azure Speech; Azure Vision | 
| Microsoft.Search | Support knowledge retrieval over your data | Azure AI Search | 
| Microsoft.MachineLearningServices | Train, deploy, and operate custom and open source machine learning models | Azure AI Hub (and its projects); Azure Machine Learning Workspace | 

For many scenarios, the Foundry resource is the recommended starting point. Foundry resources share the Microsoft.CognitiveServices provider namespace with services such as Azure OpenAI, Azure Speech, Azure Vision, and Azure Language. This shared provider namespace helps align management APIs, access control patterns, networking, and policy behavior across related AI resources.

[!INCLUDE [Resource provider kinds](../../foundry/includes/resource-provider-kinds.md)]

Resource types under the same provider namespaces share the same management APIs, and use similar [Azure Role Based Access Control](/azure/role-based-access-control/overview) actions, networking configurations, and aliases for Azure Policy configuration. If you're upgrading from Azure OpenAI to Foundry, your existing custom Azure policies and Azure Role Based Access Control actions continue to apply.

[!INCLUDE [architecture 2](../../foundry/includes/concepts-architecture-2.md)]

## Computing infrastructure

Foundry uses a flexible compute architecture to support different [model access](../concepts/foundry-models-overview.md) and workload execution scenarios. 

- **Model Hosting Architecture**: Foundry models access is provided in different ways:
  
  - [Standard deployment in Foundry resources](deployments-overview.md#standard-deployment-in-foundry-resources)
  - [Deployment to serverless API endpoints in Azure AI Hub resources](deployments-overview.md#serverless-api-endpoint)
  - [Deployment to managed computes in Azure AI Hub resources](deployments-overview.md#managed-compute)

  For an overview of data, privacy, and security considerations with these deployment options, see [Data, privacy, and security for use of models](../how-to/concept-data-privacy.md).

- **Workload Execution:** Agents, Evaluations, and Batch jobs run as managed container compute, fully managed by Microsoft. 

- **Networking Integration:** For enhanced security and compliance when your Agents connect with external systems, [container injection](../agents/how-to/virtual-networks.md) allows the platform network to host APIs and inject a subnet into your network. This setup enables local communication of your Azure resources within the same virtual network. 

  If you require end-to-end network isolation, review current limitations before rollout. In the new Foundry portal experience, end-to-end isolation scenarios aren't fully supported. Use the classic experience, SDK, or CLI guidance for network-isolated deployments. For details, see [How to configure a private link for Foundry](../how-to/configure-private-link.md).

[!INCLUDE [architecture 3](../../foundry/includes/concepts-architecture-3.md)]
