---
title: How to use Azure OpenAI Service in AI Foundry portal
titleSuffix: Azure AI Foundry
description: Learn how to use Azure OpenAI Service in AI Foundry portal.
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

# How to use Azure OpenAI Service in AI Foundry portal

You might have existing Azure OpenAI Service resources and model deployments that you created using the old Azure OpenAI Studio or via code. You can pick up where you left off by using your existing resources in AI Foundry portal.

This article describes how to:
- Use Azure OpenAI Service models outside of a project.
- Use Azure OpenAI Service models and an AI Foundry project.

> [!TIP]
> You can use Azure OpenAI Service in AI Foundry portal without creating a project or a connection. When you're working with the models and deployments, we recommend that you work outside of a project. Eventually, you want to work in a project for tasks such as managing connections, permissions, and deploying the models to production.

## Use Azure OpenAI models outside of a project

You can use your existing Azure OpenAI model deployments in AI Foundry portal outside of a project. Start here if you previously deployed models using the old Azure OpenAI Studio or via the Azure OpenAI Service SDKs and APIs.

To use Azure OpenAI Service outside of a project, follow these steps:
1. Go to the [AI Foundry home page](https://ai.azure.com) and make sure you're signed in with the Azure subscription that has your Azure OpenAI Service resource.
1. Find the tile that says **Focused on Azure OpenAI Service?** and select **Let's go**. 

    :::image type="content" source="../../media/azure-openai-in-ai-studio/home-page.png" alt-text="Screenshot of the home page in Azure AI Foundry portal with the option to select Azure OpenAI Service." lightbox="../../media/azure-openai-in-ai-studio/home-page.png":::

    If you don't see this tile, you can also go directly to the [Azure OpenAI Service page](https://ai.azure.com/resource/overview) in AI Foundry portal.

1. You should see your existing Azure OpenAI Service resources. In this example, the Azure OpenAI Service resource `contoso-azure-openai-eastus` is selected.

    :::image type="content" source="../../media/ai-services/azure-openai-studio-select-resource.png" alt-text="Screenshot of the Azure OpenAI Service resources page in Azure AI Foundry portal." lightbox="../../media/ai-services/azure-openai-studio-select-resource.png":::

    If your subscription has multiple Azure OpenAI Service resources, you can use the selector or go to **All resources** to see all your resources. 

If you create more Azure OpenAI Service resources later (such as via the Azure portal or APIs), you can also access them from this page.

## <a name="project"></a> Use Azure OpenAI Service in a project

You might eventually want to use a project for tasks such as managing connections, permissions, and deploying models to production. You can use your existing Azure OpenAI Service resources in an AI Foundry project. 

Let's look at two ways to connect Azure OpenAI Service resources to a project:

- [When you create a project](#connect-azure-openai-service-when-you-create-a-project-for-the-first-time)
- [After you create a project](#connect-azure-openai-service-after-you-create-a-project)

### Connect Azure OpenAI Service when you create a project for the first time

When you create a project for the first time, you also create a hub. When you create a hub, you can select an existing Azure AI services resource (including Azure OpenAI) or create a new AI services resource.

:::image type="content" source="../../media/how-to/projects/projects-create-resource.png" alt-text="Screenshot of the create resource page within the create project dialog." lightbox="../../media/how-to/projects/projects-create-resource.png":::

For more details about creating a project, see the [create an AI Foundry project](../../how-to/create-projects.md) how-to guide or the [create a project and use the chat playground](../../quickstarts/get-started-playground.md) quickstart.

### Connect Azure OpenAI Service after you create a project

If you already have a project and you want to connect your existing Azure OpenAI Service resources, follow these steps:

1. Go to your AI Foundry project.
1. Select **Management center** from the left pane.
1. Select **Connected resources** (under **Project**) from the left pane. 
1. Select **+ New connection**.

    :::image type="content" source="../../media/ai-services/connections-add.png" alt-text="Screenshot of the connected resources page with the button to create a new connection." lightbox="../../media/ai-services/connections-add.png":::

1. On the **Add a connection to external assets** page, select the kind of AI service that you want to connect to the project. For example, you can select Azure OpenAI Service, Azure AI Content Safety, Azure AI Speech, Azure AI Language, and other AI services.

    :::image type="content" source="../../media/ai-services/connections-add-assets.png" alt-text="Screenshot of the page to select the kind of AI service that you want to connect to the project." lightbox="../../media/ai-services/connections-add-assets.png":::

1. On the next page in the wizard, browse or search to find the resource you want to connect. Then select **Add connection**.  

    :::image type="content" source="../../media/ai-services/connections-add-azure-openai.png" alt-text="Screenshot of the page to select the Azure AI Service resource that you want to connect to the project." lightbox="../../media/ai-services/connections-add-azure-openai.png":::

1. After the resource is connected, select **Close** to return to the **Connected resources** page. You should see the new connection listed.

## Try Azure OpenAI models in the playgrounds

You can try Azure OpenAI models in the Azure OpenAI Service playgrounds outside of a project.

> [!TIP]
> You can also try Azure OpenAI models in the project-level playgrounds. However, while you're only working with the Azure OpenAI Service models, we recommend working outside of a project.

1. Go to the [Azure OpenAI Service page](https://ai.azure.com/resource/overview) in AI Foundry portal.
1. Select a playground from under **Resource playground** in the left pane.

    :::image type="content" source="../../media/ai-services/playgrounds/azure-openai-studio-playgrounds.png" alt-text="Screenshot of the playgrounds that you can select to use Azure OpenAI Service." lightbox="../../media/ai-services/playgrounds/azure-openai-studio-playgrounds.png":::

Here are a few guides to help you get started with Azure OpenAI Service playgrounds:
- [Quickstart: Use the chat playground](../../quickstarts/get-started-playground.md)
- [Quickstart: Get started using Azure OpenAI Assistants](../../../ai-services/openai/assistants-quickstart.md?context=/azure/ai-studio/context/context)
- [Quickstart: Use GPT-4o in the real-time audio playground](../../../ai-services/openai/realtime-audio-quickstart.md?context=/azure/ai-studio/context/context)
- [Quickstart: Analyze images and video with GPT-4 for Vision in the playground](../../quickstarts/multimodal-vision.md)

Each playground has different model requirements and capabilities. The supported regions will vary depending on the model. For more information about model availability per region, see the [Azure OpenAI Service models documentation](../../../ai-services/openai/concepts/models.md).

## Fine-tune Azure OpenAI models

In AI Foundry portal, you can fine-tune several Azure OpenAI models. The purpose is typically to improve model performance on specific tasks or to introduce information that wasn't well represented when you originally trained the base model.

1. Go to the [Azure OpenAI Service page](https://ai.azure.com/resource/overview) in AI Foundry portal to fine-tune Azure OpenAI models.
1. Select **Fine-tuning** from the left pane.

    :::image type="content" source="../../media/ai-services/fine-tune-azure-openai.png" alt-text="Screenshot of the page to select fine-tuning of Azure OpenAI Service models." lightbox="../../media/ai-services/fine-tune-azure-openai.png":::

1. Select **+ Fine-tune model** in the **Generative AI fine-tuning** tabbed page.
1. Follow the [detailed how to guide](../../../ai-services/openai/how-to/fine-tuning.md?context=/azure/ai-studio/context/context) to fine-tune the model.

For more information about fine-tuning Azure AI models, see:
- [Overview of fine-tuning in AI Foundry portal](../../concepts/fine-tuning-overview.md)
- [How to fine-tune Azure OpenAI models](../../../ai-services/openai/how-to/fine-tuning.md?context=/azure/ai-studio/context/context)
- [Azure OpenAI models that are available for fine-tuning](../../../ai-services/openai/concepts/models.md?context=/azure/ai-studio/context/context)


## Deploy models to production

You can deploy Azure OpenAI base models and fine-tuned models to production via the AI Foundry portal.

1. Go to the [Azure OpenAI Service page](https://ai.azure.com/resource/overview) in AI Foundry portal.
1. Select **Deployments** from the left pane.

    :::image type="content" source="../../media/ai-services/endpoint/models-endpoints-azure-openai-deployments.png" alt-text="Screenshot of the models and endpoints page to view and create Azure OpenAI Service deployments." lightbox="../../media/ai-services/endpoint/models-endpoints-azure-openai-deployments.png":::

You can create a new deployment or view existing deployments. For more information about deploying Azure OpenAI models, see [Deploy Azure OpenAI models to production](../../how-to/deploy-models-openai.md).

## Develop apps with code

At some point, you want to develop apps with code. Here are some developer resources to help you get started with Azure OpenAI Service and Azure AI services:
- [Azure OpenAI Service and Azure AI services SDKs](../../../ai-services/reference/sdk-package-resources.md?context=/azure/ai-studio/context/context)
- [Azure OpenAI Service and Azure AI services REST APIs](../../../ai-services/reference/rest-api-resources.md?context=/azure/ai-studio/context/context)
- [Quickstart: Get started building a chat app using code](../../quickstarts/get-started-code.md)
- [Quickstart: Get started using Azure OpenAI Assistants](../../../ai-services/openai/assistants-quickstart.md?context=/azure/ai-studio/context/context)
- [Quickstart: Use real-time speech to text](../../../ai-services/speech-service/get-started-speech-to-text.md?context=/azure/ai-studio/context/context)


## Related content

- [Azure OpenAI in AI Foundry portal](../../azure-openai-in-ai-studio.md)
- [Use Azure AI services resources](./connect-ai-services.md)
