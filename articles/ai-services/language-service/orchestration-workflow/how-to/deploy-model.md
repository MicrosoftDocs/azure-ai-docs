---
title: How to deploy an orchestration workflow project
titleSuffix: Foundry Tools
description: Learn about deploying orchestration workflow projects.
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: how-to
ms.date: 11/18/2025
ms.author: lajanuar
ms.custom: language-service-orchestration
---
# Deploy an orchestration workflow model 

Once you're satisfied with how your model performs, it's ready to be deployed, and query it for predictions from utterances. Deploying a model makes it available for use through the [prediction API](https://aka.ms/ct-runtime-swagger).

## Prerequisites

* A successfully [created project](create-project.md) 
* [Labeled utterances](tag-utterances.md) and successfully [trained model](train-model.md)
<!--* Reviewed the [model evaluation details](view-model-evaluation.md) to determine how your model is performing.-->

For more information, *see*  [project development lifecycle](../overview.md#project-development-lifecycle).

## Deploy model

After you reviewed the model's performance and decide it's a good fit for use in your environment, you need to assign it to a deployment to be able to query it. Assigning the model to a deployment makes it available for use through the [prediction API](https://aka.ms/clu-apis). We recommended that you create a deployment named `production` to which you assign the best model you built so far and use it in your system. You can create another deployment called `staging` to which you can assign the model you're currently working on to be able to test it. You can have a maximum on 10 deployments in your project. 

### Submit deployment job

[!INCLUDE [deploy model](../includes/rest-api/deploy-model.md)]

### Get deployment job status

[!INCLUDE [get deployment status](../includes/rest-api/get-deployment-status.md)]

## Swap deployments

After you're done testing a model assigned to one deployment, you might want to assign it to another deployment. Swapping deployments involves:
* Taking the model assigned to the first deployment, and assigning it to the second deployment. 
* taking the model assigned to second deployment and assign it to the first deployment. 

This step can be used to swap your `production` and `staging` deployments when you want to take the model assigned to `staging` and assign it to `production`. 

[!INCLUDE [Swap deployments](../includes/rest-api/swap-deployment.md)]

## Delete deployment

[!INCLUDE [Delete deployment](../includes/rest-api/delete-deployment.md)]

## Assign deployment resources

You can [deploy your project to multiple regions](../../concepts/custom-features/multi-region-deployment.md) by assigning different Language resources that exist in different regions.


[!INCLUDE [Assign resource](../../conversational-language-understanding/includes/rest-api/assign-resources.md)]

## Unassign deployment resources

When unassigning or removing a deployment resource from a project, you can also delete all the deployments that are deployed to that resource region.

[!INCLUDE [Unassign resource](../../conversational-language-understanding/includes/rest-api/unassign-resources.md)]

## Next steps

Use [prediction API to query your model](call-api.md)
