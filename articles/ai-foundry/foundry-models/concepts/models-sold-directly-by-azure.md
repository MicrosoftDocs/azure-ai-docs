---
title: Foundry Models sold directly by Azure
titleSuffix: Microsoft Foundry
description: Learn about Microsoft Foundry Models sold directly by Azure, their capabilities, deployment types, and regional availability for AI applications.
author: msakande
ms.author: mopeakande
manager: nitinme
ms.date: 11/13/2025
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: product-comparison
ms.custom:
  - references_regions
  - tool_generated
  - build-aifnd
  - build-2025
monikerRange: 'foundry-classic || foundry'
ai-usage: ai-assisted
zone_pivot_groups: models-sold-directly-by-azure

#CustomerIntent: As a developer or AI practitioner, I want to explore and understand Microsoft Foundry Models sold directly by Azure, including Azure OpenAI models and selected partner models, along with their capabilities and regional availability, so that I can choose the right model for my AI application.
---

# Foundry Models sold directly by Azure

[!INCLUDE [version-banner](../../includes/version-banner.md)]

This article lists a selection of Microsoft Foundry Models sold directly by Azure along with their capabilities, [deployment types, and regions of availability](deployment-types.md), excluding [deprecated and legacy models](../../concepts/model-lifecycle-retirement.md#deprecated). To see a list of Azure OpenAI models that are supported by the Foundry Agent Service, see [Models supported by Agent Service](../../agents/concepts/model-region-support.md).

Models sold directly by Azure include all Azure OpenAI models and specific, selected models from top providers. 

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


