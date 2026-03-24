---
title: "Create a project (classic)"
description: "This article describes how to create a Microsoft Foundry project so you can work with generative AI in the cloud. (classic)"
author: sdgilley
ms.author: sgilley
ms.reviewer: deeikele
ms.date: 03/24/2026
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
ROBOTS: NOINDEX, NOFOLLOW
---

# Create a project for Microsoft Foundry (classic)

Use this article to create a Foundry project and confirm that your environment is ready before you start building agents, evaluations, and files.

**Currently viewing:** :::image type="icon" source="../../foundry/media/yes-icon.svg" border="false"::: **Foundry (classic) portal version** - [Switch to version for the new Foundry portal](../../foundry/how-to/create-projects.md)

This article describes how to create a Foundry project in [Microsoft Foundry](https://ai.azure.com/?cid=learnDocs). Projects let you organize your work—such as agents, evaluations, and files—as you build stateful apps and explore new ideas.

* [!INCLUDE [fdp-description](../includes/fdp-description.md)]

* If you need access to open-source models or PromptFlow, [create a hub project type](../how-to/hub-create-projects.md) instead.

* For more information about the different project types, see [Types of projects](../what-is-foundry.md#types-of-projects).

If your organization requires customized Azure configurations like alternative names, security controls, or cost tags, you might need to use the [Azure portal](https://portal.azure.com) or [template options](create-resource-template.md) to comply with your organization's Azure Policy requirements.

## Prerequisites

* [!INCLUDE [azure-subscription](../../foundry/includes/azure-subscription.md)]

* [!INCLUDE [rbac-create](../../foundry/includes/rbac-create.md)]

    If you lack this role, request your subscription administrator to [create a Foundry resource](../../ai-services/multi-service-resource.md) and then skip to [Create multiple projects on the same resource](#create-multiple-projects-on-the-same-resource).

Use the following tabs to select the method you want to use to create a Foundry project:

# [Foundry portal](#tab/foundry)

- No other prerequisites necessary when using the portal.

# [Python SDK](#tab/python)

[!INCLUDE [create-projects-prereq-python](../../foundry/includes/create-projects-prereq-python.md)]

- (Optional) If you're working in the [Azure Government - US](/azure/azure-government/documentation-government-welcome) or [Azure operated by 21Vianet](https://azure.microsoft.com/global-infrastructure/services/?regions=china-east-2%2cchina-non-regional&products=all) regions, specify the region you want to authenticate to. This example authenticates to the Azure Government - US region:

```python
from azure.identity import AzureAuthorityHosts
DefaultAzureCredential(authority=AzureAuthorityHosts.AZURE_GOVERNMENT)
```

# [Azure CLI](#tab/azurecli)

[!INCLUDE [create-projects-prereq-cli](../../foundry/includes/create-projects-prereq-cli.md)]

---

## Create a Foundry project

Use one of the following methods.


# [Foundry portal](#tab/foundry)

These steps provide a way to create a new Azure resource with basic, default settings. 

To create a Foundry project, follow these steps:

1. [!INCLUDE [version-sign-in](../includes/version-sign-in.md)]

1. [!INCLUDE [create-project-access](../includes/create-project-access.md)]

1. Select **Foundry resource**, and then select **Next**.
1. Provide a name for your project and select **Create**. Or see the next section for advanced options.

### Advanced options

[!INCLUDE [create-projects-advanced-options](../../foundry/includes/create-projects-advanced-options.md)]

# [Python SDK](#tab/python)

[!INCLUDE [create-projects-create-python](../../foundry/includes/create-projects-create-python.md)]

# [Azure CLI](#tab/azurecli)

[!INCLUDE [create-project-CLI](../../foundry/includes/create-project-cli.md)]

---

## Create multiple projects on the same resource

[!INCLUDE [create-second-fdp-project](../includes/create-second-fdp-project.md)]

## View project settings

# [Foundry portal](#tab/foundry)

On the **Home** project page, you find information about the project.

- **Name**: The name of the project appears in the upper left corner. 
- **Subscription**: The subscription that hosts the hub that hosts the project.
- **Resource group**: The resource group that hosts the hub that hosts the project.

# [Python SDK](#tab/python)

[!INCLUDE [create-projects-view-python](../../foundry/includes/create-projects-view-python.md)]

# [Azure CLI](#tab/azurecli)

[!INCLUDE [create-projects-view-cli](../../foundry/includes/create-projects-view-cli.md)]

---

## Delete projects

# [Foundry portal](#tab/foundry)

1. [!INCLUDE [version-sign-in](../includes/version-sign-in.md)]
1. Open your project.
1. Select **Management center**.
1. Under **Resource**, select **Overview**.
1. Select any projects you no longer want to keep.
1. Select **Delete project**.

To delete the Foundry resource and all its projects:

1. In the Management center, select the resource name from the Overview section to go to the Azure portal.
1. In the Azure portal, select **Delete** to delete the resource and all its associated projects.

# [Python SDK](#tab/python)

[!INCLUDE [create-projects-delete-python](../../foundry/includes/create-projects-delete-python.md)]

# [Azure CLI](#tab/azurecli)

[!INCLUDE [create-projects-delete-cli](../../foundry/includes/create-projects-delete-cli.md)]

---

> [!IMPORTANT]
> Use with caution. You can't recover a project after it's deleted.

> [!div class="nextstepaction"]
> [Create your first connection](connections-add.md)

## Related content

- [Microsoft Foundry Quickstart](../quickstarts/get-started-code.md)
- [What is Foundry?](../what-is-foundry.md)
- [Create resources using Bicep template](create-resource-template.md)

