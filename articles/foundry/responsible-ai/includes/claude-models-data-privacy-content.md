---
title: Include file
description: include file
author: msakande
ms.author: mopeakande
ms.reviewer: keijik
ms.service: microsoft-foundry
ms.topic: include
ms.date: 06/23/2026
ms.custom: include, classic-and-new
---

This article explains how data is processed when you use Claude models in Microsoft Foundry. Claude models in Microsoft Foundry are third-party Marketplace offerings from Anthropic. Data handling depends on the hosting option you select when deploying the Claude model. 

Microsoft Foundry offers two hosting options for deploying your Claude models: 

- **Hosted on Azure**
- **Hosted on Anthropic infrastructure**

For both hosting options, Anthropic remains the seller and operator of Claude models in Microsoft Foundry and acts as an independent data processor for prompts and outputs associated with Claude models. Your use of the Claude models is subject to the terms of use Anthropic provides for Claude models and APIs. 

## Hosted on Azure

If you choose the **Hosted on Azure** deployment option, Azure infrastructure processes your prompts and outputs. This processing includes request ingress, API services, and GPU inference. The selected Azure geography stores data at rest, and processing is scoped to applicable "Global" or "DataZone" deployment options available on Microsoft Foundry. 

Automatic safeguards flag content that might be sent to Anthropic Trust & Safety for review. Anthropic personnel review customer content on an exceptions-only basis to investigate potential safety violations, subject to applicable Anthropic terms. 

## Hosted on Anthropic Infrastructure

If you choose the **Hosted on Anthropic Infrastructure** deployment option, Anthropic hosted infrastructure processes your prompts and outputs. Data might be processed outside of Azure, including outside of your selected Azure region. To learn more about the terms that govern data processing in Anthropic-hosted infrastructure, see [Anthropic's Data processing Addendum](https://www.anthropic.com/legal/data-processing-addendum) and [Anthropic's Commercial Terms of Service](https://aka.ms/anthropic_tandc).

Microsoft continues to provide Microsoft Foundry experience, Azure infrastructure, and billing services for this deployment option. Microsoft also collects billing, usage, customer contact, and transaction information for Marketplace operations. Microsoft might share such customer contact information, transaction details, and usage information with Anthropic so that Anthropic can operate, support, and communicate with customers about the model. Microsoft processes data for these services under the Microsoft Products and Services Data Protection Addendum and applicable Marketplace terms. 

## Where can I learn about harmful content screening?

Claude models in Microsoft Foundry use Anthropic safety systems and safeguards, supported by Microsoft. To learn more about harmful content screening, safety review, and Anthropic-specific processing, see Anthropic’s documentation and the Anthropic terms presented during deployment. 

## Related content

- [Claude Consumption Units (CCU) billing in Microsoft Foundry](../../foundry-models/concepts/claude-models-billing.md)
- [Claude models in Microsoft Foundry](../../foundry-models/concepts/claude-models.md)
- [Microsoft Products and Services Data Protection Addendum (DPA)](https://www.microsoft.com/licensing/docs/view/Microsoft-Products-and-Services-Data-Protection-Addendum-DPA)
- [Anthropic's Data processing Addendum](https://www.anthropic.com/legal/data-processing-addendum)
- [Anthropic's Commercial Terms of Service](https://aka.ms/anthropic_tandc)
