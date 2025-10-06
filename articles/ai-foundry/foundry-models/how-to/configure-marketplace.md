---
title: Configure access to Models from Partners and Community
description: Learn how to configure Azure Marketplace access for Azure AI Foundry Models from partners and community, including requirements and troubleshooting.
author: msakande   
ms.author: mopeakande
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: how-to
ms.date: 09/29/2025

#CustomerIntent: As an Azure administrator or developer, I want to configure Azure Marketplace access for Azure AI Foundry Models from partners and community to deploy and use these models effectively.
---

# Configure access to Foundry Models from partners and community

Certain models in Azure AI Foundry Models are offered directly by the model provider through the Azure Marketplace. This article explains the requirements to use Azure Marketplace if you plan to use such models in your workloads. Models sold directly by Azure, like DeepSeek, Black Forest Labs, or Azure OpenAI in Foundry Models, don't have this requirement. 

> [!NOTE]
> All models offered in Foundry Models are hosted in Microsoft's Azure environment. The service doesn't interact with any external services or model provider.


[!INCLUDE [marketplace-rbac](../../foundry-models/includes/configure-marketplace/rbac.md)]

## Country availability

Users can access models from partners and community with pay-as-you-go billing only if their Azure subscription belongs to a billing account in a country or region where the model offer is available. Availability varies per model provider and model SKU. For more information, see [Region availability for models](../../how-to/deploy-models-serverless-availability.md).

## Troubleshooting

Use the following troubleshooting guide to find and solve errors when deploying third-party models in AI Foundry Models:

| Error | Description |
|-------|-------------|
| This offer is not made available by the provider in the country where your account and Azure Subscription are registered. | The model provider didn't make the specific model SKU available in the country where you registered your subscription. Each model provider decides which countries to make the offer available in, and availability can vary by model SKU. You need to deploy the model to a subscription with billing in a supported country. See the list of countries at [Region availability for models](../../how-to/deploy-models-serverless-availability.md).  |
| Marketplace Subscription purchase eligibility check failed. | The model provider didn't make the specific model SKU available in the country where you registered your subscription, or the model isn't available in the region where you deployed the Azure AI Services resource. See [Region availability for models](../../how-to/deploy-models-serverless-availability.md). |
| Unable to create a model deployment for model "model-name". If the error persists, please contact HIT (Human Intelligence Team) via this link: https://go.microsoft.com/fwlink/?linkid=2101400&clcid=0x409 and request to allowlist the Azure subscription. | Azure Marketplace rejects the request to create a model subscription. This rejection can happen for multiple reasons, including subscribing to the model offering too often or from multiple subscriptions at the same time. Contact support by using the provided link and include your subscription ID. |
| This offer is not available for purchasing by subscriptions belonging to Microsoft Azure Cloud Solution Providers. | Cloud Solution Provider (CSP) subscriptions can't purchase third-party model offerings. Consider using models offered as first-party consumption service. |