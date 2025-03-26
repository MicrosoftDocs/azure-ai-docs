---
title: How to deploy Stability AI family of models with Azure Machine Learning studio
titleSuffix: Azure Machine Learning studio
description: How to deploy Stability AI family of models with Azure Machine Learning studio
manager: scottpolly
ms.service: azure-machine-learning
ms.topic: how-to
ms.date: 02/12/2025
ms.author: timanghn
author: tinaem
ms.reviewer: ssalgado
reviewer: ssalgadodev
ms.custom: references_regions
---

# How to deploy Stability AI family of models with Azure Machine Learning studio

[!INCLUDE [machine-learning-preview-generic-disclaimer](includes/machine-learning-preview-generic-disclaimer.md)]

In this article, you learn how to useAzure Machine Learning studio to deploy Stability AI collection of models as a serverless API with pay-as-you-go billing.

The Stability AI collection of models include Stable Image Core, Stable Image Ultra and Stable Diffusion 3.5 Large. 

### Stable Diffusion 3.5 Large
At 8.1 billion parameters, with superior quality and prompt adherence, this base model is the most powerful in the Stable Diffusion family and is ideal for professional use cases at 1 megapixel resolution. 

Stable Diffusion 3.5 large supports text and image prompt inputs for image generations. 

### Stable Image Core
Leveraging an enhanced version of SDXL, Stable Image Core, delivers exceptional speed and efficiency while maintaining the high-quality output synonymous with Stable Diffusion models.

Stable Image Core supports text prompt inputs only for image generations.

### Stable Image Ultra
Powered by the advanced capabilities of Stable Diffusion 3.5 Large, Stable Image Ultra sets a new standard in photorealism. Stable Image Ultra is ideal for product imagery in marketing and advertising. It also excels in typography, dynamic lighting, and vibrant color rendering.

Stable Image Ultra supports text prompt inputs only for image generations.

[!INCLUDE [models-preview](../ai-foundry/includes/models-preview.md)]


## Deploy a Stability AI model as a serverless API

Stability AI models in the model catalog can be deployed as a serverless API with pay-as-you-go billing, providing a way to consume them as an API without hosting them on your subscription, while keeping the enterprise security and compliance organizations need. This deployment option doesn't require quota from your subscription. 


### Prerequisites

- An Azure subscription with a valid payment method. Free or trial Azure subscriptions won't work. If you don't have an Azure subscription, create a [paid Azure account](https://azure.microsoft.com/pricing/purchase-options/pay-as-you-go) to begin.
- An Azure Machine Learning workspace and a compute instance. If you don't have these, use the steps in the [Quickstart: Create workspace resources](quickstart-create-resources.md) article to create them. The serverless API model deployment offering for Stability AI is only available with workspaces created in these regions:

     * East US
     * East US 2
     * North Central US
     * South Central US
     * West US
     * West US 3
    
    For a list of  regions that are available for each of the models supporting serverless API endpoint deployments, see [Region availability for models in serverless API endpoints](concept-endpoint-serverless-availability.md).

- Azure role-based access controls (Azure RBAC) are used to grant access to operations in Azure Machine Learning. To perform the steps in this article, your user account must be assigned the __owner__ or __contributor__ role for the Azure subscription. Alternatively, your account can be assigned a custom role that has the following permissions:

    - On the Azure subscription—to subscribe the workspace to the Azure Marketplace offering, once for each workspace, per offering:
      - `Microsoft.MarketplaceOrdering/agreements/offers/plans/read`
      - `Microsoft.MarketplaceOrdering/agreements/offers/plans/sign/action`
      - `Microsoft.MarketplaceOrdering/offerTypes/publishers/offers/plans/agreements/read`
      - `Microsoft.Marketplace/offerTypes/publishers/offers/plans/agreements/read`
      - `Microsoft.SaaS/register/action`
 
    - On the resource group—to create and use the SaaS resource:
      - `Microsoft.SaaS/resources/read`
      - `Microsoft.SaaS/resources/write`
 
    - On the workspace—to deploy endpoints (the Azure Machine Learning data scientist role contains these permissions already):
      - `Microsoft.MachineLearningServices/workspaces/marketplaceModelSubscriptions/*`  
      - `Microsoft.MachineLearningServices/workspaces/serverlessEndpoints/*`

    For more information on permissions, see [Manage access to an Azure Machine Learning workspace](how-to-assign-roles.md).



### Create a new deployment

These steps demonstrate the deployment of a Stability AI Model. To create a deployment:

1. Go to [Azure Machine Learning studio](https://ml.azure.com/home).
1. Select the workspace in which you want to deploy your models. To use the pay-as-you-go model deployment offering, your workspace must belong to one of the available regions listed in the prerequisites of this article.
1. Choose `Stable Diffusion 3.5 Large` to deploy from the [model catalog](https://ml.azure.com/model/catalog).

   Alternatively, you can initiate deployment by going to your workspace and selecting **Endpoints** > **Serverless endpoints** > **Create**.

1. On the **Details** page for `Stable Diffusion 3.5 Large`, select **Deploy** and then select **Serverless API with Azure AI Content Safety**.

1. On the deployment wizard, select the link to **Azure Marketplace Terms** to learn more about the terms of use. You can also select the **Marketplace offer details** tab to learn about pricing for the selected model.
1. If this is your first time deploying the model in the workspace, you have to subscribe your workspace for the particular offering (for example, `Stable Diffusion 3.5 Large`) from Azure Marketplace. This step requires that your account has the Azure subscription permissions and resource group permissions listed in the prerequisites. Each workspace has its own subscription to the particular Azure Marketplace offering, which allows you to control and monitor spending. Select **Subscribe and Deploy**.

    > [!NOTE]
    > Subscribing a workspace to a particular Azure Marketplace offering (in this case, Stability AI) requires that your account has **Contributor** or **Owner** access at the subscription level where the project is created. Alternatively, your user account can be assigned a custom role that has the Azure subscription permissions and resource group permissions listed in the [prerequisites](#prerequisites).

1. Once you sign up the workspace for the particular Azure Marketplace offering, subsequent deployments of the _same_ offering in the _same_ workspace don't require subscribing again. Therefore, you don't need to have the subscription-level permissions for subsequent deployments. If this scenario applies to you, select **Continue to deploy**.

1. Give the deployment a name. This name becomes part of the deployment API URL. This URL must be unique in each Azure region.

1. Select **Deploy**. Wait until the deployment is finished and you're redirected to the serverless endpoints page.
1. Select the endpoint to open its Details page.
1. Select the **Test** tab to start interacting with the model.
1. You can also take note of the **Target** URL and the **Secret Key** to call the deployment and generate completions.   
1. You can always find the endpoint's details, URL, and access keys by navigating to **Workspace** > **Endpoints** > **Serverless endpoints**.

### Consume Stability AI models as a serverless API

1. In the **workspace**, select **Endpoints** > **Serverless endpoints**.
1. Find and select the `Stable Diffusion 3.5 Large` deployment you created.
1. Copy the **Target** URL and the **Key** token values.
1. Make an API request based on the type of model you deployed. For an example, see the [reference section](#reference-for-stability-ai-models-deployed-as-a-serverless-api)

## Reference for Stability AI models deployed as a serverless API

Stability AI models on Models as a Service implement the Azure AI Model Inference API on the route `/image/generations`.

#### Request example 

```
{
      "prompt": "A photo of a cat",
      "negative_prompt": "A photo of a dog",
      "image_prompt": {
        "image": "puqkvvlvgcjyzughesnkena",
        "strength": 1
        },
      "size": "1024x1024",
      "output_format": "png",
      "seed": 26
}
```

#### Response

```
{
    "image": "iVBORw0KGgoAAAANSUhEUgAABgA...",
    "created": 1739161682
}
```

## Cost and quotas

### Cost and quota considerations for Stability AI models deployed as a serverless API

The Stability AI models are deployed as a serverless API and is offered by Stability AI through Azure Marketplace and integrated with Azure Machine Learning studio for use. You can find Azure Marketplace pricing when deploying or fine-tuning models.

Each time a workspace subscribes to a given model offering from Azure Marketplace, a new resource is created to track the costs associated with its consumption. The same resource is used to track costs associated with inference and fine-tuning; however, multiple meters are available to track each scenario independently.

For more information on how to track costs, see [Monitor costs for models offered through the Azure Marketplace](/azure/ai-foundry/how-to/costs-plan-manage#monitor-costs-for-models-offered-through-the-azure-marketplace).

Quota is managed per deployment. Each deployment has a rate limit of 200,000 tokens per minute and 1,000 API requests per minute. However, we currently limit one deployment per model per project. Contact Microsoft Azure Support if the current rate limits aren't sufficient for your scenarios.

## Content filtering

Models deployed as a serverless API are protected by Azure AI content safety. When deployed to managed compute, you can opt out of this capability. With Azure AI content safety enabled, both the prompt and completion pass through an ensemble of classification models aimed at detecting and preventing the output of harmful content. The content filtering (preview) system detects and takes action on specific categories of potentially harmful content in both input prompts and output completions. Learn more about [Azure AI Content Safety](/azure/ai-services/content-safety/overview).

## Related content

- [Model Catalog and Collections](concept-model-catalog.md)
- [Deploy and score a machine learning model by using an online endpoint](how-to-deploy-online-endpoints.md)
- [Plan and manage costs for Azure AI Foundry](/azure/ai-foundry/how-to/costs-plan-manage)
- [Region availability for models in serverless API endpoints](concept-endpoint-serverless-availability.md)
