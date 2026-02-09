---
title: Deploy Microsoft Foundry Models in the Foundry portal
description: Learn how to deploy Microsoft Foundry Models in the Foundry portal for AI inference applications and integration into your projects.
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: how-to
ms.date: 11/21/2025
ms.custom: ignite-2024, github-universe-2024
author: msakande   
ms.author: mopeakande
manager: nitinme
recommendations: false
monikerRange: 'foundry-classic || foundry'
ai.usage: ai-assisted

#CustomerIntent: As a developer or AI practitioner, I want to deploy Microsoft Foundry Models in the Foundry portal so that I can integrate these AI models into my applications and perform inference tasks for my business needs.
---

# Deploy Microsoft Foundry Models in the Foundry portal

[!INCLUDE [version-banner](../../includes/version-banner.md)]

In this article, you learn how to use the Foundry portal to deploy a Foundry Model in a Foundry resource for use in performing inferencing tasks. Foundry Models include models such as Azure OpenAI models, Meta Llama models, and more. Once you deploy a Foundry Model, you can interact with it by using the Foundry Playground and inference it by using code. 

This article uses a Foundry Model from partners and community `Llama-3.2-90B-Vision-Instruct` for illustration. Models from partners and community require that you subscribe to Azure Marketplace before deployment. On the other hand, Foundry Models sold directly by Azure, such as Azure Open AI in Foundry Models, don't have this requirement. For more information about Foundry Models, including the regions where they're available for deployment, see [Foundry Models sold directly by Azure](../concepts/models-sold-directly-by-azure.md) and [Foundry Models from partners and community](../concepts/models-from-partners.md).

## Prerequisites

To complete this article, you need:

- An Azure subscription with a valid payment method. If you don't have an Azure subscription, create a [paid Azure account](https://azure.microsoft.com/pricing/purchase-options/pay-as-you-go) to begin. If you're using [GitHub Models](https://docs.github.com/en/github-models/), you can [upgrade to Foundry Models](quickstart-github-models.md) and create an Azure subscription in the process.

- Access to Microsoft Foundry with appropriate permissions to create and manage resources.

- A [Microsoft Foundry project](../../how-to/create-projects.md). This kind of project is managed under a Foundry resource.

- [Foundry Models from partners and community](../concepts/models-from-partners.md) require access to **Azure Marketplace** to create subscriptions. Ensure you have the [permissions required to subscribe to model offerings](configure-marketplace.md). [Foundry Models sold directly by Azure](../concepts/models-sold-directly-by-azure.md) don't have this requirement.

## Deploy a model

::: moniker range="foundry-classic"

Deploy a model by following these steps in the Foundry portal:

1. [!INCLUDE [version-sign-in](../../includes/version-sign-in.md)]

1. Go to the **Model catalog** section in the Foundry portal.

1. Select a model and review its details in the model card. This article uses `Llama-3.2-90B-Vision-Instruct` for illustration.

1. Select **Use this model**.

1. For [Foundry Models from partners and community](../concepts/models-from-partners.md), you need to subscribe to Azure Marketplace. This requirement applies to `Llama-3.2-90B-Vision-Instruct`, for example. Read the terms of use and select **Agree and Proceed** to accept the terms.

   > [!NOTE]
   > For [Foundry Models sold directly by Azure](../concepts/models-sold-directly-by-azure.md), such as the Azure OpenAI model `gpt-4o-mini`, you don't subscribe to Azure Marketplace.

1. Configure the deployment settings. By default, the deployment receives the name of the model you're deploying, but you can modify the name as needed before deploying the model. Later during inferencing, the deployment name is used in the `model` parameter to route requests to this particular model deployment. This convention allows you to configure specific names for your model deployments.

   > [!TIP]
   > Each model supports different deployment types, providing different data residency or throughput guarantees. See [deployment types](../concepts/deployment-types.md) for more details. In this example, the model supports the Global Standard deployment type.

1. The Foundry portal automatically selects the Foundry resource associated with your project as the **Connected AI resource**. Select **Customize** to change the connection if needed. If you're deploying under the **Serverless API** deployment type, the project and resource must be in one of the supported regions of deployment for the model.
   
   :::image type="content" source="../media/add-model-deployments/models-deploy-customize.png" alt-text="Screenshot showing how to customize the deployment if needed." lightbox="../media/add-model-deployments/models-deploy-customize.png":::

1. Select **Deploy**. The model's deployment details page opens up while the deployment is being created.

1. When the deployment completes, the model is ready for use. You can also use the [Foundry Playgrounds](../../concepts/concept-playgrounds.md) to interactively test the model.

::: moniker-end

::: moniker range="foundry"

Deploy a model by following these steps in the Foundry portal:

1. [!INCLUDE [version-sign-in](../../includes/version-sign-in.md)]

1. From the Foundry portal homepage, select **Discover** in the upper-right navigation, then **Models** in the left pane.

1. Select a model and review its details in the model card. This article uses `Llama-3.2-90B-Vision-Instruct` for illustration.

1. Select **Deploy** > **Custom settings** to customize your deployment. Alternatively, you can use the default deployment settings by selecting **Deploy** > **Default settings**.

1. For [Foundry Models from partners and community](../concepts/models-from-partners.md), you need to subscribe to Azure Marketplace. This requirement applies to `Llama-3.2-90B-Vision-Instruct`, for example. Read the terms of use and select **Agree and Proceed** to accept the terms.

   > [!NOTE]
   > For [Foundry Models sold directly by Azure](../concepts/models-sold-directly-by-azure.md), such as the Azure OpenAI model `gpt-4o-mini`, you don't subscribe to Azure Marketplace.

1. Configure the deployment settings. By default, the deployment receives the name of the model you're deploying, but you can modify the name as needed before deploying the model. Later during inferencing, the deployment name is used in the `model` parameter to route requests to this particular model deployment. This convention allows you to configure specific names for your model deployments. Select **Deploy** to create your deployment.

   > [!TIP]
   > Each model supports different deployment types, providing different data residency or throughput guarantees. See [deployment types](../concepts/deployment-types.md) for more details. In this example, the model supports the Global Standard deployment type.

1. The Foundry portal automatically deploys your model in the Foundry resource associated with your project. Your project and resource must be in one of the supported regions of deployment for the model. 

1. Select **Deploy**. When the deployment completes, you land on the [Foundry Playgrounds](../../concepts/concept-playgrounds.md) where you can interactively test the model.

::: moniker-end

## Manage models

::: moniker range="foundry-classic"

You can manage the existing model deployments in the resource by using the Foundry portal.

1. Go to the **Models + Endpoints** section in [Foundry portal](https://ai.azure.com/?cid=learnDocs).

1. The portal groups and displays model deployments per resource. Select the **Llama-3.2-90B-Vision-Instruct** model deployment from the section for your Foundry resource. This action opens the model's deployment page.

   :::image type="content" source="../media/add-model-deployments/endpoints-foundry-resource-connection.png" alt-text="Screenshot showing the list of models available under a given connection." lightbox="../media/add-model-deployments/endpoints-foundry-resource-connection.png":::

::: moniker-end

::: moniker range="foundry"

You can manage the existing model deployments in the resource by using the Foundry portal.

1. Select **Build** in the upper-right navigation.

1. Select **Models** in the left pane to see the list of deployments in the resource.

::: moniker-end


## Test the deployment in the playground

::: moniker range="foundry-classic"

You can interact with the new model in the Foundry portal by using the playground. The playground is a web-based interface that lets you interact with the model in real-time. Use the playground to test the model with different prompts and see the model's responses.

1. From the model's deployment page, select **Open in playground**. This action opens the chat playground with the name of your deployment already selected.

   :::image type="content" source="../media/add-model-deployments/playground-chat-models.png" alt-text="Screenshot showing how to select a model deployment to use in playground." lightbox="../media/add-model-deployments/playground-chat-models.png":::

1. Type your prompt and see the outputs.

1. Use **View code** to see details about how to access the model deployment programmatically.

::: moniker-end

::: moniker range="foundry"

You can interact with the new model in the Foundry portal by using the playground. The playground is a web-based interface that lets you interact with the model in real-time. Use the playground to test the model with different prompts and see the model's responses.

1. From the list of deployments, select the **Llama-3.2-90B-Vision-Instruct** deployment to open up the playground page.

1. Type your prompt and see the outputs.

1. Select the **Code** tab to see details about how to access the model deployment programmatically.

::: moniker-end


## Inference the model with code

To perform inferencing on the deployed model with code samples, see the following examples:

- To use the **Responses API with Foundry Models sold directly by Azure**, such as Microsoft AI, DeepSeek, and Grok models, see [How to generate text responses with Microsoft Foundry Models](generate-responses.md).

- To use the **Responses API with OpenAI models**, see [Getting started with the responses API](../../openai/how-to/responses.md).

- To use the **Chat completions API with models sold by partners**, such as the Llama model deployed in this article, see [Model support for chat completions](../../openai/api-version-lifecycle.md#model-support).

## Regional availability and quota limits of a model

For Foundry Models, the default quota varies by model and region. Certain models might only be available in some regions. For more information on availability and quota limits, see [Azure OpenAI in Microsoft Foundry Models quotas and limits](../../openai/quotas-limits.md) and [Microsoft Foundry Models quotas and limits](../quotas-limits.md).

## Quota for deploying and inferencing a model

For Foundry Models, deploying and inferencing consume quota that Azure assigns to your subscription on a per-region, per-model basis in units of Tokens-per-Minute (TPM). When you sign up for Foundry, you receive default quota for most of the available models. Then, you assign TPM to each deployment as you create it, which reduces the available quota for that model. You can continue to create deployments and assign them TPMs until you reach your quota limit.

When you reach your quota limit, you can only create new deployments of that model if you:

- Request more quota by submitting a [quota increase form](https://aka.ms/oai/stuquotarequest).
- Adjust the allocated quota on other model deployments in the Foundry portal, to free up tokens for new deployments.

For more information about quota, see [Microsoft Foundry Models quotas and limits](../quotas-limits.md) and [Manage Azure OpenAI quota](../../openai/how-to/quota.md?tabs=rest).

## Related content

- [How to generate text responses with Microsoft Foundry Models](generate-responses.md)
- [Azure OpenAI supported programming languages](../../openai/supported-languages.md)