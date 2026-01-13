---
manager: nitinme
author: santiagxf
ms.author: fasantia 
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.date: 1/21/2025
ms.topic: include
zone_pivot_groups: azure-ai-models-deployment
---

[!INCLUDE [Header](intro.md)]

* An AI project resource.

* The **Deploy models to Azure AI model inference service** feature is turned on.

   :::image type="content" source="../../media/quickstart-ai-project/ai-project-inference-endpoint.gif" alt-text="An animation showing how to turn on the Deploy models to Azure AI model inference service feature in Microsoft Foundry portal." lightbox="../../media/quickstart-ai-project/ai-project-inference-endpoint.gif":::

## Add a connection

You can create a connection to a Foundry Tools resource using the following steps:

1. Go to [Foundry portal](https://ai.azure.com/?cid=learnDocs).

2. In the lower left corner of the screen, select **Management center**.

3. In the section **Connected resources** select **New connection**.

4. Select **Foundry Tools**.

5. In the browser, look for an existing Foundry Tools resource in your subscription.

6. Select **Add connection**.

7. The new connection is added to your Hub.

8. Return to the project's landing page to continue and now select the new created connection. Refresh the page if it doesn't show up immediately. 

   :::image type="content" source="../../media/quickstart-ai-project/overview-endpoint-and-key.png" alt-text="Screenshot of the landing page for the project, highlighting the location of the connected resource and the associated inference endpoint." lightbox="../../media/quickstart-ai-project/overview-endpoint-and-key.png":::

## See model deployments in the connected resource

You can see the model deployments available in the connected resource by following these steps:

1. Go to [Foundry portal](https://ai.azure.com/?cid=learnDocs).

2. On the left pane, select **Models + endpoints**.

3. The page displays the model deployments available to your, grouped by connection name. Locate the connection you have just created, which should be of type **Foundry Tools**.

   :::image type="content" source="../../media/quickstart-ai-project/endpoints-ai-services-connection.png" alt-text="Screenshot showing the list of models available under a given connection." lightbox="../../media/quickstart-ai-project/endpoints-ai-services-connection.png":::

4. Select any model deployment you want to inspect.

5. The details page shows information about the specific deployment. If you want to test the model, you can use the option **Open in playground**.

6. The Foundry playground is displayed, where you can interact with the given model.
