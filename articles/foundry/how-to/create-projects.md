---
title: "Create a project"
description: "This article describes how to create a Microsoft Foundry project so you can work with generative AI in the cloud."
author: sdgilley
ms.author: sgilley
ms.reviewer: deeikele
ms.date: 01/09/2026
ms.service: azure-ai-foundry
ms.topic: how-to
ms.custom:
  - classic-and-new
  - ignite-2023
  - build-2024
  - ignite-2024
  - build-aifnd
  - build-2025
  - dev-focus
ai-usage: ai-assisted
# customer intent: As a developer, I want to create a Microsoft Foundry project so I can work with generative AI.
---

# Create a project for Microsoft Foundry
This article describes how to create a Foundry project in [Microsoft Foundry](https://ai.azure.com/?cid=learnDocs). Projects let you organize your work—such as agents, evaluations, and files—as you build stateful apps and explore new ideas.

If your organization requires customized Azure configurations like alternative names, security controls, or cost tags, you might need to use the [Azure portal](https://portal.azure.com) or [template options](create-resource-template.md) to comply with your organization's Azure Policy requirements.

## Prerequisites

* [!INCLUDE [azure-subscription](../includes/azure-subscription.md)]

* [!INCLUDE [rbac-create](../includes/rbac-create.md)]

* Use the following tabs to select the method you want to use to create a Foundry project:

    # [Foundry portal](#tab/foundry)
    
    - [!INCLUDE [azure-subscription](../includes/azure-subscription.md)]
    
    # [Python SDK](#tab/python)
    
    - [Set up your development environment](develop/install-cli-sdk.md?tabs=python)
    - Run `az login` or `az login --use-device-code` in your environment before running code.
    - **Quick validation**: Before creating a project, verify your SDK and authentication are working by testing the client:
    
      ```python
      from azure.identity import DefaultAzureCredential
      from azure.mgmt.cognitiveservices import CognitiveServicesManagementClient
      
      # Test authentication by instantiating the client
      credential = DefaultAzureCredential()
      subscription_id = "<your-subscription-id>"  # Replace with your subscription ID
      client = CognitiveServicesManagementClient(credential, subscription_id)
      print("✓ Authentication successful! Ready to create a project.")
      ```
    
    
    - Complete these steps to start your Python script:
        1. Install packages: `pip install azure-identity azure-mgmt-cognitiveservices~=13.7.0b1`. If you're in a notebook cell, use `%pip install` instead.
        1. Use `pip show azure-mgmt-cognitiveservices` to check that your version is 13.7 or greater.
        1. Start your script with the following code to create the `client` connection and variables used throughout this article. This example creates the project in East US:
        
            :::code language="python" source="~/foundry-samples-main/samples-classic/python/quickstart/create_project.py" id="create_client":::
    
        1. (Optional) If you have multiple accounts, add the tenant ID of the Microsoft Entra ID you want to use into the `DefaultAzureCredential`.
                
            ```python
            DefaultAzureCredential(interactive_browser_tenant_id="<TENANT_ID>")
            ```    
    
    # [Azure CLI](#tab/azurecli)
    
    - Install the [Azure CLI](/cli/azure/install-azure-cli). 
    - Set default values for `subscription`.
    
      ```azurecli
        # Set your default subscription
        az account set --subscription "{subscription-name}"
       ```
    
    ---

## Create a Foundry project

# [Foundry portal](#tab/foundry)

These steps provide a way to create a new Azure resource with basic, defaulted, settings. 

To create a Foundry project, follow these steps:

1. [!INCLUDE [version-sign-in](../includes/version-sign-in.md)]

1. The project you're working on appears in the upper-left corner.
1. To create a new project, select the project name, and then select **Create new project**.
1. Give your project a name and select **Create project**. Or see next section for advanced options.

### Advanced options

1. You create a Foundry project on a `Foundry` resource. The portal automatically creates this resource when you create the project. Select an existing **Resource group** to use, or leave the default to create a new resource group.

    > [!TIP]
    > Especially for getting started, create a new resource group for your project. The resource group makes it easy to manage the project and all its resources together.

1. Select a **Location** or use the default. The location is the region where the project resources are hosted. 

1. Select **Create**. You see the progress of resource creation. The project is created when the process is complete.

# [Python SDK](#tab/python)

To create a Foundry project:

- Add the following code to create a Foundry project by using the variables and `client` connection from the [Prerequisites](#prerequisites).

    :::code language="python" source="~/foundry-samples-main/samples-classic/python/quickstart/create_project.py" id="create_resource_project":::

    References: [CognitiveServicesManagementClient](/python/api/azure-mgmt-cognitiveservices/azure.mgmt.cognitiveservices.CognitiveServicesManagementClient).

# [Azure CLI](#tab/azurecli)

[!INCLUDE [create-project-cli](../includes/create-project-cli.md)]

---

## Create multiple projects on the same resource

[!INCLUDE [create-second-fdp-project](../includes/create-second-fdp-project.md)]

## View project settings

# [Foundry portal](#tab/foundry)

On the **Home** project page, you see the project endpoint and API key for the project. You don't need the API key if you use Microsoft Entra ID authentication.

# [Python SDK](#tab/python)

:::code language="python" source="~/foundry-samples-main/samples-classic/python/quickstart/create_project.py" id="show_project":::

References: [CognitiveServicesManagementClient](/python/api/azure-mgmt-cognitiveservices/azure.mgmt.cognitiveservices.CognitiveServicesManagementClient).

# [Azure CLI](#tab/azurecli)

To view settings for the project, use the `az cognitiveservices account connection show` command. For example:

```azurecli
az cognitiveservices account connection show \
--name my-foundry-project \
--resource-group my-foundry-rg
```

---

## Delete projects

# [Foundry portal](#tab/foundry)

1. [!INCLUDE [version-sign-in](../includes/version-sign-in.md)] 
1. In the upper-right navigation, select **Operate**.
1. In the left pane, select **Admin**.
1. Select your project.
1. In the upper right, select the trash can icon to delete the project.

# [Python SDK](#tab/python)

This code uses the variables and `client connection` from the Prerequisites. First, create the client connection:

```python
client.projects.begin_delete(
    resource_group_name, foundry_resource_name, foundry_project_name
)
```

References: [CognitiveServicesManagementClient](/python/api/azure-mgmt-cognitiveservices/azure.mgmt.cognitiveservices.CognitiveServicesManagementClient).

Delete a Foundry resource and all of its projects:

```python
# Delete projects
projects = client.projects.list(resource_group_name, foundry_resource_name)

for project in projects: 
    print("Deleting project:", project.name)
    client.projects.begin_delete(resource_group_name, foundry_resource_name,
        project_name=project.name.split('/')[-1]
    ).wait()

# Delete resource
print("Deleting resource:", foundry_resource_name)
client.accounts.begin_delete(resource_group_name, foundry_resource_name).wait()
```

References: [CognitiveServicesManagementClient](/python/api/azure-mgmt-cognitiveservices/azure.mgmt.cognitiveservices.CognitiveServicesManagementClient).

# [Azure CLI](#tab/azurecli)

Run the following command:

```azurecli
az cognitiveservices account project delete \
--name my-foundry-rg \
--project-name my-foundry-project
```

References: [az cognitiveservices account project delete](/cli/azure/cognitiveservices/account/project#az-cognitiveservices-account-project-delete).

---

> [!IMPORTANT]
> Use with caution. You can't recover a project after it's deleted.

## Related content

- [Microsoft Foundry Quickstart](../quickstarts/get-started-code.md)
- [What is Foundry?](../what-is-foundry.md)

