---
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: include
ms.date: 11/18/2025
ms.author: lajanuar
---
## Prerequisites

* Azure subscription - [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn)



## Create a new Azure Language in Foundry Tools resource and Azure storage account

Before you can use custom named entity recognition (NER), you need to create a Language resource, which gives you the credentials that you need to create a project and start training a model. You also need an Azure storage account, where you can upload your dataset that is used in building your model.

> [!IMPORTANT]
> To get started quickly, we recommend creating a new Language resource. Use the steps provided in this article, to create Azure Language resource, and create and/or connect a storage account at the same time. Creating both at the same time is easier than doing it later.
>
> If you have a preexisting resource that you'd like to use, you need to connect it to storage account. See [create project](../../how-to/create-project.md)  for information.

[!INCLUDE [create a new resource from the Azure portal](../resource-creation-azure-portal.md)]



## Upload sample data to blob container

[!INCLUDE [Uploading sample data for custom NER](blob-storage-upload.md)]



### Get your resource keys and endpoint

[!INCLUDE [Get keys and endpoint Azure portal](../get-keys-endpoint-azure.md)]



## Create a custom NER project

Once your resource and storage account are configured, create a new custom NER project. A project is a work area for building your custom ML models based on your data. Your project is accessed you and others who have access to Azure Language resource being used.

Use the tags file you downloaded from the [sample data](https://github.com/Azure-Samples/cognitive-services-sample-data-files) in the previous step and add it to the body of the following request. 

### Trigger import project job 

[!INCLUDE [Import a project using the REST API](../rest-api/import-project.md)]



### Get import job status

 [!INCLUDE [get import project status](../rest-api/get-import-status.md)]



## Train your model

Typically after you create a project, you go ahead and start [tagging the documents](../../how-to/tag-data.md) you have in the container connected to your project. For this quickstart, you imported a sample tagged dataset and initialized your project with the sample JSON tags file.

### Start training job

After your project is imported, you can start training your model. 

[!INCLUDE [train model](../rest-api/train-model.md)]



### Get training job status

Training could take sometime between 10 and 30 minutes for this sample dataset. You can use the following request to keep polling the status of the training job until successfully completed.

[!INCLUDE [get training model status](../rest-api/get-training-status.md)]



## Deploy your model

Generally after training a model you would review it's [evaluation details](../../how-to/view-model-evaluation.md) and [make improvements](../../how-to/view-model-evaluation.md) if necessary. In this quickstart, you just deploy your model, and make it available for you to try in Language Studio, or you can call the [prediction API](https://aka.ms/ct-runtime-swagger).

### Start deployment job

[!INCLUDE [deploy model](../rest-api/deploy-model.md)]



### Get deployment job status

[!INCLUDE [get deployment status](../rest-api/get-deployment-status.md)]



## Extract custom entities

After your model is deployed, you can start using it to extract entities from your text using the [prediction API](https://aka.ms/ct-runtime-swagger). In the sample dataset, downloaded earlier, you can find some test documents that you can use in this step.

### Submit a custom NER task

[!INCLUDE [submit a custom NER task using the REST API](../rest-api/submit-task.md)]



### Get task results

[!INCLUDE [get custom NER task results](../rest-api/get-results.md)]



## Clean up resources

[!INCLUDE [Delete project using the REST API](../rest-api/delete-project.md)]
