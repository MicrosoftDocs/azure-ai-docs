---
title: "Hide preview features with Azure tags in Foundry portals (temp)"
description: "Learn how to hide preview features in Microsoft Foundry portals by applying an Azure tag at the correct scope, and understand behavior across classic and new experiences. (temp)"
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
---

# Hide preview features with Azure tags (temp)

Hide preview features in both Foundry portal experiences (new and classic) by applying a tag at the appropriate scope in Azure portal. This approach helps teams focus on generally available capabilities in production environments.

This control is separate from role-based access control (RBAC). Use tags to hide preview portal surfaces, and use RBAC when you need to block specific operations or permissions. For RBAC guidance, see [Disable preview features with role-based access control](../concepts/disable-preview-features-with-rbac.md).

This article covers the suppression of preview features in Foundry portals. It doesn't define SDK or REST API enforcement behavior.

## Prerequisites

- A Foundry resource and project.
- Permission to add or edit tags at your target scope in Azure. For example, **Contributor** or **Tag Contributor**.
- Access to [Azure portal](https://portal.azure.com).

## Apply the tag in Azure portal

Apply the preview-feature suppression tag at the scope your organization governs.

> [!IMPORTANT]
> Use the exact tag key and value:
> - Tag key: `AZML_DISABLE_PREVIEW_FEATURE`
> - Tag value: `true`

1. Sign in to [Azure portal](https://portal.azure.com).
1. Go to the scope where you want to suppress preview features.
   - Use subscription scope for organization-wide governance.
   - Use Foundry resource scope for granular control.

1. Select **Tags**.
1. Add the preview suppression tag key and value:
   - Key: `AZML_DISABLE_PREVIEW_FEATURE`
   - Value: `true`
1. Select **Apply**.
1. Repeat for other scopes, as needed.

:::image type="content" source="../media/disable-preview-features/disable-preview-tag.png" alt-text="Screenshot show disabling preview features in Azure portal for a Foundry resource.":::

## Verify suppression in both portal experiences

After the tag is saved, verify behavior in both experiences.

1. Open [Microsoft Foundry](https://ai.azure.com).
1. Open your tagged project.
1. Validate that preview-only UI features are hidden. 
    * In the classic portal, the Preview features tool in the upper-right is disabled.
    * In the new portal, you won't see any **PREVIEW** labels, as the features in preview will no longer be visible.  
1. Toggle between new and classic experiences by using **New Foundry**, and validate the same behavior.

Expected result: preview features are hidden in both new and classic Foundry portal experiences.

## Troubleshoot suppression issues

Use the following checks when suppression doesn't behave as expected.

1. Confirm the tag key and value are correct, then save again.
1. Confirm the tag is applied at the intended governance scope (subscription, resource group, or resource/project).
1. Refresh the Foundry portal and wait a few minutes for propagation.
1. Confirm your account can edit tags at that scope.
1. If preview UI still appears after you verify scope and tag values, sign out and back in to refresh your session.
1. If preview UI still appears in a tagged scope after these checks, file a support request as a potential product bug.

## Related content

- [Disable preview features with role-based access control](../concepts/disable-preview-features-with-rbac.md)
- [Role-based access control for Microsoft Foundry](../concepts/rbac-foundry.md)
