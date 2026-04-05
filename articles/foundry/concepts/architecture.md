---
title: "Microsoft Foundry architecture"
description: "Learn about the architecture of Microsoft Foundry."
ms.service: azure-ai-foundry
ms.custom:
  - classic-and-new
  - build-2024
  - ignite-2024
  - doc-kit-assisted
ms.topic: concept-article
ms.date: 01/06/2026
ms.reviewer: deeikele
ms.author: sgilley
author: sdgilley
ai-usage: ai-assisted
---

# Microsoft Foundry architecture

[!INCLUDE [architecture 1](../includes/concepts-architecture-1.md)]

## Azure AI resource types and providers

Within the Azure AI product family, you can use these [Azure resource providers](/azure/azure-resource-manager/management/resource-providers-and-types) that support user needs at different layers in the stack.

| Resource provider | Purpose | Supports resource type kinds |
| --- | --- | --- |
| Microsoft.CognitiveServices | Supports Agentic and GenAI application development composing and customizing prebuilt models. | Foundry; Azure OpenAI service; Azure Speech; Azure Vision | 
| Microsoft.Search | Support knowledge retrieval over your data | Azure AI Search | 

For many scenarios, the Foundry resource is the recommended starting point. Foundry resources share the Microsoft.CognitiveServices provider namespace with services such as Azure OpenAI, Azure Speech, Azure Vision, and Azure Language. This shared provider namespace helps align management APIs, access control patterns, networking, and policy behavior across related AI resources.

[!INCLUDE [Resource provider kinds](../includes/resource-provider-kinds.md)]

Resource types under the same provider namespaces share the same management APIs, and use similar [Azure Role Based Access Control](/azure/role-based-access-control/overview) actions, networking configurations, and aliases for Azure Policy configuration. If you're upgrading from Azure OpenAI to Foundry, your existing custom Azure policies and Azure Role Based Access Control actions continue to apply.

[!INCLUDE [architecture 2](../includes/concepts-architecture-2.md)]

## Computing infrastructure

- **Model Hosting Architecture** is provided by standard deployment in Foundry resources.   

- **Workload Execution:** Agents, Evaluations, and Batch jobs run as managed container compute, fully managed by Microsoft. 

- **Networking Integration:** For enhanced security and compliance when your Agents connect with external systems, [container injection](../agents/how-to/virtual-networks.md) allows the platform network to host APIs and inject a subnet into your network. This setup enables local communication of your Azure resources within the same virtual network. 

  If you require end-to-end network isolation, review current limitations before rollout. In the new Foundry portal experience, end-to-end isolation scenarios aren't fully supported. Use the classic experience, SDK, or CLI guidance for network-isolated deployments. For details, see [How to configure a private link for Foundry](../how-to/configure-private-link.md).

[!INCLUDE [architecture 3](../includes/concepts-architecture-3.md)]
