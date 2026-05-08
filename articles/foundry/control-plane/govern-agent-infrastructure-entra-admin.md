---
title: Govern agent infrastructure as a Microsoft Entra administrator
description: Learn how to elevate access, assign the right roles, and take infrastructure-level actions on Foundry agents as a Microsoft Entra administrator.
ms.topic: how-to
ms.service: microsoft-foundry
ms.date: 04/30/2026
ms.author: mahender
author: mattchenderson
ms.custom: dev-focus
ai-usage: ai-assisted
#customer intent: As a Microsoft Entra administrator, I want to understand how to govern Foundry agent infrastructure so that I can manage agents responsibly without disrupting shared resources.
---

# Govern agent infrastructure as a Microsoft Entra administrator

As a Microsoft Entra administrator, you might need to take action on Microsoft Foundry agents in your tenant. Before you do, understand that Foundry gives you **infrastructure actions**, not just runtime governance. When you stop or delete an agent, you operate on Azure resources. These resources might serve multiple tenants or teams.

This article helps you:
- Get the access you need
- Understand how admin center actions map to Azure resource operations
- Make informed decisions about when and how to intervene

The guidance here focuses on infrastructure-level governance of agents built with [Foundry Agent Service](../agents/overview.md) as a fallback for situations that require direct administrative action.

> [!IMPORTANT]
> Always prefer **Stop** over **Delete** when you need to take action against an agent. Stopping is reversible. Deletion permanently removes Azure resources and can affect other tenants.

## Prerequisites

- One of the following Microsoft Entra role assignments:
  - [Microsoft Entra Global Administrator](/entra/identity/role-based-access-control/permissions-reference#global-administrator)
  - [Microsoft Entra AI Administrator](/entra/identity/role-based-access-control/permissions-reference#ai-administrator)
- If your organization uses [Privileged Identity Management (PIM)](/entra/id-governance/privileged-identity-management/pim-configure), activate your role assignment before proceeding.

> [!IMPORTANT]
> **[AI Administrators](/entra/identity/role-based-access-control/permissions-reference#ai-administrator)**: You can't perform the [access elevation procedure](#elevate-access-to-manage-azure-subscriptions) yourself. You should coordinate with the agent owner first, who can either:
> - Take the infrastructure actions on your behalf
> - Grant you necessary Azure role assignments on the specific resources
> 
> If you can't identify or reach the agent owner, coordinate with a Global Administrator as an alternative.

## Understand how agent infrastructure works

Foundry agents live within **projects**. Projects are part of a Foundry account resource in an Azure subscription. A project gives developers a shared workspace to build, test, and collaborate on agents. Each project has its own compute, storage, and a shared agent identity. Multiple agents can exist within a single project. Actions against the project affect all agents in that project.

Developers create **Foundry agents** within a project. Each agent gets a unique identity and endpoint for interaction. Foundry automatically registers each agent with the [Agent 365 registry](/microsoft-365/admin/manage/agent-registry) using the agent's unique identity. 

Agents can have multiple **agent versions** as developers iterate and improve their functionality. Each version represents a snapshot of the agent's configuration and behavior at a specific point in time.

> [!NOTE]
> [Prompt agents](../agents/quickstarts/prompt-agent.md) can also use a common endpoint that serves all agents in the project. Agents that run this way share the project's infrastructure and identity. Don't use project endpoints for production. Foundry doesn't create more registrations in Agent 365 for project endpoints or project identities.

When a developer publishes an agent, Foundry creates a dedicated **agent application** resource. This resource has its own endpoint and Entra agent identity. The application identity is separate from the individual agent identities created earlier. Foundry also registers the application in the Agent 365 registry using the application's unique identity. 

Agent applications can have multiple **agent deployments**. Each deployment references an existing agent version as its definition.

For a full description of agent lifecycle operations, see [Manage agents in Foundry Control Plane](how-to-manage-agents.md). To learn more about Foundry concepts referenced in this section, see:

- [Microsoft Foundry architecture](../concepts/architecture.md) for how Foundry resources map to Azure resources.
- [Agent identity concepts](../agents/concepts/agent-identity.md) for how agent identities work in Microsoft Entra ID.
- [Plan and manage Foundry](../concepts/planning.md) for subscription and resource group organization.

### Infrastructure actions vs. admin center actions

The actions available in the Foundry Control Plane are **infrastructure operations** on Azure resources. They're different from the **Block** and **Unblock** actions you might be familiar with in Microsoft 365 Admin Center.

**Block actions** in Microsoft 365 Admin Center and Teams Admin Center affect agent visibility to users:
- **Scope**: Only affects agent projection in Teams and Microsoft 365 Copilot
- **Impact**: Users can't access the agent through these specific channels
- **Foundry Access**: The agent remains fully functional in Foundry portal and other integration points
- **Infrastructure**: No impact on underlying Azure resources or compute

**Infrastructure actions** in Foundry Control Plane affect the agent's underlying resources:
- [**Stop** and **Start**](how-to-manage-agents.md#start-and-stop-agents) operate on individual deployments by deallocating or provisioning compute. They affect the underlying Azure infrastructure and make the agent unavailable across all channels (Teams, Microsoft 365 Copilot, Foundry, APIs).
- **Delete** permanently removes Azure resources. For published agents, deletion includes the agent application and its deployments. This action can't be undone.

If an agent application serves a multitenant scenario, infrastructure actions affect **all consumers** of that agent, not just your tenant's users.

Always prefer **Stop** over **Delete**. Stopping preserves the option to restart later. Delete should be a last resort, used only after you coordinate with resource owners and confirm the agent should never run again.

## Identify the Foundry resource type for an agent

The Agent 365 registry shows a unified inventory of Foundry agents and agent applications. Both are "agents", but they have different management capabilities. To know what options you have, you first need to identify which Foundry resource type you're dealing with.

Foundry registers both types with a **Foundry Azure resource ID**:

| Resource type | Resource ID pattern<sup>1</sup> |
|---|---|
| Foundry agent | `.../projects/{project-name}/agents/{agent-name}` |
| Agent application | `.../projects/{project-name}/applications/{application-name}` |

<sup>1</sup> The full resource ID pattern is omitted for brevity. Both share a common prefix: `/subscriptions/{sub-id}/resourceGroups/{group}/providers/Microsoft.CognitiveServices/accounts/{account-name}/projects/{project-name}/...`. The key differentiator is the segment after the project: either `agents/{agent-name}` or `applications/{application-name}`.

In Microsoft 365 Admin Center, you can find these values in the "Platform details" section. The admin center automatically detects the resource type. For agent applications, it shows **Stop** or **Start** buttons or [prompts you for elevation if you're eligible](#elevate-access-to-manage-azure-subscriptions).

## Coordinate with resource owners

Foundry agents require Azure resources organized within specific subscriptions, resource groups, and projects. Those resources have owners. Before you take infrastructure-level action, identify and work with those owners whenever possible.

### When to coordinate vs. act independently

| Situation | Recommended approach |
|---|---|
| Active security threat or policy violation | Act first (stop the agent), then notify the resource owners. |
| Routine compliance review or audit finding | Contact the resource owners and work together on remediation. |
| Agent consuming unexpected resources or cost | Notify the resource owners. Consider stopping the agent only if costs are critical and owners are unresponsive. |
| Agent misbehaving but not a security risk | Contact the resource owners before taking action. Stop only if the behavior is actively harmful. |

Infrastructure governance is a shared responsibility. Global administrators have the access to act. Resource owners have the context to understand the impact. Coordinating leads to better outcomes.

### Identify resource owners

Start by checking the owners listed in the agent registration details in Microsoft 365 Admin Center. You can also identify owners and sponsors through the Entra objects.

If you can see the Azure resources (elevate access if you can't - see the next section), check which users have permission over the resources:

1. In the [Azure portal](https://portal.azure.com/), navigate to the resource group that contains the agent's Foundry project.
1. Select **Access control (IAM)** > **Role assignments** to see who has permissions over the resource.

Resource stakeholders might have many different roles. Privileged roles like **Owner** or **Contributor** are a good signal. However, not all stakeholders have these privileged roles.

Check the [Activity Log](/azure/azure-monitor/platform/activity-log?tabs=log-analytics) for the resource. The log shows who took management actions recently. This approach helps you identify current resource managers, even if they don't have privileged role assignments.

## Elevate access to manage Azure subscriptions

Microsoft Entra ID and Azure use separate access control systems. Your administrator role doesn't automatically give you access to Azure subscriptions. To see and manage Azure resources that back Foundry agents, you need Azure role assignments. If you don't have the right permissions, elevate your access.

The elevation procedure requires the Global Administrator role. AI Administrators should coordinate with agent owners or Global Administrators. See the [Prerequisites](#prerequisites) for details.

Elevation assigns you the **User Access Administrator** role at root scope (`/`). This role gives you visibility into all subscriptions and management groups in your tenant.

For the full procedure, see [Elevate access to manage all Azure subscriptions and management groups](/azure/role-based-access-control/elevate-access-global-admin).

> [!IMPORTANT]
> Remove your elevated access as soon as you finish. Elevation at root scope is a powerful permission, and the principle of least privilege applies. Follow the [de-elevation procedure](#remove-elevated-access) when you complete your tasks.
>
> If your organization uses PIM, deactivate your Global Administrator role assignment after you remove the elevation toggle.

### Remove elevated access

When you finish your admin tasks, remove your elevated permissions in reverse order:

1. **Remove Azure role assignments**: Remove any Azure AI roles you gave yourself (such as Azure AI Owner) from the specific Foundry projects or resource groups.

   **Azure portal**:
   1. In the Azure portal, navigate to the resource where you assigned yourself roles.
   1. Select **Access control (IAM)** > **Role assignments**.
   1. Find your user account in the role assignments list.
   1. Select the assignment and choose **Remove**.

   **Azure CLI**:
   ```azurecli
   # List current role assignments to find the assignment ID
   az role assignment list --assignee <your-email> --scope <resource-scope>
   
   # Remove the specific role assignment
   az role assignment delete --ids <assignment-id>
   ```

1. **Remove User Access Administrator role**: Remove the root-level User Access Administrator role from the elevation procedure.

   **Azure portal**:
   1. In the Azure portal, go to **Microsoft Entra ID** > **Properties**.
   1. Under **Access management for Azure resources**, set the toggle to **No**.
   1. Select **Save**.

   **Azure CLI**:
   ```azurecli
   # Remove the User Access Administrator role at root scope
   az role assignment delete \
     --assignee <your-email> \
     --role "User Access Administrator" \
     --scope "/"
   ```

This two-step process ensures you remove both the specific permissions you granted yourself and the broad elevation that enabled those grants.

## Assign the right roles

After you elevate your access, assign yourself the minimum role needed for your action. Don't stay at root scope longer than necessary.

| Action | Minimum built-in role for Foundry agent objects | Minimum built-in role for Agent applications |
|---|---|---|
| View | [Azure AI User]<br/>(**Reader** isn't sufficient) | [Reader](/azure/role-based-access-control/built-in-roles/general#reader) |
| Stop/Start | _Not supported_ | [Azure AI Owner] |
| Delete | [Azure AI User] | [Azure AI Owner] |

[Azure AI User]: /azure/role-based-access-control/built-in-roles/ai-machine-learning#azure-ai-user
[Azure AI Owner]: /azure/role-based-access-control/built-in-roles/ai-machine-learning#azure-ai-owner

Assign roles at the narrowest scope possible. For Foundry agents, assign the role over just the Foundry project resource you want to work with. For agent applications, assign the role at the application scope. If you only need to manage agents in a single resource group, assign the role at the resource group scope. Don't assign these roles at the subscription or management group scope.

If your organization uses PIM, consider creating eligible assignments instead of permanent ones. Eligible assignments require activation. This approach creates an audit trail and enforces time limits.

## Take action on an agent

When you need to intervene, choose the least disruptive action for your situation. Your choice of action and agent type determines which interface you use to manage the agent. Use the tabs in each section to identify the right interface for your scenario.

# [Microsoft 365 Admin Center](#tab/microsoft-365-admin-center)

Microsoft 365 Admin Center includes Foundry agents in your full agent inventory. You can conveniently stop and start agent applications directly from the registry entry.

| Agent type | Supported actions in Microsoft 365 Admin Center |
| --- | --- |
| Agent applications | Stop, Start |
| Foundry agents | _None - use another interface_ |

# [Foundry portal](#tab/foundry-portal)

The Foundry portal provides a web-based interface for managing Foundry resources.

| Agent type | Supported actions in the portal |
| --- | --- |
| Agent applications | Stop, Start, Delete |
| Foundry agents | Delete _(Stop and Start aren't supported)_|

# [REST API](#tab/rest-api)

The REST API lets you manage Foundry programmatically. This approach is useful when you need to act across multiple deployments or automate lifecycle operations.

| Agent type | Supported actions in the portal |
| --- | --- |
| Agent applications | Stop, Start, Delete |
| Foundry agents | Delete _(Stop and Start aren't supported)_ |

The examples use `az rest` commands to simplify authentication. The easiest way to run these commands is through [Azure Cloud Shell](/azure/cloud-shell/overview). Cloud Shell requires no installation and uses your current Azure sign-in session. If you prefer to work locally, [install the Azure CLI](/cli/azure/install-azure-cli) and [sign in](/cli/azure/authenticate-azure-cli) first.

For each REST API example, replace the placeholder values with your own subscription, resource group, Foundry account, project, and other resource names.

---

### Stop an agent

Stopping an agent is the preferred approach for most situations. Stopping disables the agent without destroying resources. You can restart the agent later. 

# [Agent application](#tab/agent-application/microsoft-365-admin-center)

When you open the agent details page for a Foundry agent application, Microsoft 365 Admin Center automatically checks if you have the necessary permissions to manage the agent. If you do, a **Stop** or **Start** button is available at the top of the page, based on the current state of the application. If you don't see these buttons but are a Global Administrator, follow the prompt to automatically elevate your access and grant yourself the Azure AI Owner role over the agent application.

If your agent application is currently running, select **Stop** to stop it. This action stops every agent deployment associated with the application. The agent application and its deployments still exist. You can start them again later.

When you're ready to start the agent application again, select **Start**. This action starts the agent application's most recent deployment. If you need to start other deployments, use the REST API.

If you elevated your access, make sure to [remove it when you're done](#remove-elevated-access).

# [Foundry agent](#tab/foundry-agent/microsoft-365-admin-center)

The Foundry agent resource type doesn't have a stop API. For agent resources that can't continue to run, consider deletion.

# [Agent application](#tab/agent-application/foundry-portal)

For the full stop procedure in the portal, see [Start and stop agents](how-to-manage-agents.md#start-and-stop-agents).

# [Foundry agent](#tab/foundry-agent/foundry-portal)

The Foundry agent resource type doesn't have a stop API. For agent resources that can't continue to run, consider deletion.

# [Agent application](#tab/agent-application/rest-api)

To fully stop an agent application, you need to stop each of its deployments. Stopping a deployment deallocates the underlying compute resources, but the deployment and application still exist and can be restarted later.

First, list the deployments for your agent application:

```azurecli
az rest --method get \
  --uri "https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts/{accountName}/projects/{projectName}/applications/{applicationName}/agentdeployments?api-version=2025-10-01-preview"
```

Then, for each deployment, run the stop command:

```azurecli
az rest --method post \
  --uri "https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts/{accountName}/projects/{projectName}/applications/{applicationName}/agentdeployments/{deploymentName}/stop?api-version=2025-10-01-preview"
```

When you're ready to start the agent application again, you can start a deployment with this command:

```azurecli
az rest --method post \
  --uri "https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts/{accountName}/projects/{projectName}/applications/{applicationName}/agentdeployments/{deploymentName}/start?api-version=2025-10-01-preview"
```

# [Foundry agent](#tab/foundry-agent/rest-api)

The Foundry agent resource type doesn't have a stop API. For agent resources that can't continue to run, consider deletion.

---

### Delete an agent (last resort)

Deletion permanently removes agent resources and can't be undone. Before you delete, verify that no other tenants or teams depend on the agent, and confirm that the resource owners agree with permanent removal.

# [Agent application](#tab/agent-application/microsoft-365-admin-center)

Deleting Foundry agents isn't supported in Microsoft 365 Admin Center. Use another interface to delete if truly necessary.

# [Foundry agent](#tab/foundry-agent/microsoft-365-admin-center)

Deleting Foundry agents isn't supported in Microsoft 365 Admin Center. Use another interface to delete if truly necessary.

# [Agent application](#tab/agent-application/foundry-portal)

The Foundry portal doesn't currently provide a way to directly delete agent applications. If you need to remove just the application object, use the REST API.

# [Foundry agent](#tab/foundry-agent/foundry-portal)

To delete an agent:

1. In the [Foundry portal](https://ai.azure.com/nextgen), select **Operate** > **Assets** > **Agents**.
1. Find and select the agent you want to delete.
1. Select **Edit**. This action takes you to the **Build** tab for that agent.
1. Select the three dots (**...**) next to the **Save**, **Preview**, and **Publish** buttons, and then select **Delete agent**.
1. Type the agent name to confirm, and then select **Delete**.

To delete an individual agent version, select the version through the dropdown next to the **Save** button. Then, within the same dropdown, select **Delete current version**.

> [!CAUTION]
> Deleting an agent permanently removes the resource. If the agent serves multiple tenants, this action affects all of them. Always prefer stopping a deployment over deleting it.

# [Agent application](#tab/agent-application/rest-api)

When you use the agent application model, you can delete the entire application or individual deployments. Deleting the application removes all deployments and the application itself. Deleting a deployment only removes that deployment, but the application and other deployments remain.

#### Delete the entire agent application

To delete the entire agent application, run the following command:

```azurecli
az rest --method delete \
  --uri "https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts/{accountName}/projects/{projectName}/applications/{applicationName}?api-version=2025-10-01-preview"
```

> [!CAUTION]
> Deleting an agent application permanently removes the Azure resource and all its deployments. If the agent serves multiple tenants, this action affects all of them. Always prefer stopping a deployment over deleting it.

#### Delete a specific deployment within an agent application

If you just want to delete a specific deployment, first obtain the deployment name from the list of deployments for the application:

```azurecli
az rest --method get \
  --uri "https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts/{accountName}/projects/{projectName}/applications/{applicationName}/agentdeployments?api-version=2025-10-01-preview"
```

Then, run this command to delete that deployment:

```azurecli
az rest --method delete \
  --uri "https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts/{accountName}/projects/{projectName}/applications/{applicationName}/agentdeployments/{deploymentName}?api-version=2025-10-01-preview"
```

> [!CAUTION]
> Deleting a deployment permanently removes the Azure resource. If application traffic is being routed to a deleted deployment, clients see errors. If the agent serves multiple tenants, this action affects all of them. Always prefer stopping a deployment over deleting it.

# [Foundry agent](#tab/foundry-agent/rest-api)

If you're sure you need to delete a Foundry agent, use this command:

```azurecli
az rest --method delete \
  --resource "https://ai.azure.com/" \
  --uri "https://{accountName}.services.ai.azure.com/api/projects/{projectName}/agents/{agentName}?api-version=2025-11-15-preview"
```

> [!CAUTION]
> Deleting an agent permanently removes the resource. If the agent serves multiple tenants, this action affects all of them. Always prefer stopping a deployment over deleting it.

---

## Related content

- [Elevate access to manage all Azure subscriptions and management groups](/azure/role-based-access-control/elevate-access-global-admin)
- [Manage agents in Foundry Control Plane](how-to-manage-agents.md)
- [What is Microsoft Foundry Control Plane?](overview.md)
- [Agent identity concepts in Microsoft Foundry](../agents/concepts/agent-identity.md)
- [Agent applications in Microsoft Foundry](../agents/how-to/agent-applications.md)
