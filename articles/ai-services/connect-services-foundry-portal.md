---
title: How to use Foundry Tools in Microsoft Foundry portal
titleSuffix: Foundry Tools
description: Learn how to use Foundry Tools in Microsoft Foundry portal. You can use existing Foundry Tools resources in Microsoft Foundry portal by creating a connection to the resource.
manager: nitinme
ms.service: azure-ai-services
ms.custom:
  - ignite-2023
  - build-2024
  - ignite-2024
ms.topic: how-to
ms.date: 12/11/2025
ms.reviewer: lajanuar
ms.author: lajanuar
author: laujan
---

# How to use Foundry Tools in Microsoft Foundry portal

You might have existing resources for Foundry Tools that you used in the old studios such as Azure OpenAI Studio or Speech Studio. You can pick up where you left off by using your existing resources in the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs).

This article describes how to use new or existing Foundry Tools resources in a Foundry project.

## Usage scenarios

Depending on the Foundry Tool and model you want to use, you can use them in Foundry portal via:
- [Bring your existing Foundry Tools resources](#connect-foundry-tools-after-you-create-a-project) into a project. You can use your existing Foundry Tools resources in a Foundry project by creating a connection to the resource.
- The [model catalog](#discover-foundry-models-in-the-model-catalog). You don't need a project to browse and discover Foundry Models. Some of the Foundry Tools are available for you to try via the model catalog without a project. Some Foundry Tools require a project to use them in the playgrounds.
- The [project-level playgrounds](#try-foundry-tools-in-the-project-level-playgrounds).
- [Fine-tune](#fine-tune-foundry-tools) models. You can fine-tune a subset of Foundry Tools models in Foundry portal.
- [Deploy](#deploy-models-to-production) models. You can deploy base models and fine-tuned models to production. Most Foundry Tools models are already deployed and ready to use.

### Connect Foundry Tools after you create a project

You can connect Foundry Tools resources to a Foundry project after you create a project. To use your existing Foundry Tools resources (such as Azure Speech in Foundry Tools) in a Foundry project, you need to create a connection to the resource.

1. Create a Foundry project. For detailed instructions, see [Create a Foundry project](../ai-foundry/how-to/create-projects.md).
1. Go to your Foundry project.
1. Select **Management center** from the left pane.
1. Select **Connected resources** (under **Project**) from the left pane. 
1. Select **+ New connection**.

    :::image type="content" source="./media/ai-foundry/connections-add.png" alt-text="Screenshot of the connected resources page with the button to create a new connection." lightbox="./media/ai-foundry/connections-add.png":::

1. On the **Add a connection to external assets** page, select the kind of resource that you want to connect to the project. For example, you can select Foundry Tools (for a connection to multiple services in one resource), Azure OpenAI in Foundry Models, Azure Content Safety, Azure Speech, Azure Language, and other Foundry Tools.

    :::image type="content" source="./media/ai-foundry/connections-add-assets.png" alt-text="Screenshot of the page to select the kind of Foundry Tool that you want to connect to the project." lightbox="./media/ai-foundry/connections-add-assets.png":::

1. On the next page in the wizard, browse or search to find the resource you want to connect. Then select **Add connection**.  

    :::image type="content" source="./media/ai-foundry/connections-add-speech.png" alt-text="Screenshot of the page to select the Foundry Tools that you want to connect to the project." lightbox="./media/ai-foundry/connections-add-speech.png":::

1. After the resource is connected, select **Close** to return to the **Connected resources** page. You should see the new connection listed.

## Discover Foundry Models in the model catalog

You can discover Foundry Models in the model catalog without a project. Some Foundry Tools are available for you to try via the model catalog without a project. 

1. Go to the [Azure Model catalog page](https://ai.azure.com/explore/models) in Foundry portal.
1. Scroll down the page to see the list of available models. You can also use the search box to find a specific model.
1. From the **Collections** dropdown, select **Microsoft**. Search for Foundry Tools by entering **azure-ai** in the search box.

    :::image type="content" source="./media/ai-foundry/ai-services-model-catalog.png" alt-text="Screenshot of the model catalog page in Foundry portal with the option to search by collection and name." lightbox="./media/ai-foundry/ai-services-model-catalog.png":::

1. Select a model to view more details about it. You can also try the model if it's available for you to try without a project.

## Try Foundry Tools in the project level playgrounds

In the project-level playgrounds, you can try Foundry Tools such as Azure Speech and Azure Language.

1. Go to your Foundry project. If you need to create a project, see [Create a Foundry project](../ai-foundry/how-to/create-projects.md).
1. Select **Playgrounds** from the left pane and then select a playground to use. In this example, select **Try the Speech playground**.

    :::image type="content" source="./media/ai-foundry/azure-ai-services-playgrounds.png" alt-text="Screenshot of the project level playgrounds that you can use." lightbox="./media/ai-foundry/azure-ai-services-playgrounds.png":::

## Fine-tune Foundry Tools

In Foundry portal, you can fine-tune some Foundry Tools. For example, you can fine-tune a model for custom speech. 

1. Go to your Foundry project. If you need to create a project, see [Create a Foundry project](../ai-foundry/how-to/create-projects.md).
1. Select **Fine-tuning** from the left pane.
1. Select **AI Service fine-tuning**.

    :::image type="content" source="./media/ai-foundry/fine-tune-azure-ai-services.png" alt-text="Screenshot of the page to select fine-tuning of Foundry Tools." lightbox="./media/ai-foundry/fine-tune-azure-ai-services.png":::

1. Select **+ Fine-tune**.
1. Follow the wizard to fine-tune a model for the capabilities that you want.

## Deploy models to production

Once you have a project, several Foundry Tools are already deployed and ready to use. 

1. Go to your Foundry project.
1. Select **Models + endpoints** (under **My assets**) from the left pane. 
1. Select the **Service endpoints** tab to view the list of Foundry Tools models that are already deployed.

    :::image type="content" source="./media/ai-foundry/models-endpoints-ai-services-deployments.png" alt-text="Screenshot of the models and endpoints page to view Foundry Tools endpoints." lightbox="./media/ai-foundry/models-endpoints-ai-services-deployments.png":::

    In this example, we see six Foundry Tools deployments (such as Azure Speech and Azure Language) via the default connection. These models were already available for use when you created the project.

You don't deploy Foundry Tools from the **Models + endpoints** page. Foundry Tools models are already deployed and ready to use.

However, you can deploy [fine-tuned Foundry tools](#fine-tune-foundry-tools). For example, you might want to deploy a custom speech model that you fine-tuned. In this case, you can deploy the model from the corresponding fine-tuning page. 

## Related content

- [What are Foundry Tools?](./what-are-ai-services.md)
- [How to add a new connection in Foundry portal](../ai-foundry/how-to/connections-add.md)
