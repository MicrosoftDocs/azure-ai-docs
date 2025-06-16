---
title: Include file
description: Include file
author: sdgilley
ms.author: sgilley
ms.reviewer: deeikele
ms.date: 05/05/2025
ms.service: azure-ai-foundry
ms.topic: include
ms.custom:
  - include
  - build-aifnd
  - build-2025
---

> [!TIP]
> The rest of this article shows how to create a **[!INCLUDE [fdp](../includes/fdp-project-name.md)]**.  Select **[!INCLUDE [hub](../includes/hub-project-name.md)]** at the top of this article if you want to create a [!INCLUDE [hub](../includes/hub-project-name.md)] instead.

* [!INCLUDE [fdp-description](../includes/fdp-description.md)]

* This project type gives you the best support for:

    * Agents 
    * AI Foundry API to work with agents and across models
    * Models sold directly by Azure - Azure OpenAI, DeepSeek, xAI, etc.
    * Partner & Community Models sold through Marketplace - Stability, Bria, Cohere, etc. 
    * Project files (directly upload files and start experimenting)
    * Evaluations
    * Fine-tuning
    * Playgrounds


## Prerequisites

Use the following tabs to select the method you plan to use to create a [!INCLUDE [fdp](../includes/fdp-project-name.md)]:

# [Azure AI Foundry portal](#tab/ai-foundry)

- An Azure subscription. If you don't have an Azure subscription, create a [free account](https://azure.microsoft.com/free/).
- You must be **Owner** of the subscription to have appropriate access control necessary to create the Azure AI Foundry resource that is the parent of the project.  If you don't have this access, have your administrator [create an AI Foundry resource](../../ai-services/multi-service-resource.md) for you to use.  Then skip to [Create multiple projects on the same resource](#create-multiple) to create your project.


# [Python SDK](#tab/python)

- An Azure subscription. If you don't have an Azure subscription, create a [free account](https://azure.microsoft.com/free/).
- You must be **Owner** of the subscription to receive the appropriate access control needed to use the project.
- [Set up your development environment](../how-to/develop/install-cli-sdk.md?tabs=python)
- Authenticate with `az login` or `az login --use-device-code` in your environment before running code.
- Complete these steps to start your Python script:
    1. Install packages: `pip install azure-identity azure-mgmt-cognitiveservices`. If in a notebook cell, use `%pip install azure-identity azure-mgmt-cognitiveservices`.
    1. Use `pip show azure-mgmt-cognitiveservices` to verify your version is 13.7 or greater.
    1. Start your script with the following code to create the `client` connection and variables used throughout this article.  This example creates the project in West US:
    
        ```python
        from azure.identity import DefaultAzureCredential
        from azure.mgmt.cognitiveservices import CognitiveServicesManagementClient
        
        sub_id = 'your-sub'
        rgp = 'your-resource-group'
        resource_name = 'your-resource'
        project_name = 'your-project'
        location = 'westus'
        
        client = CognitiveServicesManagementClient(
            credential=DefaultAzureCredential(), 
            subscription_id=sub_id,
            api_version="2025-04-01-preview"
        )


# [Azure CLI](#tab/azurecli)

- An Azure subscription. If you don't have an Azure subscription, create a [free account](https://azure.microsoft.com/free/).
- You must be **Owner** of the subscription to receive the appropriate access control needed to use the project.
- [Azure CLI](/cli/azure/install-azure-cli) 

---

## Create a [!INCLUDE [fdp-project-name](fdp-project-name.md)]

# [Azure AI Foundry portal](#tab/ai-foundry)

These steps provide a way to create a new Azure resource with basic, defaulted, settings. 

> [!TIP]
> If your organization requires customized Azure configurations like alternative names, security controls or cost tags, use one of these methods instead to comply with your organization's Azure Policy compliance:
> * [Create your first AI Foundry resource](../../ai-services/multi-service-resource.md) 
> * [Create an Azure AI Foundry resource using a Bicep file](../how-to/create-resource-template.md) 

To create a [!INCLUDE [fdp-project-name](fdp-project-name.md)] in [Azure AI Foundry](https://ai.azure.com/?cid=learnDocs), follow these steps:

1. Sign in to [Azure AI Foundry](https://ai.azure.com/?cid=learnDocs).

1. [!INCLUDE [create-project-access](create-project-access.md)]

1. Select **Azure AI Foundry resource**, then select **Next**.
1. Provide a name for your project and select **Create**.  Or see next section for advanced options.

### Advanced options

A [!INCLUDE [fdp-project-name](fdp-project-name.md)] is created on an `AI Foundry` resource. This resource is created for you automatically when you create the project. 

To customize the settings for your project, follow these steps:

1. In the **Create a project** form, select **Advanced options**.

1. Select an existing **Resource group** you want to use, or leave the default to create a new resource group.

    > [!TIP]
    > Especially for getting started we recommend you create a new resource group for your project. The resource group allows you to easily manage the project and all of its resources together. 

1. Select a **Location** or use the default. The location is the region where the hub is hosted. Azure AI services availability differs per region. For example, certain models might not be available in certain regions.

1. Select **Create**. You see progress of resource creation and the project is created when the process is complete.

# [Python SDK](#tab/python)

To create a [!INCLUDE [fdp](../includes/fdp-project-name.md)]:


1. Add this code to create a [!INCLUDE [fdp-project-name](../includes/fdp-project-name.md)], using the variables and `client` connection from the [Prerequisites](#prerequisites).

    ```python

    # Create resource
    resource = client.accounts.begin_create(
        resource_group_name=rgp,
        account_name=resource_name,
        account={
            "location": location,
            "kind": "AIServices",
            "sku": {"name": "S0",},
            "identity": {"type": "SystemAssigned"},
            "properties": {"allowProjectManagement": True}
        }
    )
    # Create default project
    project = client.projects.begin_create(
        resource_group_name=rgp,
        account_name=resource_name,
        project_name=project_name,
        project={
            "location": location,
            "identity": {"type": "SystemAssigned"},
            "properties": {}
        }
    )
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


# [Azure CLI](#tab/azurecli)

<!-- To create a [!INCLUDE [fdp](../includes/fdp-project-name.md)]:

1. Authenticate to your Azure subscription from the Azure CLI with the following command:

    ```azurecli
    az login
    ```

    For more information on authenticating, see [Authentication methods](/cli/azure/authenticate-azure-cli).

1. Create a resource group, for example in East US:

    ```azurecli
    az group create --name {my_resource_group} --location eastus
    ```

1. Now use the following commands to create a new [!INCLUDE [fdp](../includes/fdp-project-name.md)]:

    [!INCLUDE [cli-create-project](cli-create-project.md)]
 -->

CLI commands not currently available for creating a [!INCLUDE [fdp-project-name](fdp-project-name.md)].

---

## <a name="create-multiple"></a> Create multiple projects on the same resource

[!INCLUDE [create-second-fdp-project](create-second-fdp-project.md)]

## View project settings

# [Azure AI Foundry portal](#tab/ai-foundry)

On the project **Home** page, you can find information about the project.

- Name: The name of the project appears in the top left corner. 
- Subscription: The subscription that hosts the hub that hosts the project.
- Resource group: The resource group that hosts the hub that hosts the project.


# [Python SDK](#tab/python)

```python
    # Get project
    project = client.projects.get(
        resource_group_name=rgp,
        account_name=account_name,
        project_name=project_name
    )
    print(project)
```

# [Azure CLI](#tab/azurecli)

To view settings for the project, use the `az cognitiveservices account connection show` command. For example:

```azurecli
az cognitiveservices account connection show --name {my_project_name} --resource-group {my_resource_group}
```

---

## Related content

- [Quickstart: Get started with Azure AI Foundry](../quickstarts/get-started-code.md?pivots=fdp-project)
- [Learn more about Azure AI Foundry](../what-is-azure-ai-foundry.md)
