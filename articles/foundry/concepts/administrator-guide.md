---
title: Elevated-role tasks in Microsoft Foundry
description: Learn which elevated roles are required for administrator tasks in Microsoft Foundry, why each role is needed, and where to find detailed procedures.
author: sdgilley
ms.author: sgilley
ms.service: microsoft-foundry
ms.topic: concept-article
ms.date: 04/28/2026
ai-usage: ai-assisted
#customer intent: As an IT administrator, I want to understand which elevated roles are required for each area of Microsoft Foundry so that I can plan role assignments and troubleshoot permission errors.
---

# Elevated-role tasks in Microsoft Foundry

Developers who have the **Foundry User** role at the Foundry resource or project scope can build agents, run inferences, and use most Foundry features. However, many administrative tasks require elevated roles such as **Owner**, **Contributor**, **Foundry Account Owner**, or other specialized roles.

This article explains which elevated roles are needed for each area of Foundry administration, why those roles are required, and links to the detailed procedures. Use it as a reference when developers encounter permission errors or when you plan role assignments for a new environment.

> [!NOTE]
> Preview features, hosted options, and specific backing resources can require additional roles or data-plane permissions. Check the linked articles for the exact requirements in your scenario.

For background on Foundry role definitions, see [Role-based access control for Microsoft Foundry](../concepts/rbac-foundry.md).


## Key concepts

- **Control plane** — Operations that manage Azure resources (create, delete, configure). Governed by Azure RBAC roles like Owner and Contributor.
- **Data plane** — Operations that use a resource's runtime capabilities (read blobs, query indexes). Governed by data roles like Storage Blob Data Contributor.
- **Managed identity** — An automatically managed Microsoft Entra identity that authenticates to backing resources without stored credentials. In Foundry, the project managed identity is the identity that your project uses at runtime. Some setups also rely on the account-level shared identity for resource access. Use the identity name that matches your scenario instead of treating the two terms as interchangeable.
- **Foundry resource** — The Azure resource (of type `Microsoft.CognitiveServices/accounts`) that hosts your Foundry projects.
- **Scope** — The level at which a role assignment applies: subscription, resource group, resource, or project. Roles assigned at a higher scope inherit downward.

## Environment setup overview

When you provision a new Foundry environment, the tasks follow this general order:

1. **Create a Foundry resource** — Required before all other tasks.
1. **Create one or more projects** — Agents, models, and connections live inside projects.
1. **Assign roles to developers** — Developers need **Foundry User** for general access. Model deployment requires a separate role.
1. **Deploy models** — Requires **Foundry Account Owner**.
1. **Configure agent infrastructure** (if needed).
1. **Configure networking** (if needed).
1. **Set up guardrails and policies**.
1. **Enable monitoring**.

> [!TIP]
> **Small team (1-5 developers)?** Assign **Owner** to yourself at the resource group scope and **Foundry User** to each developer at the Foundry resource scope. This assignment covers most administrative tasks. For larger teams, use Microsoft Entra groups and scope roles per project.

The remaining sections explain the role requirements for each area. For a summary of all elevated roles, see [Quick reference: role summary](#quick-reference-role-summary).

## Create and configure Foundry resources

Creating Foundry resources and projects requires control-plane permissions that developers typically don't have. These operations modify Azure Resource Manager objects, so they need roles like **Contributor** or **Foundry Account Owner** at the subscription or resource group level.

| Task | Minimum role | Scope | Details |
|------|-------------|-------|---------|
| Create a Foundry resource | **Contributor**, **Foundry Account Owner**, *or* **Foundry Owner** | Subscription or resource group | [Create your first resource](../../ai-services/multi-service-resource.md) |
| Create a Foundry project | **Contributor**, **Foundry Account Owner**, *or* **Foundry Owner** | Foundry resource | [Create and manage projects](../how-to/create-projects.md) |
| Upgrade from Azure OpenAI Service | **Owner** *or* **Contributor** | Azure OpenAI resource | [Upgrade from Azure OpenAI Service](../how-to/upgrade-azure-openai.md) |
| Recover or purge deleted accounts | **Contributor** | Subscription | [Recover or purge deleted resources](../../ai-services/recover-purge-resources.md) |
| Create resources using Bicep | **Contributor** *or* **Owner** | Resource group | [Create resources using Bicep template](../how-to/create-resource-template.md) |

For step-by-step instructions using the Azure CLI, Bicep, or the portal, see [Create your first resource](../../ai-services/multi-service-resource.md) and [Create and manage projects](../how-to/create-projects.md).

## Assign roles to team members

To assign any role to a user, you need the **Owner** or **User Access Administrator** role at the target scope. The **Foundry Account Owner** and **Foundry Project Manager** roles can conditionally assign the **Foundry User** role only.

> [!NOTE]
> A role assigned at resource group scope applies to all Foundry resources and projects within that group. Assign at the narrowest scope that meets your needs.

| Task | Minimum role | Scope | Details |
|------|-------------|-------|---------|
| Assign **Foundry User** to developers | **Owner** *or* **User Access Administrator** | Foundry resource or project | [Role-based access control](../concepts/rbac-foundry.md) |
| Assign **Foundry User** (conditional) | **Foundry Account Owner** *or* **Foundry Project Manager** | Foundry resource or project | [Role-based access control](../concepts/rbac-foundry.md) |
| Create custom RBAC roles | **Owner** | Subscription or resource group | [Role-based access control](../concepts/rbac-foundry.md) |
| Assign custom roles | **User Access Administrator** *or* **Role Based Access Control Administrator** | Target scope | [Role-based access control](../concepts/rbac-foundry.md) |
| Manage roles with Microsoft Entra groups | **Owner** *or* **User Access Administrator** | Target scope | [Role-based access control](../concepts/rbac-foundry.md) |

> [!TIP]
> Use Microsoft Entra groups to simplify role assignments. Create a security group, assign it the appropriate role, and add developers as members. See [Role-based access control](../concepts/rbac-foundry.md) for a walkthrough.

### Scope considerations

- Assign the **Foundry User** role at the **Foundry resource** scope to grant access to all projects in the resource.
- Assign at the **project** scope to limit access to a single project.
- For organizations that use [Microsoft Entra Privileged Identity Management (PIM)](/entra/id-governance/privileged-identity-management/pim-configure), consider making elevated role assignments eligible rather than permanent. Eligible assignments require [just-in-time activation](/entra/id-governance/privileged-identity-management/pim-resource-roles-activate-your-roles), which reduces standing privilege exposure.

For step-by-step role assignment procedures, see [Role-based access control for Microsoft Foundry](../concepts/rbac-foundry.md) and [Assign Azure roles](/azure/role-based-access-control/role-assignments-steps).

> [!NOTE]
> Role assignments can take up to five minutes to propagate. If a developer reports access denied immediately after assignment, ask them to wait and retry. See [Troubleshoot common permission errors](#troubleshoot-common-permission-errors) for common causes.

## Configure agent infrastructure

Agent setup is the most permission-intensive area in Foundry. The required roles depend on which setup option you choose.

| Setup option | Choose when | Prerequisites | Trade-off |
|---|---|---|---|
| **[Standard](#standard-agent-setup)** | You need full control over data residency and resource provisioning | Provisioned Cosmos DB, AI Search, and Storage resources in your resource group | You manage provisioning and RBAC for Cosmos DB, Search, and Storage |
| **[Hosted](#hosted-agent-setup)** | You want the fastest path with minimal setup | None — Foundry provisions backing resources for you | Foundry manages backing resources; less networking control |
| **[BYO resources](#bring-your-own-resources)** | You already have Cosmos DB, Search, or Storage with specific compliance requirements | Existing Cosmos DB, AI Search, or Storage resources with network access configured | You attach existing resources and manage their RBAC |

Review the subsection that matches your setup option. Skip the others - you can return to them later if your requirements change.

### Standard agent setup

Standard agent setup requires you to provision and manage your own Azure Cosmos DB, Azure AI Search, and Azure Storage resources. This approach gives you full control over data residency but requires assigning data-plane roles to the project managed identity on each backing resource.

| Task | Minimum role | Scope | Details |
|------|-------------|-------|---------|
| Assign cross-service roles (Cosmos DB, Search, Storage) | **Owner** *or* **Role Based Access Control Administrator** | Resource group | [Standard agent setup](../agents/concepts/standard-agent-setup.md) |
| Provision agent resources | **Foundry Account Owner** *or* **Owner** | Subscription | [Set up your agent resources](../agents/environment-setup.md) |

Assign the following data-plane roles to the Foundry project managed identity on the backing resources:

| Resource | Role |
|----------|------|
| Azure Cosmos DB | **Cosmos DB Built-in Data Contributor** |
| Azure AI Search | **Search Index Data Contributor**, **Search Service Contributor** |
| Azure Storage (`azureml-blobstore`) | **Storage Blob Data Contributor** |
| Azure Storage (`agents-blobstore`) | **Storage Blob Data Owner** |

> [!NOTE]
> **Cosmos DB Built-in Data Contributor** is a Cosmos DB data-plane role. Assign it through the Azure CLI (`az cosmosdb sql role assignment create`) or Bicep - not through the standard **Access control (IAM)** blade. For details, see [Configure role-based access control for Azure Cosmos DB](/azure/cosmos-db/how-to-connect-role-based-access-control).

For the full provisioning procedure and Bicep templates, see [Standard agent setup](../agents/concepts/standard-agent-setup.md).

### Hosted agent setup

Hosted agent setup is still the fastest path for agent runtime infrastructure, but it has explicit resource and RBAC prerequisites. In addition to your Foundry account and project, plan for Azure Container Registry (ACR), Application Insights, and a linked Log Analytics workspace.

| Task area | Minimum role | Scope | Notes |
|---|---|---|---|
| Create ACR, Application Insights, and Log Analytics resources | **Contributor** *or* **Owner** | Resource group | Required when your hosted deployment flow creates these resources. |
| Create Hosted agents and agent versions (data plane) | **Foundry User**, **Foundry Project Manager**, *or* **Foundry Owner** | Foundry project | **Owner**/**Contributor** alone are insufficient for data-plane agent create or update operations. |
| Create project connections | **Foundry Project Manager**, **Foundry Account Owner**, **Foundry Owner**, **Contributor**, *or* **Owner** | Foundry project | Required for ACR and observability connections. |
| Assign ACR pull/read role to project managed identity | **Owner** *or* **Role Based Access Control Administrator** | ACR resource | Assign **Container Registry Repository Reader** (or **AcrPull**). |
| Push images to ACR for deployment | **Container Registry Repository Writer** (or **AcrPush**) | ACR resource | Required for the user or principal that pushes agent images. |
| Read agent telemetry for evaluations | **Log Analytics Data Reader** | Log Analytics workspace | Needed by the project managed identity for evaluations that read workspace data. |

> [!NOTE]
> **Foundry Project Manager** and **Foundry Account Owner** can assign only the **Foundry User** role in their constrained role-assignment scope. Use **Owner** or **Role Based Access Control Administrator** when you need role assignments on external resources such as ACR or Log Analytics.

For detailed instructions on hosted agent permissions, see [Hosted agent permissions reference](../agents/concepts/hosted-agent-permissions.md).

For step-by-step instructions, see [Deploy a hosted agent](../agents/how-to/deploy-hosted-agent.md). 

### Bring your own resources

Use this option when you already have Azure Cosmos DB, AI Search, or Storage resources with specific compliance requirements. You attach existing resources to a Foundry project and assign the required data-plane roles to the project managed identity.

| Task | Minimum role | Scope | Details |
|------|-------------|-------|---------|
| Attach your own resources | **Foundry Account Owner** *or* **Owner** | Subscription | [Use your own Azure resources](../agents/how-to/use-your-own-resources.md) |
| Assign roles to managed identity | **Owner** *or* **User Access Administrator** | Target resource | [Use your own Azure resources](../agents/how-to/use-your-own-resources.md) |

For detailed instructions, see [Use your own Azure resources](../agents/how-to/use-your-own-resources.md).

### Agent tools with elevated requirements

Several agent tools require **Contributor** or higher to provision or configure their backing resources.

#### Infrastructure tools

| Tool | Minimum role | Scope | Details |
|------|-------------|-------|---------|
| Bing grounding | **Contributor** *or* **Owner** | Subscription or resource group | [Bing tools](../agents/how-to/tools/bing-tools.md) |
| Browser automation (preview) | **Contributor** *or* **Owner** | Resource group | [Browser automation](../agents/how-to/tools/browser-automation.md) |
| AI Search | **Search Index Data Contributor**, **Search Service Contributor** | AI Search resource | [AI Search tool](../agents/how-to/tools/ai-search.md) |
| File search | **Storage Blob Data Contributor** | Project storage account | [File search](../agents/how-to/tools/file-search.md) |
| Custom code interpreter (preview) | **Container Apps ManagedEnvironments Contributor** + **Foundry Owner** | Subscription or resource group | [Custom code interpreter](../agents/how-to/tools/custom-code-interpreter.md) |

#### Integration tools

| Tool | Minimum role | Scope | Details |
|------|-------------|-------|---------|
| OpenAPI tool | **Contributor** *or* **Owner** | Foundry project | [OpenAPI tool](../agents/how-to/tools/openapi.md) |
| MCP tool | **Contributor** *or* **Owner** | Foundry project | [Model Context Protocol tool](../agents/how-to/tools/model-context-protocol.md) |
| Agent-to-agent (preview) | **Contributor** *or* **Owner** | Foundry resource | [Agent-to-agent](../agents/how-to/tools/agent-to-agent.md) |
| Azure Speech | **Storage Blob Data Contributor** | Storage account | [Azure Speech tool](../agents/how-to/tools/azure-ai-speech.md) |

### Publish agents

Publishing promotes an agent from a development asset inside a Foundry project into a managed Agent Application resource with a stable endpoint. To publish an agent, you need the **Foundry Project Manager** role on the Foundry resource scope.

| Task | Minimum role | Scope | Details |
|------|-------------|-------|---------|
| Publish an agent as an Agent Application | **Foundry Project Manager** | Foundry resource | [Publish and share agents](../agents/how-to/publish-agent.md) |
| Invoke a published Agent Application | **Foundry User** | Agent Application resource | [Invoke Agent Applications](../agents/how-to/publish-responses.md) |
| Publish an agent to Microsoft 365 and Teams | **Foundry Project Manager** | Foundry project | [Publish agents to Microsoft 365 and Teams](../agents/how-to/publish-copilot.md) |
| Reassign RBAC to published agent identity | **Owner** *or* **User Access Administrator** | Target resource | [Agent identity concepts](../agents/concepts/agent-identity.md) |

> [!IMPORTANT]
> When you publish an agent, it receives a new distinct Entra agent identity. Permissions assigned to the project's shared identity don't transfer. Reassign RBAC roles on any downstream resources the agent accesses (storage, search, Key Vault) to the new agent identity. For details, see [Agent identity concepts](../agents/concepts/agent-identity.md).

## Deploy and manage models

To deploy a model, you need the **Foundry Account Owner** role on the Foundry resource. Some scenarios, such as marketplace models or provisioned throughput, require higher roles. The following table lists all model-related tasks and their role requirements.


| Task | Minimum role | Scope | Details |
|------|-------------|-------|---------|
| Deploy a model from the catalog | **Foundry Account Owner** | Foundry resource | [Create model deployments](../foundry-models/how-to/create-model-deployments.md) |
| Deploy Foundry Models | **Foundry Account Owner** | Foundry resource | [Deploy Foundry Models](../foundry-models/how-to/deploy-foundry-models.md) |
| Deploy provisioned throughput | **Foundry Account Owner** | Foundry resource | [Provisioned throughput](../openai/how-to/provisioned-get-started.md) |
| Deploy marketplace models | **Contributor** | Subscription | [Deploy Foundry Models](../foundry-models/how-to/deploy-foundry-models.md) |
| Deploy Fireworks models | **Foundry Owner** (project) + Subscription **Contributor** | Subscription and project | [Enable Fireworks models](../how-to/fireworks/enable-fireworks-models.md) |
| Fine-tune a model | **Foundry Owner** (*or* **Foundry User** + **Foundry Account Owner**) | Foundry resource | [Role-based access control](../concepts/rbac-foundry.md) |
| Deploy fine-tuned model cross-tenant | **Foundry Project Manager** | Source and destination resources | [Fine-tuning deployment](../openai/how-to/fine-tuning.md) |
| View quotas | **Foundry Account Owner** | Subscription | [Manage quotas](../how-to/quota.md) |
| Request quota increases | **Contributor** | Subscription | [Manage quotas](../how-to/quota.md) |
| Edit quotas | **Foundry Account Owner** | Foundry resource and subscription | [Manage quotas](../how-to/quota.md) |
| Create content blocklists | **Foundry Account Owner** | Azure OpenAI resource | [Use blocklists](../openai/how-to/use-blocklists.md) |

Marketplace model deployments require subscription-level access because they create billing agreements. Fine-tuning requires **Foundry Owner** because it creates training jobs that consume compute and storage. Before deploying any model, verify that your subscription has sufficient quota for the target model and region - see [Manage quotas](../how-to/quota.md).


For step-by-step deployment instructions, see [Create model deployments](../foundry-models/how-to/create-model-deployments.md).

## Configure security and networking

Network and encryption configurations require elevated roles on multiple resources. These configurations span the Foundry resource, virtual networks, DNS zones, and Key Vault, so you typically need multiple roles.

### Private endpoints

Private endpoints restrict access to your Foundry resource to traffic from specific virtual networks. Configuring a private endpoint requires roles on three different resources.

| Task | Minimum role | Scope | Details |
|------|-------------|-------|---------|
| Create private endpoint | **Contributor** *or* **Owner** | Foundry resource | [Configure private link](../how-to/configure-private-link.md) |
| Configure VNet | **Network Contributor** | Virtual network | [Configure private link](../how-to/configure-private-link.md) |
| Configure private DNS zone | **Private DNS Zone Contributor** | DNS zone | [Configure private link](../how-to/configure-private-link.md) |

For step-by-step instructions, see [Configure private link](../how-to/configure-private-link.md).

### Managed virtual networks

A managed virtual network isolates Foundry resources behind a Foundry-managed network. This setup simplifies network configuration compared to bringing your own VNet.

| Task | Minimum role | Scope | Details |
|------|-------------|-------|---------|
| Configure managed VNet | **Owner** *or* **Contributor** | Foundry resource | [Managed virtual network](../how-to/managed-virtual-network.md) |
| Assign RBAC to resources in managed VNet | **Owner** *or* **Role Based Access Control Administrator** | Target resources | [Managed virtual network](../how-to/managed-virtual-network.md) |

### Network security perimeter

A network security perimeter provides a centralized way to manage network access across multiple Azure resources. Add your Foundry resource to an existing perimeter to enforce consistent network rules.

| Task | Minimum role | Scope | Details |
|------|-------------|-------|----------|
| Add Foundry to network security perimeter (preview) | **Owner**, **Contributor**, *or* **Network Contributor** | Foundry resource | [Network security perimeter](../how-to/add-foundry-to-network-security-perimeter.md) |

### Customer-managed keys

By using customer-managed keys (CMK), you can encrypt Foundry data with keys you control in Azure Key Vault. CMK requires roles on both the Key Vault and the Foundry resource because you grant the managed identity access to your key and then configure the resource to use it.

| Task | Minimum role | Scope | Details |
|------|-------------|-------|---------|
| Assign RBAC on Key Vault | **Owner** *or* **User Access Administrator** | Key Vault | [Configure customer-managed keys](../concepts/encryption-keys-portal.md) |
| Assign **Key Vault Crypto User** to managed identity | **Owner** *or* **User Access Administrator** | Key Vault | [Configure customer-managed keys](../concepts/encryption-keys-portal.md) |
| Configure encryption on Foundry resource | **Contributor** *or* **Owner** | Foundry resource | [Configure customer-managed keys](../concepts/encryption-keys-portal.md) |

For the full procedure, see [Configure customer-managed keys](../concepts/encryption-keys-portal.md).

### Key Vault connections

A Key Vault connection lets Foundry projects access secrets, certificates, and keys stored in Azure Key Vault without embedding credentials in code. Create a connection when your agents or deployed models need to retrieve API keys or certificates at runtime.

| Task | Minimum role | Scope | Details |
|------|-------------|-------|---------|
| Create a Key Vault connection | **Key Vault Contributor** + **Key Vault Administrator** | Key Vault | [Store secrets in your Azure Key Vault](../how-to/set-up-key-vault-connection.md) |

## Set up guardrails and policies

Set up guardrails and Azure Policy assignments to restrict which models, tools, and configurations are available in your Foundry environment. You need admin-level roles to complete these tasks because they enforce governance boundaries across all developers in a subscription or resource group.

| Task | Minimum role | Scope | Details |
|------|-------------|-------|---------|
| Create guardrails | **Foundry Account Owner** or higher | Foundry resource | [Create guardrails](../guardrails/how-to-create-guardrails.md) |
| Create guardrail policies | **Owner** *or* **Resource Policy Contributor** | Subscription or resource group | [Create guardrail policies](../control-plane/quickstart-create-guardrail-policy.md) |
| Create model deployment policies | **Owner** *or* **Resource Policy Contributor** | Subscription or resource group | [Model deployment policy](../how-to/model-deployment-policy.md) |
| Create custom policy definitions | **Resource Policy Contributor** (least privilege) *or* **Owner** | Target scope | [Create custom policy definitions](../how-to/custom-policy-definition.md) |
| Configure third-party guardrails | **Owner** (subscription) + **Key Vault Administrator** | Subscription and Key Vault | [Third-party integrations](../guardrails/third-party-integrations.md) |
| Enforce token limits via AI Gateway | **API Management Service Contributor** *or* **Owner** | APIM resource | [Enforce token limits](../control-plane/how-to-enforce-limits-models.md) |
| Govern agent tools via AI Gateway | **API Management Service Contributor** *or* **Owner** | APIM instance | [Govern agent tools](../agents/how-to/tools/governance.md) |

For a walkthrough of creating your first guardrail, see [Create guardrails](../guardrails/how-to-create-guardrails.md). For model deployment policies, see [Model deployment policy](../how-to/model-deployment-policy.md).

## Manage compliance and monitoring

Compliance and monitoring tasks span Azure RBAC roles and Microsoft Entra directory roles. Understanding the distinction is important - you assign directory roles in the [Microsoft Entra admin center](https://entra.microsoft.com), not in the Azure portal's **Access control (IAM)** blade.

| Task | Minimum role | Scope | Details |
|------|-------------|-------|---------|
| Enable Microsoft Defender for Cloud | **Security Admin** *or* **Owner** | Subscription | [Manage compliance and security](../control-plane/how-to-manage-compliance-security.md) |
| Configure Microsoft Purview | **Foundry Account Owner** | Foundry resource | [Manage compliance and security](../control-plane/how-to-manage-compliance-security.md) |
| Configure diagnostic settings | **Monitoring Contributor** | Foundry resource | [Monitor models](../foundry-models/how-to/monitor-models.md) |
| Configure Application Insights tracing | **Contributor** or higher | Application Insights resource | [Trace agent framework](../observability/how-to/trace-agent-framework.md) |
| Govern agent infrastructure (Entra admin) | **Global Administrator** *or* **Microsoft Entra AI Administrator** | Microsoft Entra tenant | [Govern agent infrastructure as Entra admin](../control-plane/govern-agent-infrastructure-entra-admin.md) |
| Configure Conditional Access policies | **Conditional Access Administrator** | Microsoft Entra ID | [MCP security best practices](../mcp/security-best-practices.md) |

> [!IMPORTANT]
> The **Global Administrator** elevation grants **User Access Administrator** at root scope (`/`) across all subscriptions. Remove this elevation after you complete the required tasks. For details, see [Govern agent infrastructure as Entra admin](../control-plane/govern-agent-infrastructure-entra-admin.md).

For step-by-step monitoring setup, see [Monitor models](../foundry-models/how-to/monitor-models.md) and [Trace agent framework](../observability/how-to/trace-agent-framework.md).

## Configure storage and data-plane access

Foundry agents, evaluations, and several tools require data-plane roles on storage and search resources. Assign these roles to the Foundry project managed identity - not to human users - so the service can access backing resources at runtime.

The following table includes an **Assigned to** column because these roles apply to managed identities rather than to human users.

| Task | Minimum role to assign | Assigned to | Target resource | Details |
|------|----------------------|-------------|-----------------|---------|
| BYO storage for Foundry | **Storage Blob Data Contributor** | Project managed identity | Storage account | [Connect to your own storage](../how-to/bring-your-own-azure-storage-foundry.md) |
| BYO storage for Speech/Language | **Storage Blob Data Contributor** | Foundry managed identity | Storage account | [Connect to your own storage for Speech/Language](../how-to/bring-your-own-azure-storage-speech-language-services.md) |
| Run evaluations with Entra ID storage | **Storage Blob Data Owner** | User and project resource | Storage account | [Evaluation regions and limits](../concepts/evaluation-regions-limits-virtual-network.md) |
| Foundry IQ indexing (preview) | **Search Index Data Contributor** | Project managed identity | AI Search resource | [Foundry IQ connection](../agents/how-to/foundry-iq-connect.md) |

> [!NOTE]
> Assigning data-plane roles like **Storage Blob Data Contributor** to a managed identity requires **Owner** or **User Access Administrator** on the target resource.

## Set up disaster recovery

Disaster recovery for Foundry covers two scenarios: failover of the Foundry resource itself (high availability) and failover of agent backing resources. Agent service DR is especially role-intensive because it requires access to Cosmos DB, AI Search, and Storage in addition to the Foundry resource.

| Task | Minimum role | Scope | Details |
|------|-------------|-------|----------|
| Configure high availability | **Owner** *or* **Contributor** + **User Access Administrator** | Resource group | [High availability and resiliency](../how-to/high-availability-resiliency.md) |
| Agent service DR (operator) | **Owner** *or* **Contributor** + **DocumentDB Account Contributor** + **Search Service Contributor** + **Storage Blob Data Contributor** | Resource group and backing resources | [Agent service disaster recovery](../how-to/agent-service-operator-disaster-recovery.md) |
| Agent service DR (platform) | **Contributor** *or* **Owner** + **Storage Account Contributor** | Foundry resources and storage | [Disaster recovery from platform outage](../how-to/agent-service-platform-disaster-recovery.md) |

For detailed DR procedures, see [High availability and resiliency](../how-to/high-availability-resiliency.md) and [Agent service disaster recovery](../how-to/agent-service-operator-disaster-recovery.md).

## Configure connections and integrations

Foundry integrates with API Management, MCP servers, and external services. Most integration tasks require at least **Contributor** because they create or modify Azure resources. Linking Foundry to an AI Gateway requires the **Foundry Account Owner** role because it changes the account's configuration.

| Task | Minimum role | Scope | Details |
|------|-------------|-------|---------|
| Add connections to Foundry | **Foundry User**, **Foundry Owner**, *or* **Contributor** | Foundry project | [Create a connection](../how-to/connections-add.md) |
| Enable AI Gateway (APIM) | **Contributor** *or* **Owner** | Resource group or subscription | [Enable AI API Management gateway](../configuration/enable-ai-api-management-gateway-portal.md) |
| Link Foundry to AI Gateway | **Foundry Account Owner** *or* **Foundry Owner** | Foundry resource | [Enable AI API Management gateway](../configuration/enable-ai-api-management-gateway-portal.md) |
| Configure MCP server access | **Contributor** or higher | Foundry project | [Get started with MCP](../mcp/get-started.md) |
| Build your own MCP server | **Contributor** | Resource group | [Build your own MCP server](../mcp/build-your-own-mcp-server.md) |
| Manage MCP access (role assignment) | **Owner** *or* **User Access Administrator** | Target resource | [MCP security best practices](../mcp/security-best-practices.md) |
| Configure Claude Code | **Contributor** *or* **Owner** | Resource group | [Configure Claude Code](../foundry-models/how-to/configure-claude-code.md) |
| Manage tags on resources | **Contributor** *or* **Tag Contributor** | Target scope | [Disable preview features](../how-to/disable-preview-features.md) |

## Quick reference: role summary

The following table summarizes the primary elevated roles and when administrators need them. Use it to quickly identify which role to assign for a given task category.

| Role | When it's needed |
|------|-----------------|
| **Owner** | Role assignments, custom RBAC roles, policy creation, subscription-level operations |
| **Contributor** | Resource provisioning, marketplace model deployment, MCP write operations, private endpoints |
| **Foundry Account Owner** | Create Foundry resources and projects, model deployment, quota management, content blocklists, guardrails, Purview integration, conditional role assignment |
| **Foundry Project Manager** | Publish agents, conditional **Foundry User** role assignment |
| **Foundry Owner** | Fine-tuning, hosted agent deployment, combined data-plane and control-plane operations |
| **User Access Administrator** | Assign roles when you don't have Owner; CMK Key Vault RBAC; container registry access |
| **Storage Blob Data Contributor/Owner** | Agent backing storage, evaluations, BYO storage, file search tool |
| **Search Index Data Contributor** | AI Search-backed agent tools, Foundry IQ indexing |
| **Key Vault Administrator** | Key Vault connections, third-party guardrails |
| **Resource Policy Contributor** | Azure Policy assignments for model deployment and custom policies |
| **Global Administrator** | Tenant-level agent governance, access elevation |
| **Security Admin** | Microsoft Defender for Cloud |
| **Monitoring Contributor** | Diagnostic settings |
| **Network Contributor** | VNet configuration, network security perimeter |

## Troubleshoot common permission errors

When developers encounter permission errors, use the task tables in this article to identify the required role. The following table maps common error messages to likely causes and resolutions.

| Error message | Likely cause | Resolution |
|--------------|-------------|------------|
| `AuthorizationFailed` or `The client does not have authorization to perform action` | Missing control-plane role (**Owner**, **Contributor**, or resource-specific role) | Identify the task in this article, note the minimum role and scope, then assign the role. |
| Agent create or update fails even with **Owner**/**Contributor** | Missing Foundry data-plane role on the project | Assign **Foundry User**, **Foundry Project Manager**, or **Foundry Owner** at the project scope. See [Hosted agent setup](#hosted-agent-setup). |
| `Creating that role assignment requires Microsoft.Authorization/roleAssignments/write` (or equivalent) | Caller has **Foundry Project Manager** or **Foundry Account Owner**, but needs to assign roles outside the allowed **Foundry User** constraint | Use **Owner** or **Role Based Access Control Administrator** at the target resource scope (for example, ACR or Log Analytics). |
| `ForbiddenError` on model deployment | Missing **Foundry Account Owner** on the Foundry resource | See [Deploy and manage models](#deploy-and-manage-models). |
| `LinkedAuthorizationFailed` during resource creation | Missing permissions on a linked resource (storage, Key Vault, or search) | Check [Configure agent infrastructure](#configure-agent-infrastructure) for cross-service role requirements. |
| Agent returns `403` at runtime | Missing data-plane role on a backing resource | Verify the managed identity role assignments in the [Standard agent setup](#standard-agent-setup) table. |
| Legacy `Azure AI Developer` role assigned, but Foundry tasks still fail | Legacy hub-project role assignment doesn't map to current Foundry role requirements | Use the role mappings in this article and assign the required role at the correct scope for the failing task. |
| **Publish Agent** button is disabled | Missing **Foundry Project Manager** on the Foundry resource scope | Assign **Foundry Project Manager** on the Foundry resource (account) scope, not just on the project scope. See [Publish agents](#publish-agents). |
| `RoleAssignmentExists` | Role already assigned at the same scope | No action needed. |
| Model name or region error (for example, `InvalidModelName`) | Model not available in the selected region | Check [Model region availability](/azure/ai-services/openai/concepts/models#model-summary-table-and-region-availability) and redeploy in a supported region. |
| Quota error (for example, `InsufficientQuota`) | Deployment exceeds the subscription's TPM quota for the model/region | See [Manage quotas](../how-to/quota.md) to view current usage and request increases. |
| `Cosmos DB Built-in Data Contributor` not found in IAM | Cosmos DB data-plane roles aren't visible in the portal's **Access control (IAM)** blade | Assign this role through the Azure CLI (`az cosmosdb sql role assignment create`) or Bicep. See the [Standard agent setup](#standard-agent-setup) NOTE for details. |
| `Could not resolve host` or DNS resolution failure after private endpoint setup | Private DNS zone not linked to the virtual network, or DNS records not propagated | Verify the private DNS zone is linked to the correct VNet. See [Configure private link](../how-to/configure-private-link.md). |
| `Authorization_RequestDenied` from Microsoft Graph or Entra ID | Missing Microsoft Entra directory role (for example, **Global Administrator** or **Microsoft Entra AI Administrator**) | Entra directory roles are assigned in the [Microsoft Entra admin center](https://entra.microsoft.com), not in Azure RBAC. See [Manage compliance and monitoring](#manage-compliance-and-monitoring). |

> [!TIP]
> Role assignments can take up to five minutes to propagate. Ask the developer to sign out and sign back in after you assign the role. For general Azure RBAC troubleshooting, see [Troubleshoot Azure RBAC](/azure/role-based-access-control/troubleshooting).

## Related content

- [Role-based access control for Microsoft Foundry](../concepts/rbac-foundry.md)
- [Authentication and authorization](../concepts/authentication-authorization-foundry.md)
- [Plan rollout](../concepts/planning.md)
- [Assign Azure roles](/azure/role-based-access-control/role-assignments-steps)
- [Manage compliance and security](../control-plane/how-to-manage-compliance-security.md)
- [Govern agent infrastructure as Entra admin](../control-plane/govern-agent-infrastructure-entra-admin.md)
- [Manage quotas](../how-to/quota.md)
- [Monitor models](../foundry-models/how-to/monitor-models.md)
- [Set up your agent resources](../agents/environment-setup.md)
- [Configure private link](../how-to/configure-private-link.md)
- [Troubleshoot Azure RBAC](/azure/role-based-access-control/troubleshooting)
