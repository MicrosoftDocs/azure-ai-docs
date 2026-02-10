---
title: Deploy Fine-Tuned Models with Managed Compute in Microsoft Foundry
titleSuffix: Microsoft Foundry
description: Deploy fine-tuned models using managed compute in Microsoft Foundry portal. Step-by-step guide to fine-tune, train, and deploy custom models with GPU compute resources.
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: how-to
ms.date: 08/15/2025
ms.reviewer: vkann
reviewer: kvijaykannan
ms.author: ssalgado
manager: nitinme
author: ssalgadodev
ms.custom: 
  - references_regions
  - hub-only
ai-usage: ai-assisted
#customer intent: As a data scientist using a managed compute, I want to learn how to fine-tune models to improve model performance for specific tasks. 
---

# Fine-tune models using managed compute (preview)

[!INCLUDE [classic-banner](../includes/classic-banner.md)]

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

Learn how to fine-tune and deploy models using managed compute in Microsoft Foundry. Adjust training parameters (learning rate, batch size, epochs) to optimize performance.

Fine-tuning a pretrained model for a related task is more efficient than training a new model from scratch.

Use the fine-tune settings in the portal to configure data, compute, and hyperparameters. After training completes you can evaluate and deploy the resulting model.

In this article, you learn how to:

- Select a foundation model.
- Configure compute and data splits.
- Tune hyperparameters safely.
- Submit and monitor a fine-tune job.
- Evaluate and deploy the fine-tuned model.


## Prerequisites

[!INCLUDE [hub-only-prereq](../includes/hub-only-prereq.md)]

- Azure role-based access controls (Azure RBAC) are used to grant access to operations in Foundry portal. To perform the steps in this article, your user account must be assigned the __owner__ or __contributor__ role for the Azure subscription. For more information on permissions, see [Role-based access control in Foundry portal](../concepts/rbac-foundry.md).

## Fine-tune a foundation model using managed compute

[!INCLUDE [tip-left-pane](../includes/tip-left-pane.md)]

1. [!INCLUDE [classic-sign-in](../includes/classic-sign-in.md)]

1. If you're not already in your project, select it. 
1. Select **Fine-tuning** from the left pane.

    1. Select **Fine-tune a model** and add the model that you want to fine-tune. This article uses _Phi-3-mini-4k-instruct_ for illustration.
    1. Select **Next** to see the available fine-tune options. Some foundation models support only the __Managed compute__ option.

1. Alternatively, you could select **Model catalog** from the left sidebar of your project and find the model card of the foundation model that you want to fine-tune.

    1. Select __Fine-tune__ on the model card to see the available fine-tune options. Some foundation models support only the __Managed compute__ option.

    :::image type="content" source="../media/how-to/fine-tune-managed-compute/fine-tune-options.png" alt-text="Screenshot showing fine-tuning options for a foundation model in Foundry." lightbox="../media/how-to/fine-tune-managed-compute/fine-tune-options.png":::

1. Select **Managed compute**. This opens **Basic settings**.

### Configure fine-tune settings

In this section, you go through the steps to configure fine-tuning for your model, using a managed compute.

1. Provide a model name (for example, `phi3mini-faq-v1`). Select **Next** for **Compute**.

1. Select a GPU VM size. Ensure quota for the chosen SKU.

    :::image type="content" source="../media/how-to/fine-tune-managed-compute/fine-tune-compute.png" alt-text="Screenshot showing settings for the compute to use for fine-tuning." lightbox="../media/how-to/fine-tune-managed-compute/fine-tune-compute.png":::

1. Select **Next** for **Training data**. Task type may be preset (for example, **Chat completion**). 

1. Provide training data (upload JSONL/CSV/TSV or select a registered dataset). Balance examples to reduce bias.

1. Select **Next** for **Validation data**. Keep **Automatic split** or supply a separate dataset.

1. Select **Next** for **Task parameters**. Adjust epochs, learning rate, batch size. Start conservative; iterate based on validation metrics.

1. Select **Next** for **Review**. Confirm counts and parameters.

1. Select **Submit** to start the job.

### Monitor and evaluate

- Track job status in the fine-tuning jobs list.
- Review logs for preprocessing or allocation issues.
- After completion, view generated evaluation metrics (if enabled) or run a separate evaluation comparing base vs fine-tuned model.

### Deploy the fine-tuned model

Deploy from the job summary. Use a deployment name like `faq-v1`. Record model version and dataset hash for reproducibility. Add tracing to monitor real requests.

### Troubleshooting

| Issue | Cause | Action |
|-------|-------|-------|
| Stuck in Queued | Insufficient GPU capacity | Try alternate SKU or region |
| Overfitting quickly | Too many epochs / small dataset | Reduce epochs or expand data |
| No metric improvement | Dataset noise / misaligned objective | Refine labeling or metric selection |
| Higher latency post deploy | Larger base model / adapter overhead | Consider smaller base model or tune batch size |

## Related content

- [Fine-tune models overview](../concepts/fine-tuning-overview.md)
- [Generate chat completions](../openai/api-version-lifecycle.md)
- [Featured models](../concepts/models-inference-examples.md)