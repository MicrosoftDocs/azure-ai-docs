---
title: "Set up a Microsoft Foundry project in Visual Studio Code"
description: "Sign in to Azure, select an existing Microsoft Foundry project, or create a project with Foundry Toolkit for Visual Studio Code."
manager: mcleans
ms.service: microsoft-foundry
ms.subservice: foundry-sdk
content_well_notification:
  - AI-contribution
ai-usage: ai-assisted
ms.topic: how-to
ms.date: 08/20/2026
ms.reviewer: erichen
ms.author: rotabor
author: bobtabor-msft

# customer intent: As an AI app developer, I want to set up a Foundry project in Visual Studio Code so that I can work with cloud models and agents in Foundry Toolkit.
ms.custom:
  - doc-kit-assisted
---

# Set up a Microsoft Foundry project in Visual Studio Code

Sign in to Azure, and then select an existing Foundry project or create one with
Microsoft Foundry Toolkit for Visual Studio Code. Foundry Toolkit uses the
project you select as its default project for cloud models, agents, tools, and
evaluations.

## Prerequisites

- [Install Microsoft Foundry Toolkit for Visual Studio Code](install-foundry-toolkit-visual-studio-code.md).
- An [Azure subscription](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- To select an existing project, access to that project. For more information,
  see [Role-based access control for Microsoft Foundry](../../concepts/rbac-foundry.md).
- To create a project, meet the
  [prerequisites to create a Foundry project](../create-projects.md#prerequisites).

## Sign in to Azure

Foundry Toolkit uses the account, tenant, and subscriptions available through
the Azure Resources extension.

1. In the Activity Bar, select **Azure**.
1. In the **Azure Resources** view, select **Sign in to Azure**.
1. Complete the sign-in flow.
1. In **Accounts & Tenants**, confirm that the account and tenant for your
   Foundry resources are selected.
1. In **Resources**, confirm that the target subscription is visible.

## Select an existing project

Set an accessible project as the default project for Foundry Toolkit.

1. In the Activity Bar, select **Foundry Toolkit**.
1. Under **My Resources**, select **Set Foundry Project**.
1. Select **Switch project**.

   :::image type="content" source="../../media/how-to/get-started-projects-vs-code/set-foundry-project.png" alt-text="Screenshot of Foundry Toolkit showing Set Foundry Project and the choices to switch projects or create a project." lightbox="../../media/how-to/get-started-projects-vs-code/set-foundry-project.png":::

1. Select the Azure subscription that contains the project.
1. Select the Foundry project.
1. Under **My Resources**, confirm that the project resources appear.

The selected project remains the default until you select another project,
clear the default project, sign out, or lose access to the project.

## Create a project

Use Foundry Toolkit to create a Foundry account and project with basic default
settings. For customized networking, security, naming, or Azure Policy
requirements, use the [Foundry portal](https://ai.azure.com/) or an
[infrastructure template](../create-resource-template.md).

1. In the Activity Bar, select **Foundry Toolkit**.
1. Under **My Resources**, select **Set Foundry Project**.
1. Select **Create project**.
1. Select your Azure subscription.
1. Select an existing resource group, or select **Create new resource group**.
1. If you create a resource group, enter the resource group name, and then
   select a location.
1. Enter a name for the Foundry project.
1. Monitor the notification for project creation progress.

   :::image type="content" source="../../media/how-to/get-started-projects-vs-code/project-creation-progress.png" alt-text="Screenshot of a Foundry Toolkit notification showing Foundry project creation progress." lightbox="../../media/how-to/get-started-projects-vs-code/project-creation-progress.png":::

1. Wait for the notification that the project deployed successfully.
1. Under **My Resources**, confirm that the new project resources appear.

Foundry Toolkit creates a Foundry account named from the project, creates the
project under that account, and sets the project as the Toolkit default.

## Switch the default project

Change the cloud project used by Foundry Toolkit without changing your Azure
account.

1. Under **My Resources**, locate the current default project.
1. Select the gear icon next to the project.
1. Select **Switch Default Project**.

   :::image type="content" source="../../media/how-to/get-started-projects-vs-code/switch-default-project.png" alt-text="Screenshot of the Foundry Toolkit project actions menu with Switch Default Project selected." lightbox="../../media/how-to/get-started-projects-vs-code/switch-default-project.png":::

1. Select **Switch project**.
1. Select the subscription and another accessible project.
1. Under **My Resources**, confirm that the selected project resources appear.

To work without a cloud project, run **Foundry Toolkit: Clear Default Project**.

## Clean up resources

Selecting an existing project doesn't create Azure resources. If you created a
project in this article, its resources can incur charges.

- If you used a shared resource group, don't delete the resource group. Follow
  [Delete projects](../create-projects.md#delete-projects) to remove the
  project. Delete the Foundry account only if Toolkit created it for this
  procedure and it contains no other projects or resources.
- If you created a dedicated resource group and no longer need anything in it,
  open the [Azure portal](https://portal.azure.com), select the resource group,
  and select **Delete resource group**.

> [!WARNING]
> Deleting a resource group permanently deletes every resource in it. Review
> the resource list before you confirm deletion.

## Related content

- [Microsoft Foundry Toolkit for Visual Studio Code overview](get-started-projects-visual-studio-code.md)
- [Create a project for Microsoft Foundry](../create-projects.md)
- [Role-based access control for Microsoft Foundry](../../concepts/rbac-foundry.md)
