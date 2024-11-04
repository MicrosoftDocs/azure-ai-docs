---
title: Use your existing Azure OpenAI and AI services resources
titleSuffix: Azure AI Studio
description: Learn how to use your existing Azure OpenAI and AI services resources in Azure AI Studio.
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

# Use your existing Azure OpenAI and AI services resources

You might have existing Azure AI services resources (including Azure OpenAI model deployments) that you created using the old studios such as Azure OpenAI Studio or Speech Studio. You can pick up where you left off by using your existing resources in AI Studio.

This article describes how to:
- Use your existing Azure OpenAI model deployments without a project.
- Use your existing Azure OpenAI and AI services resources in an AI Studio project.

> [!TIP]
> Even if you don't yet have any Azure OpenAI model deployments, you can use Azure OpenAI Service in AI Studio without creating a project or a connection. If you're only using Azure OpenAI Service, we recommend working outside of a project. 

## Use your Azure OpenAI model deployments without a project

You can use your existing Azure OpenAI model deployments in AI Studio without creating a project or a connection. Start here if you previously deployed models using the old Azure OpenAI Studio or via the Azure OpenAI Service SDKs and APIs.

To use your existing Azure OpenAI deployments or to otherwise use Azure OpenAI Service without a project, follow these steps:
1. Go to the [AI Studio home page](https://ai.azure.com) and make sure you're signed in with the Azure subscription that has your Azure OpenAI Service resource (with or without model deployments.)
1. Find the tile that says **Focused on Azure OpenAI Service?** and select **Let's go**. 

    :::image type="content" source="../media/azure-openai-in-ai-studio/home-page.png" alt-text="Screenshot of the home page in Azure AI Studio with the option to select Azure OpenAI Service." lightbox="../media/azure-openai-in-ai-studio/home-page.png":::

    If you don't see this tile, you can also go directly to the [Azure OpenAI Service page](https://ai.azure.com/resource/overview) in AI Studio.

1. You should see your existing Azure OpenAI Service resources (with any existing deployments). In case your subscription has multiple Azure OpenAI Service resources, you can use the selector or go to **All resources** to see all your resources.

    :::image type="content" source="../media/ai-services/azure-openai-studio-select-resource.png" alt-text="Screenshot of the Azure OpenAI Service resources page in Azure AI Studio." lightbox="../media/ai-services/azure-openai-studio-select-resource.png":::

If you create more Azure OpenAI Service resources later (such as via the Azure portal or APIs), you can also access them from this page.

## Use your Azure OpenAI and AI services resources in a project

To use your existing Azure AI services resources (such as Azure OpenAI Service or Azure AI Speech) in an AI Studio project, you need to create a connection to the resource.

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


## Related content

- [What are Azure AI services?](../../ai-services/what-are-ai-services.md?context=/azure/ai-studio/context/context)
- [Connections in Azure AI Studio](../concepts/connections.md)
