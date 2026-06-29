---
title: "Hosted agent permissions reference"
description: "Reference for permissions required to create, deploy, and interact with hosted agents in Microsoft Foundry."
manager: mcleans
author: mattchenderson
ms.author: mahender
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.topic: reference
ms.date: 04/21/2026
ms.custom:
  - azure-ai-agents
  - classic-and-new
  - doc-kit-assisted
ai-usage: ai-assisted
---

# Hosted agent permissions reference

When working with [Hosted agents in Microsoft Foundry][hosted-agents], it's important to understand the various permissions involved. There are several classes of permissions involved in Hosted agent development, spanning the Azure Resource Manager control plane and the Foundry data plane:

- Permissions granted to users or principals working with Foundry resources
- Permissions granted to the Foundry project
- Permissions granted to the agent

This article is a companion to [Role-based access control for Microsoft Foundry][foundry-rbac], which introduces role-based access control (RBAC) concepts and the built-in roles available in Microsoft Foundry. You should familiarize yourself with that article before proceeding. This article covers the operations involved in Hosted agent development and deployment, the permissions required to perform those operations, and which built-in roles cover those permissions.

For end-to-end deployment and lifecycle tasks, see [Deploy a Hosted agent][deploy] and [Manage Hosted agent lifecycle][lifecycle]. For identity-specific behavior, see [Agent identity][agent-identity].

> [!IMPORTANT]
> Always adhere to the principle of least privilege when assigning permissions. Only grant the permissions necessary for users and agents to perform their tasks, and regularly review and update permissions as needed.

## Roles in this article

Azure AI Foundry permissions span two planes: the Azure Resource Manager (ARM) control plane and the Foundry data plane. [Owner][role-owner] and [Contributor][role-contributor] roles have broad ARM control plane permissions but don't include data plane permissions. Data plane operations—such as creating agents or interacting with them—require specific Azure AI Foundry roles like [Foundry User][role-ai-user], [Foundry Project Manager][role-project-manager], or [Foundry Owner][role-ai-owner].

[!INCLUDE [role-rename-note](../../includes/role-rename-note.md)]

This article references the following built-in roles. For information about custom role definitions, see [Azure custom roles](/azure/role-based-access-control/custom-roles).

| Role | Purpose in Hosted agent deployment |
| ----- | ------------------------------------- |
| [Owner][role-owner] | Full permissions to create and manage Azure resources |
| [Contributor][role-contributor] | Create and manage Azure resources |
| [Role Based Access Control Administrator][role-rbac-admin] | Create role assignments on Azure resources |
| [Foundry User][role-ai-user] | Create agents, perform model inference, and interact with agents |
| [Foundry Project Manager][role-project-manager] | Manage projects, create agents, perform model inference, interact with agents, and create role assignments |
| [Foundry Account Owner][role-account-owner] | Create deployments, manage projects, and handle account-level resources. Create role assignments for control plane operations only. Can't perform data plane operations such as creating or interacting with agents. |
| [Foundry Owner][role-ai-owner] | Full control plane and data plane permissions over account resources, but can't create role assignments |
| [Container Registry Repository Reader][role-acr-reader] | Pull container images from the registry |
| [Container Registry Repository Writer][role-acr-writer] | Push container images to the registry |
| [AcrPull][role-acrpull] | Pull container images from the registry |
| [AcrPush][role-acrpush] | Push container images to the registry |
| [Log Analytics Data Reader][role-log-analytics] | Read telemetry data for evaluations |
| [Cognitive Services OpenAI User][role-openai-user] | Access account-level OpenAI endpoints directly |
| [Cognitive Services User][role-cog-services-user] | Access account-level capabilities (Speech, Vision, Language) directly |

> [!CAUTION]
> Although it might sound like an appropriate role for a developer working with Hosted agents, the **Azure AI Developer** built-in role is insufficient for Hosted agent scenarios. This role is scoped to Azure Machine Learning and Foundry hubs, not to the Foundry project resources used by Hosted agents, and it doesn't include the resource management permissions required for Hosted agent deployment.

## Quick diagnosis by symptom

Use these links to jump directly to sections that address common permission issues:

- **Can't create agent**: See [Agent creation](#agent-creation)
- **Agent can't access models**: See [Agent access beyond defaults](#agent-access-beyond-defaults)
- **Deployment fails**: See [Hosted agent deployment](#hosted-agent-deployment) and [Azure Container Registry setup](#azure-container-registry-setup)
- **Agent can't pull images at runtime**: See [Azure Container Registry setup](#azure-container-registry-setup)
- **Agent interaction fails**: See [Agent interaction](#agent-interaction)
- **Role assignment fails**: See [Creating that role assignment requires](#azure-resource-setup) sections and [Connections setup](#connections-setup)
- **Can't publish agent to Teams or Microsoft 365 Copilot**: See [Azure Bot Service setup](#azure-bot-service-setup)

## Hosted agent solution architecture

A completed Hosted agent setup involves multiple Azure resources, identity assignments, and connections working together. The following diagram shows the key components and their relationships:

```
Foundry Account
├── Model Deployment
└── Foundry Project (has managed identity)
    ├── Hosted Agent
    │   └── Agent Version → references container image
    ├── Connection to Azure Container Registry
    └── Connection to Application Insights

Separate Azure Resources:
├── Azure Container Registry → contains container image
├── Application Insights → logs to Log Analytics Workspace
└── Log Analytics Workspace

Role assignments:
• Foundry Project → Foundry User role on Foundry Account
• Foundry Project → Container Registry Repository Reader role on Azure Container Registry
• Foundry Project → Log Analytics Data Reader role on Log Analytics Workspace

Optional (Teams / M365 Copilot publishing):
└── Azure Bot Service → connected to agent application (Channels auth mode)
```

The diagram above shows how resources are organized hierarchically and which role assignments enable communication between them. The following sections provide detailed configuration requirements for each component.

### Required Azure resources

Each Hosted agent deployment requires these Azure resources to be properly configured:

- **A Foundry account**
    - A role assignment allows the project managed identity to access the account for model access. `Foundry User` is the recommended built-in role.
- **A model deployment (in the account)**
- **A Foundry project (in the account)**
    - The project has a managed identity. The project also gets an agent blueprint and agent identity when its first agent is created.
    - Role assignments allow client users or principals to interact with agents in the project at runtime. `Foundry User` is the recommended built-in role.
    - Some advanced scenarios might require explicit role assignments for the agent identity on the project. For more information, see [Explicit project-level access](#explicit-project-level-access).
- **A Hosted agent (in the project)**
    - The agent automatically gets an agent blueprint and agent identity.
- **An agent version (in the Hosted agent object)**
- **An Azure Container Registry (ACR)**
    - A role assignment allows the project's managed identity to pull images from the registry. [Container Registry Repository Reader][role-acr-reader] is the recommended built-in role.
    - A role assignment allows a user or service principal that deploys the agent to push images to the registry. [Container Registry Repository Writer][role-acr-writer] is the recommended built-in role.
- **An Application Insights component**
- **A Log Analytics workspace (linked to the Application Insights component)**
    - A role assignment allows the project's managed identity to read telemetry for evaluations. [Log Analytics Data Reader][role-log-analytics] is the recommended built-in role.
- **Several connection resources (in the project):**
    - A connection is created for the Azure Container Registry, which the project uses for image pulling.
    - A connection is created for Application Insights, which the project uses to emit telemetry for its agents. This connection doesn't use identity by default.
      
Some set of users or principals needs permission to create and manage these resources. This article assumes a configuration where the Azure resources are all within the same resource group, and shows granting write access over that resource group. This resource group approach is a common configuration for many teams, but your specific setup may vary. If you have a different resource organization strategy, you might need to split up permissions across the resource groups you use.

This list doesn't include networking resources. However, the user or service principal that provisions the Azure resources may also need permission to create and manage virtual networks, subnets, and private endpoints to secure the resources.

### Agent applications

If you use [agent applications](../how-to/agent-applications.md), the list also includes:

- **An agent application (in the project)**
    - The agent application automatically gets an agent blueprint and agent identity. If you configure any explicit role assignments for the Hosted agent's agent identity (such as for [advanced scenarios](#explicit-project-level-access)), repeat those assignments for the agent application's agent identity.
- **An agent deployment (in the agent application)**

## Azure resource setup

### Foundry account setup

Creating a Foundry account requires the `Microsoft.CognitiveServices/accounts/write` permission at the scope of the resource group.

| Built-in role | Scope | Can assignee create a Foundry account? |
| --- | --- | --- |
| Owner | Resource group | ✔ Yes |
| Contributor | Resource group | ✔ Yes |
| Foundry User | Resource group | ✗ No |
| Foundry Project Manager | Resource group | ✗ No |
| Foundry Account Owner | Resource group | ✔ Yes |
| Foundry Owner | Resource group | ✔ Yes |

The project's managed identity needs access to the Foundry account to perform model inference through the project endpoint. The project's access is covered by the `Foundry User` role at the scope of the Foundry account. This role assignment might be created automatically when the project is created, depending on the permissions of the user or service principal creating the project.

More role assignments might be needed if your agent code accesses the account-level OpenAI endpoint directly or other account-level capabilities not proxied by the project endpoint. For more information, see [Account-level access](#account-level-access).

### Model deployment

Creating a model deployment requires the `Microsoft.CognitiveServices/accounts/deployments/write` permission at the scope of the Foundry account.

| Built-in role | Scope | Can assignee deploy a model to a Foundry account? |
| --- | --- | --- |
| Owner | Foundry account | ✔ Yes |
| Contributor | Foundry account | ✔ Yes |
| Foundry User | Foundry account | ✗ No |
| Foundry Project Manager | Foundry account | ✗ No |
| Foundry Account Owner | Foundry account | ✔ Yes |
| Foundry Owner | Foundry account | ✔ Yes |

### Project setup

Creating a Foundry project requires the `Microsoft.CognitiveServices/accounts/projects/write` permission at the scope of the Foundry account.

| Built-in role | Scope | Can assignee create a Foundry project? |
| --- | --- | --- |
| Owner | Foundry account | ✔ Yes |
| Contributor | Foundry account | ✔ Yes |
| Foundry User | Foundry account | ✗ No |
| Foundry Project Manager | Foundry account | ✔ Yes |
| Foundry Account Owner | Foundry account | ✔ Yes |
| Foundry Owner | Foundry account | ✔ Yes |

If the creator of the project has the ability to assign the `Foundry User` role at the scope of the account, the system automatically creates two role assignments:

- The project creator is granted the Foundry User role at the scope of the Foundry account.
- The project's managed identity is granted the Foundry User role at the scope of the Foundry account.

### Azure Container Registry setup

Creating an Azure Container Registry requires the `Microsoft.ContainerRegistry/registries/write` permission at the scope of the resource group.

> [!NOTE]
> For Hosted agents, support for the container registry behind a private network (private endpoint with public network access disabled) depends on when the Foundry project was created. Projects created after June 25, 2026 support a private registry. Projects created before that date require the registry to be reachable over its public endpoint. Existing projects aren't affected. For the full list of network constraints, see [Limitations](../how-to/virtual-networks.md#limitations).
>
> The registry's `azureADAuthenticationAsArmPolicy` policy status must be set to `enabled`. This setting allows ACR to accept Microsoft Entra tokens scoped to Azure Resource Manager. To check or update the status, use [`az acr config authentication-as-arm`](/cli/azure/acr/config/authentication-as-arm).

| Built-in role | Scope | Can assignee create a container registry? |
| --- | --- | --- |
| Owner | Resource group | ✔ Yes |
| Contributor | Resource group | ✔ Yes |
| Foundry User | Resource group | ✗ No |
| Foundry Project Manager | Resource group | ✗ No |
| Foundry Account Owner | Resource group | ✗ No |
| Foundry Owner | Resource group | ✗ No |

The project's managed identity needs permissions to pull the image from ACR. There are two built-in roles suitable to this task, which should be assigned at the ACR registry resource scope:
- [Container Registry Repository Reader][role-acr-reader] (preferred because it models the pull as a data action)
- [AcrPull][role-acrpull]

Creating that role assignment requires the `Microsoft.Authorization/roleAssignments/write` permission at the scope of the ACR registry.

For details on assigning roles in Azure, see [Create Azure role assignments][create-role-assignment].

| Built-in role | Scope | Can assignee create a role assignment? |
| --- | --- | --- |
| Owner | ACR registry | ✔ Yes |
| Contributor | ACR registry | ✗ No |
| Foundry User | ACR registry | ✗ No |
| Foundry Project Manager | ACR registry | ✗ No<sup>1</sup> |
| Foundry Account Owner | ACR registry | ✗ No<sup>1</sup> |
| Foundry Owner | ACR registry | ✗ No |
| Role Based Access Control Administrator | ACR registry | ✔ Yes |

<sup>1</sup> These roles have `roleAssignments/write` but are constrained to only assign the `Foundry User` role, which doesn't cover ACR permissions.

The user or service principal that pushes images to the registry also needs a role assignment. For more information, see the [Hosted agent deployment](#hosted-agent-deployment) section.

### Application Insights and Log Analytics setup

Creating an Application Insights resource requires the `Microsoft.Insights/components/write` permission at the scope of the resource group.

| Built-in role | Scope | Can assignee create an Application Insights resource? |
| --- | --- | --- |
| Owner | Resource group | ✔ Yes |
| Contributor | Resource group | ✔ Yes |
| Foundry User | Resource group | ✗ No |
| Foundry Project Manager | Resource group | ✗ No |
| Foundry Account Owner | Resource group | ✗ No |
| Foundry Owner | Resource group | ✗ No |

Creating a Log Analytics workspace requires the `Microsoft.OperationalInsights/workspaces/write` permission at the scope of the resource group.

| Built-in role | Scope | Can assignee create a Log Analytics workspace? |
| --- | --- | --- |
| Owner | Resource group | ✔ Yes |
| Contributor | Resource group | ✔ Yes |
| Foundry User | Resource group | ✗ No |
| Foundry Project Manager | Resource group | ✗ No |
| Foundry Account Owner | Resource group | ✗ No |
| Foundry Owner | Resource group | ✗ No |

If you plan to use the evaluations feature, the project's managed identity needs permissions to read from the Log Analytics workspace. You can enable this access by granting the `Log Analytics Data Reader` role to the project's managed identity at the scope of the Log Analytics workspace.

Creating that role assignment requires the `Microsoft.Authorization/roleAssignments/write` permission at the scope of the Log Analytics workspace.

For details on assigning roles in Azure, see [Create Azure role assignments][create-role-assignment].

| Built-in role | Scope | Can assignee create a role assignment? |
| --- | --- | --- |
| Owner | Log Analytics workspace | ✔ Yes |
| Contributor | Log Analytics workspace | ✗ No |
| Foundry User | Log Analytics workspace | ✗ No |
| Foundry Project Manager | Log Analytics workspace | ✗ No<sup>1</sup> |
| Foundry Account Owner | Log Analytics workspace | ✗ No<sup>1</sup> |
| Foundry Owner | Log Analytics workspace | ✗ No |
| Role Based Access Control Administrator | Log Analytics workspace | ✔ Yes |

<sup>1</sup> These roles have `roleAssignments/write` but are constrained to only assign the `Foundry User` role, which doesn't cover Log Analytics permissions.

### Connections setup

Creating a connection requires the `Microsoft.CognitiveServices/accounts/projects/connections/write` permission at the scope of the Foundry project.

| Built-in role | Scope | Can assignee create a connection? |
| --- | --- | --- |
| Owner | Foundry project | ✔ Yes |
| Contributor | Foundry project | ✔ Yes |
| Foundry User | Foundry project | ✗ No |
| Foundry Project Manager | Foundry project | ✔ Yes |
| Foundry Account Owner | Foundry project | ✔ Yes |
| Foundry Owner | Foundry project | ✔ Yes |

The user or service principal creating the connections also needs the connection information for the Application Insights component and the container registry. The connection details can be provided by the user or service principal that created those resources, or by having read access over those resources.

> [!NOTE]
> Hosted agents often use tools and connections that target more Azure resources. Those resources might require extra role assignments for the calling identity or the agent identity at the target resource scope. For example, tools that access Storage, Azure AI Search, Key Vault, or databases typically require their own data plane permissions in addition to core setup permissions documented in this article.

### Agent applications

If you use agent applications, you need to create an agent application in the Foundry project. Creating an agent application requires the `Microsoft.CognitiveServices/accounts/projects/applications/write` permission at the scope of the Foundry project.

| Built-in role | Scope | Can assignee create an agent application? |
| --- | --- | --- |
| Owner | Foundry project | ✔ Yes |
| Contributor | Foundry project | ✔ Yes |
| Foundry User | Foundry project | ✗ No |
| Foundry Project Manager | Foundry project | ✔ Yes |
| Foundry Account Owner | Foundry project | ✔ Yes |
| Foundry Owner | Foundry project | ✔ Yes |

`agentDeployment` objects are also ARM resources, but they're created as part of the Hosted agent deployment process. For more information, see [Hosted agent deployment](#hosted-agent-deployment).

## Agent creation

Agents are created through a data plane operation. Creating an agent requires the `Microsoft.CognitiveServices/accounts/AIServices/agents/write` permission at the scope of the Foundry project.

| Built-in role | Scope | Can assignee create an agent? |
| --- | --- | --- |
| Owner | Foundry project | ✗ No |
| Contributor | Foundry project | ✗ No |
| Foundry User | Foundry project | ✔ Yes |
| Foundry Project Manager | Foundry project | ✔ Yes |
| Foundry Account Owner | Foundry project | ✗ No |
| Foundry Owner | Foundry project | ✔ Yes |

The agent has implicit access to core capabilities within its own project, such as model inferencing. No explicit role assignment is needed for the standard case. For advanced scenarios that require explicit access, see [Agent access beyond defaults](#agent-access-beyond-defaults).

## Hosted agent deployment

Hosted agent deployment operations are control plane operations. For step-by-step deployment guidance, see [Deploy a Hosted agent][deploy].

### Push an image to the registry

The user or service principal deploying the agent needs permission to push the image to ACR. There are two built-in roles suitable to this task, which should be assigned at the ACR registry resource scope:
- [Container Registry Repository Writer][role-acr-writer] (preferred because it models the push as a data action)
- [AcrPush][role-acrpush]

### Create a new agent version

Creating an agent requires the `Microsoft.CognitiveServices/accounts/AIServices/agents/write` permission at the scope of the Foundry project.

| Built-in role | Scope | Can assignee create an agent version? |
| --- | --- | --- |
| Owner | Foundry project | ✗ No |
| Contributor | Foundry project | ✗ No |
| Foundry User | Foundry project | ✔ Yes |
| Foundry Project Manager | Foundry project | ✔ Yes |
| Foundry Account Owner | Foundry project | ✗ No |
| Foundry Owner | Foundry project | ✔ Yes |

If you use agent applications, you also need to create an `agentDeployment` object that references a newly deployed agent version. This is a management plane operation. Creating an `agentDeployment` object requires the `Microsoft.CognitiveServices/accounts/projects/applications/agentDeployments/write` permission at the scope of the agent application.

| Built-in role | Scope | Can assignee create an `agentDeployment` object? |
| --- | --- | --- |
| Owner | Foundry account | ✔ Yes |
| Contributor | Foundry account | ✔ Yes |
| Foundry User | Foundry account | ✗ No |
| Foundry Project Manager | Foundry account | ✔ Yes |
| Foundry Account Owner | Foundry account | ✔ Yes |
| Foundry Owner | Foundry account | ✔ Yes |

### Update the agent to use the new version

If you use the _agent endpoint_, version selection is configured on the agent object. Updating the agent to use the new version requires the `Microsoft.CognitiveServices/accounts/AIServices/agents/write` permission at the scope of the Foundry project.

| Built-in role | Scope | Can assignee update the agent version? |
| --- | --- | --- |
| Owner | Foundry project | ✗ No |
| Contributor | Foundry project | ✗ No |
| Foundry User | Foundry project | ✔ Yes |
| Foundry Project Manager | Foundry project | ✔ Yes |
| Foundry Account Owner | Foundry project | ✗ No |
| Foundry Owner | Foundry project | ✔ Yes |

If instead you use the _agent application_, version selection is configured on the agent application object. Updating the agent application to use the new `agentDeployment` object requires the `Microsoft.CognitiveServices/accounts/projects/applications/write` permission at the scope of the agent application.

| Built-in role | Scope | Can assignee update the agent application? |
| --- | --- | --- |
| Owner | Foundry account | ✔ Yes |
| Contributor | Foundry account | ✔ Yes |
| Foundry User | Foundry account | ✗ No |
| Foundry Project Manager | Foundry account | ✔ Yes |
| Foundry Account Owner | Foundry account | ✔ Yes |
| Foundry Owner | Foundry account | ✔ Yes |

### Azure Bot Service setup

Publishing your agent to Microsoft Teams or Microsoft 365 Copilot is optional. When you do, the publishing flow performs control plane operations to create an Azure Bot Service resource and configure its channels, then updates either the agent or the agent application to allow requests from Bot Service.

#### Creating the bot service

Creating the bot service resource requires the `Microsoft.BotService/botServices/write` permission at the scope of the resource group.

| Built-in role | Scope | Can assignee create a bot service? |
| --- | --- | --- |
| Owner | Resource group | ✔ Yes |
| Contributor | Resource group | ✔ Yes |
| Foundry User | Resource group | ✗ No |
| Foundry Project Manager | Resource group | ✗ No |
| Foundry Account Owner | Resource group | ✗ No |
| Foundry Owner | Resource group | ✗ No |

> [!NOTE]
> Azure Bot Service is a separate resource type from Foundry. Azure AI–scoped built-in roles don't include `Microsoft.BotService/*` permissions.

#### Configuring channels

Configuring the Teams and Microsoft 365 Extensions channels on the bot service requires the `Microsoft.BotService/botServices/channels/write` permission at the scope of the bot service resource.

| Built-in role | Scope | Can assignee configure channels? |
| --- | --- | --- |
| Owner | Bot service | ✔ Yes |
| Contributor | Bot service | ✔ Yes |
| Foundry User | Bot service | ✗ No |
| Foundry Project Manager | Bot service | ✗ No |
| Foundry Account Owner | Bot service | ✗ No |
| Foundry Owner | Bot service | ✗ No |

#### Updating the agent or agent application

The publishing flow sets Channels (Azure Bot Service) as the authentication mode on the agent or agent application. The object that is updated depends on your scenario:

- **Agent application scenario**: The agent application object is updated. This is a control plane write operation. The same role requirements apply as documented in [Agent applications](#agent-applications-1).
- **Agent endpoint scenario**: The agent object is updated. This is a data plane write operation. The same role requirements apply as documented in [Create a new agent version](#create-a-new-agent-version).

For step-by-step guidance on publishing to Teams or M365 Copilot, see [Publish agents to Microsoft 365 Copilot and Microsoft Teams][publish-copilot].

## Agent interaction

Interacting with the agent requires the calling user or service principal to have a data plane permission. To interact with an _agent application_, they need `Microsoft.CognitiveServices/accounts/AIServices/applications/invoke/action` at the scope of the agent application.

<!-- TODO: Add endpoint interaction permission when available
- To interact with an _agent endpoint_, they need `Microsoft.CognitiveServices/accounts/AIServices/endpoints/interact/action` at the scope of the Foundry project.
-->

| Built-in role | Scope | Can assignee interact with the agent? |
| --- | --- | --- |
| Owner | Foundry project | ✗ No |
| Contributor | Foundry project | ✗ No |
| Foundry User | Foundry project | ✔ Yes |
| Foundry Project Manager | Foundry project | ✔ Yes |
| Foundry Account Owner | Foundry project | ✗ No |
| Foundry Owner | Foundry project | ✔ Yes |

### Delegate the end-user identity

A middle-tier service that authenticates its own end users can scope a session to a specific end user by sending the `x-ms-user-identity` header. To send that header, the calling identity must hold the following data plane permission on the agent:

`Microsoft.CognitiveServices/accounts/AIServices/agents/endpoints/UserIdentityImpersonation/action`

A caller that sends `x-ms-user-identity` without this permission receives a `403`. For how to use delegated identity, see [Isolate hosted agent sessions per user](../how-to/isolate-sessions-per-user.md#isolate-sessions-for-your-own-users).

## Agent observability

### Viewing telemetry data

Accessing agent telemetry data requires read permissions on the Application Insights resource. This includes viewing traces, logs, and metrics through the Azure portal, Foundry portal, APIs, and monitoring tools.

Assign [Monitoring Reader](/azure/role-based-access-control/built-in-roles#monitoring-reader) at the Application Insights resource scope. The `*/read` permissions in this role access the underlying Log Analytics workspace data without requiring a separate workspace-scoped assignment.

If you need to work against the Log Analytics workspace directly, also assign [Log Analytics Reader](/azure/role-based-access-control/built-in-roles#log-analytics-reader) at the workspace scope. If the workspace tables are [protected](/azure/azure-monitor/logs/protected-tables-configure), also assign [Privileged Monitoring Data Reader](/azure/azure-monitor/logs/manage-access?tabs=portal#privileged-monitoring-data-reader) to read the protected tables.

| Built-in role | Scope | Can assignee access agent telemetry data? |
| --- | --- | --- |
| Owner | Application Insights | ✔ Yes |
| Contributor | Application Insights | ✔ Yes |
| Foundry User | Application Insights | ✗ No (sees metrics, but not traces) |
| Foundry Project Manager | Application Insights | ✗ No |
| Foundry Account Owner | Application Insights | ✗ No (sees metrics, but not traces) |
| Foundry Owner | Application Insights | ✗ No |
| Monitoring Reader | Application Insights | ✔ Yes |
| Log Analytics Reader | Log Analytics Workspace | ✔ Yes (from workspace directly) |
| Privileged Monitoring Data Reader | Log Analytics Workspace | ✔ Yes (required for [protected tables](/azure/azure-monitor/logs/protected-tables-configure)) |

#### Cost display in billing currency

Viewing costs in billing currency in the Foundry portal requires the `Microsoft.Billing/billingProperty/read` permission. This permission requires a subscription or billing-account-scoped assignment. Resource group scope doesn't cover this permission.

This permission is for portal display convenience and isn't required for Hosted agent functionality. You can safely omit this permission for most users.

| Built-in role | Scope | Can assignee view costs in billing currency? |
| --- | --- | --- |
| Owner | Subscription | ✔ Yes |
| Contributor | Subscription | ✔ Yes |
| [Cost Management Reader](/azure/role-based-access-control/built-in-roles#cost-management-reader) | Subscription | ✔ Yes |
| Foundry User | Subscription | ✗ No |

## Agent access beyond defaults

By default, an agent has implicit access to core capabilities within its own project. No explicit role assignment or additional configuration is needed for the standard case. Implicit access covers:

- Model inferencing through the project endpoint
- Session storage read and write

Additional permissions might be needed when an agent uses connected tools that access external resources, references data outside its own project, or operates at account-level scope.

### Explicit project-level access

Some advanced scenarios might require explicit role assignments for the agent identity on the Foundry project. This section outlines the permission needs as if the agent didn't have its implicit access to the project.

In the absence of implicit access, the agent identity would need the following permissions at the scope of the Foundry project to perform model inferencing with the project endpoint:

- `Microsoft.CognitiveServices/accounts/AIServices/responses/*`
- `Microsoft.CognitiveServices/accounts/AIServices/agents/storage/read` (for custom definitions, use `Microsoft.CognitiveServices/accounts/AIServices/agents/*/read`)
- `Microsoft.CognitiveServices/accounts/AIServices/agents/storage/write` (for custom definitions, use `Microsoft.CognitiveServices/accounts/AIServices/agents/*/write`)

| Built-in role | Scope | Can assigned agent perform model inferencing? |
| --- | --- | --- |
| Owner | Foundry project | ✗ No |
| Contributor | Foundry project | ✗ No |
| Foundry User | Foundry project | ✔ Yes |
| Foundry Project Manager | Foundry project | ✔ Yes |
| Foundry Account Owner | Foundry project | ✗ No |
| Foundry Owner | Foundry project | ✔ Yes |

> [!TIP]
> `Foundry User` is the least-privilege built-in role that can perform model inferencing with the project endpoint. However, it includes a broader set of permissions than strictly necessary for this operation. To lower the privilege given to your agent, consider creating a custom role with only `Microsoft.CognitiveServices/accounts/AIServices/responses/*`, `Microsoft.CognitiveServices/accounts/AIServices/agents/*/read`, and `Microsoft.CognitiveServices/accounts/AIServices/agents/*/write`. Remember, the default case does not require a role assignment, so you only need to add this in advanced scenarios.

Creating that role assignment requires the `Microsoft.Authorization/roleAssignments/write` permission at the scope of the Foundry project.

For details on assigning roles in Azure, see [Create Azure role assignments][create-role-assignment].

| Built-in role | Scope | Can assignee create a role assignment? |
| --- | --- | --- |
| Owner | Foundry project | ✔ Yes |
| Contributor | Foundry project | ✗ No |
| Foundry User | Foundry project | ✗ No |
| Foundry Project Manager | Foundry project | ✔ Yes for `Foundry User` role<sup>1</sup> |
| Foundry Account Owner | Foundry project | ✔ Yes for `Foundry User` role<sup>1</sup> |
| Foundry Owner | Foundry project | ✗ No |
| Role Based Access Control Administrator | Foundry project | ✔ Yes |

<sup>1</sup> Both `Foundry Project Manager` and `Foundry Account Owner` have a constraint that they can only assign the `Foundry User` role. If you plan to use a custom role definition for the agent to access the project, `Foundry Project Manager` and `Foundry Account Owner` won't be able to assign that custom role.

> [!NOTE]
> Because the role assignment is needed against the agent identity, it can't be created until after the agent is created. Therefore, the user or principal that creates the agent also needs permission to create role assignments. [Foundry Project Manager][role-project-manager] at the project scope is the recommended role assignment for agent creators in this scenario, as that role includes both the required data plane permissions and the ability to assign the `Foundry User` role.

### Account-level access

When you use the Foundry SDK and the project endpoint for model inference, the project proxies inference calls to the account-level deployment using its own managed identity. However, if your agent code bypasses the project endpoint and calls the account-level OpenAI endpoint directly (for example, `https://{account}.cognitiveservices.azure.com`), the agent's identity needs one of the following roles at account scope:

- [Cognitive Services OpenAI User][role-openai-user] - covers only OpenAI data actions.
- [Foundry User][role-ai-user] - covers all CognitiveServices data actions on the account.

Account-level capabilities aren't proxied by the project endpoint. These capabilities include Speech, Content Safety, Computer Vision, Document Intelligence, Language, and Translator. They require a role assignment at account scope if your agent accesses them directly. For these capabilities, assign one of the following roles at account scope:

- [Cognitive Services User][role-cog-services-user] - covers Speech, Vision, Language, and other non-OpenAI capabilities.
- [Foundry User][role-ai-user] - covers all CognitiveServices data actions, including OpenAI and the capabilities listed previously, with a single grant.

## Related content

- [Hosted agents][hosted-agents]: Learn the Hosted agent architecture and lifecycle.
- [Role-based access control for Microsoft Foundry][foundry-rbac]: Review built-in roles, scopes, and assignment patterns.
- [Agent identity][agent-identity]: Understand how agent identity and project managed identity differ.

<!--> Link definitions <!-->

[hosted-agents]: ./hosted-agents.md
[deploy]: ../how-to/deploy-hosted-agent.md
[lifecycle]: ../how-to/manage-hosted-agent.md
[publish-copilot]: ../how-to/publish-copilot.md

[create-role-assignment]: /azure/role-based-access-control/role-assignments-steps

[foundry-rbac]: ../../concepts/rbac-foundry.md
[agent-identity]: ./agent-identity.md

[role-owner]: /azure/role-based-access-control/built-in-roles#owner
[role-contributor]: /azure/role-based-access-control/built-in-roles#contributor
[role-rbac-admin]: /azure/role-based-access-control/built-in-roles#role-based-access-control-administrator
[role-ai-user]: /azure/ai-foundry/concepts/rbac-foundry#azure-ai-user
[role-project-manager]: /azure/ai-foundry/concepts/rbac-foundry#azure-ai-project-manager
[role-account-owner]: /azure/ai-foundry/concepts/rbac-foundry#azure-ai-account-owner
[role-ai-owner]: /azure/ai-foundry/concepts/rbac-foundry#azure-ai-owner
[role-acr-reader]: /azure/role-based-access-control/built-in-roles#container-registry-repository-reader
[role-acr-writer]: /azure/role-based-access-control/built-in-roles#container-registry-repository-writer
[role-acrpull]: /azure/role-based-access-control/built-in-roles#acrpull
[role-acrpush]: /azure/role-based-access-control/built-in-roles#acrpush
[role-log-analytics]: /azure/role-based-access-control/built-in-roles#log-analytics-data-reader
[role-openai-user]: /azure/role-based-access-control/built-in-roles#cognitive-services-openai-user
[role-cog-services-user]: /azure/role-based-access-control/built-in-roles#cognitive-services-user
