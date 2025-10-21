---
title: Feature availability across cloud regions
titleSuffix: Azure AI Foundry
description: This article lists Azure AI Foundry feature availability across cloud regions.
ms.service: azure-ai-foundry
ms.topic: concept-article
ms.date: 10/21/2025
ms.reviewer: deeikele
ms.author: sgilley
author: sdgilley
monikerRange: 'foundry-classic || foundry'
ms.custom: references_regions, build-2024, copilot-scenario-highlight
---

# Azure AI Foundry feature availability across cloud regions

[!INCLUDE [version-banner](../includes/version-banner.md)]

:::moniker range="foundry" 
[!INCLUDE [foundry-link](../default/includes/foundry-link.md)]brings together various Azure AI capabilities that were previously only available as standalone Azure services. While we strive to make all features available in all regions where Azure AI Foundry is supported at the same time, feature availability might vary by region. In this article, you learn what Azure AI Foundry features are available across cloud regions.  

## Azure AI Foundry projects

Azure AI Foundry is currently available in the following Azure regions. 

::: moniker-end

:::moniker range="foundry-classic" 
[!INCLUDE [classic-link](../includes/classic-link.md)] brings together various Azure AI capabilities that were previously only available as standalone Azure services. While we strive to make all features available in all regions where Azure AI Foundry is supported at the same time, feature availability might vary by region. In this article, you learn what Azure AI Foundry features are available across cloud regions.  

## Azure AI Foundry projects

Azure AI Foundry is currently available in the following Azure regions. You can [create either a [!INCLUDE [fdp-project-name](../includes/fdp-project-name.md)] or [!INCLUDE [hub-project-name](../includes/hub-project-name.md)] in Azure AI Foundry](../how-to/create-projects.md) in these regions.

::: moniker-end

<!-- Government regions for foundry-classic only at this time -->
:::moniker range="foundry" 
:::row:::
    :::column:::
- Australia East
- Brazil South
- Canada Central
- Canada East
- East US
- East US 2
- France Central
- Germany West Central
- Japan East
    :::column-end:::
    :::column:::
- Korea Central
- North Central US
- Norway East
- Poland Central
- South Africa North
- South Central US
- South India       
- Sweden Central
- Switzerland North
    :::column-end:::
    :::column:::
- UAE North
- UK South
- West Europe
- West US
- West US 3
    :::column-end:::
:::row-end:::
::: moniker-end

:::moniker range="foundry-classic"
:::row:::
    :::column:::
- Australia East
- Brazil South
- Canada Central
- Canada East
- East US
- East US 2
- France Central
- Germany West Central
- Japan East
    :::column-end:::
    :::column:::
- Korea Central
- North Central US
- Norway East
- Poland Central
- South Africa North
- South Central US
- South India       
- Sweden Central
- Switzerland North
    :::column-end:::
    :::column:::
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

## Azure AI Foundry features
 
You can add features from different regions to your project. You might need to use a different region for a particular feature, based on the region availability of that feature.

For maximum feature availability, consider East US 2, Sweden Central, or West US 2 as your primary regions, as they offer the most comprehensive coverage across Azure AI services.

The following table lists the availability of Azure AI Foundry features across Azure regions.

::: moniker range="foundry"

| Service                        | Description                                                                                                                                          | Link                                                                                                      |
|--------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------|
| Azure OpenAI                   | Note that some models might not be available within the Azure AI Foundry model catalog.                                                              | [Azure OpenAI quotas and limits](/azure/ai-foundry/openai/quotas-limits).
| Speech capabilities            | Azure AI Speech capabilities including custom neural voice vary in regional availability due to underlying hardware availability.                     | [Speech service supported regions](../../ai-services/speech-service/regions.md).                           |
| Azure AI Content Safety        | To use the Content Safety APIs, create your Azure AI Content Safety resource in a supported region.                                           | [What is Azure AI Content Safety?](../../ai-services/content-safety/overview.md#region-availability).       |
| Azure AI Foundry Agent Service         | Azure AI Foundry Agent Service supports the same models as the chat completions API in Azure OpenAI.                                                          | [Azure AI Foundry Agent Service region availability](../../ai-services/agents/concepts/model-region-support.md#azure-openai-models). |


::: moniker-end

:::moniker range="foundry-classic"

| Service                        | Description                                                                                                                                          | Link                                                                                                      |
|--------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------|
| Azure OpenAI                   | Note that some models might not be available within the Azure AI Foundry model catalog.                                                              | [Azure OpenAI quotas and limits](/azure/ai-foundry/openai/quotas-limits).
| Speech capabilities            | Azure AI Speech capabilities including custom neural voice vary in regional availability due to underlying hardware availability.                     | [Speech service supported regions](../../ai-services/speech-service/regions.md).                           |
| Serverless deployment     | Some models in the model catalog can be deployed as serverless deployments.                                                      | [Region availability for models in serverless deployment](../how-to/deploy-models-serverless-availability.md). |
| Azure AI Content Safety        | To use the Content Safety APIs, create your Azure AI Content Safety resource in a supported region.                                           | [What is Azure AI Content Safety?](../../ai-services/content-safety/overview.md#region-availability).       |
| Azure AI Foundry Agent Service         | Azure AI Foundry Agent Service supports the same models as the chat completions API in Azure OpenAI.                                                          | [Azure AI Foundry Agent Service region availability](../../ai-services/agents/concepts/model-region-support.md#azure-openai-models). |



## Azure AI Foundry in sovereign clouds

### Azure Government (United States)

Available to US government entities and their partners only. For more information, see [Azure Government documentation](/azure/azure-government/documentation-government-welcome) and [Compare Azure Government and global Azure](/azure/azure-government/compare-azure-government-global-azure).

- **Azure AI Foundry portal URL:**
  - [https://ai.azure.us/](https://ai.azure.us/)
- **Regions:**
  - US Gov Arizona
  - US Gov Virginia
- **Available pricing tiers:**
  - Standard. For more information, see [Azure AI Foundry pricing](https://azure.microsoft.com/pricing/details/ai-foundry/).
- **Supported features:**
  - [Azure OpenAI in Azure AI Foundry Models](../openai/azure-government.md)
  - Azure AI Services
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

Use AI to help you find the right region for your needs.  Open the [Foundry agent](../foundry-agent/ask-foundry-agent.md) and customize this prompt for your specific case:

```copilot-prompt
   Based on the features I need for my Azure AI Foundry project, which regions would you recommend to create the project? 
   I need: [list your required features here, such as: gpt-4o models, speech capabilities, custom avatar training, etc.]
```

*Copilot is powered by AI, so surprises and mistakes are possible. For more information, see [Copilot general use FAQs](https://aka.ms/copilot-general-use-faqs).*

## Next steps

- [Azure global infrastructure products by region](https://azure.microsoft.com/global-infrastructure/services/)
