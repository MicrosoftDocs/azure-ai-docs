---
title: Create and Configure your Storage Account for Evaluations
titleSuffix: Microsoft Foundry
description:  Learn how to create and configure your storage account for Microsoft Foundry evaluations.
ms.service: azure-ai-foundry
ms.topic: how-to
ms.date: 01/30/2026
ms.reviewer: none
ms.author: lagayhar
author: lgayhardt
ai-usage: ai-assisted
---

# How to create and configure your storage account for use in Microsoft Foundry Projects

[!INCLUDE [classic-banner](../includes/classic-banner.md)]

> [!IMPORTANT]
> This guidance only applies to the new Foundry resource based projects, not hub-based projects.

When you run evaluations by using user-provided datasets, you can connect a storage account to your Microsoft Foundry Resource. Use this storage account to store the datasets. However, providing this connection isn't enough. You must also give the project contributor access to the blob storage to allow read and write access to the storage account. These instructions walk you through how to create the storage account, connect it to your project, and give resource permission.

## Prerequisites

[!INCLUDE [uses-fdp-only](../includes/uses-fdp-only.md)]

## Create your blob storage account

If you have already created your blob storage account, you can skip this section.  

Foundry evaluations use the user's blob storage account to store datasets for use in evaluations. To create the storage account, follow the steps in this section:

1. Go to your Foundry project and find your resource group. To find your resource group, select the project name in the top right corner and select your resource group. This selection takes you to the resource group in Azure portal.
1. Select **Create** on the Resource Group page.
1. Search for "Storage Account" and select the Storage Account option that's published by Microsoft.

      :::image type="content" source="../media/evaluations/storage/storage-account.png" alt-text="A screenshot showing the Microsoft storage account option." lightbox="../media/evaluations/storage/storage-account.png":::

1. Create your storage account.
    1. *Storage account name*: Give your storage account a meaningful name.
    1. *Region*: Recommendation: Create the storage account in the same region you created your project. To find this region, go back to Foundry, select the project name in the top right corner of the screen (which is the same option you selected earlier to find the link to your resource group), and review the Location of the resource group. Note: it doesn't default to the same region.
    1. *Primary service*: Azure Blob Storage or Azure Data Lake Storage Gen 2.
    1. *Performance*: Standard.
    1. *Redundancy*: Geo-redundant storage (GRS).
    1. Select **Review+Create**.
    1. Select **Create**.
1. Your storage account is now created. Allow time for the resource to be fully provisioned, normally 1-2 minutes.

## Connect your blob storage account in Foundry

After you create the storage account, connect the blob storage account to the Foundry resource. If you have already connected the storage account, you can skip this section.

1. Go to your project at ai.azure.com. Make sure you're in the project where you want to run evaluations.
1. In the lower left corner at the bottom of the menu, select **Management Center**.
1. Select **Connected Resources** under "Resource (your resource name here)", NOT Project.
1. Select **New connection**.
1. Select **Storage account**.
     :::image type="content" source="../media/evaluations/storage/add-storage-account.png" alt-text="A screenshot showing the adding a storage account as a new connection to your resource." lightbox="../media/evaluations/storage/add-storage-account.png":::
1. Search for your storage account name that you created.
1. For **Authentication method**, select Microsoft Entra ID.
1. Select **Add Connection**.
1. The connection is created. Continue to the next section to provision permissions for Foundry resource to the blob storage account.

## Give Foundry resource permission to read and write to the storage account

To set up this storage account to store your datasets for evaluation runs in Foundry, you must provide the project permissions to access the storage account.

1. Go to your project in Foundry.
1. In the upper-left corner, select your project name dropdown.
1. Select the **Resource Group** link. This link takes you to Azure portal for the resource group.
1. Select the storage account you created under the *Resources* table.
1. On the right hand side, select **Access Control (IAM)**.
1. Select +Add -> Add role assignment.
    > [!NOTE]
    > If this is disabled, go to **Role assignments** and under *All*, ask an owner to take the next steps.

    :::image type="content" source="../media/evaluations/storage/access-control.png" alt-text="A screenshot of access control in the storage account settings highlighting add role assignment. " lightbox="../media/evaluations/storage/access-control.png":::
1. In the *Job function roles* table, search for "Storage Blob Data Contributor" and select that option. Then select **Next** at the bottom of the screen.
1. In the "Assign access to" option, select **Managed identity**.
1. Select **+ Select members**.
    1. *Subscription*: Your subscription
    1. *Managed identity*: All system-assigned managed identities.
    1. Select: Search for your project name. Select your project, not the resource. It should be formatted [ResourceName]/[ProjectName]. Don't select the resource name, which doesn't have the "/[ProjectName] after it.
    1. Select **Select** button at the bottom.
1. Select **Review + assign** twice.

You now provided your project with write access to your blob storage account. After a few minutes, you can add data during an evaluation in Foundry.

## Related content

- [Run evaluations in the cloud](./develop/cloud-evaluation.md)
