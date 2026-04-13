---
title: Include file
description: Include file
author: jonburchel
ms.reviewer: andyaviles
ms.author: jburchel
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 03/20/2026
ms.custom: include
---

If you don't set up a Key Vault connection, Microsoft Foundry stores connection details in a Microsoft-managed Key Vault outside your subscription. To manage your own secrets, connect your Azure Key Vault to Foundry. Before you begin, review the [limitations](#limitations) for Key Vault connections.

Azure Key Vault is a cloud service for securely storing and accessing secrets. A secret is anything that you want to tightly control access to, such as API keys, passwords, certificates, or cryptographic keys. For more information, see [About Azure Key Vault](/azure/key-vault/general/overview).

## Prerequisites

- An Azure subscription.
- A Foundry resource with no existing connections at the resource or project level.
- An Azure Key Vault in your subscription, or permissions to create one.
- One of the following Azure RBAC roles on your Key Vault:
  - [Key Vault Secrets Officer](/azure/role-based-access-control/built-in-roles/security#key-vault-secrets-officer) (minimal permissions)
  - [Key Vault Contributor](/azure/role-based-access-control/built-in-roles/security#key-vault-contributor)
  - [Key Vault Administrator](/azure/role-based-access-control/built-in-roles/security#key-vault-administrator)
