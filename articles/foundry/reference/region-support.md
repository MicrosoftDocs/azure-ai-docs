---
title: "Feature availability across cloud regions"
description: "This article lists Microsoft Foundry feature availability across cloud regions."
ms.service: azure-ai-foundry
ms.topic: concept-article
ms.date: 01/23/2026
ms.reviewer: deeikele
ms.author: sgilley
author: sdgilley
ai-usage: ai-assisted
ms.custom:
  - references_regions, build-2024, copilot-scenario-highlight, dev-focus
  - classic-and-new
  - doc-kit-assisted
---

# Microsoft Foundry feature availability across cloud regions

[!INCLUDE [foundry-link](../includes/foundry-link.md)] brings together various Azure AI capabilities that were previously only available as standalone Azure services. While Microsoft strives to make all features available in all regions where Microsoft Foundry is supported at the same time, feature availability might vary by region. In this article, you learn what Foundry features are available across cloud regions.  

This article gives you:
- Regions where you can create a Foundry project.
- Links to the authoritative regional availability pages for major features.

This article doesn't include a single real-time matrix for every model and feature combination. Use the linked service-specific pages to confirm current availability before deployment.

## Foundry projects

Foundry is currently available in the following Azure regions. 

<!-- Government regions for foundry-classic only at this time -->
:::row:::
    :::column:::
- Australia East
- Brazil South
- Canada Central
- Canada East
- Central India
- Central US
- East Asia
- East US
- East US 2
- France Central
- Germany West Central
- Italy North
    :::column-end:::
    :::column:::
- Japan East
- Korea Central
- North Central US
- North Europe
- Norway East
- Qatar Central
- South Africa North
- South Central US
- South India
- Southeast Asia
    :::column-end:::
    :::column:::
- Spain Central
- Sweden Central
- Switzerland North
- UAE North
- UK South
- West Europe
- West US
- West US 3
:::column-end:::
:::row-end:::

## Foundry features

Use the following list to investigate regional availability for specific features you plan to use.

- **Azure OpenAI**: Some models might not be available within the Foundry model catalog. [Azure OpenAI quotas and limits](/azure/ai-foundry/openai/quotas-limits#regional-quota-capacity-limits).
- **Speech capabilities**: Azure Speech in Foundry Tools capabilities, including custom neural voice, vary in regional availability due to underlying hardware availability. [Speech service supported regions](../../ai-services/speech-service/regions.md)
- **Azure AI Content Safety**: To use the Content Safety APIs, create your Azure AI Content Safety resource in a supported region. [What is Azure AI Content Safety?](../../ai-services/content-safety/overview.md#region-availability)
- **Foundry Agent Service**: Agent Service supports Azure OpenAI model deployments, but exact model and tool availability varies by region. [Agent Service region availability](../agents/concepts/limits-quotas-regions.md#azure-openai-model-support)

[!INCLUDE [region-support 1](../includes/reference-region-support-1.md)]

[!INCLUDE [region-support 2](../includes/reference-region-support-2.md)]
