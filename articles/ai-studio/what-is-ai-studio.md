---
title: What is Azure AI Studio?
titleSuffix: Azure AI Studio
description: Azure AI Studio is a trusted platform that empowers developers to drive innovation and shape the future with AI in a safe, secure, and responsible way.
manager: scottpolly
keywords: Azure AI services, cognitive
ms.service: azure-ai-studio
ms.topic: overview
ms.date: 10/31/2024
ms.reviewer: sgilley
ms.author: sgilley
author: sdgilley
ms.custom: ignite-2023, build-2024
#customer intent: As a developer, I want to understand what Azure AI Studio is so that I can use it to build AI applications.
---

# What is Azure AI Studio?

[Azure AI Studio](https://ai.azure.com) is a trusted platform that empowers developers to drive innovation and shape the future with AI in a safe, secure, and responsible way.

[AI Studio](https://ai.azure.com) is designed for developers to:

- Build generative AI applications on an enterprise-grade platform.
- Explore, build, test, and deploy using cutting-edge AI tools and ML models, grounded in responsible AI practices.
- Collaborate with a team for the full life-cycle of application development.

With AI Studio, you can explore a wide variety of models, services and capabilities, and get to building AI applications that best serve your goals. The Azure AI Studio platform facilitates scalability for transforming proof of concepts into full-fledged production applications with ease. Continuous monitoring and refinement support long-term success.  

:::image type="content" source="./media/explore/ai-studio-home.png" alt-text="Screenshot of the Azure AI Studio home page with links to get started." lightbox="./media/explore/ai-studio-home.png":::

When you come to AI Studio, you find that all paths lead to a project. Projects are easy-to-manage containers for your work—and the key to collaboration, organization, and connecting data and other services. Before you create your first project, you can explore models from many providers, and try out AI services and capabilities. When you're ready to move forward with a model or service, AI Studio guides you to create a project. Once you are in a project, all of the Azure AI capabilities come to life.

> [!NOTE]
> If you want to focus only on Azure OpenAI models and capabilities, we have a place where you can work with your Azure OpenAI resource instead of a project. For more information, see [What is Azure OpenAI in Azure AI Studio?](azure-openai-in-ai-studio.md). However, for most situations, we recommend an AI Studio project to build with a wide range of AI models, functionalities and tools as you build, test, and deploy AI solutions.

## Work in an Azure AI project

An AI Studio project is where you do most of your development work. You can work with your project in the Azure AI Studio, or using the SDK in your preferred development environment. Once you have a project, you can connect to it from your code. You can explore models and capabilities before creating a project, but once you're ready to build, customize, test, and operationalize, a project is where you'll want to be.

When you choose to deploy a model or work with AI Services, you're prompted to select a project if you aren't already in one.

Once you're in a project, you'll see an overview of what you can do with it on the **Overview** page.

:::image type="content" source="media/explore/project-view-current.png" alt-text="Screenshot shows the project overview in Azure AI Studio." lightbox="media/explore/project-view-current.png":::

The studio is organized around your goals. Generally, as you develop with Azure AI, you'll likely go through a few distinct stages of project development:

* **Define and explore**. In this stage you define your project goals, and then explore and test models and services against your use case to find the ones that enable you to achieve your goals.
* **Build and customize**. In this stage, you're actively building solutions and applications with the models, tools, and capabilities you selected. You can also customize models to perform better for your use case by fine-tuning, grounding in your data, and more. Building and customizing might be something you choose to do in the Azure AI Studio, or through code and the Azure AI SDKs. Either way, a project provides you with everything you need.
  * Once you're actively developing in your project, the **Overview** page shows the things you want easy access to, like your endpoints and keys.
* **Assess and improve**. In this stage, you're looking for where you can improve your application's performance. You might choose to use tools like tracing to debug your application or compare evaluations to hone in on how you want your application to behave. You can also integrate with safety & security systems so you can be confident when you take your application to production.

If you're an admin, or leading a development team, and need to manage the team's resources, project access, quota, and more, you can do that in the Management Center.

## Management center

The management center is a part of the Azure AI Studio that streamlines governance and management activities. In the management center, you can view and manage:

- Projects and resources
- Quotas and usage metrics
- Govern access and permissions

For more information, see [Management center overview]().

## Pricing and billing

Azure AI Studio is monetized through individual products customer access and consume in the platform, including API and models, complete AI toolchain, and responsible AI and enterprise grade production at scale products. Each product has its own billing model and price. 

The platform is free to use and explore. Pricing occurs at deployment level. For more information abut AI Studio pricing, see [AI Studio pricing](https://aka.ms/Azure-AI-Studio-New-Pricing-Page).

Using AI Studio also incurs cost associated with the underlying services. To learn more, read [Plan and manage costs for Azure AI services](./how-to/costs-plan-manage.md).

## Region availability

AI Studio is available in most regions where Azure AI services are available. For more information, see [region support for AI Studio](reference/region-support.md).

## How to get access

You can [explore AI Studio (including the model catalog)](./how-to/model-catalog.md) without signing in. 

But for full functionality there are some requirements:

- You need an [Azure account](https://azure.microsoft.com/free/). 

## Related content

- [Quickstart: Use the chat playground in Azure AI Studio](quickstarts/get-started-playground.md)
- [Build a custom chat app in Python using the Azure AI SDK](quickstarts/get-started-code.md)
- [Create a project](./how-to/create-projects.md)
