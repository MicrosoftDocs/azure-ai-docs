---
title: Include file
description: Include file
author: jonburchel
ms.reviewer: meerakurup
ms.author: jburchel
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 03/20/2026
ms.custom: include
---

## Troubleshooting

- If the portal experience doesn't show your Foundry resource as associable, confirm that Foundry is supported for NSP association in your region and review the supported resource types: [Network security perimeter concepts](/azure/private-link/network-security-perimeter-concepts).
- If you don't see logs after enabling diagnostics, confirm that you selected `allLogs` and that your destination is supported: [Diagnostic logs for Network Security Perimeter](/azure/private-link/network-security-perimeter-diagnostic-logs).
- If Learning mode looks correct but Enforced mode blocks access, return to Learning mode and add the minimum inbound and outbound rules needed for your scenario: [Azure OpenAI NSP guidance](/azure/ai-foundry/openai/how-to/network-security-perimeter).
- If your managed identity can't reach co-located resources, verify that both resources are in the same NSP and that role assignments are correct.
- If logs don't appear immediately after you enable diagnostics, allow up to 15 minutes for diagnostic data to propagate to your Log Analytics workspace.

## Review limitations and considerations

- NSP governs data-plane traffic. Control-plane (management) operations might still succeed unless separately restricted.
- Use a managed identity (system or user-assigned) with appropriate role assignments for any data source access (for example Azure Blob Storage used for batch inputs/outputs).
- Co-locate dependent services (Azure OpenAI, Azure Storage, Azure AI Search, and so on) in the same NSP when you need mutual access with minimal outbound allow rules.

For more information, see [Network security perimeter concepts](/azure/private-link/network-security-perimeter-concepts).

## View and manage your configuration

Use REST or CLI to audit and reconcile:
- REST reference (perimeter core): [Network security perimeter REST API](/rest/api/network-security-perimeter/)
- (Example) Profile and association operations (CLI): [Azure CLI network perimeter commands](/cli/azure/network/perimeter?view=azure-cli-latest)

Use API version `2024-10-01` or the latest version shown in the REST reference when scripting. Always confirm the current API version in the reference before scripting.

## Related content

- [Role-based access control for Foundry](../concepts/rbac-foundry.md)
- [Network security perimeter concepts](/azure/private-link/network-security-perimeter-concepts)
- [Azure OpenAI NSP article](/azure/ai-foundry/openai/how-to/network-security-perimeter)
- [Azure CLI network perimeter reference](/cli/azure/network/perimeter?view=azure-cli-latest)
- [What is Foundry Agent Service?](../agents/overview.md)
