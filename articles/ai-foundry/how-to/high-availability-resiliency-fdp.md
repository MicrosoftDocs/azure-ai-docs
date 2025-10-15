---
title: High availability and resiliency for Azure AI Foundry projects and agent services
description: Learn how to plan for high availability and resiliency for Azure AI Foundry projects and agent services.
ms.service: azure-ai-foundry
ms.topic: how-to
ms.author: jburchel 
author: jonburchel 
ms.reviewer: andyaviles
ms.date: 10/07/2025
ai.usage: ai-assisted
---

# High availability and resiliency for Azure AI Foundry projects and agent services

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

Plan ahead to maintain business continuity and prepare for disaster recovery with [Azure AI Foundry](https://ai.azure.com/?cid=learnDocs).

Microsoft strives to ensure that Azure services are always available. However, unplanned service outages might occur. Create a disaster recovery plan to handle regional service outages. In this article, you learn how to:

* Plan a multi-region deployment of Azure AI Foundry and associated resources.
* Maximize your chances to recover logs, notebooks, Docker images, and other metadata.
* Design your solution for high availability.
* Fail over to another region.

> [!IMPORTANT]
> Azure AI Foundry itself doesn't provide automatic failover or disaster recovery.

> [!NOTE]
> The information in this article only applies to **[!INCLUDE [fdp](../includes/fdp-project-name.md)]**. For disaster recovery for **[!INCLUDE [hub](../includes/hub-project-name.md)]**, see [Disaster recovery for Azure AI Foundry hubs](disaster-recovery.md).

## Understand Azure services for Azure AI Foundry

Azure AI Foundry depends on multiple Azure services. Some of these services are set up in your subscription. You're responsible for the high availability configuration of these services. Microsoft manages some services that are created in a Microsoft subscription. 

Azure services include:

* **Azure AI Foundry infrastructure**: A Microsoft managed environment for the Azure AI Foundry project.

* **Required associated resources**: Resources set up in your subscription when you create an Azure AI Foundry project. These resources include Azure Storage and Azure Key Vault.
  * The default storage has models, training logs, and references to data assets.
  * Azure Key Vault stores credentials for Azure Storage and connections.

* **Optional associated resources**: Resources you attach to your Azure AI Foundry project. These resources include Azure Container Registry and Application Insights.
  * Azure Container Registry stores Docker images for training and inference environments.
  * Application Insights monitors Azure AI Foundry.

* **Connections**: Azure AI Foundry connects to other services. You're responsible for configuring their high availability settings.

The following table shows the Azure services that Microsoft manages and the ones you manage. It also indicates the services that are highly available by default.

| Service | Managed by | High availability by default |
| ----- | ----- | ----- |
| **Azure AI Foundry infrastructure** | Microsoft | |
| **Associated resources** |  |  |
| Azure Storage | You | |
| Azure Key Vault | You | ✓ |
| Azure Container Registry | You | |
| Application Insights | You | Not applicable |
| **Connections to external services** like Azure AI Services | You | |

The rest of this article explains how to make each service highly available.

## Disaster prevention

Prevention is the primary defense against outages. The following proactive measures reduce the likelihood of these incidents. Apply these recommendations to help you [design for resiliency](/azure/well-architected/reliability/principles#design-for-resiliency) in your workload.

### Prevent resource deletion

To prevent most accidental deletions, apply *delete* [resource locks](/azure/azure-resource-manager/management/lock-resources) to critical resources. Locks protect against resource-level deletion but not data plane operations. Apply delete locks to these resources:

| Resource                 | Protection provided | Limitations |
| :----------------------- | :------------------ | :---------- |
| Azure AI Foundry account | Prevents deletion of account, projects, models, connections, and agent capability hosts | Doesn't protect individual agents or threads |
| Azure Cosmos DB account  | Prevents deletion of account, `enterprise_memory` database, and containers | Doesn't protect data within containers |
| Azure AI Search service  | Prevents deletion of the search service instance | Doesn't protect indexes or data within indexes |
| Azure Storage account | Prevents deletion of account and blob containers | Doesn't protect individual blobs. When deleting a container, the Storage Account locks can be overwritten. |

For resilience-in-depth, combine resource locks with the Azure Policy [`denyAction` effect](/azure/governance/policy/concepts/effect-deny-action) to block resource provider delete requests. This layered approach strengthens protection regardless of each resource's recovery capabilities.

### Implement least privilege access

Use Azure Role-Based Access Control (RBAC) to limit access to control and data planes. Grant only required permissions and audit them regularly.

In production, don't grant standing *delete* permissions on these resources to any principal. For data plane access to state stores, only the project's managed identity should have standing *write* permissions.

Data can also be destroyed through Azure AI Foundry Agent Service REST APIs; for example, [Delete Agent](/rest/api/aifoundry/aiagents/delete-agent/delete-agent) or [Delete Thread](/rest/api/aifoundry/aiagents/threads/delete-thread). Built-in AI roles like [Azure AI User](/azure/ai-foundry/concepts/rbac-azure-ai-foundry#azure-ai-user) can delete operational data using these APIs or the AI Foundry portal. Accidents or abuse of these APIs can create recovery needs. No built-in AI role is read-only for these [data plane operations](/rest/api/aifoundry/aiagents/operation-groups). Create [custom roles](/azure/ai-foundry/concepts/rbac-azure-ai-foundry#create-custom-roles-for-projects) to limit access to these `Microsoft.CognitiveServices/*/write` data actions.

### Implement the single responsibility principle

Dedicate your Azure Cosmos DB account, Azure AI Search service, and Azure Storage account exclusively to your workload's AI Agent Service. Sharing these resources with other Azure AI Foundry accounts or workload components increases risk through broader permission surfaces and a larger blast radius. Unrelated operations from one workload should never remove or corrupt agent state in another workload. This separation also allows you to make per-project recovery decisions without needing to take an all-or-nothing approach.

### Use zone-redundant configurations

Use zone-redundant configurations for your Azure Cosmos DB account, Azure AI Search service, and Azure Storage account. This setup protects against zone failures within a region. Zone-redundant configurations don't protect against full regional outages or human/automation errors. The Microsoft-hosted components of the Azure AI Foundry Agent Service are zone-redundant. 

> [!WARNING]
> **TODO: VERIFY THIS LAST STATEMENT AND ADD ANY MORE DETAILS AVAILABLE.**

## Resource configuration to support recovery

Resources need to be configured to support recovery prior to an incent happening. Enable these capabilities on your resources. The recovery steps included in this guide assume the following have been configured.

| Resource                 | Recommended configurations | Purpose |
| :----------------------- | :------------------------- | :------ |
| Azure AI Foundry account | Establish an [explicit connection to Microsoft Purview](/purview/developer/secure-ai-with-purview). | Supports data continuity for compliance scenarios like eDiscovery requests after thread data is lost in an incident. |
| AI Foundry project       | Use a user-assigned managed identity, not a system-assigned managed identity. **TODO: ICM IS OPEN BECAUSE THIS CONFIGURATION FAILS WHEN DEPLOYING THE CAP HOST** | Supports restoration of access to agent dependencies without needing changes on the dependencies. |
| AI Foundry Agent Service | Use the [Standard agent deployment mode](/azure/ai-foundry/agents/concepts/standard-agent-setup). | This mode increases incident risk but provides more recovery capabilities than Basic. |
| Azure Cosmos DB          | Enable [Continuous backup with point-in-time restore](/azure/cosmos-db/continuous-backup-restore-introduction). | Helps you recover from an accidental delete of the `enterprise_memory` database, one of its containers, or the whole account. |
| Azure Cosmos DB          | Use a name another customer is unlikely to request. | Reduces the risk of naming collisions during restoration steps. |
| Azure Cosmos DB          | Enable read replication to your designated failover region, and enable [Service-Managed Failover](/azure/cosmos-db/how-to-manage-database-account#enable-service-managed-failover-for-your-azure-cosmos-db-account). | Enables the Cosmos DB service to switch the write region from the primary region to the secondary region during a prolonged regional outage. |
| Azure AI Search          | Use a name another customer is unlikely to request. | Reduces the risk of naming collisions during restoration steps. |
| Azure Storage account    | Use geo-zone-redundant storage (GZRS). Your workload's recovery region could be the secondary region for this Storage account, but it's not required. | Allows customer-managed failover to be initiated to the predetermined region. |

### Deployment modes and recovery implications

Basic mode provides almost no recovery capabilities for human or automation-based resource loss. In the [Standard deployment mode](/azure/ai-foundry/agents/concepts/standard-agent-setup), you host agent state in your own Azure Cosmos DB, Azure AI Search, and Azure Storage accounts. This topology adds incident risk (for example, direct data deletion) but gives you control over, and the responsibility for, recovery procedures.

> [!TIP]
> Azure AI Foundry Agent Service has no availability or state durability Service Level Agreement (SLA). Standard mode offloads SLAs and data durability assurances to the underlying storage components.

### Use user-assigned managed identities

When a component uses a managed identity to access a dependency, you must grant that identity the required role assignments on the dependency. With a system-assigned managed identity, a recovery action that recreates the faulted resource results in a new principal ID. You must then reapply all required role assignments on every dependency for the new principal ID and delete the old, now orphaned, assignments. Some dependencies (for example those used by tools or knowledge sources) might be owned by other teams, which adds cross-team coordination and delay during recovery.

Using a user-assigned managed identity avoids this reassignment effort. After you restore the faulted resource, reattach the existing user-assigned managed identity. Existing role assignments on dependencies remain valid; no further action is required.

> [!IMPORTANT]
> Avoid treating a single user-assigned managed identity as a universal identity for multiple unrelated uses.
>
> For example, assign a dedicated user-assigned managed identity per project. Even if two projects have identical role assignments today, treat that situation as temporary. Future divergence can grant unnecessary permissions to one project if they share an identity, violating least privilege. Separate identities also let dependency logs distinguish activity per project.

### Use repeatable deployment techniques

Define the account, projects, capability host, and dependencies in infrastructure as code (IaC) such as Bicep or Terraform. Some recovery steps require redeploying resources exactly as they were. Treat IaC as the source of truth to reproduce configuration and role assignments quickly. Build your IaC modular so that you can independently deploy each project.

Make agents redeployable. For ephemeral agents, existing application code is usually sufficient. For long‑lived agents, store their JSON definitions and knowledge/tool bindings in source control and automate deployment via pipeline calls to the Azure AI Foundry APIs. Automatically update client configuration for new agent IDs. This process rehydrates agent definitions, knowledge files, and tool connections.

Avoid untracked changes made directly in the Azure AI Foundry portal or Azure portal. Untracked production changes make recovery slower and error-prone.

If you still choose system-assigned identities (contrary to the recommendation to [use user-assigned managed identities](#use-user-assigned-managed-identities)), design IaC to recreate, not mutate, each role assignment that references the project's principal ID. The principal ID on role assignments is immutable and can't be updated to a new value. Use a `guid()` expression that incorporates the principal ID so a regenerated identity produces a distinct role assignment name.

### Minimize treating Azure AI Search as a primary data store

Azure AI Search is designed to hold a derived, query‑optimized projection of authoritative content that you store elsewhere. Don't rely on it as the only location of knowledge assets. During recovery you must be able to recreate agents that reference file-based knowledge in either the production or recovery environment.

User‑uploaded files attached within conversation threads generally can't be recovered because they're not registered or persisted outside the thread context. Set expectations that these attachments are transient and will be lost in a disaster.



## Plan for multiregional deployment

A multiregional deployment relies on the creation of Azure AI Foundry resources and other infrastructure in two Azure regions. If a regional outage occurs, switch to the other region. When you plan where to deploy your resources, consider:

* Regional availability: If possible, use a region in the same geographic area, not necessarily the closest one. To check regional availability for Azure AI Foundry, see [Azure products by region](https://azure.microsoft.com/global-infrastructure/services/).
* Azure paired regions: Paired regions coordinate platform updates and prioritize recovery efforts where needed. But not all regions are paired. For more information, see [Azure paired regions](/azure/reliability/cross-region-replication-azure).
* Service availability: Decide whether to use hot/hot, hot/warm, or hot/cold for your solution's resources.
    
    * Hot/hot: Both regions are active at the same time, and either region is ready to use immediately.
    * Hot/warm: The primary region is active. The secondary region has critical resources (for example, deployed models) ready to start. Deploy noncritical resources manually in the secondary region.
    * Hot/cold: The primary region is active. The secondary region has Azure AI Foundry and other resources deployed, along with the required data. Deploy resources such as models, model deployments, and pipelines manually.

> [!TIP]
> Depending on your business requirements, you might treat Azure AI Foundry services differently.

Azure AI Foundry builds on other services. Some services can replicate to other regions. You must manually create other services in multiple regions. The following table lists the services, who is responsible for replication, and an overview of the configuration:

| Azure service | Geo-replicated by | Configuration |
| ----- | ----- | ----- |
| Azure AI Foundry projects | You | Create a projects in the selected regions. |
| Key Vault | Microsoft | Use the same Azure Key Vault instance with the Azure AI Foundry project and resources in both regions. Azure Key Vault automatically fails over to a secondary region. For more information, see [Azure Key Vault availability and redundancy](/azure/key-vault/general/disaster-recovery-guidance).|
| Storage account | You | Azure AI Foundry projects don't support default storage account failover using geo-redundant storage (GRS), geo-zone-redundant storage (GZRS), read-access geo-redundant storage (RA-GRS), or read-access geo-zone-redundant storage (RA-GZRS). Configure a storage account according to your needs and use it for your project. All subsequent projects use the project's storage account. For more information, see [Azure Storage redundancy](/azure/storage/common/storage-redundancy). |
| Azure Container Registry | Microsoft | Configure the Azure Container Registry instance to geo-replicate to the paired region for Azure AI Foundry. Use the same instance for both projects. For more information, see [Geo-replication in Azure Container Registry](/azure/container-registry/container-registry-geo-replication). |
| Application Insights | You | Create Application Insights for the project in both regions. To adjust the data retention period and details, see [Data collection, retention, and storage in Application Insights](/azure/azure-monitor/logs/data-retention-archive). |

Use these development practices to enable fast recovery and restart in the secondary region:

* Use Azure Resource Manager templates. Templates are infrastructure as code and let you quickly deploy services in both regions.
* To avoid drift between the two regions, update your continuous integration and deployment pipelines to deploy to both regions.
* Create role assignments for users in both regions.
* Create network resources such as Azure virtual networks and private endpoints for both regions. Ensure users can access both network environments. For example, configure VPN and DNS for both virtual networks.

## Design for high availability

### Availability zones

Some Azure services support availability zones. In regions that support availability zones, if a zone goes down, projects pause, and you should save your data. You can't refresh data until the zone is back online.

For more information, see [Availability zone service support](/azure/reliability/availability-zones-service-support).

### Deploy critical components to multiple regions

Decide the level of business continuity you need. The level can differ between components of your solution. For example, you might use a hot/hot configuration for production pipelines or model deployments, and hot/cold for development.

Azure AI Foundry is a regional service and stores data both on the service side and in a storage account in your subscription. If a regional disaster occurs, service data can't be recovered. However, you can recover data that the service stores in the storage account in your subscription if storage redundancy is enabled. Service-side data is mostly metadata (tags, asset names, descriptions). Data in your storage account is typically not metadata, like uploaded data.

For connections, create two separate resources in two distinct regions, and then create two connections for the project. For example, if AI Services is critical for business continuity, create two AI Services resources and two project connections. With this configuration, if one region goes down, the other region stays operational.

For any projects that are essential to business continuity, deploy resources in two regions.

### Isolated storage

If you connect data to customize your AI application, you can use those datasets in Azure AI and outside Azure AI. Dataset volume can be large, so it might be good practice to keep this data in a separate storage account. Evaluate the data replication strategy that makes the most sense for your use case.

In the Azure AI Foundry portal, create a connection to your data. If you have multiple Azure AI Foundry instances in different regions, you can point to the same storage account because connections work across regions.
 

## Initiate a failover

### Continue work in the failover project

When the primary project is unavailable, switch to the secondary project to continue development. Azure AI Foundry doesn't automatically submit jobs to the secondary project during an outage. Update your configuration to point to the secondary project resources. Avoid hard-coded project references.

Azure AI Foundry can't sync or recover artifacts or metadata between projects. Depending on your deployment strategy, you might need to move or recreate artifacts in the failover project to continue. If you configure the primary and secondary projects to share associated resources with geo-replication enabled, some objects can be available in the failover project. For example, both projects can share the same Docker images, configured datastores, and Azure Key Vault resources.

> [!NOTE]
> Jobs that run during a service outage don't automatically transition to the secondary project. They're also unlikely to resume and finish successfully in the primary project after the outage. Resubmit these jobs in the secondary project or in the primary project after the outage.

## Recovery options

### Resource deletion

If you delete a project and its resources, some resources support soft delete and can be recovered. Projects don't support soft delete. If you delete them, you can't recover them. The following table shows which services support soft delete.

| Service | Soft delete enabled |
| ------- | ------------------- |
| Azure AI Foundry project | Unsupported | 
| Azure AI Services resource | Yes |
| Azure Storage | See [Recover a deleted storage account](/azure/storage/common/storage-account-recover#recover-a-deleted-account-from-the-azure-portal). |
| Azure Key Vault | Yes |

## Related content

Review the [Azure service-level agreements](https://www.microsoft.com/licensing/docs/view/Service-Level-Agreements-SLA-for-Online-Services?lang=1).
