---
title: "Feature availability across cloud regions (temp)"
description: "This article lists Microsoft Foundry feature availability across cloud regions. (temp)"
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
---

# Microsoft Foundry feature availability across cloud regions (temp)

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

## How to verify region support for your workload

Use this process before you create resources:

1. Select a candidate project region from the **Foundry projects** list in this article.
1. Verify model and quota availability in [Azure OpenAI quotas and limits](/azure/ai-foundry/openai/quotas-limits#regional-quota-capacity-limits).
1. Verify feature-specific support in the **Foundry features** list links.
1. Confirm the final service list in [Azure global infrastructure products by region](https://azure.microsoft.com/global-infrastructure/services/).

## Quick decision checklist

Before you choose a production region, confirm all answers are **Yes**:

- Is your required model available in the target region?
- Do you have enough quota in that region for your expected traffic?
- Are all dependent services (for example, Speech, Content Safety, Agent Service tools) available in that region?
- Do your compliance requirements require a sovereign cloud region?
- Have you validated availability in both docs and your portal experience for the same subscription and tenant?

When you validate availability, keep these constraints in mind:

- Azure OpenAI quotas are allocated per region, per subscription, and per model or deployment type.
- Azure Speech keys are region-specific and only work for the region where the Speech resource is created.
- The region list in this article is a documentation snapshot. Always verify against the linked service-specific and infrastructure pages before production rollout.

## Troubleshoot region mismatch issues

If a feature isn't available in your selected region:

- Use the feature-specific regional availability article linked in **Foundry features**.
- Create the required dependent resource in a supported region.
- Re-check model availability and quota limits for that region.
- For Speech workloads, confirm that your app configuration uses the same region as your Speech resource.
- If your organization requires a sovereign cloud, review **Foundry in sovereign clouds** in this article.

## Use AI to find the best region

Use AI to help you find the right region for your needs.  Open [Ask AI](../concepts/ask-ai.md) and customize this prompt for your specific case:

```copilot-prompt
   Based on the features I need for my Foundry project, which regions would you recommend to create the project? 
   I need: [list your required features here, such as: gpt-4o models, speech capabilities, custom avatar training, etc.]
```

*Copilot is powered by AI, so surprises and mistakes are possible. For more information, see [Copilot general use FAQs](https://aka.ms/copilot-general-use-faqs).*

## Next step

- [Azure global infrastructure products by region](https://azure.microsoft.com/global-infrastructure/services/)
