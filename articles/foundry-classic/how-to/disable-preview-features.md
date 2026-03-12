---
title: "Hide preview features with Azure tags in Foundry portals (classic)"
description: "Learn how to hide preview features in Microsoft Foundry portals by applying an Azure tag at the correct scope, and understand behavior across classic and new experiences. (classic)"
author: sdgilley
ms.author: sgilley
ms.reviewer: shwinne
ms.date: 02/24/2026
ms.topic: how-to
ms.service: azure-ai-foundry
ms.custom:
  - dev-focus
  - classic-and-new
#customer intent: As an admin, I want to hide preview features in Foundry portals by using Azure tags so that teams use generally available capabilities in production environments.
ai-usage: ai-assisted
ROBOTS: NOINDEX, NOFOLLOW
---

# Hide preview features with Azure tags (classic)

[!INCLUDE [classic-banner](../includes/classic-banner.md)]

Hide preview features in both Foundry portal experiences (new and classic) by applying a tag at the appropriate scope in Azure portal. This approach helps teams focus on generally available capabilities in production environments.

This control is separate from role-based access control (RBAC). Use tags to hide preview portal surfaces, and use RBAC when you need to block specific operations or permissions. For RBAC guidance, see [Disable preview features in Microsoft Foundry](../../foundry/how-to/disable-preview-features.md#block-preview-features-with-custom-rbac-roles).

This article covers the suppression of preview features in Foundry portals. It doesn't define SDK or REST API enforcement behavior.

## Prerequisites

- A Foundry resource and project.
- Permission to add or edit tags at your target scope in Azure. For example, **Contributor** or **Tag Contributor**.
- Access to [Azure portal](https://portal.azure.com).

[!INCLUDE [disable-preview-tag-procedure](../../foundry/includes/disable-preview-tag-procedure.md)]

## Related content

- [Disable preview features in Microsoft Foundry](../../foundry/how-to/disable-preview-features.md)
- [Role-based access control for Microsoft Foundry](../concepts/rbac-foundry.md)
