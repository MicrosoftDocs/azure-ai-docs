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

> [!IMPORTANT]
> Azure AI Foundry portal uses projects and hubs to create Azure AI Services accounts and configure Azure AI model inference. If you don't want to use hubs and projects, you can create the resources using either the [Azure CLI](../../how-to/quickstart-create-resources.md?pivots=programming-language-cli), [Bicep](../../how-to/quickstart-create-resources.md?pivots=programming-language-bicep), or [create the Azure AI services resource using the Azure portal](../../../../ai-services/multi-service-resource.md?context=/azure/ai-services/model-inference/context/context).

## Create the resources

To create a project with an Azure AI Services account, follow these steps:

1. Go to [Azure AI Foundry portal](https://ai.azure.com).

2. On the landing page, select **Create project**.

3. Give the project a name, for example "my-project".

4. In this tutorial, we create a brand new project under a new AI hub, hence, select **Create new hub**.

5. Give the hub a name, for example "my-hub" and select **Next**.

6. The wizard updates with details about the resources that are going to be created. Select **Azure resources to be created** to see the details.

    :::image type="content" source="../../media/create-resources/create-project-with-hub-details.png" alt-text="Screenshot showing the details of the project and hub to be created." lightbox="../../media/create-resources/create-project-with-hub-details.png":::    

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

11. Turn on the **Deploy models to Azure AI model inference service** feature.

    :::image type="content" source="../../media/quickstart-ai-project/ai-project-inference-endpoint.gif" alt-text="An animation showing how to turn on the Azure AI model inference service deploy models feature in Azure AI Foundry portal." lightbox="../../media/quickstart-ai-project/ai-project-inference-endpoint.gif":::

4. Close the panel.

10. To use Azure AI model inference, you need to add model deployments to your Azure AI services account.

## Next steps

> [!div class="nextstepaction"]
> [Add and configure models](../../how-to/create-model-deployments.md)
