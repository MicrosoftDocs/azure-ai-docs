---
title: How to train your custom text classification model - Foundry Tools
titleSuffix: Foundry Tools
description: Learn about how to train your model for custom text classification.
#services: cognitive-services
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: how-to
ms.date: 11/18/2025
ms.author: lajanuar
ms.custom: language-service-custom-classification
---
# How to train a custom text classification model

Training is the process where the model learns from your [labeled data](tag-data.md). After training is completed, you can [view the model's performance](view-model-evaluation.md) to determine if you need to improve your model.

To train a model, start a training job. Only successfully completed jobs create a usable model. Training jobs expire after seven days. After this period, you won't be able to retrieve the job details. If your training job completed successfully and a model was created, the job expiration isn't affected. You can only have one training job running at a time, and you can't start other jobs in the same project. 

Depending on the dataset size and the complexity of your schema, training times can vary from a few minutes up to several hours.



## Prerequisites

Before you train your model, you need:

* [A successfully created project](create-project.md) with a configured Azure blob storage account, 
* Text data that is [uploaded](design-schema.md#data-preparation) to your storage account.
* [Labeled data](tag-data.md)

See the [project development lifecycle](../overview.md#project-development-lifecycle).

## Data splitting

Before you start the training process, labeled documents in your project are divided into a training set and a testing set. Each one of them serves a different function.
The **training set** is used in training the model and where the model learns the class/classes assigned to each document. 
The **testing set** is a blind set that isn't introduced to the model during training but only during evaluation. 
After the model is trained successfully, it can make predictions from the documents in the testing set. Based on these predictions, the model's [evaluation metrics](../concepts/evaluation-metrics.md) are calculated. 
We recommend making sure that all your classes are adequately represented in both the training and testing set.

Custom text classification supports two methods for data splitting:

* **Automatically splitting the testing set from training data**: The system splits your labeled data between the training and testing sets, according to the percentages you choose. The system attempts to have a representation of all classes in your training set. The recommended percentage split is 80% for training and 20% for testing. 

 > [!NOTE]
 > If you choose the **Automatically splitting the testing set from training data** option, only the data assigned to training set is split according to the percentages provided.

* **Use a manual split of training and testing data**: This method enables users to define which labeled documents should belong to which set. This step is only enabled if you added documents to your testing set during [data labeling](tag-data.md).

## Train model with REST API


### Start training job

[!INCLUDE [train model](../includes/rest-api/train-model.md)]

### Get training job status

Training could take sometime depending on the size of your training data and complexity of your schema. You can use the following request to keep polling the status of the training job until successfully completed.

 [!INCLUDE [get training model status](../includes/rest-api/get-training-status.md)]


### Cancel training job with REST API

[!INCLUDE [Cancel training](../includes/rest-api/cancel-training.md)]


## Next steps

After training is completed, you're able to [view the model's performance](view-model-evaluation.md) to optionally improve your model if needed. Once you're satisfied with your model, you can deploy it, making it available to use for [classifying text](call-api.md).
