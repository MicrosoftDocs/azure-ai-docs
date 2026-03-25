---
title: "Model router for Microsoft Foundry concepts (classic)"
description: "Learn about the model router feature in Azure OpenAI in Microsoft Foundry Models. (classic)"
author: PatrickFarley
ms.author: pafarley
manager: nitinme
ms.date: 03/18/2026
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
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
> The [Microsoft Foundry (new)](../../what-is-foundry.md) portal offers enhanced configuration options for model router. [Switch to the Microsoft Foundry (new) documentation]() to see the latest features.

[!INCLUDE [model-router 1](../../../foundry/openai/includes/concepts-model-router-1.md)]

## Routing mode

With the latest version, if you choose custom deployment, you can select the **routing mode** to optimize for quality or cost while maintaining a baseline level of performance. Setting a routing mode is optional, and if you don't set one, your deployment defaults to the Balanced mode.

Available routing modes:

| Mode | Description |
|------|-----------|
| Balanced (default) | Considers both cost and quality dynamically. Perfect for general-purpose scenarios |
| Quality | Prioritizes for maximum accuracy. Best for complex reasoning or critical outputs |
| Cost | Prioritizes for more cost savings. Ideal for high-volume, budget-sensitive workloads |

[!INCLUDE [model-router 2](../../../foundry/openai/includes/concepts-model-router-2.md)]