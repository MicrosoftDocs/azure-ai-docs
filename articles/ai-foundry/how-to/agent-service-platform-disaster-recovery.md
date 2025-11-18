---
title: Foundry Agent Service platform outage recovery
ms.service: azure-ai-foundry
ms.reviewer: ckittel
description: Recover Foundry Agent Service projects from Azure platform and regional outages with warm standby, failover, and failback procedures.
monikerRange: 'foundry-classic || foundry'
#customer intent: As a developer, I want to understand how to recreate projects in a standby region so that I can restore critical functionality during a regional outage.
author: jonburchel
ms.author: jburchel
ms.date: 11/18/2025
ms.topic: reliability-article
ms.collection: ce-skilling-ai-copilot
ms.custom: arb-aiml
ai-usage: ai-assisted
---

# Foundry Agent Service platform outage recovery

[!INCLUDE [version-banner](../includes/version-banner.md)]

This article covers recovery from Azure platform incidents that take an entire region or a regional dependency offline, for example, a prolonged regional outage or loss of a stateful dependency.

The recommended approach to [design for recovery](/azure/well-architected/reliability/principles#design-for-recovery) in your workload is a warm standby, failover, and failback plan for mass outages combined with per-service recovery capabilities for localized outages.

> [!IMPORTANT]
> This is one article of a three-part series.
>
> Read the overview guide first to understand platform limitations, prevention controls, and required baseline configuration. For prerequisites and context, see [Foundry Agent Service disaster recovery](./agent-service-disaster-recovery.md). This article explains why some losses are unrecoverable and why recovery often means reconstruction rather than restoration.
>
> If you're looking for recommendations on recovering from human-caused or automation-caused deletions and localized data loss, see [Resource and data loss recovery](./agent-service-operator-disaster-recovery.md).

## Architecture preparation

Establish and maintain a warm standby environment in a paired or otherwise acceptable region. This environment supports an active-passive approach that reduces recovery time with limited idle cost.

- Create a virtual network in the failover region that mirrors the primary region's subnet topology and all required cross-premises connectivity. Keep egress controls and firewall rules synchronized while this environment is idle.
- Create a Microsoft Foundry account with agent capability enabled in that network. Don't create projects, project-specific connections, or model deployments.
- Enable Azure diagnostics, Defender for Cloud, and Purview integration on the standby account, matching the configuration of your production instance.

Maintain this low-idle-cost, fully networked warm standby account. It hosts no projects during normal operations. Re-create only needed projects (and their dependencies) during failover based on business criticality and during failover drills.

### Gateway routing

If your clients' configurations are outside your control, add a layer of indirection between your clients and the Agent Service [data plane APIs](/rest/api/aifoundry/aiagents/operation-groups). Implement the [Gateway Routing](/azure/architecture/patterns/gateway-routing) pattern in a multiregion gateway such as [API Management configured for multiple regions](/azure/api-management/api-management-howto-deploy-multi-region). This indirection lets you fail over the data plane APIs without updating your clients' fully qualified domain name (FQDN) configuration by instead updating failover routing inside the gateway.

## Complete regional outage

**Scenario:** The primary region hosting your Foundry account and dependencies is unavailable because of a platform provider outage that renders all resources in your primary region unavailable.

**During the incident:** Complete outage. You can't create, delete, modify, or invoke agents in any projects. Data plane API calls error or time-out. The Foundry portal is unavailable for the whole account.

### Fail over to secondary region

For each project, decide whether to recover. Compare the project's business continuity requirement with the outage's expected duration, business consequences, and alternative continuity plans.

Don't fail over a project's agents if required knowledge stores and tools don't also fail over. If you own those stores and tools, run their recovery playbooks first.

For *each project* you choose to recover, follow these steps:

1. Deploy the project's capability host dependencies (Azure Cosmos DB, Azure AI Search, Azure Storage) in the recovery region using your infrastructure as code (IaC) assets. Match topology and configuration. If multiple projects share the same dependencies, do this step only once.

      > [!TIP]
   > Pre-provisioning these resources reduces recovery time but increases cost and operational overhead. A hybrid approach is possible. For example, Azure Storage is already deployed because it's inexpensive when idle; Azure AI Search isn't.

1. Create the project's user-assigned managed identity. Give it access to the new regional dependencies.

1. Create the project in the standby Foundry account via IaC and assign the managed identity. Point the project's capability host to the new regional dependencies. Apply role assignments for clients, operators, and automation principals.

1. Redeploy agents (definitions, knowledge files, and tool connections) from source control or application code. They're new agents with new IDs and have **no access** to prior threads or files.

1. Recover any client components, if part of the workload, per their recovery playbooks.

1. Update clients to use the new Foundry account fully qualified domain name (FQDN) and new agent IDs.

   If an AI gateway pattern is used, then clients will continue to use the gateway's FQDN. The gateway configuration will instead need to be updated to route requests to the newly created project on behalf of it clients.

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

### What about multi-region support on the Agent Service dependencies?

Using multi-region writes and reads on Azure Cosmos DB doesn't improve recovery. The `enterprise_memory` database partitions data by a globally unique identifier per project instance. A multi-region write topology doesn't prevent data loss on failback because data created during the failover is in containers keyed to new project IDs. You must still manage role-based access control (RBAC) for the new project identity. Use a new temporary Azure Cosmos DB instance during the failover.

Using Azure Storage multi-region recovery also doesn't improve recovery outcomes. Like Azure Cosmos DB, the data in this account is partitioned by a globally unique identifier per project and so the same limitations apply.

## Complete regional outage for Azure Cosmos DB accounts

**Scenario:** The Azure Cosmos DB account used by your Agent Service is unavailable due to a platform provider outage in your region. No other services are affected in this outage.

**During the incident:** Complete outage of all projects that used the `enterprise_memory` database in this Azure Cosmos DB instance. You can't create, delete, modify, or invoke agents. All calls to the Foundry data plane APIs return errors. The agent experience in the Foundry portal isn't available for the account.

**Recovery steps:**

The Azure Cosmos DB team initiates a service-managed failover automatically based on internal decisions that you can't directly influence. Normally, you wait until this failover occurs and don't take self-directed action. After the incident, possibly three or more days later, the team fails your instance back to the primary region.

> [!TIP]
> If you have a business-critical need to fail over sooner, you can initiate a [forced failover](/azure/cosmos-db/how-to-manage-database-account#perform-forced-failover-for-your-azure-cosmos-db-account) to your failover region. This causes data loss for any writes that haven't been replicated to the failover region yet.

**Results:**

- Agents might experience intermittent connectivity issues during failover and failback. Calls to Azure Cosmos DB are routed to your secondary region until the primary region is restored as the write region.

- **Recovery time:** Once triggered by the Azure Cosmos DB team or a forced failover, expect 30 minutes or more.

- **Recovery point:** Depending on the outage, up to 15 minutes of data might be permanently lost. This includes agents created, updated, or deleted just before the outage and threads created or updated just before the outage.

## Complete regional outage for Azure AI Search services

**Scenario:** The Azure AI Search service used by your Agent Service for real-time indexing is unavailable due to a platform provider outage in your region. Connected pre-indexed knowledge stored in other Azure AI Search services is likely also affected by this outage, but its recovery falls on the data owner for that service and is out of scope for this article. No other services are affected in this outage.

**During the incident:** Agents with file-based knowledge generate an error when they consult that knowledge. Threads that involved uploaded files return errors if the agent attempts to recall indexed data. Attempts to add files as knowledge to agents or into threads result in an error. Agents that don't use file-based knowledge and workloads that don't support file uploads likely experience no change.

**Recovery steps:** None. Wait until the Azure AI Search service is restored in your primary region. Consider going into a graceful degradation state in your workload that avoids any file uploads during this period.

> [!IMPORTANT]
> If you have a business-critical need to fail over sooner, [Perform a destructive reset of the Azure AI Agent Service capability host](./agent-service-operator-disaster-recovery.md#perform-a-destructive-reset-of-the-azure-ai-agent-service-capability-host) and use a new AI Search instance in your failover region. This causes *complete data loss* in your production instance. When AI Search is available again in your primary region, perform the same destructive reset action again.
>
> We don't advise this approach unless your users are tolerant of thread loss and your agents can easily rehydrate their file-based knowledge.

**Results:**

- Agent capability fully recovered.

- Recovery time: indeterminate.

- Recovery point: state preserved up to the AI Search outage; in-flight operations near the outage might not persist.

## Complete regional outage for Azure Storage accounts

**Scenario:** The Azure Storage account used by your Agent Service is unavailable due to a platform provider outage in your region. A Storage outage often affects downstream services. An outage in Azure Storage is unlikely to manifest as a limited scope outage in your workload.

**During the incident:** You can't create new agents that use file-based knowledge as part of their definition. Attempts to add new files as knowledge to agents or into threads result in an error. Agents that don't use file-based knowledge and workloads that don't support file uploads see no change, assuming the issue is limited to normal runtime usage of your Storage account.

**Recovery steps:**

1. Decide whether to wait for service recovery or initiate a failover. If multiple services experience outages due to Storage being down, failing over your Storage account might not recover the whole system.
1. If you choose to proceed with the failover, use the Azure Az PowerShell module to [initiate the customer-managed (unplanned) failover](/azure/storage/common/storage-initiate-account-failover?tabs=azure-powershell#initiate-the-failover) to your account's secondary region.
1. Wait for the failover to complete.

**Results:**

- Agent capability is temporarily recovered to a failover Storage region. Calls to Azure Storage are routed to the secondary region until the primary region is restored as the write region.

- Recovery time: 20 or more minutes.

- Recovery point: State is preserved up to about 15 minutes before the Storage account outage. Expect some data loss.

**Failback steps:**

Remember that an unplanned failover is a temporary state, and you must fail back to your primary region. Follow [the unplanned failback process](/azure/storage/common/storage-failover-customer-managed-unplanned?tabs=grs-ra-grs#the-unplanned-failback-process-grsra-grs) once the Storage service has fully recovered.

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