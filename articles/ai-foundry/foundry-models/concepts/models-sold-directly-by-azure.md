---
title: Foundry Models sold directly by Azure
titleSuffix: Azure AI Foundry
description: Explore the Foundry Models sold directly by Azure and their capabilities.
author: msakande
ms.author: mopeakande
manager: nitinme
ms.date: 09/05/2025
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: conceptual
ms.custom:
  - references_regions
  - tool_generated
  - build-aifnd
  - build-2025
zone_pivot_groups: models-sold-directly-by-azure

# customer intent:
---

# Foundry Models sold directly by Azure

Azure AI Foundry Models gives you access to flagship models in Azure AI Foundry to consume them as APIs with flexible deployment options. Foundry Models belong to one of two categories: Models sold directly by Azure and Models from partners and community. 
This article lists a selection of Foundry Models sold directly by Azure along with their capabilities, [deployment types, and regions of availability](deployment-types.md), excluding [deprecated and legacy models](../../concepts/model-lifecycle-retirement.md#deprecated). 

Models sold directly by Azure include all Azure OpenAI models and specific, selected models from top providers. To learn more about these models, see [Models sold directly by Azure](../../concepts/foundry-models-overview.md#models-sold-directly-by-azure).

Depending on what [kind of project](../../what-is-azure-ai-foundry.md#work-in-an-azure-ai-foundry-project) you're using in Azure AI Foundry, you might see a different selection of these models. Specifically, if you're using a Foundry project, built on an Azure AI Foundry resource, you see the models that are available for standard deployment to a Foundry resource. Alternatively, if you're using a hub-based project, hosted by an Azure AI Foundry hub, you see models that are available for deployment to managed compute and serverless APIs. These model selections do overlap in many cases, since many models support the multiple [deployment options](../../concepts/deployments-overview.md). 

## Region availability for models sold directly by Azure

**_Add tables that summarize ADM region availability_**


::: zone pivot="azure-openai"

[!INCLUDE [models-azure-direct-openai](../../openai/includes/models-azure-direct-openai.md)]

::: zone-end


::: zone pivot="azure-direct-others"

[!INCLUDE [models-azure-direct-others](../includes/models-azure-direct-others.md)]

::: zone-end


