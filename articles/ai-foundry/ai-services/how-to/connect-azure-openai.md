---
title: How to use Azure OpenAI Service in Azure AI Foundry portal
titleSuffix: Azure AI Foundry
description: Learn how to use Azure OpenAI Service in Azure AI Foundry portal.
manager: nitinme
ms.service: azure-ai-foundry
ms.custom:
  - ignite-2023
  - build-2024
  - ignite-2024
ms.topic: how-to
ms.date: 2/12/2025
ms.reviewer: eur
ms.author: eur
author: eric-urban
---

# How to use Azure OpenAI Service in Azure AI Foundry portal

Azure OpenAI Service provides REST API access to OpenAI's powerful language models. Azure OpenAI Studio was previously where you went to access and work with the Azure OpenAI Service. This studio is now integrated into [Azure AI Foundry portal](https://ai.azure.com). 
You might have existing Azure OpenAI Service resources and model deployments that you created using the old Azure OpenAI Studio or via code. You can pick up where you left off by using your existing resources in Azure AI Foundry portal.

This article describes how to:
- Use Azure OpenAI Service models outside of a project.
- Use Azure OpenAI Service models and an Azure AI Foundry project.

> [!TIP]
> You can use Azure OpenAI Service in Azure AI Foundry portal without creating a project or a connection. When you're working with the models and deployments, we recommend that you work outside of a project. Eventually, you want to work in a project for tasks such as managing connections, permissions, and deploying the models to production.

## Prerequisites

- If you don't have an Azure subscription, <a href="https://azure.microsoft.com/free/cognitive-services" target="_blank">create one for free</a>.
- You need permissions to create an Azure AI Foundry hub or have one created for you.
    - If your role is **Contributor** or **Owner**, you can follow the steps in this tutorial.
    - If your role is **Azure AI Developer**, the hub must already be created before you can complete this tutorial. Your user role must be **Azure AI Developer**, **Contributor**, or **Owner** on the hub. For more information, see [hubs](../../concepts/ai-resources.md) and [Azure AI roles](../../concepts/rbac-ai-foundry.md).
- Your subscription needs to be below your [quota limit](../../how-to/quota.md) to [deploy a new model in this tutorial](#deploy-a-chat-model). Otherwise you already need to have a [deployed chat model](../../how-to/deploy-models-openai.md).

## Focus on Azure OpenAI Service

If you've been using Azure OpenAI Studio, all your work, such as your deployments, content filters, batch jobs or fine-tuned models, is still available in Azure AI Foundry portal. All the features and functionality are still here, though the look and feel of some features are updated.

:::image type="content" source="../media/azure-openai-in-ai-studio/studio-home.png" alt-text="Screenshot shows the new Azure OpenAI in Azure AI Foundry portal." lightbox="../media/azure-openai-in-ai-studio/studio-home.png":::

Use the left navigation area to perform your tasks with Azure OpenAI models:

* **Select models**: The **Model catalog** houses all the available Azure OpenAI models.

    :::image type="content" source="../media/azure-openai-in-ai-studio/model-catalog.png" alt-text="Screenshot shows the model catalog in Azure OpenAI Service." lightbox="../media/azure-openai-in-ai-studio/model-catalog.png":::

* **Try models**: Use the various **Playgrounds** to decide which model is best for your needs.
* **Deploy models**: In the **Model catalog** or **Deployments** list in the left navigation, you see all supported models. You can deploy models from either section.
* **Fine-tune**: Use **Fine-tuning** to find your fine-tuned/custom models or create new fine-tune jobs.
* **Batch jobs**: Create and manage jobs for your global batch deployments.
* Use the resource name in the top left to switch to another recently used resource.  Or find all your Azure OpenAI Service resources in the top right-hand corner under **All resources**.

    :::image type="content" source="../media/azure-openai-in-ai-studio/all-resources.png" alt-text="Screenshot shows the top right access to all resources in Azure AI Service section of Azure AI Foundry." lightbox="../media/azure-openai-in-ai-studio/all-resources.png":::

## Azure OpenAI in an Azure AI Foundry project

While the previous sections show how to focus on just the Azure OpenAI Service, you can also incorporate other AI services and models from various providers in Azure AI Foundry portal. You can access the Azure OpenAI Service in two ways:

* When you focus on just the Azure OpenAI Service, as described in the previous sections, you don't use a project.
* Azure AI Foundry portal uses a project to organize your work and save state while building customized AI apps. When you work in a project, you can connect to the service. For more information, see [How to use Azure OpenAI Service in Azure AI Foundry portal](how-to/connect-azure-openai.md#project).

When you create a project, you can try other models and tools along with Azure OpenAI. For example, the **Model catalog** in a project contains many more models than just Azure OpenAI models. Inside a project, you'll have access to features that are common across all AI services and models.

When you are only working with Azure OpenAI, working outside a project allow you to access the features that are specific to Azure OpenAI.  

This table highlights the differences between working with Azure OpenAI outside of a project or in a project in Azure AI Foundry portal:


|  | **Azure OpenAI Service without a project** | **Azure OpenAI Service with a project** |
|--|--|--|
| **Purpose** | Primarily focused on providing access to Azure OpenAI's models and functionalities. Allows users to deploy, fine-tune, and manage Azure OpenAI models. |  A broader platform that focuses on end-to-end tooling to build generative AI applications.  Integrates multiple AI services and models from various providers, including Azure OpenAI. Designed to support a wide range of AI functionalities and use cases. |
| **Features** | Includes a model catalog, fine-tuning capabilities, and deployment options. Access all Azure OpenAI models and manage them within this resource. | Offers models from providers like Meta, Microsoft, Cohere, Mistral, and NVIDIA. Provides a comprehensive suite of tools for building, testing, and deploying AI solutions. Powers AI capabilities like translation, summarization, conversation, document generation, facial recognition, and more. |
| **Usage** | Ideal when you need to work specifically with Azure OpenAI models and use their capabilities for various applications. | Provides enterprise-grade features like access management and private networks.  Suitable when you want to explore and use a diverse set of AI services and models. Includes a unified interface for managing different AI resources and projects. Create an Azure AI Foundry project to use AI services or models from other model providers. |

> [!NOTE]
> When you need features specific to Azure OpenAI, such as batch jobs, Azure OpenAI Evaluation, and vector stores, work outside of a project.

### Navigate to/from projects

Pay attention to the top left corner of the screen to see which context you are in.

* When you are in the Azure AI Foundry portal landing page, with choices of where to go next, you see **Azure AI Foundry**.

    :::image type="content" source="../media/azure-openai-in-ai-studio/ai-studio-no-project.png" alt-text="Screenshot shows top left corner of screen for Azure AI Foundry without a project.":::

* When you are in a project, you see **Azure AI Foundry / project name**. The project name allows you to switch between projects.

    :::image type="content" source="../media/azure-openai-in-ai-studio/ai-studio-project.png" alt-text="Screenshot shows top left corner of screen for Azure AI Foundry with a project.":::

* When you're working with Azure OpenAI outside of a project, you see **Azure AI Foundry | Azure OpenAI / resource name**. The resource name allows you to switch between Azure OpenAI resources.

    :::image type="content" source="../media/azure-openai-in-ai-studio/ai-studio-azure-openai.png" alt-text="Screenshot shows top left corner of screen for Azure AI Foundry when using Azure OpenAI without a project.":::

Use the **Azure AI Foundry** breadcrumb to navigate back to the Azure AI Foundry portal home page.

## Use Azure OpenAI models outside of a project

You can use your existing Azure OpenAI model deployments in Azure AI Foundry portal outside of a project. Start here if you previously deployed models using the old Azure OpenAI Studio or via the Azure OpenAI Service SDKs and APIs.

To use Azure OpenAI Service outside of a project, follow these steps:

1. Go to the [Azure AI Foundry home page](https://ai.azure.com) and make sure you're signed in with the Azure subscription that has your Azure OpenAI Service resource.
1. Find the tile that says **Focused on Azure OpenAI Service?** and select **Let's go**. 

    :::image type="content" source="../../media/azure-openai-in-ai-studio/home-page.png" alt-text="Screenshot of the home page in Azure AI Foundry portal with the option to select Azure OpenAI Service." lightbox="../../media/azure-openai-in-ai-studio/home-page.png":::

    If you don't see this tile, you can also go directly to the [Azure OpenAI Service page](https://ai.azure.com/resource/overview) in Azure AI Foundry portal.

1. You should see your existing Azure OpenAI Service resources. In this example, the Azure OpenAI Service resource `contoso-azure-openai-eastus` is selected.

    :::image type="content" source="../../media/ai-services/azure-openai-studio-select-resource.png" alt-text="Screenshot of the Azure OpenAI Service resources page in Azure AI Foundry portal." lightbox="../../media/ai-services/azure-openai-studio-select-resource.png":::

    If your subscription has multiple Azure OpenAI Service resources, you can use the selector or go to **All resources** to see all your resources. 

If you create more Azure OpenAI Service resources later (such as via the Azure portal or APIs), you can also access them from this page.

## <a name="project"></a> Use Azure OpenAI Service in a project

You might eventually want to use a project for tasks such as managing connections, permissions, and deploying models to production. You can use your existing Azure OpenAI Service resources in an Azure AI Foundry project. 

Let's look at two ways to connect Azure OpenAI Service resources to a project:

- [When you create a project](#connect-azure-openai-service-when-you-create-a-project-for-the-first-time)
- [After you create a project](#connect-azure-openai-service-after-you-create-a-project)

### Connect Azure OpenAI Service when you create a project for the first time

When you create a project for the first time, you also create a hub. When you create a hub, you can select an existing Azure AI services resource (including Azure OpenAI) or create a new AI services resource.

:::image type="content" source="../../media/how-to/projects/projects-create-resource.png" alt-text="Screenshot of the create resource page within the create project dialog." lightbox="../../media/how-to/projects/projects-create-resource.png":::

For more details about creating a project, see the [create an Azure AI Foundry project](../../how-to/create-projects.md) how-to guide or the [create a project and use the chat playground](../../quickstarts/get-started-playground.md) quickstart.

### Connect Azure OpenAI Service after you create a project

If you already have a project and you want to connect your existing Azure OpenAI Service resources, follow these steps:

1. Go to your Azure AI Foundry project.
1. Select **Management center** from the left pane.
1. Select **Connected resources** (under **Project**) from the left pane. 
1. Select **+ New connection**.

    :::image type="content" source="../../media/ai-services/connections-add.png" alt-text="Screenshot of the connected resources page with the button to create a new connection." lightbox="../../media/ai-services/connections-add.png":::

1. On the **Add a connection to external assets** page, select the kind of AI service that you want to connect to the project. For example, you can select Azure OpenAI Service, Azure AI Content Safety, Azure AI Speech, Azure AI Language, and other AI services.

    :::image type="content" source="../../media/ai-services/connections-add-assets.png" alt-text="Screenshot of the page to select the kind of AI service that you want to connect to the project." lightbox="../../media/ai-services/connections-add-assets.png":::

1. On the next page in the wizard, browse or search to find the resource you want to connect. Then select **Add connection**.  

    :::image type="content" source="../../media/ai-services/connections-add-azure-openai.png" alt-text="Screenshot of the page to select the Azure AI Service resource that you want to connect to the project." lightbox="../../media/ai-services/connections-add-azure-openai.png":::

1. After the resource is connected, select **Close** to return to the **Connected resources** page. You should see the new connection listed.

## Deploy a chat model

> [!TIP]
> You can try Azure OpenAI models in the project-level playgrounds, or outside of a project. If you're only working with the Azure OpenAI Service models, we recommend working outside of a project, so you can skip deployment

[!INCLUDE [deploy-model](../../includes/deploy-model.md)]

7. Once the model is deployed, select **Open in playground** to test your model.

You're now in a project, with a deployed model. You can use the chat playground to interact with your model.

For more information about deploying models, see [how to deploy models](../../how-to/deploy-models-openai.md).

## Try Azure OpenAI models in the playgrounds

You can try Azure OpenAI models in the Azure OpenAI Service playgrounds outside of a project.

1. Go to the [Azure OpenAI Service page](https://ai.azure.com/resource/overview) in Azure AI Foundry portal.
1. Select a playground from under **Playgrounds** in the left pane.

    :::image type="content" source="../../media/ai-services/playgrounds/azure-openai-studio-playgrounds.png" alt-text="Screenshot of the playgrounds that you can select to use Azure OpenAI Service." lightbox="../../media/ai-services/playgrounds/azure-openai-studio-playgrounds.png":::

Here are a few guides to help you get started with Azure OpenAI Service playgrounds:

- [Quickstart: Get started using Azure OpenAI Assistants](../../../ai-services/openai/assistants-quickstart.md?context=/azure/ai-studio/context/context)
- [Quickstart: Use GPT-4o in the real-time audio playground](../../../ai-services/openai/realtime-audio-quickstart.md?context=/azure/ai-studio/context/context)
- [Quickstart: Analyze images and video in the chat playground](/azure/ai-services/openai/gpt-v-quickstart)

Each playground has different model requirements and capabilities. The supported regions vary depending on the model. For more information about model availability per region, see the [Azure OpenAI Service models documentation](../../../ai-services/openai/concepts/models.md).

## Use the chat playground

1. To use the chat playground, select **Chat** from the **Playgrounds** section of the left pane.
1. In the **System message** text box, provide a prompt to guide the assistant. You can specify any instructions for the chat, from something simple like "You're an AI assistant that helps people find information." to something highly detailed and specific to your requirements.
1. Optionally, add a safety system message by selecting the **Add section** button, then **Safety system messages**. Choose from the prebuilt messages, and then edit them to your needs.
1. Select **Apply changes** to save your changes, and when prompted to see if you want to update the system message, select **Continue**. 
1. In the chat session pane, enter the following question: "How much do the TrailWalker hiking shoes cost?"
1. Select the right arrow icon to send.

    :::image type="content" source="../../media/tutorials/chat/chat-without-data.png" alt-text="Screenshot of the first chat question without grounding data." lightbox="../../media/tutorials/chat/chat-without-data.png":::

1. The assistant either replies that it doesn't know the answer or provides a generic response. For example, the assistant might say, "The price of TrailWalker hiking shoes can vary depending on the brand, model, and where you purchase them." The model doesn't have access to current product information about the TrailWalker hiking shoes. 

Next, you can add your data to the model to help it answer questions about your products. Try the [Deploy an enterprise chat web app](../../tutorials/deploy-chat-web-app.md) tutorial to learn more.

## Fine-tune Azure OpenAI models

In Azure AI Foundry portal, you can fine-tune several Azure OpenAI models. The purpose is typically to improve model performance on specific tasks or to introduce information that wasn't well represented when you originally trained the base model.

1. Go to the [Azure OpenAI Service page](https://ai.azure.com/resource/overview) in Azure AI Foundry portal to fine-tune Azure OpenAI models.
1. Select **Fine-tuning** from the left pane.

    :::image type="content" source="../../media/ai-services/fine-tune-azure-openai.png" alt-text="Screenshot of the page to select fine-tuning of Azure OpenAI Service models." lightbox="../../media/ai-services/fine-tune-azure-openai.png":::

1. Select **+ Fine-tune model** in the **Generative AI fine-tuning** tabbed page.
1. Follow the [detailed how to guide](../../../ai-services/openai/how-to/fine-tuning.md?context=/azure/ai-studio/context/context) to fine-tune the model.

For more information about fine-tuning Azure AI models, see:
- [Overview of fine-tuning in Azure AI Foundry portal](../../concepts/fine-tuning-overview.md)
- [How to fine-tune Azure OpenAI models](../../../ai-services/openai/how-to/fine-tuning.md?context=/azure/ai-studio/context/context)
- [Azure OpenAI models that are available for fine-tuning](../../../ai-services/openai/concepts/models.md?context=/azure/ai-studio/context/context)


## Deploy models to production

You can deploy Azure OpenAI base models and fine-tuned models to production via the Azure AI Foundry portal.

1. Go to the [Azure OpenAI Service page](https://ai.azure.com/resource/overview) in Azure AI Foundry portal.
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

- [Azure OpenAI in Azure AI Foundry portal](../../azure-openai-in-ai-foundry.md)
- [Use Azure AI services resources](./connect-ai-services.md)
