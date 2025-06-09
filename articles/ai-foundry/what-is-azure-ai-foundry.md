---
title: What is Azure AI Foundry?
titleSuffix: Azure AI Foundry
description: Azure AI Foundry is a trusted platform that empowers developers to drive innovation and shape the future with AI in a safe, secure, and responsible way.
author: sdgilley
ms.author: sgilley
manager: scottpolly
ms.reviewer: sgilley
ms.date: 05/12/2025
ms.service: azure-ai-foundry
ms.topic: overview
ms.custom:
  - ignite-2023
  - build-2024
  - ignite-2024
  - build-aifnd
  - build-2025
keywords:
  - Azure AI services
  - cognitive
# customer intent: As a developer, I want to understand what Azure AI Foundry is so that I can use it to build AI applications.
---

# What is Azure AI Foundry?

[Azure AI Foundry](https://ai.azure.com/?cid=learnDocs) provides a unified platform for enterprise AI operations, model builders, and application development. This foundation combines production-grade infrastructure with friendly interfaces, ensuring organizations can build and operate AI applications with confidence. 

[Azure AI Foundry](https://ai.azure.com/?cid=learnDocs) is designed for developers to:

- Build generative AI applications on an enterprise-grade platform.
- Explore, build, test, and deploy using cutting-edge AI tools and ML models, grounded in responsible AI practices.
- Collaborate with a team for the full life-cycle of application development.

With Azure AI Foundry, you can explore a wide variety of models, services and capabilities, and get to building AI applications that best serve your goals. Azure AI Foundry facilitates scalability for transforming proof of concepts into full-fledged production applications with ease. Continuous monitoring and refinement support long-term success.  

## Work in an Azure AI Foundry project

An Azure AI Foundry project is where you do most of your development work. You can work with your project in the Azure AI Foundry portal, or use the SDK in your preferred development environment.

## <a name="project-types"></a> Types of projects

Azure AI Foundry supports two types of projects: a **[!INCLUDE [hub](includes/hub-project-name.md)]** and a **[!INCLUDE [fdp](includes/fdp-project-name.md)]**. In most cases, you'll want to use a [!INCLUDE [fdp-project-name](includes/fdp-project-name.md)].

* [!INCLUDE [fdp-description](includes/fdp-description.md)]

* [!INCLUDE [hub-description](includes/hub-description.md)]


### Which type of project do I need?

* In general, you should use a [!INCLUDE [fdp-project-name](includes/fdp-project-name.md)] if you are looking to build agents or work with models. 
* Use a [!INCLUDE [hub-project-name](includes/hub-project-name.md)] when you need features that are not available in a [!INCLUDE [fdp-project-name](includes/fdp-project-name.md)]. See the following table for more on feature availability.


This table summarizes features available in the two project types:  


| Capability | [!INCLUDE [fdp](includes/fdp-project-name.md)] | [!INCLUDE[hub](includes/hub-project-name.md)] |
| --- | --- | --- |
| Agents | ✅ (GA) | ✅ (Preview only) |
| Azure AI Foundry Models including Azure OpenAI models | ✅ (Native support) | Available via connections |
| AI Foundry API to work with agents and across models| ✅ (Native support) | Available via connections |
| Project files (directly upload files and start experimenting) | ✅ | |
| Project-level isolation of files and outputs | ✅ | ✅|
| Evaluations | ✅ | ✅ |
| Playground | ✅ | ✅ |
| Prompt flow |  | ✅ |
| Managed compute  |  | ✅ |
| Required Azure dependencies | - | Azure Storage account, Azure Key Vault |

### <a name="how-do-i-know"></a> How do I know which type of project I have?

Here are some of the ways to identify your project type:

* From the **breadcrumb navigation** section

    * A [!INCLUDE [fdp-project-name](includes/fdp-project-name.md)] displays **(AI Foundry)** on the second line
    * A [!INCLUDE [hub-project-name](includes/hub-project-name.md)] displays **(Hub)** on the second line

    :::image type="content" source="media/how-to/projects/breadcrumb.png" alt-text="Screenshot shows both a Foundry and hub based project in the breadcrumb navigation.":::

* From the **All resources** page

    * A [!INCLUDE [fdp-project-name](includes/fdp-project-name.md)] displays **(AI Foundry)** as the parent resource
    * A [!INCLUDE [hub-project-name](includes/hub-project-name.md)] displays **(Hub)** as the parent resource

    :::image type="content" source="media/how-to/projects/all-resources.png" alt-text="Screenshot shows both a Foundry and hub based project in the All Resources page.":::

<!-- * From the **Overview** section of the project

    * If it's a [!INCLUDE [fdp-project-name](includes/fdp-project-name.md)], you see an **Azure AI Foundry endpoint**

        :::image type="content" source="media/how-to/projects/fdp-project-overview.png" alt-text="Screenshot shows a Foundry project overview page." lightbox="media/how-to/projects/fdp-project-overview.png":::

    * If it's a [!INCLUDE [hub-project-name](includes/hub-project-name.md)], you see a **Project connection string**

        :::image type="content" source="media/how-to/projects/hub-project-overview.png" alt-text="Screenshot shows a hub based project overview page." lightbox="media/how-to/projects/hub-project-overview.png"::: -->

## Navigate in the Azure AI Foundry portal

In the Azure AI Foundry portal, you can navigate among all your resources using the breadcrumbs at the top of the page. The breadcrumbs show recent resources, along with a link to all resources. 

The left pane is organized around your goals. Generally, as you develop with Azure AI, you'll likely go through a few distinct stages of project development:

* **Define and explore**. In this stage you define your project goals, and then explore and test models and services against your use case to find the ones that enable you to achieve your goals.
* **Build and customize**. In this stage, you're actively building solutions and applications with the models, tools, and capabilities you selected. You can also customize models to perform better for your use case by fine-tuning, grounding in your data, and more. Building and customizing might be something you choose to do in the Azure AI Foundry portal, or through code and the Azure AI Foundry SDKs. Either way, a project provides you with everything you need.
  * Once you're actively developing in your project, the **Overview** page shows the things you want easy access to, like your endpoints and keys.
* **Observe and improve**. In this stage, you're looking for where you can improve your application's performance. You might choose to use tools like tracing to debug your application or compare evaluations to hone in on how you want your application to behave. You can also integrate with safety & security systems so you can be confident when you take your application to production.

If you're an admin, or leading a development team, and need to manage the team's resources, project access, quota, and more, you can do that in the Management Center.
 
## <a name="left-pane"></a> Customize the left pane

The left pane of the Azure AI Foundry portal is your main navigation tool. Customize this area to show the parts of the portal you want to use.

Pin or unpin items into the left pane. When you unpin an item, it is hidden from the left pane but can be found again in the **...More** menu.

* Select **... More** at the bottom of the pane to see items to pin and unpin.
* Customize each project separately. The left pane is not shared across projects.
* The left pane is not shared across users. Each user customizes their own left pane for each project. 

## Management center

The management center is a part of the Azure AI Foundry portal that streamlines governance and management activities. In the management center, you can view and manage:

- Projects and resources
- Quotas and usage metrics
- Govern access and permissions

For more information, see [Management center overview](./concepts/management-center.md).

## Pricing and billing

Azure AI Foundry is monetized through individual products customer access and consume in the platform, including API and models, complete AI toolchain, and responsible AI and enterprise grade production at scale products. Each product has its own billing model and price. 

The platform is free to use and explore. Pricing occurs at deployment level. 

Using Azure AI Foundry also incurs cost associated with the underlying services. To learn more, read [Plan and manage costs for Azure AI services](./how-to/costs-plan-manage.md).

## Region availability

Azure AI Foundry is available in most regions where Azure AI services are available. For more information, see [region support for Azure AI Foundry](reference/region-support.md).

## How to get access

You can [explore Azure AI Foundry portal (including the model catalog)](./how-to/model-catalog-overview.md) without signing in. 

But for full functionality, you need an [Azure account](https://azure.microsoft.com/pricing/purchase-options/azure-account). 

## Related content

- [Quickstart: Get started with Azure AI Foundry](quickstarts/get-started-code.md)
- [Create a project](./how-to/create-projects.md)
- [Get started with an AI template](how-to/develop/ai-template-get-started.md)
