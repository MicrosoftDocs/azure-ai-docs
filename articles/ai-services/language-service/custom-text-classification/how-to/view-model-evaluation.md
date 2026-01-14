---
title: View a custom text classification model evaluation - Foundry Tools
titleSuffix: Foundry Tools
description: Learn how to view the evaluation scores for a custom text classification model
#services: cognitive-services
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: how-to
ms.date: 12/15/2025
ms.author: lajanuar
ms.custom: language-service-custom-classification
---
# View your text classification model's evaluation and details

After your model has finished training, you can view the model performance and see the predicted classes for the documents in the test set. 

> [!NOTE]
> Using the **Automatically split the testing set from training data** option may result in different model evaluation result every time you [train a new model](train-model.md), as the test set is selected randomly from the data. To make sure that the evaluation is calculated on the same test set every time you train a model, make sure to use the **Use a manual split of training and testing data** option when starting a training job and define your **Test** documents when [labeling data](tag-data.md).

## Prerequisites

Before viewing model evaluation you need:

* [A custom text classification project](create-project.md) with a configured Azure blob storage account.
* Text data that has [been uploaded](design-schema.md#data-preparation) to your storage account.
* [Labeled data](tag-data.md)
* A successfully [trained model](train-model.md)

See the [project development lifecycle](../overview.md#project-development-lifecycle).

## Model details (REST API)

### Single label classification
[!INCLUDE [Model evaluation](../includes/rest-api/model-evaluation-single-label.md)]

### Multi label classification 

[!INCLUDE [Model evaluation](../includes/rest-api/model-evaluation-multi-label.md)]


## Load or export model data (REST API)

[!INCLUDE [Load export model](../includes/rest-api/load-export-model.md)]


## Delete model (REST API)

[!INCLUDE [Delete model](../includes/rest-api/delete-model.md)]

## Next steps

As you review your how your model performs, learn about the [evaluation metrics](../concepts/evaluation-metrics.md) that are used. Once you know whether your model performance needs to improve, you can begin improving the model.
