---
title: Preparing data and designing a schema for custom named entity recognition (NER)
titleSuffix: Foundry Tools
description: Learn about how to select and prepare data, to be successful in creating custom NER projects.
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: how-to
ms.date: 11/18/2025
ms.author: lajanuar
ms.custom: language-service-custom-ner
---
# How to prepare data and define a schema for custom NER

In order to create a custom NER model, you need quality data to train it. This article covers how you should select and prepare your data, along with defining a schema. Defining the schema is the first step in [project development lifecycle](../overview.md#project-development-lifecycle), and it defines the entity types/categories that you need your model to extract from the text at runtime.

## Schema design

The schema defines the entity types/categories that you need your model to extract from text at runtime. 

* Review documents in your dataset to be familiar with their format and structure.

* Identify the [entities](../glossary.md#entity) you want to extract from the data.

    For example, if you're extracting entities from support emails, you might need to extract "Customer name," "Product name," "Request date," and "Contact information."

* Avoid entity types ambiguity.

    **Ambiguity** happens when entity types you select are similar to each other. The more ambiguous your schema the more labeled data you need to differentiate between different entity types.

    For example, if you're extracting data from a legal contract, to extract "Name of first party" and "Name of second party" you need to add more examples to overcome ambiguity since the names of both parties look similar. Avoid ambiguity as it saves time, effort, and yields better results.

* Avoid complex entities. Complex entities can be difficult to pick out precisely from text. Consider breaking it down into multiple entities.

    For example, extracting "Address" would be challenging if not broken down into smaller entities. There are so many variations of how addresses appear, it would take large number of labeled entities to teach the model to extract an address, as a whole, without breaking it down. However, if you replace "Address" with "Street Name," "PO Box," "City," "State" and "Zip," the model requires fewer labels per entity.

## Data selection

The quality of data you train your model with affects model performance greatly.

* Use real-life data that reflects your domain's problem space to effectively train your model. You can use synthetic data to accelerate the initial model training process, but it differs from your real-life data and make your model less effective when used.

* Balance your data distribution as much as possible without deviating far from the distribution in real-life.

* Use diverse data whenever possible to avoid overfitting your model. Less diversity in training data may lead to your model learning spurious correlations that may not exist in real-life data. 
 
* Avoid duplicate documents in your data. Duplicate data has a negative effect on the training process, model metrics, and model performance. 

* Consider where your data comes from. If you're collecting data from one person, department, or part of your scenario, you're likely missing diversity that may be important for your model to learn about. 

> [!NOTE]
> If your documents are in multiple languages, select the **enable multi-lingual** option during [project creation](../quickstart.md) and set the **language** option to the language of most your documents.

## Data preparation

As a prerequisite for creating a project, your training data needs to be uploaded to a blob container in your storage account. You can create and upload training documents from Azure directly, or through using the Azure Storage Explorer tool. Using the Azure Storage Explorer tool allows you to upload more data quickly.  

* [Create and upload documents from Azure](/azure/storage/blobs/storage-quickstart-blobs-portal#create-a-container)
* [Create and upload documents using Azure Storage Explorer](/azure/vs-azure-tools-storage-explorer-blobs)

You can only use `.txt` documents. If your data is in other format, you can use [CLUtils parse command](https://github.com/microsoft/CognitiveServicesLanguageUtilities/blob/main/CustomTextAnalytics.CLUtils/Solution/CogSLanguageUtilities.ViewLayer.CliCommands/Commands/ParseCommand/README.md) to change your document format.

You can upload an annotated dataset, or you can upload an unannotated one and label your data.
 
## Test set

When defining the testing set, make sure to include example documents that aren't present in the training set. Defining the testing set is an important step to calculating the [model performance](view-model-evaluation.md#model-details-rest-api). Also, make sure that the testing set includes documents that represent all entities used in your project.

## Next steps

If you haven't already, create a custom NER project. If it's your first time using custom NER, consider following the [quickstart](../quickstart.md) to create an example project. For more information, *see* the [how-to article](../how-to/create-project.md).
