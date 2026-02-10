---
title: Foundry Agent Service disaster recovery
monikerRange: 'foundry-classic || foundry'
ms.service: azure-ai-foundry
ms.reviewer: ckittel
description: "Plan disaster recovery for Foundry Agent Service: limitations, readiness checklist, and recovery paths for platform outages and data loss."
#customer intent: As a developer, I want to automate the redeployment of agent definitions so that I can speed up disaster recovery processes.
author: jonburchel
ms.author: jburchel
ms.date: 01/20/2026
ms.topic: reliability-article
ms.collection: ce-skilling-ai-copilot
ai-usage: ai-assisted
ms.custom: pilot-ai-workflow-jan-2026
---

# Foundry Agent Service disaster recovery

[!INCLUDE [version-banner](../includes/version-banner.md)]

Use this article as the starting point for disaster recovery (DR) planning for Foundry Agent Service in the [Standard deployment mode](/azure/ai-foundry/agents/concepts/standard-agent-setup). It explains what you can and can't recover, what to prepare before an incident, and where to find recovery procedures for platform outages and resource or data loss.

> [!IMPORTANT]
> This is the overview article in a three-part series.
>
> - You're here: Understand limitations, prevention controls, and required baseline configuration.
> - For prolonged regional outages and platform incidents, see [Agent Service platform outage recovery strategies](./agent-service-platform-disaster-recovery.md).
> - For human-caused or automation-caused deletions and localized data loss, see [Agent Service resource and data loss recovery strategies](./agent-service-operator-disaster-recovery.md).
>
> To reduce the likelihood of recovery events, see [High availability and resiliency for Foundry projects and agent services](high-availability-resiliency.md).

## Scope and definitions

This series focuses on DR for Foundry projects that use Agent Service in Standard deployment mode.

- **Blast radius boundary**: In most workloads, a single Foundry project is the recovery unit.
- **State**: Agent definitions, conversation threads (including user-uploaded files), and any file-based knowledge stored in the capability host dependencies.
- **Data plane APIs**: APIs used to create, update, and invoke agents and threads. For details, see [AI Agents REST API operation groups](/rest/api/aifoundry/aiagents/operation-groups).

For general recovery design concepts (including setting recovery objectives such as RPO and RTO), see [Design for recovery](/azure/well-architected/reliability/principles#design-for-recovery).

## DR readiness checklist

Complete these actions before you rely on Agent Service in production:

1. Choose a recovery strategy per project (for example, warm standby and reconstruction) and document your recovery objectives.
1. Configure required baseline protections and recovery features on your dependencies. For guidance, see [High availability and resiliency for Foundry projects and agent services](high-availability-resiliency.md).
1. Treat agent definitions as code. Store agent definitions, knowledge assets, and tool bindings in source control so you can redeploy them quickly.
1. Automate redeployment of agents and any client updates needed for new agent IDs.
1. Practice recovery. Run periodic drills so operators can execute the recovery steps under time pressure.

Agent Service deployments can encounter incidents that affect availability and data integrity in these components:

- **Data plane APIs**: Services responsible for creating, updating, and invoking agents
- **Agent capability host**: Per-project infrastructure that houses your agents
- **Agent definitions**: Prompts, knowledge connections, file-based context, and tool integrations
- **Conversation threads**: Text conversations and user-uploaded files

Disasters stem from prolonged platform outages, or from human or automation errors. Incidents in any component can make one or more agents unreachable or inoperable. Some incidents stop normal service operation.

Agent Service is stateful. Recovery focuses on preserving and restoring state stored in your project's Azure Cosmos DB, Azure AI Search, and Azure Storage account. This guide doesn't cover recovery for other Foundry features or for grounding stores or tools used by agents.

## Built-in recovery capabilities

The Agent Service has important limitations that shape your workload's disaster recovery (DR) design. Consider these factors when you set realistic recovery point objectives (RPOs) and recovery time objectives (RTOs).

> [!IMPORTANT]
> Agent Service doesn't provide built-in disaster recovery capabilities. It doesn't replicate state, create backups, or support point-in-time restore. One project can't use the data of another project. The service doesn't have any supported method for active-active, multi-region replication. Microsoft Support can't recover orphaned data, migrate data between projects, or combine state from multiple sources.
>
> The recommendations in this guide are compensating controls. Recovery might not be possible. An incident can permanently remove an agent and its data, such as threads and knowledge.

## Unrecoverable scenarios and expectations

Plan for scenarios where recovery isn't possible or where recovery restores only functionality (not state):

- **Thread deletion**: There isn't a supported way to restore a deleted conversation thread.
- **Project reconstruction**: If a project is deleted and you recreate it, you redeploy agents as new resources with new agent IDs. Thread history and user-uploaded files from the deleted project aren't recoverable.
- **Cross-region failover**: In a regional outage, you typically restore service by recreating projects and redeploying agents in another region. Standby-region agents don't have access to prior threads, and any standby-region state is lost during failback.
- **State migration**: There isn't a supported way to merge or migrate agent state between projects or between regions.

### General implications for your recovery design

- Treat each independent workload capability as an isolated blast radius. Design recovery decisions and procedures to support independent recovery. This boundary is usually a single Foundry project, but it can be multiple projects that share the same dependencies and recovery requirements.
- The recovery point for stateful content can be total loss. Plan for business and user acceptance of that loss.
- Recovery time mostly depends on how fast you can reapply infrastructure as code and redeploy agent definitions. Invest in automation accordingly.
- Warm standby environments start mostly empty. Recovery is reconstruction, not promotion of a hot replica.
- Avoid designs or user expectations that assume you can later consolidate a recovery environment's data back into a production environment's data.

## Disaster prevention

Preventing disasters is easier and less costly than recovering from them. Stop disasters from happening in the first place by applying proactive measures. For more information, see [High availability and resiliency for Foundry projects and agent services](high-availability-resiliency.md#disaster-prevention).

## Resource configuration to support recovery

Configure your resources to support recovery before an incident happens. Enable specific features and settings that facilitate recovery processes. For more information, see [High availability and resiliency: Resource configuration to support recovery](high-availability-resiliency.md#resource-configuration-to-support-recovery).

## Recover from Azure outages

In the standard deployment model, the Agent Service is a jointly managed service. Microsoft operates and maintains the control plane and capability host. You operate the agent stateful resources; Azure Cosmos DB, Azure AI Search, and Azure Storage account. All of these services depend on your deployment region's availability. If Azure is experiencing a prolonged region-wide outage, your approach to recovery focuses on getting another instance running in a region that isn't experiencing an outage.

> [!div class="nextstepaction"]
> [Agent Service platform outage recovery strategies](agent-service-platform-disaster-recovery.md)

## Recover from resource and data loss incidents

The Agent Service has a significant amount of state and interconnected resources that you're responsible for in your workload. A user or automation process can delete or corrupt that state. The disruption might be accidental or malicious. Your recovery approach varies based on which resource or data element was lost.

> [!div class="nextstepaction"]
> [Agent Service resource and data loss recovery strategies](agent-service-operator-disaster-recovery.md)

## Business continuity

Disaster recovery is only one part of your business continuity strategy. For agent-based flows, plan how you continue to deliver value when agents are inoperable or data is lost. Set realistic expectations with users and business partners. Fall back to planned contingencies as needed.

For example, the Purview integration provides a compliance safety net for workloads that require eDiscovery. If agents and their threads are lost, you can still respond to eDiscovery requests by using Purview. This approach doesn't restore agent functionality or data, but it helps you meet compliance continuity needs.

Likewise, if your agent provides customer support capabilities to reduce the amount of human time spent with individual customers, you can fall back to email or phone support operations when agents are unavailable. Planned graceful degradation in your workload should direct workload users to alternatives.

## Next steps

Start your Agent Service DR design with [recovery strategies for platform outages](agent-service-platform-disaster-recovery.md), and then plan your [resource and data loss recovery strategies](agent-service-operator-disaster-recovery.md).

To reduce incident likelihood and improve recovery readiness, follow [High availability and resiliency for Foundry projects and agent services](high-availability-resiliency.md).
