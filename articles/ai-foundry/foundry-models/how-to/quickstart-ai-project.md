---
title: Configure your AI Project for Microsoft Foundry Models
titleSuffix: Microsoft Foundry
description: Learn how to upgrade your AI project to use models deployed in Microsoft Foundry Models in Microsoft Foundry Service.
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: how-to
ms.date: 10/09/2025
ms.custom: ignite-2024, github-universe-2024
author: ssalgadodev
ms.author: ssalgado
recommendations: false
ms.reviewer: fasantia
reviewer: santiagxf
---

# Configure your AI project to use Microsoft Foundry Models

[!INCLUDE [classic-banner](../../includes/classic-banner.md)]

If you already have an AI project in Microsoft Foundry, the model catalog deploys models from partner model providers as stand-alone endpoints in your project by default. Each model deployment has its own set of URI and credentials to access it. On the other hand, Azure OpenAI models are deployed to the Foundry resource or to the Azure OpenAI in Foundry Models resource.

[!INCLUDE [migrate-model-inference-to-v1-openai](../../includes/migrate-model-inference-to-v1-openai.md)]

You can change this behavior and deploy both types of models to Foundry resources. Once configured, *deployments of models as serverless API deployments happen to the connected Foundry resource* instead to the project itself, giving you a single set of endpoint and credentials to access all the models deployed in Foundry. You can manage models from Azure OpenAI and partner model providers in the same way.

Additionally, deploying models to Foundry Models brings the extra benefits of:

> [!div class="checklist"]
> * [Routing capability](inference.md#routing)
> * [Custom content filters](../concepts/content-filter.md)
> * Global capacity deployment type
> * [Key-less authentication with Microsoft Entra ID](./configure-entra-id.md)

In this article, you learn how to configure your project to use Foundry Models deployments.

## Prerequisites

To complete this tutorial, you need:

* An Azure subscription. If you're using [GitHub Models](https://docs.github.com/en/github-models/), you can upgrade your experience and create an Azure subscription in the process. To learn more, see [Upgrade from GitHub Models to Foundry Models](./quickstart-github-models.md).

* A Foundry resource. For more information, see [Create your first Foundry resource](../../../ai-services/multi-service-resource.md).

* A Foundry project and hub. For more information, see [How to create and manage a Foundry hub](../../../ai-foundry/how-to/create-azure-ai-resource.md).

    > [!TIP]
    > When your AI hub is provisioned, a Foundry resource is created with it and the two resources are connected. To see which resource is connected to your project, go to the [Foundry portal](https://ai.azure.com/?cid=learnDocs) > **Management center** > **Connected resources**, and find the connections of type **Foundry Tools**. 


## Configure the project to use Foundry Models

To configure the project to use the Foundry Models capability in Foundry, follow these steps:

1. In the landing page of your project, select **Management center** at the bottom of the sidebar menu. Identify the Foundry resource connected to your project.

1. If no resource is listed, your AI hub doesn't have a Foundry resource connected to it. Create a new connection.

   1. Select **+New connection**, then choose **Microsoft Foundry** from the tiles.

   1. In the window, look for an existing resource in your subscription and then select **Add connection**.

   1. The new connection is added to your hub.

1. Return to the project's landing page.

1. Under **Included capabilities**, ensure you select **Azure AI Inference**. The **Azure AI model inference endpoint** URI is displayed along with the credentials to get access to it.

    :::image type="content" source="../media/quickstart-ai-project/overview-endpoint-and-key.png" alt-text="Screenshot of the landing page for the project, highlighting the location of the connected resource and the associated inference endpoint." lightbox="../media/quickstart-ai-project/overview-endpoint-and-key.png":::

    > [!TIP]
    > Each Foundry resource has a single **Azure AI model inference endpoint** that can be used to access any model deployment on it. The same endpoint serves multiple models depending on which ones are configured. To learn how the endpoint works, see [Azure OpenAI inference endpoint](inference.md#azure-openai-inference-endpoint).

1. Take note of the endpoint URL and credentials.


### Create the model deployment in Foundry Models

For each model you want to deploy under Foundry Models, follow these steps:

1. Go to the **Model catalog** in [Foundry portal](https://ai.azure.com/explore/models).

1. Scroll to the model you're interested in and select it.

    :::image type="content" source="../media/add-model-deployments/models-search-and-deploy.gif" alt-text="Animation showing how to search models in the model catalog and select one for viewing its details." lightbox="../media/add-model-deployments/models-search-and-deploy.gif":::

1. You can review the details of the model in the model card.

1. Select **Use this model**.

1. For model providers that require more contract terms, you're asked to accept those terms by selecting **Agree and proceed**.

    :::image type="content" source="../media/add-model-deployments/models-deploy-agree.png" alt-text="Screenshot showing how to agree the terms and conditions of a Mistral-Large model." lightbox="../media/add-model-deployments/models-deploy-agree.png":::

1. You can configure the deployment settings at this time. By default, the deployment receives the name of the model you're deploying. The deployment name is used in the `model` parameter for request to route to this particular model deployment. It allows you to configure specific names for your models when you attach specific configurations. For instance, `o1-preview-safe` for a model with a strict content filter.

1. We automatically select a Foundry connection depending on your project because you turned on the feature **Deploy models to Azure AI model inference service**. Select **Customize** to change the connection based on your needs. If you're deploying under the **serverless API** deployment type, the models need to be available in the region of the Foundry resource.

    :::image type="content" source="../media/add-model-deployments/models-deploy-customize.png" alt-text="Screenshot showing how to customize the deployment if needed." lightbox="../media/add-model-deployments/models-deploy-customize.png":::

1. Select **Deploy**.

1. Once the deployment finishes, you see the endpoint URL and credentials to get access to the model. Notice that now the provided URL and credentials are the same as displayed in the landing page of the project for the **Foundry Models endpoint**.

1. You can view all the models available under the resource by going to **Models + endpoints** section and locating the group for the connection to your resource:

    :::image type="content" source="../media/quickstart-ai-project/endpoints-ai-services-connection.png" alt-text="Screenshot showing the list of models available under a given connection." lightbox="../media/quickstart-ai-project/endpoints-ai-services-connection.png":::


### Upgrade your code with the new endpoint

Once your Foundry resource is configured, you can start consuming it from your code. You need the endpoint URL and key for it, which can be found in the **Overview** section:

You can use any of the supported SDKs to get predictions out from the endpoint. The following SDKs are officially supported:

* OpenAI SDK
* Azure OpenAI SDK
* Azure AI Inference package
* Azure AI Projects package

For more information and examples, see [Supported programming languages for Azure AI Inference SDK](../supported-languages.md). The following example shows how to use the Azure AI Inference package with the newly deployed model:

[!INCLUDE [code-create-chat-client](../../foundry-models/includes/code-create-chat-client.md)]

Generate your first chat completion:

[!INCLUDE [code-create-chat-completion](../../foundry-models/includes/code-create-chat-completion.md)]

Use the parameter `model="<deployment-name>` to route your request to this deployment. *Deployments work as an alias of a given model under certain configurations*. To learn how Foundry Models routes deployments, see [Routing](inference.md#routing).


## Move from serverless API deployments to Foundry Models

Although you configured the project to use Foundry Models, existing model deployments continue to exist within the project as serverless API deployments. Those deployments aren't moved for you. Hence, you can progressively upgrade any existing code that references previous model deployments. To start moving the model deployments, we recommend the following workflow:

1. Recreate the model deployment in Foundry Models. This model deployment is accessible under the **Foundry Models endpoint**.

1. Upgrade your code to use the new endpoint.

1. Clean up the project by removing the serverless API deployment.


### Upgrade your code with the new endpoint

Once the models are deployed under Foundry, you can upgrade your code to use the Foundry Models endpoint. The main difference between how serverless API deployments and Foundry Models work resides in the endpoint URL and model parameter. While serverless API deployments have a set of URI and key per each model deployment, Foundry Models has only one for all of them.

The following table summarizes the changes you have to introduce:

| Property | serverless API deployments | Foundry Models |
| -------- | ------------------------ | ------------------------ |
| Endpoint    | `https://<endpoint-name>.<region>.inference.ai.azure.com` | `https://<ai-resource>.services.ai.azure.com/models` |
| Credentials | One per model/endpoint. | One per Foundry resource. You can use Microsoft Entra ID too. |
| Model parameter | None. | Required. Use the name of the model deployment. |


### Clean-up existing serverless API deployments from your project

After you refactored your code, you might want to delete the existing serverless API deployments inside of the project (if any).

For each model deployed as serverless API deployments, follow these steps:

1. Go to the [Foundry portal](https://ai.azure.com/?cid=learnDocs).

1. Select **Models + endpoints**, then choose the **Service endpoints** tab.

1. Identify the endpoints of type **serverless API deployment** and select the one you want to delete.

1. Select the option **Delete**.

    > [!WARNING]
    > This operation can't be reverted. Ensure that the endpoint isn't currently used by any other user or piece of code.

1. Confirm the operation by selecting **Delete**.

1. If you created a **serverless API deployment connection** to this endpoint from other projects, such connections aren't removed and continue to point to the inexistent endpoint. Delete any of those connections for avoiding errors.

## Limitations

Consider the following limitations when configuring your project to use Foundry Models:

* Only models that support serverless API deployments are available for deployment to Foundry Models. Models requiring compute quota from your subscription (managed compute), including custom models, can only be deployed within a given project as Managed Online Endpoints and continue to be accessible using their own set of endpoint URI and credentials.
* Models available as both serverless API deployments and managed compute offerings are, by default, deployed to Foundry Models in Foundry resources. Foundry portal doesn't offer a way to deploy them to Managed Online Endpoints. You have to turn off the feature mentioned at [Configure the project to use Foundry Models](#configure-the-project-to-use-foundry-models) or use the Azure CLI/Azure ML SDK/ARM templates to perform the deployment.

## Next step

> [!div class="nextstepaction"]
> [Add models to your endpoint](./create-model-deployments.md)
