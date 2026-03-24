---
title: "Customer-Managed Keys (CMKs) for Microsoft Foundry (classic)"
description: "Learn how to use CMKs for enhanced encryption and data security in Microsoft Foundry. Configure Azure Key Vault integration and meet compliance requirements. (classic)"
ms.author: jburchel 
author: jonburchel 
ms.reviewer: deeikele
ms.date: 03/06/2026
ms.service: azure-ai-services
ms.topic: how-to
ms.custom:
  - classic-and-new
  - ignite-2023
  - build-aifnd
  - build-2025
  - references-regions
ai-usage: ai-assisted 
# Customer intent: As an admin, I want to understand how I can use my own encryption keys with Microsoft Foundry.
ROBOTS: NOINDEX, NOFOLLOW
---

# Customer-managed keys (CMKs) for Microsoft Foundry (classic)

**Currently viewing:** :::image type="icon" source="../../foundry/media/yes-icon.svg" border="false"::: **Foundry (classic) portal version** - [Switch to version for the new Foundry portal](../../foundry/concepts/encryption-keys-portal.md)

> [!TIP]
> An alternate hub-focused article is available: [Customer-managed keys for hub projects](hub-encryption-keys-portal.md).

Customer-managed key (CMK) encryption in [!INCLUDE [classic-link](../../foundry/includes/classic-link.md)] gives you control over encryption of your data. Use CMKs to add an extra protection layer and help meet compliance requirements with Azure Key Vault integration.

Microsoft Foundry provides robust encryption capabilities, including the ability to use CMKs stored in Key Vault to help secure your sensitive data. CMK encryption applies to data at rest stored in the Foundry resource's associated storage accounts, including project artifacts, uploaded files, and evaluation data.

This article explains how to configure CMK encryption by using Key Vault for your Foundry resource.

[!INCLUDE [encryption-keys-portal 1](../../foundry/includes/concepts-encryption-keys-portal-1.md)]
