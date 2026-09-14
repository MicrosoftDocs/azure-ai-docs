---
title: "Create a private skill catalog in Foundry Agent Service"
description: "Create a private skill catalog in Foundry Agent Service using Azure API Center. Let developers discover and use organization-scoped agent skills."
author: mattwojo
reviewer: lindazqli
ms.author: mattwoj
ms.reviewer: zhuoqunli
ms.date: 09/14/2026
ms.manager: mcleans
ms.topic: how-to
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.custom: pilot-ai-workflow-jan-2026, doc-kit-assisted
ai-usage: ai-assisted
#CustomerIntent: As a platform admin, I want to create a private skill catalog so that developers in my organization can discover and use approved agent skills.
---

# Create a private skill catalog (preview)
[!INCLUDE [preview-feature](../../openai/includes/preview-feature.md)]

Create a private skill catalog so developers in your organization can discover and use agent skills through Foundry. A skill is a reusable capability - instructions, bundled scripts, and tool references - that an agent can consume to extend what it does. A private skill catalog uses [Azure API Center](/azure/api-center/register-discover-skills) to register organization-scoped skills that only your developers can access.

## Prerequisites

* A Foundry project. For setup guidance, see [Create projects in Microsoft Foundry](../../how-to/create-projects.md).
* Permissions to discover and use skills in your Foundry project. For more information, see [Role-based access control in Microsoft Foundry](../../concepts/rbac-foundry.md).
* An [Azure API Center](/azure/api-center/set-up-api-center). "API Center" is the name that developers use to find the catalog in Foundry. Use a descriptive name.
* One or more skills that you want to share with your organization, typically hosted in a source-code repository such as GitHub. Register them with API Center by following [Register skills in your API center](/azure/api-center/register-discover-skills).

## Plan administrator and developer access

Before you create the catalog, decide who manages it and who consumes it.

| Goal | Who | Where | What to do |
| --- | --- | --- | --- |
| Create and manage the skill catalog | Catalog admins | Azure API Center | Create the API Center resource, register skills, and define the allowed tools each skill can access. |
| Discover skills from the private catalog | Developers | Azure API Center (RBAC) | Assign access at the API Center resource or a parent scope so developers can view the registered skills. |
| Use skills | Developers | Foundry project | Confirm developers can access the Foundry project and can use skills from the catalog. |

## Register skills and define allowed tools

Register each skill in your API Center so it's discoverable, and scope what it's allowed to reach.

1. In the [Azure portal](https://portal.azure.com), go to your API Center resource.
1. In the sidebar under **Inventory**, select **Assets**.
1. Select **+ Register an asset** > **Skill**, and provide the skill's title, summary, description, lifecycle stage, and the **Source URL** of the Git repository that holds the skill's source code.
1. Under **Allowed tools**, select **+ Add tool** to specify the APIs or MCP servers from your API inventory that the skill can access.

    > [!IMPORTANT]
    > The allowed tools list is the governance boundary for a skill. It explicitly defines which resources the skill can consume, so a shared skill can't reach endpoints you didn't approve.

1. Optionally add **License** and **Contact information**, then select **Create**.

To keep the catalog in sync with source instead of re-uploading, integrate a Git repository with your API Center. For more information, see [Synchronize API assets from a Git repo](/azure/api-center/synchronize-assets-git).

## (Optional) Assess skill quality before promotion

API Center can automatically assess registered skills against default or custom criteria before you promote them.

1. In the [Azure portal](https://portal.azure.com), go to your API Center resource.
1. Select **Governance** > **AI Assessment**.
1. Select the **Skills** tab, set **Assessment status** to **Enabled**, and accept the default criteria or add custom criteria (name, score range, pass threshold, and weight).
1. Select **Save**.

Developers can then view assessment results on each skill's details page in the API Center portal.

## Grant developer access to the catalog

Assign Azure RBAC permissions so developers can discover skills from your private catalog in Foundry.

1. Decide whether to grant access to a security group or to individual users.
1. On the API Center resource, or on a parent resource group or subscription that contains the API Center, assign the [Azure API Center Data Reader](/azure/role-based-access-control/built-in-roles/integration#azure-api-center-data-reader) role (or an equivalent custom role) to the users who need access to the skill catalog.

The Azure API Center role assignment and the Foundry project role assignment control access to different resources. Assigning permissions only at the Foundry project scope does not grant access to API Center catalog data. Users must also have the appropriate Azure API Center role assignment at the API Center resource scope (or an inherited scope such as its parent resource group or subscription). The Azure API Center Data Reader role provides read access to Azure API Center data plane operations.

Role assignments can take up to 24 hours to propagate. If developers don't see the catalog immediately, wait and try again.

## Verify catalog discovery in Foundry

After you grant access, confirm that developers can find and use the catalog in the Foundry portal.

1. In the Foundry portal, open the project that your developers use.
1. Go to **Build** > **Tools** > **Skills**, and then select **Browse skills**.
1. Under **Registry**, select the API Center name. The catalog isn't listed as a separate item on the page. Its name appears as a registry filter.
1. Select a skill from the catalog and review its summary, source, compatibility, and allowed tools.

If the catalog appears and displays your registered skills, the configuration is complete.

## Troubleshoot private skill catalog issues

If you encounter problems setting up or using your private skill catalog, use the following table to identify and resolve common issues.

| Issue | Cause | Resolution |
| --- | --- | --- |
| The private skill catalog doesn't appear in Foundry. | You don't have access to the API Center resource, or you're looking for the catalog outside the registry filters. | Confirm that the Azure API Center Data Reader role applies at the API Center resource or a parent scope. Then go to **Build** > **Tools** > **Skills** > **Browse skills** and look for the API Center name under **Registry**. |
| The catalog appears, but a skill is missing. | The skill isn't registered, or Git sync hasn't run. | Confirm the skill is registered under **Inventory** > **Assets** in API Center, and that any Git repository integration has synced. |
| A skill runs but can't reach a resource. | The resource isn't in the skill's allowed tools. | Add the required API or MCP server to the skill's **Allowed tools** in API Center. |
| The catalog doesn't appear after role assignment. | The role assignment is at the wrong scope, or Azure RBAC propagation isn't complete. | In the Azure portal, open the API Center resource and verify under **Access control (IAM)** that the role assignment applies to the API Center resource. Wait up to 24 hours after correcting the assignment, and then try again. |
| The skill source can't be opened. | The **Source URL** is incorrect, or the repository is private. | Verify the Git repository URL in the skill registration and confirm the developer has access to the repository. |

## Related content

[What is Toolbox in Foundry?](../concepts/toolbox-overview.md)

[Create a private tool catalog (preview)](private-tool-catalog.md)

[Register skills in your API center](/azure/api-center/register-discover-skills)
