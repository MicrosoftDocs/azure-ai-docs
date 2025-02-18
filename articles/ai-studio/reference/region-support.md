---
title: Azure AI Foundry feature availability across clouds regions
titleSuffix: Azure AI Foundry
description: This article lists Azure AI Foundry feature availability across clouds regions.
manager: scottpolly
ms.service: azure-ai-foundry
ms.topic: conceptual
ms.date: 01/15/2025
ms.reviewer: deeikele
ms.author: sgilley
author: sdgilley
ms.custom: references_regions, build-2024
---

# Azure AI Foundry feature availability across clouds regions

Azure AI Foundry brings together various Azure AI capabilities that previously were only available as standalone Azure services. While we strive to make all features available in all regions where Azure AI Foundry is supported at the same time, feature availability may vary by region. In this article, you'll learn what Azure AI Foundry features are available across cloud regions.  

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

> [!NOTE]
> Azure AI Foundry is currently not available in Azure Government regions or air-gap regions.

## Azure AI Foundry features
 
You can add features from different regions to your project. You may need to use a different region for a particular feature, based on the region availability of that feature.

The following table lists the availability of Azure AI Foundry features across Azure regions.

| Service                        | Description                                                                                                                                          | Link                                                                                                      |
|--------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------|
| Azure OpenAI                   | Note that some models might not be available within the Azure AI Foundry model catalog.                                                              | [Azure OpenAI quotas and limits](/azure/ai-services/openai/quotas-limits)
| Speech capabilities            | Azure AI Speech capabilities including custom neural voice vary in regional availability due to underlying hardware availability.                     | [Speech service supported regions](../../ai-services/speech-service/regions.md)                           |
| Serverless API deployments     | Some models in the model catalog can be deployed as a serverless API with pay-as-you-go billing.                                                      | [Region availability for models in Serverless API endpoints](../how-to/deploy-models-serverless-availability.md) |
| Azure AI Content Safety        | To use the Content Safety APIs, you must create your Azure AI Content Safety resource in a supported region.                                           | [What is Azure AI Content Safety?](../../ai-services/content-safety/overview.md#region-availability)       |
| Azure AI Agent Service         | Azure AI Agent Service supports the same models as the chat completions API in Azure OpenAI.                                                          | [Azure AI Agent Service region availability](../../ai-services/agents/concepts/model-region-support.md#azure-openai-models) |

## Next steps

- See [Azure global infrastructure products by region](https://azure.microsoft.com/global-infrastructure/services/).
