---
title: How to create Custom sentiment analysis projects
titleSuffix: Azure AI services
description: Learn about the steps for using Azure resources with Custom sentiment analysis.
#services: cognitive-services
author: jboback
manager: nitinme
ms.service: azure-ai-language
ms.topic: how-to
ms.date: 11/21/2024
ms.author: jboback
ms.custom: language-service-custom-classification, references_regions
---

# How to create Custom sentiment analysis project

Use this article to learn how to set up the requirements for starting with Custom sentiment analysis and create a project.

## Prerequisites

Before you start using Custom sentiment analysis, you'll need:

* An Azure subscription - [Create one for free](https://azure.microsoft.com/free/cognitive-services).

## Create a Language resource 

Before you start using Custom sentiment analysis, you'll need an Azure Language resource. It's recommended to create your Language resource and connect a storage account to it in the Azure portal. Creating a resource in the Azure portal lets you create an Azure storage account at the same time, with all of the required permissions preconfigured. You can also read further in the article to learn how to use a pre-existing resource, and configure it to work with Custom sentiment analysis.

You also need an Azure storage account where you'll upload your `.txt` documents that will be used to train a model to classify text.

> [!NOTE]
>  * You need to have an **owner** role assigned on the resource group to create a Language resource.
>  * If you will connect a pre-existing storage account, you should have an **owner** role assigned to it.

## Create Language resource and connect storage account


> [!Note]
> You shouldn't move the storage account to a different resource group or subscription once it's linked with the Language resource.

[!INCLUDE [create a new resource from the Azure portal](../../../includes/custom/resource-creation-azure-portal.md)]

[!INCLUDE [create a new resource from Language Studio](../../../includes/custom/resource-creation-language-studio.md)]

[!INCLUDE [create a new resource with Azure PowerShell](../../../includes/custom/resource-creation-powershell.md)]


---

> [!NOTE]
> * The process of connecting a storage account to your Language resource is irreversible, it cannot be disconnected later.
> * You can only connect your language resource to one storage account.

## Using a pre-existing Language resource

[!INCLUDE [use an existing resource](../../../includes/custom/use-pre-existing-resource.md)]


## Create a Custom sentiment analysis project

Once your resource and storage container are configured, create a new Custom sentiment analysis project. A project is a work area for building your custom AI models based on your data. Your project can only be accessed by you and others who have access to the Azure resource being used. If you have labeled data, you can [import it](#import-a-custom-sentiment-analysis-project) to get started.

### [Language Studio](#tab/studio)

[!INCLUDE [Language Studio project creation](../../../includes/custom/language-studio/create-project.md)]


### [REST APIs](#tab/apis)

[!INCLUDE [REST APIs project creation](../../includes/custom/rest-api/create-project.md)]

---

## Import a Custom sentiment analysis project

<!--If you have already labeled data, you can use it to get started with the service. Make sure that your labeled data follows the [accepted data formats](../concepts/data-formats.md).-->

### [Language Studio](#tab/studio)

[!INCLUDE [Import project](../../../includes/custom/language-studio/import-project.md)]

### [REST APIs](#tab/apis)

[!INCLUDE [Import project](../../includes/custom/rest-api/import-project.md)]

---

## Get project details

### [Language Studio](#tab/studio)

[!INCLUDE [Language Studio project details](../../../includes/custom/language-studio/project-details.md)]

### [REST APIs](#tab/apis)

[!INCLUDE [REST API project details](../../includes/custom/rest-api/project-details.md)]

---

## Delete project

### [Language Studio](#tab/studio)

[!INCLUDE [Delete project using Language Studio](../../../includes/custom/language-studio/delete-project.md)]

### [REST APIs](#tab/apis)

[!INCLUDE [Delete project using the REST API](../../includes/custom/rest-api/delete-project.md)]

---

## Next steps

* [Sentiment analysis overview](../../overview.md)
<!--* You should have an idea of the [project schema](design-schema.md) you will use to label your data.

* After your project is created, you can start [labeling your data](tag-data.md), which will inform your text classification model how to interpret text, and is used for training and evaluation.-->
