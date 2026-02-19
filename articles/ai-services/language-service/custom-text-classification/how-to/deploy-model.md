---
title: How to deploy a custom text classification model
titleSuffix: Foundry Tools
description: Learn how to deploy a model for custom text classification.
#services: cognitive-services
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: how-to
ms.date: 12/15/2025
ms.author: lajanuar
ms.custom: language-service-custom-classification
---
# Deploy a model and classify text using the runtime API

Once you're satisfied with how your model performs, it's ready to be deployed; and use it to classify text. Deploying a model makes it available for use through the [prediction API](https://aka.ms/ct-runtime-swagger).

## Prerequisites

* [A custom text classification project](create-project.md) with a configured Azure storage account,
* Text data that is [uploaded](design-schema.md#data-preparation) to your storage account.
* [Labeled data](tag-data.md) and successfully [trained model](train-model.md)
* Reviewed the [model evaluation details](view-model-evaluation.md) to determine how your model is performing.

See the [project development lifecycle](../overview.md#project-development-lifecycle).

## Deploy model (REST API)

After you review your model's performance and decided it can be used in your environment, you need to assign it to a deployment to be able to query it. Assigning the model to a deployment makes it available for use through the [prediction API](https://aka.ms/ct-runtime-swagger). We recommend that you create a deployment named `production` to which you assign the best model you built so far and use it in your system. You can create another deployment called `staging` to which you can assign the model you're currently working on to be able to test it. You can have a maximum on 10 deployments in your project.

### Submit deployment job

[!INCLUDE [deploy model](../includes/rest-api/deploy-model.md)]

### Get deployment job status

[!INCLUDE [get deployment status](../includes/rest-api/get-deployment-status.md)]

## Swap deployments (REST API)

You can swap deployments after testing a model assigned to one deployment, and want to assign it to another. Swapping deployments involves taking the model assigned to the first deployment, and assigning it to the second deployment. Then taking the model assigned to second deployment and assign it to the first deployment. This step could be used to swap your `production` and `staging` deployments when you want to take the model assigned to `staging` and assign it to `production`.

[!INCLUDE [Swap deployments](../includes/rest-api/swap-deployment.md)]

## Delete deployment (REST API)

[!INCLUDE [Delete deployment](../includes/rest-api/delete-deployment.md)]

## Assign deployment resources (REST API)

You can [deploy your project to multiple regions](../../concepts/custom-features/multi-region-deployment.md) by assigning different Language resources that exist in different regions.

[!INCLUDE [Assign resource](../includes/rest-api/assign-resources.md)]

## Unassign deployment resources (REST API)

When you unassign or remove a deployment resource from a project, you also delete all the deployments previously deployed to that resource region.

[!INCLUDE [Unassign resource](../includes/rest-api/unassign-resources.md)]

## Next steps

* Use [prediction API to query your model](call-api.md)
