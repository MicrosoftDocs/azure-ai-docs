---
title: "Set up an Azure Key Vault Connection (classic)"
description: "Learn how to securely connect your Azure Key Vault to Foundry. Follow step-by-step instructions to manage secrets and ensure seamless integration. (classic)"
author: jonburchel
ms.author: jburchel
ms.reviewer: andyaviles
ms.date: 02/24/2026
ms.topic: how-to
ms.service: azure-ai-foundry
ms.custom:
  - dev-focus
  - classic-and-new
ai-usage: ai-assisted
# zone_pivot_groups: set-up-key-vault
ROBOTS: NOINDEX, NOFOLLOW
---

# Set up an Azure Key Vault connection in Microsoft Foundry (classic)

**Currently viewing:** :::image type="icon" source="../../foundry/media/yes-icon.svg" border="false"::: **Foundry (classic) portal version** - [Switch to version for the new Foundry portal](../../foundry/how-to/set-up-key-vault-connection.md)

[!INCLUDE [set-up-key-vault-connection 1](../../foundry/includes/how-to-set-up-key-vault-connection-1.md)]

## Limitations

Create Azure Key Vault connections only when you need them.

If you bring your own Azure Key Vault, review these limitations:

- Limit Azure Key Vault connections to one per Foundry resource. Delete an Azure Key Vault connection only if no other connections exist at the Foundry resource or project level.

- Foundry doesn't support secret migration. Remove and recreate connections yourself.
- Deleting the underlying Azure Key Vault breaks the Foundry resource. Azure Key Vault stores secrets for connections that don't use Microsoft Entra ID. Any Foundry feature that depends on those connections stops working.
- Deleting connection secrets that your Foundry resource stores in your bring your own (BYO) Azure Key Vault can break connections to other services.

<!-- ::: zone pivot="ai-foundry-portal" -->

## Use the Foundry (classic) portal

Create a connection to Azure Key Vault in the Foundry (classic) portal.

1. [!INCLUDE [classic-sign-in](../../foundry/includes/classic-sign-in.md)]
1. Select or create your project. 
1. Select **Management center** in the lower left pane. You might need to scroll to find it.

1. Check that there are no connections in the **Resource** or **Project** sections. If connections exist, **Azure Key Vault** isn't available.

1. In the **Resource** section, select **Connected resources**.

1. In the **Connected resources** section, select **+ New connection**.

   :::image type="content" source="../media/setup-key-vault-connection/select-azure-key-vault.jpeg" alt-text="Screenshot of the Connected resources section with the + New connection button selected, showing Azure Key Vault as an available option.":::

1. Select **Azure Key Vault**.

   :::image type="content" source="../media/setup-key-vault-connection/azure-key-vault-connection.jpeg" alt-text="Screenshot of the Azure Key Vault selection dialog with Azure Key Vault selected.":::

1. Select your **Azure Key Vault**, and then select **Connect**.
1. It might take a few minutes after these steps are completed before you can use the connection.

### Verify the connection

After you create the connection, verify that the Key Vault appears in the **Connected resources** list. Select the connection to view its properties and confirm the Key Vault resource ID.

<!-- ::: zone-end -->
<!-- ::: zone pivot="bicep" -->

[!INCLUDE [set-up-key-vault-connection 2](../../foundry/includes/how-to-set-up-key-vault-connection-2.md)]
