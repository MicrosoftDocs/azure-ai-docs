---
title: Azure Marketplace requirements for Foundry Models from partners
description: Learn about the requirements needed to configure Azure Marketplace access for Microsoft Foundry Models from partners and community and troubleshoot errors.
author: msakande   
ms.author: mopeakande
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: how-to
ms.date: 11/21/2025
monikerRange: 'foundry-classic || foundry'
ai-usage: ai-assisted
ms.custom:  pilot-ai-workflow-jan-2026
ms.custom:  pilot-ai-workflow-jan-2026
#CustomerIntent: As an Azure administrator or developer, I want to know the requirements to configure Azure Marketplace access for Microsoft Foundry Models from partners and community to deploy and use these models effectively.
---

# Azure Marketplace requirements for Foundry Models from partners

[!INCLUDE [version-banner](../../includes/version-banner.md)]

Certain Microsoft Foundry Models are offered directly by the model provider through the Azure Marketplace. These models belong to the collection of [Foundry Models from partners and community](../concepts/models-from-partners.md). This article explains the requirements to use Azure Marketplace if you plan to use such models in your workloads. [Foundry Models sold directly by Azure](../concepts/models-sold-directly-by-azure.md), like DeepSeek, Black Forest Labs, or Azure OpenAI in Foundry Models, don't have this requirement.

## Prerequisites

- An Azure subscription. If you don't have one, create a [free account](https://azure.microsoft.com/free/).
- A [Microsoft Foundry project](../../how-to/create-projects.md).

[!INCLUDE [marketplace-rbac](../../foundry-models/includes/configure-marketplace/rbac.md)]

## Country/region availability

Users can access models from partners and community with pay-as-you-go billing only if their Azure subscription belongs to a billing account in a country/region or region where the model offer is available. Availability varies per model provider and model SKU. For more information, see [Region availability for models](../../how-to/deploy-models-serverless-availability.md).

## Troubleshooting

Use the following troubleshooting guide to find and solve errors when deploying third-party models in Foundry Models:

| Error | Description |
|-------|-------------|
| Offer not available in your country/region | The model provider didn't make the specific model SKU available in the country/region where you registered your subscription. Each model provider decides which countries/regions are available, and availability can vary by model SKU. Deploy the model to a subscription with billing in a supported country/region. See [Region availability for models](../../how-to/deploy-models-serverless-availability.md). |
| Marketplace purchase eligibility check failed | The model provider didn't make the specific model SKU available in your country/region, or the model isn't available in the region where you deployed the Foundry resource. See [Region availability for models](../../how-to/deploy-models-serverless-availability.md). |
| Unable to create a model deployment | Azure Marketplace rejected the request to create a model subscription. This rejection can happen for multiple reasons, including subscribing to the model offering too often or from multiple subscriptions at the same time. Contact [support](https://go.microsoft.com/fwlink/?linkid=2101400&clcid=0x409) and include your subscription ID. |
| CSP subscription not supported | Cloud Solution Provider (CSP) subscriptions can't purchase third-party model offerings. Consider using models offered as a first-party consumption service. |

## Related content

- [Deploy Foundry Models](deploy-foundry-models.md)
- [Region availability for models](../../how-to/deploy-models-serverless-availability.md)
- [Models from partners and community](../concepts/models-from-partners.md)
