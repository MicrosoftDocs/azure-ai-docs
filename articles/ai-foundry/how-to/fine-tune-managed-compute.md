---
title: Fine-tune models using a managed compute with Azure AI Foundry portal (preview)
titleSuffix: Azure AI Foundry
description: Learn how to fine-tune models using a managed compute with Azure AI Foundry.
manager: scottpolly
ms.service: azure-ai-foundry
ms.topic: how-to
ms.date: 04/25/2025
ms.reviewer: vkann
reviewer: kvijaykannan
ms.author: mopeakande
author: msakande
ms.custom: references_regions

#customer intent: As a data scientist using a managed compute, I want to learn how to fine-tune models to improve model performance for specific tasks. 
---

# Fine-tune models using managed compute (preview)

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

This article explains how to use a managed compute to fine-tune a model in the Azure AI Foundry portal. Fine-tuning involves adapting a pretrained model to a new, related task or domain. When you use a managed compute for fine-tuning, you use your computational resources to adjust training parameters such as learning rate, batch size, and number of training epochs to optimize the model's performance for a specific task. 

Fine-tuning a pretrained model to use for a related task is more efficient than building a new model, as fine-tuning builds upon the pretrained model's existing knowledge and reduces the time and data needed for training.

To improve model performance, you might consider fine-tuning a foundation model with your training data. You can easily fine-tune foundation models by using the fine-tune settings in the Azure AI Foundry portal.


## Prerequisites

[!INCLUDE [hub-only-prereq](../includes/hub-only-prereq.md)]

- Azure role-based access controls (Azure RBAC) are used to grant access to operations in Azure AI Foundry portal. To perform the steps in this article, your user account must be assigned the __owner__ or __contributor__ role for the Azure subscription. For more information on permissions, see [Role-based access control in Azure AI Foundry portal](../concepts/rbac-azure-ai-foundry.md).

## Fine-tune a foundation model using managed compute

[!INCLUDE [tip-left-pane](../includes/tip-left-pane.md)]

1. Sign in to [Azure AI Foundry](https://ai.azure.com).

1. If you're not already in your project, select it. 
1. Select **Fine-tuning** from the left pane.

    1. Select **Fine-tune model** and add the model that you want to fine-tune. This article uses _Phi-3-mini-4k-instruct_ for illustration.
    1. Select **Next** to see the available fine-tune options. Some foundation models support only the __Managed compute__ option.

1. Alternatively, you could select **Model catalog** from the left sidebar of your project and find the model card of the foundation model that you want to fine-tune.

    1. Select __Fine-tune__ on the model card to see the available fine-tune options. Some foundation models support only the __Managed compute__ option.

    :::image type="content" source="../media/how-to/fine-tune-managed-compute/fine-tune-options.png" alt-text="Screenshot showing fine-tuning options for a foundation model in Azure AI Foundry." lightbox="../media/how-to/fine-tune-managed-compute/fine-tune-options.png":::

1. Select __Managed compute__ to use your personal compute resources. This action opens up the "Basic settings" page of a window for specifying the fine-tuning settings.

### Configure fine-tune settings

In this section, you go through the steps to configure fine-tuning for your model, using a managed compute.

1. Provide a name for the fine-tuned model on the "Basic settings" page, and select **Next** to go to the "Compute" page.

1. Select the Azure Machine Learning compute cluster to use for fine-tuning the model. Fine-tuning runs on GPU compute. Ensure that you have sufficient compute quota for the compute SKUs you plan to use.

    :::image type="content" source="../media/how-to/fine-tune-managed-compute/fine-tune-compute.png" alt-text="Screenshot showing settings for the compute to use for fine-tuning." lightbox="../media/how-to/fine-tune-managed-compute/fine-tune-compute.png":::

1. Select **Next** to go to the "Training data" page. On this page, the "Task type" is preselected as **Chat completion**.

1. Provide the training data to use to fine-tune your model. You can choose to either upload a local file (in JSONL, CSV or TSV format) or select an existing registered dataset from your project.

1. Select **Next** to go to the "Validation data" page. Keep the **Automatic split of training data** selection to reserve an automatic split of training data for validation. Alternatively, you could provide a different validation dataset by uploading a local file (in JSONL, CSV or TSV format) or selecting an existing registered dataset from your project.

1. Select **Next** to go to the "Task parameters" page. Tuning hyperparameters is essential for optimizing large language models (LLMs) in real-world applications. It allows for improved performance and efficient resource usage. You can choose to keep the default settings or customize parameters like epochs or learning rate.

1. Select **Next** to go to the "Review" page and check that all the settings look good.

1. Select **Submit** to submit your fine-tuning job. Once the job completes, you can view evaluation metrics for the fine-tuned model. You can then deploy this model to an endpoint for inferencing.

## Related Contents

- [Fine-tune models with Azure AI Foundry](../concepts/fine-tuning-overview.md)
- [How to generate chat completions with Azure AI Foundry Models](../model-inference/how-to/use-chat-completions.md?context=/azure/ai-foundry/context/context)
- [Featured models of Azure AI Foundry](../concepts/models-featured.md)
