---
manager: nitinme
ms.service: azure-ai-models
ms.custom:
ms.topic: include
ms.date: 10/08/2024
ms.author: fasantia
author: santiagxf
---

As opposite to GitHub Models where all the models are already configured, the Azure AI Services resource allow you to control which models are available in your endpoint and under which configuration.

You can add all the models you need in the endpoint by using [Azure AI Studio for GitHub](https://ai.azure.com/github). In the following example, we add a `Mistral-Large` model in the service:

1. Go to **Model catalog** section in [Azure AI Studio for GitHub](https://ai.azure.com/github).

2. Scroll to the model you are interested in and select it.
   
   :::image type="content" source="../../media/ai-services/add-model-deployments/models-search-and-deploy.gif" alt-text="An animation showing how to search models in the model catalog and select one for viewing its details." lightbox="../../media/ai-services/add-model-deployments/models-search-and-deploy.gif":::

3. You can review the details of the model in the model card.

4. Select **Deploy**.

5. For models providers that require additional terms of contract, you will be asked to accept those terms. This is the case for Mistral models for instance. Accept the terms on those cases by selecting **Subscribe and deploy**.
   
   :::image type="content" source="../../media/ai-services/add-model-deployments/models-deploy-agree.png" alt-text="An screenshot showing how to agree the terms and conditions of a Mistral-Large model." lightbox="../../media/ai-services/add-model-deployments/models-deploy-agree.png":::

6.  You can configure the deployment settings at this time. By default, the deployment receives the name of the model you are deploying. The deployment name is used in the `model` parameter for request to route to this particular model deployment. This allow you to also configure specific names for your models when you attach specific configurations. For instance `o1-preview-safe` for a model with a strict content safety content filter.

   > [!TIP]
   > Each model may support different deployments types, providing different data residency or throughput guarantees. See [deployment types](/azure/ai-studio/ai-services/concepts/deployment-types) for more details.

7.  Use the **Customize** option if you need to change settings like [content filter](/azure/ai-studio/ai-services/concepts/content-filter) or rate limiting (if available).
   
   :::image type="content" source="../../media/ai-services/add-model-deployments/models-deploy-customize.png" alt-text="An screenshot showing how to customize the deployment if needed." lightbox="../../media/ai-services/add-model-deployments/models-deploy-customize.png":::

8.  Select **Deploy**.

9.  Once the deployment completes, the new model will be listed in the page and it's ready to be used.