---
title: Disable creation of classic agents and assistants
description: Learn how to disable and re-enable creating classic agents and assistants on an Azure OpenAI account by setting a resource tag.
author: aahill
ms.author: aahi
ms.date: 05/27/2026
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.topic: how-to
ms.custom: doc-kit-assisted
ai-usage: ai-assisted
#Customer Intent: As an admin, I want to disable creating classic agents and assistants on an Azure OpenAI account so that I can enforce migration to the new Foundry Agent Service.
---

# Disable creation of classic agents and assistants

You can disable creating or updating classic agents and assistants on an Azure OpenAI account by setting the `MS-AOAI-Feature-Assistants` resource tag to `Disabled`. This tag blocks Assistants API and classic agent operations on the account while leaving other Azure OpenAI capabilities (completions, embeddings, and image generation) unchanged.

## Prerequisites

- The [Azure CLI](/cli/azure/install-azure-cli) installed.
- You're signed in to Azure with `az login`.
- **Owner**, **Contributor**, or **Tag Contributor** access on the target subscription or resource group. Tag Contributor is the least-privilege option for tag-only operations.

## Disable assistants and classic agents

To disable creation, set the `MS-AOAI-Feature-Assistants` tag to `Disabled` on the Azure OpenAI account.

Replace `<sub>` with your subscription ID, `<rg>` with your resource group name, and `<account>` with your Azure OpenAI account name. You can find these values in the Azure portal or by running `az resource list --resource-type Microsoft.CognitiveServices/accounts --output table`.

# [Azure CLI](#tab/cli)

```bash
az resource tag \
    --is-incremental \
    --tags MS-AOAI-Feature-Assistants=Disabled \
    --ids /subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.CognitiveServices/accounts/<account>
```

> [!IMPORTANT]
> Always include `--is-incremental` (or `-i`) so the command adds the tag without replacing existing tags on the resource.

# [Bicep](#tab/bicep)

```bicep
resource aoai 'Microsoft.CognitiveServices/accounts@2025-04-01-preview' = {
  name: '<account>'
  location: '<location>'
  kind: 'OpenAI'
  sku: {
    name: 'S0'
  }
  tags: {
    'MS-AOAI-Feature-Assistants': 'Disabled'
  }
  properties: {
    // Include your existing account properties here
  }
}
```

---

## Verify the tag

After you set the tag, confirm it was applied:

```bash
az resource show \
    --ids /subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.CognitiveServices/accounts/<account> \
    --query tags
```

The output should include `"MS-AOAI-Feature-Assistants": "Disabled"`.

## Re-enable assistants and classic agents

To re-enable creation, set the same tag to `Enabled`.

# [Azure CLI](#tab/cli)

```bash
az resource tag \
    --is-incremental \
    --tags MS-AOAI-Feature-Assistants=Enabled \
    --ids /subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.CognitiveServices/accounts/<account>
```

# [Bicep](#tab/bicep)

```bicep
resource aoai 'Microsoft.CognitiveServices/accounts@2025-04-01-preview' = {
  name: '<account>'
  location: '<location>'
  kind: 'OpenAI'
  sku: {
    name: 'S0'
  }
  tags: {
    'MS-AOAI-Feature-Assistants': 'Enabled'
  }
  properties: {
    // Include your existing account properties here
  }
}
```

---

## What gets disabled

When the tag is set to `Disabled`, the following Assistants API and classic agent operations are blocked on the account:

| Blocked operation | API surface |
|---|---|
| Create assistant | Assistants API |
| Update assistant | Assistants API |
| Create agent | Classic agents |
| Update agent | Classic agents |
| Create thread | Assistants API |
| Create run | Assistants API |
| Create thread and run | Assistants API |
| Create assistant file | Assistants API |

Existing assistants, threads, and files remain in place, but they can't be modified and no new ones can be created until the tag is set back to `Enabled`.

> [!NOTE]
> This tag doesn't affect the new Foundry Agent Service. To build agents with the latest capabilities, [migrate to the new agent service](migrate.md).

## Troubleshooting

| Symptom | Resolution |
|---|---|
| Tag applied, but assistants can still be created | Verify the tag value is exactly `Disabled` (case-sensitive) by running the verification command above. |
| Permission denied when setting the tag | Confirm you have **Owner**, **Contributor**, or **Tag Contributor** access on the resource. |
| Other tags disappeared after running the command | You ran `az resource tag` without `--is-incremental`. Re-apply the missing tags and include the `-i` flag in future commands. |

## Related content

- [Migrate to the new Foundry Agent Service](migrate.md)
- [Tag resources with the Azure CLI](/azure/azure-resource-manager/management/tag-resources-cli)
- [Migrate from Agent Applications to the new agent model](migrate-agent-applications.md)
