---
title: Set up permissions for Microsoft Foundry evaluation workflows
description: Find and assign the Azure roles required to run evaluations, evaluate traces, use your own storage, and set up scheduled or continuous evaluation in Microsoft Foundry.
author: lgayhardt
ms.author: lagayhar
ms.reviewer: none
ms.date: 09/29/2026
ms.topic: how-to
ms.service: microsoft-foundry
ms.subservice: foundry-observability
ms.custom: doc-kit-assisted
ai-usage: ai-assisted
#CustomerIntent: As a Foundry user or administrator, I want to know which roles to assign for my evaluation workflow so that evaluations can run without authorization errors.
---

# Set up permissions for Microsoft Foundry evaluation workflows

Use this article to find the roles required for your Microsoft Foundry evaluation workflow. You don't need every role listed here. Start with the common evaluation role, and then add roles only if your workflow uses scheduled or continuous evaluation, traces, or your own storage account.

> [!TIP]
> For most portal and SDK evaluation workflows, your signed-in account needs the **Foundry User** role on the Foundry project. The extra roles in this article apply to specific workflows and resources.

[!INCLUDE [role-rename-note](../../includes/role-rename-note.md)]

## Before you begin

To [assign Azure roles](/azure/role-based-access-control/role-assignments-portal), you need `Microsoft.Authorization/roleAssignments/write` permission at the target scope. For example, the **Role Based Access Control Administrator** and **User Access Administrator** roles include this permission. If you can't create role assignments, send the relevant rows from this article to your administrator.

Evaluation workflows can use more than one identity:

- **Your identity** is the account that you use to sign in to the Foundry portal, Azure Developer CLI, or SDK.
- **An application identity** is the workload identity or service principal that runs evaluations in an application or CI/CD pipeline.
- **The project managed identity** is the identity that Foundry uses to access connected resources, such as traces or storage.

## Find the roles for your workflow

First, assign the role in this table for the evaluation task you want to perform.

| I want to | Assign the role to | Role | Assign at |
| --- | --- | --- | --- |
| Create continuous or scheduled evaluation rules | The project managed identity | **Foundry User** | The Foundry resource or project used for the evaluation rule |
| Run or review portal or SDK evaluations, including agent, synthetic dataset, admin-connected model, and benchmark workflows | Your identity or application identity | **Foundry User**, or a role with equivalent permissions | The Foundry resource or project that contains the evaluation |
| Run evaluations in CI/CD | The workload identity or service principal used by the pipeline | **Foundry User**, or a role with equivalent permissions | The Foundry resource or project that contains the evaluation |
| Run agent evaluations with the Azure Developer CLI | Your identity | **Foundry User** | The Foundry resource |

Evaluation jobs use Microsoft Entra ID. If an evaluation invokes a model deployment, assign **Foundry User** at the Foundry account scope. A project-only role assignment doesn't authorize model inference. For more information, see [Deployment type-specific permissions](../../concepts/rbac-foundry.md#deployment-typespecific-permissions).

For the permissions included in Foundry roles and guidance for custom roles, see [Role-based access control for Microsoft Foundry](../../concepts/rbac-foundry.md).

## Add permissions for trace-based workflows

Use this section if you run one-time, continuous, or scheduled evaluations over Application Insights traces, create a dataset from traces, or view log-based monitoring data.

The identity that submits a trace evaluation or trace-based dataset job first needs the **Foundry User** role from [Find the roles for your workflow](#find-the-roles-for-your-workflow). Then assign the following roles:

| I want to | Assign the role to | Role | Assign at |
| --- | --- | --- | --- |
| Run trace evaluations or create datasets from traces | The project managed identity | **Reader** | The connected Application Insights resource |
| Read protected trace tables during evaluation or dataset generation | The project managed identity | **Privileged Monitoring Data Reader**, in addition to **Reader** | The connected Application Insights resource |
| View traces or log-based monitoring data | Your identity | **Log Analytics Reader** | The connected Application Insights resource and, for workspace-scoped queries, its linked Log Analytics workspace |
| View protected trace content | Your identity | **Privileged Monitoring Data Reader**, in addition to **Log Analytics Reader** | The Application Insights resource for resource-scoped queries or the Log Analytics workspace for workspace-scoped queries |

Trace evaluation and dataset generation use a resource-context query against the connected Application Insights resource. The [Reader role](/azure/role-based-access-control/built-in-roles/general#reader) provides the resource read permission required for this query.

If the linked Log Analytics workspace is configured to [**Require workspace permissions**](/azure/azure-monitor/logs/manage-access#access-control-mode), also assign **Log Analytics Reader** to the project managed identity on that workspace. For protected tables, assign **Privileged Monitoring Data Reader** on the workspace too. If the workspace uses [DataActionsOnly mode](/azure/azure-monitor/logs/manage-access#dataactionsonly-mode), use **Log Analytics Data Reader** instead of a control-plane reader role.

For information about protected trace content, see [Protect sensitive content in traces](traces-sensitive-content.md).

## Add permissions for your own storage account

Use this section only if your Foundry project connects to your own Azure Storage account by using Microsoft Entra ID authentication.

| Assign the role to | Role | Assign at |
| --- | --- | --- |
| The project managed identity | **Storage Blob Data Contributor** | The storage account connected to the Foundry project |

This role lets the evaluation service read and write datasets and evaluation results in blob storage. If the connection uses an account key instead, this managed-identity role isn't used. Microsoft recommends Microsoft Entra ID authentication for granular access control.

For storage and network requirements, see [Bring your own storage](../../concepts/evaluation-regions-limits-virtual-network.md#bring-your-own-storage).

## Verify your setup

After you assign the roles:

1. In the Azure portal, open each resource where you assigned a role.
1. Select **Access control (IAM)** > **Check access**.
1. Search for the user, application identity, or project managed identity.
1. Confirm that the expected role appears at the required scope.
1. Wait several minutes for new role assignments to take effect, and then retry the workflow.

If an evaluation still fails with `401 Unauthorized` or `403 Forbidden`, see [Troubleshoot evaluation and observability issues](troubleshooting.md).

## Next steps

- To run an evaluation with an SDK, see [Introduction to cloud evaluation](cloud-evaluation.md).
- To evaluate an agent, see [Evaluate your AI agents](evaluate-agent.md).
- To evaluate production telemetry, see [Evaluate model and agent traces](cloud-evaluation-deployed-interactions.md).
- To create reusable evaluation data from production traffic, see [Convert agent traces into evaluation datasets](traces-to-dataset.md).
- To evaluate production traffic on a schedule, see [Monitor agents and set up continuous evaluation](how-to-monitor-agents-dashboard.md).
