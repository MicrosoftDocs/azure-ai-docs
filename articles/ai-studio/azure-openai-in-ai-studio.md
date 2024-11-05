---
title: Azure OpenAI in Azure AI Studio
titleSuffix: Azure AI Studio
description: Learn about using Azure OpenAI models in Azure AI Studio, including when to use a project and when to use without a project.
manager: scottpolly
keywords: Azure AI services, cognitive, Azure OpenAI
ms.service: azure-ai-studio
ms.topic: overview
ms.date: 11/04/2024
ms.reviewer: shwinne
ms.author: sgilley
author: sdgilley
ms.custom: ignite-2023, build-2024
# customer intent: As a developer, I want to understand the different ways I can work with Azure OpenAI models so that I can build and deploy AI models.
---

# What is Azure OpenAI in Azure AI Studio?

Azure OpenAI Service provides REST API access to OpenAI's powerful language models. Azure OpenAI Studio was previously where you went to access and work with the Azure OpenAI Service. This studio is now integrated into Azure AI Studio. 

## Access Azure OpenAI Service in Azure AI Studio

From the [Azure AI Studio](https://ai.azure.com) landing page, use the **Let's go** button in the **Focused on Azure OpenAI Service?** section.

:::image type="content" source="media/azure-openai-in-ai-studio/home-page.png" alt-text="Screenshot shows Azure AI Studio home page.":::

You can also use [https://ai.azure.com/resource](https://ai.azure.com/resource) to directly access Azure OpenAI models outside of a project.

## Focus on Azure OpenAI Service

If you've been using Azure OpenAI Studio, all your work, such as your deployments, content filters, batch jobs or fine-tuned models, is still available. All the features and functionality are still here, though the look and feel of some features are updated.

:::image type="content" source="media/azure-openai-in-ai-studio/studio-home.png" alt-text="Screenshot shows the new Azure OpenAI in Azure AI Studio." lightbox="media/azure-openai-in-ai-studio/studio-home.png":::

Use the left navigation area to perform your tasks with Azure OpenAI models:

* **Select models**: The **Model catalog** houses all the available Azure OpenAI models.

    :::image type="content" source="media/azure-openai-in-ai-studio/model-catalog.png" alt-text="Screenshot shows the model catalog in Azure OpenAI Service." lightbox="media/azure-openai-in-ai-studio/model-catalog.png":::

* **Try models**: Use the various **Resource playgrounds** to decide which model is best for your needs.
* **Deploy models**: In the **Model catalog** or **Deployments** list in the left navigation, you see all supported models. You can deploy models from either section.
* **Fine-tune**: Use **Fine-tuning** to find your fine-tuned/custom models or create new fine-tune jobs.
* **Batch jobs**: Create and manage jobs for your global batch deployments.
* Use the resource name in the top left to switch to another recently used resource.  Or find all your Azure OpenAI Service resources in the top right-hand corner under **All resources**.

    :::image type="content" source="media/azure-openai-in-ai-studio/all-resources.png" alt-text="Screenshot shows the top right access to all resources in Azure AI Service section of Azure AI Studio." lightbox="media/azure-openai-in-ai-studio/all-resources.png":::

## Azure OpenAI in an Azure AI Studio project

While the previous sections show how to focus on just the Azure OpenAI Service, you can also incorporate other AI services and models from various providers in Azure AI Studio. You can access the Azure OpenAI Service in two ways:

* When you focus on just the Azure OpenAI Service, as described in the previous sections, you don't use a project.
* Azure AI Studio uses a project to organize your work and save state while building customized AI apps. When you work in a project, you can [connect](./how-to/connections-add.md) to the service.

When you create a project, you can try other models and tools along with Azure OpenAI. For example, the **Model catalog** in a project contains many more models than just Azure OpenAI models. Inside a project, you'll have access to features that are common across all AI services and models.

When you are only working with Azure OpenAI, working outside a project allow you to access the features that are specific to Azure OpenAI.  

This table highlights the differences between working with Azure OpenAI outside of a project or in a project in Azure AI Studio:


|  | **Azure OpenAI Service without a project** | **Azure AI Studio with a project** |
|--|--|--|
| **Purpose** | Primarily focused on providing access to Azure OpenAI's models and functionalities. Allows users to deploy, fine-tune, and manage Azure OpenAI models. |  A broader platform that focuses on end-to-end tooling to build generative AI applications.  Integrates multiple AI services and models from various providers, including Azure OpenAI. Designed to support a wide range of AI functionalities and use cases. |
| **Features** | Includes a model catalog, fine-tuning capabilities, and deployment options. Access all Azure OpenAI models and manage them within this resource. | Offers models from providers like Meta, Microsoft, Cohere, Mistral, and NVIDIA. Provides a comprehensive suite of tools for building, testing, and deploying AI solutions. Powers AI capabilities like translation, summarization, conversation, document generation, facial recognition, and more. |
| **Usage** | Ideal when you need to work specifically with Azure OpenAI models and use their capabilities for various applications. | Provides enterprise-grade features like access management and private networks.  Suitable when you want to explore and use a diverse set of AI services and models. Includes a unified interface for managing different AI resources and projects. Create an Azure AI Studio project to use AI services or models from other model providers. |

> [!NOTE]
> When you need features specific to Azure OpenAI, such as batch jobs and vector stores, work outside of a project.

### Navigate to/from projects

Pay attention to the top left corner of the screen to see which context you are in.

* When you are in the Azure AI Studio landing page, with choices of where to go next, you see **Azure AI Studio**.

    :::image type="content" source="media/azure-openai-in-ai-studio/ai-studio-no-project.png" alt-text="Screenshot shows top left corner of screen for AI Studio without a project.":::

* When you are in a project, you see **Azure AI Studio / project name**. The project name allows you to switch between projects.

    :::image type="content" source="media/azure-openai-in-ai-studio/ai-studio-project.png" alt-text="Screenshot shows top left corner of screen for AI Studio with a project.":::

* When you're working with Azure OpenAI outside of a project, you see **Azure AI Studio | Azure OpenAI / resource name**. The resource name allows you to switch between Azure OpenAI resources.

    :::image type="content" source="media/azure-openai-in-ai-studio/ai-studio-azure-openai.png" alt-text="Screenshot shows top left corner of screen for AI Studio when using Azure OpenAI without a project.":::

Use the **Azure AI Studio** breadcrumb to navigate back to the Azure AI Studio home page. You can also navigate back to the Azure AI Studio home page when you see **View all Azure AI Studio resources & projects** in the top right corner of the screen.

## Related content

* [Azure OpenAI Documentation](/azure/ai-services/openai/)
