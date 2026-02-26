---
title: Create a hub project
titleSuffix: Microsoft Foundry
description: Learn how to create a hub-based project in Microsoft Foundry.
author: sdgilley
ms.author: sgilley
ms.reviewer: deeikele
ms.date: 12/29/2025
ms.service: azure-ai-foundry
ms.topic: how-to
ms.custom:
  - build-2025
  - hub-only
  - dev-focus
ai-usage: ai-assisted
---

# Create a hub project for Microsoft Foundry

[!INCLUDE [uses-hub-only](../includes/uses-hub-only.md)]

> [!TIP]
> An alternate Foundry project creation article is available: [Create a project for Microsoft Foundry (Foundry projects)](create-projects.md).

This article describes how to create a hub-based project in Foundry. Use a hub project when you need prompt flow, managed compute, Azure Machine Learning compatibility, or advanced development features.

For more information on the different project types, see [Types of projects](../what-is-foundry.md#types-of-projects).

## Prerequisites

Choose a method:

# [Foundry portal](#tab/portal)

- Azure subscription.
- Required role: **Owner** or **Contributor** on the hub resource.

# [Python SDK](#tab/python)

- Azure subscription.
- Required role: **Owner** or **Contributor** on the hub resource.
- Azure Machine Learning SDK v2.
- Existing hub resource (see create hub article).
- Azure CLI installed and authenticated (`az login`).

# [Azure CLI](#tab/cli)

- Azure subscription.
- Required role: **Owner** or **Contributor** on the hub resource.
- Azure CLI and machine learning extension installed. Follow the steps in the [Install and set up the machine learning extension](/azure/machine-learning/how-to-configure-cli) article to install.
- Existing hub resource.

---


## Set up your environment

# [Foundry portal](#tab/portal)

No additional setup is necessary if you're using the Foundry portal.

# [Python SDK](#tab/python)

[!INCLUDE [SDK setup](../includes/development-environment-config.md)]

Verify your authentication by listing existing hubs:

```python
hubs = ml_client.workspaces.list()
for hub in hubs:
    print(f"Hub: {hub.name}")
```

If you receive an authentication error, ensure your Azure credentials are configured (run `az login` or set up your credentials via the Azure Identity SDK). If you receive a permission error, check that you have the Contributor role on the subscription or resource group.


# [Azure CLI](#tab/cli)

1. To authenticate to your Azure subscription from the Azure CLI, use the following command:

    ```azurecli
    az login
    ```

    For more information on authenticating, see [Authentication methods](/cli/azure/authenticate-azure-cli).

1. Verify your authentication by listing existing hubs:

    ```azurecli
    az ml workspace list --resource-group <your-resource-group-name>
    ```

    If the command succeeds and displays any existing hubs, your authentication is correct.

---

## Create a hub project

# [Foundry portal](#tab/portal)

[!INCLUDE [Create Foundry project](../includes/create-hub-project.md)]

# [Python SDK](#tab/python)

```python
from azure.ai.ml.entities import Project


my_project_name = "myexampleproject"  # Project names must be lowercase, 3–64 chars, alphanumeric with hyphens
my_display_name = "My Example Project"
hub_name = "myhubname"  # Hub resource name
hub_id = f"/subscriptions/{subscription_id}/resourceGroups/{resource_group}/providers/Microsoft.MachineLearningServices/workspaces/{hub_name}"

my_project = Project(
    name=my_project_name,
    display_name=my_display_name,
    hub_id=hub_id
)

created_project = ml_client.workspaces.begin_create(workspace=my_project).result()
print(f"Project '{created_project.name}' created successfully.")
```

**What this snippet does:** Defines project properties and creates the project on the existing hub. The `.result()` method waits for the creation to complete. Expected output: A confirmation message displaying the created project name.

**References:**
- [Project entity](/python/api/azure-ai-ml/azure.ai.ml.entities.project)
- [MLClient.workspaces](/python/api/azure-ai-ml/azure.ai.ml.mlclient#workspaces)
- [Azure Identity DefaultAzureCredential](/python/api/azure-identity/azure.identity.defaultazurecredential)

# [Azure CLI](#tab/cli)

```azurecli
az ml workspace create --kind project --hub-id <my-hub-id> --resource-group <my-resource-group> --name <my-project-name>
```

Replace the placeholders as follows:
- `<my-hub-id>`: Full resource ID of the hub in format `/subscriptions/{subscription_id}/resourceGroups/{resource_group}/providers/Microsoft.MachineLearningServices/workspaces/{hub_name}`
- `<my-resource-group>`: Name of the resource group containing your hub
- `<my-project-name>`: Name for the new project (lowercase, 3–64 characters, alphanumeric with hyphens)

**What this command does:** Creates a new hub-based project associated with the specified hub.

**References:**
- [az ml workspace create](/cli/azure/ml/workspace#az-ml-workspace-create)

---

## View project settings

# [Foundry portal](#tab/portal)

Open project **Overview** to see the name, subscription, and resource group. Use **Management center** for shared assets or **Manage in Azure portal** for the underlying resource.

# [Python SDK](#tab/python)

```python
ml_client = MLClient(workspace_name=my_project_name, resource_group_name=resource_group, subscription_id=subscription_id, credential=DefaultAzureCredential())
```

# [Azure CLI](#tab/cli)

```azurecli
az ml workspace show --name {my_project_name} --resource-group {my_resource_group}
```
---

## Project resources

Shared from hub: connections, compute, network configuration.

Project-scoped resources:
- Components (datasets, flows, indexes, deployments)
- Project connections
- Storage containers and file share:
  - workspaceblobstore – default data uploads
  - workspaceartifactstore – components and metadata
  - workspacefilestore – files from compute and prompt flow

> [!NOTE]
> If you disable storage public access, storage connections might delay creation until the first private network access.

## Delete projects

1. Open the hub in the portal.
1. Go to Management center > Overview.
1. Select the projects to remove.
1. Select **Delete project**.

To delete a hub and all its projects, select **Delete hub** in **Hub properties** to open Azure portal hub deletion.

## Related content

- [Create a Foundry project](create-projects.md).
- [Quickstart: Get started with Foundry (Hub projects)](../quickstarts/hub-get-started-code.md).
- [Learn more about Foundry](../what-is-foundry.md).
