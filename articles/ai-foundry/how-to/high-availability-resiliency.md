---
title: High availability and resiliency for Microsoft Foundry projects and Agent Services
description: Learn how to plan for high availability and resiliency for Microsoft Foundry projects and Agent Service.
monikerRange: 'foundry-classic || foundry'
ms.service: azure-ai-foundry
ms.topic: how-to
ms.author: jburchel 
author: jonburchel 
ms.reviewer: andyaviles
ms.date: 02/02/2026
ms.custom: dev-focus
ai-usage: ai-assisted
---

# High availability and resiliency for Microsoft Foundry projects and Agent Services

[!INCLUDE [version-banner](../includes/version-banner.md)]

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

Plan ahead to maintain business continuity and prepare for disaster recovery with [Microsoft Foundry](https://ai.azure.com/?cid=learnDocs).

Microsoft strives to ensure that Azure services are always available. However, unplanned service outages might occur. Create a disaster recovery plan to handle regional service outages. In this article, you learn how to:

* Plan a multi-region deployment of Foundry and associated resources.
* Maximize your chances to recover logs, notebooks, Docker images, and other metadata.
* Design your solution for high availability.
* Fail over to another region.

> [!IMPORTANT]
> Foundry itself doesn't provide automatic failover or disaster recovery.

:::moniker-range="foundry-classic"
> [!NOTE]
> The information in this article applies only to **[!INCLUDE [fdp](../includes/fdp-project-name.md)]**. For disaster recovery for **[!INCLUDE [hub](../includes/hub-project-name.md)]**, see [Disaster recovery for Foundry hubs](hub-disaster-recovery.md).
:::moniker-end

## Prerequisites

- An Azure subscription. If you don't have one, create a [free account](https://azure.microsoft.com/free/).
- A Microsoft Foundry account and project. For more information, see the [Microsoft Foundry Quickstart](../quickstarts/get-started-code.md).
- Azure CLI installed (optional, for applying resource locks via command line).
- Appropriate RBAC roles:
  - **Owner** or **Contributor** on the resource group to deploy and configure resources.
  - **User Access Administrator** to assign RBAC roles to managed identities.
  - **Cosmos DB Operator** for Azure Cosmos DB configuration.
  - **Search Service Contributor** for Azure AI Search configuration.
  - **Storage Account Contributor** for Azure Storage configuration.

## Service model and shared responsibility

Microsoft and you jointly operate the Foundry Agent Service. Microsoft runs the control plane and capability host platform components. You operate and are responsible for the durability of any customer-owned stateful dependencies such as Azure Cosmos DB, Azure AI Search, and Azure Storage when using Standard agent deployment mode. In Basic mode, Microsoft manages those data components and recovery options are limited. In Standard mode, business continuity and disaster recovery (BCDR) follows the guidance for each underlying Azure service. This division requires a shared responsibility approach for availability, security, and data protection.

## Understand Azure services for Foundry

Foundry is an Azure native service with fewer implicit dependencies than the earlier hub/workspace model. Foundry projects can attach resources based on workload patterns, such as retrieval, orchestration, monitoring, and integration. Treat attached resources as optional unless your workload requires them.

Service categories include:

* **Platform infrastructure (Microsoft-managed)**: Control plane and project metadata service components that Microsoft operates regionally.
* **Optional workload and integration resources (customer-managed)**: Azure Storage, Azure Key Vault, Azure Container Registry (ACR), Application Insights, Azure Logic Apps, Azure Functions, Azure AI Search, Azure Cosmos DB, Azure Event Grid, SharePoint, Microsoft Purview (explicit connection), and other connection targets.
* **Connections**: Configuration objects that reference external Azure or SaaS services. You own their high availability configuration.

None of these optional resources, such as Key Vault, Storage, ACR, and Application Insights, are hard dependencies of the Foundry resource model itself, though your solution might require them. Design per workload and avoid assuming a fixed mandatory set.

| Resource type | Example services | Managed by | Notes on availability |
| ------------- | ---------------- | ---------- | --------------------- |
| Platform infrastructure | Foundry control plane, project metadata | Microsoft | Regional; no customer action for zone configuration. |
| State stores (Standard agent mode) | Azure Cosmos DB, Azure AI Search, Azure Storage | You | Configure redundancy, backup, replication. |
| Security and secrets | Azure Key Vault | You | Automatic zone redundancy when supported; configure RBAC and purge protection. |
| Monitoring | Application Insights | You | Consider multiregion instances or failover strategy. |
| Image and artifact registry | Azure Container Registry | You | Use geo-replication as needed. |
| Integration and workflow | Logic Apps, Functions, Event Grid | You | Align region and DR strategy with agent dependencies. |
| Compliance and data mapping | Microsoft Purview (connected) | You | Enable continuity for eDiscovery scenarios. |
| Other knowledge and tool sources | SharePoint, custom APIs | You | Configure per service HA. |

The rest of this article explains how to make each component highly available.

## Disaster prevention

Prevention is the primary defense against outages. The following proactive measures reduce the likelihood of these incidents. Apply these recommendations to help you design resiliency in your workload.

Learn more: [Design for resiliency](/azure/well-architected/reliability/principles#design-for-resiliency).

### Prevent resource deletion

To prevent most accidental deletions, apply delete [resource locks](/azure/azure-resource-manager/management/lock-resources) to critical resources. Locks protect against resource-level deletion but not data plane operations. Apply delete locks to these resources.

The following table describes the protections and limitations for each resource:

| Resource                 | Protection provided | Limitations |
| :----------------------- | :------------------ | :---------- |
| Foundry account | Prevents deletion of account, projects, models, connections, and agent capability hosts. | Doesn't protect individual agents or threads. |
| Azure Cosmos DB account  | Prevents deletion of account, `enterprise_memory` database, and containers. | Doesn't protect data within containers. |
| Azure AI Search service  | Prevents deletion of the search service instance. | Doesn't protect indexes or data within indexes. |
| Azure Storage account | Prevents deletion of account and blob containers. | Doesn't protect individual blobs. When deleting a container, the Storage Account locks can be overwritten. |

For resilience in depth, combine resource locks with the Azure Policy [`denyAction` effect](/azure/governance/policy/concepts/effect-deny-action) to block resource provider delete requests. This layered approach strengthens protection regardless of each resource's recovery capabilities.

The following Azure CLI command applies a delete lock to a Foundry account:

```azurecli
az lock create \
  --name "FoundryAccountLock" \
  --lock-type CanNotDelete \
  --resource-group "<your-resource-group>" \
  --resource-name "<your-foundry-account>" \
  --resource-type "Microsoft.CognitiveServices/accounts"
```

To verify the lock was applied:

```azurecli
az lock list --resource-group "<your-resource-group>" --output table
```

Expected output shows the lock name and type for your resources.

**Reference:** [az lock create](/cli/azure/lock#az-lock-create)

### Implement least privilege access

Use Azure role-based access control (RBAC) to limit access to control and data planes. Grant only required permissions and audit them regularly.

In production, don't grant standing delete permissions on these resources to any principal. For data plane access to state stores, only the project's managed identity should have standing write permissions.

You can also destroy data through Agent Service REST APIs. For example, see [Delete Agent](/rest/api/aifoundry/aiagents/delete-agent/delete-agent) or [Delete Thread](/rest/api/aifoundry/aiagents/threads/delete-thread). Built-in AI roles like [Azure AI User](../concepts/rbac-foundry.md#built-in-roles) can delete operational data by using these APIs or the Foundry portal. Accidents or abuse of these APIs can create recovery needs. No built-in AI role is read only for these [data plane operations](/rest/api/aifoundry/aiagents/operation-groups). Create [custom roles](../concepts/rbac-foundry.md#create-custom-roles-for-projects) to limit access to these `Microsoft.CognitiveServices/*/write` data actions.

### Implement the single responsibility principle

Dedicate your Azure Cosmos DB account, Azure AI Search service, and Azure Storage account exclusively to your workload's AI Agent Service. Sharing these resources with other Foundry accounts or workload components increases risk through broader permission surfaces and a larger blast radius. Unrelated operations from one workload should never remove or corrupt agent state in another workload. This separation also allows you to make per‑workload recovery decisions without needing to take an all-or-nothing approach.

### Use zone-redundant configurations

Use zone redundant configurations for your Azure Cosmos DB account, Azure AI Search service, and Azure Storage account. This setup protects against zone failures within a region. Zone redundant configurations don't protect against full regional outages or human or automation errors. The Microsoft-hosted components of the Agent Service are zone redundant.

## Resource configuration to support recovery

You need to configure resources to support recovery before an incident happens. Enable these capabilities on your resources. The recovery steps in this guide assume that you configured the following settings.

| Resource                 | Recommended configurations | Purpose |
| :----------------------- | :------------------------- | :------ |
| Foundry account | Establish an [explicit connection to Microsoft Purview](/purview/developer/secure-ai-with-purview). | Supports data continuity for compliance scenarios like eDiscovery requests after thread data is lost in an incident. |
| Foundry project       | Use a user-assigned managed identity, not a system-assigned managed identity. | Supports restoration of access to agent dependencies without needing changes on the dependencies. |
| Foundry Agent Service | Use the [Standard agent deployment mode](/azure/ai-foundry/agents/concepts/standard-agent-setup). | This mode increases incident risk but provides more recovery capabilities than Basic. |
| Azure Cosmos DB          | Enable [Continuous backup with point-in-time restore](/azure/cosmos-db/continuous-backup-restore-introduction). | Helps you recover from an accidental delete of the `enterprise_memory` database, one of its containers, or the whole account. |
| Azure Cosmos DB          | Use a name another customer is unlikely to request. | Reduces the risk of naming collisions during restoration steps. |
| Azure Cosmos DB          | Enable read replication to your designated failover region, and enable [Service-Managed Failover](/azure/cosmos-db/how-to-manage-database-account#enable-service-managed-failover-for-your-azure-cosmos-db-account). | Enables the Cosmos DB service to switch the write region from the primary region to the secondary region during a prolonged regional outage. |
| Azure AI Search          | Use a name another customer is unlikely to request. | Reduces the risk of naming collisions during restoration steps. |
| Azure Storage account    | Use geo-zone-redundant storage (GZRS). Your workload's recovery region can be the secondary region for this Storage account, but it's not required. | Allows customer-managed failover to be initiated to the predetermined region. |

**References:**
- [Azure Cosmos DB high availability](/azure/cosmos-db/high-availability)
- [Azure AI Search service reliability](/azure/search/search-reliability)
- [Azure Storage redundancy](/azure/storage/common/storage-redundancy)

### Deployment modes and recovery implications

Basic mode provides almost no recovery capabilities for human or automation-based resource loss. In the [Standard deployment mode](/azure/ai-foundry/agents/concepts/standard-agent-setup), you host agent state in your own Azure Cosmos DB, Azure AI Search, and Azure Storage accounts. This topology adds incident risk (for example, direct data deletion) but gives you control over, and the responsibility for, recovery procedures.

> [!TIP]
> Agent Service has no availability or state durability Service Level Agreement (SLA). Standard mode offloads SLAs and data durability assurances to the underlying storage components.

### Use user-assigned managed identities

When a component uses a managed identity to access a dependency, grant that identity the required role assignments on the dependency. With a system-assigned managed identity, a recovery action that recreates the faulted resource results in a new principal ID. You must then reapply all required role assignments on every dependency for the new principal ID and delete the old, now orphaned, assignments. Some dependencies (for example those used by tools or knowledge sources) might be owned by other teams, which adds cross-team coordination and delay during recovery.

Using a user-assigned managed identity avoids this reassignment effort. After you restore the faulted resource, reattach the existing user-assigned managed identity. Existing role assignments on dependencies remain valid; no further action is required.

> [!IMPORTANT]
> Avoid treating a single user-assigned managed identity as a universal identity for multiple unrelated uses.
>
> For example, assign a dedicated user-assigned managed identity per project. Even if two projects have identical role assignments today, treat that situation as temporary. Future divergence can grant unnecessary permissions to one project if they share an identity, violating least privilege. Separate identities also let dependency logs distinguish activity per project.

### Use repeatable deployment techniques

Define the account, projects, capability host, and dependencies in infrastructure as code (IaC) such as Bicep or Terraform. Some recovery steps require redeploying resources exactly as they were. Treat IaC as the source of truth to reproduce configuration and role assignments quickly. Build your IaC modular so that you can independently deploy each project.

Make agents redeployable. For ephemeral agents, existing application code is usually sufficient. For long‑lived agents, store their JSON definitions and knowledge or tool bindings in source control and automate deployment via pipeline calls to the Foundry APIs. Automatically update client configuration for new agent IDs. This process rehydrates agent definitions, knowledge files, and tool connections.

Avoid untracked changes made directly in the Foundry portal or Azure portal. Untracked production changes make recovery slower and error-prone.

If you still choose system-assigned identities (contrary to the recommendation to [use user-assigned managed identities](#use-user-assigned-managed-identities)), design IaC to recreate, not mutate, each role assignment that references the project's principal ID. The principal ID on role assignments is immutable and can't be updated to a new value. Use a `guid()` expression that incorporates the principal ID so a regenerated identity produces a distinct role assignment name.

### Minimize treating Azure AI Search as a primary data store

Azure AI Search is designed to hold a derived, query‑optimized projection of authoritative content that you store elsewhere. Don't rely on it as the only location of knowledge assets. During recovery you must be able to recreate agents that reference file-based knowledge in either the production or recovery environment.

User‑uploaded files attached within conversation threads generally can't be recovered because they're not registered or persisted outside the thread context. Set expectations that these attachments are transient and are lost in a disaster.

## Backup and restoration guidance

Conversation thread history durability depends on the underlying Standard mode state stores, which include Cosmos DB `enterprise_memory` database, Azure AI Search indexes, and Storage blobs for attachments. Currently, there's no built-in one-click export or import feature for complete conversation histories to support later bulk restoration. Use service APIs to periodically snapshot critical agent definitions, tool bindings, and knowledge source references.

For compliance continuity, connect to Microsoft Purview to preserve lineage and classification metadata even if operational thread data is lost.

## Plan for multiregional deployment

A multiregional deployment relies on creating Foundry resources and other infrastructure in two Azure regions. If a regional outage occurs, switch to the other region. When you plan where to deploy your resources, consider:

* Regional availability: If possible, use a region in the same geographic area, not necessarily the closest one. To check regional availability for Foundry, see [Azure products by region](https://azure.microsoft.com/global-infrastructure/services/).
* Azure paired regions: Paired regions coordinate platform updates and prioritize recovery efforts where needed. However, not all regions are paired. For more information, see [Azure paired regions](/azure/reliability/cross-region-replication-azure).
* Service availability: Decide whether to use hot/hot, hot/warm, or hot/cold for your solution's resources.
    
    * Hot/hot: Both regions are active at the same time, and either region is ready to use immediately.
    * Hot/warm: The primary region is active. The secondary region has critical resources (for example, deployed models) ready to start. Deploy noncritical resources manually in the secondary region.
    * Hot/cold: The primary region is active. The secondary region has Foundry and other resources deployed, along with the required data. Deploy resources such as models, model deployments, and pipelines manually.

> [!TIP]
> Depending on your business requirements, you might treat Foundry services differently.

Foundry builds on other services. Some services replicate to other regions. You must manually create other services in multiple regions. The following table lists the services, who is responsible for replication, and an overview of the configuration:

| Azure service | Geo-replicated by | Configuration |
| ----- | ----- | ----- |
| Foundry projects | You | Create projects in the selected regions. |
| Key Vault | Microsoft | Use the same Azure Key Vault instance with the Foundry project and resources in both regions. Azure Key Vault automatically fails over to a secondary region. For more information, see [Azure Key Vault availability and redundancy](/azure/key-vault/general/disaster-recovery-guidance).|
| Storage account | You | Foundry projects don't support default storage account failover using geo-redundant storage (GRS), geo-zone-redundant storage (GZRS), read-access geo-redundant storage (RA-GRS), or read-access geo-zone-redundant storage (RA-GZRS). Configure a storage account according to your needs, and use it for your project. All subsequent projects use the project's storage account. For more information, see [Azure Storage redundancy](/azure/storage/common/storage-redundancy). |
| Azure Container Registry | Microsoft | Configure the Azure Container Registry instance to replicate geographically to the paired region for Foundry. Use the same instance for both projects. For more information, see [Geo-replication in Azure Container Registry](/azure/container-registry/container-registry-geo-replication). |
| Application Insights | You | Create Application Insights for the project in both regions. To adjust the data retention period and details, see [Data collection, retention, and storage in Application Insights](/azure/azure-monitor/logs/data-retention-archive). |

Use these development practices to enable fast recovery and restart in the secondary region:

* Use Azure Resource Manager templates. Templates are infrastructure as code, and they let you quickly deploy services in both regions.
* To avoid drift between the two regions, update your continuous integration and deployment pipelines to deploy to both regions.
* Create role assignments for users in both regions.
* Create network resources such as Azure virtual networks and private endpoints for both regions. Ensure users can access both network environments. For example, configure VPN and DNS for both virtual networks.

## Design for high availability

### Availability zones

Some Azure services support availability zones. In regions that support availability zones, if a zone goes down, projects pause, and you should save your data. You can't refresh data until the zone comes back online.

Learn more in [Availability zone service support](/azure/reliability/availability-zones-service-support).

### Deploy critical components to multiple regions

Decide what level of business continuity you need. The level can differ between components of your solution. For example, you might use a hot/hot configuration for production pipelines or model deployments, and hot/cold for development.

Foundry is a regional service that stores data on the service side and in a storage account in your subscription. If a regional disaster occurs, you can't recover service data. You can recover data that the service stores in the storage account in your subscription if storage redundancy is enabled. Service-side data is mostly metadata like tags, asset names, and descriptions. Data in your storage account typically isn't metadata, like uploaded data.

For connections, create two separate resources in two different regions, and then create two connections for the project. For example, if Foundry Tools is critical for business continuity, create two AI Services resources and two project connections. With this configuration, if one region goes down, the other region stays operational.

For any projects that are essential to business continuity, deploy resources in two regions.

### Isolated storage

If you connect data to customize your AI application, you can use datasets in Azure AI and outside Azure AI. Dataset volume can be large, so it might be a good idea to keep this data in a separate storage account. Evaluate the data replication strategy that makes the most sense for your use case.

In the Foundry portal, create a connection to your data. If you have multiple Foundry instances in different regions, you can point to the same storage account. Connections work across regions.

## Initiate a failover

### Continue work in the failover project

When the primary project is unavailable, switch to the secondary project to continue development work. Foundry doesn't automatically submit jobs to the secondary project during an outage, so you need to update your configuration. Update your configuration to point to the secondary project resources. Avoid hard-coded project references.

Foundry doesn't sync or recover artifacts or metadata between projects. Depending on your deployment strategy, you might need to move or recreate artifacts in the failover project. If you configure the primary and secondary projects to share associated resources with geo-replication enabled, some objects are available in the failover project. For example, both projects share the same Docker images, configured datastores, and Azure Key Vault resources.

> [!NOTE]
> Jobs that run during a service outage don't automatically transition to the secondary project. They also don't typically resume and finish successfully in the primary project after the outage. Resubmit these jobs in the secondary project or in the primary project after the outage.

## Recovery options

### Resource deletion

If you delete a project and its resources, some resources support soft delete and can be recovered from deletion. Projects don't support soft delete, so they can't be recovered after deletion. After you delete a project, you can't recover it. The following table shows which services support soft delete.

| Service | Soft delete enabled |
| ------- | ------------------- |
| Foundry project | No |
| Azure Storage | See [Recover a deleted storage account](/azure/storage/common/storage-account-recover#recover-a-deleted-account-from-the-azure-portal) |
| Azure Key Vault | Yes |

For recovery of other Foundry resources (accounts, projects) after deletion or purge scenarios, see [Recover or purge deleted Foundry resources](/azure/ai-services/recover-purge-resources).

## Troubleshooting

| Issue | Possible cause | Resolution |
| ----- | -------------- | ---------- |
| Resource lock doesn't prevent deletion | Lock applied at wrong scope | Verify the lock is applied directly to the resource, not just the resource group. Use `az lock list --resource-group <rg>` to confirm. |
| RBAC permission denied when configuring Cosmos DB | Missing role assignment | Ensure you have **Cosmos DB Operator** or **Contributor** role on the Cosmos DB account. |
| Failover project can't access shared resources | Managed identity mismatch | If you use system-assigned identity, reapply role assignments. Consider switching to user-assigned managed identity. |
| Point-in-time restore fails for Cosmos DB | Continuous backup not enabled | Enable continuous backup before an incident occurs. This setting can't be applied retroactively. |

## Related content

[Azure service-level agreements](https://www.microsoft.com/licensing/docs/view/Service-Level-Agreements-SLA-for-Online-Services?lang=1)
