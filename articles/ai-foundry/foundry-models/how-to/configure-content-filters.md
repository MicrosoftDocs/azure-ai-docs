---
title: 'How to configure content filters for models in Azure AI Foundry'
titleSuffix: Azure AI Foundry
description: Learn to use and configure the content filters that come with Azure AI Foundry, including getting approval for gated modifications.
ms.service: azure-ai-model-inference
ms.topic: how-to
ms.date: 05/19/2025
author: msakande
ms.author: mopeakande
ms.reviewer: yinchang
reviewer: ychang-msft
recommendations: false
ms.custom: ignite-2024, github-universe-2024
zone_pivot_groups: azure-ai-models-deployment
ai-usage: ai-assisted

#CustomerIntent: As a developer working with Azure AI Foundry Models, I want to configure custom content filters for my model deployments so that I can implement appropriate safety guardrails, control harmful content detection at specific severity levels, and ensure my AI applications comply with responsible AI standards and organizational policies.
---

# How to configure content filters for models in Azure AI Foundry

::: zone pivot="ai-foundry-portal"
[!INCLUDE [portal](../../foundry-models/includes/configure-content-filters/portal.md)]
::: zone-end

::: zone pivot="programming-language-cli"
[!INCLUDE [cli](../../foundry-models/includes/configure-content-filters/cli.md)]
::: zone-end

::: zone pivot="programming-language-bicep"
[!INCLUDE [bicep](../../foundry-models/includes/configure-content-filters/bicep.md)]
::: zone-end

## Next steps

- Read more about [content filtering categories and severity levels](../../model-inference/concepts/content-filter.md) with Azure OpenAI in Azure AI Foundry Models.
- Learn more about red teaming from our: [Introduction to red teaming large language models (LLMs) article](../../openai/concepts/red-teaming.md).
