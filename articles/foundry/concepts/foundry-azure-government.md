---
title: "Microsoft Foundry in Azure Government"
titleSuffix: Microsoft Foundry
description: "Feature availability, regions, and endpoints for the Microsoft Foundry portal and platform in Azure Government (USGov Virginia and USGov Arizona)."
author: jvenezia
ms.author: jvenezia
ms.service: microsoft-foundry
ms.subservice: foundry-platform
ms.topic: concept-article
ms.date: 06/05/2026
ai-usage: ai-assisted
ms.custom:
  - references_regions
  - classic-and-new
keywords:
  - Microsoft Foundry
  - Azure Government
  - USGov Virginia
  - USGov Arizona
  - sovereign cloud
---

# Microsoft Foundry in Azure Government

Microsoft Foundry is available in Azure Government for US federal, state, and local governments and their partners. Use this article to find the supported regions, endpoints, and platform features in Azure Government. For agent-specific feature availability, see [Foundry Agent Service feature availability in Azure Government](../agents/concepts/azure-government.md).

## Supported regions

Microsoft Foundry is deployed in the following Azure Government regions:

| Region | Region identifier |
| --- | --- |
| US Gov Virginia | `usgovvirginia` |
| US Gov Arizona | `usgovarizona` |

Capabilities can differ by region. See the feature tables in this article and in [Foundry Agent Service feature availability in Azure Government](../agents/concepts/azure-government.md) for specifics.

## Endpoints

Use the following endpoints to access the Foundry portal, your project, and the Azure portal in Azure Government.

### Foundry portal

```text
https://ai.azure.us/nextgen
```

### Foundry project endpoint

Replace `{resource-name}` and `{project-name}` with your values:

```text
https://{resource-name}.services.ai.azure.us/api/projects/{project-name}
```

### Azure portal

```text
https://portal.azure.us
```

## Models

For the list of Foundry Models sold directly by Azure that are available in Azure Government, see [Foundry Models sold by Azure in Azure Government](../foundry-models/concepts/models-sold-directly-by-azure-gov.md).

## Azure OpenAI features

| Feature | Available |
| --- | --- |
| Responses API | Yes |
| Model router | No |

## Enterprise and security features

| Feature | Available |
| --- | --- |
| Agent identity (Microsoft Entra) | Yes |
| Private networking (VNet integration) | Yes |
| Role-based access control (RBAC) | Yes |
| Network Security Perimeter (NSP) | Yes |
| Content safety and guardrails | Yes |

For more information on adding Foundry to a Network Security Perimeter, see [Add Microsoft Foundry to a network security perimeter](../how-to/add-foundry-to-network-security-perimeter.md).

## Guardrails

| Guardrail | Available |
| --- | --- |
| Block lists | Yes |
| Jailbreak detection | Yes |
| Content Safety | Yes |
| Protected materials detection | Yes |

## Observability

| Capability | Available |
| --- | --- |
| Tracing (prompt agents) | Yes |
| Evaluations | No |
| Optimization | No |

## Foundry Agent Service

Foundry Agent Service is available in Azure Government with a subset of agent types and tools. For the full list of supported agent types, tools, and publishing options, see [Foundry Agent Service feature availability in Azure Government](../agents/concepts/azure-government.md).

## Quotas and limits

For quotas and limits that apply to Azure OpenAI models in Azure Government, see [Azure OpenAI quotas and limits in Azure Government](../openai/quotas-limits-gov.md).

## Related content

For more information on Microsoft Foundry in Azure Government, see:

- [Foundry Agent Service feature availability in Azure Government](../agents/concepts/azure-government.md) — Agent types, tools, and publishing options
- [Foundry Models sold by Azure in Azure Government](../foundry-models/concepts/models-sold-directly-by-azure-gov.md) — Available models in Azure Government
- [Azure OpenAI quotas and limits in Azure Government](../openai/quotas-limits-gov.md) — Service quotas
- [Add Microsoft Foundry to a network security perimeter](../how-to/add-foundry-to-network-security-perimeter.md) — NSP integration
- [Azure Government documentation](/azure/azure-government/documentation-government-welcome) — Compliance certifications and onboarding
