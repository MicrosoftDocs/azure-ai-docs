---
title: "Quickstart: Set up Microsoft Foundry resources"
description: "Learn how to create a Microsoft Foundry project, deploy a model, and grant access to team members so they can build AI applications."
ms.service: microsoft-foundry
ms.subservice: foundry-platform
ms.custom:
  - build-2025
  - dev-focus
  - devx-track-azurecli
  - doc-kit-assisted
ms.topic: quickstart
ms.date: 08/25/2026
ms.reviewer: sgilley
ms.author: sgilley
author: sdgilley
ai-usage: ai-assisted
# customer intent: As an admin or team lead, I want to create a Foundry project and deploy a model so my team members can use it to build AI applications.
---

# Quickstart: Set up Microsoft Foundry resources
In this quickstart, you create a [Microsoft Foundry](https://ai.azure.com) project and deploy a model. If you're managing a team, you also grant access to team members. After you complete these steps, you or your team can start building AI applications using the deployed model.

> [!TIP]
> This quickstart shows you how to create resources to build an agent with a basic setup. For more advanced scenarios that use your own resources, see [Set up your environment for agent development](../agents/environment-setup.md).

## Prerequisites

- [!INCLUDE [azure-subscription](../includes/azure-subscription.md)]
- If you're creating the project for yourself: 
    - [!INCLUDE [rbac-create](../includes/rbac-create.md)]
- If you're creating the project for a team: 
    - [!INCLUDE [rbac-assign-roles](../includes/rbac-assign-roles.md)]
    - A list of user email addresses or Microsoft Entra security group IDs for team members who need access.

If you use the Azure CLI instead of the portal, the **Contributor** or **Owner** role on the resource group is enough to create the resource and project. You still need a role that can assign roles, such as **Owner**, to grant access to team members.

Select your preferred method by using the following tabs:

# [Azure CLI](#tab/azurecli)

- Install the [Azure CLI](/cli/azure/install-azure-cli) version 2.80.0 or later. Check your version with `az version`, and run `az upgrade` if you need a newer one.

  Version 2.80.0 added the `az cognitiveservices account project` commands that these steps use. On an earlier version, the commands fail with `unrecognized arguments` or `'project' is misspelled or not recognized by the system`.

- Sign in to Azure:

  ```azurecli
  az login
  ```

# [Foundry portal](#tab/portal)

- Access to the [Microsoft Foundry portal](https://ai.azure.com).

---

## Create a project

Create a Foundry project to organize your work. The project contains models, agents, and other resources your team uses.

> [!TIP]
> Create your project in the **West US 3** region if you want to try an [instant model (preview)](../concepts/instant-models.md).

# [Azure CLI](#tab/azurecli)

[!INCLUDE [create-project-cli](../includes/create-project-cli.md)]

# [Foundry portal](#tab/portal)

1. [!INCLUDE [foundry-sign-in](../includes/foundry-sign-in.md)]
1. Create a project.
    * If this is your first use of Foundry, you'll be asked to create or search for a project to continue. Select **Create a new project** in the dropdown.
        :::image type="content" source="../media/quickstart-create-foundry-resources/initial-foundry.png" alt-text="Screenshot of the Foundry portal showing the project selection dropdown with the Create new project option highlighted.":::
    * If you already have a project loaded, select its name in the upper-left corner, and then select **Create new project**.
        :::image type="content" source="../media/quickstart-create-foundry-resources/create-from-project.png" alt-text="Screenshot of Foundry portal showing the Create a new project dropdown selected and project creation form fields visible.":::
1. Enter a project name, such as `my-foundry-project`.
1. Select **Advanced options** to configure the resource group and location:
   - **Resource group**: Create a new resource group or select an existing one. If you create a new resource group, you can more easily manage the project and all its resources together.
   - **Location**: Select the region closest to your team.
1. Select **Create project**.

   Wait for the project to be created. When the project overview page appears, your project is ready.

---

## Deploy a model

Deploy a model that you can use. This example uses **gpt-5-mini**, but you can choose any available model.

> [!TIP]
> To try an [instant access model (preview)](../concepts/instant-models.md), you can skip this step.

# [Azure CLI](#tab/azurecli)

1. List the models available in your region so you can confirm the model name and version:

   ```azurecli
   az cognitiveservices model list \
       --location eastus \
       --query "[?model.name=='gpt-5-mini'].{version:model.version,skus:join(',',model.skus[].name)}" \
       --output table
   ```

1. Deploy the model:

   ```azurecli
   az cognitiveservices account deployment create \
       --name my-foundry-resource \
       --resource-group my-foundry-rg \
       --deployment-name gpt-5-mini \
       --model-name gpt-5-mini \
       --model-version "2025-08-07" \
       --model-format OpenAI \
       --sku-capacity 10 \
       --sku-name GlobalStandard
   ```

   If the command fails with `DeploymentModelNotSupported`, the model, version, or SKU isn't available in your region. Use the output of the previous step to choose a supported combination.

1. Verify the deployment succeeded:

   ```azurecli
   az cognitiveservices account deployment show \
       --name my-foundry-resource \
       --resource-group my-foundry-rg \
       --deployment-name gpt-5-mini \
       --query properties.provisioningState --output tsv
   ```

   The output shows `Succeeded` when the deployment is ready.

Reference: [az cognitiveservices account deployment](/cli/azure/cognitiveservices/account/deployment)

# [Foundry portal](#tab/portal)

1. Select **Discover** in the upper-right navigation, then **Models** in the left pane.
1. Search for **gpt-5-mini**.
1. Select **Deploy** > **Default settings** to add it to your project.
1. Note the deployment name (for example, `gpt-5-mini`). Your team needs this name to use the model.

---

## Get your project connection details

You need your project endpoint to connect from code. If you're administering this project for others, send them this endpoint along with the deployment name.

# [Azure CLI](#tab/azurecli)

Get the project endpoint:

```azurecli
az cognitiveservices account project show \
    --name my-foundry-resource \
    --resource-group my-foundry-rg \
    --project-name my-foundry-project \
    --query 'properties.endpoints."AI Foundry API"' --output tsv
```

The output is your project endpoint, in the form `https://my-foundry-resource.services.ai.azure.com/api/projects/my-foundry-project`. Use this value in other quickstarts and tutorials.

# [Foundry portal](#tab/portal)

1. Sign in to [Microsoft Foundry](https://ai.azure.com/?cid=learnDocs) by using your Azure account.
1. Select your project.
1. [!INCLUDE [find-endpoint](../includes/find-endpoint.md)]
1. Copy the endpoint value. You use this value in other quickstarts and tutorials.

---

## For administrators - grant access

If you're administering a team, assign the **Foundry User** role to team members so they can use the project and deployed models. This role provides the minimum permissions needed to build and test AI applications. For other roles you might need to assign, see [Role-based access control for Microsoft Foundry](../concepts/rbac-foundry.md).

# [Azure CLI](#tab/azurecli)

[!INCLUDE [add-users-cli](../includes/add-users-cli.md)] 

# [Foundry portal](#tab/portal)

[!INCLUDE [add-users](../includes/add-users.md)]

---

## Verify team member access

[!INCLUDE [verify-team-access](../includes/verify-team-access.md)]

To confirm the deployed model is available, ask the team member to select **Build** in the upper-right navigation, then **Models** in the left pane.

## Clean up resources

When you no longer want this project, delete the resource group to delete all resources associated with it.

# [Azure CLI](#tab/azurecli)

```azurecli
az group delete --name my-foundry-rg --yes --no-wait
```

Deletion runs in the background. To confirm that the resource group is gone, run:

```azurecli
az group exists --name my-foundry-rg
```

The output shows `false` when deletion finishes.

# [Foundry portal](#tab/portal)

In the [Azure portal](https://portal.azure.com), find and select your resource group. Select **Delete** and confirm to delete the resource group and all its associated resources.

---

## Next step
 
> [!div class="nextstepaction"]
> [Microsoft Foundry quickstart](../quickstarts/get-started-code.md)

