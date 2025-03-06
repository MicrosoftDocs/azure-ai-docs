---
title: "Tutorial: Getting started with DeepSeek-R1 reasoning model in Azure AI model inference"
titleSuffix: Azure AI Foundry
description: Learn about the reasoning capabilities of DeepSeek-R1 in Azure AI model inference.
manager: scottpolly
ms.service: azure-ai-model-inference
ms.topic: tutorial
ms.date: 03/01/2025
ms.reviewer: fasantia
ms.author: msakande
author: mopeakande
---

# Tutorial: Get started with DeepSeek-R1 reasoning model in Azure AI model inference

In this tutorial, you learn:

> [!div class="checklist"]
> * How to create and configure the Azure resources to use DeepSeek-R1 model in Azure AI model inference.
> * How to configure the model deployment.
> * How to use DeepSeek-R1 using the Azure AI Inference SDK or REST APIs.
> * How to use DeepSeek-R1 using other SDKs.

## Prerequisites

To complete this article, you need:

* An Azure subscription. If you're using [GitHub Models](https://docs.github.com/en/github-models/), you can upgrade your experience and create an Azure subscription in the process. Read [Upgrade from GitHub Models to Azure AI model inference](../../how-to/quickstart-github-models.md) if that's your case.

[!INCLUDE [about-reasoning](../includes/use-chat-reasoning/about-reasoning.md)]

## Create the resources

Azure AI model inference is a capability in Azure AI Services resources in Azure. You can create model deployments under the resource to consume their predictions. You can also connect the resource to Azure AI Hubs and Projects in Azure AI Foundry to create intelligent applications if needed. The following picture shows the high level architecture.

:::image type="content" source="../media/quickstart-get-started-deepseek-r1/resources-architecture.png" alt-text="A diagram showing the high level architecture of the resources created in the tutorial." lightbox="../media/quickstart-get-started-deepseek-r1/resources-architecture.png":::

To create an Azure AI project that supports model inference for DeepSeek-R1, follow these steps:

1. Go to [Azure AI Foundry portal](https://ai.azure.com) and log in with your account.

2. On the landing page, select **Create project**.

3. Give the project a name, for example "my-project".

4. In this tutorial, we create a brand new project under a new AI hub, hence, select **Create new hub**. Hubs are containers for multiple projects and allow you to share resources across all the projects.

5. Give the hub a name, for example "my-hub" and select **Next**.

6. The wizard updates with details about the resources that are going to be created. Select **Azure resources to be created** to see the details.

    :::image type="content" source="../media/create-resources/create-project-with-hub-details.png" alt-text="Screenshot showing the details of the project and hub to be created." lightbox="../media/create-resources/create-project-with-hub-details.png":::    

7. You can see that the following resources are created:

    | Property       | Description |
    | -------------- | ----------- |
    | Resource group | The main container for all the resources in Azure. This helps get resources that work together organized. It also helps to have a scope for the costs associated with the entire project. |
    | Location       | The region of the resources that you're creating. |
    | Hub            | The main container for AI projects in Azure AI Foundry. Hubs promote collaboration and allow you to store information for your projects. |
    | AI Services    | The resource enabling access to the flagship models in Azure AI model catalog. In this tutorial, a new account is created, but Azure AI services resources can be shared across multiple hubs and projects. Hubs use a connection to the resource to have access to the model deployments available there. To learn how, you can create connections between projects and Azure AI Services to consume Azure AI model inference you can read [Connect your AI project](../../how-to/configure-project-connection.md). |

8. Select **Create**. The resources creation process starts. 

9. Once completed, your project is ready to be configured.

10. Azure AI model inference is a Preview feature that needs to be turned on in Azure AI Foundry. At the top navigation bar, over the right corner, select the **Preview features** icon. A contextual blade shows up at the right of the screen.

11. Turn the feature **Deploy models to Azure AI model inference service** on.

    :::image type="content" source="../media/quickstart-ai-project/ai-project-inference-endpoint.gif" alt-text="An animation showing how to turn on the Azure AI model inference service deploy models feature in Azure AI Foundry portal." lightbox="../media/quickstart-ai-project/ai-project-inference-endpoint.gif":::

12. Close the panel.


## Add DeepSeek-R1 model deployment

Let's now create a new model deployment for DeepSeek-R1:

1. Go to **Model catalog** section in [Azure AI Foundry portal](https://ai.azure.com/explore/models) and find the model [DeepSeek-R1]() model.

3. You can review the details of the model in the model card.

4. Select **Deploy**.

5. The wizard shows the model's terms and conditions. DeepSeek-R1 is offered as a Microsoft first party consumption service. You can review our privacy and security commitments under [Data, privacy, and Security](). Accept the terms on those cases by selecting **Subscribe and deploy**.

   :::image type="content" source="../media/quickstart-get-started-deepseek-r1/models-deploy-agree.png" alt-text="Screenshot showing how to agree the terms and conditions of a DeepSeek-R1 model." lightbox="../media/quickstart-get-started-deepseek-r1/models-deploy-agree.png":::

6. You can configure the deployment settings at this time. By default, the deployment receives the name of the model you're deploying. The deployment name is used in the `model` parameter for request to route to this particular model deployment. This allows you to also configure specific names for your models when you attach specific configurations.

7. We automatically select an Azure AI Services connection depending on your project. Use the **Customize** option to change the connection based on your needs. DeepSeek-R1 is currently offered under the **Global Standard** deployment type which offers higher throughput and performance.

8. Select **Deploy**.

   :::image type="content" source="../media/quickstart-get-started-deepseek-r1/models-deploy.png" alt-text="Screenshot showing how to deploy the model." lightbox="../media/quickstart-get-started-deepseek-r1/models-deploy.png":::

9.  Once the deployment completes, the new model is listed in the page and it's ready to be used.

## Use the model in playground

You can get started by using the model in the playground to have an idea of the model capabilities.

1. On the deployment details page, select **Open in playground** option in the top bar.

2. In the **Deployment** drop down, the deployment you created has been automatically selected.

3. Configure the system prompt as needed. In general, reasoning models don't use system messages in the same way that other types of models.

   :::image type="content" source="../media/quickstart-get-started-deepseek-r1/playground-chat-models.png" alt-text="Screenshot showing how to select a model deployment to use in playground, configure the system message, and test it out." lightbox="../media/quickstart-get-started-deepseek-r1/playground-chat-models.png":::

4. Type your prompt and see the outputs.

5. Additionally, you can use **View code** so see details about how to access the model deployment programmatically.

[!INCLUDE [best-practices](../includes/use-chat-reasoning/best-practices.md)]

## Use the model in code

[!INCLUDE [code-chat-reasoning](../includes/code-create-chat-reasoning.md)]

Reasoning may generate longer responses and consume a larger amount of tokens. You can see the [rate limits](../quotas-limits.md) that apply to DeepSeek-R1 models. Consider having a retry strategy to handle rate limits being applied. You can also [request increases to the default limits](../quotas-limits.md#request-increases-to-the-default-limits).

### Parameters

In general, reasoning models don't support the following parameters you can find in chat completion models:

* Temperature
* Presence penalty
* Repetition penalty
* Parameter `top_p`

## Related content

* [Use chat reasoning models](../how-to/use-chat-reasoning.md)
* [Use image embedding models](../how-to/use-image-embeddings.md)
* [Azure AI Model Inference API](.././reference/reference-model-inference-api.md)