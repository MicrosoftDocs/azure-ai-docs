---
title: Feature availability across cloud regions
titleSuffix: Microsoft Foundry
description: This article lists Microsoft Foundry feature availability across cloud regions.
ms.service: azure-ai-foundry
ms.topic: concept-article
ms.date: 01/23/2026
ms.reviewer: deeikele
ms.author: sgilley
author: sdgilley
monikerRange: 'foundry-classic || foundry'
ms.custom: references_regions, build-2024, copilot-scenario-highlight, dev-focus
---

# Microsoft Foundry feature availability across cloud regions

[!INCLUDE [version-banner](../includes/version-banner.md)]

:::moniker range="foundry" 
[!INCLUDE [foundry-link](../default/includes/foundry-link.md)] brings together various Azure AI capabilities that were previously only available as standalone Azure services. While Microsoft strives to make all features available in all regions where Microsoft Foundry is supported at the same time, feature availability might vary by region. In this article, you learn what Foundry features are available across cloud regions.  

## Foundry projects

Foundry is currently available in the following Azure regions. 

::: moniker-end

:::moniker range="foundry-classic" 
[!INCLUDE [classic-link](../includes/classic-link.md)] brings together various Azure AI capabilities that were previously only available as standalone Azure services. While Microsoft strives to make all features available in all regions where Foundry is supported at the same time, feature availability might vary by region. In this article, you learn what Foundry features are available across cloud regions.  

## Foundry projects

Foundry is currently available in the following Azure regions. You can [create either a [!INCLUDE [fdp-project-name](../includes/fdp-project-name.md)] or [!INCLUDE [hub-project-name](../includes/hub-project-name.md)] in Foundry](../how-to/create-projects.md) in these regions.

:::row:::
    :::column:::
- Australia East
- Brazil South
- Canada Central
- Canada East
- Central India
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

::: moniker-end

<!-- Government regions for foundry-classic only at this time -->
:::moniker range="foundry"
:::row:::
    :::column:::
- Australia East
- Brazil South
- Canada Central
- Canada East
- Central India
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
::: moniker-end

## Foundry features
 

For maximum feature availability, consider East US 2 or Sweden Central as your primary regions, as they offer the most comprehensive coverage across features.

Use the following table to investigate regional availability for specific features you plan to use.

::: moniker range="foundry"

| Service                        | Description                                                                                                                                          | Link                                                                                                      |
|--------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------|
| Azure OpenAI                   | Some models might not be available within the Foundry model catalog.                                                              | [Azure OpenAI quotas and limits](/azure/ai-foundry/openai/quotas-limits#regional-quota-capacity-limits).
| Speech capabilities            | Azure Speech in Foundry Tools capabilities, including custom neural voice, vary in regional availability due to underlying hardware availability.                     | [Speech service supported regions](../../ai-services/speech-service/regions.md)                           |
| Azure AI Content Safety        | To use the Content Safety APIs, create your Azure AI Content Safety resource in a supported region.                                           | [What is Azure AI Content Safety?](../../ai-services/content-safety/overview.md#region-availability).       |
| Foundry Agent Service         | Agent Service supports the same models as the chat completions API in Azure OpenAI.                                                          | [Agent Service region availability](../default/agents/concepts/limits-quotas-regions.md#azure-openai-model-support). |


::: moniker-end

:::moniker range="foundry-classic"

| Service                        | Description                                                                                                                                          | Link                                                                                                      |
|--------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------|
| Azure OpenAI                   | Some models might not be available within the model catalog.                                                              | [Azure OpenAI quotas and limits](/azure/ai-foundry/openai/quotas-limits#regional-quota-capacity-limits).
| Speech capabilities            | Azure Speech capabilities, including custom neural voice, vary in regional availability due to underlying hardware availability.                     | [Speech service supported regions](../../ai-services/speech-service/regions.md).                           |
| Serverless deployment     | Some models in the model catalog can be deployed as serverless deployments.                                                      | [Region availability for models in serverless deployment](../how-to/deploy-models-serverless-availability.md). |
| Azure AI Content Safety        | To use the Content Safety APIs, create your Azure AI Content Safety resource in a supported region.                                           | [What is Azure AI Content Safety?](../../ai-services/content-safety/overview.md#region-availability).       |
| Agent Service         | Agent Service supports the same models as the chat completions API in Azure OpenAI.                                                          | [Agent Service region availability](../agents/concepts/model-region-support.md). |


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

:::moniker-end

## Use AI to find the best region

Use AI to help you find the right region for your needs.  Open [Ask AI](../concepts/ask-ai.md) and customize this prompt for your specific case:

```copilot-prompt
   Based on the features I need for my Foundry project, which regions would you recommend to create the project? 
   I need: [list your required features here, such as: gpt-4o models, speech capabilities, custom avatar training, etc.]
```

*Copilot is powered by AI, so surprises and mistakes are possible. For more information, see [Copilot general use FAQs](https://aka.ms/copilot-general-use-faqs).*

## Next step

- [Azure global infrastructure products by region](https://azure.microsoft.com/global-infrastructure/services/)
