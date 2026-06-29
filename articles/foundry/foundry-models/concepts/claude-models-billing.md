---
title: Claude consumption units (CCU) billing in Microsoft Foundry
description: Claude consumption units (CCU) bill Claude models in Microsoft Foundry through Azure Marketplace. Learn token-to-CCU conversion, costs, and migration here.
ms.service: microsoft-foundry
ms.subservice: foundry-models
ms.topic: concept-article
ms.date: 06/23/2026
ms.custom:
  - classic-and-new
  - doc-kit-assisted
author: msakande
ms.author: mopeakande
ms.reviewer: aashishb
reviewer: aashishb
ai-usage: ai-assisted

#CustomerIntent: As a developer using Claude models in Foundry, I want to understand how CCU billing works in Microsoft Foundry so that I can accurately predict my application costs.
---


# Claude Consumption Units (CCU) billing in Microsoft Foundry

This article explains how Claude models from Anthropic are billed in Microsoft Foundry. Claude models use a billing unit called the **Claude Consumption Unit (CCU)**, which is the same construct Anthropic uses across its other supported cloud platforms. Use of CCU ensures that pricing, discounts, and invoicing are consistent for customers and partners wherever Claude models are deployed.


## What is a Claude Consumption Unit?

A **Claude Consumption Unit (CCU)** is a unit of measure used solely for invoicing of Claude models. CCU billing applies to [all Claude models offered in Foundry](claude-models.md#available-claude-models). CCU is the billing unit only. The way you call Claude models, the tokens you send and receive, and the per-model rate limits are unchanged. If you're sizing a workload, continue to plan with **tokens per minute (TPM)** and **requests per minute (RPM)**.

- CCU has a **fixed price**, published on the Claude offer on Azure Marketplace.
- Token usage on Claude models is converted to CCU using Anthropic's published per-model token rates at [Claude pricing](https://aka.ms/ccu-pricing), after applying any contractual discounts.
- CCU is the **single billing dimension** for Claude models in Foundry. One Marketplace meter replaces the previous per-model token meters.
- The CCU meter is **MACC-eligible**. You're billed by Microsoft on your Azure invoice, and CCU spend decrements your Microsoft Azure Consumption Commitment (MACC) the same way any other Azure Marketplace consumption does.

This is the same CCU construct Anthropic uses on its other supported cloud platforms. Pricing, discount semantics, and the conversion model are consistent across clouds. For Anthropic's cross-cloud reference, see [Claude pricing](https://aka.ms/ccu-pricing).

## CCU at a glance

| Concept | Details |
|---|---|
| **Billing unit** | Claude Consumption Unit (CCU) |
| **CCU price** | Fixed; published on the Claude offer on Azure Marketplace |
| **Token rates** | Anthropic's per-model token rates, published at [Claude pricing](https://aka.ms/ccu-pricing) |
| **Conversion** | Token usage is converted to CCU using Anthropic's published per-model token rates, after discounts |
| **Billing cadence** | Hourly metering, invoiced monthly in arrears |
| **Payment model** | Pay-as-you-go through Azure Marketplace; no prepaid CCU credits |
| **Discounts** | Applied at the token-to-CCU conversion step via Azure Marketplace private offers |
| **Currency** | CCU is denominated in USD; your Azure invoice converts to local currency per your billing account terms |
| **Tax** | Calculated and collected by Microsoft per your Azure billing account |
| **Regional availability** | CCU billing applies in all regions where Claude models in Foundry are deployed |
| **Cost visibility** | Single CCU line in Azure Cost Management; per-model token detail in the Foundry portal |

## How tokens become CCU

For every Claude API call you make through Foundry, token usage is converted to CCU as follows:

1. Anthropic meters the input and output tokens consumed by the call, by model.
1. Token usage is priced using Anthropic's per-model token rates, published at [Claude pricing](https://aka.ms/ccu-pricing). The rate in effect at the time of each call applies, so changes to Anthropic's published rates take effect immediately for subsequent calls.
1. Any contractual discount you have (for example, an Azure Marketplace private offer with Anthropic) is applied at this step.
1. The resulting dollar amount is converted to CCU at the fixed CCU price published on the Claude offer on Azure Marketplace.
1. CCU is metered hourly to Azure Marketplace and rolls up onto your Azure invoice.

### Forecasting CCU spend

To estimate monthly cost, multiply your expected token volume by the per-model rate from [Claude pricing](https://aka.ms/ccu-pricing), apply any discounts from your private offer, and divide the resulting dollar amount by the CCU price to get expected CCU.

For example, suppose your workload runs for one billing period and consumes Claude model usage that, after applicable discounts, converts to **1,000 CCU**. The following are true for the workload's cost estimate:

- It is metered to Azure Marketplace as **1,000 CCU**.
- It appears on your Azure invoice and in Azure Cost Management as a single line for 1,000 CCU, valued at the published CCU price; that is, **1,000 CCU × CCU price**.
- Per-model token breakdown remains available in the Foundry portal.

## Subscribing to a Claude offer in Foundry

You can subscribe to the Claude offer either from **Azure Marketplace** or from the **Microsoft Foundry portal**. Both lead to the same CCU billing model:

To subscribe from Azure Marketplace:

1. Discover Claude on [Azure Marketplace](https://marketplace.microsoft.com/).
1. Select the **Claude Platform on Foundry** offer and accept it on your Azure billing account.
1. You're redirected into the Microsoft Foundry catalog.
1. Deploy any Claude model from the catalog.
1. Usage is metered and billed in CCU.

To subscribe from the Microsoft Foundry portal:

1. In the Foundry portal, browse the model catalog and select a Claude model.
1. Accept the **Claude platform** offer.
1. Deploy the model.
1. Usage is metered and billed in CCU.


## Where you see CCU

| Surface | What appears |
|---|---|
| **Azure Cost Management** | Usage and cost rolled up as CCU |
| **Microsoft Foundry portal — Pricing tab** | A link to the [Claude pricing](https://aka.ms/ccu-pricing) documentation |
| **Microsoft Foundry portal — Monitoring tab** | Per-model token usage and request counts |
| **Marketplace order / private offer** | A single CCU plan replaces previous per-model plans |

## Discounts and Azure Marketplace private offers

Customers with negotiated Anthropic pricing receive their discount through an **Azure Marketplace private offer**. The discount is applied at the token-to-CCU conversion step (step 3 in [How tokens become CCU](#how-tokens-become-ccu)), not as a separate line item on the invoice.

Key characteristics:

- **Per-model discount rates.** A private offer can carry different discount rates for different Claude models. The applicable rate is used per call before conversion to CCU.
- **No prepaid CCU credits.** CCU is metered in arrears. You don't purchase a balance of CCU in advance.
- **MACC continues to apply.** CCU spend decrements your Microsoft Azure Consumption Commitment the same way other Azure Marketplace consumption does.

If you have an existing private offer with Anthropic that predates the CCU billing model, see [Existing deployments and migration](#existing-deployments-and-migration).

## Existing deployments and migration

CCU billing applies to Claude deployments you create in Foundry going forward. Deployments you created before CCU became generally available continue to bill on their existing per-model plan without interruption.

To move an existing workload to CCU billing, create a new deployment in Foundry—new deployments are billed in CCU automatically.

If you have a negotiated private offer with Anthropic, contact your Microsoft or Anthropic account team for help moving to CCU while preserving your negotiated pricing.

## Sizing and rate limits

CCU doesn't change how you size Claude workloads. Continue to plan with:

- **Tokens per minute (TPM)** and **requests per minute (RPM)** quotas, which are per model.
- Anthropic's per-model token rates for cost modeling.

For current Claude model quotas in Foundry, see [Use Claude models in Foundry Models](../how-to/use-foundry-models-claude.md).

## Support and billing disputes

For any support question or billing dispute, contact Microsoft support the same way you do today.

## What CCU doesn't change

- **Your application code.** No SDK or API changes are required.
- **Per-model token rates.** Anthropic's published per-model rates continue to drive cost. CCU is the unit those rates roll up into for invoicing.
- **MACC eligibility.** Claude usage continues to decrement your Microsoft Azure Consumption Commitment.
- **Your Microsoft billing relationship.** Your invoice, payment terms, and tax handling continue to be with Microsoft.
- **Per-call experience.** Request and response payloads, latency, throughput, and rate-limiting behavior are unchanged.

## Frequently asked questions

### Is CCU a price change?

No. CCU is a change in billing format, not in price. Your cost is driven by Anthropic's per-model token rates, published at [Claude pricing](https://aka.ms/ccu-pricing), and any discounts in your private offer—none of which change when usage rolls up into CCU on your Azure invoice.

### Do I need to do anything when Claude models become generally available in Foundry?

No. The system automatically bills new deployments in CCU. Existing deployments continue on their current plan without interruption. To move an existing workload to CCU, create a new deployment in Foundry.

### Where do I see per-model usage if my invoice only shows CCU?

You can see per-model token and request detail in the **Monitoring tab** of the Microsoft Foundry portal for operational and sizing visibility.

### How does CCU interact with MACC?

CCU spend decrements your Microsoft Azure Consumption Commitment the same way other Azure Marketplace consumption does. CCU billed by other cloud providers doesn't decrement your Microsoft Azure Consumption Commitment.

### Who do I contact for support or a billing dispute?

Contact Microsoft support the same way you do today.

## Related content

- [Claude models in Microsoft Foundry](claude-models.md)
- [Use Claude models in Foundry Models](../how-to/use-foundry-models-claude.md)
- [Plan and manage costs for Microsoft Foundry](../../concepts/manage-costs.md)
- [Claude pricing](https://aka.ms/ccu-pricing)
