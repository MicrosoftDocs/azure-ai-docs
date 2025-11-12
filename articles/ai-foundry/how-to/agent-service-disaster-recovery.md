---
title: Foundry Agent Service disaster recovery
monikerRange: 'foundry-classic || foundry'
ms.service: azure-ai-foundry
ms.reviewer: ckittel
description: Learn about disaster recovery patterns and best practices for Foundry Agent Service to ensure business continuity and resilience.
#customer intent: As a developer, I want to automate the redeployment of agent definitions so that I can speed up disaster recovery processes.
author: jonburchel
ms.author: jburchel
ms.date: 11/18/2025
ms.topic: reliability-article
ms.collection: ce-skilling-ai-copilot
ai-usage: ai-assisted
---

# Foundry Agent Service disaster recovery

[!INCLUDE [version-banner](../includes/version-banner.md)]

This three-article series provides disaster recovery guidance for Foundry Agent Service, focusing on the Standard deployment mode. It explains how to prepare Azure resources, execute recovery procedures, and identify failure scenarios you can't fully recover from.

Azure AI Agent Service deployments can encounter incidents that affect availability and data integrity in these components:

- **Data plane APIs**: Services responsible for creating, updating, and invoking agents
- **Agent capability host**: Per-project infrastructure that houses your agents
- **Agent definitions**: Prompts, knowledge connections, file-based context, and tool integrations
- **Conversation threads**: Text conversations and user-uploaded files

Disasters stem from prolonged platform outages, or from human or automation errors. Incidents in any component can make one or more agents unreachable or inoperable. Some incidents stop normal service operation.

The AI Agent Service is stateful. Recovery focuses on preserving and restoring that state stored in your project's Azure Cosmos DB, Azure AI Search, and Azure Storage account. This guide doesn't cover recovery for other Microsoft Foundry features or for grounding stores or tools used by agents.

## Built-in recovery capabilities

The Agent Service has important limitations that shape your workload's disaster recovery (DR) design. Consider these factors when you set realistic recovery point objectives (RPOs) and recovery time objectives (RTOs).

> [!IMPORTANT]
> Agent Service doesn't provide built-in disaster recovery capabilities. It doesn't replicate state, create backups, or support point-in-time restore. One project can't use the data of another project. The service doesn't have any supported method for active-active, multi-region replication. Microsoft Support can't recover orphaned data, migrate data between projects, or combine state from multiple sources.
>
> The recommendations in this guide are compensating controls. Recovery might not be possible. An incident can permanently remove an agent and its data, such as threads and knowledge.

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

Start your Foundry Agent Service design with [recovery strategies for platform outages](agent-service-platform-disaster-recovery.md), and then plan your [resource and data loss recovery strategies](agent-service-operator-disaster-recovery.md).