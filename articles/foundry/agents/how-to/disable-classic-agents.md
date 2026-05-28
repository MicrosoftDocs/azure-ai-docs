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

You can disable creating or updating classic agents and assistants on an Azure OpenAI account by setting the `MS-AOAI-Feature-Assistants` tag to `Disabled`. This tag opts the account out of the Assistants API surface while leaving other model and inference features unchanged.

## Prerequisites

* The [Azure CLI](/cli/azure/install-azure-cli) installed.
* You're signed in to Azure with `az login`.
* **Owner** or **Contributor** access on the target subscription or resource group.

## Disable assistants and classic agents

To disable creation, set the `MS-AOAI-Feature-Assistants` tag to `Disabled` on the Azure OpenAI account.

# [Azure CLI](#tab/cli)

```bash
# CLI — single account
az resource tag --tags MS-AOAI-Feature-Assistants=Disabled \
    --ids /subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.CognitiveServices/accounts/<account>
```

# [Bicep](#tab/bicep)

```bicep
// Bicep — single account
resource aoai 'Microsoft.CognitiveServices/accounts@2024-10-01' = {
  name: 'my-foundry-account'
  // ...
  tags: {
    'MS-AOAI-Feature-Assistants': 'Disabled'
  }
}
```

---

## Re-enable assistants and classic agents

To re-enable creation, set the same tag to `Enabled`.

# [Azure CLI](#tab/cli)

```bash
# CLI — single account
az resource tag --tags MS-AOAI-Feature-Assistants=Enabled \
    --ids /subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.CognitiveServices/accounts/<account>
```

# [Bicep](#tab/bicep)

```bicep
// Bicep — single account
resource aoai 'Microsoft.CognitiveServices/accounts@2024-10-01' = {
  name: 'my-foundry-account'
  // ...
  tags: {
    'MS-AOAI-Feature-Assistants': 'Enabled'
  }
}
```

---

## What gets disabled

When the tag is set to `Disabled`, the following Assistants API operations are blocked on the account:

* Create assistant
* Update assistant
* Create agent
* Update agent
* Create thread
* Create run
* Create thread and run
* Create assistant file

Existing assistants, threads, and files remain in place, but they can't be modified and no new ones can be created until the tag is set back to `Enabled`.

## Related content

* [Migrate to the new Foundry Agent Service](/azure/foundry/agents/how-to/migrate)
