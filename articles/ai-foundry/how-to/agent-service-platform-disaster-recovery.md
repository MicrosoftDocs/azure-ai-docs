---
title: Foundry Agent Service platform outage recovery
ms.service: azure-ai-foundry
ms.reviewer: ckittel
description: Recover Foundry Agent Service projects from Azure platform and regional outages with warm standby, failover, and failback procedures.
monikerRange: 'foundry-classic || foundry'
#customer intent: As a developer, I want to understand how to recreate projects in a standby region so that I can restore critical functionality during a regional outage.
author: jonburchel
ms.author: jburchel
ms.date: 02/02/2026    
ms.topic: reliability-article
ms.collection: ce-skilling-ai-copilot
ms.custom: arb-aiml, dev-focus
ai-usage: ai-assisted
---

# Foundry Agent Service platform outage recovery

[!INCLUDE [version-banner](../includes/version-banner.md)]

This article covers recovery from Azure platform incidents that take an entire region or a regional dependency offline. Examples of these incidents include prolonged regional outages or loss of a stateful dependency.

The recommended approach to [design for recovery](/azure/well-architected/reliability/principles#design-for-recovery) in your workload is a warm standby, failover, and failback plan for mass outages combined with per-service recovery capabilities for localized outages.

> [!IMPORTANT]
> This article is part of a three-part series.
>
> To understand platform limitations, prevention controls, and required baseline configuration, see the overview guide. For prerequisites and context, see [Foundry Agent Service disaster recovery](./agent-service-disaster-recovery.md). This article explains why some losses are unrecoverable and why recovery often means reconstruction rather than restoration.
>
> For recommendations on recovering from human-caused or automation-caused deletions and localized data loss, see [Resource and data loss recovery](./agent-service-operator-disaster-recovery.md).

## Prerequisites

Before you implement the disaster recovery procedures in this article, ensure you have:

- An Azure subscription with an active Microsoft Foundry account using Agent Service in [Standard deployment mode](/azure/ai-foundry/agents/concepts/standard-agent-setup).
- One of the following Azure RBAC roles at the subscription or resource group scope:
  - **Contributor** or **Owner** for creating and managing Foundry accounts, projects, and dependencies
  - **Azure AI Project Manager** for managing Foundry projects
  - **Storage Account Contributor** for initiating Storage account failover
  - For details on each role's permissions, see [Role-based access control for Microsoft Foundry](/azure/ai-foundry/concepts/rbac-foundry).
- Agent definitions, knowledge assets, and tool bindings stored in source control for redeployment.
- Infrastructure as code (IaC) templates (Bicep, ARM, or Terraform) for your capability host dependencies (Azure Cosmos DB, Azure AI Search, Azure Storage).
- Familiarity with the [disaster recovery overview](./agent-service-disaster-recovery.md) and the [high availability and resiliency guidance](high-availability-resiliency.md).

## Architecture preparation

Establish and maintain a warm standby environment in a paired or otherwise acceptable region. This environment supports an active-passive approach that reduces recovery time with limited idle cost.

- Create a virtual network in the failover region that mirrors the primary region's subnet topology and all required cross-premises connectivity. Keep egress controls and firewall rules synchronized while this environment is idle.
- Create a Microsoft Foundry account with agent capability enabled in that network. Don't create projects, project-specific connections, or model deployments.
- Enable Azure diagnostics, Defender for Cloud, and Purview integration on the standby account, matching the configuration of your production instance.

Maintain this low-idle-cost, fully networked warm standby account. It hosts no projects during normal operations. Re-create only needed projects (and their dependencies) during failover based on business criticality and during failover drills.

### Monitor for regional outages

Configure [Azure Service Health alerts](/azure/service-health/alerts-activity-log-service-notifications-portal) to notify you of service issues and planned maintenance. These alerts can trigger automated actions or notify your operations team to initiate failover procedures.

The following Azure CLI command creates a basic Service Health alert rule:

```azurecli
az monitor activity-log alert create \
  --name "FoundryServiceHealthAlert" \
  --resource-group "<your-resource-group>" \
  --condition category=ServiceHealth \
  --action-group "<your-action-group-id>" \
  --description "Alert for Azure service health events affecting Foundry"
```

**Reference:** [az monitor activity-log alert create](/cli/azure/monitor/activity-log/alert)

### Automate failover

To reduce recovery time, automate the failover steps by using scripts or infrastructure as code (IaC) templates. Trigger this automation by your monitoring system or manually by your operations team. For example, you can use [Azure Automation](/azure/automation/overview) runbooks or [Azure Logic Apps](/azure/logic-apps/logic-apps-overview) to execute your failover scripts in response to Azure Service Health alerts.

### Gateway routing

It's always a good idea to have a level of abstraction between clients and APIs. Add a layer of indirection between your clients and the Agent Service [data plane APIs](/rest/api/aifoundry/aiagents/operation-groups). Implement the [Gateway Routing](/azure/architecture/patterns/gateway-routing) pattern in a multiregion gateway such as [API Management configured for multiple regions](/azure/api-management/api-management-howto-deploy-multi-region). This indirection lets you fail over the data plane APIs without updating your clients' fully qualified domain name (FQDN) configuration by instead updating failover routing inside the gateway.

## Complete regional outage

**Scenario:** A platform provider outage makes all resources in your primary region unavailable. The primary region that hosts your Foundry account and dependencies is unavailable.

**During the incident:** Complete outage. You can't create, delete, modify, or invoke agents in any projects. Data plane API calls error or time-out. The Foundry portal is unavailable for the whole account.

### Fail over to secondary region

For each project, decide whether to recover. Compare the project's business continuity requirement with the outage's expected duration, business consequences, and alternative continuity plans.

Don't fail over a project's agents if required knowledge stores and tools don't also fail over. If you own those stores and tools, run their recovery playbooks first.

For *each project* you choose to recover, follow these steps:

1. Deploy the project's capability host dependencies (Azure Cosmos DB, Azure AI Search, Azure Storage) in the recovery region by using your infrastructure as code (IaC) assets. Match topology and configuration. If multiple projects share the same dependencies, do this step only once.

      > [!TIP]
   > Pre-provisioning these resources reduces recovery time but increases cost and operational overhead. A hybrid approach is possible. For example, Azure Storage is already deployed because it's inexpensive when idle; Azure AI Search isn't.

1. Create the project's user-assigned managed identity. Give it access to the new regional dependencies.

1. Create the project in the standby Foundry account via IaC and assign the managed identity. Point the project's capability host to the new regional dependencies. Apply role assignments for clients, operators, and automation principals.

1. Redeploy agents (definitions, knowledge files, and tool connections) from source control or application code. They're new agents with new IDs and have **no access** to prior threads or files.

1. Recover any client components, if part of the workload, per their recovery playbooks.

1. Update clients to use the new Foundry account fully qualified domain name (FQDN) and new agent IDs.

   If an AI gateway pattern is used, then clients continue to use the gateway's FQDN. The gateway configuration instead needs to be updated to route requests to the newly created project on behalf of its clients.

   > [!IMPORTANT]
   > If clients support in-product messaging, notify users they're in a standby environment. Prior conversation history is unavailable, and new conversations *are lost* after failback.

**Results:**

Agent functionality is restored for recovered projects. Agents have no access to prior threads while in the standby region. Threads and agents created in the standby region don't persist after failback. Recovery restores functionality only; state isn't portable across regions.

- Recovery time: 30 or more minutes per project.

- Recovery point: No state is transferable between regions. Original state returns only when the primary region is back. Expect standby‑region state to become permanently lost after failback.

### Fail back to primary region

When the primary region is stable and fully operational, return traffic there and reestablish the secondary as a warm standby.

For each failed-over project:

1. Delete the project from the failover (standby) Foundry account. This action orphans all agents and threads created during the failover.

1. Delete the project's managed identity.

1. If this project is the last one referencing them, delete the three capability host dependencies in the failover region.

      > [!IMPORTANT]
   > This step permanently deletes all state created during the failover period. There's no recovery or merge capability for this data.

1. If clients still point to the failover (standby) Foundry account, update them to use the original project's FQDN and original agent IDs.

**Results:**

- Original agents resume with their pre-outage state.
- Recovery time: 10 or more minutes per project.
- Recovery point: State is exactly as it existed before failover. No cross‑region state transfer. Standby‑region state is permanently lost.

### What about multi-region support on Agent Service dependencies?

Using multi-region writes and reads on Azure Cosmos DB doesn't improve recovery. The `enterprise_memory` database partitions data by a globally unique identifier per project instance. A multiregion write topology doesn't prevent data loss on failback because data created during the failover is in containers keyed to new project IDs. You must still manage role-based access control (RBAC) for the new project identity. Use a new temporary Azure Cosmos DB instance during the failover.

Using Azure Storage multiregion recovery also doesn't improve recovery outcomes. Like Azure Cosmos DB, the data in this account is partitioned by a globally unique identifier per project and so the same limitations apply.

## Complete regional outage for Azure Cosmos DB accounts

**Scenario:** A platform provider outage in your region makes the Azure Cosmos DB account that your Agent Service uses unavailable. No other services are affected in this outage.

**During the incident:** All projects that use the `enterprise_memory` database in this Azure Cosmos DB instance experience a complete outage. You can't create, delete, modify, or invoke agents. All calls to the Foundry data plane APIs return errors. The agent experience in the Foundry portal isn't available for the account.

**Recovery steps:**

The Azure Cosmos DB team initiates a service-managed failover automatically based on internal decisions that you can't directly influence. Normally, you wait until this failover occurs and don't take self-directed action. After the incident, possibly three or more days later, the team fails your instance back to the primary region.

> [!TIP]
> If you have a business-critical need to fail over sooner, you can initiate a [forced failover](/azure/cosmos-db/how-to-manage-database-account#perform-forced-failover-for-your-azure-cosmos-db-account) to your failover region. This action causes data loss for any writes that aren't replicated to the failover region yet.

**Results:**

- Agents might experience intermittent connectivity problems during failover and failback. Calls to Azure Cosmos DB are routed to your secondary region until the primary region is restored as the write region.

- **Recovery time:** Once triggered by the Azure Cosmos DB team or a forced failover, expect 30 minutes or more.

- **Recovery point:** Depending on the outage, up to 15 minutes of data might be permanently lost. This loss includes agents created, updated, or deleted just before the outage and threads created or updated just before the outage.

## Complete regional outage for Azure AI Search services

**Scenario:** A platform provider outage in your region makes the Azure AI Search service unavailable. This outage likely affects connected pre-indexed knowledge stored in other Azure AI Search services, but recovery of that knowledge is the responsibility of the data owner and is out of scope for this article. No other services are affected in this outage.

**During the incident:** Agents with file-based knowledge generate an error when they consult that knowledge. Threads that involved uploaded files return errors if the agent attempts to recall indexed data. Attempts to add files as knowledge to agents or into threads result in an error. Agents that don't use file-based knowledge and workloads that don't support file uploads likely experience no change.

**Recovery steps:** None. Wait until the Azure AI Search service is restored in your primary region. Consider going into a graceful degradation state in your workload that avoids any file uploads during this period.

> [!IMPORTANT]
> If you have a business-critical need to fail over sooner, [Perform a destructive reset of the Azure AI Agent Service capability host](./agent-service-operator-disaster-recovery.md#perform-a-destructive-reset-of-the-azure-ai-agent-service-capability-host) and use a new AI Search instance in your failover region. This action causes *complete data loss* in your production instance. When AI Search is available again in your primary region, perform the same destructive reset action again.
>
> We don't advise this approach unless your users are tolerant of thread loss and your agents can easily rehydrate their file-based knowledge.

**Results:**

- Agent capability fully recovered.

- Recovery time: indeterminate.

- Recovery point: state preserved up to the AI Search outage; in-flight operations near the outage might not persist.

## Complete regional outage for Azure Storage accounts

**Scenario:** A platform provider outage in your region makes the Azure Storage account unavailable. A Storage outage often affects downstream services. An outage in Azure Storage is unlikely to manifest as a limited scope outage in your workload.

**During the incident:** You can't create new agents that use file-based knowledge as part of their definition. Attempts to add new files as knowledge to agents or into threads result in an error. Agents that don't use file-based knowledge and workloads that don't support file uploads see no change, assuming the issue is limited to normal runtime usage of your Storage account.

**Recovery steps:**

1. Decide whether to wait for service recovery or initiate a failover. If multiple services experience outages due to Storage being down, failing over your Storage account might not recover the whole system.
1. If you choose to proceed with the failover, use the Azure Az PowerShell module to [initiate the customer-managed (unplanned) failover](/azure/storage/common/storage-initiate-account-failover?tabs=azure-powershell#initiate-the-failover) to your account's secondary region:

   ```powershell
   # Check current geo-replication status
   $account = Get-AzStorageAccount -ResourceGroupName "<your-resource-group>" `
     -Name "<your-storage-account>" -IncludeGeoReplicationStats
   $account.GeoReplicationStats

   # Initiate unplanned failover (runs as background job)
   $job = Invoke-AzStorageAccountFailover -ResourceGroupName "<your-resource-group>" `
     -Name "<your-storage-account>" -Force -AsJob
   $job | Wait-Job
   ```

   **Reference:** [Invoke-AzStorageAccountFailover](/powershell/module/az.storage/invoke-azstorageaccountfailover)

1. Wait for the failover to complete.

**Results:**

- Agent capability is temporarily recovered to a failover Storage region. Calls to Azure Storage are routed to the secondary region until the primary region is restored as the write region.

- Recovery time: 20 or more minutes.

- Recovery point: State is preserved up to about 15 minutes before the Storage account outage. Expect some data loss.

**Failback steps:**

Remember that an unplanned failover is a temporary state, and you must fail back to your primary region. Follow [the unplanned failback process](/azure/storage/common/storage-failover-customer-managed-unplanned?tabs=grs-ra-grs#the-unplanned-failback-process-grsra-grs) once the Storage service fully recovers.

> [!TIP]
> If possible, use a planned maintenance window and shut down traffic to your AI Agent Service data endpoints 10 minutes before failback. This traffic pause ensures that you minimize any data loss during the recovery.

**Results:**

- Agent capability is returned to your primary Storage region.

- Recovery time: 10 or more minutes.

- Recovery point: State is preserved up to about 10 minutes before the Storage failback. Expect some data loss.

## Next step

Account for human-based failures in your recovery design.

> [!div class="nextstepaction"]
> [Resource and data loss recovery strategies](agent-service-operator-disaster-recovery.md)
