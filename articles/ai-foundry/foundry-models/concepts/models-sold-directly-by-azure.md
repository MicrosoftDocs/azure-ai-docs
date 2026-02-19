---
title: Foundry Models sold directly by Azure
titleSuffix: Microsoft Foundry
description: Learn about Microsoft Foundry Models sold directly by Azure, their capabilities, deployment types, and regional availability for AI applications.
author: msakande
ms.author: mopeakande
manager: nitinme
ms.date: 02/12/2026
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: product-comparison
ms.custom:
  - references_regions
  - tool_generated
  - build-aifnd
  - build-2025
  - pilot-ai-workflow-jan-2026
monikerRange: 'foundry-classic || foundry'
ai-usage: ai-assisted
zone_pivot_groups: models-sold-directly-by-azure

#CustomerIntent: As a developer, I want to browse the full list of Microsoft Foundry Models sold directly by Azure, including their capabilities and regional availability, so that I can select the right model for my application.
---

# Foundry Models sold directly by Azure

[!INCLUDE [version-banner](../../includes/version-banner.md)]

:::moniker range="foundry-classic"
This article lists a selection of Microsoft Foundry Models sold directly by Azure along with their capabilities, [deployment types, and regions of availability](deployment-types.md), excluding [deprecated and legacy models](../../concepts/model-lifecycle-retirement.md#deprecated). To see a list of Azure OpenAI models that are supported by the Foundry Agent Service, see [Models supported by Agent Service](../../agents/concepts/model-region-support.md).
:::moniker-end

:::moniker range="foundry"
This article lists a selection of Microsoft Foundry Models sold directly by Azure along with their capabilities, [deployment types, and regions of availability](deployment-types.md), excluding [deprecated and legacy models](../../concepts/model-lifecycle-retirement.md#deprecated). To see a list of Azure OpenAI models that are supported by the Foundry Agent Service, see [Models supported by Agent Service](../../default/agents/concepts/limits-quotas-regions.md).
:::moniker-end

Models sold directly by Azure include all Azure OpenAI models and specific, selected models from top providers. These models are billed through your Azure subscription, covered by Azure service-level agreements, and supported by Microsoft. For models offered by partners outside of this list, see [Foundry Models from partners and community](models-from-partners.md).

Use the tabs at the top of this page to switch between [Azure OpenAI models](https://learn.microsoft.com/azure/ai-foundry/foundry-models/concepts/models-sold-directly-by-azure?pivots=azure-openai) and [other model collections](https://learn.microsoft.com/azure/ai-foundry/foundry-models/concepts/models-sold-directly-by-azure?pivots=azure-direct-others) from providers like Cohere, DeepSeek, Meta, Mistral AI, and xAI.

::: moniker range="foundry-classic"

[!INCLUDE [models-list-introduction](../includes/models-list-introduction.md)]

::: moniker-end

::: moniker range="foundry"

Foundry Models are available for standard deployment to a Foundry resource.

::: moniker-end

To learn more about attributes of Foundry Models sold directly by Azure, see [Explore Foundry Models](../../concepts/foundry-models-overview.md#models-sold-directly-by-azure).


::: zone pivot="azure-openai"

[!INCLUDE [models-azure-direct-openai](../../openai/includes/models-azure-direct-openai.md)]

::: zone-end


::: zone pivot="azure-direct-others"

[!INCLUDE [models-azure-direct-others](../includes/models-azure-direct-others.md)]

::: zone-end


