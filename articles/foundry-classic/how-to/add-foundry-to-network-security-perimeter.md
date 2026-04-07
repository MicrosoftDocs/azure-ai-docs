---
title: "Add Microsoft Foundry to a network security perimeter (classic)"
description: "Quickly learn how to associate a Microsoft Foundry resource with a network security perimeter and where to find detailed guidance for access rules, logging, and management. (classic)"
author: jonburchel
ms.author: jburchel
ms.reviewer: meerakurup
ms.date: 02/23/2026
ms.topic: how-to
ms.service: azure-ai-foundry
ms.custom:
  - dev-focus
  - classic-and-new
ai-usage: ai-assisted
ROBOTS: NOINDEX, NOFOLLOW
---

# Add Microsoft Foundry to a network security perimeter (classic)

**Currently viewing:** :::image type="icon" source="../../foundry/media/yes-icon.svg" border="false"::: **Foundry (classic) portal version** - [Switch to version for the new Foundry portal](../../foundry/how-to/add-foundry-to-network-security-perimeter.md)

Use a network security perimeter (NSP) to restrict data-plane access to your Microsoft Foundry resource and group it with other protected PaaS resources. An NSP lets you:

- Enforce inbound and outbound access rules instead of broad public exposure.
- Reduce data exfiltration risk by containing traffic within a logical boundary.
- Centrally log network access decisions across associated resources.

This article gives only the Foundry-specific pointers you need. All procedural detail for creating perimeters, defining access rules, enabling logging, and using APIs lives in existing Azure networking documentation. Follow the links in each section for the authoritative steps.

> [!IMPORTANT]
> Network security perimeter support for Microsoft Foundry is in public preview under [supplemental terms of use](https://azure.microsoft.com/support/legal/preview-supplemental-terms/). Review the [limitations and considerations](#review-limitations-and-considerations) before you start.

[!INCLUDE [uses-fdp-only](../includes/uses-fdp-only.md)]
:::image type="content" source="../../foundry/media/how-to/network/network-security-perimeter-diagram.png" alt-text="Diagram that shows a Foundry resource inside a network security perimeter boundary, with inbound rules filtering external traffic and outbound rules controlling egress to external services." lightbox="../../foundry/media/how-to/network/network-security-perimeter-diagram.png":::

The diagram shows a Foundry resource inside an NSP boundary. Inbound access rules filter traffic from external sources, and outbound access rules control egress to services outside the perimeter.

[!INCLUDE [add-foundry-to-network-security-perimeter 1](../../foundry/includes/how-to-add-foundry-to-network-security-perimeter-1.md)]

## Validate before enforcement

1. Stay in Learning mode initially; review access logs for denies affecting required traffic.
1. Add or refine inbound and outbound rules.
1. Switch to Enforced mode.
1. Open [Foundry](https://ai.azure.com/?cid=learnDocs) and perform a model deployment or chat test. Success indicates required traffic is permitted.
1. If blocked, revert to Learning mode or add rules and retry.

[!INCLUDE [add-foundry-to-network-security-perimeter 2](../../foundry/includes/how-to-add-foundry-to-network-security-perimeter-2.md)]
