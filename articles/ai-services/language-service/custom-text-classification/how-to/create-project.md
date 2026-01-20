---
title: How to create custom text classification projects
titleSuffix: Foundry Tools
description: Learn about the steps for using Azure resources with custom text classification.
#services: cognitive-services
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: how-to
ms.date: 12/18/2025
ms.author: lajanuar
ms.custom: language-service-custom-classification, references_regions
---
# How to create custom text classification project

Use this article to learn how to set up the requirements for starting with custom text classification and create a project.

## Prerequisites

Before you start using custom text classification, you need:

* An Azure subscription - [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

## Create a Language resource 

Before you start using custom text classification, you need an Azure Language in Foundry Tools resource. We recommended that you create your Language resource and connect a storage account to it in the Azure portal. Creating a resource in the Azure portal lets you create an Azure storage account at the same time, with all of the required permissions preconfigured. You can also read further in the article to learn how to use a preexisting resource, and configure it to work with custom text classification.

You also need an Azure storage account where to upload your `.txt` documents that are used to train a model to classify text.

> [!NOTE]
>  * You need to have an **owner** role assigned on the resource group to create a Language resource.
>  * If you connect a preexisting storage account, you should have an **owner** role assigned to it.

## Create Language resource and connect storage account


> [!Note]
> You shouldn't move the storage account to a different resource group or subscription once it's linked with Azure Language resource.

### [Using the Azure portal](#tab/azure-portal)

[!INCLUDE [create a new resource from the Azure portal](../includes/resource-creation-azure-portal.md)]

### [Using Azure PowerShell](#tab/azure-powershell)

[!INCLUDE [create a new resource with Azure PowerShell](../includes/resource-creation-powershell.md)]

---

> [!NOTE]
> * The process of connecting a storage account to your Language resource is irreversible—it can't be disconnected later.
> * You can only connect your language resource to one storage account.

## Using a preexisting Language resource

[!INCLUDE [use an existing resource](../includes/use-pre-existing-resource.md)]


## Create a custom text classification project (REST API)

Once your resource and storage container are configured, create a new custom text classification project. A project is a work area for building your custom AI models based on your data. Your project is only accessible by you and others who have access to the Azure resource being used. If you labeled data, you can [import it](#import-a-custom-text-classification-project-rest-api) to get started.


[!INCLUDE [REST APIs project creation](../includes/rest-api/create-project.md)]


## Import a custom text classification project (REST API)

If you already labeled data, you can use it to get started with the service. Make sure that your labeled data follows the [accepted data formats](../concepts/data-formats.md).

[!INCLUDE [Import project](../includes/rest-api/import-project.md)]

## Get project details (REST API)

[!INCLUDE [REST API project details](../includes/rest-api/project-details.md)]

## Delete project (REST API)


[!INCLUDE [Delete project using the REST API](../includes/rest-api/delete-project.md)]


## Next steps

* You should plan the [project schema](design-schema.md) used to label your data.

* After your project is created, you can start [labeling your data](tag-data.md). Labeling informs your text classification model how to interpret text and is used for training and evaluation.
