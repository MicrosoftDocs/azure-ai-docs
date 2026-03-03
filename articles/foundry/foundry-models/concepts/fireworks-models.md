---
title: Fireworks models in Microsoft Foundry (preview)
titleSuffix: Microsoft Foundry
description: Learn about Fireworks models available in the Foundry model catalog, including available models, data privacy, and frequently asked questions.
author: voutilad
ms.author: davevoutila
manager: nitinme
ms.date: 02/25/2026
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: conceptual
ms.custom:
  - build-aifnd
monikerRange: 'foundry'
ai-usage: ai-assisted
---

# Fireworks models in Foundry (preview)

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

Through integration with [Fireworks AI](https://fireworks.ai/), you can

- experiment with the latest open source models before they're available [directly from Azure](../concepts/models-sold-directly-by-azure.md)

- scale up using [Provisioned throughput](../../openai/concepts/provisioned-throughput.md)

- deploy and scale your own customized open source models

All from your Foundry project while using Azure's access and security controls.

## Enabling Fireworks on Foundry

While in preview, Fireworks requires an administrator to enable the preview feature within your Azure subscription.

To enable Fireworks, your Azure identity must have either the **Subscription Owner** or **Subscription Contributor** role.

1. Sign in to the [Azure portal](https://portal.azure.com)

1. In the search box, enter _subscriptions_ and select **Subscriptions**.

1. Select the link for your subscription's name.

1. From the left menu, under **Settings**, select **Preview features**.

1. Select the link for the **Fireworks AI on Foundry TKTKTKTKTK** preview feature.

1. Review the terms provided in the **Description** and the [data privacy](#data-privacy) section in this documentation.

1. If you don't agree to the terms, select **Close** and don't continue. Otherwise, select **Register**.

1. Select **OK**.

The **Preview features** screen refreshes and the preview feature's **State** is displayed. It might take up to 30 minutes for the feature to enable for your subscription.


## Available models

The following Fireworks models are available in the Foundry model catalog:

| Model provider | Model name | Model ID |
|---|---|---|
| DeepSeek | DeepSeek v3.1 | FW-DeepSeek-v3.1 |
| DeepSeek | DeepSeek v3.2 | FW-DeepSeek-v3.2 |
| Moonshot AI | Kimi K2 Thinking | FW-Kimi-K2-Thinking |
| Moonshot AI | Kimi K2 Instruct 0905 | FW-Kimi-K2-Instruct-0905 |
| Moonshot AI | Kimi K2.5 | FW-Kimi-K2.5 |
| OpenAI | gpt-oss-120b | FW-gpt-oss-120b |
| Zhipu AI | GLM-4.7 | FW-GLM-4.7

## Data privacy

Fireworks model deployments made available via Foundry send inference traffic outside of Azure to the Fireworks AI cloud. Your Microsoft customer agreements (including the Product Terms and Microsoft's Data Protection Addendum) don't apply to your use of Fireworks services from within Microsoft Foundry.

Consult the Fireworks AI [Trust Center](https://trust.fireworks.ai/) to review their Data Processing Addendum and certifications and their [Privacy Notice](https://fireworks.ai/privacy-policy) to understand their privacy commitment.

## Frequently asked questions

### Is Fireworks on Foundry available in Azure for US Government?

No, currently the Fireworks service isn't available for Azure Government cloud users.

### How can I get quota for Fireworks model deployments?

We're updating the quota request [form](https://aka.ms/oai/stuquotarequest) to allow requesting quota for Fireworks on Foundry. In the meantime, contact your Azure account team.

### I have a Fireworks AI account. Can I use my existing Fireworks deployments?

No, you need to create new deployments in Foundry. If you'd like to shift consumption to Azure, contact your Fireworks account team to assist.

### How do I disable Fireworks in my Foundry project?

Fireworks can be disabled at the Azure subscription level. Follow the steps to [unregister preview features](/azure/azure-resource-manager/management/preview-features#unregister-preview-feature) in your Azure subscription.

## Related content

- [Foundry Models from partners and community](models-from-partners.md)
- [Foundry model catalog overview](models-sold-directly-by-azure.md)
- [Azure built-in roles](/azure/role-based-access-control/built-in-roles#privileged)
- [Azure Preview features](/azure/azure-resource-manager/management/preview-features)