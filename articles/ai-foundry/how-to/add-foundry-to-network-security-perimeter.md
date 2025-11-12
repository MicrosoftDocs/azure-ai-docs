---
title: Add Microsoft Foundry to a network security perimeter
description: Quickly learn how to associate a Microsoft Foundry resource with a network security perimeter and where to find detailed guidance for access rules, logging, and management.
monikerRange: 'foundry-classic || foundry'
author: jonburchel
ms.author: jburchel
ms.reviewer: meerakurup
ms.date: 09/29/2025
ms.topic: concept-article
ms.service: azure-ai-foundry
ai-usage: ai-assisted
---

# Add Microsoft Foundry to a network security perimeter (preview)

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

Use a network security perimeter (NSP) to restrict data‑plane access to your Microsoft Foundry resource and group it with other protected PaaS resources. An NSP lets you:

- Enforce inbound and outbound access rules instead of broad public exposure.
- Reduce data exfiltration risk by containing traffic within a logical boundary.
- Centrally log network access decisions across associated resources.

This article gives only the Foundry-specific pointers you need. All procedural detail for creating perimeters, defining access rules, enabling logging, and using APIs lives in existing Azure networking documentation. Follow the links in each section for the authoritative steps.

[!INCLUDE [uses-fdp-only](../includes/uses-fdp-only.md)]

:::image type="content" source="../media/how-to/network/network-security-perimeter-diagram.png" alt-text="Diagram of the NSP for Foundry." lightbox="../media/how-to/network/network-security-perimeter-diagram.png":::

## Limitations and considerations

- Some Foundry capabilities (for example fine-tuning and Assistants APIs) may be unavailable inside an enforced NSP boundary. 
- NSP governs data plane traffic. Control plane (management) operations may still succeed unless separately restricted.
- Use a managed identity (system or user‑assigned) with appropriate role assignments for any data source access (for example Azure Blob Storage used for batch inputs/outputs).
- Co-locate dependent services (Azure OpenAI, Azure Storage, Azure AI Search, etc.) in the same NSP when you need mutual access with minimal outbound allow rules.
- Foundry Agent Service: Supported; Secured Standard Agents with full network isolation rely on Private Link and do not require or support NSP.
- Private Link takes precedence over NSP evaluation when both are configured; traffic resolves through Private Link first.

For more information, see [Network security perimeter concepts](/azure/private-link/network-security-perimeter-concepts).

## Prerequisites

Create an existing Foundry resource (or plan to create one) and required managed identity assignments.

If any prerequisite behavior is unclear or changes, consult the latest Azure OpenAI + NSP article for parity details in [Azure OpenAI NSP guidance](/azure/ai-foundry/openai/how-to/network-security-perimeter).

## Associate your Foundry resource

Portal (summary):
1. Open the Azure portal and navigate to your Network security perimeter resource.
2. Select **Associated resources** (or **Resources** depending on UI iteration) > **Add / Associate**.
3. Choose the target profile, pick your Foundry resource, set access mode (start with Learning), and confirm.

CLI (for automation) and full creation steps: see the NSP quickstarts (CLI or PowerShell):
- [Create a network security perimeter (CLI)](/azure/private-link/create-network-security-perimeter-cli)
- [Create a network security perimeter (PowerShell)](/azure/private-link/create-network-security-perimeter-powershell)

After association, traffic evaluation begins per the selected access mode.


## Access modes (Learning vs Enforced)

Start in Learning to observe would‑be denies. Switch to Enforced once required inbound/outbound rules are defined. Reference [NSP access modes](/azure/private-link/network-security-perimeter-concepts#access-modes) for more details.

## Interaction with `publicNetworkAccess`

- Learning mode: `publicNetworkAccess` still governs exposure while you assess logs.
- Enforced mode: NSP rules take precedence; `publicNetworkAccess` is effectively overridden by allowed inbound rules.

## Change access mode

In the portal, locate the association entry for your Foundry resource and choose **Change access mode**. Use automation via `az network perimeter association update` (see Azure CLI reference) when scripting.

## Enable logging

Configure diagnostic settings on the NSP resource to send `allLogs` to Log Analytics, Storage, or Event Hubs. For detailed steps and more information about rule context, refer [Enable NSP logging](/azure/azure-monitor/fundamentals/network-security-perimeter#add-a-network-security-perimeter-inbound-access-rule).

## Interpret logs

Query the `network-security-perimeterAccessLogs` table in your Log Analytics workspace to validate allow/deny decisions and finalize required sources or destinations before enforcing. Use KQL filters on `MatchedRule` or `Profile` to isolate Foundry traffic.


## Define access rules

Within the profile, choose:
- Inbound rules: IP ranges or subscription (managed identity) sources.
- Outbound rules: FQDN destinations needed beyond co-located perimeter resources.

Rule creation steps (portal screenshots, CLI parameters, examples):
- [A walkthrough of configuring inbound and outbound rules](/azure/ai-foundry/openai/how-to/network-security-perimeter#add-an-access-rule-for-your-azure-openai-service) using Azure OpenAI NSP (which applies to Foundry data‑plane scenarios).
- Azure CLI reference (access rules): [az network perimeter profile access-rule](/cli/azure/network/perimeter/profile/access-rule?view=azure-cli-latest&preserve-view=true)

Implicit trust: Resources inside the same NSP can reach each other when requests are authenticated via managed identity or role assignment; explicit rules are needed only for external sources/destinations or API key patterns.

### Inbound rules

Choose IP range (CIDR) or subscription scope. Prefer subscription + managed identity for internal service‑to‑service traffic; fall back to IP range only when identity‑based access isn't feasible.

### Outbound rules

List only required FQDNs (principle of least privilege). Keep dependent Azure services in the same NSP to minimize outbound allow entries.

## Validate before enforcement

::: moniker range="foundry-classic"

1. Stay in Learning mode initially; review access logs for denies affecting required traffic.
2. Add or refine inbound/outbound rules.
3. Switch to Enforced mode.
4. Open [Foundry](https://ai.azure.com/?cid=learnDocs) and perform a model deployment or chat test. Success indicates required traffic is permitted.
5. If blocked, revert to Learning or add rules and retry.

::: moniker-end

::: moniker range="foundry"

1. Stay in Learning mode initially; review access logs for denies affecting required traffic.
2. Add or refine inbound/outbound rules.
3. Switch to Enforced mode.
4. Open [!INCLUDE [foundry-link](../default/includes/foundry-link.md)] and perform a model deployment or chat test. Success indicates required traffic is permitted.
5. If blocked, revert to Learning or add rules and retry.

::: moniker-end

## View and manage configuration

Use REST or CLI to audit and reconcile:
- REST reference (perimeter core): [Network security perimeter REST API](/rest/api/network-security-perimeter/)
- (Example) Profile and association operations (CLI): [Azure CLI network perimeter commands](/cli/azure/network/perimeter?view=azure-cli-latest&preserve-view=true)
- Configuration reconciliation APIs for perimeter profiles and associations. Use the latest published preview or stable version. Use the correct preview version for configuration APIs, currently `2024-10-01`.

Always confirm the latest API version in the reference before scripting.


## Related content

- [Role-based access control for Foundry](../concepts/rbac-azure-ai-foundry.md)
- [Network security perimeter concepts](/azure/private-link/network-security-perimeter-concepts)
- [Azure OpenAI NSP article](/azure/ai-foundry/openai/how-to/network-security-perimeter)
- [Azure CLI network perimeter reference](/cli/azure/network/perimeter?view=azure-cli-latest&preserve-view=true)
- [What is Foundry Agent Service?](../agents/overview.md)
