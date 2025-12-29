---
title: How to create and manage a Microsoft Foundry hub
titleSuffix: Microsoft Foundry
description: Learn how to create and manage a Microsoft Foundry hub from the Azure portal or from the Microsoft Foundry portal. Your developers can then create projects from the hub.
ms.service: azure-ai-foundry
ms.custom:
  - ignite-2023
  - build-2024
  - ignite-2024
  - hub-only
ms.topic: how-to
ms.date: 12/29/2025
ms.reviewer: deeikele
ms.author: sgilley
author: sdgilley
# Customer Intent: As an admin, I need to create and manage a Microsoft Foundry hub so that my team can use it to create projects for collaboration.
---

# How to create and manage a Microsoft Foundry hub

[!INCLUDE [hub-only-alt](../includes/uses-hub-only-alt.md)]

In [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs), hubs provide the environment for a team to collaborate and organize work, and help you as a team lead or IT admin centrally set up security settings and govern usage and spend. You can create and manage a hub from the Azure portal, and then your developers can create projects from the hub.

In this article, you learn how to create and manage a hub in Foundry portal with the default settings so you can get started quickly. Do you need to customize security or the dependent resources of your hub? Then use [Azure portal](create-secure-ai-hub.md) or [template options](create-azure-ai-hub-template.md). 

> [!TIP]
> If you're an individual developer and not an admin, dev lead, or part of a larger effort that requires a hub, you can create a project directly from the Foundry portal without creating a hub first. For more information, see [Create a project](create-projects.md).
> 
> If you're an admin or dev lead and would like to create your Foundry hub using a template, see the articles on using [Bicep](create-azure-ai-hub-template.md) or [Terraform](create-hub-terraform.md).

## Create a secure hub in the Azure portal

If your organization is using [Azure Policy](/azure/governance/policy/overview), set up a hub that meets your organization's requirements instead of using Foundry for resource creation. 

1. From the [Azure portal](https://portal.azure.com), search for `Foundry`. From the left menu, select **AI Hubs**, and then select **+ Create** and **Hub**.

    :::image type="content" source="../media/how-to/hubs/create-hub.png" alt-text="Screenshot of the Foundry portal." lightbox="../media/how-to/hubs/create-hub.png":::

1. Enter your hub name, subscription, resource group, and location details. For **Azure AI services base models**, select an existing Foundry resource or create a new one. Foundry resources include multiple API endpoints for Speech, Content Safety, and Azure OpenAI. 

1. Select the **Storage** tab to specify storage account settings. For storing credentials, either provide your Azure Key Vault or use the [Microsoft-managed credential store (preview)](#choose-how-credentials-are-stored).

1. Select the **Inbound Access** and **Outbound Access** tab to set up network isolation. For more information, see the [network isolation](configure-managed-network.md) article.


1. Select the **Encryption** tab to set up data encryption. By default, **Microsoft-managed keys** are used to encrypt data. You can select to **Encrypt data using a customer-managed key**. 

1. Select the **Identity** tab. By default, **System assigned identity** is enabled, but you can switch to **User assigned identity** if existing storage, key vault, and container registry are selected in **Storage**. You can also select whether to use **Credential-based** or **Identity-based** access to the storage account.

    > [!NOTE]
    > If you select **User assigned identity**, your identity needs to have the `Cognitive Services Contributor` role in order to successfully create a new hub.

1. Select **Review + create** > **Create**. 


## Manage access control

You can add and remove users from the [Foundry portal](https://ai.azure.com?cid=LearnDocs) management center. Both the hub and projects within the hub have a **Users** entry in the left-menu that allows you to add and remove users. When adding users, you can assign them built-in roles.

:::image type="content" source="../media/how-to/hubs/studio-user-management.png" alt-text="Screenshot of the users area of the management center for a hub." lightbox="../media/how-to/hubs/studio-user-management.png":::

For custom role assignments, use **Access control (IAM)** within the Azure portal.

To add grant users permissions from the Azure portal, see the [Azure role assignments](/azure/role-based-access-control/role-assignments-portal) article.

## Manage your hub from the Foundry portal

### Networking

Hub networking settings can be set during resource creation or changed in the **Networking** tab in the Azure portal view. Creating a new hub invokes a Managed Virtual Network. This streamlines and automates your network isolation configuration with a built-in Managed Virtual Network. The Managed Virtual Network settings are applied to all projects created within a hub. 

At hub creation, select between the networking isolation modes: **Public**, **Private with Internet Outbound**, and **Private with Approved Outbound**. To secure your resource, select either **Private with Internet Outbound** or **Private with Approved Outbound** for your networking needs. For the private isolation modes, a private endpoint should be created for inbound access. For more information on network isolation, see [Managed virtual network isolation](configure-managed-network.md). To create a secure hub, see [Create a secure hub](create-secure-ai-hub.md). 

At hub creation in the Azure portal, creation of associated Foundry Tools, Storage account, Key vault (optional), Application insights (optional), and Container registry (optional) is given. These resources are found on the Resources tab during creation. 

To connect to Foundry Tools (Azure OpenAI, Azure AI Search, and Azure AI Content Safety) or storage accounts in Foundry portal, create a private endpoint in your virtual network. Ensure the public network access (PNA) flag is disabled when creating the private endpoint connection. For more about Foundry Tools connections, see [Virtual networks for Foundry Tools](../../ai-services/cognitive-services-virtual-networks.md). You can optionally bring your own Azure AI Search, but it requires a private endpoint connection from your virtual network.

### Encryption
Projects that use the same hub, share their encryption configuration. Encryption mode can be set only at the time of hub creation between Microsoft-managed keys and Customer-managed keys (CMK). 

From the Azure portal view, navigate to the encryption tab, to find the encryption settings for your hub. 

For hubs that use CMK encryption mode, you can update the encryption key to a new key version. This update operation is constrained to keys and key versions within the same Key Vault instance as the original key.

:::image type="content" source="~/reusable-content/ce-skilling/azure/media/ai-studio/resource-manage-encryption.png" alt-text="Screenshot of the Encryption page of the hub in the Azure portal." lightbox="~/reusable-content/ce-skilling/azure/media/ai-studio/resource-manage-encryption.png":::

### Update Azure Application Insights and Azure Container Registry

To use custom environments for Prompt Flow, you're required to configure an Azure Container Registry for your hub. To use Azure Application Insights for Prompt Flow deployments, a configured Azure Application Insights resource is required for your hub. Updating the workspace-attached Azure Container Registry or Application Insights resources might break lineage of previous jobs, deployed inference endpoints, or your ability to rerun earlier jobs in the workspace. After association with a Foundry hub, Azure Container Registry and Application Insights resources can't be disassociated (set to null).

You can use the Azure portal, Azure SDK/CLI options, or the infrastructure-as-code templates to update both Azure Application Insights and Azure Container Registry for the hub.

# [Azure portal](#tab/portal)

You can configure your hub for these resources during creation or update after creation. 

To update Azure Application Insights from the Azure portal, navigate to the **Properties** for your hub in the Azure portal, then select **Change Application Insights**.

:::image type="content" source="~/reusable-content/ce-skilling/azure/media/ai-studio/resource-manage-update-associated-resources.png" alt-text="Screenshot of the properties page of the hub resource in the Azure portal." lightbox="~/reusable-content/ce-skilling/azure/media/ai-studio/resource-manage-update-associated-resources.png":::

# [Python SDK](#tab/python)

```python
from azure.ai.ml.entities import Hub

my_app_insights = "{APPLICATION_INSIGHTS_ARM_ID}"
my_container_registry = "{CONTAINER_REGISTRY_ARM_ID}"

# construct a basic hub
my_hub = Hub(name="myexamplehub", 
             location="East US", 
             application_insights=my_app_insights,
             container_registry=my_container_registry)

# update_dependent_resources is used to give consent to update the workspace dependent resources.
created_hub = ml_client.workspaces.begin_update(workspace=my_hub, update_dependent_resources=True).result()
```

# [Azure CLI](#tab/azurecli)

See flag documentation for [```az ml workspace update```](/cli/azure/ml/workspace#az-ml-workspace-update)

```azurecli
az ml workspace update -n "myexamplehub" -g "{MY_RESOURCE_GROUP}" -a "APPLICATION_INSIGHTS_ARM_ID" -u
```
---

### Choose how credentials are stored

Select scenarios in Foundry portal store credentials on your behalf. For example, when you create a connection in Foundry portal to access an Azure Storage account with stored account key, access Azure Container Registry with admin password, or when you create a compute instance with enabled SSH keys. No credentials are stored with connections when you choose Microsoft Entra ID identity-based authentication.

You can choose where credentials are stored:

- **Your Azure Key Vault**: This requires you to manage your own Azure Key Vault instance and configure it per hub. It gives you more control over secret lifecycle, for example, to set expiry policies. You can also share stored secrets with other applications in Azure.
   
- **Microsoft-managed credential store (preview)**: In this variant Microsoft manages an Azure Key Vault instance on your behalf per hub. No resource management is needed on your side and the vault doesn't show in your Azure subscription. Secret data lifecycle follows the resource lifecycle of your hubs and projects. For example, when a project's storage connection is deleted, its stored secret is deleted as well.

After your hub is created, it isn't possible to switch between Your Azure Key Vault and using a Microsoft-managed credential store.

## Delete a Foundry hub

To delete a hub from [Foundry](https://ai.azure.com?cid=LearnDocs), select the hub and then select **Delete hub** from the **Hub properties** section of the page.

:::image type="content" source="../media/how-to/hubs/studio-delete-hub.png" alt-text="Screenshot of the delete hub link in hub properties." lightbox="../media/how-to/hubs/studio-delete-hub.png":::

> [!NOTE]
> You can also delete the hub from the [Azure portal](https://portal.azure.com).

Deleting a hub deletes all associated projects. When a project is deleted, all nested endpoints for the project are also deleted. You can optionally delete connected resources; however, make sure that no other applications are using this connection. For example, another Foundry deployment might be using it.

## Related content

- [Create a hub project](hub-create-projects.md)
- [Learn more about Foundry](../what-is-azure-ai-foundry.md)
- [Learn more about hubs](../concepts/ai-resources.md)
