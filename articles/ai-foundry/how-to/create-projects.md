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

This article describes how to create an [Azure AI Foundry](https://ai.azure.com) project. Projects are folders that let you organize your work for exploring new ideas, and as you're prototyping on a particular use cases.

Azure AI Foundry supports two types of projects: a **[!INCLUDE [fdp](../includes/fdp-project-name.md)]** and a **[!INCLUDE [hub](../includes/hub-project-name.md)]**. For more information about the differences between these two project types, see [Types of projects](../what-is-azure-ai-foundry.md#project-types).

::: zone pivot="hub-project"

> [!TIP]
> The rest of this article shows how to create a **[!INCLUDE [hub](../includes/hub-project-name.md)]**. Select **[!INCLUDE [fdp](../includes/fdp-project-name.md)]** at the top of this article if you want to create a [!INCLUDE [fdp](../includes/fdp-project-name.md)] instead.


* [!INCLUDE [hub-description](../includes/hub-description.md)]

* Use this project type for:

    * Prompt flow
    * Models-as-a-platform
    * [Azure Machine Learning](../../machine-learning/index.yml) compatibility

* This project can also be used for:

    * Agents (preview)
    * Project-level isolation of files and outputs
    * Evaluations
    * Playgrounds


## Prerequisites

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

## Create a project

# [Azure AI Foundry portal](#tab/ai-foundry)

[!INCLUDE [Create Azure AI Foundry project](../includes/create-hub-project.md)]

# [Python SDK](#tab/python)

The code in this section assumes you have an existing hub. If you don't have a hub, see [How to create and manage an Azure AI Foundry hub](create-azure-ai-resource.md) to create one.

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

# [Azure CLI](#tab/azurecli)

The code in this section assumes you have an existing hub. If you don't have a hub, see [How to create and manage an Azure AI Foundry hub](create-azure-ai-resource.md) to create one.

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

---

## View project settings

# [Azure AI Foundry portal](#tab/ai-foundry)

On the project **Overview** page, you can find information about the project.

:::image type="content" source="../media/how-to/projects/project-settings.png" alt-text="Screenshot of an Azure AI Foundry project settings page." lightbox = "../media/how-to/projects/project-settings.png":::

- Name: The name of the project appears in the top left corner. You can rename the project using the edit tool.
- Subscription: The subscription that hosts the hub that hosts the project.
- Resource group: The resource group that hosts the hub that hosts the project.

Select **Management center** to navigate to the project resources in Azure AI Foundry portal.
Select **Manage in Azure portal** to navigate to the project resources in the Azure portal.

# [Python SDK](#tab/python)

To manage or use the new project, include it in the `MLClient`:

```python
ml_client = MLClient(workspace_name=my_project_name, resource_group_name=resource_group, subscription_id=subscription_id,credential=DefaultAzureCredential())
```

# [Azure CLI](#tab/azurecli)

To view settings for the project, use the `az ml workspace show` command. For example:

```azurecli
az ml workspace show --name {my_project_name} --resource-group {my_resource_group}
```

---


## Access project resources

Common configurations on the hub are shared with your project, including connections, compute instances, and network access, so you can start developing right away.

In addition, many resources are only accessible by users in your project workspace:

- Components including datasets, flows, indexes, deployed model API endpoints (open and serverless).
- Connections created by you under 'project settings.'
- Azure Storage blob containers, and a fileshare for data upload within your project. Access storage using the following connections:
   
   | Data connection | Storage location | Purpose |
   | --- | --- | --- |
   | workspaceblobstore | {project-GUID}-azureml-blobstore | Default container for data uploads |
   | workspaceartifactstore | {project-GUID}-azureml | Stores components and metadata for your project such as model weights |
   | workspacefilestore | {project-GUID}-code | Hosts files created on your compute and using prompt flow |

> [!NOTE]
> Storage connections aren't created directly with the project when your storage account has public network access set to disabled. These are created instead when a first user accesses Azure AI Foundry over a private network connection. [Troubleshoot storage connections](troubleshoot-secure-connection-project.md#troubleshoot-configurations-on-connecting-to-storage)

## Related content

- [Deploy an enterprise chat web app](../tutorials/deploy-chat-web-app.md)

- [Learn more about Azure AI Foundry](../what-is-azure-ai-foundry.md)

- [Learn more about hubs](../concepts/ai-resources.md)

::: zone-end

::: zone pivot="fdp-project"

[!INCLUDE [create-project-fdp](../includes/create-project-fdp.md)]

::: zone-end