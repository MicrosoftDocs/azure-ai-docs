---
#services: cognitive-services
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: include
ms.date: 11/18/2025
ms.author: lajanuar
ms.custom: language-service-custom-classification
---
## Prerequisites

* Azure subscription - [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).



## Create a new Azure Language in Foundry Tools resource and Azure storage account

Before you can use custom text classification, you need to create a Language resource, which gives you the credentials that you need to create a project and start training a model. You also need an Azure storage account, where you can upload your dataset that is used to build your model.

> [!IMPORTANT]
> To quickly get started, we recommend creating a new Language resource using the steps provided in this article. Using the steps in this article lets you create Azure Language resource and storage account at the same time, which is easier than doing it later.
>
> If you have a [preexisting resource](../../how-to/create-project.md#using-a-preexisting-language-resource) that you'd like to use, you need to connect it to storage account.
>
> Adding the role **Storage Blob Data Contributor** is essential for interacting with *any resource* that utilizes the storage account.

[!INCLUDE [create a new resource from the Azure portal](../resource-creation-azure-portal.md)]
    


## Upload sample data to blob container

[!INCLUDE [Uploading sample data for custom tex classification](blob-storage-upload.md)]
    


## Create a custom text classification project

Once your resource and storage container are configured, create a new custom text classification project. A project is a work area for building your custom ML models based on your data. Your project is only accessible to you and others who have access to Azure Language resource being used.

[!INCLUDE [Create a project using Language Studio](../language-studio/create-project.md)]
    


## Train your model

Typically after you create a project, you go ahead and start [labeling the documents](../../how-to/tag-data.md) you have in the container connected to your project. For this quickstart, you imported a sample labeled dataset and initialized your project with the sample JSON labels file.

[!INCLUDE [Train a model using Language Studio](../language-studio/train-model.md)]



## Deploy your model

Generally after training a model you would review its [evaluation details](../../how-to/view-model-evaluation.md) and [make improvements](../../how-to/view-model-evaluation.md) if necessary. In this quickstart, you deploy your model, and make it available for you to try in Language Studio, or you can call the [prediction API](https://aka.ms/ct-runtime-swagger).

[!INCLUDE [Deploy a model using Language Studio](../language-studio/deploy-model.md)]



## Test your model

After your model is deployed, you can start using it to classify your text via [Prediction API](https://aka.ms/ct-runtime-swagger). For this quickstart, you use the [Language Studio](https://aka.ms/LanguageStudio) to submit the custom text classification task and visualize the results. In the sample dataset, you downloaded earlier you can find some test documents that you can use in this step.

[!INCLUDE [Test a model using Language Studio](../language-studio/test-model.md)]



## Clean up projects

[!INCLUDE [Delete project using Language Studio](../language-studio/delete-project.md)]
