---
title: "Configure Customer-Managed Keys for Microsoft Foundry"
description: "Configure customer-managed key (CMK) encryption for a Microsoft Foundry resource by using Azure Key Vault or Azure Managed HSM with the portal, Bicep, or the Azure CLI."
ms.author: scottpolly 
author: s-polly 
ms.reviewer: deeikele
ms.date: 08/24/2026
ms.service: microsoft-foundry
ms.topic: how-to
ms.custom:
  - classic-and-new
  - ignite-2023
  - build-aifnd
  - build-2025
  - references-regions
  - doc-kit-assisted
ai-usage: ai-assisted 
# Customer intent: As an admin, I want to understand how I can use my own encryption keys with Microsoft Foundry.
---

# Configure customer-managed keys for Microsoft Foundry

This article shows how to configure customer-managed key (CMK) encryption for a [!INCLUDE [foundry-link](../includes/foundry-link.md)] resource by using Azure Key Vault or Azure Managed HSM. CMK encryption applies to data at rest in the Foundry resource's associated storage accounts, including project artifacts, uploaded files, and evaluation data.

To understand what CMK covers across Foundry capabilities and the compute stack before you configure it, see [Customer-managed key encryption in Microsoft Foundry](customer-managed-keys.md).

[!INCLUDE [encryption-keys-portal 1](../includes/concepts-encryption-keys-portal-1.md)]
