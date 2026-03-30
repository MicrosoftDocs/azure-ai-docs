---
title: "Known issues - Microsoft Foundry"
description: "Find known issues, workarounds, and solutions for Microsoft Foundry, including Speech, Translator, and portal services. Review before submitting a support request."
ai-usage: ai-assisted
ms.service: azure-ai-foundry
ms.topic: troubleshooting-known-issue
ms.date: 02/19/2026
author: s-polly
ms.author: scottpolly
ms.reviewer: bgilmore
ms.custom:
  - classic-and-new
  - doc-kit-assisted
---

# Known issues - Microsoft Foundry

[!INCLUDE [foundry-known-issues 1](../includes/reference-foundry-known-issues-1.md)]

## General Foundry known issues

| Issue ID | Category | Title | Description | Workaround | Issue publish date |
|--------|--------|----|-----------|----------|-------------------|
| 0001   | Foundry portal | Network isolation in new Foundry  | The new Foundry portal experience doesn't support end-to-end network isolation. | When you configure network isolation (disable public network access, enable private endpoints, and use virtual network-injected Agents), you must use the classic Foundry portal experience, the SDK, or CLI to securely access your Foundry projects.  | December 5, 2025 |
| 0002   | Foundry portal | Multiple projects per Foundry resource  | The new Foundry portal experience doesn't support multiple projects per Foundry resource. Each Foundry resource supports only one default project. | None  | December 5, 2025 |

[!INCLUDE [foundry-known-issues 2](../includes/reference-foundry-known-issues-2.md)]
