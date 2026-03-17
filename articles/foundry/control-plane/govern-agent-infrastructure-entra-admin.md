---
title: Govern agent infrastructure as a Microsoft Entra global administrator
description: Learn how to elevate access, assign the right roles, and take infrastructure-level actions on Foundry agents as a Microsoft Entra global administrator.
ms.topic: how-to
ms.service: azure-ai-foundry
ms.date: 02/27/2026
ms.author: mahender
author: mattchenderson
ms.custom: dev-focus, doc-kit-assisted
ai-usage: ai-assisted
#customer intent: As an Entra Global Administrator, I want to understand how to govern Foundry agent infrastructure so that I can manage agents responsibly without disrupting shared resources.
---

# Govern agent infrastructure as a Microsoft Entra global administrator

As a Microsoft Entra global administrator, you might need to take action on Microsoft Foundry agents running in your tenant. Before you do, it's important to understand that the actions available to you in Foundry are **infrastructure actions**, not just runtime governance. When you stop or delete an agent, you're operating on Azure resources that might serve multiple tenants or teams.

This article helps you get the access you need, understand how admin center actions map to Azure resource operations, and make informed decisions about when and how to intervene. The guidance here focuses on infrastructure-level governance of agents built with [Foundry Agent Service](../agents/overview.md) as a fallback for situations that require direct administrative action.

> [!IMPORTANT]
> Always prefer **Stop** over **Delete** when you need to disable an agent. Stopping is reversible. Deletion permanently removes Azure resources and can affect other tenants.

## Prerequisites

- A [Microsoft Entra Global Administrator](/entra/identity/role-based-access-control/permissions-reference#global-administrator) role assignment. If your organization uses [Privileged Identity Management (PIM)](/entra/id-governance/privileged-identity-management/pim-configure), activate your Global Administrator role assignment before proceeding.

> [!NOTE]
> You don't need existing access to Azure subscriptions. This article walks you through how to [elevate your access](#elevate-access-to-manage-azure-subscriptions) to get visibility into the Azure resources that back Foundry agents.

## Understand how agent infrastructure works

Foundry agents are organized within **projects**, which are in turn part of a Foundry account resource in an Azure subscription. A project is a shared workspace where developers build, test, and collaborate on agents. Projects are Azure resources, backed by compute, storage, and a shared agent identity. Multiple agents can exist within a single project.

When a developer creates an agent in a project, the agent starts in an unpublished state. It shares the project's endpoint and identity and doesn't have its own dedicated Azure resources. An agent can have multiple versions. If you take action against the project itself, that action affects all agents within it.

When a developer publishes an agent, Foundry creates a dedicated **application** resource with its own endpoint, deployment, and Entra agent identity. Because published agents have their own infrastructure, you can take targeted action against them without affecting the rest of the project.

For a full description of agent lifecycle operations, see [Manage agents in Foundry Control Plane](how-to-manage-agents.md). To learn more about Foundry concepts referenced in this section, see:

- [Microsoft Foundry architecture](../concepts/architecture.md) for how Foundry resources map to Azure resources.
- [Agent identity concepts](../agents/concepts/agent-identity.md) for how agent identities work in Microsoft Entra ID.
- [Plan and manage Foundry](../concepts/planning.md) for subscription and resource group organization.

### Infrastructure actions vs. admin center actions

The actions available in the Foundry Control Plane are **infrastructure operations** on Azure resources. They're not the same as the **Block** and **Unblock** actions you might be familiar with in Microsoft 365 Admin Center. If an agent application serves a multitenant scenario, infrastructure actions affect **all consumers** of that agent, not just your tenant's users.

- [**Stop** and **Start**](how-to-manage-agents.md#start-and-stop-agents) operate on individual deployments by deallocating or provisioning compute. They affect the underlying Azure infrastructure, not just how an agent is used in your organization.
- **Delete** permanently removes Azure resources. For published agents, this includes the Agent Application and its deployments. This action can't be undone.

Always prefer **Stop** over **Delete**. Stopping preserves the option to restart later. Delete should be a last resort, used only after you've coordinated with resource owners and confirmed the agent should never run again.

## Elevate access to manage Azure subscriptions

Microsoft Entra ID and Azure use independent access control systems. Your Global Administrator role doesn't automatically grant you access to Azure subscriptions. To see and manage the Azure resources that back Foundry agents, you need to elevate your access.

Elevation assigns you the **User Access Administrator** role at root scope (`/`), which gives you visibility into all subscriptions and management groups in your tenant.

For the full procedure, see [Elevate access to manage all Azure subscriptions and management groups](/azure/role-based-access-control/elevate-access-global-admin).

> [!IMPORTANT]
> Remove your elevated access as soon as you finish. Elevation at root scope is a powerful permission, and the principle of least privilege applies. If your organization uses PIM, deactivate your Global Administrator role assignment after you remove the elevation toggle.

## Coordinate with resource owners

Foundry agents are backed by Azure resources that belong to specific subscriptions, resource groups, and projects. Those resources have owners. Before you take infrastructure-level action, identify and work with those owners whenever possible.

### When to coordinate vs. act independently

| Situation | Recommended approach |
|---|---|
| Active security threat or policy violation | Act first (Stop the agent), then notify the resource owners. |
| Routine compliance review or audit finding | Contact the resource owners and work together on remediation. |
| Agent consuming unexpected resources or cost | Notify the resource owners. Consider stopping the agent only if costs are critical and owners are unresponsive. |
| Agent misbehaving but not a security risk | Contact the resource owners before taking action. Stop only if the behavior is actively harmful. |

Infrastructure governance is a shared responsibility. Global administrators have the access to act, but resource owners have the context to understand the impact. Coordinating leads to better outcomes.

### Identify resource owners

1. In the Azure portal, navigate to the resource group that contains the agent's Foundry project.
1. Select **Access control (IAM)** > **Role assignments** to see who has permissions over the resource.

The relevant stakeholders for a resource could have many different roles. Privileged roles like **Owner** or **Contributor** are a good signal if you see them, but not everyone who is a stakeholder would necessarily have those assigned.

You can also look at the [Activity Log](/azure/azure-monitor/platform/activity-log?tabs=log-analytics) for the resource to see who has taken management actions recently. This can help you identify who is currently managing the resource, even if they don't have a privileged role assignment.

## Assign the right roles

After you elevate your access, assign yourself the minimum role needed for the action you want to take. Don't stay at root scope longer than necessary.

| Action you want to take | Minimum built-in role |
|---|---|
| View deployments within an agent application | [Azure AI User](/azure/role-based-access-control/built-in-roles/ai-machine-learning#azure-ai-user)<br/>(**Reader** is not sufficient) |
| Stop or start an agent deployment | [Azure AI Owner] |
| Resource management, including deletion | [Azure AI Owner] |

[Azure AI Owner]: /azure/role-based-access-control/built-in-roles/ai-machine-learning#azure-ai-owner

Assign roles at the narrowest scope possible. This usually means assigning the role over just the Foundry project resource you want to work with. If you only need to manage agents in a single resource group, assign the role there instead of at the subscription level.

If your organization uses PIM, consider creating eligible assignments instead of permanent ones. Eligible assignments require activation, which creates an audit trail and enforces time limits.

## Take action on an agent

When you need to intervene, choose the least disruptive action that addresses the situation.

### Stop an agent in the portal

Stopping an agent is the preferred approach for most situations. It disables the agent without destroying any resources, and you can restart later. For the full stop procedure, see [Start and stop agents](how-to-manage-agents.md#start-and-stop-agents).

### Delete an agent in the portal (last resort)

Deletion permanently removes agent resources and can't be undone. Before you delete, verify that no other tenants or teams depend on the agent, and confirm that the resource owners agree with permanent removal.

To delete an agent:

1. In the Foundry portal, select **Operate** > **Assets** > **Agents**.
1. Select the agent you want to delete.
1. Select **Edit**. This takes you to the **Build** tab for that agent.
1. Select the three dots (**...**) next to the **Save**, **Preview**, and **Publish** buttons, and then select **Delete agent**.
1. Type the agent name to confirm, and then select **Delete**.

To delete an individual agent version, select the version through the dropdown next to the **Save** button. Then, within the same dropdown, select **Delete current version**.

### Manage deployments with the REST API

You can also manage agent deployments programmatically by using the Azure Resource Manager REST API. This approach is useful when you need to act across multiple deployments or automate lifecycle operations.

The easiest way to run these commands is through [Azure Cloud Shell](/azure/cloud-shell/overview), which requires no installation and uses your current Azure sign-in session. If you prefer to work locally, [install the Azure CLI](/cli/azure/install-azure-cli) and [sign in](/cli/azure/authenticate-azure-cli) first.

The following examples use `az rest`. Replace the placeholder values with your own subscription, resource group, Foundry account, project, agent application, and deployment names.

#### List deployments for an agent application

```azurecli
az rest --method get \
  --uri "https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts/{accountName}/projects/{projectName}/applications/{applicationName}/agentdeployments?api-version=2025-10-01-preview"
```

#### Stop a deployment

```azurecli
az rest --method post \
  --uri "https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts/{accountName}/projects/{projectName}/applications/{applicationName}/agentdeployments/{deploymentName}/stop?api-version=2025-10-01-preview"
```

#### Start a deployment

```azurecli
az rest --method post \
  --uri "https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts/{accountName}/projects/{projectName}/applications/{applicationName}/agentdeployments/{deploymentName}/start?api-version=2025-10-01-preview"
```

#### Delete a deployment

```azurecli
az rest --method delete \
  --uri "https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts/{accountName}/projects/{projectName}/applications/{applicationName}/agentdeployments/{deploymentName}?api-version=2025-10-01-preview"
```

> [!CAUTION]
> Deleting a deployment permanently removes the Azure resource. If the agent serves multiple tenants, this action affects all of them. Always prefer stopping a deployment over deleting it.

## Related content

- [Elevate access to manage all Azure subscriptions and management groups](/azure/role-based-access-control/elevate-access-global-admin)
- [Manage agents in Foundry Control Plane](how-to-manage-agents.md)
- [What is Microsoft Foundry Control Plane?](overview.md)
- [Agent identity concepts in Microsoft Foundry](../agents/concepts/agent-identity.md)
- [Publish and share agents in Microsoft Foundry](../agents/how-to/publish-agent.md)
