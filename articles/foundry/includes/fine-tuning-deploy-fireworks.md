---
title: Deploy fine-tuned models with Fireworks on Foundry (preview)
titleSuffix: Microsoft Foundry
description: Deploy a compatible fine-tuned model with Fireworks on Foundry from the Foundry portal.
author: chillatom
ms.author: coreyhill
ms.reviewer: mopeakande
ms.service: microsoft-foundry
ms.subservice: foundry-model-inference
ms.topic: include
ms.date: 10/07/2026
ms.custom: doc-kit-assisted, references_regions
ai-usage: ai-assisted
---

## Deploy with Fireworks on Foundry (preview)

[!INCLUDE [Feature preview](../includes/feature-preview.md)]

Deploy a compatible fine-tuned model with Fireworks on Foundry. For compatibility and deployment options, see the [fine-tuning overview](../fine-tuning/overview.md#deployment-options).

### Before you begin

- Have a fine-tuned model registered in Foundry and ready for Fireworks deployment.
- Ask a Subscription Owner or Subscription Contributor to [enable Fireworks on Foundry](../how-to/fireworks/enable-fireworks-models.md#enable-fireworks-on-foundry).
- Complete the [Fireworks permissions setup](../how-to/fireworks/enable-fireworks-models.md#prerequisites) and confirm sufficient quota in a supported region.

### Deploy in the portal

1. Open your project in the [Foundry portal](https://ai.azure.com).
1. Open the details view for your completed fine-tuning job, then select **Deploy**.
1. Choose **Fireworks**.
1. Enter a name for your deployment.
1. Choose an available [deployment type](../fine-tuning/overview.md#deployment-options) based on your requirements, and configure capacity within your available quota.
1. Review [pricing](https://aka.ms/oai/pricing) and the provider terms, then select **Deploy**.
1. Wait for model preparation and deployment to complete.

When deployment completes, open the [Foundry playground](../fine-tuning/deploy-fine-tuned-models.md#use-your-deployed-fine-tuned-model) and test your model.

If your model isn't registered and you have local model files, follow [Import custom models with Fireworks](../how-to/fireworks/import-custom-models.md). Don't upload an already registered model again.
