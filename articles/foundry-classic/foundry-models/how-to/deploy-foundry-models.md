---
title: "Deploy Microsoft Foundry Models in the Foundry portal (classic)"
description: "Learn how to deploy Microsoft Foundry Models in the Foundry portal for AI inference applications and integration into your projects. (classic)"
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: how-to
ms.date: 02/09/2026
ms.custom:
  - ignite-2024, github-universe-2024, pilot-ai-workflow-jan-2026
  - classic-and-new
author: msakande   
ms.author: mopeakande
manager: nitinme
recommendations: false
ai-usage: ai-assisted

#CustomerIntent: As a developer or AI practitioner, I want to deploy Microsoft Foundry Models in the Foundry portal so that I can integrate these AI models into my applications and perform inference tasks for my business needs.
ROBOTS: NOINDEX, NOFOLLOW
---

# Deploy Microsoft Foundry Models in the Foundry portal (classic)

**Currently viewing:** :::image type="icon" source="../../../foundry/media/yes-icon.svg" border="false"::: **Foundry (classic) portal version** - [Switch to version for the new Foundry portal](../../../foundry/foundry-models/how-to/deploy-foundry-models.md)

[!INCLUDE [deploy-foundry-models 1](../../../foundry/foundry-models/includes/how-to-deploy-foundry-models-1.md)]

## Deploy a model

Deploy a model by following these steps in the Foundry portal:

1. [!INCLUDE [version-sign-in](../../includes/version-sign-in.md)]

1. Go to the **Model catalog** section in the Foundry portal.

1. Select a model and review its details in the model card. This article uses `Llama-3.2-90B-Vision-Instruct` for illustration.

1. Select **Use this model**.

1. For [Foundry Models from partners and community](../concepts/models-from-partners.md), you need to subscribe to Azure Marketplace. This requirement applies to `Llama-3.2-90B-Vision-Instruct`, for example. Read the terms of use and select **Agree and Proceed** to accept the terms.

   > [!NOTE]
   > For [Foundry Models sold directly by Azure](../concepts/models-sold-directly-by-azure.md), such as the Azure OpenAI model `gpt-4o-mini`, you don't subscribe to Azure Marketplace.

1. Configure the deployment settings:

   - By default, the deployment uses the model name. You can modify this name before deploying.
   - During inference, the deployment name is used in the `model` parameter to route requests to this particular deployment.

   > [!TIP]
   > Each model supports different deployment types, providing different data residency or throughput guarantees. See [deployment types](../concepts/deployment-types.md) for more details. In this example, the model supports the Global Standard deployment type.

1. The Foundry portal automatically selects the Foundry resource associated with your project as the **Connected AI resource**. Select **Customize** to change the connection if needed. If you're deploying under the **Serverless API** deployment type, the project and resource must be in one of the supported regions of deployment for the model.
   
   :::image type="content" source="../../../foundry/foundry-models/media/add-model-deployments/models-deploy-customize.png" alt-text="Screenshot showing how to customize the deployment if needed." lightbox="../../../foundry/foundry-models/media/add-model-deployments/models-deploy-customize.png":::

1. Select **Deploy**. The model's deployment details page opens up while the deployment is being created.

1. When the deployment completes, the model is ready for use. You can also use the [Foundry Playgrounds](../../concepts/concept-playgrounds.md) to interactively test the model.

## Manage models

You can manage the existing model deployments in the resource by using the Foundry portal.

1. Go to the **Models + Endpoints** section in [Foundry portal](https://ai.azure.com/?cid=learnDocs).

1. The portal groups and displays model deployments per resource. Select the **Llama-3.2-90B-Vision-Instruct** model deployment from the section for your Foundry resource. This action opens the model's deployment page.

   :::image type="content" source="../media/add-model-deployments/endpoints-foundry-resource-connection.png" alt-text="Screenshot showing the list of models available under a given connection." lightbox="../media/add-model-deployments/endpoints-foundry-resource-connection.png":::

## Test the deployment in the playground

You can interact with the new model in the Foundry portal by using the playground. The playground is a web-based interface that lets you interact with the model in real-time. Use the playground to test the model with different prompts and see the model's responses.

1. From the model's deployment page, select **Open in playground**. This action opens the chat playground with the name of your deployment already selected.

   :::image type="content" source="../media/add-model-deployments/playground-chat-models.png" alt-text="Screenshot showing how to select a model deployment to use in playground." lightbox="../media/add-model-deployments/playground-chat-models.png":::

1. Type your prompt and see the outputs.

1. Use **View code** to see details about how to access the model deployment programmatically.

[!INCLUDE [deploy-foundry-models 2](../../../foundry/foundry-models/includes/how-to-deploy-foundry-models-2.md)]
