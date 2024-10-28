---
title: Fine-tune models using a user-managed compute with Azure AI Studio
titleSuffix: Azure AI Studio
description: Learn how to fine-tune models using a user-managed compute with Azure AI Studio.
manager: scottpolly
ms.service: azure-ai-studio
ms.topic: how-to
ms.date: 10/25/2024
ms.reviewer: vkann
reviewer: kvijaykannan
ms.author: mopeakande
author: msakande
ms.custom: references_regions

#customer intent: As a data scientist using a user-managed compute, I want to learn how to fine-tune models to improve model performance for specific tasks. 
---

# Fine-tune models using user-managed compute

This article explains how to use a user-managed compute to fine-tune a foundation model in Azure AI Studio. Fine-tuning involves adapting a pretrained model to a new, related task or domain. When you use a managed compute for fine-tuning, you use your computational resources to adjust training parameters such as learning rate, batch size, and number of training epochs to optimize the model's performance for a specific task. Fine-tuning a pretrained model to use for a related task is more efficient than building a new model, as it builds upon the pretrained model's existing knowledge and reduces the time and data needed for training.

To improve model performance, you might consider fine-tuning a foundation model with your training data. You can easily fine-tune foundation models by using either the fine-tune settings in AI Studio or by using code-based samples.

__Todo: link to the code-based samples__

## Prerequisites

- An Azure subscription with a valid payment method. Free or trial Azure subscriptions won't work. If you don't have an Azure subscription, create a [paid Azure account](https://azure.microsoft.com/pricing/purchase-options/pay-as-you-go) to begin.

- An [Azure AI Studio hub](create-azure-ai-resource.md).

- An [Azure AI Studio project](create-projects.md).

- Azure role-based access controls (Azure RBAC) are used to grant access to operations in Azure AI Studio. To perform the steps in this article, your user account must be assigned the __owner__ or __contributor__ role for the Azure subscription. For more information on permissions, see [Role-based access control in Azure AI Studio](../concepts/rbac-ai-studio.md).

## Fine-tune a foundation model using managed compute

1. Sign in to [Azure AI Studio](https://ai.azure.com).
1. Select **Fine-tuning** from the left sidebar and add the foundation model that you want to finetune.
1. Alternatively, you could select **Model catalog** from the left sidebar and find the model card of the foundation model that you want to finetune.
1. Select __Fine-tune__ on the model card to see the available fine-tune options. Some foundation models support only the __User-managed compute__ option.
1. Select the __User-managed compute__ option to use your personal compute resources. This action opens up a window where you can specify the fine-tuning settings.

  :::image type="content" source="../media/how-to/fine-tune-managed-compute/fine-tune-options.png" alt-text="Screenshot showing fine-tuning options for a foundation model in AI Studio." lightbox="../media/how-to/fine-tune-managed-compute/fine-tune-options.png":::

### Configure fine-tune settings

In this section, you go through the steps to configure fine-tuning for your model, using a managed compute.

#### Basic settings

1. Provide a name for the fine-tuned model on the "Basic settings" page.

#### Compute

1. Provide the Azure Machine Learning compute cluster to use for fine-tuning the model. Fine-tuning runs on GPU compute. Ensure that you have sufficient compute quota for the compute SKUs you plan to use.

  :::image type="content" source="../media/how-to/fine-tune-managed-compute/fine-tune-compute.png" alt-text="Screenshot showing settings for the compute to use for fine-tuning." lightbox="../media/how-to/fine-tune-managed-compute/fine-tune-compute.png":::

#### Training data

1. Provide the training data to use to fine-tune your model. You can choose to either upload a local file (in JSONL, CSV or TSV format) or select an existing registered dataset from your workspace.

1. Map the columns from your input data, based on the schema needed for the task. For example, map the column names that correspond to the _sentence_ and _label_ keys for text classification.

:::image type="content" source="../media/how-to/fine-tune-managed-compute/fine-tune-training-data.png" alt-text="Screenshot showing settings for the training data to use for fine-tuning." lightbox="../media/how-to/fine-tune-managed-compute/fine-tune-training-data.png":::

#### Validation data

1. Provide the data to use to validate your model. Selecting __Automatic split__ reserves an automatic split of training data for validation. Alternatively, you can provide a different validation dataset.

#### Task parameters

1. Tuning hyperparameter is essential for optimizing large language models (LLMs) in real-world applications. It allows for improved performance and efficient resource usage. You can choose to keep the default settings or customize parameters like epochs or learning rate.

#### Review

1. Select __Finish__ in the fine-tune form to submit your fine-tuning job. Once the job completes, you can view evaluation metrics for the fine-tuned model. You can then deploy this model to an endpoint for inferencing.

## Related Contents
- [Fine-tuning in Azure AI Studio - Azure AI Studio | Microsoft Learn](../concepts/fine-tuning-overview.md)
- [Deploy Phi-3 family of small language models with Azure AI Studio](../how-to/deploy-models-phi-3.md)