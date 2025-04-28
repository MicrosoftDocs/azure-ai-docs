---
title: Manage, collaborate, and organize with hubs
titleSuffix: Azure AI Foundry
description: This article introduces concepts about Azure AI Foundry hubs for your Azure AI Foundry projects.
manager: scottpolly
ms.service: azure-ai-foundry
ms.custom:
  - ignite-2023
  - build-2024
  - ai-learning-hub
  - ignite-2024
ms.topic: conceptual
ms.date: 02/19/2025
ms.reviewer: deeikele
ms.author: larryfr
author: Blackmist
---

# Manage, collaborate, and organize with hubs

Hubs are the primary top-level Azure resource for Azure AI Foundry and provide a central way for a team to govern security, connectivity, and computing resources across playgrounds and projects. Once a hub is created, developers can create projects from it and access shared company resources without needing an IT administrator's repeated help.

Project workspaces that are created using a hub inherit the same security settings and shared resource access. Teams can create project workspaces as needed to organize their work, isolate data, and/or restrict access. 

In this article, you learn more about hub capabilities, and how to set up a hub for your organization. You can see the resources created in the [Azure portal](https://portal.azure.com/) and in [Azure AI Foundry](https://ai.azure.com).

## Rapid AI use case exploration without IT bottlenecks

Successful AI applications and models typically start as prototypes, where developers test the feasibility of an idea, or assess the quality of data or a model for a particular task. The prototype is a stepping stone towards project funding or a full-scale implementation.

When a single platform team is responsible for the setup of cloud resources, the transition from proving the feasibility of an idea to a funded project might be a bottleneck in productivity. Such a team might be the only one authorized to configure security, connectivity or other resources that might incur costs. This situation can cause a huge backlog, resulting in development teams getting blocked on innovating with a new idea. In Azure AI Foundry portal, hubs help mitigate this bottleneck. IT can set up a preconfigured, reusable environment (a hub), for a team one time. Then the team can use that hub to create their own projects for prototyping, building, and operating AI applications.

## Set up and secure a hub for your team

Get started by [creating your first hub in Azure AI Foundry portal](../how-to/create-azure-ai-resource.md), or use [Azure portal](../how-to/create-secure-ai-hub.md) or [templates](../how-to/create-azure-ai-hub-template.md) for advanced configuration options. You can customize networking, identity, encryption, monitoring, or tags, to meet compliance with your organization’s requirements.

Often, projects in a business domain require access to the same company resources such as vector indices, model endpoints, or repos. As a team lead, you can preconfigure connectivity with these resources within a hub, so developers can access them from any new project workspace without delay on IT.

[Connections](connections.md) let you access objects in Azure AI Foundry portal that are managed outside of your hub. For example, uploaded data on an Azure storage account, or model deployments on an existing Azure OpenAI resource. A connection can be shared with every project or made accessible to one specific project. Connections can be configured with key-based access or Microsoft Entra ID to authorize access to users on the connected resource. Plus, as an administrator, you can track, audit, and manage connections across projects using your hub.

## Shared Azure resources and configurations

Various management concepts are available on hubs to support team leads and admins to centrally manage a team's environment. 

* **Security configuration** including public network access, [virtual networking](#virtual-networking), customer-managed key encryption, and privileged access to whom can create projects for customization. Security settings configured on the hub automatically pass down to each project. A managed virtual network is shared between all projects that share the same hub.
* **Connections** are named and authenticated references to Azure and non-Azure resources like data storage providers. Use a connection as a means for making an external resource available to a group of developers without having to expose its stored credential to an individual.
* **Compute and quota allocation** is managed as shared capacity for all projects in Azure AI Foundry portal that share the same hub. This quota includes compute instance as managed cloud-based workstation for an individual. The same user can use a compute instance across projects.
* **AI services access keys** to endpoints for prebuilt AI models are managed on the hub scope. Use these endpoints to access foundation models from Azure OpenAI, Speech, Vision, and Content Safety with one [API key](#azure-ai-services-api-access-keys)
* **Policy** enforced in Azure on the hub scope applies to all projects managed under it.
* **Dependent Azure resources** are set up once per hub and associated projects and used to store artifacts you generate while working in Azure AI Foundry portal such as logs or when uploading data. For more information, see [Azure AI dependencies](#azure-ai-dependencies).

## Organize work in projects for customization

A hub provides the hosting environment for [projects](../how-to/create-projects.md) in Azure AI Foundry portal. A project is an organizational container that has tools for AI customization and orchestration. It lets you organize your work, save state across different tools like prompt flow, and collaborate with others. For example, you can share uploaded files and connections to data sources.

Multiple projects can use a hub, and multiple users can use a project. A project also helps you keep track of billing, and manage access and provides data isolation. Every project uses dedicated storage containers to let you upload files and share it with only other project members when using the 'data' experiences.

Projects let you create and group reusable components that can be used across tools in Azure AI Foundry portal:

| Asset | Description |
| --- | --- |
| Data | Dataset that can be used to create indexes, fine-tune models, and evaluate models. |
| Flows | An executable instruction set that can implement the AI logic.​​ |
| Evaluations | Evaluations of a model or flow. You can run manual or metrics-based evaluations. |
| Indexes | Vector search indexes generated from your data. |

Projects also have specific settings that only hold for that project:

| Asset | Description |
| --- | --- |
| Project connections | Connections to external resources like data storage providers that only you and other project members can use. They complement shared connections on the hub accessible to all projects.|
| Prompt flow runtime | Prompt flow is a feature that can be used to generate, customize, or run a flow. To use prompt flow, you need to create a runtime on top of a compute instance. |

> [!NOTE]
> In Azure AI Foundry portal, you can also manage language and notification settings that apply to all projects that you can access regardless of the hub or project.

## Azure AI services API access keys

The hub allows you to set up connections to existing Azure OpenAI or Azure AI Services resource types, which can be used to host model deployments. You can access these model deployments from connected resources in Azure AI Foundry portal. Keys to connected resources can be listed from the Azure AI Foundry portal or Azure portal. For more information, see [Find Azure AI Foundry resources in the Azure portal](#find-azure-ai-foundry-resources-in-the-azure-portal).

### Virtual networking

Hubs, compute resources, and projects share the same Microsoft-managed Azure virtual network. After you configure the managed networking settings during the hub creation process, all new projects created using that hub will inherit the same virtual network settings. Therefore, any changes to the networking settings are applied to all current and new project in that hub. By default, hubs provide public network access.

To establish a private inbound connection to your hub environment, create an Azure Private Link endpoint on the following scopes:
* The hub
* The dependent `Azure AI services` providing resource
* Any other [Azure AI dependency](#azure-ai-dependencies) such as Azure storage

While projects show up as their own tracking resources in the Azure portal, they don't require their own private link endpoints to be accessed. New projects that are created after hub setup, do automatically get added to the network-isolated environment.

## Connections to Azure and third-party resources

Azure AI offers a set of connectors that allows you to connect to different types of data sources and other Azure tools. You can take advantage of connectors to connect with data such as indexes in Azure AI Search to augment your flows.

Connections can be set up as shared with all projects in the same hub, or created exclusively for one project. To manage connections via Azure AI Foundry, go to your project and then select **Management center**.  Select **Connected resources** in either the **Hub** or **Project** section to manage shared connections for the project or hub, respectively. As an administrator, you can audit both shared and project-scoped connections on a hub level to have a single pane of glass of connectivity across projects.

## Azure AI dependencies

Azure AI Foundry layers on top of existing Azure services including Azure AI and Azure Machine Learning services. While it might not be visible on the display names in Azure portal, Azure AI Foundry, or when using the SDK or CLI, some of these architectural details become apparent when you work with the Azure REST APIs, use Azure cost reporting, or use infrastructure-as-code templates such as Azure Bicep or Azure Resource Manager. From an Azure Resource Provider perspective, Azure AI Foundry resource types map to the following resource provider kinds:

[!INCLUDE [Resource provider kinds](../includes/resource-provider-kinds.md)]

When you create a new hub, a set of dependent Azure resources are required to store data that you upload or get generated when working in Azure AI Foundry portal. If not provided by you, and required, these resources are automatically created.

[!INCLUDE [Dependent Azure resources](../includes/dependent-resources.md)]

## Managing cost

Azure AI costs accrue by [various Azure resources](#azure-ai-dependencies). 

In general, a hub and project don't have a fixed monthly cost, and you're only charged for usage in terms of compute hours and tokens used. Azure Key Vault, Storage, and Application Insights charge transaction and volume-based, dependent on the amount of data stored with your projects. 

If you require to group costs of these different services together, we recommend creating hubs in one or more dedicated resource groups and subscriptions in your Azure environment.

You can use [cost management](/azure/cost-management-billing/costs/quick-acm-cost-analysis) and [Azure resource tags](/azure/azure-resource-manager/management/tag-resources) to help with a detailed resource-level cost breakdown, or run [Azure pricing calculator](https://azure.microsoft.com/pricing/calculator/) on the above listed resources to obtain a pricing estimate. For more information, see [Plan and manage costs for Azure AI services](../how-to/costs-plan-manage.md).

## Find Azure AI Foundry resources in the Azure portal

In the [Azure portal](https://portal.azure.com), search for and then select **Azure AI Foundry** entry. From the AI Foundry section of the portal, you can find your AI Foundry resources.

- The **All resources** section lists all resources.
- The **AI Foundry** section lists [!INCLUDE [fdp](../includes/fdp-project-name.md)] resources.
- The **AI Hubs** section lists [!INCLUDE [hub](../includes/hub-project-name.md)] resources.
- The **Azure OpenAI** section lists Azure OpenAI resources.
- The **AI Search** section lists Azure AI Search resources.
- Use the **More services** and **Classic AI services** sections to find other Azure AI services.

:::image type="content" source="../media/portal/overview.png" lightbox="../media/portal/overview.png" alt-text="The Azure AI Foundry overview page in the Azure portal.":::

You can also go directly to your hub and project resources in the Azure portal from the Azure AI Foundry portal by using the following steps:

> [!NOTE]
> These steps assume that the hub and project are in the same resource group.

1. In [Azure AI Foundry](https://ai.azure.com), go to the hub or project and select **Management center** to view your project resources.
1. From the management center, select the overview for the hub or project and then select the link to **Manage in Azure portal**.
    
    :::image type="content" source="../media/concepts/azureai-project-view-ai-studio.png" alt-text="Screenshot of the Azure AI Foundry project overview page with links to the Azure portal." lightbox="../media/concepts/azureai-project-view-ai-studio.png":::

## Next steps

- [Quickstart: Analyze images and video in the chat playground](/azure/ai-services/openai/gpt-v-quickstart)
- [Learn more about Azure AI Foundry](../what-is-azure-ai-foundry.md)
- [Learn more about projects](../how-to/create-projects.md)
