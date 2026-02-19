---
title: "Quickstart: Set up Microsoft Foundry resources"
titleSuffix: Microsoft Foundry
description: Learn how to create a Microsoft Foundry project, deploy a model, and grant access to team members so they can build AI applications.
ms.service: azure-ai-foundry
ms.custom:
  - build-2025
  - dev-focus
  - devx-track-azurecli
ms.topic: quickstart
ms.date: 01/16/2026
ms.reviewer: sgilley
ms.author: sgilley
author: sdgilley
ai-usage: ai-assisted
# customer intent: As an admin or team lead, I want to create a Foundry project and deploy a model so my team members can use it to build AI applications.
---

# Quickstart: Set up Microsoft Foundry resources

In this quickstart, you create a [Microsoft Foundry](https://ai.azure.com) project and deploy a model. If you're managing a team, you also grant access to team members. After you complete these steps, you or your team can start building AI applications using the deployed model.

> [!TIP]
> This quickstart shows you how to create resources to build an agent with a basic setup. For more advanced scenarios that use your own resources, see [Set up your environment for agent development](../../agents/environment-setup.md).

## Prerequisites

- [!INCLUDE [azure-subscription](../../includes/azure-subscription.md)]
- If you're creating the project for yourself: 
    - [!INCLUDE [rbac-create](../../includes/rbac-create.md)]
- If you're creating the project for a team: 
    - [!INCLUDE [rbac-assign-roles](../../includes/rbac-assign-roles.md)]
    - A list of user email addresses or Microsoft Entra security group IDs for team members who need access.

Select your preferred method by using the following tabs:

# [Azure CLI](#tab/azurecli)

- Install the [Azure CLI](/cli/azure/install-azure-cli) version 2.67.0 or later (check with `az version`).
- Sign in to Azure:

  ```azurecli
  az login
  ```

# [Foundry portal](#tab/portal)

- Access to the [Microsoft Foundry portal](https://ai.azure.com).

---

## Create a project

Create a Foundry project to organize your work. The project contains models, agents, and other resources your team uses.

# [Azure CLI](#tab/azurecli)

[!INCLUDE [create-project-cli](../includes/create-project-cli.md)]

# [Foundry portal](#tab/portal)

1. Go to [Microsoft Foundry](https://ai.azure.com).
1. Sign in with your Azure account.
1. Select the project name in the upper-left corner, and then select **Create new project**.
1. Enter a project name, such as `my-foundry-project`.
1. Select **Advanced options** to configure the resource group and location:
   - **Resource group**: Create a new resource group or select an existing one. If you create a new resource group, you can more easily manage the project and all its resources together.
   - **Location**: Select the region closest to your team.
1. Select **Create project**.

   Wait for the project to be created. When the project overview page appears, your project is ready.

---

## Deploy a model

Deploy a model that you can use. This example uses **gpt-4.1-mini**, but you can choose any available model.

# [Azure CLI](#tab/azurecli)

```azurecli
az cognitiveservices account deployment create \
    --name my-foundry-resource \
    --resource-group my-foundry-rg \
    --deployment-name gpt-4.1-mini \
    --model-name gpt-4.1-mini \
    --model-version "2025-04-14" \
    --model-format OpenAI \
    --sku-capacity 10 \
    --sku-name Standard
```

Verify the deployment succeeded:

```azurecli
az cognitiveservices account deployment show \
    --name my-foundry-resource \
    --resource-group my-foundry-rg \
    --deployment-name gpt-4.1-mini
```

When the deployment is ready, the output shows `"provisioningState": "Succeeded"`.

Reference: [az cognitiveservices account deployment](/cli/azure/cognitiveservices/account/deployment)

# [Foundry portal](#tab/portal)

1. In your project, select **Discover** in the upper-right navigation.
1. Select **Models**.
1. Search for **gpt-4.1-mini**.
1. Select **Deploy** > **Default settings** to add it to your project.
1. Note the deployment name (for example, `gpt-4.1-mini`). Your team needs this name to use the model.

---

## Get your project connection details

You need your project endpoint to connect from code. If you're administering this project for others, send them this endpoint along with the deployment name.

1. Sign in to [Microsoft Foundry](https://ai.azure.com/?cid=learnDocs) by using your Azure account.
1. Select your project.
1. [!INCLUDE [find-endpoint](../includes/find-endpoint.md)]
1. Copy the endpoint value. You use this value in other quickstarts and tutorials.

## For administrators - grant access

If you're administering a team, assign the **Azure AI User** role to team members so they can use the project and deployed models. This role provides the minimum permissions needed to build and test AI applications.

# [Azure CLI](#tab/azurecli)

[!INCLUDE [add-users-cli](../includes/add-users-cli.md)] 

# [Foundry portal](#tab/portal)

[!INCLUDE [add-users](../includes/add-users.md)]

---

### Verify team member access

Ask a team member to verify their access by signing in to [Microsoft Foundry](https://ai.azure.com), selecting the project from the project list, and confirming the deployed model appears under **Build** > **Models**.

If the team member can't access the project, verify that the role assignment completed successfully. Check that you used the correct email address or security group ID. Make sure the team member's Azure account is in the same Microsoft Entra tenant.


## Clean up resources

When you no longer want this project, delete the resource group to delete all resources associated with it.

# [Azure CLI](#tab/azurecli)

```azurecli
az group delete --name my-foundry-rg --yes --no-wait
```

# [Foundry portal](#tab/portal)

In the [Azure portal](https://portal.azure.com), find and select your resource group. Select **Delete** and confirm to delete the resource group and all its associated resources.

---

## Next step
 
> [!div class="nextstepaction"]
> [Microsoft Foundry quickstart](../../quickstarts/get-started-code.md)


