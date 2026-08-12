---
title: "Model router for Microsoft Foundry concepts"
description: "Learn about the model router feature in Azure OpenAI in Microsoft Foundry Models."
author: PatrickFarley
ms.author: pafarley
manager: mcleans
ms.date: 08/12/2026
ms.service: microsoft-foundry
ms.subservice: foundry-model-inference
ms.topic: concept-article
ms.custom:
  - classic-and-new
  - build-2025
  - dev-focus
  - doc-kit-assisted
ai-usage: ai-assisted
---

# Model router for Microsoft Foundry

Model router is a trained language model that intelligently routes your prompts in real time to the most suitable large language model (LLM). You deploy model router like any other Foundry model. Thus, it delivers high performance while saving on costs, reducing latencies, and increasing responsiveness, while maintaining comparable quality, all packaged as a single model deployment.

> [!VIDEO https://learn-video.azurefd.net/vod/player?id=32338ec4-89bf-4438-8cc3-2e3f01e88533]

To try model router quickly, follow [How to use model router](../how-to/model-router.md). After you deploy model router, send a request to the deployment. Model router selects an underlying model for each request based on your routing settings. For a deep dive into the routing pipeline, training, and decision logic, see [How model router works](model-router-how-it-works.md).

> [!NOTE]
> You do not need to separately deploy the supported LLMs for use with model router, with the exception of the Claude models. To use model router with your Claude models, first deploy them from the model catalog. The deployments are invoked by model router if they're selected for routing.


[!INCLUDE [model-router 1](../includes/concepts-model-router-1.md)]

## Supported regions

Model router supports Global Standard and Data Zone Standard deployments in all of the following regions.

| Region | Global Standard | Data Zone Standard |
| :--- | :---: | :---: |
| Australia East | Supported | Supported |
| Brazil South | Supported | Supported |
| Canada East | Supported | Supported |
| Central US | Supported | Supported |
| East US | Supported | Supported |
| East US 2 | Supported | Supported |
| France Central | Supported | Supported |
| Germany West Central | Supported | Supported |
| Italy North | Supported | Supported |
| Japan East | Supported | Supported |
| Japan West | Supported | Supported |
| Korea Central | Supported | Supported |
| North Central US | Supported | Supported |
| Poland Central | Supported | Supported |
| South Africa North | Supported | Supported |
| South Central US | Supported | Supported |
| South India | Supported | Supported |
| Southeast Asia | Supported | Supported |
| Spain Central | Supported | Supported |
| Sweden Central | Supported | Supported |
| Switzerland North | Supported | Supported |
| Switzerland West | Supported | Supported |
| UK South | Supported | Supported |
| UK West | Supported | Supported |
| West Central US | Supported | Supported |
| West Europe | Supported | Supported |
| West US | Supported | Supported |
| West US 3 | Supported | Supported |

> [!NOTE]
> The models available to model router in each region are limited to the supported underlying models available in that region. This regional expansion lets you use model router to route requests across the available supported models in each listed region.

## Routing mode

With the latest version, if you choose custom deployment, you can select the **routing mode** to optimize for quality or cost while maintaining a baseline level of performance. Setting a routing mode is optional, and if you don’t set one, your deployment defaults to the Balanced mode.

Available routing modes:

| Mode | Description |
| ------ | ----------- |
| Balanced (default) | Considers both cost and quality dynamically. Perfect for general-purpose scenarios |
| Quality | Prioritizes for maximum accuracy. Best for complex reasoning or critical outputs |
| Cost | Prioritizes for more cost savings. Ideal for high-volume, budget-sensitive workloads |

## Govern model router deployments

If your organization uses Azure Policy to control which models can be deployed, model router honors the same built-in Foundry model deployment policy that governs standard model deployments. The policy applies to the model subset that a developer can include in a model router deployment, and it's enforced consistently across the Foundry portal, REST API, Azure CLI, and ARM templates. For the IT admin assignment steps and the developer experience, see [Govern model router deployments with Azure Policy](../../how-to/model-router-policy.md).

[!INCLUDE [model-router 2](../includes/concepts-model-router-2.md)]
