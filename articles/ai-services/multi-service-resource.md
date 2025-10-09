---
title: Create an AI Foundry resource
titleSuffix: Azure AI services
description: Create and manage an AI Foundry resource.
author: jonburchel
ms.author: jburchel
ms.date: 10/07/2025
ms.service: azure-ai-services
ms.topic: quickstart
ms.custom:
  - devx-track-azurecli
  - devx-track-azurepowershell
  - build-2024
  - ignite-2024
  - build-2025
zone_pivot_groups: programming-languages-portal-cli-ps
---

# Quickstart: Set up your first AI Foundry resource

Learn how to create and manage an Azure AI Foundry resource. It's the [primary Azure resource type](../ai-foundry/concepts/resource-types.md) for building, deploying, and managing generative AI models and applications including agents in Azure.

An Azure resource is required to use and manage services in Azure. It defines the scope for configuring access, security such as networking, billing, and monitoring. 

Azure AI Foundry resource is the next version and renaming of former "Azure AI Services". It provides the application environment for hosting your agents, model deployments, evaluations, and more.

Looking to configure AI Foundry with advanced security settings? See [advanced AI Foundry creation options](../ai-foundry/how-to/create-resource-template.md)

Looking to use [Azure AI Search skills?](../search/tutorial-skillset.md) See [Use Azure AI Foundry with Azure AI Search skills](multi-services-resource-search-skills.md).

## Create your first resource

An Azure AI Foundry resource can organize the work for multiple use cases, and is [typically shared](../ai-foundry/concepts/planning.md) between a team of developers that work on use cases in a similar business or data domain. Projects acts as folders to group related work.

:::image type="content" source="../ai-foundry/media/how-to/projects/projects-multi-setup.png" alt-text="Diagram explaining concepts of an Azure AI Foundry setup.":::

To create your first resource, with basic Azure settings, follow the below steps using either Azure portal, Azure CLI, or PowerShell.

::: zone pivot="azportal"

[!INCLUDE [Azure portal quickstart](includes/quickstarts/management-azportal.md)]

::: zone-end

::: zone pivot="azcli"

[!INCLUDE [Azure CLI quickstart](includes/quickstarts/management-azcli.md)]

::: zone-end

::: zone pivot="azpowershell"

[!INCLUDE [Azure PowerShell quickstart](includes/quickstarts/management-azpowershell.md)]

::: zone-end

## Access your resource

With your first resource created, you can access it via [Foundry Portal for UX prototyping](https://ai.azure.com/), [Foundry SDK for development](), or via [Azure portal for administrative management](https://portal.azure.com).

## Grant or obtain developer permissions

[Azure Role Based Access Control](/azure/role-based-access-control/resource-provider-operations) (RBAC) differentiates permissions between management and development actions. To build with Foundry, your user account must be assigned developer permissions ("data actions"). You can either use one of the built-in RBAC roles, or use a custom RBAC role.

Built-in Azure RBAC developer roles for Foundry include:

|Role|Description|
|---|---|
|Azure AI project manager|Grants development permissions, and project management permissions. Can invite other users to collaborate on a project as 'Azure AI user'.|
|Azure AI user|Grants development permissions.|

Only authorized users, typically the Azure subscription or resource group owner, can assign a role via either [Azure portal] or [AI Foundry Portal via management center]. [Learn more about role-based access control](../ai-foundry/concepts/rbac-azure-ai-foundry.md).

> [!IMPORTANT]
> Azure Owner and Contributor roles do only include management permissions, and not development permissions. Development permissions are required to build with all capabilities in Foundry.

## Start building in your first project

With permissions set up, you're now ready to start building Foundry. In [Azure AI Foundry Portal](https://ai.azure.com/) open or [create your first project](../ai-foundry/how-to/create-projects.md). Projects organize your agent and model customization work in Foundry, and you can create multiple under the same resource.

Explore some of the services that come bundled with your resource:

| Service | Description | 
| --- | --- | 
| ![Azure AI Foundry icon](~/reusable-content/ce-skilling/azure/media/ai-services/ai-foundry.svg) [Azure AI Foundry Agent Service](./agents/index.yml) | Combine the power of generative AI models with tools that allow agents to access and interact with real-world data sources. |
| ![Azure AI Foundry icon](~/reusable-content/ce-skilling/azure/media/ai-services/ai-foundry.svg) [Azure AI Model Inference](../ai-foundry/model-inference/index.yml) | Performs model inference for flagship models in the Azure AI Foundry model catalog. |
| ![Azure OpenAI in Azure AI Foundry Models icon](~/reusable-content/ce-skilling/azure/media/ai-services/azure-openai.svg) [Azure OpenAI](../ai-foundry/openai/index.yml) | Perform a wide variety of natural language tasks. | 
| ![Content Safety icon](~/reusable-content/ce-skilling/azure/media/ai-services/content-safety.svg) [Content Safety](./content-safety/index.yml) | An AI service that detects unwanted contents. | 
| ![Document Intelligence icon](~/reusable-content/ce-skilling/azure/media/ai-services/document-intelligence.svg) [Document Intelligence](./document-intelligence/index.yml) | Turn documents into intelligent data-driven solutions. |
| ![Language icon](~/reusable-content/ce-skilling/azure/media/ai-services/language.svg) [Language](./language-service/index.yml) | Build apps with industry-leading natural language understanding capabilities. |
| ![Speech icon](~/reusable-content/ce-skilling/azure/media/ai-services/speech.svg) [Speech](./speech-service/index.yml) | Speech to text, text to speech, translation, and speaker recognition. |
| ![Translator icon](~/reusable-content/ce-skilling/azure/media/ai-services/translator.svg) [Translator](./translator/index.yml) | Use AI-powered translation technology to translate more than 100 in-use, at-risk, and endangered languages and dialects. | 

## Next steps

- [Create a project](../ai-foundry/how-to/create-projects.md) to organize your work.
- [Connect tools](../ai-foundry/how-to/connections-add.md) to build more rich applications.
- Learn about [access control in AI Foundry](../ai-foundry/concepts/rbac-azure-ai-foundry.md) to invite others to your working environment.
- [Secure your resource using private networking](../ai-foundry/how-to/configure-private-link.md)
- [Use Azure AI Foundry with Azure AI Search skills](multi-services-resource-search-skills.md)
