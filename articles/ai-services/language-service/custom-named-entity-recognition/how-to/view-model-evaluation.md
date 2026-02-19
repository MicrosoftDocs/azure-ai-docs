---
title: Evaluate a Custom Named Entity Recognition (NER) model
titleSuffix: Foundry Tools
description: Learn how to evaluate and score your Custom Named Entity Recognition (NER) model
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: how-to
ms.date: 11/18/2025
ms.author: lajanuar
ms.custom: language-service-custom-ner
---
# View the custom NER model's evaluation and details

After your model finishes training, you can view the model performance and see the extracted entities for the documents in the test set. 

> [!NOTE]
> Using the **Automatically split the testing set from training data** option may result in different model evaluation result every time you [train a new model](train-model.md), as the test set is selected randomly from the data. To make sure that the evaluation is calculated on the same test set every time you train a model, make sure to use the **Use a manual split of training and testing data** option when starting a training job and define your **Test** documents when [labeling data](tag-data.md).

## Prerequisites

Before viewing model evaluation, you need:

* A successfully [created project](create-project.md) with a configured Azure blob storage account.
* Text data [uploaded](design-schema.md#data-preparation) to your storage account.
* [Labeled data](tag-data.md)
* A [successfully trained model](train-model.md)

For more information, *see* the [project development lifecycle](../overview.md#project-development-lifecycle).

## Model details (REST API)

[!INCLUDE [Model evaluation](../includes/rest-api/model-evaluation.md)]


## Load or export model data (REST API)

[!INCLUDE [Load export model](../includes/rest-api/load-export-model.md)]

## Delete model (REST API)

[!INCLUDE [Delete model](../includes/rest-api/delete-model.md)]

## Next steps

* [Deploy your model](deploy-model.md)
* Learn about the [metrics used in evaluation](../concepts/evaluation-metrics.md). 
