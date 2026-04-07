---
title: "Deploy Microsoft Foundry Models in the Foundry portal"
description: "Learn how to deploy Microsoft Foundry Models in the Foundry portal for AI inference applications and integration into your projects."
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: how-to
ms.date: 02/09/2026
ms.custom:
  - ignite-2024, github-universe-2024, pilot-ai-workflow-jan-2026
  - classic-and-new
  - doc-kit-assisted
author: msakande   
ms.author: mopeakande
manager: nitinme
recommendations: false
ai-usage: ai-assisted

#CustomerIntent: As a developer or AI practitioner, I want to deploy Microsoft Foundry Models in the Foundry portal so that I can integrate these AI models into my applications and perform inference tasks for my business needs.
---

# Deploy Microsoft Foundry Models in the Foundry portal

[!INCLUDE [deploy-foundry-models 1](../includes/how-to-deploy-foundry-models-1.md)]

## Deploy a model

Deploy a model by following these steps in the Foundry portal:

1. [!INCLUDE [version-sign-in](../../includes/version-sign-in.md)]

1. From the Foundry portal homepage, select **Discover** in the upper-right navigation, then **Models** in the left pane.

1. Select a model and review its details in the model card. This article uses `Llama-3.2-90B-Vision-Instruct` for illustration.

1. Select **Deploy** > **Custom settings** to customize your deployment. Alternatively, you can use the default deployment settings by selecting **Deploy** > **Default settings**.

1. For [Foundry Models from partners and community](../concepts/models-from-partners.md), you need to subscribe to Azure Marketplace. This requirement applies to `Llama-3.2-90B-Vision-Instruct`, for example. Read the terms of use and select **Agree and Proceed** to accept the terms.

   > [!NOTE]
   > For [Foundry Models sold directly by Azure](../concepts/models-sold-directly-by-azure.md), such as the Azure OpenAI model `gpt-4o-mini`, you don't subscribe to Azure Marketplace.

1. Configure the deployment settings:

   - By default, the deployment uses the model name. You can modify this name before deploying.
   - During inference, the deployment name is used in the `model` parameter to route requests to this particular deployment.

   Select **Deploy** to create your deployment.

   > [!TIP]
   > Each model supports different deployment types, providing different data residency or throughput guarantees. See [deployment types](../concepts/deployment-types.md) for more details. In this example, the model supports the Global Standard deployment type.

1. When the deployment completes, you land on the [Foundry Playgrounds](../../concepts/concept-playgrounds.md) where you can interactively test the model. Your project and resource must be in one of the supported regions of deployment for the model. Verify that the deployment status shows **Succeeded** in your deployment list.

## Manage models

You can manage the existing model deployments in the resource by using the Foundry portal.

1. Select **Build** in the upper-right navigation.

1. Select **Models** in the left pane to see the list of deployments in the resource.

From a deployment's detail page, you can view endpoint details and keys, adjust deployment settings, or delete a deployment that you no longer need.

## Test the deployment in the playground

You can interact with the new model in the Foundry portal by using the playground. The playground is a web-based interface that lets you interact with the model in real-time. Use the playground to test the model with different prompts and see the model's responses.

1. From the list of deployments, select the **Llama-3.2-90B-Vision-Instruct** deployment to open up the playground page.

1. Type your prompt and see the outputs.

1. Select the **Code** tab to see details about how to access the model deployment programmatically.

[!INCLUDE [deploy-foundry-models 2](../includes/how-to-deploy-foundry-models-2.md)]
