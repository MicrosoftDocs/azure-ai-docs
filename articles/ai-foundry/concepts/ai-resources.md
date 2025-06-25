---
title: Hubs and hub-based project overview
titleSuffix: Azure AI Foundry
description: This article introduces concepts about Azure AI Foundry hubs for your Azure AI Foundry projects.
ms.author: sgilley
author: sdgilley
manager: scottpolly
ms.reviewer: deeikele
ms.date: 04/28/2025
ms.service: azure-ai-foundry
ms.topic: concept-article
ms.custom:
  - ignite-2023
  - build-2024
  - ai-learning-hub
  - ignite-2024
  - build-aifnd
  - build-2025
---

# Hub resources overview

> [!NOTE]
> You must use a **[!INCLUDE [hub](../includes/hub-project-name.md)]** for the features mentioned in this article. A **[!INCLUDE [fdp](../includes/fdp-project-name.md)]** is not supported. For more information, see [Project types](../what-is-azure-ai-foundry.md#which-type-of-project-do-i-need).

Azure AI Hub is a resource type that is used in combination with Azure AI Foundry resource type, and is only required for selected use cases. Hub resources provides access to open-source model hosting and finetuning capabilities, as well as Azure Machine Learning capabilities, next to capabilities supported by its associated AI Foundry resource.

When you create an AI Hub, an Azure AI Foundry resource is automatically provisioned. Hub resources can be used in [Azure AI Foundry](https://ai.azure.com/?cid=learnDocs) and [Azure Machine Learning studio](https://ml.azure.com).

Hubs have their own project types that support a differentiated feature set from Foundry projects. See [project types](../what-is-azure-ai-foundry.md#which-type-of-project-do-i-need) for an overview of supported features.

## Create an AI hub resource

Get started by [creating your first hub in Azure AI Foundry portal](../how-to/create-azure-ai-resource.md), or use [Azure portal](../how-to/create-secure-ai-hub.md) or [templates](../how-to/create-azure-ai-hub-template.md) for advanced configuration options such as networking.

Hubs group one or more projects together with common settings including data access and security configurations. Projects act as folders to organize work and give access to developer APIs.

## Create a hub-based project

To start developing, [create a [!INCLUDE [hub-project-name](../includes/hub-project-name.md)]](../how-to/create-projects.md?pivots=hub-project). Hub-projects can be accessed in [AI Foundry Portal](https://ai.azure.com/?cid=learnDocs) to build with generative AI tools, and [ML Studio](https://ml.azure.com) to build with tools designed for custom machine learning model training.

## Project concepts

Projects let you create and group reusable components that can be used across tools:

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

## Share configurations across projects using hub

A hub shares configurations for a group of projects. As a team lead, consider creating a hub for use cases that share the same security configurations or business domain to avoid repetitive setup and let developers create their own project against the pre-configured environment.

Shared configurations managed on the hub include:
* **Security** including public network access, customer-managed key encryption, and identity controls. Security settings configured on the hub automatically pass down to each project. A managed virtual network is shared between all projects that share the same hub.
* **Connections** let you access objects in Azure AI Foundry portal that are managed outside of your hub. For example, uploaded data on an Azure storage account, or model deployments on an existing Azure OpenAI or AI Foundry resource. Optionally use connection to store shared credentials, so developers can implicitly access remote objects during development.
* **Compute and quota allocation** is managed as shared capacity for all projects in Azure AI Foundry portal that share the same hub. This quota includes compute instance as managed cloud-based workstation for an individual. The same user can use a compute instance across projects.
* **Policy** enforced in Azure on the hub scope applies to all projects managed under it.
* **Dependent Azure resources** are set up once per hub and associated projects and used to store artifacts you generate while working in Azure AI Foundry portal such as logs or when uploading data. For more information, see [dependent resources](#storage-and-key-vault-dependent-resources).

## Access Azure AI Foundry models from hub-based projects

Hubs let you manage connections to existing Azure OpenAI or Azure AI Foundry resources, so you can use their models and selected customization capabilities in hub-based projects. 

After a connection is created, model deployments are accessible via playground experiences. When you use Finetuning experiences in a hub-based project, your finetuning jobs are implicitly executed on the connected AI Foundry resource (default project context).

## Storage and Key Vault dependent resources

Azure AI Hub is an implementation of Azure Machine Learning and requires multiple Azure services as a dependency.

[!INCLUDE [Resource provider kinds](../includes/resource-provider-kinds.md)]

If not provided by you, the following dependent resources are automatically created.

[!INCLUDE [Dependent Azure resources](../includes/dependent-resources.md)]

## Next steps

- [Create a [!INCLUDE [hub-project-name](../includes/hub-project-name.md)]](../how-to/create-projects.md?pivots=hub-project)
- [Quickstart: Analyze images and video in the chat playground](/azure/ai-services/openai/gpt-v-quickstart)
- [Learn more about Azure AI Foundry](../what-is-azure-ai-foundry.md)
- [Learn more about projects](../how-to/create-projects.md?pivots=hub-project)
