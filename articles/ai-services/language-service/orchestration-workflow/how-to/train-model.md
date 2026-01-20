---
title: How to train and evaluate models in orchestration workflow
description: Learn how to train a model for orchestration workflow projects.
titleSuffix: Foundry Tools
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: how-to
ms.date: 11/18/2025
ms.author: lajanuar
ms.custom: language-service-orchestration
---
# Train your orchestration workflow model

Training is the process where the model learns from your [labeled utterances](tag-utterances.md). After training is completed, you can [view model performance](view-model-evaluation.md).

To train a model, start a training job. Only successfully completed jobs create a model. Training jobs expire after seven days, after this time you can no longer be able to retrieve the job details. If your training job completed successfully and a model is created, it isn't affected if the job expires. You can only have one training job running at a time, and you can't start other jobs in the same project. 

The training times can be anywhere from a few seconds when dealing with simple projects, up to a couple of hours when you reach the [maximum limit](../service-limits.md) of utterances.

Model evaluation is triggered automatically after training is completed successfully. The evaluation process starts by using the trained model to run predictions on the utterances in the testing set, and compares the predicted results with the provided labels (which establishes a baseline of truth). The results are returned so you can review the [model's performance](view-model-evaluation.md).

## Prerequisites

* A successfully [created project](create-project.md) with a configured Azure blob storage account

See the [project development lifecycle](../overview.md#project-development-lifecycle).

## Data splitting

Before you start the training process, labeled utterances in your project are divided into a training set and a testing set. Each one of them serves a different function.
The **training set** is used in training the model. It's the set from which the model learns the labeled utterances. 
The **testing set** is a blind set that isn't introduced to the model during training but only during evaluation. 

After the model is trained successfully, the model can be used to make predictions from the utterances in the testing set. These predictions are used to calculate [evaluation metrics](../concepts/evaluation-metrics.md).

We recommend that all your intents are adequately represented in both the training and testing set.

Orchestration workflow supports two methods for data splitting:

* **Automatically splitting the testing set from training data**: The system splits your tagged data between the training and testing sets, according to the percentages you choose. The recommended percentage split is 80% for training and 20% for testing. 

 > [!NOTE]
 > If you choose the **Automatically splitting the testing set from training data** option, only the data assigned to training set is split according to the percentages provided.

* **Use a manual split of training and testing data**: This method enables users to define which utterances should belong to which set. This step is only enabled if you added utterances to your testing set during [labeling](tag-utterances.md).

> [!Note]
> You can only add utterances in the training dataset for non-connected intents only.


## Train model 

### Start training job

[!INCLUDE [train model](../includes/rest-api/train-model.md)]

### Get training job status

Training could take sometime depending on the size of your training data and complexity of your schema. You can use the following request to keep polling the status of the training job until it successfully completes.

[!INCLUDE [get training model status](../includes/rest-api/get-training-status.md)]

### Cancel training job

[!INCLUDE [Cancel training](../includes/rest-api/cancel-training.md)]

---

## Next steps
* [Model evaluation metrics concepts](../concepts/evaluation-metrics.md)
* How to [deploy a model](./deploy-model.md)
