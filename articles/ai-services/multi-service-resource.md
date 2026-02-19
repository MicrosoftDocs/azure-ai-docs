---
title: Create a Foundry resource
titleSuffix: Foundry Tools
description: Create and manage a Foundry resource.
author: laujan
ms.author: lajanuar
manager: nitinme
ms.date: 10/02/2025
ms.service: azure-ai-services
ms.topic: quickstart
ms.custom:
  - devx-track-azurecli
  - devx-track-azurepowershell
  - build-2024
  - ignite-2024
  - build-2025
  - ai-assisted
ai-usage: ai-assisted
zone_pivot_groups: programming-languages-portal-cli-ps
---

# Quickstart: Set up your first Foundry resource

In this quickstart, you create a Microsoft Foundry resource and verify access.

Learn how to create and manage a Foundry resource. It's the [primary Azure resource type](../ai-foundry/concepts/resource-types.md) for building, deploying, and managing generative AI models and applications including agents in Azure.

An Azure resource is required to use and manage services in Azure. It defines the scope for configuring access, security such as networking, billing, and monitoring. 

Foundry resource is the next version and renaming of former "Foundry Tools". It provides the application environment for hosting your agents, model deployments, evaluations, and more.

A Foundry resource can organize the work for multiple use cases, and is [typically shared](../ai-foundry/concepts/planning.md) between a team of developers that work on use cases in a similar business or data domain. Projects act as folders to group related work. 

:::image type="content" source="../ai-foundry/media/how-to/projects/projects-multi-setup.png" alt-text="Diagram showing Foundry resource containing multiple projects, each with deployments and connections.":::

> [!NOTE]
> Only the default project is available in the Foundry (new) portal. Use the Foundry (classic) portal to interact with all other projects on a Foundry resource.

Looking to configure Foundry with advanced security settings? See [advanced Foundry creation options](../ai-foundry/how-to/create-resource-template.md)

## Create your first resource

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

With your first resource created, you can access it via [Foundry portal for UX prototyping](https://ai.azure.com/), [Foundry SDK for development](), or via [Azure portal for administrative management](https://portal.azure.com).

### Verify your setup

You can verify that your resource is set up correctly by using the Azure AI Projects SDK to connect and list projects. This minimal example confirms authentication and access.

```python
# Install the SDK: pip install azure-ai-projects azure-identity
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

# Replace with your actual values from Azure portal
client = AIProjectClient(
    subscription_id="<your-subscription-id>",
    resource_group_name="<your-resource-group>",
    project_name="<your-project-name>",
    credential=DefaultAzureCredential()
)

# List projects to verify connection
projects = client.projects.list()
print(f"Successfully connected. Found {len(list(projects))} projects.")
```

**Expected output**: `Successfully connected. Found X projects.` where X is the number of projects in your resource.

**References**:
- [AIProjectClient class](/python/api/azure-ai-projects/azure.ai.projects.aiprojectclient)
- [DefaultAzureCredential class](/python/api/azure-identity/azure.identity.defaultazurecredential)

## Grant or obtain developer permissions

[Azure Role Based Access Control](/azure/role-based-access-control/resource-provider-operations) (RBAC) differentiates permissions between management and development actions. To build with Foundry, your user account must be assigned developer permissions ("data actions"). You can either use one of the built-in RBAC roles, or use a custom RBAC role.

Built-in Azure RBAC developer roles for Foundry include:

|Role|Description|
|---|---|
|Azure AI Project Manager|Grants development permissions, and project management permissions. Can invite other users to collaborate on a project as 'Azure AI User'.|
|Azure AI User|Grants development permissions.|
| **Azure AI Account Owner**   | Grants full access to manage AI projects and accounts. Can invite other users to collaborate on a project as 'Azure AI User'. |
| **Azure AI Owner**    | Grants full access to managed AI projects and accounts and build and develop with projects. |

>[!NOTE]
> The Azure AI Owner role will be available to assign in the Azure and Foundry portal soon.

:::image type="content" source="../ai-foundry/media/how-to/network/detailed-rbac-diagram.png" alt-text="Diagram of the built-in roles in Foundry." lightbox="../ai-foundry/media/how-to/network/detailed-rbac-diagram.png":::

For larger enterprises with strict role based access requirements, we recommend utilizing the Azure AI User role the least  privilege developer permissions. For smaller enterprises wanting their developers to self-serve within their organization, we recommend utilizing the Azure AI Owner role for developer permissions as well as resource creation permissions. 

Only authorized users, typically the Azure subscription or resource group owner, can assign a role via either [Azure portal](link to Azure portal) or [Foundry portal via Admin](Link to Foundry portal). [Learn more about role-based access control](../ai-foundry/concepts/rbac-foundry.md).

> [!IMPORTANT]
> Azure Owner and Contributor roles do only include management permissions, and not development permissions. Development permissions are required to build with all capabilities in Foundry.

## Start building in your first project

With permissions set up, you're now ready to start building Foundry. In [Foundry portal](https://ai.azure.com/) open or [create your first project](../ai-foundry/how-to/create-projects.md). Projects organize your agent and model customization work in Foundry, and you can [create multiple under the same resource](../ai-foundry/how-to/create-projects.md#create-multiple-projects-on-the-same-resource).

Explore some of the services that come bundled with your resource:

| Service | Description | 
| --- | --- | 
| ![Foundry icon](~/reusable-content/ce-skilling/azure/media/ai-services/ai-foundry.svg) [Foundry Agent Service](./agents/index.yml) | Combine the power of generative AI models with tools that allow agents to access and interact with real-world data sources. |
| ![Foundry icon](~/reusable-content/ce-skilling/azure/media/ai-services/ai-foundry.svg) [Azure Model Inference](../ai-foundry/model-inference/index.yml) | Performs model inference for flagship models in the Foundry model catalog. |
| ![Azure OpenAI in Foundry Models icon](~/reusable-content/ce-skilling/azure/media/ai-services/azure-openai.svg) [Azure OpenAI](../ai-foundry/openai/index.yml) | Perform a wide variety of natural language tasks. | 
| ![Content Safety icon](~/reusable-content/ce-skilling/azure/media/ai-services/content-safety.svg) [Content Safety](./content-safety/index.yml) | A Foundry Tool that detects unwanted contents. | 
| ![Document Intelligence icon](~/reusable-content/ce-skilling/azure/media/ai-services/document-intelligence.svg) [Document Intelligence](./document-intelligence/index.yml) | Turn documents into intelligent data-driven solutions. |
| ![Language icon](~/reusable-content/ce-skilling/azure/media/ai-services/language.svg) [Language](./language-service/index.yml) | Build apps with industry-leading natural language understanding capabilities. |
| ![Speech icon](~/reusable-content/ce-skilling/azure/media/ai-services/speech.svg) [Speech](./speech-service/index.yml) | Speech to text, text to speech, translation, and speaker recognition. |
| ![Translator icon](~/reusable-content/ce-skilling/azure/media/ai-services/translator.svg) [Translator](./translator/index.yml) | Use AI-powered translation technology to translate more than 100 in-use, at-risk, and endangered languages and dialects. | 

## Next steps

- [Create a project](../ai-foundry/how-to/create-projects.md) to organize your work.
- [Connect tools](../ai-foundry/how-to/connections-add.md) to build more rich applications.
- Learn about [access control in Foundry](../ai-foundry/concepts/rbac-foundry.md) to invite others to your working environment.
- [Secure your resource using private networking](../ai-foundry/how-to/configure-private-link.md)
