---
title: "Set up an Azure Key Vault Connection"
description: "Learn how to securely connect your Azure Key Vault to Foundry. Follow step-by-step instructions to manage secrets and ensure seamless integration."
author: jonburchel
ms.author: jburchel
ms.reviewer: andyaviles
ms.date: 02/24/2026
ms.topic: how-to
ms.service: azure-ai-foundry
ms.custom:
  - dev-focus
  - classic-and-new
  - doc-kit-assisted
ai-usage: ai-assisted
# zone_pivot_groups: set-up-key-vault
---

# Set up an Azure Key Vault connection in Microsoft Foundry

[!INCLUDE [set-up-key-vault-connection 1](../includes/how-to-set-up-key-vault-connection-1.md)]

## Limitations

Create Azure Key Vault connections only when you need them.

If you bring your own Azure Key Vault, review these limitations:

- Limit Azure Key Vault connections to one per Foundry resource. Delete an Azure Key Vault connection only if no other connections exist at the Foundry resource or project level.

- Foundry doesn't support secret migration. Remove and recreate connections yourself.
- Deleting the underlying Azure Key Vault breaks the Foundry resource. Azure Key Vault stores secrets for connections that don't use Microsoft Entra ID. Any Foundry feature that depends on those connections stops working.
- Deleting connection secrets that your Foundry resource stores in your bring your own (BYO) Azure Key Vault can break connections to other services.

[!INCLUDE [set-up-key-vault-connection 2](../includes/how-to-set-up-key-vault-connection-2.md)]
