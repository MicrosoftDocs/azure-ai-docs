---
title: "Feature availability across cloud regions (classic)"
description: "This article lists Microsoft Foundry feature availability across cloud regions. (classic)"
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
ROBOTS: NOINDEX, NOFOLLOW
---

# Microsoft Foundry feature availability across cloud regions (classic)

**Currently viewing:** :::image type="icon" source="../../foundry/media/yes-icon.svg" border="false"::: **Foundry (classic) portal version** - [Switch to version for the new Foundry portal](../../foundry/reference/region-support.md)

[!INCLUDE [foundry-link](../../foundry/includes/foundry-link.md)] brings together various Azure AI capabilities that were previously only available as standalone Azure services. While Microsoft strives to make all features available in all regions where Foundry is supported at the same time, feature availability might vary by region. In this article, you learn what Foundry features are available across cloud regions.

## Foundry projects

Foundry is currently available in the following Azure regions. You can [create either a [!INCLUDE [fdp-project-name](../../foundry/includes/fdp-project-name.md)] or [!INCLUDE [hub-project-name](../includes/hub-project-name.md)] in Foundry](../how-to/create-projects.md) in these regions.

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
- US Gov Virginia
- US Gov Arizona
:::column-end:::
:::row-end:::

<!-- Government regions for foundry-classic only at this time -->

## Foundry features

Use the following list to investigate regional availability for specific features you plan to use.

- **Foundry Models**: Model availability depends on the provider and deployment type. Region support differs between Azure OpenAI models, models sold directly by Azure, and models from partners and community. Check the following pages for details:
  - [Foundry Models sold directly by Azure](../../foundry/foundry-models/concepts/models-sold-directly-by-azure.md) — Azure OpenAI models and selected models from other providers, with deployment types and regional availability.
  - [Deployment types](../../foundry/foundry-models/concepts/deployment-types.md) — compare Global Standard, Provisioned, DataZone, and other deployment types that affect where data is processed.
  - [Foundry Models from partners and community](../../foundry/foundry-models/concepts/models-from-partners.md) — models from third-party providers available through the model catalog.
  - [Azure OpenAI quotas and limits](/azure/ai-foundry/openai/quotas-limits#regional-quota-capacity-limits) — regional quota and capacity limits for Azure OpenAI models.
- **Serverless deployment**: Some models in the model catalog can be deployed as serverless deployments. [Region availability for models in serverless deployment](../how-to/deploy-models-serverless-availability.md)
- **Speech capabilities**: Azure Speech capabilities, including custom neural voice, vary in regional availability due to underlying hardware availability. [Speech service supported regions](../../ai-services/speech-service/regions.md)
- **Azure AI Content Safety**: To use the Content Safety APIs, create your Azure AI Content Safety resource in a supported region. [What is Azure AI Content Safety?](../../ai-services/content-safety/overview.md#region-availability)
- **Agent Service**: Agent Service supports Azure OpenAI model deployments, but exact model and tool availability varies by region. [Agent Service region availability](../agents/concepts/model-region-support.md)

## How to verify region support for your workload

Use this process before you create resources:

1. Select a candidate project region from the **Foundry projects** list in this article.
1. Verify feature-specific support in the **Foundry features** list links.
1. Check available quota for a specific model and region. In the Foundry portal, go to **Operate** > **Quota** and turn on the **Show all** toggle to see all models and regions, including models you haven't deployed yet. For more information, see [Quota in Foundry Control Plane](../../foundry/control-plane/overview.md#quota).
1. Confirm the final service list in [Azure global infrastructure products by region](https://azure.microsoft.com/global-infrastructure/services/).

[!INCLUDE [region-support 1](../../foundry/includes/reference-region-support-1.md)]

## Foundry in sovereign clouds

### Azure Government (United States)

Available only to US government entities and their partners. For more information, see [Azure Government documentation](/azure/azure-government/documentation-government-welcome) and [Compare Azure Government and global Azure](/azure/azure-government/compare-azure-government-global-azure).

- **Foundry portal URL:**
  - [https://ai.azure.us/](https://ai.azure.us/)
- **Regions:**
  - US Gov Arizona
  - US Gov Virginia
- **Available pricing tiers:**
  - Standard. For more information, see [Foundry pricing](https://azure.microsoft.com/pricing/details/ai-foundry/).
- **Supported features:**
  - [Azure OpenAI in Foundry Models](../openai/azure-government.md)
  - Foundry Tools
    - [Speech](../../ai-services/speech-service/regions.md)
    - Speech playground (preview)
    - Language playground (preview)
    - Language + [Translator](../../ai-services/translator/reference/sovereign-clouds.md)
    - Vision + Document
    - Content Safety
  - Model catalog. For the list of supported models, see [Machine learning cloud parity](../../machine-learning/reference-machine-learning-cloud-parity.md).
  - Templates (preview)
  - Prompt flow
  - Tracing (preview)
  - Guardrails & controls
    - Content filters
    - Profanity blocklist (preview)
  - Management center
- **Unsupported features in Azure Government regions:**
  - Serverless endpoints  
  - Content Understanding
  - Agents playground
  - Images playground
  - Real-time audio playground
  - Healthcare playground
  - Fine-tuning 
  - Azure AI Agents
  - Batch jobs 
  - Azure OpenAI Evaluation
  - Deploy Web App
  - VS Code Extension

[!INCLUDE [region-support 2](../../foundry/includes/reference-region-support-2.md)]
