---
title: "Troubleshoot Foundry agents (preview)"
description: "Find troubleshooting guides for Fabric IQ, connectors and managed MCP servers, routines, and Tool Search in Microsoft Foundry."
manager: nitinme
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.topic: troubleshooting
ms.date: 05/20/2026
author: zhuoqunli
ms.author: zhuoqunli
ms.custom:
  - dev-focus
  - doc-kit-assisted
ai-usage: ai-assisted
---

# Troubleshoot Foundry agents (preview)

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

Select the feature area to go to its dedicated troubleshooting guide.

| Feature | Troubleshooting guide |
|---|---|
| Fabric IQ — connection, authentication, OAuth consent, and data access | [Troubleshoot Fabric IQ connections](TSG%20-%20Fabric%20IQ.md) |
| Connectors and managed MCP servers — OAuth flows, RBAC, tool invocation | [Troubleshoot connectors and managed MCP servers](TSG%20-%20Connectors.md) |
| Routines — trigger failures, run errors, scheduling, and monitoring | [Troubleshoot routines](TSG%20-%20Routines.md) |
| Tool Search — toolbox configuration, MCP sessions, tool selection | [Troubleshoot Tool Search](TSG%20-%20Tool%20Search.md) |

## General RBAC reference

Most agent authorization failures trace back to one of the following role assignments. For feature-specific RBAC details, see the individual guides above.

| Error | Required role | Scope |
|---|---|---|
| `Principal does not have access to API/Operation` | **Azure AI User** (or **Foundry User**) | Project scope: `.../accounts/{account}/projects/{project}` |
| `lacks required data action '...agents/write'` | **Azure AI User** | Account scope: `.../accounts/{account}` |
| `403 Forbidden` on Fabric IQ or Work IQ calls | **Foundry User** | Project scope |
| OAuth consent errors | Admin consent required | Tenant-wide (Global Administrator action) |

> [!TIP]
> Granting a role only at the account scope is not sufficient for Foundry project-level checks. Always grant the **Azure AI User** or **Foundry User** role at **both** account scope and project scope for agent runtime identities.

For full role assignment steps, see [Azure role-based access control in Foundry](../../concepts/rbac-foundry.md).

## Related content

- [Connect agents to Microsoft Fabric with Fabric IQ](tools/fabric-iq.md)
- [Add managed MCP servers powered by connector namespaces](tools/connectors.md)
- [Automate agents with routines](use-routines.md)
- [Curate intent-based toolbox in Foundry](tools/toolbox.md)
- [Azure role-based access control in Foundry](../../concepts/rbac-foundry.md)
- [Agent identity](../concepts/agent-identity.md)
