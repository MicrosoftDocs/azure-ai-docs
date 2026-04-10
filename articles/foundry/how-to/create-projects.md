---
title: "Create a project"
description: "This article describes how to create a Microsoft Foundry project so you can work with generative AI in the cloud."
author: sdgilley
ms.author: sgilley
ms.reviewer: deeikele
ms.date: 04/08/2026
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
  - doc-kit-assisted
ai-usage: ai-assisted
# customer intent: As a developer, I want to create a Microsoft Foundry project so I can work with generative AI.
---

# Create a project for Microsoft Foundry

Use this article to create a Foundry project and confirm that your environment is ready before you start building agents, evaluations, and files.

This article describes how to create a Foundry project in [Microsoft Foundry](https://ai.azure.com/?cid=learnDocs). Projects let you organize your work—such as agents, evaluations, and files—as you build stateful apps and explore new ideas.

If your organization requires customized Azure configurations like alternative names, security controls, or cost tags, you might need to use the [Azure portal](https://portal.azure.com) or [template options](create-resource-template.md) to comply with your organization's Azure Policy requirements.

## Prerequisites

* [!INCLUDE [azure-subscription](../includes/azure-subscription.md)]

* [!INCLUDE [rbac-create](../includes/rbac-create.md)]

Use the following tabs to select the method you want to use to create a Foundry project:

# [Foundry portal](#tab/foundry)

- No other prerequisites necessary when using the portal.

# [Python SDK](#tab/python)

[!INCLUDE [create-projects-prereq-python](../includes/create-projects-prereq-python.md)]

# [Azure CLI](#tab/azurecli)

[!INCLUDE [create-projects-prereq-cli](../includes/create-projects-prereq-cli.md)]

---

## Create a Foundry project

Use one of the following methods.


# [Foundry portal](#tab/foundry)

These steps provide a way to create a new Azure resource with basic default settings. 

To create a Foundry project, follow these steps:

1. [!INCLUDE [version-sign-in](../includes/version-sign-in.md)]

1. The project you're working on appears in the upper-left corner.
1. To create a new project, select the project name, and then select **Create new project**.
1. Give your project a name and select **Create project**. Or see the next section for advanced options.

### Advanced options

[!INCLUDE [create-projects-advanced-options](../includes/create-projects-advanced-options.md)]

# [Python SDK](#tab/python)

[!INCLUDE [create-projects-create-python](../includes/create-projects-create-python.md)]

# [Azure CLI](#tab/azurecli)

[!INCLUDE [create-project-CLI](../includes/create-project-cli.md)]

---

## Create multiple projects on the same resource

[!INCLUDE [create-second-fdp-project](../includes/create-second-fdp-project.md)]

## View project settings

# [Foundry portal](#tab/foundry)

On the **Home** project page, you see the project endpoint and API key for the project. You don't need the API key if you use Microsoft Entra ID authentication.

# [Python SDK](#tab/python)

[!INCLUDE [create-projects-view-python](../includes/create-projects-view-python.md)]

# [Azure CLI](#tab/azurecli)

[!INCLUDE [create-projects-view-cli](../includes/create-projects-view-cli.md)]

---

## Delete projects

# [Foundry portal](#tab/foundry)

1. [!INCLUDE [version-sign-in](../includes/version-sign-in.md)]
1. In the upper-right navigation, select **Operate**.
1. In the left pane, select **Admin**.
1. Select your project.
1. In the upper right, select the trash can icon to delete the project.

# [Python SDK](#tab/python)

[!INCLUDE [create-projects-delete-python](../includes/create-projects-delete-python.md)]

# [Azure CLI](#tab/azurecli)

[!INCLUDE [create-projects-delete-cli](../includes/create-projects-delete-cli.md)]

---

> [!IMPORTANT]
> Use with caution. You can't recover a project after it's deleted.

> [!div class="nextstepaction"]
> [Create your first connection](connections-add.md)

## Related content

- [Microsoft Foundry Quickstart](../quickstarts/get-started-code.md)
- [What is Foundry?](../what-is-foundry.md)
- [Create resources using Bicep template](create-resource-template.md)

