---
manager: nitinme
author: santiagxf
ms.author: fasantia 
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.date: 1/21/2025
ms.topic: include
---

[!INCLUDE [Feature preview](../../../includes/feature-preview.md)]

In this article, you learn how to create the resources required to use Microsoft Foundry Models in your projects.

## Understand the resources

Foundry Models is a capability in Foundry Services (formerly known Azure AI Services). You can create model deployments under the resource to consume their predictions. You can also connect the resource to Azure AI Hubs and Projects in Foundry to create intelligent applications if needed. The following picture shows the high level architecture.

:::image type="content" source="../../media/create-resources/resources-architecture.png" alt-text="A diagram showing the high level architecture of the resources created in the tutorial." lightbox="../../media/create-resources/resources-architecture.png":::

Foundry Services don't require AI projects or AI hubs to operate and you can create them to consume flagship models from your applications. However, additional capabilities are available if you **deploy a Foundry project and hub**, including playground, or agents.

The tutorial helps you create:

> [!div class="checklist"]
> * A Foundry resource.
> * A model deployment for each of the models supported with serverless API deployments.
> * (Optionally) A Foundry project and hub.
> * (Optionally) A connection between the hub and the models in Foundry.

## Prerequisites

To complete this article, you need:

* An Azure subscription. If you're using [GitHub Models](https://docs.github.com/en/github-models/), you can upgrade your experience and create an Azure subscription in the process. Read [Upgrade from GitHub Models to Foundry](../../how-to/quickstart-github-models.md) if that's your case.