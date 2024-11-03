---
title: Where can I use Azure OpenAI and AI services resources?
titleSuffix: Azure AI Studio
description: Learn where you can use your existing Azure OpenAI and AI services resources in Azure AI Studio.
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

# Where can I use Azure OpenAI and AI services resources?

In Azure AI Studio, you can use your Azure OpenAI and AI services resources in the following ways:
- Use your Azure OpenAI model deployments without a project.
- Use your Azure OpenAI and AI services resources in an AI Studio project.

> [!TIP]
> For information about how to bring your existing Azure OpenAI and AI services resources to AI Studio, see the [how-to guide](./connect-ai-services.md#use-your-azure-openai-model-deployments-without-a-project).

## Develop apps with code

This article describes where you can use your Azure OpenAI and AI services resources in AI Studio. But now or later, you might want to develop apps with code. Here are some developer resources to help you get started with Azure OpenAI Service and Azure AI services:
- [Azure OpenAI Service and Azure AI services SDKs](../../ai-services/reference/sdk-package-resources.md?context=/azure/ai-studio/context/context)
- [Azure OpenAI Service and Azure AI services REST APIs](../../ai-services/reference/rest-api-resources.md?context=/azure/ai-studio/context/context)
- [Quickstart: Get started building a chat app using code](../quickstarts/get-started-code.md)
- [Quickstart: Get started using Azure OpenAI Assistants](../../ai-services/openai/assistants-quickstart.md?context=/azure/ai-studio/context/context)
- [Quickstart: Use real-time speech to text](../../ai-services/speech-service/get-started-speech-to-text.md?context=/azure/ai-studio/context/context)

## Usage scenarios

Depending on the AI service and model you want to use, you can use them in AI Studio via:
- The [model catalog](#discover-azure-ai-models-in-the-model-catalog). You don't need a project to browse and discover Azure AI models. Some of the Azure AI services are available for you to try via the model catalog without a project. Some Azure AI services require a project to use in the playgrounds.
- The [Azure OpenAI Service playgrounds](#try-azure-openai-models-in-the-azure-openai-playgrounds). You don't need a project to try Azure OpenAI models in the Azure OpenAI Service playgrounds.
- The [project-level playgrounds](#try-azure-ai-services-and-azure-openai-in-the-project-level-playgrounds). You need a project to try Azure AI services such as Azure AI Speech and Azure AI Language. 
- [Azure AI Services demo pages](#try-out-azure-ai-services-demos). You can browse Azure AI services capabilities and step through the demos. You can try some limited demos for free without a project.
- [Fine-tune](#fine-tune-azure-ai-models) models. You can fine-tune a subset of Azure OpenAI Service and other Azure AI services models in AI Studio.
- [Deploy](#deploy-models-to-production) models. You can deploy base models and fine-tuned models to production. Most Azure AI services models are already deployed and ready to use.

Here's a table that summarizes the previous points about where you can use your Azure OpenAI Service and AI services resources in AI Studio:

| Scenario | Azure OpenAI Service | Azure AI services |
| --- | --- | --- |
| Discover models | Model catalog | Model catalog |
| Try models | Azure OpenAI Service playgrounds<br/>Project-level playgrounds | Try demo pages<br/>Project-level playgrounds |
| Fine-tune models | Yes | Yes |
| Deploy models | Yes | Fine-tuned models only |

## Discover Azure AI models in the model catalog

You can discover Azure AI models in the model catalog without a project. Some Azure AI services are available for you to try via the model catalog without a project. 

1. Go to the [AI Studio home page](https://ai.azure.com).
1. Select the tile that says **Model catalog and benchmarks**. 

    :::image type="content" source="../media/explore/ai-studio-home-model-catalog.png" alt-text="Screenshot of the home page in Azure AI Studio with the option to select the model catalog tile." lightbox="../media/explore/ai-studio-home-model-catalog.png":::

    If you don't see this tile, you can also go directly to the [Azure AI model catalog page](https://ai.azure.com/explore/models) in AI Studio.

1. From the **Collections** dropdown, select **Microsoft**. Search for Azure AI services models by entering **azure-ai** in the search box.

    :::image type="content" source="../media/ai-services/models/ai-services-model-catalog.png" alt-text="Screenshot of the model catalog page in Azure AI Studio with the option to search by collection and name." lightbox="../media/ai-services/models/ai-services-model-catalog.png":::

1. Select a model to view more details about it. You can also try the model if it's available for you to try without a project.


## Try Azure OpenAI models in the Azure OpenAI playgrounds

You can try Azure OpenAI models in the Azure OpenAI Service playgrounds without a project.

1. Go to the [Azure OpenAI Service page](https://ai.azure.com/resource/overview) in AI Studio.
1. Select a playground from under **Resource playground** in the left pane.

    :::image type="content" source="../media/ai-services/playgrounds/azure-openai-studio-playgrounds.png" alt-text="Screenshot of the playgrounds that you can select to use Azure OpenAI Service." lightbox="../media/ai-services/playgrounds/azure-openai-studio-playgrounds.png":::

Here are a few guides to help you get started with Azure OpenAI Service playgrounds:
- [Quickstart: Use the chat playground](../quickstarts/get-started-playground.md)
- [Quickstart: Get started using Azure OpenAI Assistants](../../ai-services/openai/assistants-quickstart.md?context=/azure/ai-studio/context/context)
- [Quickstart: Use GPT-4o in the real-time audio playground](../../ai-services/openai/realtime-audio-quickstart.md?context=/azure/ai-studio/context/context)
- [Quickstart: Analyze images and video with GPT-4 for Vision in the playground](../quickstarts/multimodal-vision.md)

Each playground has different model requirements and capabilities. The supported regions will vary depending on the model. For more information about model availability per region, see the [Azure OpenAI Service models documentation](../../ai-services/openai/concepts/models.md).

## Try Azure AI services and Azure OpenAI in the project level playgrounds

In the project-level playgrounds, you can try Azure AI services such as Azure AI Speech and Azure AI Language. 

> [!NOTE]
> You can also try Azure OpenAI models in the project-level playgrounds. However, if you're only using Azure OpenAI Service, [we recommend working outside of a project](./connect-ai-services.md#use-your-azure-openai-model-deployments-without-a-project).

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

The presentation and flow of the demo pages might vary depending on the service. In some cases, you need to select a project or connection to use the service. For more information about Azure AI services connections, see [Use your existing Azure OpenAI and AI services resources](./connect-ai-services.md).

## Fine-tune Azure AI models

In AI Studio, you can fine-tune several Azure OpenAI models and some of the other Azure AI services models.

### Azure OpenAI model fine-tuning

1. Go to the [Azure OpenAI Service page](https://ai.azure.com/resource/overview) in AI Studio to fine-tune Azure OpenAI models.
1. Select **Fine-tuning** from the left pane.

    :::image type="content" source="../media/ai-services/fine-tune-azure-openai.png" alt-text="Screenshot of the page to select fine-tuning of Azure OpenAI Service models." lightbox="../media/ai-services/fine-tune-azure-openai.png":::

1. Select **+ Fine-tune model**.
1. Follow the [detailed how to guide](../../ai-services/openai/how-to/fine-tuning.md?context=/azure/ai-studio/context/context) to fine-tune the model.

For more information about fine-tuning Azure AI models, see:
- [Overview of fine-tuning in AI Studio](../concepts/fine-tuning-overview.md)
- [How to fine-tune Azure OpenAI models](../../ai-services/openai/how-to/fine-tuning.md?context=/azure/ai-studio/context/context)
- [Azure OpenAI models that are available for fine-tuning](../../ai-services/openai/concepts/models.md?context=/azure/ai-studio/context/context)

### Azure AI services model fine-tuning

1. Go to your AI Studio project. If you need to create a project, see [Create an AI Studio project](../how-to/create-projects.md).
1. Select **Fine-tuning** from the left pane.
1. Select **AI Service fine-tuning** > **+ Fine-tune**.

    :::image type="content" source="../media/ai-services/fine-tune-azure-ai-services.png" alt-text="Screenshot of the page to select fine-tuning of Azure AI Services models." lightbox="../media/ai-services/fine-tune-azure-ai-services.png":::

1. Select **+ Fine-tune model**.
1. Follow the wizard to fine-tune a model for the capabilities that you want. For example, you can fine-tune a model for custom speech. 

## Deploy models to production

You can deploy Azure AI base models and fine-tuned models to production via the AI Studio.

### Azure OpenAI model deployments

For Azure OpenAI models, you can deploy them to production before or after fine-tuning.

1. Go to the [AI Studio home page](https://ai.azure.com) and make sure you're signed in with the Azure subscription that has your Azure OpenAI Service resource (with or without model deployments.)
1. Select **Deployments** from the left pane.

    :::image type="content" source="../media/ai-services/endpoint/models-endpoints-azure-openai-deployments.png" alt-text="Screenshot of the models and endpoints page to view and create Azure OpenAI Service deployments." lightbox="../media/ai-services/endpoint/models-endpoints-azure-openai-deployments.png":::

You can create a new deployment or view existing deployments. For more information about deploying Azure OpenAI models, see [Deploy Azure OpenAI models to production](../how-to/deploy-models-openai.md).

### Azure AI services model deployments

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
- [Use your existing Azure OpenAI and AI services resources](./connect-ai-services.md)
