---
title: How to train your Custom Named Entity Recognition (NER) model
titleSuffix: Foundry Tools
description: Learn about how to train your model for Custom Named Entity Recognition (NER).
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: how-to
ms.date: 11/18/2025
ms.author: lajanuar
ms.custom: language-service-custom-ner
---
# Train your custom named entity recognition model

Training is the process where the model learns from your [labeled data](tag-data.md). After training is completed, you'll be able to view the [model's performance](view-model-evaluation.md) to determine if you need to improve your model.

To train a model, you start a training job and only successfully completed jobs create a model. Training jobs expire after seven days, which means you won't be able to retrieve the job details after this time. If your training job completed successfully and a model was created, the model isn't affected. You can only have one training job running at a time, and you can't start other jobs in the same project. 

The training times vary. Training can be anywhere from a few minutes, when dealing with few documents, or several hours, depending on the dataset size and the complexity of your schema.


## Prerequisites

* A successfully [created project](create-project.md) with a configured Azure blob storage account
* Text data [uploaded](design-schema.md#data-preparation) to your storage account.
* [Labeled data](tag-data.md)

See the [project development lifecycle](../overview.md#project-development-lifecycle).

## Data splitting

Before you start the training process, labeled documents in your project are divided into a training set and a testing set. Each one of them serves a different function.
The **training set** is used in training the model. It's the set from which the model learns the labeled entities and what spans of text are to be extracted as entities. 
The **testing set** is a blind set that isn't introduced to the model during training but only during evaluation. 
After model training is completed successfully, the model is used to make predictions from the test documents and [evaluation metrics](../concepts/evaluation-metrics.md) are calculated. 
We recommend that you make sure that all your entities are adequately represented in both the training and testing set.

Custom NER supports two methods for data splitting:

* **Automatically splitting the testing set from training data**: The system splits your labeled data between the training and testing sets, according to the percentages you choose. The recommended percentage split is 80% for training and 20% for testing. 

 > [!NOTE]
 > If you choose the **Automatically splitting the testing set from training data** option, only the data assigned to a training set is split according to the percentages provided.

* **Use a manual split of training and testing data**: This method enables users to define which labeled documents should belong to which set. This step is only enabled if you added documents to your testing set during [data labeling](tag-data.md).

## Train model (REST API)

Once you have labeled your data and configured your data split settings, you can start training your custom NER model using the REST API. The training process involves submitting a training job request and monitoring its progress until completion. This section provides the API calls needed to initiate training and check the status of your training job.

### Start training job

[!INCLUDE [train model](../includes/rest-api/train-model.md)]

### Get training job status (REST API)

Training can take some time, depending on the size of your training data and complexity of your schema. You can use the following request to keep polling the status of the training job until successful completion.

 [!INCLUDE [get training model status](../includes/rest-api/get-training-status.md)]


### Cancel training job (REST API)

If you need to stop a training job that's currently in progress, you can cancel it using the REST API. Canceling a training job is useful when you discover an issue with your data or configuration and want to make corrections before restarting the training process.

[!INCLUDE [Cancel training](../includes/rest-api/cancel-training.md)]

## Next steps

After training is completed, you'll be able to view [model performance](view-model-evaluation.md) to optionally improve your model if needed. Once you're satisfied with your model, you can deploy it, making it available to use for [extracting entities](call-api.md) from text.
