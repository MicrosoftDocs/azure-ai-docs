---
manager: nitinme
author: santiagxf
ms.author: fasantia 
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.date: 09/29/2025
ms.topic: include
zone_pivot_groups: azure-ai-models-deployment
---

[!INCLUDE [Header](intro.md)]


## Add a model

Add models to the Foundry Models endpoint by following these steps:

1. Go to the **Model catalog** section in [Microsoft Foundry portal](https://ai.azure.com/explore/models).

1. Select the model you want. This article uses Mistral-Large-2411 for illustration.

1. Review the details of the model in the model card.

1. Select **Use this model**.

1. For [Foundry Models from partners and community](../../concepts/models-from-partners.md), you need to subscribe to Azure Marketplace. This requirement applies to Mistral-Large-2411, for example. Select **Agree and Proceed** to accept the terms.

   :::image type="content" source="../../media/add-model-deployments/models-deploy-agree.png" alt-text="Screenshot showing how to agree the terms and conditions of a Mistral-Large model." lightbox="../../media/add-model-deployments/models-deploy-agree.png":::

1. Configure the deployment settings. By default, the deployment receives the name of the model you're deploying. The deployment name is used in the `model` parameter for request to route to this particular model deployment. This naming convention allows you to configure specific names for your models when you attach specific configurations. For instance, use `o1-preview-safe` for a model with a strict content filter.

   > [!TIP]
   > Each model supports different deployment types, providing different data residency or throughput guarantees. See [deployment types](../../concepts/deployment-types.md) for more details.

1. The portal automatically selects a Foundry connection depending on your project. Use the **Customize** option to change the connection based on your needs. If you're deploying under the **Serverless API** deployment type, the models need to be available in the region of the Foundry resource.
   
   :::image type="content" source="../../media/add-model-deployments/models-deploy-customize.png" alt-text="Screenshot showing how to customize the deployment if needed." lightbox="../../media/add-model-deployments/models-deploy-customize.png":::

   > [!TIP]
   > If the desired resource isn't listed, you might need to create a connection to it. See [Configure Foundry Models in my project](../../how-to/configure-project-connection.md) in Foundry portal.

1. Select **Deploy**.

1. When the deployment completes, the new model is listed in the page and it's ready to use.

## Manage models

You can manage the existing model deployments in the resource by using the Foundry portal.

1. Go to the **Models + Endpoints** section in [Foundry portal](https://ai.azure.com/?cid=learnDocs).

1. The portal groups and displays model deployments per connection. Select the **Mistral-Large-2411** model deployment from the section for your Foundry resource. This action opens the model's deployment page.

   :::image type="content" source="../../media/add-model-deployments/endpoints-foundry-resource-connection.png" alt-text="Screenshot showing the list of models available under a given connection." lightbox="../../media/add-model-deployments/endpoints-foundry-resource-connection.png":::


## Test the deployment in the playground

You can interact with the new model in Foundry portal by using the playground:

1. From the model's deployment page, select **Open in playground**. This action opens the chat playground with the name of your deployment already selected.

   :::image type="content" source="../../media/add-model-deployments/playground-chat-models.png" alt-text="Screenshot showing how to select a model deployment to use in playground." lightbox="../../media/add-model-deployments/playground-chat-models.png":::

1. Type your prompt and see the outputs.

1. Use **View code** to see details about how to access the model deployment programmatically.
