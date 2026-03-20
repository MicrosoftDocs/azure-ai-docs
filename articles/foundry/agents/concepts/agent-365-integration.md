---
title: "Microsoft Agent 365 integration with Foundry"
description: "Learn how Microsoft Foundry integrates with Microsoft Agent 365 to provide enterprise-grade agent governance, observability, security, and lifecycle management."
author: deeikele
ms.author: deeikele
ms.reviewer: jburchel
ms.date: 03/19/2026
ms.topic: concept-article
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ai-usage: ai-assisted
#CustomerIntent: As an IT admin or platform engineer, I want to understand how Foundry agents integrate with Agent 365 so that I can plan governance and security for AI agents in my organization.
---

# Microsoft Agent 365 integration with Microsoft Foundry

[Microsoft Agent 365](/microsoft-agent-365/overview) is Microsoft's enterprise control plane for AI agents. It gives IT teams a single place to observe, govern, and secure every agent across an organization, regardless of where that agent was built or acquired. Microsoft Foundry agents integrate with Agent 365 so that organizations can apply consistent identity, security, and lifecycle management policies to agents built in Foundry.

This article explains what Agent 365 provides, how it connects to Foundry, and how data flows between the two platforms.

## Agent 365 core capabilities

Agent 365 is built on five pillars:

| Capability | Description |
|---|---|
| **Registry** | Provides a complete inventory of all agents in the organization, including agents built in Foundry and Copilot Studio, agents registered by administrators, and shadow agents discovered in the tenant. |
| **Access control** | Brings agents under management and limits their access to only the resources they need by using Microsoft Entra ID-based controls and risk-based Conditional Access policies. |
| **Visualization** | Enables organizations to explore connections between agents, people, and data, and to monitor agent behavior and performance in real time. |
| **Interoperability** | Equips agents with access to Microsoft 365 apps and organizational data so they can participate in real workflows. Agents can also connect to Work IQ for organizational context. |
| **Security** | Protects agents from threats and vulnerabilities by integrating with Microsoft Defender, Microsoft Purview, and the broader Microsoft security stack. It also helps protect data agents create or use from oversharing, leaks, and risky behavior. |

For the full list of Agent 365 capabilities and prerequisites, see the [Agent 365 overview](/microsoft-agent-365/overview).

## How Foundry integrates with Agent 365

Foundry and Agent 365 connect in two ways:

- **Automatic registry sync** &mdash; Published Foundry agents automatically appear in the Agent 365 registry. This gives IT administrators a single pane of glass for agent inventory without manual registration.

- **Digital worker publishing** &mdash; Foundry hosted agents can be published as *digital workers* to Agent 365. A digital worker is an agent that acts autonomously on behalf of a user and receives its own Microsoft Entra Agent ID. After publishing and admin approval, the digital worker appears in the Agent 365 registry and can be connected to Microsoft Teams and other Microsoft 365 surfaces.

For step-by-step instructions on publishing a Foundry agent to Agent 365, see [Publish an agent as a digital worker in Agent 365](../how-to/agent-365.md).

### Enablement and data collection

Before Foundry can send agent activity data to Agent 365, your organization must complete two steps:

1. **Obtain a license** &mdash; Your tenant needs at least one Microsoft 365 Copilot license and enrollment in the [Frontier preview program](https://adoption.microsoft.com/copilot/frontier-program/). For licensing details and enrollment FAQs, see [Agent 365 prerequisites](/microsoft-agent-365/overview#prerequisites).
1. **Enable Agent 365 and accept terms** &mdash; A global administrator signs into the [Microsoft 365 admin center](https://admin.microsoft.com/), navigates to **Copilot** > **Settings** > **User access** > **Copilot Frontier**, and selects which users or groups get access. The administrator is prompted to agree to the terms of service before Agent 365 is activated. For the full walkthrough, see [Enable Agent 365](/microsoft-agent-365/overview#enable-agent-365).

Both steps are required before any data flows from Foundry to Agent 365, even if the Azure Resource Manager properties on a Foundry resource are set to enabled. For a summary of how data residency differs between the two platforms, see [Data residency](#data-residency).

After these steps are complete, agent activity data from Foundry is ingested into the Agent 365 control plane, powering the registry, analytics dashboards, and security features. Logging is controlled per Foundry resource through the `agent365Config` resource provider configuration. For details on how logging works and how to opt out, see [Configure Agent 365 data collection for Microsoft Foundry](../how-to/configure-agent-365-data-collection.md).

> [!NOTE]
> Even if the logging property is set to enabled on a Foundry resource, no data is ingested unless your tenant has a valid Agent 365 license and the administrator has accepted the Agent 365 terms of service.

## Data residency

Microsoft Foundry and Agent 365 follow different data residency models:

| Platform | Data residency model |
|---|---|
| **Microsoft Foundry** | Data residency follows the **Azure region** you select when creating the Foundry resource. All agent data, model deployments, and logs remain in that region. |
| **Microsoft Agent 365** | Data residency follows the **storage location of the Microsoft Entra ID tenant**. Agent inventory, analytics, and governance data are stored in the geography associated with the tenant. |

When agent activity data flows from Foundry into Agent 365, it moves from the Azure region-based residency model to the Entra ID tenant-based residency model. For workloads with specific data residency requirements, you can opt out individual Foundry resources from Agent 365 data collection while keeping other resources enabled. This lets you maintain Agent 365 governance for most of your estate and restrict data flows only where regulations require it. For details, see [Configure Agent 365 data collection for Microsoft Foundry](../how-to/configure-agent-365-data-collection.md).

## Related content

- [Configure Agent 365 data collection for Microsoft Foundry](../how-to/configure-agent-365-data-collection.md)
- [Publish an agent as a digital worker in Agent 365](../how-to/agent-365.md)
- [Agent identity concepts in Microsoft Foundry](agent-identity.md)
- [Agent 365 overview](/microsoft-agent-365/overview)
