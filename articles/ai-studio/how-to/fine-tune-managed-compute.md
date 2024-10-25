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

This article explains how to use a user-managed compute fine-tune a machine learning model in Azure AI Studio. Fine-tuning involves adapting a pretrained model to a new, related task or domain. WHen you use a managed compute for fine-tuning, you use your computational resources to adjust training parameters such as learning rate, batch size, and number of training epochs to optimize the model's performance for a specific task. Fine-tuning a pretrained model to use for a related task is more efficient than building a new model, as it builds upon the pretrained model's existing knowledge and reduces the time and data needed for training.

To improve model performance, you might consider fine-tuning a foundation model with your training data. You can easily fine-tune foundation models by using either the fine-tune settings in AI Studio or by using code-based samples.

__Todo: link to the code-based samples__

## Prerequisites

- An Azure subscription with a valid payment method. Free or trial Azure subscriptions won't work. If you don't have an Azure subscription, create a [paid Azure account](https://azure.microsoft.com/pricing/purchase-options/pay-as-you-go) to begin.

- An [Azure AI Studio hub](create-azure-ai-resource.md).

- An [Azure AI Studio project](create-projects.md).

- Azure role-based access controls (Azure RBAC) are used to grant access to operations in Azure AI Studio. To perform the steps in this article, your user account must be assigned the __owner__ or __contributor__ role for the Azure subscription. 

## Fine-tune using user-managed compute in 

You can access the fine-tune settings form using one of the following methods:
1.    Choose the "Fine-Tuning" option from the left menu, and then select any foundation model.

2.    Choose the "Model Card" option from the left menu for any foundation model, and then click the 'Fine-tune' button on the model card.
Select the suitable Service method to fine-tune your model. You can choose between 'Hosted fine-tuning' or 'User-managed compute'. If you intend to use your own compute resources, select the 'User-managed compute' option. To learn more about Fine-tuning using Serverless API, refer to the related content articles.


  > [!NOTE]
  > Some foundation models support only the 'User-managed compute' option.

![Fine tune options in AI Studio](../media/how-to/fine-tuning-maap/fine-tune-options.png)

### Fine-tune Settings:

#### Basic Settings

- In the basic settings, provide a name for the fine-tuned model.

#### Compute

- Provide the Azure Machine Learning Compute cluster you would like to use for fine-tuning the model. Fine-tuning needs to run on GPU compute. Ensure that you have sufficient compute quota for the compute SKUs you wish to use.

![Fine tune compute in AI Studio](../media/how-to/fine-tuning-maap/fine-tune-compute.png)

#### Training Data

1.    Pass in the training data you would like to use to fine-tune your model. You can choose to either upload a local file (in JSONL, CSV or TSV format) or select an existing registered dataset from your workspace.

2.    Once you've selected the dataset, you need to map the columns from your input data, based on the schema needed for the task. For example: map the column names that correspond to the 'sentence' and 'label' keys for Text Classification.

![Fine tune training data in AI Studio](../media/how-to/fine-tuning-maap/fine-tune-training-data.png)


#### Validation data

- Pass in the data you would like to use to validate your model. Selecting Automatic split reserves an automatic split of training data for validation. Alternatively, you can provide a different validation dataset.

#### Test Parameters 

- Tuning hyperparameter is essential for optimizing large language models (LLMs) in real-world applications. It allows for improved performance and efficient resource usage. You can choose to keep the default settings or customize parameters like epochs or learning rate.

#### Review 

- Select Finish in the fine-tune form to submit your fine-tuning job. Once the job completes, you can view evaluation metrics for the fine-tuned model. You can then deploy this model to an endpoint for inferencing.

## Related Contents
- [Fine-tuning in Azure AI Studio - Azure AI Studio | Microsoft Learn](../concepts/fine-tuning-overview.md)
- [Deploy Phi-3 family of small language models with Azure AI Studio](../how-to/deploy-models-phi-3.md)