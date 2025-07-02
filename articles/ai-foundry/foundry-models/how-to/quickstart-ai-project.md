---
title: Configure your AI project to use Azure AI Foundry Models
titleSuffix: Azure AI Foundry
description: Learn how to upgrade your AI project to use models deployed in Azure AI Foundry Models in Azure AI Foundry Service
ms.service: azure-ai-model-inference
ms.topic: how-to
ms.date: 05/19/2025
ms.custom: ignite-2024, github-universe-2024
manager: scottpolly
author: ssalgadodev
ms.author: ssalgado
recommendations: false
ms.reviewer: fasantia
reviewer: santiagxf
---

# Configure your AI project to use Azure AI Foundry Models

If you already have an AI project in Azure AI Foundry, the model catalog deploys models from third-party model providers as stand-alone endpoints in your project by default. Each model deployment has its own set of URI and credentials to access it. On the other hand, Azure OpenAI models are deployed to Azure AI Services resource or to the Azure OpenAI in Azure AI Foundry Models resource.

You can change this behavior and deploy both types of models to Azure AI Foundry Services (formerly known Azure AI Services). Once configured, **deployments of models as a serverless API deployments happen to the connected Azure AI Services resource** instead to the project itself, giving you a single set of endpoint and credential to access all the models deployed in Azure AI Foundry. You can manage Azure OpenAI and third-party model providers models in the same way.

Additionally, deploying models to Azure AI Foundry Models brings the extra benefits of:

> [!div class="checklist"]
> * [Routing capability](inference.md#routing).
> * [Custom content filters](../../model-inference/concepts/content-filter.md).
> * Global capacity deployment type.
> * [Key-less authentication](../../model-inference/how-to/configure-entra-id.md) with role-based access control.

In this article, you learn how to configure your project to use Foundry Models deployments.

## Prerequisites

To complete this tutorial, you need:

* An Azure subscription. If you're using [GitHub Models](https://docs.github.com/en/github-models/), you can upgrade your experience and create an Azure subscription in the process. Read [Upgrade from GitHub Models to Foundry Models](../../model-inference/how-to/quickstart-github-models.md) if it's your case.

* An Azure AI services resource. For more information, see [Create an Azure AI Services resource](../../../ai-services/multi-service-resource.md??context=/azure/ai-services/model-inference/context/context).

* An Azure AI project and Azure AI Hub.

    > [!TIP]
    > When your AI hub is provisioned, an Azure AI services resource is created with it and the two resources connected. To see which Azure AI services resource is connected to your project, go to the [Azure AI Foundry portal](https://ai.azure.com/?cid=learnDocs) > **Management center** > **Connected resources**, and find the connections of type **AI Services**. 


## Configure the project to use Foundry Models

To configure the project to use the Foundry Models capability in Azure AI Foundry Services, follow these steps:

1. Go to [Azure AI Foundry portal](https://ai.azure.com/?cid=learnDocs).

2. At the top navigation bar, over the right corner, select the **Preview features** icon. A contextual blade shows up at the right of the screen.

3. Turn on the **Deploy models to Azure AI model inference service** feature.

    :::image type="content" source="../media/quickstart-ai-project/ai-project-inference-endpoint.gif" alt-text="An animation showing how to turn on the Deploy models to Azure AI model inference service feature in Azure AI Foundry portal." lightbox="../media/quickstart-ai-project/ai-project-inference-endpoint.gif":::

1. Close the panel.

2. In the landing page of your project, identify the Azure AI Services resource connected to your project. Use the drop-down to change the resource you're connected if you need to.

3. If no resource is listed in the drop-down, your AI Hub doesn't have an Azure AI Services resource connected to it. Create a new connection by:

   1. In the lower left corner of the screen, select **Management center**.

   2. In the section **Connections** select **New connection**.

   3. Select **Azure AI services**.

   4. In the browser, look for an existing Azure AI Services resource in your subscription.

   5. Select **Add connection**.

   6. The new connection is added to your Hub.

   7. Return to the project's landing page to continue and now select the new created connection. Refresh the page if it doesn't show up immediately. 

4. Under **Included capabilities**, ensure you select **Azure AI Inference**. The **Foundry Models endpoint** URI is displayed along with the credentials to get access to it.

    :::image type="content" source="../media/quickstart-ai-project/overview-endpoint-and-key.png" alt-text="Screenshot of the landing page for the project, highlighting the location of the connected resource and the associated inference endpoint." lightbox="../media/quickstart-ai-project/overview-endpoint-and-key.png":::

    > [!TIP]
    > Each Azure AI Foundry Services resource has a single **Foundry Models endpoint** which can be used to access any model deployment on it. The same endpoint serves multiple models depending on which ones are configured. Learn about [how the endpoint works](inference.md#azure-openai-inference-endpoint).

5. Take note of the endpoint URL and credentials.


### Create the model deployment in Foundry Models

For each model you want to deploy under Foundry Models, follow these steps:

1. Go to **Model catalog** section in [Azure AI Foundry portal](https://ai.azure.com/explore/models).

2. Scroll to the model you're interested in and select it.

    :::image type="content" source="../media/add-model-deployments/models-search-and-deploy.gif" alt-text="An animation showing how to search models in the model catalog and select one for viewing its details." lightbox="../media/add-model-deployments/models-search-and-deploy.gif":::

3. You can review the details of the model in the model card.

4. Select **Deploy**.

5. For models providers that require more terms of contract, you're asked to accept those terms. Accept the terms on those cases by selecting **Subscribe and deploy**.

    :::image type="content" source="../media/add-model-deployments/models-deploy-agree.png" alt-text="Screenshot showing how to agree the terms and conditions of a Mistral-Large model." lightbox="../media/add-model-deployments/models-deploy-agree.png":::

6. You can configure the deployment settings at this time. By default, the deployment receives the name of the model you're deploying. The deployment name is used in the `model` parameter for request to route to this particular model deployment. It allows you to configure specific names for your models when you attach specific configurations. For instance, `o1-preview-safe` for a model with a strict content filter.

7. We automatically select an Azure AI Services connection depending on your project because you turned on the feature **Deploy models to Azure AI model inference service**. Use the **Customize** option to change the connection based on your needs. If you're deploying under the **serverless API** deployment type, the models need to be available in the region of the Azure AI Services resource.

    :::image type="content" source="../media/add-model-deployments/models-deploy-customize.png" alt-text="Screenshot showing how to customize the deployment if needed." lightbox="../media/add-model-deployments/models-deploy-customize.png":::

8. Select **Deploy**.

9. Once the deployment finishes, you see the endpoint URL and credentials to get access to the model. Notice that now the provided URL and credentials are the same as displayed in the landing page of the project for the **Foundry Models endpoint**.

10. You can view all the models available under the resource by going to **Models + endpoints** section and locating the group for the connection to your AI Services resource:

    :::image type="content" source="../media/quickstart-ai-project/endpoints-ai-services-connection.png" alt-text="Screenshot showing the list of models available under a given connection." lightbox="../media/quickstart-ai-project/endpoints-ai-services-connection.png":::


### Upgrade your code with the new endpoint

Once your Azure AI Services resource is configured, you can start consuming it from your code. You need the endpoint URL and key for it, which can be found in the **Overview** section:

You can use any of the supported SDKs to get predictions out from the endpoint. The following SDKs are officially supported:

* OpenAI SDK
* Azure OpenAI SDK
* Azure AI Inference package
* Azure AI Projects package

See the [supported languages and SDKs](../../model-inference/supported-languages.md) section for more details and examples. The following example shows how to use the Azure AI Inference package with the newly deployed model:

[!INCLUDE [code-create-chat-client](../../foundry-models/includes/code-create-chat-client.md)]

Generate your first chat completion:

[!INCLUDE [code-create-chat-completion](../../foundry-models/includes/code-create-chat-completion.md)]

Use the parameter `model="<deployment-name>` to route your request to this deployment. *Deployments work as an alias of a given model under certain configurations*. See [Routing](inference.md#routing) page to learn how Azure AI Foundry Models routes deployments.


## Move from serverless API deployments to Foundry Models

Although you configured the project to use Foundry Models, existing model deployments continue to exist within the project as serverless API deployments. Those deployments aren't moved for you. Hence, you can progressively upgrade any existing code that reference previous model deployments. To start moving the model deployments, we recommend the following workflow:

1. Recreate the model deployment in Foundry Models. This model deployment is accessible under the **Foundry Models endpoint**.

2. Upgrade your code to use the new endpoint.

3. Clean up the project by removing the serverless API deployment.


### Upgrade your code with the new endpoint

Once the models are deployed under Azure AI Foundry Services, you can upgrade your code to use the Foundry Models endpoint. The main difference between how serverless API deployments and Foundry Models works reside in the endpoint URL and model parameter. While serverless API deployments have a set of URI and key per each model deployment, Foundry Models has only one for all of them.

The following table summarizes the changes you have to introduce:

| Property | serverless API deployments | Foundry Models |
| -------- | ------------------------ | ------------------------ |
| Endpoint      | `https://<endpoint-name>.<region>.inference.ai.azure.com` | `https://<ai-resource>.services.ai.azure.com/models` |
| Credentials | One per model/endpoint. | One per Azure AI Services resource. You can use Microsoft Entra ID too. |
| Model parameter | None. | Required. Use the name of the model deployment. |


### Clean-up existing serverless API deployments from your project

After you refactored your code, you might want to delete the existing serverless API deployments inside of the project (if any).

For each model deployed as serverless API deployments, follow these steps:

1. Go to [Azure AI Foundry portal](https://ai.azure.com/?cid=learnDocs).

2. Select **Models + endpoints**.

3. Identify the endpoints of type **serverless API deployment** and select the one you want to delete.

4. Select the option **Delete**.

    > [!WARNING]
    > This operation can't be reverted. Ensure that the endpoint isn't currently used by any other user or piece of code.

5. Confirm the operation by selecting **Delete**.

6. If you created a **serverless API deployment connection** to this endpoint from other projects, such connections aren't removed and continue to point to the inexistent endpoint. Delete any of those connections for avoiding errors.

## Limitations

Consider the following limitations when configuring your project to use Foundry Models:

* Only models supporting serverless API deployments are available for deployment to Foundry Models. Models requiring compute quota from your subscription (Managed Compute), including custom models, can only be deployed within a given project as Managed Online Endpoints and continue to be accessible using their own set of endpoint URI and credentials.
* Models available as both serverless API deployments and managed compute offerings are, by default, deployed to Foundry Models in Azure AI Foundry Services resources. Azure AI Foundry portal doesn't offer a way to deploy them to Managed Online Endpoints. You have to turn off the feature mentioned at [Configure the project to use Foundry Models](#configure-the-project-to-use-foundry-models) or use the Azure CLI/Azure ML SDK/ARM templates to perform the deployment.

## Next steps

* [Add more models](../../model-inference/how-to/create-model-deployments.md) to your endpoint.
