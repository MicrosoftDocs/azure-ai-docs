---
title: Azure OpenAI in Azure AI Studio
titleSuffix: Azure AI Studio
description: Learn about using Azure OpenAI resources in Azure AI Studio.
manager: scottpolly
keywords: Azure AI services, cognitive, Azure OpenAI
ms.service: azure-ai-studio
ms.topic: overview
ms.date: 10/23/2024
ms.reviewer: shwinne
ms.author: sgilley
author: sdgilley
ms.custom: ignite-2023, build-2024
---

# Azure OpenAI in Azure AI Studio

Azure OpenAI Studio is now integrated into Azure AI Studio.

While Azure **AI** Studio uses a project-based approach, Azure **OpenAI** Studio does not use projects. Now that Azure OpenAI Studio is integrated into Azure AI Studio, you have the choice of working with the Azure OpenAI resource itself or within a project.

## Comparing project and outside-of-project approaches

This table highlights the differences between using a project and working outside of a project in Azure AI Studio:


|  | **Azure OpenAI resource (outside a project)** | **AI Studio project** |
|--|--|--|
| **Purpose** | Primarily focused on providing access to Azure OpenAI's models and functionalities. Allows users to deploy, fine-tune, and manage Azure OpenAI models. |  A broader platform that integrates multiple AI services and models from various providers, including Azure OpenAI. Designed to support a wide range of AI functionalities and use cases. |
| **Features** | Includes a model catalog, fine-tuning capabilities, and deployment options. Access all Azure OpenAI models and manage them within this resource. | Offers a comprehensive suite of tools for building, testing, and deploying AI solutions. Powers AI capabilities like translation, summarization, conversation, document generation, facial recognition, and more. Also offers models from providers like Meta, Microsoft, Cohere, Mistral, and NVIDIA. |
| **Usage** | Ideal when you need to work specifically with Azure OpenAI models and use their capabilities for various applications. | Suitable when you want to explore and use a diverse set of AI services and models. Provides a unified interface for managing different AI resources and projects. |

> [!NOTE]
> Projects currently do not support all Azure OpenAI features. These features include Batch jobs and vector stores. Create Azure AI Studio projects if you would like to use AI services or models from other model providers. 

## Work outside a project

You can access Azure OpenAI Resource directly from Azure AI Studio without creating a project. Use the **Let's go** button in the **Azure OpenAI** section of the Azure AI Studio home page.

:::image type="content" source="media/aoai-in-ai-studio/home-page.png" alt-text="Screenshot shows Azure AI Studio home page.":::

You can also continue to use the [Azure OpenAI Studio weblink.](https://oai.azure.com) 

When you're outside of a project, you're in a section of Azure AI Studio that is dedicated to Azure OpenAI resources, and looks similar to the previous Azure OpenAI Studio.
If you've been using Azure OpenAI Studio, all your work is still here. No features or functionality are removed, though the look and feel of some features are updated:

* Resource access: All Azure OpenAI Studio resources can be found in the top right-hand corner under **All resources**.
* Model catalog: The **Model catalog** houses all the available Azure OpenAI models. You can also fine-tune or deploy a model from the **Fine-tuning** or **Deployments** section respectively.
* Deploy models: From the **Model catalog** or **Deployments** list in the left navigation, you  see all supported models. You can deploy models from either section.
* Fine-tuning: Use **Fine-tuning** to find your fine-tuned/custom models or create new fine-tune jobs.

### Navigate to/from projects

Pay attention to the top left corner of the screen to see which context you are in.

* When you are in a project, you see **Azure AI Studio / project name**.

    :::image type="content" source="media/aoai-in-ai-studio/ai-studio-project.png" alt-text="Screenshot shows top left corner of screen for AI Studio with a project.":::

* When you are working with an Azure OpenAI resource outside of a project, you see **Azure AI Studio / resource name / Azure OpenAI**.

* When you are in Azure AI Studio home page, without a project, you see **Azure AI Studio**.

    :::image type="content" source="media/aoai-in-ai-studio/ai-studio-no-project.png" alt-text="Screenshot shows top left corner of screen for AI Studio without a project.":::

Use the **Azure AI Studio** breadcrumb to navigate back to the Azure AI Studio home page. You can also navigate back to the Azure AI Studio home page when you see **View all Azure AI Studio resources & projects** in the top right corner of the screen.

## Next step

* [Azure OpenAI Documentation](/azure/ai-services/openai/)
