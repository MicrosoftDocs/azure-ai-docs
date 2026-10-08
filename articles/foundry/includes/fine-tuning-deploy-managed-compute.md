---
title: Deploy fine-tuned models with Managed Compute (preview)
titleSuffix: Microsoft Foundry
description: Deploy a compatible fine-tuned model with Managed Compute in Microsoft Foundry.
author: chillatom
ms.author: coreyhill
ms.reviewer: mopeakande
ms.service: microsoft-foundry
ms.subservice: foundry-model-inference
ms.topic: include
ms.date: 10/07/2026
ms.custom: doc-kit-assisted
ai-usage: ai-assisted
---

## Deploy with Managed Compute (preview)

[!INCLUDE [Feature preview](../includes/feature-preview.md)]

Deploy a compatible fine-tuned model with Managed Compute. For compatibility and deployment options, see the [fine-tuning overview](../fine-tuning/overview.md#deployment-options).

### Before you begin

- Have a fine-tuned adapter that matches the base model and version.
- Have a base deployment that uses a LoRA-enabled deployment template. If you need to create one, follow [Deploy open-source models with Managed Compute](../how-to/deploy-models-managed.md#deploy-the-model).
- Complete the [Managed Compute permissions and quota setup](../how-to/deploy-models-managed.md#prerequisites).

### Deploy in the portal

1. Open your project in the [Foundry portal](https://ai.azure.com).
1. Open the details view for your completed fine-tuning job, then select **Deploy**.
1. Choose **Managed Compute**.
1. Enter a name for your deployment.
1. Select the compatible base deployment.
1. Review the configuration and select **Deploy**.
1. Wait for deployment to complete.

When deployment completes, open the [Foundry playground](../fine-tuning/deploy-fine-tuned-models.md#use-your-deployed-fine-tuned-model) and test your model.
