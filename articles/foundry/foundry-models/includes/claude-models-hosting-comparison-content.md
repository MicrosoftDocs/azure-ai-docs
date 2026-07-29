---
title: Include file
description: Include file
author: msakande
ms.author: mopeakande
ms.reviewer: ambadal
ms.service: microsoft-foundry
ms.topic: include
ms.date: 07/24/2026
ms.custom: include, classic-and-new
ai-usage: ai-assisted
---

Microsoft Foundry offers Claude models in two hosting configurations: **Hosted on Azure** and **Hosted on Anthropic infrastructure**. This article outlines how the various aspects are impacted by the hosting option you choose.

For model availability and capabilities, see [Claude models in Microsoft Foundry](../concepts/claude-models.md). For detailed data handling information, see [Data, privacy, and security for Claude models](../../responsible-ai/claude-models/data-privacy.md).


## At a glance

The following table summarizes the key differences between Azure-hosted and Anthropic-hosted Claude models in Microsoft Foundry.

| Topic | Hosted on Azure | Hosted on Anthropic |
|---|---|---|
| **Seller of record** | Anthropic | Anthropic |
| **Data processor** | Anthropic | Anthropic |
| **SLA** | Anthropic is the operator and provides any SLA.  | Anthropic is the operator and provides any SLA. |
| **Data retention** | Governed by [Anthropic's Data Processing Addendum](https://www.anthropic.com/legal/data-processing-addendum) and [Anthropic's Commercial Terms of Service](https://aka.ms/anthropic_tandc) | Governed by [Anthropic's Data Processing Addendum](https://www.anthropic.com/legal/data-processing-addendum) and [Anthropic's Commercial Terms of Service](https://aka.ms/anthropic_tandc) |
| **Data residency** | Data at rest is stored in the selected Azure geography and processing is scoped to applicable "global" or "DataZone" deployment options on Microsoft Foundry. | Data might be processed outside Azure, including outside the selected Azure region. |
| **Data zone availability** | Global Standard and Data Zone Standard (US) | Global Standard only |
| **Quota increase form** | [Foundry quota request](https://aka.ms/oai/stuquotarequest) | [Foundry quota request](https://aka.ms/oai/stuquotarequest) |
| **Compliance** | Refer to [Anthropic Trust Center](https://trust.anthropic.com/)| Refer to [Anthropic Trust Center](https://trust.anthropic.com/)|
| **Support path** | Microsoft Support | Microsoft Support |
| **Purchasing flow** | Azure Marketplace → CCU meter; MACC-eligible | Azure Marketplace → CCU meter; MACC-eligible |


> [!NOTE]
> For both hosting options, Anthropic is the seller and operator of Claude models in Microsoft Foundry. Claude models are Non-Microsoft Products under the Product Terms. Your use of Claude models is subject to the terms of use Anthropic provides for Claude models and APIs.

## Model and API differences

The following table summarizes operational differences that affect how you build and run applications on each hosting option.

| Dimension | Hosted on Azure | Hosted on Anthropic|
|---|---|---|
| **Model availability** | Opus 5, Opus 4.8, Sonnet 5, and Haiku 4.5 | Opus 5, Opus 4.8, Sonnet 5, Haiku 4.5, preview models (Fable), and older versions of Opus, Sonnet, and Haiku |
| **Deployment types** | Global Standard and Data Zone Standard (US) | Global Standard only |
| **Supported APIs** | Messages, Token counting | Messages, Token counting, plus /files and /skills |
| **Additional capabilities** | Core capability set | Core set plus [additional capabilities](https://docs.claude.com/en/docs/build-with-claude/overview) |
| **Content safety** | Anthropic safety systems active | Anthropic safety systems active |

## Data processing and residency

[!INCLUDE [claude-data-hosting](../../responsible-ai/includes/claude-data-hosting.md)]


## Support path

For both hosting options, contact **Microsoft Support** for all support questions, including:

- Deployment issues in the Microsoft Foundry portal
- Billing questions and disputes
- Azure Marketplace subscription issues
- API connectivity issues

## Purchasing, billing, and quotas

### Purchasing flow

Both hosting options use the same Azure Marketplace purchasing flow:

1. Subscribe to the **Claude Platform on Foundry** offer through [Azure Marketplace](https://marketplace.microsoft.com/) or the Microsoft Foundry portal model catalog.
1. Accept the offer on your Azure billing account.
1. Deploy a Claude model from the Foundry catalog. If the model is available in both versions, you land on the Azure-hosted version by default.
1. Usage is metered and billed in Claude Consumption Units (CCU).

For step-by-step instructions, see [Deploy and use Claude models in Microsoft Foundry](../how-to/use-foundry-models-claude.md).

### Billing

Both hosting options use **Claude Consumption Units (CCU)** for billing, with the following characteristics:

- **Microsoft bills** you on your Azure invoice
- **MACC-eligible** — CCU spend decrements your Microsoft Azure Consumption Commitment
- **Hourly metering**, invoiced monthly in arrears
- **Pay-as-you-go** — no prepaid CCU credits

For a full explanation of CCU billing, see [Claude Consumption Units (CCU) billing in Microsoft Foundry](../concepts/claude-models-billing.md).

### Subscription type restrictions

The following subscription types aren't supported for Claude models:

- Free trial subscriptions
- Student subscriptions
- Credit-based subscriptions
- Enterprise accounts in South Korea
- Cloud Solution Provider (CSP) subscriptions

### Quota increase

To request a quota increase beyond your default rate limits, submit the [quota increase request form](https://aka.ms/oai/stuquotarequest).

For current default rate limits by subscription type, see [Claude models in Microsoft Foundry — Quotas and rate limits](../concepts/claude-models.md#quotas-rate-limits-and-regions).

## Choose the right option for your workload

**Choose Hosted on Azure if:**

- You need data residency within a specific Azure geography
- You need Data Zone Standard (US) deployment

**Choose Hosted on Anthropic if:**

- You need access to API features that aren't yet available in the hosted on Azure version

## Related content

### Microsoft
- [Claude models in Microsoft Foundry](../concepts/claude-models.md)
- [Data, privacy, and security for Claude models in Microsoft Foundry](../../responsible-ai/claude-models/data-privacy.md)
- [Claude Consumption Units (CCU) billing in Microsoft Foundry](../concepts/claude-models-billing.md)
- [Deploy and use Claude models in Microsoft Foundry](../how-to/use-foundry-models-claude.md)
- [Microsoft Products and Services Data Protection Addendum (DPA)](https://www.microsoft.com/licensing/docs/view/Microsoft-Products-and-Services-Data-Protection-Addendum-DPA)

### Anthropic
- [Claude help center](https://support.claude.com/en/)
- [Claude platform docs](https://docs.claude.com)
- [Anthropic's Data Processing Addendum](https://www.anthropic.com/legal/data-processing-addendum)
- [Anthropic's Commercial Terms of Service](https://aka.ms/anthropic_tandc)
