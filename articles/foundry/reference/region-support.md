---
title: "Feature availability across cloud regions (temp)"
description: "This article lists Microsoft Foundry feature availability across cloud regions. (temp)"
ms.service: azure-ai-foundry
ms.topic: concept-article
ms.date: 01/23/2026
ms.reviewer: deeikele
ms.author: sgilley
author: sdgilley
ms.custom:
  - references_regions, build-2024, copilot-scenario-highlight, dev-focus
  - classic-and-new
---

# Microsoft Foundry feature availability across cloud regions (temp)

[!INCLUDE [foundry-link](../includes/foundry-link.md)] brings together various Azure AI capabilities that were previously only available as standalone Azure services. While Microsoft strives to make all features available in all regions where Microsoft Foundry is supported at the same time, feature availability might vary by region. In this article, you learn what Foundry features are available across cloud regions.  

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
 

For maximum feature availability, consider East US 2 or Sweden Central as your primary regions, as they offer the most comprehensive coverage across features.

Use the following table to investigate regional availability for specific features you plan to use.

| Service                        | Description                                                                                                                                          | Link                                                                                                      |
|--------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------|
| Azure OpenAI                   | Some models might not be available within the Foundry model catalog.                                                              | [Azure OpenAI quotas and limits](/azure/ai-foundry/openai/quotas-limits#regional-quota-capacity-limits).
| Speech capabilities            | Azure Speech in Foundry Tools capabilities, including custom neural voice, vary in regional availability due to underlying hardware availability.                     | [Speech service supported regions](../../ai-services/speech-service/regions.md)                           |
| Azure AI Content Safety        | To use the Content Safety APIs, create your Azure AI Content Safety resource in a supported region.                                           | [What is Azure AI Content Safety?](../../ai-services/content-safety/overview.md#region-availability).       |

<!-- CLASSIC-ONLY: Table row(s) removed. To restore, update links and uncomment:
| Foundry Agent Service         | Agent Service supports the same models as the chat completions API in Azure OpenAI.                                                          | [Agent Service region availability](../../ai-services/agents/concepts/model-region-support.md#azure-openai-models). |
-->

## Use AI to find the best region

Use AI to help you find the right region for your needs.  Open [Ask AI](../concepts/ask-ai.md) and customize this prompt for your specific case:

```copilot-prompt
   Based on the features I need for my Foundry project, which regions would you recommend to create the project? 
   I need: [list your required features here, such as: gpt-4o models, speech capabilities, custom avatar training, etc.]
```

*Copilot is powered by AI, so surprises and mistakes are possible. For more information, see [Copilot general use FAQs](https://aka.ms/copilot-general-use-faqs).*

## Next step

- [Azure global infrastructure products by region](https://azure.microsoft.com/global-infrastructure/services/)
