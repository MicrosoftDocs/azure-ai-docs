---
title: Create custom named entity recognition (NER) projects and use Azure resources
titleSuffix: Foundry Tools
description: Learn how to create and manage projects and Azure resources for custom NER.
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: how-to
ms.date: 11/18/2025
ms.author: lajanuar
ms.custom: language-service-custom-ner, references_regions
---
# How to create custom named entity recognition (NER) project

Use this article to learn how to set up the requirements for starting with custom NER and create a project.

## Prerequisites

Before you start using custom NER, you need:

* An Azure subscription - [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

## Create a Language resource 

Before you start using custom NER, you need an Azure Language in Foundry Tools resource. We recommend that you create your Language resource and connect a storage account to it in the Azure portal. Creating a resource in the Azure portal lets you create an Azure storage account at the same time, with all of the required permissions preconfigured. You can also read further in the article to learn how to use a preexisting resource, and configure it to work with custom named entity recognition.

You also need an Azure storage account where you upload your `.txt` documents that are used to train a model to extract entities.

> [!NOTE]
>  * You need to have an **owner** role assigned on the resource group to create a Language resource.
>  * If you connect a preexisting storage account, you should have an owner role assigned to it.

## Create Language resource and connect storage account

You can create a resource in the following ways:

* The Azure portal
* PowerShell

> [!Note]
> You shouldn't move the storage account to a different resource group or subscription once it's linked with Azure Language resource.

[!INCLUDE [create a new resource from the Azure portal](../includes/resource-creation-azure-portal.md)]

[!INCLUDE [create a new resource with Azure PowerShell](../includes/resource-creation-powershell.md)]


> [!NOTE]
> * The process of connecting a storage account to your Language resource is irreversible. It can't be disconnected later.
> * You can only connect your language resource to one storage account.

## Using a preexisting Language resource

[!INCLUDE [use an existing resource](../includes/use-pre-existing-resource.md)]

## Create a custom named entity recognition project (REST API)

Once your resource and storage container are configured, create a new custom NER project. A project is a work area for building your custom AI models based on your data. Only you can access your project along with others who have access to the Azure resource being used. If you labeled data, you can use it to get started by [importing a project](#import-project-rest-api).

[!INCLUDE [REST APIs project creation](../includes/rest-api/create-project.md)]

## Import project (REST API)

If you already labeled data, you can use it to get started with the service. Make sure that your labeled data follows the [accepted data formats](../concepts/data-formats.md).

[!INCLUDE [Import project](../includes/rest-api/import-project.md)]

## Get project details (REST API)

[!INCLUDE [REST APIs project details](../includes/rest-api/project-details.md)]

## Delete project (REST API)

[!INCLUDE [Delete project using the REST API](../includes/rest-api/delete-project.md)]

## Next steps

* You should have an idea of the [project schema](design-schema.md) you use to label your data.

* After your project is created, you can start [labeling your data](tag-data.md). This process informs your entity extraction model how to interpret text, and is used for training and evaluation.
