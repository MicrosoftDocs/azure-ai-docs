---
title: "Rate limits, region support, and enterprise features for evaluation"
description: "Learn about region availability, rate limits, virtual network support, and using your own storage account for evaluation in Microsoft Foundry."
author: lgayhardt
ms.author: lagayhar
ms.reviewer: skohlmeier
ms.date: 04/03/2026
ms.topic: concept-article
ms.service: azure-ai-foundry
ai-usage: ai-assisted
ms.custom:
  - references_regions
  - classic-and-new
---

# Rate limits, region support, and enterprise features for evaluation

[!INCLUDE [evaluation-regions-limits-virtual-network 1](../includes/concepts-evaluation-regions-limits-virtual-network-1.md)]

## Bring your own storage

You can use your own storage account to run evaluations.

1. Create and connect your storage account to your Foundry project at the resource level. You can [use a Bicep template](https://github.com/azure-ai-foundry/foundry-samples/blob/main/infrastructure/infrastructure-setup-bicep/01-connections/connection-storage-account.bicep), which provisions and connects a storage account to your Foundry project with key authentication.
1. Make sure the connected storage account has access to all projects.
1. If you connected your storage account by using Microsoft Entra ID, assign the **Storage Blob Data Owner** role to the project's managed identity on your **storage account** resource in the Azure portal.
1. To verify the connection, go to the **Management** section of your Foundry project in the [Foundry portal](https://ai.azure.com). Your storage account appears as a connected resource under **Storage accounts**.

### Troubleshooting

If evaluation runs fail after connecting storage, check the following:

- **Missing managed identity permissions**: Verify the project's managed identity has the **Storage Blob Data Owner** role on the storage account. Missing this role is the most common cause of evaluation failures with custom storage.
- **Network-restricted storage**: If your storage account has a firewall or virtual network rule, add the Foundry project's managed identity as a trusted service, or configure the storage account to allow access from your Foundry project's virtual network.
- **Storage account not visible in projects**: If the connected storage account doesn't appear under all projects, confirm you connected the storage account at the hub (account) level and that the **access to all projects** setting is enabled.

[!INCLUDE [evaluation-regions-limits-virtual-network 2](../includes/concepts-evaluation-regions-limits-virtual-network-2.md)]
