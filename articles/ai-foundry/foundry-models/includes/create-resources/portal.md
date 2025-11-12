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

## Create the resources

To create a project with a Microsoft Foundry (formerly known Azure AI Services) resource, follow these steps:

1. Go to [Foundry portal](https://ai.azure.com/?cid=learnDocs).

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
    | Hub            | The main container for AI projects in Foundry. Hubs promote collaboration and allow you to store information for your projects. |
    | Foundry    | In this tutorial, a new account is created, but Foundry Services can be shared across multiple hubs and projects. Hubs use a connection to the resource to have access to the model deployments available there. To learn how, you can create connections between projects and Foundry to consume Foundry Models you can read [Connect your AI project](../../how-to/configure-project-connection.md). |

8. Select **Create**. The resources creation process starts. 

9. Once completed, your project is ready to be configured.

10. To use Foundry Models, you need to add model deployments.

## Next steps

> [!div class="nextstepaction"]
> [Add and configure models](../../how-to/create-model-deployments.md)
