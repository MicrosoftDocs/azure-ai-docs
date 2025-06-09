---
title: How to use Azure AI services in Azure AI Foundry portal
titleSuffix: Azure AI Services
description: Learn how to use Azure AI services in Azure AI Foundry portal. You can use existing Azure AI services resources in Azure AI Foundry portal by creating a connection to the resource.
manager: nitinme
ms.service: azure-ai-services
ms.custom:
  - ignite-2023
  - build-2024
  - ignite-2024
ms.topic: how-to
ms.date: 4/14/2025
ms.reviewer: eur
ms.author: eur
author: eric-urban
---

# How to use Azure AI services in Azure AI Foundry portal

You might have existing resources for Azure AI services that you used in the old studios such as Azure OpenAI Studio or Speech Studio. You can pick up where you left off by using your existing resources in the [Azure AI Foundry portal](https://ai.azure.com/?cid=learnDocs).

This article describes how to use new or existing Azure AI services resources in an Azure AI Foundry project.

## Usage scenarios

Depending on the AI service and model you want to use, you can use them in Azure AI Foundry portal via:
- [Bring your existing Azure AI services resources](#connect-azure-ai-services-after-you-create-a-project) into a project. You can use your existing Azure AI services resources in an Azure AI Foundry project by creating a connection to the resource.
- The [model catalog](#discover-azure-ai-models-in-the-model-catalog). You don't need a project to browse and discover Azure AI models. Some of the Azure AI services are available for you to try via the model catalog without a project. Some Azure AI services require a project to use them in the playgrounds.
- The [project-level playgrounds](#try-azure-ai-services-in-the-project-level-playgrounds). 
- [Fine-tune](#fine-tune-azure-ai-services-models) models. You can fine-tune a subset of Azure AI services models in Azure AI Foundry portal.
- [Deploy](#deploy-models-to-production) models. You can deploy base models and fine-tuned models to production. Most Azure AI services models are already deployed and ready to use.

### Connect Azure AI services after you create a project

You can connect Azure AI services resources to an Azure AI Foundry project after you create a project. To use your existing Azure AI services resources (such as Azure AI Speech) in an Azure AI Foundry project, you need to create a connection to the resource.

1. Create an Azure AI Foundry project. For detailed instructions, see [Create an Azure AI Foundry project](../ai-foundry/how-to/create-projects.md).
1. Go to your Azure AI Foundry project.
1. Select **Management center** from the left pane.
1. Select **Connected resources** (under **Project**) from the left pane. 
1. Select **+ New connection**.

    :::image type="content" source="./media/ai-foundry/connections-add.png" alt-text="Screenshot of the connected resources page with the button to create a new connection." lightbox="./media/ai-foundry/connections-add.png":::

1. On the **Add a connection to external assets** page, select the kind of AI service that you want to connect to the project. For example, you can select Azure AI services (for a connection to multiple services in one resource), Azure OpenAI in Azure AI Foundry Models, Azure AI Content Safety, Azure AI Speech, Azure AI Language, and other AI services.

    :::image type="content" source="./media/ai-foundry/connections-add-assets.png" alt-text="Screenshot of the page to select the kind of AI service that you want to connect to the project." lightbox="./media/ai-foundry/connections-add-assets.png":::

1. On the next page in the wizard, browse or search to find the resource you want to connect. Then select **Add connection**.  

    :::image type="content" source="./media/ai-foundry/connections-add-speech.png" alt-text="Screenshot of the page to select the Azure AI resource that you want to connect to the project." lightbox="./media/ai-foundry/connections-add-speech.png":::

1. After the resource is connected, select **Close** to return to the **Connected resources** page. You should see the new connection listed.

## Discover Azure AI models in the model catalog

You can discover Azure AI models in the model catalog without a project. Some Azure AI services are available for you to try via the model catalog without a project. 

1. Go to the [Azure AI model catalog page](https://ai.azure.com/explore/models) in Azure AI Foundry portal.
1. Scroll down the page to see the list of available models. You can also use the search box to find a specific model.
1. From the **Collections** dropdown, select **Microsoft**. Search for Azure AI services models by entering **azure-ai** in the search box.

    :::image type="content" source="./media/ai-foundry/ai-services-model-catalog.png" alt-text="Screenshot of the model catalog page in Azure AI Foundry portal with the option to search by collection and name." lightbox="./media/ai-foundry/ai-services-model-catalog.png":::

1. Select a model to view more details about it. You can also try the model if it's available for you to try without a project.

## Try Azure AI services in the project level playgrounds

In the project-level playgrounds, you can try Azure AI services such as Azure AI Speech and Azure AI Language. 

1. Go to your Azure AI Foundry project. If you need to create a project, see [Create an Azure AI Foundry project](../ai-foundry/how-to/create-projects.md).
1. Select **Playgrounds** from the left pane and then select a playground to use. In this example, select **Try the Speech playground**.

    :::image type="content" source="./media/ai-foundry/azure-ai-services-playgrounds.png" alt-text="Screenshot of the project level playgrounds that you can use." lightbox="./media/ai-foundry/azure-ai-services-playgrounds.png":::

1. Optionally, you can select a different connection to use in the playground. 

    :::image type="content" source="./media/ai-foundry/speech-playground.png" alt-text="Screenshot of the Speech playground in a project." lightbox="./media/ai-foundry/speech-playground.png":::

## Fine-tune Azure AI services models

In Azure AI Foundry portal, you can fine-tune some Azure AI services models. For example, you can fine-tune a model for custom speech. 

1. Go to your Azure AI Foundry project. If you need to create a project, see [Create an Azure AI Foundry project](../ai-foundry/how-to/create-projects.md).
1. Select **Fine-tuning** from the left pane.
1. Select **AI Service fine-tuning**.

    :::image type="content" source="./media/ai-foundry/fine-tune-azure-ai-services.png" alt-text="Screenshot of the page to select fine-tuning of Azure AI Services models." lightbox="./media/ai-foundry/fine-tune-azure-ai-services.png":::

1. Select **+ Fine-tune**.
1. Follow the wizard to fine-tune a model for the capabilities that you want.

## Deploy models to production

Once you have a project, several Azure AI services models are already deployed and ready to use. 

1. Go to your Azure AI Foundry project.
1. Select **Models + endpoints** (under **My assets**) from the left pane. 
1. Select the **Service endpoints** tab to view the list of Azure AI services models that are already deployed.

    :::image type="content" source="./media/ai-foundry/models-endpoints-ai-services-deployments.png" alt-text="Screenshot of the models and endpoints page to view Azure AI services endpoints." lightbox="./media/ai-foundry/models-endpoints-ai-services-deployments.png":::

    In this example, we see six Azure AI Services deployments (such as Azure AI Speech and Azure AI Language) via the default connection. These models were already available for use when you created the project.

There's no option to deploy Azure AI services models from the **Models + endpoints** page. Azure AI services models are already deployed and ready to use.

However, you can deploy [fine-tuned Azure AI services models](#fine-tune-azure-ai-services-models). For example, you might want to deploy a custom speech model that you fine-tuned. In this case, you can deploy the model from the corresponding fine-tuning page. 

## Related content

- [What are Azure AI services?](./what-are-ai-services.md)
- [How to add a new connection in Azure AI Foundry portal](../ai-foundry/how-to/connections-add.md)
