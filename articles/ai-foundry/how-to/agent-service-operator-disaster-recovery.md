---
title: Foundry Agent Service resource and data loss recovery
monikerRange: 'foundry-classic || foundry'
ms.service: azure-ai-foundry
ms.reviewer: ckittel
description: Recover Foundry Agent Service projects from human or automation errors, accidental deletions, and stateful dependency loss or corruption.
#customer intent: As a developer, I want to recreate a Microsoft Foundry project after accidental deletion so that I can redeploy agents and resume operations.
author: jonburchel
ms.author: jburchel
ms.date: 11/18/2025
ms.topic: reliability-article
ms.collection: ce-skilling-ai-copilot
ms.custom: arb-aiml
ai-usage: ai-assisted
---

# Foundry Agent Service resource and data loss recovery

[!INCLUDE [version-banner](../includes/version-banner.md)]

This article covers recovery from human or automation-caused incidents that result in Azure resource or data loss for Foundry Agent Service projects using the [Standard deployment mode](/azure/ai-foundry/agents/concepts/standard-agent-setup). Incidents include accidental deletion of Microsoft Foundry accounts or projects, deletion of agents or threads, and loss or corruption of state in Azure Cosmos DB, Azure AI Search, or Azure Storage that supports the capability host.

> [!IMPORTANT]
> This is one article of a three-part series.
>
> Read the overview guide first to understand platform limitations, prevention controls, and baseline configuration. See [Agent Service disaster recovery](./agent-service-disaster-recovery.md) for prerequisites and context. That article explains why some losses are unrecoverable and why recovery often means reconstruction rather than restoration.
>
> To learn how to architect your solution for high availability and resiliency to prevent these scenarios, see [High availability and resiliency](high-availability-resiliency.md).
>
> If you're looking for recommendations on how to recover from platform or regional outages, see [Platform outage recovery](./agent-service-platform-disaster-recovery.md) for warm standby, regional failover, and failback.

## Foundry accounts and projects

The following sections describe recovery strategies for incidents that affect a Foundry account or any of its projects. These recovery steps assume that you [configured your resources](./agent-service-disaster-recovery.md#resource-configuration-to-support-recovery) to enable recovery and that prevention measures didn't work.

### Foundry account deleted

**Scenario:** Your Foundry account with production projects and agents is deleted.

**During the incident:** Complete outage. You can't create, delete, modify, or invoke agents. All calls to the Foundry data plane APIs return errors. The Foundry portal is unavailable for the account.

**Recovery steps:**

> [!WARNING]
> These steps completely orphan all agent data within all projects in this account:
>
> - Agent definitions
> - Thread text and files
> - File-based knowledge defined at the agent level
>
> This data resides in the currently associated Azure Cosmos DB, Azure AI Search, and Azure Storage account resources. That data will no longer be associated with this account's projects. The data is permanently orphaned and *can't be recovered through any supported action*.

1. Don't purge the Foundry account resource. A purge makes recovery involve additional steps and considerations not documented here.

1. Within 48 hours, use the [recover account feature](/azure/ai-services/recover-purge-resources). After 48 hours, you can't recover accounts.

1. Account recovery doesn't restore private endpoints. Recreate the three private endpoints in your environment.

1. Account recovery doesn't restore projects. Recreate each project and its capability host, one at a time, from your infrastructure-as-code assets. Start with the project's former *default* project. Use the same project name you had before. Reuse the same capability host dependencies (Azure Cosmos DB, Azure AI Search, and Azure Storage) that were connected to this project before the incident.

   1. Associate the project's former user-assigned managed identity. If you used a system-assigned managed identity, re-enable it. Recreate required role assignments on downstream dependencies and remove orphaned assignments that reference old principal IDs.

   1. Redeploy the project's agents (definitions, knowledge files, and tool connections) from source control or application code. They function as new agents with new IDs and no access to prior threads or data. This *fresh start* restores workload functionality without any historical state.

      > [!TIP]
      > To facilitate this recovery, ensure you maintain your agent definitions, knowledge files, and tool connections in source control. For more information, see [Use repeatable deployment techniques](high-availability-resiliency.md#use-repeatable-deployment-techniques).

   1. Restore role assignments on the project for clients, operators, and automation principals.

   1. Update clients to use the new agent IDs.

1. Reapply your *delete* resource lock.

**Results:**

- All functionality is restored. Clients continue to operate against the same fully qualified domain names (FQDNs) using their existing role assignments, but with new agent IDs.

- Recovery time: 30 or more minutes

- Recovery point: Complete state loss for all agents in all projects in the account. This data isn't recoverable.

#### Foundry project deleted

**Scenario:** A Foundry project with production agents is deleted.

**During the incident:** You can't create, delete, modify, or invoke agents in that project. API calls referencing the project return errors. The portal view for that project is unavailable. Other projects are unaffected.

**Recovery steps:**

> [!WARNING]
> These steps completely orphan all agent data within this project:
>
> - Agent definitions
> - Thread text and files
> - File-based knowledge defined at the agent level
>
> This data resides in the currently associated Azure Cosmos DB, Azure AI Search, and Azure Storage account resources. That data will no longer be associated with this project. Recreate the project by using infrastructure as code so configuration matches the prior state.

   - Reassign the same user-assigned managed identity.
   - Deploy the same capability host configuration referencing the same downstream dependencies.

1. Redeploy agents (definitions, knowledge files, and tools) from source control or application code. They become new agents with new IDs and have **no access** to prior threads or files.

1. Apply a *delete* resource lock on the Foundry account.

**Results:**

- Functionality is restored for the project.

  Clients can continue using the same project name or FQDN patterns; they must update any hard-coded or stored agent IDs.

- Recovery time: minutes

- Recovery point: Total loss of thread text and uploaded files for all agents that were in the project. No recovery of this data is supported.

  > [!IMPORTANT]
  > Even if you use the same Azure Cosmos DB, Azure AI Search, or Azure Storage accounts, lingering data from the previous project's agents isn't reused and is unreachable. There's no supported method to migrate orphaned data to the new project's new capability host.

## Agent Service

The following sections describe recovery strategies for incidents that are localized to the Agent Service, such as specific agents. These recovery steps assume that you [configured your resources](./agent-service-disaster-recovery.md#resource-configuration-to-support-recovery) to enable recovery and that prevention measures failed.

### A production agent is deleted

**Scenario:** A long-lived production agent is accidentally deleted.

**During the incident:** Clients can't invoke or configure this agent. API calls referencing the agent ID return errors. Other agents aren't affected. Existing threads (including those created by the agent) aren't affected.

**Recovery steps:**

1. Redeploy the agent (definitions, knowledge files, and tool connections) from source control or application code. It becomes a new agent with a new ID.
1. Update clients to use the new agent ID and resume interactions on existing threads.

**Results:**

- Agent capability is restored, allowing it to interact with all existing threads and create new threads.

- Recovery time: Minutes

- Recovery point: state preserved up to deletion; in-flight operations at the exact deletion time might not persist.

### A production thread is deleted

**Scenario:** An active thread is accidentally deleted.

**During the incident:** Clients can't continue the conversation in this thread. API calls referencing the thread ID return errors. Other threads aren't affected.

**Recovery steps:** None. There's no supported recovery capability for this scenario.

Cosmos DB's point-in-time restore lets you recover data to a different account, not the same account. Direct manipulation of data (such as trying to recreate the thread's records) in your `enterprise_memory` database isn't a supported action.

**Results:**

- Recovery time: not applicable

- Recovery point: all state in this thread is destroyed. All previously indexed files from the thread are orphaned.

  With Purview integration enabled, you can still respond to eDiscovery requests using Purview's copy of the thread. This approach doesn't restore the thread, but it helps you meet compliance continuity needs.

  Purview's copy might not be fully up to date, as there's an ingestion delay.

## Agent Service dependencies

The following sections describe recovery strategies for incidents that are localized to one of the Agent Service dependencies in the Standard deployment model, such as Azure Cosmos DB. These recovery steps assume that you [configured your resources](./agent-service-disaster-recovery.md#resource-configuration-to-support-recovery) to enable recovery and that prevention measures failed.

### Cosmos DB account is deleted

**Scenario:** The Azure Cosmos DB account hosting the `enterprise_memory` database for one or more projects is accidentally deleted.

**During the incident:** Complete outage for projects configured to use this Cosmos DB account. You can't create, delete, modify, or invoke those projects' agents. The Foundry portal shows frequent error messages and has undefined behavior.

**Recovery steps:**

1. Use the Azure portal, Azure CLI, or Azure PowerShell cmdlet to restore the Azure Cosmos DB account. *Don't* redeploy from your IaC.

   - Restore it to the *exact same* resource group and account name it was before
   - Choose the latest restore point.
   - Azure Cosmos DB charges a nominal fee for this restoration action.
   - Ensure Azure Diagnostics configuration is restored.

   > [!TIP]
   > Your account name was released to the public the moment your account was deleted, you need to be expeditious in this restoration because if your account name is taken by another customer before you restore, you'll experience complete data loss as you'll need to [perform a destructive reset of the Azure AI Agent Service capability host](#perform-a-destructive-reset-of-the-azure-ai-agent-service-capability-host).

1. Apply a [*delete* resource lock](/azure/azure-resource-manager/management/lock-resources) on the Cosmos DB account.

1. Use your IaC to redeploy all of the associated projects' role assignments on this Cosmos DB account and its restored `enterprise_memory` database. The restoration process in the previous step doesn't restore role assignments.

**Results:**

- Agent capability restored.

- Recovery time: 10 or more minutes.

- Recovery point: State preserved up to account deletion; in-flight operations at the exact deletion time might not persist.

### The `enterprise_memory` database is deleted

**Scenario:** The `enterprise_memory` database for one or more projects is accidentally deleted.

**During the incident:** Complete outage for projects configured to use this Cosmos DB account. You can't create, delete, modify, or invoke those projects' agents. The Foundry portal shows frequent error messages and has undefined behavior.

**Recovery steps:**

1. Use the Azure portal, Azure CLI, or Azure PowerShell cmdlet to initiate a point-in-time restore to the same account.

   - Select the `enterprise_memory` database
   - Choose the latest restore point.
   - No role assignments need to be reapplied, they're preserved in this restoration.
   - Azure Cosmos DB charges a nominal fee for this restoration action.

1. Apply a [*delete* resource lock](/azure/azure-resource-manager/management/lock-resources) on the Cosmos DB account.

**Results:**

- Agent capability restored.

- Recovery time: 10 or more minutes.

- Recovery point: State preserved up to database deletion; in-flight operations at the exact deletion time might not persist.

### A container in the `enterprise_memory` database is deleted

**Scenario:** A container in the `enterprise_memory` database is accidentally deleted.

**During the incident:** Deleting the container halts availability of agents within a single Foundry project. You can't create, delete, modify, or invoke that project's agents. The Foundry portal shows error messages and has undefined behavior. Other projects' agents are unaffected.

**Recovery steps:**

Use the Azure portal, Azure CLI, or Azure PowerShell cmdlet to initiate a point-in-time restore to the same account.

   - Select the `enterprise_memory` database.
   - Choose the [latest restore point](/azure/cosmos-db/restore-account-continuous-backup) for the deleted container.
   - No role assignments need to be reapplied, they're preserved with this restoration.
   - Azure Cosmos DB charges a nominal fee for this restoration action.

**Results:**

- Agent capability restored.

- Recovery time: 10 or more minutes.

- Recovery point: State preserved up to container deletion; in-flight operations at the exact deletion time might not persist.

### Data within one or more containers in the `enterprise_memory` database is deleted or corrupted

**Scenario:** One or more of the containers in the `enterprise_memory` experiences a loss of data or data corruption through unsupported direct Cosmos DB data plane API or portal interaction.

**During the incident:** Corruption or deletion of data within a container creates unpredictable loss of availability. Which agents or threads fail depends on the affected containers and the projects they serve. One agent or thread might fail, or several projects could be disrupted. Failures appear as inability to invoke an agent or interact with a thread. You can still create new agents and new threads.

**Recovery steps:**

Generally speaking, there are no specific recovery capabilities for this scenario. If you lost thread database records, then see [a production thread is deleted](#a-production-thread-is-deleted) for details about this scenario. If you lost agent records, follow the [a production agent is deleted recovery process](#a-production-agent-is-deleted).

> [!NOTE]
> The point-in-time restore capability in Cosmos DB isn't helpful against data-level loss or corruption such as those described here; it only supports recovery from container, database, or account deletes.

**Results:**

- Recovery time: Situational.

- Recovery point: Total loss for the affected entities. You likely lost one or more agents or threads with no state recovery possible.

  If you lost a thread, you can still respond to eDiscovery requests using Purview's copy of the thread, which wouldn't mirror this direct data delete or corruption.

### AI Search service is deleted

**Scenario:** The Azure AI Search service providing real-time indexing capabilities for agents and threads in one or more projects is accidentally deleted.

This instance is not to be confused with any AI Search indexes that are connected to products and used as a durable knowledge store for workload data. Recovery of those search indexes should follow the guidelines at [Reliability in Azure AI Search](/azure/reliability/reliability-ai-search). This instance is specifically the dedicated instance supporting the Agent Service runtime.

**During the incident:** Agents with file-based knowledge generate errors when they consult that knowledge. Threads that involved uploaded files return errors if the agent recalls indexed data. Attempts to add files as knowledge to agents or into threads fail. Agents that don't use file-based knowledge and workloads without file uploads likely see no change. The capability host is considered broken and future behavior is undefined.

**Recovery steps:**

1. Use your IaC to deploy a new instance of Azure AI Search and its private endpoints.

   - Use the *exact same* resource group and service name it was before.
   - Redeploy all of the associated projects' role assignments on this Azure AI Search service.
   - Ensure Azure Diagnostics configuration is restored.

   > [!TIP]
   > Your service name was released to the public the moment your service was deleted, you need to be expeditious in this restoration because if your service name is taken by another customer before you restore, you'll experience complete data loss as you'll need to [perform a destructive reset of the Azure AI Agent Service capability host](#perform-a-destructive-reset-of-the-azure-ai-agent-service-capability-host).

1. Apply a *delete* resource lock on the AI Search service.

1. Delete all agents that used file-based knowledge then redeploy those agents (definitions, knowledge files, and tool connections) from source control or application code. They become new agents with new IDs, having new indexes created for them with their file data.

1. Update clients to use the new agent IDs and resume interactions on existing threads.

If you've gone against the [single responsibility principle recommendation](high-availability-resiliency.md#implement-the-single-responsibility-principle) and combined both Agent Service runtime usage and durable workload knowledge into a single AI Search instance, recovery needs to be a combination of what's was presented here and a [rehydration of your durable knowledge store](/azure/reliability/reliability-ai-search#backups).

**Results:**

- Agent capability mostly restored. Existing threads experience an unpredictable user experience if they had state indexed in the deleted AI Search service. New threads operate as normal.

- Recovery time: 20 or more minutes.

- Recovery point: Complete and unrecoverable loss of state for all existing threads. File-based state for agent knowledge is reconstructed.

### An index in your AI Search service is deleted

**Scenario:** An individual index in the Azure AI Search service providing real-time indexing capabilities for agents and threads in one or more projects is accidentally deleted.

**During the incident:** Depending on which index was deleted, an agent may lose access to its file knowledge and produce errors, or a thread with uploaded files returns errors and an undefined experience when the agent recalls previously indexed data.

**Recovery steps:**

If the index was tied to an agent's direct file knowledge:

1. Delete all agents that used file-based knowledge then redeploy those agents (definitions, knowledge files, and tool connections) from source control or application code. They become new agents with new IDs, having new indexes created for them.
1. Update clients to use the new agent IDs and resume interactions on existing threads.

If the index was tied to knowledge uploaded as part of a thread, there's no recovery steps for this situation.

**Results:**

- Agent capability mostly restored. If the index was related to an existing thread, that thread has an unpredictable user experience. Other threads and all new threads operate as normal.

- Recovery time: Minutes.

- Recovery point: Complete and unrecoverable loss of state for any directly affected threads. File-based state for agent knowledge is reconstructed.

## Perform a destructive reset of the Azure AI Agent Service capability host

When other recovery options aren't available, you can perform a complete reset of your project's AI Agent Service capability host. This reset is a *fresh start* that restores functionality but permanently orphans all agents, threads, and related state.

> [!CAUTION]
> Performing these steps orphans all existing agent state, making all agent data permanently unretrievable through any Foundry Agent Service API call. This process restores functionality but *provides no data recovery point*.
>
> This is a **last resort** after you exhaust all other options. **All agents and threads are permanently lost.**

1. Remove the *delete* lock from the Foundry account.

1. Delete the project's capability host by issuing a [Project Capability Hosts - Delete](/rest/api/aifoundry/accountmanagement/project-capability-hosts/delete) API request for the project that you're resetting.

   > [!WARNING]
   > This operation completely orphans all agent data:
   >
   > - Agent definitions
   > - Thread text and files
   > - File-based knowledge defined at the agent level
   >
   > This data resides in the currently associated Azure Cosmos DB, Azure AI Search, and Azure Storage account resources. The data is no longer associated with this project. The data is considered permanently orphaned and *can't be recovered through any supported action*.

1. Reapply the *delete* lock to the Foundry account.

1. Re-create the project's capability host by using infrastructure as code or a [Project Capability Hosts - Create](/rest/api/aifoundry/accountmanagement/project-capability-hosts/create-or-update) API request.

   Before you re-create the capability host, ensure that:

   - Your Azure Cosmos DB, Azure AI Search, and Azure Storage accounts are deployed
   - The project's managed identity has the same permissions to these resources as before the reset

   > [!IMPORTANT]
   > Even if you reuse the same Azure Cosmos DB, Azure AI Search, or Azure Storage accounts, lingering data from the previous association isn't reused and is unreachable. No supported method exists to migrate orphaned data to the new capability host.

1. Redeploy agents from source control or from application code. They function as new agents with new IDs and no access to prior threads or data. This *fresh start* restores workload functionality without any historical data.

## Related content

- [High availability and resiliency for Microsoft Foundry projects and Agent Services](high-availability-resiliency.md)
- [Agent Service disaster recovery](agent-service-disaster-recovery.md)

## Next step

Account for platform failures in your recovery design.

> [!div class="nextstepaction"]
> [Recovery strategies for platform outages](agent-service-platform-disaster-recovery.md)
