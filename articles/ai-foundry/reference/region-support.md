---
title: Azure AI Foundry feature availability across clouds regions
titleSuffix: Azure AI Foundry
description: This article lists Azure AI Foundry feature availability across clouds regions.
manager: scottpolly
ms.service: azure-ai-foundry
ms.topic: conceptual
ms.date: 04/28/2025
ms.reviewer: deeikele
ms.author: sgilley
author: sdgilley
ms.custom: references_regions, build-2024
---

# Azure AI Foundry feature availability across clouds regions

[Azure AI Foundry](https://ai.azure.com) brings together various Azure AI capabilities that previously were only available as standalone Azure services. While we strive to make all features available in all regions where Azure AI Foundry is supported at the same time, feature availability may vary by region. In this article, you'll learn what Azure AI Foundry features are available across cloud regions.  

## Azure AI Foundry projects

Azure AI Foundry is currently available in the following Azure regions. You can create [projects in Azure AI Foundry portal](../how-to/create-projects.md) in these regions.

- Australia East
- Brazil South
- Canada Central
- Canada East
- East US
- East US 2
- France Central
- Germany West Central
- Japan East
- Korea Central
- North Central US
- Norway East
- Poland Central
- South Africa North
- South Central US
- South India
- Sweden Central
- Switzerland North
- UAE North
- UK South
- West Europe
- West US
- West US 3
- US Gov Virginia
- US Gov Arizona

## Azure AI Foundry features
 
You can add features from different regions to your project. You may need to use a different region for a particular feature, based on the region availability of that feature.

The following table lists the availability of Azure AI Foundry features across Azure regions.

| Service                        | Description                                                                                                                                          | Link                                                                                                      |
|--------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------|
| Azure OpenAI                   | Note that some models might not be available within the Azure AI Foundry model catalog.                                                              | [Azure OpenAI quotas and limits](/azure/ai-services/openai/quotas-limits)
| Speech capabilities            | Azure AI Speech capabilities including custom neural voice vary in regional availability due to underlying hardware availability.                     | [Speech service supported regions](../../ai-services/speech-service/regions.md)                           |
| Serverless API deployments     | Some models in the model catalog can be deployed as a serverless API with pay-as-you-go billing.                                                      | [Region availability for models in Serverless API endpoints](../how-to/deploy-models-serverless-availability.md) |
| Azure AI Content Safety        | To use the Content Safety APIs, you must create your Azure AI Content Safety resource in a supported region.                                           | [What is Azure AI Content Safety?](../../ai-services/content-safety/overview.md#region-availability)       |
| Azure AI Foundry Agent Service         | Azure AI Foundry Agent Service supports the same models as the chat completions API in Azure OpenAI.                                                          | [Azure AI Foundry Agent Service region availability](../../ai-services/agents/concepts/model-region-support.md#azure-openai-models) |

## Azure AI Foundry in sovereign clouds

### Azure Government (United States)

Available to US government entities and their partners only. See more information about Azure Government [here](/azure/azure-government/documentation-government-welcome) and [here.](/azure/azure-government/compare-azure-government-global-azure)

- **Azure AI Foundry portal URL:**
  - [https://ai.azure.us/](https://ai.azure.us/)
- **Regions:**
  - US Gov Arizona
  - US Gov Virginia
- **Available pricing tiers:**
  - Standard. See more pricing details [here](https://azure.microsoft.com/pricing/details/ai-foundry/)
- **Supported features:**
  - [Azure OpenAI Services](../../ai-services/openai/azure-government.md)
  - Azure AI Services
    - [Speech](../../ai-services/speech-service/regions.md)
    - Speech playground (preview)
    - Language playground (preview)
    - Language + [Translator](../../ai-services/translator/reference/sovereign-clouds.md)
    - Vision + Document
    - Content Safety
  - Model catalog. See list of supported models [here](../../machine-learning/reference-machine-learning-cloud-parity.md)
  - Templates (preview)
  - Prompt flow
  - Tracing (preview)
  - Guardrails & controls
    - Content filters
    - Profanity blocklist (preview)
  - Management center
- **Unsupported features:**
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

## Next steps

- See [Azure global infrastructure products by region](https://azure.microsoft.com/global-infrastructure/services/).
