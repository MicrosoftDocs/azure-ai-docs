---
title: Azure OpenAI in Azure AI Studio
titleSuffix: Azure AI Studio
description: Learn about using Azure OpenAI models in Azure AI Studio, including when to use a project and when to use without a project.
manager: scottpolly
keywords: Azure AI services, cognitive, Azure OpenAI
ms.service: azure-ai-studio
ms.topic: overview
ms.date: 10/23/2024
ms.reviewer: shwinne
ms.author: sgilley
author: sdgilley
ms.custom: ignite-2023, build-2024
# customer intent: As a developer, I want to understand the different ways I can work with Azure OpenAI models so that I can build and deploy AI models.
---

# What is Azure OpenAI in Azure AI Studio?

Access the Azure OpenAI service inside Azure AI Studio in two different contexts: within a project and outside of a project.

While Azure **AI** Studio uses a project-based approach, Azure **OpenAI** Studio did not use projects. Now that Azure OpenAI is fully integrated into Azure AI Studio, you have the choice of working:
* Without a project, working only with Azure OpenAI models.
* In a project, along with other models and resources.

## Understand project and non-project approaches

You can use Azure OpenAI models with or without an AI Studio project. When you create a project, you can try other models and tools along with Azure OpenAI. But you can do more with Azure OpenAI models outside of a project. This table highlights the differences between working with Azure OpenAI outside of a project or in a project in Azure AI Studio:


|  | **Azure OpenAI without a project** | **AI Studio with a project** |
|--|--|--|
| **Purpose** | Primarily focused on providing access to Azure OpenAI's models and functionalities. Allows users to deploy, fine-tune, and manage Azure OpenAI models. |  A broader platform that integrates multiple AI services and models from various providers, including Azure OpenAI. Designed to support a wide range of AI functionalities and use cases. |
| **Features** | Includes a model catalog, fine-tuning capabilities, and deployment options. Access all Azure OpenAI models and manage them within this resource. | Offers a comprehensive suite of tools for building, testing, and deploying AI solutions. Powers AI capabilities like translation, summarization, conversation, document generation, facial recognition, and more. Also offers models from providers like Meta, Microsoft, Cohere, Mistral, and NVIDIA. |
| **Usage** | Ideal when you need to work specifically with Azure OpenAI models and use their capabilities for various applications. | Suitable when you want to explore and use a diverse set of AI services and models. Provides a unified interface for managing different AI resources and projects. Create an Azure AI Studio project to use AI services or models from other model providers. |

> [!NOTE]
> Projects currently do not support all Azure OpenAI features. These features include batch jobs and vector stores. To use these features, work outside of a project.

## Work outside a project

You can access Azure OpenAI models directly from Azure AI Studio without creating a project. Use the **Let's go** button in the **Azure OpenAI** section of the Azure AI Studio home page.

:::image type="content" source="media/aoai-in-ai-studio/home-page.png" alt-text="Screenshot shows Azure AI Studio home page.":::

You can also use [https://ai.azure.com/resource](https://ai.azure.com/resource) to directly access Azure OpenAI models outside of a project.

When you're working with Azure OpenAI outside of a project, you're in a section of Azure AI Studio that is dedicated to Azure OpenAI models, and looks similar to the previous Azure OpenAI Studio.
If you've been using Azure OpenAI Studio, all your work is still here, such as your deployments, content filters, batch jobs or fine-tuned models, which remain saved in Azure OpenAI. No features or functionality are removed, though the look and feel of some features are updated:

* Access your existing resources and deployments: All Azure OpenAI Studio resources can be found in the top right-hand corner under **All resources**.
* Model catalog: The **Model catalog** houses all the available Azure OpenAI models. You can also fine-tune or deploy a model from the **Fine-tuning** or **Deployments** section respectively.
* Deploy models: From the **Model catalog** or **Deployments** list in the left navigation, you  see all supported models. You can deploy models from either section.
* Fine-tuning: Use **Fine-tuning** to find your fine-tuned/custom models or create new fine-tune jobs.

### Navigate to/from projects

Pay attention to the top left corner of the screen to see which context you are in.

* When you are in the Azure AI Studio home page, with choices of where to go next, you see **Azure AI Studio**.

    :::image type="content" source="media/aoai-in-ai-studio/ai-studio-no-project.png" alt-text="Screenshot shows top left corner of screen for AI Studio without a project.":::

* When you are in a project, you see **Azure AI Studio / project name**.

    :::image type="content" source="media/aoai-in-ai-studio/ai-studio-project.png" alt-text="Screenshot shows top left corner of screen for AI Studio with a project.":::

* When you are working with Azure OpenAI outside of a project, you see **Azure AI Studio | Azure OpenAI**.

    :::image type="content" source="media/aoai-in-ai-studio/ai-studio-aoai.png" alt-text="Screenshot shows top left corner of screen for AI Studio when using Azure OpenAI without a project.":::



Use the **Azure AI Studio** breadcrumb to navigate back to the Azure AI Studio home page. You can also navigate back to the Azure AI Studio home page when you see **View all Azure AI Studio resources & projects** in the top right corner of the screen.

## Related content

* [Azure OpenAI Documentation](/azure/ai-services/openai/)
