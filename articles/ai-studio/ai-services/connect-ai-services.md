---
title: Use your existing Azure AI services resources in Azure AI Studio
titleSuffix: Azure AI Studio
description: Learn how to use your existing Azure AI services resources in Azure AI Studio.
manager: nitinme
ms.service: azure-ai-studio
ms.custom:
  - ignite-2023
  - build-2024
  - ignite-2024
ms.topic: how-to
ms.date: 11/19/2024
ms.reviewer: eur
ms.author: eur
author: eric-urban
---

# How to use your existing Azure AI services resources in Azure AI Studio

You might have existing Azure AI services resources that you created using the old studios such as Azure OpenAI Studio or Speech Studio. You can pick up where you left off by using your existing resources in AI Studio.

This article describes how to use new or existing Azure AI services resources in an AI Studio project.

## Usage scenarios

Depending on the AI service and model you want to use, you can use them in AI Studio via:
- The [model catalog](#discover-azure-ai-models-in-the-model-catalog). You don't need a project to browse and discover Azure AI models. Some of the Azure AI services are available for you to try via the model catalog without a project. Some Azure AI services require a project to use in the playgrounds.
- The [project-level playgrounds](#try-azure-ai-services-in-the-project-level-playgrounds). You need a project to try Azure AI services such as Azure AI Speech and Azure AI Language. 
- [Azure AI Services demo pages](#try-out-azure-ai-services-demos). You can browse Azure AI services capabilities and step through the demos. You can try some limited demos for free without a project.
- [Fine-tune](#fine-tune-azure-ai-models) models. You can fine-tune a subset of Azure AI services models in AI Studio.
- [Deploy](#deploy-models-to-production) models. You can deploy base models and fine-tuned models to production. Most Azure AI services models are already deployed and ready to use.

## Use your Azure AI services resources in a project

To use your existing Azure AI services resources (such as Azure AI Speech) in an AI Studio project, you need to create a connection to the resource.

1. Create an AI Studio project. For detailed instructions, see [Create an AI Studio project](../how-to/create-projects.md).
1. Go to your AI Studio project.
1. Select **Management center** from the left pane.
1. Select **Connected resources** (under **Project**) from the left pane. 
1. Select **+ New connection**.

    :::image type="content" source="../media/ai-services/connections-add.png" alt-text="Screenshot of the connected resources page with the button to create a new connection." lightbox="../media/ai-services/connections-add.png":::

1. On the **Add a connection to external assets** page, select the kind of AI service that you want to connect to the project. For example, you can select Azure OpenAI Service, Azure AI Content Safety, Azure AI Speech, Azure AI Language, and other AI services.

    :::image type="content" source="../media/ai-services/connections-add-assets.png" alt-text="Screenshot of the page to select the kind of AI service that you want to connect to the project." lightbox="../media/ai-services/connections-add-assets.png":::

1. On the next page in the wizard, browse or search to find the resource you want to connect. Then select **Add connection**.  

    :::image type="content" source="../media/ai-services/connections-add-speech.png" alt-text="Screenshot of the page to select the Azure AI resource that you want to connect to the project." lightbox="../media/ai-services/connections-add-speech.png":::

1. After the resource is connected, select **Close** to return to the **Connected resources** page. You should see the new connection listed.

## Discover Azure AI models in the model catalog

You can discover Azure AI models in the model catalog without a project. Some Azure AI services are available for you to try via the model catalog without a project. 

1. Go to the [AI Studio home page](https://ai.azure.com).
1. Select the tile that says **Model catalog and benchmarks**. 

    :::image type="content" source="../media/explore/ai-studio-home-model-catalog.png" alt-text="Screenshot of the home page in Azure AI Studio with the option to select the model catalog tile." lightbox="../media/explore/ai-studio-home-model-catalog.png":::

    If you don't see this tile, you can also go directly to the [Azure AI model catalog page](https://ai.azure.com/explore/models) in AI Studio.

1. From the **Collections** dropdown, select **Microsoft**. Search for Azure AI services models by entering **azure-ai** in the search box.

    :::image type="content" source="../media/ai-services/models/ai-services-model-catalog.png" alt-text="Screenshot of the model catalog page in Azure AI Studio with the option to search by collection and name." lightbox="../media/ai-services/models/ai-services-model-catalog.png":::

1. Select a model to view more details about it. You can also try the model if it's available for you to try without a project.

## Try Azure AI services in the project level playgrounds

In the project-level playgrounds, you can try Azure AI services such as Azure AI Speech and Azure AI Language. 

1. Go to your AI Studio project. If you need to create a project, see [Create an AI Studio project](../how-to/create-projects.md).
1. Select **Playgrounds** from the left pane and then select a playground to use. In this example, select **Try the Speech playground**.

    :::image type="content" source="../media/ai-services/playgrounds/azure-ai-services-playgrounds.png" alt-text="Screenshot of the project level playgrounds that you can use." lightbox="../media/ai-services/playgrounds/azure-ai-services-playgrounds.png":::

1. Optionally, you can select a different connection to use in the playground. In the Speech playground, you can connect to Azure AI Services multi-service resources or Speech service resources. 

    :::image type="content" source="../media/ai-services/playgrounds/speech-playground.png" alt-text="Screenshot of the Speech playground in a project." lightbox="../media/ai-services/playgrounds/speech-playground.png":::

If you have other connected resources, you can use them in the corresponding playgrounds. For example, in the Language playground, you can connect to Azure AI Services multi-service resources or Azure AI Language resources.

:::image type="content" source="../media/ai-services/playgrounds/language-playground.png" alt-text="Screenshot of the Language playground in a project." lightbox="../media/ai-services/playgrounds/language-playground.png":::

## Try out Azure AI Services demos

You can browse Azure AI services capabilities and step through the demos. You can try some limited demos for free without a project.

1. Go to the [AI Studio home page](https://ai.azure.com) and make sure you're signed in with the Azure subscription that has your Azure AI services resource.
1. Find the tile that says **Explore Azure AI Services** and select **Try now**. 

    :::image type="content" source="../media/explore/home-ai-services.png" alt-text="Screenshot of the home page in Azure AI Studio with the option to select Azure AI Services." lightbox="../media/explore/home-ai-services.png":::

    If you don't see this tile, you can also go directly to the [Azure AI Services page](https://ai.azure.com/explore/aiservices) in AI Studio.

1. You should see tiles for Azure AI services that you can try. Select a tile to get to the demo page for that service. For example, select **Language + Translator**.

    :::image type="content" source="../media/ai-services/overview/ai-services-capabilities.png" alt-text="Screenshot of the landing page to try Azure AI Services try out capabilities in Azure AI Studio." lightbox="../media/ai-services/overview/ai-services-capabilities.png":::

The presentation and flow of the demo pages might vary depending on the service. In some cases, you need to select a project or connection to use the service. 

## Fine-tune Azure AI services models

In AI Studio, you can fine-tune some Azure AI services models. For example, you can fine-tune a model for custom speech. 

1. Go to your AI Studio project. If you need to create a project, see [Create an AI Studio project](../how-to/create-projects.md).
1. Select **Fine-tuning** from the left pane.
1. Select **AI Service fine-tuning** > **+ Fine-tune**.

    :::image type="content" source="../media/ai-services/fine-tune-azure-ai-services.png" alt-text="Screenshot of the page to select fine-tuning of Azure AI Services models." lightbox="../media/ai-services/fine-tune-azure-ai-services.png":::

1. Select **+ Fine-tune model**.
1. Follow the wizard to fine-tune a model for the capabilities that you want. 

## Deploy models to production

Once you have a project, several Azure AI services models are already deployed and ready to use. 

1. Go to your AI Studio project.
1. Select **Management center** from the left pane.
1. Select **Models + endpoints** (under **Project**) from the left pane. 
1. Select the **Service deployments** tab to view the list of Azure AI services models that are already deployed.

    :::image type="content" source="../media/ai-services/endpoint/models-endpoints-ai-services-deployments.png" alt-text="Screenshot of the models and endpoints page to view Azure AI services deployments." lightbox="../media/ai-services/endpoint/models-endpoints-ai-services-deployments.png":::

    In this example, we see:
    - Six Azure AI Services deployments (such as Azure AI Speech and Azure AI Language) via the default connection. These models were already available for use when you created the project.
    - Another Azure AI Speech deployment via the `contosoazureaispeecheastus` example connection. This example assumes that you connected to an Azure AI Speech resource after creating the project. For more information about connecting to Azure AI services, see [Use your existing Azure OpenAI and AI services resources](./connect-ai-services.md).

There's no option to deploy Azure AI services models from the **Models + endpoints** page. Azure AI services models are already deployed and ready to use.

However, you can deploy [fine-tuned Azure AI services models](#azure-ai-services-model-fine-tuning). For example, you might want to deploy a custom speech model that you fine-tuned. In this case, you can deploy the model from the corresponding fine-tuning page. 


## Related content

- [What are Azure AI services?](../../ai-services/what-are-ai-services.md?context=/azure/ai-studio/context/context)
- [Connections in Azure AI Studio](../concepts/connections.md)
