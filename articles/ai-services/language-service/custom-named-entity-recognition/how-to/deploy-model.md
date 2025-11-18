---
title: How to deploy a custom named entity recognition (NER) model
titleSuffix: Foundry Tools
description: Learn how to deploy a model for custom NER.
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: how-to
ms.date: 11/18/2025
ms.author: lajanuar
ms.custom: language-service-custom-ner
---
# Deploy a model and extract entities from text using the runtime API

Once you're satisfied with how your model performs, it's ready to be deployed and used to recognize entities in text. Deploying a model makes it available for use through the [prediction API](https://aka.ms/ct-runtime-swagger).

## Prerequisites

* A successfully [created project](create-project.md) with a configured Azure storage account.
* Text data that is [uploaded](design-schema.md#data-preparation) to your storage account.
* [Labeled data](tag-data.md) and successfully [trained model](train-model.md)
* Reviewed the [model evaluation details](view-model-evaluation.md) to determine how your model is performing.

 For more information, *see* [project development lifecycle](../overview.md#project-development-lifecycle).

## Deploy model

After you review your model's performance and decided it can be used in your environment, you need to assign it to a deployment. Assigning the model to a deployment makes it available for use through the [prediction API](https://aka.ms/ct-runtime-swagger).  We recommend that you create a deployment named *production* to which you assign the best model you built so far and use it in your system. You can create another deployment called *staging* to which you can assign the model you're currently working on to be able to test it. You can have a maximum of 10 deployments in your project. 

# [Microsoft Foundry](#tab/azure-ai-foundry)

For information on how to deploy your custom model in the Foundry, *see* [Deploy your fine-tuned model ](/azure/ai-foundry/openai/how-to/fine-tuning-deploy?tabs=portal#deploy-your-fine-tuned-model).
   
# [REST APIs](#tab/rest-api)

### Submit deployment job

[!INCLUDE [deploy model](../includes/rest-api/deploy-model.md)]

### Get deployment job status

[!INCLUDE [get deployment status](../includes/rest-api/get-deployment-status.md)]

---

## Swap deployments

After you're done testing a model assigned to one deployment and you want to assign this model to another deployment, you can swap these two deployments. Swapping deployments involves taking the model assigned to the first deployment, and assigning it to the second deployment. Then taking the model assigned to second deployment, and assigning it to the first deployment. You can use this process to swap your *production* and *staging* deployments when you want to take the model assigned to *staging* and assign it to *production*. 

# [Foundry](#tab/azure-ai-foundry)

To replace a deployed model, you can exchange the deployed model with a different model in the same region:

1. Select the model name under **Name** then select **Deploy model**.

1. Select **Swap model**.

   The redeployment takes several minutes to complete. In the meantime, deployed model continues to be available for use with the Translator API until this process is complete.

# [REST APIs](#tab/rest-api)

[!INCLUDE [Swap deployments](../includes/rest-api/swap-deployment.md)]

---


## Delete deployment

# [Foundry](#tab/azure-ai-foundry)
If you no longer need your project, you can delete it from the Foundry.

1. Navigate to the [Foundry](https://ai.azure.com/) home page. Initiate the authentication process by signing in, unless you already completed this step and your session is active.
1. Select the project that you want to delete from the **Keep building with Foundry**
1. Select **Management center**.
1. Select **Delete project**.

To delete the hub along with all its projects:

1. Navigate to the **Overview** tab inn the **Hub** section.

1. On the right, select **Delete hub**.
1. The link opens the Azure portal for you to delete the hub.

# [REST APIs](#tab/rest-api)

[!INCLUDE [Delete deployment](../includes/rest-api/delete-deployment.md)]

---

## Assign deployment resources

You can [deploy your project to multiple regions](../../concepts/custom-features/multi-region-deployment.md) by assigning different Language resources that exist in different regions.

# [Foundry](#tab/azure-ai-foundry)

For more information on how to deploy you custom model, *see* [Deploy your fine-tuned model](/azure/ai-foundry/openai/how-to/fine-tuning-deploy?tabs=python#deploy-your-fine-tuned-model)

# [REST APIs](#tab/rest-api)

[!INCLUDE [Assign resource](../../custom-text-classification/includes/rest-api/assign-resources.md)]

---

## Unassign deployment resources

To unassign or remove a deployment resource from a project, you also delete all the deployments for to that resource region.

# [Foundry](#tab/azure-ai-foundry)

If you no longer need your project, you can delete it from the Foundry.

1. Navigate to the [Foundry](https://ai.azure.com/) home page. Initiate the authentication process by signing in, unless you already completed this step and your session is active.
1. Select the project that you want to delete from the **Keep building with Foundry**
1. Select **Management center**.
1. Select **Delete project**.

To delete the hub along with all its projects:

1. Navigate to the **Overview** tab inn the **Hub** section.

1. On the right, select **Delete hub**.
1. The link opens the Azure portal for you to delete the hub.

   
# [REST APIs](#tab/rest-api)

[!INCLUDE [Unassign resource](../../custom-text-classification/includes/rest-api/unassign-resources.md)]

---

## Next steps

After you have a deployment, you can use it to [extract entities](call-api.md) from text.
