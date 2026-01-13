---
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: include
ms.date: 1/21/2025
ms.author: fasantia
author: santiagxf
---

As opposite to GitHub Models where all the models are already configured, the Foundry Tools resource allows you to control which models are available in your endpoint and under which configuration.

You can add all the models you need in the endpoint by using [Microsoft Foundry for GitHub](https://ai.azure.com/github). In the following example, we add a `Mistral-Large` model in the service:

1. Go to **Model catalog** section in [Foundry for GitHub](https://ai.azure.com/github).

2. Scroll to the model you're interested in and select it.
   
   :::image type="content" source="../../media/add-model-deployments/models-search-and-deploy.gif" alt-text="An animation showing how to search models in the model catalog and select one for viewing its details." lightbox="../../media/add-model-deployments/models-search-and-deploy.gif":::

3. You can review the details of the model in the model card.

4. Select **Deploy**.

5. For model providers that require more terms of contract, you are asked to accept those terms. This is the case for Mistral models for instance. Accept the terms on those cases by selecting **Subscribe and deploy**.
   
   :::image type="content" source="../../media/add-model-deployments/models-deploy-agree.png" alt-text="Screenshot showing how to agree the terms and conditions of a Mistral-Large model." lightbox="../../media/add-model-deployments/models-deploy-agree.png":::

6.  You can configure the deployment settings at this time. By default, the deployment receives the name of the model you're deploying. The deployment name is used in the `model` parameter for request to route to this particular model deployment. This allows you to also configure specific names for your models when you attach specific configurations. For instance `o1-preview-safe` for a model with a strict content filter. Use third-party models like Mistral, you can also configure the deployment to use a specific version of the model.

   > [!TIP]
   > Each model can support different deployments types, providing different data residency or throughput guarantees. See [deployment types](../../concepts/deployment-types.md) for more details.

7.  Use the **Customize** option if you need to change settings like [content filter](../../concepts/content-filter.md).
   
   :::image type="content" source="../../media/add-model-deployments/models-deploy-customize.png" alt-text="Screenshot showing how to customize the deployment if needed." lightbox="../../media/add-model-deployments/models-deploy-customize.png":::

8.  Select **Deploy**.

9.  Once the deployment completes, the new model is listed in the page and it's ready to be used.