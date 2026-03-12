---
title: Include file
description: Include file
author: sdgilley
ms.reviewer: sgilley
ms.author: sgilley
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 03/11/2026
ms.custom: include
---

## Apply the tag in Azure portal

Apply the preview-feature suppression tag at the scope your organization governs.

> [!IMPORTANT]
> Use the exact tag key and value:
> - Tag key: `AZML_DISABLE_PREVIEW_FEATURE`
> - Tag value: `true`

1. Sign in to [Azure portal](https://portal.azure.com/?cid=learnDocs).
1. Go to the scope where you want to suppress preview features.
   - Use subscription scope for organization-wide governance.
   - Use resource group scope to cover all resources in a group.
   - Use Foundry resource scope for granular control.

1. Select **Tags**.
1. Add the preview suppression tag key and value:
   - Key: `AZML_DISABLE_PREVIEW_FEATURE`
   - Value: `true`
1. Select **Apply**.
1. Repeat for other scopes, as needed.

:::image type="content" source="../media/disable-preview-features/disable-preview-tag.png" alt-text="Screenshot of the Azure portal Tags pane showing the AZML_DISABLE_PREVIEW_FEATURE tag set to true on a Foundry resource.":::

### Apply the tag with Azure CLI

You can also apply the tag by using the Azure CLI. Replace `<resource-id>` with the full resource ID of your subscription, resource group, or Foundry resource.

```azurecli
az tag update --resource-id <resource-id> --operation merge --tags AZML_DISABLE_PREVIEW_FEATURE=true
```

To find the resource ID for a Foundry resource:

```azurecli
az resource show --name <resource-name> --resource-group <resource-group> --resource-type "Microsoft.CognitiveServices/accounts" --query id --output tsv
```

## Remove the tag to re-enable preview features

To restore preview features, remove the `AZML_DISABLE_PREVIEW_FEATURE` tag.

### Remove the tag in Azure portal

1. In the [Azure portal](https://portal.azure.com), go to the resource, resource group, or subscription where you applied the tag.
1. Select **Tags**.
1. Select the delete icon (trash can) next to the `AZML_DISABLE_PREVIEW_FEATURE` tag.
1. Select **Apply**.

### Remove the tag with Azure CLI

```azurecli
az tag update --resource-id <resource-id> --operation delete --tags AZML_DISABLE_PREVIEW_FEATURE=true
```

After you remove the tag, refresh the Foundry portal or sign out and back in. Preview features reappear within a few minutes.

## Verify suppression in both portal experiences

After the tag is saved, allow a few minutes for propagation and then verify behavior in both experiences.

1. Open [Microsoft Foundry](https://ai.azure.com).
1. Open your tagged project.
1. Validate that preview-only UI features are hidden.
    * In the classic portal, the Preview features tool in the upper-right is disabled.
    * In the new portal, you won't see any **PREVIEW** labels, as the features in preview will no longer be visible.
1. Toggle between new and classic experiences by using **New Foundry**, and validate the same behavior.

Expected result: preview features are hidden in both new and classic Foundry portal experiences.

## Troubleshoot suppression issues

Use the following table when suppression doesn't behave as expected.

| Symptom | Cause | Resolution |
| --- | --- | --- |
| Preview features still appear after applying the tag. | Tag key or value is incorrect. | Verify the tag key is exactly `AZML_DISABLE_PREVIEW_FEATURE` and the value is `true` (case-sensitive). Save the tag again. |
| Tag is applied but only some scopes are suppressed. | Tag is applied at a narrower scope than intended. | Confirm the tag is applied at the intended governance scope (subscription, resource group, or resource). Apply it at a broader scope if needed. |
| Preview features reappear after a few minutes. | Browser session is using a cached state. | Sign out and back in, or clear the browser cache and refresh the Foundry portal. |
| Unable to add or edit the tag. | Your account lacks tag permissions at that scope. | Verify that you have the **Contributor** or **Tag Contributor** role at the target scope. |
| Preview features still appear after verifying scope, tag, and permissions. | Possible propagation delay or product bug. | Wait a few minutes for propagation. If the issue persists, file a support request. |
