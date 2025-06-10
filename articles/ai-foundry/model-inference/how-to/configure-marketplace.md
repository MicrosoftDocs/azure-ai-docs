---
title: Configure access to Models from Partners and Community
description: Learn how to configure access to Models from Partners and Community.
author: ssalgadodev
ms.author: ssalgado
ms.service: azure-ai-model-inference
ms.topic: how-to
ms.date: 5/11/2025
manager: scottpolly
ms.reviewer: fasantia
reviewer: santiagxf
---

# Configure access to Models from Partners and Community

Certain models in Azure AI Foundry Models are offered directly by the model provider through the Azure Marketplace. This article explains the requirements to use Azure Marketplace if you plan to use such models in your workloads. Models Sold Directly by Azure, like DeepSeek or Phi, or Azure OpenAI in Foundry Models, like GPTs, don't have this requirement. 

> [!TIP]
> All models offered in AI Foundry Models are hosted in Microsoft's Azure environment and the Service does NOT interact with any external services or model provider.

:::image type="content" source="../media/configure-marketplace/azure-marketplace-3p.png" alt-text="A diagram with the overall architecture of Azure Marketplace integration with AI Foundry Models." lightbox="../media/configure-marketplace/azure-marketplace-3p.png":::

[!INCLUDE [marketplace-rbac](../includes/configure-marketplace/rbac.md)]

## Country availability

Models from Partners and Community with Pay-as-you-go billing is available only to users whose Azure subscription belongs to a billing account in a country/region where the model offer is available. Availability varies per model provider and model SKU. Read [Region availability for models](../../how-to/deploy-models-serverless-availability.md).

## Troubleshooting

Use the following troubleshooting guide to find and solve errors when deploying third-party models in AI Foundry Models:

| Error | Description |
|-------|-------------|
| This offer is not made available by the provider in the country where your account and Azure Subscription are registered. | The model provider didn't make the specific model SKU available in the country where the subscription is registered. Each model provider may decide to make the offer available in specific countries and such may vary by model SKU. You need to deploy the model to a subscription having billing on a supported country. See the list of countries at [Region availability for models](../../how-to/deploy-models-serverless-availability.md).  |
| Marketplace Subscription purchase eligibility check failed. | The model provider didn't make the specific model SKU available in the country where the subscription is registered or it isn't available in the region where you deployed the Azure AI Services resource. See [Region availability for models](../../how-to/deploy-models-serverless-availability.md). |
| Unable to create a model deployment for model "model-name". If the error persists, please contact HIT (Human Intelligence Team) via this link: https://go.microsoft.com/fwlink/?linkid=2101400&clcid=0x409 and request to allowlist the Azure subscription. | Azure Marketplace rejects the request to create a model subscription. Such can be due to multiple reasons, including subscribing to the model offering too often, or from multiple subscriptions at the same time. Please contact support using the provided link indicating your subscription ID. |
| This offer is not available for purchasing by subscriptions belonging to Microsoft Azure Cloud Solution Providers | Cloud Solution Provider (CSP) subscriptions do not have the ability to purchase third-party model offerings. You can consider models offered as first-party consumption service. |