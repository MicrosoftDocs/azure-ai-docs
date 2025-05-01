---
title: Create a project
titleSuffix: Azure AI Foundry
description: This article describes how to create an Azure AI Foundry project so you can work with generative AI in the cloud.
manager: scottpolly
ms.service: azure-ai-foundry
ms.custom:
  - ignite-2023
  - build-2024
  - ignite-2024
ms.topic: how-to
ms.date: 04/11/2025
ms.reviewer: deeikele
ms.author: sgilley
author: sdgilley
zone_pivot_groups: project-type
# customer intent: As a developer, I want to create an Azure AI Foundry project so I can work with generative AI.
---

# Create a project for Azure AI Foundry

This article describes how to create an [Azure AI Foundry](https://ai.azure.com) project. A project is used to organize your work and save state while building customized AI apps.

Azure AI Foundry supports two types of projects: a **[!INCLUDE [fdp](../includes/fdp-project-name.md)]** and a **[!INCLUDE [hub](../includes/hub-project-name.md)]**. For more information about the differences between these two project types, see [Types of projects](../what-is-azure-ai-foundry.md#project-types).

::: zone pivot="fdp-project"

> [!TIP]
> The rest of this article shows how to create a **[!INCLUDE [fdp](../includes/fdp-project-name.md)]**.  Select **[!INCLUDE [hub](../includes/hub-project-name.md)]** at the top of this article if you want to create a [!INCLUDE [hub](../includes/hub-project-name.md)] instead.

A [!INCLUDE [fdp](../includes/fdp-project-name.md)] is built on an Azure AI Foundry resource. This project type does not use a hub. Essential connections to storage and Azure AI Search are built into the resource for more seamless development. 

::: zone-end

::: zone pivot="hub-project"

> [!TIP]
> The rest of this article shows how to create a **[!INCLUDE [hub](../includes/hub-project-name.md)]**.  Select **[!INCLUDE [fdp](../includes/fdp-project-name.md)]** at the top of this article if you want to create a [!INCLUDE [fdp](../includes/fdp-project-name.md)] instead.

A [!INCLUDE [hub](../includes/hub-project-name.md)] is hosted by an Azure AI Foundry hub. If your company has an administrative team that has created a hub for you, you can create a project from that hub. If you are working on your own, you can create a project and a default hub will automatically be created for you.

For more information about the projects and hubs model, see [Azure AI Foundry hubs](../concepts/ai-resources.md).

::: zone-end

## Prerequisites

::: zone pivot="fdp-project"

Use the following tabs to select the method you plan to use to create a [!INCLUDE [fdp](../includes/fdp-project-name.md)]:

# [Azure AI Foundry portal](#tab/ai-foundry)

- An Azure subscription. If you don't have an Azure subscription, create a [free account](https://azure.microsoft.com/free/).
- You must be **Owner** of the subscription to assign the appropriate access control needed to use the project.


# [Python SDK](#tab/python)

- An Azure subscription. If you don't have an Azure subscription, create a [free account](https://azure.microsoft.com/free/).
- You must be **Owner** of the subscription to assign the appropriate access control needed to use the project.
- [Set up your development environment](develop/install-cli-sdk.md?tabs=python)
- Authenticate with `az login` or `az login --use-device-code` in your environment before running code.


# [Azure CLI](#tab/azurecli)

- An Azure subscription. If you don't have an Azure subscription, create a [free account](https://azure.microsoft.com/free/).
- You must be **Owner** of the subscription to assign the appropriate access control needed to use the project.
- [Azure CLI](/cli/azure/install-azure-cli) 

---

::: zone-end

::: zone pivot="hub-project"

Use the following tabs to select the method you plan to use to create a [!INCLUDE [hub](../includes/hub-project-name.md)]:

# [Azure AI Foundry portal](#tab/ai-foundry)

- An Azure subscription. If you don't have an Azure subscription, create a [free account](https://azure.microsoft.com/free/).

# [Python SDK](#tab/python)

- An Azure subscription. If you don't have an Azure subscription, create a [free account](https://azure.microsoft.com/free/).
- [Azure Machine Learning SDK v2](https://aka.ms/sdk-v2-install).
- An Azure AI Foundry hub. If you don't have a hub, see [Create a hub using the Azure Machine Learning SDK and CLI](develop/create-hub-project-sdk.md).
- [Azure CLI](/cli/azure/install-azure-cli) 
- Authenticate with `az login` or `az login --use-device-code` in your environment before running code.


# [Azure CLI](#tab/azurecli)

- An Azure subscription. If you don't have an Azure subscription, create a [free account](https://azure.microsoft.com/free/).
- [Azure CLI and the machine learning extension](/azure/machine-learning/how-to-configure-cli). If you don't have the Azure CLI and machine learning extension installed, follow the steps in the [Install and set up the machine learning extension](/azure/machine-learning/how-to-configure-cli) article.
- An Azure AI Foundry hub. If you don't have a hub, see [Create a hub using the Azure Machine Learning SDK and CLI](develop/create-hub-project-sdk.md).

---
::: zone-end

## Create a project

# [Azure AI Foundry portal](#tab/ai-foundry)

::: zone pivot="fdp-project"

[!INCLUDE [Create Azure AI Foundry project](../includes/create-fdp-project.md)]

::: zone-end

::: zone pivot="hub-project"

[!INCLUDE [Create Azure AI Foundry project](../includes/create-hub-project.md)]

::: zone-end

# [Python SDK](#tab/python)

::: zone pivot="fdp-project"

To create a [!INCLUDE [fdp](../includes/fdp-project-name.md)]:

1. Install azure-identity: `pip install azure-identity`. If in a notebook cell, use `%pip install azure-identity`.

1. Use the following code to create a [!INCLUDE [fdp-project-name](../includes/fdp-project-name.md)]:

    ```python
    from azure.identity import DefaultAzureCredential
    from azure.mgmt.cognitiveservices import CognitiveServicesManagementClient
    import os
    import json
    
    subscription_id = 'your-subscription-id'
    resource_group_name = 'your-resource-group-name'
    foundry_resource_name = 'your-foundry-resource-name'
    foundry_project_name = 'your-foundry-project-name'
    location = 'eastus'
    
    # TODO: add code to create create a new resource group
    
    client = CognitiveServicesManagementClient(
        subscription_id=subscription_id,
        credential=DefaultAzureCredential(), 
        api_version="2025-04-01-preview"
    )
    
    account = client.accounts.begin_create(
        resource_group_name=resource_group_name,
        account_name=foundry_resource_name,
        foundry_project_name=foundry_project_name,
        account={
            "location": location,
            "kind": "AIServices",
            "sku": {
                "name": "S0",
            },
            "identity": {
                "type": "SystemAssigned"
            },
            "properties": {
                "allowProjectManagement": True
            }
        }
    )
    
    # TODO: code to do role assignment to give user project manager role on the account
    ```
1. (Optional) If you have multiple accounts, add the tenant ID of the Microsoft Entra ID you wish to use into the `DefaultAzureCredential`. Find your tenant ID from the [Azure portal](https://portal.azure.com) under **Microsoft Entra ID, External Identities**.
        
    ```python
    DefaultAzureCredential(interactive_browser_tenant_id="<TENANT_ID>")
    ```
        
1. (Optional) If you're working on in the [Azure Government - US](/azure/azure-government/documentation-government-welcome) or [Azure China 21Vianet](https://azure.microsoft.com/global-infrastructure/services/?regions=china-east-2%2cchina-non-regional&products=all) regions, specify the region into which you want to authenticate. You can specify the region with `DefaultAzureCredential`. The following example authenticates to the Azure Government - US region:
        
    ```python
    from azure.identity import AzureAuthorityHosts
    DefaultAzureCredential(authority=AzureAuthorityHosts.AZURE_GOVERNMENT)
    ```

::: zone-end

::: zone pivot="hub-project"

The code in this section assumes you have an existing hub.  If you don't have a hub, see [How to create and manage an Azure AI Foundry hub](create-azure-ai-resource.md) to create one.

[!INCLUDE [SDK setup](../includes/development-environment-config.md)]

6. Use the following code to create a project from a hub you or your administrator created previously. Replace example string values with your own values:

    ```Python
    from azure.ai.ml.entities import Project
    
    my_project_name = "myexampleproject"
    my_display_name = "My Example Project"
    hub_name = "myhubname" # Azure resource manager ID of the hub
    hub_id=f"/subscriptions/{subscription_id}/resourceGroups/{resource_group}/providers/Microsoft.MachineLearningServices/workspaces/{hub_name}"
    
    my_project = Project(name=my_project_name, 
                    display_name=my_display_name,
                    hub_id=hub_id)
    
    created_project = ml_client.workspaces.begin_create(workspace=my_project).result()
    ```

::: zone-end

# [Azure CLI](#tab/azurecli)

::: zone pivot="fdp-project"

To create a [!INCLUDE [fdp](../includes/fdp-project-name.md)]:

1. Authenticate to your Azure subscription from the Azure CLI with the following command:

    ```azurecli
    az login
    ```

    For more information on authenticating, see [Authentication methods](/cli/azure/authenticate-azure-cli).

1. Once the extension is installed and authenticated to your Azure subscription, create a resource group:

    ```azurecli
    az group create --name {my_resource_group} --location eastus
    ```

- Assign role assignments to the group.  Substitute your name and resource group in these commands:

   ```azurecli
    az role assignment create --role "Azure AI User" --assignee "joe@contoso.com" --resource-group {my_resource_group} 
    az role assignment create --role "Azure AI Developer" --assignee "joe@contoso.com" --resource-group {my_resource_group} 
    ```

1. Now use the following command to create a new [!INCLUDE [fdp](../includes/fdp-project-name.md)]:

    ```azurecli
    az cognitiveservices account project create --name {my_project_name} -resource-group {my_resource_group}
    ```

::: zone-end

::: zone pivot="hub-project"

The code in this section assumes you have an existing hub.  If you don't have a hub, see [How to create and manage an Azure AI Foundry hub](create-azure-ai-resource.md) to create one.

1. To authenticate to your Azure subscription from the Azure CLI, use the following command:

    ```azurecli
    az login
    ```

    For more information on authenticating, see [Authentication methods](/cli/azure/authenticate-azure-cli).

1. Once the extension is installed and authenticated to your Azure subscription, use the following command to create a new Azure AI Foundry project from an existing Azure AI Foundry hub:

    ```azurecli
    az ml workspace create --kind project --hub-id {my_hub_ID} --resource-group {my_resource_group} --name {my_project_name}
    ```

    Form `my_hub_ID` with this syntax: `/subscriptions/{subscription_id}/resourceGroups/{resource_group}/providers/Microsoft.MachineLearningServices/workspaces/{hub_name}`.

::: zone-end

---

## View project settings

# [Azure AI Foundry portal](#tab/ai-foundry)

::: zone pivot="fdp-project"


On the project **Overview** page you can find information about the project.

- Name: The name of the project appears in the top left corner. You can rename the project using the edit tool.
- Subscription: The subscription that hosts the hub that hosts the project.
- Resource group: The resource group that hosts the hub that hosts the project.

::: zone-end

::: zone pivot="hub-project"

On the project **Overview** page you can find information about the project.

:::image type="content" source="../media/how-to/projects/project-settings.png" alt-text="Screenshot of an Azure AI Foundry project settings page." lightbox = "../media/how-to/projects/project-settings.png":::

- Name: The name of the project appears in the top left corner. You can rename the project using the edit tool.
- Subscription: The subscription that hosts the hub that hosts the project.
- Resource group: The resource group that hosts the hub that hosts the project.

Select **Management center** to navigate to the project resources in Azure AI Foundry portal.
Select **Manage in Azure portal** to navigate to the project resources in the Azure portal.

::: zone-end

# [Python SDK](#tab/python)

::: zone pivot="fdp-project"

```python
    # Get project
    project = client.projects.get(
        resource_group_name=rgp,
        account_name=account_name,
        project_name=project_name
    )
    print(project)
```

::: zone-end

::: zone pivot="hub-project"

To manage or use the new project, include it in the `MLClient`:

```python
ml_client = MLClient(workspace_name=my_project_name, resource_group_name=resource_group, subscription_id=subscription_id,credential=DefaultAzureCredential())
```
::: zone-end

# [Azure CLI](#tab/azurecli)

::: zone pivot="fdp-project"

To view settings for the project, use the `az cognitiveservices account connection show` command. For example:

```azurecli
az cognitiveservices account connection show --name {my_project_name} --resource-group {my_resource_group}
```

::: zone-end

::: zone pivot="hub-project"

To view settings for the project, use the `az ml workspace show` command. For example:

```azurecli
az ml workspace show --name {my_project_name} --resource-group {my_resource_group}
```

::: zone-end
---

::: zone pivot="hub-project"

## Access project resources

Common configurations on the hub are shared with your project, including connections, compute instances, and network access, so you can start developing right away.

In addition, a number of resources are only accessible by users in your project workspace:

- Components including datasets, flows, indexes, deployed model API endpoints (open and serverless).
- Connections created by you under 'project settings.'
- Azure Storage blob containers, and a fileshare for data upload within your project. Access storage using the following connections:
   
   | Data connection | Storage location | Purpose |
   | --- | --- | --- |
   | workspaceblobstore | {project-GUID}-azureml-blobstore | Default container for data uploads |
   | workspaceartifactstore | {project-GUID}-azureml | Stores components and metadata for your project such as model weights |
   | workspacefilestore | {project-GUID}-code | Hosts files created on your compute and using prompt flow |

> [!NOTE]
> Storage connections are not created directly with the project when your storage account has public network access set to disabled. These are created instead when a first user accesses Azure AI Foundry over a private network connection. [Troubleshoot storage connections](troubleshoot-secure-connection-project.md#troubleshoot-configurations-on-connecting-to-storage)

::: zone-end

## Related content

- [Deploy an enterprise chat web app](../tutorials/deploy-chat-web-app.md)

- [Learn more about Azure AI Foundry](../what-is-azure-ai-foundry.md)

::: zone pivot="hub-project"

- [Learn more about hubs](../concepts/ai-resources.md)

::: zone-end