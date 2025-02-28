---
manager: nitinme
author: santiagxf
ms.author: fasantia 
ms.service: azure-ai-model-inference
ms.date: 1/21/2025
ms.topic: include
zone_pivot_groups: azure-ai-models-deployment
---

[!INCLUDE [Header](intro.md)]

* An AI project connected to your Azure AI Services resource with the feature **Deploy models to Azure AI model inference service** on.

  * You can follow the steps at [Configure Azure AI model inference service in my project](../../how-to/quickstart-ai-project.md#configure-the-project-to-use-azure-ai-model-inference) in Azure AI Foundry.

## Add a model

You can add models to the Azure AI model inference endpoint using the following steps:

1. Go to **Model catalog** section in [Azure AI Foundry portal](https://ai.azure.com/explore/models).

2. Scroll to the model you're interested in and select it.

   :::image type="content" source="../../media/add-model-deployments/models-search-and-deploy.gif" alt-text="An animation showing how to search models in the model catalog and select one for viewing its details." lightbox="../../media/add-model-deployments/models-search-and-deploy.gif":::

3. You can review the details of the model in the model card.

4. Select **Deploy**.

5. For model providers that require more terms of contract, you'll be asked to accept those terms. This is the case for Mistral models for instance. Accept the terms on those cases by selecting **Subscribe and deploy**.

   :::image type="content" source="../../media/add-model-deployments/models-deploy-agree.png" alt-text="Screenshot showing how to agree the terms and conditions of a Mistral-Large model." lightbox="../../media/add-model-deployments/models-deploy-agree.png":::

6. You can configure the deployment settings at this time. By default, the deployment receives the name of the model you're deploying. The deployment name is used in the `model` parameter for request to route to this particular model deployment. This allows you to also configure specific names for your models when you attach specific configurations. For instance `o1-preview-safe` for a model with a strict content safety content filter.

   > [!TIP]
   > Each model can support different deployments types, providing different data residency or throughput guarantees. See [deployment types](../../concepts/deployment-types.md) for more details.

5. We automatically select an Azure AI Services connection depending on your project. Use the **Customize** option to change the connection based on your needs. If you're deploying under the **Standard** deployment type, the models need to be available in the region of the Azure AI Services resource.
   
   :::image type="content" source="../../media/add-model-deployments/models-deploy-customize.png" alt-text="Screenshot showing how to customize the deployment if needed." lightbox="../../media/add-model-deployments/models-deploy-customize.png":::

   > [!TIP]
   > If the desired resource isn't listed, you might need to create a connection to it. See [Configure Azure AI model inference service in my project](../../how-to/configure-project-connection.md) in Azure AI Foundry portal.

6. Select **Deploy**.

7. Once the deployment completes, the new model is listed in the page and it's ready to be used.

## Manage models

You can manage the existing model deployments in the resource using Azure AI Foundry portal.

1. Go to **Models + Endpoints** section in [Azure AI Foundry portal](https://ai.azure.com).

2. Scroll to the connection to your Azure AI Services resource. Model deployments are grouped and displayed per connection.

   :::image type="content" source="../../media/quickstart-ai-project/endpoints-ai-services-connection.png" alt-text="Screenshot showing the list of models available under a given connection." lightbox="../../media/quickstart-ai-project/endpoints-ai-services-connection.png":::

3. You see a list of models available under each connection. Select the model deployment you're interested in.

4. **Edit** or **Delete** the deployment as needed.


## Test the deployment in the playground

You can interact with the new model in Azure AI Foundry portal using the playground:

> [!NOTE]
> Playground is only available when working with AI projects in Azure AI Foundry. Create an AI project to get full access to all the capabilities in Azure AI Foundry.

1. Go to **Playgrounds** section in [Azure AI Foundry portal](https://ai.azure.com).

2. Depending on the type of model you deployed, select the playground needed. In this case we select **Chat playground**.

3. In the **Deployment** drop down, under **Setup** select the name of the model deployment you have created.

   :::image type="content" source="../../media/add-model-deployments/playground-chat-models.png" alt-text="Screenshot showing how to select a model deployment to use in playground." lightbox="../../media/add-model-deployments/playground-chat-models.png":::

4. Type your prompt and see the outputs.

5. Additionally, you can use **View code** so see details about how to access the model deployment programmatically.
