---
title: "Deep dive into Foundry Agent Service networking"
description: "Understand the network architecture, subnet sizing, IP allocation, and traffic flow for hosted and prompt agents in Microsoft Foundry Agent Service with bring-your-own VNet."
author: aahill
ms.author: aahi
ms.date: 09/07/2026
ms.manager: mcleans
ms.topic: concept-article
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.custom: references_regions, doc-kit-assisted
ai-usage: ai-assisted
---

# Deep dive into Foundry Agent Service networking

When you run Microsoft Foundry Agent Service with a bring-your-own virtual network (VNet), you're responsible for sizing the delegated subnet, planning IP allocation, and understanding how agent traffic flows through the platform. This article explains the network architecture behind hosted and prompt agents, the IP-allocation model, and the signals that indicate capacity issues. It's intended for cloud and network architects who already chose bring-your-own VNet for Foundry Agent Service. To configure the network, see [Set up private networking for Foundry Agent Service](../how-to/virtual-networks.md).

If you use a coding agent like GitHub Copilot to plan your VNet, subnet, and capacity model, the [Microsoft Foundry Skill](../../how-to/develop/use-microsoft-foundry-skill.md) can help you reason through the architecture and apply Foundry networking guidance in your own environment.

## Network architecture overview

The following diagram shows the two zones involved in any Foundry Agent Service request: the Microsoft-managed Foundry platform network on the left, and your customer VNet on the right.

:::image type="content" source="../media/networking-deep-dive/architecture.png" alt-text="Architecture diagram showing the Foundry platform network on the left with the Foundry endpoint, a Micro VM host layer, the Tools Service, and the Data Proxy host layer. On the right, the customer VNet contains a delegated subnet that holds Micro VMs and the Data Proxy on Azure Container Apps, plus a separate private endpoint subnet for storage, SQL Database, and Key Vault. Arrows show Hosted agent traffic flowing through the Micro VM and prompt agent traffic flowing directly through the Tools Service. Both paths converge at the Data Proxy and egress to customer resources through private endpoints." lightbox="../media/networking-deep-dive/architecture.png":::

The platform network hosts the Foundry endpoint, the Micro VM host layer that runs Hosted agents, the Tools Service, and the Data Proxy host layer. Your customer VNet contains a delegated subnet (where Micro VMs and the Data Proxy consume IPs) and a private endpoint subnet that connects to your storage, databases, and Key Vault.

Two request flows traverse this architecture:

- **Hosted agent**: Client to Foundry endpoint to Micro VM (`/invoke`) to Tools Service to Data Proxy to customer resources through private endpoints.
- **Prompt agent**: Client to Foundry endpoint to Tools Service to Data Proxy to customer resources through private endpoints. There's no Micro VM on this path.

## Key concepts

| Term | What it means |
|------|---------------|
| **Foundry instance** | Your Microsoft Foundry resource. The top-level container that holds your projects, agents, and networking configuration. |
| **Hosted agent** | An agent you build and deploy yourself by using your own container image through Azure Container Registry. You control CPU, memory, and code. |
| **Prompt agent** | An agent where compute and scaling are fully managed by Microsoft. You define behavior through configuration. No container image or infrastructure management is required. |
| **Single-tenant data proxy** | A platform-managed networking component dedicated to your Foundry project that handles outbound connectivity for your agents. Each project gets its own isolated data proxy instance. All tool calls route through the data proxy. |
| **Tool server** | A backend service registered at the project level that your agents can call to perform actions, such as querying a database or invoking an external API. In bring-your-own VNet configurations, tool server traffic routes through the single-tenant data proxy. |
| **Delegated subnet** | The subnet in your VNet that you delegate to Foundry Agent Service. All agent infrastructure (data proxies and Micro VMs) deploys into this subnet and consumes IPs from it. |
| **Micro VM** | The lightweight virtual machine that runs a Hosted agent. |
| **Version** | A change that affects how your agent runs, such as new code, a new container image, or a configuration update. Only runtime-affecting changes create a new version. |

## How traffic flows

Every Foundry Agent Service request enters at the Foundry endpoint and exits to your customer resources through private endpoints. The agent type determines what happens in between.

### Inbound to the Foundry endpoint

Clients send HTTPS requests to your Foundry endpoint (for example, `<your-resource>.services.ai.azure.com`). The platform's API gateway authenticates the request and routes it based on the target agent type.

### Hosted agent path

For a Hosted agent, the platform forwards the request to a Micro VM in your delegated subnet over the `/invoke` protocol. The Micro VM has two network interfaces:

| Traffic type | Route |
|------|-------|
| Agent's own outbound traffic | Direct, through the Micro VM's dedicated NIC in the delegated subnet. |
| Tool server calls | Through the single-tenant data proxy, regardless of agent type. |

Even though the Micro VM has its own NIC, any tool invocation is routed through the data proxy.

### Prompt agent path

For a prompt agent, the agent runs in Microsoft-managed compute. The Foundry endpoint forwards the request directly to the Tools Service, which calls the single-tenant data proxy. IPs are allocated at the project level, so all prompt agents within a project share the same data proxy infrastructure.

### Egress to customer resources

Outbound traffic from the data proxy reaches your storage accounts, databases, and Key Vault through private endpoints in your private endpoint subnet. Configure the corresponding Private DNS zones (for example, `privatelink.blob.core.windows.net`, `privatelink.database.windows.net`, and `privatelink.vaultcore.azure.net`) so name resolution stays inside the VNet.

## Subnet sizing and IP allocation

Subnet configuration applies at the **Foundry account level**. All projects in the account share the same subnet configuration, and hosted and prompt agents share the same delegated subnet. The recommended size has to cover combined IP usage from agents across every project, platform upgrades, and scaling events.

### Recommended subnet size

Use a **/24 CIDR** range as the starting point for production workloads, and choose a larger range when your expected peak concurrency requires it. Don't use a /27 subnet for production workloads. Although /27 can support small development or evaluation deployments, it leaves very little headroom. Platform upgrades, rollouts, and scaling events all need temporary extra IPs, and a small subnet can become exhausted during these operations.

Plan subnet capacity in this order:

1. Estimate peak concurrent hosted agent sessions across all projects in the account for the region. Projects in the account share subnet capacity. All Foundry accounts and projects in the subscription and region share the session quota separately.
1. Check the region's default concurrent session quota in [Default service limits](limits-quotas-regions.md#default-service-limits).
1. Size the subnet so usable IPs meet or exceed the target by using the table in [Subnet size and concurrent sessions](#subnet-size-and-concurrent-sessions). Keep the planned peak below 80% of usable IPs to absorb upgrade and scaling spikes.
1. If the target exceeds the regional default, [request a limit increase](limits-quotas-regions.md#request-a-limit-increase). Specify the subscription, region, and expected concurrency. Increases depend on regional capacity.
1. If you need more sessions than the subnet's usable IPs allow and the subnet can't grow, request an increase to the IP-to-session mapping in the same support request.

### Supported IP ranges

Your subnet must use **RFC 1918 private IPv4 ranges** only:

- `10.0.0.0/8`
- `172.16.0.0/12` (covers `172.16.x.x` through `172.31.x.x`)
- `192.168.0.0/16`

Public IP ranges and CGNAT ranges (for example, `100.64.0.0/10`) aren't supported and cause routing failures.

### How IPs are consumed

IP addresses from the delegated subnet support hosted agent sessions and project-level networking components. Actual consumption changes with concurrent sessions, project count, scaling, and platform maintenance. Size the subnet for your expected peak concurrent sessions and keep enough unused addresses for temporary capacity needs. Plan capacity by sessions and usable subnet IPs, not by infrastructure units such as pods.

### Subnet size and concurrent sessions

The number of concurrent agent sessions available per subscription varies by region. By default, concurrent sessions and usable subnet IPs map **1:1**, subject to the limit for your region.

| Subnet | Total IPs | Usable IPs | Approximate concurrent sessions |
|--------|-----------|------------|---------------------------------|
| /27    | 32        | ~27        | ~20                             |
| /26    | 64        | ~59        | ~50                             |
| /25    | 128       | ~123       | ~100                            |
| /24    | 256       | ~251       | ~250                            |
| /23    | 512       | ~507       | ~500                            |
| /22    | 1,024     | ~1,019     | ~1,000                          |
| /21    | 2,048     | ~2,043     | ~2,000                          |

The table shows common subnet sizes and isn't exhaustive. You can use a larger supported subnet when it fits your private IP address plan. The extra addresses provide capacity and operational headroom but don't increase your per-subscription regional session quota.

The **Approximate concurrent sessions** column estimates capacity from usable subnet IPs under the default mapping. These values aren't production planning targets. Plan for lower concurrency so project-level networking components and the recommended 20% operational headroom also fit in the subnet. Your per-subscription regional session quota further limits actual concurrency. For example, in a region with a 1,000-session quota, a subnet larger than /22 adds IP headroom but doesn't increase concurrency unless you request a quota increase.

A session represents hosted-agent compute and persisted file state, not conversation history. Session capacity therefore doesn't determine how many conversations your application can maintain. With the Responses protocol, a conversation is associated with a session, while other invocation patterns can reuse a session without platform-managed conversation history. For details, see [Sessions versus conversations](../how-to/manage-hosted-sessions.md#sessions-versus-conversations).

To support more concurrent sessions within the same subnet, create an Azure support request. In the request, specify the subscription, region, and expected number of concurrent sessions. Based on your requirements and regional capacity, support can increase the mapping to **10 concurrent sessions per usable IP (1:10)**. For the default concurrent session quota available per region, see [Foundry Agent Service quotas](limits-quotas-regions.md#default-service-limits).

### Project capacity

A Foundry instance supports approximately **250 projects** at low traffic. Under heavy traffic, when agents run many concurrent sessions, the effective limit can drop to as few as **~25 projects**. When IPs are exhausted, new project provisioning fails.

> [!IMPORTANT]
> Don't plan to run at theoretical maximum capacity. Target a maximum of **80% subnet utilization** to absorb spikes from upgrades and scaling.

### Behavior during platform maintenance

Platform upgrades run old and new infrastructure in parallel, which temporarily increases IP consumption. A /24 subnet provides enough buffer to handle these temporary spikes alongside your normal workloads. Infrastructure upgrades are fully Microsoft-managed, including their timing.

### Outbound connectivity

Hosted agents run in microVMs attached to your delegated subnet and use that for outbound communication. Tool calls always route through the single-tenant data proxy. For source-code agent deployments, the provisioning step also requires outbound access to specific endpoints. See [Firewall requirements for private virtual networks](../how-to/deploy-hosted-agent-code.md#firewall-requirements-for-private-virtual-networks).

### Performance and scaling

Hosted agents support custom CPU and memory configurations. You select from available CPU and memory pairs when you create an agent version. Starting or resuming a session can require compute provisioning. If the subnet doesn't have enough available IP addresses, the platform can't provision compute for additional sessions.

## Prompt agents networking behavior

Prompt agents also run on Azure Container Apps, but compute and scaling are fully managed by Microsoft. You don't configure CPU or memory.

### Versions and IP usage

Unlike hosted agent sessions, prompt agent versions don't consume IPs. Project-level networking components still consume addresses from the delegated subnet.

### Outbound connectivity

Prompt agents use the single-tenant data proxy for all outbound connectivity. IPs are allocated at the **project level**, so all prompt agents within a project share the same data proxy infrastructure.

### Limits and performance

There's no hard limit on the number of prompt agents you can deploy per Foundry instance. Because compute and scaling are fully managed, there are no expected latency or performance issues tied to the number of prompt agents deployed.

## VNet peering and IP overlap

Overlapping IP ranges cause routing failures, so all peered VNets must use **unique, non-overlapping IP ranges**. This rule applies to bidirectional peering configurations as well. Only RFC 1918 private IPv4 ranges are supported. CGNAT addresses (for example, `100.x.x.x`) aren't.

If you can't avoid IP overlap, use [Managed virtual network](../../how-to/managed-virtual-network.md) instead of bring-your-own VNet. Managed VNet automates the network setup and eliminates IP overlap concerns.

## Monitor IP usage and detect exhaustion

The Azure portal doesn't currently expose IP utilization for delegated subnets, so you can't monitor it directly. The primary indicators of IP exhaustion are **HTTP 5xx errors from the data proxy** and, for hosted agents, **HTTP 429 `subnet_exhausted` errors during session creation or resume**. When IPs are exhausted, data proxy scaling and new project provisioning fail, and hosted agents can't allocate compute for new or resumed sessions. Monitor data proxy health and hosted agent session success as leading indicators of capacity issues.

Consider deploying a new Foundry instance with a fresh subnet when you observe:

- The data proxy returning 5xx errors.
- Hosted agent session creation or resume failing with HTTP 429 `subnet_exhausted` errors.
- New project provisioning failures.

> [!IMPORTANT]
> The platform doesn't proactively warn you when IP capacity is running low. Monitor the signals listed earlier to avoid unexpected provisioning failures.

## Quick reference

| Topic | Recommendation |
|-------|----------------|
| Subnet size | Use /24 or larger for production. /27 is the minimum but risky. With the default 1:1 mapping, subnet capacity ranges from approximately 20 concurrent sessions with /27 to 2,000 with /21. Size for less than 80% utilization, or request up to a 1:10 mapping (one IP address for 10 sessions) through Azure support. |
| Utilization target | Stay below 80% subnet utilization to absorb upgrade and scaling spikes. |
| Supported IP ranges | RFC 1918 only: `10.x`, `172.16` through `172.31.x`, and `192.168.x`. No public or CGNAT ranges. |
| Project capacity | ~250 projects at low traffic, as few as ~25 at full scale. Driven by IP availability. |
| IP consumption | Hosted agent sessions and project-level networking components consume IPs. Prompt agent versions don't. |
| Outbound connectivity | Hosted agent sessions use the delegated subnet. All tool calls route through the single-tenant data proxy. |
| Hosted compared to prompt | Hosted: custom CPU and memory and your ACR. Prompt: fully managed scaling. |
| VNet peering | Peered VNets must have non-overlapping IP ranges. Use Managed VNet if overlap exists. |
| Monitoring | No direct IP monitoring in the portal. Watch for data proxy 500 errors. |
| Performance | Starting or resuming a session can require compute provisioning. IP exhaustion prevents additional session compute from being provisioned. |

## Related content

- [Set up private networking for Foundry Agent Service](../how-to/virtual-networks.md)
- [Hosted agents in Foundry Agent Service](hosted-agents.md)
- [Managed virtual network](../../how-to/managed-virtual-network.md)
- [Configure private link](../../how-to/configure-private-link.md)
