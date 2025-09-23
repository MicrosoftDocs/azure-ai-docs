---
title: Create and Configure your Storage Account for Evaluations
titleSuffix: Azure AI Foundry
description:  Learn how to create and configure your storage account for Azure AI Foundry evaluations.
ms.service: azure-ai-foundry
ms.topic: how-to
ms.date: 09/22/2025
ms.reviewer: gregharen
ms.author: lagayhar
author: lgayhardt
---

# How to create and configure your storage account for use in Azure AI Foundry Projects

> [!IMPORTANT]
> This guidance only applies to the new Foundry resource based projects, not hub-based projects. These steps aren't required for hub-based projects.

When running evaluations with user provided datasets, users must connect a Storage Account to their Azure AI Foundry Resource. This is the storage account that is used to store these datasets. However, providing this connection isn't enough, the project must also be given contributor access to the blob storage to allow read and write access to the storage account. These instructions walk you through how to create the storage account, connect it to your project, and give resource permission.

## Prerequisites

[!INCLUDE [uses-fdp-only](../includes/uses-fdp-only.md)]

## Create your blob storage account

If you have already created your blob storage account, you can skip this section.  

Azure AI Foundry evaluations use the user's blob storage account to store datasets for use in evaluations. To create the storage account, follow the below steps:

1. Go to your AI Foundry Project and find your resource group. To find your resource group, select the project name in the top right corner and select your resource group. This takes you to the resource group in Azure portal.
1. Select **Create** on the Resource Group page.
1. Search "Storage Account" and select the Storage Account option that is published by Microsoft.

      :::image type="content" source="../media/evaluations/storage/storage-account.png" alt-text="A screenshot showing the Microsoft storage account option." lightbox="../media/evaluations/storage/storage-account.png":::

1. Create your storage account.
    1. *Storage account name*: Give your storage account a meaningful name.
    1. *Region*: Recommendation: Create the storage account in the same region you created your project. To find this, go back to Azure AI Foundry, select the project name in the top right corner of the screen (which is the same option you selected earlier to find the link to your resource group), and review the Location of the resource group. Note: it will not default to the same region.
    1. *Primary service*: Azure Blob Storage or Azure Data Lake Storage Gen 2.
    1. *Performance*: Standard.
    1. *Redundancy*: Geo-redundant storage (GRS).
    1. Select **Review+Create**.
    1. Select **Create**.
1. Your storage account is now created. Allow time for the resource to be fully provisioned, normally 1-2 minutes.

## Connect your blob storage account in Azure AI Foundry

Now that the storage account has been created, it's time to connect the blob storage account to the Azure AI Foundry resource. If you have already completed this step, you can skip to the next section.

1. Navigate to your project at ai.azure.com. Ensure you are in the project you're trying to run evaluations for.
1. In the lower left corner at the bottom of the menu, select **Management Center**.
1. Select **Connected Resources** under "Resource (your resource name here)", NOT Project.
1. Select **New connection**.
1. Select **Storage account**.
     :::image type="content" source="../media/evaluations/storage/add-storage-account.png" alt-text="A screenshot showing the adding a storage account as a new connection to your resource." lightbox="../media/evaluations/storage/add-storage-account.png":::
1. Search for your storage account name that you created.
1. Authentication method: Recommended: Microsoft Entra ID.
1. Select **Add Connection**.
1. The connection is now created. Continue to the next section to provision permissions for Azure AI Foundry resource to the blob storage account.

## Give Azure AI Foundry resource permission to read/write to the storage account

The final step to setting up this storage account to store your datasets for evaluation runs in Azure AI Foundry, you must provide the project permissions to access the storage account. To do so, follow the below steps:

1. Navigate to your project in Azure AI Foundry.
1. In the top left corner, select your project name dropdown.
1. Select the Resource Group link, which will take you to Azure portal for the resource group.
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

You have now provided your project with write access to your blob storage account. After a few minutes, you'll be able to add data during an evaluation in AI Foundry.

## Related content

- [Run evaluations in the cloud](./develop/cloud-evaluation.md)
