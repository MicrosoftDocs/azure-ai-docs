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
ai-usage: ai-assisted
---

# Create a hub project for Microsoft Foundry

[!INCLUDE [uses-hub-only](../includes/uses-hub-only.md)]

> [!TIP]
> An alternate Foundry project creation article is available: [Create a project for Microsoft Foundry (Foundry projects)](create-projects.md).

This article describes how to create a hub-based project in Foundry. Use a hub project when you need prompt flow, managed compute, Azure Machine Learning compatibility, or advanced development features.

See [Types of projects](../what-is-azure-ai-foundry.md#types-of-projects) for more information on the different project types.

## Prerequisites

Choose a method:

# [Foundry portal](#tab/portal)

- Azure subscription.

# [Python SDK](#tab/python)

- Azure subscription.
- Azure Machine Learning SDK v2.
- Existing hub resource (see create hub article).
- Azure CLI installed and authenticated (`az login`).

# [Azure CLI](#tab/cli)

- Azure subscription.
- Azure CLI with ML extension installed.
- Existing hub resource.

---

## Create a hub project

# [Foundry portal](#tab/portal)

[!INCLUDE [Create Foundry project](../includes/create-hub-project.md)]

# [Python SDK](#tab/python)

```python
from azure.ai.ml.entities import Project

my_project_name = "myexampleproject"
my_display_name = "My Example Project"
hub_name = "myhubname"  # Hub resource name
hub_id = f"/subscriptions/{subscription_id}/resourceGroups/{resource_group}/providers/Microsoft.MachineLearningServices/workspaces/{hub_name}"

my_project = Project(
    name=my_project_name,
    display_name=my_display_name,
    hub_id=hub_id
)

created_project = ml_client.workspaces.begin_create(workspace=my_project).result()
```

# [Azure CLI](#tab/cli)

```azurecli
az ml workspace create --kind project --hub-id {my_hub_ID} --resource-group {my_resource_group} --name {my_project_name}
```
`my_hub_ID` syntax: `/subscriptions/{subscription_id}/resourceGroups/{resource_group}/providers/Microsoft.MachineLearningServices/workspaces/{hub_name}`

---

## View project settings

# [Foundry portal](#tab/portal)

Open project Overview to see name, subscription, resource group. Use Management center for shared assets or Manage in Azure portal for underlying resource.

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

Project-scoped:
- Components (datasets, flows, indexes, deployments)
- Project connections
- Storage containers & file share:
  - workspaceblobstore – default data uploads
  - workspaceartifactstore – components & metadata
  - workspacefilestore – files from compute & prompt flow

> [!NOTE]
> Storage connections may delay creation when storage public access is disabled until first private network access.

## Delete projects

1. Open hub in portal.
2. Management center > Overview.
3. Select projects to remove.
4. Delete project.

Delete hub (with all projects): In Hub properties, select Delete hub to open Azure portal hub deletion.

## Related content

- [Create a Foundry project](create-projects.md).
- [Quickstart: Get started with Foundry (Hub projects)](../quickstarts/hub-get-started-code.md).
- [Learn more about Foundry](../what-is-azure-ai-foundry.md).
