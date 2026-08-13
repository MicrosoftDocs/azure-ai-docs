---
title: "Model router for Microsoft Foundry concepts (classic)"
description: "Learn about the model router feature in Azure OpenAI in Microsoft Foundry Models. (classic)"
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

ROBOTS: NOINDEX, NOFOLLOW
---

# Model router for Microsoft Foundry (classic)

**Currently viewing:** :::image type="icon" source="../../../foundry/media/yes-icon.svg" border="false"::: **Foundry (classic) portal version** - [Switch to version for the new Foundry portal](../../../foundry/openai/concepts/model-router.md)

Model router is a trained language model that intelligently routes your prompts in real time to the most suitable large language model (LLM). You deploy model router like any other Foundry model. Thus, it delivers high performance while saving on costs, reducing latencies, and increasing responsiveness, while maintaining comparable quality, all packaged as a single model deployment.

> [!NOTE]
> You do not need to separately deploy the supported LLMs for use with model router, with the exception of the Claude models. To use model router with your Claude models, first deploy them from the model catalog. The deployments are invoked by model router if they're selected for routing.

To try model router quickly, follow [How to use model router](../how-to/model-router.md). After you deploy model router, send a request to the deployment. Model router selects an underlying model for each request based on your routing settings.

> [!TIP]
> The [Microsoft Foundry (new)](../../../foundry/what-is-foundry.md) portal offers enhanced configuration options for model router. [Switch to the Microsoft Foundry (new) documentation](../../../foundry/openai/concepts/model-router.md) to see the latest features.

[!INCLUDE [model-router 1](../../../foundry/openai/includes/concepts-model-router-1.md)]

## Supported regions

Model router supports Global Standard deployments in all of the following regions. A check mark (✅) indicates that the deployment type is available. A hyphen (-) indicates that it's not available.

| Region | Global Standard | Data Zone Standard |
| :--- | :---: | :---: |
| Australia East | ✅ | ✅ |
| Brazil South | ✅ | - |
| Canada East | ✅ | - |
| Central US | ✅ | ✅ |
| East US | ✅ | ✅ |
| East US 2 | ✅ | ✅ |
| France Central | ✅ | ✅ |
| Germany West Central | ✅ | ✅ |
| Italy North | ✅ | ✅ |
| Japan East | ✅ | ✅ |
| Japan West | ✅ | ✅ |
| Korea Central | ✅ | ✅ |
| North Central US | ✅ | ✅ |
| Poland Central | ✅ | ✅ |
| South Africa North | ✅ | - |
| South Central US | ✅ | ✅ |
| South India | ✅ | ✅ |
| Southeast Asia | ✅ | ✅ |
| Spain Central | ✅ | ✅ |
| Sweden Central | ✅ | ✅ |
| Switzerland North | ✅ | ✅ |
| Switzerland West | ✅ | - |
| UK South | ✅ | - |
| UK West | ✅ | - |
| West Central US | ✅ | - |
| West Europe | ✅ | ✅ |
| West US | ✅ | ✅ |
| West US 3 | ✅ | ✅ |

> [!NOTE]
> The models available to model router in each region are limited to the supported underlying models available in that region. This regional expansion lets you use model router to route requests across the available supported models in each listed region.

## Routing mode

With the latest version, if you choose custom deployment, you can select the **routing mode** to optimize for quality or cost while maintaining a baseline level of performance. Setting a routing mode is optional, and if you don't set one, your deployment defaults to the Balanced mode.

Available routing modes:

| Mode | Description |
| ------ | ----------- |
| Balanced (default) | Considers both cost and quality dynamically. Perfect for general-purpose scenarios |
| Quality | Prioritizes for maximum accuracy. Best for complex reasoning or critical outputs |
| Cost | Prioritizes for more cost savings. Ideal for high-volume, budget-sensitive workloads |

[!INCLUDE [model-router 2](../../../foundry/openai/includes/concepts-model-router-2.md)]