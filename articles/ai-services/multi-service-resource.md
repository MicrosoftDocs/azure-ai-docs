---
title: Create a Foundry resource
titleSuffix: Foundry Tools
description: Create and manage a Foundry resource.
author: laujan
ms.author: lajanuar
manager: nitinme
ms.date: 05/13/2026
ms.service: foundry-tools
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

:::image type="content" source="../foundry/media/how-to/projects/projects-multi-setup.png" alt-text="Diagram showing Foundry resource containing multiple projects, each with deployments and connections.":::

## Three ways to create a Foundry resource

Choose the path that matches your governance requirements:

| Approach | When to use it | How to create it |
| --- | --- | --- |
| **Basic setup** — public networking, Microsoft-managed encryption, default storage. | Quick prototypes, individual developers, or tenants without strict security requirements. | This quickstart (Azure portal, Azure CLI, or Azure PowerShell). |
| **With security controls** — your network, your encryption key, your identity, your policies. | IT admins enforcing an organization security baseline. | The Azure portal advanced tabs (Storage, Network, Identity, Encryption) shown in [Configure advanced security settings in the Azure portal](#configure-advanced-security-settings-in-the-azure-portal), or the [Bicep](../ai-foundry/how-to/create-resource-template.md) and [Terraform](../ai-foundry/how-to/create-resource-terraform.md) quickstarts. |
| **Standard setup for agents** — security controls plus your own Azure Cosmos DB, AI Search, and Storage account for agent thread storage. | Production agent deployments with data residency, compliance, or capacity-management requirements. Variants apply to Speech, Language, Vision, and Content Understanding. | The **Storage** > **Agent service** section of the Azure portal create wizard (shown in [Configure advanced security settings in the Azure portal](#configure-advanced-security-settings-in-the-azure-portal)), or the [Bicep](../ai-foundry/how-to/create-resource-template.md) and [Terraform](../ai-foundry/how-to/create-resource-terraform.md) quickstarts. |

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

## Configure advanced security settings in the Azure portal

The Azure portal **Create a Foundry resource** wizard exposes additional tabs for security and storage controls. Use these tabs when you create a resource with the **with security controls** or **standard setup for agents** approaches described earlier. Each tab corresponds to a specific governance concern; the following sections describe what each one controls and when to use it.

### Network tab — restrict who can reach your resource

On the **Network** tab, under **Inbound Access**, choose how the resource is reachable from outside Azure:

- **All networks** — public endpoint open to the internet. Use only for prototypes.
- **Selected networks** — public endpoint scoped to specific virtual networks and IP ranges.
- **Disabled** — public endpoint turned off. Reach the resource exclusively through [private endpoints](../ai-foundry/how-to/configure-private-link.md). Use this option for regulated workloads or when your organization's network policy bans public endpoints.

:::image type="content" source="media/multi-service-resource/advanced/foundry-create-network-tab.png" alt-text="Screenshot of the Network tab in the Create a Foundry resource wizard, showing the All networks, Selected networks, and Disabled options under Inbound Access." lightbox="media/multi-service-resource/advanced/foundry-create-network-tab.png":::

### Identity tab — choose how the resource authenticates to other services

On the **Identity** tab, enable a **system-assigned managed identity** (one identity tied to the resource lifecycle) or attach **user-assigned managed identities** (reusable identities you can grant to multiple resources). Use a managed identity instead of API keys whenever the Foundry resource needs to call Azure Storage, Azure Cosmos DB, Azure Key Vault, or any other Azure-RBAC-protected service. For role assignment guidance, see [Role-based access control for Foundry](../ai-foundry/concepts/rbac-foundry.md).

### Encryption tab — bring your own key for at-rest encryption

On the **Encryption** tab, the default is **Microsoft-managed keys**. Select **Encrypt data using a customer-managed key** (CMK) when your organization requires control over the key lifecycle, key rotation cadence, or revocation. CMK requires an Azure Key Vault with soft-delete and purge protection, and a managed identity with **Key Vault Crypto Service Encryption User** rights. For prerequisites and rotation guidance, see [Customer-managed keys for encryption](../ai-foundry/concepts/encryption-keys-portal.md).

:::image type="content" source="media/multi-service-resource/advanced/foundry-create-encryption-tab.png" alt-text="Screenshot of the Encryption tab in the Create a Foundry resource wizard, showing the Encrypt data using a customer-managed key checkbox under Data Encryption." lightbox="media/multi-service-resource/advanced/foundry-create-encryption-tab.png":::

### Storage tab — bring your own data stores for the Agent service

On the **Storage** tab, the **Credential storage and application logging** section lets you point the resource at your own **Azure Key Vault** and **Application Insights** instances instead of Microsoft-managed defaults.

The **Agent service** section is where you opt into the **standard setup for agents**. Select **Select Resources** to bind your own **Azure Cosmos DB** account (for thread storage), **Azure AI Search** index (for knowledge retrieval), and **Storage account** (for files) to a model deployment. Use this option when you need data residency, customer-managed encryption on agent data, or capacity isolation for production agent workloads. Speech and Language services have an analogous **Storage Account (preview)** option. For the architecture and prerequisites, see [Agent service capability hosts](../ai-foundry/agents/concepts/capability-hosts.md).

:::image type="content" source="media/multi-service-resource/advanced/foundry-create-storage-agent-service.png" alt-text="Screenshot of the Storage tab Agent service section in the Create a Foundry resource wizard, showing the Select Resources button and the Model Deployment, Cosmos DB, AI Search, and Storage Account columns, with the Speech and Language service section beneath it." lightbox="media/multi-service-resource/advanced/foundry-create-storage-agent-service.png":::

> [!TIP]
> If your security baseline is the same for every Foundry resource you create, capture it once with [Bicep](../ai-foundry/how-to/create-resource-template.md) or [Terraform](../ai-foundry/how-to/create-resource-terraform.md). The infrastructure-as-code articles cover the same controls plus parameterization, source control, and repeatable deployment.

## Access your resource

With your first resource created, you can access it via [Foundry portal for UX prototyping](https://ai.azure.com/), [Foundry SDK for development](../ai-foundry/how-to/develop/sdk-overview.md), or via [Azure portal for administrative management](https://portal.azure.com).

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
|Foundry Project Manager|Grants development permissions, and project management permissions. Can invite other users to collaborate on a project as 'Foundry User'.|
|Foundry User|Grants development permissions.|
| **Foundry Account Owner**   | Grants full access to manage AI projects and accounts. Can invite other users to collaborate on a project as 'Foundry User'. |
| **Foundry Owner**    | Grants full access to managed AI projects and accounts and build and develop with projects. |

[!INCLUDE [role-rename-note](../foundry/includes/role-rename-note.md)]

>[!NOTE]
> The Foundry Owner role will be available to assign in the Azure and Foundry portal soon.

:::image type="content" source="../foundry/media/how-to/network/detailed-rbac-diagram.png" alt-text="Diagram of the built-in roles in Foundry." lightbox="../foundry/media/how-to/network/detailed-rbac-diagram.png":::

For larger enterprises with strict role based access requirements, we recommend utilizing the Foundry User role the least  privilege developer permissions. For smaller enterprises wanting their developers to self-serve within their organization, we recommend utilizing the Foundry Owner role for developer permissions as well as resource creation permissions. 

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
